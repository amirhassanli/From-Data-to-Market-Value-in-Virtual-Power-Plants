# -*- coding: utf-8 -*-
"""s2_pdfs.py — Semantic Scholar openAccessPdf lookup for the 15 subsample studies."""
import csv, io, json, os, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

OUT = r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder\PDFs"
have = {fn.split("__")[0] for fn in os.listdir(OUT)}
BROWSER = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"

DOI = {}
with open(r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\Coding_Sheet_BLIND.csv",
          newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        DOI[r["study"].strip()] = (r.get("doi") or "").strip()

key = list(csv.DictReader(open(r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder\SUBSAMPLE_key.csv",
                               newline="", encoding="utf-8-sig")))


def slug(s):
    import re
    return re.sub(r"[^A-Za-z0-9]+", "_", s)[:48].strip("_")


for row in key:
    study = row["study"].strip()
    ref = row["reference"].strip("[]")
    if ref in have:
        continue
    doi = DOI.get(study, "")
    try:
        req = urllib.request.Request(
            "https://api.semanticscholar.org/graph/v1/paper/DOI:%s?fields=title,openAccessPdf,externalIds" % doi,
            headers={"User-Agent": BROWSER})
        with urllib.request.urlopen(req, timeout=30) as resp:
            meta = json.load(resp)
    except Exception as e:
        print("%-40s S2-FAIL %s" % (study[:40], str(e)[:60]))
        continue
    pdf = (meta.get("openAccessPdf") or {}).get("url", "")
    print("%-40s %s" % (study[:40], pdf[:90] if pdf else "no OA pdf at S2"))
    if pdf:
        fn = os.path.join(OUT, "%s__%s.pdf" % (ref, slug(study)))
        try:
            rq = urllib.request.Request(pdf, headers={"User-Agent": BROWSER})
            with urllib.request.urlopen(rq, timeout=60) as resp2:
                data = resp2.read(12_000_000)
            if data[:5] == b"%PDF-":
                open(fn, "wb").write(data)
                print("     SAVED (%d KB)" % (len(data) // 1024))
            else:
                print("     NONPDF — will try in browser")
        except Exception as e:
            print("     DL-FAIL %s" % str(e)[:50])
    time.sleep(1.2)

print("\ntotal PDFs now in folder: %d / 15" % len(os.listdir(OUT)))
