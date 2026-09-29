# AI Modul 6.2: Panduan Instruktur dan Kunci Solusi Matriks Konfusi (Confusion Matrix) - Evaluasi Multi-Kelas

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) dan Panduan Pedagogis

### 1.1 Informasi Umum Modul
- **Mata Kuliah:** Kecerdasan Buatan dan Sains Data Pertanian Presisi
- **Modul:** 6.2 (Matriks Konfusi: Anatomi Kesalahan Klasifikasi Biner dan Multi-Kelas)
- **Sasaran Peserta:** Mahasiswa Program Studi Agroteknologi, Agribisnis, dan Teknik Pertanian INSTIPER Yogyakarta
- **Alokasi Waktu:** 150 Menit (1 Sesi Tatap Muka / Praktikum Komputasi)

### 1.2 Tujuan Instruksional Khusus (TIK)
Pada akhir sesi pembelajaran ini, mahasiswa diharapkan mampu:
1. Membedah anatomi matriks kontinjensi $2 \times 2$ (Biner) dan $K \times K$ (Multi-Kelas) secara terstruktur.
2. Menghitung nilai Presisi, Recall, dan F1-Score per kelas kematangan buah secara manual dan terprogram.
3. Menjelaskan secara presisi perbedaan konsekuensi antara *Macro-Averaging*, *Micro-Averaging*, dan *Weighted-Averaging*.
4. Mengaudit sistem sortasi Tandan Buah Segar (TBS) di Pabrik Kelapa Sawit (PKS) menggunakan integrasi matriks konfusi dan matriks biaya operasional (*cost matrix*).

### 1.3 Alokasi Waktu Pembelajaran (150 Menit)

| Sesi | Durasi | Aktivitas Instruktur | Aktivitas Mahasiswa | Output / Indikator |
| :---: | :---: | :--- | :--- | :--- |
| **I** | 20 Menit | **Apersepsi & Kasus Industri:** Mendiskusikan proses sortasi buah TBS di loading ramp PKS dan ancaman penalti ALB (*Free Fatty Acid*). | Menganalisis foto-foto buah mentah, matang, dan lewat matang. | Mahasiswa memahami latar belakang fisik dan ekonomi sortasi. |
| **II** | 35 Menit | **Teori Matriks Multi-Kelas:** Membedah diagonal utama vs off-diagonal, normalisasi baris (Recall) vs kolom (Presisi), serta 3 metode agregasi. | Menyimak formulasi, mencatat keterangan simbol, dan mempraktikkan cara membaca rumus. | Penguasaan matematis notasi $C_{ij}$ dan formulasi agregasi. |
| **III** | 50 Menit | **Hands-On Coding Lab:** Memandu eksekusi Jupyter Notebook `AI_Modul_6.2_Confusion_Matrix.ipynb`. | Melatih Random Forest, memplot heatmap konfusi Seaborn, dan menghitung matriks penalti. | Skrip berjalan lancar (0 error) dan visualisasi heatmap tersimpan. |
| **IV** | 30 Menit | **Bedah Kasus HOTS:** Diskusi kelompok menghitung kerugian finansial sortasi $1.000$ tandan buah. | Mengerjakan perhitungan manual dan mempresentasikan sel kerugian terbesar. | Kemampuan berpikir tingkat tinggi dan kalkulasi biaya riil. |
| **V** | 15 Menit | **Refleksi & Sintesis:** Merangkum temuan galat bersebelahan dan mengantarkan ke konsep Cross-Validation. | Mengajukan pertanyaan reflektif dan evaluasi mandiri. | Sintesis pemahaman dan kesiapan ke modul berikutnya. |

---

## 2. Kunci Jawaban Lengkap dan Pembahasan Evaluasi Mandiri Mahasiswa

### 2.1 Pembahasan Latihan 8.1: Evaluasi Kritis Matriks Multi-Kelas Sortasi PKS
**Data Matriks Konfusi ($N = 1.000$ tandan):**

| Kelas Aktual \ Prediksi | Mentah ($M$) | Kurang Matang ($KM$) | Matang ($MT$) | Lewat Matang ($LM$) | Total Baris ($N_k$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mentah ($M$)** | **180** | 15 | 5 | 0 | $200$ |
| **Kurang Matang ($KM$)** | 20 | **230** | 40 | 10 | $300$ |
| **Matang ($MT$)** | 0 | 25 | **380** | 15 | $420$ |
| **Lewat Matang ($LM$)** | 0 | 0 | 15 | **65** | $80$ |
| **Total Kolom ($\hat{N}_k$)**| $200$ | $270$ | $440$ | $90$ | **Total = 1.000** |

#### Butir 1: Perhitungan Presisi dan Recall per Kelas Individual
1. **Kelas Mentah ($M$):**
   - $\text{Recall}_M = \frac{C_{11}}{\text{Total Baris } 1} = \frac{180}{200} = 90{,}00\%$
   - $\text{Precision}_M = \frac{C_{11}}{\text{Total Kolom } 1} = \frac{180}{200} = 90{,}00\%$
2. **Kelas Kurang Matang ($KM$):**
   - $\text{Recall}_{KM} = \frac{C_{22}}{\text{Total Baris } 2} = \frac{230}{300} \approx 76{,}67\%$
   - $\text{Precision}_{KM} = \frac{C_{22}}{\text{Total Kolom } 2} = \frac{230}{270} \approx 85{,}19\%$
3. **Kelas Matang ($MT$):**
   - $\text{Recall}_{MT} = \frac{C_{33}}{\text{Total Baris } 3} = \frac{380}{420} \approx 90{,}48\%$
   - $\text{Precision}_{MT} = \frac{C_{33}}{\text{Total Kolom } 3} = \frac{380}{440} \approx 86{,}36\%$
4. **Kelas Lewat Matang ($LM$):**
   - $\text{Recall}_{LM} = \frac{C_{44}}{\text{Total Baris } 4} = \frac{65}{80} = 81{,}25\%$
   - $\text{Precision}_{LM} = \frac{C_{44}}{\text{Total Kolom } 4} = \frac{65}{90} \approx 72{,}22\%$

#### Butir 2: Perhitungan Macro-Precision dan Weighted-Precision
1. **Macro-Precision (Rerata tidak berbobot):**
   $$\text{Macro-P} = \frac{90{,}00\% + 85{,}19\% + 86{,}36\% + 72{,}22\%}{4} = \frac{333{,}77\%}{4} \approx 83{,}44\%$$
2. **Weighted-Precision (Dibobot proporsi sampel $N_k / 1.000$):**
   $$\begin{aligned}
   \text{Weighted-P} &= (0{,}20 \times 90{,}00\%) + (0{,}30 \times 85{,}19\%) + (0{,}42 \times 86{,}36\%) + (0{,}08 \times 72{,}22\%) \\
   &= 18{,}00\% + 25{,}557\% + 36{,}271\% + 5{,}778\% \\
   &\approx 85{,}61\%
   \end{aligned}$$
- **Penjelasan Perbedaan:**  
  Nilai *Weighted-Precision* ($85{,}61\%$) lebih tinggi daripada *Macro-Precision* ($83{,}44\%$) karena kelas mayoritas (Matang Sempurna, $42\%$ populasi) memiliki presisi tinggi ($86{,}36\%$) yang mengangkat skor weighted, sementara kelas minoritas (Lewat Matang, hanya $8\%$ populasi) yang presisinya rendah ($72{,}22\%$) tidak terlalu menekan skor weighted namun menurunkan skor makro secara signifikan.

#### Butir 3: Galat Paling Berbahaya bagi OER Pabrik
Galat paling berbahaya bagi efisiensi ekstraksi minyak (OER) adalah **Buah Mentah yang diprediksi sebagai Matang Sempurna ($C_{13} = 5$ tandan)**. Buah mentah yang masuk ke dalam rebusan (*sterilizer*) tidak dapat melepaskan minyak sawit mentah karena vakuola minyak belum matang, memboroskan uap pabrik, dan menurunkan rendemen OER secara keseluruhan.

---

### 2.2 Pembahasan Latihan 8.2: Rancang Bangun Matriks Biaya Finansial Multi-Kelas
**Perkalian Hadamard antara Matriks Konfusi dan Matriks Penalti Biaya per Sel:**

$$\text{Rincian Biaya per Sel} = C_{ij} \times \text{Cost}_{ij}$$

1. **Baris 1 (Aktual Mentah):**
   - Diprediksi Kurang Matang ($15$ tandan $\times$ Rp $15.000$) = Rp $225.000$
   - Diprediksi Matang ($5$ tandan $\times$ Rp $120.000$) = **Rp $600.000$**
   - Subtotal Baris 1 = Rp $825.000$
2. **Baris 2 (Aktual Kurang Matang):**
   - Diprediksi Mentah ($20$ tandan $\times$ Rp $10.000$) = Rp $200.000$
   - Diprediksi Matang ($40$ tandan $\times$ Rp $40.000$) = **Rp $1.600.000$**
   - Diprediksi Lewat Matang ($10$ tandan $\times$ Rp $30.000$) = Rp $300.000$
   - Subtotal Baris 2 = Rp $2.100.000$
3. **Baris 3 (Aktual Matang):**
   - Diprediksi Kurang Matang ($25$ tandan $\times$ Rp $20.000$) = Rp $500.000$
   - Diprediksi Lewat Matang ($15$ tandan $\times$ Rp $15.000$) = Rp $225.000$
   - Subtotal Baris 3 = Rp $725.000$
4. **Baris 4 (Aktual Lewat Matang):**
   - Diprediksi Matang ($15$ tandan $\times$ Rp $90.000$) = **Rp $1.350.000$**
   - Subtotal Baris 4 = Rp $1.350.000$

#### Jawaban Butir 1: Total Kerugian Finansial Harian
$$\text{Total Kerugian} = \text{Rp } 825.000 + \text{Rp } 2.100.000 + \text{Rp } 725.000 + \text{Rp } 1.350.000 = \text{Rp } 5.000.000$$
Total kerugian finansial yang ditimbulkan oleh galat sortasi AI pada $1.000$ tandan buah adalah **Rp 5.000.000** (rata-rata kerugian Rp 5.000 per tandan buah yang diuji).

#### Jawaban Butir 2: Sumber Kerugian Terbesar
Dua sumber kerugian terbesar bagi pabrik adalah:
1. **Kurang Matang diprediksi Matang ($C_{23} = 40$ tandan):** Menyumbang **Rp 1.600.000** ($32{,}0\%$ dari total kerugian).
2. **Lewat Matang diprediksi Matang ($C_{43} = 15$ tandan):** Menyumbang **Rp 1.350.000** ($27{,}0\%$ dari total kerugian).

Secara gabungan, kesalahan melabeli buah yang belum siap atau terlalu matang sebagai "Matang Sempurna" menyumbangkan **59% total kerugian pabrik**!

#### Jawaban Butir 3: Rekomendasi Solusi Visi Komputer
1. **Penerapan Pencahayaan Buatan Terstandarisasi (*Diffused LED Tunnel*):**  
   Kesalahan terbesar terjadi antara kelas Kurang Matang dan Matang Sempurna akibat pantulan silau cahaya matahari (*specular reflection*) di loading ramp yang memutihkan warna kemerahan brondolan. Pemasangan terowongan lampu LED tertutup dengan suhu warna $5.000\text{ K}$ akan menstabilkan ekstraksi fitur warna `Hue_Mean`.
2. **Penambahan Fitur Tekstur & Estimasi Kelembekan Brondolan:**  
   Untuk membedakan buah Matang Sempurna dan Lewat Matang, model tidak boleh hanya mengandalkan warna RGB. Model perlu dilengkapi fitur tekstur fraktal (*Local Binary Patterns* / GLCM) dan pendeteksian brondolan lepas di sekitar janjang untuk mendeteksi kerutan pada kulit buah lewat matang.

---

## 3. Rubrik Penilaian Holistik & Analitik

| Kriteria Evaluasi | Bobot | Kinerja Luar Biasa (A: 85 - 100) | Kinerja Memadai (B: 70 - 84) | Kinerja Kurang (C: < 70) |
| :--- | :---: | :--- | :--- | :--- |
| **Kalkulasi & Agregasi Multi-Kelas** | 35% | Menghitung Presisi/Recall tiap kelas dengan tepat 100%, mampu menguraikan perbedaan matematis Macro vs Weighted secara lugas. | Mampu menghitung metrik per kelas namun terdapat kesalahan kecil saat pembobotan Weighted. | Salah membedakan pembagi baris (Recall) dan pembagi kolom (Presisi). |
| **Analisis Finansial PKS** | 35% | Mengintegrasikan perkalian matriks biaya secara sempurna, mengidentifikasi titik kerugian kritis OER/ALB, dan memberikan rekomendasi logis. | Menghitung total kerugian dengan benar namun rekomendasi teknis kurang berorientasi operasional PKS. | Salah menghitung total kerugian finansial atau tidak mampu membaca matriks biaya. |
| **Eksekusi Praktikum Komputasi** | 20% | Menjalankan notebook Python tanpa kendala, menghasilkan visualisasi heatmap ternormalisasi yang rapi dan komunikatif. | Menjalankan notebook namun visualisasi kurang informatif atau format label terpotong. | Mengalami error pada saat eksekusi kode evaluasi Scikit-Learn. |
| **Kerapian Dokumentasi & Argumentasi** | 10% | Laporan disusun sistematis, argumen didukung angka fakta, dan penulisan rapi sesuai kaidah akademik. | Laporan cukup lengkap namun penyampaian simpulan kurang tajam. | Laporan tidak lengkap atau format penulisan berantakan. |

---

## 4. Tips Instruktur dan Mitigasi Kekeliruan Praktikum

1. **Kekeliruan Penentuan Sumbu Normalisasi:**
   - Ingatkan mahasiswa bahwa `cm.sum(axis=1)[:, np.newaxis]` adalah normalisasi baris (Recall), sedangkan `cm.sum(axis=0)` adalah normalisasi kolom (Presisi). Normalisasi baris adalah standar industri yang paling lazim digunakan karena menjawab pertanyaan: *"Dari 100% buah mentah yang ada, berapa persen yang terdeteksi mentah?"*
2. **Hati-Hati dengan Penamaan Label Ordinal:**
   - Pastikan mahasiswa mengurutkan label secara konsisten: `[Mentah, Kurang Matang, Matang Sempurna, Lewat Matang]`. Jika urutan label teracak, analisis galat kelas bersebelahan tidak akan tampak di dekat diagonal utama.
