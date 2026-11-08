# -*- coding: utf-8 -*-
import shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
src = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
       r"Plants (revised 2026-10-27) - PHASE5.docx")
dst = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
       r"Plants (FINAL).docx")
shutil.copyfile(src, dst)
print("copied ->", dst)
