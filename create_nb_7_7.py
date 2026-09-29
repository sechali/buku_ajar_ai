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

add_md(r"""# AI Modul 7.7: Praktikum Support Vector Machine (SVM)

**Mata Kuliah:** Kecerdasan Buatan & Pembelajaran Mesin Terapan  
**Institusi:** Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Studi Kasus:** Autentikasi Mutu & Deteksi Pemalsuan Minyak Kelapa Sawit Mentah (CPO) Berbasis Spektroskopi Near-Infrared (NIR) Menggunakan Support Vector Machine

---

### Capaian Pembelajaran Praktikum
1. Mampu membangun *pipeline* terstandarisasi Support Vector Machine (`StandardScaler` + `SVC`) menggunakan pustaka Scikit-Learn.
2. Mampu mengekstraksi dan menginterpretasikan titik-titik Vektor Pendukung (*Support Vectors*) yang membentuk batas keputusan geometris.
3. Mampu membandingkan performa batas pemisah antara Kernel Linier, Polinomial, dan Radial Basis Function (RBF).
4. Mampu menganalisis efek interaksi hyperparameter penalti kesalahan ($C$) dan lebar jangkauan kernel ($\gamma$) pada visualisasi batas keputusan 2D.""")

add_md("## 1. Import Pustaka & Konfigurasi Lingkungan")

add_code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Pengaturan visualisasi
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 120

print("[OK] Seluruh pustaka Support Vector Machine berhasil dimuat!")""")

add_md(r"""## 2. Pembangkitan Dataset Spektroskopi NIR Mutu CPO

Pita absorbansi spektroskopi Near-Infrared (NIR) pada 6 panjang gelombang analitik:
- `NIR_1200nm`: Wilayah pita overtone kedua ikatan C-H trigliserida
- `NIR_1450nm`: Pita serapan ikatan O-H (indikator kadar air/moisture)
- `NIR_1720nm`: Pita overtone pertama ikatan C-H rantai ester
- `NIR_1940nm`: Pita kombinasi O-H dan C=O (indikator asam lemak bebas / FFA)
- `NIR_2150nm`: Pita serapan gugus karboksilat
- `NIR_2300nm`: Pita kombinasi C-H hidrokarbon

Target Kelas:
- `+1`: CPO Murni Mutu Ekspor (Air rendah, FFA rendah, DOBI prima)
- `-1`: CPO Tercemar / Teroksidasi (Air tinggi, FFA tinggi, mutu anjlok)""")

add_code("""np.random.seed(42)
n_samples = 400

y_cpo = np.random.choice([-1, 1], size=n_samples, p=[0.35, 0.65])

X_spectra = np.zeros((n_samples, 6))
for i in range(n_samples):
    if y_cpo[i] == 1:   # CPO Murni
        X_spectra[i, 0] = np.random.normal(0.45, 0.03)
        X_spectra[i, 1] = np.random.normal(0.22, 0.02)
        X_spectra[i, 2] = np.random.normal(0.85, 0.04)
        X_spectra[i, 3] = np.random.normal(0.18, 0.02)
        X_spectra[i, 4] = np.random.normal(0.60, 0.03)
        X_spectra[i, 5] = np.random.normal(0.72, 0.04)
    else:               # CPO Tercemar
        X_spectra[i, 0] = np.random.normal(0.52, 0.05)
        X_spectra[i, 1] = np.random.normal(0.48, 0.06)
        X_spectra[i, 2] = np.random.normal(0.74, 0.05)
        X_spectra[i, 3] = np.random.normal(0.42, 0.05)
        X_spectra[i, 4] = np.random.normal(0.66, 0.04)
        X_spectra[i, 5] = np.random.normal(0.61, 0.06)

col_names = ['NIR_1200nm', 'NIR_1450nm', 'NIR_1720nm', 'NIR_1940nm', 'NIR_2150nm', 'NIR_2300nm']
df_cpo = pd.DataFrame(X_spectra, columns=col_names)
df_cpo['Mutu_CPO'] = y_cpo

print(f"Dataset Spektra CPO berhasil dibangkitkan: {df_cpo.shape[0]} sampel")
df_cpo.head()""")

add_md("## 3. Eksplorasi Visual: Profil Spektrum Absorbansi Rata-rata CPO")

add_code("""wavelengths = [1200, 1450, 1720, 1940, 2150, 2300]
mean_murni = df_cpo[df_cpo['Mutu_CPO'] == 1][col_names].mean().values
std_murni = df_cpo[df_cpo['Mutu_CPO'] == 1][col_names].std().values

mean_cemar = df_cpo[df_cpo['Mutu_CPO'] == -1][col_names].mean().values
std_cemar = df_cpo[df_cpo['Mutu_CPO'] == -1][col_names].std().values

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(wavelengths, mean_murni, 'o-', color='#2e7d32', linewidth=2.5, label='CPO Murni (+1)')
ax.fill_between(wavelengths, mean_murni - std_murni, mean_murni + std_murni, color='#2e7d32', alpha=0.2)

ax.plot(wavelengths, mean_cemar, 's--', color='#d32f2f', linewidth=2.5, label='CPO Tercemar (-1)')
ax.fill_between(wavelengths, mean_cemar - std_cemar, mean_cemar + std_cemar, color='#d32f2f', alpha=0.2)

ax.set_title('Profil Kurva Rata-rata Spektrum Absorbansi NIR CPO Murni vs Tercemar', fontweight='bold')
ax.set_xlabel('Panjang Gelombang (nm)')
ax.set_ylabel('Absorbansi (A.U.)')
ax.legend(loc='upper left')
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

add_md("## 4. Pembagian Data & Membangun Pipeline StandardScaler + SVC")

add_code("""X = df_cpo[col_names]
y = df_cpo['Mutu_CPO']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Konstruksi Pipeline (Kewajiban Mutlak Standardisasi pada SVM)
svm_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf', C=10.0, gamma='scale', random_state=42))
])

svm_pipe.fit(X_train, y_train)

train_acc = svm_pipe.score(X_train, y_train)
test_acc = svm_pipe.score(X_test, y_test)

print(f"Akurasi Latih SVM Pipeline : {train_acc * 100:.2f}%")
print(f"Akurasi Uji SVM Pipeline   : {test_acc * 100:.2f}%")""")

add_md(r"""## 5. Ekstraksi Vektor Pendukung (*Support Vectors*)

Meneliti sampel-sampel kritis yang berada tepat di perbatasan margin.""")

add_code("""svm_model = svm_pipe.named_steps['svm']
n_sv = svm_model.support_vectors_.shape[0]
n_samples_train = len(X_train)

print("=== PROFIL VEKTOR PENDUKUNG (SUPPORT VECTORS) ===")
print(f"Total Sampel Pelatihan : {n_samples_train}")
print(f"Jumlah Support Vectors : {n_sv} ({n_sv / n_samples_train * 100:.1f}% dari data latih)")
print(f"Distribusi SV per Kelas: Tercemar = {svm_model.n_support_[0]}, Murni = {svm_model.n_support_[1]}")
print(f"Nilai Intersep Bias b  : {svm_model.intercept_[0]:.4f}")""")

add_md("## 6. Evaluasi Model: Matriks Konfusi & Laporan Klasifikasi")

add_code("""y_pred = svm_pipe.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(
    cm, annot=True, fmt='d', cmap='Blues',
    xticklabels=['Tercemar (-1)', 'Murni (+1)'],
    yticklabels=['Tercemar (-1)', 'Murni (+1)'],
    ax=ax
)
ax.set_title('Matriks Konfusi Autentikasi CPO (SVM RBF)', fontweight='bold')
ax.set_xlabel('Prediksi Model SVM')
ax.set_ylabel('Aktual Laboratorium')
plt.show()

print("=== LAPORAN EVALUASI MODEL SVM KERNEL RBF ===")
print(classification_report(y_test, y_pred, target_names=['Tercemar (-1)', 'Murni (+1)']))""")

add_md("## 7. Eksperimen Komparasi Jenis Kernel (Linear vs Poly vs RBF)")

add_code("""kernels = ['linear', 'poly', 'rbf']
kernel_results = []

for k in kernels:
    p = Pipeline([
        ('scaler', StandardScaler()),
        ('svm', SVC(kernel=k, C=10.0, random_state=42))
    ])
    p.fit(X_train, y_train)
    n_v = p.named_steps['svm'].support_vectors_.shape[0]
    kernel_results.append({
        'Kernel': k.upper(),
        'Akurasi Latih (%)': p.score(X_train, y_train) * 100,
        'Akurasi Uji (%)': p.score(X_test, y_test) * 100,
        'Jumlah Support Vectors': n_v
    })

df_kernels = pd.DataFrame(kernel_results)
print("=== KOMPARASI KINERJA BERBAGAI FUNGSI KERNEL SVM ===")
print(df_kernels.to_string(index=False))""")

add_md(r"""## 8. Visualisasi Batas Keputusan 2D & Eksperimen Parameter $C$ dan $\gamma$

Menggunakan 2 fitur paling diskriminatif (`NIR_1450nm` air dan `NIR_1940nm` asam) untuk memvisualisasikan kontur hiperbidang non-linier.""")

add_code("""X_2d = df_cpo[['NIR_1450nm', 'NIR_1940nm']]
scaler_2d = StandardScaler()
X_2d_scaled = scaler_2d.fit_transform(X_2d)

# Variasi Gamma untuk Kernel RBF
gammas = [0.1, 1.0, 10.0]
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Meshgrid untuk visualisasi kontur
x_min, x_max = X_2d_scaled[:, 0].min() - 0.5, X_2d_scaled[:, 0].max() + 0.5
y_min, y_max = X_2d_scaled[:, 1].min() - 0.5, X_2d_scaled[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))

for idx, g in enumerate(gammas):
    clf = SVC(kernel='rbf', C=10.0, gamma=g, random_state=42)
    clf.fit(X_2d_scaled, y)
    
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    axes[idx].contourf(xx, yy, Z, levels=[-100, 0, 100], alpha=0.3, colors=['#d32f2f', '#2e7d32'])
    axes[idx].contour(xx, yy, Z, levels=[0], linewidths=2.5, colors=['#1565c0'])
    axes[idx].contour(xx, yy, Z, levels=[-1, 1], linewidths=1.5, linestyles='--', colors=['#d32f2f', '#2e7d32'])
    
    # Plot data points
    axes[idx].scatter(X_2d_scaled[y==1, 0], X_2d_scaled[y==1, 1], color='#2e7d32', s=25, label='Murni (+1)')
    axes[idx].scatter(X_2d_scaled[y==-1, 0], X_2d_scaled[y==-1, 1], color='#d32f2f', s=25, label='Tercemar (-1)')
    
    # Lingkari support vectors
    svs = clf.support_vectors_
    axes[idx].scatter(svs[:, 0], svs[:, 1], s=80, facecolors='none', edgecolors='k', linewidths=1.2)
    
    axes[idx].set_title(f'RBF SVM: C=10, Gamma={g} ({len(svs)} SV)', fontweight='bold')
    axes[idx].set_xlabel('NIR 1450nm (Air)')
    axes[idx].set_ylabel('NIR 1940nm (FFA)')
    axes[idx].legend(loc='upper left', fontsize=8)

plt.tight_layout()
plt.show()""")

add_md("## 9. Simulasi Inspeksi Spektroskopi Sampel Truk Tangki Baru")

add_code("""truk_tangki = pd.DataFrame([
    # Truk 1: Absorbansi air dan FFA rendah (CPO Murni Ekspor)
    {'NIR_1200nm': 0.44, 'NIR_1450nm': 0.21, 'NIR_1720nm': 0.86, 'NIR_1940nm': 0.17, 'NIR_2150nm': 0.59, 'NIR_2300nm': 0.73},
    # Truk 2: Absorbansi air tinggi dan FFA tinggi (CPO Tercemar)
    {'NIR_1200nm': 0.53, 'NIR_1450nm': 0.50, 'NIR_1720nm': 0.72, 'NIR_1940nm': 0.44, 'NIR_2150nm': 0.67, 'NIR_2300nm': 0.60}
])

hasil_pred = svm_pipe.predict(truk_tangki)
jarak_margin = svm_pipe.decision_function(truk_tangki)

label_teks = {1: 'LAYAK EKSPOR (MURNI)', -1: 'DITOLAK / TERCEMAR'}

print("=== HASIL INSPEKSI SPEKTROSKOPI ONLINE DI TERMINAL BULKING ===")
for i in range(len(truk_tangki)):
    print(f"\\n--- Truk Tangki #{i+1} ---")
    print(f"Keputusan Sistem : {label_teks[hasil_pred[i]]}")
    print(f"Jarak ke Margin  : {jarak_margin[i]:+.4f} (Positif = Wilayah Murni, Negatif = Wilayah Tercemar)")""")

add_md(r"""## 10. Tugas Mandiri & Eksplorasi Mahasiswa

1. **Uji Tanpa StandardScaler**: Latih model SVM langsung pada data mentah $X$ tanpa `StandardScaler`. Bandingkan akurasi uji dan jumlah vektor pendukung dengan model yang distandardisasi. Jelaskan perbedaannya!
2. **Eksplorasi Grid Search Parameter C**: Lakukan `GridSearchCV` dengan variasi parameter $C \in [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]$. Amati bagaimana kenaikan $C$ memengaruhi jumlah Vektor Pendukung yang terpilih.
3. **Analisis Transisi Paradigma**: Semua algoritma dari 7.1 hingga 7.7 memerlukan label kelas $y$ untuk belajar. Bagaimana jika di lapangan perkebunan kita memiliki ribuan data spektrum tanah tanpa ada label kelas mutu sama sekali? Jelaskan bagaimana algoritma Unsupervised Learning seperti K-Means (AI Modul 7.8) memecahkan masalah ini!""")

notebook_path = r"e:\Project Buku\notebooks\part-07\AI_Modul_7.7_Praktikum_Support_Vector_Machine.ipynb"
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
