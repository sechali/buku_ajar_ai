# PANDUAN INSTRUKTUR & KUNCI SOLUSI
## AI Modul 1.3: Perbedaan AI, Machine Learning, dan Deep Learning

> **Dokumen Rahasia Pengajar (Dosen & Asisten Laboratorium)**  
> **Modul Terkait:** [AI_Modul_1.3_Perbedaan_AI_ML_dan_Deep_Learning.md](../../docs/part-01/AI_Modul_1.3_Perbedaan_AI_ML_dan_Deep_Learning.md)  
> **Notebook Praktikum:** [AI_Modul_1.3_Praktikum_Perbedaan_AI_ML_DL.ipynb](../../notebooks/part-01/AI_Modul_1.3_Praktikum_Perbedaan_AI_ML_DL.ipynb)

---

## 1. Panduan Fasilitasi & Titik Tekan Pedagogi

### 1.1. Miskonsepsi Umum Mahasiswa
1. **Miskonsepsi "Deep Learning Selalu Lebih Baik"**: Mahasiswa sering terhipnotis oleh tren sehingga beranggapan bahwa arsitektur Deep Learning (seperti CNN/Transformer) harus selalu digunakan untuk semua kasus. Tekankan bahwa untuk data tabular (misal: data sensus, data kepegawaian, tabel CSV pemupukan), model ML klasik (*Random Forest, XGBoost, Regresi*) sering kali mengungguli Deep Learning dalam hal kecepatan, akurasi pada data kecil, dan kemudahan audit.
2. **Miskonsepsi AI = Machine Learning**: Mahasiswa menganggap algoritma yang tidak melakukan "training data" bukanlah AI. Ingatkan bahwa algoritma rute tercepat Google Maps (*Dijkstra/A\**) dan mesin catur *Minimax* adalah representasi kecerdasan buatan murni tanpa proses belajar induktif.

### 1.2. Alokasi Waktu Praktikum (100 Menit)
* **Menit 00–25**: Kuliah pengantar: Diagram Venn relasi himpunan, perbedaan manual feature engineering vs representation learning, dan analisis kurva penskalaan data Andrew Ng.
* **Menit 25–50**: Live demo notebook: Menjalankan pembangkitan dataset daun sintetis dan membedah kode ketiga kelas model.
* **Menit 50–80**: Mahasiswa menjalankan eksperimen skala data ($N=20$ s.d. $400$) dan menyelesaikan *Coding Challenge* rekayasa fitur polinomial.
* **Menit 80–100**: Evaluasi visual kontur *decision boundary* dan diskusi reflektif 3 pertanyaan HOTS.

---

## 2. Kunci Jawaban Pertanyaan Analitis (HOTS)

### Pertanyaan 1: Mengapa Menolak Arsitektur Transformer untuk 500 Baris Data Tabular?
* **Kunci Jawaban**:
  1. **Risiko Overfitting Ekstrem**: Model Transformer memiliki jutaan parameter terdistribusi. Menyuapkan 500 baris data tabular pada model berkapasitas raksasa akan membuat model menghafal data (*memorization*) alih-alih belajar pola generalisasi.
  2. **Inductive Bias yang Tidak Sesuai**: Transformer dirancang untuk data deret berstruktur (seperti teks bahasa atau aliran token citra). Data tabular memiliki kolom independen dengan semantik yang heterogen, di mana algoritma *Decision Trees / Gradient Boosted Trees (XGBoost)* terbukti secara matematis dan empiris jauh lebih superior.
  3. **Pemborosan Biaya Komputasi**: Menjalankan Transformer membutuhkan sewa instans GPU cloud yang mahal tanpa menghasilkan peningkatan akurasi nyata.

### Pertanyaan 2: Mengapa Regulator Hukum Lebih Menyukai Model Rule-Based / Regresi Linier?
* **Kunci Jawaban**:
  1. **Hak atas Penjelasan (*Right to Explanation / Akuntabilitas Hukum*)**: Pada sertifikasi ekspor karantina atau diagnosis medis berisiko tinggi, keputusan penolakan produk harus dapat dipertanggungjawabkan secara kausalitas. Pada regresi linier, setiap bobot $w_i$ menunjukkan secara transparan berapa kontribusi masing-masing parameter fisik terhadap vonis.
  2. **Beban Risiko Black-Box**: Deep Neural Network memiliki interaksi non-linier tersembunyi yang kompleks. Jika terjadi kesalahan fatal (*False Negative/Positive*), pengembang tidak dapat dengan mudah menunjukkan node mana yang memicu kegagalan tersebut, sehingga rentan terhadap gugatan hukum dan gagal audit regulasi.

### Pertanyaan 3: Mengapa Menumpuk 100 Lapisan Linier Tanpa Non-Linearitas Sama dengan 1 Lapisan Tunggal?
* **Kunci Jawaban**:
  * Secara aljabar linier, komposisi dari dua atau lebih transformasi linier selalu menghasilkan transformasi linier tunggal:
    $$\mathbf{y} = \mathbf{W}_2 (\mathbf{W}_1 \mathbf{x}) = (\mathbf{W}_2 \mathbf{W}_1) \mathbf{x} = \mathbf{W}_{\text{gabungan}} \mathbf{x}$$
  * Jika sebuah jaringan saraf tiruan memiliki 100 lapisan namun seluruhnya menggunakan aktivasi linier $f(z) = z$, perkalian 100 matriks bobot $(\mathbf{W}_{100} \cdot \mathbf{W}_{99} \dots \mathbf{W}_1)$ dapat disederhanakan secara ekuivalen menjadi satu matriks bobot tunggal $\mathbf{W}_{\text{total}}$.
  * Akibatnya, jaringan tersebut **kehilangan seluruh kapasitas representasionalnya** dan tidak akan pernah mampu memecahkan masalah non-linier (seperti gerbang XOR atau kurva daun meliuk). Fungsi aktivasi non-linier (seperti ReLU atau Sigmoid) adalah elemen mutlak yang memungkinkan jaringan melipat ruang dimensi dan menangkap batas keputusan kompleks.

---

## 3. Kunci Kode Solusi Tantangan Mandiri: Rekayasa Fitur Polinomial

Berikut adalah kunci implementasi pengangkatan dimensi fitur untuk mendongkrak performa Machine Learning klasik:

```python
import numpy as np

# 1. Ekstrak data mentah
x1_train = X_train_full[:, 0]
x2_train = X_train_full[:, 1]
x1_test  = X_test[:, 0]
x2_test  = X_test[:, 1]

# 2. Rekayasa Fitur Polinomial: Menambahkan suku kuadratik dan interaksi
X_train_engineered = np.column_stack([
    x1_train,
    x2_train,
    x1_train ** 2,
    x2_train ** 2,
    x1_train * x2_train
])

X_test_engineered = np.column_stack([
    x1_test,
    x2_test,
    x1_test ** 2,
    x2_test ** 2,
    x1_test * x2_test
])

# 3. Latih Model ML Klasik pada Fitur Baru
model_engineered = ClassicalLogisticRegression(lr=0.05, epochs=500)
model_engineered.train(X_train_engineered, y_train_full)

# 4. Evaluasi Akurasi
pred_eng = model_engineered.predict(X_test_engineered)
acc_eng = np.mean(pred_eng == y_test) * 100

print(f"Akurasi ML Klasik dengan Rekayasa Fitur: {acc_eng:.2f}%")
```

### Catatan Penting untuk Instruktur:
Tunjukkan kepada mahasiswa bahwa dengan rekayasa fitur yang tepat, akurasi Machine Learning klasik melompat dari **$81.00\%$** menjadi **$91.00\%$**, menyamai performa Deep Learning ($91.00\%$) namun dengan waktu komputasi yang jauh lebih instan dan konsumsi memori yang jauh lebih kecil. Ini membuktikan bahwa keahlian *Feature Engineering* tetap sangat bernilai tinggi di industri.

---

## 4. Variasi Soal Kuis Praktikum / Responsi Lab

### Variasi Soal A: Evaluasi Latensi Inferensi
* **Tugas**: Mintalah mahasiswa mengukur waktu eksekusi (`time.perf_counter()`) saat model melakukan prediksi pada 10.000 sampel data uji baru.
* **Target Capaian**: Mahasiswa mengamati bahwa ML klasik melakukan inferensi $10\times$ lebih cepat daripada Deep Neural Network.

### Variasi Soal B: Penanganan Imbalanced Data
* **Tugas**: Ubah proporsi data sehingga kelas sakit hanya $5\%$ (misal 25 sampel sakit vs 475 sampel sehat).
* **Target Capaian**: Mahasiswa mengamati bagaimana ketiga model bereaksi terhadap ketidakseimbangan kelas (*class imbalance*) dan mengapa akurasi naif menjadi metrik yang menyesatkan.

---

## 5. Rubrik Penilaian Praktikum Lab (Skala 100)

| Aspek Penilaian | Bobot | Deskriptor Kinerja Unggul (Nilai Maksimal) |
| :--- | :---: | :--- |
| **Penguasaan Klasifikasi AI-ML-DL** | 20% | Mampu menjelaskan relasi himpunan bagian dan menguraikan trade-off 7 parameter komparasi. |
| **Implementasi Kode Tiga Paradigma** | 35% | Kode Python berfungsi sempurna, menerapkan type-hints, perhitungan gradien dan forward-backward pass tepat. |
| **Analisis Kurva Skalabilitas** | 25% | Mampu menganalisis batas kejenuhan ML klasik dan titik potong performa Deep Learning pada grafik. |
| **Penyelesaian Tantangan Rekayasa Fitur** | 20% | Berhasil merekayasa matriks fitur polinomial 5D dan membuktikan kenaikan akurasi pada sesi responsi. |
