import json
import os

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

# Notebook content
add_md("""# AI Modul 7.5: Praktikum Random Forest & Evaluasi Ansambel

**Mata Kuliah:** Kecerdasan Buatan & Pembelajaran Mesin Terapan  
**Institusi:** Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Studi Kasus:** Otomatisasi Klasifikasi Mutu TBS Sawit dan Estimasi Rendemen CPO (OER) Menggunakan Ensemble Random Forest, Validasi Out-of-Bag (OOB), dan Analisis Kepentingan Fitur (MDI)

---

### Capaian Pembelajaran Praktikum
1. Mampu mengimplementasikan algoritma Random Forest untuk tugas klasifikasi multi-kelas dan regresi menggunakan pustaka Scikit-Learn.
2. Mampu memanfaatkan evaluasi Out-of-Bag (OOB Score) sebagai estimasi validasi internal bebas bias tanpa membagi data validasi eksternal.
3. Mampu menganalisis signifikansi fitur agronomi melalui Mean Decrease in Impurity (MDI) dan Permutation Importance.
4. Mampu mendiagnosis kurva konvergensi jumlah estimator ($B$) dan membandingkan ketangguhan Random Forest versus pohon tunggal (Decision Tree).""")

add_md("## 1. Import Pustaka & Konfigurasi Lingkungan")

add_code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, mean_squared_error, r2_score

# Pengaturan visualisasi
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 120

print("[OK] Seluruh pustaka ensemble Random Forest berhasil dimuat!")""")

add_md("""## 2. Pembangkitan Dataset Sortasi TBS Pabrik Kelapa Sawit (PKS)

Fitur inspeksi di Loading Ramp PKS:
- `Brondolan_Lepas_%`: Persentase buah lepas dari tandan (2.0% - 35.0%)
- `Kadar_FFA_%`: Kadar Asam Lemak Bebas / Free Fatty Acid (1.0% - 8.5%)
- `Kadar_Air_%`: Persentase kadar air mesokarp buah (12.0% - 32.0%)
- `Jam_Tunda_Angkut`: Durasi jeda panen hingga penimbangan di PKS (2 - 48 jam)
- `Berat_Tandan_kg`: Berat tandan buah segar (8.0 - 35.0 kg)
- `Ketinggian_Blok`: Elevasi topografi blok kebun asal (30 - 450 mdpl)

Target:
- `Kelas_Mutu`: 0 (Afkir / Mentah), 1 (Standar), 2 (Matang Prima / Mutu Ekspor)
- `Rendemen_OER_%`: Persentase ekstraksi minyak aktual (16.0% - 26.5%)""")

add_code("""np.random.seed(42)
n_samples = 1500

brondolan = np.random.uniform(2.0, 35.0, n_samples)
kadar_ffa = np.random.uniform(1.0, 8.5, n_samples)
kadar_air = np.random.uniform(12.0, 32.0, n_samples)
jam_tunda = np.random.uniform(2.0, 48.0, n_samples)
berat_tandan = np.random.uniform(8.0, 35.0, n_samples)
ketinggian_blok = np.random.uniform(30.0, 450.0, n_samples)

# Skor gabungan kualitas tandan
skor_mutu = (
    0.35 * (brondolan / 35.0) -
    0.30 * (kadar_ffa / 8.5) -
    0.20 * (jam_tunda / 48.0) +
    0.15 * (berat_tandan / 35.0) +
    np.random.normal(0, 0.04, n_samples)
)

# Kategori Mutu TBS: 0 = Afkir, 1 = Standar, 2 = Prima
kelas_mutu = np.zeros(n_samples, dtype=int)
kelas_mutu[skor_mutu >= 0.08] = 1
kelas_mutu[skor_mutu >= 0.22] = 2

# Rendemen Ekstraksi Minyak Sawit (OER %) untuk uji regresi
rendemen_oer = (
    18.0 + 
    0.22 * brondolan - 
    0.85 * kadar_ffa - 
    0.08 * jam_tunda + 
    0.05 * berat_tandan + 
    np.random.normal(0, 0.45, n_samples)
)
rendemen_oer = np.clip(rendemen_oer, 15.0, 27.0)

df_sawit = pd.DataFrame({
    'Brondolan_Lepas_%': brondolan,
    'Kadar_FFA_%': kadar_ffa,
    'Kadar_Air_%': kadar_air,
    'Jam_Tunda_Angkut': jam_tunda,
    'Berat_Tandan_kg': berat_tandan,
    'Ketinggian_Blok': ketinggian_blok,
    'Kelas_Mutu': kelas_mutu,
    'Rendemen_OER_%': rendemen_oer
})

print(f"Dataset berhasil dibangkitkan! Total sampel: {len(df_sawit)}")
df_sawit.head()""")

add_md("## 3. Eksplorasi Data & Distribusi Kelas Mutu")

add_code("""fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

# Distribusi Kelas Mutu
sns.countplot(x='Kelas_Mutu', hue='Kelas_Mutu', data=df_sawit, palette='viridis', legend=False, ax=axes[0])
axes[0].set_title('Distribusi Kelas Mutu TBS Sawit', fontweight='bold')
axes[0].set_xticks([0, 1, 2])
axes[0].set_xticklabels(['Afkir (0)', 'Standar (1)', 'Prima (2)'])
axes[0].set_ylabel('Jumlah Sampel')

# Korelasi Fitur Utama vs Rendemen OER
scatter = axes[1].scatter(df_sawit['Brondolan_Lepas_%'], df_sawit['Rendemen_OER_%'], c=df_sawit['Kelas_Mutu'], cmap='viridis', alpha=0.6)
axes[1].set_title('Hubungan Brondolan Lepas vs Rendemen OER', fontweight='bold')
axes[1].set_xlabel('Brondolan Lepas (%)')
axes[1].set_ylabel('Rendemen CPO (%)')

plt.tight_layout()
plt.show()""")

add_md("## 4. Pembagian Data & Pelatihan Model Pembanding: Decision Tree Tunggal")

add_code("""fitur = ['Brondolan_Lepas_%', 'Kadar_FFA_%', 'Kadar_Air_%', 'Jam_Tunda_Angkut', 'Berat_Tandan_kg', 'Ketinggian_Blok']
X = df_sawit[fitur]
y = df_sawit['Kelas_Mutu']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Decision Tree tunggal tanpa pemangkasan (Baseline)
dt_baseline = DecisionTreeClassifier(random_state=42)
dt_baseline.fit(X_train, y_train)

dt_train_acc = dt_baseline.score(X_train, y_train)
dt_test_acc = dt_baseline.score(X_test, y_test)

print(f"Akurasi Latih Decision Tree Tunggal : {dt_train_acc * 100:.2f}% (Tanda Overfitting)")
print(f"Akurasi Uji Decision Tree Tunggal   : {dt_test_acc * 100:.2f}%")""")

add_md("""## 5. Pelatihan Random Forest Classifier dengan Validasi Out-of-Bag (OOB)

Kita melatih `RandomForestClassifier` dengan $B = 150$ pohon estimator, memilih acak $m = \\sqrt{p}$ fitur di setiap pembelahan, dan mengaktifkan `oob_score=True`.""")

add_code("""rf_clf = RandomForestClassifier(
    n_estimators=150,
    max_features='sqrt',
    max_depth=12,
    min_samples_leaf=2,
    oob_score=True,
    random_state=42,
    n_jobs=-1
)

rf_clf.fit(X_train, y_train)

rf_train_acc = rf_clf.score(X_train, y_train)
rf_oob_acc = rf_clf.oob_score_
rf_test_acc = rf_clf.score(X_test, y_test)

print(f"Akurasi Latih Random Forest    : {rf_train_acc * 100:.2f}%")
print(f"Akurasi Out-of-Bag (OOB Score) : {rf_oob_acc * 100:.2f}% (Estimasi Validasi Internal Bebas Bias)")
print(f"Akurasi Data Uji Independen    : {rf_test_acc * 100:.2f}%")""")

add_md("""## 6. Komparasi Stabilitas Kinerja: Decision Tree vs Random Forest""")

add_code("""komparasi_df = pd.DataFrame({
    'Model': ['Decision Tree Tunggal', 'Random Forest (150 Pohon)'],
    'Akurasi Latih (%)': [dt_train_acc * 100, rf_train_acc * 100],
    'Akurasi Uji (%)': [dt_test_acc * 100, rf_test_acc * 100],
    'Gap Overfitting (%)': [(dt_train_acc - dt_test_acc) * 100, (rf_train_acc - rf_test_acc) * 100]
})
print("=== TABEL KOMPARASI MODEL KLASIFIKASI TBS ===")
print(komparasi_df.to_string(index=False))""")

add_md("""## 7. Eksperimen Konvergensi Skor OOB vs Jumlah Estimator ($B$)

Menguji dinamika peningkatan akurasi internal OOB saat jumlah pohon ditingkatkan dari 15 hingga 250.""")

add_code("""tree_range = [15, 25, 40, 60, 80, 100, 150, 200, 250]
oob_scores = []
test_scores = []

for b in tree_range:
    model = RandomForestClassifier(
        n_estimators=b,
        max_features='sqrt',
        oob_score=True,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    oob_scores.append(model.oob_score_)
    test_scores.append(model.score(X_test, y_test))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(tree_range, np.array(oob_scores)*100, 'o-', color='#1e88e5', linewidth=2, label='Skor Validasi Internal (OOB)')
ax.plot(tree_range, np.array(test_scores)*100, 's--', color='#e53935', linewidth=2, label='Akurasi Uji Independen')
ax.set_title('Dinamika Konvergensi Akurasi vs Jumlah Pohon Estimator (Random Forest)', fontweight='bold')
ax.set_xlabel('Jumlah Pohon (n_estimators / B)')
ax.set_ylabel('Akurasi (%)')
ax.axvline(80, color='darkgreen', linestyle=':', label='Ambang Konvergensi Optimal (B = 80)')
ax.legend(loc='lower right')
plt.tight_layout()
plt.show()""")

add_md("""## 8. Analisis Kepentingan Fitur: MDI vs Permutation Importance

Kita membandingkan dua metode pengukuran kontribusi variabel:
1. **MDI (*Mean Decrease in Impurity*)**: Berdasarkan akumulasi perolehan Gini selama pelatihan pohon.
2. **Permutation Importance**: Berdasarkan degradasi skor saat nilai suatu fitur diacak secara acak pada data uji.""")

add_code("""# 1. Mean Decrease in Impurity (MDI)
mdi_importances = rf_clf.feature_importances_

# 2. Permutation Importance
perm_importance = permutation_importance(rf_clf, X_test, y_test, n_repeats=15, random_state=42, n_jobs=-1)
perm_mean = perm_importance.importances_mean

df_importance = pd.DataFrame({
    'Fitur': fitur,
    'MDI (%)': mdi_importances * 100,
    'Permutation (%)': perm_mean * 100
}).sort_values(by='Permutation (%)', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot MDI
df_mdi = df_importance.sort_values(by='MDI (%)', ascending=False)
sns.barplot(x='MDI (%)', y='Fitur', hue='Fitur', data=df_mdi, ax=axes[0], palette='Blues_r', legend=False)
axes[0].set_title('A. Mean Decrease in Impurity (MDI)', fontweight='bold')
axes[0].set_xlabel('Kontribusi Impurity (%)')

# Plot Permutation Importance
sns.barplot(x='Permutation (%)', y='Fitur', hue='Fitur', data=df_importance, ax=axes[1], palette='Greens_r', legend=False)
axes[1].set_title('B. Permutation Importance pada Data Uji', fontweight='bold')
axes[1].set_xlabel('Penurunan Akurasi Uji saat Diacak (%)')

plt.tight_layout()
plt.show()

print("=== TABEL KONTRIBUSI VARIABEL AGRONOMI ===")
print(df_importance.to_string(index=False))""")

add_md("## 9. Evaluasi Akhir: Matriks Konfusi & Laporan Klasifikasi Multi-Kelas")

add_code("""y_pred_rf = rf_clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred_rf)

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(
    cm, annot=True, fmt='d', cmap='Blues',
    xticklabels=['Afkir', 'Standar', 'Prima'],
    yticklabels=['Afkir', 'Standar', 'Prima'],
    ax=ax
)
ax.set_title('Matriks Konfusi Random Forest Sortasi TBS', fontweight='bold')
ax.set_xlabel('Prediksi Model Ansambel')
ax.set_ylabel('Kelas Aktual Lapangan')
plt.show()

print("=== LAPORAN EVALUASI MODEL RANDOM FOREST ===")
print(classification_report(y_test, y_pred_rf, target_names=['Afkir', 'Standar', 'Prima']))""")

add_md("""## 10. Implementasi Kasus Regresi: Prediksi Rendemen CPO (OER %)

Selain klasifikasi, Random Forest sangat handal dalam memprediksi target kontinu seperti rendemen ekstraksi minyak (*Oil Extraction Rate* / OER %).""")

add_code("""y_reg = df_sawit['Rendemen_OER_%']
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X, y_reg, test_size=0.25, random_state=42
)

rf_reg = RandomForestRegressor(
    n_estimators=120,
    max_features=1/3, # Heuristik p/3 untuk regresi
    max_depth=10,
    oob_score=True,
    random_state=42,
    n_jobs=-1
)
rf_reg.fit(X_train_r, y_train_r)

y_pred_r = rf_reg.predict(X_test_r)
r2 = r2_score(y_test_r, y_pred_r)
rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_r))

print(f"Skor R² Data Uji Rendemen CPO : {r2:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f} % OER")
print(f"OOB R² Score Data Latih       : {rf_reg.oob_score_:.4f}")

fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(y_test_r, y_pred_r, alpha=0.5, color='#2e7d32', edgecolors='k')
ax.plot([y_reg.min(), y_reg.max()], [y_reg.min(), y_reg.max()], 'r--', linewidth=2, label='Prediksi Ideal (1:1)')
ax.set_title('Aktual vs Prediksi Rendemen Minyak Sawit (OER %)', fontweight='bold')
ax.set_xlabel('Rendemen Aktual Laboratorium PKS (%)')
ax.set_ylabel('Prediksi Random Forest Regressor (%)')
ax.legend()
plt.tight_layout()
plt.show()""")

add_md("""## 11. Tugas Mandiri & Eksplorasi Mahasiswa

1. **Eksplorasi Max Features**: Uji performa klasifikasi Random Forest dengan variasi `max_features` antara `None` (semua fitur digunakan di setiap simpul / Bagging murni) versus `sqrt` versus `log2`. Analisis efeknya terhadap skor OOB dan korelasi antar-pohon!
2. **Simulasi Truk Baru**: Buat fungsi Python untuk menerima input 6 parameter mutu dari 3 truk baru yang tiba di pabrik, dan tampilkan estimasi kelas mutunya beserta probabilitas konsensus juri pohon (`predict_proba`).
3. **Analisis Kritis Limitasi Ekstrapolasi**: Buat sampel hipotetis dengan nilai `Brondolan_Lepas_%` = 60.0% (di luar rentang data latih yang maksimal 35%). Amati prediksi rendemen OER dari `RandomForestRegressor`. Mengapa model tidak mampu memprediksi di luar rentang nilai historisnya?""")

notebook_path = r"e:\Project Buku\notebooks\part-07\AI_Modul_7.5_Praktikum_Random_Forest.ipynb"
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
