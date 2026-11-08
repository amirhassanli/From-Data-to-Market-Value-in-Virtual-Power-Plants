# -*- coding: utf-8 -*-
"""Semantic citation fixes: Table III rows 5-11 and the 9.2 review-gap list.
Identity-based (old-number targets derived from the original docx identities)."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
doc = docx.Document(P5)
CH = []

# ---------------- 9.2 list
for p in doc.paragraphs:
    txt = "".join(r.text for r in p.runs)
    if "Taken together with" in txt:
        old = "Taken together with [8], [16], [17], [33], [63], and [79],"
        new = "Taken together with [8], [17], [34], [65], [66], and [74],"
        if old in txt:
            i = txt.find(old)
            pos = 0
            for r in p.runs:
                if pos <= i < pos + len(r.text):
                    lo = i - pos
                    r.text = r.text[:lo] + new + r.text[lo + len(old):]
                    CH.append("9.2 list fixed")
                    break
                pos += len(r.text)
        break

# ---------------- Table III rows
ROWTARGETS = {
    5: ["[18]"],
    6: ["[19]"],
    7: ["[20]", "[21]", "[22]", "[23]", "[24]"],
    8: ["[25]", "[26]", "[27]", "[28]"],
    9: ["[29]", "[30]", "[31]"],
    10: ["[32]", "[33]", "[34]", "[35]"],
    11: ["[36]", "[10]"],
}
t = doc.tables[2]
for ri, targets in ROWTARGETS.items():
    c = t.rows[ri].cells[1]
    p = c.paragraphs[0]
    runs = p.runs
    full = "".join(r.text for r in runs)
    matches = [m for m in re.finditer(r"\[(\d+)\]", full)]
    equals = len(matches) == len(targets)
    # order check (robustness): ascending? record
    info = "%d tokens, target %d" % (len(matches), len(targets))
    if not equals:
        CH.append("Table III row %d SKIPPED (%s)" % (ri, info))
        continue
    # replace token k with targets[k], run-aware
    owner = []
    for ri_, r in enumerate(runs):
        owner.extend([ri_] * len(r.text))
    out = [[] for _ in runs]
    pos = 0
    for k, m in enumerate(matches):
        for j in range(pos, m.start()):
            out[owner[j]].append(full[j])
        out[owner[min(m.start(), len(owner) - 1)]].append(targets[k])
        pos = m.end()
    for j in range(pos, len(full)):
        out[owner[j]].append(full[j])
    for r, chars in zip(runs, out):
        r.text = "".join(chars)
    CH.append("Table III row %d fixed" % ri)

doc.save(P5)
print("applied:")
for x in CH:
    print("  -", x)
