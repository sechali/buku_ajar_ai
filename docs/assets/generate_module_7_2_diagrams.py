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
# FIGURE 1: Anatomi Fungsi Sigmoid dan Decision Boundary
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Kurva Sigmoid dan Log-Odds
z = np.linspace(-7, 7, 200)
p = 1 / (1 + np.exp(-z))

ax1.plot(z, p, color='#1f77b4', linewidth=3, label=r'Fungsi Sigmoid: $\sigma(z) = \frac{1}{1 + e^{-z}}$')
ax1.axhline(0.5, color='#d62728', linestyle='--', linewidth=1.5, label='Ambang Keputusan Baku (Threshold $\\tau = 0.5$)')
ax1.axvline(0.0, color='gray', linestyle=':', linewidth=1.2)
ax1.axhline(1.0, color='#2ca02c', linestyle=':', linewidth=1.2, alpha=0.7)
ax1.axhline(0.0, color='#2ca02c', linestyle=':', linewidth=1.2, alpha=0.7)

# Shading regions
ax1.fill_between(z, 0.5, 1.0, where=(z >= 0), color='#2ca02c', alpha=0.15, label='Wilayah Prediksi Kelas 1 (Lolos Mutu)')
ax1.fill_between(z, 0.0, 0.5, where=(z < 0), color='#d62728', alpha=0.15, label='Wilayah Prediksi Kelas 0 (Afkir / Ditolak)')

# Annotations
ax1.scatter([0], [0.5], color='#d62728', s=100, zorder=5)
ax1.annotate('Titik Infleksi\n$z = 0 \\rightarrow p = 0.5$\nOdds = 1:1', xy=(0, 0.5), xytext=(1.2, 0.35),
             arrowprops=dict(facecolor='#d62728', shrink=0.08, width=1.5, headwidth=6),
             fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d62728'))

ax1.set_title('A. Kurva Aktivasi Sigmoid & Pemetaan Probabilitas\nTransformasi Kombinasi Linier $z$ Menjadi $P(y=1|x) \\in [0, 1]$', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Logit / Skor Linier $z = \\mathbf{w}^T \\mathbf{x} + b$', fontsize=11, fontweight='bold')
ax1.set_ylabel('Probabilitas Prediksi $\\hat{p} = P(y=1)$', fontsize=11, fontweight='bold')
ax1.set_ylim(-0.05, 1.05)
ax1.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Linear Decision Boundary 2D pada Sortasi TBS
np.random.seed(42)
n_pts = 60
# Class 0: TBS Afkir / FFA Tinggi, Kadar Air Tinggi
ffa_0 = np.random.normal(4.8, 0.8, n_pts)
air_0 = np.random.normal(8.5, 1.1, n_pts)
# Class 1: TBS Prima / FFA Rendah, Kadar Air Normal
ffa_1 = np.random.normal(2.2, 0.6, n_pts)
air_1 = np.random.normal(5.2, 0.9, n_pts)

ax2.scatter(ffa_0, air_0, color='#d62728', marker='x', s=60, linewidth=2, label='TBS Afkir / Rusak ($y=0$)')
ax2.scatter(ffa_1, air_1, color='#2ca02c', marker='o', s=60, edgecolors='k', alpha=0.85, label='TBS Prima / Lolos ($y=1$)')

# Decision Boundary line: w1*x1 + w2*x2 + b = 0 -> x2 = -(w1*x1 + b)/w2
x_boundary = np.linspace(1.0, 6.0, 50)
y_boundary = -(1.8 * x_boundary - 13.5) / 1.5
ax2.plot(x_boundary, y_boundary, color='#1f77b4', linewidth=2.5, linestyle='-', label=r'Batas Keputusan: $\mathbf{w}^T \mathbf{x} + b = 0$')

# Annotations
ax2.annotate('Batas Ambang Pisah Linier\nProbabilitas $P=0.5$', xy=(3.5, 4.8), xytext=(4.2, 3.2),
             arrowprops=dict(facecolor='#1f77b4', shrink=0.08, width=1.5, headwidth=6),
             fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', edgecolor='#1f77b4'))

ax2.set_title('B. Garis Batas Keputusan (Decision Boundary) 2D\nPemisahan Mutu TBS Pabrik Kelapa Sawit (PKS)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Kadar Asam Lemak Bebas / FFA (% Bobot)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Kadar Air Buah (% Moisture)', fontsize=11, fontweight='bold')
ax2.set_xlim(0.8, 6.5)
ax2.set_ylim(2.5, 11.5)
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "anatomi_fungsi_sigmoid_dan_decision_boundary.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "anatomi_fungsi_sigmoid_dan_decision_boundary.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Fungsi Rugi Log Loss dan Kurva Penalti
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

p_vals = np.linspace(0.001, 0.999, 300)
loss_y1 = -np.log(p_vals)
loss_y0 = -np.log(1 - p_vals)

# Panel 1: Kurva Penalti Asimetris Log Loss
ax1.plot(p_vals, loss_y1, color='#1f77b4', linewidth=2.8, label=r'Penalti jika Label Riil $y = 1$: $-\ln(\hat{p})$')
ax1.plot(p_vals, loss_y0, color='#d62728', linewidth=2.8, linestyle='--', label=r'Penalti jika Label Riil $y = 0$: $-\ln(1 - \hat{p})$')

ax1.scatter([0.95], [-np.log(0.95)], color='#2ca02c', s=100, zorder=5)
ax1.annotate('Prediksi Benar & Yakin\n$\\hat{p} = 0.95 \\rightarrow \\text{Rugi} = 0.051$', xy=(0.95, -np.log(0.95)), xytext=(0.55, 1.2),
             arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2ca02c'))

ax1.scatter([0.05], [-np.log(0.05)], color='#d62728', s=100, zorder=5)
ax1.annotate('Salah & Terlalu Percaya Diri!\n$\\hat{p} = 0.05 \\rightarrow \\text{Rugi} \\to 3.00$', xy=(0.05, -np.log(0.05)), xytext=(0.15, 3.8),
             arrowprops=dict(facecolor='#d62728', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d62728'))

ax1.set_title('A. Kurva Penalti Binary Cross-Entropy (Log Loss)\nPenalti Asimtotik Menuju $\\infty$ bagi Prediksi Percaya Diri yang Salah', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Probabilitas Prediksi Model $\\hat{p} = P(y=1|x)$', fontsize=11, fontweight='bold')
ax1.set_ylabel('Besaran Nilai Rugi / Loss ($J$)', fontsize=11, fontweight='bold')
ax1.set_ylim(-0.2, 5.5)
ax1.legend(loc='upper center', frameon=True, facecolor='white', framealpha=0.9)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Sifat Cembung Log Loss vs Non-Cembung MSE pada Klasifikasi
w_vals = np.linspace(-3.5, 3.5, 200)
# True data: 1 point at x=2, y=1
x_pt = 2.0
y_pt = 1.0
p_pred = 1 / (1 + np.exp(-w_vals * x_pt))

# Log loss: -ln(p)
bce_curve = -np.log(p_pred)
# MSE: (y - p)^2 = (1 - p)^2
mse_curve = (y_pt - p_pred)**2 * 3.5 # scaled for comparison

ax2.plot(w_vals, bce_curve, color='#2ca02c', linewidth=3, label='Binary Cross-Entropy (Konveks Murni / Single Global Minimum)')
ax2.plot(w_vals, mse_curve, color='#d62728', linewidth=2.5, linestyle=':', label='Mean Squared Error (Non-Konveks pada Klasifikasi / Terjebak Flat Gradient)')

ax2.scatter([1.5], [-np.log(1/(1+np.exp(-1.5*2)))], color='#2ca02c', s=120, marker='*', zorder=6)
ax2.annotate('Gradien Selalu Menuntun\nke Minimum Global', xy=(1.5, 0.05), xytext=(-0.5, 1.8),
             arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=6),
             fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2ca02c'))

ax2.annotate('Zona Gradien Lenyap (Vanishing)\nMengunci Algoritma Optimasi', xy=(-2.5, 3.4), xytext=(-3.2, 4.5),
             arrowprops=dict(facecolor='#d62728', shrink=0.08, width=1.5, headwidth=6),
             fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d62728'))

ax2.set_title('B. Sifat Permukaan Optimasi: BCE vs MSE\nKeunggulan Konveksitas Binary Cross-Entropy pada Pembelajaran Mesin', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Nilai Parameter Bobot ($w$)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Nilai Fungsi Objektif Rugi', fontsize=11, fontweight='bold')
ax2.set_ylim(-0.2, 6.0)
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "fungsi_rugi_log_loss_dan_kurva_penalti.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "fungsi_rugi_log_loss_dan_kurva_penalti.png"))
print(f"[OK] Generated {fig2_path}")
