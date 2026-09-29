import os
import json

os.makedirs('docs/part-12', exist_ok=True)
os.makedirs('notebooks/part-12', exist_ok=True)
os.makedirs('instructor_resources/part-12', exist_ok=True)
os.makedirs('docx/part-12', exist_ok=True)
os.makedirs('docx/instructor_resources/part-12', exist_ok=True)

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
# MODUL 12.7: YOLO (YOU ONLY LOOK ONCE)
# ==============================================================================

doc_12_7 = r"""# AI Modul 12.7: YOLO (You Only Look Once)

## 1. Peta Konsep & Orientasi Pembelajaran

Dalam ranah deteksi objek digital, keluarga algoritma **YOLO (You Only Look Once)**, yang dipelopori oleh Redmon et al. (2016), menandai lompatan paradigma paling revolusioner dalam sejarah visi komputer modern. Sebelum kehadiran YOLO, sistem deteksi objek didominasi oleh pendekatan dua tahap (*two-stage detectors*) seperti R-CNN yang memisahkan pembentukan proposal wilayah dari klasifikasi kotak, menjadikannya sangat lambat (kurang dari 5 frame per detik / FPS) dan tidak memadai untuk sistem otonom real-time.

YOLO membingkai ulang tugas deteksi objek bukan lagi sebagai masalah klasifikasi bertahap, melainkan sebagai **masalah regresi langsung (*direct regression problem*)** dari piksel citra mentah menuju koordinat kotak pembatas (*bounding boxes*) dan probabilitas kelas dalam **satu kali perambatan maju (*single forward pass*)**. Dalam industri agrokompleks—seperti sensus tandan buah segar (TBS) kelapa sawit menggunakan drone berkecepatan 30 km/jam atau penyortiran buah pada ban berjalan berkecepatan tinggi—arsitektur YOLO menjadi standar emas komputasi tepi (*edge computing*) berkat kemampuan inferensinya yang mampu menembus 60 hingga 120 FPS pada kartu grafis kompak.

```mermaid
flowchart TD
    A["Citra Masukan H x W x 3"] --> B["Backbone CSPDarknet (Ekstraksi Fitur Spasial)"]
    B --> C["Neck PANet / FPN (Penyatuan Fitur Multi-Skala P3, P4, P5)"]
    C --> D["Head Deteksi YOLO (Kisi Kisi S x S)"]
    D --> E["Tensor Prediksi: [tx, ty, tw, th, p_objectness, c_1..c_C]"]
    E --> F["Decoding Bounding Box & CIoU Loss Optimization"]
    F --> G["Non-Maximum Suppression (NMS) GPU"]
    G --> H["Deteksi Real-Time Kecepatan Tinggi (> 45 FPS)"]
```

Tujuan instruksional Modul 12.7 ini meliputi:
1. Memahami prinsip kerja pembagian kisi spasial (*grid cells*), konsep *objectness score*, dan penguraian tensor prediksi keluaran YOLO.
2. Membedah evolusi arsitektur YOLO: dari *grid regression* YOLOv1, *anchor boxes* YOLOv2-v4, hingga arsitektur *anchor-free* dan *CSPDarknet* pada YOLO modern.
3. Menurunkan formulasi matematis fungsi kerugian gabungan: *CIoU Bounding Box Loss*, *Objectness BCE Loss*, dan *Multi-Class Cross-Entropy*.
4. Mengimplementasikan lapisan kepala deteksi (*YOLO Detection Head*) dan mekanisme dekoding koordinat kotak berbasis PyTorch.
5. Membangun sistem deteksi tandan kelapa sawit siap panen pada citra inspeksi udara.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Mekanisme Pembagian Kisi Spasial (Grid Cell Architecture)

YOLO membagi citra masukan menjadi kisi berukuran $S \times S$. Jika titik pusat dari suatu objek berada di dalam kisi sel $(i, j)$, maka sel kisi tersebut bertanggung jawab penuh untuk mendeteksi objek terkait.

Setiap sel kisi memprediksi $B$ kotak pembatas (*bounding boxes*). Setiap kotak pembatas terdiri atas 5 nilai regresi:

$$b = [t_x, t_y, t_w, t_h, p_o]$$

Serta distribusi probabilitas bersyarat untuk $C$ kelas kategori:

$$P(\text{Class}_k \mid \text{Object}), \quad k \in \{1, \dots, C\}$$

Sehingga dimensi tensor keluaran akhir untuk kisi berukuran $S \times S$ adalah:

$$\text{Shape} = S \times S \times (B \cdot 5 + C)$$

### 2.2 Dekoding Koordinat Bounding Box

Untuk menjamin kestabilan pelatihan gradien dan mencegah kotak pembatas melompat ke luar area kisi penanggung jawab, koordinat kotak didekodekan secara non-linear:

$$b_x = \sigma(t_x) + c_x$$

$$b_y = \sigma(t_y) + c_y$$

$$b_w = p_w \cdot \exp(t_w)$$

$$b_h = p_h \cdot \exp(t_h)$$

Dimana:
* $(c_x, c_y)$ adalah koordinat offset sudut kiri atas dari sel kisi terkait.
* $\sigma(\cdot)$ adalah fungsi sigmoid logistik yang membatasi pergeseran pusat kotak hanya di dalam batas sel ($0 \le \sigma(t) \le 1$).
* $(p_w, p_h)$ adalah dimensi lebar dan tinggi kotak acuan (*anchor prior*).
* $(b_x, b_y, b_w, b_h)$ adalah koordinat prediksi akhir ternormalisasi terhadap resolusi citra.

### 2.3 Formulasi Kerugian Gabungan (YOLO Multi-Task Loss)

Fungsi kerugian YOLO mengintegrasikan tiga komponen penalti simultan:

$$\mathcal{L}_{\text{total}} = \lambda_{\text{coord}} \mathcal{L}_{\text{box}} + \lambda_{\text{obj}} \mathcal{L}_{\text{obj}} + \lambda_{\text{noobj}} \mathcal{L}_{\text{noobj}} + \lambda_{\text{cls}} \mathcal{L}_{\text{cls}}$$

1. **Complete IoU (CIoU) Box Loss**:
Mempertimbangkan tumpang tindih area, jarak titik pusat Euclidean, dan konsistensi rasio aspek ($v$):

$$\mathcal{L}_{\text{CIoU}} = 1 - \text{IoU} + \frac{\rho^2(b, b^{\text{gt}})}{c^2} + \alpha v$$

$$v = \frac{4}{\pi^2} \left( \arctan \frac{w^{\text{gt}}}{h^{\text{gt}}} - \arctan \frac{w}{h} \right)^2, \quad \alpha = \frac{v}{(1 - \text{IoU}) + v}$$

2. **Objectness Confidence Loss**:
Menggunakan Binary Cross-Entropy (BCE) dengan penalti berbeda antara sel yang memuat objek ($\mathbb{I}_{ij}^{\text{obj}}$) dan sel latar belakang kosong ($\mathbb{I}_{ij}^{\text{noobj}}$):

$$\mathcal{L}_{\text{obj}} = - \sum_{i=0}^{S^2} \sum_{j=0}^B \left[ \mathbb{I}_{ij}^{\text{obj}} \log(p_o) + \lambda_{\text{noobj}} \mathbb{I}_{ij}^{\text{noobj}} \log(1 - p_o) \right]$$

3. **Classification Loss**:
Cross-Entropy multi-kelas untuk seluruh kelas yang relevan:

$$\mathcal{L}_{\text{cls}} = - \sum_{i=0}^{S^2} \mathbb{I}_i^{\text{obj}} \sum_{c \in \text{classes}} \left[ q_c \log(\hat{p}_c) + (1 - q_c) \log(1 - \hat{p}_c) \right]$$

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Arsitektur dan Mekanisme Grid YOLO](../../docs/assets/arsitektur_dan_mekanisme_grid_yolo.png)

Diagram di atas mengilustrasikan:
1. **Kisi Spasial Citra**: Pembagian citra ke dalam sel $S \times S$ dengan penetapan sel pusat objek.
2. **Backbone CSPDarknet & Neck**: Ekstraksi fitur visual multi-skala berkecepatan tinggi.
3. **Tensor Deteksi Keluaran**: Setiap sel memproyeksikan koordinat spasial, skor keberadaan objek, dan sebaran probabilitas kelas.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lapisan kepala deteksi (*YOLO Detection Head*) dan fungsi pengurai koordinat tensor (*tensor decoder*) di PyTorch:

```python
import torch
import torch.nn as nn
from typing import Tuple

class MiniYOLOHead(nn.Module):
    '''
    Kepala Deteksi YOLO Mini Multi-Skala dengan Proyeksi Bounding Box.
    '''
    def __init__(self, in_channels: int, num_anchors: int, num_classes: int):
        super().__init__()
        self.num_anchors = num_anchors
        self.num_classes = num_classes
        # Setiap anchor memprediksi: tx, ty, tw, th, conf + num_classes
        out_channels = num_anchors * (5 + num_classes)
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Input shape: (Batch, in_channels, GridH, GridW)
        out = self.conv(x)
        B, C, H, W = out.shape
        # Ubah dimensi menjadi: (Batch, num_anchors, GridH, GridW, 5 + num_classes)
        out = out.view(B, self.num_anchors, 5 + self.num_classes, H, W)
        out = out.permute(0, 1, 3, 4, 2).contiguous()
        return out

def decode_yolo_predictions(preds: torch.Tensor, anchors: torch.Tensor, img_size: int = 416) -> torch.Tensor:
    '''
    Mendekodekan tensor mentah YOLO menjadi koordinat piksel absolut [x1, y1, x2, y2, conf, class_id].
    preds: (Batch, num_anchors, GridH, GridW, 5 + C)
    anchors: (num_anchors, 2) [anchor_w, anchor_h]
    '''
    device = preds.device
    B, num_anchors, H, W, num_attrs = preds.shape
    
    # Buat grid koordinat sel
    grid_y, grid_x = torch.meshgrid(torch.arange(H, device=device), torch.arange(W, device=device), indexing='ij')
    grid_xy = torch.stack([grid_x, grid_y], dim=-1).view(1, 1, H, W, 2).float()
    
    # Reshape anchors untuk broadcasting
    anchor_wh = anchors.view(1, num_anchors, 1, 1, 2).to(device)
    
    # 1. Dekode pusat kotak (cx, cy)
    box_xy = (torch.sigmoid(preds[..., 0:2]) + grid_xy) * (img_size / W)
    # 2. Dekode dimensi kotak (w, h)
    box_wh = torch.exp(preds[..., 2:4]) * anchor_wh
    
    # Konversi ke format [x1, y1, x2, y2]
    x1y1 = box_xy - box_wh / 2.0
    x2y2 = box_xy + box_wh / 2.0
    
    # Skor keyakinan objek
    conf = torch.sigmoid(preds[..., 4:5])
    # Probabilitas kelas
    cls_probs = torch.softmax(preds[..., 5:], dim=-1)
    
    return torch.cat([x1y1, x2y2, conf, cls_probs], dim=-1)
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Sensus Buah Sawit Otomatis Berkecepatan Tinggi via Wahana Nirawak (Drone)

Dalam manajemen operasional perkebunan kelapa sawit skala puluhan ribu hektar, inventarisasi potensi panen dilakukan dengan menerbangkan drone otonom yang menyusuri blok-blok tanaman dengan kecepatan jelajah 25-30 km/jam pada ketinggian 15 meter.

**Tantangan Sistem Deteksi**:
* Citra video berkecepatan 30 FPS harus diproses secara lokal pada modul komputasi tepi yang terpasang di wahana (*NVIDIA Jetson Xavier NX*).
* Model dua tahap (seperti Faster R-CNN) hanya mampu mencapai 6-8 FPS, menyebabkan penumpukan buffer video (*buffer lag*) dan frame yang terlewati (*dropped frames*).

**Penerapan Rekayasa YOLO**:
* Model **YOLOv8-Small** yang dikonversi ke format *TensorRT FP16* mampu berjalan pada kecepatan **58 FPS** dengan konsumsi daya hanya 15 Watt.
* Sistem berhasil mendeteksi dan menghitung tandan buah sawit dengan tingkat presisi **95.1%** dan *recall* **93.4%**, bahkan ketika drone bergerak cepat di atas tajuk pohon dengan bayangan pelepah yang dinamis.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Perbandingan varian arsitektur YOLO pada inferensi satu citra $640 \times 640$:

| Model | Ukuran Bobot | Parameter (Juta) | FLOPs (Giga) | Latensi GPU T4 (ms) | Throughput (FPS) | mAP@0.5:0.95 (COCO) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **YOLOv8-Nano (n)** | ~6.2 MB | 3.2 M | 8.7 G | ~2.1 ms | ~470 FPS | 37.3% |
| **YOLOv8-Small (s)** | ~22.5 MB | 11.2 M | 28.6 G | ~3.8 ms | ~260 FPS | 44.9% |
| **YOLOv8-Medium (m)**| ~52.0 MB | 25.9 M | 78.9 G | ~7.4 ms | ~135 FPS | 50.2% |
| **YOLOv8-XLarge (x)**| ~136.0 MB| 68.2 M | 257.8 G | ~18.2 ms | ~55 FPS | 53.9% |

Untuk instalasi kamera tepi industri perkebunan bertenaga baterai atau drone, varian **Nano** dan **Small** memberikan performa operasional terbaik.

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **Ketidakstabilan Eksponensial Dimensi Kotak** | Prediksi lebar/tinggi kotak meledak menjadi nilai tak hingga (*Inf / NaN*). | Nilai $t_w$ atau $t_h$ terlalu besar sebelum dilewatkan ke fungsi eksponensial $\exp(t)$. | Terapkan pembatasan nilai (*clipping*) pada input eksponensial: `torch.clamp(tw, max=4.0)` atau gunakan formula *anchor-free decoupled head*. |
| **Objek Berukuran Sangat Kecil Luput Terdeteksi** | Brondolan sawit yang tercecer di tanah tidak pernah terdeteksi pada citra drone. | Langkah *downsampling* backbone terlalu besar ($32\times$), sehingga objek kecil berukuran $< 16$ piksel lenyap dari peta fitur lapisan P5. | Tambahkan *head deteksi ekstra resolusi tinggi* pada lapisan P2 ($4\times$ downsampling) atau naikkan resolusi masukan menjadi $1024 \times 1024$. |
| **Dominasi Penalti Sel Latar Belakang (No-Object Loss)** | Skor keyakinan objek runtuh mendekati 0 untuk seluruh prediksi. | Jumlah sel latar belakang kosong ($99\%$) mendominasi total loss dibanding sel objek ($1\%$). | Turunkan bobot $\lambda_{\text{noobj}}$ menjadi $0.5$ atau gunakan *Focal Loss* pada cabang *objectness*. |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Analisis Output Tensor**: Jika sebuah model YOLOv3 menggunakan kisi $13 \times 13$, 3 anchor boxes per sel, dan mendeteksi 4 kelas komoditas agro (Kelapa Sawit, Karet, Kakao, Kopi), hitung jumlah total elemen pada tensor prediksi lapisan tersebut.
   * *Solusi*:
     * Dimensi per anchor: $5 + 4 = 9$ nilai.
     * Dimensi per sel: $3 \times 9 = 27$ nilai.
     * Total elemen tensor: $13 \times 13 \times 27 = 169 \times 27 = \mathbf{4.563} \text{ elemen float}$.

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual & Matematis)**: Turunkan secara analitis mengapa *Complete IoU (CIoU)* menghasilkan konvergensi lokalisasi yang jauh lebih stabil dan cepat dibandingkan *Mean Squared Error (MSE)* pada koordinat sudut kotak pembatas.
2. **Soal 2 (Komputasional)**: Rancang modul PyTorch kustom untuk menghitung kerugian *Distance-IoU (DIoU) Loss* antara sekumpulan kotak prediksi dan ground truth berdimensi $(N, 4)$.

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 12.8: Single Shot Detector (SSD)

Kita telah memahami bagaimana YOLO merevolusi visi komputer dengan memperlakukan deteksi objek sebagai regresi kisi simultan. Namun, sebelum YOLO menyempurnakan arsitektur multi-skala pada versi-versi terbarunya, arsitektur perintis lain yang meletakkan dasar deteksi piramida multi-resolusi adalah **Single Shot MultiBox Detector (SSD)**.

Pada **AI Modul 12.8: Single Shot Detector (SSD)**, kita akan membedah arsitektur SSD: pemanfaatan peta fitur bertingkat (*multi-scale feature maps*) dari berbagai kedalaman backbone, perancangan kotak acuan default (*default boxes*), serta strategi penyeimbangan data *Hard Negative Mining*.

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). *You only look once: Unified, real-time object detection*. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 779-788.
2. Redmon, J., & Farhadi, A. (2017). *YOLO9000: Better, faster, stronger*. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 7263-7271.
3. Wang, C. Y., Bochkovskiy, A., & Liao, H. Y. M. (2023). *YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 7464-7475.
4. Zheng, Z., et al. (2020). *Distance-IoU loss: Faster and better learning for bounding box regression*. Proceedings of the AAAI Conference on Artificial Intelligence, 34(07), 12993-13000.
5. Jocher, G., Chaurasia, A., & Qiu, J. (2023). *Ultralytics YOLO* (Version 8.0.0). https://github.com/ultralytics/ultralytics.
"""

validate_text(doc_12_7, "AI_Modul_12.7_YOLO.md")
with open("docs/part-12/AI_Modul_12.7_YOLO.md", "w", encoding="utf-8") as f:
    f.write(doc_12_7)

# Notebook 12.7
nb_12_7_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 12.7: Praktikum YOLO (Grid Decoding dan Inference Head)\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Membangun modul YOLO Detection Head di PyTorch.\n",
            "2. Mengimplementasikan fungsi dekoding koordinat kisi non-linear ($t_x, t_y, t_w, t_h \\to x_1, y_1, x_2, y_2$).\n",
            "3. Mensimulasikan pipeline inferensi deteksi tandan kelapa sawit pada resolusi spasial $13 \\times 13$."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import torch\n",
            "import torch.nn as nn\n",
            "import numpy as np\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "import matplotlib.patches as patches\n",
            "\n",
            "torch.manual_seed(42)\n",
            "print(f\"PyTorch Versi: {torch.__version__}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Definisi Modul Mini YOLO Detection Head"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class MiniYOLOHead(nn.Module):\n",
            "    def __init__(self, in_channels=64, num_anchors=3, num_classes=2):\n",
            "        super().__init__()\n",
            "        self.num_anchors = num_anchors\n",
            "        self.num_classes = num_classes\n",
            "        # (tx, ty, tw, th, conf) + num_classes\n",
            "        self.out_dim = num_anchors * (5 + num_classes)\n",
            "        self.conv = nn.Conv2d(in_channels, self.out_dim, kernel_size=1)\n",
            "        \n",
            "    def forward(self, x):\n",
            "        out = self.conv(x)\n",
            "        B, C, H, W = out.shape\n",
            "        out = out.view(B, self.num_anchors, 5 + self.num_classes, H, W)\n",
            "        return out.permute(0, 1, 3, 4, 2).contiguous()\n",
            "\n",
            "head = MiniYOLOHead(in_channels=64, num_anchors=3, num_classes=2)\n",
            "dummy_feat = torch.randn(1, 64, 13, 13)\n",
            "raw_preds = head(dummy_feat)\n",
            "print(f\"Bentuk Tensor Fitur Input: {dummy_feat.shape}\")\n",
            "print(f\"Bentuk Tensor Prediksi YOLO Head: {raw_preds.shape} (Batch, Anchors, H, W, Attrs)\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Fungsi Dekoding Tensor Koordinat Menjadi Bounding Box"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def decode_yolo_grid(preds, anchors, img_size=416):\n",
            "    B, num_anchors, H, W, _ = preds.shape\n",
            "    device = preds.device\n",
            "    \n",
            "    grid_y, grid_x = torch.meshgrid(torch.arange(H, device=device), torch.arange(W, device=device), indexing='ij')\n",
            "    grid_xy = torch.stack([grid_x, grid_y], dim=-1).view(1, 1, H, W, 2).float()\n",
            "    anchor_wh = anchors.view(1, num_anchors, 1, 1, 2).to(device)\n",
            "    \n",
            "    # Koordinat pusat & ukuran\n",
            "    stride = img_size / W\n",
            "    box_xy = (torch.sigmoid(preds[..., 0:2]) + grid_xy) * stride\n",
            "    box_wh = torch.exp(preds[..., 2:4]) * anchor_wh\n",
            "    \n",
            "    x1y1 = box_xy - box_wh / 2.0\n",
            "    x2y2 = box_xy + box_wh / 2.0\n",
            "    conf = torch.sigmoid(preds[..., 4:5])\n",
            "    cls_prob = torch.softmax(preds[..., 5:], dim=-1)\n",
            "    \n",
            "    return torch.cat([x1y1, x2y2, conf, cls_prob], dim=-1)\n",
            "\n",
            "# Inisialisasi anchor boxes [w, h] dalam skala piksel\n",
            "anchors = torch.tensor([[30., 40.], [60., 70.], [110., 130.]])\n",
            "decoded_boxes = decode_yolo_grid(raw_preds, anchors, img_size=416)\n",
            "print(f\"Tensor Hasil Dekoding: {decoded_boxes.shape}\")\n",
            "print(\"[VALIDASI SUKSES] Dekoding koordinat grid YOLO selesai tanpa galat!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Simulasi Deteksi Tandan Buah Sawit dan Visualisasi"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Simulasi nilai deteksi kuat pada sel kisi (6, 6) anchor 1\n",
            "mock_preds = torch.zeros(1, 3, 13, 13, 7)\n",
            "mock_preds[0, 1, 6, 6, 0:2] = 0.5  # Tengah sel\n",
            "mock_preds[0, 1, 6, 6, 2:4] = 0.0  # Ukuran sama persis anchor\n",
            "mock_preds[0, 1, 6, 6, 4] = 6.0    # Skor keyakinan sangat tinggi (sigmoid -> ~0.997)\n",
            "mock_preds[0, 1, 6, 6, 5] = 4.0    # Kelas 0: Tandan Matang\n",
            "\n",
            "res = decode_yolo_grid(mock_preds, anchors, img_size=416)\n",
            "target_det = res[0, 1, 6, 6].detach().numpy()\n",
            "\n",
            "x1, y1, x2, y2, c, p0, p1 = target_det\n",
            "print(f\"Hasil Deteksi Simulasi:\")\n",
            "print(f\"  Koordinat BBox: [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]\")\n",
            "print(f\"  Confidence: {c:.4f}\")\n",
            "print(f\"  Probabilitas Kelas 0 (Tandan Matang): {p0:.4f}\")\n",
            "\n",
            "# Visualisasi Citra Simulasi\n",
            "fig, ax = plt.subplots(figsize=(6, 6))\n",
            "ax.set_xlim(0, 416)\n",
            "ax.set_ylim(416, 0) # Format citra\n",
            "\n",
            "# Gambar grid 13x13\n",
            "for g in range(14):\n",
            "    pos = g * (416 / 13)\n",
            "    ax.axvline(pos, color='gray', linestyle=':', alpha=0.4)\n",
            "    ax.axhline(pos, color='gray', linestyle=':', alpha=0.4)\n",
            "    \n",
            "# Bounding box deteksi\n",
            "rect = patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=2.5, edgecolor='#E65100', facecolor='#FFE0B2', alpha=0.6)\n",
            "ax.add_patch(rect)\n",
            "ax.text(x1, y1-8, f\"Tandan Matang: {c:.2f}\", fontsize=10, fontweight='bold', color='#E65100')\n",
            "plt.title('Simulasi Inferensi Kepala Deteksi YOLO pada Grid 13x13')\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_yolo_grid_inference_12_7.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Visualisasi inferensi YOLO disimpan sebagai 'praktikum_yolo_grid_inference_12_7.png'\")"
        ]
    }
]

with open("notebooks/part-12/AI_Modul_12.7_Praktikum_YOLO.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_12_7_cells), f, indent=2)
print("[OK] Generated notebooks/part-12/AI_Modul_12.7_Praktikum_YOLO.ipynb")

# Guide 12.7
guide_12_7 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 12.7 - YOLO (You Only Look Once)

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Filosofi Single-Stage Detector vs Two-Stage, konsep pembagian kisi $S \times S$, dan peran anchor boxes.
* **Menit 35 - 65**: Penurunan matematis fungsi transformasi non-linear koordinat kotak dan komponen kerugian CIoU.
* **Menit 65 - 100**: Praktikum komputer: Perakitan modul `MiniYOLOHead` di PyTorch, penguraian tensor prediksi, dan visualisasi kotak pada grid.
* **Menit 100 - 130**: Studi kasus sensus buah kelapa sawit via kamera drone berkecepatan 30 km/jam.
* **Menit 130 - 150**: Pembahasan jebakan numerik fungsi eksponensial dan strategi eliminasi redundansi NMS di GPU.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Keunggulan CIoU vs MSE Loss)
* MSE memperlakukan keempat koordinat ($x, y, w, h$) sebagai variabel independen, padahal dimensi kotak memiliki relasi geometris ketat (misal: rasio aspek).
* MSE sangat sensitif terhadap skala absolut: kotak besar mendominasi gradien dibanding kotak kecil dengan error proporsional identik.
* Sebaliknya, **Complete IoU (CIoU)**:
  1. Bersifat invarian terhadap skala objek (*scale invariant*).
  2. Memberikan gradien halus bahkan saat kotak tidak beririsan (melalui penalti jarak Euclidean titik pusat).
  3. Mempertahankan konsistensi rasio aspek ($v$) secara simultan.

### Solusi Soal Mandiri 2 (Implementasi Distance-IoU / DIoU Loss)
```python
import torch

def diou_loss(pred_boxes, gt_boxes):
    '''
    pred_boxes, gt_boxes: Tensor (N, 4) format [x1, y1, x2, y2]
    '''
    # 1. Hitung Intersection over Union
    x1 = torch.max(pred_boxes[:, 0], gt_boxes[:, 0])
    y1 = torch.max(pred_boxes[:, 1], gt_boxes[:, 1])
    x2 = torch.min(pred_boxes[:, 2], gt_boxes[:, 2])
    y2 = torch.min(pred_boxes[:, 3], gt_boxes[:, 3])
    
    inter = torch.clamp(x2 - x1, min=0) * torch.clamp(y2 - y1, min=0)
    area_pred = (pred_boxes[:, 2] - pred_boxes[:, 0]) * (pred_boxes[:, 3] - pred_boxes[:, 1])
    area_gt = (gt_boxes[:, 2] - gt_boxes[:, 0]) * (gt_boxes[:, 3] - gt_boxes[:, 1])
    union = area_pred + area_gt - inter
    iou = inter / (union + 1e-7)
    
    # 2. Titik pusat kotak
    pred_cx = (pred_boxes[:, 0] + pred_boxes[:, 2]) / 2.0
    pred_cy = (pred_boxes[:, 1] + pred_boxes[:, 3]) / 2.0
    gt_cx = (gt_boxes[:, 0] + gt_boxes[:, 2]) / 2.0
    gt_cy = (gt_boxes[:, 1] + gt_boxes[:, 3]) / 2.0
    
    # Jarak Euclidean titik pusat (rho^2)
    rho_sq = (pred_cx - gt_cx)**2 + (pred_cy - gt_cy)**2
    
    # 3. Kotak penutup terkecil C
    c_x1 = torch.min(pred_boxes[:, 0], gt_boxes[:, 0])
    c_y1 = torch.min(pred_boxes[:, 1], gt_boxes[:, 1])
    c_x2 = torch.max(pred_boxes[:, 2], gt_boxes[:, 2])
    c_y2 = torch.max(pred_boxes[:, 3], gt_boxes[:, 3])
    c_diag_sq = (c_x2 - c_x1)**2 + (c_y2 - c_y1)**2 + 1e-7
    
    # DIoU = IoU - (rho^2 / c^2)
    diou = iou - (rho_sq / c_diag_sq)
    return (1.0 - diou).mean()
```

---

## 3. Rubrik Penilaian Praktikum
* **Perakitan Lapisan YOLO Head (30%)**: Ketepatan manipulasi bentuk tensor (*view, permute*) berdimensi tinggi di PyTorch.
* **Logika Dekoding Bounding Box (35%)**: Implementasi matematis sigmoid dan eksponensial offset terverifikasi benar.
* **Visualisasi & Interpretasi (20%)**: Menampilkan proyeksi spasial bounding box pada grid koordinat citra dengan tepat.
* **Kualitas Kode & Standar Rekayasa (15%)**: Kode bebas galat, efisien secara komputasi, dan terdokumentasi dengan baik.
"""

validate_text(guide_12_7, "AI_Modul_12.7_Panduan_Instruktur_dan_Kunci_Solusi.md")
with open("instructor_resources/part-12/AI_Modul_12.7_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_12_7)

print("[OK] Selesai Modul 12.7!")

# ==============================================================================
# MODUL 12.8: SINGLE SHOT DETECTOR (SSD)
# ==============================================================================

doc_12_8 = r"""# AI Modul 12.8: Single Shot Detector (SSD)

## 1. Peta Konsep & Orientasi Pembelajaran

Dalam perkembangan arsitektur deteksi objek satu tahap (*single-stage detectors*), **Single Shot MultiBox Detector (SSD)**, yang dirumuskan oleh Liu et al. (2016), meletakkan salah satu pilar konseptual paling penting: **deteksi fitur piramidal multi-skala (*multi-scale feature pyramid detection*)**. Sebelum hadirnya SSD, detektor satu tahap awal (seperti YOLOv1) memproyeksikan seluruh deteksi hanya dari satu lapisan keluaran terakhir yang telah mengalami resolusi penyusutan ekstrem ($32\times$ downsampling), yang mengakibatkan kegagalan total dalam mendeteksi objek-objek kecil.

SSD mengatasi kelemahan tersebut dengan mengekstrak prediksi deteksi secara simultan dari **berbagai lapisan konvolusi pada kedalaman yang berbeda**. Lapisan-lapisan awal yang beresolusi tinggi ($38 \times 38$ dan $19 \times 19$) bertanggung jawab mendeteksi objek-objek berukuran mikro, sedangkan lapisan-lapisan dalam beresolusi rendah ($5 \times 5$ dan $1 \times 1$) bertanggung jawab mendeteksi objek-objek berukuran besar. Dalam domain pertanian presisi—seperti deteksi serangga hama kumbang badak (*Oryctes rhinoceros*) pada daun sawit berdampingan dengan deteksi kanopi pohon secara utuh—konsep piramida fitur SSD menjadi dasar dari arsitektur modern seperti *Feature Pyramid Network* (FPN) dan *RetinaNet*.

```mermaid
flowchart TD
    A["Citra Masukan 300 x 300 x 3"] --> B["Base Network (VGG-16 Truncated)"]
    B --> C["Conv4_3 (38 x 38 x 512) -> Prediksi Objek Sangat Kecil"]
    B --> D["Conv7 (19 x 19 x 1024) -> Prediksi Objek Kecil"]
    D --> E["Conv8_2 (10 x 10 x 512) -> Prediksi Objek Sedang"]
    E --> F["Conv9_2 (5 x 5 x 256) -> Prediksi Objek Besar"]
    F --> G["Conv10_2 (3 x 3 x 256) & Conv11_2 (1 x 1 x 256) -> Objek Sangat Besar"]
    C & D & E & F & G --> H["Penggabungan 8.732 Default Bounding Boxes"]
    H --> I["Hard Negative Mining (Rasio Negatif:Positif = 3:1)"]
    I --> J["Deteksi Akurat Seluruh Spektrum Ukuran Objek"]
```

Tujuan instruksional Modul 12.8 ini meliputi:
1. Memahami arsitektur piramida fitur multi-resolusi SSD dan perancangan kotak acuan bawaan (*default boxes / prior boxes*).
2. Menguasai strategi pencocokan kotak (*matching strategy*) berbasis ambang batas Jaccard / IoU.
3. Memahami formulasi matematis *Hard Negative Mining* untuk menyeimbangkan disparitas ekstrem antara sampel latar belakang dan objek.
4. Menurunkan fungsi kerugian gabungan *MultiBox Loss* (Smooth L1 untuk regresi dan Softmax Cross-Entropy untuk klasifikasi).
5. Mengimplementasikan generator kotak default dan mekanisme inferensi multi-skala pada dataset hama perkebunan.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Multi-Scale Feature Maps dan Perancangan Default Boxes

SSD menggunakan $m$ lapisan peta fitur konvolusional untuk memprediksi deteksi. Skala kotak default $s_k$ untuk peta fitur ke-$k$ dirumuskan secara linear:

$$s_k = s_{\min} + \frac{s_{\max} - s_{\min}}{m - 1} (k - 1), \quad k \in \{1, \dots, m\}$$

Dimana $s_{\min} = 0.2$ (skala terkecil mencakup 20% ukuran citra) dan $s_{\max} = 0.9$ (skala terbesar mencakup 90% ukuran citra).

Untuk setiap lapisan fitur, digunakan sekumpulan rasio aspek $a_r \in \{1, 2, 3, \frac{1}{2}, \frac{1}{3}\}$. Dimensi lebar ($w_k^a$) dan tinggi ($h_k^a$) kotak default dihitung melalui:

$$w_k^a = s_k \sqrt{a_r}, \quad h_k^a = \frac{s_k}{\sqrt{a_r}}$$

Khusus untuk rasio aspek $a_r = 1$, ditambahkan satu kotak ekstra dengan skala geometrik:

$$s'_k = \sqrt{s_k s_{k+1}}$$

Sehingga setiap lokasi sel fitur memprediksi 4 atau 6 kotak default. Pada model standar SSD300 (masukan $300 \times 300$), total kotak default yang dievaluasi adalah:

$$38^2 \times 4 + 19^2 \times 6 + 10^2 \times 6 + 5^2 \times 6 + 3^2 \times 4 + 1^2 \times 4 = 5776 + 2166 + 600 + 150 + 36 + 4 = \mathbf{8.732} \text{ kotak}$$

### 2.2 Strategi Pencocokan dan Hard Negative Mining

Selama fase pelatihan, setiap kotak ground truth dipasangkan dengan kotak default yang memiliki IoU tertinggi, kemudian setiap kotak default yang memiliki $\text{IoU} \ge 0.5$ terhadap kotak ground truth mana pun ditetapkan sebagai **sampel positif**.

Dari 8.732 kotak, biasanya hanya 10-50 kotak yang berstatus positif, sementara sisanya adalah **sampel negatif (latar belakang kosong)**. Disparitas ekstrem ini (rasio $> 100:1$) dapat merusak kestabilan gradien.

**Solusi Hard Negative Mining**:
Kotak-kotak negatif diurutkan berdasarkan nilai kerugian keyakinan (*confidence loss*) tertinggi (sampel negatif yang paling membingungkan model). Hanya diambil sampel negatif teratas dengan rasio maksimum terhadap sampel positif:

$$\frac{N_{\text{neg}}}{N_{\text{pos}}} \le 3$$

Strategi ini mempercepat konvergensi dan menghasilkan akurasi klasifikasi latar belakang yang jauh lebih tangguh.

### 2.3 Formulasi Kerugian Gabungan (MultiBox Loss)

Fungsi kerugian terbobot SSD didefinisikan sebagai:

$$\mathcal{L}(x, c, l, g) = \frac{1}{N} \left( \mathcal{L}_{\text{conf}}(x, c) + \alpha \mathcal{L}_{\text{loc}}(x, l, g) \right)$$

Dimana $N$ adalah jumlah kotak default positif yang cocok. Jika $N = 0$, loss diatur ke 0.

1. **Confidence Loss $\mathcal{L}_{\text{conf}}$**:
Cross-Entropy multi-kelas atas probabilitas kelas yang diprediksi $c$:

$$\mathcal{L}_{\text{conf}}(x, c) = - \sum_{i \in \text{Pos}}^N x_{ij}^p \log(\hat{c}_i^p) - \sum_{i \in \text{Neg}} \log(\hat{c}_i^0)$$

2. **Localization Loss $\mathcal{L}_{\text{loc}}$**:
Regresi Smooth L1 antara offset kotak prediksi $l$ dan kotak ground truth $g$ terhadap kotak default $d$:

$$\mathcal{L}_{\text{loc}}(x, l, g) = \sum_{i \in \text{Pos}}^N \sum_{m \in \{cx, cy, w, h\}} x_{ij}^k \text{Smooth}_{L1}(l_i^m - \hat{g}_j^m)$$

$$\text{Smooth}_{L1}(u) = \begin{cases} 0.5 u^2, & \text{jika } |u| < 1 \\ |u| - 0.5, & \text{lainnya} \end{cases}$$

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Arsitektur Single Shot MultiBox Detector (SSD)](../../docs/assets/arsitektur_single_shot_detector_ssd_multiscale.png)

Diagram di atas mengilustrasikan:
1. **Base Network Truncated**: Ekstraksi representasi dasar citra.
2. **Piramida Multi-Skala**: Dari resolusi tinggi $38 \times 38$ (Conv4_3) hingga resolusi terkompresi $1 \times 1$ (Conv11_2).
3. **Penggabungan 8.732 Kotak Default**: Prediksi paralel terdistribusi untuk mendeteksi objek dari skala piksel mikro hingga makro.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi komputasi pembuatan kotak acuan default (*Default Boxes Generator*) dan algoritma *Hard Negative Mining* berbasis PyTorch:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from typing import List, Tuple

class SSDDefaultBoxesGenerator:
    '''
    Generator Kotak Acuan Default (Prior Boxes) Multi-Skala Berstandar SSD300.
    '''
    def __init__(self, img_size: int = 300):
        self.img_size = img_size
        self.feature_maps = [38, 19, 10, 5, 3, 1]
        self.steps = [8, 16, 32, 64, 100, 300]
        self.min_sizes = [30, 60, 111, 162, 213, 264]
        self.max_sizes = [60, 111, 162, 213, 264, 315]
        self.aspect_ratios = [[2], [2, 3], [2, 3], [2, 3], [2], [2]]
        
    def generate(self) -> torch.Tensor:
        boxes = []
        for k, f_k in enumerate(self.feature_maps):
            step = self.steps[k]
            for i in range(f_k):
                for j in range(f_k):
                    cx = (j + 0.5) * step / self.img_size
                    cy = (i + 0.5) * step / self.img_size
                    
                    # Kotak rasio 1 (ukuran min)
                    s_k = self.min_sizes[k] / self.img_size
                    boxes.append([cx, cy, s_k, s_k])
                    
                    # Kotak rasio 1 ekstra (ukuran geometrik)
                    s_prime = math.sqrt(s_k * (self.max_sizes[k] / self.img_size))
                    boxes.append([cx, cy, s_prime, s_prime])
                    
                    # Kotak dengan berbagai rasio aspek
                    for ar in self.aspect_ratios[k]:
                        w = s_k * math.sqrt(ar)
                        h = s_k / math.sqrt(ar)
                        boxes.append([cx, cy, w, h])
                        boxes.append([cx, cy, h, w])
                        
        return torch.tensor(boxes, dtype=torch.float32) # (Total Boxes, 4)

def hard_negative_mining(conf_loss: torch.Tensor, pos_mask: torch.Tensor, neg_pos_ratio: int = 3) -> torch.Tensor:
    '''
    Penyaringan sampel negatif berdasarkan tingkat loss tertinggi.
    conf_loss: Tensor (Batch, Num_Boxes) nilai cross-entropy per kotak
    pos_mask: Tensor Boolean (Batch, Num_Boxes)
    return: Tensor Boolean neg_mask yang terpilih
    '''
    num_pos = pos_mask.long().sum(dim=1, keepdim=True)
    num_neg = torch.clamp(num_pos * neg_pos_ratio, min=1)
    
    # Abaikan loss sampel positif dengan memberi nilai -inf
    conf_loss_neg = conf_loss.clone()
    conf_loss_neg[pos_mask] = -float('inf')
    
    # Urutkan dari loss terbesar
    _, indices = conf_loss_neg.sort(dim=1, descending=True)
    _, rank = indices.sort(dim=1)
    
    neg_mask = rank < num_neg
    return neg_mask
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Deteksi Serangan Kumbang Badak (*Oryctes rhinoceros*) pada Tanaman Kelapa Sawit Belum Menghasilkan (TBM)

Kumbang badak (*Oryctes rhinoceros*) adalah hama pemakan pucuk daun muda kelapa sawit yang paling destruktif pada fase TBM (umur 1-3 tahun). Kumbang dewasa mengebor pangkal pupus daun, menyebabkan daun muda patah berbentuk huruf "V" yang khas.

**Tantangan Deteksi Citra**:
Pada citra kanopi utuh beresolusi tinggi yang diambil dari kamera tiang pemantau:
1. Lubang gerekan kumbang berukuran sangat kecil (hanya $15 \times 15$ piksel pada citra).
2. Pucuk daun yang patah berukuran sedang ($120 \times 80$ piksel).
3. Seluruh tajuk tanaman berukuran besar ($400 \times 400$ piksel).

**Keunggulan Solusi SSD**:
* Lapisan fitur resolusi tinggi SSD (Conv4_3) mampu melokalisasi lubang gerekan mikro yang biasanya hilang pada detektor resolusi tunggal.
* Lapisan fitur menengah dan dalam (Conv8_2 dan Conv10_2) secara simultan mengonfirmasi orientasi patahan pelepah huruf "V" pada konteks tajuk tanaman utuh.
* Sistem menghasilkan akurasi deteksi dini serangan kumbang sebesar **92.6%**, memungkinkan aplikasi insektisida presisi terfokus hanya pada pohon yang terserang.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Perbandingan karakteristik operasional SSD terhadap detektor lainnya:

| Metrik Evaluasi | Faster R-CNN (ResNet-50) | YOLOv4 | SSD300 (VGG-16) | SSD512 (VGG-16) |
| :--- | :--- | :--- | :--- | :--- |
| **Tipe Paradigma** | Two-Stage | Single-Stage | Single-Stage | Single-Stage |
| **Total Anchor / Default Boxes** | ~2.000 (setelah RPN) | ~22.000 (Multi-scale) | 8.732 | 24.564 |
| **Kecepatan Inferensi (FPS T4)** | ~18 FPS | ~65 FPS | ~46 FPS | ~22 FPS |
| **mAP (Pascal VOC 2007)** | 76.4% | 82.8% | 77.2% | 79.8% |
| **Sensitivitas Objek Mikro** | Tinggi | Sangat Tinggi | Cukup Tinggi | Tinggi |

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **Gradien Conv4_3 Meledak (Gradient Explosion)** | Nilai loss menjadi *NaN* di epoch awal pelatihan. | Conv4_3 memiliki skala norma aktivasi yang jauh lebih besar dibanding lapisan dalam lainnya karena letaknya dekat dengan stem. | Terapkan normalisasi L2 per kanal (*L2 Normalization Layer*) dengan parameter skala yang dapat dipelajari ($\gamma \approx 20$). |
| **Matching Collapse saat Training** | Tidak ada satu pun kotak default yang cocok dengan ground truth ($N = 0$). | Objek ground truth memiliki rasio aspek atau ukuran yang ekstrem di luar batas cakupan kotak default SSD. | Perkaya variasi rasio aspek kotak default dan tambahkan augmentasi *RandomExpand* / *RandomCrop* berbasis Jaccard overlap. |
| **Hard Negative Mining Mengabaikan Positif** | Akurasi klasifikasi latar belakang tinggi tetapi recall objek mendekati nol. | Masking sampel positif keliru sehingga kotak positif ikut tertekan dalam penapisan negatif. | Pastikan `pos_mask` diterapkan secara ketat sebelum perankingan loss negatif (`conf_loss_neg[pos_mask] = -inf`). |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Kalkulasi Kotak Default**: Hitung jumlah kotak default yang dihasilkan oleh lapisan fitur ke-3 ($10 \times 10$) pada SSD300 jika setiap sel memiliki 6 rasio aspek.
   * *Solusi*:
     * Luas spasial: $10 \times 10 = 100$ sel.
     * Kotak per sel: 6 kotak.
     * Total kotak lapisan ke-3: $100 \times 6 = \mathbf{600} \text{ kotak default}$.

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual)**: Mengapa arsitektur SSD menghentikan penggunaan *Fully-Connected layers* dari backbone VGG-16 dan menggantinya dengan lapisan konvolusional murni? Jelaskan dampaknya terhadap kecepatan inferensi dan fleksibilitas resolusi masukan.
2. **Soal 2 (Komputasional)**: Rancang modul PyTorch `L2Norm` yang menormalisasi setiap vektor aktivasi spasial pada lapisan Conv4_3 sepanjang dimensi kanal dan mengalikannya dengan parameter bobot skalar terpelajari $\gamma$.

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 12.9: Faster R-CNN

Kita telah menuntaskan pembahasan detektor satu tahap berkecepatan tinggi: YOLO (Modul 12.7) dan SSD (Modul 12.8). Namun, dalam aplikasi medis, inspeksi kegagalan struktur mekanis pabrik, atau pemetaan ilmiah di mana **presisi batas koordinat dan minimasi False Positive** jauh lebih krusial daripada sekadar kecepatan frame tinggi, pendekatan dua tahap (*two-stage*) tetap menjadi rujukan utama.

Pada **AI Modul 12.9: Faster R-CNN (Regions with Convolutional Neural Networks)**, kita akan membedah arsitektur dua tahap terpopuler: mekanisme kerja *Region Proposal Network* (RPN), penyelarasan fitur kuantisasi halus melalui *RoIAlign*, dan integrasi *multi-task loss head*.

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Liu, W., et al. (2016). *SSD: Single shot multibox detector*. European Conference on Computer Vision (ECCV), 21-37.
2. Lin, T. Y., Dollár, P., Girshick, R., He, K., Hariharan, B., & Belongie, S. (2017). *Feature pyramid networks for object detection*. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2117-2125.
3. Redmon, J., & Farhadi, A. (2018). *YOLOv3: An incremental improvement*. arXiv preprint arXiv:1804.02767.
4. Girshick, R. (2015). *Fast R-CNN*. Proceedings of the IEEE International Conference on Computer Vision (ICCV), 1440-1448.
5. Howard, A. G., et al. (2017). *MobileNets: Efficient convolutional neural networks for mobile vision applications*. arXiv preprint arXiv:1704.04861.
"""

validate_text(doc_12_8, "AI_Modul_12.8_Single_Shot_Detector_(SSD).md")
with open("docs/part-12/AI_Modul_12.8_Single_Shot_Detector_(SSD).md", "w", encoding="utf-8") as f:
    f.write(doc_12_8)

# Notebook 12.8
nb_12_8_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 12.8: Praktikum Single Shot MultiBox Detector (SSD)\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Membangun generator Kotak Acuan Default (*Default Boxes*) multi-skala berstandar SSD300.\n",
            "2. Mengimplementasikan algoritma *Hard Negative Mining* untuk mengatasi ketidakseimbangan kelas latar belakang.\n",
            "3. Memvisualisasikan distribusi spasial kotak default pada piramida fitur resolusi berbeda."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import torch\n",
            "import torch.nn as nn\n",
            "import numpy as np\n",
            "import math\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "import matplotlib.patches as patches\n",
            "\n",
            "torch.manual_seed(42)\n",
            "print(f\"PyTorch Versi: {torch.__version__}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Implementasi Generator Default Boxes SSD300"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class SSDDefaultBoxesGenerator:\n",
            "    def __init__(self, img_size=300):\n",
            "        self.img_size = img_size\n",
            "        self.feature_maps = [38, 19, 10, 5, 3, 1]\n",
            "        self.steps = [8, 16, 32, 64, 100, 300]\n",
            "        self.min_sizes = [30, 60, 111, 162, 213, 264]\n",
            "        self.max_sizes = [60, 111, 162, 213, 264, 315]\n",
            "        self.aspect_ratios = [[2], [2, 3], [2, 3], [2, 3], [2], [2]]\n",
            "        \n",
            "    def generate(self):\n",
            "        boxes = []\n",
            "        for k, f_k in enumerate(self.feature_maps):\n",
            "            step = self.steps[k]\n",
            "            for i in range(f_k):\n",
            "                for j in range(f_k):\n",
            "                    cx = (j + 0.5) * step / self.img_size\n",
            "                    cy = (i + 0.5) * step / self.img_size\n",
            "                    \n",
            "                    s_k = self.min_sizes[k] / self.img_size\n",
            "                    boxes.append([cx, cy, s_k, s_k])\n",
            "                    \n",
            "                    s_prime = math.sqrt(s_k * (self.max_sizes[k] / self.img_size))\n",
            "                    boxes.append([cx, cy, s_prime, s_prime])\n",
            "                    \n",
            "                    for ar in self.aspect_ratios[k]:\n",
            "                        w = s_k * math.sqrt(ar)\n",
            "                        h = s_k / math.sqrt(ar)\n",
            "                        boxes.append([cx, cy, w, h])\n",
            "                        boxes.append([cx, cy, h, w])\n",
            "                        \n",
            "        return torch.tensor(boxes, dtype=torch.float32)\n",
            "\n",
            "gen = SSDDefaultBoxesGenerator(img_size=300)\n",
            "default_boxes = gen.generate()\n",
            "print(f\"Total Default Boxes SSD300: {len(default_boxes):,} kotak\")\n",
            "assert len(default_boxes) == 8732, f\"Jumlah kotak salah: {len(default_boxes)}\"\n",
            "print(\"[VALIDASI SUKSES] 8.732 Kotak Default SSD300 tergenerasi sempurna!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Implementasi Algoritma Hard Negative Mining"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def hard_negative_mining(conf_loss, pos_mask, neg_pos_ratio=3):\n",
            "    num_pos = pos_mask.long().sum(dim=1, keepdim=True)\n",
            "    num_neg = torch.clamp(num_pos * neg_pos_ratio, min=1)\n",
            "    \n",
            "    conf_loss_neg = conf_loss.clone()\n",
            "    conf_loss_neg[pos_mask] = -float('inf')\n",
            "    \n",
            "    _, indices = conf_loss_neg.sort(dim=1, descending=True)\n",
            "    _, rank = indices.sort(dim=1)\n",
            "    \n",
            "    neg_mask = rank < num_neg\n",
            "    return neg_mask\n",
            "\n",
            "# Simulasi batch berukuran 2 dengan 8.732 kotak\n",
            "mock_conf_loss = torch.rand(2, 8732)\n",
            "mock_pos_mask = torch.zeros(2, 8732, dtype=torch.bool)\n",
            "# Misalkan hanya ada 10 kotak positif per citra\n",
            "mock_pos_mask[0, :10] = True\n",
            "mock_pos_mask[1, :15] = True\n",
            "\n",
            "selected_neg_mask = hard_negative_mining(mock_conf_loss, mock_pos_mask, neg_pos_ratio=3)\n",
            "print(f\"Batch 0: Positif={mock_pos_mask[0].sum().item()}, Negatif Terpilih={selected_neg_mask[0].sum().item()} (Rasio 1:3)\")\n",
            "print(f\"Batch 1: Positif={mock_pos_mask[1].sum().item()}, Negatif Terpilih={selected_neg_mask[1].sum().item()} (Rasio 1:3)\")\n",
            "assert selected_neg_mask[0].sum().item() == 30, \"Sampling negatif gagal!\"\n",
            "print(\"[VALIDASI SUKSES] Hard Negative Mining menyeimbangkan rasio 3:1 secara presisi!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Visualisasi Kotak Default pada Peta Fitur Resolusi Berbeda"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, ax = plt.subplots(figsize=(6, 6))\n",
            "ax.set_xlim(0, 1)\n",
            "ax.set_ylim(1, 0) # Invert Y\n",
            "\n",
            "# Kotak dari Lapisan Resolusi Tinggi (Conv4_3, k=0) -> Kecil (Biru)\n",
            "b_small = default_boxes[0].numpy()\n",
            "rect_s = patches.Rectangle((b_small[0]-b_small[2]/2, b_small[1]-b_small[3]/2), b_small[2], b_small[3],\n",
            "                          linewidth=2, edgecolor='blue', facecolor='none')\n",
            "ax.add_patch(rect_s)\n",
            "ax.text(b_small[0]-b_small[2]/2, b_small[1]-b_small[3]/2-0.02, \"Conv4_3 (Objek Mikro)\", color='blue', fontsize=8)\n",
            "\n",
            "# Kotak dari Lapisan Resolusi Menengah (Conv8_2, k=2) -> Sedang (Hijau)\n",
            "idx_mid = 5776 + 2166 + 300\n",
            "b_mid = default_boxes[idx_mid].numpy()\n",
            "rect_m = patches.Rectangle((b_mid[0]-b_mid[2]/2, b_mid[1]-b_mid[3]/2), b_mid[2], b_mid[3],\n",
            "                          linewidth=2, edgecolor='green', facecolor='none')\n",
            "ax.add_patch(rect_m)\n",
            "ax.text(b_mid[0]-b_mid[2]/2, b_mid[1]-b_mid[3]/2-0.02, \"Conv8_2 (Objek Sedang)\", color='green', fontsize=8)\n",
            "\n",
            "# Kotak dari Lapisan Resolusi Rendah (Conv11_2, k=5) -> Besar (Merah)\n",
            "b_large = default_boxes[-1].numpy()\n",
            "rect_l = patches.Rectangle((b_large[0]-b_large[2]/2, b_large[1]-b_large[3]/2), b_large[2], b_large[3],\n",
            "                          linewidth=2, edgecolor='red', facecolor='none')\n",
            "ax.add_patch(rect_l)\n",
            "ax.text(b_large[0]-b_large[2]/2, b_large[1]-b_large[3]/2-0.02, \"Conv11_2 (Objek Makro)\", color='red', fontsize=8)\n",
            "\n",
            "plt.title('Cakupan Skala Kotak Acuan Default SSD Multi-Resolusi')\n",
            "plt.grid(True, linestyle='--', alpha=0.5)\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_ssd_default_boxes_coverage_12_8.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Grafik cakupan disimpan sebagai 'praktikum_ssd_default_boxes_coverage_12_8.png'\")"
        ]
    }
]

with open("notebooks/part-12/AI_Modul_12.8_Praktikum_Single_Shot_Detector_(SSD).ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_12_8_cells), f, indent=2)
print("[OK] Generated notebooks/part-12/AI_Modul_12.8_Praktikum_Single_Shot_Detector_(SSD).ipynb")

# Guide 12.8
guide_12_8 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 12.8 - Single Shot Detector (SSD)

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Konsep dasar Multi-Scale Feature Maps dan perancangan kotak acuan default (*Default Boxes*).
* **Menit 35 - 65**: Strategi pencocokan Jaccard IoU dan mekanisme Hard Negative Mining (rasio 3:1).
* **Menit 65 - 100**: Praktikum komputer: Implementasi generator 8.732 kotak default SSD300 dan seleksi sampel negatif di PyTorch.
* **Menit 100 - 130**: Studi kasus deteksi hama kumbang badak (*Oryctes rhinoceros*) pada tanaman sawit fase TBM.
* **Menit 130 - 150**: Pembahasan normalisasi L2 pada lapisan Conv4_3 dan kuis komparasi SSD vs YOLO.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Penggantian Fully-Connected VGG pada SSD)
* Lapisan Fully-Connected (FC) asli VGG-16 mengunci dimensi citra masukan pada resolusi kaku ($224 \times 224$), menyerap lebih dari 100 juta parameter, dan menghancurkan topologi spasial 2D menjadi 1D.
* SSD mengonversi FC6 dan FC7 menjadi lapisan konvolusional murni (Conv6 dan Conv7):
  1. Mengurangi parameter model secara drastis dari 138 juta menjadi ~26 juta.
  2. Memungkinkan jaringan menerima dimensi citra fleksibel ($300 \times 300$ atau $512 \times 512$).
  3. Mempertahankan resolusi spasial untuk diekstraksi lebih lanjut ke lapisan piramida berikutnya.

### Solusi Soal Mandiri 2 (Modul L2 Normalization PyTorch)
```python
import torch
import torch.nn as nn

class L2Norm(nn.Module):
    def __init__(self, num_channels, scale=20.0):
        super().__init__()
        self.num_channels = num_channels
        self.gamma = nn.Parameter(torch.Tensor(num_channels))
        self.reset_parameters(scale)
        self.eps = 1e-10
        
    def reset_parameters(self, scale):
        nn.init.constant_(self.gamma, scale)
        
    def forward(self, x):
        # x: Tensor (Batch, Channels, H, W)
        norm = x.pow(2).sum(dim=1, keepdim=True).sqrt() + self.eps
        x = torch.div(x, norm)
        # Reshape gamma untuk per-channel scaling
        out = self.gamma.unsqueeze(0).unsqueeze(2).unsqueeze(3) * x
        return out

# Uji tensor Conv4_3 (N, 512, 38, 38)
conv4_3_feat = torch.randn(2, 512, 38, 38) * 50.0 # Aktivasi besar
l2_norm = L2Norm(512, scale=20.0)
out_norm = l2_norm(conv4_3_feat)
print(f"Norma kanal setelah normalisasi: {out_norm[:, :, 0, 0].norm(dim=1)}") # Bernilai ~20.0
```

---

## 3. Rubrik Penilaian Praktikum
* **Kebenaran Formulasi Default Boxes (35%)**: Generator menghasilkan tepat 8.732 kotak berdimensi dan berpusat benar.
* **Implementasi Hard Negative Mining (35%)**: Logika pengurutan loss dan perankingan menghasilkan rasio presisi 3:1.
* **Visualisasi Piramida Fitur (15%)**: Representasi visual memperlihatkan rentang skala kotak mikro hingga makro dengan jelas.
* **Kualitas Kode & Standar Rekayasa (15%)**: Struktur kode modular, efisien secara komputasi, dan terdokumentasi dengan baik.
"""

validate_text(guide_12_8, "AI_Modul_12.8_Panduan_Instruktur_dan_Kunci_Solusi.md")
with open("instructor_resources/part-12/AI_Modul_12.8_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_12_8)

print("[OK] Selesai Modul 12.8!")
