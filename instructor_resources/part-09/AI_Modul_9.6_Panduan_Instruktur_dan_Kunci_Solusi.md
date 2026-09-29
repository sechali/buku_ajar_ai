# AI Modul 9.6: Panduan Instruktur & Kunci Solusi
## Algoritma Backpropagation & Aturan Rantai Kalkulus

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-09-06-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Aturan Rantai Multivariat & 4 Persamaan Backprop; 70 Menit Praktikum Python Scratch Engine & Gradient Checking; 30 Menit Evaluasi Dinamika Pelatihan TBS)
* **Karakteristik Modul**: Diferensiasi Otomatis Terbalik (*Reverse-Mode Automatic Differentiation*), Propagasi Galat Matriks Transpose, Pemrograman Dinamis Forward-Backward

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Modul 9.6 adalah inti mekanika terdalam dari kecerdasan buatan modern. Pendekatan pedagogis yang disarankan:
1. **Analogi Rantai Komando Audit Kebun**:
   * Bayangkan sebuah divisi logistik perkebunan kelapa sawit yang mengalami kerugian Rp 100 juta karena truk terlambat tiba di PKS.
   * *Forward Pass*: Perintah mengalir dari Direktur Operasional $\to$ Manajer Lapangan $\to$ Mandor $\to$ Sopir Truk $\to$ Hasil Timbangan PKS.
   * *Backpropagation*: Tim auditor mengusut kerugian dari hilir ke hulu. Berapa persen denda kesalahan yang harus ditanggung oleh sopir truk ($\boldsymbol{\delta}^{(L)}$)? Berapa porsi yang diakibatkan oleh disposisi rute mandor ($\boldsymbol{\delta}^{(L-1)}$)? Berapa porsi akibat salah instruksi manajer?
   * *Koneksi Algoritma*: Aturan rantai kalkulus $\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{(l)}} = \mathbf{A}^{(l-1)T} \boldsymbol{\delta}^{(l)}$ adalah rumusan audit matematis presisi yang membagikan tanggung jawab galat secara adil ke setiap bobot sinapsis sesuai besar kontribusinya.
2. **Konteks Spesifik INSTIPER**:
   * Tunjukkan bahwa mahasiswa INSTIPER tidak boleh hanya tahu memanggil `.fit()` dari pustaka instan.
   * Memahami Backpropagation dari dasar memberikan kemampuan mendiagnosis mengapa model visi komputer deteksi jamur atau sortasi TBS mengalami stagnasi pelatihan, serta bagaimana memodifikasi arsitektur khusus untuk chip berdaya rendah di traktor kebun.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Backpropagation memperbarui bobot secara langsung."**
  * *Koreksi Instruktur*: Tegaskan pemisahan konseptual dua langkah: **Backpropagation HANYA bertugas menghitung nilai turunan parsial (gradien $\frac{\partial \mathcal{L}}{\partial \mathbf{W}}$)**. Tahap pembaruan parameter yang sebenarnya dilakukan oleh algoritma **Optimizer** (seperti Gradient Descent, Momentum, atau Adam) menggunakan formula $\mathbf{W} \leftarrow \mathbf{W} - \eta \frac{\partial \mathcal{L}}{\partial \mathbf{W}}$.
* **Miskonsepsi 2: "Nilai galat delta $\boldsymbol{\delta}^{(l)}$ sama dengan nilai luaran aktivasi $\mathbf{a}^{(l)}$."**
  * *Koreksi Instruktur*: Luruskan bahwa $\mathbf{a}^{(l)}$ mengalir maju (*forward*) dan selalu positif jika menggunakan ReLU, sedangkan $\boldsymbol{\delta}^{(l)}$ mengalir mundur (*backward*) dan dapat bernilai positif maupun negatif (menunjukkan arah dorongan untuk menaikkan atau menurunkan net input).
* **Miskonsepsi 3: "Gradient Checking harus selalu diaktifkan selama pelatihan berlangsung."**
  * *Koreksi Instruktur*: Ingatkan bahwa komputasi beda hingga numerik pada Gradient Checking sangat lambat (membutuhkan 2 forward pass per parameter). Gradient Checking hanya dijalankan sebagai alat diagnostik (*unit test*) untuk memverifikasi kebenaran matematika kode sebelum pelatihan produksi skala besar dijalankan.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual Backward Pass Satu Sampel Lengkap (C3)
Spesifikasi jaringan:
* Masukan: $x = 2.0$, Target sejati: $y = 1.0$.
* Lapisan Tersembunyi: $w_1 = 0.5, b_1 = 0.1$, Aktivasi ReLU.
* Lapisan Luaran: $w_2 = 1.2, b_2 = -0.3$, Aktivasi Sigmoid $\sigma(z)$.
* Fungsi Rugi: $\mathcal{L}_{\text{BCE}} = -[y \ln(\hat{y}) + (1 - y) \ln(1 - \hat{y})]$.

#### Langkah 1: Perambatan Maju (Forward Pass)
* Net input tersembunyi:
  $$z_1 = w_1 x + b_1 = (0.5)(2.0) + 0.1 = 1.0 + 0.1 = \mathbf{1.10}$$
* Aktivasi tersembunyi (ReLU):
  $$a_1 = \max(0, 1.10) = \mathbf{1.10}$$
* Net input luaran:
  $$z_2 = w_2 a_1 + b_2 = (1.2)(1.10) + (-0.3) = 1.32 - 0.30 = \mathbf{1.02}$$
* Aktivasi luaran (Sigmoid):
  $$\hat{y} = \sigma(1.02) = \frac{1}{1 + e^{-1.02}} = \frac{1}{1 + 0.3606} = \frac{1}{1.3606} \approx \mathbf{0.7350}$$
* Nilai kerugian BCE:
  $$\mathcal{L} = -[1.0 \cdot \ln(0.7350) + 0] = -\ln(0.7350) \approx \mathbf{0.3079}$$

#### Langkah 2: Galat Lapisan Luaran ($\delta_2$)
Untuk kombinasi Sigmoid + BCE:
$$\delta_2 = \hat{y} - y = 0.7350 - 1.0 = \mathbf{-0.2650}$$

#### Langkah 3: Gradien Parameter Lapisan Luaran
* Terhadap bobot $w_2$:
  $$\frac{\partial \mathcal{L}}{\partial w_2} = a_1 \cdot \delta_2 = (1.10)(-0.2650) = \mathbf{-0.2915}$$
* Terhadap bias $b_2$:
  $$\frac{\partial \mathcal{L}}{\partial b_2} = \delta_2 = \mathbf{-0.2650}$$

#### Langkah 4: Galat Lapisan Tersembunyi ($\delta_1$)
Persamaan 2: $\delta_1 = (\delta_2 \cdot w_2) \cdot \text{ReLU}'(z_1)$.
Karena $z_1 = 1.10 > 0$, maka $\text{ReLU}'(1.10) = 1.0$.
$$\delta_1 = [(-0.2650)(1.2)] \cdot 1.0 = \mathbf{-0.3180}$$

#### Langkah 5: Gradien Parameter Lapisan Tersembunyi
* Terhadap bobot $w_1$:
  $$\frac{\partial \mathcal{L}}{\partial w_1} = x \cdot \delta_1 = (2.0)(-0.3180) = \mathbf{-0.6360}$$
* Terhadap bias $b_1$:
  $$\frac{\partial \mathcal{L}}{\partial b_1} = \delta_1 = \mathbf{-0.3180}$$

#### Langkah 6: Pembaruan Parameter dengan $\eta = 0.1$
Formula: $\theta \leftarrow \theta - \eta \frac{\partial \mathcal{L}}{\partial \theta}$.
* $w_1 \leftarrow 0.5 - 0.1(-0.6360) = 0.5 + 0.0636 = \mathbf{0.5636}$
* $b_1 \leftarrow 0.1 - 0.1(-0.3180) = 0.1 + 0.0318 = \mathbf{0.1318}$
* $w_2 \leftarrow 1.2 - 0.1(-0.2915) = 1.2 + 0.02915 = \mathbf{1.2292}$
* $b_2 \leftarrow -0.3 - 0.1(-0.2650) = -0.3 + 0.0265 = \mathbf{-0.2735}$

*Verifikasi Konsistensi Fisis*: Karena target adalah $y=1$ dan prediksi masih $0.735$ (terlalu rendah), seluruh bobot ($w_1, w_2$) dan bias ($b_1, b_2$) mengalami penyesuaian positif untuk memperbesar luaran prediksi pada iterasi berikutnya.

---

### Soal 2: Pembuktian Efisiensi Komputasi Analitik vs Beda Hingga Numerik (C4)
Arsitektur jaringan: $[128, 256, 128, 64, 4]$.

#### 1. Perhitungan Jumlah Total Parameter
* Lapisan 1: $\mathbf{W}^{(1)} \in \mathbb{R}^{128 \times 256} = 32.768$, $\mathbf{b}^{(1)} \in \mathbb{R}^{256} = 256$. Subtotal = $33.024$.
* Lapisan 2: $\mathbf{W}^{(2)} \in \mathbb{R}^{256 \times 128} = 32.768$, $\mathbf{b}^{(2)} \in \mathbb{R}^{128} = 128$. Subtotal = $32.896$.
* Lapisan 3: $\mathbf{W}^{(3)} \in \mathbb{R}^{128 \times 64} = 8.192$, $\mathbf{b}^{(3)} \in \mathbb{R}^{64} = 64$. Subtotal = $8.256$.
* Lapisan 4: $\mathbf{W}^{(4)} \in \mathbb{R}^{64 \times 4} = 256$, $\mathbf{b}^{(4)} \in \mathbb{R}^{4} = 4$. Subtotal = $260$.
* **Total Parameter ($P$)**:
  $$P = 33.024 + 32.896 + 8.256 + 260 = \mathbf{74.436\text{ parameter}}$$

#### 2. Perbandingan Waktu Komputasi ($T_{\text{forward}} = 2.5\text{ ms} = 0.0025\text{ detik}$)
* **Metode Beda Hingga Numerik Dua Sisi**:
  Membutuhkan $2 \times P$ kali forward pass untuk satu kali iterasi pembaruan bobot:
  $$\text{Waktu} = 2 \times 74.436 \times 0.0025\text{ detik} = 372.18\text{ detik} \approx \mathbf{6.20\text{ Menit per Iterasi!}}$$
  Untuk melatih model selama 10.000 iterasi, waktu yang dibutuhkan adalah $62.000\text{ menit} \approx \mathbf{43\text{ Hari}}!$

* **Metode Backpropagation Analitik**:
  Satu sapuan mundur membutuhkan waktu komputasi setara dengan $\approx 2 \times T_{\text{forward}}$:
  $$\text{Waktu per Iterasi} = T_{\text{forward}} + T_{\text{backward}} \approx 2.5\text{ ms} + 5.0\text{ ms} = \mathbf{7.5\text{ milidetik (0.0075 detik)}}$$
  Untuk 10.000 iterasi: $10.000 \times 0.0075 = \mathbf{75\text{ detik (1.25 Menit)}}!$

#### 3. Rasio Percepatan Komputasi (*Speedup Factor*)
$$\text{Speedup} = \frac{372.18\text{ detik}}{0.0075\text{ detik}} \approx \mathbf{49.624\times \text{ lipat lebih cepat!}}$$
*Interpretasi Akademik*: Tanpa algoritma Backpropagation, pelatihan model Deep Learning modern yang memiliki miliaran parameter (seperti GPT atau model visi drone YOLO) akan membutuhkan waktu jutaan tahun komputasi, menjadikannya kemustahilan fisik.

---

### Soal 3: Analisis Matematis Titik Belok Tak Terdiferensialkan pada ReLU ($z=0$) (C4)

#### 1. Pembuktian Teoretis Ketakberdiferensialan ReLU pada $z=0$
Definisi turunan menurut limit kalkulus:
* Limit turunan dari sisi kanan ($z \to 0^+$):
  $$\lim_{h \to 0^+} \frac{f(0 + h) - f(0)}{h} = \lim_{h \to 0^+} \frac{h - 0}{h} = \mathbf{1.0}$$
* Limit turunan dari sisi kiri ($z \to 0^-$):
  $$\lim_{h \to 0^-} \frac{f(0 + h) - f(0)}{h} = \lim_{h \to 0^-} \frac{0 - 0}{h} = \mathbf{0.0}$$
Karena limit kiri ($0.0$) tidak sama dengan limit kanan ($1.0$), maka menurut teorema dasar kalkulus diferensial, **fungsi ReLU tidak memiliki turunan (*non-differentiable*) tepat pada titik $z = 0$**.

#### 2. Konsep Subgradien (*Subgradient*) pada Pustaka Modern
Untuk fungsi cembung (*convex*) yang memiliki sudut tajam, kalkulus subgradien mendefinisikan subgradien $\partial f(0)$ sebagai sembarang nilai kemiringan garis singgung pendukung yang berada di antara limit kiri dan limit kanan:
$$\partial f(0) = [0.0, 1.0]$$
Seluruh pustaka modern (PyTorch, TensorFlow) mengadopsi konvensi deterministik sederhana dengan menetapkan nilai subgradien tepat di titik nol:
$$\text{ReLU}'(0) \equiv 0.0 \quad \text{(atau } 1.0\text{)}$$

#### 3. Dampak Pemilihan Subgradien di Praktik
Dalam implementasi praktikum dengan bilangan floating-point 64-bit, probabilitas suatu nilai net input tepat bernilai $0.000000000000000$ adalah mendekati nol secara statistik (*measure zero*). Menetapkan turunan bernilai $0.0$ pada $z \leq 0$ memberikan stabilitas numerik terbaik dan mendukung terciptanya representasi representasional yang hemat (*sparse activations*).

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Hasil Gradient Checking pada `MLPScratchEngine`
Hasil uji pada 25 parameter acak model menghasilkan nilai:
$$\text{Relative Difference} \approx 2.65 \times 10^{-9}$$
Nilai ini jauh di bawah ambang batas $10^{-7}$, membuktikan bahwa implementasi 4 persamaan fundamental Backprop bebas dari cacat matematis.

### 4.2 Dinamika Penurunan Rugi Pelatihan
* Pada 20 epoch pertama, nilai loss CCE terjun bebas dari $0.809$ menjadi $0.030$ (penurunan $96.3\%$).
* Pada epoch ke-80, loss menyusut hingga $0.0048$ dengan akurasi data uji mencapai **$99.33\%$**, memverifikasi keberhasilan perambatan balik galat multi-lapis.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Penurunan Teori 4 Persamaan Fundamental Backpropagation | 25% | Mampu menguraikan peran aturan rantai kalkulus, menurunkan $\boldsymbol{\delta}^{(L)}$ dan $\boldsymbol{\delta}^{(l)}$, serta menjelaskan mekanisme gradient descent. |
| **C3 (Penerapan)** | Perhitungan Manual Backward Pass & Implementasi Scratch | 35% | Mampu melakukan penyesuaian bobot manual step-by-step dan membangun kelas Python Backpropagation mandiri tanpa modul bawaan. |
| **C4 (Analisis)** | Efisiensi Waktu Komputasi & Uji Gradient Checking | 40% | Mampu membuktikan percepatan $49.000\times$ dibanding beda hingga, menganalisis subgradien ReLU, dan mengeksekusi gradient checking. |

---

## 6. Jembatan Pedagogis ke AI Modul 8.5 (Optimizers Lanjut)

Di akhir sesi praktikum, instruktur disarankan memandu refleksi transisi:
1. **Refleksi Keberhasilan**: Mahasiswa telah membuktikan bahwa Backpropagation mampu melatih model visi sortasi TBS hingga akurasi $99.33\%$.
2. **Keterbatasan Vanilla Gradient Descent**:
   * Ajukan pertanyaan kritis: *"Pada formula $\mathbf{W} \leftarrow \mathbf{W} - \eta \nabla_{\mathbf{W}} \mathcal{L}$, laju belajar $\eta$ bernilai seragam dan tetap untuk seluruh parameter."*
   * *"Apa yang terjadi jika suatu bobot berada pada jurang sempit yang curam sedangkan bobot lain berada di dataran landai?"*
   * Bobot pertama akan berosilasi melompat liar, sementara bobot kedua bergerak sangat lambat seperti kura-kura.
3. **Mengantarkan Modul 8.5**: Sampaikan bahwa pada pertemuan berikutnya (**AI Modul 8.5: Optimasi Penurunan Gradien Lanjut**), mahasiswa akan mempelajari bagaimana menambahkan **Momentum fisik** serta algoritma laju belajar adaptif (**RMSprop dan Adam**) yang menjadi optimizer standar emas di seluruh dunia.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
2. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
3. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. [Tersedia di koleksi src/]
4. Griewank, A., & Walther, A. (2008). *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation* (2nd ed.). SIAM.
5. LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. *Proceedings of the IEEE*, 86(11), 2278-2324.
6. Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press.
7. Nielsen, M. A. (2015). *Neural Networks and Deep Learning*. Determination Press.
8. Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*, 323(6088), 533-536.
9. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. [Tersedia di koleksi src/]
