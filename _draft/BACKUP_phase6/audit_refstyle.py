# -*- coding: utf-8 -*-
import sys, io, re, docx
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
     r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P)
ps = d.paragraphs
cut = next(i for i, p in enumerate(ps) if p.text.strip().startswith("14. References"))
refs = [p for p in ps[cut + 1:] if re.match(r"^\[\d+\]", p.text.strip())]

no_issue = []
has_issue = []
ital = 0
for p in refs:
    t = p.text
    n = int(re.match(r"^\[(\d+)\]", t).group(1))
    (has_issue if re.search(r"no\.\s*\d", t) else no_issue).append(n)
    if any(r.italic for r in p.runs):
        ital += 1

print("entries with 'no. <issue>': %d %s" % (len(has_issue), has_issue))
print("entries without:           %d %s" % (len(no_issue), no_issue))
print("entries using italic runs: %d / %d" % (ital, len(refs)))

print("\n=== sample run breakdown, [1] and [4] ===")
for p in refs[:4]:
    print(p.text[:60])
    for r in p.runs[:8]:
        print("    italic=%s  %r" % (r.italic, r.text[:60]))
    print()
