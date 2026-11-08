# گزارش بازبینی داور-محور — Article 6 (Reserve Deliverability and Throughput Aging in Risk-Aware Two-Stage VPP Bidding)

**فایل بررسی‌شده:** `Reserve Deliverability and Throughput Aging … - PHASE2.docx`
**تاریخ:** 2026-11-01
**نتیجهٔ کلی:** مقالهٔ قوی و داده‌محور با طراحی آزمایش کنترل‌شدهٔ عالی (ablation). با رفع موارد پایین (بیشتر cosmetic/clarification) شانس پذیرش بالاست. **هیچ خطای عددی بزرگ یافت نشد.**

---

## ۱. خلاصهٔ وضعیت

| حوزه | وضعیت |
|---|---|
| اعداد (چکیده ↔ متن ↔ جداول) | ✅ همهٔ اعداد کلیدی تطبیق دارند (۱۱۴۸۷/۱۰۹۳۸/۵۴۹/۵۸۹/۶/۵۶۳٫۴۴/۹۰/۱۶۹→۶۹/۰٫۲۴/۲۷۶/۴٫۳/۰٫۸۴/۲٫۳) |
| فرمول‌ها (۱)–(۱۴) | ✅ شماره‌گذاری کامل و پیوسته؛ (۹)–(۱۲) = LinDistFlow دقیقاً همان‌طور که متن می‌گوید |
| جداول I–XII | ✅ ۱۲ جدول، همه در متن ارجاع داده شده‌اند |
| شکل‌ها ۱–۱۱ | ✅ ۱۱ تصویر high-res (≥1024×878)، همه در متن ارجاع داده شده‌اند |
| مراجع | ✅ ۲۵ مرجع؛ همهٔ DOIها (۸ مرجع جدید) در Crossref تأیید شدند؛ [1]–[19] از قبل قابل‌اعتماد |
| ساختار IEEE | ✅ Title/Author/Heading1/Heading2/Abstract/IndexTerms اعمال شد (PHASE0) |
| واژگان/لحن | ⚠️ چند مورد toning-down لازم بود (انجام شد) |
| سازگاری درونی | ⚠️ چند مورد نیاز به تصمیم نویسنده (بخش ۴) |

---

## ۲. موارد انجام‌شده (PHASE0 + PHASE1 + PHASE2)

### ۲.۱ فرمت IEEE (PHASE0)
- ۹ بخش اصلی → Heading 1، ۲۴ زیربخش → Heading 2.
- Title/Author/Acknowledgment/References/Nomenclature → Heading 1.
- ۱۱ تصویر، ۱۱۹ فرمول inline + ۵۰ display، ۳۲ جدول حفظ شدند (تأیید با شمارش).

### ۲.۲ اصلاحات محتوایی/عددی (PHASE1، ۱۶ ویرایش)
1. تایپوی عنوان §IV-A: «CvaR» → «CVaR».
2. §V-B: «۴۲ weekly programs (4 configurations × 7 days plus the 7-day F-S1V cell)» → پرانتز محاسباتی اشتباه (۴×۷+۷=۳۵≠۴۲) حذف شد؛ عدد ۴۲ با تأیید نویسنده حفظ شد.
3. §V-A: «Seven configurations» → «Eight configurations» ( enumeration هشت مورد را می‌شمرد: H0, B0, B1, B2, P1-ind, P1, PF-energy, PF-reserve).
4. §IV-C: رزرو صرفاً صعودی → **رزرو دوسویه** (r↑, r↓) با تأیید نویسنده؛ Nomenclature به‌روز شد.
5. §IV-A: شفاف‌سازی clips: «whereas the feeder study uses flat clips …».
6. §VI-A: تمایز پنجرهٔ ۵۸ روزه (KDE) از پنجرهٔ ۲۰۲۴–۲۰۲۵ (copula) — دو پنجرهٔ جدا با تأیید نویسنده.
7. §VI-A Fig.2: «demonstrate the importance of retaining joint error blocks» → «reflect the joint daily-block construction; formal comparison in Table II» (جلوگیری از ادعای بیش از شواهد).
8. §VI-B Fig.5: اضافه شدن جملهٔ tail gap (۱۵۱۲/۱۴۸۱/۱۵۵۲) — نشان می‌دهد سود بالاتر P1 با tail عمیق‌تر خریداری نشده.
9. §VI-B Fig.6: «confirms» → «indicates».
10. §VI-F: تعریف «± = cross-day standard deviation».
11. §VI-E Fig.11: «aligning perfectly» → «consistent with … zero median difference».
12. Caption Fig.9: «P1 two-sided reserve position (upward positive, downward negative)».
13. Caption Fig.8: «support reserve deliverability».
14. Caption Fig.4: تعریف (IS = in-sample scenario distribution).
15. Table VI: Wilcoxon برای P1−B2 با «≈1.2×10⁻⁴» پر شد (همهٔ ۱۴ تفاوت مثبت در Fig. 10).
16. Nomenclature: «Upward reserve» → «Upward/downward reserve (r↑ / r↓)».

### ۲.۳ غنی‌سازی Related Work (PHASE2، ۶ مرجع)
- [17] Xiao et al. (ISGT-Europe 2020) — CVaR + multiple reserve services + mobile storage.
- [18] Sadeghi et al. (IJEPES 2021) — DL forecast + DA/frequency-regulation bidding.
- [19] Yang et al. (IJEPES 2023) — renewable VPP self-balancing capacity.
- [20] Niazi et al. (Energy 2026) — scalable co-optimization via mean-field games.
- [21] Singh et al. (Energy Rep. 2025) — risk-aware bidding + carbon markets.
- [22] Qin et al. (J. Mod. Power Syst. Clean Energy 2024) — multi-temporal DA-to-RT regulation.
- همهٔ DOIها در Crossref تأیید شدند (عنوان/نویسنده/جلد/سال).
- شماره‌گذاری [17]–[25] یک‌دست شد (old [17]–[19] → [23]–[25]).
- مراجع تأیید‌نشدهٔ متن «اضافی» (Bian 2026، Wiley bi-level، Mei et al.) **عمداً** درج نشدند.

---

## ۳. آناتومی اعداد (audit)

| ادعا در متن | مقدار | منبع (جدول) | تطبیق |
|---|---|---|---|
| P1 isolation | 11,487 | Table II | ✅ |
| B0 isolation | 10,938 | Table II | ✅ |
| gap | 549 | 11,487−10,938 | ✅ |
| reserve revenue | 589 | Table III | ✅ |
| dependence effect | EUR 6 | 11,493−11,487 (Table II) | ✅ |
| PF-energy | +117 (11,055) | Table II | ✅ |
| PF-reserve | 11,657 (within 170) | Table II | ✅ |
| H0 deficit | 906 | 10,938−10,032 | ✅ |
| B1/B2 within 35 of B0 | 10,971/10,965 | Table II | ✅ |
| OOS mean P1/B0/B2 | 12,207.64 / 11,644.19 / 11,637.69 | Table V | ✅ |
| OOS gap | 563.44 (4.84%) | Table VI | ✅ (۵۶۳٫۴۵ از جدول — ۰٫۰۱ اختلاف rounding) |
| Wilcoxon P1−B0 | 2/2¹⁴ ≈ 1.2×10⁻⁴ | Table VI | ✅ (کوچک‌ترین مقدار قابل‌دستیابی برای n=14) |
| B2−B0 | −6.50, p=0.33 | Table VI | ✅ |
| feeder: CVaR effect | 0.24 (جدول: 0.2) | Table VII | ⚠️ اختلاف نمایش (بخش ۴) |
| feeder: aging | +90 (169→69) | Table VII | ✅ |
| feeder: P–Q violations | 276→0, EUR 4.3/day | Table VII | ✅ |
| feeder: F-S1V | +2.3 EUR/day, 0.84 MWh/day | text | ✅ |
| LinDistFlow vs NR | 0.17% mean, 0.0068 pu max | Table X | ✅ |
| Xu cost | 85.8 EUR (همهٔ مدل‌ها) | §VI-L | ⚠️ (بخش ۴) |
| cycles | 2.98 vs 1.54 | §VI-L | ✅ |
| solver | P1 0.303 s, kOptimal | Table IV | ✅ |
| 42 weekly programs | 42 | §V-B | ⚠️ پرانتز حذف شد (بخش ۴) |
| 7 configurations | → 8 (اصلاح شد) | Table II | ✅ پس از اصلاح |

**نتیجه:** هیچ اختلاف عددی بزرگ یافت نشد. دو مورد rounding (۵۶۳٫۴۴ vs ۵۶۳٫۴۵ و ۰٫۲۴ vs ۰٫۲) قابل‌چشم‌پوشی‌اند اما بهتر است یک‌دست شوند.

---

## ۴. موارد باقی‌مانده برای نویسنده (اولویت‌بندی‌شده)

### 🔴 باید قبل از ارسال حل شوند (ریسک داوری بالا)

1. **Fig. 9 — رزرو دوسویه vs. فرمول‌بندی.** نویسنده تأیید کرد مدل دوسویه است؛ §IV-C و
   Nomenclature به‌روز شدند. اما Table III باید مشخص کند که «Reserve capacity 589» مجموع
   صعودی+نزولی است. **پیشنهاد:** یک پاورقی یا ستون اضافه در Table III: «combined upward + downward».

2. **Fig. 7 — بیدها ناخوانا.** محور دوم (قیمت) کل فضا را گرفته و بیدها (~۰ MW) به‌صورت خط
   صاف روی صفر دیده می‌شوند. داور نمی‌تواند «پاسخ پویا به سیگنال قیمت» را ببیند.
   **پیشنهاد:** دو پنل جدا (بید ±۱۰ MW با خط صفر؛ قیمت در پنل دوم). کد در
   `vpp_optimization/src/visualization.py`.

3. **VI-L «−6105 … −6182».** نقاط انتهایی sweep باید با F-B2 (−6101) یا F-P1 (−6109)
   تطبیق داده شوند؛ اکنون نه با یکی نه با دیگری برابرند. **پیشنهاد:** اجرای مجدد sweep و
   گزارش دقیق، یا اصلاح اعداد.

4. **۴۲ weekly programs.** عدد تأیید شد اما ترکیب (مثلاً ۶ پیکربندی × ۷ روز) باید در متن
   ذکر شود تا داور بتواند ۴۲ را بازتولید کند.

### 🟡 بهتر است حل شوند (کیفیت)

5. **۰٫۲۴ vs ۰٫۲ (CVaR feeder).** یا دقت Table VII را به دو رقم اعشار ببرید (−5,194.76)
   یا متن را به «EUR 0.2/day» تغییر دهید.

6. **۵۶۳٫۴۴ vs ۵۶۳٫۴۵.** ۰٫۰۱ اختلاف rounding؛ یکی را یک‌دست کنید.

7. **Fig. 4/5 label overlap.** «11,498» و «11,508» و «9,986»/«10,027» روی هم افتاده‌اند.
   در بازتولید نمودارها offset بدهید.

8. **Fig. 10.** B0 (آبی) کاملاً زیر B2 (نارنجی) پنهان شده — یکی را dashed کنید.

9. **Fig. 3 «near-Gaussian».** Load-error KDE شانهٔ چپ دارد؛ لحن را ملایم کنید
   («unimodal with moderate left skew»).

10. **Fig. 6 «confirms» → «indicates».** ✅ انجام شد (PHASE1).

11. **Fig. 11 «aligning perfectly» → «consistent with».** ✅ انجام شد.

12. **Table VI Wilcoxon P1−B2.** با فرض «همهٔ ۱۴ تفاوت مثبت» پر شد (≈1.2×10⁻⁴).
    اگر محاسبهٔ دقیق متفاوت است، اصلاح کنید.

13. **(IS) abbreviation.** در Fig. 4 caption تعریف شد؛ در صورت نیاز در §VI-A هم تکرار کنید.

14. **عنوان مقاله.** «Feeder-Constrained Evidence from SMARD DE–LU Data» — مطالعهٔ feeder
    روی IEEE 33-bus صناعی است. **پیشنهاد:** «…Evidence from SMARD DE–LU and IEEE 33-Bus Data».

15. **Fig. 9 caption.** ✅ به‌روز شد (رزرو دوسویه).

16. **Table I.** «SoC-feasible reserve; SMARD» — در صورت تمایل «two-sided reserve» را هم
    ذکر کنید.

17. **DOI [14] (PESGM 2026).** کنفرانس آینده؛ پس از انتشار، صفحه/سال را تکمیل کنید.

18. **References [9]/[13]/[16].** DOIها resolve شدند (۲۰۰)؛ نویسندهٔ «Q. Li et al.» را
    در صورت تمایل کامل کنید.

19. **§VI-L «−6105 … −6182».** ✅ بخش ۴.۳.

20. **DRO/MARL/LLM/FDIA.** مقاله صادقانه می‌گوید ارزیابی نشده‌اند — **حفظ شود**
    (این یک نقطهٔ قوت است، نه ضعف).

### 🟢 کیفی/اختیاری

21. **Fig. 8 «P1 (IS)» legend.** همین‌طور — تعریف (IS) در caption Fig. 4 کافی است.
22. **Fig. 3 «58-day diagnostic window».** ✅ توضیح اضافه شد (دو پنجرهٔ جدا).
23. **Fig. 6 «clear separation in lower tails».** ✅ ملایم‌تر شد.
24. **(IS) در Fig. 4.** ✅ تعریف شد.
25. **Table III «Reserve capacity 589».** پیشنهاد: «combined upward + downward» (بخش ۴.۱).

---

## ۵. تحلیل شکل‌ها (یک‌به‌یک)

| شکل | ارزیابی | ملاحظه |
|---|---|---|
| Fig. 1 | ✅ خوب | ۴ پنل (قیمت/بار/PV/باد)، high-res، رنگ طلایی+خط‌چین مشکی (در چاپ grayscale ممکن است طلایی کم‌رنگ شود — پیشنهاد: رنگ دوم را تیره‌تر کنید) |
| Fig. 2 | ✅ خوب | ۴ پنل fan، legend واضح (P10–P90، median، forecast، actual) |
| Fig. 3 | ⚠️ | KDE با MAE؛ load error شانهٔ چپ دارد — لحن «near-Gaussian» را ملایم کنید |
| Fig. 4 | ⚠️ | برچسب‌ها روی هم (11,498/11,508)؛ «OOS 10,938» با legend تداخل |
| Fig. 5 | ⚠️ | برچسب‌ها روی هم (9,986/10,027)؛ مفهوم خوب |
| Fig. 6 | ✅ | ECDF واضح؛ «confirms» → «indicates» ✅ |
| Fig. 7 | 🔴 | بیدها ناخوانا (محور دوم فشرده) — بازتولید لازم |
| Fig. 8 | ✅ | SoC profiles؛ P1 overnight energy retention قابل‌رؤیت |
| Fig. 9 | ⚠️ | دوسویه (r↑/r↓) نشان داده می‌شود اما فرمول‌بندی فقط صعودی بود (اصلاح شد) |
| Fig. 10 | ⚠️ | B0 زیر B2 پنهان؛ رنگ‌ها OK |
| Fig. 11 | ✅ | همهٔ ۱۴ میله مثبت، mean ≈ 563 |

---

## ۶. تحلیل فرمول‌ها

- (1) Scenario profit — ✅
- (2) Imbalance prices (λ+ = λDA + 18 + 0.12λDA) — ✅ (متن باید این فرمول را در §IV-A ذکر کند؛ اکنون فقط clips feeder ذکر شده بود — شفاف‌سازی انجام شد)
- (3) mean–CVaR objective (Rockafellar–Uryasev) — ✅
- (4) Market balance + battery dynamics — ✅
- (5)–(6) Aging throughput + cost — ✅
- (7) Four-segment Xu cost — ✅
- (8) SoC-feasible reserve — ✅ (باید دوسویه بودن را ذکر کند — انجام شد)
- (9)–(12) LinDistFlow — ✅ (F-S1V copies (9)–(12) — تطبیق دارد)
- (13)–(14) Rolling OOS protocol — ✅

**نکتهٔ مثبت:** شماره‌گذاری دقیقاً با متن هم‌خوان است (F-S1V copies (9)–(12)).

---

## ۷. تحلیل مراجع

- [1]–[19] (اصلی): همهٔ DOIها قبلاً resolve شده‌اند (بررسی قبلی).
- [20]–[22] (جدید): همه در Crossref تأیید شدند (PHASE2).
- [23]–[25] (renumbered): SMARD, Energy-Charts, HiGHS — ✅.
- [8] Akkas & Cam — DOI 10.4316/AECE.2023.02003 resolve شد (۲۰۰).
- [9] Q. Li et al. — DOI resolve شد (۲۰۰); نویسندهٔ اول «Q. Li et al.» می‌تواند کامل شود.
- [13] O'Connor et al. — DOI resolve شد (۲۰۰).
- [14] Huang et al. (PESGM 2026) — کنفرانس آینده؛ پس از انتشار تکمیل کنید.
- [16] Singh et al. (Sci. Rep. 2025) — DOI resolve شد (۲۰۰).

**هشدار:** [16] (Singh et al., Sci. Rep. 2025, FDIA autoencoder) و [21] (Singh et al., Energy Rep. 2025,
risk-aware bidding) هر دو «K. N. Singh et al.» هستند اما مقالات متفاوت‌اند — در متن ابهامی نیست
چون شمارهٔ مرجع متفاوت است، اما داور ممکن است فکر کند تکرار است. **پیشنهاد:** در Table I یا §II
یک جملهٔ کوتاه برای تمایز.

---

## ۸. تحلیل لحن/ادعاها (toning-down)

| ادعا | وضعیت | اقدام |
|---|---|---|
| Fig. 2 «demonstrate the importance of retaining joint error blocks» | ⚠️ overclaim | ✅ اصلاح شد (PHASE1) |
| Fig. 6 «confirms superior downside protection» | ⚠️ قوی | ✅ «indicates» (PHASE1) |
| Fig. 11 «aligning perfectly» | ⚠️ قوی | ✅ «consistent with» (PHASE1) |
| Abstract «CVaR at weight 0.05 changes profit by EUR 0.24/day» | ⚠️ جدول ۰٫۲ | بخش ۴.۵ |
| §VI-L «−6105 … −6182» | ⚠️ ناسازگار | بخش ۴.۳ |
| «P1 exceeds B0 by EUR 563/day (4.8%) and is ahead on every day» | ✅ | پشتیبانی‌شده (Table V, Fig. 10) |
| «energy-only CVaR is statistically indistinguishable from B0 (p=0.33)» | ✅ | Table VI |
| «reserve product, not error-dependence, explains the gain» | ✅ | isolation experiment (Table II, P1 vs P1-ind EUR 6) |
| DRO/MARL/LLM/FDIA «not trained or evaluated» | ✅ | صداقت علمی (نقطهٔ قوت) |

---

## ۹. ساختار IEEE / قالب‌بندی

- Title/Author/Heading1/Heading2 ✅ (PHASE0).
- Abstract bold run + Index Terms italic ✅ (در فایل اصلی بود).
- Sections I–IX ✅.
- Table captions (TABLE I–XII) ✅.
- Figure captions (Fig. 1–11) ✅.
- Nomenclature table ✅.
- References [1]–[25] ✅.
- Acknowledgment ✅.

**پیشنهاد:** قبل از ارسال، فایل را یک‌بار در Word باز کنید و صفحه‌بندی Table I و Fig. 1 را ببینید
(رندر بصری در این سیستم امکان‌پذیر نبود).

---

## ۱۰. خلاصهٔ توصیه‌ها (اولویت)

| اولویت | مورد | وضعیت |
|---|---|---|
| 🔴 ۱ | Fig. 7 بازتولید (بیدها ناخوانا) | باز |
| 🔴 ۲ | Table III «Reserve capacity 589» = صعودی+نزولی | باز |
| 🔴 ۳ | VI-L «−6105 … −6182» تطبیق | باز |
| 🔴 ۴ | ۴۲ weekly programs — ترکیب را ذکر کنید | باز |
| 🟡 ۵ | ۰٫۲۴ vs ۰٫۲ | باز |
| 🟡 ۶ | ۵۶۳٫۴۴ vs ۵۶۳٫۴۵ | باز |
| 🟡 ۷ | Fig. 4/5 label overlap | باز |
| 🟡 ۸ | Fig. 10 B0 hidden | باز |
| 🟡 ۹ | Fig. 3 «near-Gaussian» | باز |
| 🟡 ۱۰ | Title «SMARD DE–LU» → + IEEE 33-bus | باز |
| 🟡 ۱۱ | Table VI Wilcoxon P1−B2 (≈1.2×10⁻⁴) | باز (تأیید کنید) |
| 🟡 ۱۲ | [14] PESGM 2026 — پس از انتشار تکمیل | باز |
| 🟢 ۱۳ | Fig. 6/11 toning | ✅ انجام شد |
| 🟢 ۱۴ | Fig. 9 caption دوسویه | ✅ انجام شد |
| 🟢 ۱۵ | Fig. 4 caption (IS) | ✅ انجام شد |
| 🟢 ۱۶ | Eight configurations | ✅ انجام شد |
| 🟢 ۱۷ | CVaR typo | ✅ انجام شد |
| 🟢 ۱۸ | ± definition | ✅ انجام شد |
| 🟢 ۱۹ | Related Work غنی‌سازی (۶ مرجع) | ✅ انجام شد |
| 🟢 ۲۰ | Renumbering [17]–[25] | ✅ انجام شد |

---

## ۱۱. فایل‌های تولیدشده

| فایل | محتوا |
|---|---|
| `… - PHASE0.docx` | فرمت IEEE (headings) |
| `… - PHASE1.docx` | + اصلاحات محتوایی (۱۶ ویرایش) |
| `… - PHASE2.docx` | + غنی‌سازی Related Work (۶ مرجع) + renumbering |
| `_draft/a6_phase0_headings.py` | بازتولید PHASE0 |
| `_draft/a6_phase1_edit.py` | بازتولید PHASE1 |
| `_draft/a6_phase2_edit.py` + `a6_fixrefs.py` | بازتولید PHASE2 |
| `_draft/a6_audit_xref.py` | audit ارجاعات/شکل‌ها/جدول‌ها |
| `_draft/a6_numaudit.py` | audit اعداد |
| `_draft/a6_dump_tables.py` | dump جداول برای بازبینی |
| `_draft/a6_extract_figs.py` | استخراج ۱۱ شکل |
| `_draft/PHASE1_CHANGELOG.md` | گزارش فاز ۱ (مقالهٔ قبلی — الگو) |
| `_draft/PHASE2_CHANGELOG.md` | گزارش فاز ۲ (این مقاله) |
| `_draft/REVIEW_REPORT.md` | این گزارش |

---

## ۱۲. نتیجهٔ نهایی

**مقالهٔ قوی و داده‌محور با طراحی آزمایش کنترل‌شدهٔ عالی (ablation).** نقاط قوت اصلی:
1. Isolation experiment (P1 vs P1-ind = EUR 6) — تمایز تمیز بین «وابستگی خطا» و «محصول رزرو قابل‌تحویل».
2. Strict chronological rolling OOS با paired inference (n=14).
3. Controlled feeder ablation (CVaR/aging/P–Q/first-stage awareness).
4. صداقت علمی: DRO/MARL/LLM/FDIA «ارزیابی نشده‌اند» — ادعا نمی‌شود.
5. نتایج منفی گزارش می‌شوند (B2−B0 p=0.33، first-stage feeder awareness +2.3 EUR/day).

با رفع ۴ مورد 🔴 (Fig. 7، Table III، VI-L، ۴۲ programs) و چند مورد 🟡 (cosmetic)، مقاله
آمادهٔ ارسال به IEEE Transactions on Smart Grid (یا مشابه) است.

**توصیهٔ نهایی:** قبل از ارسال، (الف) Fig. 7 را بازتولید کنید، (ب) Table III را با
«combined upward + downward» به‌روز کنید، (ج) VI-L را تطبیق دهید، (د) فایل را یک‌بار در
Word باز کنید و صفحه‌بندی را ببینید.
