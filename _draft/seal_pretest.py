# -*- coding: utf-8 -*-
"""Seal the pre-retest state: SHA-256 of the master matrix + key, dated."""
import hashlib, io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

items = [("_draft/dmdi_coding_matrix.csv", "master DMDI coding matrix (A_ ratings)"),
         (r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder\SUBSAMPLE_key.csv",
          "subsample key (coder A original ratings, sealed until retest returned)"),
         (r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder\IntraCoder_ReCode_SHEET.csv",
          "coder-facing retest sheet (B_ columns empty at freeze)"),
         ("_draft/build_codebook_docx.py", "codebook builder (rules unchanged)")]
out = ["SEAL — pre-retest state, frozen 2026-11-03 (protocol seed 20261103)", ""]
for p, label in items:
    out.append("%s  %s  (%s)" % (sha(p), os.path.basename(p), label))
txt = "\n".join(out) + "\n"
path = r"C:\Users\Mahboobian\Downloads\DMDI_IntraCoder\SEAL_pre_retest.txt"
with open(path, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt)
print("written:", path)
