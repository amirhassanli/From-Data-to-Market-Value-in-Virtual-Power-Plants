# -*- coding: utf-8 -*-
"""Final structural audit of PHASE3: headings, cross-references, counts, tone."""
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

P = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
     r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P)

paras = d.paragraphs
idx_refs = next(i for i, p in enumerate(paras) if p.text.strip().startswith("14. References"))

headings = [(p.style.name, p.text.strip()) for p in paras[:idx_refs + 1]
            if p.style.name.startswith("Heading")]
print("=== headings (%d) ===" % len(headings))
for st, t in headings:
    print("  %-9s %s" % (st, t[:90]))

nums = {}
for st, t in headings:
    m = re.match(r"^(\d+(?:\.\d+)?)\.?\s", t)
    if m:
        nums[m.group(1)] = t

body = "\n".join(p.text for p in paras[:idx_refs])
for t in d.tables:
    for r in t.rows:
        for c in r.cells:
            body += "\n" + c.text

print("\n=== section cross-references ===")
cited_secs = sorted(set(re.findall(r"Sections?\s+(\d+(?:\.\d+)?)", body)),
                    key=lambda s: [int(x) for x in s.split(".")])
bad = []
for s in cited_secs:
    ok = s in nums
    if not ok:
        bad.append(s)
    print("  Section %-4s %s  %s" % (s, "OK  " if ok else "MISSING", nums.get(s, "")[:60]))
print("  -> missing:", bad or "none")

# multi-section references like "Sections 7-10" or "Sections 2.7 and 11.6"
print("\n=== spans / pairs ===")
for m in re.finditer(r"Sections?\s+(\d+)(?:\.\d+)?\s*[\u2013-]\s*(\d+)", body):
    print("  span", m.group(0))
for m in re.finditer(r"Sections?\s+([\d.]+)\s+and\s+([\d.]+)", body):
    print("  pair", m.group(0))

print("\n=== table / figure cross-references ===")
tabs = sorted(set(re.findall(r"Table ([IVXL]+)", body)))
figs = sorted(set(int(x) for x in re.findall(r"Figs?\.\s*(\d+)", body)))
caps_t = [p.text.split(" ")[1] for p in paras if p.text.strip().startswith("TABLE ")]
caps_f = [int(p.text.split(" ")[1].rstrip(".")) for p in paras
          if re.match(r"^Fig\. \d+\.", p.text.strip())]
print("  tables referenced:", tabs)
print("  tables captioned :", caps_t)
print("  figures referenced:", figs)
print("  figures captioned :", caps_f)
print("  referenced but not captioned:",
      [t for t in tabs if t not in caps_t], [f for f in figs if f not in caps_f])
print("  captioned but never referenced:",
      [t for t in caps_t if t not in tabs], [f for f in caps_f if f not in figs])

print("\n=== quantitative claims vs Table XI ===")
TXI = {"I": (22, 17, 0), "U": (23, 15, 1), "D": (32, 7, 0), "M": (31, 8, 0),
       "O": (2, 5, 32), "S": (4, 18, 17), "R": (0, 38, 1)}
counts = [tuple(int(x) for x in m.groups())
          for m in re.finditer(r"(\d{1,2})/39\s+explicit,\s+(\d{1,2})/39\s+partial", body)]
print("  triplets stated in prose:", counts)
for c in counts:
    print("     %s  in Table XI: %s" % (c, c in TXI.values()))
singles = re.findall(r"\((\d{1,2})/39,\s*(\d{1,2})/39,\s*and\s*(\d{1,2})/39", body)
print("  abstract triplet:", singles)

print("\n=== consistency of key numbers ===")
for key in ("2,670", "1,002", "1,668", "39 studies", "35 of 39", "36/41", "88%"):
    print("  %-10s occurrences: %d" % (key, body.count(key)))

print("\n=== abstract ===")
ab = next(p for p in paras if p.text.startswith("Virtual power plants (VPPs) turn"))
print("  words:", len(re.findall(r"[A-Za-z0-9][\w'\u2019\-]*", ab.text)))
print("  citations inside abstract:", re.findall(r"\[\d+\]", ab.text) or "none")

print("\n=== numbers appearing only once (possible orphans) ===")
print("  tables:", len(d.tables), " body children:", len(list(d.element.body.iterchildren())))
