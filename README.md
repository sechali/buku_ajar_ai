# AI Academy: Buku Praktikum Interaktif
### *100 Interactive Jupyter Notebooks for Precision Agriculture & Palm Oil Agro-Industry*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Notebooks](https://img.shields.io/badge/Notebooks-100%20Complete-brightgreen.svg)]()
[![Curriculum Parts](https://img.shields.io/badge/Curriculum-13%20Parts-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Google%20Colab%20%7C%20JupyterLab-yellow.svg?logo=googlecolab&logoColor=white)]()
[![Institution](https://img.shields.io/badge/Institution-INSTIPER%20Yogyakarta-darkgreen.svg)](https://instiperjogja.ac.id/)

---

## 📌 Ringkasan Eksekutif (Executive Summary)

Repositori ini memuat **100 Buku Kerja Praktikum Interaktif (Jupyter Notebooks)** untuk mata kuliah **AI Academy**. 

Dirancang secara khusus untuk menjembatani disiplin **Teknik Informatika, Sains Data, dan Agroteknologi**, seluruh *notebook* mengintegrasikan implementasi kode Python berstandar industri dengan kasus nyata agroindustri perkebunan kelapa sawit dan pertanian presisi tropis di Indonesia.

Setiap *notebook* dilengkapi dengan tautan **1-Click Open In Colab** sehingga mahasiswa dan peneliti dapat langsung mengeksekusi dan bereksplorasi di lingkungan cloud Google Colab tanpa kendala instalasi lokal.

---

## 🌟 Fitur Unggulan Praktikum (Key Highlights)

1. **100 Notebook Mandiri (*Self-Contained*)**:
   - Seluruh modul praktikum (Part 01 s.d. Part 13) telah teruji dan dapat dieksekusi secara mulus (*zero-error*).
2. **Kasus Riil Agrokompleks & Kelapa Sawit**:
   - Sortasi TBS kelapa sawit, deteksi penyakit bercak daun (*Curvularia*) dan busuk pangkal batang (*Ganoderma*), pemrosesan citra drone multispektral, estimasi hara NPK, prediksi kadar asam lemak bebas (ALB/FFA), serta monitoring sensor IoT lahan gambut.
3. **Eksekusi 1-Klik di Google Colab**:
   - Setiap notebook memiliki tombol *badge* langsung untuk membuka notebook di Google Colab dengan konfigurasi GPU/CPU siap pakai.
4. **Metodologi Sains Data Rigor**:
   - Mengimplementasikan isolasi data ketat (*anti-data leakage*), validasi silang spasial (*spatial block cross-validation*), evaluasi komparatif metrik, dan interpretasi model (*Explainable AI*).

---

## 🗺️ Peta Kurikulum & Pembagian 13 Bagian (Curriculum Map)

| Bagian | Topik Praktikum | Rentang Notebook | Cakupan Utama |
| :---: | :--- | :---: | :--- |
| **Part 01** | Pengantar AI & Paradigma Komputasi | Modul 1.1 – 1.7 | Eksplorasi paradigma AI, data tabular pertanian, dan komputasi dasar. |
| **Part 02** | Logika Komputasi & Pemrograman Dasar | Modul 2.1 – 2.9 | Algoritma dasar, struktur kontrol percabangan/perulangan, fungsi, dan logika agronomis. |
| **Part 03** | Struktur Data & Ekosistem Python | Modul 3.1 – 3.10 | List/dict comprehension, penanganan berkas (CSV/JSON), eksepsi, dan modul Python. |
| **Part 04** | Pengolahan, Analisis, & Visualisasi Data | Modul 4.1 – 4.8 | Komputasi vektor NumPy, manipulasi data Pandas, data cleaning, dan visualisasi Matplotlib/Seaborn. |
| **Part 05** | Fondasi Matematika & Aljabar Linier AI | Modul 5.1 – 5.7 | Vektor-matriks, dekomposisi data, kalkulus gradien, fungsi kerugian, dan optimasi numerik. |
| **Part 06** | Evaluasi Model & Validasi Silang | Modul 6.1 – 6.4 | Metrik evaluasi klasifikasi/regresi, matriks konfusi, kurva ROC-AUC, K-Fold, dan Spatial Cross-Validation. |
| **Part 07** | Machine Learning Klasik Terbimbing | Modul 7.1 – 7.10 | Regresi Linier/Logistik, KNN, Decision Tree, Random Forest, Naive Bayes, SVM, Gradient Boosting. |
| **Part 08** | Unsupervised Learning & Reduksi Dimensi | Modul 8.1 – 8.5 | Pipeline preprocessing terisolasi, evaluasi model, interpretasi fitur PFI/SHAP, inferensi operasional. |
| **Part 09** | Deep Learning & Jaringan Saraf Tiruan | Modul 9.1 – 9.9 | Perceptron, MLP multi-layer, backpropagation, optimasi SGD/Adam, regularisasi, PyTorch framework. |
| **Part 10** | Pelatihan & Regularisasi Deep Learning | Modul 10.1 – 10.7 | Matriks piksel citra, ruang warna RGB/HSV, konvolusi 2D, filter spasial, deteksi tepi Sobel/Canny. |
| **Part 11** | Pengolahan Citra Digital & OpenCV Dasar | Modul 11.1 – 11.9 | Pustaka OpenCV, thresholding Otsu, kontur geometri, deteksi visual, pemrosesan video & webcam streaming. |
| **Part 12** | Convolutional Neural Networks & Object Detection | Modul 12.1 – 12.10 | Arsitektur CNN (VGG/ResNet), transfer learning, metrik IoU/NMS, YOLO detector, SSD, Faster R-CNN. |
| **Part 13** | Integrasi Sistem AI & Deployment Industri | Modul 13.1 – 13.4.2 | Integrasi model dengan video streaming, multi-object tracking (SORT), antarmuka GUI/web dasbor, pemantauan CCTV PKS. |

---

## 📂 Struktur Direktori Repositori (Repository Structure)

```text
├── notebooks/                  # 100 Berkas Praktikum Interaktif (Jupyter Notebooks .ipynb)
│   ├── part-01/ (7 notebooks)  # Pengantar AI & Paradigma Komputasi
│   ├── part-02/ (9 notebooks)  # Logika Komputasi & Pemrograman Dasar
│   ├── part-03/ (10 notebooks) # Struktur Data & Ekosistem Python
│   ├── part-04/ (8 notebooks)  # Pengolahan, Analisis, & Visualisasi Data
│   ├── part-05/ (7 notebooks)  # Fondasi Matematika & Aljabar Linier AI
│   ├── part-06/ (4 notebooks)  # Evaluasi Model & Validasi Silang
│   ├── part-07/ (10 notebooks) # Machine Learning Klasik Terbimbing
│   ├── part-08/ (5 notebooks)  # Unsupervised Learning & Reduksi Dimensi
│   ├── part-09/ (9 notebooks)  # Deep Learning & PyTorch Dasar
│   ├── part-10/ (7 notebooks)  # Dasar Visi Komputer & Matriks Citra
│   ├── part-11/ (9 notebooks)  # Pengolahan Citra Digital & OpenCV
│   ├── part-12/ (10 notebooks) # CNN, Transfer Learning, & Object Detection
│   └── part-13/ (5 notebooks)  # Integrasi Sistem AI, Video Tracking, & Dasbor Web
└── README.md                   # Panduan & Dokumentasi Repositori
```

---

## 🚀 Panduan Menjalankan Notebook

### 1. Menjalankan di Cloud via Google Colab (Paling Disarankan)
1. Buka folder `notebooks/` pada repositori ini di GitHub.
2. Buka berkas notebook (`.ipynb`) yang ingin Anda pelajari.
3. Klik lencana badge **Open In Colab** pada baris paling atas notebook:
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com)
   
4. Untuk modul Part 09 s.d. Part 13 (*Deep Learning & Visi Komputer*), aktifkan akselerasi GPU secara gratis di Colab:
   * Menu: `Runtime` $\to$ `Change runtime type` $\to$ Pilih `T4 GPU` $\to$ `Save`.

---

### 2. Menjalankan di Komputer Lokal

```bash
# 1. Kloning repositori
git clone https://github.com/sechali/buku_ajar_ai.git
cd buku_ajar_ai

# 2. Buat dan aktifkan lingkungan virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Instal pustaka yang dibutuhkan
pip install --upgrade pip
pip install numpy pandas matplotlib seaborn scikit-learn opencv-python torch torchvision jupyterlab

# 4. Jalankan Jupyter Lab
jupyter lab
```

---

## 👥 Tim Pengembang Kurikulum

* **Tim Akademik & Laboratorium Kecerdasan Buatan**
* **Institut Pertanian STIPER (INSTIPER) Yogyakarta**
* Fokus Riset: *Precision Agriculture, Agro-Industrial Informatics, Machine Learning & Computer Vision*.

---

## 📄 Lisensi (License)

Materi praktikum ini didistribusikan di bawah lisensi [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).
