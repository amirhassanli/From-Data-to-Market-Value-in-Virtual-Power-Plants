# Simulated peer review and point-by-point response

Both reports were written against the cleaned pre-review version (original manuscript with the production notes, referee-disposition tables, companion-draft material and the uncited reference list removed). The right-hand column states what the post-review manuscript does.

## Reviewer 1 — evidence-synthesis methodology (recommendation: major revision)

| # | Concern | Resolution in the post-review version |
|---|---|---|
| 1.1 | "Systematic" framing is not supported: the 39-study core was not drawn from the database search, and no PRISMA counts exist. | Title and text use "structured evidence review". The database search is repurposed as a coverage audit of the core (recall reported, Section II-E, Fig. 1). Counts are produced by script 01 from real exports. |
| 1.2 | The Fig. 2 box says coding was at "publisher/abstract level"; O, S and R cannot be judged from abstracts, so NR is inflated. | A `coding_basis` field (fulltext/abstract) is recorded per study. The number coded on full text is reported (Sections II-F, XII). The supervisor pack asks for full-text double coding. |
| 1.3 | Reviews were coded on I–R and counted in the 39 denominator, which makes O/S/R look worse. | Reviews are excluded from DMDI coding; all percentages use primary studies only (Table VI). |
| 1.4 | Single coder, no agreement statistic, while the paper criticises reproducibility. | Blinded second coder on 10 randomly drawn primary studies; weighted κ computed by script 02 (Section II-F). |
| 1.5 | The "verified core" contains two entries that the authors themselves could not verify. | Both are flagged `verified = FALSE`, excluded from every count and from the reference list. They can be reinstated only if the DOI appears in a database export. |
| 1.6 | The ladder is inconsistent: studies with O = NR sit at Level 3 although Level 3 requires temporal out-of-sample evidence. | Ladder levels are assigned by a deterministic rule (Table IV) in script 02; the per-study maturity columns were removed from tables. |
| 1.7 | The claim that no dedicated carbon review exists conflicts with the carbon-oriented review in the reference list. | The claim is withdrawn. The contribution is restated as a study-level audit of settlement-consistent, uncertainty-aware carbon modelling (Section IX). |
| 1.8 | The "weak O, S, R" result partly follows from the authors' own strict rules (R = 0 explicit). | The floor effect is stated in Sections VI and XII; conclusions rely on direction, not exact counts. |

## Reviewer 2 — VPP technical and market content (recommendation: major revision)

| # | Concern | Resolution |
|---|---|---|
| 2.1 | Layer-maturity ratings (high/medium/low) in the decision-integrity table are unsupported opinion. | Ratings deleted. Table V is a qualitative threat–countermeasure map with citations. The paragraph claiming it "mirrors" the DMDI result was removed. |
| 2.2 | A robust-bidding study on a Shenzhen campus is described as "field-validated deployment". | The source abstract states a case study on a real-world campus. The text now calls it retrospective evaluation on real campus data and does not place it above Level 4. |
| 2.3 | Citation errors: the campus study cited under the wrong reference number; a market table row attributed to Kim & Choi that describes Choi et al. 2025; one DOI for Fan & Liu does not match the paper (the record reads 10.1049/rpg2.12806); a risk-aware bidding paper carries the author list of a different paper. | All corrected. The Choi et al. row is attributed correctly; the Fan & Liu DOI is fixed; the author list of the risk-aware paper is reduced to "Singh *et al.*" pending a record check (listed in the supervisor email). |
| 2.4 | Figures and tables appear out of order (Fig. 2 before Fig. 1; Fig. 5 before Fig. 4; ladder used before it is defined; Fig. 7 sits before Fig. 8). | All items renumbered in order of first citation. The ladder is defined in Section IV before use. Figures reduced from eight to five, tables from fourteen to eleven. |
| 2.5 | Settlement and out-of-sample evidence is not applicable to every study. | Section VI states that NR on O or S describes the evidence offered, not a defect, for studies without deployment claims. |
| 2.6 | Too many instruments (DMDI, Q1–Q8, four-layer framework, archetypes, coupling levels). | The Q1–Q8 layer, the uncertainty taxonomy, the paradigm table and the technology-maturity discussion were removed. Two coupling views remain, with distinct roles. |
| 2.7 | AI-use disclosure sits in the methods; IEEE requires it in the Acknowledgments with system, sections and level of use. | Moved to the Acknowledgment with all three elements. |
| 2.8 | Carbon archetype examples and the "A4–A6 appear in the most recent studies" claim are not backed by coding. | Examples limited to two studies whose titles state the mechanism; the unsupported claim was removed. |
| 2.9 | Jurisdictional coverage of the core is unknown. | Added as a stated limitation (Section XII). |

## Residual risks after revision (what a third reviewer could still raise)

1. Coverage: if the recall of the core in the formal search is low, the authors must add the missing eligible studies and recode.
2. Full-text recoding of all abstract-coded studies has not been done; this is the largest remaining validity threat.
3. Narrative sentences on data-dependent findings (D and M best reported; O, S, R weak) must be re-read against the Table VI produced by script 02.
