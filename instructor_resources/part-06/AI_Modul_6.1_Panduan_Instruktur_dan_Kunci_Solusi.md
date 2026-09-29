# AI Modul 6.1: Panduan Instruktur dan Kunci Solusi Evaluasi Klasifikasi - Akurasi, Presisi, Recall, dan F-Beta Score

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) dan Panduan Pedagogis

### 1.1 Informasi Umum Modul
- **Mata Kuliah:** Kecerdasan Buatan dan Sains Data Pertanian Presisi
- **Modul:** 6.1 (Evaluasi Klasifikasi: Akurasi, Presisi, Sensitivitas/Recall, F-Beta)
- **Sasaran Peserta:** Mahasiswa Program Studi Agroteknologi, Agribisnis, dan Teknik Pertanian INSTIPER Yogyakarta
- **Alokasi Waktu:** 150 Menit (1 Sesi Tatap Muka / Praktikum Komputasi)

### 1.2 Tujuan Instruksional Khusus (TIK)
Pada akhir sesi ini, mahasiswa diharapkan dapat:
1. Membedakan secara analitis antara Kesalahan Tipe I (*False Positive*) dan Kesalahan Tipe II (*False Negative*) dalam konteks agronomi kebun.
2. Membuktikan secara matematis bahaya mempercayai metrik Akurasi pada populasi penyakit tanaman yang langka (*Accuracy Paradox*).
3. Menghitung secara manual dan memprogram metrik Presisi, Recall, F1-Score, dan F2-Score.
4. Menemukan ambang batas probabilitas klasifikasi ($\tau$) yang meminimalkan total kerugian operasional kebun berbasis parameter biaya riil.

### 1.3 Alokasi Waktu Pembelajaran (150 Menit)

| Sesi | Durasi | Aktivitas Instruktur | Aktivitas Mahasiswa | Output / Indikator |
| :---: | :---: | :--- | :--- | :--- |
| **I** | 20 Menit | **Apersepsi & Fenomena Lapangan:** Membuka sesi dengan studi kasus "Model AI 99% Akurat yang Membiarkan Kebun Sawit Hancur oleh Ganoderma". | Diskusi interaktif mengenai risiko penyakit menular vs biaya obat. | Mahasiswa menyadari kelemahan fatal metrik akurasi tunggal. |
| **II** | 35 Menit | **Bedah Teoretis & Formulasi Matematis:** Membahas ruang keputusan, Presisi, Recall, Spesifisitas, F1-Score, dan F-Beta. | Mencatat, menelaah dimensi simbol, dan melafalkan cara baca rumus. | Pemahaman konseptual dan penguasaan formula matematis. |
| **III** | 50 Menit | **Hands-On Coding Lab:** Memandu eksekusi Jupyter Notebook `AI_Modul_6.1_Accuracy_Precision_Recall.ipynb`. | Menjalankan model logreg, plotting kurva PR, dan komputasi kurva biaya. | Skrip berjalan lancar (0 error) dan menghasilkan grafik visual. |
| **IV** | 30 Menit | **Diskusi HOTS & Optimasi Biaya:** Membedah studi kasus kerugian finansial kumbang tanduk. | Menghitung trade-off biaya dan mempresentasikan rekomendasi. | Kemampuan analisis kritis sintesis bisnis-agronomi. |
| **V** | 15 Menit | **Refleksi & Post-Test Cepat:** Menyimpulkan materi dan memberikan jembatan ke Confusion Matrix. | Mengisi kuis reflektif 3 butir soal konsep. | Evaluasi pemahaman formatif langsung. |

---

## 2. Kunci Jawaban Lengkap dan Pembahasan Evaluasi Mandiri Mahasiswa

### 2.1 Pembahasan Soal HOTS 1: Analisis Dekonstruksi Paradoks Akurasi
**Soal:** Model pengujian ulat api (*Setothosea asigna*) pada $10.000$ daun sawit ($100$ daun sakit, $9.900$ daun sehat). Model malas (*naive*) selalu memprediksi seluruh daun sebagai "SEHAT".

**Langkah Penyelesaian Matematis:**
1. **Identifikasi Elemen Matriks:**
   - Karena model memprediksi semua daun "SEHAT" ($0$), maka:
     - $TP = 0$ (tidak ada daun sakit yang terdeteksi)
     - $FP = 0$ (tidak ada daun sehat yang dituduh sakit)
     - $FN = 100$ (seluruh $100$ daun sakit lolos sebagai sehat)
     - $TN = 9.900$ (seluruh daun sehat terprediksi sehat)
     - Total sampel $N = 10.000$

2. **Perhitungan Metrik:**
   - **Akurasi:**
     $$\text{Accuracy} = \frac{TP + TN}{N} = \frac{0 + 9.900}{10.000} = \frac{9.900}{10.000} = 99{,}0\%$$
   - **Sensitivitas / Recall:**
     $$\text{Recall} = \frac{TP}{TP + FN} = \frac{0}{0 + 100} = \frac{0}{100} = 0{,}0\%$$
   - **Presisi:**
     $$\text{Precision} = \frac{TP}{TP + FP} = \frac{0}{0 + 0} \implies \text{Tak Terdefinisi (atau 0.0)}$$
   - **Skor F1:**
     $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = 2 \times \frac{0 \times 0}{0 + 0} = 0{,}0\%$$

**Pembahasan Pedagogis:**
Nilai akurasi $99{,}0\%$ memberikan ilusi keunggulan palsu karena mencerminkan proporsi kelas mayoritas sehat. Namun, nilai Recall $0{,}0\%$ dan F1-Score $0{,}0\%$ membuktikan secara telak bahwa model tersebut sama sekali tidak memiliki kemampuan diagnostik. Dalam operasional perkebunan, model ini akan menyebabkan $100$ koloni ulat api berkembang biak tanpa hambatan hingga menyebabkan defoliasi kanopi secara menyeluruh.

---

### 2.2 Pembahasan Soal HOTS 2: Dilema Ambang Batas Sortasi TBS di Loading Ramp PKS
**Soal:** Pemilah otomatis TBS membagi buah menjadi "MATANG SEMPURNA" (Positif) dan "MENTAH/LEWAT MATANG" (Negatif). Jika ambang batas diturunkan dari $\tau = 0{,}50$ menjadi $\tau = 0{,}20$:

**Pembahasan:**
1. **Dampak Matematis Penurunan Ambang Batas:**
   - Menurunkan ambang batas ke $\tau = 0{,}20$ berarti model menjadi jauh lebih longgar dan permisif dalam mencap buah sebagai "MATANG".
   - **Recall melonjak tinggi:** Hampir semua buah yang benar-benar matang akan berhasil masuk (*low FN*).
   - **Presisi merosot drastis:** Banyak buah yang sebenarnya mentah atau lewat matang akan ikut terlabeli sebagai buah matang (*high FP*).

2. **Analisis Dampak Bisnis Pabrik Kelapa Sawit (PKS):**
   - **Penurunan ambang batas ini MERUGIKAN PKS!**
   - Di pabrik kelapa sawit, mencampurkan buah mentah (*unripe*) ke dalam rebusan (*sterilizer*) mengakibatkan brondolan tidak terlepas sempurna dari janjang, menurunkan efisiensi ekstraksi minyak (*Oil Extraction Rate* - OER anjlok).
   - Mencampurkan buah lewat matang (*overripe*) memicu lonjakan Asam Lemak Bebas (*Free Fatty Acid* - FFA $> 5\%$) akibat hidrolisis enzimatik, sehingga CPO terkena penalti diskon harga di pasar ekspor.
   - Oleh karena itu, pada tahap sortasi PKS, manajer pabrik **wajib mempertahankan Presisi Tinggi** (ambang batas ketat $\tau \ge 0{,}50$ atau bahkan $\tau = 0{,}70$) guna menjamin hanya buah bermutu prima yang masuk ke proses pengolahan.

---

### 2.3 Pembahasan Tantangan Komputasi Kumbang Tanduk (*Oryctes rhinoceros*)
**Data Kasus:** $N = 1.000$ pokok. $TP = 70$, $FP = 30$, $FN = 10$, $TN = 890$.
- $C_{FP} = \text{Rp } 50.000$ (inspeksi mandor).
- $C_{FN} = \text{Rp } 400.000$ (kematian titik tumbuh).

#### Jawaban Butir 1: Metrik Dasar Model Utama
1. **Akurasi:**
   $$\text{Accuracy} = \frac{70 + 890}{1.000} = \frac{960}{1.000} = 96{,}0\%$$
2. **Presisi:**
   $$\text{Precision} = \frac{70}{70 + 30} = \frac{70}{100} = 70{,}0\%$$
3. **Recall:**
   $$\text{Recall} = \frac{70}{70 + 10} = \frac{70}{80} = 87{,}5\%$$
4. **Spesifisitas:**
   $$\text{Specificity} = \frac{890}{890 + 30} = \frac{890}{920} \approx 96{,}74\%$$
5. **Skor F1:**
   $$F_1 = 2 \times \frac{0{,}70 \times 0{,}875}{0{,}70 + 0{,}875} = \frac{1{,}225}{1{,}575} \approx 0{,}7778 \quad (77{,}78\%)$$

#### Jawaban Butir 2: Perhitungan F-Beta
1. **Skor $F_2$ ($\beta = 2{,}0$):**
   $$F_2 = (1 + 2^2) \times \frac{0{,}70 \times 0{,}875}{(2^2 \times 0{,}70) + 0{,}875} = 5 \times \frac{0{,}6125}{2{,}80 + 0{,}875} = \frac{3{,}0625}{3{,}675} \approx 0{,}8333 \quad (83{,}33\%)$$
2. **Skor $F_{0.5}$ ($\beta = 0{,}5$):**
   $$F_{0.5} = (1 + 0{,}25) \times \frac{0{,}70 \times 0{,}875}{(0{,}25 \times 0{,}70) + 0{,}875} = 1{,}25 \times \frac{0{,}6125}{0{,}175 + 0{,}875} = \frac{0{,}765625}{1{,}05} \approx 0{,}7292 \quad (72{,}92\%)$$
- **Rekomendasi Manajerial:** Manajer kebun wajib menggunakan **Skor $F_2$** karena kerugian akibat kumbang tanduk yang lolos ($C_{FN} = \text{Rp } 400.000$) delapan kali lipat lebih besar daripada biaya inspeksi pohon sehat ($C_{FP} = \text{Rp } 50.000$).

#### Jawaban Butir 3: Analisis Komparasi Kerugian Finansial Antar-Model
- **Total Biaya Kesalahan Model Utama:**
  $$\text{Total Cost}_1 = (30 \times \text{Rp } 50.000) + (10 \times \text{Rp } 400.000) = \text{Rp } 1.500.000 + \text{Rp } 4.000.000 = \text{Rp } 5.500.000$$

- **Total Biaya Kesalahan Model Alternatif ($FP = 80, FN = 2$):**
  $$\text{Total Cost}_2 = (80 \times \text{Rp } 50.000) + (2 \times \text{Rp } 400.000) = \text{Rp } 4.000.000 + \text{Rp } 800.000 = \text{Rp } 4.800.000$$

- **Kesimpulan Bisnis:**  
  Meskipun Model Alternatif menghasilkan alarm palsu jauh lebih banyak ($80$ vs $30$), **Model Alternatif lebih menghemat uang perusahaan sebesar Rp 700.000** (Rp 4.800.000 vs Rp 5.500.000) karena berhasil menekan jumlah kematian pokok dari $10$ menjadi hanya $2$ pokok. Ini membuktikan bahwa dalam agribisnis, meminimalkan False Negative memiliki nilai ekonomi yang sangat tinggi.

---

## 3. Rubrik Penilaian Kinerja Praktikum Mahasiswa

| Kriteria Evaluasi | Bobot | Indikator Kinerja Luar Biasa (A: 85 - 100) | Indikator Kinerja Memadai (B: 70 - 84) | Indikator Kinerja Kurang (C: < 70) |
| :--- | :---: | :--- | :--- | :--- |
| **Pemahaman Teoretis & Rumus** | 30% | Menjelaskan relasi seluruh metrik secara tepat, memahami pembobotan F-Beta, dan mengartikulasikan cara baca rumus secara verbal. | Menghitung metrik dengan benar namun kurang mendalam dalam menjelaskan pergeseran ambang batas. | Keliru dalam membedakan antara Presisi dan Recall atau salah rumus dasar. |
| **Eksekusi Kode Komputasi** | 35% | Menjalankan seluruh notebook tanpa error, mengimplementasikan optimasi threshold, dan memprogram kalkulasi biaya secara vektorisasi. | Menjalankan notebook standar namun kesulitan saat memodifikasi fungsi kerugian biaya. | Terjadi syntax error atau gagal mengimpor pustaka evaluasi Scikit-Learn. |
| **Analisis Finansial-Agronomi** | 25% | Mengintegrasikan parameter biaya agribisnis nyata ke dalam pemilihan model terbaik dan memberikan rekomendasi manajerial berbasis data. | Menyebutkan biaya kesalahan namun tidak mampu membuktikan model mana yang paling hemat. | Menilai performa model hanya berdasarkan angka akurasi persentase semata. |
| **Dokumentasi & Presentasi** | 10% | Grafik disajikan bersih dengan anotasi informatif, kode berstandar PEP 8, serta interpretasi ringkas dan runtut. | Grafik terbaca dengan baik namun anotasi minim. | Tampilan grafik berantakan atau format laporan tidak rapi. |

---

## 4. Kekeliruan Umum Mahasiswa (*Common Pitfalls*) dan Tips Troubleshooting

1. **Potensi Galat `zero_division` pada Scikit-Learn:**
   - *Masalah:* Saat model tidak memprediksi satupun kelas positif ($TP=0, FP=0$), pemanggilan `precision_score()` akan memicu peringatan *UndefinedMetricWarning* dan mengembalikan nilai $0.0$.
   - *Solusi Instruktur:* Tekankan mahasiswa untuk selalu menyertakan parameter `zero_division=0` pada fungsi evaluasi Scikit-Learn.
2. **Tertukarnya Nilai Aktual dan Prediksi pada Confusion Matrix:**
   - *Masalah:* Mahasiswa sering memanggil `confusion_matrix(y_pred, y_test)` terbalik.
   - *Solusi Instruktur:* Ingatkan urutan standar Scikit-Learn adalah `(y_true, y_pred)`. Jika terbalik, posisi False Positive dan False Negative akan tertukar 180 derajat!
3. **Miskonsepsi Ambang Batas Default 0.50:**
   - *Masalah:* Mahasiswa menganggap angka $\tau = 0{,}50$ adalah hukum mutlak yang tidak boleh diubah.
   - *Solusi Instruktur:* Jelaskan bahwa $0{,}50$ hanyalah konvensi simetris matematis. Dalam dunia agribisnis, titik ambang batas selalu ditentukan oleh perbandingan matriks biaya ($C_{FP}$ vs $C_{FN}$).
