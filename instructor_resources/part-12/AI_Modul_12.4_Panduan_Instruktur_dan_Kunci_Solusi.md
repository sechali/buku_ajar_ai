# Panduan Instruktur & Kunci Solusi: AI Modul 12.4 - Transfer Learning

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Konsep transfer learning, inductive transfer, dan bahaya overfitting pada dataset terbatas.
* **Menit 30 - 65**: Penjelasan mendalam Feature Extraction vs Fine-Tuning serta formula Discriminative Learning Rates.
* **Menit 65 - 100**: Praktikum komputer: Pembekuan bobot backbone, implementasi `param.requires_grad = False`, konfigurasi PyTorch parameter groups.
* **Menit 100 - 130**: Studi kasus diagnosis defisiensi hara bibit sawit (N, K, Mg, B) dengan 200 sampel citra.
* **Menit 130 - 150**: Pembahasan potensi kekeliruan umum (keselarasan normalisasi ImageNet, catastrophic forgetting).

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Kapan Fine-Tuning Memperburuk Performa)
* Fine-tuning dapat memperburuk performa model jika:
  1. **Dataset Target Sangat Kecil (< 300 sampel)** dan **Domain Sangat Mirip dengan Sumber**: Mengaktifkan gradien pada jutaan parameter backbone akan langsung memicu *overfitting*, merusak fitur general yang sudah optimal.
  2. **Learning Rate Terlalu Besar**: Memperbarui bobot awal dengan laju pembelajaran besar akan memicu *Catastrophic Forgetting*, menghilangkan filter tepi dan tekstur dasar. Dalam kondisi data sangat minim, *Feature Extraction* murni selalu lebih aman dan stabil.

### Solusi Soal Mandiri 2 (MobileNetV2 Selective Unfreezing)
```python
import torch
import torchvision.models as models

# Muat model MobileNetV2
mobilenet = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

# Bekukan seluruh lapisan terlebih dahulu
for param in mobilenet.parameters():
    param.requires_grad = False

# Buka pembekuan pada blok fitur ke-17, 18, dan classifier head
for param in mobilenet.features[17].parameters():
    param.requires_grad = True
for param in mobilenet.features[18].parameters():
    param.requires_grad = True
for param in mobilenet.classifier.parameters():
    param.requires_grad = True

p_train = sum(p.numel() for p in mobilenet.parameters() if p.requires_grad)
p_total = sum(p.numel() for p in mobilenet.parameters())
print(f"Parameter Aktif: {p_train:,} / {p_total:,} ({p_train/p_total*100:.2f}%)")
```

---

## 3. Rubrik Penilaian Praktikum
* **Penguasaan Mekanisme Pembekuan Bobot (30%)**: Implementasi `param.requires_grad = False` tepat dan terverifikasi secara logis.
* **Konfigurasi Parameter Groups (30%)**: Berhasil mendefinisikan laju pembelajaran bertingkat pada optimizer AdamW.
* **Stabilitas Pelatihan (25%)**: Model konvergen dan mencapai akurasi validasi $\ge 88\%$ pada data simulasi defisiensi hara.
* **Struktur Kode & Dokumentasi (15%)**: Kode modular, bebas galat sintaks, dan menyajikan visualisasi metrik yang jelas.
