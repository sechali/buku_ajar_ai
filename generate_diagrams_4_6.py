import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('e:/Project Buku/docs/assets', exist_ok=True)
artifact_dir = r'C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11'

# -------------------------------------------------------------
# Diagram 1: Anatomi Arsitektur Hirarkis Matplotlib & Seaborn
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
ax.set_xlim(0, 15)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title("Anatomi Arsitektur Objek Matplotlib dan Hubungannya dengan Seaborn", 
             fontsize=13, fontweight='bold', pad=15, color='#0F172A')

# Outer Figure Box
fig_box = patches.FancyBboxPatch((0.5, 0.5), 14.0, 8.8, boxstyle="round,pad=0.2", fc="#F8FAFC", ec="#0284C7", lw=2.5)
ax.add_patch(fig_box)
ax.text(1.2, 8.8, "Objek Figure (Kanvas Keseluruhan Gambar)", fontsize=11, fontweight='bold', color="#0369A1")

# Subplot Axes 1 (Left: Scatter / Line)
ax1_box = patches.FancyBboxPatch((1.2, 1.8), 6.0, 6.5, boxstyle="round,pad=0.15", fc="white", ec="#334155", lw=1.8)
ax.add_patch(ax1_box)
ax.text(4.2, 7.8, "Objek Axes 1 (Plot Scatter/Line)", fontsize=10, fontweight='bold', ha='center', color="#0F172A")

# Draw elements inside Axes 1
# Spines
ax.plot([1.8, 6.6], [2.8, 2.8], color="#0F172A", lw=2) # X Spine
ax.plot([1.8, 1.8], [2.8, 7.2], color="#0F172A", lw=2) # Y Spine
ax.plot([6.6, 6.6], [2.8, 7.2], color="#94A3B8", ls=':', lw=1) # Right Spine
ax.plot([1.8, 6.6], [7.2, 7.2], color="#94A3B8", ls=':', lw=1) # Top Spine

# Axis labels & Title
ax.text(4.2, 7.4, "Title: Respon Dosis Pupuk", fontsize=8.5, ha='center', fontweight='bold', color="#1E293B")
ax.text(4.2, 2.2, "X-Axis Label (Dosis NPK kg/pokok)", fontsize=8, ha='center', color="#475569")
ax.text(1.3, 5.0, "Y-Axis Label (Tonase TBS)", fontsize=8, rotation=90, va='center', ha='center', color="#475569")

# Grid & Ticks
for tx in [2.8, 3.8, 4.8, 5.8]:
    ax.plot([tx, tx], [2.7, 2.8], color="#0F172A", lw=1.5) # Major Ticks
    ax.text(tx, 2.5, f"{int((tx-1.8)*2)}", fontsize=7.5, ha='center', color="#334155")
    ax.plot([tx, tx], [2.8, 7.2], color="#F1F5F9", ls='-', lw=0.8, zorder=1) # Grid

# Synthetic scatter points
pts_x = [2.4, 3.1, 3.8, 4.5, 5.2, 5.9]
pts_y = [3.5, 4.2, 5.1, 5.8, 6.4, 6.7]
ax.scatter(pts_x, pts_y, color="#2563EB", s=50, zorder=3, edgecolors='k')
ax.plot(pts_x, pts_y, color="#1D4ED8", lw=1.5, zorder=2)

# Legend Box
leg_box = patches.Rectangle((4.7, 3.3), 1.6, 0.9, fc="#F8FAFC", ec="#CBD5E1", lw=1)
ax.add_patch(leg_box)
ax.text(5.5, 3.75, "Legend\nData Blok", fontsize=7, ha='center', va='center', color="#334155")

# Subplot Axes 2 (Right: Seaborn statistical plot)
ax2_box = patches.FancyBboxPatch((7.8, 1.8), 6.2, 6.5, boxstyle="round,pad=0.15", fc="#EFF6FF", ec="#2563EB", lw=1.8)
ax.add_patch(ax2_box)
ax.text(10.9, 7.8, "Lapisan Abstraksi Seaborn (Statistical Axes)", fontsize=10, fontweight='bold', ha='center', color="#1E40AF")

# Seaborn capabilities card
sb_cards = [
    ("Figure-Level Functions", "sns.relplot(), sns.displot(), sns.catplot()\nMembuat objek FacetGrid mandiri, mengelola multi-subplot secara otomatis."),
    ("Axes-Level Functions", "sns.scatterplot(), sns.histplot(), sns.boxplot()\nMenggambar langsung ke objek Matplotlib Axes yang telah ada (ax=ax)."),
    ("Visualisasi Statistik Otomatis", "Estimasi densitas kernel (KDE), interval kepercayaan (95% CI bootstrap), dan pemetaan palet diskrit/kontinu.")
]
y_sb = 6.8
for c_title, c_desc in sb_cards:
    sc = patches.FancyBboxPatch((8.2, y_sb-0.75), 5.4, 1.15, boxstyle="round,pad=0.08", fc="white", ec="#93C5FD", lw=1)
    ax.add_patch(sc)
    ax.text(8.4, y_sb+0.15, f"• {c_title}:", fontsize=8.5, fontweight='bold', color="#1D4ED8")
    ax.text(8.4, y_sb-0.35, c_desc, fontsize=7.5, color="#1E293B", wrap=True)
    y_sb -= 1.5

# Bottom summary banner
bot_card = patches.FancyBboxPatch((1.2, 0.8), 12.6, 0.7, boxstyle="round,pad=0.08", fc="#FEF3C7", ec="#D97706", lw=1.2)
ax.add_patch(bot_card)
ax.text(7.5, 1.15, "Prinsip Integrasi: Gunakan Seaborn untuk pemodelan statistik cepat, gunakan Matplotlib OO API (fig, ax) untuk kustomisasi presisi publikasi ilmiah.", 
        fontsize=8.5, fontweight='bold', ha='center', va='center', color="#92400E")

plt.tight_layout()
out1 = 'e:/Project Buku/docs/assets/anatomi_arsitektur_matplotlib_dan_seaborn.png'
plt.savefig(out1, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'anatomi_arsitektur_matplotlib_dan_seaborn.png'), dpi=300)
plt.close()
print("Saved:", out1)

# -------------------------------------------------------------
# Diagram 2: Panduan Pemilihan Grafik Ilmiah (Data-to-Viz)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 8), dpi=300)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title("Panduan Pemilihan Grafik Visualisasi Sains Data Agribisnis (Data-to-Viz)", 
             fontsize=13, fontweight='bold', pad=15, color='#0F172A')

categories = [
    (2.0, "1. Distribusi", "#EFF6FF", "#1D4ED8", [
        ("Histogram & KDE", "Menilai simetri, modalitas (unimodal vs bimodal), dan kemencengan"),
        ("Boxplot / Boxenplot", "Mendeteksi pencilan dan perbandingan kuartil multi-kelompok"),
        ("Violin Plot", "Kombinasi boxplot dengan estimasi densitas probabilitas KDE")
    ]),
    (6.0, "2. Relasi / Korelasi", "#F0FDF4", "#15803D", [
        ("Scatter Plot & Regplot", "Mengevaluasi hubungan linier/kurvilinier antar 2 variabel kontinu"),
        ("Heatmap Korelasi", "Inspeksi multikolinieritas matriks fitur numerik secara masif"),
        ("Pairplot Multi-Fitur", "Matriks sebaran berlabel kategori untuk eksplorasi dimensi tinggi")
    ]),
    (10.0, "3. Komparasi Kelompok", "#FEFCE8", "#A16207", [
        ("Barplot dengan CI", "Membandingkan rerata dengan interval kepercayaan 95%"),
        ("Pointplot / Line Chart", "Melihat tren agregat produksi antar afdeling atau waktu"),
        ("Strip / Swarm Plot", "Menampilkan sebaran setiap titik data diskrit tanpa tumpang tindih")
    ]),
    (14.0, "4. Spasial & Komposisi", "#FAF5FF", "#7E22CE", [
        ("Heatmap Grid Spasial", "Peta nilai kelembaban tanah atau NDVI piksel kanopi kebun"),
        ("Stacked Bar Chart", "Proporsi fraksi kematangan TBS (Mentah, Masak, Lewat Masak)"),
        ("Line Deret Waktu", "Dinamika runtun waktu curah hujan dan rata-rata bergerak (SMA)")
    ])
]

for cx, title, bg, border, items in categories:
    h_box = patches.FancyBboxPatch((cx-1.8, 7.3), 3.6, 0.9, boxstyle="round,pad=0.1", fc=border, ec=border, lw=1.5)
    ax.add_patch(h_box)
    ax.text(cx, 7.75, title, fontsize=9.5, fontweight='bold', ha='center', va='center', color='white')
    
    b_box = patches.FancyBboxPatch((cx-1.8, 1.0), 3.6, 6.1, boxstyle="round,pad=0.15", fc=bg, ec=border, lw=1.5)
    ax.add_patch(b_box)
    
    y_pos = 6.3
    for it_name, it_desc in items:
        ibox = patches.FancyBboxPatch((cx-1.65, y_pos-0.6), 3.3, 1.15, boxstyle="round,pad=0.08", fc="white", ec=border, lw=1)
        ax.add_patch(ibox)
        ax.text(cx-1.5, y_pos+0.3, f"• {it_name}:", fontsize=8.5, fontweight='bold', color=border)
        ax.text(cx-1.5, y_pos-0.15, it_desc, fontsize=7.5, color="#1E293B", wrap=True)
        y_pos -= 1.6

# Connectors
for i in range(len(categories)-1):
    x_from = categories[i][0] + 1.8
    x_to = categories[i+1][0] - 1.8
    ax.annotate("", xy=(x_to, 4.2), xytext=(x_from, 4.2), 
                arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#64748B", mutation_scale=18))

# Bottom note
bot = patches.FancyBboxPatch((0.4, 0.2), 15.2, 0.6, boxstyle="round,pad=0.08", fc="#F1F5F9", ec="#475569", lw=1.2, ls=':')
ax.add_patch(bot)
ax.text(8.0, 0.5, "Prinsip Edward Tufte: 'Maksimalkan Rasio Tinta-Data (Data-Ink Ratio). Hilangkan elemen dekoratif yang tidak mengomunikasikan informasi (Chartjunk).'", 
        fontsize=8.5, style='italic', fontweight='bold', ha='center', va='center', color="#334155")

plt.tight_layout()
out2 = 'e:/Project Buku/docs/assets/panduan_pemilihan_grafik_visualisasi_ilmiah.png'
plt.savefig(out2, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'panduan_pemilihan_grafik_visualisasi_ilmiah.png'), dpi=300)
plt.close()
print("Saved:", out2)
