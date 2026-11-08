# -*- coding: utf-8 -*-
"""Follow-up c: clear the residual duplicated fragments + pending token fixes."""
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


# --- layers paragraph: residual duplicate after partial collapse
edit_text(doc.paragraphs,
          "Thisprofitable under the two-settlement market design itself "
          "\u2014 i.e., whether the attacker\u2019s objective is stated directly in "
          "market currency rather than in generic system-cost terms [50]. This reframing",
          "This reframing", "layers residual dup")

# --- distributed-opt paragraph: residual duplicate
edit_text(doc.paragraphs,
          "let largeBenders decomposition [54] let large",
          "let large", "distopt residual dup")

# --- 8.3 two-step spot-market: Mei [52]
edit_text(doc.paragraphs, "two-step spot-market formulations [78]",
          "two-step spot-market formulations [52]", "emptygap Mei")

# --- blockchain paragraph: Andoni [49]
edit_text(doc.paragraphs, "ex-post verification cheap [48]",
          "ex-post verification cheap [49]", "blockchain Andoni")

# --- DT/FedAvg paragraph: Tao [48], McMahan [50]
edit_text(doc.paragraphs, "simulated attack or drift [47]",
          "simulated attack or drift [48]", "DT Tao")
edit_text(doc.paragraphs, "federated learning [49] allows",
          "federated learning [50] allows", "FedAvg McMahan")

# --- carbon-coding intro: fenrg Y.Wang [34]
edit_text(doc.paragraphs, "DMDI-coded core plus [33],",
          "DMDI-coded core plus [34],", "carbon coding set intro")

doc.save(P5)
print("applied:", APPLIED)
