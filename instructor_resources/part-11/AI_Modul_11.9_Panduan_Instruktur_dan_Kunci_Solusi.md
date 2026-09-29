# AI Modul 11.9: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-09
* **Topik Utama**: Real-Time Camera Processing, Multi-Threading, dan Eliminasi Buffer Lag
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Konkurensi & Buffer Hardware, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.9, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Masalah penumpukan buffer perangkat keras pada streaming video kamera industri dan konsekuensi delay di konveyor pabrik.
* **Menit 25 - 50**: Desain arsitektur multi-threaded: pemisahan I/O thread dan worker thread, penggunaan `threading.Lock`, dan perancangan OSD HUD.
* **Menit 50 - 120**: Praktikum laboratorium: konstruksi kelas `ThreadedCameraStream`, eksekusi streaming tanpa lag, dan penyematan telemetri PKS.
* **Menit 120 - 150**: Rangkuman seluruh Part 11, evaluasi capaian kompetensi, dan orientasi transisi menuju Deep Learning Computer Vision (Part 12).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Hardware Buffer Lag** | Mampu menguraikan mekanisme akumulasi delay $N_{\text{buf}} \times T_{\text{proc}}$ dan solusi threading secara presisi. | Memahami bahwa streaming memiliki delay namun kurang memahami peran buffer driver sistem operasi. | Mengira keterlambatan kamera selalu disebabkan oleh koneksi internet atau kabel yang jelek. |
| **Implementasi Multi-Threading** | Menulis kelas streamer multi-utas lengkap dengan `Lock`, penanganan daemon thread, dan method `stop()` yang bersih. | Mampu menjalankan threading namun tidak menerapkan locking memori dengan benar. | Terjadi deadlock atau thread tidak dapat dihentikan saat aplikasi ditutup. |
| **Perancangan OSD & Visualisasi** | Menghasilkan tata letak HUD informatif dengan pemantauan FPS dinamis dan penanganan headless. | Mampu menggambar teks pada frame namun tata letaknya bertumpuk atau kurang terbaca. | Terjadi galat pemanggilan fungsi display di dalam thread sekunder. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Analisis Akumulasi Penyangga Buffer
Diketahui: Kamera 30 FPS ($T_{\text{cam}} = \frac{1}{30}\text{ s} \approx 33.3\text{ ms}$). Waktu komputasi algoritma $T_{\text{proc}} = 80\text{ ms}$. Kapasitas buffer $N_{\text{buf}} = 4$ frame.
1. **Laju Bingkai Efektif Pemrosesan**:
   Karena algoritma membutuhkan $80\text{ ms}$ per frame, laju pemrosesan maksimal adalah:
   $$\text{FPS}_{\text{efektif}} = \frac{1000\text{ ms}}{80\text{ ms}} = 12.5\text{ FPS}$$
2. **Keterlambatan (Lag) Visual**:
   Karena kamera menghasilkan 30 frame per detik sedangkan pemroses hanya mampu melayani 12.5 frame per detik, buffer perangkat keras sebesar 4 frame akan selalu terisi penuh dengan frame-frame yang belum sempat diambil. Keterlambatan waktu dari saat peristiwa fisik terjadi hingga frame tersebut diproses di layar adalah:
   $$\text{Lag} = N_{\text{buf}} \times T_{\text{proc}} = 4 \times 80\text{ ms} = 320\text{ milidetik} \approx 0.32\text{ detik}$$
   Jika terdapat buffer antrean sistem operasi tambahan (seperti RTSP buffer 2 detik), keterlambatan dapat membengkak hingga $2 - 5\text{ detik}$. Pada kecepatan konveyor $1.5\text{ m/s}$, keterlambatan $2\text{ detik}$ berarti buah sawit telah berpindah sejauh $3.0\text{ meter}$ dari posisi yang tampak di monitor operator!
3. **Solusi ThreadedCameraStream**:
   Thread khusus I/O terus-menerus memanggil `cap.read()` pada kecepatan penuh kamera (30 FPS) dan menimpa variabel `self.frame` dengan frame terbaru, membuang frame-frame lama yang terlewat. Ketika thread pemroses selesai memproses suatu frame ($80\text{ ms}$ kemudian), ia langsung mengambil frame yang paling baru diambil pada saat itu. Akibatnya, ukuran antrean buffer menjadi nol ($N_{\text{buf}} = 0$) dan keterlambatan visual langsung tereliminasi ke titik minimum.

### Jawaban Soal Konseptual 2: Evaluasi Keamanan Threading (Thread-Safety)
Pemanggilan `self.frame.copy()` di dalam blok `with self.lock:` mutlak diperlukan karena:
1. Matriks citra dalam NumPy/OpenCV beroperasi melalui penunjuk memori (*memory pointer*). Jika metode `read()` hanya mengembalikan referensi `return self.frame` tanpa kloning (`.copy()`), maka thread pemroses dan thread akuisisi akan membaca dan memodifikasi blok memori RAM yang sama secara simultan.
2. Ketika thread pemroses sedang membaca baris-baris piksel untuk ekstraksi kontur, thread akuisisi kamera dapat sewaktu-waktu menimpa memori tersebut dengan data frame baru yang masuk dari kamera USB. Fenomena ini menyebabkan kondisi balapan (*race condition*) dan menghasilkan artefak robekan citra (*image tearing* / separuh frame lama bercampur dengan separuh frame baru) yang dapat memicu galat memori atau deteksi cacat palsu.
