# -*- coding: utf-8 -*-
"""genoa_probe.py — Genoa IRIS (ssl-unverified) -> find repository PDF copy."""
import io, re, ssl, sys, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"}
url = "https://hdl.handle.net/11311/1222132"
try:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        final = r.geturl()
        html = r.read(2_000_000).decode("utf-8", errors="replace")
    print("final url:", final)
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if m:
        print("citation_pdf_url:", m.group(1))
    hrefs = sorted(set(re.findall(r'href=["\']([^"\']*(?:\.pdf|bitstream|retrieve)[^"\']*)["\']', html, re.I)))
    for h in hrefs[:15]:
        print("href:", h[:130])
    if not hrefs and not m:
        print("title:", re.findall(r"<title>([^<]*)</title>", html, re.I)[:1])
except Exception as e:
    print("FAIL", str(e)[:150])
