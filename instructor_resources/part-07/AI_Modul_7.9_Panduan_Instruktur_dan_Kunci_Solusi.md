# AI Modul 7.9: Panduan Instruktur & Kunci Solusi
## Principal Component Analysis (PCA)

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-09-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Aljabar Linier Matriks Kovarians & Nilai Eigen; 70 Menit Praktikum Python Scree Plot & 2D Biplot; 30 Menit Evaluasi Kasus Citra Drone)
* **Karakteristik Modul**: Reduksi Dimensi Linier Tanpa Pengawas (*Unsupervised Dimensionality Reduction*), Dekomposisi SVD, Penginderaan Jauh Perkebunan (*Remote Sensing*)

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Modul 7.9 memadukan konsep matematika murni aljabar linier dengan kebutuhan praktis kompresi big data perkebunan:
1. **Analogi Bayangan Objek 3D pada Dinding 2D**:
   * Ajukan pertanyaan sederhana: *"Jika Anda memegang selembar daun kelapa sawit di depan lampu sorot, dari sudut manakah bayangan daun di dinding terlihat paling jelas dan paling luas bentuk aslinya?"*
   * Sudut terbaik adalah sudut yang memaksimalkan luas permukaan bayangan. Itulah persis apa yang dilakukan PCA: mencari sudut pandang baru (vektor eigen) yang memaksimalkan penyebaran varians data terproyeksi!
2. **Konteks Spesifik INSTIPER**:
   * Tunjukkan bahwa citra drone multispektral kebun sawit menghasilkan jutaan piksel dengan 8 hingga 25 saluran spektral. Mengolah seluruh saluran mentah akan membuat komputer kebun mengalami *out of memory*. PCA meringkasnya menjadi 2 atau 3 saluran komposit yang dapat langsung divisualisasikan dalam warna RGB komposit untuk mendeteksi kanopi pohon yang stres.
   * Tekankan makna Biplot: panjang dan arah panah loading menunjukkan variabel spektral mana yang saling bersinergi (misal NIR dan NDVI searah menunjukkan biomassa lebat, berlawanan dengan Red yang menunjukkan daun kering).

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "PCA memilih fitur-fitur yang bagus dan menghapus fitur-fitur yang jelek."**
  * *Koreksi Instruktur*: Jelaskan perbedaan tegas antara *Feature Selection* dan *Feature Extraction*. PCA tidak pernah membuang fitur mentah secara langsung; PCA meramu seluruh fitur asli menjadi variabel baru melalui kombinasi linier terbobot.
* **Miskonsepsi 2: "Komponen Utama pertama (PC1) selalu menjadi variabel terbaik untuk membedakan kelas penyakit tanaman."**
  * *Koreksi Instruktur*: Ingatkan bahwa PCA adalah algoritma *Unsupervised*. PC1 mencari variabilitas total terbesar data (yang mungkin disebabkan oleh intensitas cahaya matahari saat drone terbang). Terkadang variasi penyakit tanaman yang halus justru terkandung pada PC2 atau PC3.
* **Miskonsepsi 3: "Data tidak perlu distandardisasi jika semuanya dalam satuan persentase."**
  * *Koreksi Instruktur*: Sekalipun satuannya sama, jika satu variabel memiliki variabilitas alami yang jauh lebih lebar (misal $10 - 80\%$) dibanding variabel lain yang stabil ($1 - 3\%$), variabel yang lebar akan mendominasi PC1 secara sepihak. Standardisasi dengan `StandardScaler` tetap menjadi prasyarat mutlak.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual Matriks Kovarians 2D & Mean Centering (C3)
Data mentah:
$$\mathbf{X}_{\text{mentah}} = \begin{pmatrix} 20 & 2 \\ 30 & 4 \\ 40 & 6 \\ 50 & 8 \end{pmatrix}, \quad N = 4$$

#### Langkah 1: Menghitung Rata-rata Kolom ($\bar{x}_1$ dan $\bar{x}_2$)
$$\bar{x}_1 = \frac{20 + 30 + 40 + 50}{4} = \frac{140}{4} = \mathbf{35.0}$$
$$\bar{x}_2 = \frac{2 + 4 + 6 + 8}{4} = \frac{20}{4} = \mathbf{5.0}$$

#### Langkah 2: Membentuk Matriks Terpusat ($\mathbf{X} = \mathbf{X}_{\text{mentah}} - \bar{\mathbf{X}}$)
$$\mathbf{X} = \begin{pmatrix} 20 - 35 & 2 - 5 \\ 30 - 35 & 4 - 5 \\ 40 - 35 & 6 - 5 \\ 50 - 35 & 8 - 5 \end{pmatrix} = \begin{pmatrix} -15 & -3 \\ -5 & -1 \\ +5 & +1 \\ +15 & +3 \end{pmatrix}$$

#### Langkah 3: Menghitung Matriks Kovarians Sampel ($\mathbf{\Sigma} = \frac{1}{N-1}\mathbf{X}^T \mathbf{X}$)
Derajat kebebasan: $N - 1 = 4 - 1 = 3$.
$$\mathbf{X}^T \mathbf{X} = \begin{pmatrix} -15 & -5 & 5 & 15 \\ -3 & -1 & 1 & 3 \end{pmatrix} \begin{pmatrix} -15 & -3 \\ -5 & -1 \\ 5 & 1 \\ 15 & 3 \end{pmatrix}$$

Elemen matriks:
* $\text{Var}(x_1) = (-15)^2 + (-5)^2 + 5^2 + 15^2 = 225 + 25 + 25 + 225 = 500$
* $\text{Cov}(x_1, x_2) = (-15)(-3) + (-5)(-1) + (5)(1) + (15)(3) = 45 + 5 + 5 + 45 = 100$
* $\text{Var}(x_2) = (-3)^2 + (-1)^2 + 1^2 + 3^2 = 9 + 1 + 1 + 9 = 20$

Bagi dengan $N - 1 = 3$:
$$\mathbf{\Sigma} = \frac{1}{3} \begin{pmatrix} 500 & 100 \\ 100 & 20 \end{pmatrix} = \begin{pmatrix} 166.67 & 33.33 \\ 33.33 & 6.67 \end{pmatrix}$$

---

### Soal 2: Penentuan Nilai Eigen & Vektor Eigen Analitik (C3)
Matriks kovarians:
$$\mathbf{\Sigma} = \frac{1}{3} \begin{pmatrix} 500 & 100 \\ 100 & 20 \end{pmatrix}$$

#### Langkah 1: Persamaan Karakteristik Determinan
$$\det(\mathbf{\Sigma} - \lambda \mathbf{I}) = 0$$
$$\det \begin{pmatrix} \frac{500}{3} - \lambda & \frac{100}{3} \\ \frac{100}{3} & \frac{20}{3} - \lambda \end{pmatrix} = \left(\frac{500}{3} - \lambda\right)\left(\frac{20}{3} - \lambda\right) - \left(\frac{100}{3}\right)^2 = 0$$
$$\lambda^2 - \left(\frac{500 + 20}{3}\right)\lambda + \left[\frac{10000 - 10000}{9}\right] = 0$$
$$\lambda^2 - \frac{520}{3}\lambda + 0 = 0 \implies \lambda\left(\lambda - \frac{520}{3}\right) = 0$$

#### Langkah 2: Menentukan Nilai Eigen
$$\lambda_1 = \frac{520}{3} \approx \mathbf{173.3333} \quad \text{dan} \quad \lambda_2 = \mathbf{0.0000}$$

#### Langkah 3: Menentukan Vektor Eigen Unit $\mathbf{u}_1$ untuk $\lambda_1 = 173.3333$
$$(\mathbf{\Sigma} - \lambda_1 \mathbf{I})\mathbf{u}_1 = \mathbf{0}$$
$$\begin{pmatrix} \frac{500}{3} - \frac{520}{3} & \frac{100}{3} \\ \frac{100}{3} & \frac{20}{3} - \frac{520}{3} \end{pmatrix} \begin{pmatrix} u_{11} \\ u_{12} \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$
$$-\frac{20}{3} u_{11} + \frac{100}{3} u_{12} = 0 \implies 20 u_{11} = 100 u_{12} \implies u_{11} = 5 u_{12}$$

Normalkan panjang vektor agar $\|\mathbf{u}_1\| = 1$:
$$u_{11}^2 + u_{12}^2 = (5 u_{12})^2 + u_{12}^2 = 26 u_{12}^2 = 1 \implies u_{12} = \frac{1}{\sqrt{26}} \approx 0.1961$$
$$u_{11} = \frac{5}{\sqrt{26}} \approx 0.9806$$
$$\mathbf{u}_1 = \begin{pmatrix} 0.9806 \\ 0.1961 \end{pmatrix}$$

#### Langkah 4: Menghitung Rasio Varians Terjelaskan ($\text{EVR}_1$)
$$\text{EVR}_1 = \frac{\lambda_1}{\lambda_1 + \lambda_2} = \frac{173.3333}{173.3333 + 0.0} = \mathbf{1.000 \text{ (atau } 100.0\%)}$$
*Interpretasi Fisis*: Karena kedua variabel asli memiliki hubungan linier sempurna ($x_1 = 5x_2 + 10$), Komponen Utama 1 berhasil merangkum 100% variasi data tanpa ada sedikit pun informasi yang hilang.

---

### Soal 3: Analisis Scree Plot, Retensi Varians, dan Rekonstruksi Data (C4)
Urutan nilai eigen:
$$\lambda = [5.20, 2.10, 1.10, 0.65, 0.40, 0.25, 0.15, 0.08, 0.05, 0.02]$$
Total varians = $\sum \lambda = 10.00$ (karena $p = 10$ pada data terstandardisasi).

#### 1. Penerapan Kriteria Kaiser-Guttman
Kriteria Kaiser-Guttman menetapkan bahwa hanya komponen dengan nilai eigen $\lambda > 1.0$ yang dipertahankan:
* $\lambda_1 = 5.20 > 1.0$ (Lolos)
* $\lambda_2 = 2.10 > 1.0$ (Lolos)
* $\lambda_3 = 1.10 > 1.0$ (Lolos)
* $\lambda_4 = 0.65 < 1.0$ (Gugur)
*Jumlah Komponen yang Dipertahankan*: **3 Komponen Utama (PC1, PC2, PC3)**.

#### 2. Perhitungan Persentase Varians Kumulatif
$$\text{EVR}_{\text{kumulatif}} = \frac{5.20 + 2.10 + 1.10}{10.00} \times 100\% = \frac{8.40}{10.00} \times 100\% = \mathbf{84.0\%}$$
Nilai $84.0\%$ memenuhi batas standar retensi informasi industri perkebunan ($> 80\%$). Mereduksi data dari 10 fitur menjadi 3 fitur berhasil menghemat $70\%$ ruang penyimpanan sekaligus mempertahankan mayoritas mutlak variabilitas tanah.

#### 3. Bahaya Penggunaan Hanya 1 Komponen Utama ($PC_1$)
Jika hanya $PC_1$ yang digunakan:
* Varians yang terwakili: $5.20 / 10.00 = 52.0\%$.
* Informasi yang hilang (*reconstruction loss*): $100\% - 52\% = \mathbf{48.0\%}$.
* *Bahaya Agronomi*: Kehilangan hampir separuh informasi ($48\%$) akan membutakan sistem terhadap variasi unsur hara sekunder penting (seperti dinamika fosfat atau kejenuhan aluminium yang biasanya terekam pada PC2 dan PC3). Peta kesuburan tanah yang dihasilkan akan terlalu simplistis dan berisiko memicu rekomendasi pemupukan yang keliru di blok-blok kebun bermasalah.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Efek Pelatihan PCA Tanpa StandardScaler
Ketika `StandardScaler` dihilangkan pada data spektral:
* Variabel `B5_NIR` yang memiliki nilai reflektansi tertinggi menyerap hingga $85\%$ bobot pada PC1.
* Variabel indeks vegetasi (`NDRE`, `GNDVI`) yang berskala desimal sempit terpinggirkan dengan loading mendekati nol, merusak keseimbangan analisis biologis kanopi.

### 4.2 Evaluasi Rekonstruksi Data
Nilai *Mean Squared Reconstruction Error* yang sangat kecil ($MSE \approx 0.00051$) membuktikan bahwa data asli 8 dimensi dapat dipulihkan kembali dari ruang proyeksi 2D dengan tingkat akurasi mencapai $93.98\%$.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Teori Nilai Eigen, Kovarians, & Dekomposisi SVD | 25% | Mampu menguraikan formulasi maksimasi varians proyeksi, menurunkan persamaan nilai eigen, dan menerangkan hubungan SVD dengan PCA. |
| **C3 (Penerapan)** | Standardisasi Pipeline, Scree Plot & 2D Biplot | 35% | Mampu mengimplementasikan `StandardScaler` dan `PCA`, menghitung EVR kumulatif, serta memvisualisasikan grafik Biplot dengan panah loading. |
| **C4 (Analisis)** | Kriteria Retensi Kaiser & Transisi ke Boosting | 40% | Mampu menganalisis batas retensi varians aman, mengevaluasi galat rekonstruksi data, serta mengartikulasikan transisi ke Gradient Boosting. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.10 (Gradient Boosting)

Di penutup praktikum, instruktur disarankan memimpin perenungan strategis menuju modul pamungkas:
1. **Refleksi Keterbatasan Model Linier**: PCA bekerja luar biasa dalam merangkum varians secara linier tanpa label ($y = \emptyset$). Namun, bagaimana jika tugas korporasi perkebunan adalah memprediksi hasil tonase panen TBS ($y$) secara non-linier dengan tingkat presisi tertinggi?
2. **Keterbatasan Random Forest**: Ingatkan mahasiswa pada Modul 7.5: Random Forest melatih ratusan pohon secara acak tanpa saling berkomunikasi.
3. **Mengantarkan Mahakarya Terakhir Part 7**: Sampaikan bahwa pada pertemuan pamungkas Part 7 (**AI Modul 7.10: Gradient Boosting / XGBoost**), mahasiswa akan mempelajari puncak algoritma pembelajaran mesin terarah: membangun ansambel pohon secara berurutan (*sequential*), di mana setiap pohon baru bertugas mengoreksi residu galat pohon sebelumnya, menghasilkan performa prediktif kelas dunia.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Pearson, K. (1901). On lines and planes of closest fit to systems of points in space. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science*, 2(11), 559-572.
2. Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*, 24(6), 417-441.
3. Jolliffe, I. T. (2002). *Principal Component Analysis* (2nd ed.). Springer.
4. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
5. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
6. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
7. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
