# -*- coding: utf-8 -*-
"""Global citation-consistency audit: label-year/bracket identity + first-citation order."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P5)
ps = d.paragraphs
cut = next(i for i, p in enumerate(ps) if p.text.strip().startswith("14. References"))

# -------- reference registry
REF = {}
for p in ps[cut + 1:]:
    t = p.text.strip()
    m = re.match(r"^\[(\d+)\]\s*(.+)$", t)
    if m:
        num = int(m.group(1))
        body = m.group(2)
        authors_seg = body.split("\u201c")[0]
        surnames = set(re.findall(r"\b[A-Z][a-zA-Z\u00C0-\u024F'\-]{2,}\b", authors_seg))
        # parse the printed year only up to the DOI string (the DOI may contain a
        # year-looking segment such as 10.1016/j.ejor.2019.07.022)
        pre_doi = body.split("doi:")[0]
        ys = re.findall(r"\b(20\d\d)\b", pre_doi)
        year = int(ys[-1]) if ys else None
        REF[num] = {"surnames": surnames, "year": year, "text": body[:80]}
print("refs registered:", len(REF))

# -------- collect body & cells in document order (tables included via body scan)
UNITS = []  # (kind, where, text)
stop = False
ti = 0
for child in d.element.body.iterchildren():
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = Paragraph(child, d)
        if p.text.strip().startswith("14. References"):
            stop = True
            continue
        if not stop:
            UNITS.append(("P", "body", p.text))
    elif tag == "tbl" and not stop:
        tb = Table(child, d)
        ti += 1
        for r in tb.rows:
            for c in r.cells:
                UNITS.append(("T%d" % ti, "cell", c.text))

problems = []
order = []
seen = set()
TOK = re.compile(r"\[(\d{1,2})\]")
CIT = re.compile(r"\[\d{1,2}\](?:\s*[\u2013\u2014-]\s*\[\d{1,2}\])*")
YEAR = re.compile(r"\((20\d\d)\)")

for kind, where, txt in UNITS:
    if kind.startswith("P") and re.match(r"^\[\d+\]", txt.strip()):
        continue  # reference list paragraphs
    for m in CIT.finditer(txt):
        for tok in re.findall(r"\d{1,2}", m.group(0)):
            n = int(tok)
            if n not in seen:
                seen.add(n)
                order.append(n)
            if n not in REF:
                problems.append("%s: token [%d] beyond ref list" % (kind, n))
                continue
        # year-proximity check: strictly "(YYYY)" immediately before the token
        head = txt[:m.start()]
        ym = None
        yend = re.search(r"\((20\d\d)\)\s*$", head)
        if yend:
            ym = yend.group(1)
        if ym:
            for tok in re.findall(r"\d{1,2}", m.group(0)):
                n = int(tok)
                ry = REF[n]["year"]
                if ry is not None and ry != int(ym):
                    problems.append("%s %s: '(2024) [%d]' but ref is %d — %s"
                                    % (kind, where, n, ry, REF[n]["text"]))

# -------- first-citation order
exp = list(range(1, len(REF) + 1))
print("\nfirst-citation sequence equals 1..%d: %s" % (len(REF), order == exp))
if order != exp:
    for i, (got, want) in enumerate(zip(order, exp)):
        if got != want:
            print("  first divergence at position %d: got ref [%d], expected [%d]" % (i + 1, got, want))
            break
    print("  refs not cited in body/tables:", [n for n in exp if n not in seen])
    print("  unexpected citations:", [n for n in seen if n > len(REF)])

print("\nyear-bracket problems: %d" % len(problems))
for x in problems[:40]:
    print("  ", x)
