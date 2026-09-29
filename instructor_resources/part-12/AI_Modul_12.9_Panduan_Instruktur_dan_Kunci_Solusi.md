# Panduan Instruktur & Kunci Solusi: AI Modul 12.9 - Faster R-CNN

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Evolusi Two-Stage Detectors: R-CNN, Fast R-CNN, dan Faster R-CNN.
* **Menit 35 - 65**: Penjelasan matematis RPN, anchor priors 9 variasi, dan formulasi Interpolasi Bilinear RoIAlign.
* **Menit 65 - 100**: Praktikum komputer: Perakitan RPN di PyTorch, pengujian `torchvision.ops.RoIAlign`, dan penyelarasan koordinat.
* **Menit 100 - 130**: Studi kasus inspeksi cacat retak mikro bejana tekan turbin uap di pabrik kelapa sawit.
* **Menit 130 - 150**: Pembahasan potensi kendala teknis kuantisasi diskrit dan komparasi mendalam Faster R-CNN vs YOLO.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Kalkulasi Interpolasi Bilinear RoIAlign)
* Diberikan titik $(x, y) = (2.3, 4.7)$:
  * Koordinat tetangga: $x_0 = 2, x_1 = 3, y_0 = 4, y_1 = 5$.
  * Bobot selisih:
    * $\Delta x = 2.3 - 2 = 0.3 \implies (1 - \Delta x) = 0.7$
    * $\Delta y = 4.7 - 4 = 0.7 \implies (1 - \Delta y) = 0.3$
  * Bobot masing-masing titik:
    * $w_{00} = (1 - 0.3)(1 - 0.7) = 0.7 \times 0.3 = 0.21$
    * $w_{10} = 0.3 \times 0.3 = 0.09$
    * $w_{01} = 0.7 \times 0.7 = 0.49$
    * $w_{11} = 0.3 \times 0.7 = 0.21$
  * Nilai interpolasi kontinu:
    $$f(2.3, 4.7) = 0.21(10) + 0.09(20) + 0.49(30) + 0.21(40) = 2.1 + 1.8 + 14.7 + 8.4 = \mathbf{27.0}$$

### Solusi Soal Mandiri 2 (Generator 9 Anchor Dasar PyTorch)
```python
import torch

def generate_base_anchors(base_size=16, ratios=[0.5, 1.0, 2.0], scales=[8, 16, 32]):
    anchors = []
    for scale in scales:
        area = (base_size * scale) ** 2
        for r in ratios:
            w = round((area / r) ** 0.5)
            h = round(w * r)
            # Koordinat [x1, y1, x2, y2] berpusat di (0, 0)
            anchors.append([-w/2, -h/2, w/2, h/2])
    return torch.tensor(anchors, dtype=torch.float32)

base_anchors = generate_base_anchors()
print(f"Total Base Anchors: {len(base_anchors)} (3 skala x 3 rasio = 9)")
print(base_anchors)
```

---

## 3. Rubrik Penilaian Praktikum
* **Perakitan Modul RPN (35%)**: Implementasi lapisan konvolusi dan pembagian skor/delta terverifikasi benar.
* **Pemanfaatan RoIAlign (35%)**: Memahami penanganan `spatial_scale` dan format tensor proposal multi-batch.
* **Analisis Teoretis Komparatif (15%)**: Kedalaman penjelasan eliminasi kuantisasi spasial diskrit via RoIAlign.
* **Kualitas Kode & Standar Rekayasa (15%)**: Kode modular, bebas galat sintaks, dan terdokumentasi dengan baik.
