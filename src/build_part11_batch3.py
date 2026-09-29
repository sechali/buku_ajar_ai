import os
import json
import re

BANNED_WORDS = ['taksonomi', 'tripartit', 'ontologis', 'epistemologis', 'dialektika', 'manifestasi dependensi', 'de facto']

def validate_text(text, filename):
    lower = text.lower()
    for w in BANNED_WORDS:
        if w in lower:
            raise ValueError(f"BANNED WORD FOUND in {filename}: '{w}'")
    bad_ctrl = [c for c in text if ord(c) < 32 and c not in '\t\n\r']
    if bad_ctrl:
        raise ValueError(f"CONTROL CHARACTERS FOUND in {filename}: {len(bad_ctrl)}")
    print(f"[VALIDATED] 0 banned words & 0 control chars in {filename}")

# ==============================================================================
# MODUL 11.7: Video Processing
# ==============================================================================
def create_modul_11_7():
    md_content = r"""# AI Modul 11.7: Video Processing

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-11-07
* **Mata Kuliah**: Visi Komputer dan Pengolahan Citra Digital (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Genap)
* **Prasyarat**: AI Modul 11.6 (Face Detection)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pemuatan Stream VideoCapture, Codec VideoWriter FourCC, Profiling FPS Presisi"] --> B["OUTCOMES: Kemampuan Membangun Pipeline Pengolahan Video Kontinu Tanpa Frame Drop"]
    B --> C["IMPACTS: Sistem Pemantauan Aliran Konveyor TBS & Inspeksi Penerbangan Drone Kebun"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** struktur representasi temporal video digital, mekanisme penguraian kontainer (*demuxing*) dan pengodean (*decoding*) frame menggunakan kelas `cv2.VideoCapture`, format pengodean video terkompresi FourCC (MP4V, XVID, H.264), serta penulisan video dengan `cv2.VideoWriter`.
2. **Menerapkan (C3)** perulangan pemrosesan frame berurutan (*frame processing loop*), ekstraksi metadata video (panjang frame, dimensi resolusi, FPS bawaan), serta pengukuran laju bingkai per detik aktual (*throughput FPS*) menggunakan modul `time.perf_counter()`.
3. **Menganalisis (C4)** faktor-faktor penyebab penurunan laju bingkai (*frame drops*) dan akumulasi latensi (*latency accumulation*) pada pipeline inspeksi video aliran Tandan Buah Segar di pabrik kelapa sawit.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Pemahaman mendalam properti `cv2.VideoCapture` (`CAP_PROP_POS_FRAMES`, `CAP_PROP_FPS`, `CAP_PROP_FRAME_COUNT`).
  * Skrip Python modular berstandar PEP 8 untuk pembacaan berkas video, pemrosesan frame per frame, dan penulisan berkas keluaran MP4.
  * Laporan pengukuran profil waktu komputasi pemrosesan frame visual vs waktu decoding I/O.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian merancang sistem pengarsipan video inspeksi pabrik kelapa sawit dengan kompresi yang optimal.
  * Kemampuan menyinkronkan waktu komputasi algoritma visi komputer dengan kecepatan fisik sabuk konveyor industri.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Efisiensi pemantauan operasional pabrik dan inspeksi udara drone melalui dokumentasi video terotomatisasi yang terindeks secara digital.

---

## 2. Profil Fundamental Video Processing: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Video digital secara fungsional adalah tensor berdimensi empat yang menggabungkan dimensi ruang dua dimensi, kanal warna, dan dimensi waktu diskrit:

$$\mathcal{V}(t, y, x, c) \in \mathbb{R}^{T \times H \times W \times C}$$

1. **Penguraian Aliran Temporal (*Temporal Stream Demuxing*)**: Mengekstrak matriks citra dua dimensi berurutan $I_t(y, x)$ pada interval waktu sampling periodik $\Delta t = \frac{1}{\text{FPS}}$.
2. **Operasi Per-Frame Tersinkronisasi**: Menjalankan algoritma pengolahan citra (filtering, thresholding, deteksi) pada setiap frame $I_t$ sebelum frame $I_{t+1}$ tiba di buffer.
3. **Enkoding dan Kompresi Video (*Video Compression*)**: Mengompresi kembali kumpulan frame hasil olahan menggunakan algoritma estimasi gerak antar-frame (*inter-frame prediction*) ke dalam format kontainer seperti MP4 atau AVI.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Perekaman Terindeks Stasiun Loading Ramp**: Merekam aliran truk buah yang membongkar muatan dan menyematkan metadata nomor kendaraan dan jam panen pada pojok video (*on-screen display*).
* **Inspeksi Kontinu Penerbangan Drone**: Memproses video rekaman drone yang terbang di atas barisan pohon kelapa sawit untuk mendata tajuk tanaman secara mulus.
* **Audit Operasional Pabrik**: Menyimpan rekaman video terkompresi dengan bitrate rendah untuk arsip kendali mutu selama 30 hari.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
Dalam industri agrokompleks, mengandalkan foto tunggal (*still photo*) tidak memadai karena objek bergerak melintas secara kontinu. Video processing memungkinkan sistem menangkap objek dari berbagai sudut pandang saat objek bergerak di atas sabuk berjalan (*conveyor belt*).

### 2.4 Analisis Kelebihan dan Kekurangan Codec Video OpenCV

| FourCC Codec | Format Kontainer | Kompatibilitas Sistem | Rasio Kompresi | Rekomendasi Industri Kebun |
| :--- | :--- | :--- | :--- | :--- |
| **`mp4v`** | `.mp4` | Sangat luas (Windows, Linux, Mac). | Sedang hingga Tinggi | Standar penyimpanan video laporan inspeksi kebun. |
| **`XVID`** | `.avi` | Sangat matang di lingkungan Windows lama. | Sedang | Sistem CCTV pabrik kelapa sawit konvensional. |
| **`MJPG`** | `.avi` | Ringan pada CPU (kompresi JPEG per frame). | Rendah (Ukuran Berkas Besar) | Perekaman berkecepatan tinggi tanpa beban kompresi berat. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Pabrik Kelapa Sawit mengoperasikan kamera pengawas di atas konveyor penyortiran buah afkir berkecepatan $1.0\text{ meter/detik}$. Video beresolusi $1280 \times 720$ dibaca pada 30 FPS. Sistem membaca setiap frame, menandai buah mentah dengan kotak merah, menghitung nilai FPS aktual, dan menyimpan video ringkasan berdurasi 1 jam ke dalam media penyimpanan NAS pabrik dengan codec `mp4v` untuk laporan harian asisten sortasi.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Pelepasan Objek VideoCapture dan VideoWriter**: Objek `cap` dan `out` wajib dilepaskan secara eksplisit menggunakan `cap.release()` dan `out.release()`. Kegagalan memanggil `.release()` pada `VideoWriter` akan menyebabkan header berkas video tidak tertutup sempurna (*unfinalized container*), sehingga video hasil olahan rusak dan tidak dapat diputar.
2. **Kesesuaian Dimensi Frame pada VideoWriter**: Dimensi lebar dan tinggi frame yang dilewatkan ke `out.write(frame)` harus sama persis dengan parameter `(frame_width, frame_height)` yang dideklarasikan saat inisialisasi `cv2.VideoWriter`. Perbedaan 1 piksel saja akan menyebabkan frame diabaikan tanpa peringatan error.

---

## 3. Landasan Teori & Konsep Matematis Video Processing

![Pipeline Video Processing VideoCapture dan FPS Profiling](../assets/pipeline_video_processing_videocapture_dan_fps_profiling.png)

### 3.1 Teori Laju Bingkai dan Jeda Waktu Spasial
Jika suatu objek komoditas pertanian bergerak di atas konveyor dengan kecepatan linier $v\text{ (m/s)}$, dan kamera memiliki laju akuisisi $\text{FPS}$ frame per detik, maka pergeseran fisik objek antar-frame berturut-turut adalah:

$$\Delta s = \frac{v}{\text{FPS}}$$

Misalkan $v = 1.5\text{ m/s}$ dan $\text{FPS} = 30$:
$$\Delta s = \frac{1.5}{30} = 0.05\text{ meter} = 5\text{ cm per frame}$$

Jika waktu komputasi algoritma visi komputer per frame adalah $t_{\text{proc}}$, maka syarat mutlak agar sistem berjalan tanpa kehilangan data (*real-time constraint*) adalah:

$$t_{\text{proc}} \le \frac{1}{\text{FPS}} = \Delta t$$

Untuk $\text{FPS} = 30$, waktu pemrosesan maksimal per frame adalah $33.33\text{ milidetik}$. Jika $t_{\text{proc}} > 33.33\text{ ms}$, buffer video akan menumpuk dan memicu keterlambatan visual (*lag*).

### 3.2 Profiling Laju Bingkai Aktual (*FPS Calculation*)
Laju bingkai per detik dihitung secara dinamis menggunakan rata-rata bergerak (*moving average*) dari interval waktu jam internal prosesor beresolusi tinggi:

$$\text{FPS}_t = \frac{1}{t_{\text{current}} - t_{\text{previous}}}$$

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Sumber Video: cap = cv2.VideoCapture(source)"] --> B{"cap.isOpened()?"}
    B -- Tidak --> C["Lempar Eksepsi FileNotFoundError"]
    B -- Ya --> D["Inisialisasi VideoWriter: out = cv2.VideoWriter(...)"]
    D --> E["Loop: ret, frame = cap.read()"]
    E --> F{"ret == True?"}
    F -- Tidak --> G["Akhir Video: Break Loop"]
    F -- Ya --> H["Pemrosesan Frame (Analisis & Anotasi OSD)"]
    H --> I["Kalkulasi Latensi & FPS Aktual"]
    I --> J["Tulis Frame: out.write(processed_frame)"]
    J --> E
    G --> K["cap.release() & out.release() -> Simpan Video"]
```

Implementasi Python modular untuk pipeline pembacaan, pemrosesan, pengukuran FPS, dan penulisan video:

```python
import cv2
import numpy as np
import time

# 1. Pembangkitan Video Sintetis Aliran Konveyor TBS Sawit (30 Frame)
video_filename = "synthetic_conveyor.mp4"
fps = 30.0
W, H = 640, 480
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(video_filename, fourcc, fps, (W, H))

for frame_idx in range(60): # 2 Detik Video Sintetis
    frame = np.full((H, W, 3), 40, dtype=np.uint8) # Sabuk konveyor abu-abu
    # Simulasikan buah sawit bergerak dari kiri ke kanan (x bertambah per frame)
    pos_x = int(50 + frame_idx * 8)
    pos_y = 240
    cv2.circle(frame, (pos_x, pos_y), 45, (20, 100, 220), -1) # Buah jingga
    cv2.putText(frame, f"Frame #{frame_idx+1}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    writer.write(frame)

writer.release()
print(f"[OK] Berkas video sintetis berhasil dibuat: {video_filename}")

# 2. Pipeline Pemrosesan Video dengan Profiling FPS
cap = cv2.VideoCapture(video_filename)
if not cap.isOpened():
    raise FileNotFoundError("Gagal membuka file video!")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
native_fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Total Frame: {total_frames}, FPS Asli: {native_fps:.1f}")

processed_out = cv2.VideoWriter("processed_conveyor.mp4", fourcc, fps, (W, H))

frame_count = 0
prev_time = time.perf_counter()
fps_list = []

while True:
    ret, frame = cap.read()
    if not ret:
        break # Video selesai
        
    frame_count += 1
    
    # Operasi Visi Komputer per frame: Konversi warna dan penandaan deteksi
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    
    # Hitung waktu pemrosesan dan FPS aktual
    curr_time = time.perf_counter()
    dt = curr_time - prev_time
    prev_time = curr_time
    current_fps = 1.0 / dt if dt > 0 else 0.0
    fps_list.append(current_fps)
    
    # Anotasi On-Screen Display (OSD)
    cv2.putText(frame, f"FPS: {current_fps:.1f}", (W - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    processed_out.write(frame)

cap.release()
processed_out.release()

avg_fps = np.mean(fps_list[1:]) # Abaikan frame pertama
print(f"Pemrosesan Selesai! Rata-rata FPS Aktual: {avg_fps:.1f} FPS (Target: 30 FPS)")
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Pengukuran Throughput Konveyor PKS

### 5.1 Spesifikasi Masalah
Manajemen pabrik ingin mengetahui jumlah tonase buah sawit yang melintas di konveyor per menit secara real-time dari rekaman video kamera industri berkecepatan 30 FPS.

### 5.2 Implementasi Estimasi Laju Buah Melintas
```python
# Simulasi estimasi laju buah melintas berbasis posisi piksel
def analyze_conveyor_throughput(fps, pixel_speed_per_frame, gsd_m_per_px=0.002):
    # Kecepatan konveyor riil dalam meter/detik
    speed_mps = pixel_speed_per_frame * fps * gsd_m_per_px
    print(f"Kecepatan Fisik Sabuk Konveyor: {speed_mps:.2f} m/detik")
    return speed_mps

v_konveyor = analyze_conveyor_throughput(fps=30, pixel_speed_per_frame=8, gsd_m_per_px=0.0025)
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Lupa Memanggil `out.release()`**: Kesalahan paling sering yang menyebabkan berkas video keluaran berukuran 0 byte atau tidak memiliki header kontainer yang valid.
2. **Dimensi Frame Tidak Cocok pada VideoWriter**: Melewatkan frame dengan ukuran $(H, W)$ yang berbeda dengan dimensi deklarasi `VideoWriter((W, H))` (ingat: VideoWriter meminta urutan Lebar dulu lalu Tinggi).
3. **Mengabaikan Nilai `ret` dari `cap.read()`**: Mengakses `frame.shape` tanpa memeriksa `if not ret:` akan memicu crash pada akhir video ketika frame bernilai `None`.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Struktur `try ... finally`**: Selalu gunakan blok `try ... finally` atau manajemen konteks agar fungsi `.release()` dijamin terpanggil meskipun terjadi eksepsi di tengah loop.
2. **Gunakan FourCC `mp4v` untuk Portabilitas**: Format MP4V dapat diputar langsung di sebagian besar peramban web dan aplikasi pemutar media modern tanpa instalasi codec tambahan.
3. **Gunakan Jam Beresolusi Tinggi**: Gunakan selalu `time.perf_counter()` alih-alih `time.time()` untuk kalkulasi FPS presisi tingkat mikrodetik.

---

## 7. Rangkuman Modul

* Video digital diolah sebagai kumpulan frame diskrit kontinu menggunakan objek `cv2.VideoCapture`.
* Penulisan video membutuhkan pendefinisian FourCC codec yang sesuai melalui kelas `cv2.VideoWriter`.
* Syarat mutlak real-time video processing adalah waktu komputasi per frame $t_{\text{proc}} \le \frac{1}{\text{FPS}}$.
* Pelepasan sumber daya video (`release()`) dan konsistensi dimensi frame merupakan prasyarat mutlak keandalan pipeline video OpenCV.

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Kalkulasi Batasan Latensi Real-Time (Bloom C3)**: Kamera pengawas di stasiun sortasi pabrik kelapa sawit merekam video pada frekuensi 60 frame per detik (FPS = 60).
   * Berapakah anggaran waktu komputasi maksimal ($t_{\text{budget}}$) dalam milidetik yang tersedia bagi model AI per frame agar video tidak mengalami keterlambatan (*lag*)?
   * Jika model AI membutuhkan waktu rata-rata 25 milidetik per frame, apakah sistem dapat berjalan real-time pada 60 FPS? Jelaskan alternatif solusinya!
2. **Evaluasi Dimensi VideoWriter (Bloom C4)**: Seorang programmer membuat objek VideoWriter dengan baris kode:
   `out = cv2.VideoWriter('out.mp4', fourcc, 30.0, (480, 640))`
   namun frame yang ditulis diperoleh dari citra berdimensi `frame = np.zeros((480, 640, 3), dtype=np.uint8)`. Mengapa video hasil olahan tidak memuat frame yang ditulis? Temukan kesalahan fatal pada urutan dimensinya!

### Tugas Pemrograman Mandiri
Buatlah skrip Python yang memproses video konveyor sintetis, mendeteksi buah sawit pada setiap frame, menghitung nilai FPS aktual, dan mencetak teks OSD penunjuk status "KONVEYOR NORMAL" jika FPS $\ge 25$ atau "PERINGATAN: SISTEM LAMBAT" jika FPS $< 25$ dengan warna dinamis (Hijau/Merah)!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 11.8: Motion Detection

Kita telah menguasai cara membaca aliran video frame per frame, mengukur laju bingkai FPS secara presisi, dan menyimpan kembali video hasil olahan. Namun, pemrosesan video yang kita lakukan sejauh ini masih memperlakukan setiap frame secara statis tanpa memanfaatkan hubungan korelasi antar-waktu (*temporal correlation*). Bagaimana jika kita ingin mengetahui apakah ada objek yang bergerak melintas di depan kamera pengawas? Bagaimana cara memisahkan objek yang bergerak dari latar belakang kebun yang diam?

Pada **AI Modul 11.8: Motion Detection**, kita akan memasuki ranah analisis gerak temporal: mempelajari metode **Absolute Frame Differencing**, pemodelan latar belakang statistik **Background Subtraction MOG2**, serta estimasi vektor kecepatan gerak **Optical Flow Lucas-Kanade** untuk memantau keamanan kebun dan dinamika aliran buah sawit.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media. (Bab 2: Introduction to OpenCV & HighGUI).
2. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications* (2nd ed.). Springer. (Bab 8: Video Processing).
3. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson.
4. Tan, K. S., & Isa, N. A. M. (2019). Real-time fresh fruit bunch monitoring on conveyor using machine vision. *Industrial Automation and Computing Review*, 11(3), 205-218.
"""
    validate_text(md_content, "AI_Modul_11.7_Video_processing.md")
    with open("docs/part-11/AI_Modul_11.7_Video_processing.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-11/AI_Modul_11.7_Video_processing.md")

    # Notebook 11.7
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 11.7: Praktikum Video Processing\n",
                    "**Mata Kuliah:** Visi Komputer dan Pengolahan Citra Digital  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Membangkitkan berkas video simulasi dan mengonfigurasi `cv2.VideoWriter` dengan FourCC codec `mp4v`.\n",
                    "2. Membaca aliran video frame per frame menggunakan `cv2.VideoCapture`.\n",
                    "3. Melakukan pengukuran dan pencatatan laju bingkai aktual (*FPS Profiling*) menggunakan `time.perf_counter()`.\n",
                    "4. Menyematkan teks anotasi *On-Screen Display* (OSD) dan menyimpan video hasil olahan.\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import cv2\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import time\n",
                    "\n",
                    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                    "print(f'OpenCV Version: {cv2.__version__}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Pembangkitan Video Sintetis Aliran Konveyor TBS Sawit\n",
                    "Membangkitkan video berdurasi 60 frame (2 detik pada 30 FPS) yang mensimulasikan buah sawit melintas di sabuk berjalan."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "video_path = 'conveyor_synthetic.mp4'\n",
                    "fps = 30.0\n",
                    "W, H = 640, 480\n",
                    "fourcc = cv2.VideoWriter_fourcc(*'mp4v')\n",
                    "out_writer = cv2.VideoWriter(video_path, fourcc, fps, (W, H))\n",
                    "\n",
                    "for i in range(60):\n",
                    "    frame = np.full((H, W, 3), 45, dtype=np.uint8)\n",
                    "    # Buah melintas dari kiri ke kanan\n",
                    "    bx = int(60 + i * 8.5)\n",
                    "    by = 240\n",
                    "    cv2.circle(frame, (bx, by), 40, (20, 110, 220), -1)\n",
                    "    cv2.putText(frame, f'Conveyor Frame: #{i+1}', (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)\n",
                    "    out_writer.write(frame)\n",
                    "\n",
                    "out_writer.release()\n",
                    "print(f'[OK] Berkas video berhasil disimpan: {video_path}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Pemrosesan Video dan Profiling FPS Nyata\n",
                    "Membaca frame video, menerapkan deteksi sederhana, mengukur FPS aktual, dan menyimpan video teranotasi."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "cap = cv2.VideoCapture(video_path)\n",
                    "assert cap.isOpened(), 'Gagal membuka video!'\n",
                    "\n",
                    "total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))\n",
                    "print(f'Total Frame Video: {total_frames}')\n",
                    "\n",
                    "processed_path = 'conveyor_processed.mp4'\n",
                    "processed_writer = cv2.VideoWriter(processed_path, fourcc, fps, (W, H))\n",
                    "\n",
                    "fps_history = []\n",
                    "t_prev = time.perf_counter()\n",
                    "sample_frames = []\n",
                    "\n",
                    "while True:\n",
                    "    ret, frame = cap.read()\n",
                    "    if not ret:\n",
                    "        break\n",
                    "        \n",
                    "    # Simulasi komputasi inspeksi buah\n",
                    "    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\n",
                    "    _, mask = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)\n",
                    "    \n",
                    "    # Profiling FPS\n",
                    "    t_curr = time.perf_counter()\n",
                    "    dt = t_curr - t_prev\n",
                    "    t_prev = t_curr\n",
                    "    inst_fps = 1.0 / dt if dt > 0 else 0.0\n",
                    "    fps_history.append(inst_fps)\n",
                    "    \n",
                    "    # Anotasi OSD\n",
                    "    cv2.putText(frame, f'FPS: {inst_fps:.1f}', (W - 140, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)\n",
                    "    processed_writer.write(frame)\n",
                    "    \n",
                    "    if len(sample_frames) < 3 and len(fps_history) in [15, 30, 45]:\n",
                    "        sample_frames.append(frame.copy())\n",
                    "\n",
                    "cap.release()\n",
                    "processed_writer.release()\n",
                    "\n",
                    "avg_fps = np.mean(fps_history[1:])\n",
                    "print(f'Selesai memproses {len(fps_history)} frame! Rata-rata FPS: {avg_fps:.1f}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Hasil Pengukuran FPS dan Sampel Frame Video\n",
                    "Menampilkan grafik stabilitas laju bingkai dan cuplikan frame video hasil olahan."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))\n",
                    "\n",
                    "ax1.plot(fps_history[1:], color='dodgerblue', linewidth=2)\n",
                    "ax1.axhline(30.0, color='crimson', linestyle='--', label='Target 30 FPS')\n",
                    "ax1.set_title('Dinamika Profiling FPS Video Processing', fontsize=11, fontweight='bold')\n",
                    "ax1.set_xlabel('Nomor Frame')\n",
                    "ax1.set_ylabel('Laju Bingkai (FPS)')\n",
                    "ax1.legend()\n",
                    "\n",
                    "if sample_frames:\n",
                    "    ax2.imshow(cv2.cvtColor(sample_frames[-1], cv2.COLOR_BGR2RGB))\n",
                    "    ax2.set_title('Cuplikan Frame Video Teranotasi OSD', fontsize=11, fontweight='bold')\n",
                    "    ax2.axis('off')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_video_processing_11_7.png', dpi=150)\n",
                    "plt.show()\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open("notebooks/part-11/AI_Modul_11.7_Praktikum_Video_Processing.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-11/AI_Modul_11.7_Praktikum_Video_Processing.ipynb")

    # Guide 11.7
    guide_content = r"""# AI Modul 11.7: Panduan Instruktur dan Kunci Solusi

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
* **Menit 120 - 150**: Pembahasan jebakan dimensi matriks pada VideoWriter dan pengantar Modul 11.8 (Motion Detection).

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
"""
    validate_text(guide_content, "AI_Modul_11.7_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-11/AI_Modul_11.7_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-11/AI_Modul_11.7_Panduan_Instruktur_dan_Kunci_Solusi.md")

# ==============================================================================
# MODUL 11.8: Motion Detection
# ==============================================================================
def create_modul_11_8():
    md_content = r"""# AI Modul 11.8: Motion Detection

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-11-08
* **Mata Kuliah**: Visi Komputer dan Pengolahan Citra Digital (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Genap)
* **Prasyarat**: AI Modul 11.7 (Video Processing)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pemodelan Frame Differencing, Background Subtractor MOG2, Vektor Optical Flow"] --> B["OUTCOMES: Kemampuan Mendeteksi & Melacak Objek Bergerak pada Aliran Video Perkebunan"]
    B --> C["IMPACTS: Sistem Keamanan Perimeter Kebun Sawit & Pemantauan Dinamika Aliran Buah Otomatis"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** prinsip matematis deteksi gerak visual, metode diferensiasi bingkai absolut (*absolute frame differencing*), pemodelan latar belakang statistik adaptif campuran Gaussian (*Gaussian Mixture-based Background Subtraction / MOG2*), serta persamaan batasan kecerahan optik (*optical flow brightness constancy equation*).
2. **Menerapkan (C3)** fungsi `cv2.absdiff()`, `cv2.createBackgroundSubtractorMOG2()`, dan algoritma sparse optical flow Lucas-Kanade (`cv2.calcOpticalFlowPyrLK()`) untuk mendeteksi pergerakan objek pada aliran video perkebunan kelapa sawit.
3. **Menganalisis (C4)** perbedaan performa deteksi gerak terhadap gangguan derau alami lingkungan terbuka: goyangan dedaunan tertiup angin, perubahan bayangan awan dinamis, dan objek bergerak yang berhenti mendadak.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Formulasi matematis model probabilitas campuran Gaussian dan fungsi selisih temporal.
  * Skrip Python modular berstandar PEP 8 untuk segmentasi latar depan (*foreground mask*) dan pelacakan lintasan pergerakan objek.
  * Plot visual perbandingan masker gerak antara Frame Differencing dan MOG2.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian merancang sistem pengawasan CCTV pintar untuk mendeteksi intrusi satwa liar atau pencurian hasil panen di perimeter perkebunan.
  * Kemampuan mengukur kecepatan pergerakan komoditas di atas konveyor secara nirkontak.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Peningkatan keamanan aset perkebunan dan efisiensi logistik panen melalui sistem peringatan dini berbasis visi komputer otomatis.

---

## 2. Profil Fundamental Motion Detection: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Deteksi gerak dalam video mengidentifikasi wilayah spasial yang mengalami perubahan intensitas signifikan sepanjang waktu:
1. **Diferensiasi Temporal Langsung**: Menghitung magnitudo perubahan intensitas antar dua bingkai berurutan:
   $$D(t, y, x) = |I_t(y, x) - I_{t-1}(y, x)|$$
2. **Pemodelan Latar Belakang Adaptif (MOG2)**: Memodelkan nilai intensitas setiap piksel latar belakang menggunakan campuran $K$ distribusi Gaussian ($\mathcal{N}(\mu_k, \sigma_k^2)$). Piksel yang menyimpang lebih dari $2.5\sigma$ dari seluruh komponen latar belakang diklasifikasikan sebagai objek bergerak (*foreground*).
3. **Estimasi Vektor Aliran Optik**: Menghitung arah dan besar kecepatan perpindahan piksel $(u, v) = \left(\frac{dx}{dt}, \frac{dy}{dt}\right)$ berbasis asumsi kekekalan kecerahan.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Deteksi Intrusi Hama Babi Hutan & Gajah di Batas Kebun**: Kamera termal/IR mendeteksi pergerakan satwa liar yang melintasi parit batas perkebunan pada malam hari.
* **Pemantauan Kelancaran Konveyor TBS**: Mendeteksi kemacetan (*jamming*) aliran tandan buah di corong perebusan pabrik kelapa sawit secara instan jika pergerakan berhenti.
* **Penghitungan Otomatis Lori Pengangkut Buah**: Mendeteksi gerak maju lori di rel pabrik untuk sensus logistik harian.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
1. **Mereduksi Beban Komputasi Deteksi**: Alih-alih menjalankan model deteksi objek berat pada setiap frame di seluruh area citra, sistem hanya mengaktifkan inferensi pada area kotak (*bounding box*) yang terdeteksi memiliki pergerakan (*motion-triggered processing*).
2. **Beroperasi Tanpa Label Kategori Objek**: Mampu mendeteksi sembarang benda bergerak tanpa perlu dilatih sebelumnya pada jenis objek tertentu.

### 2.4 Analisis Kelebihan dan Kekurangan Metode Deteksi Gerak

| Metode | Kompleksitas Komputasi | Keunggulan Utama | Kelemahan Kritis | Skenario Penggunaan Kebun |
| :--- | :--- | :--- | :--- | :--- |
| **Frame Differencing** | Sangat Rendah ($O(1)$) | Respons instan, memori minimal. | Objek berhenti mendadak hilang; bagian dalam objek seragam berlubang. | Deteksi kilat objek melintas di koridor sempit. |
| **MOG2 Subtraction** | Sedang | Memodelkan latar belakang berulang (daun bergoyang) dan mendeteksi bayangan. | Memerlukan waktu pemanasan (*learning history*) beberapa frame awal. | Kamera CCTV permanen stasiun sortasi dan pintu pabrik. |
| **Lucas-Kanade Optical Flow** | Sedang hingga Tinggi | Menghasilkan vektor arah dan kecepatan gerak. | Gagal jika pergeseran objek terlalu besar (*large displacement*). | Pengukuran kecepatan konveyor dan tracking drone. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Divisi Keamanan Kebun PT Agro Mandiri memasang kamera CCTV pengawas di jembatan timbang blok terluar. Algoritma MOG2 (`cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)`) memantau area penimbangan. Ketika truk pengangkut TBS melintas di malam hari, sistem mendeteksi pergerakan, memisahkan bayangan truk dari badan truk, dan mengaktifkan lampu sorot serta perekaman resolusi tinggi secara otomatis.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Masalah Kamera Bergerak**: Seluruh metode background subtraction statis mengasumsikan kamera terpasang kokoh pada posisi diam (*static camera*). Jika kamera bergetar atau terpasang pada drone yang terbang, seluruh latar belakang akan terdeteksi sebagai objek bergerak, sehingga diperlukan teknik stabilisasi citra atau kompensasi gerak kamera global (*global motion compensation*).
2. **Penyaringan Bayangan (*Shadow Suppression*)**: Bayangan objek bergerak sering kali ikut terdeteksi sebagai objek karena mengalami penurunan intensitas. Pada MOG2, piksel bayangan ditandai dengan nilai khusus (abu-abu $127$) dan dapat difilter dengan `mask == 255`.

---

## 3. Landasan Teori & Konsep Matematis Deteksi Gerak

![Mekanisme Frame Differencing dan Optical Flow Motion Detection](../assets/mekanisme_frame_differencing_dan_optical_flow_motion_detection.png)

### 3.1 Teori Pemodelan Campuran Gaussian (MOG2)
Probabilitas mengamati nilai piksel $x_t$ pada waktu $t$ dimodelkan sebagai kombinasi linier $K$ distribusi Gaussian:

$$P(x_t) = \sum_{k=1}^{K} \omega_{k, t} \cdot \eta(x_t; \mu_{k, t}, \Sigma_{k, t})$$

di mana $\omega_{k, t}$ adalah bobot komponen ke-$k$, $\mu_{k, t}$ adalah rata-rata, dan $\Sigma_{k, t} = \sigma_{k, t}^2 I$ adalah matriks kovarians.

Jika suatu piksel baru cocok dengan salah satu distribusi (dalam jarak $2.5\sigma$), parameter distribusi diperbarui secara eksponensial:

$$\mu_t = (1 - \rho) \mu_{t-1} + \rho x_t$$
$$\sigma_t^2 = (1 - \rho) \sigma_{t-1}^2 + \rho (x_t - \mu_t)^\top (x_t - \mu_t)$$

di mana $\rho = \alpha \cdot \eta(x_t | \mu_k, \sigma_k)$ adalah laju pembelajaran adaptif.

### 3.2 Persamaan Batasan Aliran Optik (*Optical Flow Constraint*)
Berdasarkan asumsi kekekalan kecerahan (*brightness constancy assumption*):

$$I(x + \Delta x, \; y + \Delta y, \; t + \Delta t) = I(x, y, t)$$

Melalui ekspansi deret Taylor orde pertama:

$$\frac{\partial I}{\partial x} \frac{dx}{dt} + \frac{\partial I}{\partial y} \frac{dy}{dt} + \frac{\partial I}{\partial t} = 0 \implies I_x u + I_y v + I_t = 0$$

Persamaan tunggal dengan dua variabel tak diketahui $(u, v)$ ini diselesaikan oleh algoritma Lucas-Kanade dengan mengasumsikan vektor kecepatan seragam pada jendela lokal tetangga $3 \times 3$.

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Frame Aliran Video: frame_t"] --> B["Inisialisasi MOG2: cv2.createBackgroundSubtractorMOG2()"]
    B --> C["Kalkulasi Masker Latar Depan: fg_mask = sub.apply(frame_t)"]
    C --> D["Ambang Batas Bayangan: _, clean_mask = cv2.threshold(fg_mask, 250, 255, THRESH_BINARY)"]
    D --> E["Pembersihan Morfologi: cv2.morphologyEx(clean_mask, OPEN)"]
    E --> F["Ekstraksi Kontur Gerak: cv2.findContours()"]
    F --> G["Penyaringan Luas Area & Anotasi Bounding Box"]
```

Implementasi Python modular untuk deteksi gerak menggunakan Background Subtractor MOG2:

```python
import cv2
import numpy as np

# 1. Pembangkitan Sekuens Video Sintetis dengan Objek Bergerak (Truk Buah di Pos Kebun)
H, W = 400, 600
frames = []
for t in range(40):
    bg = np.full((H, W, 3), 100, dtype=np.uint8) # Latar jalan kebun
    # Objek bergerak: kotak truk pengangkut buah (x bertambah dari 50 ke 450)
    tx = int(50 + t * 10)
    ty = 180
    cv2.rectangle(bg, (tx, ty), (tx + 120, ty + 60), (30, 80, 200), -1) # Truk oranye
    # Bayangan truk di bawahnya
    cv2.rectangle(bg, (tx + 10, ty + 60), (tx + 130, ty + 75), (60, 60, 60), -1)
    frames.append(bg)

# 2. Inisialisasi Background Subtractor MOG2
subtractor = cv2.createBackgroundSubtractorMOG2(history=30, varThreshold=25, detectShadows=True)

# 3. Proses Sekuens Frame
motion_detections = []
kernel_clean = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

for idx, frame in enumerate(frames):
    fg_mask = subtractor.apply(frame)
    
    # Nilai 255: Foreground sejati; Nilai 127: Bayangan (Shadow)
    # Filter bayangan dengan hanya mengambil intensitas > 200
    _, pure_foreground = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
    
    # Pembersihan derau
    cleaned_mask = cv2.morphologyEx(pure_foreground, cv2.MORPH_OPEN, kernel_clean)
    
    # Ekstraksi kontur gerak
    cnts, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = []
    for c in cnts:
        if cv2.contourArea(c) > 500: # Filter derau kecil
            x, y, w, h = cv2.boundingRect(c)
            boxes.append((x, y, w, h))
            
    motion_detections.append(len(boxes))

print(f"Total Frame Diproses: {len(frames)}")
print(f"Deteksi Gerak Frame Terakhir: {motion_detections[-1]} objek terdeteksi")
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Pengawasan Perimeter Kebun Sawit

### 5.1 Spesifikasi Masalah
Kamera pemantau batas hutan dan kebun sawit mendeteksi pergerakan hewan liar (gajah liar / babi hutan) pada malam hari untuk memicu sirene pengusir otomatis.

### 5.2 Implementasi Filter Luas Area & Alarm Otomatis
```python
def evaluate_perimeter_alarm(detected_boxes, min_intruder_area=1500):
    for (x, y, w, h) in detected_boxes:
        area = w * h
        if area >= min_intruder_area:
            return True, f"INTRUSI TERDETEKSI! Objek Besar di Koordinat ({x}, {y}), Luas: {area} px"
    return False, "Perimeter Aman"

is_alarm, alert_msg = evaluate_perimeter_alarm(boxes, min_intruder_area=2000)
print(f"Status Sistem Keamanan: {alert_msg}")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Mengabaikan Deteksi Bayangan**: Tidak menyaring nilai 127 pada masker MOG2 menyebabkan bayangan pohon yang ikut bergerak terdeteksi sebagai objek padat terpisah.
2. **Tidak Memberikan Waktu Pemanasan Model (*Warm-up Frames*)**: Pada 5 - 10 frame awal, model MOG2 belum memiliki data statistik latar belakang yang cukup, sehingga seluruh citra akan terdeteksi sebagai gerak. Abaikan deteksi pada frame-frame pemanasan awal.
3. **Menerapkan Algoritma pada Kamera Bergoyang**: Menggunakan background subtractor pada video drone tanpa stabilisasi koordinat.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Gunakan Morfologi Opening dan Closing**: Menghilangkan derau bintik putih dan menyatukan bagian badan kendaraan/hewan yang sempat berlubang.
2. **Setel `varThreshold` Sesuai Derau Lingkungan**: Naikkan `varThreshold` (misalnya ke 36 atau 48) jika kamera menghadap ke dedaunan kebun yang bergoyang tertiup angin kencang.
3. **Kombinasikan dengan Bounding Box Tracking**: Lacak perpindahan titik centroid antar-frame untuk memastikan objek benar-benar bergerak berpindah lokasi, bukan sekadar berosilasi di tempat.

---

## 7. Rangkuman Modul

* Deteksi gerak mengidentifikasi perubahan intensitas temporal dalam video digital.
* Frame differencing adalah metode tercepat namun rentan menghasilkan objek berlubang (*hollow artifacts*).
* Algoritma MOG2 memodelkan latar belakang secara adaptif menggunakan campuran Gaussian dan mampu memisahkan bayangan bergerak secara akurat.
* Optical flow memperkirakan vektor kecepatan pergeseran piksel berbasis persamaan kekekalan kecerahan.

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Analisis Fenomena Objek Berhenti (Bloom C4)**: Sebuah truk pengangkut kelapa sawit masuk ke stasiun loading ramp, bergerak maju selama 10 detik, lalu berhenti total selama 2 menit untuk membongkar muatan.
   * Apa yang terjadi pada masker deteksi gerak jika digunakan metode **Frame Differencing** saat truk berhenti total?
   * Apa yang terjadi pada masker deteksi jika digunakan metode **MOG2** dengan parameter `history = 500` (pada 30 FPS, setara ~16 detik) saat truk berhenti selama 2 menit? Jelaskan fenomena adaptasi latar belakang tersebut!
2. **Evaluasi Persamaan Aliran Optik (Bloom C4)**: Diberikan persamaan aliran optik $I_x u + I_y v + I_t = 0$. Jelaskan mengapa persamaan ini disebut sebagai *ill-posed problem* (masalah dengan solusi tak tentu) jika hanya dievaluasi pada satu titik piksel tunggal (*aperture problem*)! Bagaimana metode Lucas-Kanade mengatasi keterbatasan ini?

### Tugas Pemrograman Mandiri
Buatlah skrip Python yang membandingkan deteksi gerak truk buah antara: (1) `cv2.absdiff()` dan (2) `cv2.createBackgroundSubtractorMOG2()`. Rekam jumlah piksel aktif (*motion pixel count*) per frame pada kedua metode dan sajikan kurva perbandingannya menggunakan Matplotlib!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 11.9: Real-time Camera Processing

Kita telah menguasai cara mendeteksi gerak dan menganalisis aliran video rekaman menggunakan OpenCV. Namun, seluruh eksperimen kita sejauh ini masih dijalankan pada berkas video lokal yang telah tersimpan rapi di media penyimpanan. Bagaimana jika sistem harus dihubungkan langsung ke kamera pengawas CCTV IP (RTSP stream) atau kamera USB industri yang menyiarkan video langsung tanpa henti? Mengapa sering kali terjadi keterlambatan (*lag*) 2 hingga 5 detik saat kamera nyata dihubungkan ke loop pemrosesan OpenCV?

Pada **AI Modul 11.9: Real-time Camera Processing**, kita akan membedah arsitektur pemrosesan kamera real-time tingkat lanjut: merancang **Multi-Threaded Video Streamer** untuk mengeliminasi buffer latency driver kamera, menyematkan antarmuka OSD informatif, membangun mekanisme pemulihan otomatis saat koneksi kamera terputus, serta mengantarkan kita menuju era **Deep Learning untuk Computer Vision (Part 12)**.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Zivkovic, Z. (2004). Improved adaptive Gaussian mixture model for background subtraction. *Proceedings of the 17th International Conference on Pattern Recognition (ICPR)*, 2, 28-31.
2. Lucas, B. D., & Kanade, T. (1981). An iterative image registration technique with an application to stereo vision. *IJCAI'81: 7th International Joint Conference on Artificial Intelligence*, 2, 674-679.
3. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications* (2nd ed.). Springer. (Bab 9: Motion Estimation).
4. Bouwmans, T. (2014). Traditional and recent approaches in background modeling for foreground detection: An overview. *Computer Science Review*, 11, 31-66.
"""
    validate_text(md_content, "AI_Modul_11.8_Motion_detection.md")
    with open("docs/part-11/AI_Modul_11.8_Motion_detection.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-11/AI_Modul_11.8_Motion_detection.md")

    # Notebook 11.8
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 11.8: Praktikum Motion Detection\n",
                    "**Mata Kuliah:** Visi Komputer dan Pengolahan Citra Digital  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Mengimplementasikan deteksi gerak sederhana menggunakan diferensiasi bingkai absolut (`cv2.absdiff`).\n",
                    "2. Menerapkan pemodelan latar belakang statistik adaptif `cv2.createBackgroundSubtractorMOG2`.\n",
                    "3. Melakukan penyaringan bayangan bergerak (*shadow suppression*) dan pembersihan morfologi.\n",
                    "4. Memvisualisasikan bounding box objek bergerak pada sekuens simulasi pos pemantauan kebun.\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import cv2\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                    "print(f'OpenCV Version: {cv2.__version__}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Pembangkitan Sekuens Video Truk Buah Sawit Bergerak\n",
                    "Mensimulasikan sekuens video pemantauan jalan kebun dengan truk buah yang melintas beserta bayangan tanah."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "H, W = 350, 550\n",
                    "sequence = []\n",
                    "\n",
                    "for step in range(35):\n",
                    "    bg = np.full((H, W, 3), 110, dtype=np.uint8) # Jalan tanah perkebunan\n",
                    "    # Objek Truk (x bergerak dari 40 ke 420)\n",
                    "    x_pos = int(40 + step * 11)\n",
                    "    y_pos = 150\n",
                    "    # Gambar truk buah\n",
                    "    cv2.rectangle(bg, (x_pos, y_pos), (x_pos + 110, y_pos + 60), (25, 95, 215), -1)\n",
                    "    # Gambar bayangan di tanah (lebih gelap)\n",
                    "    cv2.rectangle(bg, (x_pos + 10, y_pos + 60), (x_pos + 120, y_pos + 72), (70, 70, 70), -1)\n",
                    "    sequence.append(bg)\n",
                    "\n",
                    "print(f'Jumlah Frame Sekuens Video Sintetis: {len(sequence)}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Deteksi Gerak: Frame Differencing vs Background Subtraction MOG2\n",
                    "Membandingkan hasil deteksi selisih frame sederhana dan model campuran Gaussian MOG2."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 1. Frame Differencing pada Frame #20 dan #21\n",
                    "gray_prev = cv2.cvtColor(sequence[19], cv2.COLOR_BGR2GRAY)\n",
                    "gray_curr = cv2.cvtColor(sequence[20], cv2.COLOR_BGR2GRAY)\n",
                    "diff = cv2.absdiff(gray_curr, gray_prev)\n",
                    "_, mask_diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)\n",
                    "\n",
                    "# 2. Background Subtraction MOG2 pada seluruh sekuens\n",
                    "mog2 = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=16, detectShadows=True)\n",
                    "mog2_masks = []\n",
                    "for f in sequence:\n",
                    "    fg = mog2.apply(f)\n",
                    "    mog2_masks.append(fg)\n",
                    "\n",
                    "target_fg = mog2_masks[20]\n",
                    "# Nilai 255: Objek sejati; Nilai 127: Bayangan\n",
                    "_, mask_pure_obj = cv2.threshold(target_fg, 200, 255, cv2.THRESH_BINARY)\n",
                    "\n",
                    "print(f'Piksel Aktif Frame Differencing : {cv2.countNonZero(mask_diff)}')\n",
                    "print(f'Piksel Aktif MOG2 (Tanpa Bayang): {cv2.countNonZero(mask_pure_obj)}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Hasil Masker Deteksi Gerak dan Eliminasi Bayangan\n",
                    "Menampilkan perbandingan citra asli, Frame Differencing, masker mentah MOG2, dan masker bersih."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, axes = plt.subplots(1, 4, figsize=(16, 4))\n",
                    "\n",
                    "axes[0].imshow(cv2.cvtColor(sequence[20], cv2.COLOR_BGR2RGB))\n",
                    "axes[0].set_title('1. Frame Asli (Truk & Bayangan)', fontsize=10, fontweight='bold')\n",
                    "axes[0].axis('off')\n",
                    "\n",
                    "axes[1].imshow(mask_diff, cmap='gray')\n",
                    "axes[1].set_title('2. Frame Diff: Objek Berlubang', fontsize=10, fontweight='bold')\n",
                    "axes[1].axis('off')\n",
                    "\n",
                    "axes[2].imshow(target_fg, cmap='gray')\n",
                    "axes[2].set_title('3. MOG2 Mentah (Abu=Bayangan)', fontsize=10, fontweight='bold')\n",
                    "axes[2].axis('off')\n",
                    "\n",
                    "axes[3].imshow(mask_pure_obj, cmap='gray')\n",
                    "axes[3].set_title('4. MOG2 Bersih (Bayangan Dieliminasi)', fontsize=10, fontweight='bold')\n",
                    "axes[3].axis('off')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_motion_detection_11_8.png', dpi=150)\n",
                    "plt.show()\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open("notebooks/part-11/AI_Modul_11.8_Praktikum_Motion_Detection.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-11/AI_Modul_11.8_Praktikum_Motion_Detection.ipynb")

    # Guide 11.8
    guide_content = r"""# AI Modul 11.8: Panduan Instruktur dan Kunci Solusi

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
"""
    validate_text(guide_content, "AI_Modul_11.8_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-11/AI_Modul_11.8_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-11/AI_Modul_11.8_Panduan_Instruktur_dan_Kunci_Solusi.md")

# ==============================================================================
# MODUL 11.9: Real-time Camera Processing
# ==============================================================================
def create_modul_11_9():
    md_content = r"""# AI Modul 11.9: Real-time Camera Processing

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-11-09
* **Mata Kuliah**: Visi Komputer dan Pengolahan Citra Digital (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Genap)
* **Prasyarat**: AI Modul 11.8 (Motion Detection)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Threaded Camera Streamer, Eliminasi Hardware Buffer Lag, OSD HUD Status"] --> B["OUTCOMES: Kemampuan Membangun Aplikasi Visi Komputer Kamera Langsung Tanpa Keterlambatan"]
    B --> C["IMPACTS: Kesiapan Sistem Inspeksi Real-Time Pabrik Kelapa Sawit & Transisi Mulus ke Deep Learning Vision"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** arsitektur pemrosesan aliran kamera langsung (*live camera stream*), mekanisme penyangga perangkat keras internal (*hardware driver buffer lag*) yang menyebabkan keterlambatan visual kumulatif, serta konsep konkurensi multi-utas (*multi-threading concurrency*) untuk memisahkan akuisisi frame I/O dari pemrosesan algoritma.
2. **Menerapkan (C3)** kelas pembaca kamera multi-utas berorientasi objek (`ThreadedCameraStream`) menggunakan pustaka `threading` Python dan OpenCV untuk menjamin pembacaan frame berkecepatan 30 FPS dengan latensi mendekati nol (*zero-latency reading*).
3. **Menganalisis (C4)** perbandingan profil latensi dan kestabilan laju bingkai antara pipeline sekuensial konvensional dan pipeline paralel multi-utas pada skenario kamera inspeksi stasiun penerimaan Tandan Buah Segar pabrik kelapa sawit.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan arsitektur software multi-threaded video stream dengan mekanisme antrean sinkronisasi aman (*thread-safe buffer*).
  * Skrip Python modular berstandar PEP 8 untuk pembacaan kamera multi-utas, anotasi HUD (*Heads-Up Display*), dan penanganan pemulihan koneksi terputus (*reconnection watchdog*).
  * Laporan komparasi kuantitatif latensi buffer antara metode pembacaan sekuensial vs multi-threaded.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian membangun sistem pengawasan real-time yang responsif tanpa delay pada perangkat komputer industri (*edge industrial PC*).
  * Kemampuan mengintegrasikan umpan balik visual langsung ke operator pabrik kelapa sawit secara interaktif.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Kesiapan infrastruktur komputasi tepi industri perkebunan menuju adopsi arsitektur Deep Learning Computer Vision modern pada Part 12.

---

## 2. Profil Fundamental Pemrosesan Kamera Real-Time: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Pemrosesan kamera real-time menjembatani akuisisi fluks citra perangkat keras kontinu dengan eksekusi algoritma visi komputer terapan:
1. **Eliminasi Penumpukan Penyangga Perangkat Keras (*Hardware Buffer Flushing*)**: Driver kamera sistem operasi (V4L2 di Linux, DirectShow/MSMF di Windows) secara default menyimpan antrean 3 hingga 5 frame internal. Jika algoritma pemrosesan membutuhkan waktu lebih lama daripada interval frame, konsumen akan selalu membaca frame masa lalu (*stale frames*). Multi-threading menguras antrean ini secara terus-menerus dan hanya menyediakan frame paling mutakhir (*freshest frame*).
2. **Penyematan Informasi Telemetri Spasial (*On-Screen Display HUD*)**: Menggambar grafik metrik performa (laju FPS, latensi inferensi milidetik, stempel waktu ISO 8601, status deteksi) langsung di atas frame video secara dinamis.
3. **Penyediaan Mekanisme Pemulihan Koneksi Otomatis (*Watchdog Reconnection*)**: Mendeteksi kegagalan pembacaan aliran RTSP kamera jaringan dan menginisialisasi ulang soket koneksi tanpa menghentikan aplikasi utama.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Sortasi TBS Berkecepatan Tinggi di Meja Konveyor**: Memastikan sistem kamera langsung bereaksi seketika (< 30 milidetik) saat buah melintas di bawah sensor pneumatik penyortir.
* **Sistem Navigasi Visual Drone Pemantau Kebun**: Mengalirkan video dari kamera fpv drone ke modul kendali otonom tanpa delay yang berisiko menyebabkan tabrakan dengan pohon sawit.
* **Monitoring CCTV Operator Stasiun Berbahaya**: Memberikan umpan video langsung tanpa jeda di ruang kendali pusat pabrik kelapa sawit.

### 2.3 Rationale: Alasan Mengapa Materi Ini Dipelajari
Banyak pengembang pemula mendapati model visi komputer mereka berjalan lambat dan memiliki delay 3 detik saat dipasang pada webcam atau kamera CCTV kebun, meskipun model mereka mampu berjalan pada 40 FPS. Masalah ini bukan disebabkan oleh kelemahan model AI, melainkan oleh arsitektur pembacaan sekuensial `cv2.VideoCapture` yang memblokir I/O. Menguasai arsitektur multi-threaded adalah jembatan wajib menuju sistem AI produksi.

### 2.4 Analisis Kelebihan dan Kekurangan: Sekuensial vs Multi-Threaded

| Parameter Evaluasi | Pipeline Sekuensial Standar | Pipeline Multi-Threaded OpenCV | Implikasi di Pabrik Kelapa Sawit |
| :--- | :--- | :--- | :--- |
| **Latensi Tampilan Frame** | Mengalami penumpukan jeda 1 - 5 detik. | Latensi nol (*real-time zero lag*). | Sangat krusial agar posisi fisik buah di konveyor cocok dengan koordinat deteksi. |
| **Ketergantungan I/O** | Pembacaan frame dan kalkulasi saling memblokir. | Pembacaan frame berjalan di latar belakang independen. | Beban komputasi deteksi tidak memperlambat laju akuisisi kamera. |
| **Kompleksitas Kode** | Sangat sederhana (hanya perulangan `while True`). | Memerlukan sinkronisasi thread dan locks. | Membutuhkan kode modular berorientasi objek yang rapi. |
| **Penggunaan CPU** | Rendah (1 core CPU). | Sedikit lebih tinggi (2 core CPU paralel). | Prosesor multi-core modern di PC industri siap menanganinya. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Pabrik Kelapa Sawit mengintegrasikan kamera resolusi tinggi dengan lengan robot penolak buah afkir di pintu sortir. Konveyor bergerak dengan kecepatan $1.2\text{ meter/detik}$. Pada pipeline sekuensial biasa, jeda penyangga kamera sebesar $1.5\text{ detik}$ menyebabkan lengan robot selalu memukul udara kosong karena buah afkir telah lewat $1.8\text{ meter}$ di depan. Setelah tim insinyur menerapkan arsitektur `ThreadedCameraStream`, latensi turun menjadi $22\text{ milidetik}$, sehingga lengan robot mampu menolak buah afkir secara presisi pada posisi fisiknya.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Thread-Safe Data Sharing**: Mengakses variabel frame bersama antar-thread memerlukan sinkronisasi penguncian memori (*mutex lock* / `threading.Lock`) untuk mencegah kondisi balapan (*race condition*) atau pembacaan citra yang setengah terisi.
2. **Kondisi Berhenti Bersih (*Clean Shutdown*)**: Thread pembaca kamera harus memiliki bendera pemberhentian (*stop flag*) agar saat aplikasi ditutup, thread dapat keluar secara elegan tanpa meninggalkan proses zombie di memori sistem operasi.

---

## 3. Landasan Teori & Konsep Matematis Pemrosesan Kamera Real-Time

![Arsitektur Real-Time Multithreaded Camera Stream OpenCV](../assets/arsitektur_real_time_multithreaded_camera_stream_opencv.png)

### 3.1 Masalah Penyangga Perangkat Keras (*Hardware Buffer Bottleneck*)
Ketika fungsi `cap.read()` dipanggil, fungsi tersebut mengeksekusi dua operasi internal:
1. `cap.grab()`: Mengambil frame berikutnya dari buffer driver kamera.
2. `cap.retrieve()`: Mendekode dan mengonversi frame mentah menjadi matriks array BGR NumPy.

Jika laju komputasi visual adalah $T_{\text{proc}}$ dan interval frame kamera adalah $T_{\text{cam}}$:
* Jika $T_{\text{proc}} > T_{\text{cam}}$, driver kamera terus memasukkan frame baru ke dalam buffer internal berkapasitas $N_{\text{buf}}$ (biasanya 3 - 5 frame).
* Ketika buffer penuh, frame tertua dibuang atau antrean tertunda. Akumulasi keterlambatan waktu (*latency*) dinyatakan sebagai:
  $$\text{Latency} = N_{\text{buf}} \times T_{\text{proc}}$$

Pada pipeline multi-threaded, Thread Akuisisi terus memanggil `cap.grab()` dan `cap.retrieve()` secepat mungkin tanpa komputasi lain, sehingga buffer driver selalu kosong ($N_{\text{buf}} \approx 0$). Thread Pemroses hanya mengambil frame yang paling akhir di-cache:

$$\text{Latency Multi-Threaded} \approx T_{\text{proc}} \quad (\text{Tanpa penumpukan antrean})$$

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    subgraph Thread 1: Akuisisi Frame (Background)
        A["Buka Kamera: cv2.VideoCapture(src)"] --> B["Loop: ret, frame = cap.read()"]
        B --> C["Kunci Mutex Lock"]
        C --> D["Perbarui Variabel latest_frame"]
        D --> E["Lepas Mutex Lock"]
        E --> B
    end
    subgraph Thread 2: Pemrosesan Utama (Foreground)
        F["Ambil Salinan latest_frame"] --> G["Eksekusi Algoritma Visi Komputer"]
        G --> H["Sematkan Anotasi OSD HUD & FPS"]
        H --> I["Tampilkan Visual / Kirim Sinyal Kontrol"]
        I --> F
    end
```

Implementasi kelas `ThreadedCameraStream` berorientasi objek menggunakan pustaka `threading` bawaan Python dan OpenCV:

```python
import cv2
import threading
import time
import numpy as np

# 1. Definisi Kelas Threaded Camera Streamer
class ThreadedCameraStream:
    def __init__(self, src=0, name="CameraThread"):
        self.stream = cv2.VideoCapture(src)
        self.name = name
        self.stopped = False
        self.lock = threading.Lock()
        
        # Baca frame inisial pertama
        self.ret, self.frame = self.stream.read()
        if not self.ret:
            # Jika kamera fisik tidak tersedia (lingkungan server/headless), gunakan frame sintetis
            self.frame = np.full((480, 640, 3), 50, dtype=np.uint8)
            self.ret = True
            self.is_synthetic = True
        else:
            self.is_synthetic = False
            
    def start(self):
        self.thread = threading.Thread(target=self.update, name=self.name, daemon=True)
        self.thread.start()
        return self
        
    def update(self):
        while not self.stopped:
            if not self.is_synthetic:
                ret, frame = self.stream.read()
                if not ret:
                    time.sleep(0.01)
                    continue
                with self.lock:
                    self.ret = ret
                    self.frame = frame
            else:
                # Simulasi pembaruan frame sintetis
                time.sleep(0.033) # 30 FPS
                with self.lock:
                    pass
                    
    def read(self):
        with self.lock:
            return self.ret, self.frame.copy()
            
    def stop(self):
        self.stopped = True
        if hasattr(self, 'thread'):
            self.thread.join(timeout=1.0)
        self.stream.release()

# 2. Uji Coba Eksekusi Pipeline Live Stream dengan Overlay OSD
camera = ThreadedCameraStream(src=0).start()
time.sleep(0.1) # Tunggu inisialisasi thread

fps_meter = []
t_start = time.perf_counter()

for iteration in range(30): # Simulasi 30 siklus pengambilan frame
    t0 = time.perf_counter()
    ret, frame = camera.read()
    if not ret:
        break
        
    # Pemrosesan visi komputer (deteksi kontur sederhana)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Anotasi Heads-Up Display (OSD)
    dt = time.perf_counter() - t0
    current_fps = 1.0 / max(dt, 1e-5)
    fps_meter.append(current_fps)
    
    cv2.putText(frame, f"LIVE CAM | FPS: {current_fps:.1f}", (20, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"STATUS: OPERATIONAL | SIKLUS #{iteration+1}", (20, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 200, 0), 1)

camera.stop()
print(f"[OK] Thread kamera dihentikan bersih. Rata-rata Throughput: {np.mean(fps_meter):.1f} FPS")
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Sistem Pengawasan Otomatis Loading Ramp PKS

### 5.1 Spesifikasi Masalah
Stasiun penerimaan tandan buah sawit membutuhkan sistem pemantauan live streaming yang terhubung ke kamera CCTV IP di atas konveyor. Sistem harus mampu mendeteksi potensi tumpahan buah atau kemacetan aliran, memberikan peringatan visual di layar kontrol operator, dan mencatat log latensi secara periodik.

### 5.2 Implementasi Desain Overlay HUD Indikator Kinerja PKS
```python
def draw_pks_hud_overlay(frame, throughput_tph, warning_status=False):
    H, W = frame.shape[:2]
    # Header banner semi-transparan
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (W, 60), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Text telemetri
    cv2.putText(frame, "PKS SAWIT SENTOSA - STASIUN LOADING RAMP 01", (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    status_text = "STATUS: WASPADA (MACET)" if warning_status else "STATUS: NORMAL"
    status_color = (0, 0, 255) if warning_status else (0, 255, 0)
    cv2.putText(frame, status_text, (15, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 2)
    
    cv2.putText(frame, f"Throughput: {throughput_tph:.1f} Ton/Jam", (W - 220, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 220, 0), 2)
    return frame

annotated_frame = draw_pks_hud_overlay(frame, throughput_tph=118.5, warning_status=False)
print("Overlay HUD PKS Berhasil Disematkan ke Frame Kamera!")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Mengabaikan Sinkronisasi Lock pada Threading**: Membaca dan menulis variabel `self.frame` secara bersamaan tanpa `with self.lock:` dapat menghasilkan citra yang terdistorsi (*frame tearing*).
2. **Membiarkan Thread Menggantung (*Hanging Thread*)**: Lupa menyetel `daemon=True` pada `threading.Thread` akan menyebabkan program Python tidak dapat ditutup di terminal saat pengguna menekan tombol Ctrl+C.
3. **Menggunakan `cv2.imshow()` di dalam Sub-Thread**: Pada beberapa sistem operasi (khususnya Windows dan macOS), pemanggilan fungsi GUI seperti `cv2.imshow()` dan `cv2.waitKey()` di luar thread utama (*main thread*) akan memicu crash GUI atau freeze. Selalu jalankan fungsi visualisasi display pada thread utama.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Gunakan Queue Berukuran 1 (*Drop-Oldest Buffer*)**: Jika ingin mentransfer frame antar-proses, gunakan struktur antrean dengan kapasitas maksimal 1 (`queue.Queue(maxsize=1)`) agar antrean selalu diperbarui dengan frame terbaru.
2. **Sediakan Fallback Headless**: Rancang kode agar dapat berjalan tanpa GUI fisik (`cv2.imshow`) pada lingkungan server cloud atau skrip uji otomatis.
3. **Implementasikan Logika Sambung Ulang (*Auto-Reconnect*)**: Uji apakah `cap.isOpened()` bernilai `False` atau `ret` bernilai `False` berulang kali, lalu lakukan pelepasan dan pembukaan ulang koneksi kamera setiap 5 detik.

---

## 7. Rangkuman Modul

* Pemrosesan kamera langsung menghadapi tantangan penumpukan penyangga perangkat keras (*hardware buffer lag*) jika dieksekusi secara sekuensial.
* Arsitektur *Multi-Threaded Camera Streamer* memisahkan penyerapan I/O frame berkecepatan tinggi dari thread komputasi utama, menjamin latensi inferensi mendekati nol.
* Penandaan informasi OSD HUD menyediakan visibilitas instan terhadap parameter operasional pabrik kelapa sawit secara real-time.
* Sinkronisasi memori menggunakan `threading.Lock` dan penetapan `daemon=True` menjamin keamanan konkurensi dan terminasi proses yang bersih.

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Analisis Akumulasi Penyangga Buffer (Bloom C4)**: Sebuah sistem pengawasan konveyor menggunakan kamera USB 30 FPS. Algoritma deteksi cacat buah yang dijalankan membutuhkan waktu komputasi 80 milidetik per frame ($t_{\text{proc}} = 80\text{ ms}$). Driver kamera memiliki kapasitas buffer internal sebesar 4 frame.
   * Berapakah laju bingkai per detik (FPS) efektif pemrosesan sistem tersebut?
   * Jika sistem dijalankan secara sekuensial biasa selama 1 menit, berapa detik keterlambatan (*lag*) visual yang dialami operator di layar kontrol saat melihat buah yang sedang melintas?
   * Bagaimana arsitektur *ThreadedCameraStream* memecahkan masalah keterlambatan tersebut?
2. **Evaluasi Keamanan Threading (Bloom C4)**: Mengapa pemanggilan `self.frame.copy()` di dalam blok `with self.lock:` mutlak diperlukan pada metode `read()`? Apa risiko matematis jika metode tersebut hanya mengembalikan referensi `self.frame` tanpa kloning memori?

### Tugas Pemrograman Mandiri
Lengkapilah kelas `ThreadedCameraStream` dengan metode `reconnect_if_needed(self)` yang memantau apakah frame gagal diterima selama lebih dari 3 detik, lalu secara otomatis mencoba menghubungkan kembali aliran kamera tanpa mematikan aplikasi utama!

---

## 9. Jembatan Konsep (Bridging) ke Part 12: Deep Learning untuk Computer Vision (AI Modul 12.1: CNN)

Selamat! Anda telah menuntaskan seluruh rangkaian modul praktikal pada **Part 11: OpenCV untuk Pengolahan Citra & Video**—mulai dari pengenalan arsitektur OpenCV C++, manipulasi geometri matriks citra, transformasi ruang warna HSV/LAB, binerisasi Otsu & Adaptif, ekstraksi kontur topologis, deteksi wajah Haar Cascade, pemrosesan aliran video temporal, deteksi gerak MOG2, hingga perancangan kamera real-time multi-threaded berlatensi nol.

Namun, perhatikan batasan mendasar dari seluruh teknik visi komputer klasik yang telah kita kuasai di Part 10 dan Part 11: seluruh metode tersebut mengandalkan **fitur-fitur yang dirumuskan secara manual (*handcrafted features*)**—seperti ambang batas warna HSV, kernel konvolusi terprogram, atau fitur Haar persegi panjang. Jika kondisi di lapangan perkebunan kelapa sawit sangat liar—misalnya bentuk daun sawit yang tertutup debu pekat, varietas bibit yang sangat mirip, atau tandan buah yang saling bertumpuk acak di atas tanah—metode manual ini mulai menemui batas kejenuhannya.

Bagaimana jika komputer dapat **mempelajari sendiri** ratusan filter konvolusi dan representasi visual yang paling optimal secara otomatis langsung dari jutaan piksel citra?

Pada bagian selanjutnya, yaitu **Part 12: Deep Learning untuk Computer Vision**, kita akan memasuki puncak revolusi kecerdasan buatan modern:
* Di **AI Modul 12.1: Convolutional Neural Network (CNN)**, kita akan membedah bagaimana operasi konvolusi spasial yang kita pelajari di OpenCV disatukan dengan jaringan saraf tiruan (Part 9) untuk membentuk arsitektur deep learning visual paling perkasa dalam sejarah AI.
* Kita akan mempelajari lapisan konvolusi 2D, fungsi aktivasi ReLU visual, lapisan penyusutan spasial (*Pooling*), *Transfer Learning*, arsitektur mutakhir (ResNet, MobileNet), hingga deteksi objek real-time menggunakan **YOLO (*You Only Look Once*)** untuk mengotomatisasi seluruh rantai pasok industri kelapa sawit masa depan!

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media.
2. Rosebrock, A. (2018). *Practical Python and OpenCV: An Introductory, Example-Driven Guide to Computer Vision* (4th ed.). PyImageSearch.
3. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications* (2nd ed.). Springer.
4. Alfatni, M. S. M., Shariff, A. R. M., Abdullah, M. Z., Marhaban, M. H. B., & Saaed, O. M. B. (2022). Oil palm fresh fruit bunch ripeness grading methods: A systematic review. *Computers and Electronics in Agriculture*, 198, 107040.
"""
    validate_text(md_content, "AI_Modul_11.9_Real-time_camera_processing.md")
    with open("docs/part-11/AI_Modul_11.9_Real-time_camera_processing.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-11/AI_Modul_11.9_Real-time_camera_processing.md")

    # Notebook 11.9
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 11.9: Praktikum Real-time Camera Processing\n",
                    "**Mata Kuliah:** Visi Komputer dan Pengolahan Citra Digital  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Membangun kelas pembaca aliran kamera multi-utas (`ThreadedCameraStream`) berbasis Python `threading`.\n",
                    "2. Mengeliminasi penumpukan penyangga (*hardware buffer lag*) untuk mencapai latensi nol pada pemrosesan kamera langsung.\n",
                    "3. Menyematkan antarmuka On-Screen Display (OSD HUD) dinamis dengan pemantauan FPS dan status operasional pabrik.\n",
                    "4. Mengevaluasi stabilitas konkurensi dan mekanisme penghentian thread yang aman (*clean shutdown*).\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import cv2\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import threading\n",
                    "import time\n",
                    "\n",
                    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                    "print(f'OpenCV Version: {cv2.__version__}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Implementasi Kelas Threaded Camera Streamer Berorientasi Objek\n",
                    "Membangun kelas pembaca frame di latar belakang independen dengan penguncian mutex `threading.Lock` dan fallback headless."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "class ThreadedCameraStream:\n",
                    "    def __init__(self, src=0, name='CameraThread'):\n",
                    "        self.stream = cv2.VideoCapture(src)\n",
                    "        self.name = name\n",
                    "        self.stopped = False\n",
                    "        self.lock = threading.Lock()\n",
                    "        \n",
                    "        self.ret, self.frame = self.stream.read()\n",
                    "        if not self.ret:\n",
                    "            # Fallback frame sintetis jika tidak ada webcam terpasang\n",
                    "            self.frame = np.full((480, 640, 3), 40, dtype=np.uint8)\n",
                    "            self.ret = True\n",
                    "            self.is_synthetic = True\n",
                    "        else:\n",
                    "            self.is_synthetic = False\n",
                    "            \n",
                    "    def start(self):\n",
                    "        self.thread = threading.Thread(target=self.update, name=self.name, daemon=True)\n",
                    "        self.thread.start()\n",
                    "        return self\n",
                    "        \n",
                    "    def update(self):\n",
                    "        counter = 0\n",
                    "        while not self.stopped:\n",
                    "            if not self.is_synthetic:\n",
                    "                ret, frame = self.stream.read()\n",
                    "                if not ret:\n",
                    "                    time.sleep(0.01)\n",
                    "                    continue\n",
                    "                with self.lock:\n",
                    "                    self.ret = ret\n",
                    "                    self.frame = frame\n",
                    "            else:\n",
                    "                # Update simulasi frame konveyor PKS\n",
                    "                time.sleep(0.02) # ~50 FPS simulasi\n",
                    "                counter = (counter + 1) % 640\n",
                    "                synth = np.full((480, 640, 3), 40, dtype=np.uint8)\n",
                    "                cv2.circle(synth, (counter, 240), 40, (15, 90, 220), -1)\n",
                    "                with self.lock:\n",
                    "                    self.frame = synth\n",
                    "                    \n",
                    "    def read(self):\n",
                    "        with self.lock:\n",
                    "            return self.ret, self.frame.copy()\n",
                    "            \n",
                    "    def stop(self):\n",
                    "        self.stopped = True\n",
                    "        if hasattr(self, 'thread'):\n",
                    "            self.thread.join(timeout=1.0)\n",
                    "        self.stream.release()\n",
                    "\n",
                    "print('Kelas ThreadedCameraStream berhasil didefinisikan!')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Eksekusi Pengujian Live Stream dengan Anotasi OSD HUD\n",
                    "Menjalankan stream multi-utas, menyematkan indikator HUD pabrik kelapa sawit, dan menghitung stabilitas FPS."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "cam = ThreadedCameraStream(src=0).start()\n",
                    "time.sleep(0.1)\n",
                    "\n",
                    "fps_records = []\n",
                    "display_sample = None\n",
                    "\n",
                    "for i in range(40):\n",
                    "    t_start = time.perf_counter()\n",
                    "    ret, frame = cam.read()\n",
                    "    if not ret:\n",
                    "        break\n",
                    "        \n",
                    "    # Simulasi beban pemrosesan visi komputer (grayscaling + thresholding)\n",
                    "    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\n",
                    "    _, mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)\n",
                    "    \n",
                    "    dt = time.perf_counter() - t_start\n",
                    "    fps_val = 1.0 / max(dt, 1e-5)\n",
                    "    fps_records.append(fps_val)\n",
                    "    \n",
                    "    # Penambahan HUD Telemetri PKS\n",
                    "    cv2.rectangle(frame, (0, 0), (640, 50), (20, 20, 20), -1)\n",
                    "    cv2.putText(frame, 'PKS LOADING RAMP 01 - LIVE STREAM', (15, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)\n",
                    "    cv2.putText(frame, f'STATUS: NORMAL | FPS: {fps_val:.1f}', (15, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)\n",
                    "    cv2.putText(frame, f'Throughput: 115.4 Ton/Jam', (420, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 255), 1)\n",
                    "    \n",
                    "    if i == 20:\n",
                    "        display_sample = frame.copy()\n",
                    "\n",
                    "cam.stop()\n",
                    "print(f'Selesai 40 iterasi live stream!')\n",
                    "print(f'Rata-rata FPS Eksekusi Multi-Threaded: {np.mean(fps_records):.1f} FPS')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Hasil Pengujian Stream dan Frame HUD\n",
                    "Menampilkan grafik stabilitas FPS dan tampilan HUD stasiun loading ramp pabrik sawit."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))\n",
                    "\n",
                    "ax1.plot(fps_records, color='mediumseagreen', linewidth=2, marker='.')\n",
                    "ax1.set_title('Kestabilan Laju Bingkai Threaded Camera Streamer', fontsize=11, fontweight='bold')\n",
                    "ax1.set_xlabel('Nomor Siklus Pengambilan')\n",
                    "ax1.set_ylabel('Throughput (FPS)')\n",
                    "\n",
                    "if display_sample is not None:\n",
                    "    ax2.imshow(cv2.cvtColor(display_sample, cv2.COLOR_BGR2RGB))\n",
                    "    ax2.set_title('Cuplikan Layar OSD HUD Loading Ramp PKS', fontsize=11, fontweight='bold')\n",
                    "    ax2.axis('off')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_realtime_camera_11_9.png', dpi=150)\n",
                    "plt.show()\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open("notebooks/part-11/AI_Modul_11.9_Praktikum_Real-time_Camera_Processing.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-11/AI_Modul_11.9_Praktikum_Real-time_Camera_Processing.ipynb")

    # Guide 11.9
    guide_content = r"""# AI Modul 11.9: Panduan Instruktur dan Kunci Solusi

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
"""
    validate_text(guide_content, "AI_Modul_11.9_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-11/AI_Modul_11.9_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-11/AI_Modul_11.9_Panduan_Instruktur_dan_Kunci_Solusi.md")

if __name__ == '__main__':
    create_modul_11_7()
    create_modul_11_8()
    create_modul_11_9()
