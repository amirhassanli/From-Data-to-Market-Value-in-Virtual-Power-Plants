# پیشرفت جمع‌آوری PDFهای ۱۵ مطالعه — ۲۰۲۶-۱۱-۰۳

پوشهٔ مقصد: `Downloads\DMDI_IntraCoder\PDFs\`

> **نکتهٔ مهم:** اگر PDFهای متن کامل کدگذاری اول همین الان در اختیار شماست
> (Zotero یا پوشهٔ قبلی)، فقط همان‌ها را در `PDFs\` کپی کنید — بهتر از نسخهٔ
> تازه است، چون متن مقصد دقیقاً همان چیزی می‌شود که کدگذاری اول روی آن انجام
> شده، و این برای سنجهٔ «پایداری ابزار» سازگارتر است.

## A) خودکار گرفته شد (۲ از ۱۵)
| مرجع | فایل در PDFs\ | منبع |
|---|---|---|
| [64] Wang (risk-aware XGBoost/CVaR) | 64__Wang_et_al_risk_aware_XGBoost_CVaR.pdf | Elsevier OA (gold) |
| [35] Song (pay-as-bid / pay-as-clear) | 35__Song_et_al_pay_as_bid_pay_as_clear.pdf | MDPI |

## B) OA — فقط کلیک در مرورگر خودتان (بدون دسترسی institutional)
| مرجع | لینک | نام فایل پیشنهادی |
|---|---|---|
| [15] Fan & Liu (IET RPG2, gold) | https://ietresearch.onlinelibrary.wiley.com/doi/pdfdirect/10.1049/rpg2.12806?download=true | 15__Fan_and_Liu.pdf |
| [4] Ruan (Adv. Appl. Energy, gold) | https://doi.org/10.1016/j.adapen.2024.100170 → پذیرش OA، دکمهٔ Download PDF | 4__Ruan_et_al.pdf |
| [5] Gao (Applied Energy, hybrid OA) | https://doi.org/10.1016/j.apenergy.2023.122284 → نسخهٔ OA در ScienceDirect | 5__Gao_et_al.pdf |
| [18] Vahedipour (green, AAU VBN) | https://vbn.aau.dk/da/publications/20d8a346-5bcc-4440-94e8-f4a490646368 | 18__Vahedipour_Dahraie_et_al.pdf |
| [17] Wozabal (green, TUM mediatum) | https://mediatum.ub.tum.de/1524381 | 17__Wozabal_and_Rameseder.pdf |
| [67] Falabretti (green, Genova IRIS) | https://hdl.handle.net/11311/1222132 | 67__Falabretti_et_al.pdf |

## C) Closed (Elsevier) — با دسترسی campus/اشتراک (همان که در کدگذاری اول داشتید)
| مرجع | DOI | نام فایل پیشنهادی |
|---|---|---|
| [28] Wang (DRL, EV) | 10.1016/j.epsr.2021.107714 | 28__Wang_et_al_DRL_EV.pdf |
| [69] Chen (robust, EV) | 10.1016/j.jclepro.2023.136690 | 69__Chen_et_al_robust_EV.pdf |
| [75] Kim & Choi | 10.1016/j.ejor.2024.03.001 | 75__Kim_and_Choi.pdf |
| [19] Sadeghi | 10.1016/j.ijepes.2020.106646 | 19__Sadeghi_et_al.pdf |
| [10] Choi (DER combinations) | 10.1016/j.apenergy.2025.126264 | 10__Choi_et_al_DER_combinations.pdf |
| [7] Esfahani | 10.1016/j.rser.2025.115929 | 7__Esfahani_et_al.pdf |
| [21] Wang (PV forecast) | 10.1016/j.apenergy.2024.123890 | 21__Wang_et_al_PV_forecast.pdf |

## گزارش ابزارهای اتوماتیک
- `collect_pdfs.py` (پاس اول، OA مستقیم OpenAlex): ۱/۱۵
- `collect_pdfs2.py` (پاس دوم: Unpaywall + الگوها + landing HTML): +۰
- `s2_pdfs.py` (Semantic Scholar): 429 rate-limited؛ مسیر VBN را تأیید کرد
- مرورگر: MDPI ✓؛ Wiley / TUM / Genoa / ScienceDirect / VBN-files همه
  «Just a moment…» (Cloudflare) و اتوماتیک از آن نگذشت
- برای جزئیات بیشتر: `collect_pdfs.py` + `collect_pdfs2.py` (فهرست کامل
  candidateها در خروجی `diag_cands.py`)
