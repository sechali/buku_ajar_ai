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
# FIGURE 1: Arsitektur Ensemble Random Forest dan Bagging
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Diagram Alir Arsitektur Random Forest
ax1.axis('off')
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)

# Dataset Origin
bbox_data = dict(boxstyle='round,pad=0.5', facecolor='#bbdefb', edgecolor='#1976d2', linewidth=2)
ax1.text(5.0, 9.2, 'Dataset Latih Perkebunan Sawit ($N$ Baris, $p$ Fitur)\n(Brondolan, FFA, Air, Berat, Jam Tunda)',
         ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=bbox_data)

# Bootstrap Sampling arrows
ax1.annotate('', xy=(1.8, 7.3), xytext=(4.2, 8.5), arrowprops=dict(arrowstyle="->", color='#1976d2', lw=2))
ax1.annotate('', xy=(5.0, 7.3), xytext=(5.0, 8.5), arrowprops=dict(arrowstyle="->", color='#1976d2', lw=2))
ax1.annotate('', xy=(8.2, 7.3), xytext=(5.8, 8.5), arrowprops=dict(arrowstyle="->", color='#1976d2', lw=2))

ax1.text(2.6, 8.0, 'Bootstrap 1\n(~63.2%)', color='#0d47a1', fontsize=8.5, fontweight='bold')
ax1.text(5.2, 8.0, 'Bootstrap 2\n(~63.2%)', color='#0d47a1', fontsize=8.5, fontweight='bold')
ax1.text(7.4, 8.0, f'Bootstrap B\n(~63.2%)', color='#0d47a1', fontsize=8.5, fontweight='bold')

# Trees
bbox_tree = dict(boxstyle='round,pad=0.4', facecolor='#c8e6c9', edgecolor='#388e3c', linewidth=1.8)
ax1.text(1.8, 6.2, 'Pohon 1 (CART)\nFitur Acak $m=\\sqrt{p}$', ha='center', va='center', fontsize=9, fontweight='bold', bbox=bbox_tree)
ax1.text(5.0, 6.2, 'Pohon 2 (CART)\nFitur Acak $m=\\sqrt{p}$', ha='center', va='center', fontsize=9, fontweight='bold', bbox=bbox_tree)
ax1.text(6.8, 6.2, '...', ha='center', va='center', fontsize=18, fontweight='bold', color='#388e3c')
ax1.text(8.2, 6.2, 'Pohon B (CART)\nFitur Acak $m=\\sqrt{p}$', ha='center', va='center', fontsize=9, fontweight='bold', bbox=bbox_tree)

# Predictions
bbox_pred = dict(boxstyle='square,pad=0.3', facecolor='#fff9c4', edgecolor='#fbc02d', linewidth=1.5)
ax1.text(1.8, 4.4, 'Prediksi 1:\nKelas Prima', ha='center', va='center', fontsize=8.5, bbox=bbox_pred)
ax1.text(5.0, 4.4, 'Prediksi 2:\nKelas Prima', ha='center', va='center', fontsize=8.5, bbox=bbox_pred)
ax1.text(8.2, 4.4, 'Prediksi B:\nKelas Standar', ha='center', va='center', fontsize=8.5, bbox=bbox_pred)

ax1.annotate('', xy=(1.8, 4.9), xytext=(1.8, 5.5), arrowprops=dict(arrowstyle="->", color='#388e3c', lw=1.5))
ax1.annotate('', xy=(5.0, 4.9), xytext=(5.0, 5.5), arrowprops=dict(arrowstyle="->", color='#388e3c', lw=1.5))
ax1.annotate('', xy=(8.2, 4.9), xytext=(8.2, 5.5), arrowprops=dict(arrowstyle="->", color='#388e3c', lw=1.5))

# Aggregation Box
bbox_agg = dict(boxstyle='round,pad=0.5', facecolor='#ffe0b2', edgecolor='#f57c00', linewidth=2)
ax1.text(5.0, 2.5, 'MEKANISME AGREGASI ENSEMBLE:\nPemungutan Suara Mayoritas (Majority Voting)\n$\\hat{y} = \\arg\\max_c \\sum_{b=1}^B \\mathbb{I}(\\hat{y}_b = c)$',
         ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=bbox_agg)

ax1.annotate('', xy=(4.2, 3.2), xytext=(2.2, 3.8), arrowprops=dict(arrowstyle="->", color='#f57c00', lw=1.8))
ax1.annotate('', xy=(5.0, 3.2), xytext=(5.0, 3.8), arrowprops=dict(arrowstyle="->", color='#f57c00', lw=1.8))
ax1.annotate('', xy=(5.8, 3.2), xytext=(7.8, 3.8), arrowprops=dict(arrowstyle="->", color='#f57c00', lw=1.8))

# Final Output
bbox_out = dict(boxstyle='round,pad=0.4', facecolor='#e1bee7', edgecolor='#8e24aa', linewidth=2)
ax1.text(5.0, 0.9, 'PREDIKSI KONSENSUS FINAL: KELAS PRIMA (MUTU EKSPOR)\n(Tahan Derau, Stabil, dan Varians Sangat Rendah)',
         ha='center', va='center', fontsize=9.5, fontweight='bold', bbox=bbox_out)
ax1.annotate('', xy=(5.0, 1.45), xytext=(5.0, 1.85), arrowprops=dict(arrowstyle="->", color='#8e24aa', lw=2))

ax1.set_title('A. Arsitektur Ensemble Random Forest (Bagging & Subspace)\nPenggabungan Ratusan Pohon Lemah Menjadi Satu Model Super Tangguh', fontsize=12, fontweight='bold', pad=12)

# Panel 2: Reduksi Varians & Konvergensi OOB Error vs Jumlah Pohon
n_trees = np.arange(1, 151)
np.random.seed(42)
# Single tree has error ~14% with high variance, drops and stabilizes around 3.5%
oob_err = 0.035 + 0.12 * np.exp(-n_trees / 18.0) + np.random.normal(0, 0.003, len(n_trees)) * np.exp(-n_trees / 25.0)

ax2.plot(n_trees, oob_err * 100, color='#d62728', linewidth=2.5, label='Tingkat Galat Out-of-Bag (OOB Error %)')
ax2.axhline(3.5, color='#2ca02c', linestyle='--', linewidth=1.8, label='Batas Asimtotik Konvergensi Galat (3.5%)')

ax2.scatter([1], [oob_err[0]*100], color='#1f77b4', s=100, zorder=5)
ax2.annotate('Pohon Tunggal ($B=1$):\nVarians Tinggi (Galat ~15%)', xy=(1, oob_err[0]*100), xytext=(12, 14.5),
             arrowprops=dict(facecolor='#1f77b4', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', edgecolor='#1f77b4'))

ax2.scatter([80], [oob_err[79]*100], color='#2ca02c', s=100, zorder=5)
ax2.annotate('Zona Stabil ($B \\geq 60$):\nVarians Diredam Maksimal\nBebas Overfitting!', xy=(80, oob_err[79]*100), xytext=(55, 7.5),
             arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2ca02c'))

ax2.set_title('B. Konvergensi Galat Out-of-Bag (OOB Error) vs Jumlah Pohon\nPenambahan Estimator Meredam Varians Tanpa Memicu Overfitting', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Jumlah Pohon Estimator dalam Hutan ($B$ / n_estimators)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Tingkat Galat Generalisasi OOB (%)', fontsize=11, fontweight='bold')
ax2.set_xlim(0, 155)
ax2.set_ylim(1.0, 18.0)
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "arsitektur_ensemble_random_forest_dan_bagging.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "arsitektur_ensemble_random_forest_dan_bagging.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Analisis Feature Importance MDI dan OOB Evaluasi
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Ranking Feature Importance MDI
features = ['Brondolan_Lepas_%', 'Kadar_FFA_%', 'Kadar_Air_%', 'Jam_Tunda_Angkut', 'Berat_Tandan_kg', 'Ketinggian_Blok']
importance = np.array([0.38, 0.28, 0.16, 0.10, 0.05, 0.03])
y_pos = np.arange(len(features))

colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd', '#8c564b']
bars = ax1.barh(y_pos, importance * 100, color=colors, edgecolor='k', alpha=0.85, height=0.6)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(features, fontsize=10, fontweight='bold')
ax1.invert_yaxis()

for bar in bars:
    w = bar.get_width()
    ax1.text(w + 0.8, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='left', fontsize=9.5, fontweight='bold')

ax1.set_title('A. Ranking Kepentingan Fitur (Mean Decrease in Impurity / MDI)\nIdentifikasi Variabel Paling Berpengaruh terhadap Mutu TBS Sawit', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Derajat Kontribusi Relatif / Feature Importance (%)', fontsize=11, fontweight='bold')
ax1.set_xlim(0, 48)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Ekuivalensi Skor OOB vs 5-Fold Cross Validation
folds = np.array(['Fold 1', 'Fold 2', 'Fold 3', 'Fold 4', 'Fold 5', 'Mean CV', 'OOB Score'])
scores = np.array([96.2, 97.5, 95.8, 98.1, 96.9, 96.9, 96.8])
bar_colors = ['#bbdefb']*5 + ['#1976d2', '#d62728']

bars2 = ax2.bar(folds, scores, color=bar_colors, edgecolor='k', alpha=0.9, width=0.55)
ax2.set_ylim(90, 101)
ax2.axhline(96.8, color='#d62728', linestyle='--', linewidth=1.5, label='Skor Evaluasi OOB (96.8%)')

for bar in bars2:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, h + 0.25, f'{h:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_title('B. Ekuivalensi Metrik OOB vs 5-Fold Cross Validation\nValidasi Internal Bebas Bias Tanpa Memerlukan Set Validasi Terpisah', fontsize=12, fontweight='bold', pad=12)
ax2.set_ylabel('Akurasi Klasifikasi Mutu (%)', fontsize=11, fontweight='bold')
ax2.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "analisis_feature_importance_mdi_dan_oob_evaluasi.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "analisis_feature_importance_mdi_dan_oob_evaluasi.png"))
print(f"[OK] Generated {fig2_path}")
