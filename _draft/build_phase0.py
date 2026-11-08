# -*- coding: utf-8 -*-
"""Phase 0 upgrade: editorial + structural hardening of the VPP review."""
import copy
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power Plants (revised 2026-10-27).docx"
DST = r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power Plants (revised 2026-10-27) - PHASE0.docx"

doc = docx.Document(SRC)
LOG = []


def note(ok, msg):
    line = ("OK  " if ok else "FAIL") + "  " + msg
    LOG.append(line)
    print(line, flush=True)


def span_replace(p, idx, end, new):
    runs = p.runs
    text = "".join(r.text for r in runs)
    if idx < 0 or end > len(text):
        return 0
    pos = 0
    start = endr = None
    start_off = end_off = 0
    for ri, r in enumerate(runs):
        rl = len(r.text)
        if start is None and pos + rl > idx:
            start, start_off = ri, idx - pos
        if endr is None and pos + rl >= end:
            endr, end_off = ri, end - pos
        pos += rl
    if start is None or endr is None:
        return 0
    if start == endr:
        r = runs[start]
        r.text = r.text[:start_off] + new + r.text[end_off:]
    else:
        runs[start].text = runs[start].text[:start_off] + new
        for k in range(start + 1, endr):
            runs[k].text = ""
        runs[endr].text = runs[endr].text[end_off:]
    return 1


def replace_in_para(p, old, new):
    """Replace the first occurrence span-aware, preserving surrounding formatting."""
    text = "".join(r.text for r in p.runs)
    idx = text.find(old)
    if idx < 0:
        return 0
    return span_replace(p, idx, idx + len(old), new)


def apply_para_text(p, text):
    runs = p.runs
    if not runs:
        p.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


def all_paras():
    out = list(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                out.extend(c.paragraphs)
    return out


def edit_global(old, new, expect=1):
    hits = 0
    for p in all_paras():
        t = "".join(r.text for r in p.runs)
        if old in t:
            hits += replace_in_para(p, old, new)
    ok = (expect is None) or (hits == expect)
    note(ok, f"replace x{hits} (expected {expect}): {old[:70]!r}")
    return hits


ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
         "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14}
REV = {v: k for k, v in ROMAN.items()}

# ---------------------------------------------------------------- 1. figures
fig_map = {1: 2, 2: 1, 3: 3, 4: 6, 5: 4, 6: 5, 7: 7, 8: 8}
pat_fig = re.compile(r"\b(Fig\.)(\s*)(\d)")
n = 0
for p in all_paras():
    t = "".join(r.text for r in p.runs)
    if pat_fig.search(t):
        nt = pat_fig.sub(lambda m: f"{m.group(1)}{m.group(2)}{fig_map[int(m.group(3))]}", t)
        if nt != t:
            apply_para_text(p, nt)
            n += 1
note(True, f"figure renumbering applied to {n} paragraphs")

# ---------------------------------------------------------------- 2. tables
pat_tbl = re.compile(r"\b(Tables?|TABLES?)(\s+)([IVX]+)(\s*[–\-]\s*([IVX]+))?")


def _shift(m):
    head, sp, r1, tail, r2 = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
    a = ROMAN[r1] + 1 if ROMAN[r1] >= 2 else 1
    s = f"{head}{sp}{REV[a]}"
    if tail:
        b = ROMAN[r2] + 1 if ROMAN[r2] >= 2 else 1
        s += ("–" if "–" in tail else "-") + REV[b]
    return s


n = 0
for p in all_paras():
    t = "".join(r.text for r in p.runs)
    if pat_tbl.search(t):
        nt = pat_tbl.sub(_shift, t)
        if nt != t:
            apply_para_text(p, nt)
            n += 1
note(True, f"table renumbering applied to {n} paragraphs")

# ---------------------------------------------------------------- 3. tables content
TB = doc.tables


def cell_text(cell):
    return " ".join(cell.text.split())


def find_row(tbl, needle):
    for r in tbl.rows:
        if needle in cell_text(r.cells[0]):
            return r
    return None


# 3a. comparative-evidence table: reorder I, U, D, O
t = TB[7]
if cell_text(t.rows[0].cells[5]) == "OOS":
    for row in t.rows:
        vals = [cell_text(c) for c in row.cells]
        new = [vals[0], vals[1], vals[4], vals[2], vals[3], "O" if vals[5] == "OOS" else vals[5],
               vals[6], vals[7]]
        for i, v in enumerate(new):
            apply_para_text(row.cells[i].paragraphs[0], v)
    note(True, "Table VIII: columns reordered to I, U, D, O and OOS renamed O")
else:
    note(False, "Table VIII header unexpected: " + cell_text(t.rows[0].cells[5]))

# 3b. OOS -> O in the other two tables
for idx in (8, 11):
    t = TB[idx]
    ok = False
    for row in t.rows[:1]:
        for c in row.cells:
            if cell_text(c) == "OOS":
                apply_para_text(c.paragraphs[0], "O")
                ok = True
    note(ok, f"table #{idx+1}: OOS header renamed O")

# 3c. maturity harmonisation
fixes = [(7, "[8]", 6, "Level 4", "Level 5"),
         (7, "[22]", 6, "Level 3", "Level 2"),
         (7, "[27]", 6, "Level 3", "Level 2"),
         (7, "[28]", 6, "Level 3", "Level 2"),
         (8, "[8]", 5, "Level 2", "Level 5"),
         (8, "[8]", 4, "NR", "Explicit"),
         (8, "[28]", 5, "Level 1", "Level 2")]
for ti, needle, col, old, new in fixes:
    row = find_row(TB[ti], needle)
    if row is None:
        note(False, f"table #{ti+1}: row {needle} not found")
        continue
    c = row.cells[col]
    ok = cell_text(c) == old
    if ok:
        apply_para_text(c.paragraphs[0], new)
    note(ok, f"table #{ti+1} {needle}: maturity {old} -> {new} (found {cell_text(c)!r})")

# 3d. P row labelled as companion field
row = find_row(TB[10], "P — Deployment maturity")
if row:
    apply_para_text(row.cells[0].paragraphs[0],
                    "P — Deployment maturity (companion field, not a DMDI dimension)")
    note(True, "Table X: P row labelled as companion field")
else:
    note(False, "Table X: P row not found")

# ---------------------------------------------------------------- 4. text edits
edit_global(
    "through robust optimization, to distributionally robust optimization (DRO), "
    "increasingly Wasserstein-metric-based and dominant since approximately 2023 [22], [25]–[28].",
    "through interval, two-stage, and price-maker robust variants [15], [53], [54], and "
    "day-ahead bidding formulations for renewable portfolios [17], to distributionally robust "
    "optimization (DRO), increasingly Wasserstein-metric-based and dominant since approximately "
    "2023 [22], [25]–[28], [41].",
)

edit_global(
    "Market-mechanism studies that explicitly model pay-as-bid/pay-as-clear rules and imbalance "
    "penalties [36], and portfolio-composition studies that link DER composition to settlement "
    "outcomes [37], illustrate",
    "Market-mechanism studies that explicitly model pay-as-bid/pay-as-clear rules and imbalance "
    "penalties [36], studies that clear frequency-constrained products [52], and "
    "portfolio-composition studies that link DER composition to settlement outcomes [37], illustrate",
)

edit_global(
    "Of the verified core, most uncertainty-handling and market studies report objective-function "
    "or cleared-market value;",
    "Of the verified core, most uncertainty-handling and market studies, including two-step "
    "spot-market formulations [18], report objective-function or cleared-market value;",
)

edit_global(
    "and explicit uncertainty reduction from day-ahead to balancing markets [29]. These studies "
    "strengthen the forecasting layer,",
    "and explicit uncertainty reduction from day-ahead to balancing markets [29]. Work on the "
    "demand side, such as data-mining-driven incentive design for aggregated response [55], "
    "improves the input layer in much the same way. These studies strengthen the forecasting layer,",
)

edit_global(
    "and it is the reasoning behind treating L1 as a market property rather than a purely "
    "engineering one (Section 6.1).",
    "and it is the reasoning behind treating L1 as a market property rather than a purely "
    "engineering one (Section 6.1). Network feasibility belongs to the execution layer for the "
    "same reason: locational marginal flexibility formulations [46] can leave an offer technically "
    "infeasible after clearing, which turns a power-flow detail into a market-integrity question.",
)

edit_global(
    "RL and deep-learning bidding agents adapt to nonstationary prices and behavior that static "
    "scenario sets miss, but they are comparatively opaque",
    "RL and deep-learning bidding agents, including hierarchical schemes for aggregated "
    "heterogeneous microgrids [42], adapt to nonstationary prices and behavior that static "
    "scenario sets miss, but they are comparatively opaque",
)

edit_global(
    "throughput, energy cost, and the “oracle problem” (a ledger cannot verify off-chain meter "
    "truth on its own) keep maturity medium–low.",
    "throughput, energy cost, and the “oracle problem” (a ledger cannot verify off-chain meter "
    "truth on its own) keep maturity medium–low, a verdict shared by review-level assessments of "
    "blockchain integration in VPPs [39].",
)

edit_global(
    "is that forecast accuracy and realized decision value are not interchangeable evidence claims.",
    "is that forecast accuracy and realized decision value are not interchangeable evidence claims. "
    "Closed-loop designs that train the forecast against the bidding objective rather than against "
    "forecast error alone [47] make the distinction concrete.",
)

edit_global(
    "they do not imply that every VPP application requires the same market products, settlement "
    "mechanism, or validation depth.",
    "they do not imply that every VPP application requires the same market products, settlement "
    "mechanism, or validation depth. Regulatory scope differs widely across jurisdictions [35], so "
    "a coding profile that looks adequate in one market can be silent on obligations that another "
    "market imposes.",
)

edit_global("Layer 1–4 maturity ratings", "L1–L4 maturity ratings")

# ---------------------------------------------------------------- 5. maturity paragraph
OLD_MAT = (
    "Based on the verified core, the literature clusters predominantly at Levels 1–4; few studies "
    "(e.g., a data-driven robust bidding study validated on real campus-deployment data [22]) reach "
    "Level 3–4, and very few reach Levels 5–7. A precise quantitative distribution across the full "
    "literature is deferred until database-level screening (Section 2.4) is completed; the "
    "qualitative clustering pattern, however, is consistent across every evidence table in "
    "Sections 7–10."
)
NEW_MAT = (
    "Based on the verified core, the literature clusters at Levels 1–4. The rungs above 4 are "
    "sparsely populated: the settlement-aware portfolio study [8] sits at Level 5, and no study in "
    "the verified core reaches Level 6 or 7, which means that no coded paper reports pilot or "
    "sustained operational evidence. The ladder records the highest rung a study demonstrably "
    "reaches and is not treated as strictly cumulative, so a study with explicit market realism "
    "but only partial temporal separation is placed at Level 4 while its O rating is carried "
    "unchanged in the DMDI column. A precise distribution across the full literature is deferred "
    "until database-level screening (Section 2.4) is complete; the clustering itself recurs in "
    "every evidence table in Sections 7–10."
)
edit_global(OLD_MAT, NEW_MAT)

# ---------------------------------------------------------------- 6. abstract + keywords
OLD_ABS_START = "Virtual power plants (VPPs) are evolving from aggregation concepts"
NEW_ABS = (
    "Virtual power plants (VPPs) turn dispersed flexibility into market value, and they do it "
    "through a chain of steps that are usually studied one at a time: measurement, forecasting, "
    "uncertainty modelling, optimisation, bidding, clearing, dispatch, deviation, settlement. This "
    "review treats that chain as the unit of analysis. We ask a narrow question: when a VPP study "
    "reports a better forecast, a richer optimisation model, or a higher simulated profit, what "
    "evidence shows that the decision would have held at the moment it was made, and that the "
    "value survived clearing and settlement? A candidate corpus of roughly 110 records was "
    "compiled, and 39 studies were verified against publisher metadata and coded against a common "
    "evidence matrix. From that coding we build Data-to-Market Decision Integrity (DMDI), a "
    "seven-dimension instrument with explicit coding rules and four evidence levels (Explicit, "
    "Partial, Not-Reported, Not-Verifiable). The pattern is consistent across groupings: "
    "information-set, decision, and market integrity are comparatively well evidenced (22/39, "
    "32/39, and 31/39 explicit), while chronological out-of-sample validation, settlement realism, "
    "and reproducibility are rare (2/39, 4/39, and 0/39 explicit). We read that asymmetry, rather "
    "than any algorithmic shortfall, as the binding constraint on claims of deployable value. The "
    "review is reported as a structured, PRISMA-informed evidence review: database-level screening "
    "counts are disclosed as pending rather than estimated, and the DMDI ratings come from a "
    "single coding pass pending independent double-coding. DMDI and the companion Data-to-Market "
    "Maturity Ladder are offered as diagnostic tools for authors and reviewers, not as validated "
    "external standards."
)
abs_p = next(p for p in doc.paragraphs if p.text.strip().startswith(OLD_ABS_START))
apply_para_text(abs_p, NEW_ABS)
note(True, f"abstract replaced ({len(NEW_ABS.split())} words)")

OLD_KW = ("Virtual power plant, data-driven energy management, uncertainty representation, "
          "distributionally robust optimization, bidding strategy, carbon–electricity joint "
          "markets, out-of-sample validation, settlement realism, decision integrity, PRISMA, "
          "evidence review.")
NEW_KW = ("Bidding strategy, carbon–electricity joint markets, data-driven energy management, "
          "decision integrity, distributionally robust optimization, evidence review, "
          "out-of-sample validation, PRISMA, settlement realism, uncertainty representation, "
          "virtual power plant.")
edit_global(OLD_KW, NEW_KW)

# ---------------------------------------------------------------- 7. references
edit_global("art. no.", "Art. no.", expect=None)
edit_global("vol.\u00a0372, n71, 2021", "vol.\u00a0372, Art. no. n71, 2021")

# IEEE style: article numbers carried as "Art. no. N"
pat_vn = re.compile(r", vol\.\s*(\d+), (\d{4,6}), (\d{4})([,\.])")
pat_vin = re.compile(r", vol\.\s*(\d+), no\.\s*(\d+), (\d{4,6}), (\d{4})([,\.])")
pat_art = re.compile(r", art\.\s*(\d+)")
nfix = 0
for p in doc.paragraphs:
    if not re.match(r"^\[\d+\]", p.text.strip()):
        continue
    txt = "".join(r.text for r in p.runs)
    for pat, fn in (
        (pat_vin, lambda m: f", vol. {m.group(1)}, no. {m.group(2)}, Art. no. "
                            f"{m.group(3)}, {m.group(4)}{m.group(5)}"),
        (pat_vn, lambda m: f", vol. {m.group(1)}, Art. no. {m.group(2)}, "
                           f"{m.group(3)}{m.group(4)}"),
        (pat_art, lambda m: f", Art. no. {m.group(1)}"),
    ):
        ms = list(pat.finditer("".join(r.text for r in p.runs)))
        for m in reversed(ms):
            nfix += span_replace(p, m.start(), m.end(), fn(m))
note(True, f"reference article-number style normalised ({nfix} spans)")

# American spelling inside newly written passages
edit_global("modelling", "modeling", expect=None)
edit_global("optimisation", "optimization", expect=None)
edit_global("behaviour", "behavior", expect=None)
edit_global(
    "report how study-level quality was assessed [6]:",
    "report how study-level quality was assessed [6], summarized here as Q1–Q8 in Table II:",
)
edit_global("We propose the following reporting set:", "We propose the following reporting set (Table XIV):")

edit_global(
    "rather than an incidental observation, and recommend",
    "rather than an incidental observation (Fig. 3), and recommend",
)
edit_global(
    "very few reach Level 5–6. This indicates",
    "very few reach Level 5–6 (Fig. 4). This indicates",
)
edit_global(
    "no study in the verified core reaches Level 6 or 7, which means",
    "no study in the verified core reaches Level 6 or 7 (Fig. 6), which means",
)
for p in doc.paragraphs:
    if re.match(r"^\[\d+\]", p.text.strip()):
        runs = p.runs
        if runs and runs[-1].text != runs[-1].text.rstrip():
            runs[-1].text = runs[-1].text.rstrip()

# ---------------------------------------------------------------- 8. insertions
body_t = next(p for p in doc.paragraphs if p.text.startswith("Recent reviews illustrate the breadth"))
h2_t = next(p for p in doc.paragraphs if p.text.startswith("11.7 Electricity"))
h1_t = next(p for p in doc.paragraphs if p.text.startswith("12. Limitations"))
cap_t = next(p for p in doc.paragraphs if p.text.startswith("TABLE XIII — Data-to-Market"))


def make_para(template, text):
    el = copy.deepcopy(template._p)
    p = Paragraph(el, template._parent)
    rpr = None
    if template.runs:
        rpr = template.runs[0]._r.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr")
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    run = p.add_run(text)
    if rpr is not None:
        run._r.insert(0, copy.deepcopy(rpr))
    return p


def insert_before(anchor, template, text):
    p = make_para(template, text)
    anchor._p.addprevious(p._p)
    return p


# 8a. caption for the uncaptioned Q1-Q8 table
cap = make_para(cap_t, "TABLE II — Evidence-quality assessment layer (Q1–Q8): coding criteria, "
                       "kept separate from DMDI")
TB[1]._tbl.addprevious(cap._p)
note(True, "caption added for the Q1–Q8 table (new Table II)")

# 8b. section 1.3
a = next(p for p in doc.paragraphs if p.text.strip() == "2. Review Protocol")
insert_before(a, h2_t, "1.3 Organization of the paper")
insert_before(a, body_t,
              "Section 2 sets out the protocol and says plainly where it stops short of a completed "
              "PRISMA review. Section 3 positions the work against earlier surveys, and Section 4 "
              "explains how the six retrieval blocks map onto the five synthesis streams. Section 5 "
              "defines DMDI and its coding rules; Section 6 adds a second, deliberately separate "
              "instrument for decision integrity, together with the uncertainty taxonomy, the "
              "decision-paradigm comparison, and the electricity–carbon coupling archetypes that "
              "later sections rely on. Sections 7–10 report the evidence, Section 11 converts it "
              "into a research agenda and answers the research questions in order, and Sections "
              "12–13 close with limitations and conclusions.")
note(True, "Section 1.3 inserted")

# 8c. section 3 paragraph citing the remaining reviews
a = next(p for p in doc.paragraphs if p.text.strip() == "4. Synthesis Streams and Retrieval Blocks")
insert_before(a, body_t,
              "Those are not the only surveys in the field, and none of the others closes the same "
              "gap. Naval and Yusta [7] catalogue VPP models against European market designs. Mo et "
              "al. [32] and Zhu et al. [33] survey deep-learning and reinforcement-learning "
              "applications in bidding and operation, Li et al. [34] give a broad AI-driven "
              "overview, and Singh et al. [48] concentrate on uncertainty management and bidding "
              "strategy. Bedi et al. [39] trace blockchain integration, Bendigiri and Rao [40] "
              "narrow the scope to the built environment, and Bhattarai et al. [35] review the "
              "policy and regulatory envelope. Each is a useful map of a sub-literature. None of "
              "them codes a primary study against the information that was actually available at "
              "its decision gate, which is the question Table III is built to make visible.")
note(True, "Section 3 positioning paragraph inserted")

# 8d. section 11.8
a = next(p for p in doc.paragraphs if p.text.strip() == "12. Limitations")
insert_before(a, h2_t, "11.8 Answers to the research questions")
rq = [
    ("RQ1", "RQ1 asked how VPP energy-management systems are structured across the chain, and the "
            "verified core answers it unevenly. Studies are strongest in the middle, where "
            "forecasting meets optimization and a bid is formed, and thin at both ends: few "
            "describe how measurements reach the model, and fewer still describe what happens after "
            "clearing. No coded study reports all ten links as one auditable sequence."),
    ("RQ2", "RQ2 asked how uncertainty, dependence, and tail behavior travel from forecasting into "
            "the decision. Representation travels well; calibration does not. Twenty-three of 39 "
            "studies state an uncertainty model explicitly, but dependence and tail behaviour are "
            "usually asserted rather than reproduced from data, and the distortion introduced by "
            "scenario reduction is almost never quantified."),
    ("RQ3", "RQ3 asked whether forecast or AI performance translates into operational and market "
            "outcomes. For the most part it is not shown to. Predictive evidence and market-value "
            "evidence remain two largely separate literatures: studies report error metrics and "
            "stop, or report profit and never connect it to a change in the forecast."),
    ("RQ4", "RQ4 asked how carefully studies preserve information-set integrity, temporal "
            "causality, market timing, and out-of-sample validity. This is where the spread is "
            "widest. Information-set definitions are the best-reported dimension (22/39 explicit) "
            "and chronological out-of-sample evaluation the worst (2/39), so most reported "
            "performance rests on splits that a market would not have offered."),
    ("RQ5", "RQ5 asked how electricity and carbon decisions are coupled, and how uncertainty "
            "propagates between them. Coupling is real but shallow. Most studies reach objective, "
            "constraint, or market-participation coupling, few model a traded carbon position whose "
            "price is itself uncertain, and where coupling runs deep it is usually sequential "
            "rather than joint."),
    ("RQ6", "RQ6 asked about maturity. The verified core sits at Levels 1–4 of the ladder. "
            "Settlement-aware evidence is rare, pilot evidence rarer, and operational evidence "
            "absent, which is what most limits any claim about deployable value."),
]
for tag, txt in rq:
    insert_before(a, body_t, txt)
note(True, "Section 11.8 inserted with six RQ answers")

# 8e. section 11 lead-in for Figs. 7-8
h11 = next(p for p in doc.paragraphs
           if p.text.strip() == "11. Cross-Layer Evidence Gaps and a Research Agenda")
lead = make_para(body_t,
                 "Two summary views frame this section. Fig. 7 traces how the themes addressed in "
                 "the verified core shift along the chain; it is descriptive, and shows where "
                 "attention has accumulated rather than how much of the literature each theme "
                 "represents. Fig. 8 lays out the validation stack implied by DMDI, in which "
                 "forecast and algorithmic performance are tested in turn against decision, market, "
                 "settlement, and deployment constraints.")
h11._p.addnext(lead._p)
note(True, "Section 11 lead-in for Figs. 7-8 inserted")

# 8f. back matter
a = next(p for p in doc.paragraphs if p.text.strip() == "14. References")
back = [
    ("h1", "Data Availability Statement"),
    ("body", "The coding matrix for the 39 verified-core studies, including the per-dimension DMDI "
             "ratings and the maturity-ladder assignment, is available from the corresponding "
             "author on reasonable request. No new empirical measurements were generated for this "
             "review. The search strings needed to reproduce the retrieval are printed in Section "
             "2.3."),
    ("h1", "Declaration of Competing Interest"),
    ("body", "The authors declare that they have no known competing financial interests or "
             "personal relationships that could have appeared to influence the work reported in "
             "this paper."),
    ("h1", "Use of AI-Assisted Technologies"),
    ("body", "A large language model was used to support literature triage, first-pass evidence "
             "coding, and language editing, under direct author supervision. The scope and limits "
             "of that use are stated in Section 2.7. The authors reviewed every coded entry, every "
             "interpretive claim, and the final reference list, and take full responsibility for "
             "the content of the article."),
    ("h1", "Author Contributions"),
    ("body", "[To be completed before submission: author initials, contribution, and CRediT role.]"),
]
for kind, txt in back:
    insert_before(a, h1_t if kind == "h1" else body_t, txt)
note(True, "back matter inserted (4 headings + 4 statements)")

# ---------------------------------------------------------------- 9. save
doc.save(DST)
note(True, "saved: " + DST)

print("\n".join(LOG))
print("\nFAILURES:", sum(1 for x in LOG if x.startswith("FAIL")))
