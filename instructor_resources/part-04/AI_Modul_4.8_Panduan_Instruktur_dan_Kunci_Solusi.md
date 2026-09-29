# Panduan Instruktur dan Kunci Solusi
# AI Modul 4.8: Persiapan Dataset untuk AI

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) Berbasis OBE (3 SKS / 150 Menit)

Modul ini membekali mahasiswa Sarjana Sains Data, Kecerdasan Buatan, dan Teknik Pertanian dengan kecakapan tingkat lanjut dalam memformulasi data mentah menjadi representasi aljabar linier matriks fitur ($X$) dan vektor target ($y$), mengisolasi partisi data ilmiah untuk mencegah kebocoran data (*data leakage*), merekayasa fitur tabular (*feature engineering*), serta mengenkapsulasi seluruh proses pra-pemrosesan ke dalam *Scikit-Learn Pipeline*.

### 1.1 Matriks Alokasi Waktu Sesi Perkuliahan (150 Menit)

| Alokasi Waktu | Aktivitas Pembelajaran | Metode & Media | Peran Instruktur | Target Capaian Mahasiswa |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20 menit) | **Refleksi & *Problem Framing*:** Studi kasus kegagalan implementasi model AI di perkebunan akibat *data leakage* dan ilusi akurasi 99% semu. | Presentasi kasus riil, demonstrasi *overfitting* laboratorium. | Memandu diskusi kritis mengenai bahaya *data snooping* dan anomali evaluasi akurasi semu. | Mahasiswa menyadari bahwa model AI yang berkinerja sempurna di laboratorium dapat gagal total di kebun jika terjadi kebocoran data. |
| **00:20 - 00:50** (30 menit) | **Dekonstruksi Teori & Metodologi:** Pemisahan $X$ dan $y$, partisi bertingkat (*Stratified K-Fold*), komparasi skala numerik, dan enkoding kategori. | Ceramah konsep mendalam, visualisasi diagram alur pipeline. | Membedah perbedaan dampak penskalaan pada model berbasis gradien vs model berbasis pohon (*tree-based*). | Mahasiswa memahami kriteria pemilihan *StandardScaler* vs *RobustScaler* dan *OneHot* vs *OrdinalEncoder*. |
| **00:50 - 01:25** (35 menit) | **Praktikum Terbimbing (Hands-on Lab):** Eksperimen pembuatan dataset kebun, simulasi *data leakage*, dan perakitan *ColumnTransformer*. | *Live coding* terbimbing di Jupyter Notebook. | Mendampingi mahasiswa mengonfigurasi sub-pipeline untuk fitur numerik dan kategorikal. | Mahasiswa berhasil menyusun objek `ColumnTransformer` yang menggabungkan berbagai transformasi data heterogen. |
| **01:25 - 02:10** (45 menit) | **Penyelesaian Kasus HOTS Mandiri:** Pengerjaan tantangan audit kode asisten pemula (9.1), perancangan ColumnTransformer kompleks (9.2), dan penanganan Ganoderma (9.3). | Kerja mandiri berbasis tim kecil (*pair programming*). | Memfasilitasi *code review*, memeriksa logika isolasi data uji mahasiswa. | Mahasiswa mampu merekayasa kode bebas bocor dan menerapkan strategi penyeimbangan kelas minoritas. |
| **02:10 - 02:30** (20 menit) | **Evaluasi Formatif & Refleksi Akhir Part 4:** Pembahasan kunci solusi, penarikan benang merah seluruh Part 4 (Data Science dengan Python), dan pengantar Part 5 (Fundamental Machine Learning). | Diskusi kelas interaktif, sintesis capaian pembelajaran. | Memberikan umpan balik terukur dan memvalidasi kesiapan mahasiswa melangkah ke algoritma pemodelan AI. | Mahasiswa siap mengaplikasikan dataset terstandar ke dalam algoritma machine learning pada modul-modul berikutnya. |

---

## 2. Matriks Identifikasi & Remedi Miskonsepsi Umum Mahasiswa

| No | Miskonsepsi Mahasiswa | Realitas Teknis & Konseptual | Pendekatan Remedi Instruktur |
| :--- | :--- | :--- | :--- |
| 1 | "Penskalaan fitur (misal dengan `StandardScaler`) boleh dilakukan pada seluruh dataset sebelum memanggil `train_test_split()` agar seluruh data seragam." | Tindakan ini merupakan pelanggaran fatal metodologi ilmiah yang disebut **Kebocoran Data Kontaminasi (*Train-Test Contamination*)**. Data latih terkontaminasi oleh informasi nilai mean ($\mu$) dan deviasi standar ($\sigma$) dari data uji, menghasilkan metrik akurasi pengujian yang over-optimistis secara palsu. | Tunjukkan secara numerik perbedaan nilai mean populasi vs mean data latih. Tanamkan doktrin: **Aturan Emas: `.fit()` HANYA boleh dipanggil pada $X_{\text{train}}$!** |
| 2 | "Model klasifikasi penyakit tanaman yang mencapai nilai akurasi $99\%$ sudah pasti sangat andal dan siap diproduksi massal." | Jika prevalensi penyakit di kebun hanya $1\%$, model bodoh (*dummy classifier*) yang selalu memprediksi semua tanaman "SEHAT" akan memperoleh akurasi $99\%$ secara otomatis, namun model tersebut memiliki nilai **Recall = 0%** (sama sekali tidak menemukan pohon sakit). | Tunjukkan matriks konfusi (*confusion matrix*). Bimbing mahasiswa untuk tidak pernah menggunakan metrik *Accuracy* tunggal pada dataset tidak seimbang, melainkan *Recall*, *F1-Score*, atau *Precision-Recall AUC*. |
| 3 | "Semua variabel kategorikal (seperti nama varietas tanaman atau jenis tanah) harus diubah menjadi angka bulat 1, 2, 3 menggunakan Ordinal Encoding." | Variabel nominal tidak memiliki derajat tingkatan. Jika jenis tanah Alluvial diberi angka 1, Gambut 2, dan Podsolik 3, algoritma regresi linier atau jaringan saraf tiruan akan mengasumsikan tanah Podsolik memiliki magnitude $3\times$ lebih besar dari Alluvial, memicu distorsi hubungan fungsional. | Tekankan penggunaan **One-Hot Encoding** untuk variabel nominal non-berurutan, dan batasi **Ordinal Encoding** khusus untuk variabel yang memiliki hierarki nyata (misal: tingkat kematangan buah atau kerapatan gulma). |
| 4 | "Algoritma Random Forest dan XGBoost membutuhkan penskalaan fitur numerik agar proses pembagian simpul (*tree splitting*) optimal." | Pohon keputusan bersifat **invarian terhadap transformasi monotonik**. Pembagian simpul dilakukan murni berdasar urutan peringkat (*rank-order*), sehingga skala nilai $[0, 1]$ atau $[0, 10000]$ menghasilkan partisi simpul yang identik secara matematis. | Demonstrasikan pelatihan Random Forest pada data berskala asli vs data berskala standard, dan tunjukkan bahwa akurasi dan batas partisi pohon tidak berubah sama sekali. Jelaskan bahwa penskalaan diwajibkan untuk model berbasis jarak (k-NN, SVM) dan gradien (Neural Network). |

---

## 3. Panduan Solusi Lengkap Latihan HOTS (Higher-Order Thinking Skills)

### 3.1 Solusi Tantangan 9.1: Audit dan Pencegahan Kebocoran Data (Bobot: 30%)

#### 1. Dua Titik Kebocoran Data (*Data Leakage*):
- **Titik Kebocoran 1 (Langkah A - Imputasi Global):** Baris `X = X.fillna(X.mean())` menghitung rata-rata kolom dari seluruh dataset sebelum partisi train-test. Nilai rata-rata tersebut mencakup sampel yang seharusnya berada di data uji, sehingga informasi masa depan bocor ke dalam data latih.
- **Titik Kebocoran 2 (Langkah B - Penskalaan Global):** Baris `scaler.fit_transform(X)` menghitung parameter $\mu$ dan $\sigma$ dari gabungan seluruh observasi. Ini melanggar prinsip isolasi data uji (*train-test contamination*).

#### 2. Dampak Matematis terhadap Nilai $R^2$ di Masa Depan:
Model yang dievaluasi dengan data uji yang sudah terkontaminasi akan melaporkan skor $R^2$ yang tinggi (misal $R^2 = 0.88$). Namun, saat diterapkan pada data produksi kebun tahun depan di mana distribusi fitur bergeser sedikit, model akan mengalami degradasi kinerja drastis (*performance collapse*), sering kali menghasilkan $R^2 < 0.40$ atau bahkan negatif, karena model gagal menggeneralisasi data yang benar-benar asing.

#### 3. Kode Perbaikan Bebas Bocor Menggunakan Scikit-Learn Pipeline:
```python
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
import pandas as pd

# 1. Muat dataset dan eliminasi identifier
df = pd.read_csv('dataset_rendemen_sawit.csv')
X = df.drop(columns=['No_Sampel', 'Rendemen_Minyak_Persen'])
y = df['Rendemen_Minyak_Persen']

# 2. PISAHKAN DATA TERLEBIH DAHULU (Zero Leakage Principle)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Susun pipeline terenkapsulasi
pipeline_rendemen = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('regressor', Ridge())
])

# 4. Fit HANYA pada data latih (statistik dihitung eksklusif dari X_train)
pipeline_rendemen.fit(X_train, y_train)

# 5. Evaluasi obyektif pada data uji murni
r2_train = pipeline_rendemen.score(X_train, y_train)
r2_test = pipeline_rendemen.score(X_test, y_test)

print(f"R2 Score Latih: {r2_train:.3f}")
print(f"R2 Score Uji (Jujur & Bebas Bocor): {r2_test:.3f}")
```

---

### 3.2 Solusi Tantangan 9.2: Desain ColumnTransformer Heterogen (Bobot: 40%)

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, StandardScaler, OneHotEncoder, OrdinalEncoder, FunctionTransformer
import numpy as np

# 1. Definisi daftar kolom berdasarkan karakteristik data
kolom_num_robust = ['Curah_Hujan_mm', 'Tinggi_Muka_Air_Gambut_cm', 'Suhu_Maksimum_C']
kolom_num_standard = ['Usia_Tanaman_Tahun', 'Dosis_Urea_kg', 'Dosis_MOP_kg']
kolom_cat_nominal = ['Jenis_Tanah', 'Sistem_Drainase']
kolom_cat_ordinal = ['Tingkat_Gulma']

# 2. Sub-pipeline untuk numerik rentan outlier (Median + RobustScaler)
pipe_robust = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', RobustScaler())
])

# 3. Sub-pipeline untuk numerik normal (Mean + StandardScaler)
pipe_standard = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# 4. Sub-pipeline untuk kategorikal nominal (Most Frequent + OneHotEncoder drop first)
pipe_nominal = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
])

# 5. Sub-pipeline untuk kategorikal ordinal (Most Frequent + OrdinalEncoder hierarki)
urutan_gulma = [['Bersih', 'Sedang', 'Padat']]
pipe_ordinal = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OrdinalEncoder(categories=urutan_gulma))
])

# 6. Transformator rasio pupuk (Dosis Urea / (Dosis MOP + 0.1))
def hitung_rasio_pupuk(X):
    # Kolom 0: Dosis Urea, Kolom 1: Dosis MOP
    urea = X[:, [0]]
    mop = X[:, [1]]
    return urea / (mop + 0.1)

pipe_rasio_pupuk = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('rasio', FunctionTransformer(hitung_rasio_pupuk, validate=True)),
    ('scaler', StandardScaler())
])

# 7. Integrasi seluruh sub-pipeline ke dalam ColumnTransformer
preprocessor_kompleks = ColumnTransformer(transformers=[
    ('num_rob', pipe_robust, kolom_num_robust),
    ('num_std', pipe_standard, kolom_num_standard),
    ('cat_nom', pipe_nominal, kolom_cat_nominal),
    ('cat_ord', pipe_ordinal, kolom_cat_ordinal),
    ('feat_rasio', pipe_rasio_pupuk, ['Dosis_Urea_kg', 'Dosis_MOP_kg'])
], remainder='drop')

print("ColumnTransformer heterogen perkebunan berhasil dikonfigurasi secara modular.")
```

---

### 3.3 Solusi Tantangan 9.3: Penanganan Ketidakseimbangan Penyakit Ganoderma (Bobot: 30%)

#### 1. Bahaya Metrik Akurasi 99.0%:
Dengan prevalensi penyakit sebesar $1.0\%$ ($6.000$ pohon terinfeksi dari $600.000$ total pohon):
Jika model selalu memprediksi semua pohon berstatus **SEHAT (0)**, maka:
$$\text{Akurasi} = \frac{594.000 \text{ Benar}}{600.000 \text{ Total}} = 99.0\%$$
Namun, seluruh $6.000$ pohon yang sakit tidak terdeteksi sama sekali ($\text{Recall} = 0\%$). Jamur *Ganoderma boninense* menular melalui kontak akar di dalam tanah. Membiarkan ribuan pohon terinfeksi tanpa penanganan karantina akan memicu epidemi pembusukan pangkal batang di seluruh kebun, menyebabkan kebangkrutan operasional perkebunan. Akurasi 99% ini adalah **ilusi matematis yang mematikan**.

#### 2. Precision vs Recall dalam Deteksi Ganoderma:
- **Precision:** Dari seluruh tanaman yang diprediksi sakit oleh model, berapa persen yang benar-benar sakit?
  $$\text{Precision} = \frac{TP}{TP + FP}$$
  *Biaya False Positive (FP):* Tim agronomis membuang waktu dan biaya uji laboratorium untuk memeriksa pohon sehat yang dicurigai sakit.
- **Recall (Sensitivitas):** Dari seluruh pohon yang benar-benar terserang Ganoderma di lapangan, berapa persen yang berhasil dideteksi oleh model?
  $$\text{Recall} = \frac{TP}{TP + FN}$$
  *Biaya False Negative (FN):* Pohon sakit lolos dari deteksi, sporanya menyebar ke pohon-pohon tetangga, dan pohon akhirnya tumbang mati.
- **Rekomendasi Manajemen Kebun:** Kepala kebun **wajib memprioritaskan RECALL**. Biaya memeriksa sampel pohon sehat (konsekuensi *False Positive*) jauh lebih murah daripada kerugian kehilangan puluhan hektar tanaman produktif akibat lolosnya infeksi jamur mematikan (konsekuensi *False Negative*).

#### 3. Konfigurasi `class_weight='balanced'` dan Rumus Otomatisnya:
```python
from sklearn.ensemble import RandomForestClassifier

# Konfigurasi model klasifikasi dengan pembobotan biaya rugi seimbang
model_ganoderma = RandomForestClassifier(
    n_estimators=150,
    class_weight='balanced',
    random_state=42
)
```

- **Rumus Bobot Kelas Otomatis Scikit-Learn:**
  $$w_c = \frac{N}{C \times N_c}$$
  Di mana:
  - $N = 600.000$ (Total pohon)
  - $C = 2$ (Jumlah kelas: Sehat dan Terinfeksi)
  - $N_0 = 594.000$ (Pohon sehat)
  - $N_1 = 6.000$ (Pohon sakit)

- **Kalkulasi Bobot Masing-Masing Kelas:**
  $$w_0 (\text{Sehat}) = \frac{600.000}{2 \times 594.000} \approx 0.505$$
  $$w_1 (\text{Ganoderma}) = \frac{600.000}{2 \times 6.000} = \frac{600.000}{12.000} = 50.0$$

Setiap kali model melakukan kesalahan prediksi pada satu pohon terinfeksi Ganoderma, model akan dikenakan **penalti rugi sebesar $50.0$ kali lipat** dibandingkan jika salah memprediksi pohon sehat. Hal ini memaksa algoritma optimasi untuk memprioritaskan deteksi kelas minoritas secara agresif.

---

## 4. Rubrik Penilaian Portofolio Praktikum Berbasis OBE

| Kriteria Penilaian | Bobot | Sangat Memuaskan (85 - 100) | Memuaskan (70 - 84) | Kurang Memuaskan (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Integritas Partisi & Pencegahan Leakage** | 25% | Mengisolasi partisi train-test secara mutlak; seluruh perhitungan parameter pra-pemrosesan (`.fit()`) dieksekusi hanya pada data latih. | Memisahkan data dengan benar namun masih terdapat kebocoran minor pada imputasi nilai kosong. | Menjalankan normalisasi atau imputasi sebelum `train_test_split()`, memicu kontaminasi data uji. |
| **Ketepatan Rekayasa Fitur Heterogen** | 25% | Memilih metode enkoding (One-Hot vs Ordinal) dan penskalaan (Standard vs Robust) dengan justifikasi tipe dan distribusi data yang tepat. | Menerapkan enkoding dan penskalaan namun kurang mempertimbangkan resistensi terhadap outlier. | Salah menerapkan Ordinal Encoding pada data nominal atau mengabaikan kebutuhan penskalaan pada model berbasis jarak. |
| **Penanganan Ketidakseimbangan Kelas** | 25% | Mampu mengonfigurasi penalti kerugian (`class_weight`) dan mengevaluasi model berbasis metrik Recall/PR-AUC secara kritis. | Menerapkan pembobotan kelas namun analisis metrik evaluasi masih terfokus pada akurasi. | Mengabaikan ketidakseimbangan kelas sehingga model menghasilkan *zero recall* pada kelas target minoritas. |
| **Arsitektur Pipeline Terpadu** | 25% | Membangun `ColumnTransformer` dan `Pipeline` Scikit-Learn yang modular, bersih, dapat digunakan ulang, dan bebas galat eksekusi. | Menyusun pipeline fungsional namun pengelompokan transformer masih kaku atau belum memanfaatkan ColumnTransformer. | Transformasi data dilakukan secara manual terpisah-pisah di luar struktur Pipeline, rentan kesalahan manusia. |
