import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('e:/Project Buku/docs/assets', exist_ok=True)
artifact_dir = r'C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11'

# -------------------------------------------------------------
# Diagram 1: Klasifikasi Anomali Data & Strategi Pembersihan
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 8), dpi=300)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title("Klasifikasi Anomali Kualitas Data Perkebunan dan Strategi Pembersihannya", 
             fontsize=13, fontweight='bold', pad=15, color='#0F172A')

cards = [
    (2.0, "1. Nilai Hilang (Missing Values)", "#EFF6FF", "#1D4ED8", [
        ("Mekanisme MCAR", "Hilang acak murni (misal: sinyal telemetri terputus sesaat)"),
        ("Mekanisme MAR", "Hilang terikat variabel lain (sensor mati saat suhu > 40°C)"),
        ("Mekanisme MNAR", "Hilang terikat nilai itu sendiri (alat rusak saat hujan lebat ekstrem)"),
        ("Strategi Solusi", "Imputasi Median Bergerak, KNN Imputer, atau Iterative MICE")
    ]),
    (6.0, "2. Pencilan (Outliers) & Noise", "#FEF2F2", "#B91C1C", [
        ("Pencilan Univariat", "Nilai ekstrem satu variabel (misal kelembaban tanah 99%)"),
        ("Pencilan Multivariat", "Kombinasi anomali (pupuk tinggi tapi NDVI mendekati 0)"),
        ("Penyebab Fisik", "Sensor terendam air, konektor berkarat, spike voltase aki"),
        ("Strategi Solusi", "Metode IQR Tukey, Z-score Robust, Winsorizing, Isolation Forest")
    ]),
    (10.0, "3. Duplikasi & Inkonsistensi", "#FEFCE8", "#A16207", [
        ("Duplikasi Eksak", "Paket data MQTT terkirim ulang 2x akibat latensi jaringan"),
        ("Inkonsistensi Teks", "Variasi penulisan manual ('Afdeling 1', 'AFD-01', 'afd_i')"),
        ("Anomali Format", "Format tanggal rancu (DD/MM/YYYY vs MM/DD/YYYY)"),
        ("Strategi Solusi", "Deduplikasi subset kunci waktu, standarisasi regex teks")
    ]),
    (14.0, "4. Skala & Distribusi Miring", "#F0FDF4", "#15803D", [
        ("Disparitas Skala", "Variabel luas (20-40 Ha) vs curah hujan (100-400 mm)"),
        ("Distribusi Miring", "Data serangan hama skew ke kanan (mayoritas 0, sedikit tinggi)"),
        ("Efek ke Algoritma", "Mendistorsi gradient descent & pembobotan jarak Euclidean"),
        ("Strategi Solusi", "RobustScaler, StandardScaler, Transformasi Log / Yeo-Johnson")
    ])
]

for cx, col_title, bg, border, items in cards:
    # Header box
    h_box = patches.FancyBboxPatch((cx-1.8, 7.3), 3.6, 0.9, boxstyle="round,pad=0.1", fc=border, ec=border, lw=1.5)
    ax.add_patch(h_box)
    ax.text(cx, 7.75, col_title, fontsize=9.5, fontweight='bold', ha='center', va='center', color='white')
    
    # Body box
    b_box = patches.FancyBboxPatch((cx-1.8, 0.8), 3.6, 6.3, boxstyle="round,pad=0.15", fc=bg, ec=border, lw=1.5)
    ax.add_patch(b_box)
    
    y_item = 6.4
    for it_title, it_desc in items:
        ibox = patches.FancyBboxPatch((cx-1.65, y_item-0.55), 3.3, 1.1, boxstyle="round,pad=0.08", fc="white", ec=border, lw=1)
        ax.add_patch(ibox)
        ax.text(cx-1.5, y_item+0.25, f"• {it_title}:", fontsize=8.5, fontweight='bold', color=border)
        ax.text(cx-1.5, y_item-0.15, it_desc, fontsize=7.5, color="#334155", wrap=True)
        y_item -= 1.4

plt.tight_layout()
out1 = 'e:/Project Buku/docs/assets/klasifikasi_anomali_data_dan_strategi_cleaning.png'
plt.savefig(out1, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'klasifikasi_anomali_data_dan_strategi_cleaning.png'), dpi=300)
plt.close()
print("Saved:", out1)

# -------------------------------------------------------------
# Diagram 2: Alur Pipeline Terpadu Pra-Pemrosesan Data Agribisnis
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 7.5), dpi=300)
ax.set_xlim(0, 15)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title("Arsitektur Pipeline Terpadu Pra-Pemrosesan Data Mentah Menuju Model AI Agribisnis", 
             fontsize=13, fontweight='bold', pad=15, color='#0F172A')

pipeline_steps = [
    (1.5, "Tahap 1: Ingesti & Audit", ["Pembacaan multi-sumber", "Inspeksi nullability", "Pengecekan tipe data"], "#EFF6FF", "#1D4ED8"),
    (4.5, "Tahap 2: Deduplikasi & Teks", ["Eliminasi data duplikat", "Standarisasi string regex", "Penyelarasan zona waktu"], "#F0FDF4", "#15803D"),
    (7.5, "Tahap 3: Penanganan Hilang", ["Analisis MCAR/MAR/MNAR", "Imputasi domain-aware", "Penandaan missing indicator"], "#FEFCE8", "#A16207"),
    (10.5, "Tahap 4: Mitigasi Pencilan", ["Deteksi batas IQR / Z", "Winsorizing / kliping", "Audit validitas agronomi"], "#FFF7ED", "#C2410C"),
    (13.5, "Tahap 5: Transformasi Fitur", ["Robust / Standard Scaler", "One-Hot / Target Encoding", "Ekspor fitur siap latih AI"], "#FAF5FF", "#7E22CE")
]

for cx, title, bullets, bg, border in pipeline_steps:
    # Outer frame
    head = patches.FancyBboxPatch((cx-1.25, 7.2), 2.5, 0.9, boxstyle="round,pad=0.1", fc=border, ec=border, lw=1.5)
    ax.add_patch(head)
    ax.text(cx, 7.65, title, fontsize=9, fontweight='bold', ha='center', va='center', color='white')
    
    body = patches.FancyBboxPatch((cx-1.25, 1.4), 2.5, 5.6, boxstyle="round,pad=0.1", fc=bg, ec=border, lw=1.5)
    ax.add_patch(body)
    
    y_b = 6.2
    for b in bullets:
        card = patches.FancyBboxPatch((cx-1.15, y_b-0.5), 2.3, 0.95, boxstyle="round,pad=0.08", fc="white", ec=border, lw=1)
        ax.add_patch(card)
        ax.text(cx, y_b-0.05, b, fontsize=8, ha='center', va='center', color="#1E293B")
        y_b -= 1.6

# Connectors
for i in range(len(pipeline_steps)-1):
    x_from = pipeline_steps[i][0] + 1.25
    x_to = pipeline_steps[i+1][0] - 1.25
    ax.annotate("", xy=(x_to, 4.2), xytext=(x_from, 4.2), 
                arrowprops=dict(arrowstyle="-|>", lw=3, color="#64748B", mutation_scale=20))

# Bottom banner for Scikit-Learn ColumnTransformer
bot_box = patches.FancyBboxPatch((0.25, 0.3), 14.5, 0.75, boxstyle="round,pad=0.1", fc="#F1F5F9", ec="#334155", lw=1.5, ls='--')
ax.add_patch(bot_box)
ax.text(7.5, 0.68, "Enkapsulasi Produksi: Menggunakan sklearn.compose.ColumnTransformer & sklearn.pipeline.Pipeline untuk Mencegah Data Leakage", 
        fontsize=8.5, fontweight='bold', ha='center', va='center', color="#0F172A")

plt.tight_layout()
out2 = 'e:/Project Buku/docs/assets/alur_pipeline_pembersihan_dan_preprocessing.png'
plt.savefig(out2, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'alur_pipeline_pembersihan_dan_preprocessing.png'), dpi=300)
plt.close()
print("Saved:", out2)
