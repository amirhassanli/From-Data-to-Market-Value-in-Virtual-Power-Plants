# -*- coding: utf-8 -*-
"""Italicize the venue substring in the five plain-run reference entries.
Idempotent: skips entries that already contain an italic run."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import copy
import docx

P = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
     r"Plants (revised 2026-10-27) - PHASE5.docx")
doc = docx.Document(P)

TARGETS = {
    "52": "IEEE Trans. Smart Grid",
    "68": "Applied Energy",
    "74": "Int. J. Electr. Power Energy Syst.",
    "77": "Energy",
    "81": "Applied Energy",
}

ps = doc.paragraphs
cut = next(i for i, p in enumerate(ps) if p.text.strip().startswith("14. References"))
done = []
for p in ps[cut + 1:]:
    t = p.text.strip()
    m = re.match(r"^\[(\d+)\]", t)
    if not m:
        continue
    num = m.group(1)
    if num not in TARGETS:
        continue
    if any(r.italic for r in p.runs):
        done.append("%s (already italic)" % num)
        continue
    venue = TARGETS[num]
    body_text = "".join(r.text for r in p.runs)
    i = body_text.find(venue)
    if i < 0:
        print("!! venue %r not found in [%s]" % (venue, num))
        continue
    assert len(p.runs) == 1, "[%s] expected single run" % num
    r0 = p.runs[0]
    before, after = r0.text[:i], r0.text[i + len(venue):]
    r0.text = before
    # italic run for the venue
    r_it = copy.deepcopy(r0._r)
    r0._r.addnext(r_it)
    r_n = docx.text.run.Run(r_it, p)
    r_n.text = venue
    r_n.italic = True
    # plain run for the remainder
    r2 = copy.deepcopy(r0._r)
    r_n._r.addnext(r2)
    r_r = docx.text.run.Run(r2, p)
    r_r.text = after
    r_r.italic = None if r_r.italic is None else False
    done.append("%s" % num)

doc.save(P)
print("done:", done)
