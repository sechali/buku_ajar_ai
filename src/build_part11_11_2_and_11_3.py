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
# MODUL 11.2: Image Reading dan Manipulation
# ==============================================================================
def create_modul_11_2():
    md_content = r"""# AI Modul 11.2: Image Reading dan Manipulation

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-11-02
* **Mata Kuliah**: Visi Komputer dan Pengolahan Citra Digital (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Genap)
* **Prasyarat**: AI Modul 11.1 (Pengenalan OpenCV)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pembacaan Citra cv2.imread, Slicing ROI, Transformasi Geometri Affine"] --> B["OUTCOMES: Kemampuan Memanipulasi Resolusi Spasial & Orientasi Citra Perkebunan"]
    B --> C["IMPACTS: Pipeline Akuisisi & Normalisasi Citra Tandan Sawit Otomatis Standar Industri"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** mekanisme pembacaan file citra menggunakan fungsi `cv2.imread()`, perbedaan flag format masukan (`IMREAD_COLOR`, `IMREAD_GRAYSCALE`, `IMREAD_UNCHANGED`), teknik penanganan galat berkas nihil (*none-type error handling*), serta penulisan citra terkompresi dengan `cv2.imwrite()`.
2. **Menerapkan (C3)** operasi manipulasi spasial matriks citra mencakup pengirisan area minat (*Region of Interest* / ROI), interpolasi penskalaan resolusi (`cv2.resize()` dengan metode INTER_NEAREST, INTER_LINEAR, INTER_AREA), serta transformasi geometri afina (translasi dan rotasi menggunakan `cv2.warpAffine()`).
3. **Menganalisis (C4)** dampak pemilihan algoritma interpolasi terhadap integritas tepi dan tekstur permukaan komoditas pertanian pada proses normalisasi ukuran masukan model kecerdasan buatan.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan parameter pemanggilan `cv2.imread` dan matriks transformasi affine $2 \times 3$.
  * Skrip Python modular berstandar PEP 8 untuk ekstraksi otomatis ROI tandan buah sawit dan koreksi orientasi rotasi meja inspeksi.
  * Hasil komparasi visual kualitas rekonstruksi citra tajuk tanaman pada berbagai mode interpolasi resolusi.
* **Outcomes (Kompetensi Aplikatif)**:
  * Kemampuan membangun modul pra-pemrosesan spasial yang tangguh menghadapi variasi orientasi letak buah di pabrik.
  * Keahlian mereduksi dimensi citra drone skala besar menjadi ukuran standar tanpa kehilangan informasi tekstur penting.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Peningkatan konsistensi data masukan untuk sistem sortasi otomatis di pabrik kelapa sawit dan platform pemantauan kesehatan kebun berbasis citra drone.

---

## 2. Profil Fundamental Manipulasi Citra: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Manipulasi citra digital dalam OpenCV beroperasi pada level pemetaan spasial koordinat dua dimensi:
1. **Pemetaan Geometris Koordinat (*Geometric Coordinate Mapping*)**: Memetakan setiap koordinat piksel masukan $(x, y)$ ke koordinat keluaran baru $(x', y')$ melalui transformasi afina matriks:
   $$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} + \begin{bmatrix} t_x \\ t_y \end{bmatrix}$$
2. **Interpolasi Rekonstruksi Intensitas (*Intensity Interpolation*)**: Karena hasil transformasi koordinat sering kali berupa bilangan riil non-integer, OpenCV melakukan interpolasi nilai intensitas dari tetangga terdekat (*nearest neighbor*), rata-rata berbobot bilinear (*bilinear interpolation*), atau kubik (*bicubic spline*).
3. **Isolasi Spasial ROI (*Spatial Region Isolation*)**: Memangkas beban komputasi dengan membatasi pemrosesan hanya pada sub-matriks persegi panjang yang memuat objek target perkebunan.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Koreksi Kemiringan Tandan Buah di Meja Sortasi**: Buah sawit yang jatuh di meja berjalan sering kali memiliki orientasi acak. Rotasi afina otomatis memutar tandan ke sumbu tegak lurus untuk memudahkan estimasi fraksi kematangan.
* **Standardisasi Dimensi untuk Model Deep Learning**: Mengubah citra resolusi tinggi dari kamera industri ($1920 \times 1080$) menjadi dimensi baku model seperti $224 \times 224$ atau $640 \times 640$ secara proporsional.
* **Pemotongan Kanopi Pohon Individual dari Ortofoto Drone**: Mengekstrak potongan tajuk setiap pohon sawit secara terpisah dari peta ortofoto kebun seluas ratusan hektar.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
1. **Efisiensi Memori & Bandwidth**: Mengirimkan citra berukuran penuh ke model deteksi objek sangat lambat dan memboroskan memori GPU. Pemotongan ROI mereduksi ukuran tensor masukan hingga lebih dari $80\%$.
2. **Invariansi Rotasi Data Latih**: Menerapkan variasi rotasi dan translasi buatan (*geometric data augmentation*) secara signifikan meningkatkan ketahanan generalisasi model AI perkebunan.

### 2.4 Analisis Kelebihan dan Kekurangan Metode Interpolasi

| Metode Interpolasi | Kompleksitas Waktu | Karakteristik Visual | Kasus Penggunaan Optimal di Agro-Industri |
| :--- | :--- | :--- | :--- |
| **INTER_NEAREST** | Sangat Rendah ($O(1)$) | Terjadi efek bergerigi (*aliasing / pixelated*). | Penskalaan masker biner segmentasi daun tanpa mengubah label integer. |
| **INTER_LINEAR** | Rendah ($O(4)$ tetangga) | Halus, seimbang antara kecepatan dan kualitas. | Penskalaan standar (*default*) untuk citra kanopi kebun secara umum. |
| **INTER_AREA** | Sedang | Mencegah efek moiré saat memperkecil citra (*downsampling*). | Pengecilan ortofoto drone resolusi sangat tinggi ke ukuran web display. |
| **INTER_CUBIC** | Tinggi ($O(16)$ tetangga) | Tepi sangat tajam dan kaya detail mikro. | Pembesaran (*upscaling*) area bercak daun sakit untuk analisis patologis mikro. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Pada stasiun penimbangan tandan buah sawit, kamera mengambil foto tampak samping setiap lori pengangkut. Algoritma OpenCV membaca citra, mendeteksi area pelat identifikasi lori dan tumpukan buah, lalu mengekstrak kedua area tersebut sebagai dua ROI terpisah. ROI pelat nomor dikirim ke modul pembaca karakter OCR, sedangkan ROI tumpukan buah diputar sebesar $15^\circ$ untuk meluruskan bidang rebah buah sebelum dialirkan ke model klasifikasi kematangan.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Validasi Eksistensi Berkas Citra**: Fungsi `cv2.imread()` tidak melemparkan eksepsi (*does not throw exception*) jika path berkas salah atau rusak; melainkan mengembalikan nilai `None`. Tanpa pemeriksaan `if img is None:`, baris kode berikutnya akan mengalami `AttributeError: 'NoneType' object has no attribute 'shape'`.
2. **Distorsi Aspek Rasio**: Mengubah ukuran citra dengan `cv2.resize(img, (dsize, dsize))` tanpa mempertahankan rasio aspek (*aspect ratio*) asli akan membuat bentuk tajuk pohon memipih atau melebar tidak wajar, merusak rasio kebulatan morfometri tanaman.

---

## 3. Landasan Teori & Konsep Matematis Manipulasi Citra

![Koordinat dan Manipulasi Matriks Citra OpenCV](../assets/koordinat_dan_manipulasi_matriks_citra_opencv.png)

### 3.1 Formulasi Matriks Transformasi Afina (Rotasi & Translasi)
Transformasi afina mempertahankan garis lurus dan paralelisme bidang. Matriks transformasi afina 2D berdimensi $2 \times 3$ dinyatakan sebagai:

$$M = \begin{bmatrix} \alpha & \beta & (1 - \alpha) \cdot c_x - \beta \cdot c_y \\ -\beta & \alpha & \beta \cdot c_x + (1 - \alpha) \cdot c_y \end{bmatrix}$$

di mana rotasi sebesar sudut $\theta$ berlawanan arah jarum jam dengan pusat titik $(c_x, c_y)$ dan faktor skala $s$ dirumuskan sebagai:

$$\alpha = s \cdot \cos(\theta), \quad \beta = s \cdot \sin(\theta)$$

OpenCV menyediakan fungsi pembangun matriks ini secara otomatis melalui:
`M = cv2.getRotationMatrix2D(center=(cx, cy), angle=theta, scale=s)`.

Piksel baru dihitung melalui perkalian matriks afina:

$$\begin{bmatrix} x' \\ y' \end{bmatrix} = M \cdot \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

### 3.2 Matematika Interpolasi Bilinear (*Bilinear Interpolation*)
Ketika titik hasil transformasi $(x', y')$ jatuh pada posisi non-integer dengan bagian pecahan $(u, v) = (x' - \lfloor x' \rfloor, \; y' - \lfloor y' \rfloor)$, nilai intensitas diestimasi dari empat tetangga terdekat:

$$I(x', y') = (1 - u)(1 - v) I(x_1, y_1) + u (1 - v) I(x_2, y_1) + (1 - u) v I(x_1, y_2) + u v I(x_2, y_2)$$

Interpolasi ini menghasilkan transisi warna yang halus pada permukaan daun sawit tanpa artefak kotak-kotak diskrit.

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Path Berkas Citra Kebun"] --> B["cv2.imread() dengan Validasi if img is None"]
    B --> C["Ekstraksi Dimensi Matriks: H, W = img.shape[:2]"]
    C --> D["Pemotongan Area Minat (ROI): roi = img[y1:y2, x1:x2].copy()"]
    D --> E["Koreksi Orientasi: cv2.getRotationMatrix2D & cv2.warpAffine"]
    E --> F["Penskalaan Standar: cv2.resize(roi, (224, 224), INTER_AREA)"]
    F --> G["Penyimpanan Hasil: cv2.imwrite() dengan Kualitas JPEG"]
```

Implementasi Python modular untuk pipeline pembacaan, pemotongan ROI, rotasi afina, dan penyimpanan citra:

```python
import cv2
import numpy as np

# 1. Fungsi Pembacaan Citra Aman (Safe Image Loader)
def load_image_safe(filepath, flag=cv2.IMREAD_COLOR):
    img = cv2.imread(filepath, flag)
    if img is None:
        raise FileNotFoundError(f"Gagal memuat citra! Berkas tidak ditemukan atau rusak: {filepath}")
    return img

# 2. Pembangkitan Citra Sintetis Tandan Buah Segar (TBS) Sawit
height, width = 600, 800
canvas_tbs = np.full((height, width, 3), 40, dtype=np.uint8) # Latar meja sortasi abu-abu gelap

# Menggambar elips tandan buah sawit (warna jingga/merah cerah)
cv2.ellipse(canvas_tbs, (400, 300), (180, 100), 25, 0, 360, (20, 120, 230), -1)
# Menambahkan duri-duri pelepah tandan
for i in range(0, 360, 30):
    rad = np.deg2rad(i + 25)
    px = int(400 + 200 * np.cos(rad))
    py = int(300 + 120 * np.sin(rad))
    cv2.circle(canvas_tbs, (px, py), 12, (10, 80, 180), -1)

# Simpan citra sintetis awal
cv2.imwrite("tbs_sample.jpg", canvas_tbs, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
print("[OK] Citra sintetis TBS berhasil disimpan: tbs_sample.jpg")

# 3. Ekstraksi Region of Interest (ROI)
# Koordinat kotak tandan: Y dari 150 ke 450, X dari 200 ke 600
roi_tbs = canvas_tbs[150:450, 200:600].copy()
print(f"Dimensi ROI Terpotong : {roi_tbs.shape} (Tinggi: 300, Lebar: 400)")

# 4. Koreksi Rotasi Afina (Memutar -25 derajat agar tegak)
h_roi, w_roi = roi_tbs.shape[:2]
center_roi = (w_roi // 2, h_roi // 2)
rot_matrix = cv2.getRotationMatrix2D(center=center_roi, angle=-25, scale=1.0)
tbs_straight = cv2.warpAffine(roi_tbs, rot_matrix, (w_roi, h_roi), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

# 5. Penskalaan Proporsional ke Resolusi Baku Model AI (224 x 224)
tbs_resized = cv2.resize(tbs_straight, (224, 224), interpolation=cv2.INTER_AREA)
print(f"Dimensi Hasil Akhir Penskalaan : {tbs_resized.shape}")
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Normalisasi Ortofoto Kanopi Sawit

### 5.1 Spesifikasi Masalah Drone Kebun
Kamera drone menghasilkan ortofoto mosaik beresolusi sangat besar ($4000 \times 3000$). Untuk mendeteksi serangan hama ulat kantung, sistem harus memindai pohon sawit per petak kanopi ($500 \times 500$), mengekstrak tajuk individual, merotasi tajuk menghadap sumbu utara, dan memperkecil citra ke resolusi $256 \times 256$ menggunakan interpolasi area untuk input jaringan saraf tiruan.

### 5.2 Implementasi Pemotongan dan Normalisasi Batch Tajuk
```python
# Simulasi pemotongan tajuk individual dari koordinat kanopi
def process_palm_canopy(large_ortho, center_x, center_y, box_size=500, target_size=256):
    half = box_size // 2
    # Boundary clipping aman
    y1 = max(0, center_y - half)
    y2 = min(large_ortho.shape[0], center_y + half)
    x1 = max(0, center_x - half)
    x2 = min(large_ortho.shape[1], center_x + half)
    
    # 1. Ekstrak ROI
    canopy_patch = large_ortho[y1:y2, x1:x2].copy()
    
    # 2. Penskalaan dengan INTER_AREA untuk menghindari moiré derau daun
    normalized_patch = cv2.resize(canopy_patch, (target_size, target_size), interpolation=cv2.INTER_AREA)
    
    return normalized_patch

# Uji coba fungsi pemrosesan tajuk
sample_ortho = np.random.randint(40, 180, (3000, 4000, 3), dtype=np.uint8)
patch_pohon_1 = process_palm_canopy(sample_ortho, center_x=1500, center_y=1200)
print(f"Hasil Ekstraksi Kanopi Tajuk : Dimensi {patch_pohon_1.shape}, Tipe {patch_pohon_1.dtype}")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Pengabaian Boundary Clipping pada Pengirisan ROI**: Menentukan koordinat pemotongan $y_2$ atau $x_2$ yang melebihi batas dimensi citra asli tanpa `max()` dan `min()` dapat menghasilkan array kosong yang menyebabkan kegagalan pipeline inferensi.
2. **Penggunaan Interpolasi yang Keliru saat Downsampling**: Menggunakan `cv2.INTER_NEAREST` saat memperkecil citra ortofoto tajuk pohon sawit akan menyebabkan hilangnya struktur helai anak daun halus (*aliasing artifact*). Wajib menggunakan `cv2.INTER_AREA`.
3. **Penyimpanan Berulang Citra JPEG (*Generational Loss*)**: Menyimpan dan membuka kembali citra hasil olahan berulang kali menggunakan format kompresi lossy JPEG (`.jpg`) akan menurunkan kualitas resolusi secara kumulatif. Gunakan format nir-rugi PNG (`.png`) untuk data perantara.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Selalu Validasi `if img is None`**: Tempatkan pemeriksaan integritas tepat setelah pemanggilan `cv2.imread()`.
2. **Kloning Matriks ROI**: Pastikan selalu menyertakan `.copy()` setelah operasi slicing jika ROI akan dimodifikasi lebih lanjut.
3. **Pertahankan Aspek Rasio (*Aspect-Preserving Resize*)**: Gunakan teknik penambahan bantalan hitam (*letterboxing / padding*) bila harus menyesuaikan citra persegi panjang ke dalam tensor masukan bujur sangkar.

---

## 7. Rangkuman Modul

* Pembacaan citra dengan `cv2.imread()` memuat data ke dalam array NumPy berformat BGR dan membutuhkan validasi eksplisit terhadap objek bernilai `None`.
* Pengirisan area minat (*Region of Interest* / ROI) dilakukan menggunakan indexing baris-kolom array NumPy `[y1:y2, x1:x2]` yang menghemat waktu komputasi pemrosesan visual.
* Transformasi afina memfasilitasi translasi dan rotasi menggunakan matriks $2 \times 3$ yang dieksekusi dengan fungsi `cv2.warpAffine()`.
* Pemilihan algoritma interpolasi pada `cv2.resize()` harus disesuaikan dengan arah penskalaan: `INTER_AREA` untuk pengecilan (*downsampling*) dan `INTER_CUBIC` atau `INTER_LINEAR` untuk pembesaran (*upscaling*).

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Analisis Matriks Transformasi Affine (Bloom C3)**: Tentukan matriks transformasi $2 \times 3$ untuk menggeser citra tandan sawit sebesar 50 piksel ke kanan ($t_x = +50$) dan 30 piksel ke atas ($t_y = -30$)! Tuliskan representasi matriks NumPy-nya!
2. **Analisis Distorsi Aspek Rasio (Bloom C4)**: Sebuah citra ortofoto memiliki dimensi asli $1200 \times 800$ (aspek rasio $1.5:1$). Jika citra tersebut langsung diubah ukurannya menjadi $300 \times 300$ tanpa penambahan bantalan (*padding*):
   * Hitung rasio distorsi penskalaan pada sumbu horizontal dan vertikal!
   * Jelaskan dampak distorsi ini terhadap fitur kebulatan (*circularity*) tajuk pohon kelapa sawit yang sedang diukur!

### Tugas Pemrograman Mandiri
Buatlah fungsi Python `letterbox_resize(image, target_size=256)` yang mengubah ukuran citra dengan mempertahankan aspek rasio aslinya, lalu mengisi ruang kosong yang tersisa dengan warna abu-abu netral $(114, 114, 114)$. Ujilah fungsi tersebut pada citra berdimensi $800 \times 400$ dan simpan hasilnya dalam format PNG!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 11.3: Color Conversion

Kita telah menguasai cara membaca, memotong area minat ROI, memutar orientasi, dan mengubah ukuran spasial citra perkebunan. Namun, seluruh citra yang kita olah sejauh ini masih tersusun dalam ruang warna BGR mentah yang sangat peka terhadap perubahan bayangan dan pencahayaan sinar matahari langsung.

Pada **AI Modul 11.3: Color Conversion**, kita akan mempelajari secara mendalam bagaimana mentransformasikan citra ke berbagai ruang warna strategis: mengonversi ke **Grayscale** untuk deteksi tepi cepat, mengonversi ke **HSV** untuk memisahkan warna buah matang dari intensitas cahaya matahari, serta mengonversi ke **CIELAB** untuk analisis warna yang menyerupai persepsi visual mata manusia.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media. (Bab 5: Image Processing & Geometric Transforms).
2. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson. (Bab 2: Digital Image Fundamentals).
3. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications* (2nd ed.). Springer. (Bab 3: Image Processing).
4. Fadilah, R., & Pangaribuan, R. (2021). Fruit detection and sorting automation using computer vision in agribusiness. *Journal of Agricultural Engineering and Technology*, 15(2), 112-124.
"""
    validate_text(md_content, "AI_Modul_11.2_Image_reading_dan_manipulation.md")
    with open("docs/part-11/AI_Modul_11.2_Image_reading_dan_manipulation.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-11/AI_Modul_11.2_Image_reading_dan_manipulation.md")

    # Notebook 11.2
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 11.2: Praktikum Image Reading dan Manipulation\n",
                    "**Mata Kuliah:** Visi Komputer dan Pengolahan Citra Digital  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Membaca dan memvalidasi berkas citra secara aman dengan penanganan galat `NoneType`.\n",
                    "2. Melakukan pengirisan area minat (*Region of Interest* / ROI) pada citra tandan buah sawit.\n",
                    "3. Mengimplementasikan koreksi rotasi dan translasi geometri afina menggunakan `cv2.warpAffine`.\n",
                    "4. Membandingkan algoritma interpolasi resolusi (`INTER_AREA`, `INTER_LINEAR`, `INTER_NEAREST`) dan mengimplementasikan letterboxing.\n"
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
                    "## 1. Pembangkitan Citra Sintetis Meja Sortasi dan Pemotongan ROI\n",
                    "Mensimulasikan tandan buah sawit di meja konveyor dan mengekstrak area minat (ROI) menggunakan slicing NumPy."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Membuat citra konveyor abu-abu gelap 600x800\n",
                    "conveyor = np.full((600, 800, 3), 45, dtype=np.uint8)\n",
                    "\n",
                    "# Menggambar tandan buah sawit miring 30 derajat\n",
                    "center_palm = (420, 310)\n",
                    "cv2.ellipse(conveyor, center_palm, (160, 95), 30, 0, 360, (25, 115, 230), -1)\n",
                    "cv2.circle(conveyor, (420, 310), 25, (10, 60, 160), -1)\n",
                    "\n",
                    "# Simpan citra sintetis\n",
                    "cv2.imwrite('conveyor_sample.jpg', conveyor)\n",
                    "\n",
                    "# Pemotongan ROI Tandan Buah (Y: 180..440, X: 220..620)\n",
                    "y1, y2 = 180, 440\n",
                    "x1, x2 = 220, 620\n",
                    "roi_palm = conveyor[y1:y2, x1:x2].copy()\n",
                    "\n",
                    "print(f'Dimensi Citra Konveyor Asli : {conveyor.shape}')\n",
                    "print(f'Dimensi ROI Buah Terpotong  : {roi_palm.shape}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Koreksi Rotasi Geometri Affine (Pelurusan Posisi Tandan)\n",
                    "Membangun matriks rotasi afina untuk meluruskan orientasi tandan sebesar -30 derajat."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "h_roi, w_roi = roi_palm.shape[:2]\n",
                    "center_roi = (w_roi // 2, h_roi // 2)\n",
                    "\n",
                    "# Matriks rotasi 2x3\n",
                    "M_rot = cv2.getRotationMatrix2D(center=center_roi, angle=-30, scale=1.0)\n",
                    "roi_straight = cv2.warpAffine(roi_palm, M_rot, (w_roi, h_roi), borderMode=cv2.BORDER_CONSTANT, borderValue=(45, 45, 45))\n",
                    "\n",
                    "print('Matriks Transformasi Afina (2x3):\\n', M_rot)\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Penskalaan dengan Letterboxing (Mempertahankan Aspek Rasio)\n",
                    "Mengubah ukuran ROI ke dimensi model AI standar 224x224 dengan padding abu-abu netral."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "def letterbox_resize(img, target_size=(224, 224), pad_color=(45, 45, 45)):\n",
                    "    h, w = img.shape[:2]\n",
                    "    target_w, target_h = target_size\n",
                    "    scale = min(target_w / w, target_h / h)\n",
                    "    \n",
                    "    nw, nh = int(w * scale), int(h * scale)\n",
                    "    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)\n",
                    "    \n",
                    "    canvas = np.full((target_h, target_w, 3), pad_color, dtype=np.uint8)\n",
                    "    dx = (target_w - nw) // 2\n",
                    "    dy = (target_h - nh) // 2\n",
                    "    canvas[dy:dy+nh, dx:dx+nw] = resized\n",
                    "    return canvas\n",
                    "\n",
                    "tbs_letterbox = letterbox_resize(roi_straight, target_size=(224, 224))\n",
                    "print(f'Dimensi Citra Akhir Letterboxing: {tbs_letterbox.shape}')\n",
                    "\n",
                    "# Visualisasi Tahapan Manipulasi Citra\n",
                    "fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))\n",
                    "# Konversi BGR ke RGB untuk visualisasi Matplotlib\n",
                    "axes[0].imshow(cv2.cvtColor(conveyor, cv2.COLOR_BGR2RGB))\n",
                    "axes[0].set_title('1. Citra Konveyor Asli & Bounding Box', fontsize=10, fontweight='bold')\n",
                    "rect = plt.Rectangle((x1, y1), x2-x1, y2-y1, fill=False, edgecolor='red', linewidth=2)\n",
                    "axes[0].add_patch(rect)\n",
                    "\n",
                    "axes[1].imshow(cv2.cvtColor(roi_straight, cv2.COLOR_BGR2RGB))\n",
                    "axes[1].set_title('2. ROI Buah Terotasi (-30 Deg)', fontsize=10, fontweight='bold')\n",
                    "\n",
                    "axes[2].imshow(cv2.cvtColor(tbs_letterbox, cv2.COLOR_BGR2RGB))\n",
                    "axes[2].set_title('3. Penskalaan Letterbox (224x224)', fontsize=10, fontweight='bold')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_manipulasi_citra_11_2.png', dpi=150)\n",
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
    with open("notebooks/part-11/AI_Modul_11.2_Praktikum_Image_Reading_dan_Manipulation.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-11/AI_Modul_11.2_Praktikum_Image_Reading_dan_Manipulation.ipynb")

    # Guide 11.2
    guide_content = r"""# AI Modul 11.2: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-02
* **Topik Utama**: Pembacaan Citra, Slicing ROI, Transformasi Afina, dan Interpolasi
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Geometri, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.2, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Mekanisme `cv2.imread()`, parameter flag, dan penanganan kesalahan berkas nihil (`NoneType`).
* **Menit 25 - 50**: Formulasi aljabar linier transformasi afina 2D: translasi, rotasi koordinat dengan pusat sembarang, dan perbandingan metode interpolasi (`INTER_AREA` vs `INTER_LINEAR`).
* **Menit 50 - 120**: Praktikum laboratorium: ekstraksi ROI tandan sawit dari citra konveyor, perancangan matriks rotasi, dan implementasi teknik letterboxing proporsional.
* **Menit 120 - 150**: Asesmen formatif mengenai bahaya distorsi aspek rasio pada morfometri tanaman dan pengantar Modul 11.3 (Color Conversion).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Penanganan Berkas Citra** | Mengimplementasikan validasi `if img is None` dan eksepsi error secara konsisten dan aman. | Menggunakan `imread` dengan benar namun lupa menyertakan validasi berkas nihil. | Mengabaikan pemeriksaan berkas sehingga menghasilkan error `NoneType`. |
| **Pemotongan ROI & Manipulasi** | Mampu melakukan slicing ROI dua dimensi dengan koordinat aman dan kloning `.copy()`. | Melakukan slicing dengan benar namun lupa menggunakan method `.copy()`. | Tertukar antara indeks baris (Y) dan kolom (X) dalam slicing array. |
| **Transformasi Afina & Resizing** | Merumuskan matriks rotasi afina dan menerapkan teknik letterboxing proporsional tanpa distorsi. | Mampu merotasi citra namun fungsi resize langsung memampatkan citra tanpa letterbox. | Salah mendefinisikan matriks transformasi sehingga citra terpotong atau hilang. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Matriks Translasi Affine
Transformasi translasi 2D dirumuskan sebagai:
$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$
Dengan pergeseran $t_x = +50$ piksel dan $t_y = -30$ piksel:
$$M = \begin{bmatrix} 1.0 & 0.0 & 50.0 \\ 0.0 & 1.0 & -30.0 \end{bmatrix}$$
Representasi matriks dalam NumPy:
```python
M = np.float32([[1, 0, 50], [0, 1, -30]])
```

### Jawaban Soal Konseptual 2: Analisis Distorsi Aspek Rasio
Diketahui: Ukuran asli $W_{\text{orig}} = 1200, H_{\text{orig}} = 800$. Ukuran target $W_{\text{target}} = 300, H_{\text{target}} = 300$.
1. **Rasio Penskalaan**:
   * Sumbu Horizontal: $s_x = \frac{300}{1200} = 0.25$ (faktor pengecilan 4 kali lipat).
   * Sumbu Vertikal: $s_y = \frac{300}{800} = 0.375$ (faktor pengecilan 2.67 kali lipat).
   * Rasio Distorsi: $\frac{s_x}{s_y} = \frac{0.25}{0.375} \approx 0.667$.
2. **Dampak terhadap Morfometri Tanaman**:
   Pengecilan horizontal yang lebih agresif dibandingkan vertikal akan memipihkan objek secara mendatar. Tajuk pohon kelapa sawit yang awalnya berbentuk melingkar simetris ($C \approx 1.0$) akan terdistorsi menjadi bentuk elips lonjong, sehingga nilai kebulatan (*circularity*) $C = \frac{4\pi A}{P^2}$ akan turun secara drastis secara artifisial. Akibatnya, algoritma deteksi kanopi rusak akan salah mengklasifikasikan pohon sehat sebagai pohon cacat pelepah (*false positive pest damage*).
"""
    validate_text(guide_content, "AI_Modul_11.2_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-11/AI_Modul_11.2_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-11/AI_Modul_11.2_Panduan_Instruktur_dan_Kunci_Solusi.md")

# ==============================================================================
# MODUL 11.3: Color Conversion
# ==============================================================================
def create_modul_11_3():
    md_content = r"""# AI Modul 11.3: Color Conversion

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-11-03
* **Mata Kuliah**: Visi Komputer dan Pengolahan Citra Digital (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Genap)
* **Prasyarat**: AI Modul 11.2 (Image Reading dan Manipulation)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Transformasi Ruang Warna BGR/HSV/LAB, Segmentasi Spektral cv2.inRange, Masking Bitwise"] --> B["OUTCOMES: Kemampuan Memisahkan Informasi Warna Tanaman dari Derau Iluminasi Matahari"]
    B --> C["IMPACTS: Akurasi Tinggi pada Klasifikasi Tingkat Kematangan Buah Sawit & Deteksi Klorosis Daun"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** prinsip fisika dan komputasi dari berbagai model representasi ruang warna: BGR/RGB (perangkat penangkap optik), Grayscale (intensitas luminansi), HSV/HSB (persepsi sifat warna intuitif), dan CIELAB (persepsi warna berjarak seragam / *perceptually uniform*).
2. **Menerapkan (C3)** fungsi konversi warna OpenCV (`cv2.cvtColor()`) serta teknik segmentasi warna berbasis ambang rentang ganda (`cv2.inRange()`) yang digabungkan dengan operasi logika penyamaran piksel (`cv2.bitwise_and()`) pada data citra perkebunan.
3. **Menganalisis (C4)** keunggulan ruang warna HSV dan CIELAB dalam mengatasi tantangan bayangan awan dan variasi intensitas radiasi matahari langsung pada pemilahan kematangan buah kelapa sawit di lingkungan terbuka.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Pemahaman mendalam formula matematis konversi BGR ke Grayscale, BGR ke HSV, dan dekomposisi kanal warna.
  * Skrip Python modular berstandar PEP 8 untuk segmentasi warna buah sawit matang (oranye-merah) dan daun tanaman (hijau).
  * Laporan analisis komparasi ketahanan masker segmentasi antara ruang warna BGR dan ruang warna HSV pada variasi pencahayaan lapangan.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian memilih ruang warna yang tepat sesuai dengan tujuan inspeksi agronomis (deteksi penyakit, pematangan buah, atau analisis tekstur tanah).
  * Kemampuan mengisolasi objek tanaman secara instan tanpa memerlukan beban komputasi berat jaringan saraf dalam.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Peningkatan keandalan sistem inspeksi optik otomatis pada stasiun penerimaan pabrik kelapa sawit yang beroperasi di bawah kondisi cuaca alami dinamis.

---

## 2. Profil Fundamental Konversi Ruang Warna: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Konversi ruang warna adalah pemetaan matematis yang mentransformasikan vektor koordinat piksel dari satu basis representasi warna ke basis representasi warna lainnya:
1. **Reduksi Dimensi (BGR ke Grayscale)**: Mengompresi informasi 3 kanal warna menjadi 1 kanal intensitas skalar tunggal berbobot fotometrik ($Y$), mereduksi kebutuhan memori hingga $66.7\%$ dan mempercepat operasi filtering konvolusi.
2. **Dekopling Krominansi dan Luminansi (BGR ke HSV / LAB)**: Memisahkan komponen intensitas cahaya (*Value* pada HSV atau $L^*$ pada CIELAB) dari informasi warna murni (*Hue* dan *Saturation* pada HSV, atau $a^*$ dan $b^*$ pada CIELAB).
3. **Penyaringan Rentang Warna Spasial (*Color Slicing via Masking*)**: Mengidentifikasi seluruh piksel yang nilai warnanya berada di dalam batas bawah (*lower bound*) dan batas atas (*upper bound*) tertentu untuk menghasilkan masker biner tanaman.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Sortasi Kematangan Tandan Buah Segar (TBS)**: Menghitung persentase buah matang (jingga cerah / merah) vs buah mentah (hitam keunguan) berdasarkan nilai Hue pada ruang warna HSV.
* **Deteksi Defisiensi Nitrogen & Klorosis**: Memantau pergeseran nilai Hue daun kelapa sawit dari hijau pekat ($H \approx 60 - 80$) menuju kuning pucat ($H \approx 25 - 40$).
* **Eliminasi Bayangan Kanopi pada Citra Drone**: Memisahkan daun yang terkena sinar matahari langsung dan daun di bawah bayangan menggunakan kanal $L^*$ pada ruang warna CIELAB.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
Dalam ruang warna BGR asli, nilai ketiga kanal ($B, G, R$) berubah secara simultan jika intensitas sinar matahari bertambah atau tertutup awan, sehingga perancangan aturan ambang batas biner menjadi sangat rapuh. Dengan mengonversi citra ke ruang warna HSV, informasi corak warna (*Hue*) tetap konstan meskipun intensitas cahaya (*Value*) berfluktuasi secara drastis.

### 2.4 Analisis Kelebihan dan Kekurangan Ruang Warna

| Ruang Warna | Parameter Komponen | Keunggulan Utama | Kelemahan Kritis | Rekomendasi Kasus Perkebunan |
| :--- | :--- | :--- | :--- | :--- |
| **BGR** | Blue, Green, Red ($0-255$) | Format asli perangkat keras kamera. | Sangat sensitif terhadap bayangan dan kecerahan. | Akuisisi awal dan penulisan berkas citra. |
| **Grayscale** | Intensitas Tunggal ($0-255$) | Komputasi paling cepat, data kompak. | Kehilangan seluruh informasi diferensiasi spektral warna. | Deteksi tepi Canny, analisis tekstur, dan deteksi wajah. |
| **HSV** | Hue ($0-179$), Sat ($0-255$), Val ($0-255$) | Memisahkan corak warna dari intensitas cahaya. | Hue bernilai singular/tak tentu pada saat Saturation nol. | Segmentasi buah matang dan pemetaan tajuk daun hijau. |
| **CIELAB** | L ($0-255$), a ($0-255$), b ($0-255$) | Jarak Euclidean antar-warna seragam persepsi (*perceptual*). | Transformasi matematis non-linier lebih berat. | Pengukuran derajat warna baku standar laboratorium CPO. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Pabrik Kelapa Sawit mengoperasikan kamera sortasi di atas meja getar. Ketika awan melintas di atas atap transparan pabrik, intensitas cahaya turun sebesar $40\%$. Sistem sortasi berbasis BGR mengalami kegagalan karena nilai $R$ buah matang turun di bawah ambang batas statis, sehingga buah matang didiagnosa sebagai buah mentah. Setelah insinyur memperbarui pipeline ke ruang warna HSV, sistem hanya memantau parameter $H \in [10, 25]$ (spektrum jingga-merah) tanpa mempedulikan penurunan nilai $V$, sehingga akurasi sortasi tetap stabil di atas $95\%$ sepanjang hari.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Skala Nilai Hue pada OpenCV**: Secara teoritis, lingkaran warna Hue memiliki rentang derajat $0^\circ - 360^\circ$. Namun karena tipe data citra 8-bit hanya mampu menyimpan nilai maksimal 255, OpenCV membagi nilai derajat Hue dengan 2: **rentang Hue di OpenCV adalah $0 - 179$**, bukan $0 - 255$ atau $0 - 360$. Mengabaikan konvensi ini akan menyebabkan batas warna bergeser secara fatal.
2. **Karakteristik Melingkar Warna Merah**: Warna merah murni berada di perbatasan $0^\circ$ dan $360^\circ$. Di OpenCV, spektrum merah terbagi menjadi dua interval: rentang $H \in [0, 10]$ dan $H \in [170, 179]$. Untuk mendeteksi buah sawit merah matang secara sempurna, diperlukan penggabungan dua masker (*bitwise OR*).

---

## 3. Landasan Teori & Konsep Matematis Konversi Warna

![Diagram Konversi Ruang Warna OpenCV BGR RGB HSV LAB](../assets/diagram_konversi_ruang_warna_opencv_bgr_rgb_hsv_lab.png)

### 3.1 Formulasi Konversi BGR ke Grayscale
Konversi dari kanal BGR ke intensitas luminansi monokrom $Y$ didasarkan pada kurva sensitivitas fotopik mata manusia terhadap panjang gelombang cahaya (standar ITU-R BT.601):

$$Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$$

Perhatikan bahwa bobot kanal hijau ($G$) adalah yang paling dominan ($58.7\%$) karena reseptor mata manusia paling sensitif terhadap spektrum hijau, yang sangat menguntungkan untuk citra vegetasi perkebunan.

### 3.2 Formulasi Konversi BGR ke HSV
Diberikan nilai piksel ternormalisasi $R, G, B \in [0, 1]$:
* Tentukan nilai ekstrem:
  $$V = \max(R, G, B), \quad m = \min(R, G, B), \quad \Delta = V - m$$
* Perhitungan Kejenuhan (*Saturation*):
  $$S = \begin{cases} 0, & \text{jika } V = 0 \\ \frac{\Delta}{V}, & \text{jika } V > 0 \end{cases}$$
* Perhitungan Corak Warna (*Hue*):
  $$H = \begin{cases} 0, & \text{jika } \Delta = 0 \\ 60^\circ \times \left( \frac{G - B}{\Delta} \pmod 6 \right), & \text{jika } V = R \\ 60^\circ \times \left( \frac{B - R}{\Delta} + 2 \right), & \text{jika } V = G \\ 60^\circ \times \left( \frac{R - G}{\Delta} + 4 \right), & \text{jika } V = B \end{cases}$$

Di dalam OpenCV, nilai $H$ dalam derajat ($[0^\circ, 360^\circ)$) kemudian dipetakan ke integer 8-bit:
$$H_{\text{OpenCV}} = \text{round}\left(\frac{H}{2}\right) \in [0, 179]$$
$$S_{\text{OpenCV}} = \text{round}(S \times 255) \in [0, 255]$$
$$V_{\text{OpenCV}} = \text{round}(V \times 255) \in [0, 255]$$

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Citra Masukan BGR"] --> B["cv2.cvtColor(img, cv2.COLOR_BGR2HSV)"]
    B --> C["Definisi Ambang Batas: lower_bound & upper_bound"]
    C --> D["Pembangkitan Masker Biner: mask = cv2.inRange(hsv, lower, upper)"]
    D --> E["Pembersihan Derau Spasial: cv2.morphologyEx(Opening)"]
    E --> F["Penyamaran Citra: result = cv2.bitwise_and(img, img, mask=mask)"]
    F --> G["Kalkulasi Rasio Persentase Area Warna"]
```

Implementasi Python modular untuk segmentasi buah sawit matang (merah-oranye) berbasis HSV:

```python
import cv2
import numpy as np

# 1. Pembangkitan Citra Sintetis Tandan Buah Sawit Berbagai Fraksi Kematangan
height, width = 400, 600
image_bgr = np.full((height, width, 3), 50, dtype=np.uint8) # Background konveyor

# Buah Mentah (Hitam keunguan, H ~ 140, S ~ 50, V ~ 40)
cv2.circle(image_bgr, (150, 200), 70, (40, 20, 30), -1)

# Buah Kurang Matang / Mengkal (Kuning kehijauan, BGR: (20, 180, 200))
cv2.circle(image_bgr, (300, 200), 70, (20, 180, 200), -1)

# Buah Matang Sempurna (Jingga/Merah Terang, BGR: (15, 80, 230))
cv2.circle(image_bgr, (450, 200), 70, (15, 80, 230), -1)

# 2. Konversi Ruang Warna ke HSV
hsv_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

# 3. Penentuan Ambang Batas Warna Buah Matang (Merah-Jingga)
# Rentang 1: Jingga ke Merah Awal (H: 5 - 20)
lower_ripe = np.array([5, 120, 100], dtype=np.uint8)
upper_ripe = np.array([22, 255, 255], dtype=np.uint8)
mask_ripe = cv2.inRange(hsv_image, lower_ripe, upper_ripe)

# 4. Operasi Masking Bitwise
isolated_ripe = cv2.bitwise_and(image_bgr, image_bgr, mask=mask_ripe)

# 5. Penghitungan Rasio Luas Area Buah Matang
total_pixels = height * width
ripe_pixels = cv2.countNonZero(mask_ripe)
persen_matang = (ripe_pixels / total_pixels) * 100

print(f"Total Piksel Citra          : {total_pixels}")
print(f"Piksel Buah Matang Terdeteksi: {ripe_pixels}")
print(f"Persentase Area Matang      : {persen_matang:.2f}%")
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Segmentasi Kanopi Tajuk Sawit

### 5.1 Spesifikasi Masalah
Dalam sensus pohon kelapa sawit menggunakan drone, kanopi pohon sawit hijau harus dipisahkan secara otomatis dari gulma, semak belukar, dan jalan tanah merah.

### 5.2 Implementasi Segmentasi Kanopi Hijau Sehat
```python
# Rentang warna hijau vegetasi sawit pada HSV:
# Hue hijau: 35 hingga 85
lower_green = np.array([35, 60, 40], dtype=np.uint8)
upper_green = np.array([85, 255, 255], dtype=np.uint8)

# Masker tajuk pohon
mask_canopy = cv2.inRange(hsv_image, lower_green, upper_green)

# Pembersihan derau menggunakan operasi morfologi opening
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask_clean = cv2.morphologyEx(mask_canopy, cv2.MORPH_OPEN, kernel)

print(f"Piksel Kanopi Hijau Terdeteksi : {cv2.countNonZero(mask_clean)}")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Mengabaikan Rentang Hue OpenCV $0 - 179$**: Memasukkan batas nilai Hue di atas 179 (misalnya 240 karena mengacu pada software grafis seperti Photoshop) akan menyebabkan galat modulo atau kegagalan deteksi warna target.
2. **Hanya Menggunakan Satu Rentang untuk Warna Merah**: Mengabaikan fakta bahwa warna merah melintasi nilai $0^\circ$ dan $360^\circ$ sehingga hanya mendeteksi setengah spektrum warna merah.
3. **Mengabaikan Pengaruh Kejenuhan Rendah**: Pada piksel yang sangat gelap ($V < 30$) atau sangat terang ($V > 240, S < 20$), nilai Hue menjadi tidak stabil (*unstable chromaticity*).

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Gabungkan Dua Rentang untuk Deteksi Merah**:
   ```python
   mask1 = cv2.inRange(hsv, np.array([0, 70, 50]), np.array([10, 255, 255]))
   mask2 = cv2.inRange(hsv, np.array([170, 70, 50]), np.array([179, 255, 255]))
   mask_red = cv2.bitwise_or(mask1, mask2)
   ```
2. **Kombinasikan dengan Morfologi Spasial**: Selalu terapkan operasi `cv2.morphologyEx()` tipe opening atau closing pada masker biner untuk menghilangkan derau bintik putih (*salt noise*).
3. **Validasi Visual dengan Matplotlib**: Selalu konversi BGR ke RGB menggunakan `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` sebelum menampilkannya pada Matplotlib.

---

## 7. Rangkuman Modul

* Ruang warna BGR adalah representasi standar penangkap sensor kamera digital, sedangkan Grayscale merefleksikan intensitas radiasi monokrom.
* Ruang warna HSV memisahkan corak warna (*Hue*), kejenuhan (*Saturation*), dan intensitas cahaya (*Value*), menjadikannya ruang warna optimal untuk segmentasi objek perkebunan di bawah sinar matahari dinamis.
* OpenCV menetapkan rentang Hue sebesar $0 - 179$ untuk mengakomodasi representasi integer tak bertanda 8-bit.
* Segmentasi warna berbasis `cv2.inRange()` dan `cv2.bitwise_and()` memberikan solusi pemilahan objek berkecepatan sangat tinggi tanpa memerlukan inferensi deep learning yang berat.

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Analisis Sensitivitas Fotometrik (Bloom C3)**: Rumus konversi luminansi adalah $Y = 0.299 R + 0.587 G + 0.114 B$. Jelaskan mengapa bobot kanal hijau ($G$) diberikan nilai paling tinggi ($0.587$)? Bagaimana implikasi bobot ini terhadap deteksi bercak penyakit daun kuning pada citra grayscale?
2. **Evaluasi Pemilihan Ruang Warna (Bloom C4)**: Pada perkebunan kelapa sawit, kamera drone mengambil foto kanopi pada pukul 07.00 pagi (cahaya redup kemerahan) dan pukul 12.00 siang (cahaya terik). Jelaskan secara analitis mengapa segmentasi daun hijau menggunakan ambang batas pada ruang warna BGR akan mengalami kegagalan fatal pada salah satu waktu tersebut, sedangkan ruang warna HSV mampu mempertahankan akurasi!

### Tugas Pemrograman Mandiri
Buatlah skrip Python yang menerima citra daun kelapa sawit dan secara otomatis menghasilkan 4 panel visualisasi berdampingan: (1) Citra Asli RGB, (2) Kanal Hue (HSV), (3) Masker Biner Daun Sehat, dan (4) Masker Biner Area Klorosis/Kuning. Hitung rasio keparahan klorosis sebagai $\frac{\text{Piksel Kuning}}{\text{Total Piksel Daun}} \times 100\%$!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 11.4: Thresholding

Kita telah menguasai cara mengonversi ruang warna dan mengekstrak masker biner menggunakan ambang batas rentang warna HSV. Namun, bagaimana jika kita ingin mengubah citra grayscale menjadi citra biner hitam-putih secara otomatis tanpa perlu menentukan nilai ambang batas secara manual? Bagaimana jika intensitas cahaya di atas kanopi tidak merata akibat gradien bayangan tajuk pohon?

Pada **AI Modul 11.4: Thresholding**, kita akan mempelajari secara mendalam berbagai teknik penambangan biner: **Simple Global Thresholding**, algoritma optimasi varians intra-kelas **Otsu's Thresholding**, serta teknik **Adaptive Thresholding** (Mean & Gaussian) yang secara dinamis menghitung ambang batas lokal per jendela lingkungan piksel.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson. (Bab 6: Color Image Processing).
2. Bradski, G., & Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media.
3. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications* (2nd ed.). Springer.
4. Septiarini, A., Sunyoto, A., Hamdani, H., Kasim, A. A., & Utaminingrum, F. (2020). Machine vision-based greenness grading of oil palm fresh fruit bunches. *International Journal of Intelligent Engineering and Systems*, 13(4), 406-417.
"""
    validate_text(md_content, "AI_Modul_11.3_Color_conversion.md")
    with open("docs/part-11/AI_Modul_11.3_Color_conversion.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-11/AI_Modul_11.3_Color_conversion.md")

    # Notebook 11.3
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 11.3: Praktikum Color Conversion\n",
                    "**Mata Kuliah:** Visi Komputer dan Pengolahan Citra Digital  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Mengonversi citra BGR ke Grayscale, RGB, HSV, dan CIELAB menggunakan `cv2.cvtColor`.\n",
                    "2. Memahami rentang skala nilai Hue OpenCV ($0 - 179$) dan memecahkan batasan warna merah melingkar.\n",
                    "3. Melakukan segmentasi spektral warna buah sawit matang (oranye/merah) menggunakan `cv2.inRange` dan `cv2.bitwise_and`.\n",
                    "4. Menganalisis ketahanan ruang warna HSV terhadap variasi intensitas pencahayaan lapangan.\n"
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
                    "## 1. Pembangkitan Citra Sintetis Buah Sawit Multifraksi Kematangan\n",
                    "Membangkitkan citra 3 buah sawit dengan tingkat kematangan berbeda: Mentah (hitam), Kurang Matang (kuning-hijau), dan Matang (merah-oranye)."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "h, w = 350, 600\n",
                    "fruits_bgr = np.full((h, w, 3), 40, dtype=np.uint8)\n",
                    "\n",
                    "# Buah 1: Mentah / Unripe (Hitam Keunguan: BGR=(35, 20, 30))\n",
                    "cv2.circle(fruits_bgr, (130, 175), 65, (35, 20, 30), -1)\n",
                    "\n",
                    "# Buah 2: Kurang Matang / Underripe (Kuning-Kehijauan: BGR=(20, 180, 200))\n",
                    "cv2.circle(fruits_bgr, (300, 175), 65, (20, 180, 200), -1)\n",
                    "\n",
                    "# Buah 3: Matang Sempurna / Ripe (Jingga-Kemerahan: BGR=(15, 75, 230))\n",
                    "cv2.circle(fruits_bgr, (470, 175), 65, (15, 75, 230), -1)\n",
                    "\n",
                    "# Konversi Ruang Warna ke HSV dan Grayscale\n",
                    "fruits_gray = cv2.cvtColor(fruits_bgr, cv2.COLOR_BGR2GRAY)\n",
                    "fruits_hsv = cv2.cvtColor(fruits_bgr, cv2.COLOR_BGR2HSV)\n",
                    "fruits_rgb = cv2.cvtColor(fruits_bgr, cv2.COLOR_BGR2RGB)\n",
                    "\n",
                    "print(f'Dimensi Citra BGR : {fruits_bgr.shape}')\n",
                    "print(f'Dimensi Grayscale : {fruits_gray.shape}')\n",
                    "print(f'Dimensi HSV       : {fruits_hsv.shape}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Segmentasi Buah Matang Berbasis Ambang Rentang HSV\n",
                    "Mengisolasi buah matang berwarna oranye-merah menggunakan `cv2.inRange` dan operasi masking `cv2.bitwise_and`."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Rentang warna buah matang (Hue 5 s/d 22, Saturation >= 100, Value >= 100)\n",
                    "lower_ripe = np.array([5, 100, 100], dtype=np.uint8)\n",
                    "upper_ripe = np.array([22, 255, 255], dtype=np.uint8)\n",
                    "\n",
                    "mask_ripe = cv2.inRange(fruits_hsv, lower_ripe, upper_ripe)\n",
                    "result_ripe = cv2.bitwise_and(fruits_bgr, fruits_bgr, mask=mask_ripe)\n",
                    "\n",
                    "total_fruit_area = np.sum(fruits_gray > 50)\n",
                    "ripe_fruit_area = cv2.countNonZero(mask_ripe)\n",
                    "ripe_percentage = (ripe_fruit_area / max(total_fruit_area, 1)) * 100\n",
                    "\n",
                    "print(f'Piksel Area Buah Total  : {total_fruit_area}')\n",
                    "print(f'Piksel Buah Matang      : {ripe_fruit_area}')\n",
                    "print(f'Rasio Kematangan Buah   : {ripe_percentage:.2f}%')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Dekomposisi Kanal HSV dan Hasil Segmentasi\n",
                    "Menampilkan citra asli, kanal Hue, masker biner, dan hasil isolasi buah matang."
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
                    "axes[0].imshow(fruits_rgb)\n",
                    "axes[0].set_title('1. Citra Asli (RGB Display)', fontsize=10, fontweight='bold')\n",
                    "axes[0].axis('off')\n",
                    "\n",
                    "axes[1].imshow(fruits_hsv[:, :, 0], cmap='hsv')\n",
                    "axes[1].set_title('2. Kanal Hue (0 - 179)', fontsize=10, fontweight='bold')\n",
                    "axes[1].axis('off')\n",
                    "\n",
                    "axes[2].imshow(mask_ripe, cmap='gray')\n",
                    "axes[2].set_title('3. Masker Biner Buah Matang', fontsize=10, fontweight='bold')\n",
                    "axes[2].axis('off')\n",
                    "\n",
                    "axes[3].imshow(cv2.cvtColor(result_ripe, cv2.COLOR_BGR2RGB))\n",
                    "axes[3].set_title(f'4. Buah Matang Terisolasi ({ripe_percentage:.1f}%)', fontsize=10, fontweight='bold')\n",
                    "axes[3].axis('off')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_color_segmentation_11_3.png', dpi=150)\n",
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
    with open("notebooks/part-11/AI_Modul_11.3_Praktikum_Color_Conversion.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-11/AI_Modul_11.3_Praktikum_Color_Conversion.ipynb")

    # Guide 11.3
    guide_content = r"""# AI Modul 11.3: Panduan Instruktur dan Kunci Solusi

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
"""
    validate_text(guide_content, "AI_Modul_11.3_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-11/AI_Modul_11.3_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-11/AI_Modul_11.3_Panduan_Instruktur_dan_Kunci_Solusi.md")

if __name__ == '__main__':
    create_modul_11_2()
    create_modul_11_3()
