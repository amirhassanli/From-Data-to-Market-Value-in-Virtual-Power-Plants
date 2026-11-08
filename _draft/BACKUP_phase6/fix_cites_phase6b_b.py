# -*- coding: utf-8 -*-
"""Follow-up: two patterns that failed in fix_cites_phase6b (separator variants)."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import docx

P5 = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
      r"Plants (revised 2026-10-27) - PHASE5.docx")
doc = docx.Document(P5)
APPLIED = []


def edit_text(units, old, new, tag):
    for holder in units:
        if isinstance(holder, docx.table._Cell):
            paras = holder.paragraphs
        else:
            paras = [holder]
        for p in paras:
            runs = p.runs
            if not runs:
                continue
            text = "".join(r.text for r in runs)
            if old not in text:
                continue
            i = text.find(old)
            pos = 0
            for run in runs:
                if pos <= i < pos + len(run.text):
                    lo = i - pos
                    run.text = run.text[:lo] + new + run.text[lo + len(old):]
                    APPLIED.append(tag)
                    return True
                pos += len(run.text)
    return False


# Nash/Shapley sentence: em-dash before "support"
edit_text(doc.paragraphs,
          "Nash equilibrium analysis [55] and Shapley-value surplus sharing [56] \u2014 support",
          "Nash equilibrium analysis [57] and Shapley-value surplus sharing [58] \u2014 support",
          "layers games")

# cell 4 r6 c3 (Model and parameter error): semicolon-separated pair
c = doc.tables[4].rows[6].cells[3]
edit_text([c], "ambiguity sets [44]", "ambiguity sets [45]", "cell 4 r6 c3 [44]->45")
edit_text([c], "satisficing [58]", "satisficing [60]", "cell 4 r6 c3 [58]->60")

doc.save(P5)
print("applied:", APPLIED)
