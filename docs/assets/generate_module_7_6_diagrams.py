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
# FIGURE 1: Anatomi Teorema Bayes dan Arsitektur Naive Bayes
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Komponen Teorema Bayes
ax1.axis('off')
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)

ax1.text(5.0, 9.4, 'TEOREMA BAYES DALAM DIAGNOSTIK KESEHATAN TANAMAN SAWIT',
         ha='center', va='center', fontsize=11, fontweight='bold', color='#0d47a1')

# Formula Box Center
bbox_main = dict(boxstyle='round,pad=0.6', facecolor='#f5f5f5', edgecolor='#424242', linewidth=2)
ax1.text(5.0, 7.8, r'$P(C_k \mid \mathbf{x}) = \frac{P(\mathbf{x} \mid C_k) \cdot P(C_k)}{P(\mathbf{x})}$',
         ha='center', va='center', fontsize=18, fontweight='bold', bbox=bbox_main)

# Callout 1: Posterior
bbox_post = dict(boxstyle='round,pad=0.4', facecolor='#e8eaf6', edgecolor='#3f51b5', linewidth=1.5)
ax1.text(1.8, 5.8, 'POSTERIOR PROBABILITY\n$P(C_k \\mid \\mathbf{x})$\nProbabilitas tanaman sawit sakit\nsetelah mengamati gejala $\\mathbf{x}$',
         ha='center', va='center', fontsize=8.5, bbox=bbox_post)
ax1.annotate('', xy=(3.8, 7.5), xytext=(2.5, 6.6),
             arrowprops=dict(arrowstyle="->", color='#3f51b5', lw=2))

# Callout 2: Likelihood
bbox_like = dict(boxstyle='round,pad=0.4', facecolor='#e8f5e9', edgecolor='#2e7d32', linewidth=1.5)
ax1.text(5.0, 5.8, 'LIKELIHOOD (KEMUNGKINAN)\n$P(\\mathbf{x} \\mid C_k) = \\prod_{j=1}^p P(x_j \\mid C_k)$\nAsumsi Naive: Gejala diasumsikan\nsaling bebas bersyarat!',
         ha='center', va='center', fontsize=8.5, bbox=bbox_like)
ax1.annotate('', xy=(4.8, 7.3), xytext=(5.0, 6.7),
             arrowprops=dict(arrowstyle="->", color='#2e7d32', lw=2))

# Callout 3: Prior
bbox_prior = dict(boxstyle='round,pad=0.4', facecolor='#fff3e0', edgecolor='#e65100', linewidth=1.5)
ax1.text(8.2, 5.8, 'PRIOR PROBABILITY\n$P(C_k)$\nProbabilitas dasar prevalensi\npenyakit di kebun (data historis)',
         ha='center', va='center', fontsize=8.5, bbox=bbox_prior)
ax1.annotate('', xy=(5.8, 7.5), xytext=(7.5, 6.6),
             arrowprops=dict(arrowstyle="->", color='#e65100', lw=2))

# Callout 4: Evidence
bbox_evid = dict(boxstyle='round,pad=0.4', facecolor='#fce4ec', edgecolor='#c2185b', linewidth=1.5)
ax1.text(5.0, 3.5, 'EVIDENCE (NORMALISASI TOTAL)\n$P(\\mathbf{x}) = \\sum_{k=1}^K P(\\mathbf{x} \\mid C_k) P(C_k)$\nKonstanta pembagi yang sama untuk seluruh kelas',
         ha='center', va='center', fontsize=8.5, bbox=bbox_evid)
ax1.annotate('', xy=(5.0, 7.1), xytext=(5.0, 4.3),
             arrowprops=dict(arrowstyle="->", color='#c2185b', lw=2))

# Decision Rule
bbox_rule = dict(boxstyle='round,pad=0.5', facecolor='#e0f2f1', edgecolor='#00796b', linewidth=2)
ax1.text(5.0, 1.3, 'ATURAN KEPUTUSAN MAP (MAXIMUM A POSTERIORI):\n$\\hat{y} = \\arg\\max_{k \\in \\{1, \\dots, K\\}} \\left[ \\ln P(C_k) + \\sum_{j=1}^p \\ln P(x_j \\mid C_k) \\right]$\n(Operasi penjumlahan logaritma mencegah *arithmetic underflow*)',
         ha='center', va='center', fontsize=9, fontweight='bold', bbox=bbox_rule)
ax1.annotate('', xy=(5.0, 2.1), xytext=(5.0, 2.7),
             arrowprops=dict(arrowstyle="->", color='#00796b', lw=2))

ax1.set_title('A. Dekomposisi Komponen Teorema Bayes & Log-Likelihood MAP', fontsize=12, fontweight='bold', pad=12)

# Panel 2: Diagram Alir Arsitektur Inferensi Naive Bayes
ax2.axis('off')
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)

# Input Gejala
bbox_in = dict(boxstyle='round,pad=0.4', facecolor='#e1f5fe', edgecolor='#0288d1', linewidth=1.8)
ax2.text(1.5, 8.5, 'Fitur Gejala 1 ($x_1$):\nKadar Klorofil SPAD', ha='center', va='center', fontsize=8, bbox=bbox_in)
ax2.text(1.5, 6.5, 'Fitur Gejala 2 ($x_2$):\nKelembapan Daun (%)', ha='center', va='center', fontsize=8, bbox=bbox_in)
ax2.text(1.5, 4.5, 'Fitur Gejala 3 ($x_3$):\nBercak Daun (Ada/Tdk)', ha='center', va='center', fontsize=8, bbox=bbox_in)
ax2.text(1.5, 2.5, 'Fitur Gejala $p$ ($x_p$):\nPopulasi Spora Jamur', ha='center', va='center', fontsize=8, bbox=bbox_in)

# Likelihood Estimators
bbox_lik_calc = dict(boxstyle='round,pad=0.4', facecolor='#e8f5e9', edgecolor='#388e3c', linewidth=1.5)
ax2.text(5.0, 8.5, 'Gaussian PDF: $P(x_1 \\mid C_k)$\n$\\mathcal{N}(\\mu_{k1}, \\sigma_{k1}^2)$', ha='center', va='center', fontsize=8, bbox=bbox_lik_calc)
ax2.text(5.0, 6.5, 'Gaussian PDF: $P(x_2 \\mid C_k)$\n$\\mathcal{N}(\\mu_{k2}, \\sigma_{k2}^2)$', ha='center', va='center', fontsize=8, bbox=bbox_lik_calc)
ax2.text(5.0, 4.5, 'Bernoulli: $P(x_3 \\mid C_k)$\n$p_{k3}^{x_3} (1-p_{k3})^{1-x_3}$', ha='center', va='center', fontsize=8, bbox=bbox_lik_calc)
ax2.text(5.0, 2.5, 'Multinomial: $P(x_p \\mid C_k)$\n$\\theta_{kp}$ (Laplace Smoothed)', ha='center', va='center', fontsize=8, bbox=bbox_lik_calc)

# Arrows input to calc
for y_c in [8.5, 6.5, 4.5, 2.5]:
    ax2.annotate('', xy=(3.8, y_c), xytext=(2.6, y_c), arrowprops=dict(arrowstyle="->", color='#37474f', lw=1.5))

# Aggregation & Output
bbox_prod = dict(boxstyle='round,pad=0.5', facecolor='#fff9c4', edgecolor='#fbc02d', linewidth=2)
ax2.text(8.5, 5.5, 'Agregator Mandiri:\n$\\prod_{j=1}^p P(x_j \\mid C_k) \\cdot P(C_k)$\nEvaluasi Terpisah\nUntuk Tiap Kelas:\n- $C_1$: Sehat (75%)\n- $C_2$: Ganoderma (22%)\n- $C_3$: Defisiensi (3%)',
         ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_prod)

for y_c in [8.5, 6.5, 4.5, 2.5]:
    ax2.annotate('', xy=(7.2, 5.5), xytext=(6.2, y_c), arrowprops=dict(arrowstyle="->", color='#f57c00', lw=1.2))

# Result
bbox_res = dict(boxstyle='round,pad=0.4', facecolor='#d1c4e9', edgecolor='#512da8', linewidth=2)
ax2.text(8.5, 1.5, 'DIAGNOSIS AKHIR:\nKelas Ganoderma\n(Kecepatan $\\mathcal{O}(p)$,\nSiap untuk IoT Edge)',
         ha='center', va='center', fontsize=9, fontweight='bold', bbox=bbox_res)
ax2.annotate('', xy=(8.5, 2.4), xytext=(8.5, 3.8), arrowprops=dict(arrowstyle="->", color='#512da8', lw=2))

ax2.set_title('B. Arsitektur Komputasi Inferensi Paralel Naive Bayes', fontsize=12, fontweight='bold', pad=12)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "anatomi_teorema_bayes_dan_arsitektur_naive_bayes.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "anatomi_teorema_bayes_dan_arsitektur_naive_bayes.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Distribusi Gaussian Naive Bayes dan Laplace Smoothing
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

# Panel 1: Gaussian Density Functions untuk Fitur Klorofil SPAD pada Sawit Sehat vs Ganoderma
x_spad = np.linspace(20, 75, 400)
mu_sehat, sigma_sehat = 56.0, 4.2
mu_ganod, sigma_ganod = 36.5, 5.5

pdf_sehat = (1.0 / (sigma_sehat * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_spad - mu_sehat) / sigma_sehat)**2)
pdf_ganod = (1.0 / (sigma_ganod * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_spad - mu_ganod) / sigma_ganod)**2)

ax1.plot(x_spad, pdf_sehat, color='#2e7d32', linewidth=2.5, label='Sawit Sehat: $\\mathcal{N}(\\mu=56.0, \\sigma=4.2)$')
ax1.fill_between(x_spad, pdf_sehat, color='#2e7d32', alpha=0.25)

ax1.plot(x_spad, pdf_ganod, color='#d32f2f', linewidth=2.5, label='Infeksi Ganoderma: $\\mathcal{N}(\\mu=36.5, \\sigma=5.5)$')
ax1.fill_between(x_spad, pdf_ganod, color='#d32f2f', alpha=0.25)

# Ambang potong Bayesian
idx_cross = np.argmin(np.abs(pdf_sehat - pdf_ganod))
x_thresh = x_spad[idx_cross]
ax1.axvline(x_thresh, color='#1565c0', linestyle='--', linewidth=2, label=f'Titik Potong Bayes ($x={x_thresh:.1f}$ SPAD)')

# Sampel Uji Baru
x_new = 44.0
p_sehat_new = (1.0 / (sigma_sehat * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_new - mu_sehat) / sigma_sehat)**2)
p_ganod_new = (1.0 / (sigma_ganod * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_new - mu_ganod) / sigma_ganod)**2)

ax1.scatter([x_new, x_new], [p_sehat_new, p_ganod_new], color=['#2e7d32', '#d32f2f'], s=80, zorder=6)
ax1.axvline(x_new, color='purple', linestyle=':', linewidth=1.5)
ax1.annotate(f'Sampel Daun Lapangan: {x_new} SPAD\n$P(x \\mid \\text{{Ganoderma}}) > P(x \\mid \\text{{Sehat}})$',
             xy=(x_new, p_ganod_new), xytext=(x_new + 2, p_ganod_new + 0.015),
             arrowprops=dict(facecolor='purple', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#f3e5f5', edgecolor='purple'))

ax1.set_title('A. Pemodelan Fitur Kontinu Menggunakan Gaussian Naive Bayes\n(Fungsi Densitas Probabilitas Nilai Klorofil Daun Sawit SPAD)', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Nilai Pengukuran Klorofil Daun Sawit (SPAD Unit)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Densitas Probabilitas $P(x_j \\mid C_k)$', fontsize=11, fontweight='bold')
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Efek Laplace Smoothing Mencegah Zero-Frequency Problem
words = ['Bercak', 'Layu', 'Pucuk_Kering', 'Tandan_Busuk', 'Akar_Rapuh', 'Gejala_Langka']
counts_raw = np.array([45, 38, 25, 12, 18, 0])  # Gejala langka bernilai 0!
n_total = np.sum(counts_raw)
k_classes = len(words)

# Probabilitas tanpa smoothing (Raw Maximum Likelihood)
p_raw = counts_raw / n_total

# Probabilitas dengan Laplace Smoothing (alpha = 1)
alpha = 1.0
p_smoothed = (counts_raw + alpha) / (n_total + alpha * k_classes)

x_pos = np.arange(len(words))
width = 0.35

rects1 = ax2.bar(x_pos - width/2, p_raw * 100, width, label='Tanpa Smoothing (MLE: Nol Memicu Keruntuhan Produk)', color='#e53935', edgecolor='black', alpha=0.85)
rects2 = ax2.bar(x_pos + width/2, p_smoothed * 100, width, label=f'Laplace Smoothing ($\\alpha=1$: Probabilitas Positif Terjamin)', color='#1e88e5', edgecolor='black', alpha=0.85)

ax2.set_title('B. Mitigasi Zero-Frequency Trap Menggunakan Laplace Smoothing\n(Mencegah Probabilitas 0% Menggugurkan Seluruh Hasil Perkalian)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Daftar Gejala Patologis Tanaman Sawit', fontsize=11, fontweight='bold')
ax2.set_ylabel('Probabilitas Estimasi (%)', fontsize=11, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(words, fontsize=9.5, fontweight='bold', rotation=15)
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

# Highlight Zero trap
ax2.annotate('BAHAYA ZERO FREQUENCY!\n$P = 0.0\\% \\rightarrow \\prod P(x_j) = 0$!',
             xy=(5 - width/2, 0), xytext=(3.5, 12),
             arrowprops=dict(facecolor='#d32f2f', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d32f2f'))

ax2.annotate(f'Penyelamatan Laplace:\n$P = {p_smoothed[5]*100:.2f}\\%$ (Stabil!)',
             xy=(5 + width/2, p_smoothed[5]*100), xytext=(4.3, 5),
             arrowprops=dict(facecolor='#1e88e5', shrink=0.08, width=1.5, headwidth=6),
             fontsize=8.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', edgecolor='#1e88e5'))

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "distribusi_gaussian_naive_bayes_dan_laplace_smoothing.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "distribusi_gaussian_naive_bayes_dan_laplace_smoothing.png"))
print(f"[OK] Generated {fig2_path}")
