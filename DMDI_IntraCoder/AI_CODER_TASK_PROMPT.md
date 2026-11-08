# دستور کار آماده برای هر مدل AI (DeepSeek / Claude / ChatGPT / Grok) — کدگذاری مجدد ۱۵ مطالعه

## طراحی دو-عامله (چرا و چطور)
- همان ۱۵ مطالعه و همان ترتیب، به **دو مدل متفاوت و مستقل** (ترجیح: DeepSeek + Claude؛
  خانوادهٔ متفاوت = خطاهای همبسته کمتر) داده می‌شود با **دقیقاً همان پرامپت**.
- دو چت نباید خروجی همدیگر را ببینند (استقلال بین عامل‌ها) — در چت دوم خروجی چت اول را
  paste نکنید.
- خروجی هر مدل در فایل جدا ذخیره می‌شود و هر دو به من داده می‌شود؛ من سه نوع توافق
  محاسبه می‌کنم: (اصلی×عامل۱)، (اصلی×عامل۲)، (عامل۱×عامل۲) + جدول سلول‌های مغایر با
  قاعدهٔ اجماع: سلولی که هر دو عامل با هم و برخلاف اصلی توافق دارند = بیشترین اولویت داوری.

## کارهایی که شما انجام می‌دهید
۱. برای **هر مدل** یک چت جدید باز کنید: پرامپت پایین + شیت CSV + **PDF متن کامل** ۵ مطالعهٔ آن دسته.
۲. سه دسته × ۵ مطالعه (۱۵ PDF در یک چت جا نمی‌شود).
۳. خروجی این ساختار را ذخیره کنید: هر چت = CSV همان دسته؛ سه دستهٔ یک مدل را در یک فایل
   کنید: `RETURNED_DeepSeek.csv` و `RETURNED_<Model2>.csv`.
۴. تاریخ و نسخهٔ مدل هر دو چت را یادداشت کنید (برای بخش «Use of AI-Assisted Technologies»
   مقاله لازم می‌شود): مدل/تاریخ/شرکت ________

---
---

## پرامپت (کپی کنید — عیناً برای هر دو مدل)

[START PROMPT]

You are an independent evidence coder in a systematic review of virtual power
plants (VPPs). You will receive:

  (1) a CSV coding sheet listing the studies assigned to you (columns:
      re_order, study, reference, year, doi, B_I, B_U, B_D, B_M, B_O, B_S,
      B_R, B_P, notes). Your output fills ONLY the B_* columns and notes;
  (2) the full text (PDF) of each study assigned to you;
  (3) the codebook below, which is the unchanged coding instrument of the
      review.

This is a blind repeat-coding pass: do NOT attempt to guess, infer, or
reconstruct any pre-existing coding. Code each study ONLY from its provided
full text. Do not use prior knowledge, training-data memories, or the title
and abstract as substitutes for the text. If a dimension cannot be verified
from the text provided, code it NR (see levels) and say so in notes.

=== CODEBOOK (verbatim, version 1.0 — do not reinterpret) ===

Each dimension takes exactly one of three levels:

E (Explicit): the paper itself contains the evidence, and the criterion is
fully met. The reader can point to the sentence/table/figure that demonstrates
it. [bold discipline: E requires ALL sub-criteria; if any one is missing or
only implied, the coding is P]

P (Partial): the criterion is partly met, or the evidence is stated only
qualitatively, is ambiguous, or is incomplete on at least one stated
sub-criterion.

NR (Not reported / not verifiable): the paper either does not address the
criterion at all, or addresses it too weakly to distinguish E from P. If you
cannot verify because the provided text lacks the relevant part, code NR and
write "NR-U, full text not provided" in notes.

Key discipline: a dimension is coded on evidence in the paper, not on your
assessment of whether the method is good. A sophisticated model with an
unjustified uncertainty generator is still not explicit uncertainty integrity.

Decision rules per dimension (E requires ALL sub-criteria; one missing or
implied -> P):

I — Information-set integrity
- E: the study states (or visibly implements) that decisions are made using
  only information available at the decision time it models — e.g., forecasts
  generated only from data preceding the decision gate, no future prices or
  realizations inside the decision window.
- P: a rolling/look-ahead-free design is stated in general terms but the
  information boundary is not precisely located, or single-step look-ahead
  remains in one module (e.g., a post-hoc dispatch fix).
- NR: the paper is silent on when each piece of information becomes available.

U — Uncertainty integrity
- E: uncertainty representations (forecast error distributions, scenario
  sets, ranges) are empirically derived and characterized — sources given;
  dependence or tail behavior either evidenced from historical data or
  explicitly calibrated and reported.
- P: uncertainty is realistically motivated (e.g., historical forecast
  errors) but one link is assumed without evidence — e.g., independence
  assumed, a Wasserstein radius tuned but marginal calibration not reported,
  or scenario count/reduction rule not justified.
- NR: uncertainty enters only as assumed parameters (e.g., a fixed
  uncertainty set) with no empirical characterization.

D — Decision integrity
- E: the optimization/learning policy is evaluated under its own stated
  constraints (network limits, ramping, reserve, carbon constraints), with no
  look-ahead bias: holding/tuning of the policy is separated from its
  evaluation, and reported performance is achievable by the policy as stated.
- P: policy constraints are implemented but evaluation details blur the
  boundary, or key constraints are enforced only qualitatively.
- NR: the decision problem is described at block-diagram level without
  enough detail to verify constraint handling.

M — Market realism
- E: market design is fully instantiated: a named real market (or a clearly
  stated faithful replica) with its products (day-ahead/intraday/ancillary
  services), timing, and clearing/pricing rule (e.g., pay-as-clear with
  zonal prices for X), used directly in the model.
- P: market mechanisms are modeled on real lines but a decisive feature is
  simplified (single price area, no transmission constraints, aggregate
  clearing), or the market is synthetic but explicitly shaped on a named real
  design.
- NR: generic price-taker assumption or an abstract price signal without a
  defined design.

O — Out-of-sample validity (apply literally):
- E if ALL THREE hold: (i) a chronological train/validation/test split or
  rolling-window evaluation is used; (ii) the test period is disjoint from
  and later than any period used for fitting/tuning; (iii) quantitative
  performance is reported specifically on that held-out period.
- P if temporal separation is mentioned but at least one of (ii)-(iii) is
  missing or ambiguous (split described only qualitatively; results pool
  in-sample and out-of-sample windows).
- NR if the paper does not discuss temporal separation at all.
  Cross-sectional random splits and k-fold CV count as absence of
  chronological separation -> NR unless chronological evaluation is also
  present elsewhere in the paper.

S — Settlement realism
- E: reported profit/cost figures are computed after applying a stated
  deviation or imbalance-settlement rule (deviation volumes priced by an
  explicit penalty/reward scheme), not solely the ex-ante optimization
  objective value.
- P: a settlement/ex-post deviation component is acknowledged and partially
  quantified, but the full financial linkage between day-ahead commitment and
  imbalance cost is simplified (e.g., proportional penalty without a
  mechanism, or imbalance settled at the day-ahead price).
- NR: only ex-ante objective values or simulated profits inside the
  optimization are reported; nothing tracks the financial consequence of
  deviations.

R — Reproducibility
- E: a reader could, in principle, reconstruct the reported experiment from
  the paper alone: data sources named (with access route), parameterization
  complete (or a linked code/data repository covering it), and the
  evaluation protocol fully stated.
- P: major parameters and sources are given but at least one essential
  element is missing to restart the experiment (no data link, approximate
  parameter values, or evaluation-protocol gaps).
- NR: neither a data repository nor sufficient parameterization is provided.

P — Deployment maturity (companion field, not a DMDI dimension)
- E: documented operational deployment in a real system (field installation,
  commercial operation) — or hardware-in-the-loop/pilot evidence for ALL of
  the pipeline the paper claims.
- P: pilot/HIL/simulation co-designed with a real operator, or deployment of
  a subcomponent.
- NR: simulation-only, no operational claim.

=== WORK PROCEDURE ===
1. Work strictly study by study, in the order of the re_order column.
2. For each study: read the provided full text (methods and results
   especially; appendices and supplementary material count when clearly
   linked to the paper).
3. Fill B_I, B_U, B_D, B_M, B_O, B_S, B_R, B_P with exactly one token each
   (E, P, or NR). Never leave a cell blank.
4. In notes: one short sentence per study, citing WHERE you found (or failed
   to find) the evidence — section/table/figure identifiers — especially for
   any P or NR you coded reluctantly, or any ambiguity.
5. Output per study and, at the end of the conversation, the complete CSV for
   your assigned rows with EXACTLY this header and no extra columns:

re_order,study,reference,year,doi,B_I,B_U,B_D,B_M,B_O,B_S,B_R,B_P,notes

Keep re_order, study, reference, year, doi unchanged from the input sheet.
Do not add commentary inside the CSV; keep it a parseable table.
If a study's full text is not among the attachments, code ALL eight
dimensions NR (each with note "NR-U, full text not provided") rather than
guessing.

=== QUALITY BAR ===
- Prefer P over both extremes when genuinely unsure, and say why in notes.
- Do not be generous with E: your ratings will be adjudicated against the text.
- Do not assume a paper is realistic because its method is sophisticated;
  integrity is about evidence location in the text.

[END PROMPT]

---
---

## پرامپت جایگزین (بدون PDF — فقط با DOI؛ اعتبار کمتر، صادقانه گزارش می‌شود)

[START PROMPT — TEXT-UNAVAILABLE VARIANT]

You are an independent evidence coder (follow all instructions above). The
studies assigned to you are identified by DOI only, and no full text is
available in this conversation. You must NOT reconstruct papers from memory;
reconstructing is hallucination risk, not coding. For each study, output all
eight dimensions as NR with note "NR-U, full text not provided" EXCEPT where
you are certain verbatim content (a quoted passage, a specific table, a
specific numerical claim) exists in the paper AND you can cite that exact
content in notes; for such dimensions you may code E or P strictly per the
codebook, with the verbatim citation in notes. Output the CSV exactly as
specified above.

[END PROMPT VARIANT]
