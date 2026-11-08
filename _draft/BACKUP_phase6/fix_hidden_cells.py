# -*- coding: utf-8 -*-
"""Fix the four table cells whose damage was invisible to the row-matched audit.

Intended identities from PHASE3:
  Table IV r2 c3 (L2 Model mitigations): Esf-Kuhn, Lundberg, Ribeiro, Tao
  Table IV r3 c3 (L3 Execution):         Andoni
  Table IV r4 c3 (L4 Governance):        McMahan (FedAvg), Andoni
  Table VI r5 c3 (DRO):                  Mohajerin Esfahani & Kuhn

Numbers used are those valid in the post-first-renumber state; the second
renumber pass that follows recalculates first-citation order from scratch.
"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
doc = docx.Document(P5)
APPLIED = []


def cell_replace(ti, ri, ci, old, new, tag):
    c = doc.tables[ti].rows[ri].cells[ci]
    for p in c.paragraphs:
        runs = p.runs
        if not runs:
            continue
        text = "".join(r.text for r in runs)
        if old not in text:
            continue
        i = text.find(old)
        owner = []
        for k, r in enumerate(runs):
            owner.extend([k] * len(r.text))
        out = [[] for _ in runs]
        for j in range(i):
            out[owner[j]].append(text[j])
        out[owner[i]].extend(list(new))
        for j in range(i + len(old), len(text)):
            out[owner[j]].append(text[j])
        for r, chs in zip(runs, out):
            r.text = "".join(chs)
        APPLIED.append(tag)
        return
    APPLIED.append("FAILED %s" % tag)


# Table IV (idx3)
cell_replace(3, 2, 3, "[43], [44], [45], [46]", "[44], [45], [46], [47]",
             "T4 L2 cells (Goodfellow+shift)")
cell_replace(3, 3, 3, "[47]", "[48]", "T4 L3 Andoni")
cell_replace(3, 4, 3, "[48], [47]", "[65], [48]", "T4 L4 McMahan/Andoni")

# Table VI (idx5) DRO
cell_replace(5, 5, 3, "[43]", "[44]", "T6 DRO Esf-Kuhn")

doc.save(P5)
print("applied:")
for a in APPLIED:
    print("  -", a)
