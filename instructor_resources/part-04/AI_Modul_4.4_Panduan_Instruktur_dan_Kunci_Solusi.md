# AI Modul 4.4: Panduan Instruktur dan Kunci Solusi
## Data Cleaning dan Preprocessing: Mitigasi Anomali Sensor, Imputasi, dan Pipeline Bebas Kebocoran Data

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

| Komponen | Rincian Instruksional |
| :--- | :--- |
| **Mata Kuliah** | Sains Data & Kecerdasan Buatan Terapan |
| **Kode Modul** | AI Modul 4.4 |
| **Topik Pembelajaran** | Prinsip GIGO, Mekanisme Data Hilang (MCAR/MAR/MNAR), Deteksi Pencilan, Imputasi, dan Scikit-Learn Pipeline |
| **Alokasi Waktu** | 3 SKS (150 Menit Tatap Muka/Laboratorium + 180 Menit Belajar Mandiri) |
| **Prasyarat** | AI Modul 4.3 (Pandas untuk Manipulasi Data) |
| **Target OBE** | Sub-CPMK 4.4: Mahasiswa mampu merancang pipeline pembersihan data otomatis yang mengintegrasikan imputasi berbasis domain, mitigasi pencilan via *Winsorizing*, dan penskalaan fitur kebal kebocoran data (*data leakage*). |

### Matriks Distribusi Jam Pembelajaran (150 Menit)
1. **Sesi Pembuka & Refleksi Integritas Data (30 Menit):**
   - Paradigma *Garbage In, Garbage Out* (GIGO) dalam sistem AI perkebunan skala industri.
   - Teori probabilitas tiga mekanisme hilangnya data Donald Rubin (MCAR, MAR, MNAR) dengan studi kasus lapangan sawit.
2. **Sesi Telaah Konseptual & Pembuktian Matematis (30 Menit):**
   - Mengapa $Z$-score gagal (*masking effect*) pada sampel data miring beroutlier ekstrim.
   - Matematika batas interkuartil Tukey IQR, *Modified Z-Score* berbasis MAD, dan teknik kliping *Winsorizing*.
3. **Praktikum Laboratorium Terbimbing (60 Menit):**
   - Eksplorasi berkas `notebooks/part-04/AI_Modul_4.4_Praktikum_Data_Cleaning_dan_Preprocessing.ipynb`.
   - Audit data hilang, deduplikasi baris ganda, dan standardisasi variasi teks afdeling dengan Regex.
   - Deteksi pencilan probe sensor tanah dan visualisasi boxplot perbandingan *Winsorizing*.
   - Pembangunan arsitektur pipeline terpadu `ColumnTransformer` + `Pipeline` Scikit-Learn.
4. **Sesi Evaluasi & Diskusi HOTS (30 Menit):**
   - Pembahasan kasus kebocoran data (*data leakage*) akibat pemanggilan `fit_transform` sebelum `train_test_split`.
   - Presentasi strategi mitigasi anomali sensorik cuaca ekstrem di perbukitan vs dataran rendah.

---

## 2. Strategi Pedagogis dan Panduan Fasilitasi Kelas

### 2.1 Demonstrasi "The Illusion of High Accuracy" (Membongkar Data Leakage)
Lakukan demonstrasi langsung di depan mahasiswa:
1. Latih model regresi di mana penskalaan (`StandardScaler`) dilakukan **sebelum** pembagian data latih dan uji. Tunjukkan bahwa nilai $R^2$ terlihat tinggi secara artifisial.
2. Kemudian uji model yang sama pada data pengujian baru yang independen (misalnya data afdeling lain yang belum pernah dilihat). Tunjukkan bahwa performanya jatuh drastis.
3. Simpulkan kepada mahasiswa: *"Penskalaan sebelum split adalah bentuk kecurangan ilmiah (data leakage) karena model 'mencuri intip' rata-rata dan deviasi data uji."*

### 2.2 Penekanan Konseptual: "Outlier Biologis vs Outlier Teknis"
Ingatkan mahasiswa bahwa di bidang pertanian tropis:
- **Pencilan Teknis (Wajib Dieliminasi/Dikliping):** Nilai yang mustahil secara hukum fisika/biologi, seperti kelembaban tanah $98.7\%$ pada tanah mineral atau suhu kanopi $70^\circ\text{C}$ akibat sensor korslet.
- **Pencilan Biologis (Wajib Dipertahankan):** Lonjakan tonase panen pada pohon sawit yang memasuki periode panen raya (*peak crop*). Menghapus pencilan biologis akan menghilangkan wawasan kapasitas puncak kebun.

---

## 3. Identifikasi dan Remediasi Miskonsepsi Mahasiswa

### Miskonsepsi 1: "Semua nilai kosong (`NaN`) cukup diimputasi dengan nilai rata-rata (*mean*)."
- **Koreksi Konseptual:** Imputasi rata-rata hanya valid untuk data yang berdistribusi normal murni tanpa pencilan. Pada data miring (*skewed*) seperti curah hujan atau serangan hama, nilai rerata tertarik oleh nilai ekstrem. Selain itu, jika mekanisme hilangnya adalah MAR atau MNAR, imputasi rerata merusak matriks kovarians dan mengecilkan variansi alami data secara artifisial (*underestimating variance*).

### Miskonsepsi 2: "Semua pencilan (*outliers*) harus dihapus (*drop rows*) dari tabel."
- **Koreksi Konseptual:** Menghapus baris pencilan secara serampangan akan mengurangi ukuran sampel secara drastis dan membuang informasi berharga mengenai kondisi ekstrem lingkungan perkebunan. Pendekatan yang jauh lebih bijak dan terstandar adalah teknik **Winsorizing** (kliping ke batas kuartil atas/bawah), yang menetralisir distorsi nilai ekstrem tanpa membuang baris observasi.

### Miskonsepsi 3: "Scaling data (`StandardScaler` / `RobustScaler`) boleh dilakukan di awal sebelum `train_test_split`."
- **Koreksi Konseptual:** Ini adalah akar dari fenomena *Data Leakage*. Parameter statistik seperti rata-rata $\mu$, median $\tilde{x}$, atau rentang IQR harus dihitung **hanya dari data latih (*training set*)**. Data uji harus diperlakukan sebagai data masa depan yang sama sekali belum diketahui distribusinya.

### Miskonsepsi 4: "Metode $Z$-score selalu ampuh mendeteksi pencilan pada semua jenis data."
- **Koreksi Konseptual:** Pada kumpulan data dengan satu atau dua pencilan ekstrem yang sangat besar, nilai rerata ($\bar{x}$) dan deviasi standar ($s$) itu sendiri akan tergelembungkan secara masif. Akibatnya, nilai pencilan ekstrem tersebut justru memiliki skor $Z$ yang relatif kecil ($< 3.0$) sehingga gagal terdeteksi. Fenomena ini disebut *masking effect*. Metode non-parametrik (Tukey IQR) atau *Modified Z-Score* berbasis MAD jauh lebih kebal terhadap efek ini.

---

## 4. Kunci Solusi dan Pembahasan Soal Latihan & HOTS

### 4.1 Pembahasan Analisis Mekanisme Data Hilang (Bobot: 30%)

**1. Klasifikasi Mekanisme Rubin:**
- **Pola A (Sensor Mati Akibat Petir dan Angin Kencang di Perbukitan):**
  - **Klasifikasi: MAR (*Missing at Random*).**
  - *Alasan Ilmiah:* Hilangnya data curah hujan tidak terjadi secara acak murni, melainkan berkaitan langsung secara sistematis dengan variabel lingkungan teramati lainnya, yaitu kejadian cuaca ekstrem (angin kencang, petir, dan topografi perbukitan). Jika model memiliki data kecepatan angin atau tekanan udara, probabilitas hilangnya data dapat diprediksi secara matematis ($P(M \mid \text{Cuaca Ekstrem})$).
- **Pola B (Server Maintenance Berkala Setiap Hari Minggu):**
  - **Klasifikasi: MCAR (*Missing Completely at Random*).**
  - *Alasan Ilmiah:* Berhentinya pencatatan disebabkan oleh jadwal pemeliharaan rutin server IT kebun yang ditetapkan berdasarkan kalender waktu, sama sekali tidak ada keterkaitan dengan besaran curah hujan harian maupun kondisi meteorologi lapangan ($P(M \mid Y) = P(M)$).

**2. Bahaya Listwise Deletion pada Pola A:**
Jika analis menghapus baris data yang hilang pada Pola A, maka seluruh data pada hari-hari terjadinya badai petir dan angin kencang ekstrem akan terhapus dari dataset. Akibatnya, dataset latihan model peramalan banjir hanya akan memuat data hari-hari dengan cuaca tenang/sedang. Model akan mengalami **bias optimistik fatal**, di mana risiko curah hujan badai penyebab banjir tidak pernah dipelajari oleh algoritma AI.

**3. Rekomendasi Solusi Imputasi:**
- **Pola A:** Jangan dihapus. Gunakan imputasi multivariat berbasis tetangga spasial terdekat (`KNNImputer`) dengan memanfaatkan stasiun cuaca afdeling tetangga yang tidak mengalami mati daya, atau gunakan model regresi deret waktu yang mengorelasikan data kelembaban udara dengan curah hujan. Sertakan kolom *missing indicator* (`Missing_Indicator_Hujan = 1`).
- **Pola B:** Karena bersifat MCAR, imputasi interpolasi linier deret waktu atau median bergerak (*rolling median*) aman digunakan tanpa menimbulkan bias distribusi.

---

### 4.2 Pembahasan Perhitungan Komparasi Deteksi Pencilan (Bobot: 40%)
Himpunan data kelembaban tanah:
$$X = \{ 28.0, 31.0, 29.5, 30.5, 32.0, 29.0, 92.0, 30.0 \}$$
Ukuran sampel $n = 8$.

**1. Perhitungan Rerata ($\bar{x}$) dan Deviasi Standar Sampel ($s$):**
$$\sum_{i=1}^8 x_i = 28.0 + 31.0 + 29.5 + 30.5 + 32.0 + 29.0 + 92.0 + 30.0 = 302.0$$
$$\mathbf{\bar{x} = \frac{302.0}{8} = 37.75\%}$$

Hitung jumlah kuadrat deviasi $\sum (x_i - \bar{x})^2$:
- $(28.0 - 37.75)^2 = (-9.75)^2 = 95.0625$
- $(31.0 - 37.75)^2 = (-6.75)^2 = 45.5625$
- $(29.5 - 37.75)^2 = (-8.25)^2 = 68.0625$
- $(30.5 - 37.75)^2 = (-7.25)^2 = 52.5625$
- $(32.0 - 37.75)^2 = (-5.75)^2 = 33.0625$
- $(29.0 - 37.75)^2 = (-8.75)^2 = 76.5625$
- $(92.0 - 37.75)^2 = (54.25)^2 = 2943.0625$
- $(30.0 - 37.75)^2 = (-7.75)^2 = 60.0625$
$$\sum (x_i - \bar{x})^2 = 3374.00$$
Varians sampel $s^2 = \frac{3374.00}{8 - 1} = \frac{3374.00}{7} \approx 482.00$
Deviasi standar sampel:
$$\mathbf{s = \sqrt{482.00} \approx 21.95\%}$$

**2. Perhitungan $Z$-Score Titik $92.0\%$ dan Masking Effect:**
$$z_{92} = \frac{92.0 - 37.75}{21.95} = \frac{54.25}{21.95} \approx \mathbf{2.47}$$
- **Evaluasi Kriteria $|z| > 3.0$:** Karena $z_{92} = 2.47 < 3.0$, titik data $92.0\%$ **GAGAL terdeteksi sebagai pencilan** menurut aturan standar $Z$-score!
- **Penjelasan Masking Effect:** Nilai ekstrem $92.0\%$ menggelembungkan deviasi standar $s$ secara masif (dari yang seharusnya $\approx 1.3\%$ menjadi $21.95\%$). Pembagi yang luar biasa besar ini "menyembunyikan" status keekstreman data tersebut.

**3. Perhitungan Kuartil dan Rentang Interkuartil (IQR):**
Urutkan data secara menaik:
$$X_{\text{sorted}} = \{ 28.0, 29.0, 29.5, 30.0, 30.5, 31.0, 32.0, 92.0 \}$$
- Separuh bawah (*Lower half*): $\{28.0, 29.0, 29.5, 30.0\}$
  $$\mathbf{Q_1 = \frac{29.0 + 29.5}{2} = 29.25\%}$$
- Separuh atas (*Upper half*): $\{30.5, 31.0, 32.0, 92.0\}$
  $$\mathbf{Q_3 = \frac{31.0 + 32.0}{2} = 31.50\%}$$
- Median ($Q_2$):
  $$Q_2 = \frac{30.0 + 30.5}{2} = 30.25\%$$
- Rentang Interkuartil:
  $$\mathbf{\text{IQR} = Q_3 - Q_1 = 31.50 - 29.25 = 2.25\%}$$

**4. Batas Atas Tukey dan Nilai Winsorizing:**
$$F_{\text{upper}} = Q_3 + 1.5 \times \text{IQR} = 31.50 + (1.5 \times 2.25) = 31.50 + 3.375 = \mathbf{34.875\%}$$
- **Deteksi Pencilan:** Karena nilai aktual $92.0\% > 34.875\%$, maka titik data tersebut **BERHASIL terdeteksi sebagai pencilan ekstrem** oleh metode Tukey IQR!
- **Nilai Hasil Winsorizing:** Nilai $92.0\%$ dikliping ke batas atas yang valid:
  $$\mathbf{x_{\text{winsor}} = 34.88\%}$$

---

### 4.3 Pembahasan Rekayasa Arsitektur Pipeline Bebas Kebocoran Data (Bobot: 30%)

**1. Analisis Kesalahan Arsitektur & Titik Kebocoran Data:**
- Kesalahan fatal terjadi pada baris `X_scaled = scaler.fit_transform(X)`. Metode `.fit()` menghitung parameter median dan rentang interkuartil dari **seluruh sampel data `X`**.
- Ketika data kemudian dibagi menjadi `X_train` dan `X_test`, informasi statistik dari `X_test` telah bocor dan memengaruhi nilai skala pada `X_train`. Hal ini melanggar asumsi dasar evaluasi model bahwa set pengujian adalah simulasi data masa depan yang belum pernah dilihat.

**2. Kode Perbaikan Menggunakan `sklearn.pipeline.Pipeline`:**
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge

# 1. Lakukan train-test split SEBELUM operasi transformasi apa pun!
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Rangkai scaler dan model estimator ke dalam satu Pipeline atomik
pipeline_bersih = Pipeline([
    ('scaler', RobustScaler()),
    ('model', Ridge(alpha=1.0))
])

# 3. Fit pipeline HANYA pada data latih (X_train)
# Parameter scaler dihitung murni dari X_train, lalu diterapkan ke X_train
pipeline_bersih.fit(X_train, y_train)

# 4. Evaluasi pada data uji (X_test)
# Scaler secara otomatis menggunakan parameter dari X_train tanpa fitting ulang!
skor_r2 = pipeline_bersih.score(X_test, y_test)
print(f"Skor R2 Bebas Kebocoran Data: {skor_r2:.4f}")
```

---

## 5. Rubrik Penilaian Berbasis Capaian (OBE Assessment Rubric)

| Dimensi Penilaian | Sangat Kurang (< 50) | Cukup (50 - 69) | Baik (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Mekanisme Data Hilang & Imputasi (Kognitif)** | Tidak memahami perbedaan MCAR, MAR, dan MNAR; selalu mengandalkan `dropna` atau imputasi rerata. | Mampu mengidentifikasi mekanisme data hilang namun keliru memilih strategi imputasi yang sesuai. | Menjelaskan implikasi bias MCAR vs MAR secara logis dan menerapkan imputasi median/KNN dengan benar. | Menguasai analisis probabilistik Rubin, menerapkan penandaan indikator hilang (*missing indicators*), dan memahami limitasi matematis MICE. |
| **Keterampilan Deteksi Pencilan & Mitigasi (Psikomotorik)** | Gagal mendeteksi pencilan atau menghapus seluruh baris ekstrim tanpa justifikasi. | Menggunakan $Z$-score standar namun tidak menyadari adanya efek penyembunyian pencilan (*masking effect*). | Mampu menghitung batas Tukey IQR secara presisi dan menerapkan teknik *Winsorizing* dengan benar. | Membuktikan secara matematis kegagalan $Z$-score pada data miring, menerapkan *Modified Z-Score* MAD, dan membedakan anomali fisik vs biologis. |
| **Arsitektur Pipeline Bebas Kebocoran Data (Afektif & Rekayasa)** | Menulis kode yang mengalami *data leakage* parah (`fit_transform` sebelum split); tidak memahami konsep pipeline. | Memisahkan data sebelum fitting namun menulis kode transformasi ganda yang rentan inkonsistensi. | Mengemas alur pra-pemrosesan ke dalam `ColumnTransformer` dan `Pipeline` Scikit-Learn dengan rapi. | Merancang arsitektur pipeline produksi tingkat enterprise yang modular, kebal kebocoran data, menangani multi-tipe data, dan siap dideploy. |
