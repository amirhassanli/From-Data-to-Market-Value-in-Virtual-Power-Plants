# -*- coding: utf-8 -*-
"""
intra_check.py — validate and score the repeat-coding (instrument-stability) sheet.

Usage (after the repeat-coding sheet has been filled and saved here as
RETURNED_IntraCoder_ReCode.csv, or pass its path):
    python intra_check.py [RETURNED_IntraCoder_ReCode.csv]

Steps:
  1. validates the returned sheet (15 rows, order intact, every B_* in E/P/NR)
  2. joins with SUBSAMPLE_key.csv (coder A's original ratings)
  3. per dimension: observed agreement, Cohen's kappa + approx. 95% CI,
     Landis-Koch band, prevalence flag
  4. lists every discrepant cell (for adjudication) and writes
     intra_kappa_results.csv + INTRA_RESULTS.txt (ready for the manuscript)

Reporting label (see PROTOCOL amendment 1): this statistic is agent-based
repeat-coding consistency (instrument stability), NOT intra-coder or
inter-coder agreement by humans.
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


def main(path):
    with open(KEY, newline="", encoding="utf-8-sig") as f:
        keys = {r["re_order"]: r for r in csv.DictReader(f)}
    with open(path, newline="", encoding="utf-8-sig") as f:
        back = list(csv.DictReader(f))

    assert len(keys) == 15, "key sheet corrupted"
    problems = []
    if len(back) != 15:
        problems.append("returned sheet has %d rows (expected 15)" % len(back))
    by_order = {}
    for r in back:
        o = r["re_order"].strip()
        if o not in keys:
            problems.append("unknown re_order %r" % o)
            continue
        if r["study"].strip() != keys[o]["study"]:
            problems.append("row %s: study mismatch (%r vs %r)"
                            % (o, r["study"], keys[o]["study"]))
        for c in ("B_" + x for x in COLS):
            v = (r.get(c) or "").strip().upper()
            if v not in TOK:
                problems.append("row %s %s = %r (must be E, P or NR)" % (o, c, v))
        by_order[o] = r
    if problems:
        print("VALIDATION PROBLEMS — fix and re-run:")
        for p in problems:
            print("  -", p)
        return

    # per-dimension agreement
    res_rows = []
    print("%-3s %-34s %3s %6s %7s %16s  %s"
          % ("dim", "dimension", "n", "agree", "kappa", "95% CI", "band"))
    print("-" * 92)
    for d in COLS:
        a = [keys[o]["A_" + d].strip().upper() for o in sorted(by_order)]
        b = [(by_order[o].get("B_" + d) or "").strip().upper()
             for o in sorted(by_order)]
        res = kappa(a, b)
        if res is None:
            print("%-3s %-34s %3d %6s %7s %16s  %s" % (d, NAME[d], len(a), "-", "-", "-", "-"))
            continue
        po, k, se, n = res
        lo, hi = max(-1.0, k - 1.96 * se), min(1.0, k + 1.96 * se)
        flag = ""
        if max(a.count(c) for c in set(a)) / n > 0.90:
            flag = "  [prevalence: one level >90% — kappa unstable]"
        print("%-3s %-34s %3d %6.3f %7.3f %7.3f to %.2f  %s%s"
              % (d, NAME[d], n, po, k, lo, hi, band(k), flag))
        res_rows.append({"dimension": d, "n": n, "po": "%.3f" % po,
                         "kappa": "%.3f" % k, "ci_lo": "%.2f" % lo,
                         "ci_hi": "%.2f" % hi, "band": band(k),
                         "prevalence_flag": "yes" if flag else "no"})

    ks = [float(r["kappa"]) for r in res_rows]
    print()
    print("mean repeat-pass kappa over %d dimensions (agent-based): %.3f" % (len(ks), sum(ks) / len(ks)))
    print("minimum %.3f (%s)   maximum %.3f (%s)"
          % (min(ks), min(res_rows, key=lambda r: float(r["kappa"]))["dimension"],
             max(ks), max(res_rows, key=lambda r: float(r["kappa"]))["dimension"]))

    # discrepancy listing for adjudication
    print()
    print("=== discrepant cells (adjudicate before finalizing) ===")
    disc = []
    for o in sorted(by_order):
        kx = keys[o]
        for d in COLS:
            av = kx["A_" + d].strip().upper()
            bv = (by_order[o].get("B_" + d) or "").strip().upper()
            if av != bv:
                disc.append((o, kx["study"], d, av, bv,
                             (by_order[o].get("notes") or "").strip()))
                print("  row %-2s %-38s %s: A=%s R=%s %s"
                      % (o, kx["study"], d, av, bv,
                         ("| note: " + disc[-1][5]) if disc[-1][5] else ""))
    if not disc:
        print("  none — perfect temporal stability on the subsample.")

    # persist results
    with open(os.path.join(HERE, "intra_kappa_results.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["dimension", "n", "po", "kappa",
                                          "ci_lo", "ci_hi", "band",
                                          "prevalence_flag"])
        w.writeheader()
        w.writerows(res_rows)
    with open(os.path.join(HERE, "INTRA_RESULTS.txt"), "w", encoding="utf-8") as f:
        f.write("instrument-stability check: agent-based repeat-coding consistency,\n"
                "n = 15 of 39 studies (38%), stratified with rare-level enrichment\n")
        f.write("mean repeat-pass kappa = %.3f\n" % (sum(ks) / len(ks)))
        for r in res_rows:
            f.write("%s: kappa %.3f (95%% CI %.2f–%.2f), observed agreement %.3f, %s%s\n"
                    % (r["dimension"], float(r["kappa"]), float(r["ci_lo"]),
                       float(r["ci_hi"]), float(r["po"]), r["band"],
                       " [prevalence caveat]" if r["prevalence_flag"] == "yes" else ""))
        f.write("\ndiscrepant cells: %d\n" % len(disc))
    print("\nwritten: intra_kappa_results.csv | INTRA_RESULTS.txt")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
    else:
        main(sys.argv[1])
