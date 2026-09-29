# AI Modul 11.1: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-01
* **Topik Utama**: Pengenalan OpenCV, Arsitektur Sistem, dan Struktur Matriks Citra
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Arsitektur, 70 Menit Praktikum Komputer, 30 Menit Evaluasi & Diskusi)
* **Bahan Ajar & Alat**: Slide Presentasi Modul 11.1, Diktat Teori, Jupyter Notebook Praktikum, Python 3.10 dengan OpenCV 4.x.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Pengenalan ekosistem OpenCV: sejarah, arsitektur backend C++, binding Python, struktur `core`, `imgproc`, dan akselerasi OpenCL.
* **Menit 25 - 50**: Representasi matriks citra NumPy: koordinat `(x, y)` vs indeks `[y, x]`, format warna BGR, dan teori saturasi numerik.
* **Menit 50 - 120**: Praktikum laboratorium: inisialisasi lingkungan OpenCV, pembuatan citra sintetis kanopi sawit, pembuktian modulo overflow, dan benchmark Full HD.
* **Menit 120 - 150**: Pembahasan kekeliruan metodologis (BGR vs RGB), kuis pemahaman, dan pengantar modul 11.2 (Image Reading & Manipulation).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Arsitektur OpenCV** | Menjelaskan peran C++ core, SIMD, dan pemetaan NumPy array tanpa kesalahan konsep. | Memahami fungsi dasar OpenCV namun kurang memahami peran akselerasi perangkat keras. | Mengira OpenCV ditulis sepenuhnya dalam Python murni. |
| **Operasi Aritmatika Saturasi** | Menjelaskan perbedaan saturated arithmetic vs modulo overflow secara matematis dan implikasi visualnya. | Mampu menunjukkan contoh overflow namun kurang memahami formulasi matematis saturasi. | Tidak memahami penyebab perbedaan output antara `+` dan `cv2.add()`. |
| **Praktikum & Benchmarking** | Berhasil menjalankan uji benchmark Full HD, memvalidasi integritas matriks, dan menganalisis grafik latensi. | Mampu menjalankan notebook praktikum namun kesulitan memodifikasi parameter resolusi citra. | Terjadi galat sintaks akibat ketidaktahuan pengindeksan dimensi baris/kolom. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Analisis Saturasi Aritmatika
Diketahui $p_1 = 200$, $p_2 = 75$ bertipe `uint8` (rentang $0 - 255$):
1. **NumPy Biasa**:
   $$200 + 75 = 275 \equiv 275 \pmod{256} = 19$$
   Nilai piksel tergulung (*wrapped around*) menjadi 19 (tampak sangat gelap).
2. **OpenCV `cv2.add()`**:
   $$\min(255, 200 + 75) = \min(255, 275) = 255$$
   Nilai piksel mencapai saturasi putih sempurna.
3. **Dampak Fatal di Perkebunan**: Jika diterapkan pada peningkatan kontras area buah sawit matang (berwarna jingga/merah cerah), operasi modulo NumPy akan mengubah area buah yang sangat terang menjadi bercak gelap pekat (nilai 19), sehingga sistem sortasi otomatis keliru mendiagnosa buah matang sebagai buah busuk atau berlubang (*false defect detection*).

### Jawaban Soal Konseptual 2: Evaluasi Koordinat Spasial
1. **Sintaks `cv2.circle()`**:
   Parameter: `cv2.circle(img, center, radius, color, thickness)`.
   Koordinat pusat adalah $(x=400, y=300)$:
   ```python
   cv2.circle(image, (400, 300), 50, (0, 255, 0), 2)
   ```
2. **Sintaks Pengirisan (*Slicing*) NumPy untuk Bounding Box**:
   Kotak pembatas membentang dari $x_{\min} = 400 - 50 = 350$ hingga $x_{\max} = 400 + 50 = 450$, dan $y_{\min} = 300 - 50 = 250$ hingga $y_{\max} = 300 + 50 = 350$.
   Karena NumPy menggunakan urutan `[y, x]`:
   ```python
   bounding_box_tajuk = image[250:350, 350:450].copy()
   ```
