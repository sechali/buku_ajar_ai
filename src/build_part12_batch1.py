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
    nb = {
        "cells": cells,
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
    return nb

# ==============================================================================
# MODUL 12.1: CONVOLUTIONAL NEURAL NETWORK (CNN)
# ==============================================================================

doc_12_1 = r"""# AI Modul 12.1: Convolutional Neural Network (CNN)

## 1. Peta Konsep & Orientasi Pembelajaran

Convolutional Neural Network (CNN) adalah pilar fundamental dalam visi komputer modern yang dirancang khusus untuk memproses data berstruktur kisi (*grid-structured data*), seperti citra digital dua dimensi ($H \times W \times C$). Sebelum hadirnya CNN, pendekatan *Multi-Layer Perceptron* (MLP) konvensional mengharuskan perataan citra (*flattening*) menjadi satu dimensi panjang ($H \cdot W \cdot C$), yang mengakibatkan dua malapetaka komputasi: kehancuran relasi spasial antar-piksel tetangga (*spatial topology destruction*) dan ledakan kombinatorial jumlah bobot parameter yang memicu *overfitting* ekstrem.

CNN merevolusi paradigma pemrosesan visual melalui tiga prinsip komputasi fundamental: **pembagian bobot (*weight sharing*)**, **konektivitas lokal (*sparse/local connectivity*)**, dan **invariansi pergeseran (*translation equivariance*)**. Dalam sektor agroindustri dan bioinformatika modern—seperti pemilahan otomatis tandan buah segar (TBS) kelapa sawit, deteksi hawar daun (*leaf blight*), hingga estimasi luas kanopi hutan tanaman industri melalui drone—CNN bertindak sebagai mesin ekstraksi hierarki visual otomatis yang mampu mengubah piksel mentah menjadi representasi semantik berdaya pisah tinggi.

```mermaid
flowchart TD
    A["Citra Masukan H x W x C"] --> B["Lapisan Konvolusi 2D (Conv2D)"]
    B --> C["Fungsi Aktivasi Non-Linear (ReLU / LeakyReLU)"]
    C --> D["Ekstraksi Hierarki Fitur (Low Level ke High Level)"]
    D --> E["Batch Normalization"]
    E --> F["Penurunan Dimensi Spasial (Subsampling)"]
    F --> G["Fully-Connected Classifier Head"]
    G --> H["Distribusi Probabilitas Kelas (Softmax)"]
```

Tujuan instruksional Modul 12.1 ini meliputi:
1. Memahami formulasi matematis diskrit operasi konvolusi 2D, mekanisme *cross-correlation*, peran *kernel/filter*, serta pengaruh *stride* dan *padding*.
2. Menguasai analisis pertumbuhan *receptive field* efektif sepanjang kedalaman lapisan jaringan.
3. Mengimplementasikan lapisan konvolusi secara manual berbasis operasi matriks murni NumPy serta pustaka `torch.nn.Conv2d` pada PyTorch.
4. Menganalisis efisiensi komputasi FLOPs (*Floating Point Operations*) dan konsumsi memori aktivasi konvolusi.
5. Membangun model CNN awal untuk klasifikasi citra bibit kelapa sawit sehat vs terinfeksi penyakit bercak daun *Curvularia*.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Formulasi Operasi Konvolusi Diskrit 2D dan Cross-Correlation

Dalam literatur matematika murni, operasi konvolusi antara citra masukan $I$ dan kernel $K$ berukuran $(2k+1) \times (2k+1)$ didefinisikan dengan membalik kernel (*kernel flipping*):

$$S(i, j) = (I * K)(i, j) = \sum_{m=-k}^{k} \sum_{n=-k}^{k} I(i - m, j - n) K(m, n)$$

Namun, dalam seluruh kerangka kerja *deep learning* modern (seperti PyTorch dan TensorFlow), operasi yang diimplementasikan secara komputasional adalah **korelasi silang (*cross-correlation*)** tanpa pembalikan kernel, karena kernel dipelajari secara dinamis melalui proses *backpropagation*:

$$O(i, j) = (I \star K)(i, j) = \sum_{m=-k}^{k} \sum_{n=-k}^{k} I(i + m, j + n) K(m, n)$$

Untuk citra masukan multi-kanal dengan dimensi $(C_{in}, H_{in}, W_{in})$ yang diproses oleh sekumpulan $C_{out}$ filter berukuran $(C_{in}, K_h, K_w)$, nilai aktivasi pada kanal keluaran ke-$c_{out}$ di koordinat $(i, j)$ sebelum fungsi aktivasi adalah:

$$O(c_{out}, i, j) = b(c_{out}) + \sum_{c_{in}=1}^{C_{in}} \sum_{m=0}^{K_h - 1} \sum_{n=0}^{K_w - 1} I(c_{in}, i \cdot S_h + m, j \cdot S_w + n) \cdot W(c_{out}, c_{in}, m, n)$$

Dimana:
* $W(c_{out}, c_{in}, m, n)$ adalah bobot tensor kernel berdimensi $(C_{out}, C_{in}, K_h, K_w)$.
* $b(c_{out})$ adalah skalar bias untuk kanal keluaran ke-$c_{out}$.
* $S_h, S_w$ adalah langkah pergeseran (*stride*) vertikal dan horizontal.

### 2.2 Relasi Dimensi Spasial (Spatial Output Dimension)

Ukuran spasial peta fitur keluaran ($H_{out}, W_{out}$) dikontrol secara ketat oleh dimensi masukan ($H_{in}, W_{in}$), ukuran kernel ($K$), *padding* ($P$), dan *stride* ($S$) melalui fungsi lantai (*floor function*):

$$H_{out} = \left\lfloor \frac{H_{in} - K_h + 2P_h}{S_h} \right\rfloor + 1$$

$$W_{out} = \left\lfloor \frac{W_{in} - K_w + 2P_w}{S_w} \right\rfloor + 1$$

Jika $S = 1$, kita dapat mempertahankan resolusi spasial yang identik (*same padding*) dengan memilih:

$$P = \frac{K - 1}{2} \quad (\text{untuk } K \text{ bernilai ganjil})$$

### 2.3 Analisis Receptive Field

*Receptive Field* ($RF$) adalah area spasial pada citra masukan asli yang memengaruhi nilai aktivasi neuron pada lapisan tertentu. Untuk lapisan ke-$l$, ukuran *receptive field* efektif $RF_l$ dapat dihitung secara rekursif:

$$RF_l = RF_{l-1} + (K_l - 1) \cdot J_{l-1}$$

$$J_l = J_{l-1} \cdot S_l$$

Dimana:
* $RF_0 = 1$ (piksel tunggal pada citra masukan).
* $J_l$ adalah *jump* spasial kumulatif antar-fitur.
* $S_l$ adalah *stride* pada lapisan ke-$l$.

Formula ini membuktikan bahwa menumpuk dua lapisan konvolusi $3 \times 3$ ($S=1$) menghasilkan *receptive field* setara lapisan $5 \times 5$, namun hanya membutuhkan $2 \times (3^2) = 18$ bobot dibandingkan $1 \times (5^2) = 25$ bobot, dengan keuntungan tambahan berupa penyisipan fungsi non-linearitas ganda.

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Arsitektur dan Operasi Konvolusi CNN](../../docs/assets/arsitektur_dan_operasi_konvolusi_cnn.png)

Diagram di atas mengilustrasikan mekanisme konvolusi multi-kanal:
1. **Tensor Citra Masukan**: Berdimensi $(H \times W \times C)$, di mana setiap kanal warna diproses secara paralel oleh sub-filter terkait.
2. **Koleksi Filter/Kernel**: Melakukan pergeseran spasial (*sliding window*) dengan *stride* tertentu. Operasi perkalian titik (*dot product*) elemen-demi-elemen diakumulasikan sepanjang kedalaman kanal.
3. **Peta Fitur Keluaran (*Feature Map*)**: Menghasilkan representasi respons visual terhadap pola lokal (seperti orientasi gradien tepi, tekstur serat daun, atau pola bintik penyakit).

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lengkap konvolusi 2D: dari algoritma eksplisit berbasis NumPy untuk pemahaman mekanika dasar, hingga modul modular berbasis PyTorch berstandar produksi.

```python
import torch
import torch.nn as nn
import numpy as np

def conv2d_forward_numpy(X: np.ndarray, W: np.ndarray, b: np.ndarray, stride: int = 1, padding: int = 0) -> np.ndarray:
    '''
    Implementasi konvolusi 2D murni berbasis NumPy untuk verifikasi matematis.
    X: Input array dimensi (N, C_in, H, W)
    W: Kernel weights dimensi (C_out, C_in, Kh, Kw)
    b: Bias array dimensi (C_out,)
    '''
    N, C_in, H_in, W_in = X.shape
    C_out, _, Kh, Kw = W.shape
    
    H_out = int(np.floor((H_in - Kh + 2 * padding) / stride)) + 1
    W_out = int(np.floor((W_in - Kw + 2 * padding) / stride)) + 1
    
    X_pad = np.pad(X, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode='constant')
    out = np.zeros((N, C_out, H_out, W_out), dtype=np.float32)
    
    for n in range(N):
        for c_out in range(C_out):
            for i in range(H_out):
                h_start = i * stride
                h_end = h_start + Kh
                for j in range(W_out):
                    w_start = j * stride
                    w_end = w_start + Kw
                    
                    patch = X_pad[n, :, h_start:h_end, w_start:w_end]
                    out[n, c_out, i, j] = np.sum(patch * W[c_out]) + b[c_out]
                    
    return out

class AgroPalmLeafCNN(nn.Module):
    '''
    Arsitektur CNN Standar Industri untuk Deteksi Patologi Daun Bibit Kelapa Sawit.
    '''
    def __init__(self, num_classes: int = 2):
        super(AgroPalmLeafCNN, self).__init__()
        
        # Blok Ekstraksi Fitur 1
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.relu1 = nn.ReLU(inplace=True)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Blok Ekstraksi Fitur 2
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.relu2 = nn.ReLU(inplace=True)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Classifier Head
        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self.dropout = nn.Dropout(p=0.4)
        self.fc = nn.Linear(32, num_classes)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Resolusi input: (N, 3, 64, 64)
        x = self.pool1(self.relu1(self.bn1(self.conv1(x)))) # -> (N, 16, 32, 32)
        x = self.pool2(self.relu2(self.bn2(self.conv2(x)))) # -> (N, 32, 16, 16)
        x = self.gap(x)                                     # -> (N, 32, 1, 1)
        x = torch.flatten(x, 1)                             # -> (N, 32)
        x = self.dropout(x)
        logits = self.fc(x)                                 # -> (N, num_classes)
        return logits
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Inspeksi Otomatis Penyakit Bercak Daun (*Curvularia maculans*) pada Bibit Kelapa Sawit

Pada pembibitan kelapa sawit (*pre-nursery* dan *main-nursery*), serangan jamur *Curvularia maculans* memunculkan lesi nekrotik melingkar berdiameter 1-3 mm dengan halo kekuningan. Jika tidak diisolasi dalam waktu 48 jam, spora dapat menginfeksi seluruh petak pembibitan, menyebabkan penurunan vigor hingga 40%.

Pemeriksaan manual oleh mandor kebun memiliki kelemahan:
1. Kelelahan visual (*eye fatigue*) setelah menginspeksi lebih dari 500 bibit.
2. Variasi intensitas cahaya matahari tropis yang mengaburkan batas lesi nekrotik.

**Penyelesaian Rekayasa Berbasis CNN**:
* Menggunakan sensor kamera RGB beresolusi sedang ($640 \times 480$) yang dipasang pada portal *conveyor* pemindahan polybag.
* CNN mengekstrak filter tepi pada lapisan pertama untuk menangkap batas lesi yang tajam, kemudian mengombinasikannya pada lapisan kedua menjadi filter pola bintik sirkular berkontras tinggi (*texture pattern detector*).
* Model menghasilkan klasifikasi biner: Sehat (*Healthy*) vs Terinfeksi (*Infected*) dengan ambang batas keandalan $\tau = 0.85$.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

### 6.1 Kompleksitas Parameter dan FLOPs

Untuk satu lapisan konvolusi 2D standar tanpa bias:
* **Jumlah Parameter Bobot**:

$$P_{weights} = C_{out} \times C_{in} \times K_h \times K_w$$

* **Jumlah Parameter dengan Bias**:

$$P_{total} = C_{out} \times (C_{in} \times K_h \times K_w + 1)$$

* **Kompleksitas Komputasi (FLOPs)**:
Setiap piksel pada peta fitur keluaran membutuhkan $(2 \cdot C_{in} \cdot K_h \cdot K_w - 1)$ operasi perkalian dan penjumlahan. Total FLOPs lapisan konvolusi:

$$\text{FLOPs} \approx 2 \times H_{out} \times W_{out} \times (C_{in} \cdot K_h \cdot K_w) \times C_{out}$$

### 6.2 Konsumsi Memori Aktivasi (*Memory Footprint*)

Dalam fase pelatihan (*forward-pass*), setiap lapisan konvolusi harus menyimpan seluruh tensor peta fitur keluaran di VRAM GPU untuk komputasi gradien saat *backpropagation*:

$$\text{Memory}_{\text{act}} = N \times C_{out} \times H_{out} \times W_{out} \times 4 \text{ bytes (FP32)}$$

Sebagai contoh, jika ukuran batch $N = 64$, $C_{out} = 64$, $H_{out} = 128$, $W_{out} = 128$, maka memori aktivasi satu lapisan saja mencapai:

$$64 \times 64 \times 128 \times 128 \times 4 \approx 268.435.456 \text{ bytes} \approx 256 \text{ MB}$$

Hal ini menjelaskan mengapa *batch size* besar pada resolusi citra tinggi kerap memicu galat *CUDA Out of Memory* (OOM).

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **Grid Boundary Mismatch** | Galat runtime `RuntimeError: Calculated padded input size per channel: (H_out x W_out). Kernel size: (Kh x Kw). Kernel size can't be greater than actual input size` | Nilai *stride* terlalu besar atau *padding* kurang sehingga dimensi peta fitur mengecil hingga $< K$. | Gunakan formula dimensi eksplisit. Pilih *same padding* ($P = (K-1)/2$) dan verifikasi ukuran tensor dengan `print(x.shape)` di forward pass. |
| **Penyusutan Sudut Citra (*Border Degradation*)** | Akurasi deteksi objek di tepi citra merosot tajam dibandingkan di area tengah. | Penggunaan `padding=0` (*valid convolution*) yang mengabaikan informasi piksel di sepanjang batas tepi citra. | Terapkan *reflection padding* atau *replicate padding* jika informasi batas daun sangat esensial bagi diagnosis patologi. |
| **Dying ReLU pada Lapisan Konvolusi Awal** | 60-80% peta fitur menghasilkan matriks nol mutlak (*dead channels*). | *Learning rate* terlalu tinggi dikombinasikan dengan inisialisasi bobot yang buruk memicu gradien negatif masif. | Terapkan inisialisasi Kaiming He (`nn.init.kaiming_normal_`), sisipkan `BatchNorm2d`, atau beralih ke `LeakyReLU(negative_slope=0.01)`. |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Analisis Manual**: Hitung ukuran keluaran spasial ($H_{out}, W_{out}$) dan total parameter lapisan `nn.Conv2d(3, 64, kernel_size=5, stride=2, padding=2)` jika citra masukan berukuran $256 \times 256 \times 3$.
   * *Solusi*:
     $$H_{out} = \left\lfloor \frac{256 - 5 + 2(2)}{2} \right\rfloor + 1 = \left\lfloor \frac{255}{2} \right\rfloor + 1 = 127 + 1 = 128$$
     $$W_{out} = 128$$
     $$\text{Parameter} = 64 \times (3 \times 5 \times 5 + 1) = 64 \times 76 = 4.864 \text{ bobot}$$

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual)**: Buktikan secara matematis bahwa susunan tiga lapisan konvolusi $3 \times 3$ berurutan memiliki *receptive field* yang identik dengan satu lapisan konvolusi $7 \times 7$. Hitung rasio efisiensi jumlah parameter bobotnya jika kanal masuk dan keluar semuanya berjumlah $C$.
2. **Soal 2 (Komputasional)**: Buat modul PyTorch kustom `DepthwiseSeparableConv2d` yang membagi konvolusi standar menjadi *depthwise convolution* (`groups=C_in`) diikuti *pointwise convolution* ($1 \times 1$). Bandingkan penghematan FLOPs-nya terhadap konvolusi standar pada tensor berdimensi $128 \times 128 \times 64$.

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 12.2: Arsitektur CNN

Pada modul ini, kita telah menguasai operasi dasar konvolusi 2D, pembentukan *feature map*, dan perhitungan *receptive field*. Namun, menyusun lapisan-lapisan konvolusi menjadi sebuah arsitektur yang sangat dalam (*very deep networks*) memunculkan tantangan baru: degradasi performa dan lenyapnya gradien (*vanishing gradient*).

Pada **AI Modul 12.2: Arsitektur CNN**, kita akan membedah secara historis dan komparatif evolusi arsitektur legendaris dunia: **LeNet-5**, **AlexNet**, **VGG**, hingga terobosan revolusioner *residual learning* pada **ResNet**.

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). *Gradient-based learning applied to document recognition*. Proceedings of the IEEE, 86(11), 2278-2324.
2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning* (Chapter 9: Convolutional Networks). MIT Press.
3. Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). *ImageNet classification with deep convolutional neural networks*. Advances in Neural Information Processing Systems (NeurIPS 2012), 25, 1097-1105.
4. Paszke, A., et al. (2019). *PyTorch: An imperative style, high-performance deep learning library*. Advances in Neural Information Processing Systems (NeurIPS 2019), 32.
5. He, K., Zhang, X., Ren, S., & Sun, J. (2015). *Delving deep into rectifiers: Surpassing human-level performance on ImageNet classification*. Proceedings of the IEEE International Conference on Computer Vision (ICCV), 1026-1034.
"""

validate_text(doc_12_1, "AI_Modul_12.1_Convolutional_Neural_Network_(CNN).md")
with open("docs/part-12/AI_Modul_12.1_Convolutional_Neural_Network_(CNN).md", "w", encoding="utf-8") as f:
    f.write(doc_12_1)

# Notebook 12.1
nb_12_1_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 12.1: Praktikum Convolutional Neural Network (CNN)\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Membangun dan memverifikasi operasi konvolusi 2D secara matematis murni (NumPy).\n",
            "2. Mengembangkan arsitektur CNN modular menggunakan PyTorch (`torch.nn.Conv2d`, `BatchNorm2d`, `AdaptiveAvgPool2d`).\n",
            "3. Mensimulasikan dataset citra patologi bercak daun kelapa sawit (*Curvularia*) dan melatih model deteksi biner hingga konvergensi."
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
            "import torch.optim as optim\n",
            "from torch.utils.data import TensorDataset, DataLoader\n",
            "import numpy as np\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "# Reproducibility seed\n",
            "torch.manual_seed(42)\n",
            "np.random.seed(42)\n",
            "print(f\"PyTorch Version: {torch.__version__}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Verifikasi Numerik Konvolusi NumPy vs PyTorch"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def conv2d_numpy(X, W, b, stride=1, padding=0):\n",
            "    N, C_in, H_in, W_in = X.shape\n",
            "    C_out, _, Kh, Kw = W.shape\n",
            "    H_out = int(np.floor((H_in - Kh + 2 * padding) / stride)) + 1\n",
            "    W_out = int(np.floor((W_in - Kw + 2 * padding) / stride)) + 1\n",
            "    X_pad = np.pad(X, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode='constant')\n",
            "    out = np.zeros((N, C_out, H_out, W_out), dtype=np.float32)\n",
            "    for n in range(N):\n",
            "        for c in range(C_out):\n",
            "            for i in range(H_out):\n",
            "                for j in range(W_out):\n",
            "                    patch = X_pad[n, :, i*stride:i*stride+Kh, j*stride:j*stride+Kw]\n",
            "                    out[n, c, i, j] = np.sum(patch * W[c]) + b[c]\n",
            "    return out\n",
            "\n",
            "# Buat tensor uji\n",
            "X_np = np.random.randn(2, 3, 8, 8).astype(np.float32)\n",
            "W_np = np.random.randn(4, 3, 3, 3).astype(np.float32)\n",
            "b_np = np.random.randn(4).astype(np.float32)\n",
            "\n",
            "# Hasil NumPy\n",
            "out_np = conv2d_numpy(X_np, W_np, b_np, stride=1, padding=1)\n",
            "\n",
            "# Hasil PyTorch\n",
            "conv_torch = nn.Conv2d(3, 4, kernel_size=3, stride=1, padding=1)\n",
            "conv_torch.weight.data = torch.tensor(W_np)\n",
            "conv_torch.bias.data = torch.tensor(b_np)\n",
            "out_pt = conv_torch(torch.tensor(X_np)).detach().numpy()\n",
            "\n",
            "diff = np.max(np.abs(out_np - out_pt))\n",
            "print(f\"Selisih Absolut Maksimum NumPy vs PyTorch: {diff:.6e}\")\n",
            "assert diff < 1e-5, \"Implementasi konvolusi tidak cocok!\"\n",
            "print(\"[VALIDASI SUKSES] Logika konvolusi 2D konsisten secara numerik!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Sintesis Dataset Patologi Daun Kelapa Sawit\n",
            "Membuat 300 sampel citra sintetis ($3 \\times 64 \\times 64$):\n",
            "* Kelas 0: Daun Sehat (Hijau seragam dengan variasi tekstur serat alami).\n",
            "* Kelas 1: Daun Terinfeksi Bercak Daun (*Curvularia*) (Bercak nekrotik cokelat gelap dengan halo kuning)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def generate_palm_leaf_dataset(num_samples=300):\n",
            "    X = np.zeros((num_samples, 3, 64, 64), dtype=np.float32)\n",
            "    y = np.zeros(num_samples, dtype=np.int64)\n",
            "    \n",
            "    for i in range(num_samples):\n",
            "        # Latar daun hijau tropis\n",
            "        base_green = np.random.uniform(0.5, 0.8)\n",
            "        X[i, 0, :, :] = np.random.uniform(0.1, 0.25) # Kanal R (rendah)\n",
            "        X[i, 1, :, :] = base_green + np.random.normal(0, 0.05, (64, 64)) # Kanal G (tinggi)\n",
            "        X[i, 2, :, :] = np.random.uniform(0.1, 0.3) # Kanal B (rendah)\n",
            "        \n",
            "        if i >= num_samples // 2:\n",
            "            # Daun Sakit: Suntikkan bercak lesi nekrotik\n",
            "            y[i] = 1\n",
            "            num_spots = np.random.randint(3, 8)\n",
            "            for _ in range(num_spots):\n",
            "                cx, cy = np.random.randint(10, 54, size=2)\n",
            "                radius = np.random.randint(3, 7)\n",
            "                yy, xx = np.ogrid[:64, :64]\n",
            "                dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)\n",
            "                mask_spot = dist <= radius\n",
            "                # Lesi cokelat gelap / nekrotik\n",
            "                X[i, 0, mask_spot] = 0.45\n",
            "                X[i, 1, mask_spot] = 0.20\n",
            "                X[i, 2, mask_spot] = 0.05\n",
            "                \n",
            "    # Klip ke rentang valid [0, 1]\n",
            "    X = np.clip(X, 0.0, 1.0)\n",
            "    return torch.tensor(X), torch.tensor(y)\n",
            "\n",
            "X_all, y_all = generate_palm_leaf_dataset(400)\n",
            "# Bagi Train (80%) dan Validation (20%)\n",
            "train_ds = TensorDataset(X_all[:320], y_all[:320])\n",
            "val_ds = TensorDataset(X_all[320:], y_all[320:])\n",
            "\n",
            "train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)\n",
            "val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)\n",
            "print(f\"Dataset siap: Train = {len(train_ds)} sampel, Val = {len(val_ds)} sampel.\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Membangun dan Melatih Arsitektur CNN"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class AgroPalmCNN(nn.Module):\n",
            "    def __init__(self):\n",
            "        super(AgroPalmCNN, self).__init__()\n",
            "        self.features = nn.Sequential(\n",
            "            nn.Conv2d(3, 16, kernel_size=3, padding=1),\n",
            "            nn.BatchNorm2d(16),\n",
            "            nn.ReLU(inplace=True),\n",
            "            nn.MaxPool2d(2, 2),\n",
            "            \n",
            "            nn.Conv2d(16, 32, kernel_size=3, padding=1),\n",
            "            nn.BatchNorm2d(32),\n",
            "            nn.ReLU(inplace=True),\n",
            "            nn.MaxPool2d(2, 2)\n",
            "        )\n",
            "        self.classifier = nn.Sequential(\n",
            "            nn.AdaptiveAvgPool2d((1, 1)),\n",
            "            nn.Flatten(),\n",
            "            nn.Dropout(0.3),\n",
            "            nn.Linear(32, 2)\n",
            "        )\n",
            "        \n",
            "    def forward(self, x):\n",
            "        return self.classifier(self.features(x))\n",
            "\n",
            "model = AgroPalmCNN()\n",
            "criterion = nn.CrossEntropyLoss()\n",
            "optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)\n",
            "\n",
            "# Hitung parameter\n",
            "total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)\n",
            "print(f\"Total Parameter Model: {total_params:,}\")\n",
            "\n",
            "epochs = 10\n",
            "train_losses, val_accs = [], []\n",
            "\n",
            "for epoch in range(epochs):\n",
            "    model.train()\n",
            "    running_loss = 0.0\n",
            "    for batch_x, batch_y in train_loader:\n",
            "        optimizer.zero_grad()\n",
            "        outputs = model(batch_x)\n",
            "        loss = criterion(outputs, batch_y)\n",
            "        loss.backward()\n",
            "        optimizer.step()\n",
            "        running_loss += loss.item() * batch_x.size(0)\n",
            "        \n",
            "    epoch_loss = running_loss / len(train_loader.dataset)\n",
            "    train_losses.append(epoch_loss)\n",
            "    \n",
            "    # Evaluasi\n",
            "    model.eval()\n",
            "    correct = 0\n",
            "    with torch.no_grad():\n",
            "        for val_x, val_y in val_loader:\n",
            "            preds = model(val_x).argmax(dim=1)\n",
            "            correct += (preds == val_y).sum().item()\n",
            "    acc = correct / len(val_loader.dataset)\n",
            "    val_accs.append(acc)\n",
            "    \n",
            "    print(f\"Epoch [{epoch+1:02d}/{epochs}] - Loss: {epoch_loss:.4f} | Val Accuracy: {acc*100:.2f}%\")\n",
            "\n",
            "# Simpan plot metrik\n",
            "plt.figure(figsize=(10, 4))\n",
            "plt.subplot(1, 2, 1)\n",
            "plt.plot(train_losses, 'b-o', label='Training Loss')\n",
            "plt.title('Dinamika Konvergensi Loss')\n",
            "plt.xlabel('Epoch')\n",
            "plt.ylabel('Cross-Entropy Loss')\n",
            "plt.grid(True)\n",
            "\n",
            "plt.subplot(1, 2, 2)\n",
            "plt.plot(val_accs, 'g-s', label='Validation Accuracy')\n",
            "plt.title('Akurasi Validasi Model')\n",
            "plt.xlabel('Epoch')\n",
            "plt.ylabel('Akurasi')\n",
            "plt.grid(True)\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_cnn_convergence_12_1.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[SUKSES] Grafik konvergensi disimpan sebagai 'praktikum_cnn_convergence_12_1.png'\")"
        ]
    }
]

with open("notebooks/part-12/AI_Modul_12.1_Praktikum_Convolutional_Neural_Network.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_12_1_cells), f, indent=2)
print("[OK] Generated notebooks/part-12/AI_Modul_12.1_Praktikum_Convolutional_Neural_Network.ipynb")

# Guide 12.1
guide_12_1 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 12.1 - Convolutional Neural Network (CNN)

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Review keterbatasan MLP konvensional pada citra dan penjelasan 3 prinsip dasar CNN (weight sharing, sparse connectivity, equivariance).
* **Menit 30 - 60**: Penurunan matematis operasi konvolusi 2D, formula dimensi spasial, dan perhitungan receptive field bertingkat.
* **Menit 60 - 100**: Praktikum komputer: Verifikasi manual NumPy vs PyTorch `Conv2d`, pembangunan arsitektur CNN, dan penanganan tensor 4D.
* **Menit 100 - 130**: Studi kasus deteksi bercak daun bibit kelapa sawit (*Curvularia*) dan analisis kurva konvergensi.
* **Menit 130 - 150**: Pembahasan jebakan umum (grid boundary mismatch, border degradation) dan kuis formatif.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Bukti Matematis Receptive Field 3x (3x3) vs 1x (7x7))
* **Bukti Receptive Field**:
  * Lapisan 1 ($K=3, S=1$): $RF_1 = 3$. Jump $J_1 = 1$.
  * Lapisan 2 ($K=3, S=1$): $RF_2 = RF_1 + (3 - 1) \cdot 1 = 3 + 2 = 5$. Jump $J_2 = 1$.
  * Lapisan 3 ($K=3, S=1$): $RF_3 = RF_2 + (3 - 1) \cdot 1 = 5 + 2 = 7$.
  * Lapisan tunggal $7 \times 7$ memiliki $RF = 7$. Terbukti identik!
* **Rasio Efisiensi Parameter**:
  * Untuk 3 lapisan $3 \times 3$ dengan kanal $C$: $\text{Param} = 3 \times (C \times C \times 3 \times 3) = 27 C^2$.
  * Untuk 1 lapisan $7 \times 7$ dengan kanal $C$: $\text{Param} = 1 \times (C \times C \times 7 \times 7) = 49 C^2$.
  * **Rasio Penghematan**: $\frac{27 C^2}{49 C^2} \approx 0.551$ (Penghematan bobot mencapai **44.9%**).

### Solusi Soal Mandiri 2 (Depthwise Separable Convolution)
```python
import torch
import torch.nn as nn

class DepthwiseSeparableConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, padding=1):
        super().__init__()
        # Depthwise Conv: per-channel filtering
        self.depthwise = nn.Conv2d(in_channels, in_channels, kernel_size=kernel_size, 
                                   padding=padding, groups=in_channels, bias=False)
        # Pointwise Conv: 1x1 linear combination
        self.pointwise = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=True)
        
    def forward(self, x):
        return self.pointwise(self.depthwise(x))

# Verifikasi parameter
C_in, C_out = 64, 64
std_conv = nn.Conv2d(C_in, C_out, kernel_size=3, padding=1)
ds_conv = DepthwiseSeparableConv2d(C_in, C_out, kernel_size=3, padding=1)

p_std = sum(p.numel() for p in std_conv.parameters())
p_ds = sum(p.numel() for p in ds_conv.parameters())
print(f"Param Standard Conv: {p_std} | Depthwise Separable: {p_ds} | Rasio: {p_ds / p_std:.4f}")
# Output rasio sekitar ~0.113 (penghematan 88.7% parameter!)
```

---

## 3. Rubrik Penilaian Praktikum
* **Kebenaran Formulasi Numerik (30%)**: Implementasi konvolusi NumPy menghasilkan selisih absolut $< 10^{-5}$ terhadap PyTorch.
* **Arsitektur Jaringan (30%)**: Pemanfaatan `BatchNorm2d`, fungsi aktivasi non-linear, dan `AdaptiveAvgPool2d` yang tepat.
* **Performa Model & Pelatihan (25%)**: Model mencapai akurasi validasi $\ge 95\%$ pada data simulasi patologi daun sawit.
* **Analisis & Dokumentasi (15%)**: Analisis matematis FLOPs dan pemahaman komprehensif terhadap receptive field.
"""

validate_text(guide_12_1, "AI_Modul_12.1_Panduan_Instruktur_dan_Kunci_Solusi.md")
with open("instructor_resources/part-12/AI_Modul_12.1_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_12_1)

print("[OK] Selesai Modul 12.1!")
