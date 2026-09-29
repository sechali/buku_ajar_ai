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
cells.append(md_cell("""# AI Modul 6.3: Praktikum Validasi Silang (Cross-Validation) - Protokol Evaluasi Bebas Bias
**Program Studi Agroteknologi & Teknik Pertanian - INSTIPER Yogyakarta**

Pada praktikum ini, kita akan mengimplementasikan dan menganalisis protokol validasi silang:
1. **Membandingkan Skema Evaluasi:** Hold-Out Tunggal vs K-Fold Standar vs Stratified K-Fold.
2. **Mengisolasi Kebocoran Spasial:** Implementasi *Spatial Group K-Fold* berdasarkan Afdeling kebun kelapa sawit.
3. **Mencegah Kebocoran Temporal:** Validasi runtun waktu telemetri sensor kebun menggunakan *TimeSeriesSplit*.
4. **Validasi Silang Bersarang (*Nested Cross-Validation*):** Penyetelan hiperparameter model bebas optimisme semu."""))

# Cell 1: Inisialisasi
cells.append(code_cell("""import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import (
    KFold, StratifiedKFold, GroupKFold, TimeSeriesSplit,
    cross_val_score, GridSearchCV, train_test_split
)
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import root_mean_squared_error, accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("Seluruh pustaka validasi dan machine learning berhasil dimuat.")"""))

# Cell 2: Sintesis Dataset Spasial 5 Afdeling Kebun
cells.append(md_cell("""## 1. Pembuatan Dataset Spasial: Prediksi Produktivitas TBS Lintas Afdeling
Kita mensimulasikan sensus 1.500 petak kebun yang tersebar di 5 Afdeling yang memiliki topografi berbeda:
- `Afdeling_A`: Tanah mineral datar (Produktivitas tinggi)
- `Afdeling_B`: Tanah mineral berpasir (Produktivitas moderat)
- `Afdeling_C`: Area rawa dengan parit primer (Produktivitas variatif)
- `Afdeling_D`: Tanah gambut tebal (Produktivitas rendah, rentan banjir)
- `Afdeling_E`: Area perbukitan berteras (Produktivitas sangat tergantung curah hujan)

Fitur:
- `NDVI`: Indeks kerapatan kanopi drone.
- `Kerapatan_Pokok`: Jumlah pokok produktif per hektar (120 - 145 pokok/ha).
- `Curah_Hujan_Bln`: Akumulasi hujan bulanan (mm).
Target:
- `Produktivitas_Ton_Ha`: Hasil panen riil (Ton/Ha)."""))

cells.append(code_cell("""np.random.seed(42)
N_SAMPEL = 1500

afdeling_list = ['Afdeling_A', 'Afdeling_B', 'Afdeling_C', 'Afdeling_D', 'Afdeling_E']
afdeling_data = np.random.choice(afdeling_list, size=N_SAMPEL, p=[0.25, 0.25, 0.20, 0.15, 0.15])

# Efek basis per afdeling (Autokorelasi Spasial Nyata)
efek_afdeling = {
    'Afdeling_A': 4.5,
    'Afdeling_B': 2.0,
    'Afdeling_C': 0.5,
    'Afdeling_D': -3.0,
    'Afdeling_E': -1.5
}

ndvi = np.random.uniform(0.55, 0.90, size=N_SAMPEL)
kerapatan = np.random.uniform(120, 145, size=N_SAMPEL)
hujan = np.random.uniform(100, 350, size=N_SAMPEL)

# Persamaan fisik biologis produktivitas kebun dengan noise lokal
efek_spasial = np.array([efek_afdeling[a] for a in afdeling_data])
tonase = 15.0 + (12.0 * ndvi) + (0.05 * kerapatan) + (0.015 * hujan) + efek_spasial + np.random.normal(0, 1.2, size=N_SAMPEL)

df_kebun = pd.DataFrame({
    'Afdeling': afdeling_data,
    'NDVI': ndvi,
    'Kerapatan_Pokok': kerapatan,
    'Curah_Hujan_Bln': hujan,
    'Produktivitas_Ton_Ha': np.clip(tonase, 5.0, 38.0)
})

print("Struktur Data Spasial Kebun:")
print(df_kebun.groupby('Afdeling')['Produktivitas_Ton_Ha'].agg(['count', 'mean', 'std']).round(2))
print(df_kebun.head())"""))

# Cell 3: Komparasi K-Fold Acak vs Spatial Group K-Fold
cells.append(md_cell("""## 2. Eksperimen: Pembuktian Kebocoran Spasial (Random K-Fold vs Group K-Fold)
Kita membandingkan:
1. **Standard K-Fold (Acak):** Mengabaikan Afdeling, petak dari afdeling yang sama masuk ke train dan test.
2. **Spatial Group K-Fold:** Melatih model pada 4 afdeling dan mengujinya pada 1 afdeling utuh yang diisolasi secara ketat."""))

cells.append(code_cell(r"""X = df_kebun[['NDVI', 'Kerapatan_Pokok', 'Curah_Hujan_Bln']]
y = df_kebun['Produktivitas_Ton_Ha']
groups = df_kebun['Afdeling']

model_rf = RandomForestRegressor(n_estimators=80, max_depth=6, random_state=42)

# 1. Standard 5-Fold Cross Validation (Acak)
kf = KFold(n_splits=5, shuffle=True, random_state=42)
rmse_kfold = -cross_val_score(model_rf, X, y, cv=kf, scoring='neg_root_mean_squared_error')

# 2. Spatial Group 5-Fold Cross Validation (Isolasi Afdeling)
gkf = GroupKFold(n_splits=5)
rmse_gkf = -cross_val_score(model_rf, X, y, groups=groups, cv=gkf, scoring='neg_root_mean_squared_error')

print("--- HASIL EVALUASI MODEL REGRESI PRODUKTIVITAS KEBUN ---")
print(f"1. Standard K-Fold (Acak)        : Rerata RMSE = {rmse_kfold.mean():.3f} +/- {rmse_kfold.std():.3f} Ton/Ha")
print(f"2. Spatial Group K-Fold (Isolasi): Rerata RMSE = {rmse_gkf.mean():.3f} +/- {rmse_gkf.std():.3f} Ton/Ha")
print("\nCatatan: RMSE Group K-Fold lebih tinggi karena menguji kemampuan generalisasi pada Afdeling baru tanpa menyontek pola tanah lokal!")"""))

# Cell 4: Visualisasi Variansi Antar-Lipatan
cells.append(code_cell(r"""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), dpi=300)

# Subplot 1: Perbandingan Skor per Lipatan
folds_idx = np.arange(1, 6)
ax1.plot(folds_idx, rmse_kfold, marker='o', lw=2, color='#1E88E5', label='Standard K-Fold (Acak)')
ax1.plot(folds_idx, rmse_gkf, marker='s', lw=2, color='#D81B60', label='Spatial Group K-Fold (Afdeling)')
ax1.set_title('Fluktuasi Galat RMSE Antar-Lipatan', fontsize=11, fontweight='bold')
ax1.set_xlabel('Indeks Lipatan (Fold)', fontsize=10)
ax1.set_ylabel('RMSE (Ton/Ha)', fontsize=10)
ax1.set_xticks(folds_idx)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(fontsize=9)

# Subplot 2: Diagram Batang Rerata & Galat Baku
means = [rmse_kfold.mean(), rmse_gkf.mean()]
stds = [rmse_kfold.std(), rmse_gkf.std()]
bars = ax2.bar(['Standard K-Fold\n(Acak Bias)', 'Spatial Group K-Fold\n(Isolasi Afdeling)'],
               means, yerr=stds, capsize=8, color=['#90CAF9', '#F48FB1'], edgecolor='#333333', width=0.45)
ax2.set_title('Rerata Galat dan Standar Deviasi Kinerja', fontsize=11, fontweight='bold')
ax2.set_ylabel('Rerata RMSE (Ton/Ha)', fontsize=10)
for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval/2.0, f"{yval:.2f} Ton/Ha", ha='center', va='center', fontweight='bold')
ax2.grid(axis='y', linestyle=':', alpha=0.6)

plt.tight_layout()
os.makedirs('docs/assets', exist_ok=True)
plt.savefig('docs/assets/praktikum_6_3_cv_varians.png', dpi=300)
plt.close()

print("Visualisasi berhasil disimpan ke docs/assets/praktikum_6_3_cv_varians.png")"""))

# Cell 5: Time-Series Split untuk Data Runtun Waktu
cells.append(md_cell("""## 3. Validasi Runtun Waktu (*TimeSeriesSplit*) pada Data Sensor Cuaca
Pada data deret waktu, data latih hanya boleh menggunakan masa lalu, dan data uji harus berada di masa depan."""))

cells.append(code_cell("""# Simulasi Runtun Waktu Cuaca 36 Bulan
np.random.seed(42)
bulan = np.arange(1, 37)
hujan_bulanan = 200 + 80 * np.sin(2 * np.pi * bulan / 12) + np.random.normal(0, 15, size=36)
suhu_kanopi = 28 - 2 * np.sin(2 * np.pi * bulan / 12) + np.random.normal(0, 0.8, size=36)

df_ts = pd.DataFrame({'Bulan': bulan, 'Curah_Hujan': hujan_bulanan, 'Suhu_Kanopi': suhu_kanopi})

# Time Series Split 4 Iterasi
tscv = TimeSeriesSplit(n_splits=4)
print("Partisi Waktu Expanding Window:")
for i, (train_idx, test_idx) in enumerate(tscv.split(df_ts)):
    print(f"Lipatan {i+1}: Data Latih Bulan {train_idx[0]+1} s.d. {train_idx[-1]+1} ({len(train_idx)} bln) | Data Uji Bulan {test_idx[0]+1} s.d. {test_idx[-1]+1} ({len(test_idx)} bln)")"""))

# Cell 6: Nested Cross-Validation
cells.append(md_cell("""## 4. Validasi Silang Bersarang (*Nested Cross-Validation*)
Mencari kedalaman pohon terbaik (`max_depth`) di loop dalam, dan mengevaluasi generalisasi di loop luar."""))

cells.append(code_cell("""param_grid = {'max_depth': [3, 5, 8]}
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)
outer_cv = KFold(n_splits=4, shuffle=True, random_state=42)

grid_search = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_grid=param_grid,
    cv=inner_cv,
    scoring='neg_root_mean_squared_error'
)

nested_scores = -cross_val_score(grid_search, X, y, cv=outer_cv, scoring='neg_root_mean_squared_error')

print(f"Skor RMSE Nested Cross-Validation Bebas Bias: {nested_scores.mean():.3f} +/- {nested_scores.std():.3f} Ton/Ha")"""))

# Cell 7: Kesimpulan
cells.append(md_cell("""## 5. Kesimpulan Praktikum
1. **Bahaya Kebocoran Spasial:** Validasi acak menghasilkan estimasi RMSE yang tampak sangat rendah karena pohon di petak terdekat saling membocorkan informasi hara tanah.
2. **Kekuatan Spatial Group K-Fold:** Mengisolasi afdeling memberikan gambaran kinerja model sesungguhnya jika dipasang di perkebunan baru.
3. **Disiplin Waktu:** Penggunaan TimeSeriesSplit menjamin model AI peramalan cuaca tidak memanfaatkan informasi masa depan."""))

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

notebook_path = 'notebooks/part-06/AI_Modul_6.3_Cross_Validation.ipynb'
os.makedirs('notebooks/part-06', exist_ok=True)
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1)

print(f"Notebook berhasil ditulis ke {notebook_path}")
