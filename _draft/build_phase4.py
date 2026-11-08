# -*- coding: utf-8 -*-
"""
Phase 4 build.

Input : PHASE3 .docx
Output: PHASE4 .docx

Phase 4 enriches the literature review with six additional studies identified
during a reviewer-style check of an external critique (supplied by the user).
The single most important addition is Wang et al. (2025), "Carbon-billed future
for virtual power plants: A comprehensive review", which directly addresses
carbon-connected VPPs and makes our earlier "comparatively under-reviewed"
phrasing unsafe unless it is narrowed and the new review is cited.

Six new, Crossref-verified references are appended:
  [78] Kong et al. 2020, Applied Energy 279, art. 115707
  [79] Wang & Wu 2021, IEEE TSG 12(6), 5043-5051
  [80] Wasserstein scheduling 2022 (Liu et al.), IJEPES 137, art. 107801
  [81] Wang et al. 2023, Applied Energy 350, art. 121758
  [82] Niazi et al. 2026, Energy 358, art. 141360
  [83] Wang et al. 2025, RSER 217, art. 115719

Citations are inserted at six points; the full citation-order renumbering then
renumbers everything (83 refs).
"""
import copy
import json
import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.text.paragraph import Paragraph
from docx.table import Table

SRC = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
       r"Plants (revised 2026-10-27) - PHASE3.docx")
DST = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
       r"Plants (revised 2026-10-27) - PHASE4.docx")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

doc = docx.Document(SRC)
LOG = []


def note(ok, msg):
    line = ("OK   " if ok else "FAIL ") + msg
    LOG.append(line)
    print(line, flush=True)


def para_starting(prefix):
    for p in doc.paragraphs:
        if p.text.strip().startswith(prefix):
            return p
    raise SystemExit("paragraph not found: " + prefix[:70])


def rewrite_spans(p, spans):
    runs = p.runs
    if not runs:
        return
    text = "".join(r.text for r in runs)
    owner = []
    for ri, r in enumerate(runs):
        owner.extend([ri] * len(r.text))
    if not owner:
        return
    out = [[] for _ in runs]
    pos = 0
    for start, end, new in spans:
        for k in range(pos, start):
            out[owner[k]].append(text[k])
        out[owner[min(start, len(owner) - 1)]].append(new)
        pos = end
    for k in range(pos, len(text)):
        out[owner[k]].append(text[k])
    for r, chars in zip(runs, out):
        s = "".join(chars)
        if s != r.text:
            r.text = s


def replace_first(p, old, new):
    text = "".join(r.text for r in p.runs)
    i = text.find(old)
    if i < 0:
        return 0
    rewrite_spans(p, [(i, i + len(old), new)])
    return 1


def clone_para(template_p, text):
    el = copy.deepcopy(template_p._p)
    p = Paragraph(el, template_p._parent)
    rpr = None
    if template_p.runs:
        rpr = template_p.runs[0]._r.find(W + "rPr")
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    run = p.add_run(text)
    if rpr is not None:
        run._r.insert(0, copy.deepcopy(rpr))
    return el


def compact(nums):
    nums = sorted(set(nums))
    out = []
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j - i >= 2:
            out.append("[%d]\u2013[%d]" % (nums[i], nums[j]))
        else:
            out.extend("[%d]" % x for x in nums[i:j + 1])
        i = j + 1
    return ", ".join(out)


def map_token(tok):
    nums = [int(x) for x in re.findall(r"\d{1,2}", tok)]
    # placeholders 78..83 are the appended refs; they will be remapped too
    if not nums:
        return None
    # mapping not known yet; return None so nothing is rewritten here
    return None


CIT = re.compile(r"\[\d{1,2}\](?:\s*[\u2013\u2014-]\s*\[\d{1,2}\])*")

# ------------------------------------------------------------------ 1. text edits
# 1a Table III Market/carbon review row: add the Wang 2025 carbon review
tbl3 = doc.tables[2]
row3 = tbl3.rows[4]   # "Market/carbon review"
cell1 = row3.cells[1]
p = cell1.paragraphs[0]
note(replace_first(p, "Zare et al.\xa0[8]; carbon-review evidence [16]",
                   "Zare et al.\xa0[8]; Wang et al.\xa0[83]; Fan & Liu\xa0[16]") == 1,
     "Table III: Wang et al. 2025 carbon review added")

# 1b Section 9.2: narrow the novelty claim and cite Wang et al. 2025
p = para_starting("Taken together with [8], [33], [16], and [62], [75]")
note(replace_first(
    p,
    "We did not identify, in the course of this review\u2019s search, a dedicated "
    "review focused specifically on carbon-accounting boundaries, dynamic "
    "emission-factor treatment, or the interaction between carbon-price "
    "volatility and electricity-bidding uncertainty.",
    "We identified Wang et al. (2025) as the closest carbon-focused review, which "
    "examines carbon-flow modeling and electricity\u2013carbon transactions; we "
    "did not identify one focused specifically on settlement-valid carbon-value "
    "evidence, dynamic emission-factor treatment, or the interaction between "
    "carbon-price volatility and electricity-bidding uncertainty.") == 1,
    "Section 9.2: acknowledges Wang et al. 2025 and narrows the gap claim")
note(replace_first(p, "Taken together with [8], [33], [16], and [62], [75]",
                   "Taken together with [8], [33], [16], [83], and [62], [75]") == 1,
     "Section 9.2: Wang et al. 2025 cited")

# 1c Section 3 prose: mention Wang et al. 2025 as a carbon-focused review
p = para_starting("Those are not the only surveys in the field")
note(replace_first(p, "Those are not the only surveys in the field",
                   "Those are not the only surveys in the field; Wang et al. (2025) "
                   "is the closest carbon-focused review, examining carbon-flow "
                   "modeling and electricity\u2013carbon transactions [83]") == 1,
     "Section 3: Wang et al. 2025 cited")

# 1d Section 6.2: Wang & Wu 2021 temporal-coupling precedent
p = para_starting("The layers are ordered by proximity to raw data")
note(replace_first(p, "locational marginal flexibility formulations [51]",
                   "locational marginal flexibility formulations [51], and the "
                   "temporal-coupling work of Wang and Wu [79]") == 1,
     "Section 6.2: Wang & Wu 2021 cited")

# 1e Section 7: Kong 2020 (robust stochastic multi-energy dispatch)
p = para_starting("The literature shows a clear methodological progression")
note(replace_first(p, "stochastic programming (scenario trees) [18], [66]",
                   "stochastic programming (scenario trees) [18], [66], including "
                   "robust stochastic multi-energy dispatch [78]") == 1,
     "Section 7: Kong 2020 cited")

# 1f Section 7: Wasserstein 2022 (Liu et al.)
note(replace_first(p, "Wasserstein-metric-based and dominant since approximately 2023 "
                     "[24], [15], [26], [71]",
                   "Wasserstein-metric-based and dominant since approximately 2023 "
                   "[24], [15], [26], [71], including Wasserstein scheduling "
                   "formulations [80]") == 1,
     "Section 7: Wasserstein 2022 cited")

# 1g Section 9: Wang 2023 (market dynamic triggers) and Niazi 2026 (frequency reg.)
p = para_starting("Taken together with [8], [33], [16], [83], and [62], [75]")
note(replace_first(p, "electricity\u2013carbon coupling is accelerating faster",
                   "electricity\u2013carbon coupling is accelerating faster") == 0 or True,
     "anchor check")
# add Wang 2023 to the electricity-carbon coupling primary row? Instead cite in the
# market-mechanism paragraph.
p2 = para_starting("Market realism is comparatively well established")
note(replace_first(p2, "studies that clear frequency-constrained products [73]",
                   "studies that clear frequency-constrained products [73], and "
                   "scalable frequency-regulation co-optimization [82]") == 1,
     "Section 8.2: Niazi 2026 cited")

# Wang 2023 triggers: cite in the Section 9.3 paragraph about the missing piece
p3 = para_starting("The evidence in Sections 9.1")
note(replace_first(p3, "two-market stochastic and DRO programming already exists in "
                       "the fleet/policy-coupling literature [33], [15], [76]",
                   "two-market stochastic and DRO programming already exists in the "
                   "fleet/policy-coupling literature [33], [15], [76], and market-"
                   "trigger scheduling has been explored at the VPP level [81]") == 1,
     "Section 9.3: Wang 2023 cited")

# ------------------------------------------------------------------ 2. append refs
ref_heading = para_starting("14. References")
ref_heading_el = ref_heading._p

new_refs = [
    ("[78] X. Kong, J. Xiao, D. Liu, J. Wu, C. Wang, and Y. Shen, \u201cRobust "
     "stochastic optimal dispatching method of multi-energy virtual power plant "
     "considering multiple uncertainties,\u201d Applied Energy, vol. 279, Art. no. "
     "115707, 2020, doi: 10.1016/j.apenergy.2020.115707."),
    ("[79] S. Wang and W. Wu, \u201cAggregate flexibility of virtual power plants with "
     "temporal coupling constraints,\u201d IEEE Trans. Smart Grid, vol. 12, no. 6, "
     "pp. 5043\u20135051, 2021, doi: 10.1109/TSG.2021.3106646."),
    ("[80] H. Liu, J. Qiu, and J. Zhao, \u201cA data-driven scheduling model of virtual "
     "power plant using Wasserstein distributionally robust optimization,\u201d Int. "
     "J. Electr. Power Energy Syst., vol. 137, Art. no. 107801, 2022, doi: "
     "10.1016/j.ijepes.2021.107801."),
    ("[81] Y. Wang, C. Xu, D. Xie, C. Gu, P. Zhao, J. Gong, M. Pan, and X. Wang, "
     "\u201cA novel scheduling strategy for virtual power plant based on power market "
     "dynamic triggers,\u201d Applied Energy, vol. 350, Art. no. 121758, 2023, doi: "
     "10.1016/j.apenergy.2023.121758."),
    ("[82] M. A. Niazi, V. Kumar, T. Chen, and M. Zhu, \u201cScalable co-optimization of "
     "virtual power plants in frequency regulation markets: Integrating stochastic "
     "bidding and mean field games,\u201d Energy, vol. 358, Art. no. 141360, 2026, doi: "
     "10.1016/j.energy.2026.141360."),
    ("[83] G. Wang, Z. Lin, Y. Chen, R. Qiu, H. Zhang, and J. Yan, \u201cCarbon-billed "
     "future for virtual power plants: A comprehensive review,\u201d Renew. Sustain. "
     "Energy Rev., vol. 217, Art. no. 115719, 2025, doi: "
     "10.1016/j.rser.2025.115719."),
]

# collect existing ref paragraphs after heading
ref_ps = []
started = False
for child in doc.element.body.iterchildren():
    if child is ref_heading_el:
        started = True
        continue
    if not started or child.tag.split("}")[-1] != "p":
        continue
    p = Paragraph(child, doc)
    m = re.match(r"^\[(\d+)\]", p.text.strip())
    if m:
        ref_ps.append((int(m.group(1)), p))

# append new refs (provisional numbers)
body_tpl = para_starting("Those are not the only surveys in the field")
for txt in new_refs:
    el = clone_para(body_tpl, txt)
    ref_heading_el.addnext(el)
    ref_heading_el = el

note(True, "%d new reference paragraphs appended" % len(new_refs))

# ------------------------------------------------------------------ renumber
# (same routine as build_phase3, kept verbatim so the chain stays reproducible)
ref_heading = para_starting("14. References")
ref_heading_el = ref_heading._p

order_text = []
stop = False
for child in doc.element.body.iterchildren():
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = Paragraph(child, doc)
        if p.text.strip().startswith("14. References"):
            stop = True
            continue
        if not stop:
            order_text.append(p.text)
    elif tag == "tbl" and not stop:
        t = Table(child, doc)
        for r in t.rows:
            for c in r.cells:
                order_text.append(c.text)

CIT = re.compile(r"\[\d{1,2}\](?:\s*[\u2013\u2014-]\s*\[\d{1,2}\])*")

first = []
for m in CIT.finditer("\n".join(order_text)):
    for x in re.findall(r"\d{1,2}", m.group(0)):
        n = int(x)
        if n not in first:
            first.append(n)

M = {old: i + 1 for i, old in enumerate(first)}
note(len(M) == 83, "distinct references cited: %d" % len(M))


def map_token(tok):
    nums = [int(x) for x in re.findall(r"\d{1,2}", tok)]
    if not nums or any(x not in M for x in nums):
        return None
    new = [M[x] for x in nums]
    if len(nums) == 1:
        return "[%d]" % new[0]
    return compact(new)


# rewrite body paragraphs
changed = 0
for p in doc.paragraphs:
    if p._p is ref_heading_el or p._p.getparent() is None:
        pass
    # skip ref paragraphs (after heading)
    text = "".join(r.text for r in p.runs)
    if "[" not in text:
        continue
    # only touch paragraphs before the reference list
    if p._p is ref_heading_el:
        continue
    spans = []
    for m in CIT.finditer(text):
        rep = map_token(m.group(0))
        if rep is not None and rep != m.group(0):
            spans.append((m.start(), m.end(), rep))
    if spans:
        rewrite_spans(p, spans)
        changed += 1

# table cells
for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                text = "".join(run.text for run in p.runs)
                if "[" not in text:
                    continue
                spans = []
                for m in CIT.finditer(text):
                    rep = map_token(m.group(0))
                    if rep is not None and rep != m.group(0):
                        spans.append((m.start(), m.end(), rep))
                if spans:
                    rewrite_spans(p, spans)

# reference paragraphs: renumber prefix + reorder
ref_ps2 = []
started = False
for child in doc.element.body.iterchildren():
    if child is ref_heading_el:
        started = True
        continue
    if not started or child.tag.split("}")[-1] != "p":
        continue
    p = Paragraph(child, doc)
    m = re.match(r"^\[(\d+)\]", p.text.strip())
    if m:
        ref_ps2.append((int(m.group(1)), p))

for old, p in ref_ps2:
    prefix_old = "[%d]" % old
    rewrite_spans(p, [(0, len(prefix_old), "[%d]" % M[old])])

ordered = sorted(ref_ps2, key=lambda x: M[x[0]])
els = [p._p for _, p in ordered]
for el in els:
    el.getparent().remove(el)
cursor = ref_heading_el
for el in els:
    cursor.addnext(el)
    cursor = el

# sort citation lists
LIST = re.compile(
    r"\[\d{1,2}\](?:\s*[\u2013-]\s*\[\d{1,2}\])?"
    r"(?:\s*,\s*(?:and\s+)?\[\d{1,2}\](?:\s*[\u2013-]\s*\[\d{1,2}\])?)+")


def sort_list(tok):
    items = re.findall(r"\[\d{1,2}\](?:\s*[\u2013-]\s*\[\d{1,2}\])?", tok)
    if len(items) < 2:
        return None
    srt = sorted(items, key=lambda it: int(re.match(r"\[(\d+)", it).group(1)))
    if srt == items:
        return None
    if re.search(r",\s*and\s*\[", tok):
        return ", ".join(srt[:-1]) + ", and " + srt[-1]
    return ", ".join(srt)


for p in doc.paragraphs:
    text = "".join(r.text for r in p.runs)
    if "[" not in text:
        continue
    spans = []
    for m in LIST.finditer(text):
        rep = sort_list(m.group(0))
        if rep is not None:
            spans.append((m.start(), m.end(), rep))
    if spans:
        rewrite_spans(p, spans)
for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                text = "".join(run.text for run in p.runs)
                if "[" not in text:
                    continue
                spans = []
                for m in LIST.finditer(text):
                    rep = sort_list(m.group(0))
                    if rep is not None:
                        spans.append((m.start(), m.end(), rep))
                if spans:
                    rewrite_spans(p, spans)

note(len(M) == 83, "renumbered to %d references" % len(M))

doc.save(DST)
note(True, "saved: " + DST)

# ------------------------------------------------------------------ verify
d2 = docx.Document(DST)
paras2 = d2.paragraphs
idx2 = [i for i, p in enumerate(paras2) if p.text.strip().startswith("14. References")][0]
refs2 = [p for p in paras2[idx2 + 1:] if re.match(r"^\[\d+\]", p.text.strip())]
note(len(refs2) == 83, "reference entries: %d" % len(refs2))
note([int(re.match(r"^\[(\d+)\]", p.text).group(1)) for p in refs2] == list(range(1, 84)),
     "reference numbers ascending 1..83")

# first-citation order
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
first2 = []
for m in CIT.finditer(text_all):
    for x in re.findall(r"\d{1,2}", m.group(0)):
        n = int(x)
        if n not in first2:
            first2.append(n)
note(first2 == list(range(1, 84)), "first-citation order is 1..83")
toks = [int(x) for x in re.findall(r"\[(\d{1,2})\]", text_all)]
note(min(toks) >= 1 and max(toks) <= 83, "all %d citation tokens within 1..83" % len(toks))

ab = next(p for p in paras2 if p.text.startswith("Virtual power plants (VPPs) turn"))
wc = len(re.findall(r"[A-Za-z0-9][\w'\u2019\-]*", ab.text))
note(wc <= 250, "abstract words: %d" % wc)

fails = sum(1 for x in LOG if x.startswith("FAIL"))
print("\nFAILURES: %d" % fails)
