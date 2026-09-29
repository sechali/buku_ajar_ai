# AI Modul 9.5: Panduan Instruktur & Kunci Solusi
## Algoritma Forward Propagation & Loss Functions

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-09-05-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Aljabar Matriks Batch, Cross-Entropy, & MLE; 70 Menit Praktikum Python Computational Graph, BCE, CCE, & Log-Sum-Exp; 30 Menit Evaluasi Kasus Penyakit Ganoderma)
* **Karakteristik Modul**: Aliran Tensorial Graf Komputasi (*Computational Graph DAG*), Stabilisasi Numerik Floating-Point, Optimasi Fungsi Objektif Berbasis Teori Informasi

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Modul 9.5 membahas fondasi pengukuran objektif dalam deep learning. Pendekatan pengajaran yang disarankan:
1. **Analogi Papan Target Panahan dan Denda Moneter**:
   * Ajukan perumpamaan: *"Seorang pemanah menembakkan anak panah ke papan target. Fungsi rugi (Loss Function) adalah wasit yang mengukur seberapa jauh anak panah meleset dari titik tengah."*
   * *Regresi (MSE)*: Mengukur jarak sentimeter deviasi kuadratik fisik anak panah dari pusat target.
   * *Klasifikasi (Cross-Entropy)*: Memberikan denda eksponensial. Jika pemanah sangat percaya diri anak panahnya tepat di tengah ($p = 0.99$), namun ternyata meleset total ke area penonton ($y = 0$), denda yang dijatuhkan mendekati tak terhingga ($-\ln(0.01) \approx 4.6$). Hal ini memaksa pemanah mengubah bidikan secara drastis pada putaran berikutnya!
2. **Konteks Spesifik INSTIPER**:
   * Tunjukkan bahwa dalam proteksi tanaman sawit terhadap jamur *Ganoderma boninense*, biaya kesalahan tidak pernah simetris.
   * Salah menduga pohon sehat sebagai sakit (*False Positive*) hanya memicu tes ulang laboratorium berbiaya Rp 150.000. Namun, salah menduga pohon terinfeksi Ganoderma sebagai pohon sehat (*False Negative*) akan membiarkan jamur menulari blok kebun, memicu kerugian hingga Rp 45.000.000 per pohon.
   * Tunjukkan bahwa fungsi *Weighted Binary Cross-Entropy* adalah instrumen matematika yang menyuntikkan prioritas bisnis agronomi ini ke dalam algoritma AI.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Nilai loss nol koma lima (0.5) berarti model memiliki akurasi 50%."**
  * *Koreksi Instruktur*: Luruskan bahwa *Loss* dan *Accuracy* adalah dua besaran yang sama sekali berbeda. Akurasi adalah metrik diskrit ambang batas (persentase tebakan benar), sedangkan *Loss* adalah besaran skalar kontinu penalti probabilitas. Model dapat memiliki akurasi 100% namun tetap memiliki loss 0.2 jika probabilitas prediksinya belum mencapai 1.0 penuh.
* **Miskonsepsi 2: "Menggunakan fungsi rugi MSE sah-sah saja untuk klasifikasi asalkan keluarannya dibulatkan menjadi 0 atau 1."**
  * *Koreksi Instruktur*: Buktikan secara matematis bahwa memadukan MSE dengan fungsi Sigmoid menciptakan turunan $\frac{\partial \mathcal{L}}{\partial z} = (\hat{y} - y)\sigma'(z)$. Saat model membuat kesalahan fatal ($z \to -\infty$ padahal $y=1$), nilai $\sigma'(z) \to 0$. Hal ini melumpuhkan gradien pembaruan bobot (*learning slowdown*). Pasangkan selalu Sigmoid dengan BCE, dan Softmax dengan CCE!
* **Miskonsepsi 3: "Komputasi formula matematika murni di Python selalu menghasilkan angka yang sama dengan teori buku teks."**
  * *Koreksi Instruktur*: Demonstrasikan fenomena *floating-point underflow/overflow* pada komputer. Tanpa trik stabilisasi numerik (*Log-Sum-Exp* dan *epsilon clipping*), komputer akan memunculkan nilai `NaN` atau `inf` saat mengevaluasi nilai logit masukan besar ($z > 710$), merusak seluruh pelatihan model.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual Komputasi Batch Forward Pass & CCE Loss (C3)
Data masukan:
$$\mathbf{X} = \begin{pmatrix} 0.5 & 0.2 \\ 0.1 & 0.8 \end{pmatrix} \in \mathbb{R}^{2 \times 2}$$
Label target one-hot 3 kelas:
$$\mathbf{Y} = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix} \in \mathbb{R}^{2 \times 3}$$

Parameter bobot dan bias:
$$\mathbf{W} = \begin{pmatrix} 1.0 & -0.5 & 0.0 \\ 0.0 & 1.0 & -1.0 \end{pmatrix}, \quad \mathbf{b} = \begin{pmatrix} 0.1 \\ -0.2 \\ 0.1 \end{pmatrix}$$

#### Langkah 1: Menghitung Perkalian Matriks $\mathbf{X}\mathbf{W}$
* Sampel 1: $\mathbf{x}_1 = [0.5, 0.2]$
  $$[\mathbf{x}_1 \mathbf{W}]_1 = (0.5)(1.0) + (0.2)(0.0) = 0.50$$
  $$[\mathbf{x}_1 \mathbf{W}]_2 = (0.5)(-0.5) + (0.2)(1.0) = -0.25 + 0.20 = -0.05$$
  $$[\mathbf{x}_1 \mathbf{W}]_3 = (0.5)(0.0) + (0.2)(-1.0) = -0.20$$
* Sampel 2: $\mathbf{x}_2 = [0.1, 0.8]$
  $$[\mathbf{x}_2 \mathbf{W}]_1 = (0.1)(1.0) + (0.8)(0.0) = 0.10$$
  $$[\mathbf{x}_2 \mathbf{W}]_2 = (0.1)(-0.5) + (0.8)(1.0) = -0.05 + 0.80 = 0.75$$
  $$[\mathbf{x}_2 \mathbf{W}]_3 = (0.1)(0.0) + (0.8)(-1.0) = -0.80$$

#### Langkah 2: Menambahkan Vektor Bias $\mathbf{b}^T = [0.1, -0.2, 0.1]$
$$\mathbf{Z} = \begin{pmatrix} 0.50 + 0.1 & -0.05 - 0.2 & -0.20 + 0.1 \\ 0.10 + 0.1 & 0.75 - 0.2 & -0.80 + 0.1 \end{pmatrix} = \begin{pmatrix} 0.60 & -0.25 & -0.10 \\ 0.20 & 0.55 & -0.70 \end{pmatrix}$$

#### Langkah 3: Menghitung Probabilitas Luaran Softmax $\hat{\mathbf{Y}}$
* **Untuk Sampel 1**: $\mathbf{z}_1 = [0.60, -0.25, -0.10]$
  $$e^{0.60} \approx 1.8221, \quad e^{-0.25} \approx 0.7788, \quad e^{-0.10} \approx 0.9048$$
  $$\sum_1 = 1.8221 + 0.7788 + 0.9048 = 3.5057$$
  $$\hat{\mathbf{y}}_1 = \left[\frac{1.8221}{3.5057}, \frac{0.7788}{3.5057}, \frac{0.9048}{3.5057}\right] = [\mathbf{0.5198}, \mathbf{0.2222}, \mathbf{0.2581}]$$

* **Untuk Sampel 2**: $\mathbf{z}_2 = [0.20, 0.55, -0.70]$
  $$e^{0.20} \approx 1.2214, \quad e^{0.55} \approx 1.7333, \quad e^{-0.70} \approx 0.4966$$
  $$\sum_2 = 1.2214 + 1.7333 + 0.4966 = 3.4513$$
  $$\hat{\mathbf{y}}_2 = \left[\frac{1.2214}{3.4513}, \frac{1.7333}{3.4513}, \frac{0.4966}{3.4513}\right] = [\mathbf{0.3539}, \mathbf{0.5022}, \mathbf{0.1439}]$$

#### Langkah 4: Menghitung Kerugian Categorical Cross-Entropy
* **Sampel 1**: Target $\mathbf{y}_1 = [1, 0, 0]$ (Kelas sejati adalah indeks 1)
  $$\mathcal{L}_1 = -\ln(\hat{y}_{11}) = -\ln(0.5198) \approx \mathbf{0.6543}$$
* **Sampel 2**: Target $\mathbf{y}_2 = [0, 0, 1]$ (Kelas sejati adalah indeks 3)
  $$\mathcal{L}_2 = -\ln(\hat{y}_{23}) = -\ln(0.1439) \approx \mathbf{1.9386}$$
* **Rata-Rata Kerugian Batch ($J$)**:
  $$J = \frac{\mathcal{L}_1 + \mathcal{L}_2}{2} = \frac{0.6543 + 1.9386}{2} = \frac{2.5929}{2} = \mathbf{1.2965}$$

---

### Soal 2: Penurunan Analitik Gradien CCE-Softmax Terhadap Logit (C4)

Fungsi Softmax: $p_i = \frac{e^{z_i}}{\sum_{k=1}^K e^{z_k}}$.

#### 1. Pembuktian Turunan Softmax $\frac{\partial p_i}{\partial z_j}$
Gunakan aturan pembagian kalkulus $\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}$:
* **Kasus $i = j$**:
  $$\frac{\partial p_i}{\partial z_i} = \frac{e^{z_i} \left(\sum_k e^{z_k}\right) - e^{z_i} e^{z_i}}{\left(\sum_k e^{z_k}\right)^2} = \frac{e^{z_i}}{\sum_k e^{z_k}} - \left(\frac{e^{z_i}}{\sum_k e^{z_k}}\right)^2 = \mathbf{p_i(1 - p_i)}$$
* **Kasus $i \neq j$**:
  $$\frac{\partial p_i}{\partial z_j} = \frac{0 \cdot \left(\sum_k e^{z_k}\right) - e^{z_i} e^{z_j}}{\left(\sum_k e^{z_k}\right)^2} = -\left(\frac{e^{z_i}}{\sum_k e^{z_k}}\right) \left(\frac{e^{z_j}}{\sum_k e^{z_k}}\right) = \mathbf{-p_i p_j}$$

#### 2. Penurunan Rantai Gradien $\frac{\partial \mathcal{L}}{\partial z_j}$
Fungsi rugi: $\mathcal{L} = -\sum_{i=1}^K y_i \ln(p_i)$.
Turunan terhadap probabilitas: $\frac{\partial \mathcal{L}}{\partial p_i} = -\frac{y_i}{p_i}$.
Gunakan aturan rantai multivariat:
$$\frac{\partial \mathcal{L}}{\partial z_j} = \sum_{i=1}^K \frac{\partial \mathcal{L}}{\partial p_i} \frac{\partial p_i}{\partial z_j} = \frac{\partial \mathcal{L}}{\partial p_j} \frac{\partial p_j}{\partial z_j} + \sum_{i \neq j} \frac{\partial \mathcal{L}}{\partial p_i} \frac{\partial p_i}{\partial z_j}$$
Substitusikan kedua kasus:
$$\frac{\partial \mathcal{L}}{\partial z_j} = \left(-\frac{y_j}{p_j}\right) [p_j(1 - p_j)] + \sum_{i \neq j} \left(-\frac{y_i}{p_i}\right) [-p_i p_j]$$
$$\frac{\partial \mathcal{L}}{\partial z_j} = -y_j(1 - p_j) + \sum_{i \neq j} y_i p_j = -y_j + y_j p_j + p_j \sum_{i \neq j} y_i$$
Faktorkan $p_j$:
$$\frac{\partial \mathcal{L}}{\partial z_j} = -y_j + p_j \left(y_j + \sum_{i \neq j} y_i\right) = -y_j + p_j \left(\sum_{i=1}^K y_i\right)$$
Karena target adalah vektor probabilitas one-hot, $\sum_{i=1}^K y_i = 1.0$.
Maka terbukti secara sempurna:
$$\mathbf{\frac{\partial \mathcal{L}}{\partial z_j} = p_j - y_j}$$

#### 3. Keunggulan Komputasi pada Perangkat Keras GPU
Hasil $\frac{\partial \mathcal{L}}{\partial z_j} = p_j - y_j$ membuktikan bahwa untuk menghitung gradien kesalahan pada lapisan luaran, kartu grafis **hanya perlu melakukan satu operasi pengurangan element-wise matriks sederhana: $\hat{\mathbf{Y}} - \mathbf{Y}$**. Tidak diperlukan operasi perkalian matriks Hessian atau pembagian berulang yang memakan siklus komputasi.

---

### Soal 3: Analisis Komparasi Numerik Trik Log-Sum-Exp vs Naive Softmax (C4)

Logit masukan: $\mathbf{z} = [1000.0, 1002.0, 998.0]^T$.

#### 1. Analisis Kegagalan Komputasi Naive Float32
* Pada format standar IEEE 754 float32 (atau bahkan float64 yang memiliki batas atas $\approx 1.8 \times 10^{308}$):
  $$e^{1000.0} \approx 1.97 \times 10^{434} \implies \textbf{Floating-Point Overflow!}$$
* Python akan menghasilkan nilai `inf` (tak berhingga).
* Saat menghitung probabilitas $\frac{\text{inf}}{\text{inf} + \text{inf} + \text{inf}}$, operasi menghasilkan **`NaN` (*Not a Number*)**.
* Akibatnya, seluruh gradien pelatihan jaringan runtuh seketika menjadi `NaN`.

#### 2. Mekanisme Solusi Melalui Pengurangan Nilai Maksimum $c = \max(\mathbf{z})$
Tentukan nilai maksimum: $c = \max(1000.0, 1002.0, 998.0) = 1002.0$.
Kurangkan $c$ dari setiap elemen:
$$\tilde{\mathbf{z}} = \mathbf{z} - c = [1000 - 1002, 1002 - 1002, 998 - 1002]^T = \mathbf{[-2.0, 0.0, -4.0]^T}$$
Nilai eksponensial sekarang berada dalam batas aman sempurna:
$$e^{-2.0} \approx 0.1353, \quad e^{0.0} = 1.0000, \quad e^{-4.0} \approx 0.0183$$
$$\sum = 0.1353 + 1.0000 + 0.0183 = 1.1536$$
Probabilitas Softmax yang dihasilkan:
$$\hat{\mathbf{y}} = \left[\frac{0.1353}{1.1536}, \frac{1.0000}{1.1536}, \frac{0.0183}{1.1536}\right] \approx [\mathbf{0.1173}, \mathbf{0.8668}, \mathbf{0.0159}]$$
Perhitungan menghasilkan angka presisi tanpa ada error *overflow* sedikit pun.

#### 3. Pembuktian Identitas Matematis Log-Sum-Exp
$$\ln\left(\sum_{j=1}^K e^{z_j}\right) = \ln\left(\sum_{j=1}^K e^{z_j - c + c}\right) = \ln\left(\sum_{j=1}^K e^{z_j - c} \cdot e^c\right)$$
Keluarkan faktor skalar $e^c$ dari dalam tanda jumlahan:
$$= \ln\left(e^c \cdot \sum_{j=1}^K e^{z_j - c}\right) = \ln(e^c) + \ln\left(\sum_{j=1}^K e^{z_j - c}\right) = \mathbf{c + \ln\left(\sum_{j=1}^K e^{z_j - c}\right)} \quad \text{(Terbukti!)}$$

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Efek Bobot Asimetris pada Weighted Binary Cross-Entropy
Ketika parameter $w_{\text{pos}} = 10.0$ diaktifkan pada kasus Ganoderma:
* Nilai rugi rata-rata melompat lebih dari $5$ kali lipat saat model menghasilkan *False Negative* pada pohon sakit.
* Hal ini memaksa algoritma optimasi untuk menggeser ambang batas klasifikasi ke arah yang lebih sensitif, memprioritaskan *Recall* setinggi mungkin guna menyelamatkan kebun dari penyebaran epidemik.

### 4.2 Verifikasi Nilai CCE Loss pada Batch TBS
Pada praktikum, nilai $J_{\text{CCE}} \approx 1.1426$ mencerminkan kondisi awal model sebelum bobot diperbarui. Seiring berjalannya iterasi *Backpropagation* (pada Modul 8.4), nilai ini akan menyusut mendekati batas optimal $\approx 0.05$.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Graf Komputasi Forward Pass & Konsep MLE | 25% | Mampu menguraikan simpul-simpul komputasi DAG, merumuskan aljabar batch matriks, dan menjelaskan relasi MLE dengan entropi silang. |
| **C3 (Penerapan)** | Perhitungan Manual Batch & Implementasi Stabil Numerik | 35% | Mampu menghitung forward pass dan loss matriks secara presisi, serta menerapkan stabilisasi clipping dan Log-Sum-Exp. |
| **C4 (Analisis)** | Analisis Penurunan Gradien & Bukti Kelemahan MSE | 40% | Mampu menurunkan gradien $\frac{\partial \mathcal{L}}{\partial z} = p - y$, menganalisis redaman gradien pada MSE+Sigmoid, dan membuktikan identitas Log-Sum-Exp. |

---

## 6. Jembatan Pedagogis ke AI Modul 8.4 (Backpropagation)

Di akhir sesi praktikum, instruktur disarankan memimpin perenungan transisi:
1. **Refleksi Pencapaian**: Mahasiswa telah berhasil merumuskan aliran tensor maju dari input hingga skalar galat loss $J(\mathbf{W}, \mathbf{b})$.
2. **Pertanyaan Kunci**: *"Kita telah berhasil menghitung nilai galat sebesar 1.1426. Namun, dari 100 bobot yang ada di dalam jaringan, bobot mana yang paling bersalah menyebabkan galat tersebut? Berapa besar koreksi yang harus diberikan ke masing-masing bobot?"*
3. **Mengantarkan Modul 8.4**: Sampaikan bahwa pada pertemuan berikutnya (**AI Modul 8.4: Algoritma Backpropagation & Aturan Rantai Kalkulus**), mahasiswa akan mempelajari bagaimana aturan rantai kalkulus mengalirkan gradien dari simpul loss mundur ke seluruh lapisan untuk memperbarui parameter jaringan secara otomatis.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
2. Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). John Wiley & Sons.
3. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
4. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. [Tersedia di koleksi src/]
5. Lin, T. Y., Goyal, P., Girshick, R., He, K., & Dollár, P. (2017). Focal loss for dense object detection. *Proceedings of the IEEE International Conference on Computer Vision*, 2980-2988.
6. Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press.
7. Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*, 323(6088), 533-536.
8. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. [Tersedia di koleksi src/]
