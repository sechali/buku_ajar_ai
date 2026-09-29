# Panduan Instruktur & Kunci Solusi: AI Modul 13.4.1 - Deteksi Penyakit Daun

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Telaah patologi daun sawit (*Curvularia*, *Pestalotiopsis*) dan perbedaan visual terhadap defisiensi hara makro.
* **Menit 35 - 65**: Penurunan matematis rasio keparahan spasial dan Disease Severity Index (DSI).
* **Menit 65 - 100**: Praktikum komputer: Segmentasi HSV, kuantifikasi luas lesi nekrotik, dan pembuatan overlay visual.
* **Menit 100 - 130**: Studi kasus pembibitan PT Sawit Nusantara dan perancangan pohon keputusan proteksi tanaman.
* **Menit 130 - 150**: Pembahasan mitigasi pantulan cahaya matahari (*specular glare*) dan kuis evaluasi.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Keunggulan Ruang Warna HSV vs RGB)
* Ruang warna RGB mencampurkan informasi kromatik (warna murni) dengan intensitas cahaya (*luminance*) pada ketiga kanalnya ($R, G, B$). Ketika awan melintas atau terjadi bayangan pelepah, nilai ketiga kanal bergeser drastis secara non-linear, merusak ambang batas biner.
* Ruang warna **HSV** memisahkan komponen warna murni (*Hue / H*) dari saturasi (*S*) dan intensitas cahaya (*Value / V*). Variasi bayangan hanya memengaruhi kanal $V$, sedangkan nilai $H$ untuk daun hijau (rentang $35 - 85^\circ$) dan lesi nekrotik cokelat ($10 - 25^\circ$) tetap stabil.

### Solusi Soal Mandiri 2 (Metrik Bentuk Kontur Lesi)
```python
import cv2

def extract_lesion_morphology(contour):
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0:
        return 0.0, 0.0
    # Sirkularitas = 4 * pi * Area / (Perimeter^2)
    circularity = (4 * 3.14159 * area) / (perimeter ** 2)
    
    # Rasio Aspek Bounding Box
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h if h > 0 else 1.0
    return circularity, aspect_ratio

# Curvularia: sirkularitas tinggi (> 0.75), aspect ratio ~1.0
# Pestalotiopsis: sirkularitas rendah (< 0.50), memanjang elips
```

---

## 3. Rubrik Penilaian Praktikum
* **Ketepatan Segmentasi Spasial (35%)**: Masker daun dan lesi terpisah bersih tanpa menyertakan latar belakang tanah.
* **Kuantifikasi Keparahan Akurat (30%)**: Perhitungan persentase kerusakan $\phi$ konsisten dengan luas piksel terdeteksi.
* **Integrasi Rekomendasi Agronomi (20%)**: Pohon keputusan menghasilkan arahan dosis kimia dan budidaya yang logis.
* **Kualitas Visualisasi Diagnostik (15%)**: Panel gambar menampilkan citra asli, masker biner, dan overlay secara proporsional.
