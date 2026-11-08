# -*- coding: utf-8 -*-
"""Identity citation audit v2: sorted-multiset aware + detailed label report."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

P3 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE3.docx")
P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")

SKIP_TABLES = {7, 8, 9, 11, 12}     # VIII, IX, X, XII, XIII hand-fixed
SKIP_PARAS = ("Taken together with", "Several limitations qualify", "Eligibility follows",
              "The per-study coding matrix", "Stochastic, robust, DRO, and")


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def load(path):
    d = docx.Document(path)
    paras, tables, refs = [], [], {}
    stop = False
    for child in d.element.body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            p = Paragraph(child, d)
            if not stop:
                paras.append(norm(p.text))
            if p.text.strip().startswith("14. References"):
                stop = True
        elif tag == "tbl" and not stop:
            tb = Table(child, d)
            tables.append([[norm(c.text) for c in r.cells] for r in tb.rows])
    started = False
    for p in d.paragraphs:
        t = p.text.strip()
        if t.startswith("14. References"):
            started = True
            continue
        if started:
            m = re.match(r"^\[(\d+)\]\s*(.+)$", t)
            if m:
                refs[int(m.group(1))] = m.group(2)
    return paras, tables, refs


def ident(refs):
    out = {}
    for n, body in refs.items():
        dm = re.search(r"(10\.\d{4,9}/[^\s,;\)]+[^\s,;.])", body)
        if dm:
            out[n] = dm.group(1).lower()
            continue
        seg = body.split("\u201c")[0]
        ys = re.findall(r"\b(19|20)(\d\d)\b", body)
        year = (ys[-1][0] + ys[-1][1]) if ys else "?"
        surn = sorted(set(re.findall(r"\b[A-Z][a-zA-Z]{2,}", seg)))[:3]
        out[n] = ("K", tuple(surn), year)
    return out


def short(v):
    if isinstance(v, str):
        return v[-28:]
    return "K:%s:%s" % ("/".join(v[1])[:30], v[2])


def same(a, b):
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    if isinstance(a, tuple) and isinstance(b, tuple):
        setA, setB = set(a[1]), set(b[1])
        return len(setA & setB) >= 2 and a[2] == b[2]
    return False


def toks(text):
    return [int(x) for x in re.findall(r"\[(\d{1,2})\]", text)]


paras3, tbls3, refs3 = load(P3)
paras5, tbls5, refs5 = load(P5)
i3, i5 = ident(refs3), ident(refs5)

CITS = re.compile(r"\[\d{1,2}\](?:\s*[\u2013\u2014-]\s*\[\d{1,2}\])*")


def expand(text):
    out = []
    for m in CITS.finditer(text):
        out.extend(int(x) for x in re.findall(r"\d{1,2}", m.group(0)))
    return out


report = []
p3_next = 0
for k, pt in enumerate(paras5):
    if any(pt.startswith(s) for s in SKIP_PARAS):
        continue
    if "[" not in pt:
        continue
    found = None
    for j in range(p3_next, len(paras3)):
        if paras3[j][:18] == pt[:18]:
            found = j
            break
    if found is None:
        continue
    p3_next = found + 1
    s3, s5 = expand(paras3[found]), expand(pt)
    if sorted(s3) == sorted(s5):
        # same multiset; also confirm positions match
        if len(s3) == len(s5):
            bad_pos = [q for q, (a, b) in enumerate(zip(s3, s5)) if not same(i3[a], i5[b])]
            if bad_pos:
                report.append(("ORDER", k, pt[:60], [(q, s3[q], s5[q]) for q in bad_pos]))
        continue
    # multiset differs: pairwise label map for inspection
    labels3, labels5 = [], []
    li3 = {x for x in s3}
    for x in s3:
        labels3.append((x, short(i3[x])))
    for x in s5:
        labels5.append((x, short(i5[x])))
    report.append(("COUNT", k, pt[:60], labels3, labels5))

print("=== semantic multiset differences (paragraphs) ===")
for r in report:
    if r[0] == "COUNT":
        print("P5[%d] %s" % (r[1], r[2]))
        print("   p3:", r[3])
        print("   p5:", r[4])
        print()
print("=== position mismatches (same multiset, different slot) ===")
for r in report:
    if r[0] == "ORDER":
        print("P5[%d] %s %s" % (r[1], r[2], r[3]))

print()
print("=== tables ===")
for ti in range(min(len(tbls3), len(tbls5))):
    if ti in SKIP_TABLES:
        continue
    g3, g5 = tbls3[ti], tbls5[ti]
    for ri, row5 in enumerate(g5):
        if ri >= len(g3):
            break
        r3 = g3[ri]
        if r3[0][:40] != row5[0][:40]:
            continue
        for ci in range(min(len(r3), len(row5))):
            s3, s5 = expand(r3[ci]), expand(row5[ci])
            if s3 == s5:
                continue
            if sorted(s3) == sorted(s5):
                continue
            print("TBL idx%d r%d c%d (%s)" % (ti, ri, ci, r3[0][:40]))
            print("   p3:", [(x, short(i3[x])) for x in s3])
            print("   p5:", [(x, short(i5[x])) for x in s5])
            print()
