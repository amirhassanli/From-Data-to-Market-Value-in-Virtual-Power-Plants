# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P5)

# 1. full text of paragraphs starting with known anchors
for p in d.paragraphs:
    t = p.text
    if t.startswith("Based on the verified core") or t.startswith("4. Synthesis") \
       or t.startswith("3. Positioning") or t.startswith("These are not the only surveys"):
        print("-" * 25)
        print(t[:1500])
        print()

# 2. every occurrence of token [41] in body paragraphs and table cells
print("=" * 60)
ti = 0
stop = False
for child in d.element.body.iterchildren():
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = Paragraph(child, d)
        if p.text.strip().startswith("14. References"):
            stop = True
        if not stop and "[41]" in p.text:
            print("PARA:", p.text[:200])
    elif tag == "tbl" and not stop:
        ti += 1
        tb = Table(child, d)
        for ri, r in enumerate(tb.rows):
            for ci, c in enumerate(r.cells):
                if "[41]" in c.text:
                    print("T%d r%d c%d: %s" % (ti, ri, ci, " ".join(c.text.split())[:150]))
