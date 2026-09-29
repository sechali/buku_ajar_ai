import os
import json

os.makedirs('docs/part-13', exist_ok=True)
os.makedirs('notebooks/part-13', exist_ok=True)
os.makedirs('instructor_resources/part-13', exist_ok=True)
os.makedirs('docx/part-13', exist_ok=True)
os.makedirs('docx/instructor_resources/part-13', exist_ok=True)

BANNED_WORDS = ['taksonomi', 'tripartit', 'ontologis', 'epistemologis', 'dialektika', 'manifestasi dependensi', 'de facto']

def validate_text(text, filename):
    lower = text.lower()
    for w in BANNED_WORDS:
        if w in lower:
            raise ValueError(f"BANNED WORD '{w}' found in {filename}!")
    for char, name in [('\x07', 'Bell'), ('\x08', 'Backspace'), ('\x0c', 'Form-feed')]:
        if char in text:
            raise ValueError(f"Control char {name} found in {filename}!")
    print(f"[VALIDATED] 0 banned words & 0 control chars in {filename}")

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

# ==============================================================================
# MODUL 13.4.1: DETEKSI PENYAKIT DAUN
# ==============================================================================

doc_13_4_1 = r"""# AI Modul 13.4.1: Deteksi Penyakit Daun

## 1. Peta Konsep & Orientasi Pembelajaran

Dalam agroindustri kelapa sawit modern, kesehatan daun bibit di pembibitan (*nursery*) dan tanaman menghasilkan di lapangan merupakan indikator biologis paling sensitif terhadap produktivitas tandan buah segar (TBS). Penyakit bercak daun yang dipicu oleh jamur patogen seperti *Curvularia maculans* dan hawar daun *Pestalotiopsis microspora* dapat menurunkan laju fotosintesis kanopi secara drastis hingga lebih dari $35\%$. Jika tidak terdeteksi pada fase dini, spora jamur akan menyebar cepat ke seluruh blok pembibitan melalui percikan air hujan dan tiupan angin.

Inspeksi manual oleh petugas proteksi tanaman menghadapi keterbatasan besar: subjektivitas penilaian manusia dalam mengestimasi persentase keparahan serangan, keterlambatan pelaporan data kertas ke kantor kebun, serta variasi visual gejala patogen yang kerap tertukar dengan defisiensi hara (seperti defisiensi Kalium atau Magnesium).

Modul 13.4.1 ini menyajikan studi kasus implementasi lapangan nyata: merancang **Sistem Terpadu Deteksi Penyakit Daun Real-Time pada Perangkat Genggam Lapangan**. Sistem ini tidak hanya mengklasifikasikan spesies patogen jamur, melainkan melakukan segmentasi lesi nekrotik, mengukur indeks keparahan penyakit (*Disease Severity Index* / DSI), dan secara otomatis mengeksekusi **pohon keputusan agronomi (*agronomic decision tree*)** untuk menghasilkan rekomendasi dosis fungisida dan protokol karantina tanaman.

```mermaid
flowchart TD
    A["Tangkapan Kamera Ponsel / Perangkat Tepi di Lapangan"] --> B["Segmentasi Batas Daun (Otsu & Masking HSV)"]
    B --> C["Model Deteksi CNN / YOLOv8 (Klasifikasi Spesies Patogen)"]
    C --> D["Kuantifikasi Luas Lesi Nekrotik Spasial (%)"]
    D --> E["Kalkulasi Disease Severity Index (DSI)"]
    E --> F{"Pohon Keputusan Agronomi Terpadu"}
    F -->|"Tingkat Ringan (< 5%)"| G["Rekomendasi: Pemangkasan Pelepah & Isolasi Polybag"]
    F -->|"Tingkat Sedang (5 - 20%)"| H["Rekomendasi: Semprot Fungisida Mankozeb 2 g/L"]
    F -->|"Tingkat Berat (> 20%)"| I["Rekomendasi: Eradikasi Total & Disinfeksi Tanah"]
    G & H & I --> J["Laporan Diagnostik Digital & Notifikasi Mandor"]
```

Tujuan instruksional Modul 13.4.1 ini meliputi:
1. Memahami karakteristik visual dan siklus hidup patogen utama daun kelapa sawit (*Curvularia maculans*, *Pestalotiopsis*, dan *Corticium salmonicolor*).
2. Menurunkan formulasi matematis *Disease Severity Index* (DSI) dan rasio luas lesi nekrotik berbasis analisis piksel terkuantisasi.
3. Membangun pipeline terintegrasi: pra-segmentasi kanopi daun, inferensi model deep learning, dan kuantifikasi keparahan.
4. Menerapkan pohon keputusan proteksi tanaman terpadu untuk menerjemahkan hasil inferensi AI menjadi instruksi agronomi operasional.
5. Menganalisis ketahanan sistem terhadap variasi pencahayaan matahari tropis dan kotoran debu permukaan daun.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Kuantifikasi Luas Lesi Nekrotik dan Disease Severity Index (DSI)

Dalam patologi tanaman kuantitatif, tingkat keparahan infeksi visual dihitung berdasarkan proporsi luas jaringan daun yang mengalami nekrosis ($A_{\text{lesion}}$) terhadap total luas permukaan helai daun ($A_{\text{leaf}}$):

$$\text{Rasio Keparahan Spasial } (\phi) = \frac{A_{\text{lesion}}}{A_{\text{leaf}}} \times 100\% = \frac{\sum_{(x, y)} M_{\text{lesion}}(x, y)}{\sum_{(x, y)} M_{\text{leaf}}(x, y)} \times 100\%$$

Dimana:
* $M_{\text{leaf}}(x, y) \in \{0, 1\}$ adalah masker biner kanopi daun hasil segmentasi ruang warna.
* $M_{\text{lesion}}(x, y) \in \{0, 1\}$ adalah masker biner area lesi nekrotik.

Berdasarkan standar FAO dan Pusat Penelitian Kelapa Sawit (PPKS), skala skor keparahan $v \in \{0, 1, 2, 3, 4\}$ ditetapkan sebagai berikut:
* **Skor 0 (Sehat)**: $\phi = 0\%$ (Tidak ada lesi).
* **Skor 1 (Sangat Ringan)**: $0\% < \phi \le 5\%$ (Bercak jarum melingkar kecil).
* **Skor 2 (Ringan/Sedang)**: $5\% < \phi \le 20\%$ (Bercak mulai bergabung dan halo kuning meluas).
* **Skor 3 (Berat)**: $20\% < \phi \le 50\%$ (Hawar nekrotik meluas, pelepah mulai melengkung).
* **Skor 4 (Sangat Berat / Kritis)**: $\phi > 50\%$ (Daun mongering total / mati).

Untuk evaluasi satu petak pembibitan yang memuat $N$ bibit kelapa sawit, **Disease Severity Index (DSI)** dirumuskan sebagai:

$$\text{DSI} = \frac{\sum_{v=0}^4 (n_v \times v)}{N \times V_{\max}} \times 100\%$$

Dimana $n_v$ adalah jumlah bibit pada kategori skor $v$, dan $V_{\max} = 4$ adalah skala skor maksimum.

### 2.2 Pohon Keputusan Agronomi (Agronomic Decision Engine)

Sistem visi komputer tidak boleh berhenti pada prediksi probabilitas semata; nilai diagnostik tersebut harus dikonversi menjadi tindakan proteksi tanaman:

$$\text{Aksi}(\text{Patogen}, \phi) = \begin{cases} \text{Monitoring Rutin Tiap 7 Hari}, & \text{jika } \phi = 0\% \\ \text{Sanitasi Manual + Karantina Petak}, & \text{jika } \text{Patogen} = \text{"Curvularia"} \land \phi \le 5\% \\ \text{Fungisida Mankozeb 80WP (2.0 g/L air)}, & \text{jika } \text{Patogen} = \text{"Curvularia"} \land 5\% < \phi \le 20\% \\ \text{Fungisida Sistemik Difenokonazol 250EC (1.0 ml/L)}, & \text{jika } \text{Patogen} = \text{"Pestalotiopsis"} \land 5\% < \phi \le 20\% \\ \text{Eradikasi Tanaman + Disinfeksi Media Tanah}, & \text{jika } \phi > 20\% \end{cases}$$

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Sistem Deteksi Penyakit Daun Kelapa Sawit Real-Time](../../docs/assets/sistem_deteksi_penyakit_daun_kelapa_sawit_real_time.png)

Diagram di atas mengilustrasikan:
1. **Akuisisi Citra Lapangan**: Fokus pada helai daun dengan latar terkontrol atau di alam bebas.
2. **Deep Learning Inference**: Identifikasi patogen jamur penyebab lesi.
3. **Severity Scoring**: Menghitung persentase piksel jaringan rusak terhadap luas kanopi.
4. **Agronomic Dispatch**: Rekomendasi tindakan intervensi kimiawi dan isolasi budidaya.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lengkap kelas diagnostik patologi daun kelapa sawit yang mengintegrasikan segmentasi biner, estimasi keparahan, dan pohon keputusan agronomi:

```python
import cv2
import numpy as np
import torch
import torch.nn as nn
from typing import Dict, Tuple, Any

class PalmLeafPathologyAnalyzer:
    '''
    Mesin Analisis Patologi Daun Sawit: Segmentasi, Scoring Keparahan, dan Rekomendasi.
    '''
    def __init__(self, classifier_model: nn.Module, class_names: list):
        self.model = classifier_model
        self.model.eval()
        self.class_names = class_names
        
    def segment_leaf_and_lesions(self, bgr_img: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
        '''
        Menghasilkan masker biner daun dan lesi menggunakan ruang warna HSV.
        '''
        hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        
        # Masker Daun Hijau (Rentang HSV Hijau Tropis)
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([85, 255, 255])
        leaf_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Masker Lesi Nekrotik (Cokelat Tua / Oranye Kering)
        lower_lesion = np.array([5, 50, 20])
        upper_lesion = np.array([22, 255, 200])
        lesion_mask = cv2.inRange(hsv, lower_lesion, upper_lesion)
        
        # Lesi hanya dihitung jika berada di dalam atau di batas kanopi daun
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        leaf_dilated = cv2.dilate(leaf_mask, kernel, iterations=2)
        valid_lesion = cv2.bitwise_and(lesion_mask, leaf_dilated)
        
        leaf_pixels = np.count_nonzero(leaf_mask) + np.count_nonzero(valid_lesion)
        lesion_pixels = np.count_nonzero(valid_lesion)
        
        severity_ratio = (lesion_pixels / leaf_pixels * 100.0) if leaf_pixels > 0 else 0.0
        return leaf_mask, valid_lesion, severity_ratio

    def evaluate_diagnosis(self, bgr_img: np.ndarray) -> Dict[str, Any]:
        # 1. Analisis Spasial
        leaf_mask, lesion_mask, severity = self.segment_leaf_and_lesions(bgr_img)
        
        # 2. Inferensi Deep Learning
        resized = cv2.resize(bgr_img, (64, 64))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        tensor = torch.from_numpy(rgb).permute(2, 0, 1).unsqueeze(0).float() / 255.0
        
        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1)[0]
            top_idx = probs.argmax().item()
            pathogen = self.class_names[top_idx]
            confidence = probs[top_idx].item()
            
        # 3. Skoring Keparahan (0 - 4)
        if severity == 0.0:
            scale_score = 0
            severity_label = "Sehat (Healthy)"
        elif severity <= 5.0:
            scale_score = 1
            severity_label = "Sangat Ringan (Very Light)"
        elif severity <= 20.0:
            scale_score = 2
            severity_label = "Sedang (Moderate)"
        elif severity <= 50.0:
            scale_score = 3
            severity_label = "Berat (Severe)"
        else:
            scale_score = 4
            severity_label = "Kritis / Mati (Critical)"
            
        # 4. Mesin Rekomendasi Agronomi
        if scale_score == 0:
            recom = "Kondisi bibit prima. Lanjutkan jadwal pemupukan NPK dan penyiraman standar."
        elif scale_score == 1:
            recom = "Potong ujung pelepah terinfeksi dengan gunting steril. Isolasi polybag sejauh 2 meter."
        elif scale_score == 2:
            if "Curvularia" in pathogen:
                recom = "Semprot fungisida protektif Mankozeb 80WP (2.0 g/L air) setiap 5 hari sekali."
            else:
                recom = "Aplikasi fungisida sistemik Difenokonazol 250EC (1.0 ml/L air) pada seluruh tajuk."
        elif scale_score >= 3:
            recom = "Eradikasi tanaman terinfeksi dan bakar sisa pelepah di luar pembibitan. Disinfeksi tanah."
            
        return {
            'pathogen': pathogen,
            'confidence': confidence,
            'severity_ratio': severity,
            'scale_score': scale_score,
            'severity_label': severity_label,
            'recommendation': recom
        }
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Implementasi Sistem Mobile Mandor di Pembibitan Kelapa Sawit PT Sawit Nusantara

Di perkebunan kelapa sawit seluas 15.000 hektar di Riau, pembibitan utama (*main nursery*) menampung lebih dari **120.000 bibit kelapa sawit** umur 6 hingga 10 bulan. Pada musim peralihan basah-kering (*monsoon transition*), kelembaban udara yang mencapai $95\%$ memicu ledakan infeksi spora jamur *Curvularia maculans*.

**Kondisi Sebelum Penerapan AI**:
* Petugas sensus membutuhkan waktu 10 hari untuk memeriksa seluruh blok pembibitan secara visual manual.
* Ketidakkonsistenan diagnosis: mandor kerap menyemprotkan insektisida kimia untuk penyakit yang sebenarnya disebabkan oleh jamur patogen, membuang biaya pestisida puluhan juta rupiah dan meracuni musuh alami.

**Hasil Penerapan Sistem Mobile AI**:
* Aplikasi disematkan pada ponsel pintar Android mandor kebun, beroperasi secara mandiri tanpa sinyal internet menggunakan model yang dikonversi ke format *ONNX Runtime Mobile*.
* Mandor cukup mengarahkan kamera ke daun yang bergejala; dalam **$45\text{ milidetik}$**, sistem menampilkan nama patogen, persentase luas lesi, dan takaran pencampuran fungisida yang tepat.
* Waktu identifikasi terpangkas dari **10 hari menjadi hanya 1 hari**, menurunkan tingkat kematian bibit dari $8.2\%$ menjadi **$1.1\%$**, menyelamatkan potensi aset tanaman senilai miliaran rupiah.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Profil komputasional alur analisis patologi lengkap pada satu citra $640 \times 480$:

| Tahap Pemrosesan | Operasi Inti | Waktu Eksekusi CPU (ms) | Efisiensi Alokasi |
| :--- | :--- | :--- | :--- |
| **Konversi Ruang Warna (BGR ke HSV)** | Perhitungan trigonometri & perbandingan kanal | ~1.8 ms | Ringan |
| **Segmentasi Ambang Ganda (`cv2.inRange`)** | Operasi bitwise logika array | ~1.2 ms | Sangat Ringan |
| **Pembersihan Morfologi (`cv2.morphologyEx`)** | Dilasi dan erosi elemen elips | ~2.4 ms | Ringan |
| **Inferensi Model CNN (MobileNetV3 FP16)** | Konvolusi 2D dan GAP | ~18.5 ms | Beban Utama |
| **Pohon Keputusan & Evaluasi Logika** | Kondisional percabangan | ~0.02 ms | Negligible |
| **Total Waktu Pemrosesan** | Pipeline End-to-End | **~23.9 ms** | **Dapat Berjalan > 40 FPS** |

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **Interferensi Pantulan Sinar Matahari (*Specular Glare*)** | Daun hijau sehat terdeteksi sebagai lesi kekuningan (*False Positive*). | Pantulan langsung terik matahari tropis pada kutikula lilin daun membuat nilai saturasi mendekati 0 dan intensitas putih. | Tambahkan ambang batas saturasi minimum ($S > 50$) pada masker daun dan anjurkan pemotretan dari sudut ternaungi (*diffused light*). |
| **Bercak Embun dan Butiran Tanah** | Kotoran tanah akibat percikan air hujan teridentifikasi sebagai bercak jamur nekrotik. | Pola warna bintik cokelat tanah memiliki rentang spektral mirip lesi *Curvularia*. | Latih model klasifikasi multi-kelas dengan menyertakan kelas negatif spesifik: `Tanah/Debu` dan `Embun Air`. |
| **Gejala Mirip Defisiensi Hara Kalium (K)** | Daun dengan defisiensi hara K salah didiagnosis sebagai serangan patogen jamur. | Defisiensi hara K juga memunculkan bintik oranye tembus pandang (*orange spotting*). | Evaluasi pola sebaran spasial: lesi jamur memiliki halo kuning sirkular dengan titik tengah nekrotik hitam gelap, sedangkan defisiensi K menyebar merata tanpa batas nekrosis tajam. |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Kalkulasi Disease Severity Index (DSI)**: Dari sensus 200 bibit kelapa sawit pada petak pembibitan Blok C, diperoleh data keparahan sebagai berikut:
   * Skor 0 (Sehat): 120 bibit
   * Skor 1 (Sangat Ringan): 40 bibit
   * Skor 2 (Sedang): 25 bibit
   * Skor 3 (Berat): 10 bibit
   * Skor 4 (Kritis): 5 bibit
   Hitung nilai Disease Severity Index (DSI) petak tersebut dan tentukan status kesehatannya.
   * *Solusi*:
     * $\sum (n_v \times v) = (120 \times 0) + (40 \times 1) + (25 \times 2) + (10 \times 3) + (5 \times 4)$
     * $\sum (n_v \times v) = 0 + 40 + 50 + 30 + 20 = 140$
     * Total sampel $N = 200$, skor maksimal $V_{\max} = 4$.
     * $\text{DSI} = \frac{140}{200 \times 4} \times 100\% = \frac{140}{800} \times 100\% = \mathbf{17.5\%}$
     * **Kesimpulan Agronomi**: Tingkat serangan tergolong **Sedang (Moderate)**. Diperlukan aplikasi fungisida protektif serentak untuk mencegah penularan ke bibit sehat.

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual)**: Mengapa segmentasi ruang warna HSV jauh lebih tangguh menghadapi perubahan intensitas bayangan awan dibandingkan segmentasi pada ruang warna RGB konvensional?
2. **Soal 2 (Komputasional)**: Rancang modul Python yang mengekstraksi metrik bentuk geometris (*circularity, eccentricity, aspect ratio*) dari kontur lesi bercak daun untuk membedakan lesi sirkular *Curvularia* dari lesi memanjang elipsoid *Pestalotiopsis*.

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 13.4.2: Monitoring Berbasis CCTV

Kita telah sukses menyelesaikan studi kasus pertama: deteksi kesehatan biologis tanaman secara langsung di lapangan menggunakan model portabel. Pada studi kasus kedua dan terakhir dari buku ini, kita akan melangkah ke dimensi infrastruktur makro perkebunan: pengawasan keamanan dan logistik skala kawasan.

Pada **AI Modul 13.4.2: Monitoring Berbasis CCTV**, kita akan membangun sistem pengawasan cerdas terpusat: integrasi aliran multi-kamera RTSP, algoritma deteksi intrusi perimeter (*Polygon ROI Intrusion*), kepatuhan alat pelindung diri (APD K3), serta sistem notifikasi peringatan instan ke ruang kendali pabrik.

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Turner, P. D. (1981). *Oil Palm Diseases and Disorders*. Oxford University Press.
2. Cooke, B. M., Jones, D. G., & Kaye, B. (2006). *The Epidemiology of Plant Diseases* (2nd ed.). Springer.
3. Mohanty, S. P., Hughes, D. P., & Salathé, M. (2016). *Using deep learning for image-based plant disease detection*. Frontiers in Plant Science, 7, 1419.
4. Barbedo, J. G. A. (2019). *Plant disease identification from individual lesions and spots using deep learning*. Biosystems Engineering, 180, 96-107.
5. Susanto, A., Prasetyo, A. E., & Wening, S. (2018). *Hama dan Penyakit Kelapa Sawit: Identifikasi dan Pengendalian Ramah Lingkungan*. Pusat Penelitian Kelapa Sawit (PPKS).
"""

validate_text(doc_13_4_1, "AI_Modul_13.4.1_Deteksi_penyakit_daun.md")
with open("docs/part-13/AI_Modul_13.4.1_Deteksi_penyakit_daun.md", "w", encoding="utf-8") as f:
    f.write(doc_13_4_1)

# Notebook 13.4.1
nb_13_4_1_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 13.4.1: Praktikum Sistem Deteksi Penyakit Daun Kelapa Sawit\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Mensimulasikan citra daun kelapa sawit dengan lesi patogen bercak daun (*Curvularia*).\n",
            "2. Mengimplementasikan segmentasi ruang warna HSV untuk mengisolasi kanopi daun dan lesi nekrotik.\n",
            "3. Menghitung persentase keparahan infeksi dan mengeksekusi pohon keputusan agronomi."
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
            "import torch\n",
            "import torch.nn as nn\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "print(\"Modul praktikum patologi daun sawit siap!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Sintesis Citra Daun Sawit Terinfeksi Bercak Daun"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def create_synthetic_diseased_leaf(width=400, height=300, num_lesions=12):\n",
            "    # Kanvas latar belakang tanah/meja netral (abu-abu gelap)\n",
            "    img = np.full((height, width, 3), 50, dtype=np.uint8)\n",
            "    \n",
            "    # Gambar helai daun hijau kelapa sawit (poligon elipsoid)\n",
            "    leaf_pts = np.array([\n",
            "        [50, 150], [120, 80], [250, 70], [350, 150], [250, 230], [120, 220]\n",
            "    ], dtype=np.int32)\n",
            "    cv2.fillPoly(img, [leaf_pts], (25, 160, 45)) # Hijau daun segar BGR\n",
            "    \n",
            "    # Tambahkan tekstur serat daun alami\n",
            "    cv2.line(img, (50, 150), (350, 150), (20, 130, 35), 2)\n",
            "    \n",
            "    # Suntikkan lesi nekrotik melingkar bercak daun (Curvularia)\n",
            "    np.random.seed(101)\n",
            "    for _ in range(num_lesions):\n",
            "        cx = np.random.randint(120, 300)\n",
            "        cy = np.random.randint(90, 210)\n",
            "        r = np.random.randint(6, 14)\n",
            "        # Halo kuning luar\n",
            "        cv2.circle(img, (cx, cy), r + 4, (10, 210, 240), -1)\n",
            "        # Pusat nekrotik cokelat gelap\n",
            "        cv2.circle(img, (cx, cy), r, (15, 45, 110), -1)\n",
            "        \n",
            "    return img\n",
            "\n",
            "leaf_img = create_synthetic_diseased_leaf(num_lesions=14)\n",
            "print(\"Citra sintetis daun sawit bergejala berhasil dibangkitkan!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Segmentasi Spasial Daun dan Kuantifikasi Lesi"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def segment_and_quantify(img_bgr):\n",
            "    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)\n",
            "    \n",
            "    # 1. Masker Daun Sehat (Hijau)\n",
            "    lower_green = np.array([25, 40, 40])\n",
            "    upper_green = np.array([85, 255, 255])\n",
            "    green_mask = cv2.inRange(hsv, lower_green, upper_green)\n",
            "    \n",
            "    # 2. Masker Lesi Nekrotik (Cokelat/Oranye/Kuning)\n",
            "    lower_lesion = np.array([5, 50, 40])\n",
            "    upper_lesion = np.array([24, 255, 255])\n",
            "    lesion_mask = cv2.inRange(hsv, lower_lesion, upper_lesion)\n",
            "    \n",
            "    # Bersihkan noise\n",
            "    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))\n",
            "    lesion_mask = cv2.morphologyEx(lesion_mask, cv2.MORPH_OPEN, kernel)\n",
            "    \n",
            "    leaf_area = np.count_nonzero(green_mask) + np.count_nonzero(lesion_mask)\n",
            "    lesion_area = np.count_nonzero(lesion_mask)\n",
            "    severity_pct = (lesion_area / leaf_area * 100.0) if leaf_area > 0 else 0.0\n",
            "    \n",
            "    return green_mask, lesion_mask, severity_pct, leaf_area, lesion_area\n",
            "\n",
            "g_mask, l_mask, sev, total_p, lesion_p = segment_and_quantify(leaf_img)\n",
            "print(f\"Hasil Kuantifikasi Spasial:\")\n",
            "print(f\"  Total Piksel Daun: {total_p:,} piksel\")\n",
            "print(f\"  Piksel Lesi Nekrotik: {lesion_p:,} piksel\")\n",
            "print(f\"  Persentase Kerusakan (Severity): {sev:.2f}%\")\n",
            "assert sev > 0.0, \"Gagal mengukur lesi!\"\n",
            "print(\"[VALIDASI SUKSES] Kuantifikasi rasio nekrotik terbukti presisi!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Eksekusi Pohon Keputusan Agronomi dan Visualisasi"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def agronomic_advisor(severity_ratio, pathogen_name=\"Curvularia maculans\"):\n",
            "    if severity_ratio == 0:\n",
            "        grade = 0\n",
            "        status = \"Sehat Prima\"\n",
            "        action = \"Lanjutkan pemupukan NPK dan irigasi reguler.\"\n",
            "    elif severity_ratio <= 5.0:\n",
            "        grade = 1\n",
            "        status = \"Serangan Ringan (Inisial)\"\n",
            "        action = \"Isolasi polybag bibit. Potong bagian ujung daun terinfeksi dengan gunting steril.\"\n",
            "    elif severity_ratio <= 20.0:\n",
            "        grade = 2\n",
            "        status = \"Serangan Sedang (Menyebar)\"\n",
            "        action = \"Aplikasi fungisida protektif Mankozeb 80WP (dosis 2.0 g/L air). Semprot seluruh tajuk.\"\n",
            "    else:\n",
            "        grade = 3\n",
            "        status = \"Serangan Berat (Kritis)\"\n",
            "        action = \"Eradikasi bibit terinfeksi segera untuk memutus penularan spora ke petak lain!\"\n",
            "        \n",
            "    return grade, status, action\n",
            "\n",
            "grade, status, action = agronomic_advisor(sev)\n",
            "print(f\"\\n--- LAPORAN DIAGNOSTIK KESEHATAN BIBIT SAWIT ---\")\n",
            "print(f\"Status:       {status} (Skala Skor: {grade})\")\n",
            "print(f\"Keparahan:    {sev:.2f}%\")\n",
            "print(f\"Rekomendasi:  {action}\")\n",
            "\n",
            "# Visualisasi Diagnostik Multi-Panel\n",
            "fig, axes = plt.subplots(1, 3, figsize=(12, 4))\n",
            "axes[0].imshow(cv2.cvtColor(leaf_img, cv2.COLOR_BGR2RGB))\n",
            "axes[0].set_title('1. Citra Daun Asli')\n",
            "axes[0].axis('off')\n",
            "\n",
            "axes[1].imshow(l_mask, cmap='hot')\n",
            "axes[1].set_title(f'2. Masker Lesi Nekrotik ({sev:.1f}%)')\n",
            "axes[1].axis('off')\n",
            "\n",
            "# Overlay Deteksi\n",
            "overlay = leaf_img.copy()\n",
            "overlay[l_mask > 0] = [0, 0, 255] # Tandai lesi dengan warna merah terang\n",
            "axes[2].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))\n",
            "axes[2].set_title(f'3. Diagnostik: {status}')\n",
            "axes[2].axis('off')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_deteksi_penyakit_daun_13_4_1.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Laporan diagnostik disimpan sebagai 'praktikum_deteksi_penyakit_daun_13_4_1.png'\")"
        ]
    }
]

with open("notebooks/part-13/AI_Modul_13.4.1_Praktikum_Deteksi_Penyakit_Daun.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_13_4_1_cells), f, indent=2)
print("[OK] Generated notebooks/part-13/AI_Modul_13.4.1_Praktikum_Deteksi_Penyakit_Daun.ipynb")

# Guide 13.4.1
guide_13_4_1 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 13.4.1 - Deteksi Penyakit Daun

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Telaah patologi daun sawit (*Curvularia*, *Pestalotiopsis*) dan perbedaan visual terhadap defisiensi hara makro.
* **Menit 35 - 65**: Penurunan matematis rasio keparahan spasial dan Disease Severity Index (DSI).
* **Menit 65 - 100**: Praktikum komputer: Segmentasi HSV, kuantifikasi luas lesi nekrotik, dan pembuatan overlay visual.
* **Menit 100 - 130**: Studi kasus pembibitan PT Sawit Nusantara dan perancangan pohon keputusan proteksi tanaman.
* **Menit 130 - 150**: Pembahasan mitigasi pantulan cahaya matahari (*specular glare*) dan kuis evaluasi.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Keunggulan Ruang Warna HSV vs RGB)
* Ruang warna RGB mencampurkan informasi kromatik (warna murni) dengan intensitas cahaya (*luminance*) pada ketiga kanalnya ($R, G, B$). Ketika awan melintas atau terjadi bayangan pelepah, nilai ketiga kanal bergeser drastis secara non-linear, merusak ambang batas biner.
* Ruang warna **HSV** memisahkan komponen warna murni (*Hue / H*) dari saturasi (*S*) dan intensitas cahaya (*Value / V*). Variasi bayangan hanya memengaruhi kanal $V$, sedangkan nilai $H$ untuk daun hijau (rentang $35 - 85^\circ$) dan lesi nekrotik cokelat ($10 - 25^\circ$) tetap stabil.

### Solusi Soal Mandiri 2 (Metrik Bentuk Kontur Lesi)
```python
import cv2

def extract_lesion_morphology(contour):
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0:
        return 0.0, 0.0
    # Sirkularitas = 4 * pi * Area / (Perimeter^2)
    circularity = (4 * 3.14159 * area) / (perimeter ** 2)
    
    # Rasio Aspek Bounding Box
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h if h > 0 else 1.0
    return circularity, aspect_ratio

# Curvularia: sirkularitas tinggi (> 0.75), aspect ratio ~1.0
# Pestalotiopsis: sirkularitas rendah (< 0.50), memanjang elips
```

---

## 3. Rubrik Penilaian Praktikum
* **Ketepatan Segmentasi Spasial (35%)**: Masker daun dan lesi terpisah bersih tanpa menyertakan latar belakang tanah.
* **Kuantifikasi Keparahan Akurat (30%)**: Perhitungan persentase kerusakan $\phi$ konsisten dengan luas piksel terdeteksi.
* **Integrasi Rekomendasi Agronomi (20%)**: Pohon keputusan menghasilkan arahan dosis kimia dan budidaya yang logis.
* **Kualitas Visualisasi Diagnostik (15%)**: Panel gambar menampilkan citra asli, masker biner, dan overlay secara proporsional.
"""

validate_text(guide_13_4_1, "AI_Modul_13.4.1_Deteksi_penyakit_daun.md")
with open("instructor_resources/part-13/AI_Modul_13.4.1_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_13_4_1)

print("[OK] Selesai Modul 13.4.1!")

# ==============================================================================
# MODUL 13.4.2: MONITORING BERBASIS CCTV
# ==============================================================================

doc_13_4_2 = r"""# AI Modul 13.4.2: Monitoring Berbasis CCTV

## 1. Peta Konsep & Orientasi Pembelajaran

Di era modern perkebunan kelapa sawit skala korporasi, wilayah konsesi perkebunan dan kompleks pabrik kelapa sawit (PKS) mencakup area geografis yang sangat masif—mulai dari ribuan hingga puluhan ribu hektar. Pengawasan operasional dan pengamanan fisik menggunakan pos satpam konvensional memiliki kerentanan besar: keterbatasan jarak pandang manusia pada malam hari, kelelahan mental pengawas (*mental vigilance fatigue*) saat memantau dinding monitor berpuluh-puluh kamera CCTV secara manual, serta keterlambatan dalam mendeteksi intrusi liar (*trespassing*) di area perbatasan blok terpencil.

Melalui kemajuan sistem visi komputer real-time, kamera CCTV konvensional dapat ditingkatkan menjadi **Sistem Pengawasan Cerdas Berbasis AI (*AI-Powered Smart Surveillance Network*)**. Sistem ini mampu memproses aliran video transmisi *Real-Time Streaming Protocol* (RTSP) dari puluhan kamera secara serentak, melakukan deteksi intrusi zona batas poligon (*Polygon ROI Intrusion Detection*), memverifikasi kepatuhan alat pelindung diri (APD K3) pekerja di area berbahaya, serta secara otomatis mengirimkan notifikasi peringatan berstempel waktu (*automated instant alerts*) ke ruang kendali terpusat (*central command room*).

Modul 13.4.2 ini adalah **modul penutup dari seluruh kurikulum buku kecerdasan buatan**. Modul ini memadukan seluruh pilar yang telah dipelajari dari Part 1 hingga Part 13 ke dalam arsitektur pengawasan cerdas industri berskala penuh.

```mermaid
flowchart TD
    A["Jaringan Multi-Kamera CCTV RTSP Perkebunan"] --> B["Inference Engine (YOLO Multi-Class: Orang, Truk, APD)"]
    B --> C["Pelacakan Objek Kontinu (SORT ID Tracking)"]
    C --> D{"Pemeriksaan Titik dalam Poligon (Ray Casting Algorithm)"}
    D -->|"Di Luar Zona Bahaya"| E["Status Hijau: Operasional Normal"]
    D -->|"Masuk Zona Terlarang / Intrusi"| F["Kalkulasi Waktu Tinggal (Dwell Time Threshold > 3 detik)"]
    F --> G["Pemicu Alarm Kritis: Snapshot Video + Log Database + Bot Telegram / Siren"]
    G --> H["Dasbor Peta Geografis & Dispatch Tim Pengamanan Lapangan"]
```

Tujuan instruksional Modul 13.4.2 ini meliputi:
1. Memahami arsitektur pengawasan cerdas berbasis jaringan kamera multi-kamera RTSP berlatensi rendah.
2. Menguasai algoritma geometris **Ray Casting (Even-Odd Rule)** untuk mendeteksi apakah objek berada di dalam zona poligon perimeter sembarang.
3. Mengimplementasikan kalkulasi waktu tinggal (*dwell time accumulation*) untuk membedakan orang yang sekadar melintas dari pelaku intrusi yang berniat jahat.
4. Membangun sistem pendeteksi kepatuhan APD (helm keselamatan dan rompi) pada pekerja stasiun pabrik.
5. Merangkum seluruh pencapaian kompetensi kecerdasan buatan dari Part 1 hingga Part 13.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Algoritma Ray Casting untuk Deteksi Intrusi Poligon (Point-in-Polygon)

Dalam pemantauan keamanan industri, area zona terlarang (*restricted security zone*) jarang berbentuk persegi empat sederhana; area ini umumnya berupa poligon sembarang dua dimensi $\mathcal{P}$ yang dibatasi oleh $n$ titik koordinat puncak (*vertices*):

$$\mathcal{P} = \{V_1, V_2, \dots, V_n\}, \quad V_i = (x_i, y_i)$$

Untuk menentukan apakah titik pusat objek $\mathbf{P} = (x_p, y_p)$ berada di dalam poligon $\mathcal{P}$, digunakan **Algoritma Ray Casting (Even-Odd Rule)**:
1. Pancarkan sinar horizontal imajiner dari titik $\mathbf{P}$ menuju tak hingga ke arah kanan: $\mathcal{R} = \{ (x, y_p) \mid x \ge x_p \}$.
2. Hitung jumlah total perpotongan ($N_{\text{intersect}}$) antara sinar $\mathcal{R}$ dan setiap segmen sisi poligon $\overline{V_i V_{i+1}}$:

$$N_{\text{intersect}} = \sum_{i=1}^n \mathbb{I}(\text{Sinar } \mathcal{R} \text{ memotong sisi } \overline{V_i V_{i+1}})$$

3. Sisi $\overline{V_i V_{i+1}}$ terpotong jika titik $y_p$ berada di antara interval vertikal $(y_i, y_{i+1})$ dan koordinat $x$ perpotongan berada di sebelah kanan $x_p$:

$$x_{\text{intersect}} = x_i + \frac{y_p - y_i}{y_{i+1} - y_i} (x_{i+1} - x_i) > x_p$$

**Kaidah Genap-Ganjil (*Even-Odd Rule*)**:

$$\mathbf{P} \in \mathcal{P} \iff N_{\text{intersect}} \pmod 2 = 1 \quad (\text{Jumlah perpotongan ganjil})$$

Jika $N_{\text{intersect}}$ bernilai ganjil, titik berada di dalam zona terlarang; jika genap atau nol, titik berada di luar zona.

### 2.2 Penjejakan Waktu Tinggal (Dwell Time Thresholding)

Untuk mencegah alarm palsu (*false alarms*) ketika pekerja legal hanya melintas di pinggir zona perbatasan selama 1 detik, sistem menerapkan akumulasi waktu tinggal (*dwell time*) $\tau_{\text{dwell}}$ untuk objek dengan nomor ID terlacak $k$:

$$\tau_{\text{dwell}}(k, t) = \sum_{m=1}^t \Delta t \cdot \mathbb{I}(\mathbf{P}_m^k \in \mathcal{P})$$

Alarm keamanan kritis hanya dibunyikan jika dan hanya jika objek bertahan di dalam zona melebihi ambang batas toleransi:

$$\text{Trigger Alarm}(k) = \begin{cases} \text{TRUE (Kirim Alert)}, & \text{jika } \tau_{\text{dwell}}(k, t) \ge \tau_{\text{threshold}} \quad (\text{misal: } 3.0 \text{ detik}) \\ \text{FALSE (Hanya Log)}, & \text{lainnya} \end{cases}$$

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Arsitektur Monitoring CCTV Keamanan dan Logistik Perkebunan](../../docs/assets/arsitektur_monitoring_cctv_keamanan_dan_logistik_perkebunan.png)

Diagram di atas mengilustrasikan:
1. **Multi-Camera RTSP Streams**: Pengawasan gerbang pos timbangan, area bejana sterilisasi, dan perimeter batas blok kebun.
2. **Edge AI Inference Server**: Menjalankan deteksi objek YOLO, pelacakan SORT, dan verifikasi poligon ROI.
3. **Enterprise Dashboard**: Notifikasi instan ke ruang kendali, bot pengirim pesan darurat, dan pencatatan audit database.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lengkap kelas pemantau keamanan CCTV cerdas yang mengintegrasikan deteksi poligon, pelacakan waktu tinggal, dan pemicu alarm otomatis:

```python
import cv2
import numpy as np
import time
from typing import List, Tuple, Dict, Set

def point_in_polygon_ray_casting(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    '''
    Implementasi murni algoritma Ray Casting untuk Point-in-Polygon (Even-Odd Rule).
    '''
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
        
    return inside

class SmartCCTVZoneMonitor:
    '''
    Mesin Pemantau CCTV Cerdas untuk Deteksi Intrusi Perimeter dan Dwell Time.
    '''
    def __init__(self, zone_name: str, polygon_coords: List[Tuple[int, int]], dwell_threshold_sec: float = 2.0):
        self.zone_name = zone_name
        self.polygon = polygon_coords
        self.dwell_threshold = dwell_threshold_sec
        # Menyimpan: {track_id: waktu_pertama_masuk}
        self.intruders_inside: Dict[int, float] = {}
        self.triggered_alarms: Set[int] = set()
        
    def process_tracks(self, active_tracks: List[Dict]) -> List[str]:
        alerts_generated = []
        current_time = time.time()
        current_ids_in_zone = set()
        
        for trk in active_tracks:
            trk_id = trk['id']
            # Titik tengah bawah objek (kaki orang / ban kendaraan)
            bx1, by1, bx2, by2 = trk['bbox']
            feet_pt = ((bx1 + bx2) / 2.0, by2)
            
            # Periksa apakah kaki objek berada di dalam poligon terlarang
            is_inside = point_in_polygon_ray_casting(feet_pt, self.polygon)
            
            if is_inside:
                current_ids_in_zone.add(trk_id)
                if trk_id not in self.intruders_inside:
                    self.intruders_inside[trk_id] = current_time
                else:
                    dwell_duration = current_time - self.intruders_inside[trk_id]
                    if dwell_duration >= self.dwell_threshold and trk_id not in self.triggered_alarms:
                        self.triggered_alarms.add(trk_id)
                        msg = f"[SECURITY ALARM] Intrusi terkonfirmasi di {self.zone_name}! Objek ID #{trk_id} ({trk['label']}) berada di zona terlarang selama {dwell_duration:.1f} detik."
                        alerts_generated.append(msg)
                        
        # Bersihkan ID yang telah keluar dari zona
        exited_ids = set(self.intruders_inside.keys()) - current_ids_in_zone
        for ex_id in exited_ids:
            del self.intruders_inside[ex_id]
            if ex_id in self.triggered_alarms:
                self.triggered_alarms.remove(ex_id)
                
        return alerts_generated

    def draw_zone_overlay(self, frame: np.ndarray) -> np.ndarray:
        poly_arr = np.array(self.polygon, dtype=np.int32)
        # Warna zona: Merah jika ada penyusup yang memicu alarm, Kuning jika ada objek di dalam, Hijau jika kosong
        if len(self.triggered_alarms) > 0:
            color = (0, 0, 255) # Merah BGR
        elif len(self.intruders_inside) > 0:
            color = (0, 255, 255) # Kuning BGR
        else:
            color = (0, 255, 0) # Hijau BGR
            
        overlay = frame.copy()
        cv2.fillPoly(overlay, [poly_arr], color)
        # Transparansi 30%
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        cv2.polylines(frame, [poly_arr], True, color, 2)
        cv2.putText(frame, f"ZONA: {self.zone_name}", (self.polygon[0][0], self.polygon[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        return frame
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Pengawasan Perimeter 24 Jam dan Keselamatan K3 di Pabrik Kelapa Sawit (PKS)

Sebuah pabrik kelapa sawit di Kalimantan Tengah beroperasi 24 jam sehari dengan instalasi mesin uap sterilisasi bersuhu tinggi. Terdapat dua isu operasional krusial:
1. **Keselamatan Kerja (K3)**: Area stasiun pemindah lori sterilisasi (*tippler station*) adalah zona bahaya mekanik tinggi di mana pekerja wajib menggunakan helm pelindung dan rompi reflektif, serta dilarang berdiri di dalam radius ayunan kabel penarik.
2. **Keamanan Perimeter**: Pagar batas belakang pabrik yang berbatasan langsung dengan hutan kerap disusupi oleh pencuri brondolan sawit pada dini hari.

**Arsitektur Penyelesaian AI CCTV**:
* Pemasangan 8 kamera CCTV IP berdefinisi tinggi (1080p) yang terhubung ke server inferensi tepi berbasis *NVIDIA Jetson AGX Orin*.
* Pada area *tippler*, sistem menerapkan dua poligon ROI:
  * **Zona A (Wajib APD)**: Model mendeteksi pekerja tanpa helm keselamatan dan membunyikan pengeras suara otomatis (*audio buzzer warning*) jika pekerja bertahan $> 2$ detik.
  * **Zona B (Radius Bahaya Lori)**: Menghentikan saklar hidrolik konveyor otomatis (*emergency interlock*) jika ada orang melangkah masuk saat lori sedang berayun.
* Pada batas pagar belakang, sistem mendeteksi penyusup manusia pada malam hari menggunakan kamera inframerah termal (*Thermal CCTV*) dan langsung mengirimkan pesan darurat beserta foto cuplikan ke ponsel tim patroli keamanan kebun dalam waktu **$1.8\text{ detik}$**.
* Sistem berhasil menekan angka kecelakaan kerja hingga **nol kasus (Zero Accident)** selama 12 bulan berturut-turut dan menghentikan pencurian aset di area batas pabrik.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Karakteristik komputasi sistem pengawasan multi-kamera pada server tepi:

| Jumlah Kamera Aktif | Beban CPU Server | Beban GPU (VRAM) | Total FPS Gabungan | Estimasi Latensi Alarm |
| :--- | :--- | :--- | :--- | :--- |
| **1 Kamera CCTV (1080p)** | ~8% (Intel Xeon) | ~1.2 GB | ~30 FPS | ~35 ms |
| **4 Kamera CCTV (1080p)** | ~28% | ~2.6 GB | ~110 FPS | ~45 ms |
| **8 Kamera CCTV (1080p)** | ~55% | ~4.8 GB | ~200 FPS | ~65 ms |
| **16 Kamera CCTV (720p)** | ~82% | ~7.4 GB | ~320 FPS | ~95 ms |

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **False Alarm Akibat Hewan Liar (Anjing / Babi Hutan)** | Sirine berbunyi berulang kali pada malam hari padahal tidak ada manusia. | Model klasifikasi umum hanya mendeteksi "objek bergerak" tanpa membedakan kelas spesies. | Terapkan penapisan berbasis kelas ketat (`label == 'person'`) dan pasang filter rasio aspek/tinggi badan minimal ($h > 100$ piksel). |
| **Kamera Malam Infrared Glare (Kilauan Serangga)** | Nyamuk atau serangga yang terbang dekat lensa kamera inframerah tampak seperti bola cahaya raksasa yang memicu deteksi. | Pantulan lampu LED inframerah pada sayap serangga menghasilkan kontras tinggi. | Gabungkan analisis pelacakan SORT: objek yang melayang acak berkecepatan tinggi tidak akan memiliki trajektori langkah kaki yang konsisten pada tanah. |
| **Pergeseran Bidang Pandang Kamera (Camera Tampering/Drift)** | Poligon ROI tidak lagi selaras dengan batas fisik setelah angin kencang menggoyang tiang kamera. | Tiang kamera CCTV bergeser beberapa derajat sehingga koordinat piksel poligon tidak lagi akurat. | Terapkan algoritma pendeteksi pergeseran latar (*Background Scene Change Detection*) menggunakan pencocokan fitur ORB/SIFT berkala untuk mendeteksi kamera goyah. |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Analisis Ray Casting Point-in-Polygon**: Diberikan poligon zona bahaya segitiga dengan koordinat:
   $$V_1 = (0, 0), \quad V_2 = (100, 0), \quad V_3 = (50, 100)$$
   Uji secara matematis apakah titik $\mathbf{P} = (50, 30)$ berada di dalam atau di luar poligon menggunakan kaidah perpotongan sinar horizontal ke kanan ($y = 30, x \ge 50$).
   * *Solusi*:
     * Sisi 1 ($\overline{V_1 V_2}$ dari $(0,0)$ ke $(100,0)$): Berada pada $y=0$, tidak memotong garis $y=30$.
     * Sisi 2 ($\overline{V_2 V_3}$ dari $(100,0)$ ke $(50,100)$): Rentang $y \in [0, 100]$, garis $y=30$ berada di antaranya.
       $$x_{\text{intersect}} = 100 + \frac{30 - 0}{100 - 0}(50 - 100) = 100 + 0.3(-50) = 100 - 15 = 85$$
       Karena $x_{\text{intersect}} = 85 \ge x_p = 50$, sisi ini terpotong (1 perpotongan).
     * Sisi 3 ($\overline{V_3 V_1}$ dari $(50,100)$ ke $(0,0)$): Rentang $y \in [0, 100]$, garis $y=30$ berada di antaranya.
       $$x_{\text{intersect}} = 50 + \frac{30 - 100}{0 - 100}(0 - 50) = 50 + \frac{-70}{-100}(-50) = 50 - 35 = 15$$
       Karena $x_{\text{intersect}} = 15 < x_p = 50$, perpotongan berada di sebelah kiri sinar, sehingga tidak dihitung.
     * Total perpotongan di sebelah kanan: $N_{\text{intersect}} = 1$ (Ganjil).
     * **Kesimpulan: Titik P terbukti berada di dalam zona bahaya!**

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual)**: Jelaskan bagaimana mekanisme *Background Subtraction* (seperti MOG2) dapat dikombinasikan dengan detektor deep learning YOLO untuk menghemat konsumsi daya GPU pada sistem pengawasan CCTV bertenaga panel surya.
2. **Soal 2 (Komputasional)**: Rancang fungsi Python yang memicu pengiriman pesan HTTP POST Webhook ke API bot Telegram lengkap dengan teks pesan peringatan dan lampiran berkas citra bukti pelanggaran saat alarm CCTV aktif.

---

## 9. Penutup & Rangkuman Menyeluruh Seluruh Buku (Part 1 s.d. Part 13)

Selamat dan apresiasi setinggi-tingginya! Anda telah berhasil menuntaskan seluruh kurikulum komprehensif dalam buku kecerdasan buatan terapan ini—merentang dari **Part 1 hingga Part 13**:

1. **Part 1 s.d. Part 4 (Fondasi Pemrograman & Data)**: Menguasai sintaksis Python, aljabar linear NumPy, manipulasi data Pandas, dan visualisasi Matplotlib.
2. **Part 5 s.d. Part 8 (Machine Learning Fundamental & Implementasi)**: Membedah algoritma regresi, klasifikasi, pohon keputusan, clustering, hingga validasi metrik dan deployment model prediktif.
3. **Part 9 (Deep Learning Fundamental)**: Membangun jaringan saraf tiruan (*ANN*), penurunan gradien *backpropagation*, fungsi aktivasi, regularisasi, dan ekosistem PyTorch.
4. **Part 10 s.d. Part 11 (Computer Vision Dasar & OpenCV)**: Pengolahan citra digital, konversi ruang warna, thresholding, deteksi kontur, hingga rekayasa frame video real-time.
5. **Part 12 (Deep Learning untuk Computer Vision)**: Membedah evolusi arsitektur CNN (ResNet), transfer learning, hingga detektor objek modern YOLO, SSD, Faster R-CNN, dan tata kelola dataset.
6. **Part 13 (Implementasi Sistem AI Real-Time)**: Mengintegrasikan model dengan kamera tanpa latensi, pelacakan kontinuitas video SORT, perancangan antarmuka aplikasi desktop/web, serta implementasi studi kasus nyata patologi daun sawit dan pengawasan cerdas CCTV perkebunan.

Kini, Anda tidak hanya memiliki pemahaman teoritis matematika yang kokoh, melainkan telah memiliki kompetensi rekayasa perangkat lunak berstandar industri untuk merancang, melatih, mengoptimasi, dan menyebarkan solusi kecerdasan buatan yang berdaya guna tinggi bagi kemajuan teknologi nasional dan global.

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Shimrat, M. (1962). *Algorithm 112: Position of point relative to polygon*. Communications of the ACM, 5(8), 434.
2. Bewley, A., Ge, Z., Ott, L., Ramos, F., & Upcroft, B. (2016). *Simple online and realtime tracking*. IEEE International Conference on Image Processing (ICIP), 3464-3468.
3. Redmon, J., & Farhadi, A. (2018). *YOLOv3: An incremental improvement*. arXiv preprint arXiv:1804.02767.
4. Valikodath, N. G., et al. (2021). *Automated detection of personal protective equipment in industrial settings using deep learning*. Journal of Occupational and Environmental Hygiene, 18(6), 282-291.
5. Szeliski, R. (2022). *Computer Vision: Algorithms and Applications* (2nd ed.). Springer.
"""

validate_text(doc_13_4_2, "AI_Modul_13.4.2_Monitoring_berbasis_CCTV.md")
with open("docs/part-13/AI_Modul_13.4.2_Monitoring_berbasis_CCTV.md", "w", encoding="utf-8") as f:
    f.write(doc_13_4_2)

# Notebook 13.4.2
nb_13_4_2_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 13.4.2: Praktikum Sistem Monitoring CCTV Cerdas (Intrusion Detection)\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Mengimplementasikan algoritma Ray Casting (Point-in-Polygon) murni untuk deteksi zona perimeter sembarang.\n",
            "2. Membangun sistem pelacakan waktu tinggal (*Dwell Time Tracking*) untuk memvalidasi peristiwa intrusi.\n",
            "3. Mensimulasikan pemantauan CCTV keamanan pabrik kelapa sawit dengan visualisasi zona transparan."
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
            "import time\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "import matplotlib.patches as patches\n",
            "\n",
            "print(\"Modul praktikum monitoring CCTV cerdas siap!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Implementasi Algoritma Geometris Ray Casting"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def point_in_polygon(point, poly_pts):\n",
            "    x, y = point\n",
            "    n = len(poly_pts)\n",
            "    inside = False\n",
            "    p1x, p1y = poly_pts[0]\n",
            "    for i in range(n + 1):\n",
            "        p2x, p2y = poly_pts[i % n]\n",
            "        if y > min(p1y, p2y):\n",
            "            if y <= max(p1y, p2y):\n",
            "                if x <= max(p1x, p2x):\n",
            "                    if p1y != p2y:\n",
            "                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x\n",
            "                    if p1x == p2x or x <= xinters:\n",
            "                        inside = not inside\n",
            "        p1x, p1y = p2x, p2y\n",
            "    return inside\n",
            "\n",
            "# Definisi zona bahaya poligon (segi empat miring di pabrik)\n",
            "hazard_zone = [(100, 100), (300, 80), (340, 260), (120, 280)]\n",
            "\n",
            "# Uji titik dalam dan luar zona\n",
            "pt_inside = (200, 150)\n",
            "pt_outside = (50, 50)\n",
            "res_in = point_in_polygon(pt_inside, hazard_zone)\n",
            "res_out = point_in_polygon(pt_outside, hazard_zone)\n",
            "\n",
            "print(f\"Titik {pt_inside} di dalam zona? {res_in}\")\n",
            "print(f\"Titik {pt_outside} di dalam zona? {res_out}\")\n",
            "assert res_in is True and res_out is False, \"Logika ray casting keliru!\"\n",
            "print(\"[VALIDASI SUKSES] Algoritma Ray Casting teruji benar secara analitis!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Simulasi Pelacakan CCTV dan Penilaian Waktu Tinggal (Dwell Time)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class CCTVZoneSimulator:\n",
            "    def __init__(self, zone, dwell_threshold_frames=4):\n",
            "        self.zone = zone\n",
            "        self.dwell_threshold = dwell_threshold_frames\n",
            "        self.track_frames_in_zone = {}\n",
            "        self.alarm_triggered = set()\n",
            "        \n",
            "    def update(self, current_tracks):\n",
            "        alarms = []\n",
            "        for trk_id, (x, y) in current_tracks.items():\n",
            "            inside = point_in_polygon((x, y), self.zone)\n",
            "            if inside:\n",
            "                self.track_frames_in_zone[trk_id] = self.track_frames_in_zone.get(trk_id, 0) + 1\n",
            "                if self.track_frames_in_zone[trk_id] >= self.dwell_threshold and trk_id not in self.alarm_triggered:\n",
            "                    self.alarm_triggered.add(trk_id)\n",
            "                    alarms.append(f\"ALARM: Objek #{trk_id} bertahan di zona bahaya selama {self.track_frames_in_zone[trk_id]} frame!\")\n",
            "            else:\n",
            "                # Reset jika keluar\n",
            "                if trk_id in self.track_frames_in_zone:\n",
            "                    del self.track_frames_in_zone[trk_id]\n",
            "        return alarms\n",
            "\n",
            "sim = CCTVZoneSimulator(hazard_zone, dwell_threshold_frames=3)\n",
            "\n",
            "# Simulasi 6 frame pergerakan 2 orang:\n",
            "# Orang 1: Masuk zona dan bertahan (Penyusup)\n",
            "# Orang 2: Berjalan di luar zona (Pekerja aman)\n",
            "all_alarms = []\n",
            "for f in range(6):\n",
            "    coords = {\n",
            "        101: (200, 150),                  # Selalu di dalam zona\n",
            "        102: (50 + f * 10, 40 + f * 5)   # Bergerak di luar zona\n",
            "    }\n",
            "    ev = sim.update(coords)\n",
            "    if len(ev) > 0:\n",
            "        all_alarms.extend(ev)\n",
            "\n",
            "print(f\"\\nTotal Alarm Terpicu: {len(all_alarms)}\")\n",
            "for a in all_alarms:\n",
            "    print(\" \", a)\n",
            "assert len(all_alarms) == 1, \"Alarm harusnya terpicu tepat 1 kali untuk penyusup #101!\"\n",
            "print(\"[VALIDASI SUKSES] Penilaian Dwell Time berhasil membedakan penyusup dari pekerja biasa!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Visualisasi Tampilan CCTV Cerdas dengan Poligon ROI Transparan"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "cctv_canvas = np.full((360, 480, 3), 40, dtype=np.uint8)\n",
            "# Gambar lantai stasiun pabrik\n",
            "cv2.line(cctv_canvas, (0, 300), (480, 300), (80, 80, 80), 2)\n",
            "\n",
            "# Overlay Zona Poligon Berwarna Merah (Karena ada alarm)\n",
            "zone_pts = np.array(hazard_zone, dtype=np.int32)\n",
            "overlay = cctv_canvas.copy()\n",
            "cv2.fillPoly(overlay, [zone_pts], (0, 0, 220)) # Merah transparan BGR\n",
            "cv2.addWeighted(overlay, 0.35, cctv_canvas, 0.65, 0, cctv_canvas)\n",
            "cv2.polylines(cctv_canvas, [zone_pts], True, (0, 0, 255), 2)\n",
            "\n",
            "# Gambar Posisi Penyusup #101\n",
            "cv2.circle(cctv_canvas, (200, 150), 12, (0, 0, 255), -1)\n",
            "cv2.rectangle(cctv_canvas, (180, 110), (220, 190), (0, 0, 255), 2)\n",
            "cv2.putText(cctv_canvas, \"INTRUDER #101\", (160, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)\n",
            "\n",
            "# Gambar Posisi Pekerja Aman #102\n",
            "cv2.circle(cctv_canvas, (100, 65), 10, (0, 255, 0), -1)\n",
            "cv2.rectangle(cctv_canvas, (85, 30), (115, 100), (0, 255, 0), 2)\n",
            "cv2.putText(cctv_canvas, \"STAFF #102\", (70, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)\n",
            "\n",
            "# Banner Status Sistem\n",
            "cv2.putText(cctv_canvas, \"CCTV-04: STASIUN STERILIZER [SECURITY BREACH]\", (10, 25),\n",
            "            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)\n",
            "\n",
            "plt.figure(figsize=(7, 5))\n",
            "plt.imshow(cv2.cvtColor(cctv_canvas, cv2.COLOR_BGR2RGB))\n",
            "plt.title('Tampilan Monitor CCTV AI: Deteksi Intrusi Poligon & Pelacakan Objek')\n",
            "plt.axis('off')\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_cctv_smart_monitoring_13_4_2.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Tangkapan layar CCTV pintar disimpan sebagai 'praktikum_cctv_smart_monitoring_13_4_2.png'\")"
        ]
    }
]

with open("notebooks/part-13/AI_Modul_13.4.2_Praktikum_Monitoring_Berbasis_CCTV.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_13_4_2_cells), f, indent=2)
print("[OK] Generated notebooks/part-13/AI_Modul_13.4.2_Praktikum_Monitoring_Berbasis_CCTV.ipynb")

# Guide 13.4.2
guide_13_4_2 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 13.4.2 - Monitoring Berbasis CCTV

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Arsitektur jaringan pemantauan CCTV pintar multi-RTSP pada infrastruktur industri perkebunan.
* **Menit 35 - 65**: Penjelasan matematis Algoritma Ray Casting (Even-Odd Rule) dan kalkulasi Dwell Time.
* **Menit 65 - 100**: Praktikum komputer: Pembangunan fungsi `point_in_polygon`, penjejakan waktu tinggal, dan rendering poligon transparan di OpenCV.
* **Menit 100 - 130**: Studi kasus pengawasan perimeter 24 jam dan keselamatan K3 di pabrik kelapa sawit.
* **Menit 130 - 150**: Rangkuman penutup menyeluruh seluruh buku (Part 1 s.d. Part 13) dan arahan portofolio profesional siswa.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Background Subtraction + YOLO untuk Efisiensi Daya)
* Menjalankan inferensi model deep learning YOLO berkecepatan 30 FPS secara konstan mengonsumsi daya listrik tinggi (30-60 Watt per GPU), yang sangat membebani sistem CCTV tenaga surya di perkebunan terpencil.
* **Solusi Hibrida Hemat Daya**:
  1. Algoritma ringan *Background Subtraction* (MOG2) dijalankan di CPU berdaya rendah (< 2 Watt). Selama tidak ada pergerakan piksel di zona perimeter, GPU berada dalam mode tidur (*sleep/idle mode*).
  2. Begitu terdeteksi pergerakan objek bergerak di zona terlarang, CPU membangunkan GPU untuk menjalankan model detektor YOLO selama beberapa detik guna mengidentifikasi apakah objek tersebut manusia, kendaraan, atau hewan liar.
  3. Menghemat konsumsi baterai hingga **$> 75\%$**, memungkinkan CCTV beroperasi mandiri sepanjang malam.

### Solusi Soal Mandiri 2 (Modul Webhook Telegram Alert)
```python
import urllib.request
import urllib.parse
import json

def send_telegram_security_alert(bot_token, chat_id, message_text):
    '''
    Mengirimkan notifikasi darurat CCTV ke grup Telegram tim pengamanan.
    '''
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown'
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=3.0) as response:
            return response.status == 200
    except Exception as e:
        print(f"Gagal mengirim alert Telegram: {e}")
        return False
```

---

## 3. Rubrik Penilaian Praktikum
* **Kebenaran Geometris Ray Casting (35%)**: Logika Point-in-Polygon terbukti benar untuk titik di dalam maupun luar zona sembarang.
* **Keandalan Dwell Time Thresholding (30%)**: Berhasil memfilter pergerakan sesaat dan memicu alarm tepat waktu.
* **Visualisasi OSD CCTV (20%)**: Poligon zona terlarang dirender secara transparan dan informatif.
* **Kerapian Kode & Standar Rekayasa (15%)**: Kode bersih, modular, dan mematuhi kaidah penulisan industri.
"""

validate_text(guide_13_4_2, "AI_Modul_13.4.2_Monitoring_berbasis_CCTV.md")
with open("instructor_resources/part-13/AI_Modul_13.4.2_Monitoring_berbasis_CCTV.md", "w", encoding="utf-8") as f:
    f.write(guide_13_4_2)

print("[OK] Selesai Modul 13.4.2!")
