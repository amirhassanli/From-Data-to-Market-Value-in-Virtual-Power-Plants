# -*- coding: utf-8 -*-
"""
collect_pdfs2.py — second pass: try harder for the 11 studies still missing a
full-text PDF under Downloads\\DMDI_IntraCoder\\PDFs\\.

Sources tried per study (in order), all legitimate OA routes only:
  1. Unpaywall API (url_for_pdf of best + all locations)
  2. Publisher direct-PDF patterns for known-OAP gold items
     (MDPI /pdf, Wiley pdfdirect)
  3. OpenAlex OA landing pages (fetch HTML, extract <meta citation_pdf_url>
     and .pdf hrefs — works for institutional repositories like vbn.aau.dk)
  4. Retry OpenAlex best_oa_location.pdf_url with a browser-like UA
"""
import csv, io, json, os, re, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder"
OUT = os.path.join(HERE, "PDFs")
BROWSER = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

EMAIL = "dmdi.review.2026@gmail.com"   # generic contact for Unpaywall pool

def fetch(url, timeout=45, referer=None):
    req = urllib.request.Request(url, headers={
        "User-Agent": BROWSER,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        **({"Referer": referer} if referer else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(12_000_000)

def try_save(url, fn, referer=None):
    try:
        data = fetch(url, referer=referer)
    except Exception:
        return "FAIL:%s" % url[:80]
    if data[:5] == b"%PDF-":
        with open(fn, "wb") as f:
            f.write(data)
        return "SAVED %s (%d KB)" % (os.path.basename(fn), len(data) // 1024)
    if b"citation_pdf_url" in data or b".pdf" in data[:400000]:
        return "HTML:%s" % url[:80]
    return "NONPDF:%s" % url[:80]

def pdf_from_html(url):
    """extract candidate pdf urls from a landing page"""
    try:
        data = fetch(url)
    except Exception:
        return []
    html = data.decode("utf-8", errors="replace")
    cands = []
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if m:
        cands.append(m.group(1))
    for m in re.finditer(r'href=["\']([^"\']+\.pdf[^"\']*)["\']', html, re.I):
        u = m.group(1)
        if u.startswith("//"):
            u = "https:" + u
        elif u.startswith("/"):
            base = re.match(r"(https?://[^/]+)", url).group(1)
            u = base + u
        cands.append(u)
    return list(dict.fromkeys(cands))[:4]

DOI = {}
with open(r"C:\Users\Mahboobian\Downloads\DMDI_SecondCoder\Coding_Sheet_BLIND.csv",
          newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        DOI[r["study"].strip()] = (r.get("doi") or "").strip()

key = list(csv.DictReader(open(os.path.join(HERE, "SUBSAMPLE_key.csv"),
                               newline="", encoding="utf-8-sig")))
have = {fn.split("__")[0] for fn in os.listdir(OUT)}

todo = [row for row in key
        if row["reference"].strip("[]") not in have]
print("already have: %d | trying now: %d\n" % (len(have), len(todo)))

report = []
for row in todo:
    study = row["study"].strip()
    doi = DOI.get(study, "")
    if not doi:
        report.append((study, "NO-DOI")); continue
    fn = os.path.join(OUT, "%s__unknown.pdf" % row["reference"].strip("[]"))
    cands = []

    # 1) Unpaywall
    try:
        with urllib.request.urlopen(
                "https://api.unpaywall.org/v2/%s?email=%s" % (doi, EMAIL),
                timeout=30) as resp:
            up = json.load(resp)
        for loc in ([up.get("best_oa_location") or {}] +
                    [l for l in (up.get("oa_locations") or [])]):
            u = (loc.get("url_for_pdf") or "").strip()
            if u:
                cands.append(u)
    except Exception:
        pass

    # 2) publisher direct patterns
    if doi.startswith("10.3390/"):
        # MDPI: 10.3390/en18061383 -> en 18(6) 1383
        m = re.match(r"10\.3390/([a-z]+)(\d{2})(\d{2})(\d+)$", doi)
        if m:
            cands.append("https://www.mdpi.com/%s/%s/%s/%s/%s/pdf"
                         % (m.group(1), m.group(2), m.group(3), m.group(4), doi.rsplit("/", 1)[1]))
    elif doi.startswith("10.1049/"):
        cands.append("https://ietresearch.onlinelibrary.wiley.com/doi/pdfdirect/%s"
                     "?download=true" % doi)

    # 3) OpenAlex landing pages
    try:
        req = urllib.request.Request("https://api.openalex.org/works/https://doi.org/%s" % doi,
                                     headers={"User-Agent": BROWSER})
        with urllib.request.urlopen(req, timeout=30) as resp:
            meta = json.load(resp)
        for l in (meta.get("locations") or []):
            if l.get("is_oa") and (l.get("landing_page_url") or "").strip():
                cands.append(l["landing_page_url"].strip())
            u = (l.get("pdf_url") or "").strip()
            if u:
                cands.append(u)
    except Exception:
        pass

    cands = list(dict.fromkeys(cands))
    status = "NO-CANDIDATE"
    for c in cands:
        if "sciencedirect.com" in c and "/pdf" not in c and "/pdfft" not in c:
            pass   # landing page still worth href extraction
        r = try_save(c, fn)
        if r.startswith("SAVED"):
            status = r
            break
        if r.startswith("HTML:"):
            for u2 in pdf_from_html(c):
                r2 = try_save(u2, fn, referer=c)
                if r2.startswith("SAVED"):
                    status = r2
                    break
            if status.startswith("SAVED"):
                break
    else:
        if not status.startswith("SAVED"):
            status = "no luck (%d candidates tried)" % len(cands)
    report.append((study, status))
    time.sleep(0.5)

print("=== second-pass report ===")
for s, st in report:
    print("%-40s %s" % (s[:40], st))
n = len(os.listdir(OUT))
print("\ntotal PDFs now in folder: %d / 15" % n)
