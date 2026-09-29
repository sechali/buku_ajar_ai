# AI Modul 7.2: Panduan Instruktur & Kunci Solusi
## Logistic Regression

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-02-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori & Penurunan Matematis MLE/Sigmoid, 70 Menit Praktikum Terbimbing & Optimasi Threshold, 30 Menit Diskusi Kasus Asimetri Biaya PKS)
* **Karakteristik Modul**: Algoritma Supervised Classification Parametrik, Probabilitas Posterior, Optimasi Berbasis Biaya Finansial

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Regresi logistik sering kali memicu kebingungan linguistik bagi mahasiswa baru karena namanya menggunakan kata "Regresi", padahal secara operasional digunakan untuk tugas **Klasifikasi**. Instruktur perlu menegaskan distingsi ini sejak menit pertama:
1. **Mengapa Disebut Regresi?** Karena model sebenarnya meregresikan variabel target kontinu laten berupa nilai probabilitas logit $z = \ln(\text{Odds}) = \mathbf{w}^T \mathbf{x} + b$.
2. **Mengapa Digunakan untuk Klasifikasi?** Karena nilai probabilitas kontinu yang dihasilkan dipetakan ke dalam label kelas diskret $\{0, 1\}$ melalui penerapan ambang batas keputusan (*Decision Threshold* $\tau$).
3. **Konteks Spesifik INSTIPER**: Hubungkan matematika fungsi penalti Log Loss dengan standar mutu minyak sawit mentah (CPO) dan sortasi TBS:
   * Mengapa meloloskan tangki CPO ber-FFA tinggi ke kapal tanker ekspor membawa risiko denda arbitrase internasional hingga ratusan juta rupiah?
   * Mengapa asimetri biaya kesalahan ini menuntut penyetelan ambang batas $\tau > 0.50$?

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Ambang batas $\tau = 0.50$ adalah titik keputusan mutlak terbaik dalam seluruh model klasifikasi."**
  * *Koreksi Instruktur*: Ambang batas 0.50 hanya optimal jika biaya kesalahan $C_{\text{FP}} = C_{\text{FN}}$ dan distribusi kelas seimbang 50:50. Pada sektor agro-industri nyata, biaya kesalahan hampir selalu asimetris, sehingga $\tau$ harus disesuaikan secara dinamis (*Cost-Sensitive Decision Making*).
* **Miskonsepsi 2: "Regresi Logistik dapat diselesaikan secara analitik tertutup seperti OLS pada Regresi Linier."**
  * *Koreksi Instruktur*: Turunan dari fungsi log-likelihood regresi logistik menghasilkan sistem persamaan non-linier transendental yang tidak memiliki solusi bentuk tertutup (*no closed-form analytical solution*), sehingga wajib diselesaikan menggunakan metode numerik iteratif seperti Gradient Descent atau algoritma kuasi-Newton L-BFGS.
* **Miskonsepsi 3: "Akurasi 95% membuktikan model klasifikasi mutu sawit sudah sempurna."**
  * *Koreksi Instruktur*: Jika pada populasi TBS hanya ada 5% tandan busuk (*class imbalance*), model yang memprediksi seluruh tandan sehat akan meraih akurasi 95% padahal model tersebut sama sekali tidak berguna secara operasional. Tunjukkan keunggulan metrik *Precision*, *Recall*, *F1-Score*, dan *ROC-AUC*.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Komputasi Matematis Odds dan Sigmoid Manual (C3)
Diberikan persamaan skor laten sortasi TBS sawit:
$$z = -3.20 + 0.85 x_1 + 1.40 x_2$$
Dengan $x_1 = 3.0$ (indeks warna kematangan) dan $x_2 = 1.5$ dm (diameter tandan).

#### Langkah 1: Menghitung Nilai Skor Laten ($z$)
$$z = -3.20 + (0.85 \times 3.0) + (1.40 \times 1.5)$$
$$z = -3.20 + 2.55 + 2.10 = 1.45$$

#### Langkah 2: Menghitung Probabilitas Lolos Menggunakan Fungsi Sigmoid
$$\hat{p} = \sigma(z) = \frac{1}{1 + e^{-z}} = \frac{1}{1 + e^{-1.45}}$$
Karena $e^{-1.45} \approx 0.23457$:
$$\hat{p} = \frac{1}{1 + 0.23457} = \frac{1}{1.23457} \approx 0.8100 \text{ atau } 81.0\%$$

#### Langkah 3: Menghitung Rasio Kemunculan (Odds) dan Interpretasinya
$$\text{Odds} = \frac{\hat{p}}{1 - \hat{p}} = \frac{0.8100}{1 - 0.8100} = \frac{0.8100}{0.1900} \approx 4.263$$
*Interpretasi Fisis bagi Mandor Panen*: Tandan buah sawit dengan spesifikasi tersebut memiliki peluang $4.26$ kali lebih besar untuk diklasifikasikan sebagai **Layak Olah (Prima)** dibandingkan kemungkinan ditolak sebagai afkir.

---

### Soal 2: Analisis Fungsi Rugi Binary Cross-Entropy pada Kasus Ekstrem (C4)
Sampel uji memiliki label aktual **Afkir / Rusak ($y = 0$)**:
* Laboratorium A memprediksi $\hat{p}_A = 0.55$.
* Laboratorium B memprediksi $\hat{p}_B = 0.99$ (*overconfident wrong prediction*).

#### Langkah 1: Menghitung Penalti Log Loss Masing-Masing Model
Untuk sampel dengan $y = 0$, fungsi rugi bernilai:
$$J = -\ln(1 - \hat{p})$$

* **Model Laboratorium A**:
  $$J_A = -\ln(1 - 0.55) = -\ln(0.45) \approx 0.7985$$
* **Model Laboratorium B**:
  $$J_B = -\ln(1 - 0.99) = -\ln(0.01) \approx 4.6052$$

#### Langkah 2: Perbandingan Rasio Penalti
$$\text{Rasio} = \frac{J_B}{J_A} = \frac{4.6052}{0.7985} \approx 5.767 \text{ kali lipat}$$

#### Langkah 3: Alasan Teoretis Krusial Fungsi Penalti Logaritmik di PKS
Fungsi penalti logaritmik mengenakan penalti asimtotik yang melonjak menuju tak terhingga ($\to \infty$) saat model membuat prediksi yang salah dengan tingkat keyakinan sangat tinggi. Dalam operasional pabrik kelapa sawit, model yang "merasa sangat yakin 99% bahwa minyak rusak itu prima" jauh lebih berbahaya dibanding model yang "masih ragu-ragu di sekitar 55%". Penalti ekstrem ini memaksa algoritma optimasi gradien untuk mengoreksi bobot model secara masif dan mencegah keputusan keliru yang fatal pada keselamatan dan mutu pabrik.

---

### Soal 3: Penyetelan Ambang Batas Berbasis Biaya Finansial (C4)
Data biaya asimetris:
* $C_{\text{FP}} = \text{Rp } 12.000.000$ (meloloskan tandan busuk ke rebusan)
* $C_{\text{FN}} = \text{Rp } 1.500.000$ (menolak tandan segar bagus untuk sortasi ulang)

Performa pada 100 batch:
* **Opsi A ($\tau = 0.50$)**: $\text{FP} = 8$, $\text{FN} = 2$
* **Opsi B ($\tau = 0.75$)**: $\text{FP} = 1$, $\text{FN} = 7$

#### Langkah 1: Menghitung Total Kerugian Finansial Opsi A
$$\text{Biaya}_A = (\text{FP} \times C_{\text{FP}}) + (\text{FN} \times C_{\text{FN}})$$
$$\text{Biaya}_A = (8 \times 12.000.000) + (2 \times 1.500.000) = 96.000.000 + 3.000.000 = \text{Rp } 99.000.000$$

#### Langkah 2: Menghitung Total Kerugian Finansial Opsi B
$$\text{Biaya}_B = (1 \times 12.000.000) + (7 \times 1.500.000) = 12.000.000 + 10.500.000 = \text{Rp } 22.500.000$$

#### Langkah 3: Keputusan Manajerial Saintifik
$$\text{Penghematan Finansial} = \text{Biaya}_A - \text{Biaya}_B = 99.000.000 - 22.500.000 = \text{Rp } 76.500.000 \text{ (Turun } 77.27\%)$$
*Keputusan*: Manajer pabrik **wajib memilih Opsi B ($\tau = 0.75$)**. Meskipun Opsi B menghasilkan lebih banyak False Negative (7 tandan bagus harus disortasi ulang), pengorbanan ini jauh lebih murah dibandingkan risiko 8 batch tandan busuk masuk ke ketel rebusan pada Opsi A yang merusak mutu ribuan liter minyak tangki timbun.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Prediksi Mutu Sampel Tangki CPO Baru
Data laboratorium: FFA = 2.4%, Kadar Air = 0.12%, Kotoran = 0.015%.
Kode solusi:
```python
sample_baru = pd.DataFrame([{
    'FFA_Persen': 2.4,
    'Kadar_Air_Persen': 0.12,
    'Kotoran_Persen': 0.015
}])
sample_scaled = scaler.transform(sample_baru)
prob_lolos = sk_model.predict_proba(sample_scaled)[0, 1]
status_pred = int(prob_lolos >= best_tau)

print(f"Probabilitas Lolos Ekspor : {prob_lolos*100:.2f}%")
print(f"Keputusan Sistem (tau={best_tau:.2f}) : {'LOLOS EKSPOR' if status_pred == 1 else 'AFKIR'}")
```
*Hasil*: Probabilitas lolos berada pada kisaran **88% – 96%** (kategori **LOLOS EKSPOR**).

### 4.2 Analisis Pergeseran Ambang Batas ke Kanan ($\tau > 0.50$)
Ketika penalti kesalahan False Positive sangat mendominasi ($C_{\text{FP}} \gg C_{\text{FN}}$), turunan dari ekspektasi biaya menuntut peningkatan presisi (*Precision*). Menaikkan ambang batas $\tau$ memperketat syarat kelolosan, sehingga sistem hanya akan meloloskan sampel yang benar-benar memiliki kepastian sangat tinggi. Ini secara matematis menekan angka False Positive mendekati nol, meminimalkan biaya kerugian finansial pabrik.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Pemahaman Sigmoid, Odds, dan Teori MLE | 25% | Mampu menguraikan secara runut transformasi logit, sifat pemetaan fungsi sigmoid, perbedaan OLS vs Log Loss, serta makna geometris garis batas keputusan. |
| **C3 (Penerapan)** | Implementasi Pemodelan & Standardisasi Fitur | 35% | Mampu mengimplementasikan algoritma regresi logistik via NumPy scratch dan Scikit-Learn dengan konsistensi korelasi prediksi $> 0.99$, serta menerapkan `StandardScaler` secara benar bebas *data leakage*. |
| **C4 (Analisis)** | Evaluasi ROC-AUC & Optimasi Ambang Batas Biaya | 40% | Mampu menganalisis kurva ROC dan skor AUC, menginterpretasikan laporan klasifikasi, serta melakukan kalkulasi matematis penyetelan ambang batas keputusan optimal berdasarkan matriks kerugian biaya pabrik. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.3 (K-Nearest Neighbor / KNN)

Di akhir sesi kelas modul 7.2, instruktur diharapkan membangun jembatan pemikiran konseptual (*bridging concept*) menuju Modul 7.3:
1. **Menguji Batas Kemampuan Regresi Logistik**: Tanyakan kepada mahasiswa: *"Bagaimana jika di lapangan, lahan sawit terserang hama bukan terpisah oleh garis lurus, melainkan membentuk lingkaran konsentris di tengah kebun yang dikelilingi pohon-pohon sehat?"*
2. **Menyoroti Sifat Parametrik Linier**: Tunjukkan bahwa regresi logistik hanya mampu menarik garis lurus (atau hiperbidang datar linier) sebagai pemisah kelas. Pada data dengan distribusi spasial atau relasi non-linier kompleks, regresi logistik akan gagal (*underfitting*).
3. **Mengantarkan Pendekatan Berbasis Tetangga Terdekat**: Jelaskan bahwa pada pertemuan berikutnya (**AI Modul 7.3: K-Nearest Neighbor / KNN**), mahasiswa akan mempelajari paradigma non-parametrik yang tidak membuat asumsi garis kaku, melainkan mengklasifikasikan kondisi suatu blok kebun murni berdasarkan kesamaan karakteristik dengan tanaman-tanaman tetangga terdekatnya di lapangan.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
2. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
3. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
4. Hosmer, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied Logistic Regression* (3rd ed.). John Wiley & Sons.
5. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
6. Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press.
