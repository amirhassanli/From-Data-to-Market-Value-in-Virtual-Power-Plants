# گزارش ممیزی فنی و علمی مخزن مقاله VPP
**تاریخ ممیزی:** ۱۰ نوامبر ۲۰۲۶  
**مخزن:** `amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants`  
**شاخه بررسی‌شده:** `main`  
**شناسه درخت مخزن:** `a4a0cde4b08a64ca49f67d98e58ab0d60599c8b3`

## ۱. جمع‌بندی اجرایی

مخزن از نظر حجم اسناد، نسخه‌های مقاله و ابزارهای کمکی غنی است، اما در وضعیت فعلی **قابل بازتولید و آماده ارسال ژورنالی نیست**. مانع اصلی صرفاً نگارش نیست؛ زنجیره شواهد، فایل‌های ورودی، ماتریس کدگذاری، شماره‌گذاری ارجاعات و ادعاهای توافق کدگذاران با یکدیگر سازگار نیستند.

چهار مانع بحرانی:

1. داده‌های خام جست‌وجوی Scopus، Web of Science و IEEE Xplore و فایل ثبت تاریخ/عبارت جست‌وجو در مخزن وجود ندارند؛ بنابراین PRISMA، غربالگری و recall قابل بازتولید نیست.
2. ماتریس DMDI موجود با schema اسکریپت تولید جدول‌ها و شکل‌ها سازگار نیست و شماره ارجاعات آن با نسخه Markdown جدید مقاله تطبیق ندارد.
3. هیچ خروجی معتبر برای توافق کدگذار انسانی یا تکرارکدگذاری دو عامل AI در مخزن وجود ندارد؛ در عین حال متن مقاله هنوز κ و توافق بین‌کدگذاران را به‌صورت جای‌نگهدار گزارش می‌کند.
4. جدیدترین فایل Word، یعنی `IEEE_VPP_Systematic_Review_Manuscript_v7.docx`، در ۹ نوامبر بارگذاری شده، اما محتوای باینری آن از اتصال GitHub قابل استخراج و مقایسه متنی نبود. نسخه‌ای با نام `FINAL.docx` نیز از نظر blob دقیقاً کپی فایل backup فاز ۶ است و نباید صرفاً به‌دلیل نام FINAL مرجع تلقی شود.

**نتیجه تصمیمی:** هیچ عدد PRISMA، κ، جدول DMDI یا شکل مبتنی بر داده نباید در نسخه نهایی تثبیت شود تا زمانی که ورودی‌های واقعی، schema و شناسه‌های DOI اصلاح و آزمون شوند. این گزارش، یافته‌های قابل اثبات را از موارد نیازمند دسترسی بیشتر جدا می‌کند.

## ۲. دامنه و روش ممیزی

بررسی بر snapshot شاخه `main` با tree SHA بالا انجام شد. درخت مخزن شامل ۱۷۳ ورودی، ۱۶۶ فایل و ۷ پوشه است. فایل‌های متنی اصلی، اسکریپت‌های پایتون، CSVها، changelogها، پروتکل کدگذاری و تاریخچه commit بررسی شدند.

محدودیت دسترسی: GitHub connector فایل‌های متنی را خواند، اما فایل‌های باینری DOCX/PDF/PNG را به محتوای قابل‌استخراج تبدیل نکرد. بنابراین محتوای درونی DOCXها و کیفیت بصری تصاویر به‌عنوان «تأییدشده» گزارش نمی‌شوند. همچنین تلاش برای ساخت شاخه `final-version-update` با خطای GitHub API `403 Resource not accessible by integration` متوقف شد؛ هیچ commit، branch یا PR جدیدی ایجاد نشده است.

## ۳. تعیین نسخه مرجع

| فایل | شواهد نسخه | نتیجه |
|---|---|---|
| `manuscript_VPP_DMDI_post-review.md` | آخرین نسخه کامل Markdown قابل خواندن؛ commit مورخ ۷ نوامبر؛ ۴۵٬۰۲۵ نویسه، ۳۸۴ خط، ۵۹ مرجع و ۲۷ نوع placeholder | بهترین مبنای متنیِ قابل ممیزی در حال حاضر |
| `vpp_review_ieee.md` | ۵۶٬۹۱۶ نویسه؛ عنوان و روش «Systematic Review»؛ ادعای ۱۵۶ مطالعه و PRISMA قدیمی | نسخه قدیمی‌تر با ادعاهای روش‌شناختی منسوخ |
| `vpp_review_ieee.tex` | ۴۰٬۳۸۳ نویسه؛ هنوز TODO برای نویسندگان و اعداد PRISMA دارد | نسخه LaTeX قدیمی و ناتمام |
| `From Data to Market Value in Virtual Power Plants (FINAL).docx` | blob SHA آن با `_draft/BACKUP_phase6/...PHASE5.docx` یکسان است | فایل FINAL از نظر محتوای باینری همان backup است |
| `IEEE_VPP_Systematic_Review_Manuscript_v7.docx` | آخرین فایل Word بارگذاری‌شده، ۹ نوامبر؛ blob SHA متفاوت | جدیدترین فایل از نظر تاریخ، اما محتوای آن در این ممیزی قابل استخراج نبود |

**تصمیم کاری:** Markdown پس از بازنگری، مبنای موقت اصلاحات متنی است؛ اما تا زمان استخراج و مقایسه محتوای `v7.docx` نمی‌توان ادعا کرد که کامل‌ترین نسخه نهایی است. نسخه Word با نام FINAL نباید مرجع قرار گیرد.

## ۴. ممیزی روش PRISMA و داده‌های جست‌وجو

اسکریپت `01_prisma_pipeline.py` به‌طور پیش‌فرض به این ورودی‌ها وابسته است:

- `exports/scopus*.csv`
- `exports/wos*.txt`
- `exports/ieee*.csv`
- `search_log.csv`
- `dmdi_matrix.csv`

هیچ‌یک از پوشه `exports/`، فایل `search_log.csv`، فایل `screening_sheet.csv` یا خروجی‌های `prisma_values.json` و `core_recall.csv` در snapshot فعلی وجود ندارد. بنابراین:

- تعداد رکوردهای شناسایی‌شده و حذف‌شده قابل محاسبه نیست.
- تاریخ و عبارت دقیق جست‌وجوها قابل راستی‌آزمایی نیست.
- غربالگری عنوان/چکیده و متن کامل مستند نشده است.
- recall هسته مطالعات نسبت به پایگاه‌های داده قابل محاسبه نیست.

نسخه قدیمی `vpp_review_ieee.md` از جست‌وجوی ۲۰۱۵ تا اوت ۲۰۲۶ و ۱۵۶ مطالعه صحبت می‌کند؛ نسخه جدیدتر `manuscript_VPP_DMDI_post-review.md` روش را به structured evidence review و بازه ۲۰۱۸–۲۰۲۶ تغییر داده و هسته ۳۹ مطالعه را از جست‌وجوی پایگاه داده جدا کرده است. تغییر روش منطقی‌تر است، اما بدون export و search log، حتی «coverage audit» نیز عدد قابل دفاع ندارد.

**اصلاح لازم:** تا دریافت و ثبت exportهای واقعی، هیچ flow count یا recall percentage درج نشود. نمودار فعلی `fig1_prisma.png` نیز به‌دلیل نبود ورودی و خروجی محاسباتی، به‌عنوان شکل بازتولیدشده تأیید نمی‌شود.

## ۵. ممیزی ماتریس DMDI و ناسازگاری schema

فایل `DMDI_exports/dmdi_coding_matrix.csv` دارای ۳۹ ردیف و ستون‌های زیر است:

`row, study, reference, year, I, U, D, M, O, S, R, P`

اما `02_dmdi_tables_figures.py` این ستون‌ها را لازم دارد:

`key, ref, label, study_type, year, data_type, coding_basis, verified, doi, show, approach, I, U, D, M, O, S, R, notes`

در نتیجه، فایل export موجود مستقیماً ورودی معتبر اسکریپت نیست. به‌طور مشخص، `validate()` به `study_type`، `data_type` و `coding_basis` متکی است؛ این فیلدها در CSV موجود نیستند. فایل `dmdi_matrix_TEMPLATE.csv` schema مورد انتظار را دارد، اما فیلدهای ضروری آن تکمیل نشده‌اند.

### ۵.۱. تعدادهای تشخیصی از CSV فعلی

با کنار گذاشتن ۷ ردیف مرور (مطابق طبقه‌بندی SEED در اسکریپت و برچسب‌های مطالعه)، ۳۲ مطالعه اولیه باقی می‌ماند. شمارش مستقیم کدهای فعلی برای این ۳۲ ردیف چنین است:

| بعد | Explicit | Partial | Not reported |
|---|---:|---:|---:|
| I — Information-set integrity | 22 | 10 | 0 |
| U — Uncertainty integrity | 22 | 10 | 0 |
| D — Decision integrity | 30 | 2 | 0 |
| M — Market realism | 27 | 5 | 0 |
| O — Out-of-sample validity | 2 | 5 | 25 |
| S — Settlement realism | 4 | 16 | 12 |
| R — Reproducibility | 0 | 32 | 0 |

این اعداد صرفاً **شمارش تشخیصی CSV فعلی** هستند؛ نه نتایج نهایی مقاله. دلیل: در ماتریس، `coding_basis` و `data_type` وجود ندارد؛ DOI و متن کامل برای همه مطالعات در این snapshot در دسترس نیست؛ و هفت مطالعه مروری نیز در فایل کدگذاری دارای مقادیر I..R هستند، درحالی‌که نسخه جدید مقاله می‌گوید مرورها روی این ابعاد کدگذاری نشده‌اند. تا اصلاح این ناسازگاری، جدول درصدهای DMDI نباید منتشر شود.

### ۵.۲. اختلاف شماره ارجاعات

شیت کور کدگذار دوم DOI دارد و امکان تطبیق DOI با فهرست منابع Markdown را فراهم می‌کند. تطبیق نشان داد ۳۶ مورد از ۳۹ شماره ارجاع موجود در شیت با شماره مرجع متن Markdown یکسان نیست. نمونه‌ها:

| مطالعه | شماره در ماتریس/شیت | شماره در Markdown قابل خواندن |
|---|---:|---:|
| Wozabal & Rameseder | 17 | 26 |
| Vahedipour-Dahraie et al. | 18 | 27 |
| Fan & Liu | 15 | 33 |
| Choi et al. | 10 | 53 |
| Wang et al. (risk-aware) | 64 | 57 |
| Liu et al. (carbon joint) | 32 | 56 |

چهار DOI از شیت کدگذار دوم در فهرست منابع Markdown با همان DOI پیدا نشدند؛ این موارد باید با تطبیق عنوان/نویسنده بررسی شوند و نباید با شماره قدیمی به مقاله متصل بمانند. نگاشت ارجاعات باید بر اساس DOI یا شناسه پایدار انجام شود، نه شماره مرجع.

## ۶. توافق کدگذاران: ادعای مقاله با شواهد موجود منطبق نیست

### ۶.۱. کدگذار انسانی

- `DMDI_SecondCoder/Coding_Sheet_BLIND.csv` دارای ستون‌های B است، اما مقادیر کدگذار دوم خالی‌اند.
- `DMDI_exports/dmdi_second_coder_sheet.csv` دارای کدهای A است و ستون‌های B خالی‌اند.
- `_draft/DMDI_AGREEMENT_STATUS.md` نیز صریحاً اعلام می‌کند هر ۳۱۲ سلول B (۳۹ مطالعه × ۸ بعد) خالی است و κ قابل محاسبه نیست.

پس κ انسانی یا inter-coder reliability در وضعیت فعلی قابل گزارش نیست.

### ۶.۲. بازکدگذاری با دو عامل AI

پروتکل `DMDI_IntraCoder/PROTOCOL_intra_coder.md` طرح جدیدی تعریف کرده است: ۱۵ مطالعه از ۳۹ مطالعه، دو عامل AI از دو خانواده مدل، و سه مقایسه توافق. پروتکل صریحاً می‌گوید این سنجه «instrument stability / AI-repeat consistency» است و نباید به‌عنوان توافق مستقل انسانی معرفی شود.

بااین‌حال:

- `PDF_STATUS.md` فقط دریافت ۲ PDF از ۱۵ مطالعه را تأیید می‌کند.
- فایل‌های `RETURNED_DeepSeek.csv` و `RETURNED_Claude.csv` وجود ندارند.
- `AGREEMENT_RESULTS.txt` و `agent_kappa_results.csv` وجود ندارند.
- `ai_agreement.py` خروجی κ اسمی (unweighted) می‌سازد؛ این با ادعای weighted inter-coder κ در متن Markdown یکی نیست.
- متن Markdown هنوز از «weighted inter-coder agreement» و placeholderهای `{{N_DOUBLE}}` و `{{KAPPA}}` استفاده می‌کند.

**اصلاح لازم:** عبارت توافق انسانی و همه placeholderهای κ از نسخه مقاله حذف یا تا زمان وجود داده واقعی به‌صورت محدودیت صریح گزارش شوند. اگر دو عامل AI واقعاً کدگذاری را تکمیل کردند، نتیجه فقط با برچسب instrument repeatability گزارش شود؛ نه inter-coder reliability. خروجی دو عامل باید قبل از هر عددگذاری در مخزن ثبت شود.

## ۷. ممیزی اسکریپت‌ها

### `01_prisma_pipeline.py`
- ورودی‌های واقعی لازم در مخزن نیستند؛ اجرا اکنون PRISMA معتبر تولید نمی‌کند.
- فیلترهای زبان و نوع سند در صورت خالی بودن metadata اجازه عبور می‌دهند؛ این رفتار باید در گزارش روش توضیح داده یا با سیاست صریح کنترل شود.
- تصمیم‌های غربالگری فقط وقتی کامل محسوب می‌شوند که تمام رکوردها مقدار مجاز داشته باشند؛ اعتبارسنجی صریح مقادیر نامعتبر و شناسه‌های تکراری باید افزوده شود.

### `02_dmdi_tables_figures.py`
- schema فایل CSV موجود با ورودی مورد انتظار ناسازگار است.
- SEED و شماره‌های ارجاع آن با شماره‌گذاری متن Markdown فعلی همسان نیست.
- اگر داده کدگذار دوم به این اسکریپت داده شود، مسیر κ آن weighted است؛ اما شیت فعلی با شناسه‌ها و فیلدهای مورد انتظار سازگار نیست.
- خروجی‌های `dmdi_values.json`، `supplementary_S1.csv` و شکل‌های ۲ تا ۵ وجود ندارند.

### `03_build_manuscript.py`
- ۲۷ نوع placeholder در نسخه Markdown وجود دارد؛ فایل‌های JSON مورد نیاز تولید نشده‌اند، پس ساخت نسخه پرشده ممکن نیست.
- تابع `renumber()` ارجاعات بدون تطبیق در فهرست منابع را متوقف می‌کند، اما منابع uncited را حذف می‌کند؛ پیش از استفاده باید فهرست حذف‌شده‌ها به‌صورت مستقل بازبینی شود.

### `04_verify_references_crossref.py`
- فقط تطبیق DOI با metadata Crossref (عنوان، نویسنده اول، سال) انجام می‌دهد؛ صحت ادعای علمی جمله نسبت به محتوای مقاله را تأیید نمی‌کند.
- خروجی `reference_check.csv` در مخزن وجود ندارد.
- `REFERENCE_CHECK_LOG.md` مربوط به ۸ سپتامبر و نسخه‌ای با ۷۸ مرجع است؛ نسخه Markdown فعلی ۵۹ مرجع دارد. بنابراین لاگ قبلی جایگزین کنترل ارجاعات نسخه جاری نیست.

### ابزارهای کدگذار دوم و AI
- `merge_second_coder.py` با نام مطالعه join می‌کند؛ join باید با DOI یا شناسه پایدار انجام شود و در صورت رکورد تکراری/ناقص fail-closed باشد.
- `ai_agreement.py` باید تعداد ردیف‌های یکتا، کامل بودن ۱۵ شناسه و وجود همه ابعاد را سخت‌گیرانه کنترل کند. در وضعیت فعلی تعداد و یکتایی ردیف‌های برگشتی به‌طور کامل تضمین نمی‌شود.

## ۸. آلودگی و اختلاط پروژه در پوشه `_draft/`

چند فایل در `_draft/` به پروژه دیگری با موضوع reserve deliverability و throughput aging تعلق دارند، نه مقاله مرور VPP. شواهد مستقیم:

- `_draft/PHASE16_REPORT.md` عنوان/موضوع مطالعه copula، SMARD، Study-A/Study-B و aging را گزارش می‌کند.
- `_draft/PHASE15_FINAL_PACKAGING.md` عنوان مقاله «Reserve Rent, Error Dependence, and Feeder Voltage...» را ذکر می‌کند.
- `_draft/RESPONSE_TO_REVIEWERS_PHASE15.md` پاسخ داوری مقاله دیگری را شامل می‌شود.

این اسناد نباید به‌عنوان شواهد، تاریخچه اصلاح یا پاسخ داوری مقاله مرور VPP استفاده شوند. پیش از جابه‌جایی یا حذف، باید provenance هر فایل بررسی و سپس پروژه‌ها از هم جدا شوند.

## ۹. تصاویر و فایل‌های تولیدی

نسخه Markdown پس از بازنگری به این تصاویر ارجاع می‌دهد:

- `fig1_prisma.png`
- `fig2_chain.png`
- `fig3_matrix.png`
- `fig4_evidence_map.png`
- `fig5_ladder.png`

در مخزن فقط `fig1_prisma.png` و `fig2_pipeline.png` با این مجموعه مرتبط یافت شدند؛ `fig2_chain.png` و شکل‌های ۳ تا ۵ وجود ندارند. نام `fig2_pipeline.png` به‌تنهایی اثبات نمی‌کند که با شکل مورد انتظار `fig2_chain.png` یکسان است. شکل‌های مبتنی بر DMDI باید پس از اصلاح schema و اجرای موفق pipeline بازتولید شوند. کیفیت بصری فایل‌های PNG در این ممیزی تأیید نشده است.

## ۱۰. گزارش شبیه‌سازی‌شده داوری

`reviewers_report_and_response.md` در عنوان خود صریحاً «Simulated peer review» معرفی شده است. بنابراین این فایل، نظر واقعی داور ژورنال نیست. می‌توان از آن به‌عنوان internal critique checklist استفاده کرد، اما پاسخ‌نامه نباید وانمود کند که داوری رسمی دریافت شده است.

## ۱۱. اولویت‌بندی اصلاحات

| اولویت | اقدام | معیار عبور |
|---|---|---|
| P0 | تثبیت نسخه مرجع با استخراج و مقایسه `v7.docx` و Markdown | نسخه مرجع واحد، هش و تاریخ مشخص |
| P0 | دریافت exportهای خام و search log واقعی | همه ورودی‌ها موجود، schema معتبر و PRISMA قابل بازتولید |
| P0 | ساخت master DMDI با DOI، study_type، coding_basis، data_type، verified و شناسه یکتا | ۳۹ ردیف، طبقه‌بندی ۳۲ primary و ۷ review مستند، بدون ارجاع نامنطبق |
| P0 | حل اختلاف ۳۶ شماره ارجاع و DOIهای فاقد تطبیق | همه مطالعات با DOI/شناسه پایدار به مرجع درست متصل |
| P0 | تعیین تکلیف ادعای κ | یا خروجی واقعی انسانی؛ یا خروجی AI با برچسب instrument stability؛ یا حذف عدد و گزارش محدودیت |
| P1 | اصلاح و تست pipelineهای ۰۱ تا ۰۴ | اجرای موفق از داده خام تا manuscript و ثبت log |
| P1 | بازتولید شکل‌ها و جداول | هر شکل/جدول از خروجی اسکریپت و ورودی نسخه‌دار |
| P1 | پاک‌سازی `_draft/` و جداسازی پروژه مقاله دیگر | هیچ سند Article 6 در مسیر پروژه VPP باقی نماند |
| P2 | ویرایش نهایی زبان، ساختار IEEE و DOCX | تطبیق کامل متن، جدول، شکل، شماره استناد و نسخه Word |

## ۱۲. تصمیم نهایی ممیزی

در این مرحله، **نهایی‌سازی علمی مقاله قابل تأیید نیست**. علت، ضعف نگارشی نیست؛ نبود ورودی‌های خام، ناسازگاری schema، نگاشت نادرست ارجاعات، نبود داده توافق کدگذاران و عدم امکان بازرسی محتوای جدیدترین فایل Word است.

کارهای قابل انجام بدون جعل داده:
- انتخاب Markdown پس از بازنگری به‌عنوان مبنای متنی موقت؛
- اصلاح نگاشت DOI و schema؛
- تکمیل ورودی‌های خام و لاگ جست‌وجو؛
- اجرای مجدد اسکریپت‌ها و ثبت خروجی‌ها؛
- بازنویسی روش و نتایج فقط بر اساس خروجی‌های بازتولیدشده؛
- تولید نسخه Word نهایی و PR با checklist قابل بررسی.

**وضعیت GitHub:** تلاش برای ایجاد شاخه `final-version-update` با خطای 403 رد شد. هیچ فایلی در مخزن تغییر نکرده و PR ساخته نشده است. این گزارش محلی است و به‌عنوان commit یا PR معرفی نمی‌شود.

## ۱۳. مسیر فایل‌های مرجع در مخزن

- [README.md](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/README.md)
- [Manuscript after simulated review](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/manuscript_VPP_DMDI_post-review.md)
- [Older IEEE Markdown draft](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/vpp_review_ieee.md)
- [PRISMA pipeline](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/01_prisma_pipeline.py)
- [DMDI table and figure pipeline](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/02_dmdi_tables_figures.py)
- [Manuscript builder](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/03_build_manuscript.py)
- [Crossref checker](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/04_verify_references_crossref.py)
- [DMDI coding matrix](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/DMDI_exports/dmdi_coding_matrix.csv)
- [Human second-coder status](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/_draft/DMDI_AGREEMENT_STATUS.md)
- [AI repeat-coding protocol](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/DMDI_IntraCoder/PROTOCOL_intra_coder.md)
- [AI PDF status](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/DMDI_IntraCoder/PDF_STATUS.md)
- [Simulated reviewer report](https://github.com/amirhassanli/From-Data-to-Market-Value-in-Virtual-Power-Plants/blob/main/reviewers_report_and_response.md)
