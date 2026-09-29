# Panduan Instruktur & Kunci Solusi: AI Modul 12.5 - Image Classification dengan CNN

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Tinjauan pipeline end-to-end klasifikasi citra, fungsi loss Cross-Entropy, dan regularisasi Label Smoothing.
* **Menit 30 - 60**: Penjelasan matematis Grad-CAM untuk memverifikasi atensi spasial model.
* **Menit 60 - 100**: Praktikum komputer: Perakitan mesin pelatih `IndustrialCNNTrainer`, implementasi gradient clipping, checkpointing model terbaik.
* **Menit 100 - 130**: Studi kasus sortasi TBS kelapa sawit di pabrik kelapa sawit dan analisis Confusion Matrix.
* **Menit 130 - 150**: Pembahasan potensi kendala teknis shortcut learning dan kuis formatif.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Penurunan Gradien Cross-Entropy terhadap Logits)
* Misalkan $z$ adalah logits dan $\hat{y}_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$.
* Loss: $\mathcal{L} = -\sum_k q_k \ln \hat{y}_k$.
* Turunan Softmax: $\frac{\partial \hat{y}_k}{\partial z_i} = \hat{y}_i (\mathbb{I}(i=k) - \hat{y}_k)$.
* Turunan Chain Rule:
  $$\frac{\partial \mathcal{L}}{\partial z_i} = - \sum_k \frac{q_k}{\hat{y}_k} \frac{\partial \hat{y}_k}{\partial z_i} = - \frac{q_i}{\hat{y}_i} \hat{y}_i (1 - \hat{y}_i) - \sum_{k \neq i} \frac{q_k}{\hat{y}_k} (-\hat{y}_i \hat{y}_k)$$
  $$\frac{\partial \mathcal{L}}{\partial z_i} = - q_i (1 - \hat{y}_i) + \hat{y}_i \sum_{k \neq i} q_k = - q_i + q_i \hat{y}_i + \hat{y}_i (1 - q_i) = \hat{y}_i - q_i$$
* Terbukti bahwa gradien adalah selisih langsung probabilitas prediksi terhadap target ($\hat{y}_i - q_i$).

### Solusi Soal Mandiri 2 (Focal Loss PyTorch)
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, alpha=None, gamma=2.0, reduction='mean'):
        super().__init__()
        self.alpha = alpha # Tensor bobot kelas
        self.gamma = gamma
        self.reduction = reduction
        
    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none', weight=self.alpha)
        pt = torch.exp(-ce_loss) # Probabilitas kelas target
        focal_loss = ((1.0 - pt) ** self.gamma) * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss
```

---

## 3. Rubrik Penilaian Praktikum
* **Kelengkapan Pipeline Pelatihan (30%)**: Implementasi loop pelatihan, evaluasi berkala, dan checkpointing model.
* **Metrik Evaluasi & Visualisasi (30%)**: Perhitungan akurat Confusion Matrix dan interpretasi Precision/Recall multi-kelas.
* **Performa Model (25%)**: Model mencapai konvergensi stabil dan akurasi validasi $\ge 90\%$.
* **Kualitas Kode & Standar Rekayasa (15%)**: Kode modular berstandar industri dengan penanganan perangkat (CPU/GPU) yang tepat.
