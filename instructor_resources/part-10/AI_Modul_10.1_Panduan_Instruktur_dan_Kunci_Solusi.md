# AI Modul 10.1: Panduan Instruktur dan Kunci Solusi Komputasi
## Konsep dan Fundamental Computer Vision

**Mata Kuliah:** Visi Komputer dan Kecerdasan Buatan Terapan  
**Kode Mata Kuliah / SKS:** AI-10-01 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Sarjana Pertanian / Informatika Agro-Industri (INSTIPER Yogyakarta)  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 10.1 merupakan gerbang pembuka bagi mahasiswa untuk beralih dari pemrosesan data tabular dan sinyal satu dimensi (1D) menuju persepsi visual spasial multi-dimensi (2D dan 3D). Instruktur diharapkan menekankan bahwa citra digital bukanlah sekadar gambar estetis, melainkan **fungsi matriks intensitas radiasi elektromagnetik** yang dihasilkan oleh interaksi hukum fisika optik antara sumber cahaya, materi objek, dan karakteristik sensor semikonduktor.

Tiga pilar pedagogis utama yang wajib dikuasai mahasiswa:
1. **Dekomposisi Iluminasi-Reflektansi ($I = L \cdot R$)**: Mahasiswa harus memahami bahwa kamera merekam intensitas pantulan $I$, bukan warna intrinsik objek $R$. Ini menjelaskan mengapa daun kelapa sawit yang sama dapat memiliki nilai RGB berbeda pada waktu pagi, siang terik, atau saat tertutup awan mendung.
2. **Geometri Proyeksi Kamera Lubang Jarum (*Pinhole Model*)**: Menanamkan intuisi hilangnya dimensi kedalaman ($Z$) saat ruang 3D diproyeksikan ke bidang sensor 2D, serta peran matriks intrinsik $\mathbf{K}$ dalam mengubah satuan meter menjadi satuan piksel.
3. **Kompensasi Distorsi Lensa**: Memahami mengapa citra mentah dari kamera drone bersudut lebar (*wide-angle*) tidak boleh langsung digunakan untuk pengukuran luas kanopi tanpa proses *undistortion*.

### 1.2 Miskonsepsi Umum Mahasiswa & Strategi Remedi
* **Miskonsepsi 1: Mengira sistem visi komputer "melihat" seperti mata manusia.**
  * *Penjelasan Korektif*: Mata manusia memiliki respons adaptasi iluminasi non-linier dinamis (melalui pelebaran pupil dan sel fotoreseptor retina), sedangkan sensor kamera digital merekam kuantisasi muatan elektron linier per fotositus. Tanpa kalibrasi white balance dan normalisasi, komputer tidak memiliki persepsi kekonstanan warna (*color constancy*).
* **Miskonsepsi 2: Tertukar antara koordinat matriks $(row, col)$ dengan koordinat citra $(u, v)$ atau $(x, y)$.**
  * *Penjelasan Korektif*: Dalam representasi array NumPy `img[y, x]`, indeks baris pertama merepresentasikan sumbu vertikal ($y$ atau $v$, dari atas ke bawah), sedangkan indeks kolom kedua merepresentasikan sumbu horizontal ($x$ atau $u$, dari kiri ke kanan). Ingatkan mahasiswa bahwa OpenCV dan NumPy memiliki konvensi indeks yang saling terbalik pada pembacaan dimensi: `cv2.resize(img, (width, height))` vs `img.shape = (height, width)`.
* **Miskonsepsi 3: Menganggap citra beresolusi lebih tinggi selalu menghasilkan akurasi AI yang lebih baik.**
  * *Penjelasan Korektif*: Peningkatan resolusi melipatgandakan beban memori dan waktu komputasi secara kuadratik ($\mathcal{O}(H \cdot W)$). Pada banyak tugas inspeksi kanopi, resolusi berlebih hanya menangkap derau tekstur mikro yang tidak relevan bagi model klasifikasi.

---

## 2. Kunci Jawaban Lengkap & Pembahasan Soal Analitis HOTS

### Pembahasan Soal 1: Analisis Proyeksi Pinhole Kamera Drone (C3)
**Pertanyaan:**  
Drone terbang pada ketinggian $H = 50\text{ m}$, jarak fokal fisik $f = 6.0\text{ mm} = 0.006\text{ m}$, ukuran piksel sensor $d_x = d_y = 3.0\ \mu\text{m} = 3.0 \times 10^{-6}\text{ m}$. Titik prinsip optik $(c_x, c_y) = (1920, 1080)$. Dua pohon sawit terpisah sejauh $\Delta X = 9.0\text{ meter}$.

**Langkah Penyelesaian Analitis:**
1. **Kalkulasi Jarak Fokal dalam Satuan Piksel ($f_x$):**
   $$f_x = \frac{f}{d_x} = \frac{0.006\text{ m}}{3.0 \times 10^{-6}\text{ m}} = 2000.0\text{ piksel}$$

2. **Kalkulasi Jarak Spasial di Bidang Piksel Sensor ($\Delta u$):**
   Berdasarkan kesebangunan segitiga pada proyeksi kamera lubang jarum:
   $$\frac{\Delta u}{f_x} = \frac{\Delta X}{Z}$$
   Karena drone mengarah nadir tegak lurus, jarak kedalaman optik $Z$ sama dengan ketinggian terbang $H = 50\text{ meter}$:
   $$\Delta u = f_x \cdot \frac{\Delta X}{H} = 2000 \cdot \frac{9.0}{50.0} = 2000 \cdot 0.18 = 360.0\text{ piksel}$$

3. **Kalkulasi Nilai Ground Sampling Distance (GSD):**
   $$\text{GSD} = \frac{H \cdot d_x}{f} = \frac{50.0\text{ m} \cdot 3.0 \times 10^{-6}\text{ m}}{0.006\text{ m}} = 0.025\text{ m/piksel} = 2.50\text{ cm/piksel}$$
   *Verifikasi*: $\Delta u \times \text{GSD} = 360\text{ piksel} \times 2.5\text{ cm/piksel} = 900\text{ cm} = 9.0\text{ meter}$ (Terbukti konsisten eksak).

---

### Pembahasan Soal 2: Dekomposisi Iluminasi-Reflektansi & Fenomena Bayangan Awan (C4)
**Pertanyaan:**  
Intensitas awal daun sawit $I_1 = 180$ saat tersinari matahari langsung ($L_1 = 1.0$). Saat awan melintas, iluminasi turun menjadi $L_2 = 0.4$, intensitas menjadi $I_2 = 72$.

**Langkah Penyelesaian & Pembuktian:**
1. **Pembuktian Invarian Nilai Reflektansi Intrinsik ($R$):**
   Model pembentukan citra: $I = L \cdot R \implies R = I / L$.
   * Pada kondisi matahari cerah: $R_1 = \frac{I_1}{L_1} = \frac{180}{1.0} = 180$ (atau ternormalisasi $R_1 = \frac{180/255}{1.0} \approx 0.706$).
   * Pada kondisi tertutup awan: $R_2 = \frac{I_2}{L_2} = \frac{72}{0.4} = 180$ (atau ternormalisasi $R_2 = \frac{72/255}{0.4} \approx 0.706$).
   * *Kesimpulan*: Nilai $R_1 = R_2$, membuktikan bahwa **sifat reflektansi fisik daun kelapa sawit tidak berubah sama sekali**. Perubahan nilai piksel murni disebabkan oleh pelemahan energi sumber cahaya matahari.

2. **Penyebab Kegagalan Ambang Batas Absolut:**
   Jika sebuah algoritma cerdas menggunakan aturan heuristik: *"Jika intensitas hijau $I < 100$, klasifikasikan sebagai daun terinfeksi defisiensi nitrogen"*, maka ketika awan melintas ($I = 72$), daun yang sehat sempurna akan divonis menderita defisiensi nitrogen (*False Positive Error*). Ini membuktikan bahaya mendasar dari penggunaan nilai intensitas piksel absolut di lingkungan luar ruangan.

3. **Strategi Mitigasi Rekayasa:**
   * **Transformasi Homomorfik (*Homomorphic Filtering*)**: Mengambil logaritma natural dari citra: $\ln I(x, y) = \ln L(x, y) + \ln R(x, y)$. Komponen iluminasi $\ln L$ yang berfrekuensi spasial rendah ditapis menggunakan *High-Pass Filter*, sehingga hanya menyisakan variasi reflektansi $\ln R$ yang berfrekuensi spasial tinggi.
   * **Pemanfaatan Indeks Rasio Spektral Terkalibrasi**: Menggunakan indeks rasio pita (seperti NDVI atau rasio kanal $R/G$) di mana fluktuasi iluminasi skalar $L$ tereliminasi karena membagi pembilang dan penyebut secara proporsional.

---

### Pembahasan Soal 3: Diagnostik Distorsi Barel vs Pincushion (C4)
**Pertanyaan:**  
Kalibrasi menghasilkan $k_1 = -0.28$ dan $k_2 = 0.05$.

**Langkah Penyelesaian:**
1. **Identifikasi Jenis Distorsi:**
   Faktor distorsi radial adalah $f(r) = 1 + k_1 r^2 + k_2 r^4$.
   Karena nilai koefisien utama **$k_1 < 0$ (negatif)**, faktor pengali radial bernilai kurang dari 1 seiring bertambahnya jarak $r$ dari pusat optik. Hal ini menyebabkan titik-titik di pinggir bidang citra tertekan ke arah pusat, yang merupakan ciri diagnostik definitif dari **Distorsi Barel (*Barrel Distortion*)**, fenomena khas pada lensa bersudut pandang lebar (*wide-angle lens*).
2. **Dampak terhadap Estimasi Volume TBS di Tepi Konveyor:**
   Pada distorsi barel, area di tepi bidang citra mengalami kompresi spasial non-linier (objek tampak lebih kecil dan melengkung cembung). Jika sistem sortasi menghitung volume atau bobot tandan buah segar (TBS) berbasis integrasi luas kontur piksel tanpa koreksi distorsi, maka buah yang melintas di tepi pinggir konveyor akan diestimasi memiliki ukuran dan bobot yang **jauh lebih kecil daripada ukuran fisik sebenarnya (*underestimation bias*)**, menyebabkan kerugian klasifikasi sortasi pabrik.

---

## 3. Rubrik Penilaian Praktikum Laboratorium Komputasi

| Bobot Penilaian | Komponen Evaluasi | Indikator Keberhasilan |
|:---:|:---|:---|
| **30%** | **Keberhasilan Eksekusi Program** | Skrip Python/OpenCV berjalan mulus tanpa *runtime error*, menghasilkan grafik proyeksi pinhole dan dekomposisi citra yang presisi. |
| **35%** | **Ketepatan Matematis & Analitik** | Formulasi matriks intrinsik $\mathbf{K}$, kalkulasi GSD, dan penurunan dekomposisi $I=L \cdot R$ diuraikan dengan langkah aljabar yang runtut dan benar. |
| **35%** | **Analisis Diagnostik Lapangan** | Mahasiswa mampu mengaitkan konsep optik fisika dengan tantangan nyata perkebunan (bayangan awan, distorsi barel kamera drone, dan standardisasi protokol penerbangan). |

---

## 4. Panduan Pengayaan & Proyek Mandiri Tambahan
Bagi mahasiswa berkinerja tinggi (*advanced learners*), instruktur dapat menugaskan proyek mandiri:
* Melakukan kalibrasi kamera menggunakan rekaman 15 foto papan catur (*checkerboard*) dari kamera ponsel pintar masing-masing menggunakan `cv2.calibrateCamera`.
* Mengukur nilai galat reproyeksi (*Root Mean Square Reprojection Error*) dan menguji fungsi `cv2.undistort` untuk meluruskan garis bengkok pada dinding gedung laboratorium.
