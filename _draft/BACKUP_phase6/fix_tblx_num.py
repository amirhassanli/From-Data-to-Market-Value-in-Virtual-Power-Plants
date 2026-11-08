# -*- coding: utf-8 -*-
"""Table X bracket fixes (row-index based; NBSP-safe). Idempotent."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P5)
t = d.tables[9]
TARGET = {1: "[32]", 2: "[33]", 3: "[34]", 4: "[15]", 5: "[35]", 6: "[65]", 7: "[17]"}
CHANGES = []
for i, r in enumerate(t.rows[1:], 1):
    c = r.cells[0]
    cp = c.paragraphs[0]
    runs = cp.runs
    text = "".join(ru.text for ru in runs)
    m = re.search(r"\[(\d+)\]", text)
    want = TARGET[i]
    if not m:
        CHANGES.append("row %d: no bracket" % i)
        continue
    cur = "[%s]" % m.group(1)
    if cur == want:
        continue
    idx = text.find(cur)
    pos = 0
    for ru in runs:
        if pos <= idx < pos + len(ru.text):
            local = idx - pos
            ru.text = ru.text[:local] + want + ru.text[local + len(cur):]
            CHANGES.append("row %d: %s -> %s" % (i, cur, want))
            break
        pos += len(ru.text)
d.save(P5)
print("applied:")
for x in CHANGES:
    print("  -", x)

# verify
d2 = docx.Document(P5)
for i, r in enumerate(d2.tables[9].rows):
    if i:
        print("row", i, " ->", " ".join(r.cells[0].text.split()))
