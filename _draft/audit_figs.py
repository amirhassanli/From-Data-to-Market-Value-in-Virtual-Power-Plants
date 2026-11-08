# -*- coding: utf-8 -*-
"""Figure audit: embedded resolution, display size, effective dpi, colours."""
import sys, io, os, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from docx import Document
from docx.shared import Emu

P = (r"C:\Users\Mahboobian\Downloads\From Data to Market Value in Virtual Power "
     r"Plants (revised 2026-10-27) - PHASE3.docx")
d = Document(P)
DRAW = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"

try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

z = zipfile.ZipFile(P)
media = [n for n in z.namelist() if n.startswith("word/media/")]

# map rIds to filenames
rels = d.part.rels
rid2file = {}
for rid, rel in rels.items():
    if "image" in rel.reltype:
        rid2file[rid] = os.path.basename(rel.target_ref)

print("media files: %d   image relationships: %d" % (len(media), len(rid2file)))

rows = []
for i, shape in enumerate(d.inline_shapes):
    ext = shape._inline.find(".//" + WP + "extent")
    cx, cy = int(ext.get("cx")), int(ext.get("cy"))
    blip = shape._inline.find(".//" + DRAW + "blip")
    rid = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
    fn = rid2file.get(rid, "?")
    px = None
    if HAVE_PIL and fn in [os.path.basename(x) for x in media]:
        path = [x for x in media if os.path.basename(x) == fn][0]
        data = z.read(path)
        import io as _io
        im = Image.open(_io.BytesIO(data))
        px = im.size
    w_in, h_in = cx / 914400.0, cy / 914400.0
    dpi = (px[0] / w_in, px[1] / h_in) if px else (None, None)
    rows.append((i + 1, fn, w_in, h_in, px, dpi))
    print("\nFigure %d  %s" % (i + 1, fn))
    print("   display %.2f x %.2f in" % (w_in, h_in))
    if px:
        print("   pixels  %d x %d" % px)
        print("   effective dpi %.0f x %.0f" % dpi)
        if min(dpi) < 300:
            print("   WARNING: below 300 dpi")
    if w_in > 6.5 or h_in > 9.0:
        print("   WARNING: larger than the text area")

print("\n=== figures wider than the 6.5 in text column ===")
print([r[0] for r in rows if r[2] > 6.5] or "none")

print("\n=== file sizes ===")
for n in sorted(media):
    print("  %-28s %8.1f KB" % (n, len(z.read(n)) / 1024.0))
