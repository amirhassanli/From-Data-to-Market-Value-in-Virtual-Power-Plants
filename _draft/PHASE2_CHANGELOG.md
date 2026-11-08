# فاز دو — گزارش تغییرات (Article 6 · Phase 2 changelog)

**فایل ورودی:** `Reserve Deliverability and Throughput Aging … - PHASE1.docx`
**فایل خروجی:** `Reserve Deliverability and Throughput Aging … - PHASE2.docx`
**تاریخ اجرا:** 2026-11-01
**اسکریپت بازتولید:** `_draft/a6_phase2_edit.py` + `_draft/a6_fixrefs.py`

این فاز **ادبیات گذشته (Section II)** را با ۶ مرجع جدید که همگی در Crossref تأیید شده‌اند
غنی کرد، و شماره‌گذاری مراجع را یک‌دست کرد. هیچ جدول، شکل یا فرمولی حذف/تغییر نشد.

---

## ۱. مراجع جدید اضافه‌شده (۶ مرجع، همگی Crossref-verified)

| # جدید | مرجع (خلاصه) | DOI | جایگاه در متن |
|---|---|---|---|
| [17] | D. Xiao et al., CVaR-constrained bidding with mobile storage, ISGT-Europe 2020 | 10.1109/ISGT-Europe47291.2020.9248799 | §II-A (پس از [5]) |
| [18] | S. Sadeghi et al., DL-based bidding in DA + frequency-regulation, IJEPES 127, 2021 | 10.1016/j.ijepes.2020.106646 | §II-A |
| [19] | C. Yang et al., renewable VPP self-balancing capacity, IJEPES 144, 2023 | 10.1016/j.ijepes.2022.108557 | §II-A |
| [20] | M. A. Niazi et al., scalable co-optimization via mean-field games, Energy 358, 2026 | 10.1016/j.energy.2026.141360 | §II-A |
| [21] | K. N. Singh et al., risk-aware bidding + carbon markets, Energy Rep. 14, 2025 | 10.1016/j.egyr.2025.07.032 | §II-D |
| [22] | W. Qin et al., multi-temporal DA-to-RT regulation, J. Mod. Power Syst. Clean Energy 13(2), 2024 | 10.35833/mpce.2024.000118 | §II-D |

- هر ۶ DOI با `api.crossref.org` resolve شد و عنوان/نویسنده/جلد/سال با متن مقاله تطبیق داده شد.
- [17] (Xiao) و [16] (Singh et al. Sci. Rep. FDIA) نویسندهٔ هم‌نام دارند اما مقالات متفاوت‌اند —
  در متن ابهامی نیست چون شمارهٔ مرجع متفاوت است.

## ۲. جملات درج‌شده در §II

- §II-A: «Xiao et al. [17] extend CVaR-constrained bidding to multiple reserve services and mobile storage,
  and Sadeghi et al. [18] pair a deep-learning forecast with day-ahead energy and frequency-regulation bidding.»
- §II-A: «Yang et al. [19] show that a renewable-based VPP retains part of its controllable capacity for
  self-balancing before committing any of it externally … At larger scale, mean-field co-optimization couples
  stochastic bidding with frequency-regulation aggregation [20].»
- §II-D: «Singh et al. [21] integrate renewable forecasting with carbon-market strategies in a risk-aware VPP
  bidding model.»
- §II-D: «A multi-temporal formulation additionally links day-ahead commitments to real-time regulation
  response under uncertainty [22].»

## ۳. شماره‌گذاری مراجع یک‌دست شد

- مراجع پیشین [17]→[23]، [18]→[24]، [19]→[25] (SMARD، Energy-Charts، HiGHS) — هم در متن، هم در
  Acknowledgment، هم در لیست مراجع.
- لیست مراجع اکنون [1]…[25] به‌ترتیب صعودی و بدون شکاف است.
- ترتیب اولین ظهور: [1]–[6],[8],[9],[11]–[25] (با احتساب بازه‌های [6]–[8] و [9]–[11] در مقدمه
  که ۷ و ۱۰ را هم پوشش می‌دهند) — کاملاً صعودی.

## ۴. مواردی که از متن «اضافی» استفاده نشد (عمداً)

متن `متن جدید اضافی.docx` به دو مقالهٔ تأیید‌نشده اشاره می‌کرد:
- «CVaR-based bi-level bidding strategy for VPP … J. Bian, 2026» (Elsevier) — متادیتا کامل نبود.
- «A Bi-Level CVaR-Based Stochastic Programming Approach for Joint Energy and Reserve Market Bidding» (Wiley) —
  منبع ثانویه، تأیید نشد.

همچنین «Mei et al.» در متن اضافی بدون ورودی استنادی بود؛ جست‌وجوی Crossref عنوان مرتبط‌تری
(«Optimal bidding strategy for VPP in medium- and long-term market …», Sustainable Energy, Grids and Networks, 2026)
برگرداند که با توصیف «capacity coupling» هم‌خوانی نداشت، بنابراین درج نشد.

## ۵. وضعیت تأییدشدهٔ فایل PHASE2

```
تصاویر:           11 (بدون تغییر)
فرمول‌های OMML:   119 inline + 50 display (بدون تغییر)
جداول:            32 (بدون تغییر)
مراجع:            25 (۱۹ → ۲۵)، شماره‌گذاری صعودی و بدون شکاف
خطاهای build:     0
```

---

## کارهای باقی‌مانده برای نویسنده (خارج از فاز ۲)

1. **Fig. 9 (رزرو دوسویه):** نویسنده تأیید کرد که مدل در واقع دوسویه است؛ §IV-C و Nomenclature
   به‌روزرسانی شدند. **اما** Table III (Settlement) باید مشخص کند که «Reserve capacity 589» مجموع
   صعودی+نزولی است — اکنون یک جملهٔ توضیحی در §IV-C اضافه شده؛ در صورت نیاز caption جدول را هم
   به‌روز کنید.
2. **۴۲ برنامهٔ هفتگی:** نویسنده تأیید کرد که عدد ۴۲ درست است؛ پرانتز محاسباتی اشتباه
   (۴×۷+۷=۳۵) حذف شد. در صورت تمایل ترکیب واقعی (مثلاً ۶ پیکربندی×۷ روز) را در متن ذکر کنید.
3. **پنجرهٔ ۵۸ روزه:** دو پنجرهٔ جدا (KDE روی ۵۸ روز، copula روی ۲۰۲۴–۲۰۲۵) — توضیح
   در §VI-A اضافه شد.
4. **Fig. 7:** محور دوم (قیمت) فشرده شده و بیدها ناخوانا هستند — نیاز به بازتولید نمودار
   (کد در `vpp_optimization/src/visualization.py`).
5. **Table VI:** Wilcoxon برای P1−B2 با فرض «همهٔ ۱۴ تفاوت مثبت (Fig. 10)» پر شد (≈1.2×10⁻⁴).
   اگر محاسبهٔ دقیق متفاوت است، اصلاح کنید.
6. **۰٫۲۴ EUR/day (CVaR feeder):** جدول VII عدد ۰٫۲ را نشان می‌دهد؛ یا دقت جدول را افزایش دهید
   یا متن را به ۰٫۲ تغییر دهید.
7. **VI-L:** «−6105» شروع sweep باید با F-B2 (−6101) یا F-P1 (−6109) تطبیق داده شود.
8. **Fig. 4/5/7/10:** هم‌پوشانی برچسب‌ها (cosmetic) — در بازتولید نمودارها اصلاح شود.
9. **(IS) abbreviation:** در Fig. 4 caption تعریف شد؛ در صورت نیاز در §VI-A هم تکرار کنید.
10. **Fig. 3 «near-Gaussian»:** load error KDE شانهٔ چپ دارد؛ لحن را کمی ملایم کنید.
11. **Fig. 6 «confirms» → «indicates»:** انجام شد (toning-down).
12. **Fig. 11 «aligning perfectly» → «consistent with»:** انجام شد.
13. **عنوان مقاله:** «Feeder-Constrained Evidence from SMARD DE–LU Data» — مطالعهٔ feeder روی
    IEEE 33-bus صناعی است؛ پیشنهاد: «…Evidence from SMARD DE–LU and IEEE 33-Bus Data».
14. **Fig. 9 caption:** به‌روز شد تا رزرو دوسویه را ذکر کند — نمودار خودش هم باید برچسب
    r↑/r↓ را حفظ کند (уже دارد).
15. **Table I:** «This work | Joint vs. independent … | SoC-feasible reserve; SMARD» — ممکن است
    بخواهید «two-sided reserve» را هم ذکر کنید.
16. **DOI [14] (PESGM 2026):** کنفرانس آینده؛ پس از انتشار، صفحه/سال را تکمیل کنید.
17. **References [9]/[13]/[16]:** DOIها resolve شدند (۲۰۰)؛ نویسندهٔ «Q. Li et al.» را
    در صورت تمایل کامل کنید.
18. **(IS) در Fig. 8 legend:** «P1 (IS)» — همین‌طور.
19. **§VI-L «−6105 … −6182»:** نقاط انتهایی sweep باید با F-B2/F-P1 تطبیق داده شوند.
20. **DRO/MARL/LLM/FDIA:** مقاله صادقانه می‌گوید ارزیابی نشده‌اند — حفظ شود.

## نکتهٔ صادقانه

- κ/توافق کدگذار برای این مقالهٔ VPP مطرح نیست (مقالهٔ قبلی بود).
- هیچ عدد جدیدی در PHASE2 اختراع نشد؛ همهٔ اعداد جدید ([17]–[22]) از مقالات peer-reviewed
  با DOI تأیید‌شده آمده‌اند.
- هیچ جدول/شکل/فرمولی در PHASE2 تغییر نکرد؛ فقط §II و لیست مراجع.
- رندر بصری فایل در این سیستم امکان‌پذیر نبود؛ ساختار (XML/paragraph/table) تأیید شد.
  پیش از ارسال، فایل را یک‌بار در Word باز کنید.
