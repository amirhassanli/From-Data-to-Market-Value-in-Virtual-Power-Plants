# -*- coding: utf-8 -*-
"""Writing-tone and spelling audit."""
import re
import sys
import io
import collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import docx

P = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
     r"Plants (revised 2026-10-27) - PHASE5.docx")
d = docx.Document(P)
paras = d.paragraphs
idx_refs = next(i for i, p in enumerate(paras) if p.text.strip().startswith("14. References"))

body_ps = [p.text for p in paras[:idx_refs] if p.style.name in
           ("Body Text", "First Paragraph", "Compact")]

text = "\n".join(body_ps)
low = text.lower()

print("=== AI-flavoured / filler phrases ===")
TELLS = ["delve", "crucial", "pivotal", "moreover", "furthermore", "it is worth noting",
         "it should be noted", "in conclusion", "tapestry", "realm", "navigate",
         "underscore", "holistic", "seamless", "cutting-edge", "paradigm shift",
         "plays a vital role", "serves as a", "testament to", "in today's",
         "ever-evolving", "game-changer", "leverage the", "robustly", "significantly",
         "not only", "a myriad", "furthermore", "additionally,", "in summary",
         "importantly,", "notably,", "arguably", "it is important to"]
for w in TELLS:
    c = low.count(w)
    if c:
        print("  %-22s %d" % (w, c))

print("\n=== sentence statistics ===")
sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 25]
lens = [len(re.findall(r"[A-Za-z0-9][\w'\u2019\-]*", s)) for s in sents]
if lens:
    lens_sorted = sorted(lens)
    print("  sentences: %d" % len(lens))
    print("  mean words/sentence: %.1f" % (sum(lens) / len(lens)))
    print("  median: %d   p90: %d   max: %d" % (
        lens_sorted[len(lens) // 2], lens_sorted[int(len(lens) * 0.9)], max(lens)))
    over = [(n, s) for n, s in zip(lens, sents) if n > 60]
    print("  sentences over 60 words: %d" % len(over))
    for n, s in over[:6]:
        print("     %3d  %s" % (n, s[:120]))

print("\n=== punctuation habits ===")
print("  em dashes: %d   en dashes: %d   semicolons: %d   parentheses: %d"
      % (text.count("\u2014"), text.count("\u2013"), text.count(";"), text.count("(")))

print("\n=== spelling variants (US vs UK) ===")
PAIRS = [("modeling", "modelling"), ("optimization", "optimisation"),
         ("behavior", "behaviour"), ("organization", "organisation"),
         ("centralized", "centralised"), ("analyze", "analyse"),
         ("defense", "defence"), ("program", "programme"), ("center", "centre"),
         ("favor", "favour"), ("license", "licence"), ("utilization", "utilisation"),
         ("normalized", "normalised"), ("summarize", "summarise")]
for us, uk in PAIRS:
    cu, ck = low.count(us), low.count(uk)
    flag = "  <-- MIXED" if cu and ck else ""
    if cu or ck:
        print("  %-14s %3d   %-14s %3d%s" % (us, cu, uk, ck, flag))

print("\n=== hedging density ===")
for w in ("may ", "might ", "could ", "suggest", "appear", "likely", "we read",
          "in our reading", "in our assessment", "should be read"):
    print("  %-16s %d" % (w, low.count(w)))

print("\n=== first person ===")
print("  'we'/'our' occurrences: %d / %d" % (len(re.findall(r"\bwe\b", low)),
                                              len(re.findall(r"\bour\b", low))))
print("  passive 'is/are reported': %d" % len(re.findall(r"\b(is|are)\s+\w+ed\b", low)))

print("\n=== repeated openers (paragraph first three words) ===")
openers = collections.Counter(" ".join(p.split()[:3]) for p in body_ps if len(p.split()) > 3)
for o, c in openers.most_common(8):
    if c > 2:
        print("  %2d  %s" % (c, o))

print("\n=== word frequency (content words) ===")
stop = set("""the a an of to and in for on with is are was were that this these those it its as at by
from be been being we our not no but or if then than which who whom whose what when where how all any
each other such more most less least can could may might must should would will shall do does did
into over under about across between within without toward towards during because while although""".split())
words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z\-]{3,}", text)]
freq = collections.Counter(w for w in words if w not in stop)
for w, c in freq.most_common(25):
    print("  %4d  %s" % (c, w))
