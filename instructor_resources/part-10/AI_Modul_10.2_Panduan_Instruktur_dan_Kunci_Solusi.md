# AI Modul 10.2: Panduan Instruktur dan Kunci Solusi Komputasi
## Representasi Citra Digital dan Matriks Piksel

**Mata Kuliah:** Visi Komputer dan Kecerdasan Buatan Terapan  
**Kode Mata Kuliah / SKS:** AI-10-02 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Sarjana Pertanian / Informatika Agro-Industri (INSTIPER Yogyakarta)  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 10.2 meletakkan fondasi operasional bagaimana citra digital diperlakukan sebagai **struktur data komputasi numerik murni**. Instruktur diharapkan tidak hanya mengajarkan fungsi pustaka OpenCV secara dangkal, melainkan menanamkan pemahaman arsitektur sistem komputer: bagaimana array 2D dan 3D disimpan di dalam memori fisik RAM (*memory layout*), mengapa tipe data `uint8` memiliki risiko aritmatika yang fatal, dan bagaimana mengelola memori secara efisien saat memproses citra drone berukuran gigapixel.

Tiga fokus pedagogis utama:
1. **Tata Letak Memori Kontigu (*Row-Major C-Contiguity*)**: Mahasiswa harus memahami bahwa matriks 2D $H \times W$ diorganisasikan sebagai array 1D linear di RAM. Pengirisan (*slicing*) baris jauh lebih cepat daripada pengirisan kolom karena memanfaatkan hierarki *CPU cache line*.
2. **Dilema View vs Copy**: Menekankan pentingnya isolasi data mentah saat mengekstraksi Region of Interest (ROI). Perubahan pada ROI berbasis *view* akan merusak integritas data citra asli.
3. **Koreksi Gamma Adaptif via Lookup Table**: Menjelaskan konsep efisiensi komputasi $\mathcal{O}(1)$ versus pemanggilan operasi daya eksponensial per piksel $\mathcal{O}(H \times W)$.

### 1.2 Miskonsepsi Umum Mahasiswa & Strategi Remedi
* **Miskonsepsi 1: Menganggap operasi aritmatika penambahan citra selalu aman dengan operator biasa `+`.**
  * *Penjelasan Korektif*: NumPy menggunakan aritmatika modulo $256$ untuk `uint8`. Nilai $240 + 30 = 270$ akan dibungkus (*wrapped*) menjadi $14$, menghasilkan piksel hitam abnormal pada area daun yang sangat terang. Instruktur wajib mendemonstrasikan fungsi `cv2.add()` yang menerapkan fungsi saturasi (*clipping* pada 255).
* **Miskonsepsi 2: Menganggap pengirisan `roi = img[100:200, 100:200]` membuat salinan data baru di RAM.**
  * *Penjelasan Korektif*: NumPy memegang prinsip efisiensi *zero-copy*. `roi` hanyalah penunjuk (*pointer*) ke blok memori yang sama. Jika mahasiswa menggambar garis anotasi pada `roi`, citra `img` asal akan tercoret permanen. Remedinya adalah membiasakan pemanggilan metode `.copy()`.
* **Miskonsepsi 3: Tertukar antara ukuran dimensi citra $(W, H)$ dan indeks array $(H, W)$.**
  * *Penjelasan Korektif*: Citra beresolusi $1920 \times 1080$ memiliki $W = 1920$ dan $H = 1080$. Namun bentuk array NumPy adalah `img.shape = (1080, 1920)`. Mengakses piksel pada koordinat $(x, y)$ wajib dituliskan sebagai `img[y, x]`.

---

## 2. Kunci Jawaban Lengkap & Pembahasan Soal Analitis HOTS

### Pembahasan Soal 1: Kalkulasi Kebutuhan Memori dan Bandwidth Drone Ortofoto (C3)
**Pertanyaan:**  
Resolusi kamera $24\text{ MP}$ ($6000 \times 4000$ piksel), $C = 3$ saluran RGB, kecepatan tangkap $2\text{ FPS}$.  
1. Ukuran memori 1 frame citra mentah nir-kompresi ($8\text{-bit}$ per saluran).  
2. Laju *throughput* data kartu memori (MB/detik).  
3. Persentase kenaikan ukuran jika diganti sensor multispektral 5-kanal $16\text{-bit}$.

**Langkah Penyelesaian Analitis:**
1. **Kalkulasi Ukuran Memori 1 Frame ($8\text{-bit}$ RGB):**
   * Total piksel per saluran = $6000 \times 4000 = 24.000.000\text{ piksel}$.
   * Total elemen tensor 3-saluran = $24.000.000 \times 3 = 72.000.000\text{ byte}$ ($1\text{ byte/piksel}$ untuk $8\text{-bit}$).
   * Dalam satuan Megabyte desimal ($10^6$) atau biner ($2^{20} = 1.048.576\text{ byte}$):
     $$\text{Ukuran} = \frac{72.000.000\text{ B}}{1.048.576\text{ B/MB}} \approx 68.66\text{ MB (atau } 72.00\text{ MB desimal)}$$

2. **Kalkulasi Laju Throughput Data Penyimpanan:**
   $$\text{Throughput} = \text{Ukuran per Frame} \times \text{FPS} = 68.66\text{ MB} \times 2\text{ frame/detik} = 137.33\text{ MB/detik}$$
   *Rekomendasi Rekayasa*: Kartu memori drone wajib memiliki kecepatan tulis minimal standar SD Express atau CFexpress Video Speed Class V90 / V150 untuk mencegah *dropped frames*.

3. **Kalkulasi Citra Multispektral 5-Kanal $16\text{-bit}$ ($2\text{ Bytes/piksel}$):**
   * Ukuran citra baru = $6000 \times 4000 \times 5\text{ kanal} \times 2\text{ Bytes} = 240.000.000\text{ Bytes} \approx 228.88\text{ MB}$.
   * Rasio perbandingan ukuran = $\frac{240.000.000}{72.000.000} = \frac{10}{3} \approx 3.333$ kali lipat.
   * Persentase kenaikan ukuran:
     $$\text{Kenaikan} = \left(\frac{240 - 72}{72}\right) \times 100\% = \frac{168}{72} \times 100\% = 233.33\%$$

---

### Pembahasan Soal 2: Diagnostik Patologi Aritmatika Piksel Mesokarp Buah Sawit (C4)
**Pertanyaan:**  
Intensitas awal $I_{\text{awal}} = [220, 60, 10]$ (kanal BGR, di mana $B=220, G=60, R=10$). Ingin ditambah kecerahan $+45$.  
* Alternatif A: `img_A = img + 45` (NumPy).  
* Alternatif B: `img_B = cv2.add(img, 45)` (OpenCV).

**Langkah Penyelesaian & Pembuktian:**
1. **Analisis Alternatif A (NumPy Add - Modulo Arithmetic):**
   Tipe data `uint8` mengeksekusi operasi modulo $256$:
   * Kanal Blue  : $(220 + 45) \pmod{256} = 265 \pmod{256} = 9$  <-- **Pembalikan Nilai Ekstrem!**
   * Kanal Green : $(60 + 45) \pmod{256} = 105 \pmod{256} = 105$
   * Kanal Red   : $(10 + 45) \pmod{256} = 55 \pmod{256} = 55$
   * Hasil Vektor A : $I_A = [9, 105, 55]$.

2. **Analisis Alternatif B (OpenCV Add - Saturated Arithmetic):**
   OpenCV memotong nilai pada batas atas 255:
   * Kanal Blue  : $\min(220 + 45, 255) = \min(265, 255) = 255$
   * Kanal Green : $\min(60 + 45, 255) = \min(105, 255) = 105$
   * Kanal Red   : $\min(10 + 45, 255) = \min(55, 255) = 55$
   * Hasil Vektor B : $I_B = [255, 105, 55]$.

3. **Penjelasan Anomali Visual Fatal Alternatif A:**
   Pada Alternatif A, saluran Blue yang awalnya sangat dominan ($220$) anjlok menjadi hampir nol ($9$) akibat *overflow*. Akibatnya, piksel mesokarp sawit yang semula berwarna biru-oranye terang mendadak berubah menjadi kehijauan gelap kotor. Ini memicu distorsi kromatik yang merusak klasifikasi fraksi kematangan buah sawit pada sistem visi industri.

---

### Pembahasan Soal 3: Optimasi Kurva Gamma untuk Pemantauan Kanopi Berbayang (C4)
**Pertanyaan:**  
Area pelepah berbayang memiliki intensitas $r \in [0.05, 0.25]$. Pilih $\gamma = 0.4$ atau $\gamma = 2.5$.

**Langkah Penyelesaian & Analisis:**
1. **Pemilihan Nilai Gamma & Pembuktian Turunan:**
   Fungsi transformasi: $s = r^\gamma$. Turunan pertama terhadap masukan adalah laju perubahan penguatan lokal:
   $$\frac{ds}{dr} = \gamma \cdot r^{\gamma - 1}$$
   * Untuk $\gamma = 0.4 < 1.0$:
     $$\frac{ds}{dr} = 0.4 \cdot r^{-0.6} = \frac{0.4}{r^{0.6}}$$
     Ketika $r \to 0$ (area gelap), $\frac{ds}{dr} \gg 1$. Sebagai contoh, pada $r = 0.1$, $\frac{ds}{dr} \approx 1.59$. Nilai gradien yang besar berarti rentang intensitas sempit $[0.05, 0.25]$ akan diregangkan secara agresif:
     $$s(0.05) = 0.05^{0.4} \approx 0.301, \quad s(0.25) = 0.25^{0.4} \approx 0.574$$
     Rentang dinamis melebar dari $0.20$ menjadi $0.273$, mengangkat kontras urat daun di area bayangan gelap secara tajam.
   * Untuk $\gamma = 2.5 > 1.0$:
     $$\frac{ds}{dr} = 2.5 \cdot r^{1.5}$$
     Pada area gelap $r = 0.1$, $\frac{ds}{dr} \approx 0.079 \ll 1$. Nilai gelap akan semakin dimampatkan menuju hitam pekat ($s(0.05) \approx 0.0005$, $s(0.25) \approx 0.031$).
   * *Keputusan*: **Wajib memilih $\gamma = 0.4$**.

2. **Konsekuensi Visual pada Area Terang ($r = 0.95$):**
   Pada $\gamma = 0.4$, untuk $r$ mendekati $1.0$, turunan $\frac{ds}{dr} = \frac{0.4}{0.95^{0.6}} \approx 0.413 < 1$. Rentang intensitas terang akan dimampatkan (*compressed*). Nilai $r = 0.95$ dipetakan ke $s = 0.95^{0.4} \approx 0.980$. Area jalan perkebunan yang sudah terang akan sedikit lebih terang namun mengalami penurunan kontras lokal (*slight loss of highlight contrast*), tanpa mengalami pemotongan saturasi ekstrem.

---

## 3. Rubrik Penilaian Praktikum Laboratorium Komputasi

| Bobot Penilaian | Komponen Evaluasi | Indikator Keberhasilan |
|:---:|:---|:---|
| **30%** | **Keberhasilan Eksekusi & Anti-Overflow** | Skrip Python/NumPy/OpenCV berjalan 100% bebas galat, mampu menunjukkan perbedaan modulo vs saturasi dengan bukti komputasi yang valid. |
| **35%** | **Ketepatan Manipulasi Spasial & ROI** | Berhasil memotong ROI brondolan sawit dengan menggunakan `.copy()`, memahami orientasi koordinat $(y, x)$, dan mengukur alokasi memori secara presisi. |
| **35%** | **Analisis Diagnostik & Optimasi Gamma** | Mahasiswa mampu merancang tabel Lookup Table (LUT) untuk transformasi gamma dan menjelaskan perilaku kurva matematika secara analitis terhadap citra kanopi. |

---

## 4. Panduan Pengayaan & Proyek Mandiri Tambahan
Bagi mahasiswa berkinerja tinggi (*advanced learners*):
* Bangun antarmuka interaktif menggunakan slider OpenCV (`cv2.createTrackbar`) untuk mengatur nilai $\alpha$ (kontras), $\beta$ (kecerahan), dan $\gamma$ (gamma) secara *real-time* pada video umpan langsung kamera webcam atau drone.
* Implementasikan fungsi penghitungan histogram intensitas piksel 256-bin secara manual menggunakan array NumPy tanpa memanggil `cv2.calcHist`.
