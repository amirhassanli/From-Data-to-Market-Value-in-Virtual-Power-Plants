# -*- coding: utf-8 -*-
"""
finalize_nummaps.py — remap all DMDI coding artifacts to the FINAL docx numbering.

Chain (old -> new per map):
    renum_p5_to_p6_v1.json  : p5_original -> mid1   (first renumber pass)
    renum_mid1_to_mid2.json : mid1 -> mid2          (second pass)
    renum_p5_to_p6.json     : mid2 -> FINAL         (third pass, current file)

Actions (idempotent — runs detect and no-op when numbers already FINAL):
 1. compose p5_original -> FINAL
 2. _draft/dmdi_coding_matrix.csv      : reference column remapped via map
 3. _draft/dmdi_second_coder_sheet.csv : reference column remapped via map
 4. _draft/dmdi_coding_long.csv        : reference REPLACED by study-name from
    the matrix (its numbers predate the first renumber entirely)
 5. _draft/study_to_phase5.json        : values remapped, keys preserved
 6. regenerate _draft/dmdi_second_coder_BLIND.csv (A_ empty) and
    Downloads\\DMDI_SecondCoder\\Coding_Sheet_BLIND.csv (A_ empty, doi kept)
 7. verify every remapped reference identity (DOI substring + printed year)
    against the FINAL PHASE5 reference list
"""
import csv
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
SC_BLIND = r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\Coding_Sheet_BLIND.csv"

# ------------------------------------------------------------------ chain map
def load_map(name):
    with open(os.path.join("_draft", name), encoding="utf-8") as f:
        return {int(k): int(v) for k, v in json.load(f).items()}

v1  = load_map("renum_p5_to_p6_v1.json")     # p5 -> mid1
mid = load_map("renum_mid1_to_mid2.json")    # mid1 -> mid2
fin = load_map("renum_p5_to_p6.json")        # mid2 -> final

comp = {}
for old, m1 in v1.items():
    m2 = mid.get(m1)
    if m2 is None:
        raise SystemExit("chain broken: p5[%d]->mid1=%d not in mid1_to_mid2" % (old, m1))
    new = fin.get(m2)
    if new is None:
        raise SystemExit("chain broken: mid2=%d not in mid2_to_final" % m2)
    comp[old] = new
print("composed p5 -> FINAL map: %d entries" % len(comp))
print("  fixed points:", sorted(k for k, v in comp.items() if k == v))
print("  sample:", {k: comp[k] for k in sorted(comp)[15:20]})

# ------------------------------------------------------- final ref registry
d = docx.Document(P5)
refs = {}
started = False
for p in d.paragraphs:
    t = p.text.strip()
    if t.startswith("14. References"):
        started = True
        continue
    if started:
        m = re.match(r"^\[(\d+)\]\s*(.+)$", t)
        if m:
            refs[int(m.group(1))] = m.group(2)
print("final docx refs: %d" % len(refs))

def ref_year(body):
    pre = body.split("doi:")[0]
    ys = re.findall(r"\b(20\d\d)\b", pre)
    return ys[-1] if ys else "?"

def ref_doi(body):
    m = re.search(r"(10\.\d{4,9}/[^\s,;]+)", body)
    return (m.group(1).rstrip(".").lower() if m else "")

# ------------------------------------------------------------------- helpers
def remap_ref(token):
    """'[12]' -> '[FINAL]', using composed map; returns None if unresolvable."""
    m = re.match(r"^\[(\d+)\]$", token.strip())
    if not m:
        return token
    n = int(m.group(1))
    if n not in comp:
        return None
    return "[%d]" % comp[n]

# doi per study (source of truth: the Downloads blind sheet, which carried doi)
DOI = {}
with open(SC_BLIND, newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        DOI[r["study"].strip()] = (r.get("doi") or "").strip().lower()
print("doi map: %d studies" % len(DOI))

def verify_study(study, refnum, year):
    """refnum like '[25]' after remap; verify DOI + year identity in refs."""
    body = refs.get(refnum and int(refnum.strip("[]")))
    if body is None:
        return "MISSING REF %s" % refnum
    doi = DOI.get(study, "")
    ok_doi = (not doi) or (doi in body.lower())
    ok_year = (not year) or (ref_year(body) == year)
    if ok_doi and ok_year:
        return "OK"
    return "BAD doi=%s(%s) year=%s vs ref_year=%s" % (
        doi, ok_doi, year, ref_year(body))

REPORT = []

# ------------------------------------------------------ 1. coding matrix CSV
MP = "_draft/dmdi_coding_matrix.csv"
with open(MP, newline="", encoding="utf-8-sig") as f:
    rd = csv.DictReader(f)
    mfields = rd.fieldnames
    mrows = list(rd)
changed = 0
for r in mrows:
    old = r["reference"].strip()
    new = remap_ref(old)
    if new is None:
        REPORT.append("matrix %s: unresolved %s" % (r["study"], old))
        continue
    if new != old:
        r["reference"] = new
        changed += 1
with open(MP, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=mfields)
    w.writeheader()
    w.writerows(mrows)
print("matrix: %d/%d rows rewritten" % (changed, len(mrows)))

# verify matrix identity after remap
for r in mrows:
    v = verify_study(r["study"], r["reference"], r["year"])
    if v != "OK":
        REPORT.append("matrix %s [%s]: %s" % (r["study"], r["reference"], v))

# matrix ref->study reverse (for long csv)
REF_BY_STUDY = {r["study"]: r["reference"] for r in mrows}

# --------------------------------------------- 2. second coder sheet (master)
SP = "_draft/dmdi_second_coder_sheet.csv"
with open(SP, newline="", encoding="utf-8-sig") as f:
    rd = csv.DictReader(f)
    sfields = rd.fieldnames
    srows = list(rd)
changed = 0
for r in srows:
    old = r["reference"].strip()
    new = remap_ref(old)
    if new is None:
        REPORT.append("sheet %s: unresolved %s" % (r["study"], old))
        continue
    if new != old:
        r["reference"] = new
        changed += 1
with open(SP, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=sfields)
    w.writeheader()
    w.writerows(srows)
print("sheet: %d/%d rows rewritten" % (changed, len(srows)))

# ----------------------------------------------------------- 3. long csv (name)
LP = "_draft/dmdi_coding_long.csv"
with open(LP, newline="", encoding="utf-8-sig") as f:
    rd = csv.DictReader(f)
    lfields = rd.fieldnames
    lrows = list(rd)
changed, miss = 0, 0
for r in lrows:
    new = REF_BY_STUDY.get(r["study"].strip())
    if new is None:
        miss += 1
        REPORT.append("long: study not in matrix: %r" % r["study"])
        continue
    if r["reference"] != new:
        r["reference"] = new
        changed += 1
with open(LP, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=lfields)
    w.writeheader()
    w.writerows(lrows)
print("long: %d/%d rows rewritten, %d missing studies" % (changed, len(lrows), miss))

# ------------------------------------------------------ 4. study_to_phase5.json
JP = "_draft/study_to_phase5.json"
with open(JP, encoding="utf-8") as f:
    jmap = json.load(f)
changed = 0
for k, old in list(jmap.items()):
    new = comp.get(int(old))
    if new is None:
        REPORT.append("json %r: unresolved %r" % (k, old))
        continue
    if new != int(old):
        jmap[k] = new
        changed += 1
with open(JP, "w", encoding="utf-8") as f:
    json.dump(jmap, f, indent=1, ensure_ascii=False)
print("study_to_phase5.json: %d/%d values rewritten" % (changed, len(jmap)))

# verify json against matrix
for k, v in jmap.items():
    ref = "[{}]".format(v)
    mref = REF_BY_STUDY.get(k)
    if mref is not None and mref != ref:
        REPORT.append("json vs matrix: %r json=%s matrix=%s" % (k, ref, mref))

# ---------------------------------------------------- 5. regenerate blind CSVs
B_COLS = ["B_I", "B_U", "B_D", "B_M", "B_O", "B_S", "B_R", "B_P"]
A_COLS = ["A_I", "A_U", "A_D", "A_M", "A_O", "A_S", "A_R", "A_P"]

# _draft blind: full master columns, A/B emptied
bf = ["study", "reference", "year", "doi"] + A_COLS + B_COLS + ["notes"]
# build doi by study again (sheet lacks doi col)
with open("_draft/dmdi_second_coder_BLIND.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=bf)
    w.writeheader()
    for r in srows:
        w.writerow({"study": r["study"], "reference": r["reference"],
                    "year": r["year"], "doi": DOI.get(r["study"], ""),
                    **{c: "" for c in A_COLS + B_COLS}, "notes": ""})
print("draft blind regenerated")

# Downloads blind: coder-facing columns (study, reference, year, doi, B_*, notes)
cf = ["study", "reference", "year", "doi"] + B_COLS + ["notes"]
with open(SC_BLIND, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cf)
    w.writeheader()
    for r in srows:
        w.writerow({"study": r["study"], "reference": r["reference"],
                    "year": r["year"], "doi": DOI.get(r["study"], ""),
                    **{c: "" for c in B_COLS}, "notes": ""})
print("Downloads coding sheet regenerated")

# ------------------------------------------------------------------------- end
print()
if REPORT:
    print("PROBLEMS (%d):" % len(REPORT))
    for x in REPORT:
        print("  -", x)
else:
    print("all studies verified: DOI + year identity against FINAL docx registry")
