# AI Modul 11.6: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-06
* **Topik Utama**: Deteksi Objek Cepat Viola-Jones, Citra Integral, dan Haar Cascade Classifier
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Citra Integral & AdaBoost, 70 Menit Praktikum Komputer, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.6, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Sejarah dan signifikansi algoritma Viola-Jones, fitur Haar-like, dan limitasi model klasik pada wajah non-frontal.
* **Menit 25 - 50**: Pembuktian matematika efisiensi citra integral $O(1)$, mekanisme seleksi fitur AdaBoost, dan penolakan kaskade bertingkat.
* **Menit 50 - 120**: Praktikum laboratorium: verifikasi pembuktian citra integral, inisialisasi `CascadeClassifier`, dan pengujian parameter `scaleFactor` serta `minNeighbors`.
* **Menit 120 - 150**: Asesmen formatif mengenai penanganan alarm palsu pada tekstur pabrik dan pengantar Modul 11.7 (Video Processing).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Citra Integral** | Mampu menghitung dan membuktikan evaluasi area persegi panjang 4-titik secara analitis tanpa galat. | Memahami konsep citra integral namun keliru pada penentuan offset indeks matriks. | Gagal menghitung penjumlahan area menggunakan citra integral. |
| **Konfigurasi Parameter Kaskade** | Mengatur `scaleFactor`, `minNeighbors`, dan `minSize` secara proporsional sesuai jarak kamera industri. | Menggunakan parameter default tanpa memahami pengaruh perubahan nilai terhadap deteksi. | Salah memasukkan nilai parameter sehingga memicu over-detection atau no-detection. |
| **Implementasi Kode Deteksi** | Menulis skrip deteksi aman dengan verifikasi `empty()`, konversi grayscale, dan ekstraksi ROI wajah. | Mampu menjalankan deteksi namun lupa memeriksa ketersediaan berkas XML. | Mengirimkan citra BGR ke fungsi `detectMultiScale` sehingga program crash. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Kalkulasi Citra Integral Manual
Diberikan matriks $I = \begin{bmatrix} 2 & 3 & 1 \\ 4 & 1 & 5 \\ 3 & 2 & 2 \end{bmatrix}$ berdimensi $3 \times 3$.
1. **Perhitungan Matriks Citra Integral $ii(x, y)$**:
   * Baris 0:
     $ii(0, 0) = 2$
     $ii(0, 1) = 2 + 3 = 5$
     $ii(0, 2) = 5 + 1 = 6$
   * Baris 1:
     $ii(1, 0) = 2 + 4 = 6$
     $ii(1, 1) = 6 + (3 + 1) = 10$  (atau $5 + 4 + 1 = 10$)
     $ii(1, 2) = 6 + 10 + 5 - 5 = 16$
   * Baris 2:
     $ii(2, 0) = 6 + 3 = 9$
     $ii(2, 1) = 10 + 9 + 2 - 6 = 15$
     $ii(2, 2) = 16 + 15 + 2 - 10 = 23$
   Matriks Citra Integral:
   $$ii = \begin{bmatrix} 2 & 5 & 6 \\ 6 & 10 & 16 \\ 9 & 15 & 23 \end{bmatrix}$$
2. **Evaluasi Sub-Kotak $2 \times 2$ Kanan Bawah**:
   Kotak membentang dari $x \in [1, 2]$ dan $y \in [1, 2]$.
   Formula 4-titik sudut:
   $$\text{Sum} = ii(2, 2) + ii(0, 0) - ii(0, 2) - ii(2, 0) = 23 + 2 - 6 - 9 = 25 - 15 = 10$$
   Hasil penjumlahan manual: $1 + 5 + 2 + 2 = 10$. Terbukti identik sempurna!

### Jawaban Soal Konseptual 2: Evaluasi Sensitivitas Parameter Kaskade
Parameter yang harus disesuaikan untuk menekan alarm palsu (*false positives*) akibat tekstur serat karung goni adalah **menaikkan nilai `minNeighbors`** (misalnya dari nilai default 3 dinaikkan menjadi 5 atau 6).
* **Mekanisme Internal**: `minNeighbors` menentukan berapa banyak jendela kandidat deteksi yang saling tumpang tindih (*overlapping candidate bounding boxes*) yang harus sama-sama menyimpulkan adanya wajah di lokasi tersebut sebelum deteksi dinyatakan valid. Tekstur acak seperti serat karung goni mungkin secara kebetulan memicu satu atau dua fitur Haar pada skala tertentu, namun pola tersebut jarang sekali memicu deteksi yang konsisten pada berbagai pergeseran jendela tetangga. Dengan menaikkan `minNeighbors`, kandidat deteksi palsu yang hanya memiliki 1 - 2 pendukung akan langsung digugurkan (*suppressed*).
