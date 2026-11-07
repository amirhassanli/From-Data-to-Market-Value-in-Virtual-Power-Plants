**Subject:** Request for help – database exports (Scopus / Web of Science / IEEE Xplore) and a short blinded double-coding task for our VPP review

Dear Professor [Name],

I hope you are well. I am finalising the manuscript "From Data to Market Value in Virtual Power Plants: A Structured Evidence Review of Decision Integrity, Uncertainty, and Electricity–Carbon Market Integration" (target: IEEE Access / IEEE Transactions on Smart Grid). The review follows PRISMA 2020, and two items need institutional access that I do not currently have. Everything else is already automated with scripts, so the work on your side should take roughly 2–3 hours in total.

**What I am asking you to do**

**Task 1 – Database exports (about 1 hour).** Please run the three searches in the attached `search_queries.txt` (they are the union of five fixed Boolean queries on the VPP topic, 2018–2026, English) and send me:
1. the raw export files, named `scopus1.csv, scopus2.csv, …`, `wos1.txt, …`, `ieee1.csv, …` (formats are written under each query; please do not edit the files);
2. a small `search_log.csv` with columns `database,date,query`: the date you ran each search and the exact query string the interface accepted;
3. the number of hits each database displayed before export (a screenshot is fine).
If a database caps the export, please split by year and keep the numbering. If IEEE Xplore rejects the long query, the file explains the five-query fallback.

**Task 2 – Blinded double-coding of 10 studies (about 1.5 hours).** My coding of 30 primary studies is single-coder, which a reviewer will certainly challenge. Could you independently code the 10 studies listed in `coder2_TEMPLATE.csv`, using the full text and the rules in `DMDI_codebook.md` (seven dimensions, each E / P / NR)? Please do not look at any other coding, so the agreement statistic stays valid. I compute weighted Cohen's κ by script.

**Task 3 – Five quick bibliographic checks (about 20 minutes, optional but valuable).** Using Scopus/WoS, could you confirm whether these exist and send the correct record (title, authors, journal, volume, DOI)?
- DOI 10.1016/j.epsr.2021.107714 (Electric Power Systems Research 205, 107714, 2022), said to be on VPP + electric vehicles + deep reinforcement learning;
- DOI 10.3390/en18246486 (Energies 18, 6486, 2025), said to be on closed-loop joint forecasting and bidding in spot markets;
- the author list and volume of "A risk-aware bidding model for virtual power plants: Integrating renewable energy forecasting and carbon market strategies", Energy Reports, 2025, pp. 1222–1239;
- the DOI of Lei et al., Energy, vol. 338, article 138795 (2025);
- the first-author initials of Kim & Choi, European Journal of Operational Research 316(3), 2024.

**What happens next.** I run `01_prisma_pipeline.py` on your files (deduplication, PRISMA counts, and a recall check of my coded core against your search), complete the screening sheet myself, and recompute all tables and figures from the coding matrix. I will send you the full draft before submission. If you are willing to be a co-author or to be acknowledged, please let me know how you would like it handled.

Thank you very much for your help.

Kind regards,
[Your name]

*Attachments:* `search_queries.txt`, `coder2_TEMPLATE.csv`, `DMDI_codebook.md`
