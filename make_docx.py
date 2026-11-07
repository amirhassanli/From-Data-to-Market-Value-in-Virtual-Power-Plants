# -*- coding: utf-8 -*-
"""Convert vpp_review_ieee.md to IEEE-styled two-column Word document."""
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = "/home/user/vpp_review_ieee.md"
OUT = "/home/user/vpp_review_ieee.docx"

doc = Document()

# ---------- base styles ----------
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(10)
normal.paragraph_format.space_after = Pt(4)
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.line_spacing = 1.0
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

for i, (sz, bold, italic, align) in {
    1: (11, True, False, WD_ALIGN_PARAGRAPH.CENTER),
    2: (10, True, True, WD_ALIGN_PARAGRAPH.LEFT),
    3: (10, False, True, WD_ALIGN_PARAGRAPH.LEFT),
}.items():
    st = doc.styles[f"Heading {i}"]
    st.font.name = "Times New Roman"; st.font.size = Pt(sz)
    st.font.bold = bold; st.font.italic = italic; st.font.color.rgb = RGBColor(0, 0, 0)
    st.paragraph_format.space_before = Pt(8 if i == 1 else 6)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.alignment = align

sec0 = doc.sections[0]
sec0.top_margin = Inches(0.7); sec0.bottom_margin = Inches(0.7)
sec0.left_margin = Inches(0.7); sec0.right_margin = Inches(0.7)

# header / footer
hdr = sec0.header.paragraphs[0]
hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = hdr.add_run("Author et al.: From Data to Market Value in Virtual Power Plants")
r.font.size = Pt(8); r.font.italic = True; r.font.name = "Times New Roman"
ftr = sec0.footer.paragraphs[0]
ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE")
run = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = "1"
rPr = OxmlElement("w:rPr"); sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "16")
rPr.append(sz); run.append(rPr); run.append(t); fld.append(run)
ftr._p.append(fld)

def set_cols(section, num):
    sectPr = section._sectPr
    cols = sectPr.find(qn("w:cols"))
    if cols is None:
        cols = OxmlElement("w:cols"); sectPr.append(cols)
    cols.set(qn("w:num"), str(num)); cols.set(qn("w:space"), "720")

def add_runs(par, text, base_size=10, base_bold=False, base_italic=False):
    """Parse **bold**, *italic*, `code` into runs."""
    token = re.split(r"(\*\*.+?\*\*|\*[^*]+?\*|`.+?`)", text)
    for tok in token:
        if not tok:
            continue
        b, it = base_bold, base_italic
        if tok.startswith("**") and tok.endswith("**"):
            b, tok = True, tok[2:-2]
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            it, tok = True, tok[1:-1]
        elif tok.startswith("`") and tok.endswith("`"):
            tok = tok[1:-1]
        run = par.add_run(tok)
        run.font.name = "Times New Roman"; run.font.size = Pt(base_size)
        run.font.bold = b; run.font.italic = it

def add_table(rows):
    header, body = rows[0], rows[1:]
    t = doc.add_table(rows=1 + len(body), cols=len(header))
    t.style = "Table Grid"
    t.autofit = True
    for j, h in enumerate(header):
        cell = t.cell(0, j)
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h); run.font.size = Pt(7.5); run.font.bold = True
        run.font.name = "Times New Roman"
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "D9D9D9"); shd.set(qn("w:val"), "clear")
        cell._tc.get_or_add_tcPr().append(shd)
    for i, row in enumerate(body, start=1):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(val); run.font.size = Pt(7.5)
            run.font.name = "Times New Roman"
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def insert_figure(img, caption):
    doc.add_section(WD_SECTION.CONTINUOUS)
    set_cols(doc.sections[-1], 1)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(img, width=Inches(6.4))
    cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(6)
    add_runs(cap, caption, base_size=8)
    doc.add_section(WD_SECTION.CONTINUOUS)
    set_cols(doc.sections[-1], 2)

with open(SRC, encoding="utf-8") as f:
    lines = f.read().splitlines()

body_started = False
refs_mode = False
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    if not line.strip():
        i += 1; continue
    if line.strip() == "---":
        if not body_started:
            doc.add_section(WD_SECTION.CONTINUOUS)
            set_cols(doc.sections[-1], 2)
            body_started = True
        i += 1; continue
    if line.startswith("# "):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(line[2:]); run.font.size = Pt(20); run.font.bold = True
        run.font.name = "Times New Roman"
        i += 1; continue
    if line.startswith("## "):
        title = line[3:].strip()
        refs_mode = (title.upper() == "REFERENCES")
        doc.add_heading(title, level=1)
        i += 1; continue
    if line.startswith("### "):
        doc.add_heading(line[4:].strip(), level=2)
        i += 1; continue
    if line.startswith("**TABLE"):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
        add_runs(p, line.strip(), base_size=8)
        # collect table rows (skip blank lines first)
        rows = []
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        while i < len(lines) and lines[i].strip().startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                i += 1; continue
            rows.append(cells)
            i += 1
        add_table(rows)
        continue
    if line.startswith("> "):
        txt = line[2:].strip()
        if "fig1_prisma.png" in txt:
            m = re.search(r"\*\*(Fig\. 1.+?)\*\*", txt)
            insert_figure("/home/user/fig1_prisma.png", m.group(1) if m else "Fig. 1.")
        elif "fig2_pipeline.png" in txt:
            m = re.search(r"\*\*(Fig\. 2.+?)\*\*", txt)
            insert_figure("/home/user/fig2_pipeline.png", m.group(1) if m else "Fig. 2.")
        else:
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_runs(p, txt, base_size=9, base_italic=True)
        i += 1; continue
    if line.startswith("**Author"):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_runs(p, line.strip(), base_size=11)
        i += 1; continue
    if line.startswith("*Department"):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_runs(p, line.strip(), base_size=9)
        i += 1; continue
    if line.startswith("**Abstract"):
        p = doc.add_paragraph()
        m = re.match(r"\*\*(Abstract—)\*\*\s*(.*)", line.strip())
        r1 = p.add_run(m.group(1) + " "); r1.bold = True; r1.font.size = Pt(9)
        r1.font.name = "Times New Roman"
        r2 = p.add_run(m.group(2)); r2.italic = True; r2.font.size = Pt(9)
        r2.font.name = "Times New Roman"
        i += 1; continue
    if line.startswith("**Index Terms"):
        p = doc.add_paragraph()
        m = re.match(r"\*\*(Index Terms—)\*\*\s*(.*)", line.strip())
        r1 = p.add_run(m.group(1) + " "); r1.bold = True; r1.font.size = Pt(9)
        r1.font.name = "Times New Roman"
        r2 = p.add_run(m.group(2)); r2.italic = True; r2.font.size = Pt(9)
        r2.font.name = "Times New Roman"
        i += 1; continue
    if line.startswith("- "):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_runs(p, line[2:].strip(), base_size=10)
        # fix bullet font
        for run in p.runs:
            run.font.name = "Times New Roman"
        i += 1; continue
    if re.match(r"^\d+\.\s", line.strip()):
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_runs(p, re.sub(r"^\d+\.\s", "", line.strip()), base_size=10)
        for run in p.runs:
            run.font.name = "Times New Roman"
        i += 1; continue
    # regular paragraph
    p = doc.add_paragraph()
    if refs_mode:
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        add_runs(p, line.strip(), base_size=8)
    else:
        add_runs(p, line.strip(), base_size=10)
    i += 1

doc.save(OUT)
print("saved", OUT)

# verify
from docx import Document as D2
d = D2(OUT)
print("paragraphs:", len(d.paragraphs), "| tables:", len(d.tables),
      "| sections:", len(d.sections),
      "| images:", len(d.inline_shapes))
