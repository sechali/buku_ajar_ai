import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=300)

# Data kelompok
groups = ['Petani Korporasi\n(Privileged)', 'Petani Swadaya\n(Unprivileged)']
approval_before = [0.82, 0.46] # Approval rates before mitigation
approval_after = [0.76, 0.70]  # Approval rates after sample reweighting mitigation

# 1. Bar Chart Approval Rate Comparison
x = np.arange(len(groups))
width = 0.35

rects1 = ax1.bar(x - width/2, [v * 100 for v in approval_before], width, label='Sebelum Mitigasi (Model Bias)', color='#d62728', alpha=0.85)
rects2 = ax1.bar(x + width/2, [v * 100 for v in approval_after], width, label='Sesudah Mitigasi (Fair Re-weighting)', color='#2ca02c', alpha=0.85)

ax1.set_ylabel('Tingkat Persetujuan Pinjaman (%)', fontsize=10, fontweight='bold')
ax1.set_title('A. Tingkat Persetujuan Pinjaman Bibit per Kelompok', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(groups, fontsize=10, fontweight='bold')
ax1.set_ylim(0, 100)
ax1.legend(loc='lower left', fontsize=9)

for r in rects1:
    h = r.get_height()
    ax1.text(r.get_x() + r.get_width()/2., h + 1.5, f"{h:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#d62728')
for r in rects2:
    h = r.get_height()
    ax1.text(r.get_x() + r.get_width()/2., h + 1.5, f"{h:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2ca02c')

# 2. Metric Comparison: Disparate Impact Ratio (DIR)
dir_before = approval_before[1] / approval_before[0] # 0.46 / 0.82 = 0.561
dir_after = approval_after[1] / approval_after[0]   # 0.70 / 0.76 = 0.921

bars = ax2.bar(['Sebelum Mitigasi', 'Sesudah Mitigasi'], [dir_before, dir_after], 
               color=['#d62728', '#2ca02c'], width=0.45, alpha=0.85, edgecolor='black', linewidth=1.2)

# Horizontal line at 0.80 (Four-Fifths Rule Threshold)
ax2.axhline(0.80, color='blue', linestyle='--', linewidth=2, label='Ambang Batas Adil (Four-Fifths Rule = 0.80)')
ax2.set_ylabel('Disparate Impact Ratio (DIR)', fontsize=10, fontweight='bold')
ax2.set_title('B. Evaluasi Kepatuhan Hukum Regulasi Keadilan (DIR)', fontsize=11, fontweight='bold')
ax2.set_ylim(0, 1.15)
ax2.legend(loc='upper left', fontsize=9)

for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.03, f"{yval:.3f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

ax2.text(0, dir_before/2, "DISKONFORMITI!\n(Diskriminatif Ilegal)", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
ax2.text(1, dir_after/2, "LOLOS AUDIT!\n(Adil & Patuh Regulasi)", ha='center', va='center', color='white', fontweight='bold', fontsize=9)

plt.suptitle("Audit Keadilan Algoritmik: Dampak Mitigasi Bias Data Historis Pinjaman Mikro Tani", 
             fontsize=12, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\audit_bias_fairness_mitigasi.png", dpi=300, bbox_inches='tight')
plt.close()
print("Fairness audit diagram generated successfully.")
