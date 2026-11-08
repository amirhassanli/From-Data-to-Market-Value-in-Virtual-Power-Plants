# -*- coding: utf-8 -*-
"""Build the English codebook + coder instructions docx for the second coder."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx
from docx.shared import Pt, Cm

doc = docx.Document()

st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10.5)

def h(text, lvl=1):
    doc.add_heading(text, lvl)

def p(text, bold=False):
    par = doc.add_paragraph()
    r = par.add_run(text)
    r.bold = bold
    return par

def li(text):
    doc.add_paragraph(text, style="List Bullet")

# ---------------- title
h("DMDI Second-Coder Codebook and Instructions", 0)
p("For the double-coding agreement study of the review "
  "\u201cFrom Data to Market Value in Virtual Power Plants\u201d. "
  "Version 1.0 (sent to the second coder).", bold=False)

# ---------------- 1 role
h("1. Your role", 1)
p("You are the independent second coder for the review\u2019s DMDI "
  "(Data-to-Market Decision Integrity) evidence matrix. 39 studies have already been "
  "coded once (coder A). Your task is to code the same 39 studies independently, so that "
  "between-coder agreement (Cohen\u2019s kappa) can be measured and disagreements can be "
  "adjudicated into the final published coding.")
li("Code independently. Do NOT ask coder A how any study was coded, and do not look at "
   "coder A\u2019s results before your coding is finished and returned.")
li("Do not use AI assistants (ChatGPT, Copilot, etc.) to code or pre-filter studies. "
   "Use only the full text of each paper and this codebook.")
li("If you are unsure, prefer \u201cPartial\u201d over both extremes and write one line in "
   "the notes column explaining the doubt. Disagreements will be discussed after coding, "
   "not avoided during coding.")
li("Work from the full text (PDF) of each article, obtained via the DOI in the sheet. "
   "Supplementary material counts when it is clearly linked to the paper.")

# ---------------- 2 sheet
h("2. The coding sheet", 1)
p("You receive Coding_Sheet_BLIND.csv with one row per study. Columns:")
li("study, reference, year, doi \u2014 identification only; do not edit.")
li("B_I, B_U, B_D, B_M, B_O, B_S, B_R, B_P \u2014 fill every cell with exactly one token: "
   "E, P, or NR (see Section 3).")
li("notes \u2014 optional; one short sentence is ideal, especially when you code a "
   "dimension P or NR only reluctantly, or when a paper\u2019s wording was ambiguous.")
p("Always give a complete 8-token coding (E/P/NR) for each of the seven DMDI dimensions "
  "I, U, D, M, O, S, R and the companion field P. Never leave a cell blank; if the answer "
  "is genuinely indeterminable, NR plus a note is the correct coding.")

# ---------------- 3 levels
h("3. The three coding levels", 1)
p("Each dimension takes one of three evidence levels (the four-level scheme of "
  "Section 5.2 of the review, with the two NR variants combined for this exercise; if you "
  "can distinguish them, say which in the notes):", bold=False)
p("E (Explicit): the paper itself contains the evidence, and the criterion is fully met. "
  "The reader can point to the sentence/table/figure that demonstrates it.", bold=True)
p("P (Partial): the criterion is partly met, or the evidence is stated only qualitatively, "
  "is ambiguous, or is incomplete on at least one stated sub-criterion.", bold=True)
p("NR (Not reported / not verifiable): the paper either does not address the criterion at "
  "all, or addresses it too weakly to distinguish E from P. If you could not access the "
  "full text, code NR and write \u201cNR-U, full text unseen\u201d in the notes.", bold=True)
p("Key discipline: a dimension is coded on evidence in the paper, not on your assessment "
  "of whether the method is good. A sophisticated DRO model with an unjustified scenario "
  "generator is still not explicit uncertainty integrity.")

# ---------------- 4 dimensions
h("4. Decision rules per dimension", 1)
p("7 dimensions follow the decision chain Information \u2192 Forecast \u2192 Uncertainty \u2192 "
  "Decision \u2192 Bid \u2192 Clearing \u2192 Dispatch \u2192 Deviation \u2192 Settlement \u2192 "
  "Realized Value. For each dimension, E requires ALL the explicit sub-criteria; if "
  "1 of them is missing or only implied, code P.")

h("I \u2014 Information-set integrity", 2)
li("E: the study states (or visibly implements) that decisions are made using only "
   "information available at the decision time it models \u2014 e.g., forecasts generated "
   "only from data preceding the decision gate, no future prices/realizations inside the "
   "decision window.")
li("P: a rolling/look-ahead-free design is stated in general terms, but the information "
   "boundary is not precisely located, or single-step look-ahead remains in one module "
   "(e.g., a post-hoc dispatch fix).")
li("NR: the paper is silent on when each piece of information becomes available.")

h("U \u2014 Uncertainty integrity", 2)
li("E: uncertainty representations (forecast error distributions, scenario sets, ranges) "
   "are empirically derived and characterized \u2014 sources given, dependence or tail "
   "behavior either evidenced from historical data or explicitly calibrated and reported.")
li("P: uncertainty is realistically motivated (e.g., historical forecast errors) but one "
   "link is assumed without evidence \u2014 e.g., independence is assumed, a Wasserstein "
   "radius is tuned but the marginal calibration is not reported, or the scenario count/"
   "reduction rule is not justified.")
li("NR: uncertainty enters only as assumed parameters (e.g., a fixed uncertainty set) "
   "with no empirical characterization.")

h("D \u2014 Decision integrity", 2)
li("E: the optimization/learning policy is evaluated under its own stated constraints "
   "(network limits, ramping, reserve, carbon constraints), with no look-ahead bias: "
   "the holding/tuning of the policy is separated from its evaluation, and reported "
   "performance is achievable by the policy as stated.")
li("P: policy constraints are implemented but evaluation details blur the boundary "
   "(e.g., re-solving per stage with perfect information partly leaking in), or key "
   "constraints are enforced only qualitatively.")
li("NR: the decision problem is described at block-diagram level without enough detail "
   "to verify constraint handling.")

h("M \u2014 Market realism", 2)
li("E: market design is fully instantiated: a named real market (or a clearly stated "
   "faithful replica) with its products (day-ahead/intraday/AS), timing, and clearing/"
   "pricing rule (e.g., pay-as-clear with zonal prices for X), used directly in the model.")
li("P: market mechanisms are modeled on real lines, but a decisive feature is simplified "
   "(e.g., single price area, no transmission constraints, aggregate clearing), or the "
   "market is synthetic but explicitly shaped on a named real design.")
li("NR: market is a generic price-taker assumption or an abstract price signal without "
   "a defined design.")

h("O \u2014 Out-of-sample validity", 2)
p("This is the review\u2019s worked example; apply it literally:")
li("E if all three hold: (i) a chronological train/validation/test split or "
   "rolling-window evaluation is used; (ii) the test period is disjoint from and later "
   "than any period used for fitting/tuning; (iii) quantitative performance is reported "
   "specifically on that held-out period.")
li("P if temporal separation is mentioned but at least one of (ii)\u2013(iii) is missing "
   "or ambiguous (split described only qualitatively; results pool in-sample and "
   "out-of-sample windows).")
li("NR if the paper does not discuss temporal separation at all (note: cross-sectional "
   "random splits and k-fold CV count as absence of chronological separation \u2192 code "
   "NR unless chronological evaluation is also present elsewhere in the paper).")

h("S \u2014 Settlement realism", 2)
li("E: reported profit/cost figures are computed after applying a stated deviation or "
   "imbalance-settlement rule (deviation volumes priced by an explicit penalty/reward "
   "scheme), not solely the ex-ante optimization objective value.")
li("P: a settlement/ex-post deviation component is acknowledged and partially quantified, "
   "but the full financial linkage between day-ahead commitment and imbalance cost is "
   "simplified (e.g., proportional penalty without a mechanism, or imbalance settled at "
   "the day-ahead price).")
li("NR: only ex-ante objective values or simulated profits inside the optimization are "
   "reported; nothing tracks the financial consequence of deviations.")

h("R \u2014 Reproducibility", 2)
li("E: a reader could, in principle, reconstruct the reported experiment from the paper "
   "alone: data sources named (with access route), parameterization complete (or a "
   "linked code/data repository covering it), and the evaluation protocol fully stated.")
li("P: major parameters and sources are given but at least one essential element is "
   "missing to restart the experiment (e.g., no data link, Handbook-of-approximate "
   "parameter values, or evaluation protocol gaps).")
li("NR: neither a data repository nor sufficient parameterization is provided.")

h("P \u2014 Deployment maturity (companion field)", 2)
li("E: documented operational deployment in a real system (field installation, "
   "commercial operation) \u2014 or hardware-in-the-loop/pilot evidence for ALL of the "
   "pipeline the paper claims.")
li("P: pilot/HIL/simulation co-designed with a real operator, or deployment of a "
   "subcomponent.")
li("NR: simulation-only, no operational claim.")

# ---------------- 5 procedure
h("5. Suggested procedure and effort", 1)
li("Pilot pass first: code 10\u201312 studies (any spread across years and venues), "
   "return the sheet; coder A will compare and discuss discrepancies with you to "
   "calibrate borderline judgments; only then continue with the rest.")
li("Budget roughly 30\u201360 minutes per study at full attention (reading method + "
   "experiment sections, checking settlement/evaluation claims). A realistic total is "
   "25\u201340 hours for all 39."
   )
li("Keep reading order as given (or randomize if you prefer); never sort by your "
   "confidence.")
li("Record every judgment in the sheet only \u2014 no parallel summary documents that "
   "cannot be audited.")

# ---------------- 6 after coding
h("6. What happens after you return the sheet", 1)
li("Agreement (observed proportion, Cohen\u2019s kappa per dimension with 95% CI) is "
   "computed automatically from your B_ columns against coder A\u2019s A_ columns; "
   "kappa treats E/P/NR as nominal categories.")
li("Every discrepant cell goes to adjudication: coder A states the evidence used, you "
   "state yours, and the agreed code plus the reason is recorded in an adjudication log.")
li("The final published coding, the kappa table, and the adjudication log become the "
   "data-integrity layer of the review (Sections 2.7 and 10.4).")
li("If any dimension ends below \u22480.60 kappa after adjudication, the codebook rule "
   "for that dimension will be tightened and the affected studies re-coded.")

p("Questions on interpretation: write them in the notes column or in your reply email; "
  "do not resolve them by guessing coder A\u2019s intent.", bold=True)

doc.save(r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\DMDI_Codebook_Second_Coder.docx")
print("written: Downloads\\DMDI_SecondCoder\\DMDI_Codebook_Second_Coder.docx")
