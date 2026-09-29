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
# FIGURE 1: Anatomi KNN dan Efek Nilai K
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Intuisi Geometris KNN pada Serangan Hama
np.random.seed(42)
# Class 0: Tanaman Sehat
x0 = np.random.normal(3.5, 0.9, 25)
y0 = np.random.normal(6.5, 0.9, 25)
# Class 1: Tanaman Terserang Ulat Api
x1 = np.random.normal(6.5, 1.0, 25)
y1 = np.random.normal(4.0, 1.0, 25)

# Query point (pohon uji baru)
xq, yq = 5.0, 5.2

ax1.scatter(x0, y0, color='#2ca02c', s=70, edgecolors='k', alpha=0.85, label='Pohon Sawit Sehat ($y=0$)')
ax1.scatter(x1, y1, color='#d62728', s=70, marker='^', edgecolors='k', alpha=0.85, label='Pohon Terserang Hama ($y=1$)')
ax1.scatter([xq], [yq], color='#1f77b4', s=160, marker='*', edgecolors='black', linewidth=1.5, zorder=6, label='Pohon Uji Baru ($x_q$)')

# Compute distances
pts_all = np.vstack([np.column_stack([x0, y0]), np.column_stack([x1, y1])])
labels_all = np.array([0]*25 + [1]*25)
dists = np.sqrt((pts_all[:, 0] - xq)**2 + (pts_all[:, 1] - yq)**2)
sorted_indices = np.argsort(dists)

# Circles for K=3 and K=7
r_k3 = dists[sorted_indices[2]] + 0.12
r_k7 = dists[sorted_indices[6]] + 0.12

c3 = plt.Circle((xq, yq), r_k3, color='#ff7f0e', fill=False, linestyle='--', linewidth=2, label=f'Radius Lingkup $K=3$ ($r={r_k3:.2f}$)')
c7 = plt.Circle((xq, yq), r_k7, color='#9467bd', fill=False, linestyle='-.', linewidth=2, label=f'Radius Lingkup $K=7$ ($r={r_k7:.2f}$)')
ax1.add_patch(c3)
ax1.add_patch(c7)

# Connect lines to 3 nearest
for idx in sorted_indices[:3]:
    ax1.plot([xq, pts_all[idx, 0]], [yq, pts_all[idx, 1]], color='#ff7f0e', linestyle=':', linewidth=1.5)

ax1.annotate('Keputusan $K=3$:\n2 Sehat, 1 Hama $\\rightarrow$ SEHAT', xy=(xq, yq), xytext=(xq - 3.2, yq + 1.8),
             arrowprops=dict(facecolor='#ff7f0e', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff3e0', edgecolor='#ff7f0e'))

ax1.annotate('Keputusan $K=7$:\n3 Sehat, 4 Hama $\\rightarrow$ HAMA!', xy=(xq, yq), xytext=(xq + 0.8, yq - 2.2),
             arrowprops=dict(facecolor='#9467bd', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#f3e5f5', edgecolor='#9467bd'))

ax1.set_title('A. Mekanisme Klasifikasi Tetangga Terdekat\nPemungutan Suara Mayoritas Berdasarkan Lingkup Radius $K$', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Reflektansi Inframerah Dekat / NIR (Skala Sensor Drone)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Indeks Kerapatan Kanopi / NDVI', fontsize=11, fontweight='bold')
ax1.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
ax1.set_xlim(1.0, 9.0)
ax1.set_ylim(1.5, 9.0)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Kompleksitas Garis Batas Keputusan (K=1 vs K=15 vs K=45)
# Generate synthetic mesh
xx, yy = np.meshgrid(np.linspace(1, 9, 80), np.linspace(1.5, 9, 80))
grid_pts = np.c_[xx.ravel(), yy.ravel()]

from sklearn.neighbors import KNeighborsClassifier
clf1 = KNeighborsClassifier(n_neighbors=1).fit(pts_all, labels_all)
clf15 = KNeighborsClassifier(n_neighbors=15).fit(pts_all, labels_all)

z1 = clf1.predict(grid_pts).reshape(xx.shape)
z15 = clf15.predict(grid_pts).reshape(xx.shape)

ax2.contour(xx, yy, z1, levels=[0.5], colors='#d62728', linewidths=2.2, linestyles='--', label='Batas $K=1$ (Overfitting / Sangat Sensitif Derau)')
ax2.contour(xx, yy, z15, levels=[0.5], colors='#1f77b4', linewidths=3.0, linestyles='-', label='Batas $K=15$ (Generalisasi Optimal / Halus)')

ax2.scatter(x0, y0, color='#2ca02c', s=40, edgecolors='k', alpha=0.7, label='Pohon Sehat')
ax2.scatter(x1, y1, color='#d62728', s=40, marker='^', edgecolors='k', alpha=0.7, label='Pohon Hama')

# Label contours manually
ax2.plot([], [], color='#d62728', linestyle='--', linewidth=2.2, label='Batas $K=1$ (Overfitting / Bergerigi Tajam)')
ax2.plot([], [], color='#1f77b4', linestyle='-', linewidth=3.0, label='Batas $K=15$ (Kompromi Bias-Varians Optimal)')

ax2.set_title('B. Pengaruh Hiperparameter $K$ terhadap Batas Keputusan\nEvolusi dari Batas Bergerigi ($K=1$) Menuju Batas Halus ($K=15$)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Reflektansi Inframerah Dekat / NIR', fontsize=11, fontweight='bold')
ax2.set_ylabel('Indeks Kerapatan Kanopi / NDVI', fontsize=11, fontweight='bold')
ax2.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "anatomi_knn_dan_efek_nilai_k.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "anatomi_knn_dan_efek_nilai_k.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Metrik Jarak dan Curse of Dimensionality
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Kontur Iso-Jarak (L1, L2, L_inf)
theta = np.linspace(0, 2*np.pi, 200)
# L2 circle
x_l2 = np.cos(theta)
y_l2 = np.sin(theta)
# L1 diamond
t1 = np.linspace(0, 1, 50)
x_l1 = np.concatenate([t1, 1-t1, -t1, -(1-t1)])
y_l1 = np.concatenate([1-t1, -t1, -(1-t1), t1])
# L_inf square
x_linf = np.array([-1, 1, 1, -1, -1])
y_linf = np.array([-1, -1, 1, 1, -1])

ax1.plot(x_l1, y_l1, color='#d62728', linewidth=2.5, label=r'Manhattan ($L_1$ Norm): $|x| + |y| = 1$')
ax1.plot(x_l2, y_l2, color='#1f77b4', linewidth=2.8, label=r'Euclidean ($L_2$ Norm): $\sqrt{x^2 + y^2} = 1$')
ax1.plot(x_linf, y_linf, color='#2ca02c', linewidth=2.2, linestyle='--', label=r'Chebyshev ($L_\infty$ Norm): $\max(|x|, |y|) = 1$')

ax1.scatter([0], [0], color='black', s=80, zorder=5)
ax1.annotate('Pusat Titik Acuan $(0, 0)$', xy=(0, 0), xytext=(0.15, -0.25),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='black'))

ax1.set_title('A. Geometri Ruang Metrik Jarak (Iso-Distance Contours)\nBentuk Wilayah Kesetaraan Jarak Berdasarkan Nilai $p$ Minkowski', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Dimensi Fitur $x_1$ Terstandarisasi', fontsize=11, fontweight='bold')
ax1.set_ylabel('Dimensi Fitur $x_2$ Terstandarisasi', fontsize=11, fontweight='bold')
ax1.set_xlim(-1.6, 1.6)
ax1.set_ylim(-1.6, 1.6)
ax1.set_aspect('equal')
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Curse of Dimensionality (Distortion of Distances)
dims = np.arange(1, 101)
contrast_ratios = []
np.random.seed(42)

for d in dims:
    # 200 random points in d-dimensional hypercube [0, 1]^d
    pts = np.random.uniform(0, 1, size=(200, d))
    query = np.random.uniform(0, 1, size=(1, d))
    dists = np.sqrt(np.sum((pts - query)**2, axis=1))
    d_min = np.min(dists)
    d_max = np.max(dists)
    # Relative contrast: (d_max - d_min) / d_min
    contrast_ratios.append((d_max - d_min) / (d_min + 1e-9))

ax2.plot(dims, contrast_ratios, color='#d62728', linewidth=2.8, marker='o', markersize=4, markevery=5)
ax2.axhline(0.1, color='gray', linestyle=':', label='Ambang Hilangnya Kontras Jarak ($< 0.1$)')

ax2.annotate('Dimensi Rendah ($D \\leq 5$):\nKontras Jarak Jelas\nKNN Bekerja Efektif', xy=(5, contrast_ratios[4]), xytext=(12, contrast_ratios[4] + 0.8),
             arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2ca02c'))

ax2.annotate('Kutukan Dimensi ($D > 40$):\nJarak Semua Titik Menjadi Seragam!\n$\\lim_{D \\to \\infty} \\frac{d_{\\max} - d_{\\min}}{d_{\\min}} \\to 0$',
             xy=(60, contrast_ratios[59]), xytext=(35, contrast_ratios[59] + 1.2),
             arrowprops=dict(facecolor='#d62728', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d62728'))

ax2.set_title('B. Fenomena Kutukan Dimensi (Curse of Dimensionality)\nDegradasi Kontras Relatif Jarak $\\frac{d_{\\max} - d_{\\min}}{d_{\\min}}$ Seiring Bertambahnya Fitur', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Jumlah Dimensi Fitur ($D$)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Kontras Relatif Jarak Relatif', fontsize=11, fontweight='bold')
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "metrik_jarak_dan_curse_of_dimensionality_knn.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "metrik_jarak_dan_curse_of_dimensionality_knn.png"))
print(f"[OK] Generated {fig2_path}")
