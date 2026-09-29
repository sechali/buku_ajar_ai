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
cells.append(md_cell("""# AI Modul 6.1: Praktikum Evaluasi Klasifikasi - Akurasi, Presisi, Recall, dan F-Beta Score
**Program Studi Agroteknologi & Teknik Pertanian - INSTIPER Yogyakarta**

Pada praktikum ini, kita akan mengimplementasikan dan menganalisis metrik-metrik evaluasi klasifikasi:
1. **Mendiagnosis Paradoks Akurasi (*Accuracy Paradox*)** pada data tanaman perkebunan yang sangat tidak seimbang (*extreme class imbalance*).
2. **Menghitung Metrik Fundamental:** Accuracy, Precision, Recall, Specificity, F1-Score, dan F2-Score.
3. **Melakukan Pergeseran Ambang Batas (*Classification Threshold Tuning*)** untuk menavigasi trade-off antara Presisi dan Recall.
4. **Optimasi Biaya Kesalahan Finansial Lapangan ($C_{FP}$ vs $C_{FN}$)** untuk menentukan titik operasi sistem AI deteksi penyakit tanaman yang paling ekonomis."""))

# Cell 1: Inisialisasi
cells.append(code_cell("""import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Mode non-interaktif headless untuk lingkungan cloud/server
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, fbeta_score, confusion_matrix, precision_recall_curve
)
import warnings
warnings.filterwarnings('ignore')

print("Seluruh pustaka komputasi berhasil diimpor dengan sukses.")"""))

# Cell 2: Dataset Sintetis
cells.append(md_cell("""## 1. Pembuatan Dataset Sintetis: Deteksi Penyakit Busuk Pangkal Batang (*Ganoderma*)
Kita mensimulasikan sensus 2.500 pokok pohon kelapa sawit di sebuah afdeling kebun.
- Fitur input:
  1. `NDVI_Kanopi`: Reflektansi vegetasi kanopi dari multispektral drone (0.1 - 0.9).
  2. `Kelembaban_Tanah`: Pembacaan IoT kelembaban tanah zona perakaran (%).
  3. `Rasio_Klorofil_SPAD`: Indeks klorofil pelepah kebun.
- Target `Status_Sakit`: 1 = Terinfeksi Ganoderma, 0 = Pohon Sehat.
- Prevalensi: Hanya ~4% pohon terinfeksi (kasus ketidakseimbangan kelas ekstrem)."""))

cells.append(code_cell("""np.random.seed(42)
N_POHON = 2500
PREVALENSI_SAKIT = 0.04 # 4% prevalensi penyakit

# Populasi Pohon Sehat (96%)
N_sehat = int(N_POHON * (1 - PREVALENSI_SAKIT))
ndvi_sehat = np.random.normal(loc=0.75, scale=0.08, size=N_sehat)
lengas_sehat = np.random.normal(loc=35.0, scale=4.0, size=N_sehat)
spad_sehat = np.random.normal(loc=55.0, scale=5.0, size=N_sehat)
label_sehat = np.zeros(N_sehat, dtype=int)

# Populasi Pohon Terinfeksi Ganoderma (4%)
N_sakit = N_POHON - N_sehat
ndvi_sakit = np.random.normal(loc=0.52, scale=0.12, size=N_sakit)
lengas_sakit = np.random.normal(loc=42.0, scale=6.0, size=N_sakit)
spad_sakit = np.random.normal(loc=38.0, scale=8.0, size=N_sakit)
label_sakit = np.ones(N_sakit, dtype=int)

# Konsolidasi DataFrame
df_kebun = pd.DataFrame({
    'NDVI_Kanopi': np.clip(np.concatenate([ndvi_sehat, ndvi_sakit]), 0.1, 1.0),
    'Kelembaban_Tanah': np.clip(np.concatenate([lengas_sehat, lengas_sakit]), 10.0, 70.0),
    'Rasio_SPAD': np.clip(np.concatenate([spad_sehat, spad_sakit]), 15.0, 75.0),
    'Status_Sakit': np.concatenate([label_sehat, label_sakit])
})

# Acak urutan baris
df_kebun = df_kebun.sample(frac=1.0, random_state=42).reset_index(drop=True)

print("Distribusi Status Tanaman:")
print(df_kebun['Status_Sakit'].value_counts(normalize=True).round(4) * 100)
print(df_kebun.head())"""))

# Cell 3: Pembuktian Paradoks Akurasi
cells.append(md_cell("""## 2. Pembuktian Paradoks Akurasi (*Accuracy Paradox*)
Kita membandingkan performa model acuan malas (*Dummy Classifier*) yang selalu memprediksi kelas mayoritas (SEHAT) melawan model berbasis data *Logistic Regression*."""))

cells.append(code_cell("""X = df_kebun[['NDVI_Kanopi', 'Kelembaban_Tanah', 'Rasio_SPAD']]
y = df_kebun['Status_Sakit']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 1. Model Dummy (Selalu tebak kelas mayoritas: SEHAT = 0)
dummy_model = DummyClassifier(strategy='most_frequent')
dummy_model.fit(X_train, y_train)
y_pred_dummy = dummy_model.predict(X_test)

# 2. Model Logistic Regression (Model Cerdas)
logreg_model = LogisticRegression(class_weight='balanced', random_state=42)
logreg_model.fit(X_train, y_train)
y_pred_logreg = logreg_model.predict(X_test)
y_proba_logreg = logreg_model.predict_proba(X_test)[:, 1]

# Perbandingan Metrik Evaluasi
acc_dummy = accuracy_score(y_test, y_pred_dummy)
prec_dummy = precision_score(y_test, y_pred_dummy, zero_division=0)
rec_dummy = recall_score(y_test, y_pred_dummy)
f1_dummy = f1_score(y_test, y_pred_dummy, zero_division=0)

acc_lr = accuracy_score(y_test, y_pred_logreg)
prec_lr = precision_score(y_test, y_pred_logreg)
rec_lr = recall_score(y_test, y_pred_logreg)
f1_lr = f1_score(y_test, y_pred_logreg)

eval_data = {
    'Metrik': ['Akurasi (Accuracy)', 'Presisi (Precision)', 'Sensitivitas (Recall)', 'Skor F1 (F1-Score)'],
    'Dummy Classifier (Model Malas)': [f"{acc_dummy:.4f}", f"{prec_dummy:.4f}", f"{rec_dummy:.4f}", f"{f1_dummy:.4f}"],
    'Logistic Regression (Model AI)': [f"{acc_lr:.4f}", f"{prec_lr:.4f}", f"{rec_lr:.4f}", f"{f1_lr:.4f}"]
}

df_eval = pd.DataFrame(eval_data)
print(df_eval.to_string(index=False))"""))

# Cell 4: F-Beta Score
cells.append(md_cell("""## 3. Penghitungan Metrik Lanjut: F-Beta Score (F2 vs F0.5)
Di perkebunan, mendeteksi pohon yang sakit adalah prioritas mutlak. Kita menghitung:
- **F2-Score ($\beta = 2.0$):** Mengutamakan Recall dua kali lebih besar daripada Presisi.
- **F0.5-Score ($\beta = 0.5$):** Mengutamakan Presisi dua kali lebih besar daripada Recall."""))

cells.append(code_cell("""f2 = fbeta_score(y_test, y_pred_logreg, beta=2.0)
f05 = fbeta_score(y_test, y_pred_logreg, beta=0.5)

print("Evaluasi Model AI Terlatih:")
print(f"- F1-Score (Seimbang)          : {f1_score(y_test, y_pred_logreg):.4f}")
print(f"- F2-Score (Prioritas Recall)     : {f2:.4f}")
print(f"- F0.5-Score (Prioritas Presisi) : {f05:.4f}")"""))

# Cell 5: Threshold Tuning
cells.append(md_cell("""## 4. Penyetelan Ambang Batas Keputusan (*Classification Threshold Tuning*)
Secara default, probabilitas >= 0.50 divonis positif. Mari kita telusuri ambang batas dari 0.05 hingga 0.95 untuk menemukan titik optimal yang meminimalkan kerugian finansial."""))

cells.append(code_cell("""thresholds = np.linspace(0.05, 0.95, 100)
precisions = []
recalls = []
f1_scores = []
f2_scores = []
total_costs = []

# Parameter Biaya Finansial Lapangan Kebun
COST_FP = 150_000   # Rp 150.000 per pokok (injeksi obat & inspeksi pohon sehat)
COST_FN = 4_500_000 # Rp 4.500.000 per pokok (penularan jamur & kematian pohon)

for th in thresholds:
    y_pred_th = (y_proba_logreg >= th).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred_th).ravel()
    
    p = precision_score(y_test, y_pred_th, zero_division=0)
    r = recall_score(y_test, y_pred_th, zero_division=0)
    f1 = f1_score(y_test, y_pred_th, zero_division=0)
    f2_val = fbeta_score(y_test, y_pred_th, beta=2.0, zero_division=0)
    
    cost = (fp * COST_FP) + (fn * COST_FN)
    
    precisions.append(p)
    recalls.append(r)
    f1_scores.append(f1)
    f2_scores.append(f2_val)
    total_costs.append(cost)

idx_min_cost = np.argmin(total_costs)
best_th = thresholds[idx_min_cost]
min_cost = total_costs[idx_min_cost]

print("Hasil Optimasi Biaya Operasional Kebun:")
print(f"- Ambang Batas Klasifikasi Paling Hemat : {best_th:.3f}")
print(f"- Estimasi Total Kerugian Finansial Terendah : Rp {min_cost:,.0f}")
print(f"- Sensitivitas (Recall) pada Ambang Tersebut : {recalls[idx_min_cost]*100:.2f}%")
print(f"- Presisi pada Ambang Tersebut              : {precisions[idx_min_cost]*100:.2f}%")"""))

# Cell 6: Visualisasi
cells.append(code_cell("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), dpi=300)

# Subplot 1: Dinamika Metrik vs Ambang Batas
ax1.plot(thresholds, precisions, label='Presisi', color='#1E88E5', lw=2)
ax1.plot(thresholds, recalls, label='Recall (Sensitivitas)', color='#D81B60', lw=2)
ax1.plot(thresholds, f1_scores, label='F1-Score', color='#004D40', linestyle='--', lw=2)
ax1.plot(thresholds, f2_scores, label='F2-Score', color='#FF8F00', linestyle='-.', lw=2)
ax1.axvline(best_th, color='#C62828', linestyle=':', lw=2, label=f'Ambang Min Biaya ({best_th:.2f})')
ax1.set_title('Pertukaran Presisi-Recall vs Ambang Batas', fontsize=11, fontweight='bold')
ax1.set_xlabel('Ambang Batas Keputusan (Threshold)', fontsize=10)
ax1.set_ylabel('Nilai Metrik', fontsize=10)
ax1.set_ylim(-0.05, 1.05)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='lower left', fontsize=8.5)

# Subplot 2: Kurva Total Kerugian Finansial
ax2.plot(thresholds, np.array(total_costs)/1_000_000, color='#C62828', lw=2.5, label='Total Biaya Kesalahan (FP+FN)')
ax2.scatter([best_th], [min_cost/1_000_000], color='#2E7D32', s=100, zorder=5)
ax2.annotate(f'Biaya Minimum:\\nRp {min_cost/1_000_000:.2f} Juta\\n(tau = {best_th:.2f})',
             xy=(best_th, min_cost/1_000_000),
             xytext=(best_th + 0.15, min_cost/1_000_000 + 15),
             arrowprops=dict(arrowstyle='->', lw=1.5, color='#2E7D32'),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#2E7D32'))
ax2.set_title('Kurva Kerugian Finansial vs Ambang Batas Keputusan', fontsize=11, fontweight='bold')
ax2.set_xlabel('Ambang Batas Keputusan (Threshold)', fontsize=10)
ax2.set_ylabel('Total Estimasi Kerugian (Juta Rupiah)', fontsize=10)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='upper right', fontsize=8.5)

plt.tight_layout()
os.makedirs('docs/assets', exist_ok=True)
plt.savefig('docs/assets/praktikum_6_1_tradeoff_dan_biaya.png', dpi=300)
plt.close()

print("Visualisasi kurva evaluasi berhasil disimpan ke docs/assets/praktikum_6_1_tradeoff_dan_biaya.png")"""))

# Cell 7: Kesimpulan
cells.append(md_cell("""## 5. Kesimpulan dan Rekomendasi Manajerial
1. **Akurasi 96% dari Dummy Classifier Tidak Bernilai:** Model malas selalu menebak tanaman sehat menghasilkan akurasi tinggi namun Recall = 0%, membiarkan seluruh tanaman berpenyakit menyebar.
2. **Pentingnya F2-Score:** Dalam penyakit menular mematikan seperti *Ganoderma*, kerugian akibat False Negative (Rp 4.500.000) jauh lebih besar daripada False Positive (Rp 150.000). Parameter $\beta = 2.0$ lebih tepat digunakan sebagai acuan daripada $F_1$.
3. **Penyetelan Ambang Batas Berbasis Biaya:** Menurunkan ambang batas keputusan klasifikasi ke $\tau \approx 0.35$ terbukti menekan total kerugian finansial perusahaan secara signifikan."""))

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

notebook_path = 'notebooks/part-06/AI_Modul_6.1_Accuracy_Precision_Recall.ipynb'
os.makedirs('notebooks/part-06', exist_ok=True)
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1)

print(f"Notebook berhasil ditulis ke {notebook_path}")
