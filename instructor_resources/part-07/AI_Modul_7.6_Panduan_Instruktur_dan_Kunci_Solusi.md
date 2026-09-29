# AI Modul 7.6: Panduan Instruktur & Kunci Solusi
## Naive Bayes

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-06-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Teorema Bayes, Gaussian & Laplace Smoothing; 70 Menit Praktikum Python GaussianNB & Text Mining; 30 Menit Evaluasi Kasus Ganoderma)
* **Karakteristik Modul**: Pembelajaran Probabilistik Terawasi (*Probabilistic Supervised Learning*), Komputasi Edge Ringan (*Lightweight Edge AI*), Pemrosesan Teks Perkebunan

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Naive Bayes adalah transisi penting dari model berbasis pohon menuju model berbasis distribusi probabilitas formal:
1. **Dari Kompleksitas Ansambel ke Inferensi Kilat**: Setelah mahasiswa mempelajari model yang rakus komputasi dan memori seperti Random Forest pada AI Modul 7.5, perkenalkan Naive Bayes sebagai model tandingan yang sangat ramping, cepat, dan elegan.
2. **Konteks Spesifik INSTIPER**:
   * Hubungkan konsep *prior probability* dengan data epidemiologi sensus tanaman kelapa sawit: prevalensi penyakit Ganoderma di kebun replanting biasanya berkisar antara 5% hingga 10%. Model yang mengabaikan prior akan menghasilkan puluhan alarm palsu yang merugikan.
   * Tunjukkan bahwa aplikasi AI di pedalaman perkebunan sawit sering kali tidak memiliki sinyal seluler (*blank spot*). Model berukuran kecil seperti Naive Bayes dapat ditanam langsung di memori lokal gawai mandor dan mengeksekusi diagnosis dalam hitungan milidetik.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Naive Bayes mengasumsikan data latih saling bebas."**
  * *Koreksi Instruktur*: Luruskan bahwa asumsi independensi **bukan pada baris sampel data latih**, melainkan **pada fitur-fitur prediktor bersyarat terhadap kelas** ($P(x_1, x_2 \mid C_k) = P(x_1 \mid C_k) P(x_2 \mid C_k)$).
* **Miskonsepsi 2: "Karena asumsi independensi fitur hampir selalu salah di perkebunan, Naive Bayes pasti tidak akurat."**
  * *Koreksi Instruktur*: Jelaskan *Paradoks Naive Bayes*. Untuk menghasilkan klasifikasi yang benar, model tidak memerlukan estimasi probabilitas yang sempurna; model hanya perlu memastikan bahwa probabilitas kelas yang benar lebih tinggi daripada kelas lainnya ($\arg\max$).
* **Miskonsepsi 3: "Laplace smoothing mengubah hasil prediksi menjadi acak."**
  * *Koreksi Instruktur*: Tunjukkan bahwa Laplace smoothing hanya menambahkan konstanta kecil $\alpha$ agar probabilitas tidak bernilai nol mutlak. Urutan peringkat probabilitas antar-fitur tetap terjaga stabil.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual Teorema Bayes Fundamental (C3)
Parameter diagnostik kebun seluas 5.000 ha:
* Prevalensi historis Ganoderma: $P(\text{Sakit}) = 0.05 \implies P(\text{Sehat}) = 0.95$.
* Sensitivitas alat uji: $P(\text{Positif} \mid \text{Sakit}) = 0.90$.
* Spesifisitas alat uji: $P(\text{Negatif} \mid \text{Sehat}) = 0.85 \implies P(\text{Positif} \mid \text{Sehat}) = 1 - 0.85 = 0.15$ (False Positive Rate).

#### Langkah 1: Menghitung Probabilitas Total Pembacaan Sensor Positif ($P(\text{Positif})$)
Berdasarkan Hukum Probabilitas Total (*Law of Total Probability*):
$$P(\text{Positif}) = P(\text{Positif} \mid \text{Sakit}) P(\text{Sakit}) + P(\text{Positif} \mid \text{Sehat}) P(\text{Sehat})$$
$$P(\text{Positif}) = (0.90 \times 0.05) + (0.15 \times 0.95)$$
$$P(\text{Positif}) = 0.0450 + 0.1425 = \mathbf{0.1875 \text{ (atau } 18.75\%)}$$

#### Langkah 2: Menghitung Probabilitas Sebenarnya Pohon Sakit saat Sensor Positif ($P(\text{Sakit} \mid \text{Positif})$)
Terapkan Teorema Bayes:
$$P(\text{Sakit} \mid \text{Positif}) = \frac{P(\text{Positif} \mid \text{Sakit}) P(\text{Sakit})}{P(\text{Positif})}$$
$$P(\text{Sakit} \mid \text{Positif}) = \frac{0.0450}{0.1875} = \mathbf{0.2400 \text{ (atau } 24.0\%)}$$

#### Langkah 3: Penjelasan Fenomena Base Rate Fallacy & Implikasi Agronomi
Meskipun alat sensor memiliki sensitivitas $90\%$, probabilitas aktual bahwa pohon berstatus positif benar-benar terinfeksi Ganoderma **hanya 24.0%** (artinya 76% hasil positif adalah alarm palsu!).
Hal ini disebabkan oleh prevalensi penyakit yang sangat rendah ($5\%$). Jumlah pohon sehat yang amat masif ($95\%$) menghasilkan kontribusi alarm palsu mutlak ($14.25\%$) yang jauh lebih besar daripada kasus positif sejati ($4.5\%$).
*Implikasi Praktis*: Manajemen kebun **tidak boleh langsung membongkar pohon** hanya berdasarkan hasil positif alat uji cepat ini. Pohon tersebut harus ditandai untuk uji laboratorium lanjutan (*second opinion test*) atau pemantauan intensif di piringan pohon.

---

### Soal 2: Komputasi Manual Gaussian Naive Bayes (C3)
Data bibit baru: Tinggi $x_1 = 40.0\text{ cm}$.
* **Kelas Unggul ($C_1$)**: $P(C_1) = 0.60, \mu_1 = 45.0\text{ cm}, \sigma_1 = 3.0\text{ cm} \implies \sigma_1^2 = 9.0$.
* **Kelas Afkir ($C_2$)**: $P(C_2) = 0.40, \mu_2 = 32.0\text{ cm}, \sigma_2 = 4.0\text{ cm} \implies \sigma_2^2 = 16.0$.

#### Langkah 1: Menghitung Densitas Probabilitas Gauss
* **Untuk Kelas Unggul ($C_1$)**:
  $$P(x_1 = 40 \mid C_1) = \frac{1}{\sqrt{2\pi \times 9}} \exp\left( -\frac{(40 - 45)^2}{2 \times 9} \right) = \frac{1}{3\sqrt{2\pi}} \exp\left( -\frac{25}{18} \right)$$
  Karena $\frac{1}{3\sqrt{2\pi}} \approx 0.13298$ dan $\exp(-1.38889) \approx 0.24935$:
  $$P(x_1 = 40 \mid C_1) = 0.13298 \times 0.24935 = \mathbf{0.03316}$$
* **Untuk Kelas Afkir ($C_2$)**:
  $$P(x_1 = 40 \mid C_2) = \frac{1}{\sqrt{2\pi \times 16}} \exp\left( -\frac{(40 - 32)^2}{2 \times 16} \right) = \frac{1}{4\sqrt{2\pi}} \exp\left( -\frac{64}{32} \right)$$
  Karena $\frac{1}{4\sqrt{2\pi}} \approx 0.09974$ dan $\exp(-2.0) \approx 0.13534$:
  $$P(x_1 = 40 \mid C_2) = 0.09974 \times 0.13534 = \mathbf{0.01350}$$

#### Langkah 2: Menghitung Nilai Posterior Numerator
* $\text{Num}(C_1) = P(x_1 \mid C_1) \cdot P(C_1) = 0.03316 \times 0.60 = \mathbf{0.01990}$
* $\text{Num}(C_2) = P(x_1 \mid C_2) \cdot P(C_2) = 0.01350 \times 0.40 = \mathbf{0.00540}$

#### Langkah 3: Klasifikasi MAP
Karena $\text{Num}(C_1) > \text{Num}(C_2)$, model mengklasifikasikan bibit sebagai **Bibit Unggul ($C_1$)**.
Probabilitas posterior ternormalisasi:
$$P(C_1 \mid x_1) = \frac{0.01990}{0.01990 + 0.00540} = \frac{0.01990}{0.02530} \approx \mathbf{78.66\%}$$

---

### Soal 3: Analisis Matematis Zero-Frequency Trap & Laplace Smoothing (C4)
Parameter data teks:
* $N_1 = 500$ kata di $C_1$ (Darurat Hama), $N_2 = 800$ kata di $C_2$ (Rutin).
* Ukuran kosakata unik: $K = 200$.
* Kemunculan "ulat": $N_{1,\text{ulat}} = 30, N_{2,\text{ulat}} = 2$.
* Kemunculan "kutu_kebul": $N_{1,\text{kutu}} = 0, N_{2,\text{kutu}} = 4$.

#### Langkah 1: Analisis Likelihood Tanpa Smoothing
Tanpa smoothing, estimasi Maximum Likelihood menghasilkan:
$$P_{\text{MLE}}(\text{kutu\_kebul} \mid C_1) = \frac{N_{1,\text{kutu}}}{N_1} = \frac{0}{500} = \mathbf{0.0}$$
*Bahaya Keruntuhan Produk*: Jika sebuah laporan baru memuat kata *"kutu_kebul"*, maka suku $P(\text{kutu\_kebul} \mid C_1) = 0$ akan mengalikan seluruh suku lainnya dalam $\prod P(x_j \mid C_1)$, membuat skor kelas $C_1$ menjadi $0.0$ mutlak, menghapus total kemungkinan diagnosis darurat hama meskipun kata *"serangan ulat parah"* muncul berulang kali di teks yang sama.

#### Langkah 2: Perhitungan Probabilitas Terhaluskan (Laplace Smoothing $\alpha = 1.0$)
Penyebut terhaluskan:
* Untuk $C_1$: $N_1 + \alpha K = 500 + (1.0 \times 200) = \mathbf{700}$
* Untuk $C_2$: $N_2 + \alpha K = 800 + (1.0 \times 200) = \mathbf{1000}$

Kalkulasi probabilitas:
* **Kata "ulat"**:
  $$P(\text{ulat} \mid C_1) = \frac{30 + 1}{700} = \frac{31}{700} \approx \mathbf{0.04429 \text{ (4.43\%)}}$$
  $$P(\text{ulat} \mid C_2) = \frac{2 + 1}{1000} = \frac{3}{1000} = \mathbf{0.00300 \text{ (0.30\%)}}$$
* **Kata "kutu_kebul"**:
  $$P(\text{kutu\_kebul} \mid C_1) = \frac{0 + 1}{700} = \frac{1}{700} \approx \mathbf{0.00143 \text{ (0.14\%)}}$$
  $$P(\text{kutu\_kebul} \mid C_2) = \frac{4 + 1}{1000} = \frac{5}{1000} = \mathbf{0.00500 \text{ (0.50\%)}}$$

#### Langkah 3: Analisis Pengaruh Nilai $\alpha$
Nilai $\alpha$ berfungsi sebagai kekuatan bobot seragam semu. Jika $\alpha$ disetel terlalu besar (misal $\alpha = 100$), probabilitas semua kata akan tertarik ke arah $1/K$ (distribusi seragam), merusak daya beda model. Pada dataset laporan perkebunan berukuran masif ($N > 100.000$ kata), disarankan menggunakan nilai $\alpha$ yang lebih kecil seperti $\alpha = 0.1$ atau $\alpha = 0.01$ (*Lidstone smoothing*) agar estimasi frekuensi kata dominan tidak tertekan berlebihan.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Efek Perubahan Parameter `class_prior`
```python
gnb_prior = GaussianNB(priors=[0.90, 0.08, 0.02])
gnb_prior.fit(X_train, y_train)
y_pred_prior = gnb_prior.predict(X_test)
print(classification_report(y_test, y_pred_prior, target_names=nama_kelas))
```
*Temuan*: Menurunkan prior Ganoderma ke 2% menurunkan jumlah alarm palsu (*False Positive*), namun menaikkan risiko lolosnya kasus Ganoderma stadium awal (*False Negative*).

### 4.2 Uji Kalimat Asing dengan Kosakata Baru
Kalimat baru: *"traktor derek mogok di tanjakan"*
*Hasil*: Model `MultinomialNB(alpha=1.0)` tidak mengalami crash atau galat nol. Seluruh kata yang tidak terdaftar diabaikan oleh `CountVectorizer`, dan prediksi diambil semata-mata berdasarkan probabilitas prior kelas.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Teori Bayes, Asumsi Naive, & Distribusi Peluang | 25% | Mampu membedah 4 komponen Teorema Bayes, menjelaskan fungsi densitas Gauss, dan menerangkan mekanisme Laplace Smoothing. |
| **C3 (Penerapan)** | Implementasi Pemodelan & Estimasi Probabilitas | 35% | Mampu mengimplementasikan `GaussianNB` dan `MultinomialNB`, mengekstrak parameter $\mu$ dan $\sigma^2$, serta menghitung probabilitas posterior tanpa galat. |
| **C4 (Analisis)** | Analisis Multikolinieritas & Base Rate Fallacy | 40% | Mampu menganalisis fenomena degradasi multikolinieritas, membedah kekeliruan base rate fallacy pada penyakit langka, dan merancang mitigasi bias di kebun. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.7 (Support Vector Machine)

Di akhir sesi kelas modul 7.6, instruktur disarankan memfasilitasi evaluasi komparatif:
1. **Mendiskusikan Batas Linearitas Probabilitas**: Naive Bayes memisahkan data menggunakan hiper-permukaan berbasis rasio log-likelihood. Namun, bagaimana jika data memiliki pola sebaran non-linier rumit yang saling melingkar (*non-linear concentric distribution*)?
2. **Ketiadaan Konsep Margin Keamanan**: Tunjukkan bahwa Naive Bayes hanya mencari bidang potong probabilitas, tanpa memedulikan seberapa jauh bidang tersebut dari titik-titik data terluar.
3. **Mengantarkan Pendekatan Geometris SVM**: Sampaikan bahwa pada pertemuan berikutnya (**AI Modul 7.7: Support Vector Machine**), mahasiswa akan mempelajari model geometris terkuat yang memaksimalkan batas toleransi keamanan (*maximal margin hyperplane*) dan trik pemetaan dimensi tinggi (*Kernel Trick*) untuk memecahkan klasifikasi perkebunan yang paling menantang.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Bayes, T. (1763). An essay towards solving a problem in the doctrine of chances. *Philosophical Transactions of the Royal Society of London*, 53, 370-418.
2. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
3. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
4. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
5. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
6. Rish, I. (2001). An empirical study of the naive Bayes classifier. *IJCAI 2001 Workshop on Empirical Methods in Artificial Intelligence*, 3(22), 41-46.
