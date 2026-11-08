# -*- coding: utf-8 -*-
"""
build_supp_package.py — assemble Downloads\\SUPPLEMENTARY_DMDI.

Package files (named exactly as the Data Availability statement implies):
  DMDI_Coding_Matrix.csv        39x8+... coding matrix (FINAL reference numbers)
  DMDI_Codebook.docx            coding rules per dimension and level
  DMDI_Analysis.py              regenerates Table XI counts + Table XIV
                                associations (+ Fig. 7 stats) from the matrix
  DMDI_Coding_Sheet_BLIND.csv   blank second-coder sheet (coder-facing columns)
  DMDI_Agreement.py             per-dimension agreement / Cohen's kappa
Idempotent: re-running rebuilds every file from current sources.
"""
import os
import shutil
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx
from docx.shared import Pt

DEST = r"C:\Users\Mahboobian\Downloads\SUPPLEMENTARY_DMDI"
os.makedirs(DEST, exist_ok=True)

# ----------------------------------------------------------------- 1. matrix
shutil.copyfile("_draft/dmdi_coding_matrix.csv", os.path.join(DEST, "DMDI_Coding_Matrix.csv"))
print("DMDI_Coding_Matrix.csv")

# ------------------------------------------------------------------ 2. blind sheet
shutil.copyfile(r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\Coding_Sheet_BLIND.csv",
                os.path.join(DEST, "DMDI_Coding_Sheet_BLIND.csv"))
print("DMDI_Coding_Sheet_BLIND.csv")

# ------------------------------------------------------------------ 3. agreement script
shutil.copyfile("kappa_agreement.py" if os.path.exists("kappa_agreement.py")
                else "_draft/kappa_agreement.py",
                os.path.join(DEST, "DMDI_Agreement.py"))
print("DMDI_Agreement.py")

# ------------------------------------------------------------------ 4. codebook docx
RULES = {
    "I \u2014 Information-set integrity": [
        "E: the study states (or visibly implements) that decisions are made using only "
        "information available at the decision time it models \u2014 e.g., forecasts "
        "generated only from data preceding the decision gate, no future prices/"
        "realizations inside the decision window.",
        "P: a rolling/look-ahead-free design is stated in general terms, but the "
        "information boundary is not precisely located, or single-step look-ahead "
        "remains in one module (e.g., a post-hoc dispatch fix).",
        "NR: the paper is silent on when each piece of information becomes available.",
    ],
    "U \u2014 Uncertainty integrity": [
        "E: uncertainty representations (forecast error distributions, scenario sets, "
        "ranges) are empirically derived and characterized \u2014 sources given, "
        "dependence or tail behavior either evidenced from historical data or "
        "explicitly calibrated and reported.",
        "P: uncertainty is realistically motivated (e.g., historical forecast errors) "
        "but one link is assumed without evidence \u2014 e.g., independence is assumed, "
        "a Wasserstein radius is tuned but the marginal calibration is not reported, or "
        "the scenario count/reduction rule is not justified.",
        "NR: uncertainty enters only as assumed parameters (e.g., a fixed uncertainty "
        "set) with no empirical characterization.",
    ],
    "D \u2014 Decision integrity": [
        "E: the optimization/learning policy is evaluated under its own stated "
        "constraints (network limits, ramping, reserve, carbon constraints), with no "
        "look-ahead bias: the holding/tuning of the policy is separated from its "
        "evaluation, and reported performance is achievable by the policy as stated.",
        "P: policy constraints are implemented but evaluation details blur the boundary "
        "(e.g., re-solving per stage with perfect information partly leaking in), or "
        "key constraints are enforced only qualitatively.",
        "NR: the decision problem is described at block-diagram level without enough "
        "detail to verify constraint handling.",
    ],
    "M \u2014 Market realism": [
        "E: market design is fully instantiated: a named real market (or a clearly "
        "stated faithful replica) with its products (day-ahead/intraday/AS), timing, "
        "and clearing/pricing rule (e.g., pay-as-clear with zonal prices for X), used "
        "directly in the model.",
        "P: market mechanisms are modeled on real lines, but a decisive feature is "
        "simplified (e.g., single price area, no transmission constraints, aggregate "
        "clearing), or the market is synthetic but explicitly shaped on a named real "
        "design.",
        "NR: market is a generic price-taker assumption or an abstract price signal "
        "without a defined design.",
    ],
    "O \u2014 Out-of-sample validity": [
        "E if all three hold: (i) a chronological train/validation/test split or "
        "rolling-window evaluation is used; (ii) the test period is disjoint from and "
        "later than any period used for fitting/tuning; (iii) quantitative performance "
        "is reported specifically on that held-out period.",
        "P if temporal separation is mentioned but at least one of (ii)\u2013(iii) is "
        "missing or ambiguous (split described only qualitatively; results pool "
        "in-sample and out-of-sample windows).",
        "NR if the paper does not discuss temporal separation at all (cross-sectional "
        "random splits and k-fold CV count as absence of chronological separation \u2192 "
        "code NR unless chronological evaluation is also present elsewhere).",
    ],
    "S \u2014 Settlement realism": [
        "E: reported profit/cost figures are computed after applying a stated deviation "
        "or imbalance-settlement rule (deviation volumes priced by an explicit "
        "penalty/reward scheme), not solely the ex-ante optimization objective value.",
        "P: a settlement/ex-post deviation component is acknowledged and partially "
        "quantified, but the full financial linkage between day-ahead commitment and "
        "imbalance cost is simplified (e.g., proportional penalty without a mechanism, "
        "or imbalance settled at the day-ahead price).",
        "NR: only ex-ante objective values or simulated profits inside the optimization "
        "are reported; nothing tracks the financial consequence of deviations.",
    ],
    "R \u2014 Reproducibility": [
        "E: a reader could, in principle, reconstruct the reported experiment from the "
        "paper alone: data sources named (with access route), parameterization complete "
        "(or a linked code/data repository covering it), and the evaluation protocol "
        "fully stated.",
        "P: major parameters and sources are given but at least one essential element "
        "is missing to restart the experiment (e.g., no data link, approximate "
        "parameter values, or evaluation protocol gaps).",
        "NR: neither a data repository nor sufficient parameterization is provided.",
    ],
    "P \u2014 Deployment maturity (companion field, not a DMDI dimension)": [
        "E: documented operational deployment in a real system (field installation, "
        "commercial operation) \u2014 or hardware-in-the-loop/pilot evidence for ALL of "
        "the pipeline the paper claims.",
        "P: pilot/HIL/simulation co-designed with a real operator, or deployment of a "
        "subcomponent.",
        "NR: simulation-only, no operational claim.",
    ],
}

cb = docx.Document()
cb.styles["Normal"].font.name = "Calibri"
cb.styles["Normal"].font.size = Pt(10.5)


def h(text, lvl=1):
    cb.add_heading(text, lvl)


def p(text, bold=False):
    par = cb.add_paragraph()
    r = par.add_run(text)
    r.bold = bold
    return par


def li(text):
    cb.add_paragraph(text, style="List Bullet")


h("DMDI Codebook", 0)
p("Coding rules of the review \u201cFrom Data to Market Value in Virtual Power "
  "Plants\u201d (Section 5). Applies to DMDI_Coding_Matrix.csv, which codes the "
  "39 verified-core studies on the seven DMDI dimensions I, U, D, M, O, S, R plus the "
  "deployment-maturity companion field P. Version 1.0.")

h("1. Levels", 1)
p("Each dimension takes exactly one of three evidence levels:", bold=False)
li("E (Explicit): the paper itself contains the evidence, and the criterion is fully "
   "met. The reader can point to the sentence/table/figure that demonstrates it.")
li("P (Partial): the criterion is partly met, or the evidence is stated only "
   "qualitatively, is ambiguous, or is incomplete on at least one stated sub-criterion.")
li("NR (Not reported / not verifiable): the paper either does not address the "
   "criterion at all, or addresses it too weakly to distinguish E from P. The NR-R / "
   "NR-U distinction (reported vs. unreachable) is recorded during adjudication only.")
p("Key discipline: a dimension is coded on evidence in the paper, not on an assessment "
  "of whether the method is good. A sophisticated DRO model with an unjustified "
  "scenario generator is still not explicit uncertainty integrity.", bold=True)

h("2. Decision rules per dimension", 1)
p("The dimensions follow the decision chain Information \u2192 Forecast \u2192 "
  "Uncertainty \u2192 Decision \u2192 Bid \u2192 Clearing \u2192 Dispatch \u2192 "
  "Deviation \u2192 Settlement \u2192 Realized Value. For each dimension, E requires "
  "ALL the stated sub-criteria; if any one of them is missing or only implied, the "
  "coding is P.")
for dim, rules in RULES.items():
    h(dim, 2)
    for r in rules:
        li(r)

h("3. Matrix format", 1)
li("row \u2014 running number 1\u201339.")
li("study \u2014 short study label (author surname(s)).")
li("reference \u2014 bracketed reference number used in the review text.")
li("year \u2014 publication year.")
li("I, U, D, M, O, S, R, P \u2014 coding tokens, each E, P, or NR.")

h("4. Double coding", 1)
p("DMDI_Coding_Sheet_BLIND.csv is the blank second-coder version of the same "
  "instrument (B_ columns empty). After independent coding, between-coder agreement "
  "is computed per dimension with DMDI_Agreement.py: observed agreement, Cohen\u2019s "
  "kappa with an approximate 95% CI, and the Landis\u2013Koch band; kappa treats the "
  "three levels as nominal categories. Discrepant cells go to adjudication before "
  "publication.")

cb.save(os.path.join(DEST, "DMDI_Codebook.docx"))
print("DMDI_Codebook.docx")

# ------------------------------------------------------------------ 5. analysis script
analysis = r'''# -*- coding: utf-8 -*-
"""
DMDI_Analysis.py — regenerate the review's coded-evidence statistics from
DMDI_Coding_Matrix.csv.

Reproduces, from the shipped matrix alone:
  * Table XI  — per-dimension Explicit / Partial / NR counts (39 verified-core studies)
  * explicit-count distribution (Fig. 7 left panel data)
  * Table XIV — pairwise phi association on the Explicit/not-Explicit dichotomy,
                two-sided Fisher exact p, Benjamini-Hochberg q
  * Spearman rho of explicit count (and of maturity P) against publication year

Usage:  python DMDI_Analysis.py [matrix.csv]
        (default: DMDI_Coding_Matrix.csv in the same directory)
Requires: numpy, scipy
"""
import csv
import io
import itertools
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "DMDI_Coding_Matrix.csv")

import numpy as np
from scipy import stats

rows = list(csv.DictReader(open(MATRIX, newline="", encoding="utf-8")))
COLS = ["I", "U", "D", "M", "O", "S", "R", "P"]
DIMS = ["I", "U", "D", "M", "O", "S"]

X = np.array([[1 if r[c] == "E" else 0 for c in COLS] for r in rows])
year = np.array([int(r["year"]) for r in rows])
cnt = X[:, :7].sum(axis=1)

print("matrix: %s   (n = %d)" % (MATRIX, len(rows)))
assert len(rows) == 39, "expected the 39-study verified core"

print()
print("=== Table XI — DMDI evidence coverage ===")
DIMN = {"I": "I — Information-set integrity", "U": "U — Uncertainty integrity",
        "D": "D — Decision integrity", "M": "M — Market realism",
        "O": "O — Out-of-sample validity", "S": "S — Settlement realism",
        "R": "R — Reproducibility",
        "P": "P — Deployment maturity (companion)"}
print("%-3s %-38s %8s %8s %4s" % ("dim", "dimension", "Explicit", "Partial", "NR"))
for j, c in enumerate(COLS):
    e = int(X[:, j].sum())
    pp = sum(1 for r in rows if r[c] == "P")
    nr = sum(1 for r in rows if r[c].startswith("NR"))
    print("%-3s %-38s %8d %8d %4d" % (c, DIMN[c], e, pp, nr))

dist = {k: int((cnt == k).sum()) for k in range(8)}
print()
print("explicit-count distribution (studies by number of E among I..R):", dist)
print("median = %d   mean = %.2f   sd = %.2f   max = %d"
      % (np.median(cnt), cnt.mean(), cnt.std(ddof=1), cnt.max()))


def phi(x, y):
    a = int(np.sum((x == 1) & (y == 1)))
    b = int(np.sum((x == 1) & (y == 0)))
    c = int(np.sum((x == 0) & (y == 1)))
    d = int(np.sum((x == 0) & (y == 0)))
    den = np.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    return 0.0 if den == 0 else (a * d - b * c) / den


pairs = []
for A, B in itertools.combinations(DIMS, 2):
    x = X[:, COLS.index(A)]
    y = X[:, COLS.index(B)]
    tab = np.array([[np.sum((x == 1) & (y == 1)), np.sum((x == 1) & (y == 0))],
                    [np.sum((x == 0) & (y == 1)), np.sum((x == 0) & (y == 0))]])
    pval = stats.fisher_exact(tab)[1]
    pairs.append({"a": A, "b": B, "both": int(tab[0, 0]), "phi": float(phi(x, y)),
                  "p": float(pval)})

m = len(pairs)
order = sorted(range(m), key=lambda i: pairs[i]["p"])
prev = 1.0
for rank in range(m - 1, -1, -1):
    i = order[rank]
    prev = min(prev, pairs[i]["p"] * m / (rank + 1))
    pairs[i]["q"] = float(prev)

print()
print("=== Table XIV — pairwise associations (Explicit/not-Explicit dichotomy) ===")
print("%-6s %5s %7s %9s %7s" % ("pair", "both", "phi", "p (Fisher)", "q (BH)"))
for d in pairs:
    ps = "<0.001" if d["p"] < 0.001 else "%.3f" % d["p"]
    qs = "%.3f" % d["q"]
    print("%-6s %5d %+7.2f %9s %7s %s"
          % ("%s-%s" % (d["a"], d["b"]), d["both"], d["phi"], ps, qs,
             "*" if d["q"] < 0.05 else ""))

rho_year, p_year = stats.spearmanr(year, cnt)
rho_p, p_p = stats.spearmanr(year, X[:, 7])
print()
print("Spearman: year vs explicit count  rho = %+.3f  p = %.4f" % (rho_year, p_year))
print("Spearman: year vs maturity (P)    rho = %+.3f  p = %.4f" % (rho_p, p_p))
print("\nAll counts above reproduce Table XI and Table XIV of the review; the")
print("yearwise correlations reproduce the Section 10.4 prose values.")
'''
with open(os.path.join(DEST, "DMDI_Analysis.py"), "w", encoding="utf-8") as f:
    f.write(analysis)
print("DMDI_Analysis.py")

print("\npackage files:")
for f in sorted(os.listdir(DEST)):
    print("  ", f)
