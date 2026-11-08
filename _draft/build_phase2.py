# -*- coding: utf-8 -*-
"""
Phase 2 build.

Input : PHASE1 .docx (never modified)
Output: PHASE2 .docx

What this phase does
  1. Adds Section 10.4, a quantitative layer over the validated 39 x 8 coding
     matrix: explicit-dimension distribution, pairwise association with exact
     tests and Benjamini-Hochberg control, temporal trend, and the O/S
     disjointness result.
  2. Adds Table XIV (pairwise associations) and Fig. 7 (structure), which shifts
     Table XIV to XV and Figs. 7-8 to 8-9.
  3. Fixes three defects found while cross-checking the tables against the matrix:
       - Table IX attributed the pay-as-bid study to [28]; it is [36].
       - Table IX coded [8] settlement as Explicit; the matrix codes it Partial.
       - Table X includes [21], which lies outside the DMDI-coded core; Section
         9.1 said the scheme was applied to core studies only.
"""
import copy
import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power Plants (revised 2026-10-27) - PHASE1.docx"
DST = r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power Plants (revised 2026-10-27) - PHASE2.docx"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

S = json.load(open("_draft/phase2_stats.json", encoding="utf-8"))
PAIRS = {(p["a"], p["b"]): p for p in S["pairs"]}
for p in S["pairs"]:
    PAIRS[(p["b"], p["a"])] = p

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
    raise SystemExit("paragraph not found: " + prefix[:60])


def replace_in(p, old, new):
    runs = p.runs
    text = "".join(r.text for r in runs)
    idx = text.find(old)
    if idx < 0:
        return 0
    end = idx + len(old)
    pos = 0
    s = e = None
    so = eo = 0
    for ri, r in enumerate(runs):
        rl = len(r.text)
        if s is None and pos + rl > idx:
            s, so = ri, idx - pos
        if e is None and pos + rl >= end:
            e, eo = ri, end - pos
        pos += rl
    if s is None or e is None:
        return 0
    if s == e:
        runs[s].text = runs[s].text[:so] + new + runs[s].text[eo:]
    else:
        runs[s].text = runs[s].text[:so] + new
        for k in range(s + 1, e):
            runs[k].text = ""
        runs[e].text = runs[e].text[eo:]
    return 1


def set_para(p, text):
    runs = p.runs
    if not runs:
        p.add_run(text)
    else:
        runs[0].text = text
        for r in runs[1:]:
            r.text = ""


def new_para(template_p, text, parent=None):
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


def set_cell(cell, text, bold=False):
    for extra in cell.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    p = cell.paragraphs[0]
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.add_run(text)
    for r in p.runs:
        r.bold = bold


# ============================================================ 1. renumber
n89 = n78 = nxiv = 0
for p in doc.paragraphs:
    for _ in range(4):
        if replace_in(p, "Fig. 8", "Fig. 9"):
            n89 += 1
        else:
            break
note(n89 == 2, "Fig. 8 -> Fig. 9 (%d)" % n89)

for p in doc.paragraphs:
    for _ in range(4):
        if replace_in(p, "Fig. 7", "Fig. 8"):
            n78 += 1
        else:
            break
note(n78 == 2, "Fig. 7 -> Fig. 8 (%d)" % n78)

for p in doc.paragraphs:
    if p.text.strip().startswith("TABLE XIV"):
        nxiv += replace_in(p, "TABLE XIV", "TABLE XV")
        break
for p in doc.paragraphs:
    for _ in range(3):
        if replace_in(p, "Table XIV", "Table XV"):
            nxiv += 1
        else:
            break
note(nxiv == 2, "Table XIV -> Table XV (%d)" % nxiv)


# ============================================================ 2. Table IX fixes
t9 = doc.tables[8]
hdr9 = [c.text.strip() for c in t9.rows[0].cells]
assert hdr9[2] == "Settlement", hdr9

fixed_ref = fixed_s = 0
for r in t9.rows[1:]:
    c0 = r.cells[0]
    if "[28]" in c0.text:
        replace_in(c0.paragraphs[0], "[28]", "[36]")
        fixed_ref += 1
    if "[8]" in c0.text and "Kim" in c0.text:
        set_cell(r.cells[2], "Partial")
        fixed_s += 1
note(fixed_ref == 1, "Table IX: pay-as-bid study renumbered [28] -> [36]")
note(fixed_s == 1, "Table IX: [8] settlement aligned to matrix (Explicit -> Partial)")


# ============================================================ 3. Table X scope
p = para_starting("Carbon integration is often recorded only as present or absent")
n = replace_in(p,
               "applied qualitatively to the carbon-relevant verified-core studies:",
               "applied qualitatively to the carbon-relevant studies. Table X covers six "
               "studies from the DMDI-coded core plus [21], which is cited in Section 9.2 but "
               "falls outside that coding set:")
note(n == 1, "Section 9.1 states the Table X scope explicitly")


# ============================================================ 4. Section 10.4
anchor = para_starting("11. Cross-Layer Evidence Gaps and a Research Agenda")
anchor_el = anchor._p

h2_tpl = para_starting("10.3 The Data-to-Market Maturity Ladder")
body_tpl = para_starting("DMDI (Section 5) codes what evidence a study provides")
cap_tpl = para_starting("TABLE XI —")
figcap_tpl = para_starting("Fig. 6. Data-to-Market Maturity Ladder coverage")

# a Captioned Figure paragraph to clone for the image
fig_tpl = None
for pp in doc.paragraphs:
    if pp.style.name == "Captioned Figure":
        fig_tpl = pp
        break
if fig_tpl is None:
    raise SystemExit("no Captioned Figure template")

elems = []

elems.append(new_para(h2_tpl, "10.4 The statistical structure of the verified-core coding"))

elems.append(new_para(body_tpl,
    "Table XI describes each dimension on its own. It does not say whether the dimensions "
    "move together, and that matters for how the central claim of this review should be read. "
    "If out-of-sample validity and settlement realism were rare only among studies that are "
    "also weak on information, uncertainty, decision, and market integrity, then the diagnosis "
    "would reduce to a statement about study quality in general, and little would follow from "
    "it beyond a call for better papers. So we examined the joint structure of the coded "
    "matrix rather than the marginals alone."))

elems.append(new_para(body_tpl,
    "Two facts are visible before any test is run. No study in the core is explicit on more "
    "than five of the seven dimensions, and the median is three; the distribution is unimodal "
    "and sits in the middle rather than piling up at either end (Fig. 7a). The three studies "
    "that carry no explicit dimension at all are exactly the three reviews ([1], [2], [4]). "
    "That is the expected result rather than a criticism: a review synthesizes other people's "
    "evidence and does not report its own information set, hold-out split, or settlement "
    "calculation. We read the zero column as a property of the review genre and exclude "
    "nothing on that basis."))

# --- Fig. 7
fig_el = copy.deepcopy(fig_tpl._p)
fig_p = Paragraph(fig_el, fig_tpl._parent)
for r in list(fig_p.runs):
    r._r.getparent().remove(r._r)
for tag in ("drawing", "pict", "hyperlink"):
    for el in fig_el.findall(".//" + W + tag):
        el.getparent().remove(el)
run = fig_p.add_run()
run.add_picture("_draft/fig7_structure.png", width=Inches(6.3))
fig_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
elems.append(fig_el)

elems.append(new_para(figcap_tpl,
    "Fig. 7. Joint structure of the verified-core coding. (a) Number of DMDI dimensions rated "
    "Explicit per study; the bar at zero is the three review studies. (b) Pairwise φ between "
    "dimensions, with an asterisk marking pairs that survive Benjamini–Hochberg correction at "
    "q < 0.05. R is omitted from both panels because no study in the core is explicit on it."))

elems.append(new_para(body_tpl,
    "The association analysis splits the dimensions into two blocks. Information-set, "
    "uncertainty, and decision integrity are positively associated with one another: I–U "
    "φ = 0.63 and U–D φ = 0.56 both survive Benjamini–Hochberg correction across the fifteen "
    "pairwise tests (q = 0.003 and q = 0.006), and D–M φ = 0.42 is significant before "
    "correction (p = 0.022) but not after (q = 0.11). Studies that document their information "
    "set tend to document their uncertainty model and their decision constraints as well, "
    "which is what one would expect from authors working to a common reporting habit: the "
    "modelling layer behaves like a single latent construct rather than six independent ones."))

# --- Table XIV
elems.append(new_para(cap_tpl,
    "TABLE XIV — Pairwise association between DMDI dimensions in the verified-core coding "
    "(n = 39). φ is the Pearson phi coefficient on the Explicit/not-Explicit dichotomy; p is "
    "the two-sided Fisher exact test; q is the Benjamini–Hochberg adjusted value across the "
    "fifteen pairs. R is omitted because no study in the core is explicit on it, so the "
    "column has no variance."))

tbl_el = copy.deepcopy(doc.tables[0]._tbl)
while len(tbl_el.findall(W + "tr")) > 16:
    tbl_el.remove(tbl_el.findall(W + "tr")[-1])
rows_now = len(tbl_el.findall(W + "tr"))
proto = tbl_el.findall(W + "tr")[1]
while rows_now < 16:
    tbl_el.append(copy.deepcopy(proto))
    rows_now += 1

tbl = docx.table.Table(tbl_el, doc)
WIDTHS = [3000, 1500, 1300, 1700, 1500]
for gc, w in zip(tbl_el.tblGrid.findall(W + "gridCol"), WIDTHS):
    gc.set(W + "w", str(w))

ORDER = [("I", "U"), ("I", "D"), ("I", "M"), ("I", "O"), ("I", "S"),
         ("U", "D"), ("U", "M"), ("U", "O"), ("U", "S"),
         ("D", "M"), ("D", "O"), ("D", "S"),
         ("M", "O"), ("M", "S"), ("O", "S")]

HEAD = ["Dimension pair", "Both explicit", "φ", "Exact p", "q (BH)"]
for ci, h in enumerate(HEAD):
    set_cell(tbl.rows[0].cells[ci], h, bold=True)


def fmt_p(v):
    return "<0.001" if v < 0.001 else "%.3f" % v


def fmt_q(v):
    return "<0.001" if v < 0.001 else "%.3f" % v


for ri, (a, b) in enumerate(ORDER, start=1):
    d = PAIRS[(a, b)]
    vals = ["%s–%s" % (a, b), str(d["both"]), "%+.2f" % d["phi"],
            fmt_p(d["p"]), fmt_q(d["q"])]
    for ci, v in enumerate(vals):
        cell = tbl.rows[ri].cells[ci]
        set_cell(cell, v, bold=False)
        for tc in cell._tc.findall(W + "tcPr"):
            pass

elems.append(tbl_el)

elems.append(new_para(body_tpl,
    "What does not cluster is more informative than what does. Every association that "
    "involves out-of-sample validity or settlement realism is small and non-significant, "
    "with φ between −0.08 and 0.30 and exact p at or above 0.12 in all six cases (Table XIV). "
    "Reproducibility cannot be tested at all, because no study in the core is explicit on it "
    "and the column has no variance. Read together, these results place the validation layer "
    "close to orthogonal to the modelling layer in this corpus: knowing that a study states "
    "its information set tells you almost nothing about whether it held data out "
    "chronologically or reported what settlement did to its profit."))

elems.append(new_para(body_tpl,
    "The sharpest expression of the same result is a single empty cell. The two studies "
    "explicit on O ([8], [9]) and the four explicit on S ([16], [25], [36], [37]) are "
    "disjoint: not one of the thirty-nine studies reports both chronological out-of-sample "
    "validation and settlement realism (Fig. 7b). A field can live with a rare capability. "
    "What it cannot do is demonstrate the end-to-end performance claim in Section 10.1 "
    "through any single study, because the two halves of that claim are never measured "
    "together."))

elems.append(new_para(body_tpl,
    "We also tested whether the situation is improving. It is not. Spearman's ρ between "
    "publication year and the number of explicit dimensions is −0.07 (p = 0.67), so the "
    "recent half of the corpus is no more complete than the older half, even though 72% of "
    "the retrieved frame dates from 2023 onward (Section 2.4). The one field that drifts in "
    "the expected direction is deployment maturity, and only weakly (ρ = 0.26, p = 0.11). "
    "Whatever is driving the growth in VPP output over this window, it is not a secular "
    "improvement in reporting completeness."))

elems.append(new_para(body_tpl,
    "Three limits apply to everything in this subsection. The counts describe a fixed corpus "
    "of thirty-nine studies, not a sample from a population, so the exact tests are read as "
    "statements about exchangeability within the corpus rather than as inferences about the "
    "literature; with n = 39 the design can detect only large associations, and a "
    "non-significant pair means “not large here”, not “absent”. The fifteen comparisons are "
    "exploratory, which is why both exact p and Benjamini–Hochberg q are reported and why we "
    "lean on the two surviving associations rather than on any single borderline one. And the "
    "ratings themselves come from a single coding pass (Section 2.7), so a double-coded matrix "
    "could move individual cells; the structural findings above rest on the pattern across "
    "many cells, which is more robust to that than any single count."))

for el in elems:
    anchor_el.addprevious(el)
note(True, "Section 10.4 inserted (%d elements incl. Table XIV and Fig. 7)" % len(elems))


# ============================================================ 5. 11.1 cross-reference
p = para_starting("Reading Tables XI–XIII together produces a consistent picture")
n = replace_in(p,
               "(Table XII) independently. This pattern also mirrors",
               "(Table XII) independently. The joint-structure analysis in Section 10.4 "
               "sharpens the claim: O and S are not merely rare, they are unassociated with "
               "the I/D/M cluster, and no study in the core is explicit on both. This pattern "
               "also mirrors")
note(n == 1, "Section 11.1 links to the new quantitative result")


# ============================================================ 6. abstract
p = para_starting("Virtual power plants (VPPs) turn dispersed flexibility")
changes = [
    ("a richer optimization model, or a higher simulated profit, what evidence shows that the "
     "decision would have held at the moment it was made",
     "a richer optimization model, or a higher simulated profit, what evidence shows that the "
     "decision would have held at decision time"),
    ("a seven-dimension instrument with explicit coding rules and four evidence levels "
     "(Explicit, Partial, Not-Reported, Not-Verifiable)",
     "a seven-dimension instrument with explicit coding rules and four evidence levels"),
    ("The pattern is consistent: information-set, decision, and market integrity are "
     "comparatively well evidenced",
     "The pattern is consistent, and the two weakest dimensions are not merely rare but "
     "unassociated with the strong ones: information-set, decision, and market integrity are "
     "well evidenced"),
    ("turn dispersed flexibility into market value, through a chain of steps usually studied "
     "one at a time",
     "turn dispersed flexibility into market value through steps usually studied one at a time"),
    ("We ask a narrow question: when a VPP study reports", "We ask: when a VPP study reports"),
    ("what evidence shows that the decision would have held",
     "what evidence shows the decision would have held"),
    ("The review is reported as structured and PRISMA-informed",
     "The review is structured and PRISMA-informed"),
    ("as the binding constraint on claims of deployable value",
     "as the binding constraint on deployable value"),
]
for old, new in changes:
    note(replace_in(p, old, new) == 1, "abstract edit: %r" % old[:48])
wc = len(re.findall(r"[A-Za-z0-9][\w'\u2019\-]*", p.text))
note(wc <= 250, "abstract word count = %d" % wc)


doc.save(DST)
note(True, "saved: " + DST)


# ============================================================ 7. verify
d2 = docx.Document(DST)
allt = "\n".join(pp.text for pp in d2.paragraphs)
for t in d2.tables:
    for r in t.rows:
        for c in r.cells:
            allt += "\n" + c.text

note("10.4 The statistical structure" in allt, "10.4 heading present")
note("Fig. 7. Joint structure" in allt, "Fig. 7 caption present")
note("Fig. 8. Evolution of VPP research themes" in allt, "old Fig. 7 became Fig. 8")
note("Fig. 9. DMDI validation stack" in allt, "old Fig. 8 became Fig. 9")
note("TABLE XIV — Pairwise association" in allt, "Table XIV caption present")
note("TABLE XV — Decision-integrity metrics" in allt, "old Table XIV became XV")
note("(Table XV)" in allt, "in-text Table XV reference present")
note("0.63" in allt and "0.56" in allt, "phi values in text")
note("Fig. 7a" in allt and "Fig. 7b" in allt, "Fig. 7 panel references")
note("falls outside that coding set" in allt, "Table X scope note present")
note("-0.08" in allt or "\u22120.08" in allt, "negative phi present")

fails = sum(1 for x in LOG if x.startswith("FAIL"))
print("\nFAILURES: %d" % fails)
