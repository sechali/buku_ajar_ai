# Panduan Instruktur & Kunci Solusi: AI Modul 12.1 - Convolutional Neural Network (CNN)

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Review keterbatasan MLP konvensional pada citra dan penjelasan 3 prinsip dasar CNN (weight sharing, sparse connectivity, equivariance).
* **Menit 30 - 60**: Penurunan matematis operasi konvolusi 2D, formula dimensi spasial, dan perhitungan receptive field bertingkat.
* **Menit 60 - 100**: Praktikum komputer: Verifikasi manual NumPy vs PyTorch `Conv2d`, pembangunan arsitektur CNN, dan penanganan tensor 4D.
* **Menit 100 - 130**: Studi kasus deteksi bercak daun bibit kelapa sawit (*Curvularia*) dan analisis kurva konvergensi.
* **Menit 130 - 150**: Pembahasan potensi kekeliruan umum (grid boundary mismatch, border degradation) dan kuis formatif.

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
