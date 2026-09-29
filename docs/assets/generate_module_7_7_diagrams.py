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
# FIGURE 1: Anatomi SVM Margin dan Support Vectors
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Konsep Geometris Maximal Margin & Support Vectors
np.random.seed(42)
# Kelas 1: Sawit Prima (+1)
x1_pos = np.random.normal(5.5, 0.7, 20)
x2_pos = np.random.normal(6.5, 0.7, 20)

# Kelas -1: Sawit Afkir (-1)
x1_neg = np.random.normal(2.5, 0.7, 20)
x2_neg = np.random.normal(3.5, 0.7, 20)

ax1.scatter(x1_pos, x2_pos, color='#2e7d32', s=60, label='Kelas +1: Mutu Prima', edgecolors='k')
ax1.scatter(x1_neg, x2_neg, color='#d32f2f', s=60, label='Kelas -1: Mutu Afkir', edgecolors='k')

# Garis Hiperbidang w^T x + b = 0 (misal x2 = -x1 + 9 => x1 + x2 - 9 = 0)
x_line = np.linspace(1.0, 7.5, 100)
# Garis Keputusan Tengah
y_decision = -1.0 * x_line + 9.0
# Margin Atas: w^T x + b = +1
y_margin_pos = -1.0 * x_line + 10.3
# Margin Bawah: w^T x + b = -1
y_margin_neg = -1.0 * x_line + 7.7

ax1.plot(x_line, y_decision, color='#1565c0', linewidth=2.5, label=r'Hiperbidang Keputusan: $\mathbf{w}^T \mathbf{x} + b = 0$')
ax1.plot(x_line, y_margin_pos, color='#2e7d32', linestyle='--', linewidth=1.8, label=r'Batas Margin Positif: $\mathbf{w}^T \mathbf{x} + b = +1$')
ax1.plot(x_line, y_margin_neg, color='#d32f2f', linestyle='--', linewidth=1.8, label=r'Batas Margin Negatif: $\mathbf{w}^T \mathbf{x} + b = -1$')
ax1.fill_between(x_line, y_margin_neg, y_margin_pos, color='#bbdefb', alpha=0.3, label=r'Zona Margin Maksimal ($M = \frac{2}{\|\mathbf{w}\|}$)')

# Tandai Support Vectors
sv_pos = np.array([[4.8, 5.5], [5.3, 5.0]])
sv_neg = np.array([[3.2, 4.5], [3.8, 3.9]])
ax1.scatter(sv_pos[:, 0], sv_pos[:, 1], color='#2e7d32', s=160, facecolors='none', edgecolors='#ff6f00', linewidth=3)
ax1.scatter(sv_neg[:, 0], sv_neg[:, 1], color='#d32f2f', s=160, facecolors='none', edgecolors='#ff6f00', linewidth=3)

ax1.annotate('Vektor Pendukung\n(Support Vectors)\nTitik penentu batas!', xy=(4.8, 5.5), xytext=(6.2, 4.5),
             arrowprops=dict(facecolor='#ff6f00', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff3e0', edgecolor='#ff6f00'))

# Margin width arrow
ax1.annotate('', xy=(3.85, 3.85), xytext=(5.15, 5.15),
             arrowprops=dict(arrowstyle="<->", color='#d84315', lw=2.5))
ax1.text(4.2, 4.8, r'Lebar Margin $M = \frac{2}{\|\mathbf{w}\|}$', fontsize=9.5, fontweight='bold', color='#d84315', rotation=45)

ax1.set_title('A. Geometri Pemisah Margin Maksimal & Support Vectors\n(Optimal Separating Hyperplane)', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Fitur $x_1$: Nilai Klorofil SPAD Terstandardisasi', fontsize=11, fontweight='bold')
ax1.set_ylabel('Fitur $x_2$: Kadar Asam Lemak Bebas (FFA)', fontsize=11, fontweight='bold')
ax1.set_xlim(1.0, 7.5)
ax1.set_ylim(1.5, 9.0)
ax1.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Hard Margin vs Soft Margin (Variabel Slack xi dan Penalti C)
ax2.scatter(x1_pos, x2_pos, color='#2e7d32', s=50, edgecolors='k')
ax2.scatter(x1_neg, x2_neg, color='#d32f2f', s=50, edgecolors='k')

# Titik outlier/noise melanggar margin
outlier_pos = [3.5, 4.8]  # Sampel positif menyusup ke wilayah negatif
outlier_neg = [4.5, 6.2]  # Sampel negatif menyusup ke wilayah positif
ax2.scatter([outlier_pos[0]], [outlier_pos[1]], color='#2e7d32', s=80, marker='^', edgecolors='k', zorder=5)
ax2.scatter([outlier_neg[0]], [outlier_neg[1]], color='#d32f2f', s=80, marker='v', edgecolors='k', zorder=5)

ax2.plot(x_line, y_decision, color='#1565c0', linewidth=2.5)
ax2.plot(x_line, y_margin_pos, color='#2e7d32', linestyle='--', linewidth=1.5)
ax2.plot(x_line, y_margin_neg, color='#d32f2f', linestyle='--', linewidth=1.5)
ax2.fill_between(x_line, y_margin_neg, y_margin_pos, color='#ffe0b2', alpha=0.25)

# Tunjukkan variabel kelonggaran (slack xi)
ax2.annotate(r'Pelanggaran Margin ($\xi_i > 0$)', xy=(outlier_pos[0], outlier_pos[1]), xytext=(1.5, 6.2),
             arrowprops=dict(facecolor='#d32f2f', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d32f2f'))

# Formula box
bbox_c = dict(boxstyle='round,pad=0.5', facecolor='#f3e5f5', edgecolor='#7b1fa2', linewidth=2)
ax2.text(4.2, 2.2, r'$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 + C \sum_{i=1}^N \xi_i$' + '\n' +
         r'Parameter $C$ Mengatur Toleransi:' + '\n' +
         r'- $C$ Besar: Margin sempit, penalti galat keras (risiko overfit)' + '\n' +
         r'- $C$ Kecil: Margin lebar, toleran terhadap derau kebun (generalisasi tinggi)',
         ha='center', va='center', fontsize=9, bbox=bbox_c)

ax2.set_title(r'B. Formulasi Soft Margin dengan Variabel Kelonggaran ($\xi_i$)' + '\n' + 'Pengaruh Hyperparameter Regulasi $C$ pada Data Riil Perkebunan', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Fitur $x_1$: Klorofil Terstandardisasi', fontsize=11, fontweight='bold')
ax2.set_ylabel('Fitur $x_2$: Kadar FFA Terstandardisasi', fontsize=11, fontweight='bold')
ax2.set_xlim(1.0, 7.5)
ax2.set_ylim(1.5, 9.0)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "anatomi_svm_margin_dan_support_vectors.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "anatomi_svm_margin_dan_support_vectors.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Transformasi Kernel Trick dan Pemisahan Non-Linier SVM
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Data 2D Non-Linier Konsentris
np.random.seed(42)
n_pts = 120
r_in = np.random.uniform(0.3, 1.4, n_pts)
theta_in = np.random.uniform(0, 2*np.pi, n_pts)
x1_in = r_in * np.cos(theta_in)
x2_in = r_in * np.sin(theta_in)

r_out = np.random.uniform(2.2, 3.4, n_pts)
theta_out = np.random.uniform(0, 2*np.pi, n_pts)
x1_out = r_out * np.cos(theta_out)
x2_out = r_out * np.sin(theta_out)

ax1.scatter(x1_in, x2_in, color='#2e7d32', s=45, label='Kelas A: CPO Murni (Rendemen Tinggi)', edgecolors='k')
ax1.scatter(x1_out, x2_out, color='#d32f2f', s=45, label='Kelas B: CPO Tercemar / Teroksidasi', edgecolors='k')

# Boundary lingkaran
circle = plt.Circle((0, 0), 1.8, color='#1565c0', fill=False, linestyle='--', linewidth=2.5, label='Batas Keputusan Non-Linier (RBF)')
ax1.add_patch(circle)

ax1.set_title('A. Ruang Fitur Asli 2D: Data Tidak Dapat Dipisahkan Garis Lurus\n(Mustahil Dipisahkan Hiperbidang Linier Tanpa Kernel)', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Spektroskopi NIR Panjang Gelombang $\\lambda_1$', fontsize=11, fontweight='bold')
ax1.set_ylabel('Spektroskopi NIR Panjang Gelombang $\\lambda_2$', fontsize=11, fontweight='bold')
ax1.set_xlim(-4, 4)
ax1.set_ylim(-4, 4)
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Pemetaan ke Ruang Dimensi 3 (Kernel Trick: z = x1^2 + x2^2)
ax2.remove()
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

z_in = x1_in**2 + x2_in**2
z_out = x1_out**2 + x2_out**2

ax2.scatter(x1_in, x2_in, z_in, color='#2e7d32', s=40, edgecolors='k', label='Kelas A (CPO Murni)')
ax2.scatter(x1_out, x2_out, z_out, color='#d32f2f', s=40, edgecolors='k', label='Kelas B (Tercemar)')

# Hyperplane pemisah di 3D pada z = 3.24
x_plane = np.linspace(-3.5, 3.5, 10)
y_plane = np.linspace(-3.5, 3.5, 10)
X_p, Y_p = np.meshgrid(x_plane, y_plane)
Z_p = np.full_like(X_p, 3.24)

ax2.plot_surface(X_p, Y_p, Z_p, color='#2196f3', alpha=0.35, edgecolor='#1565c0')

ax2.set_title('B. Ruang Terproyeksi 3D melalui Pemetaan Kernel $\\phi(\\mathbf{x}) = (x_1, x_2, x_1^2 + x_2^2)$\nHiperbidang Linier Datar Memisahkan Kedua Kelas secara Sempurna!', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Fitur $\\phi_1$', fontsize=10, fontweight='bold')
ax2.set_ylabel('Fitur $\\phi_2$', fontsize=10, fontweight='bold')
ax2.set_zlabel('Dimensi Angkat $\\phi_3 = r^2$', fontsize=10, fontweight='bold')
ax2.legend(loc='upper left', fontsize=8.5)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "transformasi_kernel_trick_dan_pemisahan_nonlinier_svm.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "transformasi_kernel_trick_dan_pemisahan_nonlinier_svm.png"))
print(f"[OK] Generated {fig2_path}")
