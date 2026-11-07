# ترتیب اجرا (به فارسی)

1. فایل‌های پوشهٔ `supervisor_pack` را (ایمیل، queries، قالب coder2، codebook) برای استاد بفرستید.
2. وقتی exports برگشت، در یک پوشه بگذارید: `exports/` (scopus*.csv, wos*.txt, ieee*.csv) + `search_log.csv` + `dmdi_matrix.csv`.
3. `dmdi_matrix.csv` را کامل کنید (ستون‌های I..R، data_type، coding_basis برای 30 مقالهٔ اصلی). سلول‌های پیش‌پر از جدول‌های خود مقاله آمده‌اند؛ بقیه را از کدگذاری خودتان بنویسید.
4. `python 01_prisma_pipeline.py --core dmdi_matrix.csv` ← `screening_sheet.csv` ساخته می‌شود؛ ستون‌های `ta_decision` و `ft_decision` را (include/exclude) پر کنید و دوباره اجرا کنید.
5. وقتی استاد فایل `coder2` را پر کرد: `python 02_dmdi_tables_figures.py --coder2 coder2_filled.csv` (باید ستون key و I..R داشته باشد؛ فایل پر شده را با نام dmdi_matrix_coder2.csv ذخیره کنید).
6. `python 03_build_manuscript.py --src manuscript_VPP_DMDI_post-review.md --values prisma_values.json dmdi_values.json --out manuscript_filled.md --docx`
   اگر هنوز توکنی خالی باشد اسکریپت فهرست آن را چاپ می‌کند و متوقف می‌شود.
7. `python 04_verify_references_crossref.py --manuscript manuscript_filled.md --email you@example.com`
8. بعد از اجرا، جمله‌های توصیفی (مثلاً «D و M بهترین گزارش‌شده‌اند») را با جدول VI تولیدشده تطبیق دهید.
