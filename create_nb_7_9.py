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

add_md(r"""# AI Modul 7.9: Praktikum Principal Component Analysis (PCA)

**Mata Kuliah:** Kecerdasan Buatan & Pembelajaran Mesin Terapan  
**Institusi:** Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Studi Kasus:** Kompresi Dimensi Spektral Multi-Sensor Drone Kanopi Kelapa Sawit Menggunakan Principal Component Analysis (PCA) dan Visualisasi Biplot 2D

---

### Capaian Pembelajaran Praktikum
1. Mampu mengimplementasikan algoritma Principal Component Analysis menggunakan pustaka Scikit-Learn untuk reduksi dimensi tanpa pengawas.
2. Mampu menerapkan standardisasi data (`StandardScaler`) sebagai prasyarat mutlak aljabar linier PCA.
3. Mampu menentukan jumlah komponen optimal melalui visualisasi *Scree Plot* dan evaluasi *Cumulative Explained Variance Ratio*.
4. Mampu menyusun dan menginterpretasikan grafik *Biplot 2D* (interseksi skor sampel dan vektor bobot *loadings*) serta mengintegrasikannya dengan K-Means.""")

add_md("## 1. Import Pustaka & Konfigurasi Lingkungan")

add_code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Pengaturan visualisasi
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 120

print("[OK] Seluruh pustaka Principal Component Analysis berhasil dimuat!")""")

add_md(r"""## 2. Pembangkitan Dataset Spektral Drone Kanopi Sawit

Data penginderaan jauh 600 petak sampel kelapa sawit dengan 8 variabel spektral dan indeks vegetasi:
- `B1_Blue`: Reflektansi pita biru (450 nm)
- `B2_Green`: Reflektansi pita hijau (560 nm)
- `B3_Red`: Reflektansi pita merah (650 nm)
- `B4_RedEdge`: Reflektansi pita tepi merah (705 nm)
- `B5_NIR`: Reflektansi inframerah dekat (842 nm)
- `NDVI`: Normalized Difference Vegetation Index
- `NDRE`: Normalized Difference Red Edge Index
- `GNDVI`: Green Normalized Difference Vegetation Index""")

add_code("""np.random.seed(42)
n_samples = 600

# 3 Kelompok Fisiologis Kanopi:
# 1: Kanopi Sehat Rimbun (250 sampel)
# 2: Cekaman Hara N / Menguning (200 sampel)
# 3: Defisiensi Air / Kering Kritis (150 sampel)

b_nir_s = np.random.normal(0.65, 0.05, 250)
b_red_s = np.random.normal(0.08, 0.02, 250)
b_re_s = np.random.normal(0.42, 0.04, 250)

b_nir_h = np.random.normal(0.50, 0.06, 200)
b_red_h = np.random.normal(0.18, 0.03, 200)
b_re_h = np.random.normal(0.28, 0.03, 200)

b_nir_a = np.random.normal(0.35, 0.05, 150)
b_red_a = np.random.normal(0.26, 0.04, 150)
b_re_a = np.random.normal(0.20, 0.03, 150)

nir = np.concatenate([b_nir_s, b_nir_h, b_nir_a])
red = np.concatenate([b_red_s, b_red_h, b_red_a])
re = np.concatenate([b_re_s, b_re_h, b_re_a])
blue = 0.5 * red + np.random.normal(0.04, 0.01, n_samples)
green = 0.8 * re + np.random.normal(0.06, 0.02, n_samples)

ndvi = (nir - red) / (nir + red + 1e-6)
ndre = (nir - re) / (nir + re + 1e-6)
gndvi = (nir - green) / (nir + green + 1e-6)

df_spektral = pd.DataFrame({
    'B1_Blue': blue,
    'B2_Green': green,
    'B3_Red': red,
    'B4_RedEdge': re,
    'B5_NIR': nir,
    'NDVI': ndvi,
    'NDRE': ndre,
    'GNDVI': gndvi
})

print(f"Dataset berhasil dibuat: {df_spektral.shape[0]} baris x {df_spektral.shape[1]} kolom")
df_spektral.head()""")

add_md("## 3. Eksplorasi Visual: Multikolinieritas Tinggi Antar-Pita Spektral")

add_code("""fig, ax = plt.subplots(figsize=(8, 6.5))
corr_matrix = df_spektral.corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
ax.set_title('Matriks Korelasi Antar-Pita Spektral Drone (Bukti Multikolinieritas)', fontweight='bold')
plt.tight_layout()
plt.show()""")

add_md(r"""## 4. Standardisasi Fitur dengan StandardScaler

Memastikan setiap pita spektral memiliki mean = 0 dan varians = 1 sebelum analisis nilai eigen.""")

add_code("""scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_spektral)

print("=== VERIFIKASI HASIL STANDARDISASI FITUR ===")
print(f"Mean tiap fitur : {np.mean(X_scaled, axis=0).round(4)}")
print(f"Std Dev fitur   : {np.std(X_scaled, axis=0).round(4)}")""")

add_md("## 5. Pelatihan Model PCA Penuh (8 Komponen) & Nilai Eigen")

add_code("""pca_full = PCA(n_components=8, random_state=42)
pca_full.fit(X_scaled)

evr = pca_full.explained_variance_ratio_ * 100
cum_evr = np.cumsum(evr)
eigenvalues = pca_full.explained_variance_

df_pca_summary = pd.DataFrame({
    'Komponen': [f'PC{i+1}' for i in range(8)],
    'Nilai Eigen (Lambda)': eigenvalues,
    'Varians Terjelaskan (%)': evr,
    'Varians Kumulatif (%)': cum_evr
})

print("=== TABEL DEKOMPOSISI NILAI EIGEN & RETENSI VARIAN ===")
print(df_pca_summary.round(3).to_string(index=False))""")

add_md("## 6. Visualisasi Scree Plot & Kriteria Retensi Dimensi")

add_code("""fig, ax = plt.subplots(figsize=(9, 4.8))

n_comps = np.arange(1, 9)
ax.bar(n_comps, evr, color='#1565c0', alpha=0.8, edgecolor='black', label='Varians per PC (%)')
ax.plot(n_comps, cum_evr, 'r-o', linewidth=2.5, markersize=7, label='Varians Kumulatif (%)')

ax.axhline(85.0, color='green', linestyle='--', linewidth=1.5, label='Batas Aman Industri (85% Varians)')
ax.set_title('Scree Plot Analisis Spektral Drone Kelapa Sawit', fontweight='bold')
ax.set_xlabel('Komponen Utama (Principal Component)')
ax.set_ylabel('Proporsi Varians Terjelaskan (%)')
ax.set_xticks(n_comps)
ax.legend(loc='center right')
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

add_md(r"""## 7. Proyeksi Data ke Ruang 2 Dimensi (PC1 & PC2)""")

add_code("""pca_2d = PCA(n_components=2, random_state=42)
X_pca_2d = pca_2d.fit_transform(X_scaled)

df_pca_2d = pd.DataFrame(X_pca_2d, columns=['PC1', 'PC2'])
print(f"Data asli berdimensi {df_spektral.shape[1]} berhasil diringkas menjadi {df_pca_2d.shape[1]} dimensi!")
print(f"Total informasi yang berhasil dipertahankan: {sum(pca_2d.explained_variance_ratio_)*100:.2f}%")
df_pca_2d.head()""")

add_md(r"""## 8. Ekstraksi Loadings & Visualisasi PCA Biplot 2D Interaktif

Matriks *Loadings* menghubungkan kembali komponen abstrak dengan variabel spektral fisik.""")

add_code("""# Loadings = Vektor Eigen * sqrt(Nilai Eigen)
loadings = pca_2d.components_.T * np.sqrt(pca_2d.explained_variance_)

df_loadings = pd.DataFrame(
    loadings, index=df_spektral.columns, columns=['Loading_PC1', 'Loading_PC2']
)

print("=== MATRIKS BOBOT FAKTOR (FACTOR LOADINGS) ===")
print(df_loadings.round(3))

# Plot PCA Biplot 2D
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.scatter(df_pca_2d['PC1'], df_pca_2d['PC2'], color='#1e88e5', alpha=0.45, s=30, label='Sampel Kanopi Pohon')

# Gambar Vektor Panah Loading
for i, feat in enumerate(df_spektral.columns):
    ax.arrow(0, 0, loadings[i, 0]*2.8, loadings[i, 1]*2.8, color='#d32f2f', width=0.03, head_width=0.15)
    ax.text(loadings[i, 0]*3.1, loadings[i, 1]*3.1, feat, color='#b71c1c', fontweight='bold', fontsize=9.5)

ax.axhline(0, color='gray', linestyle=':', linewidth=1)
ax.axvline(0, color='gray', linestyle=':', linewidth=1)
ax.set_title(f'PCA Biplot 2D: Sampel Kanopi & Vektor Loading Spektral (Total Varians: {sum(pca_2d.explained_variance_ratio_)*100:.1f}%)', fontweight='bold')
ax.set_xlabel(f'Komponen Utama 1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% Varians) - Sumbu Vegetasi Sehat')
ax.set_ylabel(f'Komponen Utama 2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% Varians) - Sumbu Reflektansi Daun')
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

add_md(r"""## 9. Integrasi PCA dengan Klasterisasi K-Means pada Ruang 2D

Menerapkan K-Means langsung pada ruang 2D yang telah didekorelasi oleh PCA.""")

add_code("""kmeans_pca = KMeans(n_clusters=3, init='k-means++', random_state=42, n_init=10)
df_pca_2d['Klaster'] = kmeans_pca.fit_predict(X_pca_2d)

fig, ax = plt.subplots(figsize=(9, 5.5))
warna_k = ['#2e7d32', '#f57c00', '#d32f2f']
label_k = ['Zona Kanopi Sehat', 'Zona Cekaman Hara', 'Zona Cekaman Air Kritis']

for k in range(3):
    subset = df_pca_2d[df_pca_2d['Klaster'] == k]
    ax.scatter(subset['PC1'], subset['PC2'], color=warna_k[k], label=label_k[k], alpha=0.65, s=35)

centroids_2d = kmeans_pca.cluster_centers_
ax.scatter(centroids_2d[:, 0], centroids_2d[:, 1], color='black', s=200, marker='X', linewidths=2, label='Centroid Zona')

ax.set_title('Peta Zonasi Kanopi Sawit Berbasis Integrasi PCA + K-Means', fontweight='bold')
ax.set_xlabel('PC1 (Biomassa & Klorofil)')
ax.set_ylabel('PC2 (Tepi Merah & Reflektansi)')
ax.legend(loc='lower left')
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

add_md(r"""## 10. Rekonstruksi Data & Galat Residual Kompresi

Menghitung seberapa baik data asli dapat dipulihkan kembali dari ruang kompresi 2D.""")

add_code("""X_reconstructed_scaled = pca_2d.inverse_transform(X_pca_2d)
X_reconstructed = scaler.inverse_transform(X_reconstructed_scaled)

# Hitung Mean Squared Reconstruction Error
recon_error = np.mean((df_spektral.values - X_reconstructed)**2)
print("=== EVALUASI REKONSTRUKSI DATA DARI KOMPRESI PCA ===")
print(f"Mean Squared Reconstruction Error (MSE): {recon_error:.6f}")
print(f"Persentase Informasi Asli yang Hilang  : {(1 - sum(pca_2d.explained_variance_ratio_))*100:.2f}%")""")

add_md(r"""## 11. Tugas Mandiri & Eksplorasi Mahasiswa

1. **Uji Dampak Tanpa Standardisasi**: Latih model PCA langsung pada `df_spektral` tanpa `StandardScaler`. Berapa proporsi varians yang diserap oleh PC1? Bandingkan dengan hasil saat distandardisasi dan jelaskan perbedaannya!
2. **Eksplorasi Kriteria Kaiser**: Berapa banyak komponen yang memiliki nilai eigen $\lambda > 1.0$? Jika hanya komponen tersebut yang dipertahankan, berapa persen total varians yang terwakili?
3. **Analisis Transisi ke Model Ansambel**: PCA berhasil merangkum varians secara linier. Namun jika tujuan bisnis adalah memprediksi hasil panen TBS secara non-linier dengan akurasi state-of-the-art, mengapa kita memerlukan model Boosting terarah seperti Gradient Boosting (AI Modul 7.10)?""")

notebook_path = r"e:\Project Buku\notebooks\part-07\AI_Modul_7.9_Praktikum_Principal_Component_Analysis.ipynb"
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
