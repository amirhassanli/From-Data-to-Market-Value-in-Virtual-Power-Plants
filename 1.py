import matplotlib.pyplot as plt
import matplotlib.patches as patches

# تنظیمات اولیه
fig, ax = plt.subplots(figsize=(8, 6.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')  # حذف محورها

# اطلاعات جعبه‌ها (متن، مختصات، رنگ حاشیه، رنگ پس‌زمینه)
boxes = [
    {"title": "Predictive validity", "desc": "OOS forecast error, calibration, dependence", "y": 6.8, "edge": "#1f4e79", "face": "#e6f0fa"},
    {"title": "Decision validity", "desc": "Schedule-execution match, constraint feasibility", "y": 5.5, "edge": "#245f94", "face": "#d9e8f5"},
    {"title": "Market validity", "desc": "Gate closure, bid format, market sequence", "y": 4.2, "edge": "#2a70af", "face": "#cce0f0"},
    {"title": "Settlement validity", "desc": "Deviation, imbalance, penalties/revenues", "y": 2.9, "edge": "#2f81ca", "face": "#bfd8eb"},
    {"title": "Deployment validity", "desc": "Latency, reproducibility, pilot/operational evidence", "y": 1.6, "edge": "#3592e5", "face": "#b2d0e6"}
]

# رسم جعبه‌ها و متن‌ها
for box in boxes:
    # رسم مستطیل
    rect = patches.FancyBboxPatch((1.5, box["y"]), 7.0, 0.9,
                                   boxstyle="round,pad=0.05,rounding_size=0.1",
                                   edgecolor=box["edge"], facecolor=box["face"], linewidth=1.5)
    ax.add_patch(rect)
    
    # متن عنوان
    ax.text(5.0, box["y"] + 0.65, box["title"], ha='center', va='center', 
            fontsize=12, fontweight='bold', fontfamily='sans-serif', color='#111111')
    
    # متن توضیحات
    ax.text(5.0, box["y"] + 0.3, box["desc"], ha='center', va='center', 
            fontsize=9, fontfamily='sans-serif', color='#333333')

# رسم فلش‌ها بین جعبه‌ها
for i in range(len(boxes) - 1):
    y_start = boxes[i]["y"] - 0.05
    y_end = boxes[i+1]["y"] + 0.95
    ax.annotate('', xy=(5.0, y_end), xytext=(5.0, y_start),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5, mutation_scale=15))

# ذخیره تصویر با فرمت JPG
plt.tight_layout()
plt.savefig('IEEE_Validation_Stack.jpg', format='jpg', dpi=300, bbox_inches='tight')
plt.show()
print("تصویر با نام IEEE_Validation_Stack.jpg ذخیره شد.")