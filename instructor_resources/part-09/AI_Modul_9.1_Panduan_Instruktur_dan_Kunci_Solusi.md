# AI Modul 9.1: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-09-01
* **Topik Utama**: Konsep Fundamental Deep Learning & Hierarchical Feature Learning
* **Alokasi Waktu**: 150 Menit (50 Menit Kuliah Interaktif, 70 Menit Praktikum Terbimbing, 30 Menit Diskusi & Evaluasi)
* **Bahan Ajar & Alat**: Slide Presentasi Konsep, Diktat Teori Modul 9.1, Jupyter Notebook Praktikum, Proyektor, Komputer Praktikum dengan Lingkungan Python 3.10.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 20**: Pengantar paradima komputasi kecerdasan buatan: perbedaan mendasar machine learning klasik vs deep learning. Pembahasan studi kasus kegagalan ekstraksi fitur manual pada citra perkebunan skala luas.
* **Menit 20 - 50**: Landasan matematis Teorema Aproksimasi Universal, formulasi komposisi fungsi bertingkat, dan representasi tensor multi-dimensi.
* **Menit 50 - 120**: Praktikum hands-on di laboratorium: menjalankan implementasi ekstraksi fitur bertingkat dan menguji model aproksimator non-linier menggunakan NumPy murni.
* **Menit 120 - 150**: Pembahasan kesalahan umum (*pitfalls*), evaluasi kuis formatif, dan pengantar modul berikutnya (Artificial Neural Network).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teori Komparasi** | Mampu membedakan representasi fitur manual vs otomatis secara terperinci dengan contoh agronomis konkret. | Mampu menjelaskan konsep dasar perbedaan model dangkal dan dalam, namun minim elaborasi teknis. | Gagal membedakan mekanisme kerja machine learning klasik dan deep learning. |
| **Implementasi NumPy** | Mampu menyusun skrip ekstraksi fitur multi-lapisan tanpa error dengan aljabar linier yang efisien. | Mampu menjalankan skrip praktikum namun kesulitan memodifikasi dimensi matriks bobot. | Menghasilkan galat dimensi tensor (*shape mismatch*) tanpa mampu melakukan debugging mandiri. |
| **Analisis Hasil Aproksimasi** | Menginterpretasi kurva aproksimasi dan nilai RMSE secara kuantitatif serta mengaitkannya dengan kapasitas arsitektur. | Menghitung nilai RMSE akhir namun analisis kurva visual masih bersifat umum. | Tidak mampu menyimpulkan konvergensi fungsi dan makna dari nilai loss. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Komposisi Linier
Secara matematis, output dari lapisan linier pertama adalah:
$$a^{(1)} = W^{(1)} x + b^{(1)}$$
Lapisan kedua:
$$a^{(2)} = W^{(2)} a^{(1)} + b^{(2)} = W^{(2)} (W^{(1)} x + b^{(1)}) + b^{(2)} = (W^{(2)} W^{(1)}) x + (W^{(2)} b^{(1)} + b^{(2)})$$
Jika didefinisikan matriks gabungan $W' = W^{(2)} W^{(1)}$ dan vektor bias gabungan $b' = W^{(2)} b^{(1)} + b^{(2)}$, maka:
$$a^{(2)} = W' x + b'$$
Dengan induksi matematika hingga lapisan ke-$L$, seluruh perkalian matriks bobot berurutan dapat diringkas menjadi sebuah matriks linier tunggal:
$$W_{	ext{net}} = W^{(L)} W^{(L-1)} \dots W^{(1)} \quad 	ext{dan} \quad b_{	ext{net}} = \sum_{l=1}^{L} \left( \prod_{j=l+1}^{L} W^{(j)} ight) b^{(l)}$$
Dengan demikian, susunan lapisan linier bertingkat tanpa fungsi aktivasi non-linier tidak mampu meningkatkan kapasitas representasi ruang hipotesis dan secara aljabar tereduksi menjadi regresi linier biasa.

### Jawaban Soal Konseptual 2: Kedalaman vs Lebar
Klaim tersebut tidak tepat secara praktis. Meskipun Teorema Aproksimasi Universal membuktikan keberadaan eksistensi aproksimator 1 lapisan tersembunyi, teorema tersebut tidak memberikan jaminan mengenai efisiensi jumlah neuron ($N$). Untuk fungsi non-linier kompleks dan berdimensi tinggi ($d$), jumlah neuron pada 1 lapisan tersembunyi dapat membengkak secara eksponensial ($O(2^d)$). Sebaliknya, arsitektur dalam (*deep architectures*) memanfaatkan hierarki komposisionalitas (*compositionality*), di mana fitur tingkat tinggi dibangun dari kombinasi fitur tingkat rendah, sehingga mereduksi jumlah parameter yang dibutuhkan menjadi polinomial serta meningkatkan generalisasi pada data lingkungan terbuka.
