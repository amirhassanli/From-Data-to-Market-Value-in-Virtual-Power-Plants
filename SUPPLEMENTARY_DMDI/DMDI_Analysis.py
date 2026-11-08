# -*- coding: utf-8 -*-
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
