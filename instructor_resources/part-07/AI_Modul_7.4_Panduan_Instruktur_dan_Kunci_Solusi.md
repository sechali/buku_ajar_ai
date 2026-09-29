# AI Modul 7.4: Panduan Instruktur & Kunci Solusi
## Decision Tree

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-04-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Entropi/Gini & Algoritma CART, 70 Menit Praktikum Pemangkasan Pohon, 30 Menit Evaluasi Aturan Logika Bisnis PKS)
* **Karakteristik Modul**: Algoritma Pembelajaran Simbolik / Non-Parametrik, *White-Box Explainable AI*, Sortasi Mutu Pertanian

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Pohon keputusan adalah jembatan emas yang menghubungkan konsep pemrograman dasar (struktur logika percabangan `if-else` pada Part 2) dengan pembelajaran mesin otomatis (*machine learning*):
1. **Dari Manual ke Otomatis**: Ingatkan mahasiswa bagaimana pada AI Modul 2.6 mereka menulis logika `if-else` sortasi TBS secara manual dengan ambang batas *hardcoded*. Tunjukkan bahwa pada AI Modul 7.4, komputer sendiri yang secara matematis menemukan ambang batas (*threshold*) terbaik melalui minimasi ketidakmurnian Gini atau maksimasi Information Gain.
2. **Konteks Spesifik INSTIPER**: Hubungkan kriteria matematis pohon dengan aturan fraksi mutu TBS di PKS:
   * Mengapa persentase brondolan lepas menjadi fitur pemisah simpul akar (*root node*)? Karena secara fisiologis, pelepasan brondolan adalah penanda utama sintesis asam lemak dan kematangan buah.
   * Mengapa keterpahaman model (*interpretability*) sangat dihargai di pabrik kelapa sawit? Karena mandor sortasi dan supir truk membutuhkan penjelasan yang jelas mengapa suatu muatan buah dipotong timbangannya atau ditolak.

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Akurasi data latih 100% pada pohon keputusan membuktikan model tersebut sempurna."**
  * *Koreksi Instruktur*: Tunjukkan bahwa pohon keputusan tanpa pembatasan (`max_depth=None`) akan selalu mencapai akurasi data latih 100% karena pohon menghafal setiap baris sampel hingga tingkat daun individual. Ini adalah definisi klasik dari **Overfitting Ekstrem**.
* **Miskonsepsi 2: "Fitur pada pohon keputusan harus distandardisasi dengan StandardScaler seperti pada Regresi Logistik dan KNN."**
  * *Koreksi Instruktur*: Tunjukkan bahwa pohon keputusan membelah simpul berdasarkan aturan perbandingan monotonik $x_j \le \theta$. Skala angka (apakah puluhan kg atau pecahan desimal) tidak memengaruhi urutan nilai, sehingga pohon keputusan kebal terhadap perbedaan skala fitur.
* **Miskonsepsi 3: "Entropi dan Gini selalu menghasilkan struktur pohon yang bertolak belakang."**
  * *Koreksi Instruktur*: Tunjukkan kurva perbandingan keduanya. Keduanya adalah fungsi cembung simetris yang mencapai puncak pada $p=0.5$ dan bernilai 0 pada $p \in \{0, 1\}$. Pada 98% kasus praktis industri, keduanya memilih titik potong simpul yang identik, namun Gini lebih disukai karena lebih hemat komputasi (tanpa $\log_2$).

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Komputasi Manual Entropi dan Information Gain (C3)
Simpul induk $D$ ($N = 40$ tandan):
* 24 tandan Matang Prima ($y = 1$) $\implies p_1 = \frac{24}{40} = 0.60$
* 16 tandan Afkir Mentah ($y = 0$) $\implies p_0 = \frac{16}{40} = 0.40$

Pemisahan fitur Brondolan pada ambang $\theta = 15.0\%$:
* Cabang Kiri ($D_L$, $N_L = 20$): 4 Prima ($p_{L1} = 0.20$), 16 Afkir ($p_{L0} = 0.80$)
* Cabang Kanan ($D_R$, $N_R = 20$): 20 Prima ($p_{R1} = 1.00$), 0 Afkir ($p_{R0} = 0.00$)

#### Langkah 1: Menghitung Entropi Simpul Induk $H(D)$
$$H(D) = -[p_1 \log_2(p_1) + p_0 \log_2(p_0)]$$
$$H(D) = -[0.60 \log_2(0.60) + 0.40 \log_2(0.40)]$$
Karena $\log_2(0.60) \approx -0.73697$ dan $\log_2(0.40) \approx -1.32193$:
$$H(D) = -[0.60(-0.73697) + 0.40(-1.32193)] = -[-0.44218 - 0.52877] = \mathbf{0.97095 \text{ bit}}$$

#### Langkah 2: Menghitung Entropi Cabang Kiri $H(D_L)$ dan Cabang Kanan $H(D_R)$
* **Cabang Kiri**:
  $$H(D_L) = -[0.20 \log_2(0.20) + 0.80 \log_2(0.80)]$$
  Karena $\log_2(0.20) \approx -2.32193$ dan $\log_2(0.80) \approx -0.32193$:
  $$H(D_L) = -[0.20(-2.32193) + 0.80(-0.32193)] = -[-0.46439 - 0.25754] = \mathbf{0.72193 \text{ bit}}$$
* **Cabang Kanan**:
  Karena seluruh 20 sampel adalah Prima ($p = 1.0$), simpul ini murni sempurna:
  $$H(D_R) = -(1.0 \log_2 1.0 + 0) = \mathbf{0.00000 \text{ bit}}$$

#### Langkah 3: Menghitung Perolehan Informasi (Information Gain)
$$\text{IG}(D, \text{Brondolan}) = H(D) - \left[ \frac{|D_L|}{|D|} H(D_L) + \frac{|D_R|}{|D|} H(D_R) \right]$$
$$\text{IG}(D, \text{Brondolan}) = 0.97095 - \left[ \frac{20}{40}(0.72193) + \frac{20}{40}(0.00000) \right]$$
$$\text{IG}(D, \text{Brondolan}) = 0.97095 - 0.36097 = \mathbf{0.60998 \text{ bit (atau } \approx 0.61 \text{ bit)}}$$

---

### Soal 2: Perhitungan Manual Indeks Ketidakmurnian Gini (C3)
Data yang sama: Simpul Induk $D$ ($N = 40$), Cabang $D_L$ ($N_L = 20$), Cabang $D_R$ ($N_R = 20$).

#### Langkah 1: Menghitung Indeks Gini Simpul Induk $I_G(D)$
$$I_G(D) = 1 - (p_1^2 + p_0^2) = 1 - (0.60^2 + 0.40^2) = 1 - (0.36 + 0.16) = 1 - 0.52 = \mathbf{0.4800}$$

#### Langkah 2: Menghitung Indeks Gini Cabang Kiri dan Kanan
* **Cabang Kiri**:
  $$I_G(D_L) = 1 - (p_{L1}^2 + p_{L0}^2) = 1 - (0.20^2 + 0.80^2) = 1 - (0.04 + 0.64) = 1 - 0.68 = \mathbf{0.3200}$$
* **Cabang Kanan**:
  $$I_G(D_R) = 1 - (1.00^2 + 0.00^2) = 1 - 1.00 = \mathbf{0.0000}$$

#### Langkah 3: Menghitung Pengurangan Ketidakmurnian Gini ($\Delta I_G$)
$$\Delta I_G = I_G(D) - \left[ \frac{|D_L|}{|D|} I_G(D_L) + \frac{|D_R|}{|D|} I_G(D_R) \right]$$
$$\Delta I_G = 0.4800 - \left[ \frac{20}{40}(0.3200) + \frac{20}{40}(0.0000) \right] = 0.4800 - 0.1600 = \mathbf{0.3200}$$

#### Langkah 4: Interpretasi Kualitas Pemisahan
Nilai $\Delta I_G = 0.3200$ (penurunan sebesar $66.67\%$ dari ketidakmurnian awal) dan $\text{IG} = 0.61$ bit membuktikan bahwa pemisahan fitur pada ambang $15\%$ brondolan sangat efektif: mampu mengisolasi seluruh 20 tandan matang prima ke satu simpul daun murni tanpa satupun kesalahan klasifikasi.

---

### Soal 3: Analisis Optimasi Cost-Complexity Pruning (C4)
Pohon penuh $T_0$: $|T_0| = 12$, $R(T_0) = 0.04$.
Pohon terpangkas $T_1$: $|T_1| = 6$, $R(T_1) = 0.08$.

#### Langkah 1: Menentukan Titik Ambang Kritis ($\alpha_{\text{kritis}}$)
Persamaan kesetaraan fungsi objektif:
$$R_\alpha(T_0) = R_\alpha(T_1)$$
$$R(T_0) + \alpha |T_0| = R(T_1) + \alpha |T_1|$$
$$0.04 + 12\alpha = 0.08 + 6\alpha$$
$$12\alpha - 6\alpha = 0.08 - 0.04$$
$$6\alpha = 0.04 \implies \alpha_{\text{kritis}} = \frac{0.04}{6} \approx \mathbf{0.00667}$$

#### Langkah 2: Pemilihan Pohon pada Parameter Penalti $\alpha = 0.010$
* **Biaya Pohon Penuh $T_0$**:
  $$R_\alpha(T_0) = 0.04 + (0.010 \times 12) = 0.04 + 0.12 = \mathbf{0.160}$$
* **Biaya Pohon Terpangkas $T_1$**:
  $$R_\alpha(T_1) = 0.08 + (0.010 \times 6) = 0.08 + 0.06 = \mathbf{0.140}$$

*Keputusan*: Karena $R_\alpha(T_1) < R_\alpha(T_0)$, sistem **wajib memilih Pohon Terpangkas $T_1$**.

#### Langkah 3: Rationale Rekayasa AI Perkebunan
Meskipun pohon $T_1$ mengorbankan $4\%$ akurasi pada data latih (galat naik dari 0.04 ke 0.08), pemangkasan ini memangkas separuh jumlah daun (dari 12 menjadi 6). Model yang lebih ramping ini membuang cabang-cabang rapuh yang hanya menghafal derau lokal, sehingga menghasilkan generalisasi yang jauh lebih tangguh terhadap variasi truk sawit baru di lapangan dan jauh lebih mudah diaudit oleh mandor sortasi.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Prediksi Truk TBS Baru Menggunakan Aturan Pohon
Data truk baru: Brondolan = 25.0%, FFA = 2.1%, Berat Tandan = 22.0 kg.
Kode solusi:
```python
truk_baru = pd.DataFrame([{
    'Brondolan_Persen': 25.0,
    'FFA_Persen': 2.1,
    'Berat_Tandan_kg': 22.0
}])
pred_fraksi = best_pruned_tree.predict(truk_baru)[0]
nama_fraksi = ['Mentah Afkir (0)', 'Kurang Matang (1)', 'Matang Standar (2)', 'Matang Prima (3)']
print(f"Hasil Klasifikasi Mutu TBS : {nama_fraksi[pred_fraksi]}")
```
*Hasil*: Truk tersebut diklasifikasikan sebagai **Matang Prima (Kelas 3)** karena memenuhi aturan:
`Brondolan > 18.05% DAN Brondolan <= 40.35% DAN FFA <= 2.59%`.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Pemahaman Teori Entropi, Gini, dan CART | 25% | Mampu membandingkan formula matematis Gini vs Entropi, menjelaskan sifat non-parametrik pohon, dan menguraikan mekanisme pencarian batas belah fitur kontinu. |
| **C3 (Penerapan)** | Implementasi Pemodelan & Visualisasi Aturan | 35% | Mampu mengimplementasikan perhitungan Gini/Entropi Python, memvisualisasikan struktur pohon dengan `plot_tree`, serta mengekstrak teks aturan bisnis eksplisit (`export_text`) tanpa galat. |
| **C4 (Analisis)** | Optimasi Pemangkasan & Mitigasi Overfitting | 40% | Mampu menganalisis fenomena overfitting pohon tak terbatas, melakukan optimasi *Cost-Complexity Pruning* via `ccp_alpha`, serta menentukan pohon bagian (*subtree*) terbaik secara saintifik. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.5 (Random Forest)

Di akhir sesi kelas modul 7.4, instruktur disarankan memfasilitasi diskusi kritis:
1. **Mendemonstrasikan Instabilitas Pohon**: Ubah 3 baris data secara acak pada dataset mahasiswa, lalu latih ulang pohon. Tunjukkan bahwa struktur percabangan di bawah simpul akar berubah total. Tanyakan: *"Apakah Anda berani mempercayakan keputusan bisnis pabrik bernilai miliaran rupiah pada model yang begitu mudah goyah oleh segelintir sampel?"*
2. **Menjelaskan Dilema Pohon Tunggal**: Pohon tunggal menghadapi dilema varians-bias yang tajam: jika terlalu dalam ia menghafal derau (*overfitting*), jika terlalu dangkal ia gagal menangkap pola rumit (*underfitting*).
3. **Mengantarkan Konsep Kekuatan Kolektif (Ensemble)**: Jelaskan bahwa pada pertemuan berikutnya (**AI Modul 7.5: Random Forest**), mahasiswa akan mempelajari bagaimana "kebijaksanaan massa" (*Wisdom of Crowds*) diterapkan melalui penggabungan ratusan pohon acak (*Bagging*), meredam varians secara drastis dan menghasilkan model prediktif kelas dunia yang stabil dan akurat.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Breiman, L., Friedman, J., Stone, C. J., & Olshen, R. A. (1984). *Classification and Regression Trees*. CRC Press.
2. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
3. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
4. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
5. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
6. Quinlan, J. R. (1986). Induction of decision trees. *Machine Learning*, 1(1), 81-106.
