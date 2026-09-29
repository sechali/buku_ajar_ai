import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs('e:/Project Buku/docs/assets', exist_ok=True)
artifact_dir = r'C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11'

# -------------------------------------------------------------
# Diagram 1: Taksonomi Data Science & CRISP-DM
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5), dpi=300)

# Subplot 1: Venn Diagram of Data Science
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-2.2, 2.8)
ax1.axis('off')
ax1.set_title("Venn Diagram Data Science & Domain Agribisnis", fontsize=13, fontweight='bold', pad=15, color='#1A365D')

c1 = plt.Circle((-0.7, 0.7), 1.1, color='#3182CE', alpha=0.35, ec='#1D4ED8', lw=2)
c2 = plt.Circle((0.7, 0.7), 1.1, color='#38A169', alpha=0.35, ec='#15803D', lw=2)
c3 = plt.Circle((0, -0.5), 1.1, color='#D69E2E', alpha=0.35, ec='#B45309', lw=2)

ax1.add_patch(c1)
ax1.add_patch(c2)
ax1.add_patch(c3)

ax1.text(-1.1, 1.3, "Computer Science\n& Software Eng.", fontsize=10, fontweight='bold', ha='center', color='#1E3A8A')
ax1.text(1.1, 1.3, "Matematika &\nStatistika Terapan", fontsize=10, fontweight='bold', ha='center', color='#14532D')
ax1.text(0, -1.2, "Domain Knowledge\n(Agribisnis, Sawit, Kehutanan)", fontsize=10, fontweight='bold', ha='center', color='#78350F')

# Overlaps
ax1.text(0, 1.0, "Machine\nLearning", fontsize=9, fontweight='bold', ha='center', va='center', color='#0F172A')
ax1.text(-0.65, 0.05, "Software\nDevelopment", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1E293B')
ax1.text(0.65, 0.05, "Statistik\nTradisional", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1E293B')

# Center intersection
ax1.text(0, 0.35, "DATA SCIENCE\n(AI Agribisnis)", fontsize=10, fontweight='bold', ha='center', va='center', 
         bbox=dict(boxstyle="round,pad=0.3", fc="#FEF08A", ec="#CA8A04", lw=1.5), color='#854D0E')

# Subplot 2: CRISP-DM Cycle Flowchart
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title("Siklus Hidup Data Science: Kerangka Kerja CRISP-DM", fontsize=13, fontweight='bold', pad=15, color='#1A365D')

stages = [
    (5.0, 8.8, "1. Business Understanding\n(Pemahaman Masalah Kebun/PKS)", "#DBEAFE", "#1E40AF"),
    (8.2, 6.4, "2. Data Understanding\n(Eksplorasi Sensor/NDVI)", "#DCFCE7", "#166534"),
    (8.2, 3.2, "3. Data Preparation\n(Cleaning & Imputasi Hilang)", "#FEF9C3", "#854D0E"),
    (5.0, 1.0, "4. Modeling\n(Regresi/Klasifikasi/DL)", "#FFEDD5", "#9A3412"),
    (1.8, 3.2, "5. Evaluation\n(Validasi Metrik & Bisnis)", "#FCE7F3", "#9D174D"),
    (1.8, 6.4, "6. Deployment\n(Integrasi Dashboard/IoT)", "#EDE9FE", "#5B21B6")
]

for x, y, text, bg, border in stages:
    box = patches.FancyBboxPatch((x-1.5, y-0.6), 3.0, 1.2, boxstyle="round,pad=0.15", fc=bg, ec=border, lw=2)
    ax2.add_patch(box)
    ax2.text(x, y, text, fontsize=9, fontweight='bold', ha='center', va='center', color=border)

# Connectors for cycle
arrow_props = dict(arrowstyle="->", lw=2, color="#475569", connectionstyle="arc3,rad=-0.15")
ax2.annotate("", xy=(7.2, 7.0), xytext=(6.3, 8.3), arrowprops=arrow_props)
ax2.annotate("", xy=(8.2, 4.0), xytext=(8.2, 5.6), arrowprops=dict(arrowstyle="<->", lw=2, color="#475569"))
ax2.annotate("", xy=(6.3, 1.6), xytext=(7.2, 2.6), arrowprops=dict(arrowstyle="->", lw=2, color="#475569", connectionstyle="arc3,rad=-0.15"))
ax2.annotate("", xy=(4.0, 1.6), xytext=(5.0, 2.4), arrowprops=dict(arrowstyle="<->", lw=2, color="#DC2626")) # Iterasi modeling & data prep
ax2.annotate("", xy=(2.8, 2.6), xytext=(3.7, 1.6), arrowprops=dict(arrowstyle="->", lw=2, color="#475569", connectionstyle="arc3,rad=-0.15"))
ax2.annotate("", xy=(1.8, 5.6), xytext=(1.8, 4.0), arrowprops=dict(arrowstyle="->", lw=2, color="#475569"))
ax2.annotate("", xy=(3.7, 8.3), xytext=(2.8, 7.0), arrowprops=dict(arrowstyle="->", lw=2, color="#475569", connectionstyle="arc3,rad=-0.15"))

# Center core data icon
center_box = patches.FancyBboxPatch((3.8, 4.2), 2.4, 1.2, boxstyle="round,pad=0.2", fc="#F1F5F9", ec="#334155", lw=2, ls='--')
ax2.add_patch(center_box)
ax2.text(5.0, 4.8, "DATA\nPERKEBUNAN", fontsize=10, fontweight='bold', ha='center', va='center', color="#0F172A")

plt.tight_layout()
out_path1 = 'e:/Project Buku/docs/assets/taksonomi_data_science_dan_crisp_dm.png'
plt.savefig(out_path1, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'taksonomi_data_science_dan_crisp_dm.png'), dpi=300)
plt.close()
print("Saved:", out_path1)

# -------------------------------------------------------------
# Diagram 2: Arsitektur Pipeline Data Agribisnis End-to-End
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 7.5), dpi=300)
ax.set_xlim(0, 15)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title("Arsitektur Pipeline Data Agribisnis dan Pertanian Presisi Terintegrasi", fontsize=14, fontweight='bold', pad=20, color='#0F172A')

# 5 Columns of pipeline
cols = [
    (1.5, "1. Ingesti Multi-Sumber", ["Sensor IoT Cuaca & Lengas", "Citra Multispektral Drone", "ERP Timbangan PKS", "Logbook Panen Afdeling"], "#EFF6FF", "#1D4ED8"),
    (4.5, "2. Validasi & Cleaning", ["Pembersihan Noise & Spike", "Imputasi Missing Values", "Penyelarasan Stempel Waktu", "Deteksi Outlier Timbangan"], "#F0FDF4", "#15803D"),
    (7.5, "3. Transformasi & Fitur", ["Ekstraksi Indeks NDVI/NDRE", "Agregasi Curah Hujan Bulanan", "Normalisasi Min-Max/Z-Score", "Enkoding Kategori Blok Kebun"], "#FEFCE8", "#A16207"),
    (10.5, "4. Pemodelan & AI", ["Regresi Produksi TBS Sawit", "Klasifikasi Kematangan Buah", "Klastering Kesuburan Tanah", "Model Deteksi Anomali Hama"], "#FFF7ED", "#C2410C"),
    (13.5, "5. Aksi & Deployment", ["Dashboard Operasional Estate", "Peringatan Dini Penyakit", "Rekomendasi Dosis Pupuk", "Optimasi Jadwal Armada Truk"], "#FAF5FF", "#7E22CE")
]

for cx, col_title, items, bg, border in cols:
    # Header card
    head_box = patches.FancyBboxPatch((cx-1.25, 7.2), 2.5, 0.9, boxstyle="round,pad=0.1", fc=border, ec=border, lw=1.5)
    ax.add_patch(head_box)
    ax.text(cx, 7.65, col_title, fontsize=9.5, fontweight='bold', ha='center', va='center', color='white')
    
    # Body card
    body_box = patches.FancyBboxPatch((cx-1.25, 1.2), 2.5, 5.7, boxstyle="round,pad=0.1", fc=bg, ec=border, lw=1.5)
    ax.add_patch(body_box)
    
    # Items
    y_start = 6.2
    for item in items:
        item_box = patches.FancyBboxPatch((cx-1.15, y_start-0.45), 2.3, 0.9, boxstyle="round,pad=0.08", fc='white', ec=border, lw=1)
        ax.add_patch(item_box)
        ax.text(cx, y_start, item, fontsize=8.5, ha='center', va='center', color='#1E293B', wrap=True)
        y_start -= 1.3

# Connectors between columns
for i in range(len(cols)-1):
    x_from = cols[i][0] + 1.25
    x_to = cols[i+1][0] - 1.25
    ax.annotate("", xy=(x_to, 4.2), xytext=(x_from, 4.2), 
                arrowprops=dict(arrowstyle="-|>", lw=3, color="#64748B", mutation_scale=20))

# Bottom banner for data governance
gov_box = patches.FancyBboxPatch((0.25, 0.2), 14.5, 0.65, boxstyle="round,pad=0.1", fc="#F1F5F9", ec="#475569", lw=1.5, ls=':')
ax.add_patch(gov_box)
ax.text(7.5, 0.52, "Fondasi Pendukung: Tata Kelola Data (Data Governance) • Keamanan Data Kebun • Pemantauan Performa Model (MLOps)", 
        fontsize=9, fontweight='bold', ha='center', va='center', color="#334155")

plt.tight_layout()
out_path2 = 'e:/Project Buku/docs/assets/arsitektur_pipeline_data_agribisnis.png'
plt.savefig(out_path2, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'arsitektur_pipeline_data_agribisnis.png'), dpi=300)
plt.close()
print("Saved:", out_path2)
