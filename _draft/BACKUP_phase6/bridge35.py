# -*- coding: utf-8 -*-
"""p3 -> p5 reference identity bridge (doi + no-doi keyed) to adjudicate table cells."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P3 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE3.docx")
P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")


def refs_of(path):
    d = docx.Document(path)
    out = {}
    started = False
    for p in d.paragraphs:
        t = p.text.strip()
        if t.startswith("14. References"):
            started = True
            continue
        if started:
            m = re.match(r"^\[(\d+)\]\s*(.+)$", t)
            if m:
                out[int(m.group(1))] = m.group(2)
    return out


def ident(body):
    dm = re.search(r"(10\.\d{4,9}/[^\s,;\)]+[^\s,;.])", body)
    if dm:
        return dm.group(1).lower()
    seg = body.split("\u201c")[0]
    ys = re.findall(r"\b(19|20)(\d\d)\b", body)
    year = (ys[-1][0] + ys[-1][1]) if ys else "?"
    surn = sorted(set(re.findall(r"\b[A-Z][a-zA-Z]{2,}", seg)))[:3]
    return ("K", tuple(surn), year)


r3, r5 = refs_of(P3), refs_of(P5)
i3, i5 = {n: ident(b) for n, b in r3.items()}, {n: ident(b) for n, b in r5.items()}

doi3 = {v: n for n, v in i3.items() if isinstance(v, str)}
doi5 = {v: n for n, v in i5.items() if isinstance(v, str)}

bridge = {}
for n, v in i3.items():
    if isinstance(v, str):
        bridge[n] = doi5.get(v)
print("=== p3 -> p5 bridge ===")
for n in sorted(bridge):
    ok = "OK " if bridge[n] else "MISS"
    print("%s p3[%2d] (%s) -> p5[%s]  %s" % (ok, n, i3[n][:40] if isinstance(i3[n], str) else str(i3[n]), bridge[n], r3[n][:75]))

# no-doi p3 refs: match manually by year+surnames against p5 no-doi refs
print("\n=== p3 no-DOI refs (need manual bridge) ===")
for n, v in i3.items():
    if isinstance(v, tuple):
        print("p3[%2d] %s :: %s" % (n, "/".join(v[1]), r3[n][:90]))

print("\n=== p5 no-DOI refs ===")
for n, v in i5.items():
    if isinstance(v, tuple):
        print("p5[%2d] %s :: %s" % (n, "/".join(v[1]), r5[n][:90]))

# new p5 refs absent from p3 (phase-4 additions)
print("\n=== p5 refs with no p3 counterpart (phase-4 additions) ===")
p3doiset = {v for v in i3.values() if isinstance(v, str)}
for n, v in i5.items():
    if isinstance(v, str) and v not in p3doiset:
        print("p5[%2d] %s :: %s" % (n, v[:45], r5[n][:95]))

# undert pharmacy: dump the specific paragraphs from both docx
import docx as _dx
d3 = _dx.Document(P3)
d5 = _dx.Document(P5)
WANT = ("Veinott", "Martin", "1969529", "1952982", "3691418", "BigData")
print("\n=== paragraphs containing special-context words (p5) ===")
for p in d5.paragraphs:
    if any(w in p.text for w in WANT):
        print(p.text[:250])

d = docx.Document(P5)
print("\n=== FULL p5 reference list ===")
started = False
for p in d.paragraphs:
    t = p.text.strip()
    if t.startswith("14. References"):
        started = True
        continue
    if started and t:
        print(t[:180])
