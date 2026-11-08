# -*- coding: utf-8 -*-
"""
collect_pdfs.py — try to fetch open-access full-text PDFs for the 15
subsample studies (via OpenAlex best-OA locations), into
Downloads\\DMDI_IntraCoder\\PDFs\\. Paywalled items are reported for manual
institutional download. Only OA repository links are used (no publisher bypass).
"""
import csv, io, json, os, re, sys, urllib.request, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder"
OUT = os.path.join(HERE, "PDFs")
os.makedirs(OUT, exist_ok=True)

# study -> doi  (from the coder-facing blind sheet of the full 39)
DOI = {}
with open(r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\Coding_Sheet_BLIND.csv",
          newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        DOI[r["study"].strip()] = (r.get("doi") or "").strip()

key = list(csv.DictReader(open(os.path.join(HERE, "SUBSAMPLE_key.csv"),
                               newline="", encoding="utf-8-sig")))
UA = {"User-Agent": "oa-pdf-collector/1.0 (mailto:research@example.org)"}

def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s)[:48].strip("_")

report = []
for row in key:
    study = row["study"].strip()
    doi = DOI.get(study, "")
    if not doi:
        report.append((study, doi, "NO-DOI", ""))
        continue
    try:
        req = urllib.request.Request(
            "https://api.openalex.org/works/https://doi.org/%s" % doi, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as resp:
            meta = json.load(resp)
    except Exception as e:
        report.append((study, doi, "META-FAIL", str(e)[:80]))
        continue

    oa = meta.get("open_access", {})
    locs = []
    if meta.get("best_oa_location"):
        locs.append(meta["best_oa_location"])
    locs += [l for l in (meta.get("locations") or []) if l not in locs]
    pdf_url = ""
    for l in locs:
        u = (l.get("pdf_url") or "").strip()
        if u:
            pdf_url = u
            break
    if not pdf_url:
        pdf_url = (oa.get("oa_url") or "").strip()
    ok = ""
    if pdf_url:
        fn = os.path.join(OUT, "%s__%s.pdf" % (row["reference"].strip("[]"), slug(study)))
        try:
            rq = urllib.request.Request(pdf_url, headers=UA)
            with urllib.request.urlopen(rq, timeout=60) as resp:
                data = resp.read(8_000_000)
            if data[:5] == b"%PDF-":
                with open(fn, "wb") as f:
                    f.write(data)
                ok = "SAVED %s (%d KB)" % (os.path.basename(fn), len(data) // 1024)
            else:
                ok = "LANDING-PAGE (not direct pdf): %s" % pdf_url[:80]
        except Exception as e:
            ok = "DL-FAIL %s | %s" % (pdf_url[:60], str(e)[:60])
    else:
        ok = "NO-OA (paywalled all known locations)"
    report.append((study, doi, ok, (oa.get("oa_status") or "")))
    time.sleep(0.4)

print("=== result per study ===")
for study, doi, ok, status in report:
    print("%-40s %-42s %s [%s]" % (study[:40], doi[:40], ok, status))
n_ok = sum(1 for r in report if r[2].startswith("SAVED"))
print("\nsaved: %d / 15" % n_ok)
