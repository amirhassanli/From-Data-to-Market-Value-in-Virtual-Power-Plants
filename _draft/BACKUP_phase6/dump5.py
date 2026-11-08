# -*- coding: utf-8 -*-
"""Refresh dump of (paragraphs, tables, refs) from PHASE5 into phase5_full.txt."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P5)
out = []
ti = 0
for child in d.element.body.iterchildren():
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = Paragraph(child, d)
        st = p.style.name if p.style is not None else "?"
        out.append("[%s] %s" % (st, p.text))
    elif tag == "tbl":
        ti += 1
        tb = Table(child, d)
        out.append("--- TABLE %d (%dx%d) ---" % (ti, len(tb.rows), len(tb.columns)))
        for r in tb.rows:
            out.append(" | ".join(c.text.replace("\n", " / ") for c in r.cells))
with open("_draft/phase5_full.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("written %d lines, %d tables" % (len(out), ti))
