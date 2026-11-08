# -*- coding: utf-8 -*-
"""
Phase 2 statistics: joint structure of the 39 x 8 DMDI coding matrix.

Writes _draft/phase2_stats.json, which is the single source for
  - Table XIV  (pairwise associations)
  - Fig. 7     (explicit-count distribution and phi matrix)
  - the prose in Section 10.4
"""
import csv
import itertools
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import numpy as np
from scipy import stats

rows = list(csv.DictReader(open("_draft/dmdi_coding_matrix.csv", newline="", encoding="utf-8")))
COLS = ["I", "U", "D", "M", "O", "S", "R", "P"]
DIMS = ["I", "U", "D", "M", "O", "S"]

X = np.array([[1 if r[c] == "E" else 0 for c in COLS] for r in rows])
year = np.array([int(r["year"]) for r in rows])
ref = [r["reference"] for r in rows]
cnt = X[:, :7].sum(axis=1)


def phi(x, y):
    a = np.sum((x == 1) & (y == 1))
    b = np.sum((x == 1) & (y == 0))
    c = np.sum((x == 0) & (y == 1))
    d = np.sum((x == 0) & (y == 0))
    den = np.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    return 0.0 if den == 0 else (a * d - b * c) / den


pairs = []
for A, B in itertools.combinations(DIMS, 2):
    x = X[:, COLS.index(A)]
    y = X[:, COLS.index(B)]
    tab = np.array([[np.sum((x == 1) & (y == 1)), np.sum((x == 1) & (y == 0))],
                    [np.sum((x == 0) & (y == 1)), np.sum((x == 0) & (y == 0))]])
    p = stats.fisher_exact(tab)[1]
    pairs.append({"a": A, "b": B, "both": int(tab[0, 0]), "phi": float(phi(x, y)),
                  "p": float(p)})

# Benjamini-Hochberg
m = len(pairs)
order = sorted(range(m), key=lambda i: pairs[i]["p"])
prev = 1.0
for rank in range(m - 1, -1, -1):
    i = order[rank]
    prev = min(prev, pairs[i]["p"] * m / (rank + 1))
    pairs[i]["q"] = float(prev)

phi_mat = np.eye(len(DIMS))
for i, A in enumerate(DIMS):
    for j, B in enumerate(DIMS):
        if i == j:
            continue
        phi_mat[i, j] = phi(X[:, COLS.index(A)], X[:, COLS.index(B)])

rho_year, p_year = stats.spearmanr(year, cnt)
rho_p, p_p = stats.spearmanr(year, X[:, 7])

per_dim = {c: {"explicit": int(X[:, j].sum()),
               "partial": int(sum(1 for r in rows if r[c] == "P")),
               "nr": int(sum(1 for r in rows if r[c] == "NR"))}
           for j, c in enumerate(COLS)}

out = {
    "n": len(rows),
    "dims": DIMS,
    "per_dim": per_dim,
    "explicit_count_dist": {str(k): int((cnt == k).sum()) for k in range(8)},
    "count_median": float(np.median(cnt)),
    "count_mean": float(cnt.mean()),
    "count_sd": float(cnt.std(ddof=1)),
    "count_max": int(cnt.max()),
    "zero_studies": [ref[i] for i in np.where(cnt == 0)[0]],
    "max_studies": [ref[i] for i in np.where(cnt == cnt.max())[0]],
    "pairs": pairs,
    "phi_mat": phi_mat.tolist(),
    "year_rho": float(rho_year), "year_p": float(p_year),
    "maturity_rho": float(rho_p), "maturity_p": float(p_p),
    "o_explicit": [ref[i] for i in np.where(X[:, COLS.index("O")] == 1)[0]],
    "s_explicit": [ref[i] for i in np.where(X[:, COLS.index("S")] == 1)[0]],
    "o_s_overlap": sorted(set(np.where(X[:, COLS.index("O")] == 1)[0]) &
                          set(np.where(X[:, COLS.index("S")] == 1)[0])),
}

json.dump(out, open("_draft/phase2_stats.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("n =", out["n"])
print("explicit-count distribution:", out["explicit_count_dist"])
print("max explicit =", out["count_max"], " achieved by", out["max_studies"])
print("zero explicit =", out["zero_studies"])
print("O explicit:", out["o_explicit"], " S explicit:", out["s_explicit"],
      " overlap:", out["o_s_overlap"])
print("year rho=%.3f p=%.4f | maturity rho=%.3f p=%.4f"
      % (out["year_rho"], out["year_p"], out["maturity_rho"], out["maturity_p"]))
print()
print("%-6s %5s %6s %7s %7s" % ("pair", "both", "phi", "p", "q"))
for d in pairs:
    print("  %s-%s   %4d %6.3f %7.3f %7.3f %s" % (d["a"], d["b"], d["both"], d["phi"],
                                                  d["p"], d["q"], "*" if d["q"] < 0.05 else ""))
