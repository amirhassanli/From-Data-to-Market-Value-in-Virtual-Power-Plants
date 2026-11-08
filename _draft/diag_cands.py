# -*- coding: utf-8 -*-
"""diag_cands.py — list all candidate URLs per missing study (no downloads)."""
import csv, io, json, os, re, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

EMAIL = "dmdi.review.2026@gmail.com"
DOI = {}
with open(r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\Coding_Sheet_BLIND.csv",
          newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        DOI[r["study"].strip()] = (r.get("doi") or "").strip()

key = list(csv.DictReader(open(r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder\SUBSAMPLE_key.csv",
                               newline="", encoding="utf-8-sig")))
have = {fn.split("__")[0] for fn in os.listdir(
    r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder\PDFs")}

for row in key:
    study = row["study"].strip()
    if row["reference"].strip("[]") in have:
        continue
    doi = DOI.get(study, "")
    print("### %-42s %s" % (study[:42], doi))
    # unpaywall
    try:
        with urllib.request.urlopen("https://api.unpaywall.org/v2/%s?email=%s" % (doi, EMAIL),
                                    timeout=30) as resp:
            up = json.load(resp)
        locs = ([up.get("best_oa_location") or {}] +
                [l for l in (up.get("oa_locations") or [])])
        for l in locs:
            print("  UP %-8s pdf: %s" % (l.get("host_type", "?"), (l.get("url_for_pdf") or "-")[:90]))
            print("  UP %-8s lnd: %s" % (l.get("host_type", "?"), (l.get("url") or "-")[:90]))
    except Exception as e:
        print("  UP FAIL", str(e)[:60])
    # openalex
    try:
        req = urllib.request.Request("https://api.openalex.org/works/https://doi.org/%s" % doi,
                                     headers={"User-Agent": "diag/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            meta = json.load(resp)
        for l in (meta.get("locations") or []):
            print("  OA oa=%-5s pdf: %s" % (l.get("is_oa"), (l.get("pdf_url") or "-")[:90]))
            print("  OA oa=%-5s lnd: %s" % (l.get("is_oa"), (l.get("landing_page_url") or "-")[:90]))
    except Exception as e:
        print("  OA FAIL", str(e)[:60])
    time.sleep(0.3)
    print()
