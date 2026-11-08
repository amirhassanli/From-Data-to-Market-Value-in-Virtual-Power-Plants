# -*- coding: utf-8 -*-
"""Follow-up d: cross-run-safe replacement for the two residual duplicated chunks."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
doc = docx.Document(P5)
APPLIED = []


def replace_span(p, old, new, tag):
    """Cross-run-safe: distribute `new` over the run owning the span start."""
    runs = p.runs
    if not runs:
        return False
    text = "".join(r.text for r in runs)
    if old not in text:
        return False
    i = text.find(old)
    j = i + len(old)
    owner = []
    for k, r in enumerate(runs):
        owner.extend([k] * len(r.text))
    out = [[] for _ in runs]
    for m in range(i):
        out[owner[m]].append(text[m])
    out[owner[i]].extend(list(new))
    for m in range(j, len(text)):
        out[owner[m]].append(text[m])
    for r, chs in zip(runs, out):
        r.text = "".join(chs)
    APPLIED.append(tag)
    return True


# --- layers paragraph residual duplicate
o1 = ("This reframingprofitable under the two-settlement market design itself "
      "\u2014 i.e., whether the attacker\u2019s objective is stated directly in "
      "market currency rather than in generic system-cost terms [50]. This reframing matters")
for p in doc.paragraphs:
    if p.text.startswith("The layers are ordered"):
        replace_span(p, o1, "This reframing matters", "layers dup ROOT-FIX")

# --- distributed-opt paragraph residual duplicate
o2 = "let largeBenders decomposition [54] let large, heterogeneous"
for p in doc.paragraphs:
    if p.text.startswith("Distributed optimization and decomposition"):
        replace_span(p, o2, "let large, heterogeneous", "distopt dup ROOT-FIX")

doc.save(P5)
print("applied:", APPLIED)
