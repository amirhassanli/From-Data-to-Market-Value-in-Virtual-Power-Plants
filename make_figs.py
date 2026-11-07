import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({"font.family": "serif", "font.size": 9})

# ---------------- Fig 1: PRISMA flow ----------------
fig, ax = plt.subplots(figsize=(7.2, 3.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")

stages = [
    ("IDENTIFICATION", "Records identified\n(n = 1,847)\nIEEE Xplore · Scopus · WoS\nACM DL · ScienceDirect", "#1f4e79"),
    ("SCREENING", "After deduplication\n(n = 1,204)\n892 excluded\n(title / abstract)", "#2e75b6"),
    ("ELIGIBILITY", "Full-text assessed\n(n = 312)\n168 excluded\n(scope · detail · duplicates)", "#548235"),
    ("INCLUDED", "Final corpus\n(n = 156)\n+ 12 snowballed\nlandmarks", "#bf5700"),
]
x0, w, h, gap = 0.25, 2.1, 3.4, 0.28
for i, (head, body, col) in enumerate(stages):
    x = x0 + i * (w + gap)
    y = 0.8
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                         facecolor="white", edgecolor=col, linewidth=1.6)
    ax.add_patch(box)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.62), w, 0.62,
                 boxstyle="round,pad=0.02", facecolor=col, edgecolor=col))
    ax.text(x + w/2, y + h - 0.31, head, ha="center", va="center",
            fontsize=8, fontweight="bold", color="white")
    ax.text(x + w/2, y + (h - 0.62)/2, body, ha="center", va="center",
            fontsize=7.5, color="#222222", linespacing=1.35)
    if i < 3:
        ax.add_patch(FancyArrowPatch((x + w + 0.02, y + h/2),
                     (x + w + gap - 0.02, y + h/2),
                     arrowstyle="-|>", mutation_scale=12,
                     color="#404040", linewidth=1.2))
ax.text(5, 4.65, "PRISMA 2020 Flow — Study Identification, Screening, and Inclusion",
        ha="center", fontsize=10, fontweight="bold")
fig.tight_layout()
fig.savefig("/home/user/fig1_prisma.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# ---------------- Fig 2: pipeline ----------------
fig, ax = plt.subplots(figsize=(7.4, 3.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off")

steps = [
    ("1. SENSE &\nTELEMETRY", "meters · weather\nSoC · prices", "#1f4e79"),
    ("2. FORECAST", "point &\nprobabilistic", "#2e75b6"),
    ("3. OPTIMIZE\n& BID", "SP · RO · DRO\nRL bidding", "#385723"),
    ("4. CLEAR &\nDISPATCH", "DA · ID · RT\nreserves", "#7b4b00"),
    ("5. SETTLE &\nLEARN", "revenue share\nmodel update", "#843c0c"),
]
x0, w, h, gap = 0.15, 1.72, 2.0, 0.22
yc = 1.55
for i, (head, body, col) in enumerate(steps):
    x = x0 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, yc), w, h, boxstyle="round,pad=0.05",
                 facecolor=col, edgecolor="#222222", linewidth=1.0))
    ax.text(x + w/2, yc + h - 0.45, head, ha="center", va="center",
            fontsize=7.5, fontweight="bold", color="white", linespacing=1.2)
    ax.add_patch(plt.Rectangle((x + 0.08, yc + 0.12), w - 0.16, 0.85,
                 facecolor="white", edgecolor="none", alpha=0.94))
    ax.text(x + w/2, yc + 0.55, body, ha="center", va="center",
            fontsize=7, color="#222222", linespacing=1.25)
    if i < 4:
        ax.add_patch(FancyArrowPatch((x + w + 0.02, yc + h/2),
                     (x + w + gap - 0.02, yc + h/2),
                     arrowstyle="-|>", mutation_scale=12,
                     color="#404040", linewidth=1.2))
# carbon band
ax.add_patch(FancyBboxPatch((0.15, yc + h + 0.18), 5*w + 4*gap, 0.42,
             boxstyle="round,pad=0.03", facecolor="#d9ead3",
             edgecolor="#385723", linewidth=1.0, linestyle=(0, (4, 2))))
ax.text(5, yc + h + 0.39, "Carbon-accounting band: emission-flow attribution  ·  allowance settlement  ·  MRV",
        ha="center", va="center", fontsize=7.5, style="italic", color="#274e13")
# integrity shield base
ax.add_patch(FancyBboxPatch((0.15, 0.22), 5*w + 4*gap, 1.0,
             boxstyle="round,pad=0.05", facecolor="#ddebf7",
             edgecolor="#1f4e79", linewidth=1.2))
ax.text(5, 0.99, "Decision-integrity shield (L1–L4)", ha="center", fontsize=8.5,
        fontweight="bold", color="#1f4e79")
ax.text(5, 0.68, "data validation · FDI detection   |   calibration · XAI audits · digital-twin stress tests",
        ha="center", fontsize=6.4, color="#333333")
ax.text(5, 0.42, "feasibility checks · monitored settlement   |   privacy · reproducibility · audit trails",
        ha="center", fontsize=6.4, color="#333333")
ax.text(5, 4.35, "The VPP Data-to-Market-Value Pipeline", ha="center",
        fontsize=10, fontweight="bold")
fig.tight_layout()
fig.savefig("/home/user/fig2_pipeline.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Figures saved.")
