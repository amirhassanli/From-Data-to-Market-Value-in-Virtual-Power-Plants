# DMDI second-coder round — status & methods draft
(هیچ عدد جعل نمی‌شود؛ فقط قالب آماده.)

## وضعیت
- دومین کدگذار برگشت داده نشده: هر ۳۱۲ B_ سلولِ (۳۹ مطالعه × ۸ بعد) خالی است.
- به همین دلیل kappa قابل محاسبه نیست؛ `dmdi_merge_and_kappa.py` راست‌آزمایی شد:
  matching 39/39 سطر (بر اساس study+year) ✓ — فقط با پرشدن B_ گزارش می‌دهد.

## ابزار آماده
| فایل | نقش |
|---|---|
| `_draft/dmdi_second_coder_BLIND.csv` | برگهٔ کورشده برای کدگذار دوم (A_ خالی) |
| `_draft/dmdi_second_coder_sheet.csv` | شیت اصلی؛ B_ آن توسط اسکریپت پر می‌شود |
| `_draft/dmdi_merge_and_kappa.py` | merge + validation + kappa + CI + توافق |
| `_draft/kappa_agreement.py` | موتور گزارش مستقل (همچنان معتبر) |

## وقتی کدگذار دوم برگشت
```
python _draft\dmdi_merge_and_kappa.py _draft\dmdi_second_coder_BLIND.csv
```
- اگر سلول خالی/نامعتبر باشد، خطا سطر-به-سلول می‌دهد و NOTHING محاسبه می‌کند (no-fabrication).
- بعد از برگشت: هر سلول اختلافی (A≠B) در پایان چاپ می‌شود برای جلسهٔ consensus.

## روش‌نگارش (قالب متد — EN، برای مقالهٔ DMDI)
> All included studies were coded by the first author using the DMDI rubric (Explicit/Partial/NR per dimension). To assess coding reliability, a second coder — blinded to the first coder's ratings — independently coded the full corpus of N = 39 studies across all eight dimensions (I, U, D, M, O, S, R, P; 312 coding cells). Agreement was quantified per dimension with unweighted Cohen's kappa, treating the three levels as nominal categories (the conservative choice; near-misses between Explicit and Partial are not credited). Raw agreement and kappa with an approximate 95% confidence interval are reported in Table XX. Dimensions in which a single level accounts for >90% of the first coder's ratings are flagged, since kappa is unstable under extreme prevalence. All disagreements were resolved through joint discussion, and the consensus ratings form the coding matrix used throughout the analysis.

- جایگزینی: N=39 (تأیید نهایی سطرها)، اعداد kappa/CI بر维度 از خروجی اسکریپت، فرکانس سطح غالب برای dimensions پرچم‌دار.
- طبق داوری/روش: توافق خام (percent agreement) هم کنار kappa گزارش شود.

## قاعدهٔ نهایی
- گزارش فقط با چیزی که کدگذار دوم واقعاً زده پر می‌شود؛ اگر برگشتی نیامد، در مقاله می‌توان برای این مرحله عبارت «an independent second-coding round is under way» را موقتاً جایگزین کرد (قبل از سابمیت باید حذف شود).
