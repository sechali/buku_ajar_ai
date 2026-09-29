import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs('e:/Project Buku/docs/assets', exist_ok=True)
artifact_dir = r'C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11'

# -------------------------------------------------------------
# Diagram 1: Mekanisme I/O Parsing CSV dan Excel di Pandas
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 7.5), dpi=300)
ax.set_xlim(0, 15)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title("Arsitektur Alur Pembacaan Data I/O: Dari Berkas Disk ke Pandas DataFrame", 
             fontsize=13, fontweight='bold', pad=15, color='#0F172A')

steps = [
    (1.8, "1. Berkas di Media Disk", "#EFF6FF", "#1D4ED8", [
        ("Format CSV Teks", "Aliran byte biner dengan pemisah (koma, titik koma, tab)"),
        ("Format Excel XLSX", "Arsip ZIP XML terkompresi multi-lembar"),
        ("Tantangan Enkoding", "UTF-8 vs Latin-1 vs CP1252 (Windows)")
    ]),
    (5.6, "2. Mesin Parser I/O", "#F0FDF4", "#15803D", [
        ("C Parser (Default)", "Eksekusi kode mesin C cepat, hemat memori"),
        ("Python Parser", "Fleksibel untuk regex pemisah rumit, lebih lambat"),
        ("PyArrow Engine", "Multi-threaded parsing modern berkecepatan tinggi"),
        ("Excel Engine", "Pustaka 'openpyxl' (XLSX) / 'calamine' (C Rust)")
    ]),
    (9.4, "3. Konversi Tipe Data", "#FEFCE8", "#A16207", [
        ("Inferensi Skema Otomatis", "Menganalisis sampel baris untuk menebak tipe"),
        ("Deklarasi dtype Eksplisit", "Mencegah alokasi memori berlebih float64/object"),
        ("Penanganan Tanggal", "Mengonversi string ISO ke DatetimeIndex C")
    ]),
    (13.2, "4. Memori RAM DataFrame", "#FAF5FF", "#7E22CE", [
        ("Struktur BlockManager", "Penyekatan kolom numerik homogen kontigu"),
        ("Indeks Baris C Cepat", "Pencarian hash map O(1)"),
        ("Siap untuk Pemodelan", "Data tabular siap dikonsumsi AI pipeline")
    ])
]

for cx, title, bg, border, items in steps:
    # Outer frame
    head = patches.FancyBboxPatch((cx-1.6, 7.2), 3.2, 0.9, boxstyle="round,pad=0.1", fc=border, ec=border, lw=1.5)
    ax.add_patch(head)
    ax.text(cx, 7.65, title, fontsize=9.5, fontweight='bold', ha='center', va='center', color='white')
    
    body = patches.FancyBboxPatch((cx-1.6, 1.2), 3.2, 5.8, boxstyle="round,pad=0.15", fc=bg, ec=border, lw=1.5)
    ax.add_patch(body)
    
    y_b = 6.2
    for b_title, b_desc in items:
        card = patches.FancyBboxPatch((cx-1.45, y_b-0.55), 2.9, 1.15, boxstyle="round,pad=0.08", fc="white", ec=border, lw=1)
        ax.add_patch(card)
        ax.text(cx-1.3, y_b+0.25, f"• {b_title}:", fontsize=8.5, fontweight='bold', color=border)
        ax.text(cx-1.3, y_b-0.2, b_desc, fontsize=7.5, color="#1E293B", wrap=True)
        y_b -= 1.45

# Connecting arrows
for i in range(len(steps)-1):
    x_from = steps[i][0] + 1.6
    x_to = steps[i+1][0] - 1.6
    ax.annotate("", xy=(x_to, 4.2), xytext=(x_from, 4.2), 
                arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#64748B", mutation_scale=18))

# Bottom warning banner
bot_box = patches.FancyBboxPatch((0.2, 0.3), 14.6, 0.65, boxstyle="round,pad=0.08", fc="#FFF1F2", ec="#E11D48", lw=1.2, ls=':')
ax.add_patch(bot_box)
ax.text(7.5, 0.62, "Peringatan Rekayasa: Menentukan argumen 'dtype' dan 'usecols' saat membaca CSV dapat menghemat hingga 80% RAM dan melipatgandakan kecepatan parsing.", 
        fontsize=8.5, fontweight='bold', ha='center', va='center', color="#9F1239")

plt.tight_layout()
out1 = 'e:/Project Buku/docs/assets/mekanisme_io_parsing_csv_dan_excel_pandas.png'
plt.savefig(out1, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'mekanisme_io_parsing_csv_dan_excel_pandas.png'), dpi=300)
plt.close()
print("Saved:", out1)

# -------------------------------------------------------------
# Diagram 2: Strategi Ingesti Dataset Besar (Chunking vs Parquet)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), dpi=300)

# Subplot 1: Chunking Iterator Architecture
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title("Strategi Pembacaan Bongkahan (Chunking Iterator)", fontsize=11, fontweight='bold', pad=12, color='#1E40AF')

# Giant file on disk
disk_file = patches.FancyBboxPatch((0.5, 2.0), 2.8, 6.5, boxstyle="round,pad=0.15", fc="#F1F5F9", ec="#475569", lw=2)
ax1.add_patch(disk_file)
ax1.text(1.9, 8.0, "Berkas CSV Raksasa\n(Ukuran: 10 GB)\nMelebihi Kapasitas RAM!", fontsize=8.5, fontweight='bold', ha='center', color="#0F172A")

chunks = [("Bongkahan 1\n(50.000 baris)", 6.5), ("Bongkahan 2\n(50.000 baris)", 5.0), ("Bongkahan 3\n(50.000 baris)", 3.5)]
for ctext, cy in chunks:
    cbox = patches.Rectangle((0.8, cy-0.5), 2.2, 0.9, fc="#DBEAFE", ec="#2563EB", lw=1.2)
    ax1.add_patch(cbox)
    ax1.text(1.9, cy-0.05, ctext, fontsize=8, ha='center', color="#1E40AF")

# Processing pipeline in memory
ram_box = patches.FancyBboxPatch((6.0, 2.0), 3.5, 6.5, boxstyle="round,pad=0.15", fc="#ECFDF5", ec="#059669", lw=2)
ax1.add_patch(ram_box)
ax1.text(7.75, 8.0, "Memori RAM Efisien\n(Hanya Menampung\nSatu Chunk Sekaligus)", fontsize=8.5, fontweight='bold', ha='center', color="#065F46")

ax1.annotate("", xy=(6.0, 5.0), xytext=(3.3, 5.0), arrowprops=dict(arrowstyle="-|>", lw=3, color="#2563EB", mutation_scale=20))
ax1.text(4.65, 5.4, "chunksize=50000\n(Iterator)", fontsize=8, fontweight='bold', ha='center', color="#2563EB")

ram_proc = patches.Rectangle((6.3, 4.2), 2.9, 1.8, fc="white", ec="#10B981", lw=1.5)
ax1.add_patch(ram_proc)
ax1.text(7.75, 5.3, "Proses & Agregasi:\n• Filter Anomali\n• Hitung Total & Rerata\n• Buang Chunk Lama", fontsize=8, ha='center', color="#047857")

ax1.text(5.0, 0.8, "RAM Tetap Konstan Stabil (< 500 MB) Meski Data 10+ GB!", 
         fontsize=8.5, fontweight='bold', ha='center', color="#047857",
         bbox=dict(boxstyle="round,pad=0.2", fc="#D1FAE5", ec="#10B981"))

# Subplot 2: CSV vs Parquet Benchmark Chart
ax2.set_title("Komparasi Format: CSV Teks vs Apache Parquet Biner", fontsize=11, fontweight='bold', pad=12, color='#0F172A')

formats = ['CSV Standar\n(Uncompressed)', 'CSV Terkompresi\n(GZIP)', 'Apache Parquet\n(Snappy Columnar)']
sizes_mb = [520.0, 115.0, 48.0]
read_times_sec = [14.8, 18.2, 0.85]

x_pos = np.arange(len(formats))
width = 0.35

rects1 = ax2.bar(x_pos - width/2, sizes_mb, width, label='Ukuran Disk (MB)', color='#F87171', edgecolor='#991B1B')
rects2 = ax2.bar(x_pos + width/2, [t * 25 for t in read_times_sec], width, label='Waktu Baca (Detik x25)', color='#60A5FA', edgecolor='#1D4ED8')

ax2.set_ylabel('Skala Metrik (MB / Relatif)', fontsize=9, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(formats, fontsize=8.5, fontweight='bold')
ax2.legend(loc='upper right', fontsize=8.5)
ax2.grid(True, linestyle=':', alpha=0.5, axis='y')

# Annotations
ax2.text(0 - width/2, 530, "520 MB", ha='center', fontsize=8, fontweight='bold')
ax2.text(0 + width/2, 380, "14.8 s", ha='center', fontsize=8, fontweight='bold')

ax2.text(2 - width/2, 60, "48 MB\n(-90%)", ha='center', fontsize=8, fontweight='bold', color="#047857")
ax2.text(2 + width/2, 35, "0.85 s\n(17x Cepat)", ha='center', fontsize=8, fontweight='bold', color="#0369A1")

plt.tight_layout()
out2 = 'e:/Project Buku/docs/assets/strategi_ingesti_dataset_besar_chunking.png'
plt.savefig(out2, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'strategi_ingesti_dataset_besar_chunking.png'), dpi=300)
plt.close()
print("Saved:", out2)
