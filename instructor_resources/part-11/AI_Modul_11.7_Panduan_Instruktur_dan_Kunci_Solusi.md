# AI Modul 11.7: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-07
* **Topik Utama**: Video Processing, VideoCapture, VideoWriter, dan Profiling FPS
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Aliran Temporal, 70 Menit Praktikum Komputer, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.7, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Representasi temporal video digital, struktur kontainer, dan parameter penting `cv2.VideoCapture`.
* **Menit 25 - 50**: Kodek FourCC, matematika keterlambatan gerak konveyor vs FPS, dan arsitektur `VideoWriter`.
* **Menit 50 - 120**: Praktikum laboratorium: pembuatan video sintetis konveyor TBS sawit, profiling FPS presisi, dan penulisan video OSD.
* **Menit 120 - 150**: Pembahasan potensi kendala teknis dimensi matriks pada VideoWriter dan pengantar Modul 11.8 (Motion Detection).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teori Video** | Menjelaskan relasi kecepatan fisik objek, FPS, dan batas latensi $t_{\text{proc}}$ secara matematis. | Memahami konsep dasar video namun kurang tepat menghitung pergeseran fisik per frame. | Menganggap pemrosesan video sama persis dengan sekumpulan gambar acak tanpa korelasi waktu. |
| **Implementasi VideoCapture & Writer** | Menulis pipeline video dengan penanganan `cap.isOpened()`, loop aman `if not ret`, dan `release()` lengkap. | Menjalankan pipeline video namun lupa melepaskan objek `VideoWriter` di akhir kode. | Program menghasilkan berkas video kosong 0 byte akibat ketidakcocokan dimensi frame. |
| **Pengukuran Kinerja FPS** | Menghitung FPS instan dan rata-rata menggunakan `time.perf_counter()` serta menyematkannya ke layar. | Mampu mengukur waktu komputasi namun menggunakan `time.time()` yang kurang presisi. | Tidak melakukan profiling waktu pemrosesan per frame. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Kalkulasi Batasan Latensi Real-Time
1. **Anggaran Waktu Komputasi Maksimal ($t_{\text{budget}}$)**:
   Pada $\text{FPS} = 60$:
   $$t_{\text{budget}} = \frac{1}{\text{FPS}} = \frac{1}{60}\text{ detik} \approx 0.01667\text{ detik} = 16.67\text{ milidetik}$$
2. **Evaluasi Sistem**:
   Jika model AI membutuhkan $25\text{ ms}$ per frame, maka $t_{\text{proc}} = 25\text{ ms} > 16.67\text{ ms}$. Sistem **TIDAK DAPAT** berjalan real-time pada 60 FPS secara sekuensial; akan terjadi penumpukan buffer frame dan penurunan laju efektif menjadi $\frac{1000}{25} = 40\text{ FPS}$ (kehilangan 20 frame per detik / *frame dropping*).
   * **Alternatif Solusi**:
     * Menerapkan teknik *frame skipping* (misalnya memproses model AI hanya setiap 2 frame sekali, sedangkan frame perantara dilacak dengan tracker ringan).
     * Melakukan pengecilan resolusi spasial citra masukan model (misalnya dari Full HD ke $640 \times 360$).
     * Memanfaatkan akselerasi model menggunakan TensorRT atau OpenVINO pada hardware edge.

### Jawaban Soal Konseptual 2: Evaluasi Dimensi VideoWriter
Kesalahan fatal terletak pada **urutan dimensi lebar dan tinggi**:
* Deklarasi: `cv2.VideoWriter('out.mp4', fourcc, 30.0, (480, 640))` menetapkan `frame_width = 480` dan `frame_height = 640` (format tegak/portrait).
* Namun array NumPy didefinisikan sebagai `np.zeros((480, 640, 3))`, yang berarti `shape[0] = height = 480` dan `shape[1] = width = 640` (format tidur/landscape).
Karena OpenCV VideoWriter mengecek kesesuaian `(frame.shape[1], frame.shape[0]) == (width, height)`, terjadi ketidakcocokan: `(640, 480) != (480, 640)`. OpenCV secara diam-diam menolak frame tersebut tanpa melempar eksepsi, sehingga berkas keluaran menjadi kosong. Sintaks yang benar adalah:
```python
out = cv2.VideoWriter('out.mp4', fourcc, 30.0, (640, 480))
```
