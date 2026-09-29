# AI Modul 7.1: Panduan Instruktur & Kunci Solusi
## Linear Regression

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-01-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Pemaparan Teori & Pembuktian, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi & Diskusi HOTS)
* **Karakteristik Modul**: Algoritma Supervised Learning Klasik, Analisis Parametrik, Pertanian Presisi (Kelapa Sawit)

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Regresi linier adalah pintu gerbang mahasiswa menuju ranah *Machine Learning*. Sangat penting bagi instruktur untuk menanamkan pemahaman bahwa regresi linier bukan sekadar rumus garis $y = mx + c$, melainkan sebuah model probabilistik yang mengasumsikan distribusi galat dan memiliki konsekuensi inferensial yang kuat.

1. **Jembatan Konseptual**: Mulai dari konsep aljabar elementer (garis lurus 2D), perluas ke aljabar linier matriks ($n$ observasi, $p$ dimensi), lalu sambungkan ke kalkulus optimasi (Gradient Descent).
2. **Konteks Spesifik INSTIPER**: Hubungkan variabel-variabel matematika dengan realitas lapangan kelapa sawit:
   * Mengapa hubungan curah hujan dan panen sawit memiliki jeda waktu (*time lag*) fisiologis 12–24 bulan?
   * Mengapa defisit air menekan produksi TBS secara linier negatif?
   * Mengapa pupuk NPK menunjukkan respon linier pada rentang dosis moderat tetapi akan mendatar (hukum hasil yang semakin menurun / *Law of Diminishing Returns*) pada dosis ekstrem?

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "$R^2$ yang tinggi (misal 0.98) selalu membuktikan bahwa model tersebut sempurna."**
  * *Koreksi Instruktur*: Tunjukkan bahwa $R^2$ tinggi bisa disebabkan oleh multikolinearitas parah atau *overfitting*, atau karena memasukkan variabel target versi lag. Sebaliknya, pada data agronomi biologis terbuka, $R^2 \approx 0.65 - 0.75$ sudah sangat bagus karena pengaruh faktor alam tak terkendali.
* **Miskonsepsi 2: "Koefisien $\beta_j$ bertanda negatif membuktikan bahwa faktor tersebut merusak tanaman."**
  * *Koreksi Instruktur*: Jika terjadi multikolinearitas antar variabel pupuk (misal Urea dan NPK), koefisien bisa terbalik tandanya secara artifisial akibat korelasi antar fitur, bukan karena sifat biologis pupuk.
* **Miskonsepsi 3: "Gradient Descent dan OLS menghasilkan model yang berbeda."**
  * *Koreksi Instruktur*: Jika fungsi rugi cembung murni (*strictly convex*) seperti MSE pada regresi linier, Gradient Descent akan konvergen ke titik minimum global yang sama persis dengan solusi analitik Persamaan Normal OLS.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Analisis Komputasi OLS Manual (C3)
Diberikan 5 titik observasi dosis pupuk hayati ($x$) dan peningkatan panen TBS ($y$):
* $(x_1, y_1) = (2, 4)$
* $(x_2, y_2) = (4, 7)$
* $(x_3, y_3) = (6, 9)$
* $(x_4, y_4) = (8, 12)$
* $(x_5, y_5) = (10, 13)$

#### Langkah 1: Menghitung Rerata Sampel ($\bar{x}$ dan $\bar{y}$)
$$\bar{x} = \frac{2 + 4 + 6 + 8 + 10}{5} = \frac{30}{5} = 6.0$$
$$\bar{y} = \frac{4 + 7 + 9 + 12 + 13}{5} = \frac{45}{5} = 9.0$$

#### Langkah 2: Menyusun Tabel Deviasi dan Perkalian Silang
| $i$ | $x_i$ | $y_i$ | $(x_i - \bar{x})$ | $(y_i - \bar{y})$ | $(x_i - \bar{x})^2$ | $(x_i - \bar{x})(y_i - \bar{y})$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 2 | 4 | -4 | -5 | 16 | 20 |
| 2 | 4 | 7 | -2 | -2 | 4 | 4 |
| 3 | 6 | 9 | 0 | 0 | 0 | 0 |
| 4 | 8 | 12 | +2 | +3 | 4 | 6 |
| 5 | 10 | 13 | +4 | +4 | 16 | 16 |
| **Total** | **30** | **45** | **0** | **0** | **40** | **46** |

#### Langkah 3: Menghitung Kovarians dan Varians Sampel
$$\text{Cov}(x, y) = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{n - 1} = \frac{46}{4} = 11.5$$
$$\text{Var}(x) = \frac{\sum (x_i - \bar{x})^2}{n - 1} = \frac{40}{4} = 10.0$$

#### Langkah 4: Menghitung Estimator Parameter OLS ($\hat{\beta}_1$ dan $\hat{\beta}_0$)
$$\hat{\beta}_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = \frac{46}{40} = 1.15$$
$$\hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x} = 9.0 - (1.15 \times 6.0) = 9.0 - 6.9 = 2.10$$

Persamaan garis regresi OLS empiris:
$$\hat{y} = 2.10 + 1.15x$$

#### Langkah 5: Prediksi Nilai untuk $x = 7$ Liter/Ha
$$\hat{y}(7) = 2.10 + 1.15(7) = 2.10 + 8.05 = 10.15 \text{ Ton/Ha}$$

---

### Soal 2: Evaluasi Diagnostik Multikolinearitas & VIF (C4)
* **Kondisi**: $R_1^2 = 0.95$ saat $X_1$ diregresikan pada $X_2$ dan $X_3$.
* **Perhitungan Nilai $\text{VIF}_1$**:
  $$\text{VIF}_1 = \frac{1}{1 - R_1^2} = \frac{1}{1 - 0.95} = \frac{1}{0.05} = 20.0$$
* **Konsekuensi Matematis**:
  Varians dari penaksir koefisien regresi dirumuskan sebagai:
  $$\text{Var}(\hat{\beta}_1) = \frac{\sigma^2}{\sum (x_{i1} - \bar{x}_1)^2} \times \text{VIF}_1$$
  Dengan $\text{VIF}_1 = 20.0$, varians taksiran membengkak sebesar 20 kali lipat dibanding kondisi ortogonal, dan standar eror koefisien membengkak sebesar $\sqrt{20} \approx 4.47$ kali lipat. Akibatnya, nilai statistik $t = \frac{\hat{\beta}_1}{\text{SE}(\hat{\beta}_1)}$ mengecil drastis, menyebabkan variabel $X_1$ menjadi tidak signifikan secara statistik (gagal tolak $H_0$) meskipun sebenarnya memiliki pengaruh fisik yang nyata di lapangan.
* **Langkah Rekayasa Perbaikan**:
  1. *Eliminasi Fitur*: Menggugurkan salah satu variabel yang redundan (misalnya membuang $X_2$ jika $X_1$ lebih mudah dan murah diukur sensor pabrik).
  2. *Regularisasi*: Menerapkan *Ridge Regression* ($L_2$ regularization) yang menambahkan penalti $\lambda \|\boldsymbol{\beta}\|_2^2$ untuk menstabilkan pembalikan matriks $\mathbf{X}^T \mathbf{X} + \lambda \mathbf{I}$.
  3. *Transformasi Fitur*: Menggabungkan variabel berkorelasi menjadi variabel komposit tunggal (misal rasio atau indeks termodinamika entalpi uap).

---

### Soal 3: Studi Kasus Patologi Heteroskedastisitas (C4)
* **Asumsi yang Dilanggar**: Asumsi Homoskedastisitas ($\text{Var}(\epsilon_i \mid \mathbf{X}) = \sigma^2$). Terjadi **Heteroskedastisitas** di mana varians galat membesar proporsional terhadap ukuran prediksi ($\text{Var}(\epsilon_i \mid \mathbf{X}) = \sigma_i^2$).
* **Status Sifat Estimator OLS**:
  Estimator $\hat{\boldsymbol{\beta}}$ **tetap tak bias (*unbiased*)** karena pembuktian sifat tak bias $E[\hat{\boldsymbol{\beta}}] = \boldsymbol{\beta}$ hanya bergantung pada asumsi eksogenitas murni $E[\boldsymbol{\epsilon} \mid \mathbf{X}] = \mathbf{0}$, bukan pada homoskedastisitas. Namun, estimator tersebut **kehilangan predikat "BLUE"** karena tidak lagi memiliki varians minimum di antara seluruh estimator linier yang ada. Standar eror yang dihitung rumus OLS standar menjadi bias, sehingga interval keyakinan dan uji hipotesis (uji t dan uji F) menjadi menyesatkan (*misleading*).
* **Dua Strategi Pemulihan**:
  1. *Transformasi Penstabil Ragam*: Menerapkan transformasi logaritma natural pada variabel target: $\ln(y_i) = \beta_0 + \sum \beta_j x_{ij} + \epsilon_i$, yang secara matematis meredam skala varians pada nilai-nilai besar.
  2. *Weighted Least Squares (WLS)*: Memberikan bobot pembobot $w_i = \frac{1}{\sigma_i^2}$ pada setiap baris observasi, sehingga sampel dengan varians galat besar diberi bobot pengaruh yang lebih kecil dalam fungsi minimasi kuadrat.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Simulasi Skenario Panen Blok Baru
Menggunakan model yang telah dilatih pada notebook:
$$\hat{y} = \beta_0 + \beta_1(2200) + \beta_2(7.5) + \beta_3(6.2) - \beta_4(15.0)$$
Kode solusi:
```python
sample_baru = pd.DataFrame([{
    'Curah_Hujan_mm': 2200.0,
    'Pupuk_NPK_kg': 7.5,
    'Radiasi_Jam': 6.2,
    'Defisit_Air_mm': 15.0
}])
hasil_prediksi = model_sk.predict(sample_baru)[0]
print(f"Prediksi Hasil Panen TBS: {hasil_prediksi:.2f} Ton/Ha/Tahun")
```
Nilai estimasi yang diharapkan berada pada rentang **29.5 – 31.8 Ton/Ha/Tahun**.

### 4.2 Simulasi Injeksi Multikolinearitas Buatan
Kode solusi:
```python
df_sim = df_sawit.copy()
# Injeksi fitur berkorelasi 0.98
df_sim['Pupuk_Urea_kg'] = df_sim['Pupuk_NPK_kg'] * 0.6 + np.random.normal(0, 0.08, len(df_sim))

X_sim = df_sim[['Curah_Hujan_mm', 'Pupuk_NPK_kg', 'Pupuk_Urea_kg', 'Radiasi_Jam', 'Defisit_Air_mm']]
X_sim_const = X_sim.copy()
X_sim_const.insert(0, 'Konstanta', 1.0)

vif_sim = [variance_inflation_factor(X_sim_const.values, i) for i in range(1, X_sim_const.shape[1])]
for col, v in zip(X_sim.columns, vif_sim):
    print(f"VIF {col:<15}: {v:.2f}")
```
*Hasil yang diharapkan*: Nilai VIF untuk `Pupuk_NPK_kg` dan `Pupuk_Urea_kg` akan melonjak melebihi **25 – 40**, memperagakan fenomena kolinearitas ekstrem secara visual kepada mahasiswa.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Pemahaman Teoretis OLS & Asumsi Gauss-Markov | 25% | Mampu menjelaskan secara lisan/tulisan prinsip minimasi SSR, perbedaan OLS vs Gradient Descent, serta konsekuensi heteroskedastisitas dan multikolinearitas. |
| **C3 (Penerapan)** | Implementasi Kode & Ketepatan Komputasi | 35% | Mampu menyusun kode Python NumPy OLS manual dan Scikit-Learn dengan hasil identik (0 galat), serta menghasilkan metrik evaluasi MAE, RMSE, dan $R^2$ yang akurat. |
| **C4 (Analisis)** | Diagnostik Residual & Interpretasi Masalah Lapangan | 40% | Mampu membaca 4 grafik diagnostik residual, menginterpretasikan nilai VIF, mendeteksi titik pengungkit *Cook's Distance*, dan merumuskan rekomendasi agronomi berbasis koefisien model. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.2 (Logistic Regression)

Pada akhir sesi kelas praktikum Modul 7.1, instruktur disarankan untuk memfasilitasi transisi pemikiran reflektif (*reflective bridging*) mahasiswa melalui langkah-langkah berikut:
1. **Mengajukan Provokasi Kasus Lapangan**: "Jika hari ini kita berhasil memprediksi bobot ton TBS menggunakan regresi linier, bagaimana jika besok manajer PKS meminta kita mendeteksi apakah suatu truk TBS berstatus *Layak Olah* ($y=1$) atau *Afkir/Busuk* ($y=0$)?"
2. **Menunjukkan Kebuntuan Regresi Linier**: Minta salah satu mahasiswa mencoba memasukkan nilai biner $\{0, 1\}$ ke dalam persamaan garis lurus. Tunjukkan secara visual bahwa garis lurus akan menembus angka di bawah 0 dan di atas 1, membuktikan bahwa regresi linier tidak mampu membatasi nilai peluang ke dalam rentang tertutup $[0, 1]$.
3. **Mengantarkan Solusi Modul 7.2**: Jelaskan bahwa pada pertemuan berikutnya (**AI Modul 7.2: Logistic Regression**), mahasiswa akan mempelajari bagaimana fungsi Sigmoid dan transformasi Logit mampu memampatkan garis linier ke dalam kurva probabilitas berbentuk S (*S-curve*), serta bagaimana optimasi *Maximum Likelihood Estimation* (MLE) menggantikan OLS untuk klasifikasi biner cerdas di industri kelapa sawit.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
2. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
3. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
4. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
5. Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). *Introduction to Linear Regression Analysis* (6th ed.). John Wiley & Sons.
6. Wooldridge, J. M. (2020). *Introductory Econometrics: A Modern Approach* (7th ed.). Cengage Learning.
