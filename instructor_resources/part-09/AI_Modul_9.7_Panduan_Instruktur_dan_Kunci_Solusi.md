# AI Modul 9.7: Panduan Instruktur & Kunci Solusi
## Optimasi Penurunan Gradien Lanjut (SGD, Momentum, RMSprop, Adam)

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-09-07-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Dinamika Fisika Optimasi & Formulasi Adam; 70 Menit Praktikum Python Trajektori 2D & Peramalan Defisit Air Sawit; 30 Menit Evaluasi Kasus Penjadwalan Laju Belajar)
* **Karakteristik Modul**: Algoritma Optimasi Non-Konveks Orde Pertama, Koreksi Bias Eksponensial, Penjadwalan Siklik & Cosine Annealing

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Modul 9.7 melatih mahasiswa memahami bagaimana algoritma kecerdasan buatan bermanuver menuruni lanskap perbukitan fungsi rugi yang terjal. Pendekatan pengajaran yang disarankan:
1. **Analogi Bola Salju Bermassa dan Rem Hidrolik Otomatis**:
   * *SGD Biasa*: Seperti seorang pendaki yang berjalan dengan mata tertutup; di setiap langkah dia hanya meraba kemiringan tanah tepat di bawah telapak kakinya. Jika berada di jurang terjal, dia akan melangkah bolak-balik zig-zag tanpa maju ke depan.
   * *Momentum*: Seperti bola salju pejal yang menggelinding. Bola memiliki massa (inersia); gerakan melompat ke kiri-kanan akan diredam oleh beratnya sendiri, sementara dorongan ke arah bawah lembah akan berakumulasi membuat bola meluncur semakin kencang.
   * *RMSprop*: Seperti kendaraan dengan rem hidrolik cerdas pada setiap rodanya. Jika roda vertikal meluncur terlalu curam, rem otomatis menekan agar tidak terbalik. Roda horizontal yang landai diberi gas ekstra agar cepat sampai ke tujuan.
   * *Adam*: Menggabungkan bola salju Momentum dan rem hidrolik RMSprop menjadi kendaraan penjelajah lembah yang cepat, mulus, dan tangguh di segala medan!
2. **Konteks Spesifik INSTIPER**:
   * Tunjukkan bahwa data agro-klimat perkebunan kelapa sawit memiliki korelasi silang yang sangat kuat (misalnya hubungan antara suhu tinggi, defisit air, dan radiasi matahari).
   * Korelasi silang ini menciptakan lanskap fungsi rugi berbentuk elips sangat lonjong (*elongated ravines*). Penggunaan SGD biasa membutuhkan ribuan epoch yang boros listrik server kebun, sedangkan Adam mampu mencapai konvergensi optimal dalam waktu singkat.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Adam selalu menghasilkan akurasi data uji yang lebih tinggi daripada SGD."**
  * *Koreksi Instruktur*: Luruskan bahwa Adam **unggul mutlak dalam kecepatan konvergensi awal**, namun pada beberapa kasus klasifikasi citra kompleks (seperti dataset citra daun drone), SGD dengan momentum yang dipadukan dengan penjadwalan laju belajar teliti sering kali mampu menemukan cekungan minimum yang sedikit lebih datar (*flatter minima*), menghasilkan generalisasi akhir yang sedikit lebih unggul.
* **Miskonsepsi 2: "Jika menggunakan Adam, kita tidak perlu lagi mengatur laju pembelajaran $\eta$."**
  * *Koreksi Instruktur*: Nilai $\eta = 0.001$ hanyalah nilai awal *default* yang baik. Pada dataset atau arsitektur tertentu, laju ini masih bisa terlalu besar atau terlalu kecil. Penyetelan $\eta$ dan penerapan *learning rate schedule* (seperti *Cosine Annealing*) tetap mutlak dibutuhkan untuk mendapatkan performa state-of-the-art.
* **Miskonsepsi 3: "Koreksi bias pada Adam hanyalah formalitas matematika yang tidak berdampak praktis."**
  * *Koreksi Instruktur*: Tunjukkan bahwa tanpa pembagian $(1 - \beta^t)$, pada langkah pertama $t=1$, nilai momen kedua adalah $\mathbf{v}_1 = 0.001 \mathbf{g}_1^2$. Saat dibagi $\sqrt{\mathbf{v}_1} = 0.0316 |\mathbf{g}_1|$, ukuran langkah akan terdistorsi secara liar pada awal pelatihan. Koreksi bias menjamin bahwa langkah pertama tetap proporsional terhadap gradien sejati.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual Komputasi Dua Langkah Iterasi Optimizer Adam (C3)
Parameter awal: $\theta_0 = 2.0$.
Hiperparameter: $\eta = 0.1$, $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$.
Kondisi awal: $m_0 = 0.0, v_0 = 0.0$.

#### Iterasi 1 ($t = 1$), Gradien $g_1 = 0.40$:
1. **Pembaruan Momen Pertama ($m_1$)**:
   $$m_1 = \beta_1 m_0 + (1 - \beta_1) g_1 = (0.9)(0.0) + (0.1)(0.40) = \mathbf{0.0400}$$
2. **Pembaruan Momen Kedua ($v_1$)**:
   $$v_1 = \beta_2 v_0 + (1 - \beta_2) g_1^2 = (0.999)(0.0) + (0.001)(0.40^2) = 0.001 \times 0.16 = \mathbf{0.000160}$$
3. **Koreksi Bias Momen Pertama ($\hat{m}_1$)**:
   $$\hat{m}_1 = \frac{m_1}{1 - \beta_1^1} = \frac{0.0400}{1 - 0.9} = \frac{0.0400}{0.10} = \mathbf{0.4000}$$
4. **Koreksi Bias Momen Kedua ($\hat{v}_1$)**:
   $$\hat{v}_1 = \frac{v_1}{1 - \beta_2^1} = \frac{0.000160}{1 - 0.999} = \frac{0.000160}{0.001} = \mathbf{0.1600}$$
5. **Pembaruan Parameter ($\theta_1$)**:
   $$\Delta \theta_1 = \frac{\eta}{\sqrt{\hat{v}_1} + \epsilon} \hat{m}_1 = \frac{0.1}{\sqrt{0.1600} + 10^{-8}} \times 0.4000 = \frac{0.1}{0.40} \times 0.4000 = 0.25 \times 0.4000 = \mathbf{0.1000}$$
   $$\theta_1 = \theta_0 - \Delta \theta_1 = 2.0 - 0.1000 = \mathbf{1.9000}$$

---

#### Iterasi 2 ($t = 2$), Gradien $g_2 = 0.20$:
1. **Pembaruan Momen Pertama ($m_2$)**:
   $$m_2 = \beta_1 m_1 + (1 - \beta_1) g_2 = (0.9)(0.0400) + (0.1)(0.20) = 0.0360 + 0.0200 = \mathbf{0.0560}$$
2. **Pembaruan Momen Kedua ($v_2$)**:
   $$v_2 = \beta_2 v_1 + (1 - \beta_2) g_2^2 = (0.999)(0.000160) + (0.001)(0.20^2) = 0.00015984 + 0.000040 = \mathbf{0.00019984}$$
3. **Koreksi Bias Momen Pertama ($\hat{m}_2$)**:
   $$\hat{m}_2 = \frac{m_2}{1 - \beta_1^2} = \frac{0.0560}{1 - 0.81} = \frac{0.0560}{0.19} \approx \mathbf{0.2947}$$
4. **Koreksi Bias Momen Kedua ($\hat{v}_2$)**:
   $$\hat{v}_2 = \frac{v_2}{1 - \beta_2^2} = \frac{0.00019984}{1 - 0.998001} = \frac{0.00019984}{0.001999} \approx \mathbf{0.09997}$$
5. **Pembaruan Parameter ($\theta_2$)**:
   $$\sqrt{\hat{v}_2} = \sqrt{0.09997} \approx 0.3162$$
   $$\Delta \theta_2 = \frac{0.1}{0.3162 + 10^{-8}} \times 0.2947 = 0.31625 \times 0.2947 \approx \mathbf{0.0932}$$
   $$\theta_2 = \theta_1 - \Delta \theta_2 = 1.9000 - 0.0932 = \mathbf{1.8068}$$

---

### Soal 2: Analisis Matematis Mengapa Adam Berpotensi Gagal Konvergen Jika $\beta_2 < \beta_1$ (C4)

#### 1. Peran Suku Pembagi $\sqrt{\hat{\mathbf{v}}_t}$ sebagai Matriks Prakondisi
* Pada Adam, ukuran langkah efektif untuk suatu parameter adalah $\alpha_t = \frac{\eta}{\sqrt{\hat{v}_t}}$.
* Suku $\sqrt{\hat{v}_t}$ membatasi dan menormalkan langkah pembaruan. Jika sebuah gradien besar muncul (misalnya akibat sampel pencilan atau anomali sensorik), $\hat{v}_t$ melonjak, sehingga ukuran langkah berikutnya secara otomatis menyusut drastis untuk mencegah model terlempar keluar dari zona stabil.
* Namun, jika $\beta_2$ bernilai kecil (atau lebih kecil dari $\beta_1$), memori kuadrat gradien $\mathbf{v}_t$ akan meluruh sangat cepat. Begitu gradien kembali kecil, nilai $\sqrt{\hat{v}_t}$ langsung anjlok, menyebabkan ukuran langkah efektif $\frac{\eta}{\sqrt{\hat{v}_t}}$ meledak membesar secara prematur.

#### 2. Solusi AMSGrad (Reddi et al., 2018)
* Untuk menjamin konvergensi matematis pada sembarang lanskap, algoritma AMSGrad mempertahankan memori maksimum dari seluruh nilai momen kedua historis:
  $$\hat{\mathbf{v}}_t = \max\left(\hat{\mathbf{v}}_{t-1}, \mathbf{v}_t\right)$$
* Dengan operator $\max$, nilai penyebut dijamin monotonik tidak pernah mengecil ($\hat{\mathbf{v}}_t \geq \hat{\mathbf{v}}_{t-1}$), memastikan bahwa ukuran langkah efektif $\alpha_t$ bersifat non-menaik, melenyapkan risiko lonjakan langkah destruktif di akhir pelatihan.

---

### Soal 3: Desain Komparatif Penjadwalan Cosine Annealing vs Step Decay (C4)
Parameter: $T_{\max} = 120\text{ epoch}$, $\eta_0 = 0.04$, $\eta_{\min} = 0.0001$.

#### 1. Perhitungan Laju Pembelajaran Cosine Annealing
Formula:
$$\eta_t = \eta_{\min} + \frac{1}{2}(\eta_0 - \eta_{\min})\left(1 + \cos\left(\frac{t}{T_{\max}} \pi\right)\right)$$
Amplitudo: $\frac{1}{2}(0.04 - 0.0001) = \frac{0.0399}{2} = 0.01995$.

* **Pada Epoch ke-30 ($t = 30$)**:
  $$\frac{t}{T_{\max}} \pi = \frac{30}{120} \pi = \frac{\pi}{4} = 45^\circ \implies \cos\left(45^\circ\right) = \frac{\sqrt{2}}{2} \approx 0.7071$$
  $$\eta_{30} = 0.0001 + 0.01995(1 + 0.7071) = 0.0001 + 0.01995(1.7071) = 0.0001 + 0.03406 = \mathbf{0.03416}$$

* **Pada Epoch ke-60 ($t = 60$)**:
  $$\frac{t}{T_{\max}} \pi = \frac{60}{120} \pi = \frac{\pi}{2} = 90^\circ \implies \cos\left(90^\circ\right) = 0.0$$
  $$\eta_{60} = 0.0001 + 0.01995(1 + 0.0) = 0.0001 + 0.01995 = \mathbf{0.02005}$$

* **Pada Epoch ke-90 ($t = 90$)**:
  $$\frac{t}{T_{\max}} \pi = \frac{90}{120} \pi = \frac{3\pi}{4} = 135^\circ \implies \cos\left(135^\circ\right) = -\frac{\sqrt{2}}{2} \approx -0.7071$$
  $$\eta_{90} = 0.0001 + 0.01995(1 - 0.7071) = 0.0001 + 0.01995(0.2929) = 0.0001 + 0.00584 = \mathbf{0.00594}$$

#### 2. Perbandingan dengan Step Decay (Potong 50% per 30 Epoch)
* Epoch $0 - 29$: $\eta = 0.0400$
* Epoch $30 - 59$: $\eta = 0.0200$
* Epoch $60 - 89$: $\eta = 0.0100$
* Epoch $90 - 119$: $\eta = 0.0050$

#### 3. Analisis Keunggulan Fisis Cosine Annealing
* Step Decay memotong laju secara diskrit mendadak (*sudden shock*), yang dapat menyebabkan gradien terlempar keluar dari lintasan penyesuaian optimal.
* *Cosine Annealing* meluruh secara kontinu mulus. Pada awal pelatihan, laju belajar tinggi memungkinkan model melompati lembah-lembah sempit lokal yang buruk (*sharp minima*). Seiring penurunan kosinus yang melandai halus di akhir pelatihan, model mengendap secara stabil pada dasar cekungan yang lebar (*flat minima*), yang menurut literatur modern menghasilkan generalisasi data uji yang jauh lebih kokoh terhadap derau lapangan.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Perbandingan Kinerja Optimizer pada Model Defisit Air
Berdasarkan hasil pengujian empiris selama 60 epoch:
* **RMSprop & Adam**: Mencapai konvergensi tercepat hanya dalam 15–20 epoch, menghasilkan loss terendah ($< 0.004$) dan skor determinasi $R^2 > 0.988$.
* **Momentum**: Menghasilkan kurva yang lebih halus dibandingkan SGD murni dan berhasil meredam osilasi sumbu curam, mencapai $R^2 \approx 0.991$.
* **SGD Murni**: Menunjukkan kurva penurunan yang paling lambat dan berfluktuasi tajam akibat topologi jurang elips data sensor.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Teori Momen Fisik & Dinamika Laju Adaptif | 25% | Mampu menguraikan peran inersia Momentum, formula penyekalaan RMSprop, dan mekanisme koreksi bias Adam. |
| **C3 (Penerapan)** | Perhitungan Manual Dua Langkah & Implementasi Modular | 35% | Mampu menghitung secara presisi parameter $\theta$ pada iterasi 1 & 2 Adam, serta membangun kelas optimizer Python mandiri. |
| **C4 (Analisis)** | Evaluasi Lanskap Jurang & Penjadwalan Cosine Annealing | 40% | Mampu membedah trajektori elips 2D, membuktikan batas konvergensi AMSGrad, dan menghitung jadwal Cosine Annealing. |

---

## 6. Jembatan Pedagogis ke AI Modul 8.6 (Regularisasi & Generalisasi)

Di akhir sesi praktikum, instruktur disarankan memimpin perenungan penutup:
1. **Refleksi Pencapaian**: Mahasiswa kini telah menguasai optimizer paling perkasa di dunia (Adam) yang mampu melatih jaringan dengan kecepatan kilat.
2. **Munculnya Ancaman Baru**:
   * Ajukan fenomena riil: *"Model kita sekarang mampu belajar sangat cepat hingga galat data latih mendekati 0.0001 (Loss Latih = 0)."*
   * *"Namun saat model ini dipasang pada drone kebun minggu depan, mengapa akurasinya tiba-tiba jeblok menjadi 65%?"*
3. **Mengantarkan Modul Pamungkas 8.6**: Sambut mahasiswa menuju pertemuan penutup Part 8 (**AI Modul 8.6: Regularisasi & Generalisasi Deep Learning**), di mana kita akan mempelajari bagaimana menjinakkan model agar tidak mengalami *Overfitting* menggunakan teknik **Dropout, L2 Weight Decay, Batch Normalization, dan Early Stopping**.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
2. Duchi, J., Hazan, E., & Singer, Y. (2011). Adaptive subgradient methods for online learning and stochastic optimization. *Journal of Machine Learning Research*, 12(Jul), 2121-2159.
3. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
4. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. [Tersedia di koleksi src/]
5. Hinton, G. (2012). *Neural Networks for Machine Learning*. Coursera Lecture 6e.
6. Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*.
7. Loshchilov, I., & Hutter, F. (2016). SGDR: Stochastic gradient descent with warm restarts. *arXiv preprint arXiv:1608.03983*.
8. Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*, 4(5), 1-17.
9. Reddi, S. J., Kale, S., & Kumar, S. (2018). On the convergence of Adam and beyond. *International Conference on Learning Representations (ICLR)*.
10. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. [Tersedia di koleksi src/]
