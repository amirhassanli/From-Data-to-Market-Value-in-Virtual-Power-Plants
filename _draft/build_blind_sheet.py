# -*- coding: utf-8 -*-
"""Build the second-coder package: blind coding sheet (with DOIs) + sync master sheet."""
import csv, re, sys, io, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")

# 1. number -> DOI from Phase5 reference list
d = docx.Document(P5)
ps = d.paragraphs
cut = next(i for i, p in enumerate(ps) if p.text.strip().startswith("14. References"))
num2doi = {}
for p in ps[cut + 1:]:
    t = p.text.strip()
    m = re.match(r"^\[(\d+)\]", t)
    if m:
        dm = re.search(r"(10\.\d{4,9}/[^\s,;]+)", t)
        if dm:
            num2doi[int(m.group(1))] = dm.group(1).rstrip(".").lower()

# 2. master matrix (Phase5 numbering)
rows = list(csv.DictReader(open("_draft/dmdi_coding_matrix.csv", newline="", encoding="utf-8")))

# 3. sync reference numbers in the second-coder master sheet
sc = list(csv.DictReader(open("_draft/dmdi_second_coder_sheet.csv", newline="", encoding="utf-8")))
fields = list(sc[0].keys())
sc_by_study = {r["study"]: r for r in rows}
for r in sc:
    m = sc_by_study[r["study"]]
    r["reference"] = m["reference"]
with open("_draft/dmdi_second_coder_sheet.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(sc)
print("master sheet reference column synced to Phase5 numbering")

# 4. blind sheet for the second coder
out_fields = ["study", "reference", "year", "doi",
              "B_I", "B_U", "B_D", "B_M", "B_O", "B_S", "B_R", "B_P", "notes"]
blind = []
missing_doi = []
for r in sc:
    m = sc_by_study[r["study"]]
    doi = num2doi.get(int(m["reference"].strip("[]")), "")
    if not doi:
        missing_doi.append((m["study"], m["reference"]))
    blind.append({"study": r["study"], "reference": r["reference"], "year": r["year"],
                  "doi": doi, **{c: "" for c in out_fields[4:-1]}, "notes": ""})
os.makedirs(r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder", exist_ok=True)
dst = r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\Coding_Sheet_BLIND.csv"
with open(dst, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=out_fields)
    w.writeheader()
    w.writerows(blind)
print("blind sheet written:", dst)
print("studies without DOI:", missing_doi)
