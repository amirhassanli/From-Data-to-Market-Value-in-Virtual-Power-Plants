# -*- coding: utf-8 -*-
"""
ai_agreement.py — multi-agent instrument-stability analysis.

Usage (in Downloads\\DMDI_IntraCoder, after the repeat-coding sheets are
returned and saved, one file per model, e.g.):
    python ai_agreement.py RETURNED_DeepSeek.csv RETURNED_Claude.csv

Accepts one or more returned sheets (template: IntraCoder_ReCode_SHEET.csv,
columns re_order,study,reference,year,doi,B_* (E/P/NR),notes).

Computes
  * per-dimension and overall agreement of the ORIGINAL coding
    (SUBSAMPLE_key.csv, columns A_*) with every returned agent sheet;
  * agent-vs-agent agreement per dimension and overall (if >= 2 agents);
  * a cell-level vote report: cells where an agent departs from the original,
    with a consensus flag (both agents agree with each other against the
    original -> highest adjudication priority);
  * writes agent_kappa_results.csv (long format) and AGREEMENT_RESULTS.txt
    (manuscript-ready numbers, agent-based instrument-stability framing).

Reporting label (PROTOCOL amendments 1-2): agent-based instrument-stability /
repeat-coding consistency stats, NOT human intra-/inter-coder agreement.
"""
import csv, io, math, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.path.join(HERE, "SUBSAMPLE_key.csv")
COLS = ["I", "U", "D", "M", "O", "S", "R", "P"]
NAME = {"I": "Information-set integrity", "U": "Uncertainty integrity",
        "D": "Decision integrity", "M": "Market realism",
        "O": "Out-of-sample validity", "S": "Settlement realism",
        "R": "Reproducibility", "P": "Deployment maturity (companion)"}
TOK = ("E", "P", "NR")
N_RATINGS = 15 * 8


def kappa(a, b):
    n = len(a)
    cats = sorted(set(a) | set(b))
    if n == 0 or len(cats) < 2:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    na = {c: a.count(c) / n for c in cats}
    nb = {c: b.count(c) / n for c in cats}
    pe = sum(na[c] * nb[c] for c in cats)
    if pe >= 1:
        return None
    k = (po - pe) / (1 - pe)
    num = pe + pe ** 2 - sum(na[c] * nb[c] * (na[c] + nb[c]) for c in cats)
    var = num / (n * (1 - pe) ** 2)
    se = math.sqrt(max(var, 0.0))
    return po, k, se, n


def band(k):
    if k is None:
        return "not computable"
    if k < 0:
        return "poor"
    if k <= 0.20:
        return "slight"
    if k <= 0.40:
        return "fair"
    if k <= 0.60:
        return "moderate"
    if k <= 0.80:
        return "substantial"
    return "almost perfect"


def fmt_pair(pair, a, b, out_rows):
    res = kappa(a, b)
    if res is None:
        return None
    po, k, se, n = res
    lo, hi = max(-1.0, k - 1.96 * se), min(1.0, k + 1.96 * se)
    out_rows.append({"pair": pair["label"], "dimension": pair["dim"], "n": n,
                     "po": "%.3f" % po, "kappa": "%.3f" % k,
                     "ci_lo": "%.2f" % lo, "ci_hi": "%.2f" % hi,
                     "band": band(k)})
    return (po, k, lo, hi, band(k))


def label_of(path):
    base = os.path.basename(path)
    for pre in ("RETURNED_",):
        if base.startswith(pre):
            base = base[len(pre):]
    return os.path.splitext(base)[0]


def main(paths):
    with open(KEY, newline="", encoding="utf-8-sig") as f:
        keys = {r["re_order"]: r for r in csv.DictReader(f)}
    assert len(keys) == 15

    agents = {}     # label -> dict re_order -> row (validated)
    for path in paths:
        lab = label_of(path)
        with open(path, newline="", encoding="utf-8-sig") as f:
            back = list(csv.DictReader(f))
        problems = []
        by_order = {}
        for r in back:
            o = r["re_order"].strip()
            if o not in keys or r["study"].strip() != keys[o]["study"]:
                problems.append("bad row re_order/study %r" % o)
                continue
            for c in ("B_" + x for x in COLS):
                v = (r.get(c) or "").strip().upper()
                if v not in TOK:
                    problems.append("row %s %s=%r" % (o, c, v))
            by_order[o] = r
        if problems:
            print("VALIDATION PROBLEMS in %s — fix and re-run:" % lab)
            for p in problems:
                print("  -", p)
            return
        agents[lab] = by_order
        print("agent %s: %d rows validated" % (lab, len(by_order)))
    if not agents:
        print(__doc__)
        return

    labs = list(agents)
    res_rows, ksum = [], {}

    print()
    print("=== agreement with the ORIGINAL coding pass (per dimension) ===")
    for lab in labs:
        print("-- original vs %s" % lab)
        per = []
        for d in COLS:
            a = [keys[o]["A_" + d].strip().upper() for o in sorted(agents[lab])]
            b = [(agents[lab][o].get("B_" + d) or "").strip().upper()
                 for o in sorted(agents[lab])]
            r = fmt_pair({"label": "orig-vs-%s" % lab, "dim": d}, a, b, res_rows)
            tier = 1 if max(a.count(c) for c in set(a)) / len(a) > 0.90 else 0
            po, k, lo, hi, bd = r
            print("   %-2s %-30s kappa %5s (95%% CI %.2f–%.2f) %s%s"
                  % (d, NAME[d], "%.3f" % k, lo, hi, bd,
                     "  [prevalence>90%]" if tier else ""))
            per.append(r[1])
        ksum["orig-vs-%s" % lab] = per

    if len(labs) >= 2:
        print()
        print("=== agent-vs-agent agreement (per dimension) ===")
        per = []
        for d in COLS:
            a = [(agents[labs[0]][o].get("B_" + d) or "").upper()
                 for o in sorted(agents[labs[0]])]
            b = [(agents[labs[1]][o].get("B_" + d) or "").upper()
                 for o in sorted(agents[labs[1]])]
            r = fmt_pair({"label": "%s-vs-%s" % (labs[0], labs[1]), "dim": d},
                         a, b, res_rows)
            po, k, lo, hi, bd = r
            print("   %-2s %-30s kappa %5s (95%% CI %.2f–%.2f) %s"
                  % (d, NAME[d], "%.3f" % k, lo, hi, bd))
            per.append(r[1])
        ksum["%s-vs-%s" % (labs[0], labs[1])] = per

    print()
    for lab_, ks in ksum.items():
        print("mean kappa, %s: %.3f (min %.3f / max %.3f)"
              % (lab_, sum(ks) / len(ks), min(ks), max(ks)))

    # ---------------------------------------------------------------- votes
    print()
    print("=== cell-level departure report (adjudication queue) ===")
    votes = []   # (re_order, study, dim, orig, [(lab, val)...], kind)
    for o in sorted(agents[labs[0]]):
        for d in COLS:
            orig = keys[o]["A_" + d].strip().upper()
            vals = [(lab, agents[lab][o].get("B_" + d, "").strip().upper())
                    for lab in labs]
            deps = [(lab, v) for lab, v in vals if v != orig]
            if not deps:
                continue
            agent_vals = {v for _, v in deps}
            if len(deps) == len(labs) and len(agent_vals) == 1:
                kind = "CONSENSUS-DEVIATION (both agents agree against original)"
            elif len(deps) == len(labs):
                kind = "FULL-DISCORD (agents also disagree with each other)"
            else:
                kind = "single-agent departure"
            votes.append((o, keys[o]["study"], d, orig, deps, kind))
            print("  r%-2s %-36s %s: orig=%-2s %s  %s"
                  % (o, keys[o]["study"], d, orig,
                     ", ".join("%s=%s" % (l, v) for l, v in deps), kind))
    changed = set((o, d) for o, _, d, *_ in votes)
    print("\nchanged cells: %d of %d (%.1f%%)"
          % (len(changed), N_RATINGS, 100.0 * len(changed) / N_RATINGS))

    # ------------------------------------------------------------ outputs
    with open(os.path.join(HERE, "agent_kappa_results.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["pair", "dimension", "n", "po",
                                          "kappa", "ci_lo", "ci_hi", "band"])
        w.writeheader()
        w.writerows(res_rows)
    with open(os.path.join(HERE, "AGREEMENT_RESULTS.txt"), "w",
              encoding="utf-8") as f:
        f.write("instrument-stability check (agent-based repeat-coding),\n"
                "n = 15 of 39 studies (38%), stratified with rare-level enrichment\n")
        f.write("changed cells: %d of %d (%.1f%%)\n"
                % (len(changed), N_RATINGS, 100.0 * len(changed) / N_RATINGS))
        for lab_, ks in ksum.items():
            f.write("pair %s: mean kappa %.3f (min %.3f, max %.3f)\n"
                    % (lab_, sum(ks) / len(ks), min(ks), max(ks)))
        for r in res_rows:
            f.write("%-22s %-2s kappa %.3f (95%% CI %.2f–%.2f), po %.3f, %s\n"
                    % (r["pair"], r["dimension"], float(r["kappa"]),
                       float(r["ci_lo"]), float(r["ci_hi"]), float(r["po"]),
                       r["band"]))
    print("\nwritten: agent_kappa_results.csv | AGREEMENT_RESULTS.txt")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
    else:
        main(sys.argv[1:])


