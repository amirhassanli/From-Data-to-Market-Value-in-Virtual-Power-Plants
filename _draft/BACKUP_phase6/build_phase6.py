# -*- coding: utf-8 -*-
"""
Phase 6 build: reviewer-stage-1 fixes that do not depend on the human second coder.

Input : PHASE5 .docx  (edited in place)
Output: same file

1. Block/query wording made consistent everywhere (6 blocks -> 5 retrieval queries).
2. Eligibility (2.2) reconciled with the OpenAlex frame filter (journal articles and
   reviews only; conference papers enter via reference tracing).
3. Limitations paragraph split into five readable paragraphs; "and most importantly"
   removed.
4. "not only" rephrased in prose and in the Q6 cell of Table II.
5. Conclusion's "most importantly" -> "chief among them".
6. Table X reference numbers synced to the Phase 5 reference list.
7. Data Availability names the actual supplementary deliverables.
"""
import copy
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")

doc = docx.Document(P5)
CHANGES = []


def replace_in_paragraph(p, old, new, tag):
    """Replace first occurrence of `old` in paragraph text, run-aware."""
    runs = p.runs
    if not runs:
        return False
    text = "".join(r.text for r in runs)
    if old not in text:
        return False
    i = text.find(old)
    pos = 0
    for run in runs:
        if pos <= i < pos + len(run.text):
            local = i - pos
            run.text = run.text[:local] + new + run.text[local + len(old):]
            CHANGES.append(tag)
            return True
        pos += len(run.text)
    return False


# ---------------------------------------------------------------- 1. blocks/queries
for p in doc.paragraphs:
    replace_in_paragraph(
        p,
        "A six-block query set on OpenAlex returned 2,670 records",
        "Six search blocks, combined into five retrieval queries on OpenAlex, returned 2,670 records",
        "abstract blocks/queries")
    replace_in_paragraph(
        p, "The five blocks return 2,670 records",
        "The five retrieval queries return 2,670 records", "2.4 five blocks")
    replace_in_paragraph(
        p, "The five block queries returned 2,670 records",
        "The five retrieval queries returned 2,670 records", "2.4 five block queries")

# ---------------------------------------------------------------- 2. eligibility
elig = None
for p in doc.paragraphs:
    if p.text.startswith("Eligibility follows the research questions"):
        elig = p
        break
assert elig is not None
ADD = (" The OpenAlex frame itself was restricted to journal articles and reviews "
       "(Table I); conference papers and other document types therefore enter the "
       "corpus only through reference tracing from retrieved works, and the 39 "
       "verified-core studies are all journal articles or reviews.")
if "conference papers and other document types therefore enter" not in elig.text:
    last = elig.runs[-1]
    last.text = last.text.rstrip() + ADD
    CHANGES.append("eligibility reconciled with frame filter")

# ---------------------------------------------------------------- 3. limitations split
lim = None
for p in doc.paragraphs:
    if p.text.startswith("Several limitations qualify every claim"):
        lim = p
        break
assert lim is not None
txt = "".join(r.text for r in lim.runs)
if "Sixth, coverage" in txt and lim.text.count("\n") == 0 and not any(
        "\n" in r.text for r in lim.runs):
    txt2 = txt.replace("First, and most importantly, identification is executed but "
                       "screening is not",
                       "First, identification is executed but screening is not")
    i2 = txt2.find("Second, structured coding")
    i4 = txt2.find("Fourth, the complementary")
    i6 = txt2.find("Sixth, coverage")
    i7 = txt2.find("Seventh, DMDI")
    assert -1 not in (i2, i4, i6, i7)
    parts = [txt2[:i2].rstrip(), txt2[i2:i4].rstrip(), txt2[i4:i6].rstrip(),
             txt2[i6:i7].rstrip(), txt2[i7:].rstrip()]
    # rewrite the original paragraph with part 0
    lim.runs[0].text = parts[0]
    for r in lim.runs[1:]:
        r.text = ""
    # insert remaining parts as new paragraphs with the same style
    cursor = lim._p
    for part in parts[1:]:
        el = copy.deepcopy(lim._p)
        p_el_is_copied = True
        # strip runs from the copy, insert single run with part text
        wraps = el.findall(
            ".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r")
        first_r = wraps[0] if wraps else None
        for r in wraps[1:]:
            r.getparent().remove(r)
        for t_el in first_r.findall(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
            t_el.text = ""
        first_r.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
        ).text = part
        xml_sp = "{http://schemas.openxmlformats.org/xml/pr/1.0}"  # unused
        cursor.addnext(el)
        cursor = el
    CHANGES.append("limitations paragraph split into %d paragraphs" % len(parts))

# ---------------------------------------------------------------- 4. not only
for p in doc.paragraphs:
    replace_in_paragraph(
        p,
        "(deviations, imbalance penalties/rewards), not only the ex-ante objective value.",
        "(deviations, imbalance penalties/rewards), rather than the ex-ante objective value alone.",
        "5.1 not only (prose)")
    replace_in_paragraph(
        p,
        "should be evaluated not only by their mathematical treatment of uncertainty "
        "but by empirical uncertainty-model quality: calibration, coverage, dependence "
        "preservation, temporal correlation, tail behavior, scenario-reduction "
        "distortion, and out-of-sample risk.",
        "should be evaluated as much by their empirical uncertainty-model quality "
        "\u2014 calibration, coverage, dependence preservation, temporal correlation, "
        "tail behavior, scenario-reduction distortion, and out-of-sample risk \u2014 "
        "as by their mathematical treatment of uncertainty.",
        "5.x not only (uncertainty eval)")
for t in doc.tables:
    done = False
    for r in t.rows:
        for c in r.cells:
            if done:
                break
            for cp in c.paragraphs:
                if replace_in_paragraph(
                        cp,
                        "mechanisms are modeled, not only the ex-ante objective value",
                        "mechanisms are modeled, rather than the ex-ante objective value alone",
                        "Table II Q6 not only"):
                    done = True
                    break

# ---------------------------------------------------------------- 5. conclusion
for p in doc.paragraphs:
    replace_in_paragraph(
        p, "\u2014 most importantly, that screening",
        "\u2014 chief among them, that screening", "conclusion most importantly")

# ---------------------------------------------------------------- 6. Table X refs
FIX = [("Liu (2022)", "[31]", "[32]"),
       ("Liu et al. (2024)", "[32]", "[33]"),
       ("Wang et al. (2024)", "[33]", "[34]"),
       ("Bian et al. (2026)", "[34]", "[35]"),
       ("Siqin et al. (2025)", "[63]", "[65]"),
       ("Wang et al. (2025)", "[64]", "[17]")]
t = doc.tables[9]
for r in t.rows[1:]:
    c = r.cells[0]
    label = " ".join(c.text.split())
    for pre, old, new in FIX:
        if label.startswith(pre) and old in c.text:
            cp = c.paragraphs[0]
            if replace_in_paragraph(cp, pre + " " + old, pre + " " + new,
                                    "Table X " + pre):
                break

# ---------------------------------------------------------------- 7. Data Availability
for p in doc.paragraphs:
    replace_in_paragraph(
        p,
        "is provided as supplementary file",
        "is provided as supplementary file DMDI_Coding_Matrix.csv, together with the "
        "DMDI codebook (the explicit coding rules used for each dimension and level) "
        "and the analysis script that regenerates every count in Table XI from the "
        "matrix. It is provided as supplementary file dmdi_coding_matrix",
        "Data Availability") if False else None
for p in doc.paragraphs:
    if p.text.startswith("The per-study coding matrix"):
        replace_in_paragraph(
            p,
            "is provided as supplementary file dmdi_coding_matrix.csv.",
            "is provided as supplementary file DMDI_Coding_Matrix.csv, together with "
            "the DMDI codebook (the explicit coding rules used for each dimension and "
            "level) and the analysis script that regenerates every count in Table XI "
            "from the matrix.",
            "Data Availability")

doc.save(P5)
print("changes applied:")
for c in CHANGES:
    print("  -", c)
print("total:", len(CHANGES))
