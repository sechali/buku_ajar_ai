# AI Modul 9.4: Panduan Instruktur & Kunci Solusi
## Fungsi Aktivasi & Arsitektur Multi-Layer Perceptron (MLP)

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-09-04-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Non-Linieritas, Fungsi Aktivasi, & Teorema Cybenko; 70 Menit Praktikum Python MLP Sortasi TBS & Transformasi Ruang Laten; 30 Menit Evaluasi Kasus Multi-Kelas)
* **Karakteristik Modul**: Representasi Ruang Laten Non-Linier (*Latent Space Representation*), Mitigasi Vanishing Gradient, Klasifikasi Probabilistik Multi-Kelas Softmax

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Modul 9.4 adalah jembatan fundamental dari model linier sederhana menuju jaringan saraf dalam (*Deep Learning*). Pendekatan pedagogis yang disarankan:
1. **Analogi Melipat Lembaran Kertas Origami**:
   * Ambil selembar kertas dengan dua titik merah dan dua titik biru yang tersusun bersilangan seperti gerbang XOR.
   * Ajukan tantangan: *"Bisakah Anda memotong kertas ini dengan satu tebasan gunting lurus sehingga semua titik merah terpisah dari titik biru?"* Jawabannya: mustahil!
   * Namun, jika kertas tersebut **dilipat sekali (transformasi non-linier oleh lapisan tersembunyi)**, kedua titik merah akan saling menempel di satu sisi, dan kedua titik biru berada di sisi lain. Sekarang, satu tebasan lurus dapat memisahkan mereka dengan sempurna!
   * *Koneksi Algoritma*: Itulah persis apa yang dilakukan lapisan tersembunyi dengan fungsi aktivasi non-linier: melipat dan meregangkan ruang geometris fitur masukan!
2. **Konteks Spesifik INSTIPER**:
   * Tunjukkan bahwa klasifikasi kematangan buah kelapa sawit di pabrik kelapa sawit (PKS) tidak pernah sesederhana "makin merah makin matang".
   * Buah mentah berwarna hitam, buah matang berwarna jingga terang, namun buah lewat matang (*overripe*) kembali berubah warna menjadi merah gelap kehitaman akibat degradasi karotenoid dan oksidasi asam lemak. Hubungan warna terhadap kualitas rendemen CPO ini berbentuk parabola non-linier yang hanya bisa ditangkap oleh Multi-Layer Perceptron.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Makin banyak lapisan yang kita tambahkan dengan fungsi aktivasi linier $f(z) = z$, model akan semakin pintar dan akurat."**
  * *Koreksi Instruktur*: Tunjukkan pembuktian aljabar bahwa perkalian beruntun matriks linier $\mathbf{W}^{(3)}\mathbf{W}^{(2)}\mathbf{W}^{(1)}$ hanya menghasilkan satu matriks linier baru. Menumpuk 100 lapisan linier tidak ada bedanya dengan satu model regresi linier biasa. Tanpa fungsi aktivasi non-linier, kedalaman jaringan (*depth*) sama sekali tidak memiliki arti fungsional.
* **Miskonsepsi 2: "Fungsi Sigmoid selalu lebih unggul dari ReLU karena Sigmoid menghasilkan nilai kontinu halus antara 0 dan 1."**
  * *Koreksi Instruktur*: Jelaskan bahwa turunan maksimum Sigmoid hanya 0.25. Ketika jaringan memiliki 5 lapisan tersembunyi, gradien yang merambat mundur tereduksi sebesar $(0.25)^5 \approx 0.00097$, membuat neuron-neuron lapisan awal mati suri (*vanishing gradient*). ReLU merevolusi AI karena gradiennya konstan 1.0 pada nilai positif.
* **Miskonsepsi 3: "Fungsi Softmax dapat digunakan di sembarang lapisan tersembunyi."**
  * *Koreksi Instruktur*: Luruskan bahwa Softmax melibatkan normalisasi pembagian eksponensial di seluruh neuron satu lapisan ($\sum e^{z_j}$). Sifat ini dirancang khusus untuk mengubah skor logit mentah menjadi distribusi probabilitas multikelas pada **lapisan luaran (*output layer*)**, bukan untuk transformasi fitur pada lapisan tersembunyi.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual Propagasi Maju Lapisan Tersembunyi & Output Softmax (C3)
Data input: $\mathbf{x} = [0.8, 0.4]^T$.
Arsitektur: Input (2) $\to$ Hidden (2, ReLU) $\to$ Output (2, Softmax).

Matriks bobot dan bias:
$$\mathbf{W}^{(1)} = \begin{pmatrix} 1.5 & -0.5 \\ -2.0 & 1.0 \end{pmatrix}, \quad \mathbf{b}^{(1)} = \begin{pmatrix} -0.2 \\ 0.5 \end{pmatrix}$$
$$\mathbf{W}^{(2)} = \begin{pmatrix} 2.0 & -1.0 \\ -1.0 & 2.0 \end{pmatrix}, \quad \mathbf{b}^{(2)} = \begin{pmatrix} 0.0 \\ 0.1 \end{pmatrix}$$

#### Langkah 1: Menghitung Net Input Lapisan Tersembunyi $\mathbf{z}^{(1)}$
$$\mathbf{z}^{(1)} = \mathbf{W}^{(1)} \mathbf{x} + \mathbf{b}^{(1)}$$
$$z_1^{(1)} = (1.5)(0.8) + (-0.5)(0.4) + (-0.2) = 1.20 - 0.20 - 0.20 = \mathbf{0.80}$$
$$z_2^{(1)} = (-2.0)(0.8) + (1.0)(0.4) + 0.5 = -1.60 + 0.40 + 0.50 = \mathbf{-0.70}$$
$$\mathbf{z}^{(1)} = \begin{pmatrix} 0.80 \\ -0.70 \end{pmatrix}$$

#### Langkah 2: Menghitung Aktivasi Lapisan Tersembunyi $\mathbf{a}^{(1)}$ (Aktivasi ReLU)
$$a_1^{(1)} = \max(0, 0.80) = \mathbf{0.80}$$
$$a_2^{(1)} = \max(0, -0.70) = \mathbf{0.00}$$
$$\mathbf{a}^{(1)} = \begin{pmatrix} 0.80 \\ 0.00 \end{pmatrix}$$
*(Catatan: Terjadi penonaktifan/sparsitas alami pada neuron ke-2 karena nilainya negatif).*

#### Langkah 3: Menghitung Net Input Lapisan Luaran $\mathbf{z}^{(2)}$
$$\mathbf{z}^{(2)} = \mathbf{W}^{(2)} \mathbf{a}^{(1)} + \mathbf{b}^{(2)}$$
$$z_1^{(2)} = (2.0)(0.80) + (-1.0)(0.00) + 0.0 = 1.60 + 0.0 + 0.0 = \mathbf{1.60}$$
$$z_2^{(2)} = (-1.0)(0.80) + (2.0)(0.00) + 0.1 = -0.80 + 0.0 + 0.1 = \mathbf{-0.70}$$
$$\mathbf{z}^{(2)} = \begin{pmatrix} 1.60 \\ -0.70 \end{pmatrix}$$

#### Langkah 4: Menghitung Probabilitas Luaran Softmax $\hat{\mathbf{y}}$
Hitung suku eksponensial:
$$e^{z_1^{(2)}} = e^{1.60} \approx 4.9530$$
$$e^{z_2^{(2)}} = e^{-0.70} \approx 0.4966$$
Jumlah eksponensial total:
$$\sum = 4.9530 + 0.4966 = 5.4496$$

Probabilitas Softmax masing-masing kelas:
$$\hat{y}_1 = \frac{e^{1.60}}{\sum} = \frac{4.9530}{5.4496} \approx \mathbf{0.9089 \text{ (atau } 90.89\%)}$$
$$\hat{y}_2 = \frac{e^{-0.70}}{\sum} = \frac{0.4966}{5.4496} \approx \mathbf{0.0911 \text{ (atau } 9.11\%)}$$
$$\hat{\mathbf{y}} = \begin{pmatrix} 0.9089 \\ 0.0911 \end{pmatrix}$$

*Keputusan Akhir*: Model memprediksi sampel TBS sawit ini masuk ke dalam **Kelas 1** dengan tingkat keyakinan probabilitas sebesar **$90.89\%$**.

---

### Soal 2: Analisis Matematis Fenomena Vanishing Gradient pada Fungsi Sigmoid (C4)

#### 1. Pembuktian Nilai Maksimum Turunan Sigmoid $\sigma'(z) \leq 0.25$
Fungsi Sigmoid: $\sigma(z) = \frac{1}{1 + e^{-z}}$.
Turunan pertamanya:
$$\sigma'(z) = \sigma(z)(1 - \sigma(z))$$
Misalkan $u = \sigma(z)$. Karena rentang nilai $\sigma(z)$ adalah interval terbuka $(0, 1)$, kita dapat memandang turunan ini sebagai fungsi kuadrat parabola terhadap $u$:
$$g(u) = u(1 - u) = u - u^2, \quad \text{untuk } u \in (0, 1)$$

Untuk mencari titik puncak maksimum, turunkan $g(u)$ terhadap $u$ dan samakan dengan nol:
$$\frac{dg}{du} = 1 - 2u = 0 \implies u^* = \frac{1}{2} = 0.5$$

Nilai puncak maksimum:
$$g(0.5) = 0.5(1 - 0.5) = 0.5 \times 0.5 = \mathbf{0.25}$$

Untuk mencari nilai $z$ yang menghasilkan $u = 0.5$:
$$\sigma(z) = \frac{1}{1 + e^{-z}} = 0.5 \implies 1 + e^{-z} = 2 \implies e^{-z} = 1 \implies \mathbf{z = 0}$$
*Kesimpulan Terbukti*: Nilai turunan Sigmoid mencapai maksimum tepat sebesar **$0.25$** hanya pada saat $z = 0$, dan bernilai lebih kecil dari $0.25$ di seluruh titik lainnya.

#### 2. Estimasi Batas Atas Pengali Gradien pada Jaringan 5 Lapisan
Berdasarkan aturan rantai (*chain rule*) kalkulus, turunan parsial fungsi rugi terhadap bobot lapisan pertama melibatkan perkalian turunan aktivasi dari seluruh lapisan perantara:
$$\frac{\partial \text{Loss}}{\partial \mathbf{W}^{(1)}} \propto \prod_{l=1}^{5} \left(\mathbf{W}^{(l+1)T} \cdot \sigma'\left(\mathbf{z}^{(l)}\right)\right)$$
Jika bobot rata-rata $\|\mathbf{W}\| \approx 1.0$, maka faktor pengali skalar gradien dibatasi oleh:
$$\text{Faktor Pengali} \leq \left(\sigma'_{\max}\right)^5 = (0.25)^5 = \frac{1}{4^5} = \frac{1}{1024} \approx \mathbf{0.0009765}$$

#### 3. Analisis Dampak Terhadap Pembelajaran & Solusi ReLU
* **Dampak**: Gradien sinyal galat yang sampai ke lapisan tersembunyi pertama telah menyusut lebih dari $99.9\%$. Akibatnya, nilai pembaruan bobot $\Delta \mathbf{W}^{(1)} = -\eta \frac{\partial \text{Loss}}{\partial \mathbf{W}^{(1)}} \approx \mathbf{0}$. Lapisan depan tidak mengalami perubahan bobot yang berarti, sehingga jaringan gagal mempelajari ekstraksi fitur dasar.
* **Solusi ReLU**: Fungsi ReLU memiliki turunan $f'(z) = 1.0$ untuk setiap nilai positif. Perkalian berulang $(1.0)^5 = \mathbf{1.0}$, sehingga gradien mengalir deras tanpa redaman sedikit pun ke lapisan-lapisan paling awal.

---

### Soal 3: Bedah Kritis Teorema Cybenko vs Arsitektur Deep Learning Modern (C4)

#### 1. Mengapa Jaringan Dalam (*Deep*) Lebih Unggul dari Jaringan Dangkal Lebar (*Shallow*)
* Teorema Aproksimasi Universal Cybenko (1989) menjamin bahwa 1 lapisan tersembunyi cukup, namun teorema tersebut **tidak membatasi jumlah neuron $N$**.
* Untuk mengaproksimasi fungsi dengan kompleksitas tinggi (seperti tekstur variasi ribuan brondolan sawit di bawah pencahayaan berbeda), jaringan satu lapis membutuhkan jumlah neuron tersembunyi yang meledak secara eksponensial terhadap dimensi masukan ($N = \mathcal{O}(2^m)$). Hal ini memicu kebutuhan memori yang tidak realistis dan kecenderungan menghafal data (*overfitting* parah).
* Sebaliknya, **Jaringan Dalam (*Deep Networks*)** menyusun komposisi fungsi secara hierarkis:
  $$f(\mathbf{x}) = f_L(f_{L-1}(\dots f_1(\mathbf{x})))$$
  Penelitian Bengio et al. membuktikan bahwa struktur bertingkat ini mampu merepresentasikan fungsi kompleks dengan jumlah total parameter yang tumbuh secara polinomial (jauh lebih hemat dan kompak).

#### 2. Konsep Hierarchical Feature Abstraction pada Citra Perkebunan
Pada sistem visi komputer sortasi TBS berbasis jaringan multi-lapis:
1. **Lapisan Tersembunyi 1 (Fitur Rendah / Low-Level)**: Mengekstraksi batas tepi (*edges*), sudut garis, dan kontras intensitas warna dasar antara brondolan dan tangkai.
2. **Lapisan Tersembunyi 2 (Fitur Menengah / Mid-Level)**: Menggabungkan garis-garis menjadi tekstur permukaan (kulit mengkilap vs kusam) dan pola kurvatur kelengkungan brondolan buah.
3. **Lapisan Tersembunyi Akhir (Fitur Tinggi / High-Level)**: Mengabstraksikan konsep semantik utuh mengenai derajat kerapatan brondolan lepas (*abscission layer*) dan derajat kematangan TBS secara menyeluruh.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Mengapa Aktivasi Identity Menghasilkan Skor Terburuk pada Data Heterogen
Ketika data sortasi TBS memiliki pola batas kelas melengkung, aktivasi `identity` membatasi pemisahan hanya pada bidang datar hiperlinier. Model linier tidak mampu membedakan buah lewat matang dari buah mentah jika keduanya memiliki irisan reflektansi kemerahan yang mirip, menghasilkan akurasi yang stagnan.

### 4.2 Analisis Reduksi Dimensi Ruang Laten (*Latent Space PCA*)
Visualisasi PCA pada aktivasi lapisan tersembunyi ke-2 (`h2_act`) membuktikan bahwa:
* Pada ruang fitur asli, titik-titik sampel 4 kelas TBS masih saling tumpang tindih dan memanjang tak beraturan.
* Setelah melewati transformasi non-linier dua lapisan ReLU, titik-titik tersebut terkelompok menjadi 4 pulau klaster yang terpisah secara tegas dengan jarak antar-kelas yang lebar, membuktikan kekuatan manifold non-linier MLP.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Teori Aktivasi & Pembuktian Runtuhnya Jaringan Linier | 25% | Mampu membuktikan aljabar perkalian matriks linier, menguraikan karakteristik Sigmoid/Tanh/ReLU/Softmax, dan menjelaskan Teorema Cybenko. |
| **C3 (Penerapan)** | Perhitungan Manual Forward Pass & Implementasi Softmax | 35% | Mampu menghitung secara presisi aktivasi tersembunyi ReLU dan luaran probabilitas Softmax, serta membangun model MLP scikit-learn. |
| **C4 (Analisis)** | Analisis Vanishing Gradient & Dekomposisi Ruang Laten | 40% | Mampu menurunkan batas maksimum turunan Sigmoid, menganalisis efek kedalaman jaringan, dan mengevaluasi visualisasi PCA ruang laten. |

---

## 6. Jembatan Pedagogis ke AI Modul 8.3 (Forward Propagation & Loss Functions)

Di penutup praktikum, instruktur disarankan memandu refleksi transisi materi:
1. **Pencapaian Mahasiswa**: Mahasiswa telah memahami arsitektur anatomis MLP dan bagaimana fungsi aktivasi non-linier melipat ruang geometris data.
2. **Pertanyaan Pengantar**: *"Pada praktikum hari ini, kita menggunakan `best_mlp.fit()` dari Scikit-Learn sebagai kotak hitam untuk melatih bobot. Namun, bagaimana sebenarnya algoritma komputer mengetahui bahwa bobot saat ini masih salah? Bagaimana kita mengukur galat tersebut secara matematis?"*
3. **Mengantarkan Modul 8.3**: Sampaikan bahwa pada **AI Modul 8.3 (Algoritma Forward Propagation & Loss Functions)**, mahasiswa akan membedah:
   * Aliran komputasi tensorial batch perambatan maju.
   * Fungsi rugi **Binary Cross-Entropy** dan **Categorical Cross-Entropy** yang menjadi dasar matematis kalkulus optimasi seluruh model Deep Learning di dunia.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
2. Cybenko, G. (1989). Approximation by superpositions of a sigmoidal function. *Mathematics of Control, Signals and Systems*, 2(4), 303-314.
3. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
4. Glorot, X., & Bengio, Y. (2010). Understanding the difficulty of training deep feedforward neural networks. *Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (AISTATS)*, 249-256.
5. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. [Tersedia di koleksi src/]
6. He, K., Zhang, X., Ren, S., & Sun, J. (2015). Delving deep into rectifiers: Surpassing human-level performance on ImageNet classification. *Proceedings of the IEEE International Conference on Computer Vision*, 1026-1034.
7. Hornik, K. (1991). Approximation capabilities of multilayer feedforward networks. *Neural Networks*, 4(2), 251-257.
8. Maas, A. L., Hannun, A. Y., & Ng, A. Y. (2013). Rectifier nonlinearities improve neural network acoustic models. *Proc. ICML*, 30(1), 3.
9. Nair, V., & Hinton, G. E. (2010). Rectified linear units improve restricted boltzmann machines. *Proceedings of the 27th International Conference on Machine Learning (ICML-10)*, 807-814.
10. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. [Tersedia di koleksi src/]
