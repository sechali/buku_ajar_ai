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
# FIGURE 1: Anatomi K-Means Iterasi dan Pergeseran Centroid
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: Diagram Alir 4 Fase Algoritma Lloyd
ax1.axis('off')
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)

ax1.text(5.0, 9.4, 'SIKLUS ITERASI ALGORITMA K-MEANS (LLOYD\'S ALGORITHM)',
         ha='center', va='center', fontsize=11, fontweight='bold', color='#0d47a1')

# Phase 1: Inisialisasi
bbox_p1 = dict(boxstyle='round,pad=0.5', facecolor='#e3f2fd', edgecolor='#1976d2', linewidth=2)
ax1.text(5.0, 8.0, 'FASE 1: INISIALISASI PUSAT KLASTER (CENTROIDS)\nPilih $K$ titik awal secara acak atau menggunakan algoritma K-Means++\n$\\boldsymbol{\\mu}_1^{(0)}, \\boldsymbol{\\mu}_2^{(0)}, \\dots, \\boldsymbol{\\mu}_K^{(0)}$',
         ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_p1)

# Phase 2: Assignment
bbox_p2 = dict(boxstyle='round,pad=0.5', facecolor='#e8f5e9', edgecolor='#388e3c', linewidth=2)
ax1.text(5.0, 5.8, 'FASE 2: PENUGASAN KLASTER (ASSIGNMENT STEP)\nSetiap sampel data $\\mathbf{x}_i$ ditugaskan ke centroid terdekat (Jarak Euclidean terkecil):\n$c_i^{(t)} = \\arg\\min_{k \\in \\{1, \\dots, K\\}} \\|\\mathbf{x}_i - \\boldsymbol{\\mu}_k^{(t)}\\|^2$',
         ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_p2)

# Phase 3: Update
bbox_p3 = dict(boxstyle='round,pad=0.5', facecolor='#fff3e0', edgecolor='#f57c00', linewidth=2)
ax1.text(5.0, 3.6, 'FASE 3: PEMBARUAN PUSAT KLASTER (UPDATE STEP)\nHitung ulang koordinat centroid sebagai rata-rata aritmetika dari seluruh sampel anggotanya:\n$\\boldsymbol{\\mu}_k^{(t+1)} = \\frac{1}{|S_k^{(t)}|} \\sum_{i \\in S_k^{(t)}} \\mathbf{x}_i$',
         ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_p3)

# Phase 4: Convergence
bbox_p4 = dict(boxstyle='round,pad=0.5', facecolor='#f3e5f5', edgecolor='#8e24aa', linewidth=2)
ax1.text(5.0, 1.4, 'FASE 4: UJI KONVERGENSI (STOPPING CRITERIA)\nApakah posisi centroid tidak lagi bergeser $(\\|\\boldsymbol{\\mu}^{(t+1)} - \\boldsymbol{\\mu}^{(t)}\\| < \\epsilon)$?\n- Ya: Konvergen! Klaster final zonasi hara tanah terbentuk.\n- Tidak: Ulangi kembali ke Fase 2.',
         ha='center', va='center', fontsize=8.5, fontweight='bold', bbox=bbox_p4)

# Arrows between phases
ax1.annotate('', xy=(5.0, 6.7), xytext=(5.0, 7.2), arrowprops=dict(arrowstyle="->", color='#1976d2', lw=2))
ax1.annotate('', xy=(5.0, 4.5), xytext=(5.0, 5.0), arrowprops=dict(arrowstyle="->", color='#388e3c', lw=2))
ax1.annotate('', xy=(5.0, 2.3), xytext=(5.0, 2.8), arrowprops=dict(arrowstyle="->", color='#f57c00', lw=2))

# Loopback arrow
ax1.annotate('', xy=(8.6, 5.8), xytext=(8.6, 1.4), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.4", color='#d32f2f', lw=2, linestyle='--'))
ax1.text(9.4, 3.6, 'Iterasi Berulang\n(Jika Belum Konvergen)', color='#d32f2f', fontsize=8, fontweight='bold', ha='center')

ax1.set_title('A. Arsitektur Komputasi 4-Fase Algoritma K-Means (Lloyd)', fontsize=12, fontweight='bold', pad=12)

# Panel 2: Visualisasi Pergeseran Centroid 2D pada Data Hara Tanah
np.random.seed(42)
# 3 Klaster Hara Tanah: Miskin, Sedang, Subur
c1_pts = np.random.normal([2.0, 2.5], 0.6, (40, 2))
c2_pts = np.random.normal([6.0, 3.0], 0.7, (40, 2))
c3_pts = np.random.normal([4.0, 7.0], 0.6, (40, 2))

ax2.scatter(c1_pts[:, 0], c1_pts[:, 1], color='#e53935', alpha=0.6, s=40, label='Zona 1: Kritis (Defisiensi Hara)')
ax2.scatter(c2_pts[:, 0], c2_pts[:, 1], color='#fbc02d', alpha=0.6, s=40, label='Zona 2: Sedang (Perlu Perawatan)')
ax2.scatter(c3_pts[:, 0], c3_pts[:, 1], color='#2e7d32', alpha=0.6, s=40, label='Zona 3: Prima (Subur Tinggi)')

# Lintasan pergeseran centroid (Iterasi 0 -> 1 -> 2 -> Final)
track_c1 = np.array([[3.5, 4.0], [2.6, 3.1], [2.0, 2.5]])
track_c2 = np.array([[4.5, 3.5], [5.4, 3.2], [6.0, 3.0]])
track_c3 = np.array([[3.8, 5.2], [3.9, 6.3], [4.0, 7.0]])

for track, col in zip([track_c1, track_c2, track_c3], ['#b71c1c', '#f57f17', '#1b5e20']):
    # Titik awal
    ax2.scatter(track[0, 0], track[0, 1], color='white', edgecolor=col, s=120, marker='o', linewidth=2, zorder=5)
    ax2.text(track[0, 0]+0.2, track[0, 1]-0.2, r'$\mu^{(0)}$', fontsize=9, fontweight='bold', color=col)
    
    # Jalur pergeseran
    ax2.plot(track[:, 0], track[:, 1], color=col, linestyle=':', linewidth=2)
    for p in range(len(track)-1):
        ax2.annotate('', xy=(track[p+1, 0], track[p+1, 1]), xytext=(track[p, 0], track[p, 1]),
                     arrowprops=dict(arrowstyle="->", color=col, lw=1.8))
        
    # Titik final konvergen
    ax2.scatter(track[-1, 0], track[-1, 1], color=col, edgecolor='black', s=200, marker='X', linewidth=1.5, zorder=6)
    ax2.text(track[-1, 0]+0.2, track[-1, 1]+0.2, r'$\mu^*$ (Final)', fontsize=9.5, fontweight='bold', color=col)

ax2.set_title('B. Trajektori Pergeseran Centroid Menuju Optimum Konvergen\n(Studi Kasus: Pemetaan Unsur Hara N-P-K Tanah Kelapa Sawit)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Kadar Nitrogen Tersedia / N-Total (g/kg)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Kadar Kalium Tertukar / K-dd (cmol/kg)', fontsize=11, fontweight='bold')
ax2.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "anatomi_kmeans_iterasi_dan_pergeseran_centroid.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "anatomi_kmeans_iterasi_dan_pergeseran_centroid.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Evaluasi Klaster Elbow dan Silhouette Analysis
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

# Panel 1: Kurva Elbow (Inersia WCSS vs K)
k_vals = np.arange(1, 9)
# WCSS yang turun tajam lalu menekuk di K=3
wcss = np.array([1250, 680, 240, 195, 160, 135, 115, 100])

ax1.plot(k_vals, wcss, 'o-', color='#1565c0', linewidth=2.5, markersize=8)
ax1.scatter([3], [wcss[2]], color='#d32f2f', s=180, zorder=5, edgecolor='black', linewidth=2)

ax1.annotate('TITIK SIKU OPTIMAL (ELBOW POINT)\n$K = 3$ Zona Kesuburan Lahan\n(Penurunan WCSS mulai melandai)',
             xy=(3, wcss[2]), xytext=(3.5, 450),
             arrowprops=dict(facecolor='#d32f2f', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffebee', edgecolor='#d32f2f'))

ax1.set_title('A. Metode Siku (Elbow Method) Berbasis Inersia WCSS\nIdentifikasi Jumlah Klaster Alami Tanpa Supervisi Label', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlabel('Jumlah Klaster ($K$)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Inersia / Within-Cluster Sum of Squares (WCSS)', fontsize=11, fontweight='bold')
ax1.set_xticks(k_vals)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Skor Rata-rata Silhouette vs K
sil_scores = np.array([0.0, 0.54, 0.72, 0.58, 0.51, 0.46, 0.42, 0.39])
bar_colors = ['#b0bec5', '#90caf9', '#2e7d32', '#a5d6a7', '#c8e6c9', '#e8f5e9', '#f1f8e9', '#f9fbe7']

bars = ax2.bar(k_vals, sil_scores, color=bar_colors, edgecolor='black', width=0.55)
ax2.axhline(0.72, color='#2e7d32', linestyle='--', linewidth=1.5, label='Puncak Skor Silhouette Tertinggi ($s = 0.72$)')

for bar in bars:
    h = bar.get_height()
    if h > 0:
        ax2.text(bar.get_x() + bar.get_width()/2, h + 0.02, f'{h:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_title('B. Evaluasi Koefisien Silhouette Rata-rata vs Jumlah Klaster ($K$)\nMemvalidasi Kerapatan Internal dan Keterpisahan Antar-Klaster', fontsize=12, fontweight='bold', pad=12)
ax2.set_xlabel('Jumlah Klaster ($K$)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Skor Rata-rata Silhouette ($s$)', fontsize=11, fontweight='bold')
ax2.set_xticks(k_vals)
ax2.set_ylim(0, 0.85)
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "evaluasi_klaster_elbow_dan_silhouette_analysis.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "evaluasi_klaster_elbow_dan_silhouette_analysis.png"))
print(f"[OK] Generated {fig2_path}")
