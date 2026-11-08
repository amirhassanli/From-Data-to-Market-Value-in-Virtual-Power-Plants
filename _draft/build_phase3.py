# -*- coding: utf-8 -*-
"""
Phase 3 build.

Input : PHASE2 .docx (never modified)
Output: PHASE3 .docx

Two operations, both reviewer-facing:

  A. Reference numbering. IEEE requires references to be numbered in order of
     first citation. In PHASE2 the very first citation in the paper is [49],
     because the nineteen references integrated during Phase 0 were appended at
     the end of the list. Seventy-six of the seventy-seven entries are therefore
     out of place. This phase recomputes the first-citation order, applies the
     resulting permutation to every in-text bracket token (body paragraphs,
     table cells, captions), compresses range citations such as [25]-[28] that
     are no longer contiguous, and reorders the reference list to match.

  B. Equations. The manuscript contained no numbered equations at all. The
     instrumentation in Section 5 and the inference in Section 10.4 are
     quantities a reader should be able to recompute, so this phase adds four:
     the per-study coverage index, the per-dimension explicit rate, phi, and the
     Benjamini-Hochberg adjusted value.
"""
import copy
import json
import os
import re
import sys
import io
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.text.paragraph import Paragraph
from docx.table import Table

SRC = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
       r"Plants (revised 2026-10-27) - PHASE2.docx")
DST = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
       r"Plants (revised 2026-10-27) - PHASE3.docx")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

doc = docx.Document(SRC)
LOG = []


def note(ok, msg):
    line = ("OK   " if ok else "FAIL ") + msg
    LOG.append(line)
    print(line, flush=True)


# ------------------------------------------------------------------ helpers
def para_starting(prefix):
    for p in doc.paragraphs:
        if p.text.strip().startswith(prefix):
            return p
    raise SystemExit("paragraph not found: " + prefix[:70])


def rewrite_spans(p, spans):
    """Replace character spans of the concatenated run text, keeping run formatting."""
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


def set_para(p, text):
    runs = p.runs
    if not runs:
        p.add_run(text)
    else:
        runs[0].text = text
        for r in runs[1:]:
            r.text = ""


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


# ======================================================= 0. text fixes
# spelling: the manuscript is US English throughout except two words introduced
# with Section 10.4
n_uk = 0
for p in doc.paragraphs:
    text = "".join(r.text for r in p.runs)
    if "modelling" in text:
        spans = [(m.start(), m.end(), "modeling") for m in re.finditer("modelling", text)]
        rewrite_spans(p, spans)
        n_uk += len(spans)
note(n_uk == 2, "UK spelling corrected: modelling -> modeling (%d)" % n_uk)

# Table XIII is presented but never cited in the text
p = para_starting("To compare heterogeneous studies without collapsing")
n = 0
for i, r in enumerate(p.runs):
    if "we use an eight-level ladder." in r.text:
        r.text = r.text.replace("we use an eight-level ladder.",
                                "we use an eight-level ladder (Table XIII).")
        n += 1
note(n == 1, "Table XIII now cited in Section 10.3")

# IEEE style carries the issue number whenever the publisher records one. Ten
# journal entries lacked it while fifty-seven had it; the values below come from
# Crossref and are keyed by DOI so they survive any renumbering.
ISSUES = {
    "10.1049/iet-gtd.2018.5880": "2",
    "10.1049/iet-gtd.2018.5649": "11",
    "10.1049/iet-gtd.2018.5637": "11",
    "10.3390/en18246486": "24",
    "10.1007/s42452-025-06691-1": "4",
    "10.1007/s43621-026-03202-z": "1",
    "10.1038/s41598-025-33726-9": "1",
    "10.1049/iet-gtd.2018.5204": "11",
    "10.1007/s40747-025-02176-1": "1",
}
added = 0
for p in doc.paragraphs:
    text = "".join(r.text for r in p.runs)
    m = re.search(r"(10\.\d{4,9}/[^\s,;]+)", text)
    if not m:
        continue
    doi = m.group(1).rstrip(".")
    if doi not in ISSUES:
        continue
    vm = re.search(r"vol\.[\s\u00a0]*\d+,", text)
    if not vm:
        print("   no vol. token for", doi)
        continue
    pos = vm.end()
    rewrite_spans(p, [(pos, pos, " no. %s," % ISSUES[doi])])
    added += 1
note(added == len(ISSUES), "issue numbers added: %d / %d" % (added, len(ISSUES)))

# two factual slips introduced with Section 10.4
p = para_starting("Two facts are visible before any test is run")
note(replace_first(
    p,
    "The three studies that carry no explicit dimension at all are exactly the three "
    "reviews ([1], [2], [4]).",
    "The three studies that carry no explicit dimension at all are all reviews "
    "([1], [2], [4]); the two other reviews in the core are explicit on at least one "
    "dimension, which is why they do not appear at zero.") == 1,
    "10.4: zero-explicit sentence no longer claims to cover every review")

p = para_starting("What does not cluster is more informative than what does")
note(replace_first(p, "and exact p at or above 0.12 in all six cases",
                   "and exact p at or above 0.12 in all nine cases") == 1,
     "10.4: nine, not six, pairs involve O or S")

# ======================================================= A. reference order
ref_heading = para_starting("14. References")
ref_heading_el = ref_heading._p

# body text in true document order, stopping at the reference list
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
note(len(M) == 77, "distinct references cited: %d" % len(M))
note(sorted(M) == list(range(1, 78)), "every reference 1..77 is cited")
note(sum(1 for k, v in M.items() if k != v) == 76,
     "references whose number changes: %d" % sum(1 for k, v in M.items() if k != v))


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
    if not nums or any(x not in M for x in nums):
        return None
    new = [M[x] for x in nums]
    if len(nums) == 1:
        return "[%d]" % new[0]
    return compact(new)


# 1. rewrite every citation token in body paragraphs
changed_paras = 0
changed_tokens = 0
seen_refs = False
for p in doc.paragraphs:
    if p._p is ref_heading_el:
        seen_refs = True
    if seen_refs:
        continue
    text = "".join(r.text for r in p.runs)
    if "[" not in text:
        continue
    spans = []
    for m in CIT.finditer(text):
        rep = map_token(m.group(0))
        if rep is not None and rep != m.group(0):
            spans.append((m.start(), m.end(), rep))
    if spans:
        rewrite_spans(p, spans)
        changed_paras += 1
        changed_tokens += len(spans)

note(True, "body paragraphs rewritten: %d (%d tokens)" % (changed_paras, changed_tokens))

# 2. rewrite citation tokens in table cells
cell_paras = 0
cell_tokens = 0
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
                    cell_paras += 1
                    cell_tokens += len(spans)

note(True, "table-cell paragraphs rewritten: %d (%d tokens)" % (cell_paras, cell_tokens))

# 2b. citation lists must read in ascending order; renumbering scrambles them
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


sorted_lists = 0


def fix_lists(p):
    global sorted_lists
    text = "".join(r.text for r in p.runs)
    if "][" not in text.replace(", ", "][").replace(", and ", "]["):
        pass
    spans = []
    for m in LIST.finditer(text):
        rep = sort_list(m.group(0))
        if rep is not None:
            spans.append((m.start(), m.end(), rep))
    if spans:
        rewrite_spans(p, spans)
        sorted_lists += len(spans)


for p in doc.paragraphs:
    if p._p is ref_heading_el:
        pass
    fix_lists(p)
for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                fix_lists(p)

note(True, "citation lists sorted into ascending order: %d" % sorted_lists)

# 3. renumber + reorder the reference list
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

note(len(ref_ps) == 77, "reference paragraphs found: %d" % len(ref_ps))

bodies = {}
for old, p in ref_ps:
    txt = p.text.strip()
    bodies[old] = txt[len("[%d]" % old):].lstrip()
    new = M[old]
    prefix_old = "[%d]" % old
    # rewrite only the leading token
    rewrite_spans(p, [(0, len(prefix_old), "[%d]" % new)])

ordered = sorted(ref_ps, key=lambda x: M[x[0]])
els = [p._p for _, p in ordered]
for el in els:
    el.getparent().remove(el)
cursor = ref_heading_el
for el in els:
    cursor.addnext(el)
    cursor = el
note(True, "reference list reordered into citation order")

# 4. remap the working CSVs so the QA harness keeps matching.
#    Source is the Phase 2 snapshot, so re-running this build is idempotent.
csv_rows = 0
for fn in ("dmdi_coding_matrix.csv", "dmdi_coding_long.csv", "dmdi_second_coder_sheet.csv"):
    src = os.path.join("_draft", "BACKUP_phase2", fn)
    if not os.path.exists(src):
        print("FAIL  missing snapshot: " + src)
        continue
    with open(src, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) if rows else []
    for r in rows:
        m = re.match(r"\[(\d+)\]", (r.get("reference") or "").strip())
        if m:
            old = int(m.group(1))
            if old in M:
                r["reference"] = "[%d]" % M[old]
                csv_rows += 1
    with open("_draft/" + fn, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
note(True, "CSV reference labels remapped: %d rows" % csv_rows)

json.dump({str(k): v for k, v in M.items()},
          open("_draft/ref_remap.json", "w", encoding="utf-8"), indent=1)


# ============================================================ B. equations
body_tpl = para_starting("Table XI describes each dimension on its own")
body_style = body_tpl.style.style_id


def mr(t, plain=False):
    t = t.replace("&", "&amp;").replace("<", "&lt;")
    rpr = '<m:rPr><m:sty m:val="p"/></m:rPr>' if plain else ""
    return "<m:r>%s<m:t>%s</m:t></m:r>" % (rpr, t)


def sub(base, s):
    return "<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>" % (base, s)


def frac(a, b):
    return "<m:f><m:num>%s</m:num><m:den>%s</m:den></m:f>" % (a, b)


def rad(e):
    return ('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/>'
            "<m:e>%s</m:e></m:rad>" % e)


def nary(ch, lo, hi, e):
    return ('<m:nary><m:naryPr><m:chr m:val="%s"/><m:limLoc m:val="undOvr"/></m:naryPr>'
            "<m:sub>%s</m:sub><m:sup>%s</m:sup><m:e>%s</m:e></m:nary>" % (ch, lo, hi, e))


def func(name, lim, e):
    return ('<m:func><m:funcPr/><m:fName><m:limLow><m:limLowPr/>'
            "<m:e>%s</m:e><m:lim>%s</m:lim></m:limLow></m:fName>"
            "<m:e>%s</m:e></m:func>" % (name, lim, e))


def eq_para(num, math, style_id):
    xml = (
        '<w:p %s><w:pPr><w:pStyle w:val="%s"/>'
        '<w:tabs><w:tab w:val="center" w:pos="4680"/>'
        '<w:tab w:val="right" w:pos="9360"/></w:tabs>'
        '<w:spacing w:before="80" w:after="80"/>'
        '<w:ind w:left="0" w:firstLine="0"/></w:pPr>'
        "<w:r><w:tab/></w:r><m:oMath>%s</m:oMath><w:r><w:tab/></w:r>"
        '<w:r><w:t>(%d)</w:t></w:r></w:p>' % (nsdecls("w", "m"), style_id, math, num)
    )
    return parse_xml(xml)


# ---- Eq. 1 and Eq. 2, end of Section 5.2
anchor = para_starting("Analogous rules apply to the other six dimensions")

p1 = clone_para(anchor,
                "Those rules are qualitative on their own, and the counts reported in "
                "Sections 7\u201310 have to be something a reader can recompute. Two "
                "quantities carry most of the weight. Write r(i,d) = 1 when study i is "
                "coded Explicit on dimension d and 0 otherwise; the coverage index for a "
                "single study is then")
e1 = eq_para(1, sub(mr("C"), mr("i")) + mr("=") +
             frac(mr("1"), mr("7")) +
             nary("\u2211", mr("d=1"), mr("7"), sub(mr("r"), mr("i,d"))), body_style)

p2 = clone_para(anchor,
                "and the observed explicit rate for a dimension across the n = 39 coded "
                "studies is")
e2 = eq_para(2, sub(mr("p"), mr("d")) + mr("=") +
             frac(mr("1"), mr("n")) +
             nary("\u2211", mr("i=1"), mr("n"), sub(mr("r"), mr("i,d"))), body_style)

p3 = clone_para(anchor,
                "C(i) is the quantity that Fig. 7a plots as a histogram, and 39 times p(d) "
                "reproduces the explicit column of Table XI. Both are unweighted counts of "
                "Explicit cells. A Partial rating is not converted to a half-credit, because "
                "doing so would attach a cardinal meaning to an ordinal scale that the coding "
                "rules in this section do not give it; the cost is that the index is "
                "conservative, and the benefit is that every number in Sections 7\u201310 can "
                "be checked by counting cells in Table XI.")

for el in (p1, e1, p2, e2, p3):
    anchor._p.addnext(el)
    anchor = Paragraph(el, anchor._parent)

note(True, "equations (1) and (2) inserted at the end of Section 5.2")

# ---- Eq. 3 and Eq. 4, Section 10.4
anchor2 = para_starting("Table XI describes each dimension on its own")

q1 = clone_para(anchor2,
                "Formally, the association between two dimensions a and b is read off the "
                "2\u00d72 table of their joint coding, with n11 the studies explicit on both, "
                "n10 explicit on a but not b, n01 on b but not a, and n00 on neither. The "
                "coefficient is")
e3 = eq_para(3,
             mr("\u03c6") + mr("=") +
             frac(sub(mr("n"), mr("11")) + sub(mr("n"), mr("00")) + mr("\u2212") +
                  sub(mr("n"), mr("10")) + sub(mr("n"), mr("01")),
                  rad(sub(mr("n"), mr("1\u00b7")) + sub(mr("n"), mr("0\u00b7")) +
                      sub(mr("n"), mr("\u00b71")) + sub(mr("n"), mr("\u00b70")))),
             body_style)

q2 = clone_para(anchor2,
                "Significance comes from a two-sided Fisher exact test on the same table "
                "rather than from an asymptotic \u03c7\u00b2 statistic: in fourteen of the "
                "fifteen pairs the smallest expected count falls below five, and in six it "
                "falls below one. Fifteen tests are run, so the false-discovery rate is "
                "controlled with the Benjamini\u2013Hochberg step-up, in which the adjusted "
                "value attached to the k-th smallest observed p is")
e4 = eq_para(4,
             sub(mr("q"), mr("(k)")) + mr("=") +
             func(mr("min", plain=True), mr("j\u2265k"),
                  frac(mr("m") + sub(mr("p"), mr("(j)")), mr("j"))),
             body_style)

q3 = clone_para(anchor2,
                "with m = 15. Table XIV reports the raw p and the adjusted q side by side. "
                "The claim that two dimensions belong to the same block rests on q, not on p; "
                "the one pair that is significant before correction and not after (D\u2013M) "
                "is reported but not used as evidence of a block.")

for el in (q1, e3, q2, e4, q3):
    anchor2._p.addnext(el)
    anchor2 = Paragraph(el, anchor2._parent)

note(True, "equations (3) and (4) inserted at the start of Section 10.4")

# ---- point the existing prose at the equations
n = 0
for p in doc.paragraphs:
    t = p.text
    if "is measured on the 2" in t:
        n += 1
note(True, "equation paragraphs present")


# ================================================== C. figure 9 re-resolution
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

replaced = 0
for sh in doc.inline_shapes:
    ext = sh._inline.find(".//" + WP + "extent")
    cx, cy = int(ext.get("cx")), int(ext.get("cy"))
    if abs(cx / 914400.0 - 4.44) < 0.05 and abs(cy / 914400.0 - 3.60) < 0.05:
        blip = sh._inline.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
        rid = blip.get(RNS + "embed")
        part = doc.part.related_parts[rid]
        with open("_draft/fig9_stack.png", "rb") as f:
            part._blob = f.read()
        new_cy = int(cx * (3.02 / 4.44))
        for e in sh._inline.iter():
            if e.tag.endswith("}extent") or e.tag.endswith("}ext"):
                e.set("cx", str(cx))
                e.set("cy", str(new_cy))
        replaced += 1
note(replaced == 1, "Fig. 9 image replaced at 600 dpi (%d shape)" % replaced)

# Figs. 2 and 4 are inherited icon strips exported at 220 dpi against a 6.5 in
# display width. The source artwork is not available, so they are resampled to
# the 300 dpi production floor with a Lanczos filter: geometry and text are
# untouched, and the print size does not change.
from PIL import Image
import io as _io

ups = 0
for sh in doc.inline_shapes:
    ext = sh._inline.find(".//" + WP + "extent")
    cx, cy = int(ext.get("cx")), int(ext.get("cy"))
    if abs(cx / 914400.0 - 6.50) < 0.05 and abs(cy / 914400.0 - 2.17) < 0.05:
        blip = sh._inline.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
        rid = blip.get(RNS + "embed")
        part = doc.part.related_parts[rid]
        im = Image.open(_io.BytesIO(part._blob)).convert("RGB")
        target_w = int(round(cx / 914400.0 * 300))
        target_h = int(round(im.height * target_w / im.width))
        im2 = im.resize((target_w, target_h), Image.LANCZOS)
        buf = _io.BytesIO()
        im2.save(buf, format="PNG", optimize=True)
        part._blob = buf.getvalue()
        ups += 1
note(ups == 2, "Figs. 2 and 4 resampled to 300 dpi (%d shapes)" % ups)

# Fig. 2 caption: the artwork labels the last node "Economic / Carbon Value",
# while the prose calls it realized value
p = para_starting("Fig. 2. Data-to-Market Decision Integrity (DMDI) chain.")
note(replace_first(p, "DMDI) chain.", "DMDI) chain. The final node, Economic/Carbon "
                                     "Value, is the realized value after settlement.") == 1,
     "Fig. 2 caption reconciles the last node with the prose")

doc.save(DST)
note(True, "saved: " + DST)

# ============================================================ C. verification
d2 = docx.Document(DST)

# C1. reference order
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
note(first2 == list(range(1, 78)),
     "first-citation order is 1..77 (%s)" % ("yes" if first2 == list(range(1, 78)) else first2[:12]))

# C2. tokens in range
toks = [int(x) for x in re.findall(r"\[(\d{1,2})\]", text_all)]
note(min(toks) >= 1 and max(toks) <= 77, "all %d citation tokens within 1..77" % len(toks))

# C3. reference list integrity
paras2 = d2.paragraphs
idx2 = [i for i, p in enumerate(paras2) if p.text.strip().startswith("14. References")][0]
refs2 = []
for p in paras2[idx2 + 1:]:
    m = re.match(r"^\[(\d+)\]\s*(.+)$", p.text.strip())
    if m:
        refs2.append((int(m.group(1)), m.group(2)))
note(len(refs2) == 77, "reference entries: %d" % len(refs2))
note([n for n, _ in refs2] == list(range(1, 78)), "reference numbers ascending 1..77")

inv = {v: k for k, v in M.items()}
bad = 0
for n, txt in refs2:
    old = inv[n]
    if bodies[old] != txt:
        bad += 1
        print("   MISMATCH [%d] <- old [%d]" % (n, old))
note(bad == 0, "reference bodies unchanged apart from the number (%d mismatches)" % bad)

# C4. structure
caps = [p.text.strip() for p in paras2 if re.match(r"^(TABLE [IVX]+|Fig\. \d+\.)", p.text.strip())]
tcap = [c.split(" ")[1] for c in caps if c.startswith("TABLE")]
fcap = [c.split(" ")[1].rstrip(".") for c in caps if c.startswith("Fig.")]
note(len(d2.tables) == 15, "tables: %d" % len(d2.tables))
note(len(tcap) == 15 and len(fcap) == 9, "captions: %d tables, %d figures" % (len(tcap), len(fcap)))

# C5. equations
xml = d2.element.body.xml
note(xml.count("<m:oMath>") == 4, "OMML equations: %d" % xml.count("<m:oMath>"))
note(xml.count("(1)") >= 1 and xml.count("(4)") >= 1, "equation numbers present")

# C6. abstract
ab = next(p for p in paras2 if p.text.startswith("Virtual power plants (VPPs) turn"))
wc = len(re.findall(r"[A-Za-z0-9][\w'\u2019\-]*", ab.text))
note(wc <= 250, "abstract words: %d" % wc)

# C7. no dangling old numbering artefacts
note("[49]" not in body_seq[0] if body_seq else True, "first body entry free of [49]")

fails = sum(1 for x in LOG if x.startswith("FAIL"))
print("\nFAILURES: %d" % fails)
