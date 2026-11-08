# -*- coding: utf-8 -*-
"""
Phase 1 build.

Input : the Phase 0 deliverable (never modified).
Output: a new Phase 1 .docx.

What this phase does
  1. Replaces the placeholder search log (Table I) with the executed OpenAlex run.
  2. Rewrites Sections 1.2, 1.3, 2.1, 2.3, 2.4, 2.9, 11.6, 12 and 13 to match
     what was actually executed, including the measured sensitivity of the
     search strings against the analytical corpus.
  3. Adds the PRISMA-aligned flow diagram as Fig. 1, which the manuscript
     referred to but never embedded.
  4. Corrects the DOI of reference [25], which resolved to an unrelated paper.
"""
import copy
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power Plants (revised 2026-10-27) - PHASE0.docx"
DST = r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power Plants (revised 2026-10-27) - PHASE1.docx"

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


def set_para(p, text, italic=None):
    """Replace paragraph text, keeping the first run's character formatting."""
    runs = p.runs
    if not runs:
        r = p.add_run(text)
    else:
        runs[0].text = text
        for r in runs[1:]:
            r.text = ""
        r = runs[0]
    if italic is not None:
        r.italic = italic


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


def make_like(template_p, text):
    el = copy.deepcopy(template_p._p)
    p = Paragraph(el, template_p._parent)
    rpr = None
    if template_p.runs:
        rpr = template_p.runs[0]._r.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr")
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    run = p.add_run(text)
    if rpr is not None:
        run._r.insert(0, copy.deepcopy(rpr))
    return p


# ============================================================ 1. Table I
TBL = doc.tables[0]

ROWS = [
    ("Database", "Query", "Field scope and filters", "Search date", "Records"),
    ("OpenAlex", "S1 = B1 AND B2", "title and abstract; 2018–2026; article or review; English",
     "30 Oct 2026", "1,194"),
    ("OpenAlex", "S2 = B1 AND B3", "same", "30 Oct 2026", "560"),
    ("OpenAlex", "S3 = B1 AND B4", "same", "30 Oct 2026", "316"),
    ("OpenAlex", "S4 = B1 AND B5", "same", "30 Oct 2026", "445"),
    ("OpenAlex", "S5 = B1 AND B6", "same", "30 Oct 2026", "155"),
    ("OpenAlex", "S1 ∪ S2 ∪ S3 ∪ S4 ∪ S5, before de-duplication", "same", "30 Oct 2026", "2,670"),
    ("—", "Duplicates removed across blocks", "record-level, by OpenAlex work identifier",
     "—", "1,002"),
    ("OpenAlex", "S1 ∪ … ∪ S5, after de-duplication", "same", "30 Oct 2026", "1,668"),
    ("Scopus", "S1–S5 as above", "title, abstract, keywords; same filters and window",
     "not executed", "—"),
    ("Web of Science Core Collection", "S1–S5 as above", "Topic; same filters and window",
     "not executed", "—"),
    ("IEEE Xplore", "S1–S5 as above", "metadata and full text; same filters and window",
     "not executed", "—"),
]

proto_tr = TBL.rows[1]._tr
while len(TBL.rows) < len(ROWS):
    TBL._tbl.append(copy.deepcopy(proto_tr))
while len(TBL.rows) > len(ROWS):
    TBL._tbl.remove(TBL.rows[-1]._tr)

for ri, data in enumerate(ROWS):
    cells = TBL.rows[ri].cells
    for ci in range(5):
        cell = cells[ci]
        for extra in cell.paragraphs[1:]:
            extra._p.getparent().remove(extra._p)
        p = cell.paragraphs[0]
        runs = p.runs
        if runs:
            runs[0].text = data[ci]
            for r in runs[1:]:
                r.text = ""
        else:
            p.add_run(data[ci])
        for r in p.runs:
            r.bold = (ri == 0) or (ri in (6, 8))
note(True, "Table I rebuilt: %d rows x 5 columns" % len(ROWS))

cap_i = para_starting("TABLE I —")
set_para(cap_i,
         "TABLE I — Search execution log. Retrieval was executed in OpenAlex on 30 October 2026 "
         "and every count is a returned record count, not an estimate; B1–B6 denote the search "
         "blocks defined in Section 2.3. The three subscription databases were not executed for "
         "this version and are listed so that the same strings can be run without ambiguity.")
note(True, "Table I caption rewritten")


# ============================================================ 2. text edits
# 2.1 review design
p = para_starting("The review is designed as a structured literature review")
set_para(p,
         "The review is designed as a structured literature review and reported in alignment with "
         "PRISMA 2020 [6] to the extent that the executed work supports it. PRISMA 2020 specifies a "
         "27-item reporting checklist and a flow diagram for identification, screening, eligibility, "
         "and inclusion [6]. We use PRISMA as a reporting scaffold: where a stage of the flow has been "
         "executed, its counts are reported in PRISMA form (Section 2.4); where a stage has not been "
         "executed, we say so rather than estimate it. Identification is executed; screening is not "
         "(Section 2.4). The manuscript is therefore presented as a structured, PRISMA-informed "
         "evidence review rather than as a fully executed PRISMA systematic review. This is a "
         "deliberate framing choice (Section 2.9), not a cosmetic one: it prevents the manuscript from "
         "claiming a degree of database-level reproducibility that it does not have.")
note(True, "2.1 rewritten")

# 2.3 databases -> executed database
p = para_starting("Principal databases")
set_para(p,
         "The retrieval was executed in OpenAlex on 30 October 2026, against title and abstract "
         "fields, restricted to 2018–2026, English-language journal articles and reviews. OpenAlex "
         "was chosen because the search can be re-executed by any reader without a subscription; the "
         "same strings can be run in Scopus, Web of Science, or IEEE Xplore where access exists, but "
         "those three were not executed for this version and no count is reported for them (Table I). "
         "The review window is 2018–2026, with pre-2018 studies retained only as flagged foundational "
         "seed references for bidding formalism or architecture. The retrieval strategy is organized "
         "into six overlapping search blocks so that a single vocabulary choice (e.g., “data-driven "
         "VPP”) does not exclude studies using adjacent terminology such as “virtual aggregator,” "
         "“flexibility platform,” or “stochastic bidding.” The blocks and their exact Boolean "
         "strings are:")
note(True, "2.3 opening rewritten")

# after-table note
p = para_starting("The Boolean strings, field scope")
set_para(p,
         "Two properties of this result matter before the selection step. The five blocks return "
         "2,670 records but only 1,668 distinct works, so 1,002 records were duplicates and 761 "
         "works were captured by more than one block, which is what overlap between blocks is "
         "supposed to look like. Retrieval is also skewed toward recent work: 1,198 of the 1,668 "
         "works (72%) were published in 2023–2026. The strings, field scope, and set-combination "
         "logic are reproducible by any reader, and Table I records what each query returned on the "
         "date of execution rather than what it might return.")
note(True, "table note rewritten")

# 2.4 paragraph 1
p24 = para_starting("Applying the retrieval strategy")
set_para(p24,
         "Identification is complete and is reported in full. The five block queries returned 2,670 "
         "records, of which 1,002 were duplicates, leaving a de-duplicated frame of 1,668 works "
         "(Table I, Fig. 1). Screening is not complete. The frame was not read end to end at title and "
         "abstract level, so we do not report an exclusion cascade of the form PRISMA 2020 expects "
         "[6], and we do not present the frame as a screened population. Selection of the analytical "
         "corpus was purposive: works were drawn from the frame, and from citation chasing around the "
         "seed reviews [1]–[5], when they addressed a VPP decision problem closely enough to be coded "
         "against the evidence matrix in Section 5. Thirty-nine studies were then verified against "
         "publisher metadata and carried through structured coding (Section 2.7). We call this set the "
         "verified core; it is the analytical corpus for every quantitative statement in Sections 7–10.")
note(True, "2.4 paragraph 1 rewritten")

# 2.4 paragraph 2 (still described the old 110-record pool)
p = para_starting("From the working candidate corpus")
set_para(p,
         "We therefore describe the corpus precisely as 39 verified studies, selected purposively "
         "from a de-duplicated frame of 1,668 works, rather than as a population sample or a final "
         "systematic-review inclusion set. Its composition is reported study by study in Tables "
         "VIII and XI, and the coding rules that produced it are in Section 5.")
note(True, "2.4 paragraph 2 rewritten")

# query block: the union is now called a frame and is de-duplicated
p = para_starting("S1 = Block1 AND Block2")
n = replace_in(p, "Working candidate corpus = S1 ∪ S2 ∪ S3 ∪ S4 ∪ S5, restricted to 2018–2026,",
               "Search frame = S1 ∪ S2 ∪ S3 ∪ S4 ∪ S5, de-duplicated, restricted to 2018–2026,")
note(n == 1, "query block renamed to search frame")

# new sensitivity paragraph
sens = make_like(p24,
                 "Purposive selection has a cost, and it is better measured than glossed. Re-running the "
                 "five queries against the DOI identifiers of the 39 coded studies returns 35, a "
                 "sensitivity of 90%. Every miss is explainable, and none is random. Two are reviews "
                 "[2], [4] whose titles name virtual power plants but whose abstracts contain none of "
                 "the energy-management, uncertainty, AI, market, or carbon terms, so no block "
                 "intersection can reach them; block-intersection designs under-retrieve review "
                 "literature almost by construction. The other two are primary studies [37], [47] that "
                 "never use the VPP label in a title or abstract, one of which also has no abstract in "
                 "the database. The same mechanism accounts for review and policy records cited "
                 "elsewhere in the paper but outside the coded core ([35], [39], [40]). One further "
                 "record, [25], looked like a miss for a different reason: the DOI printed in our "
                 "reference list resolved to an unrelated paper, and with the corrected DOI the study "
                 "is returned by four of the five blocks (Section 2.6). Two cheap remedies follow and "
                 "both are in the research agenda (Section 11.6): a seventh block for review, policy, "
                 "and regulatory vocabulary, and forward and backward citation chasing for every "
                 "included study rather than only for the seed reviews.")
p24._p.addnext(sens._p)
note(True, "search-sensitivity paragraph inserted")

# Fig. 1 lead-in
p = para_starting("Fig. 1 reports this flow")
set_para(p,
         "Fig. 1 shows the resulting flow in PRISMA-aligned box form. The identification and "
         "de-duplication boxes carry executed counts that a reader can reproduce from Table I. The "
         "selection box is marked as purposive because that is what it was, and it feeds eligibility "
         "and inclusion directly; no record appears as excluded at screening, because no screening "
         "step was run that would justify an exclusion count. The figure should be read as "
         "identification-complete and selection-disclosed, not as a completed systematic-review "
         "cascade.")
note(True, "Fig. 1 lead-in rewritten")

# Fig. 1 caption
cap = para_starting("Fig. 1. PRISMA")
set_para(cap,
         "Fig. 1. PRISMA-aligned flow with executed identification counts. Records identified (2,670), "
         "duplicates removed (1,002), and the de-duplicated frame (1,668) are counted from Table I; the "
         "selection, eligibility, and inclusion boxes describe the purposive route to the 39-study "
         "verified core and are not an exhaustive screening cascade.")
note(True, "Fig. 1 caption rewritten")

# 1.2 scope of claims
p = para_starting("We are explicit about what this manuscript")
set_para(p,
         "We are explicit about what this manuscript does not claim. It does not report an exhaustive "
         "PRISMA exclusion cascade (Section 2.4): the retrieval is executed and counted, but screening "
         "of the full frame was purposive, and we report the measured consequence (35 of 39 coded "
         "studies recovered) rather than a claim of completeness. It does not report inter-coder "
         "reliability statistics (Sections 2.7 and 11.6), and it does not claim that DMDI is a "
         "validated instrument outside this review. These boundaries are stated here so that every "
         "subsequent claim in the paper can be read against them.")
note(True, "1.2 rewritten")

# 1.3 organisation
p = para_starting("Section 2 sets out the protocol")
set_para(p,
         "Section 2 sets out the protocol, reports the executed retrieval, and says plainly where it "
         "stops short of a completed PRISMA review. Section 3 positions the work against earlier "
         "surveys, and Section 4 explains how the six retrieval blocks map onto the five synthesis "
         "streams. Section 5 defines DMDI and its coding rules; Section 6 adds a second, deliberately "
         "separate instrument for decision integrity, together with the uncertainty taxonomy, the "
         "decision-paradigm comparison, and the electricity–carbon coupling archetypes that later "
         "sections rely on. Sections 7–10 report the evidence, Section 11 converts it into a research "
         "agenda and answers the research questions in order, and Sections 12–13 close with "
         "limitations and conclusions.")
note(True, "1.3 rewritten")

# 2.9 reporting status
p = para_starting("This review is reported as a structured evidence review")
set_para(p,
         "This review is reported as a structured evidence review rather than as a completed PRISMA "
         "2020 systematic review. Four elements of a systematic review are now reported in full: the "
         "eligibility criteria (Section 2.2), the executed retrieval with its record counts (Sections "
         "2.3–2.4, Table I), the sensitivity of that retrieval against the analytical corpus (Section "
         "2.4), and the reference-verification procedure (Section 2.6). Three elements remain "
         "incomplete and are stated as limitations rather than estimated: exhaustive title and "
         "abstract screening of the 1,668-record frame; independent double-coding of the DMDI ratings "
         "(Sections 2.7 and 11.6); and retrospective re-tagging of the existing not-reported entries "
         "into NR-R and NR-U (Section 5.3). Where a reported quantity depends on one of these "
         "unfinished steps — notably the per-dimension counts in Table XI — it is described as "
         "indicative of a pattern rather than as a prevalence estimate.")
note(True, "2.9 rewritten")

# 11.6 agenda item (i)
p = para_starting("Beyond study-level reproducibility")
n = replace_in(p,
               "(i) complete the institutional-account database run specified in Table I and freeze "
               "the PRISMA identification/screening/eligibility counts;",
               "(i) repeat the executed retrieval in Scopus, Web of Science, and IEEE Xplore and "
               "screen the combined frame exhaustively, so that the purposive selection in Section "
               "2.4 can be replaced by a full exclusion cascade;")
note(n == 1, "11.6 agenda item (i) rewritten")

# Section 12 first limitation
p = para_starting("Several limitations qualify every claim")
n = replace_in(p, "First, and most importantly, database-level identification, deduplication, and "
                  "screening counts are not yet frozen (Section 2.4); Table I's record counts and "
                  "search dates remain explicit placeholders pending institutional-account access, "
                  "and the review is titled and framed accordingly as a structured, PRISMA-informed "
                  "evidence review rather than a completed PRISMA systematic review.",
                  "First, and most importantly, identification is executed but screening is not "
                  "(Section 2.4). Table I reports what each query returned on 30 October 2026, and "
                  "the de-duplicated frame of 1,668 works is a number any reader can reproduce; what "
                  "we cannot offer is a record-by-record exclusion trail through that frame, because "
                  "selection was purposive. The measured cost is a retrieval sensitivity of 35 of 39 "
                  "for the coded core: two of the four misses are reviews whose abstracts carry none "
                  "of the stream terms, and two are studies that never use the VPP label. Those are "
                  "the numbers a reader should use to discount every "
                  "claim in Sections 7–10, and they are the reason the paper is framed as a "
                  "structured, PRISMA-informed review rather than a completed systematic review.")
note(n == 1, "Section 12 first limitation rewritten")

# the double-coding gap is now agenda item (ii), not (i)
p = para_starting("Several limitations qualify every claim")
n = replace_in(p, "and closing this gap is the first item of the research agenda (Section 11.6)",
               "and closing this gap is item (ii) of the research agenda (Section 11.6)")
note(n == 1, "Section 12 agenda cross-reference corrected")

# conclusion
p = para_starting("Within the limits stated in Section 12")
n = replace_in(p, "that database-level screening is not yet frozen",
               "that screening of the retrieved frame was purposive rather than exhaustive")
note(n == 1, "conclusion caveat rewritten")

# abstract
p = para_starting("Virtual power plants (VPPs) turn dispersed flexibility")
n1 = replace_in(p,
                "A candidate corpus of roughly 110 records was compiled, and 39 studies were verified "
                "against publisher metadata and coded against a common evidence matrix.",
                "A five-block query set executed on OpenAlex returned 2,670 records, or 1,668 after "
                "de-duplication, and 39 studies were verified against publisher metadata and coded "
                "against a common evidence matrix.")
n2 = replace_in(p,
                "database-level screening counts are disclosed as pending rather than estimated, and "
                "the DMDI ratings come from a single coding pass pending independent double-coding.",
                "identification counts are reported in full, screening was purposive rather than "
                "exhaustive and its sensitivity is measured, and the DMDI ratings come from a single "
                "coding pass pending independent double-coding.")
note(n1 == 1 and n2 == 1, "abstract updated (edited in place, %d chars)" % len(p.text))

# trim the abstract back under 250 words and fix leftover spellings
for old, new in [
    ("and they do it through a chain of steps that are usually studied one at a time",
     "through a chain of steps usually studied one at a time"),
    ("a richer optimisation model", "a richer optimization model"),
    ("A five-block query set executed on OpenAlex returned 2,670 records, or 1,668 after "
     "de-duplication, and 39 studies were verified against publisher metadata and coded against a "
     "common evidence matrix.",
     "A five-block query set on OpenAlex returned 2,670 records (1,668 after de-duplication); 39 "
     "studies were verified against publisher metadata and coded on a common evidence matrix."),
    ("The pattern is consistent across groupings: ", "The pattern is consistent: "),
    ("The review is reported as a structured, PRISMA-informed evidence review: identification "
     "counts are reported in full, screening was purposive rather than exhaustive and its "
     "sensitivity is measured, and the DMDI ratings come from a single coding pass pending "
     "independent double-coding.",
     "The review is reported as structured and PRISMA-informed: identification counts are complete, "
     "screening was purposive with its sensitivity measured, and the DMDI ratings come from a single "
     "coding pass pending independent double-coding."),
]:
    note(replace_in(p, old, new) == 1, "abstract trim: %r" % old[:45])

# spelling consistency sweep
for old, new in [("optimisation", "optimization"), ("behaviour", "behavior")]:
    hits = 0
    for pp in doc.paragraphs:
        while replace_in(pp, old, new):
            hits += 1
    for tt in doc.tables:
        for r in tt.rows:
            for c in r.cells:
                for pp in c.paragraphs:
                    while replace_in(pp, old, new):
                        hits += 1
    note(True, "spelling sweep %s -> %s (%d replaced)" % (old, new, hits))

# reference [25]
p = para_starting("[25]")
n = replace_in(p, "doi: 10.1049/rpg2.12907", "doi: 10.1049/rpg2.12806")
note(n == 1, "reference [25] DOI corrected to 10.1049/rpg2.12806")

# data availability: name the actual supplementary artefact
p = para_starting("The coding matrix for the 39 verified-core studies")
n = replace_in(p,
               "The coding matrix for the 39 verified-core studies, including the per-dimension DMDI "
               "ratings and the maturity-ladder assignment, is available from the corresponding "
               "author on reasonable request. No new empirical measurements were generated for this "
               "review. The search strings needed to reproduce the retrieval are printed in Section "
               "2.3.",
               "The per-study coding matrix for the 39 verified-core studies is provided as "
               "supplementary file dmdi_coding_matrix.csv. It reproduces the 39 × 8 grid of Fig. 5 — "
               "the seven DMDI dimensions plus the deployment-maturity companion field — and is the "
               "source of every count in Table XI. A blank second-coder version of the same sheet, "
               "and the script that computes per-dimension agreement, accompany it, so that the "
               "double-coding step described in Section 2.7 can be run against the same rules. The "
               "retrieval log in Table I and the search strings in Section 2.3 are sufficient to "
               "re-execute the identification stage. No new empirical measurements were generated "
               "for this review.")
note(n == 1, "data availability statement points to the coding matrix")


# ============================================================ 3. Fig. 1 image
tpl = None
for pp in doc.paragraphs:
    if pp.style.name == "Captioned Figure":
        tpl = pp
        break
if tpl is None:
    raise SystemExit("no Captioned Figure template")

new_el = copy.deepcopy(tpl._p)
fig_p = Paragraph(new_el, cap._parent)
for r in list(fig_p.runs):
    r._r.getparent().remove(r._r)
# drop any leftover drawing/hyperlink containers
for tag in ("drawing", "pict", "hyperlink"):
    for el in new_el.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}" + tag):
        el.getparent().remove(el)
run = fig_p.add_run()
run.add_picture("_draft/fig1_prisma.png", width=Inches(6.4))
fig_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap._p.addprevious(new_el)
note(True, "Fig. 1 image embedded before its caption")

doc.save(DST)
note(True, "saved: " + DST)

# ============================================================ 4. self-check
d2 = docx.Document(DST)
allt = "\n".join(p.text for p in d2.paragraphs)
for t in d2.tables:
    for r in t.rows:
        for c in r.cells:
            allt += "\n" + c.text
for bad in ["n/r", "institutional-account", "roughly 110", "rpg2.12907",
            "pending institutional", "working candidate corpus", "110 records",
            "optimisation", "behaviour"]:
    note(bad not in allt, "leftover check: %r absent" % bad)
note(allt.count("1,668") >= 4, "count 1,668 present (%d times)" % allt.count("1,668"))

fails = sum(1 for x in LOG if x.startswith("FAIL"))
print("\nFAILURES: %d" % fails)
