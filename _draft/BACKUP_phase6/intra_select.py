# -*- coding: utf-8 -*-
"""
intra_select.py — build the intra-coder test-retest subsample (n=15).

Design (documented in the protocol; seed fixed):
  * anchors (all included): every study with E on O or S (6 studies) and every
    zero-explicit study (3 studies) -> the two extreme strata of the rating
    distribution are guaranteed representation (rare-level enrichment guards
    the kappa prevalence paradox by making the estimate conservative).
  * remainder: 6 studies drawn uniformly at random from the remaining 30,
    year-stratified (one slot per draw cycle over year groups, seeded).
  * presentation order: shuffled with the same seed.
Seed = 20261103 (date of protocol freeze). Output:
  - Downloads\\DMDI_IntraCoder\\IntraCoder_ReCode_SHEET.csv
      columns: re_order, study, reference, year, doi, B_I..B_P, notes
      (B_* empty; NO A_* columns -> recoder cannot see original ratings)
  - Downloads\\DMDI_IntraCoder\\SUBSAMPLE_key.csv  (coder A keeps: mapping
      re_order -> original coding, for later merging/adjudication)
Prints the selection with the rationale.
"""
import csv, io, json, os, random, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SEED = 20261103
DEST = r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder"
os.makedirs(DEST, exist_ok=True)

rows = list(csv.DictReader(open("_draft/dmdi_coding_matrix.csv", newline="",
                                encoding="utf-8")))
assert len(rows) == 39
COLS = ["I", "U", "D", "M", "O", "S", "R", "P"]

def n_explicit(r):
    return sum(1 for c in COLS[:7] if r[c] == "E")

anchors, rest = [], []
for r in rows:
    rare = r["O"] == "E" or r["S"] == "E"     # rare-level studies
    zero = n_explicit(r) == 0                  # zero-explicit studies
    label = "  O/S-explicit" if rare else "  zero-explicit"
    if rare or zero:
        anchors.append((r, label))
    else:
        rest.append(r)

print("anchors (rare-level O/S explicit + zero-explicit): %d" % len(anchors))
for r, label in anchors:
    print("   %-38s [%s] %s%s" % (r["study"], r["reference"], r["year"], label))

rng = random.Random(SEED)

# year-stratified remainder draw: 6 slots over year groups
rest_sorted = sorted(rest, key=lambda r: int(r["year"]))
groups = {}
for r in rest_sorted:
    groups.setdefault(r["year"], []).append(r)
years = sorted(groups)
picks = []
cycle = 0
while len(picks) < 6:
    y = years[cycle % len(years)]
    g = groups[y]
    avail = [x for x in g if x not in picks]
    if avail:
        picks.append(rng.choice(avail))
    cycle += 1
    if cycle > 500:
        break

sub = [r for r, _ in anchors] + picks
order = list(range(len(sub)))
rng.shuffle(order)

DOI = {}
with open(r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\Coding_Sheet_BLIND.csv",
          newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        DOI[r["study"].strip()] = (r.get("doi") or "").strip()

# coder-facing sheet (shuffled, no A_ columns)
with open(os.path.join(DEST, "IntraCoder_ReCode_SHEET.csv"), "w", newline="",
          encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["re_order", "study", "reference", "year", "doi",
                "B_I", "B_U", "B_D", "B_M", "B_O", "B_S", "B_R", "B_P", "notes"])
    for oi, ix in enumerate(order):
        r = sub[ix]
        w.writerow([oi + 1, r["study"], r["reference"], r["year"],
                    DOI.get(r["study"], "")] + [""] * 8 + [""])

# coder A key: re_order -> original coding (kept by coder A, never shared)
with open(os.path.join(DEST, "SUBSAMPLE_key.csv"), "w", newline="",
          encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["re_order", "study", "reference"] + ["A_" + c for c in COLS])
    for oi, ix in enumerate(order):
        r = sub[ix]
        w.writerow([oi + 1, r["study"], r["reference"]] + [r[c] for c in COLS])

print("remainder drawn (year-stratified, seed=%d): %d" % (SEED, len(picks)))
for r in picks:
    print("   %-38s [%s] %s" % (r["study"], r["reference"], r["year"]))
print()
print("subsample rows: %d / 39 (%.0f%%)" % (len(sub), 100 * len(sub) / 39))
print("written: IntraCoder_ReCode_SHEET.csv | SUBSAMPLE_key.csv -> %s" % DEST)
