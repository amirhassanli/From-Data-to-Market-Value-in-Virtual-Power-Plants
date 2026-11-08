# -*- coding: utf-8 -*-
"""
Phase 6c: full first-citation renumbering.

Recomputes the first-appearance order of every bracket citation over the whole
document (paragraphs then table cells, in document order), assigns new numbers
1..N in that order, rewrites every token in body prose and table cells, renumbers
and re-orders the reference list. In-place on the PHASE5 docx; writes the
old->new map to _draft/renum_p5_to_p6.json.
"""
import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")

d = docx.Document(P5)

# ------------------------------------------------------------------ collect units
units = []          # (holder, text)  holder: Paragraph or Cell
stop_body = False
for child in d.element.body.iterchildren():
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = Paragraph(child, d)
        if p.text.strip().startswith("14. References"):
            stop_body = True
            continue
        if not stop_body:
            units.append(p)
    elif tag == "tbl" and not stop_body:
        tb = Table(child, d)
        for r in tb.rows:
            for c in r.cells:
                units.append(c)

# ------------------------------------------------------------------ first-appearance order
CIT = re.compile(r"\[\d{1,2}\](?:\s*[\u2013\u2014-]\s*\[\d{1,2}\])*")
order = []
seen = set()
for holder in units:
    if isinstance(holder, docx.table._Cell):
        text = "".join(pp.text for pp in holder.paragraphs)
    else:
        text = holder.text
    if not isinstance(holder, docx.table._Cell) and re.match(r"^\[\d+\]", text.strip()):
        continue
    for m in CIT.finditer(text):
        for tok in re.findall(r"\d{1,2}", m.group(0)):
            n = int(tok)
            if n not in seen:
                seen.add(n)
                order.append(n)

nrefs = len(order)
print("distinct cited refs:", nrefs)
print("first-citation order:", order)
MAP = {old: k + 1 for k, old in enumerate(order)}
assert set(MAP) == set(range(1, nrefs + 1)), "map must cover 1..N exactly"

# cross-run-safe token rewrite for a paragraph-holder
PLACE = ("\u27e6", "\u27e7")   # ⟦ ⟧


def rewrite_tokens(holder, transform):
    paras = holder.paragraphs if isinstance(holder, docx.table._Cell) else [holder]
    applied = False
    for p in paras:
        runs = p.runs
        if not runs:
            continue
        text = "".join(r.text for r in runs)
        if "[" not in text:
            continue
        ms = list(re.finditer(r"\[\d{1,2}\]", text))
        if not ms:
            continue
        if PLACE[0] in text:
            continue                    # already processed
        owner = []
        for k, r in enumerate(runs):
            owner.extend([k] * len(r.text))
        out = [[] for _ in runs]
        pos = 0
        for m in ms:
            old_t = m.group(0)
            new_t = transform(old_t)
            for j in range(pos, m.start()):
                out[owner[j]].append(text[j])
            wi = owner[min(m.start(), len(owner) - 1)]
            out[wi].extend(list(new_t))
            pos = m.end()
        for j in range(pos, len(text)):
            out[owner[j]].append(text[j])
        for r, chs in zip(runs, out):
            r.text = "".join(chs)
        applied = True
    return applied


# phase A: wrap each bracket token in placeholders
for holder in units:
    def to_ph(t, MAP=MAP):
        n = int(t[1:-1])
        return "%s%d%s" % (PLACE[0], n, PLACE[1])
    rewrite_tokens(holder, to_ph)

# phase B: replace placeholder with the new number
for holder in units:
    def from_ph(t, MAP=MAP):
        n = int(t[1:-1])
        return "[%d]" % MAP[n]

    def tr(t, MAP=MAP):
        pass
    # placeholder string itself is "\"...\"" synthetic; use regex via transform
    def transform(t, MAP=MAP):
        n = int(t[1:-1])
        return "[%d]" % MAP[n]
    rewrite_placeholder = rewrite_tokens  # reuse with custom regex

# (do phase B with a helper that matches placeholders instead of brackets)
def rewrite_placeholders(holder, MAP):
    paras = holder.paragraphs if isinstance(holder, docx.table._Cell) else [holder]
    changed = False
    for p in paras:
        runs = p.runs
        if not runs:
            continue
        text = "".join(r.text for r in runs)
        if PLACE[0] not in text:
            continue
        ms = list(re.finditer(r"%s(\d{1,3})%s" % (PLACE[0], PLACE[1]), text))
        if not ms:
            continue
        owner = []
        for k, r in enumerate(runs):
            owner.extend([k] * len(r.text))
        out = [[] for _ in runs]
        pos = 0
        for m in ms:
            new_t = "[%d]" % MAP[int(m.group(1))]
            for j in range(pos, m.start()):
                out[owner[j]].append(text[j])
            wi = owner[min(m.start(), len(owner) - 1)]
            out[wi].extend(list(new_t))
            pos = m.end()
        for j in range(pos, len(text)):
            out[owner[j]].append(text[j])
        for r, chs in zip(runs, out):
            r.text = "".join(chs)
        changed = True
    return changed


CHANGED = 0
for holder in units:
    if rewrite_placeholders(holder, MAP):
        CHANGED += 1
print("units with rewritten tokens:", CHANGED)

# ------------------------------------------------------------------ reference list
started = False
ref_paras = {}      # oldnum -> Paragraph
for p in d.paragraphs:
    t = p.text.strip()
    if t.startswith("14. References"):
        started = True
        continue
    if not started:
        continue
    m = re.match(r"^\[(\d+)\]", t)
    if m:
        ref_paras[int(m.group(1))] = p
print("ref paragraphs found:", len(ref_paras))
assert set(ref_paras) == set(range(1, nrefs + 1)), "ref list incomplete"

# rewrite each ref paragraph's leading number (cross-run-safe at the START)
for old, p in ref_paras.items():
    new = MAP[old]
    if new == old:
        # still regenerate the text "[old] " -> "[new] " (same, no-op)
        pass
    # find the run containing the leading token and rewrite precisely there
    text = "".join(r.text for r in p.runs)
    lead = "[%d]" % old
    i = text.find(lead)
    assert i == 0 or text.lstrip().startswith(lead), "leading token not first: %r" % text[:20]
    # erase leading spaces? keep as-is; replace first occurrence lengths differ
    if new != old:
        j = i + len(lead)
        owner = []
        for k, r in enumerate(p.runs):
            owner.extend([k] * len(r.text))
        out = [[] for _ in p.runs]
        for m2 in range(i):
            out[owner[m2]].append(text[m2])
        out[owner[i]].extend(list("[%d]" % new))
        for m2 in range(j, len(text)):
            out[owner[m2]].append(text[m2])
        for r, chs in zip(p.runs, out):
            r.text = "".join(chs)

# reorder ref paragraphs by new number
heading = None
for p in d.paragraphs:
    if p.text.strip().startswith("14. References"):
        heading = p
        break
cursor = heading._p
for new in range(1, nrefs + 1):
    old = [o for o, nn in MAP.items() if nn == new][0]
    el = ref_paras[old]._p
    el.getparent().remove(el)
    cursor.addnext(el)
    cursor = el

d.save(P5)

with open("_draft/renum_p5_to_p6.json", "w", encoding="utf-8") as f:
    json.dump({str(k): v for k, v in MAP.items()}, f, indent=0)
with open("_draft/renum_p6_to_p5.json", "w", encoding="utf-8") as f:
    json.dump({str(v): k for k, v in MAP.items()}, f, indent=0)

print("saved. mapping sample (old->new):")
print("  ", {k: MAP[k] for k in list(MAP)[:20]})
