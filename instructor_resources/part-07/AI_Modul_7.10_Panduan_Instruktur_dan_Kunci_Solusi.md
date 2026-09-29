# AI Modul 7.10: Panduan Instruktur & Kunci Solusi
## Gradient Boosting & Algoritma Boosting Modern (XGBoost / LightGBM)

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-10-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Mathematical Gradient Boosting & Taylor Expansion; 70 Menit Praktikum Python GBDT Early Stopping & Feature Importance; 30 Menit Evaluasi Kasus Logistik Panen TBS)
* **Karakteristik Modul**: Ansambel Sekuensial Terarah (*Sequential Boosting Ensemble*), Optimasi Ruang Fungsi (*Functional Gradient Descent*), Penanganan Data Tabular SOTA (*State-of-the-Art Tabular Modeling*)

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Modul 7.10 adalah puncak dari Part 7 (Machine Learning). Pendekatan pedagogis yang disarankan:
1. **Analogi Permainan Golf (*Putting Greens*)**:
   * Ajukan perumpamaan: *"Seorang pemain golf memukul bola pertama kali menuju lubang berjarak 100 meter. Pukulan pertama mendarat di 85 meter (kurang 15 meter). Apakah pada pukulan kedua dia kembali memukul bola dari titik awal 0 meter? Tentu tidak! Dia memukul dari posisi 85 meter dan mengarahkan pukulan kedua hanya untuk menutupi kekurangan 15 meter tersebut."*
   * *Koneksi Algoritma*: Itulah esensi Gradient Boosting! Model pertama memprediksi rata-rata awal ($F_0$). Pohon kedua tidak memprediksi $y$ asli, melainkan memprediksi kekurangan/residu pukulan pertama ($y - F_0$). Pohon ketiga memprediksi sisa residu pukulan kedua, hingga bola tepat masuk ke lubang target dengan galat minimal.
2. **Konteks Spesifik INSTIPER**:
   * Tunjukkan bahwa estimasi hasil panen kelapa sawit adalah fondasi seluruh rantai pasok industri sawit. Ketidaktepatan $\pm 20\%$ mengakibatkan truk antre berhari-hari di pabrik kelapa sawit (PKS) yang memicu lonjakan asam lemak bebas (FFA / Asam Lemak Bebas) dan kerugian miliaran rupiah.
   * Gradient Boosting memberikan akurasi tinggi karena mampu memodelkan relasi biologis yang sangat non-linier (misal kurva parabola umur pohon terhadap hasil buah) serta interaksi kompleks antara defisit air tanah dan pemupukan hara.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Makin banyak pohon ditambahkan pada Gradient Boosting, model akan selalu makin pintar seperti Random Forest."**
  * *Koreksi Instruktur*: Luruskan bahwa pada Random Forest, pohon dilatih secara independen sehingga penambahan pohon mereduksi varians tanpa memicu *overfitting*. Namun pada Gradient Boosting, pohon dilatih sekuensial mengoreksi residu. Jika $M$ terlalu besar tanpa *early stopping*, pohon-pohon terakhir akan mulai menghafal derau lokal dan pencilan data, menyebabkan *overfitting* yang parah.
* **Miskonsepsi 2: "Pohon keputusan pada Gradient Boosting harus dibuat sedalam mungkin agar prediksinya presisi."**
  * *Koreksi Instruktur*: Tekankan bahwa paradigma boosting mewajibkan pembelajar lemah (*weak learners*), yaitu pohon-pohon dangkal (*shallow trees*) dengan `max_depth = 3 - 6`. Pohon dangkal memiliki bias tinggi namun varians sangat rendah; kombinasi sekuensial ratusan pohon dangkallah yang secara bertahap memangkas bias tanpa melipatgandakan varians.
* **Miskonsepsi 3: "Laju pembelajaran (*learning rate*) $\eta$ sebaiknya disetel besar (misal 0.8 atau 1.0) agar model cepat konvergen dan hemat waktu."**
  * *Koreksi Instruktur*: Nilai $\eta$ yang besar menyebabkan model melompati titik minimum global pada ruang fungsi rugi (*overshooting*) dan menciptakan fluktuasi liar. Aturan emas industri adalah: gunakan $\eta$ kecil ($0.01 - 0.05$) dipadukan dengan jumlah pohon yang cukup serta *early stopping*.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual Pseudo-Residuals 1 Putaran Boosting untuk Regresi MSE (C3)
Data 3 sampel hasil panen petak sawit:
* $y_1 = 3.0\text{ Ton/Ha}$
* $y_2 = 2.0\text{ Ton/Ha}$
* $y_3 = 4.0\text{ Ton/Ha}$

Fungsi rugi: $L(y_i, F(\mathbf{x}_i)) = \frac{1}{2}(y_i - F(\mathbf{x}_i))^2$.

#### Langkah 1: Menentukan Model Awal Konstan $F_0(\mathbf{x})$
Untuk fungsi rugi kuadratik (MSE), model awal konstan adalah rata-rata aritmatika dari seluruh nilai target:
$$F_0(\mathbf{x}) = \arg\min_c \sum_{i=1}^{3} \frac{1}{2}(y_i - c)^2 = \bar{y}$$
$$F_0(\mathbf{x}) = \frac{y_1 + y_2 + y_3}{3} = \frac{3.0 + 2.0 + 4.0}{3} = \frac{9.0}{3} = \mathbf{3.0\text{ Ton/Ha}}$$

#### Langkah 2: Menghitung Pseudo-Residuals $r_{i1}$ pada Iterasi Pertama ($m=1$)
Turunan parsial negatif fungsi rugi:
$$r_{i1} = -\left[\frac{\partial L(y_i, F(\mathbf{x}_i))}{\partial F(\mathbf{x}_i)}\right]_{F(\mathbf{x})=F_0(\mathbf{x})} = y_i - F_0(\mathbf{x}_i)$$
* Sampel 1: $r_{11} = 3.0 - 3.0 = \mathbf{0.0\text{ Ton/Ha}}$
* Sampel 2: $r_{21} = 2.0 - 3.0 = \mathbf{-1.0\text{ Ton/Ha}}$
* Sampel 3: $r_{31} = 4.0 - 3.0 = \mathbf{+1.0\text{ Ton/Ha}}$

#### Langkah 3: Menghitung Nilai Output Daun $\gamma_{11}$ dan $\gamma_{21}$
Pohon regresi membagi data menjadi dua region daun:
* Daun Kiri $R_{11} = \{\text{Sampel 1, Sampel 2}\}$:
  $$\gamma_{11} = \frac{r_{11} + r_{21}}{2} = \frac{0.0 + (-1.0)}{2} = \mathbf{-0.5\text{ Ton/Ha}}$$
* Daun Kanan $R_{21} = \{\text{Sampel 3}\}$:
  $$\gamma_{21} = \frac{r_{31}}{1} = \frac{+1.0}{1} = \mathbf{+1.0\text{ Ton/Ha}}$$

#### Langkah 4: Menghitung Prediksi Baru $F_1(\mathbf{x})$ dengan Laju Pembelajaran $\eta = 0.10$
Formula pembaruan model:
$$F_1(\mathbf{x}_i) = F_0(\mathbf{x}_i) + \eta \cdot \gamma_{j1}$$
* Untuk Sampel 1 (masuk Daun Kiri):
  $$F_1(\mathbf{x}_1) = 3.0 + 0.10 \times (-0.5) = 3.0 - 0.05 = \mathbf{2.95\text{ Ton/Ha}}$$
  Residu baru: $e_{11} = y_1 - F_1(\mathbf{x}_1) = 3.0 - 2.95 = \mathbf{+0.05\text{ Ton/Ha}}$ (Sebelumnya $0.0$, deviasi kecil terkendali).
* Untuk Sampel 2 (masuk Daun Kiri):
  $$F_1(\mathbf{x}_2) = 3.0 + 0.10 \times (-0.5) = 3.0 - 0.05 = \mathbf{2.95\text{ Ton/Ha}}$$
  Residu baru: $e_{21} = y_2 - F_1(\mathbf{x}_2) = 2.0 - 2.95 = \mathbf{-0.95\text{ Ton/Ha}}$ (Residu mutlak menyusut dari $1.0$ menjadi $0.95$).
* Untuk Sampel 3 (masuk Daun Kanan):
  $$F_1(\mathbf{x}_3) = 3.0 + 0.10 \times (+1.0) = 3.0 + 0.10 = \mathbf{3.10\text{ Ton/Ha}}$$
  Residu baru: $e_{31} = y_3 - F_1(\mathbf{x}_3) = 4.0 - 3.10 = \mathbf{+0.90\text{ Ton/Ha}}$ (Residu mutlak menyusut dari $1.0$ menjadi $0.90$).

*Evaluasi Jumlah Kuadrat Galat Total (SSE)*:
* Sebelum boosting ($F_0$): $\text{SSE}_0 = 0.0^2 + (-1.0)^2 + 1.0^2 = 0 + 1 + 1 = \mathbf{2.000}$
* Setelah 1 putaran boosting ($F_1$): $\text{SSE}_1 = (0.05)^2 + (-0.95)^2 + (0.90)^2 = 0.0025 + 0.9025 + 0.8100 = \mathbf{1.715}$
* **Kesimpulan Terbukti**: Nilai galat kuadratik total berhasil terpangkas sebesar $14.25\%$ hanya dalam satu iterasi penyesuaian residu.

---

### Soal 2: Komputasi Pseudo-Residuals Log-Loss untuk Klasifikasi Biner (C3)
Fungsi rugi binary cross-entropy:
$$L(y_i, F(\mathbf{x}_i)) = -[y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i)]$$
di mana $p_i = \sigma(F(\mathbf{x}_i)) = \frac{1}{1 + e^{-F(\mathbf{x}_i)}}$.

#### 1. Pembuktian Analitik Penurunan Residu Probabilitas
Gunakan aturan rantai kalkulus (*Chain Rule*):
$$\frac{\partial L}{\partial F} = \frac{\partial L}{\partial p} \cdot \frac{\partial p}{\partial F}$$
Langkah A: Turunan $L$ terhadap $p$:
$$\frac{\partial L}{\partial p} = -\left[\frac{y_i}{p_i} - \frac{1 - y_i}{1 - p_i}\right] = -\left[\frac{y_i(1 - p_i) - p_i(1 - y_i)}{p_i(1 - p_i)}\right] = -\left[\frac{y_i - y_i p_i - p_i + y_i p_i}{p_i(1 - p_i)}\right] = -\frac{y_i - p_i}{p_i(1 - p_i)}$$

Langkah B: Turunan fungsi sigmoid $p$ terhadap logit $F$:
$$\frac{\partial p}{\partial F} = \sigma(F)(1 - \sigma(F)) = p_i(1 - p_i)$$

Langkah C: Kalikan kedua turunan:
$$\frac{\partial L}{\partial F} = \left(-\frac{y_i - p_i}{p_i(1 - p_i)}\right) \cdot \left(p_i(1 - p_i)\right) = -(y_i - p_i)$$

Maka turunan parsial negatif (*pseudo-residual*) adalah:
$$r_{im} = -\frac{\partial L}{\partial F} = -(-(y_i - p_i)) = \mathbf{y_i - p_i} \quad \text{(Terbukti!)}$$

#### 2. Perhitungan Kasus Pohon Terserang Hama ($y = 1$)
Model saat ini menghasilkan nilai $F_{m-1}(\mathbf{x}) = 0.0$.
* Probabilitas prediksi saat ini:
  $$p = \frac{1}{1 + e^{-0.0}} = \frac{1}{1 + 1} = \frac{1}{2} = \mathbf{0.50}$$
* Nilai pseudo-residual yang harus dipelajari oleh pohon berikutnya:
  $$r = y - p = 1.0 - 0.50 = \mathbf{+0.50}$$
* *Makna Matematis*: Residu bernilai positif $+0.50$ menandakan bahwa model saat ini masih meremehkan (*under-predicting*) kemungkinan serangan hama. Pohon berikutnya akan menambahkan nilai koreksi positif untuk menaikkan log-odds $F(\mathbf{x})$ ke arah angka yang lebih tinggi.

---

### Soal 3: Analisis Efek Shrinkage $\eta$, Ekspansi Taylor Orde 2 XGBoost, dan Trade-off Varians-Bias (C4)

#### 1. Keunggulan Nilai Kurvatur Hessian $h_i$ pada Metode Newton-Raphson XGBoost
* Gradient Boosting klasik (Friedman, 2001) hanya menggunakan gradien orde satu $g_i$, yang setara dengan metode optimasi *Gradient Descent* sederhana. Metode ini mengasumsikan permukaan fungsi rugi berupa bidang miring linier konstan, sehingga panjang langkah penyesuaian (*step size*) harus dibuat seragam dan sangat lambat untuk mencegah osilasi.
* XGBoost (Chen & Guestrin, 2016) menggunakan ekspansi Taylor orde 2 yang menyertakan suku Hessian $h_i = \frac{\partial^2 L}{\partial F^2}$, setara dengan metode optimasi **Newton-Raphson**. Hessian mengukur kelengkungan (*curvature*) permukaan rugi:
  * Jika kurvatur sangat terjal ($h_i$ besar), model secara otomatis mengambil langkah kecil yang hati-hati.
  * Jika permukaan datar ($h_i$ kecil), model berani mengambil langkah lompatan besar.
  Hal ini menghasilkan konvergensi yang jauh lebih cepat, stabil, dan presisi.

#### 2. Peran Parameter Penalti Daun $\lambda$ pada Formula Bobot Daun XGBoost
Formula bobot daun optimal XGBoost:
$$w_j^* = -\frac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda}$$
* Parameter $\lambda > 0$ bertindak sebagai penalti regularisasi L2 (*ridge penalty*).
* Jika sebuah daun hanya berisi sedikit sampel derau atau pencilan, nilai Hessian kumulatif $\sum h_i$ akan sangat kecil mendekati nol. Tanpa $\lambda$, pembagian dengan bilangan sangat kecil akan menghasilkan bobot daun $w_j^*$ yang meledak tak berhingga (*extreme weight explosion*), memorak-porandakan stabilitas model.
* Hadirnya $\lambda$ di penyebut menjinakkan nilai $w_j^*$, menyusutkannya mendekati nol (*shrinkage towards zero*), sehingga daun-daun pencilan yang tidak representatif dinetralisir secara otomatis.

#### 3. Tabel Perbandingan Komprehensif Random Forest (Bagging) vs Gradient Boosting (Boosting)

| Dimensi Evaluasi Komparatif | Random Forest (Bagging) | Gradient Boosting (Boosting) |
|:---|:---|:---|
| **Tujuan Utama Reduksi Galat** | **Mereduksi Varians** (Menstabilkan pohon-pohon yang terlalu fluktuatif) | **Mereduksi Bias** (Membangun model kuat dari pohon-pohon lemah) |
| **Sifat Pelatihan Pohon** | **Paralel & Independen** (Pohon $m$ tidak peduli hasil pohon $m-1$) | **Sekuensial Terarah** (Pohon $m$ secara khusus mengoreksi galat pohon $m-1$) |
| **Kedalaman Pohon Optimal (*Tree Depth*)** | **Pohon Sangat Dalam** (`max_depth = None` atau besar, daun murni) | **Pohon Sangat Dangkal** (`max_depth = 3 - 6`, pembelajar lemah) |
| **Risiko Overfitting terhadap Pohon ($M$)** | **Sangat Rendah / Kebal** (Menambah $M$ ribuan pohon tidak membuat overfit) | **Tinggi jika Tanpa Kontrol** (Wajib menggunakan *early stopping* & laju $\eta$ kecil) |
| **Sensitivitas terhadap Pencilan (*Outliers*)** | **Sangat Kebal** (Pencilan diredam oleh suara mayoritas voting pohon lain) | **Cukup Sensitif** (Pencilan menghasilkan residu besar yang dikejar pohon berikutnya) |
| **Kebutuhan Waktu Pelatihan Komputasi** | Cepat melalui paralelisasi multi-core CPU (`n_jobs=-1`) | Membutuhkan waktu sekuensial (dimitigasi oleh LightGBM / histogram XGBoost) |

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Efek Penyetelan Hyperparameter Learning Rate
* **Laju Belajar Terlalu Tinggi ($\eta = 0.50$)**: Kurva galat validasi menunjukkan osilasi tajam dan mengalami *overfitting* dini pada iterasi ke-25, menghasilkan RMSE validasi yang relatif buruk ($0.218\text{ Ton/Ha}$).
* **Laju Belajar Terlalu Rendah ($\eta = 0.005$)**: Model bergerak sangat lambat (*underfitting*), membutuhkan lebih dari 1000 iterasi untuk mencapai titik konvergen yang membuang waktu komputasi.
* **Laju Belajar Optimal ($\eta = 0.05$)**: Menghasilkan kurva penurunan penurunan gradien yang mulus, stabil, dan mencapai RMSE validasi terendah ($0.152\text{ Ton/Ha}$) pada iterasi ke-103 dengan *early stopping*.

### 4.2 Analisis Variabel Penentu Produksi (*Feature Importance*)
Berdasarkan metrik MDI/Gain:
1. `Umur_Tegakan_Thn` mendominasi dengan kontribusi **$\approx 58.96\%$**, mencerminkan dinamika kurva biologis fisiologi pohon sawit yang mencapai puncak pada umur prima (9-14 tahun).
2. `Defisit_Air_Kumulatif` menduduki posisi kedua (**$\approx 19.69\%$**), menegaskan sensitivitas kelapa sawit terhadap cekaman kekeringan (*water stress*) yang menghambat pembentukan bunga betina.
3. `Curah_Hujan_Bln_Lalu` menyumbang **$\approx 17.11\%$**, menjadi faktor pemicu pembesaran tandan buah.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Formulasi Matematis Residu & Optimasi Ruang Fungsi | 25% | Mampu menguraikan penurunan analitik pseudo-residuals, konsep functional gradient descent, dan peran ekspansi Taylor orde 2. |
| **C3 (Penerapan)** | Implementasi GBDT, Early Stopping & Penjadwalan Panen | 35% | Mampu menyusun pipeline scikit-learn GBDT, mengonfigurasi `validation_fraction` dan `n_iter_no_change`, serta menghitung kebutuhan logistik armada truk. |
| **C4 (Analisis)** | Analisis Komparasi Bagging-Boosting & Optimasi Laju Belajar | 40% | Mampu membedah trade-off varians-bias antara RF dan GBDT, mengevaluasi kurva shrinkage, serta menganalisis pergeseran paradigma menuju Deep Learning. |

---

## 6. Jembatan Pedagogis ke Part 8: Deep Learning & Jaringan Saraf Tiruan

Sebagai penutup resmi **Part 7: Algoritma Machine Learning**, instruktur diharapkan memimpin refleksi transisi kurikulum:
1. **Pencapaian Mahasiswa**: Tegaskan bahwa mahasiswa kini telah menguasai portofolio algoritma pembelajaran mesin tabular terlengkap di Indonesia, mulai dari regresi sederhana hingga algoritma boosting kelas dunia pemenang kompetisi Kaggle.
2. **Keterbatasan Paradigma Tabular (*Handcrafted Features*)**:
   * Jelaskan bahwa semua algoritma Part 7 membutuhkan tabel fitur yang telah diolah oleh manusia.
   * Ajukan tantangan baru: *"Bagaimana jika komputer perkebunan dihadapkan pada rekaman video drone 4K berisi jutaan pohon tanpa ada tabel angka? Bagaimana komputer dapat mengenali bercak jamur daun secara mandiri?"*
3. **Mengantarkan Gerbang Part 8**: Sambut mahasiswa memasuki era revolusioner **Deep Learning**:
   * Kita tidak lagi mendefinisikan fitur secara manual; jaringan saraf tiruan dalam (*Deep Neural Networks*) akan belajar mengekstraksi hierarki representasi visual langsung dari piksel mentah.
   * Modul 8.1 akan memulai petualangan ini dari unit terkecil kecerdasan komputasi modern: **Neuron Buatan & Perceptron**.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
2. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785-794.
3. Friedman, J. H. (2001). Greedy function approximation: a gradient boosting machine. *Annals of Statistics*, 29(5), 1189-1232.
4. Friedman, J. H. (2002). Stochastic gradient boosting. *Computational Statistics & Data Analysis*, 38(4), 367-378.
5. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
6. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
7. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
8. Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T. Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems*, 30, 3146-3154.
