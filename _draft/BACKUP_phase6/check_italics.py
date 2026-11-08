# -*- coding: utf-8 -*-
"""List reference entries whose runs contain no italic run (venue should be italic)."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
     r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P)
ps = d.paragraphs
cut = next(i for i, p in enumerate(ps) if p.text.strip().startswith("14. References"))
for p in ps[cut + 1:]:
    t = p.text.strip()
    if not re.match(r"^\[\d+\]", t):
        continue
    if not any(r.italic for r in p.runs):
        print("NO-ITALIC:", t[:130])
        for r in p.runs:
            print("    run %r italic=%s" % (r.text[:60], r.italic))
