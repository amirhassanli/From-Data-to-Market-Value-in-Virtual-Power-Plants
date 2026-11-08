# -*- coding: utf-8 -*-
"""Verify O/S-explicit study sets + maturity coding against Phase-5 ref numbers."""
import sys, io, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

rows = list(csv.DictReader(open("_draft/dmdi_coding_matrix.csv", newline="", encoding="utf-8")))
print("columns:", list(rows[0].keys()))
print()
for r in rows:
    ref = r.get("reference", "").strip("[]") or r.get("refnum", "").strip("[]")
    o = r.get("O", "").strip()
    s = r.get("S", "").strip()
    m = r.get("P", r.get("maturity", "?")).strip()
    if o.lower().startswith("e") or s.lower().startswith("e"):
        print("ref[%s]  O=%s  S=%s  P=%s  %s" % (ref, o, s, m, r["study"][:60]))
