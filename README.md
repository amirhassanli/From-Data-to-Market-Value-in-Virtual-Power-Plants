# From-Data-to-Market-Value-in-Virtual-Power-Plants

From Data to Market Value in Virtual Power Plants: A Structured Evidence Review of Decision Integrity, Uncertainty, and Electricity–Carbon Market Integration.

## دایرکتوری‌ها

| دایرکتوری | محتوا |
|---|---|
| `_draft/` | اسکریپت‌های idempotent ویرایش و آудиت (فاز ۵–۶): `audit_*.py`, `collect_pdfs*.py`, `finalize_nummaps.py`, `fix_*.py`, `xcheck.py`, `diff3_5b.py`, `renumber_phase6c.py`, `intra_select.py`, `seal_pretest.py`, `test_aiagree.py`, `backup_phase6.py`, `build_*.py`,报告‌های فاز (PHASE*_CHANGELOG.md)، بکاپ `BACKUP_phase6/` |
| `DMDI_IntraCoder/` | بسته کدگذاری تکراری AI (پنل دو-عامله): `PROTOCOL_intra_coder.md` (اصلاحات ۱–۲)، `AI_CODER_TASK_PROMPT.md` (پرامپت مشترک برای DeepSeek/Claude/ChatGPT/Grok)، `ai_agreement.py` (سه جפת κ + صف داوری)، `SUBSAMPLE_key.csv` (مهر شده، ۱۵ مطالعه)، `SEAL_pre_retest.txt` (SHA-256)، `IntraCoder_ReCode_SHEET.csv` (شیت خالی)، `PDFs/` (متن کامل مطالعه‌ها)، `PDF_STATUS.md` (وضعیت دانلود OA) |
| `SUPPLEMENTARY_DMDI/` | بسته تکمیلی: `DMDI_Coding_Matrix.csv`, `DMDI_Codebook.docx`, `DMDI_Analysis.py`, `DMDI_Agreement.py`, `DMDI_Coding_Sheet_BLIND.csv` |
| `DMDI_exports/` | صادرات‌های CSV و گزارش‌های فاز (dmdi_coding_*.csv, study_to_phase5.json, PHASE*_CHANGELOG.md) |
| `DMDI_SecondCoder/` | لوله-κ اصلی (دومین کدگذار انسان): `Coding_Sheet_BLIND.csv`, `kappa_agreement.py`, `merge_second_coder.py`, راهنمای کدگذار دوم |

## فایل‌های اصلی

| فایل | توضیحات |
|---|---|
| `From Data to Market Value in Virtual Power Plants (FINAL).docx` | نسخه تحویل‌پذیر مقاله (نسخه تازه‌شده از PHASE5، شماره‌گذاری ۱–۸۲، احراز هویت ارجاعات) |
| `01_prisma_pipeline.py` | لوله PRISMA |
| `02_dmdi_tables_figures.py` | جدولها و اشکال DMDI |
| `03_build_manuscript.py` | ساخت متن مقاله |
| `04_verify_references_crossref.py` | تایید ارجاعات از طریق Crossref |
| `kappa_agreement.py`, `merge_second_coder.py` | محاسبه و ادغام κ کدگذار دوم |
| `make_docx.py`, `make_figs.py` | تولید docx و اشکال |
| `vpp_review_ieee.docx` / `.md` / `.tex` | نسخه‌های IEEE |

## پروژه کدگذاری تکراری AI (فاز ۶ — اصلاحیهٔ ۲)

به جای کدگذار دوم انسانی، دو عامل AI از خانواده‌های متفاوت (DeepSeek + Claude) همان ۱۵ مطالعه را با **یکسان‌ترین پرامپت** و **بدون دیدن خروجی یکدیگر** کدگذاری می‌کنند. سه کاپا گزارش می‌شود: اصلی×عامل۱، اصلی×عامل۲، عامل۱×عامل۲. سلولی که هر دو عامل با هم و برخلاف اصلی توافق دارند، در صف اول داوری قرار می‌گیرد.

- نیازمندی: PDF متن کامل هر ۱۵ مطالعه در `DMDI_IntraCoder/PDFs/` (۲ مورد خودکار گرفته‌شده؛ بقیه با لینک‌های در `PDF_STATUS.md`)
- خروجی: `RETURNED_DeepSeek.csv` + `RETURNED_Claude.csv` → `python -u _draft/ai_agreement.py ...`
- گزارش در مقاله: «instrument repeatability (AI panel)» — هرگز intra-coder / inter-coder انسانی

##見解

همه ویرایش‌ها از طریق اسکریپت‌های idempotent در `_draft/` انجام می‌شود؛ فایل docx اصلی هرگز مستقیماً ویرایش نمی‌شود.
