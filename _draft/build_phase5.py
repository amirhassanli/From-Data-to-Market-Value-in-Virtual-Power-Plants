# -*- coding: utf-8 -*-
"""
Phase 5 build (v2): remove the duplicate Wang 2025 reference by a global shift.

Input : PHASE4 .docx
Output: PHASE5 .docx

Phase 4 left the Wang et al. (2025) reference in twice ([17] abbreviated,
[18] full venue). Rather than re-running the full citation-order renumber, this
phase deletes the abbreviated copy and shifts every reference number >= 18 down
by one, in both the reference list and all in-text citations (including ranges),
which is exactly the effect of deleting one entry from an otherwise ordered list.
"""
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

SRC = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
       r"Plants (revised 2026-10-27) - PHASE4.docx")
DST = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
       r"Plants (revised 2026-10-27) - PHASE5.docx")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

doc = docx.Document(SRC)
LOG = []


def note(ok, msg):
    line = ("OK   " if ok else "FAIL ") + msg
    LOG.append(line)
    print(line, flush=True)


def shift_token(tok):
    """Shift a single bracket token [n] or range [a]-[b] down by 1 if n>=18."""
    def sh(n):
        n = int(n)
        return n - 1 if n >= 18 else n

    # range
    m = re.fullmatch(r"\[(\d+)\]\s*[\u2013-]\s*\[(\d+)\]", tok.strip())
    if m:
        a, b = sh(m.group(1)), sh(m.group(2))
        return "[%d]\u2013[%d]" % (a, b)
    m = re.fullmatch(r"\[(\d+)\]", tok.strip())
    if m:
        return "[%d]" % sh(m.group(1))
    return tok


CIT = re.compile(r"\[\d{1,2}\](?:\s*[\u2013\u2014-]\s*\[\d{1,2}\])*")


def rewrite_para(p):
    runs = p.runs
    if not runs:
        return 0
    text = "".join(r.text for r in runs)
    if "[" not in text:
        return 0
    owner = []
    for ri, r in enumerate(runs):
        owner.extend([ri] * len(r.text))
    if not owner:
        return 0
    out = [[] for _ in runs]
    pos = 0
    n = 0
    for m in CIT.finditer(text):
        for k in range(pos, m.start()):
            out[owner[k]].append(text[k])
        new = shift_token(m.group(0))
        if new != m.group(0):
            n += 1
        out[owner[min(m.start(), len(owner) - 1)]].append(new)
        pos = m.end()
    for k in range(pos, len(text)):
        out[owner[k]].append(text[k])
    for r, chars in zip(runs, out):
        s = "".join(chars)
        if s != r.text:
            r.text = s
    return n


# 1. remove the abbreviated duplicate (keep the full-venue one)
removed = 0
for p in list(doc.paragraphs):
    t = p.text.strip()
    if t.startswith("[17]") and "Renew. Sustain. Energy Rev." in t and "Carbon-billed" in t:
        p._p.getparent().remove(p._p)
        removed += 1
note(removed == 1, "abbreviated duplicate removed: %d" % removed)

# 2. shift ref paragraphs with number >= 18
shifted_refs = 0
for p in doc.paragraphs:
    t = p.text.strip()
    m = re.match(r"^\[(\d+)\]", t)
    if not m:
        continue
    n = int(m.group(1))
    if n >= 18:
        # rewrite prefix
        runs = p.runs
        if runs:
            txt = "".join(r.text for r in runs)
            mm = re.match(r"^\[(\d+)\]", txt)
            if mm:
                old_prefix = mm.group(0)
                new_prefix = "[%d]" % (n - 1)
                # replace first occurrence
                idx = txt.find(old_prefix)
                owner = []
                for ri, r in enumerate(runs):
                    owner.extend([ri] * len(r.text))
                out = [[] for _ in runs]
                pos = 0
                for k in range(pos, idx):
                    out[owner[k]].append(txt[k])
                out[owner[idx]].append(new_prefix)
                pos = idx + len(old_prefix)
                for k in range(pos, len(txt)):
                    out[owner[k]].append(txt[k])
                for r, ch in zip(runs, out):
                    r.text = "".join(ch)
                shifted_refs += 1
note(True, "reference paragraphs shifted: %d" % shifted_refs)

# 3. shift citations in body paragraphs and tables
shifted_tok = 0
for p in doc.paragraphs:
    if re.match(r"^\[\d+\]", p.text.strip()):
        continue
    shifted_tok += rewrite_para(p)
for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                shifted_tok += rewrite_para(p)
note(True, "citation tokens shifted: %d" % shifted_tok)

doc.save(DST)
note(True, "saved: " + DST)

# ------------------------------------------------------------------ verify
import collections
d2 = docx.Document(DST)
paras2 = d2.paragraphs
idx2 = [i for i, p in enumerate(paras2) if p.text.strip().startswith("14. References")][0]
refs2 = [p for p in paras2[idx2 + 1:] if re.match(r"^\[\d+\]", p.text.strip())]
nums = [int(re.match(r"^\[(\d+)\]", p.text).group(1)) for p in refs2]
note(len(refs2) == 82, "reference entries: %d" % len(refs2))
note(nums == list(range(1, 83)), "reference numbers ascending 1..82")
bodies = [re.match(r"^\[\d+\]\s*(.+)$", p.text.strip()).group(1) for p in refs2]
dups = {b: c for b, c in collections.Counter(bodies).items() if c > 1}
note(len(dups) == 0, "duplicate reference bodies: %d" % len(dups))

body_seq = []
stop = False
for child in d2.element.body.iterchildren():
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = Paragraph(child, d2)
        if p.text.strip().startswith("14. References"):
            stop = True
            continue
        if not stop:
            body_seq.append(p.text)
    elif tag == "tbl" and not stop:
        t = Table(child, d2)
        for r in t.rows:
            for c in r.cells:
                body_seq.append(c.text)
text_all = "\n".join(body_seq)
toks = [int(x) for x in re.findall(r"\[(\d{1,2})\]", text_all)]
note(min(toks) >= 1 and max(toks) <= 82, "all %d citation tokens within 1..82" % len(toks))

# Wang 2025 present once
cb = sum(1 for p in refs2 if "Carbon-billed" in p.text)
note(cb == 1, "Carbon-billed refs: %d" % cb)

ab = next(p for p in paras2 if p.text.startswith("Virtual power plants (VPPs) turn"))
wc = len(re.findall(r"[A-Za-z0-9][\w'\u2019\-]*", ab.text))
note(wc <= 250, "abstract words: %d" % wc)

fails = sum(1 for x in LOG if x.startswith("FAIL"))
print("\nFAILURES: %d" % fails)
