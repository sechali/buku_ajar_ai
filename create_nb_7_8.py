import json

cells = []

def add_md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(text):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.split("\n")]
    })

add_md(r"""# AI Modul 7.8: Praktikum K-Means Clustering

**Mata Kuliah:** Kecerdasan Buatan & Pembelajaran Mesin Terapan  
**Institusi:** Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Studi Kasus:** Zonasi Otomatis Kesuburan Lahan Kelapa Sawit Berbasis Data Sensor Multi-Nutrien Tanah Menggunakan K-Means++ dan Evaluasi Silhouette

---

### Capaian Pembelajaran Praktikum
1. Mampu mengimplementasikan algoritma K-Means dengan inisialisasi cerdas K-Means++ untuk data tanpa label (*Unsupervised Learning*).
2. Mampu menerapkan *pipeline* standardisasi data (`StandardScaler`) guna mencegah distorsi jarak Euclidean pada multi-nutrien tanah.
3. Mampu menentukan jumlah klaster optimal ($K$) secara objektif menggunakan Metode Siku (*Elbow Method*) dan Analisis Skor Silhouette.
4. Mampu mengekstraksi titik pusat klaster (*centroids*), mentransformasikannya ke skala asli agronomi, dan menyusun peta rekomendasi pemupukan presisi.""")

add_md("## 1. Import Pustaka & Konfigurasi Lingkungan")

add_code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples

# Pengaturan visualisasi
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 120

print("[OK] Seluruh pustaka K-Means Clustering berhasil dimuat!")""")

add_md(r"""## 2. Pembangkitan Dataset Survei Kesuburan Tanah Perkebunan

Data hasil uji laboratorium dari 500 titik sampel tanah komposit kedalaman 0-30 cm:
- `N_Total_g_kg`: Nitrogen total tanah ($0.8 - 3.5\text{ g/kg}$)
- `P_Tersedia_ppm`: Fosfor tersedia Bray-II ($4.0 - 35.0\text{ ppm}$)
- `K_dd_cmol_kg`: Kalium dapat dipertukarkan ($0.10 - 1.20\text{ cmol/kg}$)
- `pH_Tanah`: Derajat keasaman tanah ($3.8 - 6.2$)
- `Bahan_Organik_%`: Persentase C-Organik tanah ($1.2 - 6.5\%$)""")

add_code("""np.random.seed(42)
n_titik = 500

# Pembangkitan 3 zona alami lapangan:
# Zona 1: Gambut Masam / Defisiensi Kalium Kritis (200 titik)
# Zona 2: Mineral Podsolik Sedang (200 titik)
# Zona 3: Aluvial Lembah Subur Tinggi (100 titik)

z1 = np.random.normal([1.2, 8.0, 0.20, 4.1, 5.2], [0.15, 1.5, 0.04, 0.2, 0.4], (200, 5))
z2 = np.random.normal([1.8, 16.0, 0.45, 5.0, 2.8], [0.20, 2.5, 0.06, 0.3, 0.3], (200, 5))
z3 = np.random.normal([2.6, 28.0, 0.85, 5.8, 3.8], [0.25, 3.0, 0.08, 0.3, 0.4], (100, 5))

X_tanah = np.vstack([z1, z2, z3])
np.random.shuffle(X_tanah)

fitur_tanah = ['N_Total_g_kg', 'P_Tersedia_ppm', 'K_dd_cmol_kg', 'pH_Tanah', 'Bahan_Organik_%']
df_tanah = pd.DataFrame(X_tanah, columns=fitur_tanah)

print(f"Dataset berhasil dibuat: {df_tanah.shape[0]} titik sampel")
df_tanah.head()""")

add_md("## 3. Eksplorasi Visual: Matriks Korelasi & Distribusi Nutrien")

add_code("""fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Heatmap Korelasi Pearson
corr = df_tanah.corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='YlGnBu', ax=axes[0])
axes[0].set_title('Matriks Korelasi Parameter Kimia Tanah', fontweight='bold')

# Scatter Plot N vs K Mentah
axes[1].scatter(df_tanah['N_Total_g_kg'], df_tanah['K_dd_cmol_kg'], color='#1565c0', alpha=0.6, s=35)
axes[1].set_title('Distribusi Mentah: Nitrogen Total vs Kalium Tertukar', fontweight='bold')
axes[1].set_xlabel('N Total (g/kg)')
axes[1].set_ylabel('K-dd (cmol/kg)')
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()""")

add_md(r"""## 4. Standardisasi Fitur dengan StandardScaler

Standardisasi sangat wajib karena skala parameter hara berbeda jauh (P mencapai puluhan ppm, sedangkan K berupa pecahan desimal).""")

add_code("""scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_tanah)

print("=== STATISTIK SETELAH STANDARDISASI ===")
print(f"Rata-rata fitur (Mean)  : {np.mean(X_scaled, axis=0).round(4)}")
print(f"Simpangan baku (Std Dev): {np.std(X_scaled, axis=0).round(4)}")""")

add_md(r"""## 5. Pencarian Jumlah Klaster Optimal: Metode Siku (Elbow Method)""")

add_code("""k_range = range(1, 9)
wcss = []

for k in k_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    km.fit(X_scaled)
    wcss.append(km.inertia_)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(k_range, wcss, 'o-', color='#1565c0', linewidth=2.5, markersize=7)
ax.axvline(3, color='#d32f2f', linestyle='--', linewidth=1.8, label='Titik Siku (Elbow Point: K = 3)')
ax.set_title('Metode Siku (Elbow Method): Evaluasi Inersia WCSS vs K', fontweight='bold')
ax.set_xlabel('Jumlah Klaster (K)')
ax.set_ylabel('Within-Cluster Sum of Squares (WCSS)')
ax.set_xticks(k_range)
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

add_md(r"""## 6. Validasi Kerapatan & Keterpisahan: Analisis Skor Silhouette""")

add_code("""k_sil_range = range(2, 9)
sil_scores = []

for k in k_sil_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    sil_scores.append(score)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(k_sil_range, sil_scores, color='#2e7d32', edgecolor='black', alpha=0.8, width=0.55)
ax.axhline(max(sil_scores), color='#d32f2f', linestyle=':', label=f'Skor Tertinggi (K=3: {max(sil_scores):.4f})')
ax.set_title('Evaluasi Skor Rata-rata Silhouette vs Jumlah Klaster (K)', fontweight='bold')
ax.set_xlabel('Jumlah Klaster (K)')
ax.set_ylabel('Skor Rata-rata Silhouette')
ax.set_xticks(k_sil_range)
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()

for k, s in zip(k_sil_range, sil_scores):
    print(f"K = {k}: Skor Silhouette = {s:.4f}")""")

add_md(r"""## 7. Pelatihan Model K-Means Final ($K=3$) & Profil Centroid""")

add_code("""kmeans_final = KMeans(n_clusters=3, init='k-means++', n_init=15, random_state=42)
df_tanah['Klaster'] = kmeans_final.fit_predict(X_scaled)

# Transformasi balik centroid ke skala asli agronomi
centroid_scaled = kmeans_final.cluster_centers_
centroid_asli = scaler.inverse_transform(centroid_scaled)

df_centroid = pd.DataFrame(centroid_asli, columns=fitur_tanah)
df_centroid['Jumlah_Titik'] = df_tanah['Klaster'].value_counts().sort_index().values

# Pemetaan nama zona agronomi berdasarkan kadar kalium
k_order = df_centroid['K_dd_cmol_kg'].argsort()
zona_names = {
    k_order.iloc[0]: 'Zona 1: Kritis Defisiensi Kalium',
    k_order.iloc[1]: 'Zona 2: Sedang (Mineral Reguler)',
    k_order.iloc[2]: 'Zona 3: Subur Prima'
}
df_tanah['Nama_Zona'] = df_tanah['Klaster'].map(zona_names)

print("=== PROFIL CENTROID HARA TANAH (SKALA ASLI LAPANGAN) ===")
print(df_centroid.round(3).to_string())
print(f"\\nSkor Silhouette Model Final: {silhouette_score(X_scaled, df_tanah['Klaster']):.4f}")""")

add_md("## 8. Visualisasi Spasial 2D Zonasi Kesuburan Lahan")

add_code("""fig, ax = plt.subplots(figsize=(9, 5.5))
palette_colors = {'Zona 1: Kritis Defisiensi Kalium': '#d32f2f', 
                  'Zona 2: Sedang (Mineral Reguler)': '#f57c00', 
                  'Zona 3: Subur Prima': '#2e7d32'}

for nama, col in palette_colors.items():
    subset = df_tanah[df_tanah['Nama_Zona'] == nama]
    ax.scatter(subset['N_Total_g_kg'], subset['K_dd_cmol_kg'], label=nama, color=col, alpha=0.65, s=40)

# Plot Posisi Centroid
ax.scatter(centroid_asli[:, 0], centroid_asli[:, 2], color='black', s=220, marker='X', linewidths=2, label='Titik Centroid (Rata-rata Zona)')

ax.set_title('Peta Partisi Zonasi Kesuburan Tanah Kelapa Sawit (K-Means K=3)', fontweight='bold')
ax.set_xlabel('Nitrogen Total (g/kg)')
ax.set_ylabel('Kalium Tertukar / K-dd (cmol/kg)')
ax.legend(loc='upper left')
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

add_md(r"""## 9. Penerapan Lapangan: Rekomendasi Dosis Pemupukan Terzonasi (VRF)""")

add_code("""tabel_rekomendasi = pd.DataFrame([
    {
        'Zona': 'Zona 1: Kritis Defisiensi Kalium',
        'Ciri Fisiologis': 'K < 0.3 cmol/kg, Gambut Masam, C-Organik Tinggi',
        'Rekomendasi Urea': '1.2 kg / pohon / tahun',
        'Rekomendasi MOP (KCl)': '3.5 kg / pohon / tahun (Dosis Ekstra)',
        'Dolomit (Kapur)': '2.0 kg / pohon / tahun'
    },
    {
        'Zona': 'Zona 2: Sedang (Mineral Reguler)',
        'Ciri Fisiologis': 'Hara Seimbang, pH Sedang (~5.0)',
        'Rekomendasi Urea': '2.0 kg / pohon / tahun',
        'Rekomendasi MOP (KCl)': '2.2 kg / pohon / tahun',
        'Dolomit (Kapur)': '1.0 kg / pohon / tahun'
    },
    {
        'Zona': 'Zona 3: Subur Prima',
        'Ciri Fisiologis': 'Aluvial Lembah, N & K Tinggi, pH > 5.5',
        'Rekomendasi Urea': '0.8 kg / pohon / tahun (Pangkas 60%)',
        'Rekomendasi MOP (KCl)': '1.5 kg / pohon / tahun',
        'Dolomit (Kapur)': '0.5 kg / pohon / tahun'
    }
])

print("=== REKOMENDASI PEMUPUKAN PRESISI BERBASIS KLASTER TANAH ===")
print(tabel_rekomendasi.to_string(index=False))""")

add_md(r"""## 10. Simulasi Penugasan Titik Sampel Tanah Baru

Menguji sampel tanah baru dari perluasan blok afdeling untuk menentukan zonanya.""")

add_code("""sampel_baru = pd.DataFrame([
    # Titik A: N rendah, K sangat rendah, pH 4.0 (Gambut Kritis)
    {'N_Total_g_kg': 1.15, 'P_Tersedia_ppm': 7.5, 'K_dd_cmol_kg': 0.18, 'pH_Tanah': 4.0, 'Bahan_Organik_%': 5.4},
    # Titik B: N tinggi, K tinggi, pH 5.9 (Lembah Subur)
    {'N_Total_g_kg': 2.75, 'P_Tersedia_ppm': 29.0, 'K_dd_cmol_kg': 0.90, 'pH_Tanah': 5.85, 'Bahan_Organik_%': 3.9}
])

sampel_baru_scaled = scaler.transform(sampel_baru)
klaster_pred = kmeans_final.predict(sampel_baru_scaled)

print("=== HASIL PENUGASAN ZONASI TITIK TANAH BARU ===")
for i in range(len(sampel_baru)):
    nama_z = zona_names[klaster_pred[i]]
    print(f"Titik #{i+1}: Ditugaskan ke {nama_z.upper()}")""")

add_md(r"""## 11. Tugas Mandiri & Eksplorasi Mahasiswa

1. **Eksplorasi Inisialisasi**: Latih model K-Means dengan inisialisasi acak murni (`init='random'`) sebanyak 10 kali eksperimen berbeda. Apakah nilai WCSS selalu sama atau berfluktuasi? Bandingkan kestabilannya terhadap `init='k-means++'`!
2. **Uji Dampak Tanpa Standardisasi**: Lakukan klasterisasi langsung pada `df_tanah[fitur_tanah]` tanpa `StandardScaler`. Perhatikan centroid yang dihasilkan. Parameter manakah yang mendominasi pembentukan klaster? Mengapa hal tersebut berbahaya bagi agronomi?
3. **Analisis Transisi ke Reduksi Dimensi**: Dalam survei tanah modern dengan 20 variabel hara (termasuk mikro Cu, Zn, B, Fe), kita kesulitan memvisualisasikan data di grafik 2D. Jelaskan bagaimana metode Principal Component Analysis (PCA - AI Modul 7.9) dapat dikombinasikan dengan K-Means!""")

notebook_path = r"e:\Project Buku\notebooks\part-07\AI_Modul_7.8_Praktikum_K_Means_Clustering.ipynb"
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump({
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }, f, indent=1)

print(f"[OK] Notebook successfully created at {notebook_path}")
