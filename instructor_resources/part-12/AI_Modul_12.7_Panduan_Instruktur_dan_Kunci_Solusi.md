# Panduan Instruktur & Kunci Solusi: AI Modul 12.7 - YOLO (You Only Look Once)

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Filosofi Single-Stage Detector vs Two-Stage, konsep pembagian kisi $S \times S$, dan peran anchor boxes.
* **Menit 35 - 65**: Penurunan matematis fungsi transformasi non-linear koordinat kotak dan komponen kerugian CIoU.
* **Menit 65 - 100**: Praktikum komputer: Perakitan modul `MiniYOLOHead` di PyTorch, penguraian tensor prediksi, dan visualisasi kotak pada grid.
* **Menit 100 - 130**: Studi kasus sensus buah kelapa sawit via kamera drone berkecepatan 30 km/jam.
* **Menit 130 - 150**: Pembahasan potensi kendala numerik fungsi eksponensial dan strategi eliminasi redundansi NMS di GPU.

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
