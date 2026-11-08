# -*- coding: utf-8 -*-
"""Lint the reference list: IEEE structure, DOI presence, ordering, citation order."""
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
cut = next(i for i, p in enumerate(paras) if p.text.strip().startswith("14. References")
           or p.text.strip() == "References")

refs = []
for p in paras[cut:]:
    t = p.text.strip()
    m = re.match(r"^\[(\d+)\]\s*(.+)$", t)
    if m:
        refs.append((int(m.group(1)), m.group(2), p))

print("reference entries parsed: %d" % len(refs))
nums = [n for n, _, _ in refs]
print("numbering contiguous 1..%d: %s" % (len(refs), nums == list(range(1, len(refs) + 1))))

# first-citation order — true document order: paragraphs and table cells
# interleaved as they appear in the body (paragraphs-first concatenation
# would rank every table citation after every prose citation, falsely).
body = ""
for child in d.element.body.iterchildren():
    tag = child.tag.split("}")[-1]
    if tag == "p":
        pp = Paragraph(child, d)
        if pp.text.strip().startswith("14. References") or pp.text.strip() == "References":
            break
        body += "\n" + pp.text
    elif tag == "tbl":
        for rr in Table(child, d).rows:
            for cc in rr.cells:
                body += "\n" + cc.text

# first-citation order
first = []
for m in re.finditer(r"\[(\d{1,2})\]", body):
    n = int(m.group(1))
    if n not in first:
        first.append(n)
print("\nfirst-citation order identical to list order: %s"
      % (first == sorted(first)))
if first != sorted(first):
    # report the inversions
    bad = [(i, first[i]) for i in range(len(first)) if first[i] != sorted(first)[i]]
    print("  first 12 citations:", first[:12])
    for i, n in bad[:15]:
        print("   position %2d -> [%d]  (expected [%d])" % (i, n, sorted(first)[i]))

cited = set(first)
missing = [n for n in nums if n not in cited]
extra = [n for n in cited if n not in nums]
print("\nuncited references: %s" % (missing or "none"))
print("cited but not in list: %s" % (extra or "none"))

print("\n--- structural lint per entry ---")
no_doi = []
no_vol = []
no_pages = []
no_artno = []
bad_quote = []
long_authors = []
for n, t, _ in refs:
    if "doi:" not in t and "10." not in t:
        no_doi.append(n)
    if not re.search(r"vol\.\s*\d+", t):
        no_vol.append(n)
    if not (re.search(r"pp\.\s*\d", t) or re.search(r"Art\. no\.", t) or
            re.search(r"\d+\s*\(\d+\)", t) and re.search(r"Art\.", t)):
        no_pages.append(n)
    if "Art. no." not in t and not re.search(r"pp\.\s*\d", t):
        no_artno.append(n)
    if t.count("\u201c") != 1 or t.count("\u201d") != 1:
        bad_quote.append(n)
    if t.count(",") > 12:
        long_authors.append(n)

print("no DOI:            %s" % (no_doi or "none"))
print("no 'vol.':         %s" % (no_vol or "none"))
print("no pages/art.no:   %s" % (no_pages or "none"))
print("no locator at all: %s" % (no_artno or "none"))
print("quote imbalance:   %s" % (bad_quote or "none"))
print("very long author strings (>12 commas): %s" % (long_authors or "none"))

print("\n--- DOIs: uniqueness and prefix ---")
dois = []
for n, t, _ in refs:
    m = re.search(r"(10\.\d{4,9}/[^\s,;]+)", t)
    if m:
        dois.append((n, m.group(1).rstrip(".")))
print("entries with a DOI: %d / %d" % (len(dois), len(refs)))
seen = {}
dups = []
for n, dd in dois:
    if dd.lower() in seen:
        dups.append((seen[dd.lower()], n, dd))
    seen[dd.lower()] = n
print("duplicate DOIs:", dups or "none")
for n, dd in dois:
    if not dd.startswith("10."):
        print("  odd DOI [%d] %s" % (n, dd))

print("\n--- venue distribution ---")
venues = {}
for n, t, _ in refs:
    m = re.search(r"\u201d\s*,\s*([^,]+),", t)
    v = m.group(1).strip() if m else "??"
    venues[v] = venues.get(v, 0) + 1
for v, c in sorted(venues.items(), key=lambda x: -x[1]):
    print("  %2d  %s" % (c, v))

print("\n--- year distribution ---")
years = {}
for n, t, _ in refs:
    ys = re.findall(r"\b(20\d\d)\b", t)
    y = ys[-1] if ys else "??"
    years[y] = years.get(y, 0) + 1
for y, c in sorted(years.items()):
    print("  %s  %d" % (y, c))
