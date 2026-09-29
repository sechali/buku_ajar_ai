import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig_dir = r"e:\Project Buku\docs\assets"
art_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"

# ==============================================================================
# FIGURE 1: Arsitektur Sequential Boosting dan Koreksi Residual
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Diagram Alir Arsitektur Sekuensial Gradient Boosting
ax1.axis('off')
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)

ax1.text(5.0, 9.4, 'MEKANISME PEMBELAJARAN SEKUENSIAL GRADIENT BOOSTING',
         ha='center', va='center', fontsize=11, fontweight='bold', color='#0d47a1')

# Base Model F0
bbox_f0 = dict(boxstyle='round,pad=0.4', facecolor='#e3f2fd', edgecolor='#1976d2', linewidth=1.8)
ax1.text(1.8, 7.8, 'Model Awal ($F_0$):\nPrediksi Konstan\n$F_0(x) = \\bar{y}$ (Mean)', ha='center', va='center', fontsize=8.5, bbox=bbox_f0)

# Residu 1
bbox_r1 = dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d32f2f', linewidth=1.5)
ax1.text(5.0, 7.8, 'Hitung Pseudo-Residual 1:\n$r_{i1} = y_i - F_0(x_i)$\n(Sisa Galat yang Belum Terjelaskan)', ha='center', va='center', fontsize=8.5, bbox=bbox_r1)
ax1.annotate('', xy=(3.8, 7.8), xytext=(2.8, 7.8), arrowprops=dict(arrowstyle="->", color='#d32f2f', lw=1.8))

# Tree 1
bbox_t1 = dict(boxstyle='round,pad=0.4', facecolor='#e8f5e9', edgecolor='#388e3c', linewidth=1.8)
ax1.text(8.2, 7.8, 'Pohon Lemah 1 ($h_1$):\nDilatih Memprediksi $r_{i1}$\n(Bukan Target Asli $y$!)', ha='center', va='center', fontsize=8.5, bbox=bbox_t1)
ax1.annotate('', xy=(7.0, 7.8), xytext=(6.2, 7.8), arrowprops=dict(arrowstyle="->", color='#388e3c', lw=1.8))

# Update F1
bbox_f1 = dict(boxstyle='round,pad=0.4', facecolor='#fff3e0', edgecolor='#f57c00', linewidth=1.8)
ax1.text(8.2, 5.2, 'Pembaruan Model 1:\n$F_1(x) = F_0(x) + \\eta h_1(x)$\n(Galat Menyusut)', ha='center', va='center', fontsize=8.5, bbox=bbox_f1)
ax1.annotate('', xy=(8.2, 5.9), xytext=(8.2, 7.0), arrowprops=dict(arrowstyle="->", color='#f57c00', lw=1.8))

# Residu 2
bbox_r2 = dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d32f2f', linewidth=1.5)
ax1.text(5.0, 5.2, 'Hitung Pseudo-Residual 2:\n$r_{i2} = y_i - F_1(x_i)$\n(Residu Semakin Kecil)', ha='center', va='center', fontsize=8.5, bbox=bbox_r2)
ax1.annotate('', xy=(6.2, 5.2), xytext=(7.1, 5.2), arrowprops=dict(arrowstyle="->", color='#d32f2f', lw=1.8))

# Tree 2
bbox_t2 = dict(boxstyle='round,pad=0.4', facecolor='#e8f5e9', edgecolor='#388e3c', linewidth=1.8)
ax1.text(1.8, 5.2, 'Pohon Lemah 2 ($h_2$):\nDilatih Memprediksi $r_{i2}$', ha='center', va='center', fontsize=8.5, bbox=bbox_t2)
ax1.annotate('', xy=(2.9, 5.2), xytext=(3.8, 5.2), arrowprops=dict(arrowstyle="->", color='#388e3c', lw=1.8))

# Dots
ax1.text(5.0, 3.4, '...\nIterasi Diulang Hingga $M$ Pohon Estimator Terbentuk\n...', ha='center', va='center', fontsize=10, fontweight='bold', color='#455a64')
ax1.annotate('', xy=(5.0, 4.0), xytext=(5.0, 4.5), arrowprops=dict(arrowstyle="->", color='#455a64', lw=1.8))
ax1.annotate('', xy=(5.0, 2.3), xytext=(5.0, 2.8), arrowprops=dict(arrowstyle="->", color='#455a64', lw=1.8))

# Final Consensus Model
bbox_final = dict(boxstyle='round,pad=0.5', facecolor='#f3e5f5', edgecolor='#8e24aa', linewidth=2)
ax1.text(5.0, 1.2, 'MODEL PREDIKTIF AKUMULASI FINAL:\n$F_M(\\mathbf{x}) = F_0(\\mathbf{x}) + \\sum_{m=1}^M \\eta h_m(\\mathbf{x})$\n(Presisi Ekstrem, Mengeliminasi Bias dan Varians secara Terarah)',
         ha='center', va='center', fontsize=9, fontweight='bold', bbox=bbox_final)

ax1.set_title('A. Arsitektur Sekuensial Gradient Boosting (Koreksi Residu Bertahap)', fontsize=12, fontweight='bold', pad=12)

# Panel 2: Penurunan Fungsi Rugi MSE / Residual Error Seiring Penambahan Pohon
n_trees = np.arange(1, 101)
np.random.seed(42)
# Galat latih dan uji
train_loss = 4.2 * np.exp(-n_trees / 15.0) + 0.15
test_loss = 4.2 * np.exp(-n_trees / 16.0) + 0.35 + 0.003 * np.maximum(0, n_trees - 60)

ax2.plot(n_trees, train_loss, color='#1565c0', linewidth=2.5, label='Galat Data Latih (Train MSE)')
ax2.plot(n_trees, test_loss, color='#d32f2f', linewidth=2.5, label='Galat Data Uji Independen (Test MSE)')

ax2.axvline(60, color='#2e7d32', linestyle='--', linewidth=1.8, label='Titik Estimator Optimal ($M = 60$)')
ax2.scatter([60], [test_loss[59]], color='#2e7d32', s=140, zorder=5, edgecolor='black')

ax2.annotate('Batas Generalisasi Optimal:\nTest MSE Minimum (0.35)\n' + r'$\eta = 0.10, M = 60$',
             xy=(60, test_loss[59]), xytext=(25, 2.2),
             arrowprops=dict(facecolor='#2e7d32', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2e7d32'))

ax2.annotate('Zona Overfitting:\nTrain MSE terus turun\nnamun Test MSE mulai naik!',
             xy=(95, test_loss[94]), xytext=(70, 1.4),
             arrowprops=dict(facecolor='#d32f2f', shrink=0.08, width=1.2, headwidth=5),
             fontsize=8.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d32f2f'))

ax2.set_title('B. Dinamika Konvergensi Galat Kuadrat Terkecil (MSE) vs Jumlah Pohon\n(Penyusutan Residual secara Monotonik dalam Ruang Fungsi)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Jumlah Pohon Estimator Sekuensial ($M$ / n_estimators)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Mean Squared Error (MSE)', fontsize=11, fontweight='bold')
ax2.set_xlim(0, 105)
ax2.set_ylim(0, 4.5)
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "arsitektur_sequential_boosting_dan_koreksi_residual.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "arsitektur_sequential_boosting_dan_koreksi_residual.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Analisis Learning Rate Shrinkage dan Tradeoff Komputasi
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5), dpi=300)

# Panel 1: Efek Learning Rate (eta) terhadap Kurva Test Error
iters = np.arange(1, 121)
# eta = 0.5 (Terlalu agresif, cepat konvergen tapi overfit cepat)
err_fast = 0.55 + 3.5 * np.exp(-iters / 8.0) + 0.008 * np.maximum(0, iters - 25)
# eta = 0.1 (Optimal, konvergen stabil di nilai terendah)
err_opt = 0.32 + 3.5 * np.exp(-iters / 22.0) + 0.002 * np.maximum(0, iters - 70)
# eta = 0.01 (Terlalu lambat / underfit jika iterasi sedikit)
err_slow = 1.20 + 3.5 * np.exp(-iters / 75.0)

ax1.plot(iters, err_fast, color='#d32f2f', linewidth=2.2, label=r'Laju Agresif ($\eta = 0.50$): Cepat Overfitting')
ax1.plot(iters, err_opt, color='#2e7d32', linewidth=2.8, label=r'Laju Optimal ($\eta = 0.10$): Konvergensi Terbaik')
ax1.plot(iters, err_slow, color='#1565c0', linewidth=2.2, linestyle='--', label=r'Laju Konservatif ($\eta = 0.01$): Butuh Lebih Banyak Pohon')

ax1.scatter([70], [err_opt[69]], color='#2e7d32', s=120, zorder=5)
ax1.set_title('A. Pengaruh Laju Pembelajaran (Shrinkage $\\eta$) terhadap Laju Konvergensi\n(Meredam Langkah Pembaruan untuk Mencegah Memorisasi Derau)', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Jumlah Iterasi Pohon ($M$)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Galat Prediksi Data Uji (Test Error)', fontsize=11, fontweight='bold')
ax1.set_xlim(0, 125)
ax1.set_ylim(0.2, 4.2)
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Peringkat Feature Importance Prediksi Tonase Panen Sawit (MDI / Gain)
features = ['Curah_Hujan_Bln_Lalu', 'Dosis_Pupuk_Kalium', 'Kerapatan_Pohon_Ha', 'Umur_Tegakan_Thn', 'Defisit_Air_Kumulatif', 'Ketinggian_Blok']
importance = np.array([0.34, 0.26, 0.18, 0.11, 0.07, 0.04])
y_pos = np.arange(len(features))

colors = ['#1b5e20', '#2e7d32', '#4caf50', '#81c784', '#a5d6a7', '#c8e6c9']
bars = ax2.barh(y_pos, importance * 100, color=colors, edgecolor='black', alpha=0.9, height=0.6)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(features, fontsize=10, fontweight='bold')
ax2.invert_yaxis()

for bar in bars:
    w = bar.get_width()
    ax2.text(w + 0.8, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='left', fontsize=9.5, fontweight='bold')

ax2.set_title('B. Peringkat Kepentingan Fitur (Feature Importance Gain / MDI)\nIdentifikasi Variabel Penggerak Utama Tonase Panen TBS Kelapa Sawit', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Derajat Kontribusi Relatif Model Gradient Boosting (%)', fontsize=11, fontweight='bold')
ax2.set_xlim(0, 42)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "analisis_learning_rate_shrinkage_dan_tradeoff_komputasi.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "analisis_learning_rate_shrinkage_dan_tradeoff_komputasi.png"))
print(f"[OK] Generated {fig2_path}")
