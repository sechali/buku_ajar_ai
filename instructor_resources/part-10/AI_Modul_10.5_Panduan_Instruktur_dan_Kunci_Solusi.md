# AI Modul 10.5: Panduan Instruktur dan Kunci Solusi Komputasi
## Operasi Filter Spasial dan Konvolusi 2D

**Mata Kuliah:** Visi Komputer dan Kecerdasan Buatan Terapan  
**Kode Mata Kuliah / SKS:** AI-10-05 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Sarjana Pertanian / Informatika Agro-Industri (INSTIPER Yogyakarta)  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 10.5 membedah operasi konvolusi spasial 2D yang merupakan fondasi paling fundamental dari pemrosesan sinyal citra klasik hingga arsitektur *Convolutional Neural Networks* (CNN). Dalam aplikasi rekayasa agrokompleks, instruktur harus menjembatani konsep matematis formal dengan kendala fisik di lapangan (panas sensor drone, getaran konveyor sortasi, dan fluktuasi pencahayaan alami).

Tiga fokus pengajaran utama:
1. **Dinamika Konvolusi vs Korelasi**: Memastikan mahasiswa memahami mengapa rotasi kernel $180^\circ$ diperlukan dalam konvolusi matematika formal (sifat komutatif dan asosiatif pemrosesan sinyal linier), namun mengapa korelasi silang digunakan secara universal dalam pustaka industri (OpenCV dan PyTorch) untuk efisiensi komputasi.
2. **Keterpisahan Kernel Gaussian (Kernel Separability)**: Menanamkan intuisi efisiensi algoritma komputasi $\mathcal{O}(K^2)$ versus $\mathcal{O}(2K)$. Mahasiswa harus menyadari bahwa untuk citra beresolusi tinggi, optimasi matematis ini menentukan kelayakan implementasi waktu nyata (*real-time processing*).
3. **Filter Linier vs Non-Linier pada Degradasi Sensor**: Menunjukkan secara gamblang mengapa filter rata-rata (linier) gagal total dalam menangani derau impulsif (*salt-and-pepper*), dan bagaimana *Median Filter* serta *Bilateral Filter* bekerja melalui mekanisme non-linier yang mempertahankan ketajaman kontur pelepah dan urat daun kelapa sawit.

### 1.2 Miskonsepsi Umum Mahasiswa & Strategi Remedi
* **Miskonsepsi 1: Menganggap filter pelembut rata-rata (Box filter) cocok untuk semua jenis derau.**
  * *Penjelasan Korektif*: Filter rata-rata memperlakukan derau impulsif sebagai sinyal valid dan meratakannya ke seluruh piksel tetangga. Akibatnya, satu bintik derau sensor rusak menyebar menjadi gumpalan kabur yang merusak visual. Instruktur wajib menunjukkan komparasi metrik PSNR yang membuktikan keunggulan mutlak *Median Filter* pada derau *salt-and-pepper*.
* **Miskonsepsi 2: Mengabaikan masalah underflow integer pada teknik penajaman citra (*Unsharp Masking*).**
  * *Penjelasan Korektif*: Operasi pengurangan `img - blurred` pada array `uint8` memicu pembungkusan (*wrapping*) modulo 256. Nilai selisih negatif $-20$ berubah menjadi $236$, menciptakan artefak bintik putih palsu. Remedinya adalah mewajibkan konversi ke `np.float32` sebelum pengurangan, diikuti oleh fungsi `np.clip(..., 0, 255).astype(np.uint8)`.
* **Miskonsepsi 3: Mengira Bilateral Filter selalu lebih baik daripada Gaussian Blur dalam segala situasi.**
  * *Penjelasan Korektif*: Bilateral filter memiliki kompleksitas komputasi yang jauh lebih berat karena bobot radiometrik harus dihitung ulang untuk setiap pasangan piksel berdasarkan nilai intensitas lokal, sehingga kernel tidak dapat dipisahkan (*non-separable*). Penggunaannya harus selektif, khususnya saat preservasi batas tepi objek (*edge preservation*) menjadi prioritas kritis.

---

## 2. Kunci Jawaban Lengkap & Pembahasan Soal Analitis HOTS

### Pembahasan Soal 1: Kalkulasi Konvolusi 2D Manual dengan Penanganan Padding Replikasi (C3)
**Data Diberikan:**
* Petak citra $\mathbf{A}_{3 \times 3}$:
  $$\mathbf{A} = \begin{bmatrix} 120 & 130 & 140 \\ 115 & 125 & 135 \\ 110 & 120 & 130 \end{bmatrix}$$
* Kernel penajam Laplacian $\mathbf{W}_{3 \times 3}$:
  $$\mathbf{W} = \begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end{bmatrix}$$

**Langkah Penyelesaian Analitis:**
1. **Kalkulasi Piksel Pusat $g(1, 1)$:**
   * Elemen citra yang bersesuaian dengan elemen kernel non-nol:
     * Elemen atas $(0, 1) = 130$, bobot $w = -1$
     * Elemen kiri $(1, 0) = 115$, bobot $w = -1$
     * Elemen pusat $(1, 1) = 125$, bobot $w = 5$
     * Elemen kanan $(1, 2) = 135$, bobot $w = -1$
     * Elemen bawah $(2, 1) = 120$, bobot $w = -1$
   * Nilai konvolusi:
     $$g(1, 1) = (-1)(130) + (-1)(115) + (5)(125) + (-1)(135) + (-1)(120)$$
     $$g(1, 1) = -130 - 115 + 625 - 135 - 120 = 625 - 500 = 125$$
   * *Analisis*: Karena gradien intensitas pada petak ini bersifat linier sempurna (kenaikan seragam), nilai turunan kedua Laplacian bernilai nol, sehingga intensitas piksel pusat tidak berubah.

2. **Evaluasi Batas dengan Replicate Padding pada Titik $(0, 0)$:**
   * Piksel sudut $A(0, 0) = 120$.
   * Dengan *replicate padding*, koordinat di luar batas baris $-1$ mereplikasi baris $0$, dan kolom $-1$ mereplikasi kolom $0$:
     $$\mathbf{A}_{\text{pad}(0,0)} = \begin{bmatrix} 120 & 120 & 130 \\ 120 & 120 & 130 \\ 115 & 115 & 125 \end{bmatrix}$$

3. **Kalkulasi Hasil Penapisan pada Sudut Atas-Kiri $g(0, 0)$:**
   $$g(0, 0) = (-1)(120) + (-1)(120) + (5)(120) + (-1)(130) + (-1)(115)$$
   $$g(0, 0) = -120 - 120 + 600 - 130 - 115 = 600 - 485 = 115$$

---

### Pembahasan Soal 2: Dekomposisi Keterpisahan Kernel Gaussian dan Analisis Throughput Komputasi (C3)
**Data Diberikan:**
* Resolusi video: Full HD ($1920 \times 1080 = 2.073.600\text{ piksel/frame}$)
* Kecepatan: $30\text{ FPS} \implies 2.073.600 \times 30 = 62.208.000\text{ piksel/detik}$
* Ukuran kernel Gaussian: $K = 11 \times 11$
* Kapasitas prosesor: $1.5\text{ GMAC/s} = 1.5 \times 10^9\text{ MAC/s}$.

**Langkah Penyelesaian Analitis:**
1. **Konvolusi 2D Langsung (Non-Separable):**
   * Jumlah operasi MAC per piksel = $K^2 = 11^2 = 121\text{ MAC}$.
   * Total beban komputasi per detik:
     $$\text{Beban}_{\text{2D}} = 62.208.000 \times 121 = 7.527.168.000\text{ MAC/s} \approx 7.53\text{ GMAC/s}$$

2. **Konvolusi 1D Terpisah (Separable):**
   * Jumlah operasi MAC per piksel = $2K = 2 \times 11 = 22\text{ MAC}$.
   * Total beban komputasi per detik:
     $$\text{Beban}_{\text{1D}} = 62.208.000 \times 22 = 1.368.576.000\text{ MAC/s} \approx 1.37\text{ GMAC/s}$$

3. **Rasio Efisiensi & Analisis Kelayakan Waktu Nyata:**
   * Faktor percepatan teoretis:
     $$\text{Speedup} = \frac{K^2}{2K} = \frac{121}{22} = 5.5\times$$
   * **Evaluasi Perangkat Keras**:
     * Pendekatan 2D langsung membutuhkan $7.53\text{ GMAC/s} \gg 1.5\text{ GMAC/s}$ (melebihi kapasitas hardware $502\%$, terjadi *frame drop* parah, FPS aktual hanya mampu $\sim 6\text{ FPS}$).
     * Pendekatan separable 1D membutuhkan $1.37\text{ GMAC/s} < 1.5\text{ GMAC/s}$ (berada di bawah kapasitas maksimum, **mampu berjalan stabil pada 30 FPS secara waktu nyata**).

---

### Pembahasan Soal 3: Analisis Matematis Bilateral Filter pada Batas Pelepah Daun Sawit (C4)
**Data Diberikan:**
* Piksel pusat $p$ pada daun: $f(p) = 200$. Parameter: $\sigma_s = 2.0$, $\sigma_r = 30.0$.
* Tetangga $q_1$ (daun): $f(q_1) = 195$, jarak spasial $d = 1$.
* Tetangga $q_2$ (bayangan pelepah): $f(q_2) = 45$, jarak spasial $d = 1$.

**Langkah Penyelesaian Analitis:**
1. **Bobot Spasial $w_s$ ($d = 1$):**
   $$w_s = \exp\left(-\frac{d^2}{2\sigma_s^2}\right) = \exp\left(-\frac{1^2}{2(2.0)^2}\right) = \exp\left(-\frac{1}{8}\right) = \exp(-0.125) \approx 0.8825$$

2. **Bobot Radiometrik $w_r$ untuk Tetangga Daun $q_1$ ($|f(q_1) - f(p)| = 5$):**
   $$w_r(q_1) = \exp\left(-\frac{5^2}{2(30.0)^2}\right) = \exp\left(-\frac{25}{1800}\right) = \exp(-0.01389) \approx 0.9862$$
   * Bobot gabungan $w(p, q_1) = w_s \times w_r(q_1) = 0.8825 \times 0.9862 \approx 0.8703$.

3. **Bobot Radiometrik $w_r$ untuk Tetangga Bayangan $q_2$ ($|f(q_2) - f(p)| = 155$):**
   $$w_r(q_2) = \exp\left(-\frac{155^2}{2(30.0)^2}\right) = \exp\left(-\frac{24025}{1800}\right) = \exp(-13.3472) \approx 1.597 \times 10^{-6}$$
   * Bobot gabungan $w(p, q_2) = w_s \times w_r(q_2) = 0.8825 \times 1.597 \times 10^{-6} \approx 1.409 \times 10^{-6}$.

4. **Komparasi Rasio Bobot & Argumentasi Saintifik:**
   $$\text{Rasio} = \frac{w(p, q_1)}{w(p, q_2)} = \frac{0.8703}{1.409 \times 10^{-6}} \approx 617.672$$
   * **Kesimpulan Analitis**: Bobot tetangga bayangan $q_2$ bernilai $600.000$ kali lebih kecil dibanding tetangga daun $q_1$. Dalam perhitungan rata-rata terbobot, kontribusi piksel bayangan praktis nol ($0.00016\%$). Hal ini membuktikan secara matematis bahwa Bilateral Filter mempertahankan garis batas tepi pelepah secara absolut tanpa mengalami efek pengaburan melintasi batas kontras.

---

## 3. Kunci Jawaban & Implementasi Kode Solusi Praktikum

```python
import cv2
import numpy as np

def agro_denoising_and_sharpening_pipeline(image_uint8):
    """
    Pipeline restorasi citra daun/buah sawit multi-tahap:
    1. Eliminasi derau impulsif via Median Filter
    2. Edge-preserving smoothing via Bilateral Filter
    3. Peningkatan kontur pelepah via Unsharp Masking aman
    """
    # 1. Tahap 1: Hilangkan derau bintik putih/hitam
    denoised_step1 = cv2.medianBlur(image_uint8, ksize=3)
    
    # 2. Tahap 2: Haluskan tekstur daun tanpa mengaburkan tepi pelepah
    denoised_step2 = cv2.bilateralFilter(denoised_step1, d=7, sigmaColor=50, sigmaSpace=50)
    
    # 3. Tahap 3: Unsharp Masking dalam format float32
    blurred = cv2.GaussianBlur(denoised_step2, (0, 0), sigmaX=1.2)
    high_freq_mask = denoised_step2.astype(np.float32) - blurred.astype(np.float32)
    
    sharpened = denoised_step2.astype(np.float32) + 1.2 * high_freq_mask
    final_output = np.clip(sharpened, 0, 255).astype(np.uint8)
    
    return final_output
```

---

## 4. Rubrik Penilaian Holistik & Pedoman Skoring

| Komponen Evaluasi | Bobot (%) | Indikator Kinerja Utama |
|:---|:---:|:---|
| **Ketepatan Teori Konvolusi & Filter** | 25% | Mampu membedakan konvolusi vs korelasi, merumuskan separability kernel, dan menguraikan fungsi bobot bilateral filter. |
| **Kalkulasi Numerik & Analisis Kompleksitas HOTS** | 30% | Menghitung konvolusi padding replikasi, perbandingan throughput hardware, dan rasio bobot bilateral filter secara presisi. |
| **Implementasi Kode OpenCV & Keamanan Numerik** | 35% | Mengembangkan skrip penapisan terpadu (Median, Bilateral, Unsharp Masking) dengan pencegahan overflow/underflow uint8. |
| **Kerapian Dokumentasi & Komentar Ilmiah** | 10% | Menyajikan laporan terstruktur rapi, bebas dari istilah yang dilarang, dan berfokus pada rekayasa agrokompleks. |
