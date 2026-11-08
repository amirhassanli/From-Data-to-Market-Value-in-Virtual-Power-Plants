# -*- coding: utf-8 -*-
"""repo_probe.py — extract candidate PDF links from two repository landing pages
(TUM mediatum for Wozabal, Genoa IRIS for Falabretti)."""
import io, re, sys, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"}

targets = [
    ("Wozabal TUM", "https://mediatum.ub.tum.de/1524381"),
    ("Falabretti Genoa hdl", "https://hdl.handle.net/11311/1222132"),
]
for name, url in targets:
    print("###", name)
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=45) as r:
            html = r.read(2_000_000).decode("utf-8", errors="replace")
        m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
        if m:
            print("  citation_pdf_url:", m.group(1))
        hrefs = sorted(set(re.findall(r'href=["\']([^"\']*(?:\.pdf|bitstream|download)[^"\']*)["\']', html, re.I)))
        for h in hrefs[:12]:
            print("  href:", h[:130])
        if not hrefs and not m:
            print("  title-tag:", re.findall(r"<title>([^<]*)</title>", html)[:1])
    except Exception as e:
        print("  FAIL", str(e)[:100])
    print()
