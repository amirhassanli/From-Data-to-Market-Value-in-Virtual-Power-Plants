# -*- coding: utf-8 -*-
"""Cross-check every study-level table cell against the validated 39x8 matrix."""
import csv
import re
import sys
import io
import docx

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

rows = list(csv.DictReader(open("_draft/dmdi_coding_matrix.csv", newline="", encoding="utf-8")))
COLS = ["I", "U", "D", "M", "O", "S", "R", "P"]
by_ref = {r["reference"]: r for r in rows}

LEVEL = {"explicit": "E", "partial": "P", "nr": "NR", "not reported": "NR"}

P = r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power Plants (revised 2026-10-27) - PHASE5.docx"
d = docx.Document(P)

TABLES = {7: "Table VIII", 8: "Table IX", 11: "Table XII"}
mismatches = []
unmatched = []

for ti, name in TABLES.items():
    t = d.tables[ti]
    hdr = [c.text.strip() for c in t.rows[0].cells]
    for r in t.rows[1:]:
        cells = [" ".join(c.text.split()) for c in r.cells]
        m = re.search(r"\[(\d+)\]", cells[0])
        if not m:
            unmatched.append((name, cells[0]))
            continue
        ref = "[%s]" % m.group(1)
        if ref not in by_ref:
            unmatched.append((name, cells[0]))
            continue
        for ci, h in enumerate(hdr):
            h = {"Settlement": "S"}.get(h, h)
            if h not in ("I", "U", "D", "O", "S"):
                continue
            v = LEVEL.get(cells[ci].lower())
            if v is None:
                continue
            want = by_ref[ref][h]
            if v != want:
                mismatches.append((name, ref, cells[0][:34], h, cells[ci], want))

print("mismatches: %d" % len(mismatches))
for x in mismatches:
    print("  %-11s %-5s %-34s dim %-2s table=%-8s matrix=%s" % x)

print("\nstudy rows not matched to a reference number: %d" % len(unmatched))
for x in unmatched:
    print("  %-11s %s" % x)

# reverse: which matrix studies never appear in any study-level table?
seen = set()
for ti in TABLES:
    for r in d.tables[ti].rows[1:]:
        m = re.search(r"\[(\d+)\]", " ".join(" ".join(cell.text.split()) for cell in r.cells))
        if m:
            seen.add("[%s]" % m.group(1))
print("\nmatrix rows covered by VIII/IX/XII: %d / 39" % len(seen))
print("not covered:", [r["reference"] for r in rows if r["reference"] not in seen])
