# AI Modul 11.3: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-03
* **Topik Utama**: Konversi Ruang Warna (BGR, Grayscale, HSV, CIELAB) & Segmentasi Spektral
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Ruang Warna, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Teori Warna, Diktat Modul 11.3, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Model warna fisika vs komputasi: batasan RGB/BGR di lingkungan kebun, keunggulan pemisahan luminansi-krominansi.
* **Menit 25 - 50**: Matematika konversi BGR ke HSV, rentang Hue 8-bit OpenCV ($0-179$), dan penanganan khusus warna merah melingkar.
* **Menit 50 - 120**: Praktikum komputer: konversi warna multi-ruang, segmentasi buah sawit matang dengan `inRange`, dan masking bitwise.
* **Menit 120 - 150**: Asesmen formatif dan diskusi pemanfaatan ruang warna CIELAB pada analisis mutu CPO di laboratorium.

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teori Ruang Warna** | Menjelaskan perbedaan fundamental BGR, HSV, dan CIELAB serta skala Hue $0-179$ secara akurat. | Mampu menjelaskan konsep HSV namun lupa menyebutkan batas atas $179$ di OpenCV. | Menganggap seluruh ruang warna memiliki rentang nilai yang persis sama. |
| **Implementasi Masking Spektral** | Merumuskan batas bawah/atas HSV dan menggabungkan masker ganda untuk warna merah tanpa error. | Mampu membuat masker tunggal namun tidak mengetahui cara menangani warna merah melingkar. | Salah memasukkan urutan parameter BGR alih-alih HSV pada `cv2.inRange`. |
| **Analisis Hasil Segmentasi** | Menghitung rasio luas area buah matang dan mengevaluasi ketahanan terhadap variasi bayangan. | Menampilkan hasil visualisasi dengan baik namun kurang tajam dalam analisis persentase area. | Gagal mengisolasi objek target akibat penentuan ambang batas yang tidak tepat. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Sensitivitas Fotometrik Grayscale
1. **Alasan Bobot Kanal Hijau ($0.587$) Paling Tinggi**:
   Mata manusia memiliki tiga jenis sel fotoreseptor kerucut (*cones*): S (pendek/biru), M (menengah/hijau), dan L (panjang/merah). Kerapatan sel kerucut M dan L mendominasi retina manusia dengan puncak kurva efisiensi bercahaya fotopik (*luminous efficiency function* $V(\lambda)$) berada pada panjang gelombang sekitar $555\text{ nm}$ (wilayah spektrum hijau-kekuningan). Oleh karena itu, standar fotometri internasional ITU-R BT.601 memberikan bobot tertinggi pada kanal hijau ($58.7\%$) agar citra grayscale tampak memiliki tingkat kecerahan yang paling sesuai dengan persepsi visual manusia.
2. **Implikasi terhadap Deteksi Klorosis**:
   Daun sawit yang mengalami klorosis (menguning) mengalami penurunan klorofil drastis dan peningkatan pantulan spektrum merah-kuning. Pada citra grayscale, karena bobot merah ($0.299$) dan hijau ($0.587$) keduanya relatif tinggi, daun kuning pucat akan tampak sangat terang (*high intensity gray*), sedangkan daun sehat hijau pekat memiliki intensitas yang berbeda, sehingga memudahkan penentuan ambang batas pemisahan penyakit.

### Jawaban Soal Konseptual 2: Evaluasi Ruang Warna BGR vs HSV
Pada pukul 07.00 pagi (cahaya redup), fluks foton matahari yang mencapai kanopi kelapa sawit sangat rendah, sehingga nilai ketiga kanal BGR jatuh ke nilai rendah (misalnya $R=20, G=70, B=15$). Pada pukul 12.00 siang (cahaya terik), nilai ketiga kanal melonjak tinggi (misalnya $R=70, G=220, B=50$). Jika digunakan ambang batas statis pada BGR (misalnya $G \in [150, 255]$), maka pada pukul 07.00 pagi daun sawit akan gagal terdeteksi (*false negative*) karena nilai $G=70$ berada di bawah ambang batas.
Sebaliknya, pada ruang warna HSV:
* Pukul 07.00: Rasio antar kanal menghasilkan $H \approx 65$, $S \approx 200$, $V \approx 70$.
* Pukul 12.00: Rasio antar kanal menghasilkan $H \approx 65$, $S \approx 200$, $V \approx 220$.
Meskipun intensitas $V$ melonjak tiga kali lipat, nilai corak warna $H$ tetap konstan pada nilai $65$ (spektrum hijau sejati). Dengan menyetel ambang batas pada $H \in [40, 85]$, algoritma OpenCV mampu mendeteksi kanopi daun sawit secara konsisten tanpa terpengaruh oleh pergantian waktu dan intensitas sinar matahari.
