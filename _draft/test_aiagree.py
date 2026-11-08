# -*- coding: utf-8 -*-
"""Smoke-test ai_agreement.py: two synthetic agent sheets (one near-perfect,
one with a consensus-deviation + single-agent departures)."""
import csv, os, shutil, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder"
TMP = os.path.join("_draft", "_aiagree_tmp")
if os.path.exists(TMP):
    shutil.rmtree(TMP)
os.makedirs(TMP)
shutil.copyfile(os.path.join(SRC, "ai_agreement.py"), os.path.join(TMP, "ai_agreement.py"))
shutil.copyfile(os.path.join(SRC, "SUBSAMPLE_key.csv"), os.path.join(TMP, "SUBSAMPLE_key.csv"))

COLS = ["I", "U", "D", "M", "O", "S", "R", "P"]
rows = list(csv.DictReader(open(os.path.join(TMP, "SUBSAMPLE_key.csv"),
                                newline="", encoding="utf-8-sig")))

FLIP = {"E": "P", "P": "E", "NR": "P"}

def write_agent(name, mutations):
    with open(os.path.join(TMP, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["re_order", "study", "reference", "year", "doi"]
                   + ["B_" + c for c in COLS] + ["notes"])
        for r in rows:
            vals = [r["A_" + c] for c in COLS]
            for (o, dim) in mutations:
                if r["re_order"] == o:
                    vals[COLS.index(dim)] = FLIP[vals[COLS.index(dim)]]
            w.writerow([r["re_order"], r["study"], r["reference"], "", ""]
                       + vals + [""])

# agent1: departs on r1 U and r2 I (agents1&2 BOTH depart identically on r1 I)
write_agent("RETURNED_DeepSeek.csv", [("1", "U"), ("2", "I"), ("3", "M")])
# agent2: consensus deviation on r1 I (same flip direction as agent1? both cross)
# choose mutation to r1 I only -> agent1 also has r1 I -> but r1 I original vs flip:
write_agent("RETURNED_Claude.csv", [("1", "I"), ("4", "R")])

proc = subprocess.run([sys.executable, os.path.join(TMP, "ai_agreement.py"),
                       os.path.join(TMP, "RETURNED_DeepSeek.csv"),
                       os.path.join(TMP, "RETURNED_Claude.csv")],
                      capture_output=True, text=True, encoding="utf-8",
                      errors="replace")
print(proc.stdout[-3000:])
if proc.stderr:
    print("STDERR:", proc.stderr)
print("exit code:", proc.returncode)
for f in ("agent_kappa_results.csv", "AGREEMENT_RESULTS.txt"):
    p = os.path.join(TMP, f)
    print(f, "exists:", os.path.exists(p))
shutil.rmtree(TMP)
print("temp cleaned")
