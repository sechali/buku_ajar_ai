# Panduan Instruktur & Kunci Solusi: AI Modul 12.8 - Single Shot Detector (SSD)

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
