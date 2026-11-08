# -*- coding: utf-8 -*-
"""
Per-dimension agreement for the DMDI double-coding study.

Reads dmdi_second_coder_sheet.csv (A_ columns filled, B_ columns filled by the
second coder) and reports, for each dimension, observed agreement, Cohen's
kappa and an approximate 95% confidence interval.

Usage:
    python kappa_agreement.py [sheet.csv]
"""
import csv
import math
import sys

DIMS = ["I", "U", "D", "M", "O", "S", "R", "P"]
NAME = {"I": "Information-set integrity", "U": "Uncertainty integrity",
        "D": "Decision integrity", "M": "Market realism",
        "O": "Out-of-sample validity", "S": "Settlement realism",
        "R": "Reproducibility", "P": "Deployment maturity (companion)"}


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
    # large-sample variance (Fleiss-Cohen approximation)
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
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    print("sheet: %s   rows: %d" % (path, len(rows)))
    print()
    print("%-3s %-34s %6s %7s %8s %18s  %s" %
          ("dim", "dimension", "n", "agree", "kappa", "95% CI", "Landis-Koch"))
    print("-" * 96)
    summary = []
    for d in DIMS:
        pairs = []
        for r in rows:
            av = r["A_" + d].strip().upper()
            bv = r["B_" + d].strip().upper()
            if av in ("E", "P", "NR") and bv in ("E", "P", "NR"):
                pairs.append((av, bv))
        a = [p[0] for p in pairs]
        b = [p[1] for p in pairs]
        res = kappa(a, b)
        if res is None:
            print("%-3s %-34s %6d %7s %8s %18s  %s" % (d, NAME[d], len(a), "-", "-", "-",
                                                       "not computable"))
            continue
        po, k, se, n = res
        lo = max(-1.0, k - 1.96 * se)
        hi = min(1.0, k + 1.96 * se)
        ci = "%.2f to %.2f" % (lo, hi)
        flag = ""
        if max(a.count(c) for c in set(a)) / n > 0.90:
            flag = "  [prevalence: one level >90% of studies, kappa unstable]"
        print("%-3s %-34s %6d %7.3f %8.3f %18s  %s%s" % (d, NAME[d], n, po, k, ci, band(k), flag))
        summary.append((d, k))

    print()
    if summary:
        mean = sum(k for _, k in summary) / len(summary)
        print("mean kappa over %d dimensions: %.3f" % (len(summary), mean))
        print("minimum: %.3f (%s)   maximum: %.3f (%s)" %
              (min(summary, key=lambda x: x[1])[1], min(summary, key=lambda x: x[1])[0],
               max(summary, key=lambda x: x[1])[1], max(summary, key=lambda x: x[1])[0]))
    else:
        print("No B_ columns filled yet: nothing to compute.")
    print()
    print("Note: kappa treats the three DMDI levels as nominal categories, which is the "
          "conservative choice. A weighted kappa would credit near-misses between Explicit "
          "and Partial; if that is preferred, say so explicitly in the methods.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "dmdi_second_coder_sheet.csv")
