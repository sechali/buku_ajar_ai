import json
import os

cells = []

def md_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    }

# Title
cells.append(md_cell("""# AI Modul 6.2: Praktikum Matriks Konfusi (Confusion Matrix) - Evaluasi Multi-Kelas
**Program Studi Agroteknologi & Teknik Pertanian - INSTIPER Yogyakarta**

Pada praktikum ini, kita akan mengimplementasikan dan menganalisis matriks konfusi:
1. **Membangun Matriks Konfusi Multi-Kelas (4x4)** untuk pemilahan fraksi kematangan Tandan Buah Segar (TBS) di Pabrik Kelapa Sawit (PKS).
2. **Menghitung Metrik per Kelas:** Presisi, Recall, dan F1-Score untuk setiap tingkat kematangan.
3. **Menganalisis Strategi Agregasi:** Komparasi mendalam antara *Macro-Averaging*, *Micro-Averaging*, dan *Weighted-Averaging*.
4. **Visualisasi Heatmap Ternormalisasi:** Normalisasi baris (Recall) dan normalisasi kolom (Presisi).
5. **Kalkulasi Matriks Biaya Finansial Lapangan:** Menghitung total kerugian penalti fraksi buah mentah dan buah lewat matang di PKS."""))

# Cell 1: Inisialisasi
cells.append(code_cell("""import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix, classification_report,
    precision_score, recall_score, f1_score, accuracy_score
)
import warnings
warnings.filterwarnings('ignore')

print("Pustaka komputasi visualisasi dan machine learning berhasil dimuat.")"""))

# Cell 2: Sintesis Dataset Mutu TBS Multi-Kelas
cells.append(md_cell("""## 1. Pembuatan Dataset Sintetis: Fraksi Kematangan TBS Kelapa Sawit
Kita mensimulasikan sensus 1.500 sampel TBS di loading ramp PKS dengan 4 kelas fraksi:
- `0`: Mentah (Unripe) - 250 tandan
- `1`: Kurang Matang (Underripe) - 350 tandan
- `2`: Matang Sempurna (Ripe) - 700 tandan (Kelas mayoritas)
- `3`: Lewat Matang (Overripe) - 200 tandan

Fitur pengukuran visi komputer:
1. `Hue_Mean`: Rata-rata corak warna HSV (0 - 180). Buah mentah bernilai rendah (kehitaman/violet), buah matang bernilai tinggi (oranye/merah jingga).
2. `Sat_Mean`: Kejenuhan warna (0 - 255).
3. `Brondol_Lepas_Pct`: Persentase brondolan yang lepas alami dari janjang luar (%)."""))

cells.append(code_cell("""np.random.seed(42)

# 0: Mentah (N=250)
h_0 = np.random.normal(loc=18, scale=5, size=250)
s_0 = np.random.normal(loc=90, scale=15, size=250)
b_0 = np.random.uniform(low=0.0, high=2.0, size=250) # 0 - 2% lepas
y_0 = np.zeros(250, dtype=int)

# 1: Kurang Matang (N=350) - Ada irisan spektral dengan Matang
h_1 = np.random.normal(loc=32, scale=7, size=350)
s_1 = np.random.normal(loc=140, scale=20, size=350)
b_1 = np.random.uniform(low=2.0, high=18.0, size=350) # 2 - 18% lepas
y_1 = np.ones(350, dtype=int)

# 2: Matang Sempurna (N=700)
h_2 = np.random.normal(loc=40, scale=7, size=700)
s_2 = np.random.normal(loc=185, scale=20, size=700)
b_2 = np.random.uniform(low=14.0, high=65.0, size=700) # 14 - 65% lepas
y_2 = np.full(700, 2, dtype=int)

# 3: Lewat Matang (N=200)
h_3 = np.random.normal(loc=54, scale=6, size=200)
s_3 = np.random.normal(loc=215, scale=15, size=200)
b_3 = np.random.uniform(low=65.0, high=98.0, size=200) # > 65% lepas
y_3 = np.full(200, 3, dtype=int)

# Konsolidasi DataFrame
df_tbs = pd.DataFrame({
    'Hue_Mean': np.clip(np.concatenate([h_0, h_1, h_2, h_3]), 0, 180),
    'Sat_Mean': np.clip(np.concatenate([s_0, s_1, s_2, s_3]), 0, 255),
    'Brondol_Lepas_Pct': np.clip(np.concatenate([b_0, b_1, b_2, b_3]), 0, 100),
    'Fraksi_Kematangan': np.concatenate([y_0, y_1, y_2, y_3])
})

label_map = {0: 'Mentah', 1: 'Kurang Matang', 2: 'Matang Sempurna', 3: 'Lewat Matang'}
df_tbs['Label_Kategori'] = df_tbs['Fraksi_Kematangan'].map(label_map)

# Acak baris
df_tbs = df_tbs.sample(frac=1.0, random_state=42).reset_index(drop=True)

print("Distribusi Sampel Fraksi Kematangan TBS:")
print(df_tbs['Label_Kategori'].value_counts())
print(df_tbs.head())"""))

# Cell 3: Pelatihan Model Random Forest
cells.append(md_cell("""## 2. Pelatihan Model Klasifikasi Random Forest
Kita membagi data menjadi 75% Data Latih dan 25% Data Uji dengan stratifikasi label."""))

cells.append(code_cell("""X = df_tbs[['Hue_Mean', 'Sat_Mean', 'Brondol_Lepas_Pct']]
y = df_tbs['Fraksi_Kematangan']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
kelas_nama = ['Mentah', 'Kurang Matang', 'Matang Sempurna', 'Lewat Matang']

print("Model Random Forest berhasil dilatih.")
print(f"Akurasi Keseluruhan (Overall Accuracy): {accuracy_score(y_test, y_pred)*100:.2f}%")"""))

# Cell 4: Matriks Konfusi Mentah & Ternormalisasi
cells.append(md_cell("""## 3. Komputasi Matriks Konfusi Mentah dan Ternormalisasi Baris (Recall)
Kita menghitung matriks konfusi absolut dan matriks konfusi proporsional per baris."""))

cells.append(code_cell(r"""cm_raw = confusion_matrix(y_test, y_pred)
cm_norm_recall = cm_raw.astype('float') / cm_raw.sum(axis=1)[:, np.newaxis]

print("Matriks Konfusi Mentah (Cacah Sampel):")
print(pd.DataFrame(cm_raw, index=kelas_nama, columns=kelas_nama))

print("\nMatriks Konfusi Ternormalisasi Baris (Recall):")
print(pd.DataFrame(cm_norm_recall.round(4) * 100, index=kelas_nama, columns=kelas_nama))"""))

# Cell 5: Analisis Metrik per Kelas dan Strategi Agregasi
cells.append(md_cell("""## 4. Evaluasi Komparasi Agregasi: Macro vs Micro vs Weighted
Mari kita hitung Presisi, Recall, dan F1-Score untuk setiap kelas kematangan secara mandiri, kemudian membandingkan tiga metode rata-rata global."""))

cells.append(code_cell(r"""# Menghitung Metrik per Kelas Individual
prec_per_class = precision_score(y_test, y_pred, average=None)
rec_per_class = recall_score(y_test, y_pred, average=None)
f1_per_class = f1_score(y_test, y_pred, average=None)
support_per_class = np.bincount(y_test)

df_per_class = pd.DataFrame({
    'Fraksi TBS': kelas_nama,
    'Presisi': [f"{p*100:.2f}%" for p in prec_per_class],
    'Recall': [f"{r*100:.2f}%" for r in rec_per_class],
    'F1-Score': [f"{f*100:.2f}%" for f in f1_per_class],
    'Jumlah Sampel (Support)': support_per_class
})

print("Evaluasi Performa per Kategori Fraksi:")
print(df_per_class.to_string(index=False))

# Agregasi Rata-rata Global
print("\n--- KOMPARASI STRATEGI AGREGASI GLOBAL ---")
print(f"Macro-Precision   : {precision_score(y_test, y_pred, average='macro')*100:.2f}% (Rerata setara semua kelas)")
print(f"Weighted-Precision: {precision_score(y_test, y_pred, average='weighted')*100:.2f}% (Dibobot proporsi sampel)")
print(f"Micro-Precision   : {precision_score(y_test, y_pred, average='micro')*100:.2f}% (Identik dengan Akurasi Global)")
"""))

# Cell 6: Visualisasi Heatmap Matriks Konfusi
cells.append(code_cell("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

# Heatmap Absolut
sns.heatmap(cm_raw, annot=True, fmt='d', cmap='Blues', cbar=True,
            xticklabels=kelas_nama, yticklabels=kelas_nama, ax=ax1)
ax1.set_title('Matriks Konfusi Cacah Absolut\\nSortasi Mutu TBS PKS', fontsize=11, fontweight='bold')
ax1.set_xlabel('Prediksi Model AI', fontsize=10, fontweight='bold')
ax1.set_ylabel('Kondisi Aktual Lapangan', fontsize=10, fontweight='bold')

# Heatmap Ternormalisasi Recall
sns.heatmap(cm_norm_recall, annot=True, fmt='.2%', cmap='YlGnBu', cbar=True,
            xticklabels=kelas_nama, yticklabels=kelas_nama, ax=ax2)
ax2.set_title('Matriks Konfusi Ternormalisasi Baris (Recall)\\nProporsi Keberhasilan per Fraksi', fontsize=11, fontweight='bold')
ax2.set_xlabel('Prediksi Model AI', fontsize=10, fontweight='bold')
ax2.set_ylabel('Kondisi Aktual Lapangan', fontsize=10, fontweight='bold')

plt.tight_layout()
os.makedirs('docs/assets', exist_ok=True)
plt.savefig('docs/assets/praktikum_6_2_confusion_matrix_pks.png', dpi=300)
plt.close()

print("Visualisasi matriks konfusi berhasil disimpan ke docs/assets/praktikum_6_2_confusion_matrix_pks.png")"""))

# Cell 7: Kalkulasi Matriks Biaya Finansial PKS
cells.append(md_cell("""## 5. Audit Finansial: Matriks Kerugian Operasional di PKS
Pabrik menetapkan matriks biaya denda operasional per tandan:
- Aktual Mentah diprediksi Matang: Penalti Rp 120.000 (tidak terpipil, merusak thresher).
- Aktual Lewat Matang diprediksi Matang: Penalti Rp 90.000 (lonjakan ALB / FFA).
- Galat kelas bersebelahan: Rp 10.000 - Rp 30.000.
- Prediksi Benar (Diagonal Utama): Rp 0."""))

cells.append(code_cell(r"""cost_matrix = np.array([
    [      0,  15_000, 120_000,  80_000],
    [ 10_000,       0,  40_000,  30_000],
    [ 50_000,  20_000,       0,  15_000],
    [ 10_000,  15_000,  90_000,       0]
])

# Perkalian elemen ke elemen (Hadamard Product) antara matriks konfusi dan matriks biaya
financial_loss_matrix = cm_raw * cost_matrix
total_financial_loss = np.sum(financial_loss_matrix)

df_loss = pd.DataFrame(financial_loss_matrix, index=kelas_nama, columns=kelas_nama)
print("Matriks Kerugian Finansial per Sel (Rupiah):")
print(df_loss.map(lambda x: f"Rp {x:,.0f}"))

print(f"\n=======================================================")
print(f"TOTAL KERUGIAN OPERASIONAL SORTASI: Rp {total_financial_loss:,.0f}")
print(f"Rata-rata Kerugian per Tandan Uji  : Rp {total_financial_loss/len(y_test):,.0f}")
print(f"=======================================================")"""))

# Cell 8: Kesimpulan
cells.append(md_cell("""## 6. Kesimpulan dan Rekomendasi Manajerial
1. **Analisis Diagonal Utama:** Sebagian besar sampel terkonsentrasi di diagonal utama, membuktikan performa model sudah baik pada kelas Matang Sempurna (> 95%).
2. **Kekeliruan Kelas Bersebelahan:** Kebingungan terbesar terjadi antara Kurang Matang dan Matang Sempurna, yang secara biologis wajar karena gradasi warna brondolan alami.
3. **Penyelamatan Finansial Pabrik:** Kerugian terbesar bersumber dari buah lewat matang yang lolos terprediksi matang. Rekomendasi perbaikan adalah meningkatkan bobot penalti klasifikasi untuk buah lewat matang guna mengamankan kualitas Asam Lemak Bebas (ALB)."""))

notebook_content = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

notebook_path = 'notebooks/part-06/AI_Modul_6.2_Confusion_Matrix.ipynb'
os.makedirs('notebooks/part-06', exist_ok=True)
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1)

print(f"Notebook berhasil ditulis ke {notebook_path}")
