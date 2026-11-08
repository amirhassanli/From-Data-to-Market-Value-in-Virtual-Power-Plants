# -*- coding: utf-8 -*-
"""
Phase 6b: identity-level citation fixes (adjudicated against PHASE3 DOI bridge).

Every replacement is keyed to a longer sentence fragment, never a bare number,
so runs of ops inside one paragraph cannot cascade into each other. Idempotent:
each op is skipped automatically once its anchor no longer matches.

Targets fixed:
  * SS3 survey paragraph: 5 review citations restored to Phase-5 numbers
    (Singh [41] re-anchored here -> no orphan).
  * SS5.2 "layers" paragraph: duplicated clause removed; L1/L2/ADMM/Benders/
    Nash/Shapley numbers restored (also repairs Table IV L1/L2 cells).
  * SS6.4 paradigm paragraph: Bertsimas "price of robustness" [61]->[63].
  * SS6.5 RL paragraph: Y.Li hierarchical [65]->[67], Goodfellow [43]->[44].
  * SS6.5 distributed-opt paragraph: Boyd/Benders [53],[54]->[55],[56].
  * SS7 forecast-integrity: [21],[23],[22],[66] -> [22],[24],[23],[69].
  * SS8.1 progression: full 12-token chain restored incl. Kong [71] and
    H.Liu Wasserstein [79] re-anchor.
  * SS8.2 settlement: Song [36], Mousavi [82], Niazi [68].
  * SS8.3 empty-cell: O-explicit ([80],[18]); S-explicit ([70],[15],[36],[10]).
  * SS8.4 Level-5 anchor: Kim & Choi [80].
  * SS9.x carbon gap paragraph: Chang [81], Y.Wang-fleet [34], market-trigger
    Y.Wang [77], Boehmringer [16] re-anchored.
  * SS8.x Table X evidence paragraph: [32],[33],[15] | [35],[65],[66].
  * Table V / Table VI method rows: Rockafellar [59], Ben-Haim [60], Birge [61],
    Charnes [62], Bertsimas [63], Ben-Tal [64].
"""
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")

doc = docx.Document(P5)
APPLIED = []


def edit_text(units, old, new, tag):
    """Run-aware replace of `old` in the first unit whose text contains it."""
    for holder in units:
        if isinstance(holder, docx.table._Cell):
            paras = holder.paragraphs
        else:
            paras = [holder]
        for p in paras:
            runs = p.runs
            if not runs:
                continue
            text = "".join(r.text for r in runs)
            if old not in text:
                continue
            i = text.find(old)
            pos = 0
            for run in runs:
                if pos <= i < pos + len(run.text):
                    lo = i - pos
                    run.text = run.text[:lo] + new + run.text[lo + len(old):]
                    APPLIED.append(tag)
                    return True
                pos += len(run.text)
    return False


# ---------------------------------------------------------------------------
# 1. section 3 survey paragraph (reverse-order-safe via named contexts)
edit_text(doc.paragraphs, "Naval and Yusta [36]", "Naval and Yusta [37]", "S3 Naval")
edit_text(doc.paragraphs, "Mo et al. [37] and Zhu", "Mo et al. [38] and Zhu", "S3 Mo")
edit_text(doc.paragraphs, "Zhu et al. [38] survey", "Zhu et al. [39] survey", "S3 Zhu")
edit_text(doc.paragraphs, "Li et al. [39] give a broad", "Li et al. [40] give a broad", "S3 Li")
edit_text(doc.paragraphs, "Singh et al. [40] concentrate", "Singh et al. [41] concentrate", "S3 Singh")

# ---------------------------------------------------------------------------
# 2. layers paragraph
DUP = ("terms [51].profitable under the two-settlement market design itself "
       "\u2014 i.e., whether the attacker\u2019s objective is stated directly in "
       "market currency rather than in generic system-cost terms [50]. This")
edit_text(doc.paragraphs, DUP, "terms [51]. This", "layers dup-collapse")
edit_text(doc.paragraphs, "[41], [43], whereas a more recent",
          "[42], [43], whereas a more recent", "layers L1 FDIA")
edit_text(doc.paragraphs,
          "flexibility formulations [54], and the temporal-coupling work of "
          "Wang and Wu [52] can leave",
          "flexibility formulations [53], and the temporal-coupling work of "
          "Wang and Wu [54] can leave", "layers LMP")
edit_text(doc.paragraphs, "such as ADMM [53] and Benders decomposition [54] support",
          "such as ADMM [55] and Benders decomposition [56] support", "layers ADMM")
edit_text(doc.paragraphs, "Nash equilibrium analysis [55] and Shapley-value surplus sharing [56] support",
          "Nash equilibrium analysis [57] and Shapley-value surplus sharing [58] support",
          "layers games")

# 3. paradigm paragraph
edit_text(doc.paragraphs, "\u201cprice of robustness\u201d [61]",
          "\u201cprice of robustness\u201d [63]", "paradigm Bertsimas")

# 4. RL paragraph
edit_text(doc.paragraphs, "heterogeneous microgrids [65]",
          "heterogeneous microgrids [67]", "RL Y.Li")
edit_text(doc.paragraphs, "out-of-distribution inputs [43]",
          "out-of-distribution inputs [44]", "RL Goodfellow")

# 5. distributed-opt paragraph
edit_text(doc.paragraphs, "ADMM-based coordination [53] and Benders decomposition [54] let large",
          "ADMM-based coordination [55] and Benders decomposition [56] let large",
          "distopt Boyd/Benders")

# 6. forecast-integrity paragraph
edit_text(doc.paragraphs, "distributed PV [21], long-horizon",
          "distributed PV [22], long-horizon", "forecast [21]->22")
edit_text(doc.paragraphs, "decision support [23], and explicit",
          "decision support [24], and explicit", "forecast [23]->24")
edit_text(doc.paragraphs, "balancing markets [22].",
          "balancing markets [23].", "forecast [22]->23")
edit_text(doc.paragraphs, "aggregated response [66]",
          "aggregated response [69]", "forecast Luo")

# 7. methodological progression paragraph
edit_text(doc.paragraphs, "scenario trees) [18], [67], including",
          "scenario trees) [19], [70], including", "prog SP")
edit_text(doc.paragraphs, "robust stochastic multi-energy dispatch [68]",
          "robust stochastic multi-energy dispatch [71]", "prog Kong")
edit_text(doc.paragraphs, "robust variants [69], [70], [71], and day-ahead",
          "robust variants [72], [73], [75], and day-ahead", "prog variants")
edit_text(doc.paragraphs, "renewable portfolios [72], to distributionally",
          "renewable portfolios [76], to distributionally", "prog day-ahead")
edit_text(doc.paragraphs,
          "approximately 2023 [15], [24], [26], [73], including Wasserstein",
          "approximately 2023 [25], [15], [26], [78], including Wasserstein",
          "prog DRO")
edit_text(doc.paragraphs, "Wasserstein scheduling formulations [74]",
          "Wasserstein scheduling formulations [79]", "prog Wasserstein H.Liu")

# 8. settlement paragraph
edit_text(doc.paragraphs, "imbalance penalties [35], studies",
          "imbalance penalties [36], studies", "settle Song")
edit_text(doc.paragraphs, "frequency-constrained products [76]",
          "frequency-constrained products [82]", "settle Mousavi")
edit_text(doc.paragraphs, "scalable frequency-regulation co-optimization [77]",
          "scalable frequency-regulation co-optimization [68]", "settle Niazi")

# 9. Table X evidence paragraph
edit_text(doc.paragraphs, "recent studies [15], [31], [32].",
          "recent studies [32], [33], [15].", "tblX-evidence A1A3")
edit_text(doc.paragraphs, "most recent studies [34], [63], [64]",
          "most recent studies [35], [65], [66]", "tblX-evidence A4A6")

# 10. empty-cell paragraph
edit_text(doc.paragraphs, "explicit on O ([17], [75])",
          "explicit on O ([80], [18])", "empty-cell O")
edit_text(doc.paragraphs, "explicit on S ([10], [15], [35], [67])",
          "explicit on S ([70], [15], [36], [10])", "empty-cell S")

# 11. Level-5 anchor
edit_text(doc.paragraphs, "portfolio study [75] sits at Level 5",
          "portfolio study [80] sits at Level 5", "level5 Kim&Choi")

# 12. carbon-gap paragraph
edit_text(doc.paragraphs, "single-instrument model misses [80]",
          "single-instrument model misses [81]", "carbon gap Chang1")
edit_text(doc.paragraphs, "fleet/policy-coupling literature [15], [33], [80]",
          "fleet/policy-coupling literature [34], [15], [81]", "carbon gap fleet DRO")
edit_text(doc.paragraphs, "explored at the VPP level [81]",
          "explored at the VPP level [77]", "carbon gap triggers")
edit_text(doc.paragraphs, "trade-exposed operation [82]",
          "trade-exposed operation [16]", "carbon gap Boehmringer")
edit_text(doc.paragraphs, "carbon literature [8], [80]",
          "carbon literature [8], [81]", "carbon gap corroborate")

# ---------------------------------------------------------------------------
# 13. table cells: (tableIdx, row, col, old, new)
CELLS = [
    (3, 1, 2, 0, "[41], [43]", "[42], [43]"),   # L1 Data: FDIA pair
    (3, 2, 2, 0, "[42]", "[44]"),               # L2 Model: Goodfellow
    (4, 5, 3, 0, "[57]", "[59]"),               # Outages: Rockafellar CVaR
    (4, 6, 3, 0, "[44], [58]", "[45], [60]"),   # Model/param error: Esf-Kuhn + Ben-Haim
    (5, 2, 3, 0, "[59]", "[61]"),               # SP: Birge
    (5, 3, 3, 0, "[60]", "[62]"),               # CCP: Charnes
    (5, 4, 3, 0, "[61], [62]", "[63], [64]"),   # RO/ARO: Bertsimas + Ben-Tal
    (5, 6, 3, 0, "[58]", "[60]"),               # IGDT: Ben-Haim
]
for ti, ri, ci, _, old, new in CELLS:
    c = doc.tables[ti].rows[ri].cells[ci]
    if not edit_text([c], old, new, "cell %d r%d c%d" % (ti, ri, ci)):
        # already correct?
        cur = " ".join(c.text.split())
        if old not in cur and new in cur:
            APPLIED.append("cell %d r%d c%d (already fixed)" % (ti, ri, ci))
        else:
            APPLIED.append("cell %d r%d c%d PATTERN NOT FOUND: %r in %r" % (ti, ri, ci, old, cur[:80]))

doc.save(P5)
print("applied %d ops:" % len(APPLIED))
for a in APPLIED:
    print("  -", a)
