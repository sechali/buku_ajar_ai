# AI Modul 7.8: Panduan Instruktur & Kunci Solusi
## K-Means Clustering

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-08-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Inersia WCSS, Algoritma Lloyd, & K-Means++; 70 Menit Praktikum Python Standardisasi & Evaluasi Silhouette; 30 Menit Evaluasi Studi Kasus Pupuk Presisi)
* **Karakteristik Modul**: Pembelajaran Tanpa Pengawas (*Unsupervised Learning*), Partisi Geometris Centroid, Zonasi Pertanian Presisi (*Variable Rate Fertilization*)

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Modul 7.8 adalah pintu gerbang menuju paradigma baru dalam kurikulum:
1. **Transisi Monumental ke Unsupervised Learning**: Tegaskan kepada mahasiswa bahwa pada Modul 7.1 hingga 7.7, komputer selalu memiliki "kunci jawaban" berbentuk label target $y$. Pada Modul 7.8, label tersebut ditiadakan total ($y = \emptyset$). Komputer dituntut menemukan sendiri keteraturan dan kelompok alami dari data mentah.
2. **Konteks Spesifik INSTIPER**:
   * Analogi Tiga Truk Pupuk: Bayangkan sebuah afdeling kebun kelapa sawit yang memiliki variabilitas tanah tinggi. Manajer tidak mungkin menerapkan ratusan dosis pupuk berbeda, melainkan membaginya ke dalam 3 zona logistik pupuk: Dosis Ekstra Kalium (gambut masam), Dosis Reguler (mineral), dan Dosis Hemat (aluvial subur).
   * Nilai fisis centroid: Tekankan bahwa centroid hasil K-Means bukan sekadar angka abstrak, melainkan "resep agronomi rata-rata" yang dapat langsung diterjemahkan menjadi rekomendasi kilogram pupuk per pohon.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "K-Means dapat mengetahui secara otomatis berapa jumlah kelompok alami di kebun."**
  * *Koreksi Instruktur*: Luruskan bahwa $K$ adalah hyperparameter yang wajib ditentukan manual oleh manusia. Tunjukkan bahwa metode ilmiah seperti *Elbow Method* dan *Silhouette Analysis* adalah alat bantu objektif untuk memandu pemilihan nilai $K$.
* **Miskonsepsi 2: "Tujuan utama klasterisasi adalah membuat nilai inersia WCSS sekecil mungkin."**
  * *Koreksi Instruktur*: Tunjukkan bahwa jika $K = N$, maka nilai WCSS $= 0$. Namun model tersebut tidak berguna sama sekali karena setiap pohon menjadi kelompoknya sendiri. Klasterisasi yang baik adalah kompromi antara kerapatan kelompok dan keterpahaman manajerial.
* **Miskonsepsi 3: "Standardisasi data dengan StandardScaler tidak diperlukan pada Unsupervised Learning."**
  * *Koreksi Instruktur*: Tunjukkan bahaya nyata jarak Euclidean: variabel dengan angka puluhan atau ratusan (seperti Fosfor dalam ppm) akan menenggelamkan variabel pecahan desimal (seperti Kalium dalam cmol/kg) hingga 99%, membuat zonasi kalium gagal total.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual 1 Siklus Iterasi Algoritma Lloyd 1D (C3)
Data bahan organik tanah: $X = \{1.0, 2.0, 2.5, 6.0, 7.0, 8.5\}$, dengan $K = 2$.
Centroid awal iterasi $t=0$: $\mu_1^{(0)} = 1.5$ dan $\mu_2^{(0)} = 7.5$.

#### Langkah 1: Fase Penugasan Klaster (Assignment Step)
Hitung jarak mutlak $|x_i - \mu_k|$ ke kedua centroid:
* $x_1 = 1.0$: Jarak ke $\mu_1 = |1.0 - 1.5| = 0.5$; Jarak ke $\mu_2 = |1.0 - 7.5| = 6.5 \implies \mathbf{S_1}$
* $x_2 = 2.0$: Jarak ke $\mu_1 = |2.0 - 1.5| = 0.5$; Jarak ke $\mu_2 = |2.0 - 7.5| = 5.5 \implies \mathbf{S_1}$
* $x_3 = 2.5$: Jarak ke $\mu_1 = |2.5 - 1.5| = 1.0$; Jarak ke $\mu_2 = |2.5 - 7.5| = 5.0 \implies \mathbf{S_1}$
* $x_4 = 6.0$: Jarak ke $\mu_1 = |6.0 - 1.5| = 4.5$; Jarak ke $\mu_2 = |6.0 - 7.5| = 1.5 \implies \mathbf{S_2}$
* $x_5 = 7.0$: Jarak ke $\mu_1 = |7.0 - 1.5| = 5.5$; Jarak ke $\mu_2 = |7.0 - 7.5| = 0.5 \implies \mathbf{S_2}$
* $x_6 = 8.5$: Jarak ke $\mu_1 = |8.5 - 1.5| = 7.0$; Jarak ke $\mu_2 = |8.5 - 7.5| = 1.0 \implies \mathbf{S_2}$

Anggota klaster:
$$S_1^{(0)} = \{1.0, 2.0, 2.5\} \quad \text{dan} \quad S_2^{(0)} = \{6.0, 7.0, 8.5\}$$

#### Langkah 2: Fase Pembaruan Centroid (Update Step)
Hitung rata-rata aritmetika baru:
$$\mu_1^{(1)} = \frac{1.0 + 2.0 + 2.5}{3} = \frac{5.5}{3} \approx \mathbf{1.8333}$$
$$\mu_2^{(1)} = \frac{6.0 + 7.0 + 8.5}{3} = \frac{21.5}{3} \approx \mathbf{7.1667}$$

#### Langkah 3: Perhitungan Inersia WCSS pada Akhir Siklus Pertama
* **Klaster 1**:
  $$(1.0 - 1.8333)^2 + (2.0 - 1.8333)^2 + (2.5 - 1.8333)^2$$
  $$= (-0.8333)^2 + (0.1667)^2 + (0.6667)^2 = 0.6944 + 0.0278 + 0.4444 = \mathbf{1.1667}$$
* **Klaster 2**:
  $$(6.0 - 7.1667)^2 + (7.0 - 7.1667)^2 + (8.5 - 7.1667)^2$$
  $$= (-1.1667)^2 + (-0.1667)^2 + (1.3333)^2 = 1.3611 + 0.0278 + 1.7778 = \mathbf{3.1667}$$
* **Total WCSS**:
  $$J = 1.1667 + 3.1667 = \mathbf{4.3334}$$

---

### Soal 2: Komputasi Manual Koefisien Silhouette (C3)
Data klaster 1D:
* Klaster A: $S_A = \{2.0, 4.0, 6.0\}$
* Klaster B: $S_B = \{10.0, 12.0, 14.0\}$
* Sampel target: $x_i = 6.0 \in S_A$.

#### Langkah 1: Menghitung Kerapatan Internal $a(i)$
Rata-rata jarak dari $x_i = 6.0$ ke sampel lain di dalam Klaster A:
$$a(i) = \frac{|6.0 - 2.0| + |6.0 - 4.0|}{2} = \frac{4.0 + 2.0}{2} = \frac{6.0}{2} = \mathbf{3.000}$$

#### Langkah 2: Menghitung Keterpisahan Eksternal $b(i)$
Rata-rata jarak dari $x_i = 6.0$ ke seluruh sampel di Klaster B:
$$b(i) = \frac{|6.0 - 10.0| + |6.0 - 12.0| + |6.0 - 14.0|}{3} = \frac{4.0 + 6.0 + 8.0}{3} = \frac{18.0}{3} = \mathbf{6.000}$$

#### Langkah 3: Menghitung Koefisien Silhouette $s(i)$
$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))} = \frac{6.000 - 3.000}{\max(3.000, 6.000)} = \frac{3.000}{6.000} = \mathbf{+0.5000}$$

#### Langkah 4: Interpretasi Hasil
Nilai $s(i) = +0.50$ menunjukkan bahwa sampel $x_i = 6.0$ tergolong terklaster dengan baik. Sampel berada dua kali lebih dekat ke rekan sekelompoknya ($a=3.0$) dibandingkan ke kelompok tetangga terdekatnya ($b=6.0$), tidak ada indikasi salah penempatan zona.

---

### Soal 3: Analisis Konvergensi Inersia WCSS & Algoritma K-Means++ (C4)

#### 1. Pembuktian Penurunan Monotonik WCSS
Pada setiap iterasi algoritma Lloyd:
* **Fase Penugasan**: Setiap titik $\mathbf{x}_i$ dipindahkan ke centroid yang memiliki jarak kuadrat $\|\mathbf{x}_i - \boldsymbol{\mu}_k\|^2$ terkecil. Pemindahan ini dijamin menurunkan atau minimal mempertahankan nilai $J$.
* **Fase Pembaruan**: Posisi centroid baru dihitung sebagai rata-rata aritmetika sampel anggotanya. Secara kalkulus, rata-rata aritmetika adalah titik stasioner unik yang meminimalkan turunan jumlah kuadrat $\sum (\mathbf{x}_i - \boldsymbol{\mu}_k)^2$. Oleh karena itu, pembaruan centroid selalu menurunkan atau mempertahankan nilai $J$.
Karena kedua fase selalu menurunkan $J$ dan fungsi kuadrat memiliki batas bawah nol ($J \ge 0$), maka algoritma Lloyd dijamin konvergen secara monotonik.

#### 2. Mengapa Penurunan WCSS Tidak Menjamin Optimum Global Mutlak
Fungsi WCSS adalah permukaan non-konveks (*non-convex landscape*) dengan banyak cekungan minimum lokal. Karena algoritma Lloyd bersifat *greedy*, jika inisialisasi awal buruk (misalnya dua centroid awal jatuh di klaster padat yang sama), algoritma akan terjebak pada partisi lokal yang keliru seumur hidupnya.
*Peran K-Means++*: Algoritma K-Means++ menyebarkan centroid awal secara probabilistik sebanding dengan $D(\mathbf{x})^2$. Titik yang jauh dari centroid yang sudah ada memiliki peluang terpilih jauh lebih tinggi. Secara matematis, K-Means++ membuktikan bahwa nilai ekspektasi WCSS yang dihasilkan berada dalam batas $\mathcal{O}(\log K)$ dari solusi optimal global mutlak.

#### 3. Kritik terhadap Usulan $K = 20$ untuk 100 Pohon
* **Kritik Agronomi**: Menetapkan $K = 20$ zona untuk 100 pohon menghasilkan rata-rata hanya 5 pohon per zona! Secara operasional, operator traktor atau mandor pemupuk tidak mungkin mengganti takaran pupuk setiap berpindah 5 pohon. Ini adalah kekacauan logistik yang memicu biaya operasional jauh lebih mahal daripada penghematan pupuknya.
* **Kritik Statistik**: Memilih $K$ yang terlalu besar mendekati ukuran data adalah bentuk *overfitting klaster*. Model kehilangan daya abstraksi dan merangkum derau data lokal, bukan pola variabilitas tanah yang sesungguhnya.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Efek Inisialisasi Acak vs K-Means++
Ketika diuji dengan `init='random'` sebanyak 10 kali:
* Terjadi fluktuasi nilai inersia akhir (berkisar antara 160 hingga 240) karena model beberapa kali terjebak pada minimum lokal.
* Ketika diuji dengan `init='k-means++'`, inersia konvergen secara konsisten pada nilai terendah (~155) dengan skor Silhouette stabil pada ~0.695.

### 4.2 Klasterisasi Tanpa StandardScaler
Ketika `StandardScaler` diabaikan:
* Variabel Fosfor (`P_Tersedia_ppm`) yang bernilai puluhan mendominasi 80% pembentukan klaster.
* Variabel Kalium (`K_dd_cmol_kg`) yang bernilai $0.1 - 1.2$ terabaikan total, sehingga tanah yang mengalami defisiensi kalium parah tidak dapat teridentifikasi oleh sistem zonasi.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Teori Inersia WCSS, Siklus Lloyd, & K-Means++ | 25% | Mampu menguraikan formulasi WCSS, membedah 2 fase algoritma Lloyd, dan menerangkan keunggulan inisialisasi probabilistik K-Means++. |
| **C3 (Penerapan)** | Standardisasi Pipeline, K-Means & Evaluasi | 35% | Mampu mengintegrasikan `StandardScaler`, membuat grafik Elbow & Silhouette, serta mentransformasikan centroid ke satuan agronomi asli. |
| **C4 (Analisis)** | Optimasi Partisi, Analisis Biaya & Transisi PCA | 40% | Mampu menganalisis batas optimum lokal, mengevaluasi kelayakan logistik pemupukan VRF, serta mengartikulasikan kebutuhan reduksi dimensi PCA. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.9 (Principal Component Analysis)

Di akhir sesi praktikum modul 7.8, instruktur disarankan memfasilitasi diskusi kritis mengenai keterbatasan visualisasi:
1. **Tantangan Ruang Multidimensi**: Pada praktikum 7.8, kita memiliki 5 variabel tanah, namun kita terpaksa hanya memplot 2 variabel (N vs K) pada grafik 2D. Tanyakan: *"Bagaimana dengan variabilitas 3 fitur lainnya (P, pH, Bahan Organik)? Bukankah ada informasi penting yang terpotong saat kita hanya melihat 2 sumbu?"*
2. **Kutukan Multikolinieritas**: Tunjukkan bahwa dalam survei tanah modern dengan 30 variabel hara, banyak fitur yang saling tumpang tindih.
3. **Mengantarkan Reduksi Dimensi PCA**: Buka wawasan bahwa pada pertemuan berikutnya (**AI Modul 7.9: Principal Component Analysis**), mahasiswa akan mempelajari bagaimana aljabar linier (nilai dan vektor eigen) mampu memadatkan puluhan fitur menjadi 2 Komponen Utama tanpa kehilangan pola variabilitas aslinya, menyempurnakan visualisasi klaster perkebunan presisi.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Lloyd, S. (1982). Least squares quantization in PCM. *IEEE Transactions on Information Theory*, 28(2), 129-137.
2. Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. *Proceedings of the eighteenth annual ACM-SIAM symposium on Discrete algorithms*, 1027-1035.
3. Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53-65.
4. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
5. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
6. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
7. MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. *Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability*, 1(14), 281-297.
