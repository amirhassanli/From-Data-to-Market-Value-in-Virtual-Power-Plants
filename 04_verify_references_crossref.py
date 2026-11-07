#!/usr/bin/env python3
"""
04_verify_references_crossref.py
Checks every reference that has a DOI against the Crossref REST API (free, no login) and reports:
title similarity, first-author surname match, year match.  References without a DOI are listed for manual lookup.

  python 04_verify_references_crossref.py --manuscript manuscript.md --email you@example.com
Output: reference_check.csv   (status OK / CHECK / NOT_FOUND / NO_DOI)
"""
import argparse, csv, difflib, json, re, time, urllib.parse, urllib.request
from pathlib import Path


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower())


def query(doi, email):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": f"ref-check/1.0 (mailto:{email})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manuscript", required=True)
    ap.add_argument("--email", required=True)
    ap.add_argument("--out", default="reference_check.csv")
    a = ap.parse_args()
    text = Path(a.manuscript).read_text(encoding="utf-8")
    refs = text.split("\n# References\n", 1)[1]
    rows = []
    for line in refs.strip().splitlines():
        m = re.match(r"\[(\d+)\]\s+(.*)", line.strip())
        if not m:
            continue
        n, body = m.groups()
        doi = re.search(r"doi:\s*(10\.\S+?)[.,]?\s*$", body) or re.search(r"(10\.\d{4,9}/[^\s,;]+)", body)
        title = re.search(r"[\u201c\"](.+?)[,.]?[\u201d\"]", body)
        first_author = re.match(r"([A-Z][A-Za-z.\- ]*?)\s+([\w\u00C0-\u017F\-']+)(?:,| and )", body)
        year = re.findall(r"\b(19\d\d|20\d\d)\b", body)
        if not doi:
            rows.append([n, "", "NO_DOI", "", "", "", body[:90]]); continue
        d = doi.group(1).rstrip(".,")
        try:
            msg = query(d, a.email)
            ct = (msg.get("title") or [""])[0]
            sim = difflib.SequenceMatcher(None, norm(title.group(1)) if title else "", norm(ct)).ratio()
            fam = norm((msg.get("author") or [{}])[0].get("family", ""))
            au_ok = fam != "" and fam in norm(body.split("\u201c")[0])
            cy = str((msg.get("issued", {}).get("date-parts") or [[None]])[0][0])
            yr_ok = cy in year
            status = "OK" if (sim > 0.85 and au_ok and yr_ok) else "CHECK"
            rows.append([n, d, status, f"{sim:.2f}", au_ok, yr_ok, ct[:90]])
        except Exception as e:
            rows.append([n, d, "NOT_FOUND", "", "", "", str(e)[:90]])
        time.sleep(0.3)
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ref", "doi", "status", "title_similarity", "first_author_ok", "year_ok", "crossref_title / note"])
        w.writerows(rows)
    bad = [r for r in rows if r[2] != "OK"]
    print(f"{len(rows)} references; {len(bad)} need attention -> see {a.out}")


if __name__ == "__main__":
    main()
