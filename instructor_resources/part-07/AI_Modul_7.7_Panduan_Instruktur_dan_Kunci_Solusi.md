# AI Modul 7.7: Panduan Instruktur & Kunci Solusi
## Support Vector Machine (SVM)

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-07-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Margin Maksimal, Formulasi Dual & Kernel Trick; 70 Menit Praktikum Pipeline Scikit-Learn & Spektroskopi NIR; 30 Menit Evaluasi Kasus Terminal CPO)
* **Karakteristik Modul**: Pembelajaran Geometris Terawasi (*Geometric Supervised Learning*), Optimasi Kuadratik Konveks Bebas Minimum Lokal, Klasifikasi Data Berdimensi Tinggi ($p \gg N$)

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Support Vector Machine (SVM) adalah puncak kecanggihan matematis dari keluarga model linier dan kernel:
1. **Dari Model Probabilitas ke Model Geometris Presisi**: Bimbing mahasiswa membedakan filosofi Regresi Logistik dan Naive Bayes (yang mencari probabilitas) dengan SVM (yang mencari jarak terluas / *maximal margin separator*).
2. **Konteks Spesifik INSTIPER**:
   * Jelaskan mengapa SVM sangat dipuja di laboratorium kimia analitik dan spektroskopi agro-industri. Spektrometer Near-Infrared (NIR) mengukur ratusan pita panjang gelombang dari puluhan sampel minyak kelapa sawit ($p \approx 500, N \approx 40$). Model statistik biasa akan mengalami singularitas matriks, sedangkan SVM justru bekerja paling unggul di ruang berdimensi tinggi.
   * Tunjukkan bahwa posisi vektor pendukung (*support vectors*) memiliki analogi nyata sebagai "sampel batas toleransi mutu" yang disepakati antara pembeli dan penjual CPO di pelabuhan ekspor.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "SVM mencari garis yang memisahkan data dengan benar, garis pemisah mana saja boleh asalkan akurasinya 100%."**
  * *Koreksi Instruktur*: Gambarkan banyak garis pemisah alternatif yang sama-sama mencapai akurasi 100% pada data latih. Tunjukkan bahwa hanya ada **satu garis unik** yang memaksimalkan jarak margin $M = 2/\|\mathbf{w}\|$. Garis inilah yang paling tahan terhadap pergeseran derau data baru di lapangan.
* **Miskonsepsi 2: "Standardisasi fitur tidak penting pada SVM karena margin akan menyesuaikan diri."**
  * *Koreksi Instruktur*: Buktikan secara matematis bahwa perhitungan norma $\|\mathbf{w}\|$ dan jarak Euclidean pada kernel RBF $\exp(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|^2)$ sangat sensitif terhadap skala fitur. Tanpa `StandardScaler`, fitur dengan satuan besar akan mendominasi 99% fungsi objektif, merusak margin pemisah secara fatal.
* **Miskonsepsi 3: "Kernel Trick secara fisik memproyeksikan data ke memori berdimensi tinggi."**
  * *Koreksi Instruktur*: Luruskan bahwa kernel trick adalah "keajaiban jalan pintas aljabar". Kita tidak pernah menghitung atau menyimpan koordinat $\phi(\mathbf{x})$ di memori; kita hanya menghitung fungsi skalar $K(\mathbf{x}_i, \mathbf{x}_j)$ langsung di ruang aslinya.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Geometris Jarak Margin dan Persamaan Hiperbidang (C3)
Parameter model SVM linier:
* Vektor bobot: $\mathbf{w} = \begin{pmatrix} 3 \\ 4 \end{pmatrix}$
* Nilai bias: $b = -12$

#### Langkah 1: Menghitung Norma Euclidean Vektor Bobot ($\|\mathbf{w}\|$)
$$\|\mathbf{w}\| = \sqrt{w_1^2 + w_2^2} = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = \mathbf{5.0}$$

#### Langkah 2: Menghitung Lebar Total Margin Geometris ($M$)
$$M = \frac{2}{\|\mathbf{w}\|} = \frac{2}{5.0} = \mathbf{0.40 \text{ unit}}$$

#### Langkah 3: Evaluasi Sampel Uji Baru $\mathbf{x}_{\text{uji}} = \begin{pmatrix} 2 \\ 3 \end{pmatrix}$
* **Nilai Fungsi Keputusan**:
  $$f(\mathbf{x}_{\text{uji}}) = \mathbf{w}^T \mathbf{x}_{\text{uji}} + b = (3 \times 2) + (4 \times 3) - 12 = 6 + 12 - 12 = \mathbf{+6.0}$$
* **Penentuan Kelas**:
  Karena $f(\mathbf{x}_{\text{uji}}) = +6.0 > 0$, maka $\hat{y} = \text{sign}(+6.0) = \mathbf{+1 \text{ (Kelas Positif)}}$.
* **Jarak Tegak Lurus Sampel ke Hiperbidang Keputusan**:
  $$\text{Jarak} = \frac{|\mathbf{w}^T \mathbf{x}_{\text{uji}} + b|}{\|\mathbf{w}\|} = \frac{|+6.0|}{5.0} = \mathbf{1.20 \text{ unit}}$$
  Karena jarak sampel ($1.20$) lebih besar dari setengah lebar margin ($M/2 = 0.20$), titik ini berada aman di luar koridor margin pada sisi positif.

---

### Soal 2: Komputasi Manual Kernel RBF dan Penentuan Prediksi (C3)
Parameter model SVM RBF:
* $\gamma = 0.5$, $b = -0.2$.
* Vektor Pendukung 1: $\mathbf{x}_1 = \begin{pmatrix} 1 \\ 2 \end{pmatrix}, y_1 = +1, \alpha_1 = 1.2$.
* Vektor Pendukung 2: $\mathbf{x}_2 = \begin{pmatrix} 4 \\ 6 \end{pmatrix}, y_2 = -1, \alpha_2 = 1.2$.
* Sampel Uji Baru: $\mathbf{x}^* = \begin{pmatrix} 2 \\ 3 \end{pmatrix}$.

#### Langkah 1: Menghitung Jarak Kuadrat Euclidean
* Jarak ke $\mathbf{x}_1$:
  $$\|\mathbf{x}_1 - \mathbf{x}^*\|^2 = (1 - 2)^2 + (2 - 3)^2 = (-1)^2 + (-1)^2 = 1 + 1 = \mathbf{2.0}$$
* Jarak ke $\mathbf{x}_2$:
  $$\|\mathbf{x}_2 - \mathbf{x}^*\|^2 = (4 - 2)^2 + (6 - 3)^2 = 2^2 + 3^2 = 4 + 9 = \mathbf{13.0}$$

#### Langkah 2: Menghitung Nilai Kernel RBF
* $K(\mathbf{x}_1, \mathbf{x}^*) = \exp(-\gamma \|\mathbf{x}_1 - \mathbf{x}^*\|^2) = \exp(-0.5 \times 2.0) = \exp(-1.0) \approx \mathbf{0.36788}$
* $K(\mathbf{x}_2, \mathbf{x}^*) = \exp(-\gamma \|\mathbf{x}_2 - \mathbf{x}^*\|^2) = \exp(-0.5 \times 13.0) = \exp(-6.5) \approx \mathbf{0.00150}$

#### Langkah 3: Menghitung Nilai Fungsi Keputusan $f(\mathbf{x}^*)$
$$f(\mathbf{x}^*) = \sum_{i=1}^2 \alpha_i y_i K(\mathbf{x}_i, \mathbf{x}^*) + b$$
$$f(\mathbf{x}^*) = [\alpha_1 y_1 K(\mathbf{x}_1, \mathbf{x}^*)] + [\alpha_2 y_2 K(\mathbf{x}_2, \mathbf{x}^*)] + b$$
$$f(\mathbf{x}^*) = [1.2 \times (+1) \times 0.36788] + [1.2 \times (-1) \times 0.00150] - 0.20000$$
$$f(\mathbf{x}^*) = 0.44146 - 0.00180 - 0.20000 = \mathbf{+0.23966}$$

Karena $f(\mathbf{x}^*) = +0.23966 > 0$, maka sampel uji diprediksi tergolong ke dalam **Kelas $+1$ (Mutu CPO Prima)**.

---

### Soal 3: Analisis Matematis Teorema KKT & Variabel Kelonggaran Slack (C4)

#### 1. Status Geometris Sampel Berdasarkan Nilai Koefisien Dual $\alpha_i$
* **a) $\alpha_i = 0$ (Non-Support Vectors)**:
  Sampel berada aman di luar koridor margin ($y_i(\mathbf{w}^T \mathbf{x}_i + b) > 1$ dengan $\xi_i = 0$). Titik-titik ini sama sekali tidak memberikan gaya dorong pada letak bidang pemisah; jika sampel ini dihapus dari dataset, hiperbidang SVM tidak akan bergeser sedikit pun.
* **b) $0 < \alpha_i < C$ (Free Support Vectors)**:
  Sampel berada tepat di atas batas kanonik margin ($y_i(\mathbf{w}^T \mathbf{x}_i + b) = 1$ dengan $\xi_i = 0$). Titik-titik inilah yang menentukan nilai optimal bias $b$ dan menahan lebar margin secara presisi.
* **c) $\alpha_i = C$ (Bounded Support Vectors)**:
  Sampel melanggar margin ($\xi_i > 0$). Titik ini dapat berupa sampel yang berada di dalam koridor margin ($0 < \xi_i \le 1$) atau sampel pencilan yang salah diklasifikasikan ($\xi_i > 1$).

#### 2. Dampak Kenaikan Nilai $C = 0.1 \to C = 1000.0$
* **Lebar Margin**: Nilai $C$ yang sangat besar memberikan bobot penalti pelanggaran yang sangat keras. Model dipaksa mempersempit margin ($M$ mengecil) demi meminimalkan $\sum \xi_i$.
* **Jumlah Vektor Pendukung**: Jumlah support vector berkurang karena model tidak lagi mengizinkan sampel melanggar koridor margin secara bebas.
* **Risiko Overfitting**: Risiko *overfitting* melonjak tajam karena model akan membengkokkan batas pemisah demi mengakomodasi sampel kotor atau pencilan data latih, merusak kemampuan generalisasi terhadap sampel baru di lapangan.

#### 3. Mengapa SVM Lebih Kebal terhadap Outlier Ekstrem Dibanding Regresi Logistik
Pada Regresi Logistik, fungsi rugi *Log-Loss* $-\ln(\sigma(z))$ bernilai non-nol untuk setiap sampel. Jika ada satu sampel yang berada sangat jauh di dalam wilayah kelasnya ($z \gg 0$), sampel tersebut tetap menyumbang gradien kecil pada pembaruan bobot. Jika posisinya bergeser ekstrem, seluruh bidang logistik ikut bergeser.
Sebaliknya, pada SVM, kondisi KKT menjamin bahwa begitu suatu titik berada di luar batas margin ($y_i f(\mathbf{x}_i) \ge 1$), nilai pengali Lagrange-nya adalah **$\alpha_i = 0$ mutlak**. Titik tersebut tidak memiliki kontribusi apa pun terhadap vektor bobot $\mathbf{w} = \sum \alpha_i y_i \mathbf{x}_i$. Oleh karena itu, sejauh apa pun titik aman bergeser, posisi hiperbidang SVM tetap kokoh tak tergoyahkan.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Efek Pelatihan SVM Tanpa StandardScaler
Ketika data dilatih tanpa penskalaan:
* Fitur dengan nilai desimal kecil diabaikan oleh perhitungan jarak Euclidean kernel RBF.
* Akurasi uji anjlok dari 100% menjadi sekitar 65% (setara tebakan mayoritas kelas).
* Jumlah Vektor Pendukung melonjak hingga hampir 90% dari seluruh data latih karena model gagal menemukan bidang pemisah yang rapi.

### 4.2 Eksplorasi Grid Search Parameter C
* Nilai $C = 0.01$: Model mengalami *underfitting*, margin terlalu lebar, seluruh sampel dianggap melanggar margin (jumlah SV tinggi).
* Nilai $C = 10.0$: Keseimbangan optimal, akurasi uji 100%, jumlah SV ramping (31 titik).
* Nilai $C = 1000.0$: Margin sangat sempit, model sangat kaku, waktu konvergensi algoritma optimasi QP meningkat.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Geometri Margin, Kondisi KKT, & Kernel Trick | 25% | Mampu menurunkan formula lebar margin $2/\|\mathbf{w}\|$, menjelaskan peran kondisi komplementer KKT, dan menguraikan prinsip Teorema Mercer. |
| **C3 (Penerapan)** | Implementasi Pipeline SVM & Ekstraksi Vektor | 35% | Mampu mengintegrasikan `StandardScaler` dan `SVC` dalam pipeline, mengekstrak profil Support Vectors, serta menguji sampel spektroskopi baru. |
| **C4 (Analisis)** | Analisis Hyperparameter & Transisi Paradigma | 40% | Mampu menganalisis pengaruh interaksi $C$ dan $\gamma$, membedah kekebalan outlier KKT, serta mengartikulasikan transisi ke Unsupervised Learning. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.8 (K-Means Clustering)

Di penutup praktikum, instruktur disarankan memimpin refleksi besar mengenai kurikulum pembelajaran mesin:
1. **Merayakan Penguasaan Supervised Learning**: Dari Modul 7.1 hingga 7.7, mahasiswa telah menguasai seluruh spektrum pembelajaran terawasi: Regresi Linier, Regresi Logistik, KNN, Decision Tree, Random Forest, Naive Bayes, dan SVM.
2. **Menghadapi Realitas Data Lapangan**: Tantang mahasiswa: *"Bagaimana jika perusahaan perkebunan Anda membeli citra drone seluas 50.000 hektar yang memuat 100 juta piksel tanpa ada satupun label dari mandor? Apakah ketujuh algoritma yang kita pelajari masih bisa digunakan?"*
3. **Mengantarkan Era Unsupervised Learning**: Buka wawasan bahwa pada pertemuan berikutnya (**AI Modul 7.8: K-Means Clustering**), mahasiswa akan melangkah ke era baru: membiarkan komputer menemukan sendiri pola klaster tersembunyi (*unlabeled clustering*) untuk zonasi kesuburan tanah dan manajemen perkebunan presisi modern.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273-297.
2. Vapnik, V. (1998). *Statistical Learning Theory*. Wiley-Interscience.
3. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
4. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
5. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
6. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
7. Schölkopf, B., & Smola, A. J. (2002). *Learning with Kernels: Support Vector Machines, Regularization, Optimization, and Beyond*. MIT Press.
