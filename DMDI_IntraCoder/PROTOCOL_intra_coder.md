# پروتکل intra-coder (test–retest) — فاز ۶، نسخهٔ منجمد ۲۰۲۶-۱۱-۰۳

> **اصلاحیهٔ ۱ (۳ نوامبر ۲۰۲۶ — ثبت در پروتکل):** کدگذار گذر دوم «کدگذار اول انسانی»
> نیست؛ عامل کدگذاری هوش‌مصنوعی مستقل (DeepSeek) با نظرهٔ مستقیم پژوهشگر است،
> با همان codebook تغییرنکرده و کورشده. در نتیجه سنجهٔ گزارش‌شده در مقاله
> «پایداری عامل-محورِ ابزار» نامیده می‌شود (instrument stability / AI-repeat
> consistency) و **هرگز** به‌عنوان intra-coder یا inter-coder انسانی توصیف
> نمی‌شود؛ همان‌طور که گذر اول رسماً AI-assisted افشا شده (§2.7)، گذر دوم
> نیز با مدل متفاوت انجام شد تا استقلال نسبی بین دو گذر حفظ شود.
> جهت شفافیت: این سنجه مرز پایینِ repeatability ابزار را می‌سنجد،
> نه اعتبارسنجی انسانی مستقل.

> **اصلاحیهٔ ۲ (۳ نوامبر ۲۰۲۶):** طرح از تک-عامله به **دو-عامله مستقل** ارتقا یافت:
> همان ۱۵ مطالعه و همان ترتیب به دو مدل از **دو خانوادهٔ متفاوت** (ترجیح
> DeepSeek + Claude) با پرامپت یکسان داده می‌شود؛ دو چت خروجی هم را نمی‌بینند.
> سه سنجه گزارش می‌شود: κ(اصلی×عامل۱)، κ(اصلی×عامل۲)， κ(عامل۱×عامل۲).
> قاعدهٔ داوری سلول‌ها: هر دو عامل با هم و برخلاف اصلی = بیشترین اولویت؛
> ثالث: مخالفت بین عامل‌ها = داوری مستقیم. κ روی رتبه‌بندی‌های نشده محاسبه و
> گزارش می‌شود؛ داوری جداگانه ثبت و فقط به ماتریس منتشرشده اعمال می‌گردد.
> لیبل مقاله: instrument repeatability (AI panel) — بند (ii) §11.6 همچنان باز.

این پروتکل برای سنجش **پایداری زمانی/ابزارگری کدگذاری DMDI** (پاس تکراری با عامل
کدگذاری مستقل زیر نظرهٔ پژوهشگر) تهیه شده است.

## ۱) مشخصات طرح
| مؤلفه | مقدار |
|---|---|
| روش | test–retest (همان ارزیاب، جداسازی زمانی) |
| نمونه | **۱۵ از ۳۹ مطالعه (۳۸٪)** |
| انکرها (همه) | ۶ مطالعه با E در ابعاد نادر O/S + ۳ مطالعهٔ zero-explicit |
| باقیمانده | ۶ مطالعه، تصادفی ساده با seed ثابت، لایه‌بندی سالی |
| seed | `20261103` (تاریخ منجمدشدن پروتکل) |
| فاصلهٔ حداقلی | **≥ ۱۴ روز** بین کدگذاری اول و دوم |
| سنجه | توافق مشاهده‌شده + Cohen's κ به‌ازای هر بعد + CI ≈۹۵٪ + باند Landis–Koch |
| ترتیب ارائه | به‌هم‌ریخته با همان seed (ستون `re_order` در شیت) |

**قضایت طراحی**: افزودن عمدی مطالعات دارای سطوح کمیاب (O/S-explicit) و مطالعات
zero-explicit باعث می‌شود هر سه سطح E/P/NR در نمونه حضور داشته باشد و κ زیر
سلطهٔ غلبهٔ یک‌سطحی (prevalence paradox) نرود؛ برآورد حاصل برای کل ماتریس
**محافظه‌کارانه** تفسیر می‌شود. این انتخاب صادقانه در §10.4 گزارش خواهد شد.

## ۲) قواعد کورسازی (در تمام فاصلهٔ دوهفته‌ای الزامی)
- فایل‌های زیر تا پس از برگرداندن شیت **باز نشوند**:
  - `_draft\dmdi_coding_matrix.csv` (شامل امتیازهای اصلی A_)
  - `DMDI_IntraCoder\SUBSAMPLE_key.csv` (ناک کدگذار A)
  - هر نسخه‌ای از شیت master یا بستهٔ تکمیلی که ستون‌های A_* دارد
- هنگام کدگذاری فقط از **متن کامل مقاله** (بازیابی با DOIِ ستون شیت) استفاده شود؛
  بدون دستیار AI؛ بدون مراجعه به یادداشت‌های قبلی.
- اگر حافظه چیزی را بازمی‌گرداند، خودکار همان را ننویسید؛ فقط متن مقاله ملاک است.
- ترتیب انجام همان ترتیب `re_order` (به‌هم‌ریخته) است؛ مرتب‌سازی نکنید.

## ۳) نحوهٔ پر کردن شیت
- فایل: `IntraCoder_ReCode_SHEET.csv` (۱۵ ردیف)
- ستون‌های `B_I … B_P` را با دقیقاً یک توکن پُر کنید: **E / P / NR**
- ستون `notes`: اختیاری ولی توصیه‌شده؛ به‌خصوص برای تمایزهای دشوار P/NR یا E/P
- هیچ سلولی خالی نماند؛ اگر واقعاً نامشخص است: NR + یادداشت
- ملاک همان قواعد codebook (`DMDI_Codebook.docx` در بستهٔ تکمیلی) است —
  نسخهٔ همان زمان کدگذاری اول؛ هیچ قاعده‌ای بین دو گذر تغییر نمی‌کند.

## ۴) تقویم
| رویداد | تاریخ |
|---|---|
| منجمدشدن پروتکل + کورسازی | **۳ نوامبر ۲۰۲۶** |
| کمترین تاریخ مجاز برای شروع بازگداری | **۱۷ نوامبر ۲۰۲۶** |
| بازهٔ زمانی هر مطالعه | ۳۰–۶۰ دقیقه (بخش method + experiment) |
| برگرداندن شیت | پس از پایان هر ۱۵ مورد — حداکثر تا ۲۰ نوامبر ۲۰۲۶ |
| محاسبه و گزارش | همان روز، با `intra_check.py` |

در پایان، تاریخ‌های واقعی برای درج صادقانه در مقاله ثبت شود:
- تاریخ شروع بازگداری: ________
- تاریخ پایان بازگداری: ________
- فاصله از کدگذاری اول (روز): ________

## ۵) پس از برگرداندن شیت
1. شیت پرشده را با نام `RETURNED_IntraCoder_ReCode.csv` در همین پوشه ذخیره کنید.
2. اجرا: `python intra_check.py RETURNED_IntraCoder_ReCode.csv`
3. خروجی: جدول κ به‌ازای هر بعد + فهرست سلول‌های مغایر برای داوری.
4. سلول‌های مغایر داوری و در ماتریس منتشرشده اعمال می‌شوند؛ **κ گزارش‌شده همان
   محاسبهٔ اول می‌ماند** و داوری جداگانه ثبت می‌شود (هرگز بعد از داوری κ
   بازمحاسبه نمی‌شود).
5. سپس متن §2.7 / §10.4 / §11.6(ii) با اعداد واقعی به‌روز می‌شود
   (اسکریپت idempotent تست‌شدهٔ همین پروژه).

## ۶) درج در مقاله (پیش‌نویس متن انگلیسی — اعداد پس از محاسبه جایگزین می‌شوند)

§2.7 — به‌عنوان جملهٔ بعدیِ هشدار موجودِ «has not yet been validated by
independent double-coding» (نسخهٔ دو-عامله پس از اصلاحیهٔ ۲):

> As an instrument-stability check, a stratified subsample of 15 of the 39
> verified-core studies (38%) — including every study judged Explicit on either
> of the two most rarely-Explicit dimensions, every study with no Explicit
> rating, and a seeded, year-stratified random remainder — was coded a second
> time, on [DATE], by two different, independently operated AI coding agents
> from two different model families ([MODEL 1]; [MODEL 2]; see the Use of
> AI-Assisted Technologies statement), under the unchanged codebook, blinded
> to the original ratings and notes and to each other's outputs. Statistical
> agreement with the original coding pass was κ = [VALUE_A1] (agent 1) and
> κ = [VALUE_A2] (agent 2), and the two agents agreed with each other at
> κ = [VALUE_A1A2] (per-dimension details in §10.4 and the supplementary
> package). Because all passes, like the first, involve AI assistance under
> researcher supervision, these statistics evidence the repeatability of the
> coding instrument as specified, not independent human validation;
> double-coding by a blinded human coder remains the open agenda item in
> Section 11.6 (ii).

§10.4 — پس از جملهٔ «should be read as indicative of a pattern» (نسخهٔ
دو-عامله پس از اصلاحیهٔ ۲):

> The instrument-stability check in Section 2.7 quantifies the reproducibility
> bound on these counts: a stratified 15-of-39 subsample was coded a second
> time by two different AI coding agents under the unchanged codebook, blinded
> to the original ratings and to each other. Across the 120 dimension-level
> ratings of the subsample, agreement with the original pass reached mean
> κ = [MEAN_A1] (agent 1) and [MEAN_A2] (agent 2), the agents agreed with each
> other at mean κ = [MEAN_A1A2], and [N] of 120 ratings changed between passes
> ([RATE]%). Cells on which both agents departed from the original coding were
> adjudicated against the source texts and are reflected in the published
> matrix. Because these checks span AI-assisted passes rather than human
> coders, they are reported as instrument repeatability; independent
> double-coding by a blinded human coder remains open (Section 11.6 (ii)),
> and the codebook and a blank coding sheet accompany this review so that any
> reader can run the same instrument.

§11.6 — بازنویسی بند (ii):

> (ii) a blinded re-coding by an independent human coder to re-apply the DMDI
> and Q1–Q8 instruments to the verified core and report inter-coder agreement
> (e.g., Cohen’s κ or Krippendorff’s α) per dimension — the agent-based
> instrument-stability check reported in Section 2.7 addresses repeatability
> of the instrument under AI assistance, not this item;

## ۷) ملاحظات گزارش‌دهی
- در متن مقاله فقط واژگان instrument stability / repeatability / agent-based؛
  هرگز inter-coder یا double-coded برای این سنجه؛ واژهٔ intra-coder هم
  دیگر به‌کار نمی‌رود (پس از اصلاحیهٔ ۲ کدگذار اصلی هم AI-assisted است).
- بخش «Use of AI-Assisted Technologies» مقاله باید هر دو مدل + تاریخ + نسخه +
  نقش (repeat coding under supervision) را ذکر کند — من متنش را با نتایج
  آماده می‌کنم.
- اگر بعدی در نمونه prevalence بالا داشته باشد (مثلاً R که غالباً P است)،
  اسکریپت flag می‌دهد؛ این flag صادقانه در §10.4 ذکر می‌شود.
- هیچ ادعایی در چکیده دربارهٔ این سنجه نمی‌آید؛ چکیده فقط "single coding pass"
  فعلی را حفظ می‌کند مگر بعداً تصمیم متفاوتی گرفته شود.
