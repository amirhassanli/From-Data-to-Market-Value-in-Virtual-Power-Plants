# -*- coding: utf-8 -*-
"""Promote the literal '14. References' paragraph to Heading 1 (idempotent)."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
     r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P)
done = False
for p in d.paragraphs:
    if p.text.strip() == "14. References":
        cur = p.style.name if p.style is not None else "?"
        if cur == "Heading 1":
            print("already Heading 1 — no-op")
            done = True
            break
        p.style = d.styles["Heading 1"]
        done = True
        print("promoted %r : %s -> Heading 1" % (p.text[:20], cur))
        break
assert done, "References heading not found"
d.save(P)
print("saved")
