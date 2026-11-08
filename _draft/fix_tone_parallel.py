# -*- coding: utf-8 -*-
"""Micro-fix: settlement sentence stacked-and parallelism (anchor corrected)."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
     r"Plants (revised 2026-10-27) - PHASE5.docx")
doc = docx.Document(P)
APPLIED = []

def replace_span(p, old, new, tag):
    runs = p.runs
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

OLD = "products [76], and scalable frequency-regulation co-optimization [77], and"
NEW = "products [76], scalable frequency-regulation co-optimization [77], and"
done = False
for p in doc.paragraphs:
    if "Market-mechanism studies that explicitly model" in p.text:
        done = replace_span(p, OLD, NEW, "settlement parallelism")
        break
assert done, "anchor not found"
doc.save(P)
print("applied:", APPLIED)
