import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs('e:/Project Buku/docs/assets', exist_ok=True)
artifact_dir = r'C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11'

# -------------------------------------------------------------
# Diagram 1: Kerangka Kerja Tiga Tingkat EDA
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 7.5), dpi=300)
ax.set_xlim(0, 15)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title("Kerangka Kerja Eksplorasi Data Analisis (EDA): Tiga Tingkat Investigasi Data", 
             fontsize=13, fontweight='bold', pad=15, color='#0F172A')

tiers = [
    (2.5, "Tingkat 1: Analisis Univariat", "#EFF6FF", "#1D4ED8", [
        ("Fokus Utama", "Karakteristik individual satu variabel"),
        ("Metode Non-Grafis", "Mean, Median, Modus, Varians, Skewness, Kurtosis"),
        ("Metode Grafis", "Histogram, KDE Plot, Boxplot, Rug Plot"),
        ("Kasus Agribisnis", "Sebaran tonase TBS per blok, frekuensi curah hujan")
    ]),
    (7.5, "Tingkat 2: Analisis Bivariat", "#F0FDF4", "#15803D", [
        ("Fokus Utama", "Hubungan keterkaitan antara dua variabel"),
        ("Metode Non-Grafis", "Korelasi Pearson, Spearman, Tabel Kontinjensi, Chi-Square"),
        ("Metode Grafis", "Scatter Plot, Line Chart, Clustered Bar, Boxplot Komparatif"),
        ("Kasus Agribisnis", "Korelasi NDVI vs tonase panen, pH tanah vs yield")
    ]),
    (12.5, "Tingkat 3: Analisis Multivariat", "#FAF5FF", "#7E22CE", [
        ("Fokus Utama", "Interaksi simultan >= 3 variabel dan struktur laten"),
        ("Metode Non-Grafis", "Matriks Kovarians, Korelasi Parsial, PCA, VIF"),
        ("Metode Grafis", "Heatmap Korelasi, Pairplot berlabel, 3D Scatter, Facet Grid"),
        ("Kasus Agribisnis", "Interaksi NPK-Cuaca-NDVI terhadap produktivitas kelapa sawit")
    ])
]

for cx, title, bg, border, items in tiers:
    # Header card
    h_box = patches.FancyBboxPatch((cx-2.1, 7.2), 4.2, 0.9, boxstyle="round,pad=0.1", fc=border, ec=border, lw=1.5)
    ax.add_patch(h_box)
    ax.text(cx, 7.65, title, fontsize=9.5, fontweight='bold', ha='center', va='center', color='white')
    
    # Body card
    b_box = patches.FancyBboxPatch((cx-2.1, 1.2), 4.2, 5.8, boxstyle="round,pad=0.15", fc=bg, ec=border, lw=1.5)
    ax.add_patch(b_box)
    
    y_pos = 6.2
    for label, desc in items:
        ibox = patches.FancyBboxPatch((cx-1.95, y_pos-0.55), 3.9, 1.05, boxstyle="round,pad=0.08", fc="white", ec=border, lw=1)
        ax.add_patch(ibox)
        ax.text(cx-1.8, y_pos+0.22, f"• {label}:", fontsize=8.5, fontweight='bold', color=border)
        ax.text(cx-1.8, y_pos-0.2, desc, fontsize=7.5, color="#1E293B", wrap=True)
        y_pos -= 1.35

# Connecting arrows
ax.annotate("", xy=(5.2, 4.2), xytext=(4.8, 4.2), arrowprops=dict(arrowstyle="-|>", lw=3, color="#64748B", mutation_scale=20))
ax.annotate("", xy=(10.2, 4.2), xytext=(9.8, 4.2), arrowprops=dict(arrowstyle="-|>", lw=3, color="#64748B", mutation_scale=20))

# Bottom note
bot_box = patches.FancyBboxPatch((0.4, 0.3), 14.2, 0.65, boxstyle="round,pad=0.1", fc="#F1F5F9", ec="#475569", lw=1.5, ls=':')
ax.add_patch(bot_box)
ax.text(7.5, 0.62, "Prinsip John Tukey: 'Eksplorasi Data Analisis adalah pekerjaan detektif numerik untuk mengungkap pola sebelum mengonfirmasi teori.'", 
        fontsize=8.5, style='italic', fontweight='bold', ha='center', va='center', color="#334155")

plt.tight_layout()
out1 = 'e:/Project Buku/docs/assets/kerangka_eksplorasi_data_analisis_eda.png'
plt.savefig(out1, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'kerangka_eksplorasi_data_analisis_eda.png'), dpi=300)
plt.close()
print("Saved:", out1)

# -------------------------------------------------------------
# Diagram 2: Kuartet Anscombe & Pelajaran Visualisasi Data
# -------------------------------------------------------------
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(13, 8), dpi=300)
fig.suptitle("Pelajaran Fundamental Kuartet Anscombe: Statistik Deskriptif Identik, Pola Nyata Berbeda", 
             fontsize=13, fontweight='bold', color='#0F172A', y=0.98)

# Dataset Anscombe
x1 = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
y1 = np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68])

x2 = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
y2 = np.array([9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74])

x3 = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
y3 = np.array([7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73])

x4 = np.array([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8])
y4 = np.array([6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])

line_x = np.linspace(3, 20, 100)
line_y = 3.0 + 0.5 * line_x

axes = [ax1, ax2, ax3, ax4]
titles = [
    "Dataset I: Hubungan Linier Sederhana\n(Model Regresi Valid)",
    "Dataset II: Hubungan Non-Linier Parabolik\n(Memerlukan Regresi Polinomial)",
    "Dataset III: Hubungan Linier Sempurna + 1 Outlier\n(Pencilan Merusak Garis Regresi)",
    "Dataset IV: Titik Leverage Ekstrem\n(1 Titik Menentukan Kemiringan Garis)"
]

colors = ['#1D4ED8', '#D97706', '#DC2626', '#7C3AED']

for idx, (ax, x, y, title, col) in enumerate(zip(axes, [x1, x2, x3, x4], [y1, y2, y3, y4], titles, colors)):
    ax.scatter(x, y, color=col, s=60, edgecolors='k', zorder=4)
    ax.plot(line_x, line_y, color='#475569', ls='--', lw=1.8, label='Regresi Linier (y = 3.0 + 0.5x)')
    ax.set_title(title, fontsize=9.5, fontweight='bold', pad=8, color='#0F172A')
    ax.set_xlim(2, 20)
    ax.set_ylim(2, 14)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.text(19, 2.5, "Rerata x = 9.0\nRerata y = 7.5\nr = 0.816\nR² = 0.67", 
            fontsize=7.5, ha='right', bbox=dict(boxstyle="round,pad=0.2", fc="#F8FAFC", ec="#CBD5E1"))

plt.tight_layout()
out2 = 'e:/Project Buku/docs/assets/kuartet_anscombe_dan_inspeksi_distribusi_agribisnis.png'
plt.savefig(out2, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'kuartet_anscombe_dan_inspeksi_distribusi_agribisnis.png'), dpi=300)
plt.close()
print("Saved:", out2)
