# -*- coding: utf-8 -*-
"""Delete _noop.txt + smoke-test intra_check.py end-to-end on a synthetic
returned sheet (B = A, perfect stability) in a temp copy."""
import csv, os, shutil, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

if os.path.exists("_draft/_noop.txt"):
    os.remove("_draft/_noop.txt")
    print("removed _noop.txt")

SRC = r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder"
TMP = os.path.join("_draft", "_intra_test_tmp")
if os.path.exists(TMP):
    shutil.rmtree(TMP)
os.makedirs(TMP)

# copy package scripts + key
shutil.copyfile(os.path.join(SRC, "intra_check.py"), os.path.join(TMP, "intra_check.py"))
shutil.copyfile(os.path.join(SRC, "SUBSAMPLE_key.csv"), os.path.join(TMP, "SUBSAMPLE_key.csv"))

# synthetic returned sheet: 15 rows, B_* = A_* from the key (perfect stability)
rows = list(csv.DictReader(open(os.path.join(TMP, "SUBSAMPLE_key.csv"),
                                newline="", encoding="utf-8-sig")))
COLS = ["I", "U", "D", "M", "O", "S", "R", "P"]
with open(os.path.join(TMP, "RETURNED_IntraCoder_ReCode.csv"), "w", newline="",
          encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["re_order", "study", "reference", "year", "doi"]
               + ["B_" + c for c in COLS] + ["notes"])
    for r in rows:
        w.writerow([r["re_order"], r["study"], r["reference"], "", ""]
                   + [r["A_" + c] for c in COLS] + [""])

proc = subprocess.run([sys.executable, os.path.join(TMP, "intra_check.py"),
                       os.path.join(TMP, "RETURNED_IntraCoder_ReCode.csv")],
                      capture_output=True, text=True, encoding="utf-8",
                      errors="replace")
print(proc.stdout)
if proc.stderr:
    print("STDERR:", proc.stderr)
print("exit code:", proc.returncode)

res = os.path.join(TMP, "intra_kappa_results.csv")
print("results file exists:", os.path.exists(res))
if os.path.exists(res):
    for r in csv.DictReader(open(res, encoding="utf-8")):
        print("  ", r)
shutil.rmtree(TMP)
print("temp cleaned")
