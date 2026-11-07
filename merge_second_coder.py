# -*- coding: utf-8 -*-
"""
Merge the completed blind sheet (filled by the second coder) into the master
double-coding sheet, then compute agreement.

Usage:
    python merge_second_coder.py <path-to-returned-Coding_Sheet_BLIND.csv>

After merging, run:
    python kappa_agreement.py dmdi_second_coder_sheet.csv
"""
import csv, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SHEET = "_draft/dmdi_second_coder_sheet.csv"
B_COLS = ["B_I", "B_U", "B_D", "B_M", "B_O", "B_S", "B_R", "B_P"]

def main(returned_path):
    with open(SHEET, newline="", encoding="utf-8-sig") as f:
        master = list(csv.DictReader(f))
    fields = list(master[0].keys())
    with open(returned_path, newline="", encoding="utf-8-sig") as f:
        back = list(csv.DictReader(f))
    back_by_study = {r["study"]: r for r in back}

    filled, empty, bad = 0, [], []
    for r in master:
        b = back_by_study.get(r["study"])
        if b is None:
            empty.append(r["study"]); continue
        vals = {}
        ok = True
        for c in B_COLS:
            v = (b.get(c) or "").strip().upper()
            if v not in ("E", "P", "NR"):
                ok = False; bad.append((r["study"], c, v))
            vals[c] = v
        if not ok:
            continue
        r.update(vals)
        if b.get("notes"):
            r["notes"] = (r.get("notes") or "") + ("; SECOND CODER: " + b["notes"]).strip("; ")
        filled += 1

    with open(SHEET, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(master)
    print("studies merged: %d / %d" % (filled, len(master)))
    if empty:
        print("MISSING from returned sheet:", empty)
    if bad:
        print("INVALID tokens (must be E, P or NR):", bad)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
    else:
        main(sys.argv[1])
