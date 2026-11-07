#!/usr/bin/env python3
"""
02_dmdi_tables_figures.py
Turns the study-level coding matrix (dmdi_matrix.csv) into every number, table and figure of the paper.

  python 02_dmdi_tables_figures.py --init-template        # writes dmdi_matrix.csv (39 studies, partly pre-filled)
  python 02_dmdi_tables_figures.py                         # validates + builds values + figures
  python 02_dmdi_tables_figures.py --coder2 dmdi_matrix_coder2.csv   # adds inter-coder kappa

Coding values per dimension: E (explicit) / P (partial) / NR (not reported).  Reviews are not coded on I..R.
Outputs: dmdi_values.json, supplementary_S1.csv, fig2_chain.png, fig3_matrix.png, fig4_evidence_map.png, fig5_ladder.png
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd

DIMS = ["I", "U", "D", "M", "O", "S", "R"]
DIM_NAMES = {"I": "Information-set integrity", "U": "Uncertainty integrity", "D": "Decision integrity",
             "M": "Market realism", "O": "Out-of-sample validity", "S": "Settlement realism", "R": "Reproducibility"}
LEVELS = {0: "Conceptual", 1: "Synthetic / assumed data", 2: "Historical or real data (retrospective)",
          3: "Temporal out-of-sample (O = E or P)", 4: "Market-realistic (Level 3 and M = E)",
          5: "Settlement-aware (Level 4 and S = E)", 6: "Pilot / field validation", 7: "Sustained operational deployment"}
COLS = ["key", "ref", "label", "study_type", "year", "data_type", "coding_basis", "verified", "doi", "show",
        "approach"] + DIMS + ["notes"]

# (key, ref, label, type, year, doi, approach, {dim: code})
SEED = [
 ("ruan24", 1, "Ruan et al. 2024", "review", 2024, "10.1016/j.adapen.2024.100170", "", {}),
 ("gao24", 2, "Gao et al. 2024", "review", 2024, "10.1016/j.apenergy.2023.122284", "", {}),
 ("kaiss25", 3, "Kaiss et al. 2025", "review", 2025, "10.1016/j.rser.2024.115242", "", {}),
 ("esfahani25r", 4, "Esfahani et al. 2025 (review)", "review", 2025, "10.1016/j.rser.2025.115929", "", {}),
 ("wang25r", 39, "Wang et al. 2025 (carbon review)", "review", 2025, "10.1016/j.rser.2025.115719", "", {}),
 ("zare26", 5, "Zare et al. 2026", "review", 2026, "10.1016/j.rser.2025.116448", "", {}),
 ("singh26", 49, "Singh et al. 2026", "review", 2026, "10.1109/ACCESS.2026.3691418", "", {}),
 ("wozabal20", 10, "Wozabal & Rameseder 2020", "primary", 2020, "10.1016/j.ejor.2019.07.022", "Multi-stage stochastic; DA + six intraday auctions", dict(I="E", U="E", D="E", O="E", S="P")),
 ("vahedipour20", 11, "Vahedipour-Dahraie et al. 2020", "primary", 2020, "10.1016/j.ijepes.2020.106126", "Stochastic + CVaR, demand response", dict(I="P", U="E", D="E", O="NR")),
 ("sadeghi21", 12, "Sadeghi et al. 2021", "primary", 2021, "10.1016/j.ijepes.2020.106646", "BiLSTM forecasting + DA energy/frequency-regulation bidding", dict(I="E", D="E", O="P")),
 ("sadeghi21b", 13, "Sadeghi Gougheri et al. 2021", "primary", 2021, "10.1016/j.segan.2021.100448", "BiLSTM + energy/spinning-reserve bidding", dict(I="E", D="E", O="P")),
 ("liu22", 14, "Liu 2022", "primary", 2022, "10.1016/j.ijepes.2021.107891", "Carbon-electricity integrated market bidding", dict(S="P", O="NR")),
 ("chen23", 16, "Chen et al. 2023", "primary", 2023, "10.1016/j.jclepro.2023.136690", "", {}),
 ("falabretti23", 17, "Falabretti et al. 2023", "primary", 2023, "", "Stochastic + rolling horizon, e-mobility", dict(I="E", U="E", D="E", O="P")),
 ("yang23", 18, "Yang et al. 2023", "primary", 2023, "10.1016/j.ijepes.2022.108557", "", {}),
 ("fanliu24", 26, "Fan & Liu 2024", "primary", 2024, "10.1049/rpg2.12806", "Wasserstein DRCC, electricity-carbon market", dict(I="E", U="E", D="E", O="NR", S="E")),
 ("liu24", 21, "Liu et al. 2024", "primary", 2024, "10.1016/j.ijepes.2024.110325", "Cooperative game, electricity-carbon joint market", dict(S="P", O="NR")),
 ("wang24pv", 20, "Wang et al. 2024 (PV forecast)", "primary", 2024, "10.1016/j.apenergy.2024.123890", "Adversarial GNN, data-scarce PV forecasting", dict(I="E", D="P", O="NR")),
 ("mei24", 19, "Mei et al. 2024", "primary", 2024, "", "", {}),
 ("xu24", 24, "Xu et al. 2024", "primary", 2024, "10.1016/j.apenergy.2024.123985", "Model-assisted MARL, three-stage scheduling", dict(I="P", D="E", O="NR")),
 ("wu24", 25, "Wu et al. 2024", "primary", 2024, "10.1016/j.apenergy.2024.123998", "Adaptive MARL, multi-energy buildings", dict(I="P", D="E", O="NR")),
 ("li24", 23, "Li 2024", "primary", 2024, "10.1016/j.epsr.2024.111015", "Multi-stage semi-anticipative DRO", dict(I="E", U="E", D="E", O="NR")),
 ("kimchoi24", 8, "Kim & Choi 2024", "primary", 2024, "10.1016/j.ejor.2024.03.001", "Sample-robust bidding, real business data", dict(I="E", U="E", D="E", O="E", S="P")),
 ("nadimi25a", 30, "Nadimi & Goto 2025a", "primary", 2025, "10.1016/j.renene.2024.121875", "Forecast correction, day-ahead to balancing", dict(I="E", D="E", O="P")),
 ("nadimi25b", 31, "Nadimi & Goto 2025b", "primary", 2025, "10.1016/j.apenergy.2025.125273", "DSS-BiLSTM, 38-h day-ahead forecast", dict(I="E", D="P", O="P")),
 ("li25c", 27, "Li et al. 2025 (coordinated DRO)", "primary", 2025, "10.1016/j.apenergy.2025.125514", "", {}),
 ("ma25", 28, "Ma et al. 2025", "primary", 2025, "10.1016/j.apenergy.2025.125366", "Data-driven interval robust, spot market", dict(I="E", U="E", D="E", O="NR")),
 ("song25a", 29, "Song et al. 2025a", "primary", 2025, "10.1016/j.epsr.2025.111977", "DRO with discrete price/wind scenarios", dict(I="E", U="E", D="E", O="NR")),
 ("song25b", 37, "Song et al. 2025b", "primary", 2025, "10.3390/en18061383", "Pay-as-bid / pay-as-clear with imbalance penalties", dict(S="E", O="NR")),
 ("choi25", 38, "Choi et al. 2025", "primary", 2025, "10.1016/j.apenergy.2025.126264", "DER combination optimisation, wholesale markets", dict(S="E", O="NR")),
 ("bian26", 32, "Bian et al. 2026", "primary", 2026, "10.1016/j.ijepes.2025.111555", "CVaR bi-level, energy-regulation-carbon markets", dict(I="E", U="E", D="E", O="NR", S="P")),
 ("esfahani24", 42, "Esfahani et al. 2024", "primary", 2024, "10.1016/j.apenergy.2024.122883", "", {}),
 ("li25h", 43, "Li et al. 2025 (hierarchical DRL)", "primary", 2025, "10.1016/j.apenergy.2025.125333", "", {}),
 ("siqin25", 44, "Siqin et al. 2025", "primary", 2025, "10.1016/j.energy.2025.137455", "", {}),
 ("wang25rk", 45, "Singh et al. 2025 (risk-aware)", "primary", 2025, "10.1016/j.egyr.2025.07.032", "", {}),
 ("jin26", 46, "Jin et al. 2026", "primary", 2026, "10.1007/s40747-025-02176-1", "", {}),
 ("xie26", 47, "Xie et al. 2026", "primary", 2026, "10.1038/s41598-025-33726-9", "", {}),
 ("wang22drl", 15, "Wang et al. 2022 (DRL/EV)", "primary", 2022, "10.1016/j.epsr.2021.107714", "", {}),
 ("closedloop25", 48, "Closed-loop forecasting/bidding 2025", "primary", 2025, "10.3390/en18246486", "", {}),
]
UNVERIFIED = {15, 48}


def init_template(path):
    rows = []
    for key, ref, label, typ, yr, doi, appr, codes in SEED:
        r = {c: "" for c in COLS}
        r.update(key=key, ref=ref, label=label, study_type=typ, year=yr, doi=doi, approach=appr,
                 verified="FALSE" if ref in UNVERIFIED else "TRUE", show="1" if appr else "0",
                 coding_basis="", data_type="", notes="")
        r.update(codes)
        if ref in UNVERIFIED:
            r["notes"] = "Not confirmed in any bibliographic source; excluded until the DOI is found in Scopus/WoS."
        rows.append(r)
    pd.DataFrame(rows, columns=COLS).to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Template written: {path}\nFill the blank I..R cells, data_type "
          "(conceptual|synthetic|historical|pilot|operational) and coding_basis (fulltext|abstract).")


def load(path):
    df = pd.read_csv(path, dtype=str).fillna("")
    for d in DIMS:
        df[d] = df[d].str.strip().str.upper()
    if "verified" not in df.columns:
        df["verified"] = "TRUE"
    df["verified"] = df["verified"].replace("", "TRUE").str.upper()
    return df


def validate(df):
    errs = []
    core = df[df.verified != "FALSE"]
    for _, r in core[core.study_type == "primary"].iterrows():
        for d in DIMS:
            if r[d] not in ("E", "P", "NR"):
                errs.append(f"{r['label']}: dimension {d} is '{r[d]}' (must be E, P or NR)")
        if r["data_type"] not in ("conceptual", "synthetic", "historical", "pilot", "operational"):
            errs.append(f"{r['label']}: data_type '{r['data_type']}' invalid")
        if r["coding_basis"] not in ("fulltext", "abstract"):
            errs.append(f"{r['label']}: coding_basis '{r['coding_basis']}' invalid")
    return errs


def level(r):
    dt = r["data_type"]
    if dt == "operational": return 7
    if dt == "pilot": return 6
    if dt == "conceptual": return 0
    if dt == "synthetic": return 1
    lv = 2
    if r["O"] in ("E", "P"): lv = 3
    if lv == 3 and r["M"] == "E": lv = 4
    if lv == 4 and r["S"] == "E": lv = 5
    return lv


def wkappa(a, b):
    cats = {"NR": 0, "P": 1, "E": 2}
    a = np.array([cats[x] for x in a]); b = np.array([cats[x] for x in b])
    k = 3
    w = np.abs(np.subtract.outer(np.arange(k), np.arange(k))) / (k - 1)
    obs = np.zeros((k, k))
    for i, j in zip(a, b): obs[i, j] += 1
    obs /= obs.sum()
    exp = np.outer(obs.sum(1), obs.sum(0))
    den = (w * exp).sum()
    return float("nan") if den == 0 else 1 - (w * obs).sum() / den


def figs(core_p, out, cnt):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from matplotlib.patches import FancyBboxPatch
    # Fig 2: chain
    steps = ["Information", "Forecast", "Uncertainty", "Decision", "Bid", "Clearing", "Dispatch", "Deviation",
             "Settlement", "Realized value"]
    fig, ax = plt.subplots(figsize=(7.2, 1.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 1)
    for i, s in enumerate(steps):
        x = 0.05 + i * 0.99
        ax.add_patch(FancyBboxPatch((x, 0.25), 0.85, 0.5, boxstyle="round,pad=0.02", fc="#eaf1fb", ec="#27496d"))
        ax.text(x + 0.425, 0.5, f"{i + 1}\n{s}", ha="center", va="center", fontsize=6.3)
        if i < len(steps) - 1: ax.annotate("", xy=(x + 0.97, 0.5), xytext=(x + 0.86, 0.5), arrowprops=dict(arrowstyle="->"))
    fig.savefig(out / "fig2_chain.png", dpi=300, bbox_inches="tight"); plt.close(fig)
    # Fig 3: matrix (primary studies)
    code = {"NR": 0, "P": 1, "E": 2}
    M = np.array([[code[r[d]] for d in DIMS] for _, r in core_p.iterrows()])
    fig, ax = plt.subplots(figsize=(4.2, 0.22 * len(core_p) + 1.2))
    ax.imshow(M, cmap=ListedColormap(["#440154", "#21908d", "#fde725"]), vmin=0, vmax=2, aspect="auto")
    ax.set_xticks(range(len(DIMS))); ax.set_xticklabels(DIMS)
    ax.set_yticks(range(len(core_p))); ax.set_yticklabels(core_p["label"], fontsize=6)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, ["NR", "P", "E"][M[i, j]], ha="center", va="center", fontsize=5.5,
                    color="white" if M[i, j] < 2 else "black")
    ax.set_xlabel("DMDI dimension (E explicit, P partial, NR not reported)", fontsize=7)
    fig.savefig(out / "fig3_matrix.png", dpi=300, bbox_inches="tight"); plt.close(fig)
    # Fig 4: evidence map
    rng = np.random.default_rng(7)
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    pos = {"NR": 0, "P": 1, "E": 2}
    for _, r in core_p.iterrows():
        x = pos[r["O"]] + rng.uniform(-.12, .12); y = pos[r["S"]] + rng.uniform(-.12, .12)
        ax.scatter(x, y, s=22, color="#27496d", alpha=.8)
        if r["O"] == "E" or r["S"] == "E":
            ax.annotate(r["label"], (x, y), fontsize=5.5, xytext=(3, 3), textcoords="offset points")
    ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["NR", "Partial", "Explicit"])
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(["NR", "Partial", "Explicit"])
    ax.set_xlabel("Out-of-sample validity (O)"); ax.set_ylabel("Settlement realism (S)")
    ax.grid(alpha=.25); fig.savefig(out / "fig4_evidence_map.png", dpi=300, bbox_inches="tight"); plt.close(fig)
    # Fig 5: maturity ladder
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.bar([f"L{k}" for k in LEVELS], [cnt.get(k, 0) for k in LEVELS], color="#27496d")
    ax.set_ylabel("Primary studies"); ax.set_xlabel("Data-to-Market Maturity Ladder level")
    fig.savefig(out / "fig5_ladder.png", dpi=300, bbox_inches="tight"); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", default="dmdi_matrix.csv")
    ap.add_argument("--coder2", default=None)
    ap.add_argument("--init-template", action="store_true")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    if a.init_template:
        init_template(a.matrix); return
    out = Path(a.out); out.mkdir(exist_ok=True)
    df = load(a.matrix)
    errs = validate(df)
    if errs:
        print("MATRIX NOT COMPLETE:"); [print(" -", e) for e in errs]; sys.exit(1)
    core = df[df.verified != "FALSE"].copy()
    prim = core[core.study_type == "primary"].copy()
    rev = core[core.study_type == "review"]
    n = len(prim)
    v = {"N_CORE": len(core), "N_PRIM": n, "N_REV": len(rev), "N_UNVERIFIED_EXCLUDED": int((df.verified == "FALSE").sum()),
         "N_FULLTEXT": int((prim.coding_basis == "fulltext").sum())}
    tab = ["| DMDI dimension | Explicit | Partial | Not reported |", "|---|---|---|---|"]
    for d in DIMS:
        e, p, nr = [(prim[d] == c).sum() for c in ("E", "P", "NR")]
        v.update({f"{d}_E": int(e), f"{d}_P": int(p), f"{d}_N": int(nr)})
        tab.append(f"| {d}: {DIM_NAMES[d]} | {e} ({100*e/n:.0f}%) | {p} ({100*p/n:.0f}%) | {nr} ({100*nr/n:.0f}%) |")
    v["TABLE_COVERAGE"] = "\n".join(tab)
    v["PCT_D_E"] = f"{100*v['D_E']/n:.0f}"; v["PCT_M_E"] = f"{100*v['M_E']/n:.0f}"
    prim["level"] = prim.apply(level, axis=1)
    cnt = prim["level"].value_counts().to_dict()
    lt = ["| Level | Evidence type | Primary studies |", "|---|---|---|"]
    for k, nm in LEVELS.items():
        v[f"L{k}"] = int(cnt.get(k, 0)); lt.append(f"| {k} | {nm} | {v[f'L{k}']} |")
    lt.append(f"| – | Review articles (not placed on the ladder) | {len(rev)} |")
    v["TABLE_LADDER"] = "\n".join(lt)
    v["N_LE2"] = int(sum(cnt.get(k, 0) for k in (0, 1, 2))); v["PCT_LE2"] = f"{100*v['N_LE2']/n:.0f}"
    v["N_L5PLUS"] = int(sum(cnt.get(k, 0) for k in (5, 6, 7)))
    # representative table
    sh = prim[prim["show"] == "1"].sort_values("year")
    rt = ["| Study | Approach | I | U | D | M | O | S |", "|---|---|---|---|---|---|---|---|"]
    for _, r in sh.iterrows():
        rt.append(f"| {r['label']} [{r['ref']}] | {r['approach']} | " + " | ".join(r[d] for d in "IUDMOS") + " |")
    v["TABLE_REPRESENTATIVE"] = "\n".join(rt)
    # kappa
    if a.coder2:
        c2 = load(a.coder2).set_index("key")
        both = prim[prim["key"].isin(c2.index)]
        v["N_DOUBLE"] = len(both)
        ks, allA, allB = {}, [], []
        for d in DIMS:
            x, y = both[d].tolist(), [c2.loc[k, d] for k in both["key"]]
            ks[d] = wkappa(x, y); allA += x; allB += y
        v["KAPPA"] = f"{wkappa(allA, allB):.2f}"
        v["KAPPA_RANGE"] = f"{np.nanmin(list(ks.values())):.2f}-{np.nanmax(list(ks.values())):.2f}"
        v["KAPPA_BY_DIM"] = {k: (None if np.isnan(x) else round(x, 2)) for k, x in ks.items()}
    prim.drop(columns=[]).to_csv(out / "supplementary_S1.csv", index=False, encoding="utf-8-sig")
    figs(prim, out, cnt)
    (out / "dmdi_values.json").write_text(json.dumps(v, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: x for k, x in v.items() if not k.startswith("TABLE")}, indent=2, default=str))


if __name__ == "__main__":
    main()
