# AI Modul 7.3: Panduan Instruktur & Kunci Solusi
## K-Nearest Neighbor (KNN)

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-03-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (45 Menit Teori & Geometri Ruang Metrik, 75 Menit Praktikum Terbimbing & Analisis K Optimal, 30 Menit Evaluasi HOTS & Kutukan Dimensi)
* **Karakteristik Modul**: Pembelajaran Berbasis Instansia (*Instance-Based / Lazy Learning*), Metrik Jarak Ruang Vektor, Deteksi Hama Presisi

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
KNN adalah model pertama dalam kurikulum ini yang tidak memiliki fase komputasi bobot terpisah (*no training phase*). Instruktur perlu memanfaatkan kontras ini untuk memperdalam intuisi arsitektural mahasiswa:
1. **Dua Paradigma Pembelajaran Mesin**:
   * *Eager Learner* (Regresi Linier & Logistik): Mempelajari persamaan global $\mathbf{w}^T \mathbf{x} + b$ terlebih dahulu; setelah selesai, data latih bisa dibuang; waktu inferensi sangat cepat.
   * *Lazy Learner* (KNN): Tidak membentuk fungsi matematis global; seluruh data latih wajib disimpan di RAM; waktu inferensi lambat karena memindai seluruh memori.
2. **Konteks Spesifik INSTIPER**: Hubungkan konsep kedekatan spasial dengan penyebaran hama ulat api di kebun kelapa sawit:
   * Mengapa penyebaran hama membentuk pola klaster spasial (*spatial clustering*) di sekitar pohon inang?
   * Mengapa nilai $K$ yang terlalu kecil ($K=1$) berbahaya jika drone menangkap citra daun sawit yang kotor terkena abu vulkanik atau debu jalan kebun (*noisy sample*)?

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Karena KNN tidak memiliki parameter bobot $\mathbf{w}$, algoritma ini gratis secara komputasi."**
  * *Koreksi Instruktur*: Beban komputasi KNN tidak hilang, melainkan **digeser dari fase pelatihan ke fase inferensi (*query time*)**. Pada dataset 100.000 pohon, memprediksi satu pohon baru membutuhkan 100.000 kalkulasi jarak Euclidean. Pada drone dengan komputer mini (seperti Raspberry Pi / Jetson Nano), ini akan menyebabkan *lag* komputasi parah.
* **Miskonsepsi 2: "Nilai $K$ yang semakin besar selalu meningkatkan keakuratan prediksi."**
  * *Koreksi Instruktur*: Tunjukkan kurva kompromi bias-varians. Nilai $K$ yang terlalu besar ($K \to n$) akan memicu *underfitting* parah di mana model mengabaikan variasi lokal dan selalu menebak kelas mayoritas global.
* **Miskonsepsi 3: "Standardisasi fitur hanya formalitas belaka."**
  * *Koreksi Instruktur*: Tunjukkan secara visual bahwa fitur dengan rentang ratusan (seperti reflektansi NIR 0–100) akan menggilas fitur berorde desimal (seperti NDVI 0.1–0.9), membuat NDVI sama sekali tidak diperhitungkan dalam jarak Euclidean jika tanpa `StandardScaler`.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Perhitungan Manual Metrik Jarak dan Majority Voting (C3)
Titik kueri bibit baru: $\mathbf{x}_q = (3.0, 2.0)$.
Data referensi pembibitan sawit:
* $S_1 = (1.0, 2.0)$, Label = 0 (Sehat)
* $S_2 = (2.0, 1.0)$, Label = 0 (Sehat)
* $S_3 = (4.0, 3.0)$, Label = 1 (Terserang Jamur)
* $S_4 = (5.0, 4.0)$, Label = 1 (Terserang Jamur)
* $S_5 = (2.0, 3.0)$, Label = 0 (Sehat)

#### Langkah 1: Tabel Perhitungan Jarak Euclidean dan Manhattan
| Sampel ($i$) | Koordinat $(x_1, x_2)$ | Label ($y$) | Selisih $\Delta x_1, \Delta x_2$ | Jarak Euclidean ($d_2$) | Jarak Manhattan ($d_1$) | Peringkat Jarak ($d_2$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $S_1$ | $(1.0, 2.0)$ | 0 | $-2.0, \phantom{-}0.0$ | $\sqrt{(-2)^2 + 0^2} = 2.000$ | $|-2| + |0| = 2.000$ | 4 |
| $S_2$ | $(2.0, 1.0)$ | 0 | $-1.0, -1.0$ | $\sqrt{(-1)^2 + (-1)^2} = \sqrt{2} \approx 1.414$ | $|-1| + |-1| = 2.000$ | 1 (Seri) |
| $S_3$ | $(4.0, 3.0)$ | 1 | $+1.0, +1.0$ | $\sqrt{1^2 + 1^2} = \sqrt{2} \approx 1.414$ | $|1| + |1| = 2.000$ | 2 (Seri) |
| $S_4$ | $(5.0, 4.0)$ | 1 | $+2.0, +2.0$ | $\sqrt{2^2 + 2^2} = \sqrt{8} \approx 2.828$ | $|2| + |2| = 4.000$ | 5 |
| $S_5$ | $(2.0, 3.0)$ | 0 | $-1.0, +1.0$ | $\sqrt{(-1)^2 + 1^2} = \sqrt{2} \approx 1.414$ | $|-1| + |1| = 2.000$ | 3 (Seri) |

#### Langkah 2: Klasifikasi Konsensus untuk $K = 3$ (Euclidean)
Tiga tetangga terdekat adalah $S_2$, $S_3$, dan $S_5$ (ketiganya berjarak $1.414$):
* Label $S_2$: Kelas 0 (Sehat)
* Label $S_3$: Kelas 1 (Terserang Jamur)
* Label $S_5$: Kelas 0 (Sehat)

Hasil pemungutan suara mayoritas:
$$\text{Suara Kelas 0} = 2, \quad \text{Suara Kelas 1} = 1$$
**Keputusan $K = 3$**: $\hat{y} = \mathbf{0}$ (**Sehat**).

#### Langkah 3: Klasifikasi Konsensus untuk $K = 5$ (Euclidean)
Seluruh 5 sampel diikutsertakan ($S_2, S_3, S_5, S_1, S_4$):
$$\text{Suara Kelas 0} = 3 \text{ (dari } S_1, S_2, S_5), \quad \text{Suara Kelas 1} = 2 \text{ (dari } S_3, S_4)$$
**Keputusan $K = 5$**: $\hat{y} = \mathbf{0}$ (**Sehat**).

---

### Soal 2: Analisis Komputasi Distance-Weighted KNN (C4)
Pada $K = 3$ tetangga terdekat ($S_2, S_3, S_5$), jarak masing-masing adalah $d = \sqrt{2} \approx 1.4142$.

#### Langkah 1: Menghitung Bobot Invers Jarak Kuadratik ($w_i = \frac{1}{d_i^2}$)
* $w_2 = \frac{1}{(\sqrt{2})^2} = \frac{1}{2} = 0.50$ (Kelas 0)
* $w_3 = \frac{1}{(\sqrt{2})^2} = \frac{1}{2} = 0.50$ (Kelas 1)
* $w_5 = \frac{1}{(\sqrt{2})^2} = \frac{1}{2} = 0.50$ (Kelas 0)

#### Langkah 2: Akumulasi Bobot per Kelas
$$\sum_{i \in \text{Kelas 0}} w_i = w_2 + w_5 = 0.50 + 0.50 = 1.00$$
$$\sum_{i \in \text{Kelas 1}} w_i = w_3 = 0.50$$

#### Langkah 3: Probabilitas Terbobot Ternormalisasi
$$P(y = 1 \mid \mathbf{x}_q) = \frac{\sum_{i \in \text{Kelas 1}} w_i}{\sum_{\text{Semua}} w_i} = \frac{0.50}{1.00 + 0.50} = \frac{0.50}{1.50} = \frac{1}{3} \approx 33.33\%$$
$$P(y = 0 \mid \mathbf{x}_q) = \frac{1.00}{1.50} = \frac{2}{3} \approx 66.67\%$$

*Kesimpulan*: Karena total bobot Kelas 0 ($1.00$) lebih besar dari Kelas 1 ($0.50$), keputusan tetap **Kelas 0 (Sehat)**. Keputusan identik dengan metode *uniform voting* karena jarak ketiga tetangga terdekat bernilai sama persis.

---

### Soal 3: Studi Kasus Patologi Kutukan Dimensi pada Data Drone (C4)
* **Penjelasan Teoretis Beyer et al. (1999)**:
  Dalam ruang dimensi tinggi ($p = 120$), volume ruang menjadi sangat hampa (*hyper-sparse*). Teorema Beyer membuktikan bahwa:
  $$\lim_{p \to \infty} \frac{d_{\max} - d_{\min}}{d_{\min}} = 0$$
  Ketika 117 saluran spektral yang tidak relevan dengan defisiensi Mg dimasukkan, derau acak dari saluran-saluran tersebut terakumulasi dalam penjumlahan kuadrat jarak Euclidean ($\sum_{j=1}^{120} (x_j - x_{ij})^2$). Derau acak berdimensi 117 ini menenggelamkan sinyal diskriminatif dari 3 saluran penting, sehingga jarak dari bibit uji ke pohon sehat vs pohon defisiensi Mg menjadi hampir identik ($\sim d$). KNN kehilangan daya pembeda jarak geometrisnya dan performa merosot setara tebakan acak.
* **Mengapa Model Berbasis Pohon / PCA Lebih Kebal?**
  * *Model Berbasis Pohon (Decision Tree/Random Forest)*: Memilih fitur satu per satu secara ortogonal pada setiap simpul berdasarkan kriteria *Information Gain*. Fitur bising yang tidak memiliki korelasi dengan defisiensi hara akan diabaikan dan tidak pernah dipilih sebagai simpul pemisah (*inherent feature selection*).
  * *PCA (Principal Component Analysis)*: Memproyeksikan data ke arah sumbu varians terbesar, memadatkan 120 fitur mentah menjadi beberapa komponen utama esensial sebelum diserahkan ke KNN.
* **Protokol Pra-Pemrosesan Rekayasa**:
  1. *Seleksi Fitur Domain Agronomi*: Ekstraksi indeks vegetasi terstandar yang terbukti berkorelasi dengan klorofil dan hara Mg (misal: Red Edge NDVI, Chlorophyll Index).
  2. *Analisis Korelasi & Mutual Information*: Mengeliminasi seluruh saluran spektral yang memiliki *mutual information* mendekati nol terhadap label target.
  3. *Standardisasi $Z$-score*: Memastikan seluruh fitur berada pada skala ragam unit sebelum proses kalkulasi jarak.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Prediksi Pohon Sawit Baru Menggunakan Model Terbobot
Data sensor drone: NIR = 55.0, NDVI = 0.58, Kerapatan Tajuk = 60.0%.
Kode solusi:
```python
pohon_baru = pd.DataFrame([{
    'Reflektansi_NIR': 55.0,
    'Indeks_NDVI': 0.58,
    'Kerapatan_Tajuk': 60.0
}])
pohon_scaled = scaler.transform(pohon_baru)
pred_status = model_distance.predict(pohon_scaled)[0]
prob_hama = model_distance.predict_proba(pohon_scaled)[0, 1]

print(f"Probabilitas Serangan Hama Ulat Api : {prob_hama*100:.2f}%")
print(f"Rekomendasi Tindakan Lapangan : {'SEGERA SPOT SPRAYING' if pred_status == 1 else 'MONITORING RUTIN'}")
```
*Hasil*: Probabilitas serangan berada pada rentang **65% – 85%** (rekomendasi: **SEGERA SPOT SPRAYING**).

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Pemahaman Konseptual Lazy Learner & Geometri Jarak | 25% | Mampu membedakan paradigma *lazy* vs *eager learning*, menjelaskan perbedaan geometris jarak Manhattan vs Euclidean, dan menguraikan trade-off bias-varians pada pemilihan $K$. |
| **C3 (Penerapan)** | Implementasi Pemodelan & Validasi Silang | 35% | Mampu mengimplementasikan komputasi jarak NumPy murni dengan hasil ekuivalen 100% terhadap Scikit-Learn, menerapkan `StandardScaler` secara benar, dan melakukan pencarian $K$ optimal via K-Fold CV. |
| **C4 (Analisis)** | Eksperimen Kutukan Dimensi & Pembobotan Jarak | 40% | Mampu menganalisis komparasi skema pembobotan (`uniform` vs `distance`), menguraikan bukti matematis degradasi kontras jarak pada data berdimensi tinggi, serta merumuskan protokol mitigasi pra-pemrosesan. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.4 (Decision Tree)

Di akhir sesi kelas modul 7.3, instruktur disarankan memfasilitasi refleksi konseptual mahasiswa:
1. **Mengulas Keterbatasan Operasional KNN**: Tanyakan kepada mahasiswa: *"Jika kita memasang sistem AI ini pada drone pemetaan yang terbang di atas kebun 10.000 hektar dengan 1,4 juta pohon, sanggupkah drone menghitung jutaan jarak Euclidean secara real-time tanpa kehabisan baterai?"*
2. **Menyoroti Masalah Kotak Hitam Non-Parametrik**: Tunjukkan bahwa saat manajer perkebunan bertanya: *"Mengapa pohon di blok B3 ini Anda semprot pestisida?"*, jawaban KNN hanyalah: *"Karena jarak numeriknya dekat dengan pohon lain"*, tanpa mampu memberikan batasan nilai ambang agronomi yang logis.
3. **Mengantarkan Solusi Pohon Keputusan**: Jelaskan bahwa pada pertemuan berikutnya (**AI Modul 7.4: Decision Tree**), mahasiswa akan mempelajari bagaimana algoritma mampu menghasilkan aturan logika keputusan (*If-Then Rules*) transparan berbasis entropi informasi dan indeks Gini yang dieksekusi dalam fraksi milidetik di komputer drone.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Beyer, K., Goldstein, J., Ramakrishnan, R., & Shaft, U. (1999). When is "nearest neighbor" meaningful?. *International Conference on Database Theory*, 217-235. Springer.
2. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
3. Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, 13(1), 21-27.
4. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
5. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
6. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
