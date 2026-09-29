# Panduan Instruktur & Kunci Solusi: AI Modul 12.10 - Training Dataset Citra

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Telaah format anotasi citra (YOLO txt, COCO json, Pascal VOC xml) dan formula konversi koordinat.
* **Menit 35 - 65**: Penjelasan matematis augmentasi MixUp, Mosaic, dan akselerasi komputasi Automatic Mixed Precision (AMP).
* **Menit 65 - 100**: Praktikum komputer: Perakitan `Dataset` PyTorch terintegrasi, loop pelatihan dengan `GradScaler`, dan ekspor model ONNX.
* **Menit 100 - 130**: Studi kasus kurasi dataset patologi kelapa sawit nasional (*PalmBio-Dataset*) dan mitigasi data leakage.
* **Menit 130 - 150**: Pembahasan potensi kendala teknis underflow FP16 dan orientasi transisi menuju Part 13 (Aplikasi Real-Time).

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Bentuk Distribusi Beta MixUp)
* Fungsi kepadatan probabilitas distribusi Beta:
  $$f(\lambda; \alpha, \beta) = \frac{1}{\text{B}(\alpha, \beta)} \lambda^{\alpha - 1} (1 - \lambda)^{\beta - 1}$$
* Ketika $\alpha = \beta = 0.2$:
  $$f(\lambda) \propto \lambda^{-0.8} (1 - \lambda)^{-0.8}$$
* Karena eksponen bernilai negatif ($-0.8$), nilai fungsi menuju tak terhingga ketika $\lambda \to 0$ atau $\lambda \to 1$, dan mencapai nilai minimum di $\lambda = 0.5$ (membentuk kurva U / *U-shaped*).
* **Keuntungan Matematis**: Model sebagian besar waktu menerima citra yang hampir murni ($\lambda \approx 0.9$ atau $\lambda \approx 0.1$) dengan sedikit sentuhan noise dari kelas lain, mempertahankan identitas visual objek utama sembari memuluskan batas keputusan (*decision boundary*).

### Solusi Soal Mandiri 2 (Skrip Validasi Format YOLO)
```python
import os
import glob

def validate_yolo_dataset(labels_dir):
    txt_files = glob.glob(os.path.join(labels_dir, "*.txt"))
    invalid_lines = 0
    total_boxes = 0
    for f in txt_files:
        with open(f, 'r') as fh:
            for line in fh:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                total_boxes += 1
                cls_id, xc, yc, w, h = int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                if not (0.0 <= xc <= 1.0 and 0.0 <= yc <= 1.0 and 0.0 < w <= 1.0 and 0.0 < h <= 1.0):
                    print(f"Galat koordinat pada file {f}: {line}")
                    invalid_lines += 1
    print(f"Validasi selesai: {total_boxes} kotak diperiksa. Kotak cacat: {invalid_lines}")
```

---

## 3. Rubrik Penilaian Praktikum
* **Penguasaan Format Data & Dataset Pipeline (30%)**: Pembuatan kelas `Dataset` yang rapi dan penanganan augmentasi yang tepat.
* **Penerapan Pelatihan AMP (35%)**: Konfigurasi `torch.cuda.amp.autocast` dan `GradScaler` berjalan stabil tanpa galat numerik.
* **Serialisasi Model ONNX (20%)**: Model berhasil diekspor ke format ONNX dan dapat dimuat ulang oleh runtime.
* **Kualitas Kode & Standar Rekayasa (15%)**: Kode berstandar industri, bersih, modular, dan terdokumentasi dengan baik.
