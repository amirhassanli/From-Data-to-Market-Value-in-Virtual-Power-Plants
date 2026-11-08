# -*- coding: utf-8 -*-
"""Tag-anchored fixes for the two Table-IV cells; identity-based, renumber follows."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P5 = (r"C:\Users\Mahboobian\Documents\Default Project\..\..\Documents\Default Project"
      .replace("..\\..\\Documents\\Default Project", ""))  # placeholder, set below
P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
doc = docx.Document(P5)
APPLIED = []


def cell_replace(ti, ri, ci, old, new, tag):
    c = doc.tables[ti].rows[ri].cells[ci]
    for p in c.paragraphs:
        runs = p.runs
        if not runs or old not in "".join(r.text for r in runs):
            continue
        text = "".join(r.text for r in runs)
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


# L2 Model mitigations: DRO=Esf-Kuhn, SHAP=Lundberg, LIME=Ribeiro, DT=Tao
cell_replace(3, 2, 3, "distributionally robust optimization [43]",
             "distributionally robust optimization [44]", "L2 DRO->EsfKuhn")
cell_replace(3, 2, 3, "SHAP [44]/LIME [45]", "SHAP [45]/LIME [46]", "L2 SHAP/LIME shift")
cell_replace(3, 2, 3, "digital-twin stress testing [46]",
             "digital-twin stress testing [48]", "L2 DT=Tao")

# L4 Governance: federated=McMahan(65), ledger-MRV=Andoni(47)
cell_replace(3, 4, 3, "federated learning [47]", "federated learning [65]",
             "L4 federated=McMahan")
cell_replace(3, 4, 3, "ledger-based MRV trails [48]", "ledger-based MRV trails [47]",
             "L4 ledger=Andoni")

doc.save(P5)
print("applied:", APPLIED)
