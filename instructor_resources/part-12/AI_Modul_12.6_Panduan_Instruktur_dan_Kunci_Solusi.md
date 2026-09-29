# Panduan Instruktur & Kunci Solusi: AI Modul 12.6 - Object Detection

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Perbedaan konseptual Image Classification, Localization, dan Object Detection.
* **Menit 35 - 65**: Formulasi matematis koordinat bounding box, IoU, dan algoritma Non-Maximum Suppression (NMS).
* **Menit 65 - 100**: Praktikum komputer: Implementasi kalkulasi IoU, konversi format koordinat $xywh \leftrightarrow xyxy$, dan penapisan NMS.
* **Menit 100 - 130**: Studi kasus sensus buah kelapa sawit via drone dan perbandingan Hard-NMS vs Soft-NMS.
* **Menit 130 - 150**: Pembahasan potensi kendala teknis koordinat dan evaluasi Mean Average Precision (mAP).

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Formulasi Soft-NMS Gaussian)
* Pada Hard-NMS, jika kotak kandidat $b_i$ memiliki $\text{IoU} \ge N_{\text{thresh}}$, skornya langsung diatur menjadi 0 (dihapus seketika). Akibatnya, objek lain yang kebetulan berada sangat dekat akan lenyap (*false negative*).
* Pada **Soft-NMS Gaussian**:
  $$s_i = s_i \exp \left( - \frac{\text{IoU}(M, b_i)^2}{\sigma} \right)$$
* Skor kotak tetangga tidak dihapus melainkan didegradasi secara halus sebanding dengan tingkat tumpang tindihnya. Jika kotak tersebut merepresentasikan objek kedua yang sah, skornya akan tetap berada di atas ambang batas deteksi akhir sehingga objek tetap terdeteksi.

### Solusi Soal Mandiri 2 (Implementasi Generalized IoU / GIoU)
```python
import torch

def generalized_iou(box1, box2):
    '''
    box1, box2: Tensor koordinat (4,) [x1, y1, x2, y2]
    '''
    # 1. Hitung Intersection
    x1 = torch.max(box1[0], box2[0])
    y1 = torch.max(box1[1], box2[1])
    x2 = torch.min(box1[2], box2[2])
    y2 = torch.min(box1[3], box2[3])
    inter = torch.clamp(x2 - x1, min=0) * torch.clamp(y2 - y1, min=0)
    
    # 2. Hitung Union
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - inter
    iou = inter / (union + 1e-8)
    
    # 3. Hitung Smallest Enclosing Box C
    c_x1 = torch.min(box1[0], box2[0])
    c_y1 = torch.min(box1[1], box2[1])
    c_x2 = torch.max(box1[2], box2[2])
    c_y2 = torch.max(box1[3], box2[3])
    c_area = (c_x2 - c_x1) * (c_y2 - c_y1)
    
    # 4. Formula GIoU = IoU - (C - Union) / C
    giou = iou - (c_area - union) / (c_area + 1e-8)
    return giou

# Uji dua kotak terpisah (IoU = 0)
b1 = torch.tensor([0., 0., 10., 10.])
b2 = torch.tensor([20., 20., 30., 30.])
val_giou = generalized_iou(b1, b2)
print(f"GIoU untuk kotak tak beririsan: {val_giou.item():.4f}") # Bernilai negatif, memberikan gradien jarak!
```

---

## 3. Rubrik Penilaian Praktikum
* **Kebenaran Formulasi IoU (30%)**: Implementasi IoU teruji secara analitis dan bebas galat pembagian nol.
* **Implementasi Algoritma NMS (35%)**: Logika pengurutan skor dan eliminasi iteratif berfungsi sempurna.
* **Visualisasi & Interpretasi (20%)**: Menampilkan grafik perbandingan bounding box sebelum vs sesudah NMS dengan jelas.
* **Struktur Kode & Dokumentasi (15%)**: Kode rapi, menggunakan pustaka standar, dan terdokumentasi dengan baik.
