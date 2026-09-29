import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig_dir = r"e:\Project Buku\docs\assets"
art_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"

# ==============================================================================
# FIGURE 1: Anatomi Decision Tree dan Partisi Ruang Fitur
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Skema Arsitektur Pohon Keputusan Sortasi TBS
ax1.axis('off')
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)

# Root node
bbox_root = dict(boxstyle='round,pad=0.5', facecolor='#bbdefb', edgecolor='#1976d2', linewidth=2)
ax1.text(5.0, 9.0, 'Simpul Akar (Root Node)\nPersentase Brondolan $\\leq 12.5\\%$ ?\n(Gini = 0.48, n = 200)',
         ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=bbox_root)

# Edges from root
ax1.annotate('', xy=(2.5, 6.8), xytext=(4.2, 8.3), arrowprops=dict(arrowstyle="->", color='#1976d2', lw=2))
ax1.annotate('', xy=(7.5, 6.8), xytext=(5.8, 8.3), arrowprops=dict(arrowstyle="->", color='#1976d2', lw=2))
ax1.text(3.1, 7.8, 'Benar (Ya)', color='#d62728', fontweight='bold', fontsize=9)
ax1.text(6.8, 7.8, 'Salah (Tidak)', color='#2ca02c', fontweight='bold', fontsize=9)

# Internal nodes
bbox_int1 = dict(boxstyle='round,pad=0.4', facecolor='#fff9c4', edgecolor='#fbc02d', linewidth=1.8)
ax1.text(2.5, 6.0, 'Simpul Cabang 1\nKadar FFA $\\leq 3.2\\%$ ?\n(n = 90)', ha='center', va='center', fontsize=9, fontweight='bold', bbox=bbox_int1)

bbox_int2 = dict(boxstyle='round,pad=0.4', facecolor='#fff9c4', edgecolor='#fbc02d', linewidth=1.8)
ax1.text(7.5, 6.0, 'Simpul Cabang 2\nBerat Tandan $\\leq 14.0$ kg ?\n(n = 110)', ha='center', va='center', fontsize=9, fontweight='bold', bbox=bbox_int2)

# Edges to leaves
ax1.annotate('', xy=(1.2, 3.5), xytext=(2.0, 5.2), arrowprops=dict(arrowstyle="->", color='#7f7f7f', lw=1.5))
ax1.annotate('', xy=(3.8, 3.5), xytext=(3.0, 5.2), arrowprops=dict(arrowstyle="->", color='#7f7f7f', lw=1.5))
ax1.annotate('', xy=(6.2, 3.5), xytext=(7.0, 5.2), arrowprops=dict(arrowstyle="->", color='#7f7f7f', lw=1.5))
ax1.annotate('', xy=(8.8, 3.5), xytext=(8.0, 5.2), arrowprops=dict(arrowstyle="->", color='#7f7f7f', lw=1.5))

# Leaf nodes
bbox_leaf_bad = dict(boxstyle='round,pad=0.4', facecolor='#ffcdd2', edgecolor='#d32f2f', linewidth=2)
bbox_leaf_good = dict(boxstyle='round,pad=0.4', facecolor='#c8e6c9', edgecolor='#388e3c', linewidth=2)
bbox_leaf_warn = dict(boxstyle='round,pad=0.4', facecolor='#ffe0b2', edgecolor='#f57c00', linewidth=2)

ax1.text(1.2, 2.7, 'Daun (Leaf 1)\nFRAKSI MENTAH\n(n=70, Gini=0.0)\n[REJECT SORTASI]', ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_leaf_bad)
ax1.text(3.8, 2.7, 'Daun (Leaf 2)\nKURANG MATANG\n(n=20, Gini=0.15)\n[DOWNGRADE MUTU]', ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_leaf_warn)
ax1.text(6.2, 2.7, 'Daun (Leaf 3)\nMATANG STANDAR\n(n=35, Gini=0.10)\n[OLAH REGULER]', ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_leaf_good)
ax1.text(8.8, 2.7, 'Daun (Leaf 4)\nMATANG PRIMA\n(n=75, Gini=0.0)\n[CPO PREMIUM EKSPOR]', ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_leaf_good)

ax1.text(5.0, 0.8, 'Struktur Hirarki Pohon Keputusan: Keputusan Berbasis Aturan Logis Eksplisit (White-Box)',
         ha='center', va='center', fontsize=10, fontstyle='italic', color='#333333')
ax1.set_title('A. Arsitektur Pohon Keputusan (Decision Tree Structure)\nLogika Kondisional Berjenjang Pemilahan Fraksi TBS Sawit', fontsize=12, fontweight='bold', pad=12)

# Panel 2: Partisi Ruang Fitur Ortogonal 2D (Axis-Aligned Partitioning)
np.random.seed(42)
n_pts = 120
brondol = np.random.uniform(2, 35, n_pts)
ffa_val = np.random.uniform(1.0, 6.0, n_pts)

# Decision boundaries:
# Split 1: Brondolan = 12.5%
# Split 2: Jika Brondolan <= 12.5: FFA = 3.2%
# Split 3: Jika Brondolan > 12.5: FFA = 2.5%
classes = []
for b, f in zip(brondol, ffa_val):
    if b <= 12.5:
        if f > 3.2:
            classes.append(0) # Mentah Rusak
        else:
            classes.append(1) # Kurang Matang
    else:
        if f <= 2.5:
            classes.append(3) # Matang Prima
        else:
            classes.append(2) # Matang Standar
classes = np.array(classes)

# Draw partitions (colored boxes)
# Region 1: Brondolan <= 12.5, FFA > 3.2 (Mentah)
ax2.fill_between([2, 12.5], 3.2, 6.0, color='#ffcdd2', alpha=0.45, label='Zona 1: Fraksi Mentah')
# Region 2: Brondolan <= 12.5, FFA <= 3.2 (Kurang Matang)
ax2.fill_between([2, 12.5], 1.0, 3.2, color='#ffe0b2', alpha=0.45, label='Zona 2: Kurang Matang')
# Region 3: Brondolan > 12.5, FFA > 2.5 (Matang Standar)
ax2.fill_between([12.5, 35], 2.5, 6.0, color='#fff9c4', alpha=0.45, label='Zona 3: Matang Standar')
# Region 4: Brondolan > 12.5, FFA <= 2.5 (Matang Prima)
ax2.fill_between([12.5, 35], 1.0, 2.5, color='#c8e6c9', alpha=0.45, label='Zona 4: Matang Prima')

# Draw split boundary lines
ax2.axvline(12.5, color='#1976d2', linewidth=2.5, linestyle='-', label='Pemisahan 1: Brondolan = 12.5%')
ax2.plot([2, 12.5], [3.2, 3.2], color='#d32f2f', linewidth=2.0, linestyle='--', label='Pemisahan 2: FFA = 3.2%')
ax2.plot([12.5, 35], [2.5, 2.5], color='#388e3c', linewidth=2.0, linestyle='--', label='Pemisahan 3: FFA = 2.5%')

# Scatter points
colors = ['#d32f2f', '#f57c00', '#fbc02d', '#388e3c']
markers = ['x', 's', '^', 'o']
labels_map = ['Mentah', 'Kurang Matang', 'Standar', 'Prima']

for c_idx in range(4):
    mask = (classes == c_idx)
    ax2.scatter(brondol[mask], ffa_val[mask], color=colors[c_idx], marker=markers[c_idx], s=55, edgecolors='k', alpha=0.9)

ax2.set_title('B. Partisi Ruang Fitur Ortogonal 2D (Axis-Aligned Split)\nPembagian Wilayah Keputusan Menjadi Hiper-Persegi Terisolasi', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Persentase Brondolan Lepas dari Tandan (%)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Kadar Asam Lemak Bebas / FFA (% Bobot)', fontsize=11, fontweight='bold')
ax2.set_xlim(2, 35)
ax2.set_ylim(1.0, 6.0)
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "anatomi_decision_tree_dan_partisi_ruang_fitur.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "anatomi_decision_tree_dan_partisi_ruang_fitur.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Kurva Ketidakmurnian dan Pruning Decision Tree
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Perbandingan Metrik Ketidakmurnian (Gini vs Entropy vs Misclassification)
p_vals = np.linspace(0.0001, 0.9999, 300)
entropy = -(p_vals * np.log2(p_vals) + (1 - p_vals) * np.log2(1 - p_vals))
gini = 2 * p_vals * (1 - p_vals)
misclass = 1 - np.maximum(p_vals, 1 - p_vals)

# Scale entropy by 0.5 to compare shapes directly
ax1.plot(p_vals, entropy * 0.5, color='#d62728', linewidth=2.8, label=r'Entropi Shannon Terstandar: $\frac{1}{2} H(p)$')
ax1.plot(p_vals, gini, color='#1f77b4', linewidth=2.8, linestyle='--', label=r'Ketidakmurnian Gini: $2p(1-p)$')
ax1.plot(p_vals, misclass, color='#2ca02c', linewidth=2.2, linestyle=':', label=r'Galat Miskalsifikasi: $1 - \max(p, 1-p)$')

ax1.scatter([0.5], [0.5], color='black', s=80, zorder=5)
ax1.annotate('Puncak Ketidakmurnian\n$p = 0.5$ (Distribusi Acak 50:50)', xy=(0.5, 0.5), xytext=(0.28, 0.60),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))

ax1.scatter([0.0, 1.0], [0.0, 0.0], color='#2ca02c', s=80, zorder=5)
ax1.annotate('Simpul Murni (Pure Node)\nKetidakmurnian = 0', xy=(1.0, 0.0), xytext=(0.70, 0.15),
             arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2ca02c'))

ax1.set_title('A. Perbandingan Metrik Ketidakmurnian Simpul (Node Impurity)\nKarakteristik Kurva Cembung Simetris Menuju Titik Murni', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Probabilitas Kelas Positif ($p$)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Nilai Ketidakmurnian / Impurity Score', fontsize=11, fontweight='bold')
ax1.set_ylim(-0.02, 0.70)
ax1.legend(loc='lower center', frameon=True, facecolor='white', framealpha=0.9)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Cost-Complexity Pruning Curve (Alpha vs Accuracy)
alphas = np.linspace(0.0, 0.05, 50)
# Training accuracy starts near 1.0, drops as alpha grows
train_acc = 1.0 - 0.25 * (alphas / 0.05)**0.8
# Validation accuracy has a peak around alpha = 0.015
val_acc = 0.82 + 0.13 * np.exp(-((alphas - 0.016)/0.012)**2) - 0.20 * alphas

ax2.plot(alphas, train_acc * 100, color='#1f77b4', linewidth=2.5, linestyle='--', label='Akurasi Data Latih (Training Accuracy)')
ax2.plot(alphas, val_acc * 100, color='#d62728', linewidth=3.0, label='Akurasi Data Validasi (Validation Accuracy)')

opt_alpha = alphas[np.argmax(val_acc)]
max_val = np.max(val_acc) * 100

ax2.axvline(opt_alpha, color='#2ca02c', linestyle=':', linewidth=2, label=f'Parameter Pemangkasan Optimal: $\\alpha^* = {opt_alpha:.3f}$')
ax2.scatter([opt_alpha], [max_val], color='#2ca02c', s=120, zorder=6, marker='*')

ax2.annotate('Zona Overfitting Ekstrem\nPohon Terlalu Dalam\n$\\alpha \\approx 0$', xy=(0.002, 98), xytext=(0.005, 88),
             arrowprops=dict(facecolor='#1f77b4', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', edgecolor='#1f77b4'))

ax2.annotate(f'Pohon Optimal (Pruned)\nGeneralisasi Tertinggi: {max_val:.1f}%', xy=(opt_alpha, max_val), xytext=(opt_alpha + 0.008, max_val - 4),
             arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2ca02c'))

ax2.set_title('B. Optimasi Pemangkasan Pohon (Cost-Complexity Pruning)\nMitigasi Overfitting Melalui Parameter Kompleksitas Biaya $\\alpha$', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel(r'Parameter Kompleksitas Biaya ($\alpha$ / ccp_alpha)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Akurasi Model (%)', fontsize=11, fontweight='bold')
ax2.set_ylim(65, 102)
ax2.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "kurva_ketidakmurnian_dan_pruning_decision_tree.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "kurva_ketidakmurnian_dan_pruning_decision_tree.png"))
print(f"[OK] Generated {fig2_path}")
