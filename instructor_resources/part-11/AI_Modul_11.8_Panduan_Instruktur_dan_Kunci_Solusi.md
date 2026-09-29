# AI Modul 11.8: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-08
* **Topik Utama**: Deteksi Gerak, Frame Differencing, MOG2, dan Optical Flow
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Pemodelan Latar Belakang, 70 Menit Praktikum Komputer, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.8, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Konsep deteksi gerak temporal, limitasi frame differencing langsung, dan fenomena objek berlubang (*ghosting*).
* **Menit 25 - 50**: Matematika Gaussian Mixture Model MOG2, deteksi dan eliminasi bayangan, serta persamaan Optical Flow Lucas-Kanade.
* **Menit 50 - 120**: Praktikum laboratorium: simulasi video pergerakan truk buah, penerapan `createBackgroundSubtractorMOG2`, dan pemfilteran bayangan.
* **Menit 120 - 150**: Asesmen formatif dan diskusi penanganan kamera bergoyang pada pos pengawas luar ruangan kebun.

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teori Gerak** | Menguraikan perbedaan mendasar Frame Differencing, MOG2, dan Optical Flow secara komprehensif. | Memahami fungsi subtractor namun kurang memahami peran pemodelan probabilitas Gaussian. | Mengira deteksi gerak bekerja dengan mencari perubahan warna acak. |
| **Implementasi MOG2 & Filter Bayangan** | Mengonfigurasi parameter MOG2 dan menyaring piksel abu-abu bayangan ($127$) dengan thresholding biner. | Mampu menjalankan MOG2 namun membiarkan bayangan masuk ke dalam kontur objek. | Terjadi galat saat memproses sekuens video atau salah menerapkan fungsi apply. |
| **Analisis Hasil Segmentasi** | Mengevaluasi performa deteksi pada kondisi objek bergerak vs objek berhenti secara kritis. | Menampilkan grafik dan citra hasil olahan namun analisis perbandingannya masih minim. | Tidak mampu menginterpretasi perbedaan visual antara Frame Diff dan MOG2. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Analisis Fenomena Objek Berhenti
1. **Pada Metode Frame Differencing**:
   Rumus: $D_t = |I_t - I_{t-1}|$.
   Ketika truk berhenti total, frame pada waktu $t$ persis sama dengan frame pada waktu $t-1$ ($I_t = I_{t-1}$). Akibatnya, nilai selisih $D_t$ langsung menjadi $0$ di seluruh area truk. Truk yang sedang berhenti membongkar muatan akan **hilang total (*completely disappears*)** dari masker deteksi gerak, seolah-olah truk tersebut lenyap dari lokasi.
2. **Pada Metode MOG2**:
   Algoritma MOG2 memiliki parameter memori `history = 500` (pada 30 FPS, setara dengan rentang waktu sekitar $16.7\text{ detik}$).
   * Selama $10 - 15$ detik pertama setelah truk berhenti, MOG2 tetap mendeteksi badan truk sebagai *foreground* objek bergerak karena nilai intensitas truk masih sangat menyimpang dari model latar belakang jalan kosong sebelumnya.
   * Namun seiring berjalannya waktu (setelah melewati ~17 detik hingga 2 menit), model campuran Gaussian pada lokasi tersebut mulai memperbarui nilai rata-rata ($\mu_k$) dan bobotnya ($\omega_k$) untuk mengasimilasi piksel truk ke dalam model latar belakang baru. Akhirnya, truk yang diam tersebut secara bertahap dianggap sebagai bagian permanen dari latar belakang (*absorbed into background*), dan masker gerak kembali menjadi hitam. Jika truk kemudian bergerak pergi, bekas lokasi parkirnya akan memicu deteksi semu (*ghost artifact*) sementara waktu hingga model beradaptasi kembali.

### Jawaban Soal Konseptual 2: Masalah Solusi Tak Tentu (*Aperture Problem*) Aliran Optik
Persamaan aliran optik adalah:
$$I_x u + I_y v + I_t = 0$$
Ini adalah satu persamaan linier dengan dua variabel bebas yang tidak diketahui: $u$ (kecepatan horizontal) dan $v$ (kecepatan vertikal). Secara aljabar, satu persamaan dengan dua variabel memiliki jumlah solusi tak terhingga. Fenomena fisik ini dikenal sebagai **Aperture Problem** (masalah lubang intip): jika kita melihat pergerakan garis lurus melalui celah sempit, kita hanya dapat mengamati komponen gerak yang tegak lurus terhadap garis (*normal flow*), sedangkan komponen gerak yang sejajar dengan garis tidak dapat ditentukan.
* **Solusi Lucas-Kanade**: Algoritma Lucas-Kanade menyelesaikan masalah ini dengan mengasumsikan bahwa seluruh piksel di dalam jendela lingkungan lokal kecil (misalnya jendela $3 \times 3$ yang memuat 9 piksel) memiliki vektor kecepatan $(u, v)$ yang seragam. Dengan demikian, diperoleh 9 persamaan linier untuk 2 variabel tak diketahui:
  $$\begin{bmatrix} I_{x1} & I_{y1} \\ I_{x2} & I_{y2} \\ \vdots & \vdots \\ I_{x9} & I_{y9} \end{bmatrix} \begin{bmatrix} u \\ v \end{bmatrix} = - \begin{bmatrix} I_{t1} \\ I_{t2} \\ \vdots \\ I_{t9} \end{bmatrix} \implies A \mathbf{v} = b$$
  Sistem persamaan overdetermined ini kemudian diselesaikan secara unik menggunakan metode kuadrat terkecil (*least squares method*): $\mathbf{v} = (A^\top A)^{-1} A^\top b$, dengan syarat matriks $A^\top A$ memiliki nilai eigen yang cukup besar (titik fitur memiliki variasi gradien di dua arah/sudut sudut).
