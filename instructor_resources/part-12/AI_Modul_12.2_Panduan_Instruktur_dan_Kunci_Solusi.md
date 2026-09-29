# Panduan Instruktur & Kunci Solusi: AI Modul 12.2 - Arsitektur CNN

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Telaah komparatif LeNet-5, AlexNet, VGG-16, dan ResNet.
* **Menit 35 - 65**: Penurunan matematis fenomena degradasi jaringan dan formulasi *Residual Learning* $H(x) = F(x) + x$.
* **Menit 65 - 105**: Praktikum komputer: Perakitan modul `BasicBlock` PyTorch, verifikasi penambahan dimensi proyeksi $1 \times 1$.
* **Menit 105 - 130**: Studi kasus sortasi kematangan TBS sawit (4 fraksi kematangan) dan perbandingan FLOPs vs Akurasi.
* **Menit 130 - 150**: Pembahasan potensi kendala implementasi residual dan kuis pemahaman arsitektur.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Parameter FC Layer VGG-16 vs GAP ResNet)
* **Kalkulasi Parameter FC VGG-16**:
  * Peta fitur keluaran konvolusi terakhir VGG-16: $7 \times 7 \times 512 = 25.088$ unit.
  * Lapisan FC1 ($25.088 \to 4096$): $\text{Bobot} = 25.088 \times 4096 \approx 102.760.448$ parameter!
  * Lapisan FC2 ($4096 \to 4096$): $\text{Bobot} = 4096 \times 4096 \approx 16.777.216$ parameter.
  * Hanya pada 2 lapisan FC ini saja, parameter mencapai **~119,5 Juta** (86.5% dari seluruh model).
* **Solusi Global Average Pooling (GAP) ResNet**:
  * GAP merata-ratakan seluruh area spasial $7 \times 7$ menjadi satu nilai skalar per kanal, sehingga keluaran tensor menjadi $1 \times 1 \times 512$ ($512$ unit).
  * Lapisan klasifikasi akhir ($512 \to 1000$ kelas): $\text{Bobot} = 512 \times 1000 = 512.000$ parameter.
  * GAP memangkas parameter lebih dari **99.5%**, mengeliminasi overfitting secara radikal tanpa mengurangi representasi semantik.

### Solusi Soal Mandiri 2 (Implementasi Bottleneck Block ResNet)
```python
import torch
import torch.nn as nn

class BottleneckBlock(nn.Module):
    expansion = 4
    def __init__(self, in_channels, base_channels, stride=1):
        super().__init__()
        out_channels = base_channels * self.expansion
        # 1x1 Conv (Kompresi Dimensi)
        self.conv1 = nn.Conv2d(in_channels, base_channels, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(base_channels)
        # 3x3 Conv (Ekstraksi Spasial)
        self.conv2 = nn.Conv2d(base_channels, base_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(base_channels)
        # 1x1 Conv (Ekspansi Dimensi 4x)
        self.conv3 = nn.Conv2d(base_channels, out_channels, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        
        # Shortcut Projection jika dimensi berubah
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
            
    def forward(self, x):
        identity = self.shortcut(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += identity
        return self.relu(out)

# Pengujian tensor (N, 256, 14, 14)
block = BottleneckBlock(in_channels=256, base_channels=64, stride=1)
x = torch.randn(2, 256, 14, 14)
y = block(x)
print(f"Bentuk Tensor Input: {x.shape} -> Output: {y.shape}") # (2, 256, 14, 14)
```

---

## 3. Rubrik Penilaian Praktikum
* **Implementasi Arsitektur (35%)**: Ketepatan perakitan modul residual dan keselarasan dimensi tensor pada percabangan shortcut.
* **Analisis Teoretis Komparatif (25%)**: Kedalaman penjelasan degradasi gradien dan eliminasi bottleneck parameter via GAP.
* **Performa Model (25%)**: Keberhasilan konvergensi pada dataset multi-kelas TBS sawit dengan akurasi $\ge 90\%$.
* **Kerapian Kode & Dokumentasi (15%)**: Dokumentasi rapi dan struktur modular berbasis PyTorch standar industri.
