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
# FIGURE 1: Anatomi PCA Rotasi Sumbu dan Vektor Eigen
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Rotasi Sumbu Koordinat Menuju Varians Maksimal (Vektor Eigen)
np.random.seed(42)
n_samples = 120
# Data berkorelasi kuat (misal NIR vs RedEdge pada kanopi sawit)
x_raw = np.random.normal(0, 1.8, n_samples)
y_raw = 0.85 * x_raw + np.random.normal(0, 0.65, n_samples)

ax1.scatter(x_raw, y_raw, color='#1565c0', alpha=0.55, s=35, edgecolors='none', label='Sampel Reflektansi Spektral Kanopi')

# Vektor Eigen 1 (PC1: Arah varians terbesar)
v1 = np.array([2.5, 2.5 * 0.85])
v1 = v1 / np.linalg.norm(v1) * 3.8
ax1.annotate('', xy=(v1[0], v1[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color='#d32f2f', lw=3))
ax1.text(v1[0] + 0.2, v1[1], r'Komponen Utama 1 ($\mathbf{u}_1$ / PC1)' + '\n' + r'Varians Terbesar ($\lambda_1 = 82\%$)',
         color='#d32f2f', fontsize=9.5, fontweight='bold')

# Vektor Eigen 2 (PC2: Tegak lurus ortogonal terhadap PC1)
v2 = np.array([-v1[1], v1[0]])
v2 = v2 / np.linalg.norm(v2) * 1.5
ax1.annotate('', xy=(v2[0], v2[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color='#2e7d32', lw=2.5))
ax1.text(v2[0] - 2.8, v2[1] + 0.2, r'PC2 ($\mathbf{u}_2 \perp \mathbf{u}_1$)' + '\n' + r'Sisa Varians ($\lambda_2 = 18\%$)',
         color='#2e7d32', fontsize=9, fontweight='bold')

# Garis sumbu PC1
line_x = np.linspace(-4.5, 4.5, 100)
ax1.plot(line_x, (v1[1]/v1[0]) * line_x, color='#d32f2f', linestyle='--', linewidth=1.5, alpha=0.7)

ax1.set_title('A. Rotasi Sumbu Koordinat Menuju Arah Varians Maksimal\n(Dekomposisi Vektor Eigen Ortogonal $\\mathbf{\\Sigma} \\mathbf{u} = \\lambda \\mathbf{u}$)', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Variabel Asli $x_1$: Reflektansi Red-Edge Drone (705 nm)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Variabel Asli $x_2$: Reflektansi NIR Drone (842 nm)', fontsize=11, fontweight='bold')
ax1.set_xlim(-5, 5)
ax1.set_ylim(-5, 5)
ax1.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Proyeksi Ortogonal dan Rekonstruksi Residual
# Ambil 12 titik sampel representatif
sample_idx = [5, 12, 24, 38, 45, 62, 75, 88, 92, 105, 112, 118]
x_sub = x_raw[sample_idx]
y_sub = y_raw[sample_idx]

# Proyeksi ke sumbu PC1 (arah unit vector u1)
u1_unit = v1 / np.linalg.norm(v1)
dots = x_sub * u1_unit[0] + y_sub * u1_unit[1]
proj_x = dots * u1_unit[0]
proj_y = dots * u1_unit[1]

ax2.plot(line_x, (v1[1]/v1[0]) * line_x, color='#d32f2f', linestyle='-', linewidth=2.5, label='Subruang Kompresi 1D (Sumbu PC1)')
ax2.scatter(x_sub, y_sub, color='#1565c0', s=60, edgecolors='k', zorder=5, label='Titik Data Asli 2D')
ax2.scatter(proj_x, proj_y, color='#d32f2f', s=60, edgecolors='k', zorder=5, label='Titik Terproyeksi pada PC1 (Skor Skor Komponen)')

# Garis proyeksi tegak lurus
for i in range(len(x_sub)):
    ax2.plot([x_sub[i], proj_x[i]], [y_sub[i], proj_y[i]], color='gray', linestyle=':', linewidth=1.2)

ax2.annotate('Galat Rekonstruksi Minimum:\nJarak Proyeksi Tegak Lurus Ortogonal\n' + r'$\min \sum \|\mathbf{x}_i - \hat{\mathbf{x}}_i\|^2$',
             xy=(x_sub[2], y_sub[2]), xytext=(x_sub[2]-3.2, y_sub[2]+1.2),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1.2, headwidth=5),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffde7', edgecolor='black'))

ax2.set_title('B. Proyeksi Ortogonal Meminimalkan Galat Kuadrat Rekonstruksi\n(Kompresi Dimensi Tanpa Kehilangan Pola Variabilitas Utama)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Koordinat Terstandardisasi $x_1$', fontsize=11, fontweight='bold')
ax2.set_ylabel('Koordinat Terstandardisasi $x_2$', fontsize=11, fontweight='bold')
ax2.set_xlim(-5, 5)
ax2.set_ylim(-5, 5)
ax2.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "anatomi_pca_rotasi_sumbu_dan_vektor_eigen.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "anatomi_pca_rotasi_sumbu_dan_vektor_eigen.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Analisis Scree Plot dan Biplot Agronomi
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5), dpi=300)

# Panel 1: Scree Plot & Cumulative Explained Variance Ratio
n_pcs = np.arange(1, 9)
# Proporsi varians 8 fitur kimia tanah (N, P, K, pH, Ca, Mg, C-Org, CEC)
evr = np.array([48.5, 24.2, 11.8, 6.5, 3.8, 2.4, 1.6, 1.2])
cum_evr = np.cumsum(evr)

bars = ax1.bar(n_pcs, evr, color='#1976d2', edgecolor='black', alpha=0.8, width=0.55, label='Varians Individual per PC (%)')
ax1.plot(n_pcs, cum_evr, 'o-', color='#d32f2f', linewidth=2.5, markersize=7, label='Varians Kumulatif (%)')
ax1.axhline(84.5, color='#2e7d32', linestyle='--', linewidth=1.8, label='Ambang Retensi Informasi > 80% (PC1 + PC2 = 72.7%, PC1..PC3 = 84.5%)')

for bar in bars:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h + 1.0, f'{h:.1f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

ax1.set_title('A. Scree Plot & Kurva Kumulatif Varians Terjelaskan (EVR)\nKriteria Retensi Dimensi Optimal Menggunakan Nilai Eigen', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Komponen Utama (Principal Component / PC)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Proporsi Varians Terjelaskan (%)', fontsize=11, fontweight='bold')
ax1.set_xticks(n_pcs)
ax1.set_ylim(0, 105)
ax1.legend(loc='center right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: PCA Biplot 2D (Skor Sampel + Vektor Loading Fitur)
np.random.seed(42)
# 3 Klaster Kebun Sawit: Lahan Gambut, Mineral Bukit, Aluvial Lembah
c1_score = np.random.normal([-2.5, 0.5], [0.8, 0.7], (35, 2))
c2_score = np.random.normal([1.2, -1.8], [0.7, 0.6], (35, 2))
c3_score = np.random.normal([2.0, 1.6], [0.7, 0.6], (30, 2))

ax2.scatter(c1_score[:, 0], c1_score[:, 1], color='#e53935', alpha=0.6, s=40, label='Blok Gambut Masam (Kritis)')
ax2.scatter(c2_score[:, 0], c2_score[:, 1], color='#fbc02d', alpha=0.6, s=40, label='Blok Podsolik Berbukit (Sedang)')
ax2.scatter(c3_score[:, 0], c3_score[:, 1], color='#2e7d32', alpha=0.6, s=40, label='Blok Lembah Aluvial (Subur)')

# Vektor Loading Fitur (Arah dan kekuatan korelasi fitur asli terhadap PC1 & PC2)
loadings = {
    'N-Total': (2.8, 1.2),
    'K-dd': (3.2, 0.6),
    'pH-Tanah': (2.4, 2.2),
    'Bahan-Organik': (-3.0, 1.4),
    'P-Tersedia': (1.8, -2.2),
    'Al-Tukar': (-2.6, -1.8)
}

for feat, (lx, ly) in loadings.items():
    ax2.annotate('', xy=(lx, ly), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color='#4a148c', lw=2))
    ax2.text(lx * 1.12, ly * 1.12, feat, color='#4a148c', fontsize=9, fontweight='bold', ha='center', va='center')

# Garis sumbu tengah
ax2.axhline(0, color='gray', linestyle=':', linewidth=1)
ax2.axvline(0, color='gray', linestyle=':', linewidth=1)

ax2.set_title('B. PCA Biplot 2D: Interseksi Sebaran Sampel Kebun & Vektor Loading Fitur\nVisualisasi Komprehensif Korelasi Multivariat dalam 2 Komponen Utama', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Komponen Utama 1 (PC1: 48.5% Varians) - Sumbu Kesuburan Kimiawi', fontsize=10.5, fontweight='bold')
ax2.set_ylabel('Komponen Utama 2 (PC2: 24.2% Varians) - Sumbu Keseimbangan Fosfat/pH', fontsize=10.5, fontweight='bold')
ax2.set_xlim(-4.5, 4.5)
ax2.set_ylim(-3.5, 3.5)
ax2.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=8)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "analisis_scree_plot_dan_biplot_agronomi.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "analisis_scree_plot_dan_biplot_agronomi.png"))
print(f"[OK] Generated {fig2_path}")
