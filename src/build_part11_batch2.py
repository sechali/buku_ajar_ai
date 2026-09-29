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
# MODUL 11.4: Thresholding
# ==============================================================================
def create_modul_11_4():
    md_content = r"""# AI Modul 11.4: Thresholding

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-11-04
* **Mata Kuliah**: Visi Komputer dan Pengolahan Citra Digital (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Genap)
* **Prasyarat**: AI Modul 11.3 (Color Conversion)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pemahaman Binerisasi Citra, Formulasi Otsu Varians Intra-Kelas, Adaptive Threshold"] --> B["OUTCOMES: Kemampuan Memisahkan Objek Agrikultur dari Latar Belakang pada Pencahayaan Non-Uniform"]
    B --> C["IMPACTS: Segmentasi Otomatis Defek Buah & Kanopi Kebun yang Tangguh Menghadapi Bayangan Awan"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** prinsip dasar binerisasi citra, pembagian kelas latar depan (*foreground*) dan latar belakang (*background*), perbedaan mendasar antara penambangan ambang batas global (*global thresholding*), metode penentuan ambang batas optimal otomatis Otsu, serta penambangan ambang batas adaptif lokal (*adaptive local thresholding*).
2. **Menerapkan (C3)** fungsi `cv2.threshold()` dengan berbagai tipe flag penambangan (`THRESH_BINARY`, `THRESH_BINARY_INV`, `THRESH_OTSU`) serta `cv2.adaptiveThreshold()` dengan algoritma Mean dan Gaussian menggunakan pustaka OpenCV pada citra pertanian.
3. **Menganalisis (C4)** formulasi matematika varians antar-kelas (*inter-class variance*) pada algoritma Otsu serta mengevaluasi trade-off ukuran jendela lingkungan (*block size*) pada penanganan gradien bayangan tajuk kelapa sawit di lapangan.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Derivasi matematis fungsi objektif Otsu untuk histogram bimodal.
  * Skrip Python modular berstandar PEP 8 yang membandingkan performa binerisasi ambang global statis, Otsu, dan Adaptif Gaussian.
  * Plot visual hasil segmentasi biner tandan buah sawit di bawah kondisi pencahayaan tidak seragam (*non-uniform illumination*).
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian menentukan teknik binerisasi yang paling tepat berdasarkan karakteristik histogram intensitas citra komoditas pertanian.
  * Kemampuan mengisolasi kontur cacat permukaan buah tanpa terpengaruh oleh gradien bayangan alami.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Peningkatan akurasi sortasi otomatis di pabrik kelapa sawit dan keandalan sistem inspeksi drone terhadap fluktuasi cuaca perkebunan.

---

## 2. Profil Fundamental Thresholding: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Thresholding (penambangan nilai ambang batas) adalah operasi segmentasi citra tingkat dasar yang mentransformasikan citra berskala abu-abu kontinu ($I(x, y) \in [0, 255]$) menjadi citra biner hitam-putih ($B(x, y) \in \{0, 255\}$):
1. **Pemisahan Semantik Biner**: Membagi populasi piksel ke dalam dua hipotesis kelas: objek minat ($\mathcal{C}_1$) dan latar belakang ($\mathcal{C}_0$) berdasarkan nilai ambang $T$:
   $$B(x, y) = \begin{cases} 255, & \text{jika } I(x, y) \ge T \\ 0, & \text{jika } I(x, y) < T \end{cases}$$
2. **Optimasi Varians Statistik (Metode Otsu)**: Mencari nilai ambang batas optimal $T^*$ yang memaksimalkan separabilitas antar-kelas secara otomatis tanpa intervensi manusia.
3. **Kompensasi Iluminasi Lokal (Metode Adaptif)**: Menghitung nilai ambang batas dinamis $T(x, y)$ untuk setiap piksel berdasarkan rata-rata atau pembobotan Gaussian pada jendela lingkungan berukuran $B \times B$.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Segmentasi Bercak Daun Penyakit Hawar/Bercak**: Mengisolasi lesi nekrotik berwarna gelap pada daun kelapa sawit untuk mengukur luas keparahan infeksi secara objektif.
* **Deteksi Butir Brondolan Sawit**: Memisahkan butiran buah sawit yang terlepas di lantai konveyor dari permukaan pelat besi meja sortasi.
* **Binarisasi Citra Tajuk Ortofoto Drone**: Memisahkan kanopi vegetasi hijau pekat dari permukaan tanah perkebunan dan rumput liar.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
1. **Komputasi Sangat Ringan**: Operasi thresholding dieksekusi dalam kompleksitas $O(H \cdot W)$ dan dapat diparalelisasi penuh pada GPU atau mikroprosesor murah.
2. **Prasyarat Ekstraksi Kontur**: Sebagian besar algoritma analisis bentuk dan pelacakan topologi kontur di OpenCV mensyaratkan citra masukan bertipe biner.

### 2.4 Analisis Kelebihan dan Kekurangan Metode Thresholding

| Metode | Parameter Kunci | Keunggulan Utama | Kelemahan Kritis | Skenario Penggunaan Kebun |
| :--- | :--- | :--- | :--- | :--- |
| **Global Threshold** | Nilai ambang statis $T$ | Kecepatan eksekusi tercepat. | Gagal total jika intensitas cahaya tidak merata. | Ruang inspeksi tertutup dengan lampu studio konstan. |
| **Otsu Binarization** | Tanpa parameter (otomatis) | Menemukan ambang optimal secara mandiri pada histogram bimodal. | Menghasilkan binarisasi buruk jika histogram bersifat unimodal. | Sortasi buah di stasiun dengan pencahayaan semi-terkontrol. |
| **Adaptive Gaussian** | Ukuran jendela ($B$), offset $C$ | Sangat tahan terhadap gradien bayangan awan dan sudut cahaya matahari. | Lebih lambat secara komputasi, sensitif terhadap derau bintik. | Citra ortofoto drone dan kamera pengawas luar ruangan. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Sebuah armada drone memotret blok perkebunan sawit pada sore hari saat matahari berada di sudut rendah ($30^\circ$). Bayangan tajuk pohon yang panjang menutupi separuh kanopi pohon di sebelahnya. Penambangan global statis gagal total karena kanopi yang berada di bawah bayangan memiliki nilai intensitas yang sama dengan tanah terbuka. Dengan menerapkan **Adaptive Gaussian Thresholding** dengan ukuran jendela $B = 31$, sistem mampu mengisolasi daun di bawah bayangan secara sempurna karena nilai ambang batas lokal beradaptasi terhadap intensitas lingkungan sekitarnya.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Ukuran Jendela Wajib Bilangan Ganjil**: Parameter `blockSize` pada `cv2.adaptiveThreshold()` wajib bernilai bilangan ganjil yang lebih besar dari 1 (misalnya 11, 21, 31). Memasukkan angka genap akan memicu `cv::Exception`.
2. **Kebutuhan Pra-Filtering Blur**: Sebelum menerapkan metode Otsu atau Adaptive, sangat disarankan menerapkan penapis Gaussian blur halus (`cv2.GaussianBlur(img, (5, 5), 0)`) untuk mereduksi derau frekuensi tinggi yang dapat mendistorsi puncak histogram.

---

## 3. Landasan Teori & Konsep Matematis Thresholding

![Komparasi Metode Thresholding Biner Otsu Adaptif](../assets/komparasi_metode_thresholding_biner_otsu_adaptif.png)

### 3.1 Formulasi Matematis Algoritma Otsu (1979)
Misalkan sebuah citra grayscale memiliki $L$ tingkat keabuan ($[0, 1, \dots, L-1]$) dengan total $N$ piksel. Probabilitas kemunculan tingkat keabuan $i$ dinyatakan sebagai:

$$p_i = \frac{n_i}{N}, \quad \sum_{i=0}^{L-1} p_i = 1$$

Jika kita membagi piksel menjadi dua kelas $\mathcal{C}_0$ (rentang $[0, T]$) dan $\mathcal{C}_1$ (rentang $[T+1, L-1]$):
1. **Probabilitas Kumulatif Kelas**:
   $$\omega_0(T) = \sum_{i=0}^{T} p_i, \quad \omega_1(T) = \sum_{i=T+1}^{L-1} p_i = 1 - \omega_0(T)$$
2. **Nilai Rata-rata Intensitas Kelas**:
   $$\mu_0(T) = \sum_{i=0}^{T} \frac{i \cdot p_i}{\omega_0(T)}, \quad \mu_1(T) = \sum_{i=T+1}^{L-1} \frac{i \cdot p_i}{\omega_1(T)}$$
3. **Rata-rata Intensitas Total Citra**:
   $$\mu_T = \sum_{i=0}^{L-1} i \cdot p_i = \omega_0(T) \mu_0(T) + \omega_1(T) \mu_1(T)$$
4. **Varians Antar-Kelas (*Between-Class Variance*)**:
   $$\sigma_b^2(T) = \omega_0(T) (\mu_0(T) - \mu_T)^2 + \omega_1(T) (\mu_1(T) - \mu_T)^2 = \omega_0(T) \omega_1(T) (\mu_0(T) - \mu_1(T))^2$$

Ambang batas optimal $T^*$ adalah nilai $T \in [0, L-1]$ yang memaksimalkan varians antar-kelas:

$$T^* = \arg\max_{0 \le T < L-1} \sigma_b^2(T)$$

### 3.2 Formulasi Adaptive Gaussian Thresholding
Untuk setiap piksel $(x, y)$, nilai ambang batas lokal dihitung dari bobot kernel Gaussian $G$ pada jendela $B \times B$:

$$T(x, y) = \left( \sum_{u=-k}^{k} \sum_{v=-k}^{k} G(u, v) \cdot I(x+u, y+v) \right) - C$$

di mana $k = \frac{B - 1}{2}$ dan $C$ adalah konstanta pengurang untuk mengeliminasi derau latar belakang.

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Citra Grayscale Kanopi / Buah Sawit"] --> B["cv2.GaussianBlur(src, (5, 5), 0) -> Reduksi Derau"]
    B --> C1["Metode 1: Global Threshold cv2.threshold(blur, 127, 255, THRESH_BINARY)"]
    B --> C2["Metode 2: Otsu cv2.threshold(blur, 0, 255, THRESH_BINARY + THRESH_OTSU)"]
    B --> C3["Metode 3: Adaptive Gaussian cv2.adaptiveThreshold(blur, 255, ADAPTIVE_THRESH_GAUSSIAN_C, ...)"]
    C1 --> D["Evaluasi Visual & Kuantitatif Hasil Segmentasi"]
    C2 --> D
    C3 --> D
```

Implementasi Python modular pengujian komparasi metode thresholding:

```python
import cv2
import numpy as np

# 1. Pembangkitan Citra Sintetis Kanopi dengan Gradien Bayangan Tajuk
H, W = 400, 600
# Gradien bayangan horizontal (kiri terang ~ 200, kanan gelap ~ 50)
grad_x = np.linspace(200, 50, W, dtype=np.float32)
background_gradient = np.tile(grad_x, (H, 1))

# Menambahkan objek daun sawit (bercak lebih terang relatif terhadap latar sekitarnya)
canopy_synth = background_gradient.copy()
cv2.ellipse(canopy_synth, (180, 200), (90, 45), -20, 0, 360, 240, -1)
cv2.ellipse(canopy_synth, (420, 200), (90, 45), 20, 0, 360, 110, -1) # Daun di bawah bayangan
canopy_gray = np.clip(canopy_synth, 0, 255).astype(np.uint8)

# 2. Pra-pemrosesan: Reduksi Derau dengan Gaussian Blur
blurred = cv2.GaussianBlur(canopy_gray, (5, 5), 0)

# 3. Metode A: Global Thresholding Statis (T = 127)
_, thresh_global = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

# 4. Metode B: Otsu Binarization Otomatis
otsu_thresh, thresh_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 5. Metode C: Adaptive Gaussian Thresholding (BlockSize=31, C=5)
thresh_adaptive = cv2.adaptiveThreshold(
    blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=31, C=5
)

print(f"Ambang Batas Optimal Otsu Ditemukan: T* = {otsu_thresh:.1f}")
print(f"Piksel Objek Terdeteksi Global     : {cv2.countNonZero(thresh_global)}")
print(f"Piksel Objek Terdeteksi Otsu       : {cv2.countNonZero(thresh_otsu)}")
print(f"Piksel Objek Terdeteksi Adaptif    : {cv2.countNonZero(thresh_adaptive)}")
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Deteksi Lesi Hawar Daun Sawit

### 5.1 Spesifikasi Masalah
Penyakit hawar daun (*Curvularia maculans*) menghasilkan bercak nekrotik gelap pada helai daun kelapa sawit muda. Permukaan daun sering kali memiliki pantulan lilin kutikula (*waxy glare*) yang mengacaukan penambangan global.

### 5.2 Implementasi Segmentasi Lesi Daun Berbasis Otsu Terbalik
```python
# Simulasi helai daun terang dengan bercak nekrotik gelap di tengah
leaf_surface = np.full((300, 500), 190, dtype=np.uint8)
# Bercak penyakit gelap (intensitas rendah ~ 60)
cv2.circle(leaf_surface, (200, 150), 35, 60, -1)
cv2.circle(leaf_surface, (280, 160), 25, 55, -1)
# Tambahkan derau Gaussian halus
noise = np.random.normal(0, 10, leaf_surface.shape).astype(np.int16)
leaf_noisy = np.clip(leaf_surface.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# Pembersihan blur
leaf_blur = cv2.GaussianBlur(leaf_noisy, (5, 5), 0)

# Karena lesi berwarna gelap, gunakan THRESH_BINARY_INV + THRESH_OTSU
# Bercak gelap akan bernilai 255 (putih), daun normal bernilai 0 (hitam)
opt_t, lesion_mask = cv2.threshold(leaf_blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

lesion_area = cv2.countNonZero(lesion_mask)
print(f"Ambang Pemisahan Lesi Gelap : T = {opt_t:.1f}")
print(f"Total Luas Area Lesi Penyakit: {lesion_area} piksel")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Mengabaikan Tahap Gaussian Blur**: Menerapkan Otsu atau Adaptive langsung pada citra mentah berderau tinggi akan menghasilkan artefak masker berpasir (*salt-and-pepper noise*).
2. **Memilih Block Size Terlalu Kecil pada Adaptive**: Jika ukuran `blockSize` lebih kecil daripada ukuran fisik objek kanopi, bagian tengah kanopi yang seragam akan dianggap sebagai latar belakang (*hollow object effect*).
3. **Menerapkan Otsu pada Citra yang Tidak Bimodal**: Jika citra didominasi oleh satu latar belakang seragam tanpa objek kontras, Otsu akan memotong histogram di tengah-tengah secara keliru.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Aturan Pemilihan Block Size**: Pastikan ukuran `blockSize` selalu lebih besar dari diameter objek terkecil yang ingin dideteksi.
2. **Kombinasi dengan Morfologi**: Terapkan operasi `cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)` setelah binerisasi untuk menutup lubang-lubang kecil pada objek.
3. **Pemeriksaan Visual Histogram**: Plot histogram intensitas citra terlebih dahulu untuk memverifikasi keberadaan dua puncak (*bimodal distribution*).

---

## 7. Rangkuman Modul

* Thresholding mengonversi citra grayscale menjadi biner untuk memisahkan objek target dari latar belakang.
* Metode Otsu secara matematis mencari ambang batas optimal $T^*$ yang memaksimalkan varians antar-kelas tanpa memerlukan parameter manual.
* Adaptive Thresholding menghitung ambang batas lokal secara dinamis per jendela tetangga, menjadikannya solusi terbaik untuk citra pertanian dengan gradien bayangan tajuk.
* Tahap pra-pemrosesan Gaussian blur merupakan langkah esensial untuk menjamin kestabilan dan kemulusan masker biner hasil segmentasi.

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Analisis Varians Otsu (Bloom C4)**: Suatu citra kecil memiliki 10 piksel dengan intensitas: $[10, 12, 15, 18, 20, 180, 190, 200, 210, 220]$.
   * Hitung nilai $\omega_0$ dan $\omega_1$ jika dipilih ambang batas $T = 50$!
   * Hitung nilai rata-rata kelas $\mu_0$ dan $\mu_1$!
   * Hitung varians antar-kelas $\sigma_b^2(T)$ dan jelaskan mengapa nilai ini mendekati optimal!
2. **Evaluasi Fenomena Objek Berlubang (Bloom C4)**: Mengapa penggunaan parameter `blockSize = 7` pada citra kanopi kelapa sawit yang memiliki diameter 150 piksel menghasilkan masker kanopi yang berlubang di tengah (*hollow mask*)? Jelaskan mekanisme matematis penyebab kegagalan tersebut!

### Tugas Pemrograman Mandiri
Buatlah skrip Python yang membandingkan segmentasi daun sawit dengan gradien bayangan menggunakan: (1) `cv2.THRESH_BINARY`, (2) `cv2.THRESH_OTSU`, dan (3) `cv2.ADAPTIVE_THRESH_GAUSSIAN_C`. Hitung nilai Intersection-over-Union (IoU) ketiga metode tersebut terhadap masker ground truth aktual dan sajikan dalam bentuk tabel komparasi!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 11.5: Contour Detection

Melalui operasi thresholding, kita telah berhasil mentransformasikan citra berwarna yang kompleks menjadi masker biner bersih yang memisahkan objek target dari latar belakang. Namun, citra biner hanyalah sekumpulan kisi piksel bernilai 0 dan 255. Bagaimana cara sistem mengenali bahwa sekumpulan piksel putih tersebut adalah sebuah tandan buah sawit yang utuh? Bagaimana cara mengukur luas area, perimeter, dan koordinat pusatnya?

Pada **AI Modul 11.5: Contour Detection**, kita akan melangkah dari representasi piksel biner menuju analisis topologi bentuk tingkat lanjut: memahami **Algoritma Suzuki-Abe**, mengekstraksi hierarki kontur pohon (`RETR_TREE`, `RETR_EXTERNAL`), menghitung momen spasial centroid ($C_x, C_y$), serta mengukur rasio kebulatan (*Circularity*) untuk sensus perkebunan otomatis.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Otsu, N. (1979). A threshold selection method from gray-level histograms. *IEEE Transactions on Systems, Man, and Cybernetics*, 9(1), 62-66.
2. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson. (Bab 10: Image Segmentation).
3. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media.
4. Fadilah, R., Mohamad, N., & Abdullah, M. Z. (2020). Automated segmentation of agricultural commodities under unconstrained illumination. *Computers and Electronics in Agriculture*, 178, 105788.
"""
    validate_text(md_content, "AI_Modul_11.4_Thresholding.md")
    with open("docs/part-11/AI_Modul_11.4_Thresholding.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-11/AI_Modul_11.4_Thresholding.md")

    # Notebook 11.4
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 11.4: Praktikum Thresholding\n",
                    "**Mata Kuliah:** Visi Komputer dan Pengolahan Citra Digital  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Mengimplementasikan binerisasi global statis (`cv2.threshold`) dengan berbagai tipe flag.\n",
                    "2. Menerapkan algoritma optimasi varians Otsu (`THRESH_OTSU`) pada histogram bimodal citra perkebunan.\n",
                    "3. Menguji ketahanan Adaptive Gaussian Thresholding terhadap citra kanopi dengan gradien bayangan tajuk.\n",
                    "4. Menganalisis pengaruh parameter `blockSize` dan konstanta $C$ terhadap integritas masker segmentasi.\n"
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
                    "## 1. Pembangkitan Citra Sintetis Kanopi dengan Gradien Bayangan Lapangan\n",
                    "Mensimulasikan citra tajuk kelapa sawit yang berada di bawah pengaruh gradien intensitas cahaya akibat sudut datang matahari."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "H, W = 400, 600\n",
                    "# Gradien bayangan tajuk (kiri terang ~ 210, kanan gelap ~ 40)\n",
                    "grad_line = np.linspace(210, 40, W, dtype=np.float32)\n",
                    "synthetic_base = np.tile(grad_line, (H, 1))\n",
                    "\n",
                    "# Objek Daun Sawit 1: Di sisi terang (kiri)\n",
                    "cv2.ellipse(synthetic_base, (170, 200), (95, 45), -25, 0, 360, 245, -1)\n",
                    "# Objek Daun Sawit 2: Di sisi bayangan gelap (kanan)\n",
                    "cv2.ellipse(synthetic_base, (430, 200), (95, 45), 25, 0, 360, 115, -1)\n",
                    "\n",
                    "canopy_gray = np.clip(synthetic_base, 0, 255).astype(np.uint8)\n",
                    "blurred_canopy = cv2.GaussianBlur(canopy_gray, (5, 5), 0)\n",
                    "print(f'Dimensi Citra Sintetis: {canopy_gray.shape}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Pengujian Tiga Metode Thresholding: Global, Otsu, dan Adaptif\n",
                    "Membandingkan segmentasi biner antara ambang batas global tetap, Otsu binarization, dan Adaptive Gaussian."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 1. Global Thresholding (T = 127)\n",
                    "_, mask_global = cv2.threshold(blurred_canopy, 127, 255, cv2.THRESH_BINARY)\n",
                    "\n",
                    "# 2. Otsu's Binarization Otomatis\n",
                    "otsu_val, mask_otsu = cv2.threshold(blurred_canopy, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)\n",
                    "\n",
                    "# 3. Adaptive Gaussian Thresholding (BlockSize=31, C=5)\n",
                    "mask_adapt = cv2.adaptiveThreshold(\n",
                    "    blurred_canopy, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 5\n",
                    ")\n",
                    "\n",
                    "print(f'Nilai Ambang Batas Optimal Otsu: T* = {otsu_val:.1f}')\n",
                    "print(f'Piksel Putih Tersegmentasi (Global) : {cv2.countNonZero(mask_global)}')\n",
                    "print(f'Piksel Putih Tersegmentasi (Otsu)   : {cv2.countNonZero(mask_otsu)}')\n",
                    "print(f'Piksel Putih Tersegmentasi (Adaptif): {cv2.countNonZero(mask_adapt)}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Komparasi Kinerja Penanganan Bayangan Tajuk\n",
                    "Menampilkan citra asli dan perbandingan masker biner dari ketiga metode penambangan."
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
                    "axes[0].imshow(canopy_gray, cmap='gray')\n",
                    "axes[0].set_title('1. Citra Asli (Gradien Bayangan)', fontsize=10, fontweight='bold')\n",
                    "axes[0].axis('off')\n",
                    "\n",
                    "axes[1].imshow(mask_global, cmap='gray')\n",
                    "axes[1].set_title('2. Global (T=127): Gagal di Bayangan', fontsize=10, fontweight='bold')\n",
                    "axes[1].axis('off')\n",
                    "\n",
                    "axes[2].imshow(mask_otsu, cmap='gray')\n",
                    "axes[2].set_title(f'3. Otsu (T*={otsu_val:.0f}): Gagal Separasi', fontsize=10, fontweight='bold')\n",
                    "axes[2].axis('off')\n",
                    "\n",
                    "axes[3].imshow(mask_adapt, cmap='gray')\n",
                    "axes[3].set_title('4. Adaptive: Kedua Daun Terisolasi!', fontsize=10, fontweight='bold')\n",
                    "axes[3].axis('off')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_thresholding_komparasi_11_4.png', dpi=150)\n",
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
    with open("notebooks/part-11/AI_Modul_11.4_Praktikum_Thresholding.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-11/AI_Modul_11.4_Praktikum_Thresholding.ipynb")

    # Guide 11.4
    guide_content = r"""# AI Modul 11.4: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-04
* **Topik Utama**: Binerisasi Citra, Formulasi Otsu, dan Adaptive Thresholding
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Derivasi Otsu, 70 Menit Praktikum Komputer, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.4, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Konsep binerisasi citra, pembagian kelas foreground-background, dan kelemahan thresholding global statis.
* **Menit 25 - 50**: Pembuktian matematis kriteria maksimasi varians antar-kelas Otsu $\sigma_b^2(T)$ dan mekanisme Adaptive Gaussian.
* **Menit 50 - 120**: Praktikum komputer: pembuatan citra sintetis kanopi berbayangan, perbandingan global vs Otsu vs adaptif, dan visualisasi masker.
* **Menit 120 - 150**: Pembahasan jebakan ukuran jendela ganjil dan pengantar Modul 11.5 (Contour Detection).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teoretis Otsu** | Menguraikan langkah penurunan varians antar-kelas dan syarat histogram bimodal secara runtut. | Memahami fungsi Otsu namun kurang mendalam pada formulasi varians statistik. | Gagal membedakan antara varians intra-kelas dan varians antar-kelas. |
| **Implementasi Adaptive Threshold** | Menerapkan `cv2.adaptiveThreshold()` dengan penentuan parameter `blockSize` ganjil dan konstanta $C$ yang tepat. | Mampu menjalankan fungsi adaptif namun memilih ukuran jendela yang terlalu kecil. | Terjadi galat komputasi akibat memasukkan angka genap pada `blockSize`. |
| **Analisis Hasil Binarisasi** | Menginterpretasi mengapa metode adaptif unggul menghadapi gradien pencahayaan lapangan secara komprehensif. | Mengetahui bahwa metode adaptif lebih baik namun analisis teknisnya masih minim. | Tidak mampu membaca hasil visualisasi perbedaan masker ketiga metode. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Analisis Varians Otsu
Diketahui 10 piksel: $[10, 12, 15, 18, 20, 180, 190, 200, 210, 220]$, ambang batas $T = 50$.
1. **Probabilitas Kumulatif Kelas**:
   * Kelas $\mathcal{C}_0$ (intensitas $\le 50$): ada 5 piksel $[10, 12, 15, 18, 20]$. Maka $\omega_0 = \frac{5}{10} = 0.5$.
   * Kelas $\mathcal{C}_1$ (intensitas $> 50$): ada 5 piksel $[180, 190, 200, 210, 220]$. Maka $\omega_1 = \frac{5}{10} = 0.5$.
2. **Nilai Rata-rata Kelas**:
   * $\mu_0 = \frac{10 + 12 + 15 + 18 + 20}{5} = \frac{75}{5} = 15.0$
   * $\mu_1 = \frac{180 + 190 + 200 + 210 + 220}{5} = \frac{1000}{5} = 200.0$
3. **Varians Antar-Kelas**:
   $$\sigma_b^2(T) = \omega_0 \omega_1 (\mu_0 - \mu_1)^2 = (0.5)(0.5)(15.0 - 200.0)^2 = 0.25 \times (-185.0)^2 = 0.25 \times 34225 = 8556.25$$
   Nilai ini sangat tinggi karena kedua kelompok data terpisah secara sempurna oleh lembah histogram lebar di antara 20 dan 180, sehingga memaksimalkan keterpisahan kedua kelas.

### Jawaban Soal Konseptual 2: Fenomena Objek Berlubang (Hollow Mask)
Pada Adaptive Thresholding, nilai ambang dihitung lokal per jendela $B \times B$. Jika diameter tajuk daun adalah 150 piksel namun dipilih `blockSize = 7`, maka di bagian tengah tajuk daun yang seragam, seluruh tetangga dalam jendela $7 \times 7$ memiliki intensitas yang hampir sama (misalnya sekitar $220$). Nilai ambang lokal dihitung sebagai:
$$T = \text{Mean}(I_{\text{lokal}}) - C \approx 220 - 5 = 215$$
Karena piksel di tengah tajuk bernilai 220, jika ada sedikit fluktuasi di mana piksel bernilai 214, piksel tersebut langsung diputus menjadi 0 (hitam). Lebih parah lagi, jika intensitas seragam sempurna dan $C$ positif kecil, maka kontras lokal dianggap nol sehingga algoritma menduga tidak ada tepi objek, menyebabkan bagian dalam tajuk tanaman terlubangi secara artifisial. Solusinya adalah memperbesar `blockSize` melebihi diameter objek (misalnya $B = 151$ atau $201$) agar jendela mencakup batas tepi objek dan latar belakang.
"""
    validate_text(guide_content, "AI_Modul_11.4_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-11/AI_Modul_11.4_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-11/AI_Modul_11.4_Panduan_Instruktur_dan_Kunci_Solusi.md")

# ==============================================================================
# MODUL 11.5: Contour Detection
# ==============================================================================
def create_modul_11_5():
    md_content = r"""# AI Modul 11.5: Contour Detection

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-11-05
* **Mata Kuliah**: Visi Komputer dan Pengolahan Citra Digital (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Genap)
* **Prasyarat**: AI Modul 11.4 (Thresholding)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pelacakan Batas Suzuki-Abe, Hierarki Kontur TREE/EXTERNAL, Ekstraksi Momen Centroid"] --> B["OUTCOMES: Kemampuan Mengidentifikasi Morfometri & Menghitung Populasi Objek Tanaman"]
    B --> C["IMPACTS: Sensus Otomatis Kanopi Pohon Sawit & Penghitungan Butir Brondolan Hasil Panen"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** prinsip pelacakan batas topologis algoritma Suzuki-Abe (1985) pada citra biner, representasi struktur hierarki kontur pohon (`RETR_EXTERNAL`, `RETR_TREE`, `RETR_CCOMP`), serta aproksimasi poligon kontur (`CHAIN_APPROX_SIMPLE` vs `CHAIN_APPROX_NONE`).
2. **Menerapkan (C3)** fungsi `cv2.findContours()` dan `cv2.drawContours()` untuk mengekstraksi parameter morfometri geometris: luas area (`cv2.contourArea()`), keliling perimeter (`cv2.arcLength()`), koordinat pusat massa (*centroid*) berbasis momen spasial ($C_x = \frac{M_{10}}{M_{00}}, C_y = \frac{M_{01}}{M_{00}}$), kotak pembatas tegak (`cv2.boundingRect()`), kotak pembatas terotasi (`cv2.minAreaRect()`), dan selubung cembung (*convex hull*).
3. **Menganalisis (C4)** indikator deskriptor bentuk invariansi skala: rasio kebulatan (*circularity*) dan rasio kekompakan (*solidity*) untuk membedakan pohon kelapa sawit normal dengan pohon yang terserang hama perusak pelepah.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan algoritma penelusuran batas kontur dan penafsiran vektor hierarki 4-elemen OpenCV `[Next, Previous, First_Child, Parent]`.
  * Skrip Python modular berstandar PEP 8 untuk deteksi kontur, penapisan artefak luas area, dan pelabelan koordinat pusat kanopi pohon sawit.
  * Visualisasi anotasi bounding box dan titik centroid pada data citra ortofoto perkebunan.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian membangun modul sensus pohon terotomatisasi dari ortofoto drone dengan akurasi penghitungan di atas $95\%$.
  * Kemampuan mengklasifikasikan geometri butiran komoditas pertanian berbasis morfometri tanpa ketergantungan model AI berbobot besar.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Efisiensi operasional manajemen perkebunan melalui otomatisasi inventarisasi tegakan pohon dan estimasi potensi panen per blok kebun.

---

## 2. Profil Fundamental Deteksi Kontur: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Kontur adalah kurva kontinu yang menghubungkan seluruh titik batas tepi yang memiliki nilai intensitas warna yang sama:
1. **Representasi Topologis Vektor**: Mengubah representasi raster kisi piksel biner menjadi sekumpulan titik koordinat vektor diskrit $C = \{(x_0, y_0), (x_1, y_1), \dots, (x_{k-1}, y_{k-1})\}$.
2. **Ekstraksi Momen Spasial (*Spatial Moments*)**: Mengintegrasikan sebaran spasial piksel di dalam kontur untuk menghitung momen orde nol ($m_{00}$ sebagai luas area) dan momen orde satu ($m_{10}, m_{01}$ untuk penentuan titik berat/centroid).
3. **Karakterisasi Bentuk Geometris**: Menghitung rasio bentuk invarian terhadap translasi, rotasi, dan skala (seperti kebulatan $4\pi A / P^2$ dan rasio aspek bounding box).

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Sensus Populasi Pohon Kelapa Sawit**: Menghitung jumlah tajuk pohon sawit individual dari ortofoto drone dan menandai koordinat GPS setiap pohon secara otomatis.
* **Sortasi Ukuran Butir Buah & Biji**: Mengukur diameter ekuivalen dan volume biji kopi atau buah sawit yang melintas di atas meja konveyor.
* **Deteksi Tajuk Rusak Akibat Hama Ulat Api**: Pohon yang pelepahnya dimakan hama ulat api kehilangan bentuk melingkar simetris dan menunjukkan penurunan rasio kebulatan (*circularity*) yang tajam.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
1. **Deteksi Objek Tanpa Latihan Model (*Training-Free*)**: Deteksi kontur bekerja langsung secara deterministik berbasis aturan matematika geometri murni tanpa memerlukan ribuan data latih beranotasi.
2. **Eksekusi Sangat Cepat**: Mampu memproses ratusan kontur dalam hitungan milidetik pada resolusi 4K.

### 2.4 Analisis Kelebihan dan Kekurangan Mode Retrieval Kontur

| Flag Mode Retrieval | Struktur Hierarki yang Dihasilkan | Keunggulan Utama | Kasus Penggunaan Optimal di Agro-Industri |
| :--- | :--- | :--- | :--- |
| **`cv2.RETR_EXTERNAL`** | Hanya kontur paling luar (tanpa anak). | Paling cepat, mengabaikan lubang/tekstur internal. | Sensus tajuk pohon sawit dan penghitungan tandan buah luar. |
| **`cv2.RETR_LIST`** | Seluruh kontur disimpan datar setara. | Menemukan seluruh batas tanpa overhead relasi. | Menghitung total bercak penyakit tanpa mempedulikan posisi. |
| **`cv2.RETR_TREE`** | Rekonstruksi pohon hierarki penuh (Parent-Child). | Memetakan struktur lubang di dalam kontur bersarang. | Mendeteksi lubang gerek hama di dalam daging buah sawit. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Divisi GIS Perkebunan memproses citra drone seluas 50 hektar. Setelah menerapkan masker warna hijau tajuk dan binerisasi, fungsi `cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)` dipanggil. Sistem menemukan 6.850 kontur. Dengan menyaring kontur yang memiliki luas area $A \in [1500, 8000]\text{ piksel}$, sistem mengeliminasi derau semak belukar kecil dan berhasil mendata 6.720 pohon sawit produktif dengan titik koordinat sentroid masing-masing.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Modifikasi Citra Masukan pada Versi OpenCV Lama**: Pada OpenCV versi 3.x, `findContours` memodifikasi citra biner masukan secara *in-place*. Meskipun pada OpenCV 4.x hal ini tidak lagi terjadi, membiasakan menyuplai salinan citra `mask.copy()` merupakan praktik rekayasa yang aman.
2. **Penyaringan Kontur Derau (*Noise Filtering*)**: Deteksi kontur pada citra lapangan selalu menghasilkan ratusan kontur mikro palsu akibat debu atau kerikil. Penerapan ambang batas luas area minimum (`cv2.contourArea(cnt) > MIN_AREA`) adalah keharusan mutlak.

---

## 3. Landasan Teori & Konsep Matematis Deteksi Kontur

![Hierarki Kontur dan Aproksimasi Geometri OpenCV](../assets/hierarki_kontur_dan_aproksimasi_geometri_opencv.png)

### 3.1 Teori Momen Spasial dan Titik Pusat Massa (*Centroid*)
Momen spasial orde $(p + q)$ dari suatu daerah kontur biner $\mathcal{R}$ didefinisikan sebagai:

$$m_{pq} = \sum_{x} \sum_{y} x^p y^q \cdot I(x, y)$$

di mana untuk citra biner, $I(x, y) = 1$ di dalam kontur dan $0$ di luar kontur.
* **Luas Area Kontur**:
  $$\text{Area} = m_{00}$$
* **Koordinat Pusat Massa (*Centroid*)**:
  $$\bar{x} = \frac{m_{10}}{m_{00}}, \quad \bar{y} = \frac{m_{01}}{m_{00}}$$

### 3.2 Deskriptor Bentuk Morfometri
1. **Rasio Kebulatan (*Circularity / Compactness*)**:
   $$C = \frac{4 \pi \cdot \text{Area}}{\text{Perimeter}^2}$$
   Untuk lingkaran sempurna, $C = 1.0$. Bentuk tajuk pohon sawit normal yang simetris memiliki $C \in [0.75, 0.95]$, sedangkan tajuk yang rusak atau teroklusi memiliki $C < 0.60$.
2. **Rasio Soliditas (*Solidity*)**:
   $$S = \frac{\text{Area}}{\text{ConvexArea}}$$
   di mana $\text{ConvexArea}$ adalah luas dari selubung cembung (*Convex Hull*) yang membungkus kontur tersebut.

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Masker Biner Hasil Thresholding"] --> B["cv2.findContours(mask, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)"]
    B --> C["Perulangan untuk Setiap Kontur cnt"]
    C --> D["Hitung Luas Area: A = cv2.contourArea(cnt)"]
    D --> E{"A >= MIN_AREA?"}
    E -- Tidak --> F["Abaikan Derau"]
    E -- Ya --> G["Hitung Momen Centroid: Cx = M10/M00, Cy = M01/M00"]
    G --> H["Hitung Keliling P & Rasio Kebulatan C = 4*pi*A / P^2"]
    H --> I["Visualisasi: cv2.drawContours & cv2.circle(Centroid)"]
```

Implementasi Python modular untuk sensus tajuk pohon dan ekstraksi fitur morfometri:

```python
import cv2
import numpy as np

# 1. Pembangkitan Masker Biner Ortofoto Tajuk Pohon Sawit Sintetis
H, W = 600, 800
mask_orchard = np.zeros((H, W), dtype=np.uint8)

# Menambahkan 3 tajuk pohon sawit sehat (lingkaran besar)
cv2.circle(mask_orchard, (200, 200), 75, 255, -1)
cv2.circle(mask_orchard, (450, 180), 70, 255, -1)
cv2.circle(mask_orchard, (320, 420), 80, 255, -1)

# Menambahkan 1 tajuk pohon rusak/terserang hama (elips bergerigi tidak teratur)
pts_damaged = np.array([[600, 380], [680, 390], [670, 460], [610, 480], [580, 430]], dtype=np.int32)
cv2.fillPoly(mask_orchard, [pts_damaged], 255)

# Menambahkan derau rumput kecil (artefak)
cv2.circle(mask_orchard, (100, 450), 6, 255, -1)
cv2.circle(mask_orchard, (520, 320), 8, 255, -1)

# 2. Pelacakan Kontur dengan cv2.findContours
contours, hierarchy = cv2.findContours(mask_orchard, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Total Kontur Kasar Ditemukan: {len(contours)}")

# 3. Penyaringan dan Analisis Morfometri
MIN_CANOPY_AREA = 1000 # Ambang batas luas tajuk
valid_trees = []

for idx, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    if area < MIN_CANOPY_AREA:
        continue # Abaikan derau rumput
        
    perimeter = cv2.arcLength(cnt, closed=True)
    circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
    
    # Hitung momen dan centroid
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0
        
    # Bounding box
    x, y, w, h = cv2.boundingRect(cnt)
    
    status = "Pohon Sehat" if circularity >= 0.75 else "Tajuk Rusak / Hama"
    valid_trees.append({
        "id": len(valid_trees) + 1,
        "centroid": (cx, cy),
        "area": area,
        "circularity": circularity,
        "status": status
    })

print(f"Jumlah Pohon Sawit Tervalidasi : {len(valid_trees)}")
for tree in valid_trees:
    print(f"Pohon #{tree['id']} - Centroid: {tree['centroid']} - Area: {tree['area']:.0f} px - Kebulatan: {tree['circularity']:.3f} [{tree['status']}]")
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Sensus Produksi Brondolan Sawit

### 5.1 Spesifikasi Masalah
Dalam uji mutu tandan buah di laboratorium pabrik, brondolan buah sawit yang telah direbus dipisahkan dan dihitung luas penampangnya untuk mengestimasi rasio daging buah (*mesocarp*) terhadap biji (*nut*).

### 5.2 Implementasi Convex Hull dan Soliditas Buah
```python
# Simulasi kontur buah sawit tunggal
for tree in valid_trees:
    if "Rusak" in tree["status"]:
        # Ambil kontur pohon rusak untuk analisis Convex Hull
        cnt_target = contours[0] # Contoh kontur
        hull = cv2.convexHull(cnt_target)
        hull_area = cv2.contourArea(hull)
        solidity = float(tree["area"]) / hull_area if hull_area > 0 else 0
        print(f"Analisis Soliditas Tajuk Cacat: {solidity:.3f} (Hull Area: {hull_area:.0f})")
        break
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Pembagian dengan Nol saat Menghitung Centroid**: Mengabaikan kondisi `if M["m00"] != 0:` akan memicu galat `ZeroDivisionError` pada kontur garis lurus 1 piksel.
2. **Tertukar Parameter Koordinat Bounding Box**: Nilai yang dikembalikan `cv2.boundingRect()` adalah `(x, y, w, h)`. Sering terjadi kesalahan pemotongan array dengan menulis `img[x:x+w, y:y+h]` alih-alih `img[y:y+h, x:x+w]`.
3. **Penggunaan Bendera RETR yang Terlalu Berat**: Menggunakan `RETR_TREE` pada citra daun bertekstur rumit menghasilkan ribuan kontur anak yang memperlambat komputasi. Gunakan `RETR_EXTERNAL` bila hanya membutuhkan kontur luar objek.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Gunakan `CHAIN_APPROX_SIMPLE`**: Mengompresi segmen garis lurus horizontal, vertikal, dan diagonal sehingga hanya menyimpan titik-titik ujungnya, menghemat memori RAM secara signifikan.
2. **Filter Berbasis Luas & Rasio Aspek**: Kombinasikan filter luas area dengan rasio aspek $w/h$ untuk mengeliminasi bayangan panjang pelepah daun.
3. **Konversi Koordinat ke Integer**: Koordinat sentroid dan bounding box wajib di-cast ke tipe `int` sebelum digambar pada kanvas citra menggunakan fungsi grafis OpenCV.

---

## 7. Rangkuman Modul

* Kontur adalah kurva vektor penghubung titik-titik batas intensitas sama pada citra biner yang dilacak menggunakan algoritma Suzuki-Abe.
* Momen spasial memfasilitasi kalkulasi luas area ($m_{00}$) dan koordinat titik pusat massa / centroid ($m_{10}/m_{00}, m_{01}/m_{00}$).
* Deskriptor bentuk geometris seperti kebulatan (*circularity*) dan soliditas (*solidity*) menyediakan fitur invarian untuk membedakan tajuk tanaman sehat vs tajuk rusak akibat serangan hama.
* Penerapan filter luas area minimum (`MIN_AREA`) merupakan langkah wajib untuk membersihkan derau piksel lapangan.

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Kalkulasi Rasio Kebulatan (Bloom C3)**: Dua buah tajuk kelapa sawit diukur parameternya:
   * Tajuk Pohon A: Luas $A_1 = 15.400\text{ piksel}$, Keliling $P_1 = 450\text{ piksel}$.
   * Tajuk Pohon B: Luas $A_2 = 12.000\text{ piksel}$, Keliling $P_2 = 620\text{ piksel}$.
   * Hitung rasio kebulatan $C_1$ dan $C_2$ untuk kedua pohon tersebut!
   * Manakah pohon yang kemungkinan besar mengalami kerusakan pelepah akibat hama ulat api? Berikan justifikasi teknisnya!
2. **Analisis Hierarki Kontur (Bloom C4)**: Suatu citra irisan buah sawit memiliki kontur kulit luar, kontur tempurung cangkang di dalam daging buah, dan kontur inti kernel di dalam tempurung. Jika dipanggil dengan flag `cv2.RETR_TREE`, jelaskan representasi relasi Parent-Child pada array hierarki kontur tersebut!

### Tugas Pemrograman Mandiri
Buatlah program Python yang membaca citra masker biner ortofoto kebun kelapa sawit, mendeteksi seluruh kontur pohon, menghitung centroid masing-masing pohon, menggambar nomor ID pohon di samping centroidnya menggunakan `cv2.putText()`, dan mengekspor daftar koordinat $(X, Y)$ seluruh pohon ke dalam format file teks CSV `sensus_pohon_sawit.csv`!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 11.6: Face Detection

Kita telah menguasai cara mendeteksi kontur objek agronomis berbasis bentuk geometris dan analisis momen spasial. Namun, bagaimana jika objek yang ingin kita deteksi di area perkebunan memiliki variasi tekstur internal yang jauh lebih rumit daripada sekadar bentuk lingkaran atau elips? Misalnya: bagaimana cara mendeteksi wajah pekerja kebun dan mandor untuk sistem absensi lapangan otomatis, atau memastikan kepatuhan penggunaan alat pelindung diri (helm K3) di stasiun perebusan pabrik kelapa sawit?

Pada **AI Modul 11.6: Face Detection**, kita akan mempelajari salah satu algoritma paling berpengaruh dalam sejarah visi komputer: **Haar Cascade Classifier (Viola & Jones Framework)**. Kita akan membedah representasi matematika **Integral Image**, seleksi fitur menggunakan **AdaBoost**, serta arsitektur pengali beruntun (*cascade classifier*) yang memungkinkan deteksi wajah manusia secara real-time pada kamera CCTV pabrik.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Suzuki, S., & Abe, K. (1985). Topological structural analysis of digitized binary images by border following. *Computer Vision, Graphics, and Image Processing*, 30(1), 32-46.
2. Hu, M. K. (1962). Visual pattern recognition by moment invariants. *IRE Transactions on Information Theory*, 8(2), 179-187.
3. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson. (Bab 11: Representation and Description).
4. Wu, Z., Chen, Y., Zhao, B., Kang, X., & Ding, Y. (2020). Measurement of canopy size and foliage density of oil palm using UAV LiDAR and optical imagery. *Computers and Electronics in Agriculture*, 175, 105577.
"""
    validate_text(md_content, "AI_Modul_11.5_Contour_detection.md")
    with open("docs/part-11/AI_Modul_11.5_Contour_detection.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-11/AI_Modul_11.5_Contour_detection.md")

    # Notebook 11.5
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 11.5: Praktikum Contour Detection\n",
                    "**Mata Kuliah:** Visi Komputer dan Pengolahan Citra Digital  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Mengekstrak kontur batas topologis menggunakan `cv2.findContours` dengan bendera `RETR_EXTERNAL`.\n",
                    "2. Menghitung luas area (`contourArea`), keliling (`arcLength`), dan koordinat titik pusat massa (*centroid*) berbasis momen spasial.\n",
                    "3. Menguji deskriptor kebulatan (*circularity*) untuk membedakan tajuk kelapa sawit sehat dan tajuk terserang hama.\n",
                    "4. Memvisualisasikan anotasi kontur, bounding box, dan titik centroid pada data simulasi kebun.\n"
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
                    "## 1. Pembangkitan Masker Sensus Tajuk Pohon Sawit Sintetis\n",
                    "Mensimulasikan 4 tajuk pohon sawit (3 tajuk sehat berbentuk lingkaran simetris dan 1 tajuk rusak terserang hama) disertai derau rumput liar."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "H, W = 500, 700\n",
                    "orchard_mask = np.zeros((H, W), dtype=np.uint8)\n",
                    "\n",
                    "# Pohon 1, 2, 3: Tajuk Sehat (Lingkaran Besar Simetris)\n",
                    "cv2.circle(orchard_mask, (180, 160), 65, 255, -1)\n",
                    "cv2.circle(orchard_mask, (420, 150), 60, 255, -1)\n",
                    "cv2.circle(orchard_mask, (250, 360), 70, 255, -1)\n",
                    "\n",
                    "# Pohon 4: Tajuk Rusak / Terpapar Hama (Bentuk Tak Beraturan)\n",
                    "damaged_pts = np.array([[500, 310], [580, 320], [560, 400], [510, 420], [470, 360]], dtype=np.int32)\n",
                    "cv2.fillPoly(orchard_mask, [damaged_pts], 255)\n",
                    "\n",
                    "# Derau semak belukar kecil (< 100 piksel)\n",
                    "cv2.circle(orchard_mask, (80, 400), 5, 255, -1)\n",
                    "cv2.circle(orchard_mask, (620, 200), 7, 255, -1)\n",
                    "\n",
                    "print(f'Dimensi Citra Sensus Tajuk: {orchard_mask.shape}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Pelacakan Kontur dan Ekstraksi Parameter Morfometri\n",
                    "Menerapkan `cv2.findContours` dan menghitung momen spasial, luas, keliling, serta kebulatan untuk setiap kontur tervalidasi."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "contours, hierarchy = cv2.findContours(orchard_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)\n",
                    "MIN_AREA = 800\n",
                    "\n",
                    "tree_data = []\n",
                    "canvas_vis = cv2.cvtColor(orchard_mask, cv2.COLOR_GRAY2BGR)\n",
                    "\n",
                    "for cnt in contours:\n",
                    "    area = cv2.contourArea(cnt)\n",
                    "    if area < MIN_AREA:\n",
                    "        continue # Abaikan derau semak\n",
                    "        \n",
                    "    perim = cv2.arcLength(cnt, closed=True)\n",
                    "    circ = (4 * np.pi * area) / (perim ** 2) if perim > 0 else 0\n",
                    "    \n",
                    "    M = cv2.moments(cnt)\n",
                    "    cx = int(M['m10'] / M['m00']) if M['m00'] != 0 else 0\n",
                    "    cy = int(M['m01'] / M['m00']) if M['m00'] != 0 else 0\n",
                    "    \n",
                    "    is_healthy = circ >= 0.75\n",
                    "    label = 'Pohon Sehat' if is_healthy else 'Tajuk Rusak'\n",
                    "    color = (0, 255, 0) if is_healthy else (0, 0, 255)\n",
                    "    \n",
                    "    # Gambar visualisasi\n",
                    "    cv2.drawContours(canvas_vis, [cnt], -1, color, 2)\n",
                    "    cv2.circle(canvas_vis, (cx, cy), 5, (255, 0, 0), -1)\n",
                    "    \n",
                    "    x, y, w, h = cv2.boundingRect(cnt)\n",
                    "    cv2.rectangle(canvas_vis, (x, y), (x+w, y+h), (255, 200, 0), 1)\n",
                    "    \n",
                    "    tree_data.append({\n",
                    "        'id': len(tree_data) + 1,\n",
                    "        'centroid': (cx, cy),\n",
                    "        'area': area,\n",
                    "        'circularity': circ,\n",
                    "        'status': label\n",
                    "    })\n",
                    "\n",
                    "print(f'Total Pohon Teridentifikasi: {len(tree_data)}')\n",
                    "for t in tree_data:\n",
                    "    print(f\"ID {t['id']}: Centroid={t['centroid']}, Area={t['area']:.0f}, Kebulatan={t['circularity']:.3f} [{t['status']}]\")\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Peta Sensus Kanopi Kebun Kelapa Sawit\n",
                    "Menampilkan hasil segmentasi kontur, titik centroid, dan bounding box pohon sawit."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
                    "\n",
                    "ax1.imshow(orchard_mask, cmap='gray')\n",
                    "ax1.set_title('1. Masker Biner Sensus Tajuk Kebun', fontsize=11, fontweight='bold')\n",
                    "ax1.axis('off')\n",
                    "\n",
                    "ax2.imshow(cv2.cvtColor(canvas_vis, cv2.COLOR_BGR2RGB))\n",
                    "ax2.set_title('2. Anotasi Kontur (Hijau=Sehat, Merah=Rusak)', fontsize=11, fontweight='bold')\n",
                    "ax2.axis('off')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_sensus_kontur_11_5.png', dpi=150)\n",
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
    with open("notebooks/part-11/AI_Modul_11.5_Praktikum_Contour_Detection.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-11/AI_Modul_11.5_Praktikum_Contour_Detection.ipynb")

    # Guide 11.5
    guide_content = r"""# AI Modul 11.5: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-05
* **Topik Utama**: Deteksi Kontur Suzuki-Abe, Momen Spasial, dan Analisis Bentuk
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Topologi Kontur, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.5, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Konsep topologi kontur vektor, algoritma Suzuki-Abe, dan struktur hierarki kontur pohon.
* **Menit 25 - 50**: Matematika momen spasial $m_{pq}$, penentuan koordinat centroid $(C_x, C_y)$, serta formulasi kebulatan dan soliditas.
* **Menit 50 - 120**: Praktikum komputer: pembuatan citra sintetis sensus pohon sawit, penapisan derau luas area, dan visualisasi bounding box.
* **Menit 120 - 150**: Asesmen formatif dan diskusi pemanfaatan kontur untuk penghitungan populasi pohon sawit skala ribuan hektar.

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teori Topologi** | Menjelaskan relasi hierarki kontur dan momen spasial centroid secara matematis tanpa galat. | Memahami fungsi `findContours` namun kurang memahami struktur relasi hierarki. | Menganggap kontur sama persis dengan deteksi tepi Canny. |
| **Implementasi Morfometri** | Menulis skrip ekstraksi momen, bounding box, dan rasio kebulatan secara terstruktur dan efisien. | Mampu mengekstrak kontur namun lupa menangani potensi pembagian nol pada momen. | Terjadi galat runtime saat mengekstrak koordinat pusat massa. |
| **Penyaringan Derau & Sensus** | Mengonfigurasi ambang batas luas minimum dan mengklasifikasikan tajuk sehat vs rusak dengan tepat. | Mampu menyaring kontur namun kriteria ambang batas kebulatan belum optimal. | Gagal memisahkan objek pohon dari derau semak mikro. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Kalkulasi Rasio Kebulatan
Rumus rasio kebulatan: $C = \frac{4\pi A}{P^2}$ (dengan $\pi \approx 3.14159$).
1. **Tajuk Pohon A**:
   $$C_1 = \frac{4 \times 3.14159 \times 15400}{450^2} = \frac{193521.95}{202500} \approx 0.956$$
2. **Tajuk Pohon B**:
   $$C_2 = \frac{4 \times 3.14159 \times 12000}{620^2} = \frac{150796.32}{384400} \approx 0.392$$
3. **Analisis Diagnostik Agronomis**:
   Pohon A memiliki nilai $C_1 = 0.956$ (sangat mendekati 1.0), menunjukkan geometri tajuk yang melingkar sempurna dan simetris, mencerminkan pelepah sawit yang utuh, rimbun, dan sehat.
   Sebaliknya, Pohon B memiliki nilai $C_2 = 0.392$ (sangat rendah). Nilai kelilingnya membengkak menjadi $620$ piksel meskipun luasnya lebih kecil ($12.000$ vs $15.400$), mengindikasikan batas tepi tajuk yang sangat berlekuk-lekuk dan tidak teratur. Fenomena ini adalah ciri khas tajuk kelapa sawit yang pelepahnya dimakan oleh hama ulat api (*Setothosea asigna*) atau ulat kantung (*Metisa plana*), sehingga Pohon B harus diprioritaskan untuk tindakan pengendalian hama terpadu.

### Jawaban Soal Konseptual 2: Analisis Hierarki Kontur Pohon
Pada `cv2.RETR_TREE`, relasi kontur diorganisasi dalam pohon hierarki 4 elemen `[Next, Previous, First_Child, Parent]`:
* **Kontur Kulit Luar Buah**: Berada pada tingkat tertinggi (Level 0, akar pohon). Tidak memiliki Parent (`Parent = -1`). Memiliki anak pertama yaitu tempurung cangkang (`First_Child = ID_Tempurung`).
* **Kontur Tempurung Cangkang**: Berada pada Level 1. Memiliki `Parent = ID_Kulit_Luar` dan memiliki anak pertama yaitu inti kernel (`First_Child = ID_Kernel`).
* **Kontur Inti Kernel**: Berada pada Level 2 (daun terdalam). Memiliki `Parent = ID_Tempurung` dan tidak memiliki anak (`First_Child = -1`).
Struktur hierarki bersarang ini memungkinkan algoritma mengukur ketebalan daging buah (*mesocarp*) secara otomatis dengan menghitung selisih luas kontur Level 0 dan Level 1.
"""
    validate_text(guide_content, "AI_Modul_11.5_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-11/AI_Modul_11.5_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-11/AI_Modul_11.5_Panduan_Instruktur_dan_Kunci_Solusi.md")

# ==============================================================================
# MODUL 11.6: Face Detection
# ==============================================================================
def create_modul_11_6():
    md_content = r"""# AI Modul 11.6: Face Detection

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-11-06
* **Mata Kuliah**: Visi Komputer dan Pengolahan Citra Digital (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Genap)
* **Prasyarat**: AI Modul 11.5 (Contour Detection)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pemahaman Fitur Haar-like, Matriks Citra Integral O(1), Pengklasifikasi Kaskade AdaBoost"] --> B["OUTCOMES: Kemampuan Mengimplementasikan Deteksi Wajah Real-Time Berkecepatan Tinggi"]
    B --> C["IMPACTS: Sistem Absensi Mandor Otomatis & Pemantauan Kepatuhan K3 Pekerja Pabrik Sawit"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** kerangka kerja seminal deteksi objek cepat Viola-Jones (2001), konsep matematika fitur Haar-like (fitur tepi, garis, dan pusat), representasi citra integral (*integral image*) untuk evaluasi kotak berkecepatan konstan $O(1)$, seleksi fitur adaptif AdaBoost, serta arsitektur pengklasifikasi kaskade (*attentional cascade*).
2. **Menerapkan (C3)** kelas `cv2.CascadeClassifier()` dari modul `cv2.objdetect` untuk mendeteksi wajah pekerja kebun dan mata operator secara real-time pada citra statis dan aliran video menggunakan model XML pra-latih (*pre-trained Haar cascades*).
3. **Menganalisis (C4)** sensitivitas parameter deteksi multi-skala: faktor penskalaan piramida (`scaleFactor`), batas ambang konsensus tetangga (`minNeighbors`), serta ukuran kotak minimum (`minSize`) terhadap tingkat deteksi benar (*true positives*) dan alarm palsu (*false positives*) di area industri kelapa sawit.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan algoritma kalkulasi citra integral dan pembuktian evaluasi area 4-titik referensi.
  * Skrip Python modular berstandar PEP 8 untuk deteksi wajah pekerja, penandaan bounding box, dan pemotongan ROI wajah.
  * Laporan evaluasi komparasi performa deteksi pada variasi parameter `scaleFactor` dan `minNeighbors`.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian merancang sistem absensi biometrik lapangan berbasis kamera gerbang masuk perkebunan.
  * Kemampuan mengintegrasikan deteksi wajah dengan protokol verifikasi kepatuhan alat pelindung diri (helm keselamatan K3).
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Peningkatan disiplin dan keselamatan kerja operasional pabrik kelapa sawit melalui pengawasan visual otomatis yang transparan dan akurat.

---

## 2. Profil Fundamental Deteksi Wajah: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Deteksi wajah dalam kerangka kerja Viola-Jones adalah proses klasifikasi biner spasial yang melokalisasi keberadaan dan posisi wajah manusia di dalam kisi citra:
1. **Ekstraksi Fitur Haar-like Berbobot**: Mengukur perbedaan intensitas antara area gelap (mata, alis) dan area terang (pipi, dahi, hidung) menggunakan kernel persegi panjang berbobot:
   $$\Delta = \sum_{\text{kotak hitam}} I(x, y) - \sum_{\text{kotak putih}} I(x, y)$$
2. **Akselerasi Citra Integral**: Menghitung jumlah total intensitas pada sembarang persegi panjang hanya menggunakan 4 nilai sudut pada matriks kumulatif, menghasilkan waktu eksekusi independen terhadap ukuran jendela ($O(1)$).
3. **Penyaringan Bertingkat (*Cascade Rejection*)**: Rangkaian puluhan pengklasifikasi lemah (*weak classifiers*) yang disusun secara seri, di mana jendela citra non-wajah langsung dieliminasi pada tahap-tahap awal ($> 90\%$ jendela ditolak pada 2 tahap pertama), sehingga prosesor hanya fokus memproses kandidat yang sangat menyerupai wajah.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Sistem Absensi Otomatis Pekerja Kebun di Pintu Gerbang Blok**: Memverifikasi kehadiran ratusan pemanen dan mandor secara nirkontak saat menaiki truk pengangkut kebun.
* **Pengawasan Keselamatan Kerja (K3) di Pabrik Kelapa Sawit**: Memastikan operator stasiun perebusan (*sterilizer*) dan pemurnian (*clarifier*) berada di pos jaga dan mengenakan helm pengaman.
* **Keamanan Aset Pabrik & Kantor Kebun**: Memantau akses personel ke gudang bahan kimia pemupukan dan ruang kendali listrik PKS.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
Meskipun saat ini terdapat model deteksi wajah berbasis Deep Learning (seperti MTCNN, RetinaFace, atau YOLO-Face), Haar Cascade Classifier tetap menjadi pilihan utama untuk sistem terpasang berdaya sangat rendah (*low-power edge devices* seperti Raspberry Pi atau ESP32-CAM) karena kebutuhan memori dan daya komputasinya yang sangat minimal.

### 2.4 Analisis Kelebihan dan Kekurangan Haar Cascade

| Parameter Evaluasi | Haar Cascade Classifier (Viola-Jones) | Deep Learning Face Detector (RetinaFace/YOLO) | Implikasi di Area Perkebunan |
| :--- | :--- | :--- | :--- |
| **Kebutuhan Hardware** | CPU standar berdaya sangat rendah (tanpa GPU). | Memerlukan GPU atau akselerator NPU khusus. | Haar Cascade ideal untuk kamera baterai surya mandiri di kebun. |
| **Kecepatan Inferensi** | Sangat cepat (15 - 30 FPS pada CPU biasa). | Sedang hingga berat pada CPU biasa. | Responsivitas tinggi untuk kamera pengawas pintu gerbang. |
| **Ketahanan Sudut Wajah** | Optimal pada wajah tampak depan (*frontal face*). | Mampu mendeteksi wajah menyamping (*profile*) ekstrem. | Pekerja perlu diarahkan melihat ke arah kamera saat absensi. |
| **Ketahanan Oklusi** | Rentan gagal jika wajah tertutup masker/helm tebal. | Sangat tahan terhadap oklusi parsial. | Perlu pencahayaan lampu bantu di pos pengawas pabrik. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Pabrik Kelapa Sawit PT Sawit Sentosa memasang unit komputer mini dengan kamera USB di pintu masuk stasiun boiler. Setiap pekerja yang mendekati area berbahaya dipindai menggunakan Haar Cascade. Dalam waktu 35 milidetik, sistem mendeteksi kotak wajah pekerja dan mengekstrak ROI kepala di atas wajah untuk memverifikasi warna helm keselamatan. Jika helm tidak terdeteksi, alarm peringatan berbunyi secara otomatis sebelum pintu gerbang mesin dapat dibuka.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Penyediaan Berkas XML Model Pra-latih**: `cv2.CascadeClassifier` membutuhkan path berkas XML (seperti `haarcascade_frontalface_default.xml`). Jika path salah, objek classifier akan kosong (`classifier.empty() == True`) dan memicu kegagalan diam-diam (*silent failure*).
2. **Ketergantungan Citra Grayscale**: Haar Cascade beroperasi secara eksklusif pada citra berdimensi tunggal (*grayscale*). Citra berwarna wajib dikonversi dengan `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)` sebelum pemanggilan `detectMultiScale`.

---

## 3. Landasan Teori & Konsep Matematis Deteksi Wajah

![Arsitektur Haar Cascade dan Integral Image Face Detection](../assets/arsitektur_haar_cascade_dan_integral_image_face_detection.png)

### 3.1 Teori Citra Integral (*Integral Image*)
Citra integral $ii(x, y)$ pada koordinat $(x, y)$ didefinisikan sebagai jumlah seluruh nilai piksel yang berada di sebelah kiri dan atas titik tersebut (inklusif):

$$ii(x, y) = \sum_{x' \le x, \; y' \le y} i(x', y')$$

Citra integral dapat dibangun secara efisien dalam satu kali lintasan (*single pass*) $O(H \cdot W)$ menggunakan relasi rekursif:

$$s(x, y) = s(x, y-1) + i(x, y)$$
$$ii(x, y) = ii(x-1, y) + s(x, y)$$

di mana $s(x, y)$ adalah jumlah kumulatif baris, dengan kondisi batas $s(x, -1) = 0$ dan $ii(-1, y) = 0$.

### 3.2 Evaluasi Persegi Panjang dalam Waktu Konstan $O(1)$
Diberikan empat titik sudut persegi panjang $D$: $1(x_1, y_1), 2(x_2, y_1), 3(x_1, y_2),$ dan $4(x_2, y_2)$:

$$\sum_{(x, y) \in D} i(x, y) = ii(4) + ii(1) - ii(2) - ii(3)$$

Hanya dibutuhkan tiga operasi penambahan/pengurangan sederhana terlepas dari apakah ukuran kotak adalah $24 \times 24$ piksel atau $500 \times 500$ piksel.

### 3.3 Struktur Parameter `detectMultiScale`
Metode `detectMultiScale(image, scaleFactor, minNeighbors, minSize)` mengendalikan proses piramida citra dan fusi deteksi:
* `scaleFactor`: Faktor pengecilan citra pada setiap tingkat piramida (misalnya $1.1$ berarti citra diperkecil $10\%$ per tingkat).
* `minNeighbors`: Jumlah minimum kotak kandidat bertetangga yang harus mendeteksi wajah di lokasi yang sama agar lolos verifikasi konsensus.
* `minSize`: Batas ukuran terkecil wajah yang dicari (misalnya `(30, 30)` piksel).

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Citra Masukan BGR Pekerja Pabrik"] --> B["cv2.cvtColor -> Grayscale"]
    B --> C["Memuat Model: cv2.CascadeClassifier(xml_path)"]
    C --> D["Eksekusi: faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)"]
    D --> E["Perulangan untuk Setiap Wajah (x, y, w, h)"]
    E --> F["Ekstraksi ROI Wajah: face_roi = gray[y:y+h, x:x+w]"]
    F --> G["Visualisasi: cv2.rectangle() Bounding Box"]
```

Implementasi Python modular untuk deteksi wajah pekerja menggunakan Haar Cascade:

```python
import cv2
import numpy as np
import os

# 1. Menemukan Path Bawaan Model Haar Cascade di OpenCV
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f"Berkas Haar Cascade tidak ditemukan: {cascade_path}")

face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    raise RuntimeError("Gagal memuat CascadeClassifier!")
print(f"[OK] Berkas Haar Cascade Berhasil Dimuat: {os.path.basename(cascade_path)}")

# 2. Pembangkitan Citra Sintetis Pekerja Pabrik Sawit
# (Simulasi kepala pekerja dengan mata, alis, dan mulut berintensitas kontras)
H, W = 400, 600
worker_img = np.full((H, W, 3), 180, dtype=np.uint8) # Latar dinding pabrik

# Gambar Wajah 1 (Pekerja A)
cv2.ellipse(worker_img, (200, 200), (60, 80), 0, 0, 360, (190, 160, 140), -1) # Kulit
cv2.circle(worker_img, (180, 180), 8, (40, 30, 20), -1) # Mata Kiri
cv2.circle(worker_img, (220, 180), 8, (40, 30, 20), -1) # Mata Kanan
cv2.line(worker_img, (170, 165), (190, 165), (20, 20, 20), 4) # Alis Kiri
cv2.line(worker_img, (210, 165), (230, 165), (20, 20, 20), 4) # Alis Kanan
cv2.ellipse(worker_img, (200, 240), (25, 10), 0, 0, 180, (50, 40, 120), -1) # Mulut

# Konversi ke Grayscale
gray_worker = cv2.cvtColor(worker_img, cv2.COLOR_BGR2GRAY)

# 3. Deteksi Multi-Skala
faces = face_cascade.detectMultiScale(
    gray_worker,
    scaleFactor=1.1,
    minNeighbors=3,
    minSize=(50, 50)
)
print(f"Jumlah Wajah Terdeteksi: {len(faces)}")

# Anotasi Kotak Deteksi
vis_worker = worker_img.copy()
for (x, y, w, h) in faces:
    cv2.rectangle(vis_worker, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(vis_worker, "Pekerja Terverifikasi", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Verifikasi Kehadiran Mandor di Pos Lapangan

### 5.1 Spesifikasi Masalah
Kamera pos timbangan perkebunan merekam kehadiran mandor panen setiap pagi. Sistem harus mendeteksi wajah mandor yang berdiri pada jarak $1.5 - 3.0\text{ meter}$ dari kamera, mengekstrak potongan wajah resolusi $100 \times 100$, dan menyimpannya sebagai berkas log harian berstempel waktu.

### 5.2 Implementasi Ekstraksi ROI Wajah untuk Biometrik
```python
def extract_and_log_faces(frame, detector, output_dir="face_logs"):
    os.makedirs(output_dir, exist_ok=True)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))
    
    extracted_faces = []
    for idx, (x, y, w, h) in enumerate(detections):
        # Ekstrak ROI wajah aman
        face_roi = frame[y:y+h, x:x+w].copy()
        face_norm = cv2.resize(face_roi, (100, 100), interpolation=cv2.INTER_AREA)
        
        filename = os.path.join(output_dir, f"mandor_{idx+1}.jpg")
        cv2.imwrite(filename, face_norm)
        extracted_faces.append(face_norm)
        
    return len(detections), extracted_faces

count, faces_list = extract_and_log_faces(worker_img, face_cascade)
print(f"Berhasil mengekstrak {count} wajah mandor ke direktori log.")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Nilai `scaleFactor` Terlalu Besar (Misalnya 1.5)**: Pengecilan citra sebesar $50\%$ per tingkat akan melompati ukuran wajah pekerja yang berada pada jarak menengah sehingga wajah gagal terdeteksi (*false negative*). Gunakan nilai moderat seperti $1.05 - 1.15$.
2. **Nilai `minNeighbors` Terlalu Kecil (Misalnya 0 atau 1)**: Mengakibatkan munculnya puluhan kotak deteksi palsu pada tekstur dinding pabrik atau tumpukan buah sawit. Gunakan nilai $4 - 6$ untuk lingkungan industri.
3. **Menerapkan Deteksi pada Citra BGR Asli**: Melewatkan citra 3-kanal ke fungsi `detectMultiScale` akan menghasilkan galat runtime karena model Haar Cascade hanya dirancang untuk matriks intensitas 1-kanal.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Gunakan Parameter `minSize` Sesuai Jarak**: Batasi ukuran kotak minimum (misalnya `minSize=(60, 60)`) untuk mencegah prosesor membuang waktu memeriksa kotak-kotak mikro yang mustahil berupa wajah manusia.
2. **Koreksi Iluminasi dengan Histogram Equalization**: Terapkan `cv2.equalizeHist(gray)` sebelum deteksi untuk meningkatkan kontras wajah di bawah kondisi pencahayaan pos kebun yang temaram.
3. **Validasi Model dengan `empty()`**: Selalu periksa `if face_cascade.empty():` segera setelah inisialisasi berkas XML.

---

## 7. Rangkuman Modul

* Kerangka kerja Viola-Jones mendeteksi wajah melalui kombinasi fitur Haar-like, komputasi citra integral berkecepatan $O(1)$, seleksi AdaBoost, dan pengklasifikasi kaskade bertingkat.
* Citra integral memungkinkan penjumlahan intensitas piksel persegi panjang sembarang ukuran hanya dalam 4 referensi akses memori.
* Fungsi `cv2.CascadeClassifier.detectMultiScale()` menyediakan deteksi multi-skala yang sangat efisien pada prosesor CPU berdaya rendah.
* Parameter `scaleFactor` dan `minNeighbors` mengendalikan keseimbangan antara sensitivitas deteksi dan penekanan alarm palsu.

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Kalkulasi Citra Integral Manual (Bloom C3)**: Diberikan citra kecil $3 \times 3$ dengan intensitas piksel:
   $$I = \begin{bmatrix} 2 & 3 & 1 \\ 4 & 1 & 5 \\ 3 & 2 & 2 \end{bmatrix}$$
   * Hitung matriks citra integral $ii(x, y)$ untuk seluruh koordinat!
   * Gunakan 4 nilai sudut citra integral untuk menghitung jumlah total piksel pada sub-matriks kotak $2 \times 2$ kanan bawah ($x \in [1, 2], y \in [1, 2]$)! Buktikan bahwa hasilnya persis sama dengan $1 + 5 + 2 + 2 = 10$!
2. **Evaluasi Sensitivitas Parameter Kaskade (Bloom C4)**: Pada kamera pos gerbang pabrik sawit, dilaporkan bahwa sistem sering kali mendeteksi pola serat karung goni sebagai wajah manusia. Parameter manakah antara `scaleFactor` dan `minNeighbors` yang harus disesuaikan untuk mengatasi alarm palsu tersebut? Jelaskan mekanisme internalnya!

### Tugas Pemrograman Mandiri
Rancang sebuah sistem verifikasi K3 Python yang mendeteksi wajah pekerja menggunakan Haar Cascade, lalu secara otomatis mengekstrak area kepala di atas wajah ($y - 0.6h$ hingga $y$) untuk mendeteksi keberadaan warna helm keselamatan kuning/putih menggunakan ruang warna HSV yang telah dipelajari pada Modul 11.3!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 11.7: Video Processing

Kita telah menguasai cara mendeteksi kontur objek dan wajah manusia pada citra statis menggunakan OpenCV. Namun, di dunia industri perkebunan yang sebenarnya—seperti konveyor tandan buah sawit yang bergerak nonstop atau kamera CCTV pemantau dermaga tongkang CPO—data visual tidak hadir sebagai gambar tunggal yang terisolasi, melainkan sebagai aliran kontinu puluhan gambar per detik yang terikat oleh dimensi waktu (*temporal stream*).

Pada **AI Modul 11.7: Video Processing**, kita akan melangkah memasuki dimensi pemrosesan video: memahami abstraksi `cv2.VideoCapture` dan `cv2.VideoWriter`, teknik demuxing dan decoding frame video, penghitungan laju bingkai per detik (*Frames Per Second* / FPS) secara presisi, serta teknik penulisan stream terkompresi menggunakan codec industri H.264/MP4V.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Viola, P., & Jones, M. (2001). Rapid object detection using a boosted cascade of simple features. *Proceedings of the 2001 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)*, 1, I-511.
2. Viola, P., & Jones, M. J. (2004). Robust real-time face detection. *International Journal of Computer Vision*, 57(2), 137-154.
3. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media. (Bab 13: Recognition).
4. Lienhart, R., & Maydt, J. (2002). An extended set of Haar-like features for rapid object detection. *Proceedings. International Conference on Image Processing*, 1, I-900.
"""
    validate_text(md_content, "AI_Modul_11.6_Face_detection.md")
    with open("docs/part-11/AI_Modul_11.6_Face_detection.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-11/AI_Modul_11.6_Face_detection.md")

    # Notebook 11.6
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 11.6: Praktikum Face Detection\n",
                    "**Mata Kuliah:** Visi Komputer dan Pengolahan Citra Digital  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Memuat dan mengonfigurasi model detektor `cv2.CascadeClassifier` dari berkas XML bawaan OpenCV.\n",
                    "2. Menghitung dan membuktikan efisiensi evaluasi kotak citra integral $O(1)$ secara matematis.\n",
                    "3. Melakukan deteksi wajah pekerja kebun multi-skala dengan `detectMultiScale`.\n",
                    "4. Menganalisis trade-off parameter `scaleFactor` dan `minNeighbors` pada eliminasi alarm palsu.\n"
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
                    "import os\n",
                    "\n",
                    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                    "print(f'OpenCV Version: {cv2.__version__}')\n",
                    "\n",
                    "# Verifikasi ketersediaan berkas Haar Cascade frontal face\n",
                    "xml_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'\n",
                    "print(f'Path Model Haar Cascade: {xml_file}')\n",
                    "print(f'Eksistensi Berkas XML   : {os.path.exists(xml_file)}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Pembuktian Evaluasi Kotak Cepat pada Citra Integral O(1)\n",
                    "Mendemonstrasikan pembuatan citra integral dan penghitungan jumlah intensitas sembarang kotak hanya dengan 4 akses memori."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Matriks citra kecil 4x4\n",
                    "sample_mat = np.array([\n",
                    "    [2, 3, 1, 4],\n",
                    "    [4, 1, 5, 2],\n",
                    "    [3, 2, 2, 1],\n",
                    "    [1, 4, 3, 2]\n",
                    "], dtype=np.float32)\n",
                    "\n",
                    "# Hitung citra integral OpenCV\n",
                    "integral_img = cv2.integral(sample_mat)\n",
                    "\n",
                    "# Evaluasi kotak x: 1..2, y: 1..2 (nilai asli: 1 + 5 + 2 + 2 = 10)\n",
                    "# Perhatikan bahwa cv2.integral menambahkan padding 0 pada baris dan kolom 0 (dimensi H+1, W+1)\n",
                    "x1, y1 = 1, 1\n",
                    "x2, y2 = 3, 3 # batas inklusif di integral index\n",
                    "\n",
                    "sum_integral = integral_img[y2, x2] + integral_img[y1, x1] - integral_img[y1, x2] - integral_img[y2, x1]\n",
                    "sum_manual = np.sum(sample_mat[1:3, 1:3])\n",
                    "\n",
                    "print('Matriks Citra Asli (4x4):\\n', sample_mat)\n",
                    "print('Matriks Citra Integral (5x5):\\n', integral_img)\n",
                    "print(f'Jumlah Intensitas via Citra Integral : {sum_integral:.0f}')\n",
                    "print(f'Jumlah Intensitas via Penjumlahan Langsung: {sum_manual:.0f}')\n",
                    "assert sum_integral == sum_manual, 'Kalkulasi citra integral tidak cocok!'\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Pembangkitan Citra Sintetis Pekerja Kebun dan Deteksi Wajah Multi-Skala\n",
                    "Membangkitkan citra simulasi pekerja kebun kelapa sawit dan menjalankan `detectMultiScale`."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "detector = cv2.CascadeClassifier(xml_file)\n",
                    "\n",
                    "# Buat kanvas pekerja\n",
                    "H, W = 400, 600\n",
                    "canvas = np.full((H, W, 3), 170, dtype=np.uint8)\n",
                    "\n",
                    "# Gambar wajah pekerja mandor\n",
                    "cv2.ellipse(canvas, (250, 200), (55, 75), 0, 0, 360, (185, 155, 135), -1)\n",
                    "cv2.circle(canvas, (230, 180), 7, (30, 20, 15), -1)\n",
                    "cv2.circle(canvas, (270, 180), 7, (30, 20, 15), -1)\n",
                    "cv2.line(canvas, (220, 168), (240, 168), (20, 20, 20), 3)\n",
                    "cv2.line(canvas, (260, 168), (280, 168), (20, 20, 20), 3)\n",
                    "cv2.ellipse(canvas, (250, 235), (20, 8), 0, 0, 180, (40, 30, 100), -1)\n",
                    "\n",
                    "gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)\n",
                    "\n",
                    "# Deteksi MultiScale\n",
                    "faces = detector.detectMultiScale(gray_canvas, scaleFactor=1.1, minNeighbors=3, minSize=(40, 40))\n",
                    "print(f'Jumlah Wajah Terdeteksi pada Citra: {len(faces)}')\n",
                    "\n",
                    "annotated = canvas.copy()\n",
                    "for (x, y, w, h) in faces:\n",
                    "    cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)\n",
                    "    cv2.putText(annotated, 'Mandor Kebun', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Hasil Deteksi Wajah Haar Cascade\n",
                    "Menampilkan citra grayscale dan citra anotasi bounding box hasil inferensi kaskade."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))\n",
                    "\n",
                    "ax1.imshow(gray_canvas, cmap='gray')\n",
                    "ax1.set_title('1. Citra Grayscale Masukan Detektor', fontsize=11, fontweight='bold')\n",
                    "ax1.axis('off')\n",
                    "\n",
                    "ax2.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))\n",
                    "ax2.set_title(f'2. Hasil Deteksi Wajah ({len(faces)} Terdeteksi)', fontsize=11, fontweight='bold')\n",
                    "ax2.axis('off')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_deteksi_wajah_11_6.png', dpi=150)\n",
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
    with open("notebooks/part-11/AI_Modul_11.6_Praktikum_Face_Detection.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-11/AI_Modul_11.6_Praktikum_Face_Detection.ipynb")

    # Guide 11.6
    guide_content = r"""# AI Modul 11.6: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-06
* **Topik Utama**: Deteksi Objek Cepat Viola-Jones, Citra Integral, dan Haar Cascade Classifier
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Citra Integral & AdaBoost, 70 Menit Praktikum Komputer, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.6, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Sejarah dan signifikansi algoritma Viola-Jones, fitur Haar-like, dan limitasi model klasik pada wajah non-frontal.
* **Menit 25 - 50**: Pembuktian matematika efisiensi citra integral $O(1)$, mekanisme seleksi fitur AdaBoost, dan penolakan kaskade bertingkat.
* **Menit 50 - 120**: Praktikum laboratorium: verifikasi pembuktian citra integral, inisialisasi `CascadeClassifier`, dan pengujian parameter `scaleFactor` serta `minNeighbors`.
* **Menit 120 - 150**: Asesmen formatif mengenai penanganan alarm palsu pada tekstur pabrik dan pengantar Modul 11.7 (Video Processing).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Citra Integral** | Mampu menghitung dan membuktikan evaluasi area persegi panjang 4-titik secara analitis tanpa galat. | Memahami konsep citra integral namun keliru pada penentuan offset indeks matriks. | Gagal menghitung penjumlahan area menggunakan citra integral. |
| **Konfigurasi Parameter Kaskade** | Mengatur `scaleFactor`, `minNeighbors`, dan `minSize` secara proporsional sesuai jarak kamera industri. | Menggunakan parameter default tanpa memahami pengaruh perubahan nilai terhadap deteksi. | Salah memasukkan nilai parameter sehingga memicu over-detection atau no-detection. |
| **Implementasi Kode Deteksi** | Menulis skrip deteksi aman dengan verifikasi `empty()`, konversi grayscale, dan ekstraksi ROI wajah. | Mampu menjalankan deteksi namun lupa memeriksa ketersediaan berkas XML. | Mengirimkan citra BGR ke fungsi `detectMultiScale` sehingga program crash. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Kalkulasi Citra Integral Manual
Diberikan matriks $I = \begin{bmatrix} 2 & 3 & 1 \\ 4 & 1 & 5 \\ 3 & 2 & 2 \end{bmatrix}$ berdimensi $3 \times 3$.
1. **Perhitungan Matriks Citra Integral $ii(x, y)$**:
   * Baris 0:
     $ii(0, 0) = 2$
     $ii(0, 1) = 2 + 3 = 5$
     $ii(0, 2) = 5 + 1 = 6$
   * Baris 1:
     $ii(1, 0) = 2 + 4 = 6$
     $ii(1, 1) = 6 + (3 + 1) = 10$  (atau $5 + 4 + 1 = 10$)
     $ii(1, 2) = 6 + 10 + 5 - 5 = 16$
   * Baris 2:
     $ii(2, 0) = 6 + 3 = 9$
     $ii(2, 1) = 10 + 9 + 2 - 6 = 15$
     $ii(2, 2) = 16 + 15 + 2 - 10 = 23$
   Matriks Citra Integral:
   $$ii = \begin{bmatrix} 2 & 5 & 6 \\ 6 & 10 & 16 \\ 9 & 15 & 23 \end{bmatrix}$$
2. **Evaluasi Sub-Kotak $2 \times 2$ Kanan Bawah**:
   Kotak membentang dari $x \in [1, 2]$ dan $y \in [1, 2]$.
   Formula 4-titik sudut:
   $$\text{Sum} = ii(2, 2) + ii(0, 0) - ii(0, 2) - ii(2, 0) = 23 + 2 - 6 - 9 = 25 - 15 = 10$$
   Hasil penjumlahan manual: $1 + 5 + 2 + 2 = 10$. Terbukti identik sempurna!

### Jawaban Soal Konseptual 2: Evaluasi Sensitivitas Parameter Kaskade
Parameter yang harus disesuaikan untuk menekan alarm palsu (*false positives*) akibat tekstur serat karung goni adalah **menaikkan nilai `minNeighbors`** (misalnya dari nilai default 3 dinaikkan menjadi 5 atau 6).
* **Mekanisme Internal**: `minNeighbors` menentukan berapa banyak jendela kandidat deteksi yang saling tumpang tindih (*overlapping candidate bounding boxes*) yang harus sama-sama menyimpulkan adanya wajah di lokasi tersebut sebelum deteksi dinyatakan valid. Tekstur acak seperti serat karung goni mungkin secara kebetulan memicu satu atau dua fitur Haar pada skala tertentu, namun pola tersebut jarang sekali memicu deteksi yang konsisten pada berbagai pergeseran jendela tetangga. Dengan menaikkan `minNeighbors`, kandidat deteksi palsu yang hanya memiliki 1 - 2 pendukung akan langsung digugurkan (*suppressed*).
"""
    validate_text(guide_content, "AI_Modul_11.6_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-11/AI_Modul_11.6_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-11/AI_Modul_11.6_Panduan_Instruktur_dan_Kunci_Solusi.md")

if __name__ == '__main__':
    create_modul_11_4()
    create_modul_11_5()
    create_modul_11_6()
