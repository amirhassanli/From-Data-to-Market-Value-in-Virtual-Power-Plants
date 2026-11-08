# -*- coding: utf-8 -*-
"""Sanity: final ref list identities for the numbers used in Tables IV/VI + key anchors."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P5)
started = False
want = set(range(40, 50)) | {16, 44, 57, 58, 59, 60, 61, 62, 65, 80, 82}
for p in d.paragraphs:
    t = p.text.strip()
    if t.startswith("14. References"):
        started = True
        continue
    if not started:
        continue
    m = re.match(r"^\[(\d+)\]", t)
    if m and int(m.group(1)) in want:
        print(t[:110])
