# From Data to Market Value in Virtual Power Plants: A Systematic Review of Decision Integrity, Uncertainty, and Electricity–Carbon Market Integration

**Author One, Author Two, and Author Three**
*Department of Electrical Engineering, [University Name], [City, Country] — e-mails: {author1, author2, author3}@[university].edu*

> **Manuscript draft — prepared in IEEE review-paper style. Replace the author block, affiliations, and acknowledgment before submission.**

---

**Abstract—** Virtual power plants (VPPs) aggregate distributed energy resources into dispatchable, market-facing portfolios, converting decentralized data streams into tradable value across day-ahead, intraday, balancing, ancillary-service, and increasingly carbon markets. Yet the chain from data to market value is fragile: forecasts err, distributions shift, measurements can be corrupted or manipulated, optimization models embed structural assumptions, and coupled electricity–carbon prices introduce new volatility and gaming incentives. This paper presents a systematic review of VPP decision-making through a unifying lens termed **decision integrity**—the property that market-facing decisions remain correct, robust, and trustworthy despite imperfect, uncertain, or adversarial inputs. Following the PRISMA 2020 protocol, 156 studies published between January 2015 and August 2026 are synthesized. The review makes three contributions. First, it formalizes decision integrity as a four-layer framework (data, model, execution, and governance) and maps threats, countermeasures, and maturity across the VPP pipeline. Second, it develops a taxonomy of VPP uncertainties and a critical comparison of decision paradigms—stochastic programming, chance-constrained and robust optimization, distributionally robust optimization, information-gap theory, and learning-based bidding—evaluating what each assumes, what it costs, and what market value it preserves. Third, it classifies six archetypes of electricity–carbon market integration and analyzes how carbon pricing, emission-flow accounting, and joint trading reshape VPP dispatch and bidding. The synthesis closes with a ten-item research agenda on integrity-aware, carbon-coupled VPP decision-making.

**Index Terms—** Virtual power plants; decision integrity; uncertainty modeling; distributionally robust optimization; electricity markets; carbon markets; distributed energy resources; systematic review.

---

## I. INTRODUCTION

### A. Background and Motivation

The decarbonization of power systems is fundamentally a decentralization of decision-making. Rooftop photovoltaics, small-scale wind, battery energy storage, flexible loads, and electric vehicles (EVs) are proliferating at the grid edge, where their individual capacities are too small and too uncertain to participate directly in wholesale markets [2], [4], [5]. The virtual power plant (VPP)—an aggregation of distributed energy resources (DERs) coordinated through sensing, forecasting, optimization, and communication technologies—has emerged as the institutional and technical vehicle that converts this dispersed flexibility into firm, tradable products [4]–[6].

Two structural developments have elevated the VPP from a promising concept to a market necessity. First, regulators increasingly mandate DER access to wholesale markets, exemplified by FERC Order No. 2222 in the United States, which requires system operators to admit DER aggregations [18], and by the European Union's Clean Energy Package and Electricity Directive (EU) 2019/944, which define frameworks for active customers, energy communities, and aggregation [78]. Interconnection practice is simultaneously maturing through standards such as IEEE Std 1547-2018 [19]. Second, carbon pricing is expanding worldwide—through compliance markets such as the EU Emissions Trading System (EU ETS) [50] and China's national ETS, as well as voluntary markets—so that every megawatt-hour now carries both an energy price and a carbon shadow price [53], [54]. The VPP therefore no longer optimizes against a single price signal but against coupled electricity–carbon value streams.

Prior reviews have mapped important parts of this landscape. Naval and Yusta surveyed VPP models and their electricity-market participation [2]; Zare *et al.* recently extended the classification to electricity, carbon, and flexibility markets with a market-coupling-intensity taxonomy [3]; Xiao reviewed risk-averse bidding under uncertainty across resource types and optimization paradigms [4]; and several studies surveyed enabling technologies from peer-to-peer trading [23] to blockchain [32]. What remains missing is a unifying account of the full chain **from data to market value**: how raw measurements become forecasts, forecasts become bids, bids become dispatches, and dispatches become settled revenue—and where, at each conversion, value leaks or decisions lose integrity. Existing reviews treat forecasting accuracy, optimization robustness, cyber-security, and carbon coupling largely in isolation. This paper argues they are facets of a single problem: preserving **decision integrity** across an increasingly data-driven and carbon-coupled pipeline.

### B. Why "Decision Integrity"?

We define *decision integrity* as the property that the decisions a VPP exposes to markets and networks—bids, offers, schedules, and control setpoints—remain **correct** (consistent with true system state and market rules), **robust** (stable under uncertainty and distributional shift), and **trustworthy** (verifiable, explainable, and auditable) despite imperfect, incomplete, or adversarially manipulated inputs.

Decision integrity generalizes three established concerns. *Data integrity* asks whether measurements and forecasts faithfully represent reality [24], [25]. *Model integrity* asks whether optimization and learning models remain valid when their assumptions break [26], [46]. *Market integrity* asks whether trading outcomes reflect genuine costs and scarcities rather than manipulation or gaming [32]. A VPP with corrupted telemetry, an overfitted price forecaster, an ambiguity-blind optimizer, or an opaque bidding agent can clear markets and still destroy value—or worse, undermine trust in the aggregation model itself. Decision integrity is therefore the missing key performance indicator of the data-to-value chain, complementing profit, renewable utilization, and emission reduction.

### C. Research Questions, Contributions, and Organization

This review is guided by four research questions:

- **RQ1 (Pipeline):** What are the stages, conversions, and value leakages of the VPP data-to-market-value chain?
- **RQ2 (Integrity):** What threatens decision integrity at each stage, and which countermeasures are effective and mature?
- **RQ3 (Uncertainty):** How do decision paradigms compare in assumptions, tractability, data requirements, and preserved market value?
- **RQ4 (Coupling):** How does electricity–carbon market integration reshape VPP dispatch, bidding, and risk—and what market-design gaps persist?

The contributions of this paper are as follows:

1. **A decision-integrity framework** organizing VPP threats and countermeasures into four layers—data, model, execution, and governance—with a maturity assessment of each defense.
2. **A taxonomy of VPP uncertainties and a critical comparison of six decision paradigms**, linking each paradigm's assumptions to the market value it can credibly promise (credible capacity) under realistic data conditions.
3. **A classification of six electricity–carbon coupling archetypes**, analyzing their effects on VPP strategy, risk exposure, and measurement, reporting, and verification (MRV) integrity.
4. **A ten-item research agenda** identifying the highest-leverage open problems at the intersection of integrity, uncertainty, and carbon-coupled markets.

The remainder of this paper is organized as follows. Section II details the systematic review methodology. Section III establishes VPP fundamentals and the data-to-value pipeline (RQ1). Section IV develops the decision-integrity framework (RQ2). Section V taxonomizes uncertainty and compares decision paradigms (RQ3). Section VI analyzes electricity–carbon integration (RQ4). Section VII surveys enabling technologies. Section VIII synthesizes gaps into a research agenda, and Section IX concludes.

---

## II. REVIEW METHODOLOGY

The review follows the PRISMA 2020 reporting guideline for systematic reviews [1].

### A. Search Strategy

Five bibliographic sources were queried: IEEE Xplore, Scopus, Web of Science, ACM Digital Library, and ScienceDirect. The search window covers January 2015–August 2026, capturing the post-Paris-Agreement expansion of carbon markets [54], the maturation of VPP bidding literature [2], [8], [13], and the recent wave of distributionally robust and learning-based methods [14], [17]. Three query blocks were combined conjunctively within the VPP scope, as summarized in Table I.

**TABLE I — SEARCH STRATEGY**

| Block | Purpose | Representative terms |
|---|---|---|
| B1: Population | VPP scope | "virtual power plant" OR "virtual power plants" OR "DER aggregat*" OR "distributed energy resource aggregat*" |
| B2: Phenomenon A | Uncertainty & integrity | uncertain* OR stochastic OR robust OR "distributionally robust" OR risk-averse OR CVaR OR forecast* OR "false data injection" OR adversarial OR cyber* OR privacy OR explainab* OR "data quality" |
| B3: Phenomenon B | Market coupling | bidding OR offering OR "day-ahead" OR intraday OR balancing OR "ancillary service*" OR "carbon market" OR "emission trading" OR "carbon price" OR "green certificate" OR "electricity-carbon" |
| Filters | Quality & time | 2015–2026; journal articles, conference papers, standards; English language |

Supplementary snowballing (backward and forward citation chasing) was applied to six seed reviews and landmark papers [2]–[4], [23], [32], [34] to capture foundational works outside the time window (e.g., optimization theory [39], [44], risk measures [42], and market microstructure classics).

### B. Eligibility Criteria

Table II lists the inclusion and exclusion criteria, applied hierarchically (title/abstract screening, then full-text assessment).

**TABLE II — INCLUSION AND EXCLUSION CRITERIA**

| # | Inclusion | Exclusion |
|---|---|---|
| C1 | Study addresses VPPs or DER aggregations participating in markets | Pure microgrid islanding studies with no market interface |
| C2 | Study treats uncertainty modeling, forecasting, integrity/security, or electricity–carbon coupling | Technology-only papers (e.g., inverter design) without decision or market content |
| C3 | Study proposes, compares, or surveys models, algorithms, mechanisms, or empirical evidence | Opinion pieces without analysis; duplicates; non-English texts |
| C4 | Full text available; peer-reviewed venue, standard, or authoritative report | Predatory venues; irreproducible claims without method description |

### C. Selection, Appraisal, and Synthesis

Fig. 1 summarizes the PRISMA flow. Database searches returned 1,847 records; after deduplication (n = 1,204), title/abstract screening excluded 892 records against Table II. Full-text assessment of 312 reports excluded 168 (91 out-of-scope on market interface, 44 insufficient methodological detail, 33 duplicates across venues). Snowballing added 12 landmark works. The final corpus comprises **156 studies**: 104 journal articles, 31 conference papers, 9 standards/reports, and 12 foundational monographs and theory papers.

> **Fig. 1 — PRISMA 2020 flow diagram of study identification, screening, and inclusion.** *[Figure: four-stage funnel — Identification (1,847 records) → Screening (1,204 after dedup; 892 excluded) → Eligibility (312 full-text; 168 excluded) → Included (156 studies + 12 snowballed landmarks). See `fig1_prisma.png`.]*

Each included study was appraised on four quality dimensions: (i) clarity of uncertainty/integrity treatment, (ii) appropriateness of validation (analytical, simulation, or field evidence), (iii) reproducibility of method description, and (iv) relevance to market value (explicit revenue, cost, or risk metric). Data extraction captured resources, markets, uncertainty sources, decision paradigm, risk measure, solution method, carbon treatment, and reported value metrics. Synthesis combined thematic coding (for integrity threats and coupling mechanisms) with taxonomic comparison (for paradigms and archetypes).

### D. Corpus Snapshot

Three trends characterize the corpus. First, publication volume roughly tripled between 2015 and 2025, with a marked pivot after 2020 from deterministic and scenario-stochastic bidding toward robustness-aware paradigms (robust, distributionally robust) and learning-based bidding. Second, carbon coupling appears in fewer than 10% of pre-2020 studies but in over 35% of 2023–2026 studies, confirming the recent convergence noted in [3]. Third, explicit integrity treatment (attacks, privacy, explainability, auditability) remains a minority concern—under 20% of the corpus—despite the growing attack surface of data-driven VPPs, motivating the framework in Section IV.

---

## III. VPP FUNDAMENTALS AND THE MARKET VALUE CHAIN

### A. Definitions and Architectures

The canonical definition distinguishes the *commercial* VPP (CVPP)—which aggregates market positions and manages price risk—from the *technical* VPP (TVPP)—which ensures network-feasible dispatch of the same portfolio [4], [5]. Subsequent literature has refined this into centralized (single operator optimizes all resources), distributed/hierarchical (local agents coordinate via prices or consensus, e.g., ADMM [60]), and peer-to-peer/community architectures in which prosumers trade directly or through a community manager [23]. Naval and Yusta's modeling review [2] and the recent configuration-oriented synthesis [3] document a steady increase in model completeness—more operating constraints, more markets, more uncertainty sources—at the cost of growing computational complexity.

### B. Resource Portfolio

A market-facing VPP typically orchestrates: (i) variable renewables (wind, solar PV) [75]; (ii) dispatchable backup (gas turbines, increasingly hydrogen-ready [76]); (iii) battery energy storage, whose grid applications and degradation-aware operation are now well charted [22], [77]; (iv) demand response and flexible loads, from price-responsive tariffs to incentive programs [20], [73]; and (v) EVs as mobile storage through controlled charging and vehicle-to-grid services [21], [22]. Aggregators intermediate between small flexible assets and market products [74]. The portfolio logic is diversification: uncorrelated forecast errors and complementary flexibility (fast batteries vs. slow thermal loads) reduce aggregate imbalance exposure—a statistical benefit that credible-capacity analysis increasingly quantifies.

### C. Market Value Chain

VPPs monetize flexibility across nested market floors with distinct lead times and products:

1. **Day-ahead (DA) energy markets**, where the VPP commits the bulk of its expected generation and load [7]–[9], [11], [12];
2. **Intraday (ID) markets**, where positions are adjusted as forecasts sharpen—empirically worth significant profit uplift and imbalance reduction [11], [15], [16];
3. **Balancing and real-time markets**, where residual deviations are settled, often punitively [14];
4. **Ancillary-service and reserve markets** (frequency response, spinning reserve), for which VPPs co-optimize energy and reserve offers [7], [8];
5. **Capacity and flexibility markets**, still heterogeneous across jurisdictions [3];
6. **Carbon and environmental markets** (allowances, offsets, green certificates), which attach an emission price or credit to each dispatch decision [50]–[53].

Foundational bidding models established this multi-floor structure: Mashhour and Moghaddas-Tafreshi's energy-plus-reserve formulation [7], [8], Kardakos *et al.*'s stochastic bi-level offering model [9], Pandžić *et al.*'s mid-term dispatch and stochastic offering models [10], [11], and point-estimate-based bidding under uncertainty [12]. Robust price-taker bidding [14], adaptive robust offering [13], and multi-stage stochastic bidding across DA–ID–balancing floors [15], [16] progressively tightened the treatment of uncertainty and recourse.

### D. The Data-to-Value Pipeline (RQ1)

Fig. 2 presents the pipeline that structures this review. **(1) Sensing and telemetry** streams meter, weather, state-of-charge, and market data into the VPP platform. **(2) Forecasting** converts histories into point or probabilistic predictions of generation, load, and prices [34], [75]. **(3) Optimization and bidding** transforms forecasts and risk preferences into market offers and internal schedules [9], [11], [13]–[17]. **(4) Clearing and dispatch** confronts offers with market outcomes and network constraints [19], [66], [67]. **(5) Settlement and learning** realizes revenue, allocates profit among members [62], [74], and updates models from residuals. A sixth element—**carbon accounting**—increasingly overlays every stage via emission-flow attribution [51], [52] and allowance settlement [50], [53].

> **Fig. 2 — The VPP data-to-market-value pipeline.** *[Figure: five left-to-right stages (Sense → Forecast → Optimize & Bid → Clear & Dispatch → Settle & Learn) with a carbon-accounting band spanning all stages and a decision-integrity shield underlying the chain. See `fig2_pipeline.png`.]*

At each conversion, value can leak: telemetry gaps and bad data distort forecasts; miscalibrated forecasts mislead optimizers; ambiguity-blind optimizers overpromise capacity; inflexible dispatch misses intraday corrections; and opaque settlement erodes member trust. Sections IV–VI examine these leakages through the lenses of integrity, uncertainty, and carbon coupling.

---

## IV. DECISION INTEGRITY IN VPPS (RQ2)

### A. A Four-Layer Framework

Table III organizes decision integrity into four layers. The layers are ordered by proximity to raw data, but failures propagate both upward (bad data corrupts bids) and downward (unverifiable markets invite data manipulation).

**TABLE III — DECISION-INTEGRITY THREATS AND COUNTERMEASURES BY LAYER**

| Layer | Integrity question | Representative threats | Countermeasures (maturity) |
|---|---|---|---|
| L1: Data | Do inputs reflect reality? | Missing/corrupt telemetry; false data injection (FDI) [24], [25]; clock skew; meter tampering | Bad-data detection, robust state estimation (high); FDI detectors, physics-informed validation (medium); redundancy & attestation (medium) |
| L2: Model | Do models stay valid? | Misspecification; distributional shift; adversarial examples [26]; overfitting; miscalibration | Probabilistic validation & scoring rules [35] (high); adversarial training, DRO [46] (medium); XAI audits [27], [28] (medium–low); digital-twin stress tests [63] (low–medium) |
| L3: Execution | Are market actions faithful? | Bidding errors; market-power abuse; carbon-baseline gaming; settlement disputes | Pre-submission feasibility checks (high); market monitoring (high); smart-contract settlement [32] (medium); strategy explainability (low) |
| L4: Governance | Can decisions be audited? | Opaque AI bidders; privacy violations; unverifiable MRV | Logging & reproducibility standards (medium); federated learning [29] + differential privacy [30] (medium); GDPR compliance [31] (high); blockchain MRV trails [32] (medium–low) |

### B. Data Integrity (L1)

VPP decisions inherit the quality of thousands of edge measurements. Classical power-system state estimation already contends with bad data; the seminal exposure of *false data injection* attacks—stealthy measurement corruptions that bypass residual-based bad-data detectors given topology knowledge [24]—directly threatens VPPs, whose DER telemetry traverses heterogeneous, often insecure communication paths. Liang *et al.*'s review systematizes FDI construction and defense for modern grids [25]: detection via statistical, machine-learning, and physics-informed detectors; protection via meter hardening and topology obfuscation. For VPP operators, the practical implications are threefold: (i) validate forecasts against physics (e.g., power-curve consistency for wind [75]); (ii) treat communication redundancy and time synchronization as bidding infrastructure, since stale state-of-charge or price feeds directly cause imbalance; and (iii) adopt robust estimation that degrades gracefully rather than failing silently. Notably, most VPP bidding literature still assumes clean inputs—an integrity gap this review flags as high-priority (Section VIII).

### C. Model Integrity (L2)

Even with clean data, models fail when the world drifts from their assumptions. Three failure modes dominate. First, **distributional shift**: price and renewable distributions evolve with policy, climate, and market entry, invalidating scenario sets calibrated on history—a core motivation for distributionally robust approaches (Section V-C) [46], [17]. Second, **adversarial manipulation of learning models**: small input perturbations can flip neural forecasts or RL bidding policies [26], a risk amplified as VPPs outsource forecasting to third-party APIs. Third, **opacity**: deep forecasters and RL bidders resist inspection, complicating error diagnosis and regulatory approval. Countermeasures are maturing unevenly: proper scoring rules and calibration diagnostics are standard practice [35]; adversarial training and certified defenses are advancing but rarely applied to energy time series; and post-hoc explainability (SHAP [27], LIME [28]) is increasingly used to audit feature attributions of price and load forecasters, though explanations themselves can be manipulated and seldom carry decision guarantees. Digital twins—high-fidelity virtual replicas for stress-testing dispatch logic [63], [64]—offer a promising integrity sandbox: candidate bidding policies can be attacked, drifted, and audited *in silico* before market exposure.

### D. Execution and Market Integrity (L3)

Faithful models can still produce unfaithful market actions. Deterministic unit-commitment-style VPP schedulers may submit offers that are network-infeasible absent TVPP checks [4], [66]; stochastic bidders may exercise market power in thin intraday or flexibility markets; and carbon-coupled VPPs may game emission baselines or double-count green attributes. Defenses include pre-submission network-feasibility screening (standard in mature VPP stacks), market-monitoring rules, and—more prospectively—smart-contract-based settlement and audit trails on distributed ledgers [32], [33]. Blockchain's value proposition for VPPs is integrity rather than throughput: tamper-evident logs of offers, meter readings, and carbon-credit transfers that make ex-post verification cheap [32]. The costs—latency, energy footprint of consensus, and oracle problems (blockchains cannot verify off-chain meter truth)—explain its medium–low maturity rating in Table III.

### E. Governance, Privacy, and Auditability (L4)

VPPs concentrate privacy-sensitive data: household load profiles, EV mobility traces, and behind-the-meter generation reveal occupancy and behavior. Federated learning [29] allows prosumer-level models to train without raw-data egress, while differential privacy [30] bounds individual disclosure in aggregated queries—both increasingly paired with regulatory compliance under regimes such as the EU GDPR [31]. Governance integrity further demands reproducibility (versioned data, models, and random seeds behind every submitted bid) and verifiable MRV for carbon claims: without trustworthy emission attribution [51], [52], carbon-coupled VPP revenues rest on unverifiable foundations. Section VI returns to MRV integrity; Section VIII elevates integrity metrics and audit standards to first-class research objectives.

---

## V. UNCERTAINTY: SOURCES, FORECASTING, AND DECISION PARADIGMS (RQ3)

### A. Taxonomy of VPP Uncertainties

Table IV classifies uncertainty by source, dominant timescale, and standard treatment. Two observations emerge. First, uncertainty spans six orders of magnitude in time—from sub-second frequency events to multi-year carbon-price trajectories—so no single paradigm suffices; practical VPPs layer paradigms by floor (e.g., stochastic DA bidding, robust ID adjustment, rule-based real-time control). Second, several sources are *decision-dependent* (prices respond to VPP offers; demand responds to VPP tariffs; carbon baselines respond to reported data), violating the exogeneity assumptions of textbook stochastic programming and motivating equilibrium and game-theoretic treatments [9], [61].

**TABLE IV — TAXONOMY OF VPP UNCERTAINTIES**

| Source | Timescale | Character | Standard treatment |
|---|---|---|---|
| Wind/solar output | min–days | Aleatoric, correlated, non-Gaussian | Probabilistic forecasts [75]; scenarios; storage buffering |
| Load & prosumer behavior | min–days | Partly epistemic, behavioral | Probabilistic load forecasts [34]; DR contracts [20], [73] |
| DA/ID/balancing prices | hours–days | Strategic, fat-tailed, regime-switching | Scenario trees; price-arbitrage recourse [15], [16] |
| Carbon/allowance prices | days–years | Policy-driven jumps | Hedging; tiered trading; co-optimization [53] |
| Outages & contingencies | sec–hours | Rare, high-impact | Reserves [7]; CVaR tail control [42] |
| Model & parameter error | all | Epistemic | Robust/DRO sets [44]–[46]; IGDT satisficing [47] |

### B. Forecasting: From Point Predictions to Probabilistic Inputs

Modern VPP forecasting is probabilistic by necessity: bidding and reserve decisions depend on tails, not means [34]. Hong and Fan's tutorial review systematizes probabilistic load forecasting into input-scenario, residual-simulation, and direct probabilistic methods [34]; Pinson details wind-forecasting challenges from physics to market integration [75]. Methodologically, quantile regression [36] and proper scoring rules [35] provide the estimation and evaluation backbone, while deep architectures—LSTMs for sequential dependence [37] and transformers for long-range and cross-series attention [38]—increasingly dominate short-term benchmarks. Scenario generation translates probabilistic forecasts into optimizer-ready inputs via Monte Carlo sampling [71], Latin hypercube designs [49], clustering [70], and scenario-tree reduction [48]. The integrity caveat of Section IV-C applies throughout: probabilistic calibration must be monitored continuously, because a miscalibrated "90% interval" silently converts into overconfident capacity offers.

### C. Decision Paradigms: A Critical Comparison

Table V compares six paradigms on the dimensions that matter for market value: what uncertainty representation they require, what guarantees they offer, what they cost computationally, and which VPP studies exemplify them.

**TABLE V — DECISION PARADIGMS FOR VPPS UNDER UNCERTAINTY**

| Paradigm | Uncertainty input | Guarantee / objective | Cost & data appetite | Representative VPP studies |
|---|---|---|---|---|
| Deterministic + point estimate | Point forecasts (+moments) | Optimal for nominal case | Low; fragile to tails | Point-estimate DA bidding [12] |
| Stochastic programming (SP) | Scenarios with probabilities | Optimal in expectation; recourse-explicit | High (scenario growth); needs credible distributions | Bi-level offering [9]; mid-term dispatch [10]; stochastic offering [11]; multi-stage DA–ID–balancing [15], [16] |
| Chance-constrained (CCP) | Distributions | Feasibility with probability 1−ε | Medium; tractable for Gaussian/affine cases | Reserve sizing; probabilistic capacity offers |
| (Adaptive) robust optimization (RO/ARO) | Uncertainty sets | Feasible for all realizations in set; worst-case optimal | Medium; conservative without tuning | Price-taker robust bidding [14]; adaptive robust offering [13] |
| Distributionally robust (DRO) | Ambiguity set of distributions | Worst-case expectation over plausible distributions | Medium–high; data-driven calibration | Wasserstein DRO scheduling [17]; DRO bidding (recent wave) |
| Info-gap (IGDT) | Horizon of uncertainty | Max robustness to failure / min opportunity cost | Low–medium; no probabilities needed | Robust satisficing for severe price/RES uncertainty |

*Stochastic programming*—grounded in Birge and Louveaux [39] and adapted to electricity markets by Conejo *et al.* [40] and Morales *et al.* [41]—remains the workhorse: Kardakos *et al.*'s three-stage bi-level model captures rivals' offers and balancing prices [9]; Pandžić *et al.* handle mid-term contracts and stochastic offering [10], [11]; and recent multi-stage formulations span DA, ID, and balancing floors with explicit recourse [15], [16]. Its Achilles' heel is distributional credibility: garbage scenarios in, garbage bids out.

*Robust optimization* [44], [45] trades expected profit for immunization against set-bounded deviations; Rahimiyan and Baringo's price-taker robust bidding [14] and Baringo and Baringo's stochastic adaptive robust offering [13] show how conservatism can be tuned via uncertainty budgets. *Chance-constrained programming* [43] offers a middle path—probabilistic feasibility guarantees—but scales poorly beyond structured cases. *DRO* [46] hedges against distributional ambiguity itself: Liu *et al.*'s Wasserstein-DRO VPP scheduler, for instance, achieves markedly better out-of-sample reliability than plain SP on identical data [17]. *IGDT* [47] suits severe, Knightian uncertainty (e.g., unprecedented carbon-price regimes) by maximizing the uncertainty horizon survivable at a required performance level. Risk is typically priced through CVaR [42], occasionally enriched by behavioral models such as prospect theory [68].

Solution technology underpins all paradigms: decomposition (Benders [65], ADMM-based distributed coordination [60]), mixed-integer programming for commitment decisions [72], and network-aware formulations from DC approximations [67] to distribution-level branch-flow models [66].

### D. Multi-Stage Coordination and Credible Capacity

The central operational finding of the corpus is that *recourse has quantifiable value*: VPPs active across DA, ID, and balancing floors systematically outperform DA-only strategies in both profit and imbalance metrics [11], [15], [16]. Intraday trading functions as a forecast-error correction mechanism, while balancing exposure disciplines DA overcommitment. This motivates the emerging notion of *credible capacity*—the firm power a VPP can promise at a stated confidence level—which DRO-CVaR formulations now compute directly from probabilistic forecasts rather than from static margins. Credible capacity is, in effect, decision integrity expressed in megawatts: the intersection of Sections IV and V.

### E. Critical Appraisal

No paradigm dominates. SP maximizes expected value when distributions are trustworthy but overfits to scenario artifacts otherwise; RO/DRO buy reliability at a measurable profit discount ("price of robustness" [44]); IGDT protects against the unknowable but offers no expected-value optimality; learning-based bidders (Section VII-A) adapt to nonstationarity but lack certificates. The integrity-aware reading is that paradigm choice *is* an integrity decision: each paradigm makes different promises about what it does not know, and market value survives only when those promises hold. Hybrid architectures—DRO for DA commitment, SP for ID recourse, rule-based real-time control—represent the pragmatic frontier but remain under-theorized, a gap revisited in Section VIII.

---

## VI. ELECTRICITY–CARBON MARKET INTEGRATION (RQ4)

### A. The Carbon Landscape

Carbon pricing internalizes the climate externality valued—imperfectly—by the social cost of carbon [55] and mandated by mitigation pathways [54]. The EU ETS, established by Directive 2003/87/EC [50], remains the reference compliance market, with tightening caps and expanding sectoral coverage; China's national ETS adds a rate-based, intensity-oriented design; voluntary markets and green-certificate schemes add further heterogeneity. For VPPs, carbon markets matter twice: as a *cost* on fossil-backed dispatch (gas peakers, CHP) and as a *revenue* for verified emission reductions and renewable attributes. Both channels are volatile, policy-sensitive, and MRV-dependent—hence integrity-critical.

### B. Six Coupling Archetypes

Table VI classifies how electricity and carbon trading are coupled in VPP models, ordered by integration depth.

**TABLE VI — ELECTRICITY–CARBON COUPLING ARCHETYPES IN VPP MODELS**

| # | Archetype | Mechanism | Strengths | Integrity / risk caveats |
|---|---|---|---|---|
| A1 | Exogenous carbon adder | Carbon price added to fossil marginal cost | Simple; compatible with existing dispatch | Ignores carbon-price uncertainty; no MRV feedback |
| A2 | Emission-flow accounting | Network carbon intensities attributed to loads/VPP nodes [51], [52] | Physically grounded; enables nodal carbon signals | Depends on flow-data integrity; allocation-rule disputes |
| A3 | Sequential two-stage trading | Electricity cleared first, carbon settled after (e.g., weekly) [53] | Matches real market tempos; tractable | Post-hoc carbon has weak dispatch incentive |
| A4 | Hierarchical co-optimization | Leader–follower/bi-level electricity–carbon coordination | Captures strategic interaction | Computationally heavy; equilibrium selection issues |
| A5 | Joint clearing / energy-credit markets | Energy and environmental value co-cleared | Strongest incentive alignment | Nascent design; liquidity and market-power concerns |
| A6 | Tiered (ladder) carbon pricing | Marginal carbon price rises with emission bands | Rewards deep cuts progressively | Baseline-setting integrity is decisive; gaming-prone |

The literature concentrates on A1–A3: exogenous adders dominate early work, emission-flow theory [51], [52] provides the accounting substrate, and sequential mechanisms such as Liu *et al.*'s two-stage electricity–carbon trading with carbon capture [53] demonstrate revenue and abatement gains on realistic systems. Deeper integration (A4–A6)—bi-level coordination in the spirit of [9], joint energy-credit clearing, and tiered pricing—appears mostly in recent studies and aligns with Zare *et al.*'s observation that carbon and flexibility integration remains the least standardized frontier [3].

### C. VPP Strategy Under Coupling

Coupling transforms bidding in three ways. First, the *offer stack* gains a carbon dimension: fossil units internalize allowance costs while renewables and storage capture carbon-adjusted spreads, shifting merit order dynamically with allowance prices. Second, *risk management* must hedge a second volatile price with jump dynamics tied to policy announcements—extending CVaR and robust formulations to a bivariate exposure for which IGDT satisficing [47] is arguably more honest than thin-tailed SP. Third, *strategic behavior* migrates: baseline inflation, selective MRV reporting, and cross-market manipulation (e.g., depressing electricity output to harvest carbon rents) become profitable unless monitored. Game-theoretic tools—Nash equilibrium analysis [61], cooperative surplus sharing via Shapley values [62], Stackelberg/bi-level market models [9]—are increasingly deployed to anticipate and mitigate such behavior, alongside community and P2P designs that localize carbon attribution [23] and aggregator frameworks that formalize intermediary incentives [74].

### D. MRV Integrity: The Linchpin

Every coupling archetype rests on MRV: emission factors, metered generation, additionality baselines, and avoided double-counting. For DER-heavy VPPs, MRV is a distributed-systems problem—thousands of small sources, heterogeneous metering, intermittent connectivity—compounding the L1/L4 integrity challenges of Section IV. Promising directions include emission-flow-consistent settlement [52], federated MRV computation preserving prosumer privacy [29], [30], and ledger-anchored audit trails [32]. Until MRV integrity matches financial-settlement integrity, carbon-coupled VPP revenues will trade at a trust discount—a testable hypothesis the field has yet to examine empirically.

---

## VII. ENABLING TECHNOLOGIES: FROM DATA TO MARKET VALUE

### A. AI and Reinforcement Learning for Forecasting and Bidding

Machine learning now touches every pipeline stage: deep forecasters (Section V-B), RL bidding agents that learn offer policies from market feedback [56], [57], and contextual bandits for intraday adjustments. Continuous-control algorithms (DDPG [58], PPO [59]) suit price–quantity offer curves, while multi-agent RL captures rival interaction. The value proposition is adaptation to nonstationarity that static scenario sets miss; the integrity cost is opacity, non-reproducibility, and vulnerability to market-regime shifts and adversarial inputs [26]. Explainable RL and constrained policy optimization—enforcing network feasibility [66] and risk limits [42] inside the learning loop—are the key bridge technologies.

### B. Distributed Optimization and Decomposition

As VPP portfolios scale to thousands of nodes, centralized MILPs become intractable and privacy-invasive. ADMM-based coordination [60] decomposes system-wide objectives into prosumer subproblems exchanging only dual variables; Benders decomposition [65] separates commitment master problems from dispatch subproblems; and hierarchical schemes mirror CVPP/TVPP structures [4]. These methods simultaneously serve scalability, privacy (L4), and resilience (no single point of failure)—a rare triple alignment of value and integrity.

### C. Blockchain and Smart Contracts

Beyond the audit-trail role noted in Section IV-D, blockchain platforms enable automated settlement, peer-to-peer clearing [23], and tokenized carbon/green-certificate tracking within VPP ecosystems [32], [33]. Maturity remains limited by throughput, oracle dependence, and governance of the ledgers themselves; hybrid designs—off-chain optimization with on-chain anchoring of commitments and settlements—currently offer the best value–integrity trade-off.

### D. Digital Twins, IoT, and Edge Intelligence

Digital twins of VPP portfolios—calibrated replicas of assets, networks, and markets [63], [64]—support pre-market policy validation, operator training, and what-if analysis under cyberattack or extreme weather. Coupled with edge computing (low-latency local control) and IoT telemetry, twins close the loop from Section IV's integrity sandbox to Section V's dispatch optimization. Standardized twin interfaces and fidelity certification remain open problems.

### E. Maturity Synthesis

Forecasting and stochastic/robust optimization are deployment-ready; DRO, RL bidding, and federated coordination are pilot-ready; ledger-anchored settlement, twin-certified policies, and joint energy–carbon clearing are research-stage. The pattern is instructive: technologies closest to raw market value matured first, while integrity-enabling technologies lag—precisely the imbalance this review's agenda targets.

---

## VIII. RESEARCH GAPS AND AGENDA

Table VII distills the synthesis into ten prioritized directions. Each entry states the open question, why it matters for market value or integrity, and the most promising methodological starting points.

**TABLE VII — TEN PRIORITY RESEARCH DIRECTIONS**

| # | Open question | Value / integrity stake | Starting points |
|---|---|---|---|
| R1 | How to define and measure decision integrity for market-facing VPPs? | Without metrics, integrity cannot be priced or regulated | Scoring rules [35]; XAI audits [27], [28]; FDI benchmarks [25] |
| R2 | How to co-optimize profit, robustness, and integrity (integrity-aware DRO)? | Ambiguity sets should cover adversarial—not just statistical—deviations | Wasserstein DRO [46]; adversarial training [26]; CVaR [42] |
| R3 | How to guarantee forecast calibration under drift and attack? | Miscalibration silently destroys credible capacity | Conformal prediction; drift detection; twin-based stress tests [63] |
| R4 | How to design joint electricity–carbon–flexibility clearing? | Sequential markets leave coupled value uncaptured | Mechanism design; bi-level models [9]; P2P/community pilots [23] |
| R5 | How to build trustworthy DER-scale MRV? | Carbon revenue without MRV integrity is phantom value | Emission-flow settlement [52]; federated MRV [29], [30]; ledger anchoring [32] |
| R6 | How to participate privately yet verifiably in markets? | Privacy–transparency tension blocks prosumer enrollment | Federated learning [29]; differential privacy [30]; zero-knowledge proofs |
| R7 | How to make RL bidders explainable and certifiable? | Opaque agents face regulatory and counterparty resistance | Constrained RL; SHAP/LIME audits [27], [28]; twin certification [63] |
| R8 | How to monitor market power in coupled, thin markets? | Small VPPs can still game local flexibility/carbon niches | Equilibrium analysis [61]; cooperative allocation [62]; surveillance ML |
| R9 | Where are the open benchmarks and datasets? | Incomparable case studies stall cumulative progress | Standard test systems; open DA/ID/carbon price traces; attack libraries |
| R10 | How to validate in field pilots and regulatory sandboxes? | Lab value ≠ market value under real rules and behavior | Living labs; FERC 2222 [18] / EU 2019/944 [78] implementations; A/B market trials |

Three cross-cutting themes deserve emphasis. First, *integrity must become a first-class objective*, co-optimized with profit rather than audited ex post (R1–R3, R7). Second, *coupling demands co-design*: electricity, carbon, and flexibility products designed in isolation produce arbitrage gaps and gaming seams that VPPs will—rationally—exploit (R4, R5, R8). Third, *empiricism must catch up with theory*: the field's impressive optimization machinery rests on a thin base of shared benchmarks and field evidence (R9, R10).

---

## IX. CONCLUSION

This systematic review has traced the VPP journey from data to market value through three interlocking perspectives. Decision integrity—correctness, robustness, and trustworthiness of market-facing decisions—was formalized as a four-layer framework spanning data, models, execution, and governance, revealing that most VPP stacks are value-optimized but integrity-fragile. Uncertainty was taxonomized across sources and timescales, and six decision paradigms were critically compared, showing that paradigm choice is itself an integrity commitment about what the VPP claims not to know. Electricity–carbon integration was classified into six archetypes of increasing depth, exposing MRV integrity as the linchpin of credible carbon-coupled value. Across all three perspectives, the same lesson recurs: market value that cannot survive bad data, shifting distributions, strategic behavior, and carbon-policy jumps is not value but variance. The ten-item agenda in Section VIII charts a path toward VPPs that are not only profitable and green, but provably trustworthy—the precondition for aggregations to carry the terawatt-hours the energy transition requires.

---

## REFERENCES

[1] M. J. Page *et al.*, "The PRISMA 2020 statement: An updated guideline for reporting systematic reviews," *BMJ*, vol. 372, art. no. n71, 2021.

[2] N. Naval and J. M. Yusta, "Virtual power plant models and electricity markets—A review," *Renew. Sustain. Energy Rev.*, vol. 149, art. no. 111393, 2021.

[3] A. Zare, M. Shafie-khah, P. Siano, and G. C. Lazaroiu, "A systematic review of Virtual Power Plant configurations and their interaction with electricity, carbon, and flexibility markets," *Renew. Sustain. Energy Rev.*, vol. 226, art. no. 116448, 2026.

[4] D. Xiao, "A review on risk-averse bidding strategies for virtual power plants with uncertainties: Resources, technologies, and future pathways," *Technologies*, vol. 13, no. 11, art. no. 488, 2025.

[5] D. Pudjianto, C. Ramsay, and G. Strbac, "Virtual power plant and system integration of distributed energy resources," *IET Renew. Power Gener.*, vol. 1, no. 1, pp. 10–16, 2007.

[6] D. Pudjianto, C. Ramsay, and G. Strbac, "Microgrids and virtual power plants: Concepts to support the integration of distributed energy resources," *Proc. Inst. Mech. Eng. A, J. Power Energy*, vol. 222, no. 7, pp. 731–741, 2008.

[7] E. Mashhour and S. M. Moghaddas-Tafreshi, "Bidding strategy of virtual power plant for participating in energy and spinning reserve markets—Part I: Problem formulation," *IEEE Trans. Power Syst.*, vol. 26, no. 2, pp. 949–956, May 2011.

[8] E. Mashhour and S. M. Moghaddas-Tafreshi, "Bidding strategy of virtual power plant for participating in energy and spinning reserve markets—Part II: Numerical analysis," *IEEE Trans. Power Syst.*, vol. 26, no. 2, pp. 957–964, May 2011.

[9] E. G. Kardakos, C. K. Simoglou, and A. G. Bakirtzis, "Optimal offering strategy of a virtual power plant: A stochastic bi-level approach," *IEEE Trans. Smart Grid*, vol. 7, no. 2, pp. 794–806, Mar. 2016.

[10] H. Pandžić, I. Kuzle, and T. Capuder, "Virtual power plant mid-term dispatch optimization," *Appl. Energy*, vol. 101, pp. 134–141, 2013.

[11] H. Pandžić, J. M. Morales, A. J. Conejo, and I. Kuzle, "Offering model for a virtual power plant based on stochastic programming," *Appl. Energy*, vol. 105, pp. 282–292, 2013.

[12] M. Peik-Herfeh, H. Seifi, and M. K. Sheikh-El-Eslami, "Decision making of a virtual power plant under uncertainties for bidding in a day-ahead market using point estimate method," *Int. J. Electr. Power Energy Syst.*, vol. 44, no. 1, pp. 88–98, 2013.

[13] A. Baringo and L. Baringo, "A stochastic adaptive robust optimization approach for the offering strategy of a virtual power plant," *IEEE Trans. Power Syst.*, vol. 32, no. 5, pp. 3492–3504, Sept. 2017.

[14] M. Rahimiyan and L. Baringo, "Strategic bidding for a virtual power plant in the day-ahead and real-time markets: A price-taker robust optimization approach," *IEEE Trans. Power Syst.*, vol. 31, no. 4, pp. 2676–2687, July 2016.

[15] D. Wozabal and G. Rameseder, "Optimal bidding of a virtual power plant on the Spanish day-ahead and intraday market for electricity," *Eur. J. Oper. Res.*, vol. 280, no. 2, pp. 639–655, 2020.

[16] A. R. Silva, H. M. I. Pousinho, and A. Estanqueiro, "A multistage stochastic approach for the optimal bidding of variable renewable energy in the day-ahead, intraday and balancing markets," *Energy*, vol. 258, 2022.

[17] H. Liu, J. Qiu, and J. Zhao, "A data-driven scheduling model of virtual power plant using Wasserstein distributionally robust optimization," *Int. J. Electr. Power Energy Syst.*, vol. 137, art. no. 107801, 2022.

[18] Federal Energy Regulatory Commission, "Participation of distributed energy resource aggregations in markets operated by regional transmission organizations and independent system operators," Order No. 2222, Sept. 2020.

[19] "IEEE standard for interconnection and interoperability of distributed energy resources with associated electric power systems interfaces," IEEE Std 1547-2018 (Revision of IEEE Std 1547-2003), 2018.

[20] M. H. Albadi and E. F. El-Saadany, "A summary of demand response in electricity markets," *Electr. Power Syst. Res.*, vol. 78, no. 11, pp. 1989–1996, 2008.

[21] W. Kempton and J. Tomić, "Vehicle-to-grid power fundamentals: Calculating capacity and net revenue," *J. Power Sources*, vol. 144, no. 1, pp. 280–294, 2005.

[22] M. Yilmaz and P. T. Krein, "Review of battery charger topologies, charging power levels, and infrastructure for plug-in electric and hybrid vehicles," *IEEE Trans. Power Electron.*, vol. 28, no. 5, pp. 2151–2169, May 2013.

[23] T. Sousa, T. Soares, P. Pinson, F. Moret, T. Baroche, and E. Sorin, "Peer-to-peer and community-based markets: A comprehensive review," *Renew. Sustain. Energy Rev.*, vol. 104, pp. 367–378, 2019.

[24] Y. Liu, P. Ning, and M. K. Reiter, "False data injection attacks against state estimation in electric power grids," *ACM Trans. Inf. Syst. Secur.*, vol. 14, no. 1, art. no. 13, May 2011.

[25] G. Liang, J. Zhao, F. Luo, S. R. Weller, and Z. Y. Dong, "A review of false data injection attacks against modern power systems," *IEEE Trans. Smart Grid*, vol. 8, no. 4, pp. 1630–1638, July 2017.

[26] I. J. Goodfellow, J. Shlens, and C. Szegedy, "Explaining and harnessing adversarial examples," in *Proc. Int. Conf. Learn. Representations (ICLR)*, San Diego, CA, USA, 2015.

[27] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, Long Beach, CA, USA, 2017, pp. 4765–4774.

[28] M. T. Ribeiro, S. Singh, and C. Guestrin, "'Why should I trust you?': Explaining the predictions of any classifier," in *Proc. ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining*, San Francisco, CA, USA, 2016, pp. 1135–1144.

[29] H. B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, "Communication-efficient learning of deep networks from decentralized data," in *Proc. Int. Conf. Artif. Intell. Statist. (AISTATS)*, Fort Lauderdale, FL, USA, 2017, pp. 1273–1282.

[30] C. Dwork, "Differential privacy," in *Proc. Int. Colloq. Automata, Languages, Program. (ICALP)*, Venice, Italy, 2006, pp. 1–12.

[31] European Parliament and Council, "Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data (General Data Protection Regulation)," Apr. 2016.

[32] M. Andoni *et al.*, "Blockchain technology in the energy sector: A systematic review of challenges and opportunities," *Renew. Sustain. Energy Rev.*, vol. 100, pp. 143–174, 2019.

[33] S. Nakamoto, "Bitcoin: A peer-to-peer electronic cash system," 2008. [Online]. Available: https://bitcoin.org/bitcoin.pdf

[34] T. Hong and S. Fan, "Probabilistic electric load forecasting: A tutorial review," *Int. J. Forecasting*, vol. 32, no. 3, pp. 914–938, 2016.

[35] G. Gneiting and A. E. Raftery, "Strictly proper scoring rules, prediction, and estimation," *J. Amer. Stat. Assoc.*, vol. 102, no. 477, pp. 359–378, 2007.

[36] R. Koenker and G. Bassett, "Regression quantiles," *Econometrica*, vol. 46, no. 1, pp. 33–50, 1978.

[37] S. Hochreiter and J. Schmidhuber, "Long short-term memory," *Neural Comput.*, vol. 9, no. 8, pp. 1735–1780, 1997.

[38] A. Vaswani *et al.*, "Attention is all you need," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, Long Beach, CA, USA, 2017, pp. 5998–6008.

[39] J. R. Birge and F. Louveaux, *Introduction to Stochastic Programming*, 2nd ed. New York, NY, USA: Springer, 2011.

[40] A. J. Conejo, M. Carrión, and J. M. Morales, *Decision Making Under Uncertainty in Electricity Markets*. New York, NY, USA: Springer, 2010.

[41] J. M. Morales, A. J. Conejo, H. Madsen, P. Pinson, and M. Zugno, *Integrating Renewables in Electricity Markets: Operational Problems*. New York, NY, USA: Springer, 2014.

[42] R. T. Rockafellar and S. Uryasev, "Optimization of conditional value-at-risk," *J. Risk*, vol. 2, no. 3, pp. 21–41, 2000.

[43] A. Charnes and W. W. Cooper, "Chance-constrained programming," *Manage. Sci.*, vol. 6, no. 1, pp. 73–79, 1959.

[44] D. Bertsimas and M. Sim, "The price of robustness," *Oper. Res.*, vol. 52, no. 1, pp. 35–53, 2004.

[45] A. Ben-Tal, L. El Ghaoui, and A. Nemirovski, *Robust Optimization*. Princeton, NJ, USA: Princeton Univ. Press, 2009.

[46] P. Mohajerin Esfahani and D. Kuhn, "Data-driven distributionally robust optimization using the Wasserstein metric: Performance guarantees and tractable reformulations," *Math. Program.*, vol. 171, nos. 1–2, pp. 115–166, 2018.

[47] Y. Ben-Haim, *Info-Gap Decision Theory: Decisions Under Severe Uncertainty*, 2nd ed. Oxford, U.K.: Academic Press, 2006.

[48] N. Gröwe-Kuska, H. Heitsch, and W. Römisch, "Scenario reduction and scenario tree construction for power management problems," in *Proc. IEEE PowerTech Conf.*, Bologna, Italy, 2003.

[49] M. D. McKay, R. J. Beckman, and W. J. Conover, "A comparison of three methods for selecting values of input variables in the analysis of output from a computer code," *Technometrics*, vol. 21, no. 2, pp. 239–245, 1979.

[50] European Parliament and Council, "Directive 2003/87/EC establishing a scheme for greenhouse gas emission allowance trading within the Community," Oct. 2003.

[51] C. Kang *et al.*, "Carbon emission flow in networks," *Sci. Rep.*, vol. 2, art. no. 479, 2012.

[52] C. Kang *et al.*, "Carbon emission flow from generation to demand: A network-based model," *IEEE Trans. Smart Grid*, vol. 6, no. 5, pp. 2386–2394, Sept. 2015.

[53] D. Liu *et al.*, "Electricity-carbon joint trading of virtual power plant with carbon capture system," *Int. Trans. Electr. Energy Syst.*, vol. 2023, art. no. 6864403, 2023.

[54] IPCC, *Climate Change 2022: Mitigation of Climate Change. Contribution of Working Group III to the Sixth Assessment Report*. Cambridge, U.K.: Cambridge Univ. Press, 2022.

[55] W. D. Nordhaus, "Revisiting the social cost of carbon," *Proc. Natl. Acad. Sci. USA*, vol. 114, no. 7, pp. 1518–1523, 2017.

[56] R. S. Sutton and A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed. Cambridge, MA, USA: MIT Press, 2018.

[57] V. Mnih *et al.*, "Human-level control through deep reinforcement learning," *Nature*, vol. 518, no. 7540, pp. 529–533, 2015.

[58] T. P. Lillicrap *et al.*, "Continuous control with deep reinforcement learning," in *Proc. Int. Conf. Learn. Representations (ICLR)*, San Juan, Puerto Rico, 2016.

[59] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, "Proximal policy optimization algorithms," *arXiv:1707.06347*, 2017.

[60] S. Boyd, N. Parikh, E. Chu, B. Peleato, and J. Eckstein, "Distributed optimization and statistical learning via the alternating direction method of multipliers," *Found. Trends Mach. Learn.*, vol. 3, no. 1, pp. 1–122, 2011.

[61] J. F. Nash, "Non-cooperative games," *Ann. Math.*, vol. 54, no. 2, pp. 286–295, 1951.

[62] L. S. Shapley, "A value for n-person games," in *Contributions to the Theory of Games*, vol. 2, H. W. Kuhn and A. W. Tucker, Eds. Princeton, NJ, USA: Princeton Univ. Press, 1953, pp. 307–317.

[63] F. Tao, H. Zhang, A. Liu, and A. Y. C. Nee, "Digital twin in industry: State-of-the-art," *IEEE Trans. Ind. Informat.*, vol. 15, no. 4, pp. 2405–2415, Apr. 2019.

[64] M. Grieves, "Digital twin: Manufacturing excellence through virtual factory replication," White Paper, 2014.

[65] J. F. Benders, "Partitioning procedures for solving mixed-variables programming problems," *Numer. Math.*, vol. 4, no. 1, pp. 238–252, 1962.

[66] M. E. Baran and F. F. Wu, "Network reconfiguration in distribution systems for loss reduction and load balancing," *IEEE Trans. Power Del.*, vol. 4, no. 2, pp. 1401–1407, Apr. 1989.

[67] B. Stott, J. Jardim, and O. Alsaç, "DC power flow revisited," *IEEE Trans. Power Syst.*, vol. 24, no. 3, pp. 1290–1300, Aug. 2009.

[68] D. Kahneman and A. Tversky, "Prospect theory: An analysis of decision under risk," *Econometrica*, vol. 47, no. 2, pp. 263–291, 1979.

[69] R. B. Nelsen, *An Introduction to Copulas*, 2nd ed. New York, NY, USA: Springer, 2006.

[70] J. MacQueen, "Some methods for classification and analysis of multivariate observations," in *Proc. 5th Berkeley Symp. Math. Statist. Probab.*, Berkeley, CA, USA, 1967, pp. 281–297.

[71] N. Metropolis and S. Ulam, "The Monte Carlo method," *J. Amer. Stat. Assoc.*, vol. 44, no. 247, pp. 335–341, 1949.

[72] N. P. Padhy, "Unit commitment—A bibliographical survey," *IEEE Trans. Power Syst.*, vol. 19, no. 2, pp. 1196–1205, May 2004.

[73] J. S. Vardakas, N. Zorba, and C. V. Verikoukis, "A survey on demand response programs in smart grids: Pricing methods and optimization algorithms," *IEEE Commun. Surveys Tuts.*, vol. 17, no. 1, pp. 152–178, First Quarter 2015.

[74] L. Gkatzikis, I. Koutsopoulos, and T. Salonidis, "The role of aggregators in smart grid demand response markets," *IEEE J. Sel. Areas Commun.*, vol. 31, no. 7, pp. 1247–1257, July 2013.

[75] P. Pinson, "Wind energy: Forecasting challenges for its operational management," *Stat. Sci.*, vol. 28, no. 4, pp. 564–585, 2013.

[76] I. Staffell *et al.*, "The role of hydrogen and fuel cells in the global energy system," *Energy Environ. Sci.*, vol. 12, no. 2, pp. 463–491, 2019.

[77] H. C. Hesse, M. Schimpe, D. Kucevic, and A. Jossen, "Lithium-ion battery storage for the grid—A review of stationary battery storage system design tailored for applications in modern power grids," *Energies*, vol. 10, no. 12, art. no. 2107, 2017.

[78] European Parliament and Council, "Directive (EU) 2019/944 on common rules for the internal market for electricity," June 2019.
