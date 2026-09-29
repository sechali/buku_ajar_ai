# AI Modul 10.6: Panduan Instruktur dan Kunci Solusi Komputasi
## Deteksi Tepi dan Gradien Citra (Edge Detection and Image Gradients)

**Mata Kuliah:** Visi Komputer dan Kecerdasan Buatan Terapan  
**Kode Mata Kuliah / SKS:** AI-10-06 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Sarjana Pertanian / Informatika Agro-Industri (INSTIPER Yogyakarta)  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 10.6 mengalihkan fokus dari domain intensitas kecerahan citra ke domain **perubahan spasial lokal (kalkulus diferensial diskrit)**. Dalam aplikasi perkebunan dan pabrik kelapa sawit, kemampuan mengenali batas kanopi, menghitung orientasi barisan tanaman, dan mengekstrak siluet buah sawit sangat bergantung pada ketepatan kalkulasi gradien.

Tiga pilar pedagogis utama:
1. **Representasi Fisik vs Arah Vektor Gradien**: Mahasiswa kerap mengalami kebingungan mengenai arah vektor gradien versus arah garis tepi fisik. Instruktur harus menekankan bukti geometris bahwa vektor gradien $\nabla f$ selalu menunjuk ke arah laju kenaikan intensitas tercepat, sehingga garis fisik batas tepi (*edge boundary*) **selalu tegak lurus mutlak ($90^\circ$)** terhadap vektor gradien tersebut.
2. **Keterbatasan Tipe Data Numerik**: Menanamkan pemahaman pentingnya pemilihan tipe data bertanda (`cv2.CV_64F`) pada operator Sobel/Scharr. Penggunaan `cv2.CV_8U` memotong gradien negatif menjadi nol, menghilangkan separuh kontur tanaman.
3. **Mekanisme Multi-Tahap Canny**: Memandu mahasiswa menelusuri bagaimana pelembutan Gaussian, NMS, dan histeresis ganda berkolaborasi menghasilkan garis tepi 1-piksel yang kontinu tanpa menghasilkan derau semu.

### 1.2 Miskonsepsi Umum Mahasiswa & Strategi Remedi
* **Miskonsepsi 1: Mengira arah vektor gradien adalah arah garis tepi daun.**
  * *Penjelasan Korektif*: Jika sebuah pelepah daun membentang vertikal dari atas ke bawah, intensitas piksel berubah drastis dari kiri (tanah gelap) ke kanan (daun terang). Vektor gradien mengarah horizontal ($0^\circ$), sedangkan garis pelepah daun itu sendiri berorientasi vertikal ($90^\circ$). Arah tepi adalah $\theta_{\text{edge}} = \theta_{\text{grad}} \pm 90^\circ$.
* **Miskonsepsi 2: Menggunakan operator Laplacian langsung pada citra tanpa pelembutan Gaussian.**
  * *Penjelasan Korektif*: Turunan kedua $\nabla^2 f$ sangat sensitif terhadap derau frekuensi tinggi. Menjalankan Laplacian pada citra berderau akan menghasilkan ribuan persilangan nol semu. Remedinya adalah mendemonstrasikan keunggulan *Laplacian of Gaussian (LoG)* yang melembutkan citra terlebih dahulu sebelum diferensiasi.
* **Miskonsepsi 3: Mengira piksel tepi lemah (*Weak Edge*) pada detektor Canny selalu dipertahankan.**
  * *Penjelasan Korektif*: Piksel tepi lemah hanya dipertahankan jika terhubung secara spasial (8-konektivitas) dengan setidaknya satu piksel tepi kuat (*Strong Edge*). Jika terisolasi, piksel lemah akan dibuang untuk mencegah derau bintik sensor diakui sebagai kontur tanaman.

---

## 2. Kunci Jawaban Lengkap & Pembahasan Soal Analitis HOTS

### Pembahasan Soal 1: Kalkulasi Vektor Gradien Sobel dan Orientasi Tepi Pelepah Sawit (C3)
**Data Diberikan:**
* Petak citra $\mathbf{I}_{3 \times 3}$:
  $$\mathbf{I} = \begin{bmatrix} 40 & 50 & 180 \\ 45 & 55 & 185 \\ 40 & 50 & 180 \end{bmatrix}$$
* Kernel Sobel:
  $$\mathbf{S}_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}, \quad \mathbf{S}_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

**Langkah Penyelesaian Analitis:**
1. **Kalkulasi Gradien Horizontal $G_x$:**
   $$G_x = (-1)(40) + (0)(50) + (1)(180) + (-2)(45) + (0)(55) + (2)(185) + (-1)(40) + (0)(50) + (1)(180)$$
   $$G_x = (-40 + 180) + (-90 + 370) + (-40 + 180) = 140 + 280 + 140 = +560$$

2. **Kalkulasi Gradien Vertikal $G_y$:**
   $$G_y = (-1)(40) + (-2)(50) + (-1)(180) + (0)(45) + (0)(55) + (0)(185) + (1)(40) + (2)(50) + (1)(180)$$
   $$G_y = (-40 - 100 - 180) + 0 + (40 + 100 + 180) = -320 + 320 = 0$$

3. **Kalkulasi Magnitudo Gradien:**
   * Eksak Euclidean: $M = \sqrt{G_x^2 + G_y^2} = \sqrt{560^2 + 0^2} = 560.0$
   * Aproksimasi Manhattan: $M_{\text{approx}} = |G_x| + |G_y| = |560| + |0| = 560.0$

4. **Kalkulasi Sudut Orientasi Gradien dan Arah Garis Tepi:**
   * Sudut vektor gradien: $\theta = \arctan\left(\frac{G_y}{G_x}\right) = \arctan\left(\frac{0}{560}\right) = 0.0^\circ$ (vektor gradien mengarah horizontal ke kanan).
   * Arah fisik garis tepi pelepah sawit:
     $$\theta_{\text{edge}} = 0^\circ \pm 90^\circ = 90^\circ \text{ (Vertikal Murni)}$$

---

### Pembahasan Soal 2: Analisis Algoritma Non-Maximum Suppression (NMS) pada Detektor Canny (C3)
**Data Diberikan:**
* Piksel pusat: $p = (50, 50)$, $M(p) = 85$, sudut kontinu $\theta = 72^\circ$.
* Matriks magnitudo lokal $3 \times 3$:
  $$\mathbf{M} = \begin{bmatrix} 40 & 92 & 70 \\ 50 & 85 & 80 \\ 30 & 75 & 60 \end{bmatrix}$$

**Langkah Penyelesaian Analitis:**
1. **Kuantisasi Sektor Sudut:**
   * Rentang sektor vertikal ($90^\circ$) adalah $[67.5^\circ, 112.5^\circ]$.
   * Karena $\theta = 72^\circ \in [67.5^\circ, 112.5^\circ]$, maka sudut **dikuantisasi ke Sektor $90^\circ$ (Vertikal)**.

2. **Penentuan Pasangan Piksel Pembanding:**
   * Pada sektor $90^\circ$ (vertikal), orientasi gradien berjalan ke atas dan ke bawah.
   * Dua tetangga pembanding adalah tetangga atas $(50, 49)$ dan tetangga bawah $(50, 51)$:
     * Tetangga atas: $M_{\text{atas}} = 92$
     * Tetangga bawah: $M_{\text{bawah}} = 75$

3. **Evaluasi Kriteria NMS:**
   * Kriteria NMS mewajibkan: $M(p) \ge M_{\text{atas}}$ DAN $M(p) \ge M_{\text{bawah}}$.
   * Evaluasi: $M(p) = 85 < M_{\text{atas}} = 92$.
   * **Keputusan Komputasional**: Piksel pusat $p$ **ditekan menjadi 0 (*suppressed to 0*)** karena bukan merupakan puncak lokal (*local ridge maximum*) di sepanjang garis normal gradien vertikal.

---

### Pembahasan Soal 3: Diagnostik Ambang Batas Histeresis pada Pelacakan Siluet Buah Sawit (C4)
**Data Diberikan:**
* Ambang batas: $T_{\text{low}} = 40$, $T_{\text{high}} = 100$.
* Rantai 5 piksel bersebelahan (8-konektivitas): $P_1 = 115, P_2 = 70, P_3 = 55, P_4 = 35, P_5 = 80$.

**Langkah Penyelesaian Analitis:**
1. **Klasifikasi Awal Berdasarkan Nilai Magnitudo:**
   * $P_1 = 115 \ge 100 \implies$ **Strong Edge** (pasti tepi).
   * $P_2 = 70 \in [40, 100) \implies$ **Weak Edge** (tepi kandidat).
   * $P_3 = 55 \in [40, 100) \implies$ **Weak Edge** (tepi kandidat).
   * $P_4 = 35 < 40 \implies$ **Non-Edge** (bukan tepi, dibuang ke 0).
   * $P_5 = 80 \in [40, 100) \implies$ **Weak Edge** (tepi kandidat).

2. **Pelacakan Tepi Spasial (*Edge Tracking by Hysteresis*):**
   * $P_1$ dikonfirmasi sebagai tepi (nilai biner 255).
   * $P_2$ bertetangga langsung dengan strong edge $P_1$, maka $P_2$ diaktifkan (nilai 255).
   * $P_3$ bertetangga dengan $P_2$ (yang sudah menjadi bagian kontur aktif), maka $P_3$ diaktifkan (nilai 255).
   * $P_4$ adalah non-edge ($35 < 40$), sehingga dinolkan (nilai 0). Terjadi pemutusan rantai!
   * $P_5$ adalah weak edge, namun karena terputus oleh $P_4$, $P_5$ tidak memiliki jalur 8-konektivitas yang bersambung ke $P_1$. Maka $P_5$ **dieliminasi (ditekan ke 0)** sebagai derau terisolasi.
   * **Status Citra Biner Akhir**: $P_1 = 255, P_2 = 255, P_3 = 255, P_4 = 0, P_5 = 0$.

3. **Dampak Kenaikan Ambang Bawah Menjadi $T_{\text{low}} = 60$:**
   * Jika $T_{\text{low}} = 60$, maka nilai $P_3 = 55 < 60$ berubah status dari weak edge menjadi **Non-Edge**.
   * Rantai konektivitas terputus lebih awal di $P_3$.
   * **Implikasi Rekayasa**: Hanya $P_1$ dan $P_2$ yang dipertahankan. Kontur siluet brondolan buah sawit menjadi terpotong prematur (*broken/fragmented contours*), menyebabkan kegagalan deteksi kontur tertutup pada modul ekstraksi morfometri buah.

---

## 3. Kunci Jawaban & Implementasi Kode Solusi Praktikum

```python
import cv2
import numpy as np

def detect_canopy_perimeter_and_contours(canopy_image, t_low=40, t_high=120, gsd_m=0.025):
    """
    Ekstraksi garis tepi kanopi sawit menggunakan detektor Canny
    dan estimasi keliling fisik tajuk pohon (meter).
    """
    # 1. Pelembutan Gaussian awal untuk menekan derau rumput mikro
    blurred = cv2.GaussianBlur(canopy_image, (5, 5), sigmaX=1.2)
    
    # 2. Detektor Canny dengan ambang histeresis optimal
    edges = cv2.Canny(blurred, threshold1=t_low, threshold2=t_high)
    
    # 3. Hitung keliling tajuk
    edge_pixels = np.sum(edges > 0)
    perimeter_meters = edge_pixels * gsd_m
    
    return edges, edge_pixels, perimeter_meters
```

---

## 4. Rubrik Penilaian Holistik & Pedoman Skoring

| Komponen Evaluasi | Bobot (%) | Indikator Kinerja Utama |
|:---|:---:|:---|
| **Ketepatan Teori Gradien & Deteksi Tepi** | 25% | Mampu membedakan operator orde 1 & 2, menguraikan arah ortogonal garis tepi, dan merumuskan tahapan Canny. |
| **Kalkulasi Numerik & Analisis NMS HOTS** | 30% | Menghitung konvolusi Sobel, sektor NMS kuantisasi, dan evaluasi rantai histeresis secara presisi dan sistematis. |
| **Implementasi Kode OpenCV & Parameter Tuning** | 35% | Mengembangkan alur deteksi tepi Canny dengan pemilihan tipe data bertanda (`CV_64F`) dan rasio histeresis proporsional. |
| **Kerapian Dokumentasi & Komentar Ilmiah** | 10% | Menyajikan laporan rapi, bebas dari istilah terlarang, dan berfokus pada pemecahan masalah nyata agrokompleks. |
