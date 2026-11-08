# -*- coding: utf-8 -*-
"""Extend the backup chain: BACKUP_phase6 (citations/renumber/supplementary era)."""
import os, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DEST = "_draft/BACKUP_phase6"
os.makedirs(DEST, exist_ok=True)
KEEP = [
    # fix scripts of this era
    "build_phase6.py", "fix_cites_phase6b.py", "fix_cites_phase6b_b.py",
    "fix_cites_phase6b_c.py", "fix_cites_phase6b_d.py", "fix_hidden_cells.py",
    "fix_hidden_cells2.py", "fix_tblx_num.py", "fix_semantic_cites.py",
    "fix_italics.py", "fix_refs_heading.py",
    # renumber engine + maps
    "renumber_phase6c.py",
    "renum_p5_to_p6.json", "renum_p5_to_p6_v1.json", "renum_mid1_to_mid2.json",
    "renum_p6_to_p5.json",
    # remap chain
    "finalize_nummaps.py", "check_os_levels.py", "check_singh.py", "bridge35.py",
    # audits + dumps
    "audit_cites.py", "audit_refs.py", "audit_refstyle.py", "audit_final.py",
    "audit_tone.py", "audit_figs.py", "diff3_5b.py", "dump5.py", "xcheck.py",
    "phase5_full.txt", "check_final_refs.py", "check_italics.py",
    # data + supplementary builders
    "dmdi_coding_matrix.csv", "dmdi_coding_long.csv",
    "dmdi_second_coder_sheet.csv", "dmdi_second_coder_BLIND.csv",
    "study_to_phase5.json", "phase2_stats.py",
    "build_supp_package.py", "build_codebook_docx.py", "kappa_agreement.py",
    "merge_second_coder.py", "copy_final.py",
    # intra-coder (test-retest) setup
    "intra_select.py", "test_intra.py", "seal_pretest.py",
    # docs
    "PHASE3_CHANGELOG.md", "PHASE4_CHANGELOG.md",
]
n = 0
for f in KEEP:
    src = os.path.join("_draft", f)
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(DEST, f)); n += 1
    else:
        print("  (missing, skipped):", f)

DL = r"C:\Users\Mahboobian\Downloads"
for f in os.listdir(DL):
    if f.endswith("PHASE5.docx"):
        shutil.copyfile(os.path.join(DL, f), os.path.join(DEST, f)); n += 1

# copy changelogs + remapped CSVs to Downloads
OUT = os.path.join(DL, "DMDI_exports")
os.makedirs(OUT, exist_ok=True)
EXPORTS = ["PHASE3_CHANGELOG.md", "PHASE4_CHANGELOG.md", "PHASE5_CHANGELOG.md",
           "dmdi_coding_matrix.csv", "dmdi_coding_long.csv",
           "dmdi_second_coder_sheet.csv", "dmdi_second_coder_BLIND.csv",
           "study_to_phase5.json", "phase2_stats.py"]
for f in EXPORTS:
    src = os.path.join("_draft", f)
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(OUT, f)); n += 1
        print("exported:", f)

print("backed up/exported %d files -> %s | %s" % (n, DEST, OUT))
