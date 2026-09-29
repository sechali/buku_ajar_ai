# AI Modul 11.2: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-02
* **Topik Utama**: Pembacaan Citra, Slicing ROI, Transformasi Afina, dan Interpolasi
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Geometri, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.2, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Mekanisme `cv2.imread()`, parameter flag, dan penanganan kesalahan berkas nihil (`NoneType`).
* **Menit 25 - 50**: Formulasi aljabar linier transformasi afina 2D: translasi, rotasi koordinat dengan pusat sembarang, dan perbandingan metode interpolasi (`INTER_AREA` vs `INTER_LINEAR`).
* **Menit 50 - 120**: Praktikum laboratorium: ekstraksi ROI tandan sawit dari citra konveyor, perancangan matriks rotasi, dan implementasi teknik letterboxing proporsional.
* **Menit 120 - 150**: Asesmen formatif mengenai bahaya distorsi aspek rasio pada morfometri tanaman dan pengantar Modul 11.3 (Color Conversion).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Penanganan Berkas Citra** | Mengimplementasikan validasi `if img is None` dan eksepsi error secara konsisten dan aman. | Menggunakan `imread` dengan benar namun lupa menyertakan validasi berkas nihil. | Mengabaikan pemeriksaan berkas sehingga menghasilkan error `NoneType`. |
| **Pemotongan ROI & Manipulasi** | Mampu melakukan slicing ROI dua dimensi dengan koordinat aman dan kloning `.copy()`. | Melakukan slicing dengan benar namun lupa menggunakan method `.copy()`. | Tertukar antara indeks baris (Y) dan kolom (X) dalam slicing array. |
| **Transformasi Afina & Resizing** | Merumuskan matriks rotasi afina dan menerapkan teknik letterboxing proporsional tanpa distorsi. | Mampu merotasi citra namun fungsi resize langsung memampatkan citra tanpa letterbox. | Salah mendefinisikan matriks transformasi sehingga citra terpotong atau hilang. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Matriks Translasi Affine
Transformasi translasi 2D dirumuskan sebagai:
$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$
Dengan pergeseran $t_x = +50$ piksel dan $t_y = -30$ piksel:
$$M = \begin{bmatrix} 1.0 & 0.0 & 50.0 \\ 0.0 & 1.0 & -30.0 \end{bmatrix}$$
Representasi matriks dalam NumPy:
```python
M = np.float32([[1, 0, 50], [0, 1, -30]])
```

### Jawaban Soal Konseptual 2: Analisis Distorsi Aspek Rasio
Diketahui: Ukuran asli $W_{\text{orig}} = 1200, H_{\text{orig}} = 800$. Ukuran target $W_{\text{target}} = 300, H_{\text{target}} = 300$.
1. **Rasio Penskalaan**:
   * Sumbu Horizontal: $s_x = \frac{300}{1200} = 0.25$ (faktor pengecilan 4 kali lipat).
   * Sumbu Vertikal: $s_y = \frac{300}{800} = 0.375$ (faktor pengecilan 2.67 kali lipat).
   * Rasio Distorsi: $\frac{s_x}{s_y} = \frac{0.25}{0.375} \approx 0.667$.
2. **Dampak terhadap Morfometri Tanaman**:
   Pengecilan horizontal yang lebih agresif dibandingkan vertikal akan memipihkan objek secara mendatar. Tajuk pohon kelapa sawit yang awalnya berbentuk melingkar simetris ($C \approx 1.0$) akan terdistorsi menjadi bentuk elips lonjong, sehingga nilai kebulatan (*circularity*) $C = \frac{4\pi A}{P^2}$ akan turun secara drastis secara artifisial. Akibatnya, algoritma deteksi kanopi rusak akan salah mengklasifikasikan pohon sehat sebagai pohon cacat pelepah (*false positive pest damage*).
