# Panduan Instruktur & Kunci Solusi: AI Modul 12.3 - Pooling

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Konsep dasar subsampling spasial, perbedaan fungsional Max Pooling vs Average Pooling.
* **Menit 30 - 60**: Penurunan matematis aliran gradien saat backpropagation (argmax routing vs uniform distribution).
* **Menit 60 - 95**: Telaah mendalam Global Average Pooling (GAP) dan keunggulan eliminasi overfitting.
* **Menit 95 - 125**: Praktikum komputer: Verifikasi manual NumPy, uji invariansi translasi citra tajuk sawit, dan komparasi GAP vs Dense.
* **Menit 125 - 150**: Pembahasan potensi kendala teknis downsampling berlebih dan kuis evaluasi.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Strided Convolution vs Pooling pada GAN/Autoencoder)
* **Alasan Penggantian Pooling**:
  1. **Differentiable Spatial Resampling**: Lapisan pooling memiliki fungsi tetap yang tidak dapat dioptimasi dengan gradien, sedangkan *Strided Convolution* memiliki bobot kernel yang dipelajari secara dinamis (*learnable downsampling*).
  2. **Retensi Informasi Spasial Halus**: Pada Autoencoder dan GAN, diskriminator membutuhkan informasi frekuensi spasial tinggi untuk membedakan artefak buatan dari citra asli. Max pooling membuang 75% piksel secara diskontinu, memicu artefak catur (*checkerboard artifacts*) saat di-upsample kembali.

### Solusi Soal Mandiri 2 (Implementasi L2 Pooling)
```python
import torch
import torch.nn as nn

class L2Pooling2d(nn.Module):
    def __init__(self, kernel_size=2, stride=2, eps=1e-8):
        super().__init__()
        self.avg_pool = nn.AvgPool2d(kernel_size=kernel_size, stride=stride)
        self.eps = eps
        
    def forward(self, x):
        # L2-Norm = sqrt( AvgPool( x^2 ) )
        x_sq = torch.square(x)
        avg_sq = self.avg_pool(x_sq)
        return torch.sqrt(avg_sq + self.eps)

# Uji coba tensor acak (1, 1, 8, 8)
x = torch.randn(1, 1, 8, 8)
l2_pool = L2Pooling2d(kernel_size=2, stride=2)
max_pool = nn.MaxPool2d(kernel_size=2, stride=2)

out_l2 = l2_pool(x)
out_max = max_pool(x)
print(f"Output L2 Pool:  Mean={out_l2.mean():.4f}")
print(f"Output Max Pool: Mean={out_max.mean():.4f}")
```

---

## 3. Rubrik Penilaian Praktikum
* **Kebenaran Formulasi Numerik (30%)**: Implementasi pooling manual NumPy sesuai dengan hasil PyTorch.
* **Pengujian Invariansi Translasi (30%)**: Memahami dan menginterpretasikan metrik kemiripan spasial saat citra digeser.
* **Analisis Efisiensi GAP (25%)**: Membuktikan pemangkasan drastis jumlah parameter linear head.
* **Kualitas Kode & Struktur (15%)**: Kode bersih, modular, dan mematuhi kaidah penulisan ilmiah.
