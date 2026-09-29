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

add_md("""# AI Modul 7.6: Praktikum Naive Bayes Classifier

**Mata Kuliah:** Kecerdasan Buatan & Pembelajaran Mesin Terapan  
**Institusi:** Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Studi Kasus:** Diagnostik Cepat Penyakit Busuk Pangkal Batang Kelapa Sawit (Ganoderma vs Defisiensi Hara vs Sehat) & Klasifikasi Teks Laporan Lapangan

---

### Capaian Pembelajaran Praktikum
1. Mampu mengimplementasikan algoritma Gaussian Naive Bayes untuk data sensor kontinu perkebunan menggunakan pustaka Scikit-Learn.
2. Mampu mengekstraksi dan menginterpretasikan parameter probabilistik model: Probabilitas Prior $P(C_k)$, Nilai Rata-rata $\mu$, dan Varians $\sigma^2$.
3. Mampu menganalisis estimasi probabilitas posterior $P(C_k \mid \mathbf{x})$ untuk mendukung pengambilan keputusan berisiko di perkebunan.
4. Mampu mendemonstrasikan fenomena *Zero-Frequency Trap* dan implementasi *Laplace Smoothing* pada Multinomial Naive Bayes untuk data kategorikal/teks.""")

add_md("## 1. Import Pustaka & Konfigurasi Lingkungan")

add_code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Pengaturan visualisasi
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 120

print("[OK] Seluruh pustaka Naive Bayes berhasil dimuat!")""")

add_md("""## 2. Pembangkitan Dataset Sensor Fisiologis Tanaman Sawit

Data hasil pengukuran sensor portabel mandor di lapangan:
- `Klorofil_SPAD`: Nilai kehijauan daun pelepah ke-17 (SPAD unit)
- `Kelembapan_Tajuk_%`: Kelembapan mikro kanopi pohon (%)
- `pH_Tanah`: Derajat keasaman tanah perakaran (skala pH)
- `Konduktivitas_EC`: Konduktivitas listrik tanah (mS/cm)

Target Klasifikasi:
- `0`: Pohon Sehat (Normal)
- `1`: Defisiensi Unsur Hara (Kekurangan N/K/Mg)
- `2`: Terinfeksi Jamur Ganoderma Boninense (Stadium Lanjut)""")

add_code("""np.random.seed(42)
n_samples = 1200

# Distribusi prevalensi alami: 70% Sehat, 20% Defisiensi, 10% Ganoderma
y_sim = np.random.choice([0, 1, 2], size=n_samples, p=[0.70, 0.20, 0.10])

klorofil = np.zeros(n_samples)
kelembapan = np.zeros(n_samples)
ph = np.zeros(n_samples)
ec = np.zeros(n_samples)

for i in range(n_samples):
    if y_sim[i] == 0:    # Sehat
        klorofil[i] = np.random.normal(55.0, 4.0)
        kelembapan[i] = np.random.normal(78.0, 5.0)
        ph[i] = np.random.normal(5.5, 0.4)
        ec[i] = np.random.normal(1.2, 0.2)
    elif y_sim[i] == 1:  # Defisiensi Hara
        klorofil[i] = np.random.normal(42.0, 5.0)
        kelembapan[i] = np.random.normal(72.0, 6.0)
        ph[i] = np.random.normal(4.8, 0.5)
        ec[i] = np.random.normal(0.7, 0.2)
    else:                # Terinfeksi Ganoderma
        klorofil[i] = np.random.normal(34.0, 6.0)
        kelembapan[i] = np.random.normal(60.0, 8.0)
        ph[i] = np.random.normal(4.2, 0.4)
        ec[i] = np.random.normal(2.1, 0.4)

df_patologi = pd.DataFrame({
    'Klorofil_SPAD': klorofil,
    'Kelembapan_Tajuk_%': kelembapan,
    'pH_Tanah': ph,
    'Konduktivitas_EC': ec,
    'Status_Kesehatan': y_sim
})

print(f"Dataset berhasil dibuat: {df_patologi.shape[0]} baris sampel")
df_patologi.head()""")

add_md("## 3. Eksplorasi Visual: Distribusi Fitur Fisiologis per Kelas")

add_code("""fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

nama_kelas = ['Sehat', 'Defisiensi', 'Ganoderma']
warna_kelas = ['#2e7d32', '#f57c00', '#d32f2f']

# Histogram Distribusi Klorofil
for c in range(3):
    subset = df_patologi[df_patologi['Status_Kesehatan'] == c]
    sns.kdeplot(subset['Klorofil_SPAD'], ax=axes[0], label=nama_kelas[c], color=warna_kelas[c], fill=True, alpha=0.3)
axes[0].set_title('Distribusi Densitas Klorofil Daun (SPAD)', fontweight='bold')
axes[0].set_xlabel('Nilai SPAD')
axes[0].set_ylabel('Densitas Probabilitas')
axes[0].legend()

# Scatter Plot Klorofil vs Konduktivitas EC
for c in range(3):
    subset = df_patologi[df_patologi['Status_Kesehatan'] == c]
    axes[1].scatter(subset['Klorofil_SPAD'], subset['Konduktivitas_EC'], label=nama_kelas[c], color=warna_kelas[c], alpha=0.6, edgecolors='none')
axes[1].set_title('Pemisahan Gejala: Klorofil vs Konduktivitas EC', fontweight='bold')
axes[1].set_xlabel('Klorofil (SPAD)')
axes[1].set_ylabel('Konduktivitas EC (mS/cm)')
axes[1].legend()

plt.tight_layout()
plt.show()""")

add_md("## 4. Pembagian Data & Pelatihan Model Gaussian Naive Bayes")

add_code("""fitur = ['Klorofil_SPAD', 'Kelembapan_Tajuk_%', 'pH_Tanah', 'Konduktivitas_EC']
X = df_patologi[fitur]
y = df_patologi['Status_Kesehatan']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Inisialisasi dan pelatihan GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)

train_acc = gnb.score(X_train, y_train)
test_acc = gnb.score(X_test, y_test)

print(f"Akurasi Data Latih (Train Accuracy): {train_acc * 100:.2f}%")
print(f"Akurasi Data Uji (Test Accuracy)   : {test_acc * 100:.2f}%")""")

add_md("""## 5. Inspeksi Parameter Probabilistik Model GaussianNB

Naive Bayes mempelajari parameter murni berbasis statistik deskriptif:
- `class_prior_`: Probabilitas awal $P(C_k)$
- `theta_`: Nilai rata-rata $\mu_{kj}$ tiap fitur pada tiap kelas
- `var_`: Varians $\sigma_{kj}^2$ tiap fitur pada tiap kelas""")

add_code("""print("=== PROBABILITAS PRIOR EMPIRIS P(Ck) ===")
for k, nama in enumerate(nama_kelas):
    print(f"P({nama:<12}): {gnb.class_prior_[k]*100:.2f}%")

print("\\n=== NILAI RATA-RATA FITUR TIAP KELAS (MU) ===")
df_mu = pd.DataFrame(gnb.theta_, index=nama_kelas, columns=fitur)
print(df_mu.to_string())

print("\\n=== VARIAN FITUR TIAP KELAS (SIGMA^2) ===")
df_var = pd.DataFrame(gnb.var_, index=nama_kelas, columns=fitur)
print(df_var.to_string())""")

add_md("## 6. Evaluasi Kinerja Diagnostik: Matriks Konfusi & Laporan Klasifikasi")

add_code("""y_pred = gnb.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(
    cm, annot=True, fmt='d', cmap='YlGnBu',
    xticklabels=nama_kelas, yticklabels=nama_kelas, ax=ax
)
ax.set_title('Matriks Konfusi Diagnostik Penyakit Sawit (GaussianNB)', fontweight='bold')
ax.set_xlabel('Diagnosis Model AI')
ax.set_ylabel('Status Aktual Laboratorium')
plt.show()

print("=== LAPORAN EVALUASI DIAGNOSTIK GAUSSIAN NAIVE BAYES ===")
print(classification_report(y_test, y_pred, target_names=nama_kelas))""")

add_md(r"""## 7. Prediksi Sampel Pohon Lapangan & Analisis Probabilitas Posterior

Menguji tanaman baru dan membedah skor probabilitas bersyarat $P(C_k \mid \mathbf{x})$.""")

add_code("""pohon_uji = pd.DataFrame([
    # Pohon A: Pelepah menguning, tanah masam dan konduktivitas tinggi (Tersangka Ganoderma)
    {'Klorofil_SPAD': 33.5, 'Kelembapan_Tajuk_%': 58.0, 'pH_Tanah': 4.1, 'Konduktivitas_EC': 2.2},
    # Pohon B: Pelepah hijau segar, tanah normal (Pohon Normal)
    {'Klorofil_SPAD': 56.2, 'Kelembapan_Tajuk_%': 79.0, 'pH_Tanah': 5.4, 'Konduktivitas_EC': 1.18},
    # Pohon C: Klorofil agak rendah tetapi EC rendah (Tersangka Defisiensi Hara)
    {'Klorofil_SPAD': 41.0, 'Kelembapan_Tajuk_%': 71.5, 'pH_Tanah': 4.9, 'Konduktivitas_EC': 0.65}
])

pred_labels = gnb.predict(pohon_uji)
pred_probas = gnb.predict_proba(pohon_uji)

for i in range(len(pohon_uji)):
    print(f"\\n================ POHON SAMPEL #{i+1} ================")
    print(f"Diagnosis Model : {nama_kelas[pred_labels[i]].upper()}")
    print("Rincian Probabilitas Posterior:")
    for k in range(3):
        print(f" - P({nama_kelas[k]:<12} | x): {pred_probas[i][k]*100:.3f}%")""")

add_md("""## 8. Eksperimen Efek Pelanggaran Asumsi Independensi (Multikolinieritas)

Bagaimana jika sensor mengirimkan fitur duplikat yang berkorelasi 100%?""")

add_code("""n_dups = [0, 2, 5, 10, 20, 30]
skor_uji = []

for d in n_dups:
    X_train_exp = X_train.copy()
    X_test_exp = X_test.copy()
    
    # Tambahkan fitur tiruan yang berkorelasi kuat dengan Klorofil
    for j in range(d):
        X_train_exp[f'Dup_{j}'] = X_train['Klorofil_SPAD'] + np.random.normal(0, 0.05, len(X_train))
        X_test_exp[f'Dup_{j}'] = X_test['Klorofil_SPAD'] + np.random.normal(0, 0.05, len(X_test))
        
    m = GaussianNB()
    m.fit(X_train_exp, y_train)
    skor_uji.append(m.score(X_test_exp, y_test))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(n_dups, np.array(skor_uji)*100, 'o-', color='#d32f2f', linewidth=2)
ax.set_title('Sensitivitas Naive Bayes terhadap Multikolinieritas Redundan', fontweight='bold')
ax.set_xlabel('Jumlah Fitur Duplikat yang Ditambahkan')
ax.set_ylabel('Akurasi Data Uji (%)')
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

add_md("""## 9. Penerapan Kasus Teks & Demonstrasi Laplace Smoothing (MultinomialNB)

Mengklasifikasikan catatan teks laporan mandor kebun:
- `Darurat Hama / Penyakit` (Kelas 1)
- `Operasional Rutin` (Kelas 0)""")

add_code("""dokumen_latih = [
    "ditemukan serangan ulat api di blok c afdeling satu",
    "daun kelapa sawit berlubang akibat ulat kantung parah",
    "miselium jamur ganoderma terlihat di pangkal batang pohon",
    "hama tikus merusak tandan buah sawit matang di piringan",
    "pelepah menguning gejala busuk pupus tajuk",
    "aplikasi pemupukan urea dan mop berjalan lancar",
    "pembersihan piringan pohon dan penunasan pelepah kering",
    "perbaikan jalan poros kebun dan jembatan gorong-gorong",
    "panen tbs afdeling dua selesai tepat waktu",
    "penyemprotan herbisida gulma gawangan rintis"
]
label_latih = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]

vectorizer = CountVectorizer()
X_text_train = vectorizer.fit_transform(dokumen_latih)

# 1. Model dengan Laplace Smoothing (alpha = 1.0 - Standar)
mnb_smooth = MultinomialNB(alpha=1.0)
mnb_smooth.fit(X_text_train, label_latih)

# 2. Uji Dokumen Baru dengan Kosakata Baru/Langka
dokumen_baru = [
    "mandor melaporkan ada ulat menyerang daun di gawangan",
    "pekerja sedang melakukan penunasan pelepah di blok b",
    "ditemukan serangga kutu_kebul langka beterbangan di bibitan"
]
X_text_test = vectorizer.transform(dokumen_baru)

pred_smooth = mnb_smooth.predict(X_text_test)
proba_smooth = mnb_smooth.predict_proba(X_text_test)

kategori_teks = ['Rutin', 'Darurat Hama']
print("=== HASIL KLASIFIKASI LAPORAN MANDOR (MULTINOMIAL NAIVE BAYES) ===")
for doc, p, prob in zip(dokumen_baru, pred_smooth, proba_smooth):
    print(f"\\nLaporan: '{doc}'")
    print(f"Kategori Prediksi: {kategori_teks[p]} (Probabilitas Hama: {prob[1]*100:.2f}%)")""")

add_md("""## 10. Tugas Mandiri & Eksplorasi Mahasiswa

1. **Eksplorasi Prior**: Ubah parameter `class_prior=[0.90, 0.08, 0.02]` pada model `GaussianNB`. Amati bagaimana perubahan prior ini memengaruhi sensitivitas deteksi terhadap kelas Ganoderma!
2. **Uji Dokumen Asing**: Uji sebuah kalimat baru yang sama sekali tidak mengandung kata dari data latih (misalnya *"traktor derek mogok di tanjakan"*). Amati prediksi kelas dan nilai probabilitasnya. Jelaskan peran Laplace smoothing pada kondisi ini!
3. **Analisis Kritis Komparasi**: Bandingkan kecepatan eksekusi pelatihan dan inferensi antara `GaussianNB` versus `RandomForestClassifier` pada dataset sensor 100.000 sampel. Kapan Naive Bayes lebih direkomendasikan dibanding Random Forest di perkebunan?""")

notebook_path = r"e:\Project Buku\notebooks\part-07\AI_Modul_7.6_Praktikum_Naive_Bayes.ipynb"
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
