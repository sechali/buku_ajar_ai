# AI Modul 11.4: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-04
* **Topik Utama**: Binerisasi Citra, Formulasi Otsu, dan Adaptive Thresholding
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Derivasi Otsu, 70 Menit Praktikum Komputer, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.4, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Konsep binerisasi citra, pembagian kelas foreground-background, dan kelemahan thresholding global statis.
* **Menit 25 - 50**: Pembuktian matematis kriteria maksimasi varians antar-kelas Otsu $\sigma_b^2(T)$ dan mekanisme Adaptive Gaussian.
* **Menit 50 - 120**: Praktikum komputer: pembuatan citra sintetis kanopi berbayangan, perbandingan global vs Otsu vs adaptif, dan visualisasi masker.
* **Menit 120 - 150**: Pembahasan potensi kendala teknis ukuran jendela ganjil dan pengantar Modul 11.5 (Contour Detection).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teoretis Otsu** | Menguraikan langkah penurunan varians antar-kelas dan syarat histogram bimodal secara runtut. | Memahami fungsi Otsu namun kurang mendalam pada formulasi varians statistik. | Gagal membedakan antara varians intra-kelas dan varians antar-kelas. |
| **Implementasi Adaptive Threshold** | Menerapkan `cv2.adaptiveThreshold()` dengan penentuan parameter `blockSize` ganjil dan konstanta $C$ yang tepat. | Mampu menjalankan fungsi adaptif namun memilih ukuran jendela yang terlalu kecil. | Terjadi galat komputasi akibat memasukkan angka genap pada `blockSize`. |
| **Analisis Hasil Binarisasi** | Menginterpretasi mengapa metode adaptif unggul menghadapi gradien pencahayaan lapangan secara komprehensif. | Mengetahui bahwa metode adaptif lebih baik namun analisis teknisnya masih minim. | Tidak mampu membaca hasil visualisasi perbedaan masker ketiga metode. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Analisis Varians Otsu
Diketahui 10 piksel: $[10, 12, 15, 18, 20, 180, 190, 200, 210, 220]$, ambang batas $T = 50$.
1. **Probabilitas Kumulatif Kelas**:
   * Kelas $\mathcal{C}_0$ (intensitas $\le 50$): ada 5 piksel $[10, 12, 15, 18, 20]$. Maka $\omega_0 = \frac{5}{10} = 0.5$.
   * Kelas $\mathcal{C}_1$ (intensitas $> 50$): ada 5 piksel $[180, 190, 200, 210, 220]$. Maka $\omega_1 = \frac{5}{10} = 0.5$.
2. **Nilai Rata-rata Kelas**:
   * $\mu_0 = \frac{10 + 12 + 15 + 18 + 20}{5} = \frac{75}{5} = 15.0$
   * $\mu_1 = \frac{180 + 190 + 200 + 210 + 220}{5} = \frac{1000}{5} = 200.0$
3. **Varians Antar-Kelas**:
   $$\sigma_b^2(T) = \omega_0 \omega_1 (\mu_0 - \mu_1)^2 = (0.5)(0.5)(15.0 - 200.0)^2 = 0.25 \times (-185.0)^2 = 0.25 \times 34225 = 8556.25$$
   Nilai ini sangat tinggi karena kedua kelompok data terpisah secara sempurna oleh lembah histogram lebar di antara 20 dan 180, sehingga memaksimalkan keterpisahan kedua kelas.

### Jawaban Soal Konseptual 2: Fenomena Objek Berlubang (Hollow Mask)
Pada Adaptive Thresholding, nilai ambang dihitung lokal per jendela $B \times B$. Jika diameter tajuk daun adalah 150 piksel namun dipilih `blockSize = 7`, maka di bagian tengah tajuk daun yang seragam, seluruh tetangga dalam jendela $7 \times 7$ memiliki intensitas yang hampir sama (misalnya sekitar $220$). Nilai ambang lokal dihitung sebagai:
$$T = \text{Mean}(I_{\text{lokal}}) - C \approx 220 - 5 = 215$$
Karena piksel di tengah tajuk bernilai 220, jika ada sedikit fluktuasi di mana piksel bernilai 214, piksel tersebut langsung diputus menjadi 0 (hitam). Lebih parah lagi, jika intensitas seragam sempurna dan $C$ positif kecil, maka kontras lokal dianggap nol sehingga algoritma menduga tidak ada tepi objek, menyebabkan bagian dalam tajuk tanaman terlubangi secara artifisial. Solusinya adalah memperbesar `blockSize` melebihi diameter objek (misalnya $B = 151$ atau $201$) agar jendela mencakup batas tepi objek dan latar belakang.
