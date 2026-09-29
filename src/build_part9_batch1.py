import os
import json
import re

# Banned words validation
BANNED_WORDS = ['taksonomi', 'tripartit', 'ontologis', 'epistemologis', 'dialektika', 'manifestasi dependensi', 'de facto']

def validate_text(text, filename):
    lower = text.lower()
    for w in BANNED_WORDS:
        if w in lower:
            raise ValueError(f"BANNED WORD FOUND in {filename}: '{w}'")
    print(f"[VALIDATED] 0 banned words in {filename}")

# ==============================================================================
# MODUL 9.1: Konsep Deep Learning
# ==============================================================================
def create_modul_9_1():
    md_content = """# AI Modul 9.1: Konsep Deep Learning

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-09-01
* **Mata Kuliah**: Kecerdasan Buatan Terapan & Deep Learning (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Ganjil)
* **Prasyarat**: AI Modul 8.5 (Pembuatan Sistem Prediksi Sederhana)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pemahaman Paradigma Deep Learning, Skrip Hierarchical Feature Learning, Uji Teorema Aproksimasi"] --> B["OUTCOMES: Kemampuan Membedakan Feature Engineering Manual vs Otomatis pada Data Kompleks"]
    B --> C["IMPACTS: Fondasi Komputasi Deep Learning Kokoh untuk Otomasi Pemantauan Perkebunan Modern"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** evolusi paradigma komputasi dari rekayasa fitur manual (*handcrafted feature engineering*) pada machine learning klasik menuju pembelajaran representasi hierarkis (*hierarchical representation learning*) pada deep learning.
2. **Menerapkan (C3)** konsep dasar representasi bertingkat dari data sensor mentah (*raw sensor data*) melalui jaringan saraf bertingkat menggunakan pustaka NumPy untuk mengekstraksi pola non-linier bertingkat.
3. **Menganalisis (C4)** landasan teoritis Teorema Aproksimasi Universal (*Universal Approximation Theorem*) serta mengevaluasi trade-off antara kedalaman arsitektur (*depth*), lebar arsitektur (*width*), kebutuhan volume data latih, dan kapasitas akselerasi perangkat keras GPU.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan komprehensif mengenai perbedaan fundamental antara model dangkal (*shallow models*) dan model dalam (*deep models*).
  * Skrip Python modular berstandar PEP 8 untuk mensimulasikan ekstraksi fitur bertingkat dan aproksimasi fungsi non-linier kompleks pada parameter agro-industri.
  * Analisis visual perbandingan kapasitas representasi fitur antara model linier sederhana dan jaringan saraf bertingkat.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian merancang arsitektur pemodelan data yang tepat berdasarkan kompleksitas data masukan di lingkungan perkebunan (citra drone, data cuaca temporal, profil spektrometri tanah).
  * Kemampuan mengidentifikasi kapan deep learning diperlukan dan kapan machine learning konvensional lebih mangkus digunakan.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Transformasi operasional sektor perkebunan kelapa sawit dan pertanian presisi melalui adopsi kecerdasan buatan end-to-end yang mampu mengolah data masif tanpa ketergantungan pada ekstraksi fitur manual yang melelahkan.

---

## 2. Profil Fundamental Deep Learning: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Deep Learning adalah sub-bidang dari Machine Learning yang memanfaatkan arsitektur jaringan saraf tiruan berlapis banyak (*deep artificial neural networks*) untuk mempelajari representasi data secara hierarkis langsung dari data mentah. Secara matematis dan fungsional, deep learning bekerja melalui:
1. **Komposisi Fungsi Non-Linier Bertingkat**: Memodelkan relasi pemetaan kompleks $f: \mathcal{X} \rightarrow \mathcal{Y}$ melalui komposisi berantai dari $L$ transformasi matematis:
   $$f(x) = f^{(L)}(f^{(L-1)}(\dots f^{(2)}(f^{(1)}(x))\dots))$$
   di mana setiap lapisan $l$ mentransformasikan representasi dari lapisan sebelumnya menjadi representasi yang lebih abstrak.
2. **Pembelajaran Fitur Otomatis (*End-to-End Feature Learning*)**: Mengeliminasi kebutuhan perancangan fitur manual yang memakan waktu dan berpotensi menimbulkan bias operator. Parameter representasi dipelajari secara terpadu melalui optimasi diferensiabel bersamaan dengan fungsi objektif akhir.
3. **Aproksimasi Fungsi Kontinu Kompleks**: Berdasarkan *Universal Approximation Theorem*, jaringan dengan fungsi aktivasi non-linier memiliki kapasitas matematis untuk mengaproksimasi fungsi kontinu berdimensi tinggi dengan tingkat presisi berapapun, asalkan kapasitas parameter memadai.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
Penerapan deep learning memberikan lompatan efisiensi pada ekosistem agrokompleks:
* **Analisis Multispektral Skala Lanskap**: Mengolah data mentah dari sensor multispektral drone secara end-to-end untuk memetakan defisiensi hara makro (N, P, K, Mg) dan kadar klorofil tanpa perlu merumuskan indeks vegetasi secara manual satu per satu.
* **Deteksi Penyakit Tanaman Tingkat Dini**: Mengidentifikasi gejala awal infeksi jamur Ganoderma atau penyakit bercak daun Curvularia dari ribuan piksel kanopi pada berbagai kondisi pencahayaan alami di kebun.
* **Peramalan Panen & Dinamika Iklim Mikro**: Mengintegrasikan data deret waktu stasiun cuaca, kelembapan tanah, dan riwayat produksi bulanan untuk memprediksi hasil panen Tandan Buah Segar (TBS) secara presisi.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
1. **Mengatasi Batas Kejenuhan Model Klasik**: Algoritma konvensional (seperti SVM atau Random Forest) cenderung mengalami saturasi performa (*performance plateau*) ketika volume data melimpah. Deep learning terus menunjukkan peningkatan akurasi seiring bertambahnya volume data dan kapasitas komputasi.
2. **Ketahanan terhadap Variasi Lingkungan Terbuka**: Lapisan-lapisan representasi dalam deep learning mampu mengekstraksi invarian spasial dan semantik yang tahan terhadap fluktuasi sudut datang sinar matahari, debu, dan latar belakang vegetasi liar di lapangan.
3. **Skalabilitas Komputasi Paralel**: Arsitektur deep learning diformulasikan dalam operasi tensor aljabar linier (perkalian matriks) yang sangat sesuai untuk diakselerasi secara masif menggunakan GPU dan Tensor Processing Unit (TPU).

### 2.4 Analisis Kelebihan dan Kekurangan (Tabel Komparasi)

| Parameter Evaluasi | Machine Learning Klasik | Deep Learning | Implikasi pada Agro-Industri |
| :--- | :--- | :--- | :--- |
| **Ketergantungan Fitur** | Memerlukan rekayasa fitur manual (*handcrafted features*) yang rumit. | Mempelajari representasi fitur hierarkis secara otomatis dari data mentah. | Menghemat waktu tim agronomis dalam merancang formula indeks manual. |
| **Skalabilitas Data** | Performa jenuh pada ukuran dataset sedang. | Performa terus meningkat seiring penambahan volume data besar. | Sangat optimal untuk ribuan citra drone perkebunan sawit ratusan hektar. |
| **Kebutuhan Komputasi** | Cukup menggunakan CPU standar, training cepat. | Memerlukan akselerasi GPU/TPU dengan memori besar. | Membutuhkan infrastruktur server komputasi atau cloud yang memadai. |
| **Interpretabilitas** | Relatif tinggi (koefisien linier, aturan percabangan pohon). | Cenderung berupa *black-box*, membutuhkan teknik XAI lanjut. | Keputusan agronomis krusial perlu divalidasi dengan visualisasi representasi laten. |
| **Kinerja pada Data Mentah** | Rendah jika data tidak diproses dan difilter secara ketat. | Sangat tinggi pada data mentah spasial, spektral, dan temporal. | Andal menghadapi derau sensor dan variasi iluminasi alami lapangan. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Sebuah konsorsium perkebunan kelapa sawit mengoperasikan armada drone untuk memetakan kesehatan 50.000 hektar tanaman. Jika menggunakan machine learning klasik, tim data harus merekayasa manual puluhan indeks reflektansi, tekstur GLCM, dan bentuk geometri tajuk. Dengan paradigma Deep Learning, citra ortofoto resolusi spasial tinggi dialirkan langsung ke dalam arsitektur bertingkat. Lapisan awal mengekstraksi gradien tepi daun, lapisan tengah menangkap pola radial pelepah sawit, dan lapisan puncak mengidentifikasi status kesehatan pohon serta memprediksi potensi timbulan buah secara terintegrasi.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Risiko Overfitting pada Dataset Kecil**: Mengingat jumlah parameter bebas yang sangat besar, melatih deep learning pada data perkebunan yang terbatas tanpa augmentasi dan regularisasi ketat akan menyebabkan model sekadar menghafal derau sampel.
2. **Kebutuhan Anotasi Berkualitas**: Kualitas representasi yang dipelajari sangat bergantung pada kebenaran label data lapangan (*ground truth*). Galat penentuan koordinat pohon atau salah diagnosa oleh mandor kebun akan menurunkan kualitas generalisasi model.

---

## 3. Landasan Teori & Konsep Matematis Deep Learning

![Konsep Hierarki Representasi Deep Learning Agrokompleks](../assets/konsep_hierarki_representasi_deep_learning_agrokompleks.png)

### 3.1 Hierarki Representasi Fitur (*Hierarchical Feature Representation*)
Secara mendasar, keunggulan deep learning terletak pada kemampuannya menyusun abstraksi konsep secara modular. Misalkan $x \in \mathbb{R}^d$ adalah vektor input berdimensi $d$ (misalnya pembacaan spektrum pantulan kanopi sawit).
* **Lapisan $1$ ($h^{(1)}$)**: Mempelajari kombinasi linier sederhana berbobot lokal yang mendeteksi perubahan intensitas tajam:
  $$h^{(1)} = \sigma(W^{(1)} x + b^{(1)})$$
* **Lapisan $2$ ($h^{(2)}$)**: Mengombinasikan fitur-fitur dari lapisan pertama untuk mendeteksi struktur perantara (seperti tekstur helai daun dan kerapatan stomata):
  $$h^{(2)} = \sigma(W^{(2)} h^{(1)} + b^{(2)})$$
* **Lapisan $L$ ($h^{(L)}$)**: Membentuk representasi semantik tingkat tinggi yang mewakili kondisi agronomis tanaman secara menyeluruh:
  $$\hat{y} = g(W^{(L)} h^{(L-1)} + b^{(L)})$$

Di mana $W^{(l)}$ adalah matriks bobot, $b^{(l)}$ adalah vektor bias, $\sigma(\cdot)$ adalah fungsi aktivasi non-linier elemen-demi-elemen, dan $g(\cdot)$ adalah fungsi pemetaan keluaran.

### 3.2 Teorema Aproksimasi Universal (*Universal Approximation Theorem*)
Fondasi matematis mengapa arsitektur jaringan saraf tiruan mampu memecahkan masalah kompleks dirumuskan oleh Hornik, Stinchcombe, dan White (1989) serta Cybenko (1989):

$$\forall \epsilon > 0, \; \exists G(x) = \sum_{i=1}^{N} \alpha_i \sigma(w_i^\top x + b_i) \quad \text{sedemikian sehingga} \quad \sup_{x \in K} |f(x) - G(x)| < \epsilon$$

Teorema ini menyatakan bahwa sebuah jaringan saraf *feedforward* dengan satu lapisan tersembunyi yang memiliki sejumlah terhingga neuron dan fungsi aktivasi non-linier kontinu terdistorsi ($\sigma$) dapat mengaproksimasi fungsi kontinu sembarang $f(x)$ pada himpunan kompak $K \subset \mathbb{R}^d$ dengan tingkat galat $\epsilon$ sekecil apapun yang diinginkan.

**Implikasi Praktis Kedalaman vs Lebar**:
Meskipun satu lapisan lebar secara teoritis cukup untuk mengaproksimasi sembarang fungsi, ukuran neuron yang dibutuhkan bisa meningkat secara eksponensial terhadap dimensi input ($O(2^d)$). Sebaliknya, arsitektur dalam (*deep architectures*) menyusun fitur secara hierarkis, memungkinkan penggunaan parameter yang jauh lebih efisien ($O(d)$ atau polinomial) untuk mengekspresikan fungsi-fungsi kompleks yang tersusun dari komposisi fungsi dasar.

### 3.3 Komputasi Berbasis Tensor dan Operasi Matriks
Dalam komputasi deep learning, seluruh data, bobot, dan sinyal aktivasi direpresentasikan sebagai **Tensor** (generalisasi skalar berdimensi 0, vektor berdimensi 1, dan matriks berdimensi 2 ke ruang berdimensi $N$). Untuk sekumpulan data berukuran batch $m$, forward pass pada suatu lapisan dihitung secara simultan menggunakan perkalian matriks:

$$Z = X W^\top + \mathbf{1}_m b^\top$$

di mana:
* $X \in \mathbb{R}^{m \times d_{\text{in}}}$ adalah matriks masukan berisi $m$ sampel data perkebunan dengan $d_{\text{in}}$ fitur.
* $W \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$ adalah matriks bobot koneksi antar lapisan.
* $b \in \mathbb{R}^{d_{\text{out}}}$ adalah vektor bias.
* $Z \in \mathbb{R}^{m \times d_{\text{out}}}$ adalah matriks net input terbobot sebelum aktivasi.

Operasi perkalian matriks masif ini memiliki kompleksitas komputasi $O(m \cdot d_{\text{in}} \cdot d_{\text{out}})$, yang dapat diparalelisasi secara sempurna pada ribuan unit *core* pemrosesan GPU.

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Raw Input Data: Vektor Spektral Sensor Kebun (x)"] --> B["Lapisan 1: Proyeksi Linier Z1 = X * W1.T + b1"]
    B --> C["Aktivasi Non-Linier: A1 = ReLU(Z1)"]
    C --> D["Lapisan 2: Komposisi Fitur Hierarkis Z2 = A1 * W2.T + b2"]
    D --> E["Aktivasi Non-Linier: A2 = ReLU(Z2)"]
    E --> F["Lapisan Output: Z3 = A2 * W3.T + b3 -> Output Prediksi"]
```

Berikut adalah implementasi Python murni (*pure NumPy*) yang mendemonstrasikan prinsip dasar hierarki representasi dan kapasitas aproksimasi fungsi non-linier kompleks:

```python
import numpy as np
import matplotlib.pyplot as plt

# 1. Inisialisasi Arsitektur Representasi Hierarkis
class HierarchicalFeatureExtractor:
    def __init__(self, input_dim, hidden_dim_1, hidden_dim_2, output_dim, seed=42):
        np.random.seed(seed)
        # Inisialisasi bobot He/Xavier
        self.W1 = np.random.randn(hidden_dim_1, input_dim) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros((1, hidden_dim_1))
        
        self.W2 = np.random.randn(hidden_dim_2, hidden_dim_1) * np.sqrt(2.0 / hidden_dim_1)
        self.b2 = np.zeros((1, hidden_dim_2))
        
        self.W3 = np.random.randn(output_dim, hidden_dim_2) * np.sqrt(2.0 / hidden_dim_2)
        self.b3 = np.zeros((1, output_dim))
        
    def relu(self, Z):
        return np.maximum(0, Z)
        
    def forward(self, X):
        # Lapisan 1: Ekstraksi fitur dasar (Low-level features)
        self.Z1 = np.dot(X, self.W1.T) + self.b1
        self.A1 = self.relu(self.Z1)
        
        # Lapisan 2: Pembentukan representasi semantik menengah (Mid-level features)
        self.Z2 = np.dot(self.A1, self.W2.T) + self.b2
        self.A2 = self.relu(self.Z2)
        
        # Lapisan Output: Pemetaan ke nilai target (High-level prediction)
        self.Z3 = np.dot(self.A2, self.W3.T) + self.b3
        return self.Z3, self.A1, self.A2

# Uji coba forward pass
model = HierarchicalFeatureExtractor(input_dim=8, hidden_dim_1=16, hidden_dim_2=8, output_dim=1)
sample_sensor_data = np.random.uniform(0.1, 1.0, size=(5, 8))
y_pred, feat_l1, feat_l2 = model.forward(sample_sensor_data)

print("Dimensi Input Sensor     :", sample_sensor_data.shape)
print("Dimensi Fitur Lapisan 1  :", feat_l1.shape)
print("Dimensi Fitur Lapisan 2  :", feat_l2.shape)
print("Dimensi Prediksi Output  :", y_pred.shape)
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Pemodelan Indeks Nutrisi Tanaman Sawit

### 5.1 Latar Belakang Masalah
Kandungan klorofil dan nitrogen pada tajuk pohon kelapa sawit memiliki relasi non-linier yang kompleks terhadap pantulan spektral cahaya pada panjang gelombang tampak (*visible*) hingga inframerah dekat (*near-infrared*). Pendekatan linier klasik sering kali menghasilkan galat sistematis saat menghadapi variasi kelembapan udara dan umur tanaman.

### 5.2 Implementasi Pemodelan Aproksimasi Non-Linier
```python
# Simulasi kurva non-linier respons nitrogen terhadap spektrum reflektansi
np.random.seed(42)
X_synthetic = np.linspace(-3, 3, 200).reshape(-1, 1)
# Fungsi target non-linier riil tanaman: kombinasi harmonik dan eksponensial
y_true = np.sin(2.5 * X_synthetic) + 0.5 * np.cos(X_synthetic) + 0.2 * X_synthetic**2

# Model Jaringan 2 Lapisan Sederhana untuk Aproksimasi
class UniversalApproximator:
    def __init__(self, n_hidden=32, lr=0.01):
        self.W1 = np.random.randn(n_hidden, 1) * 0.5
        self.b1 = np.zeros((1, n_hidden))
        self.W2 = np.random.randn(1, n_hidden) * 0.5
        self.b2 = np.zeros((1, 1))
        self.lr = lr
        
    def fit(self, X, y, epochs=1500):
        m = X.shape[0]
        for epoch in range(epochs):
            # Forward
            Z1 = np.dot(X, self.W1.T) + self.b1
            A1 = np.tanh(Z1)
            y_hat = np.dot(A1, self.W2.T) + self.b2
            
            # Loss MSE
            loss = np.mean((y_hat - y)**2)
            
            # Backward
            dy_hat = 2 * (y_hat - y) / m
            dW2 = np.dot(dy_hat.T, A1)
            db2 = np.sum(dy_hat, axis=0, keepdims=True)
            
            dA1 = np.dot(dy_hat, self.W2)
            dZ1 = dA1 * (1 - A1**2)
            dW1 = np.dot(dZ1.T, X)
            db1 = np.sum(dZ1, axis=0, keepdims=True)
            
            # Update
            self.W2 -= self.lr * dW2
            self.b2 -= self.lr * db2
            self.W1 -= self.lr * dW1
            self.b1 -= self.lr * db1

model_approx = UniversalApproximator(n_hidden=64, lr=0.03)
model_approx.fit(X_synthetic, y_true, epochs=2000)
y_pred = np.dot(np.tanh(np.dot(X_synthetic, model_approx.W1.T) + model_approx.b1), model_approx.W2.T) + model_approx.b2
rmse = np.sqrt(np.mean((y_pred - y_true)**2))
print(f"Hasil Aproksimasi Non-Linier Selesai. Final RMSE: {rmse:.4f}")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Mengabaikan Normalisasi Skala Input**: Memberikan nilai input sensor dengan rentang skala yang berbeda secara drastis (misalnya suhu $25 - 35^\circ\text{C}$ berdampingan dengan fluks radiasi $500.000\text{ lux}$) tanpa penskalaan akan menyebabkan gradien lapisan pertama meledak atau jenuh.
2. **Memaksakan Deep Learning pada Data Berdimensi Sangat Kecil**: Menggunakan model dalam dengan puluhan ribu parameter pada dataset perkebunan yang hanya berisi beberapa puluh sampel akan memicu overfitting fatal (*memorization artifact*).
3. **Meniadakan Non-Linearitas Antar-Lapisan**: Menyusun sepuluh lapisan linier berturut-turut tanpa fungsi aktivasi non-linier tidak menghasilkan arsitektur dalam, melainkan secara matematis ekuivalen dengan satu transformasi linier tunggal ($W_{\text{net}} = W_L \dots W_1$).

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Standarisasi Fitur Secara Konsisten**: Terapkan penskalaan z-score ($z = \frac{x - \mu}{\sigma}$) atau min-max scaling pada seluruh variabel sensor sebelum dialirkan ke dalam arsitektur.
2. **Prinsip Parsimoni Arsitektur (*Occam's Razor*)**: Mulailah dari arsitektur sederhana (satu atau dua lapisan tersembunyi) sebagai *baseline*, lalu tingkatkan kapasitas model secara gradual hanya bila bukti empiris menunjukkan terjadinya *underfitting*.
3. **Pemisahan Data Berorientasi Blok Kebun (*Spatial Cross-Validation*)**: Hindari random splitting pada data perkebunan yang berdekatan secara spasial untuk mencegah kebocoran informasi (*spatial data leakage*).

---

## 7. Rangkuman Modul

* Deep Learning merevolusi analisis data komputasional dengan menggantikan perancangan fitur manual menjadi pembelajaran representasi bertingkat secara otomatis (*hierarchical feature learning*).
* Setiap lapisan dalam jaringan saraf mengekstraksi tingkat abstraksi yang berbeda: dari fitur dasar lokal (gradien, tepi) hingga representasi semantik holistik tingkat tinggi.
* Teorema Aproksimasi Universal membuktikan secara analitis bahwa jaringan saraf dengan aktivasi non-linier memiliki kapasitas matematis untuk mengaproksimasi sembarang fungsi kontinu berdimensi tinggi.
* Operasi dasar deep learning bertumpu pada aljabar linier tensor (perkalian matriks dan penjumlahan bias) yang dipadukan dengan fungsi aktivasi non-linier elemen-demi-elemen.
* Keberhasilan aplikasi deep learning di agro-industri mensyaratkan normalisasi fitur yang ketat, pencegahan data leakage spasial, dan pemilihan kapasitas model yang proporsional terhadap volume data lapangan.

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Analisis Komposisi Fungsi (Bloom C4)**: Misalkan sebuah jaringan saraf tiruan dirancang dengan 5 lapisan tersembunyi, di mana setiap lapisan hanya menggunakan transformasi linier $z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}$ tanpa menyertakan fungsi aktivasi non-linier. Buktikan secara aljabar linier mengapa jaringan bertingkat 5 tersebut ekuivalen secara matematis dengan satu lapisan regresi linier tunggal!
2. **Evaluasi Teorema Universal (Bloom C5)**: Sebuah tim riset perkebunan mengklaim bahwa karena Teorema Aproksimasi Universal berlaku untuk 1 hidden layer yang sangat lebar, maka industri agrikultur tidak membutuhkan arsitektur dalam (*deep architectures*). Berikan sanggahan kritis dan analitis terhadap klaim tersebut dengan meninjau efisiensi parameter dan kompleksitas sampel data!

### Tugas Pemrograman Mandiri
Rancang sebuah skrip Python menggunakan pustaka NumPy untuk membandingkan kapasitas aproksimasi antara model linier sederhana ($y = wx + b$) dengan model dua lapis non-linier ($y = W_2 \tanh(W_1 x + b_1) + b_2$) pada fungsi dinamika klorofil tanaman:
$$f(x) = \exp(-0.5 x) \cdot \sin(3x) + 0.1 x^2$$
Plot kurva perbandingan prediksi kedua model terhadap data aktual dan hitung perbandingan nilai *Mean Squared Error* (MSE) keduanya!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 9.2: Artificial Neural Network (ANN)

Pada modul ini, kita telah memahami paradigma komputasi deep learning dan bagaimana fitur dipelajari secara bertingkat dari data mentah. Namun, bagaimana komponen-komponen lapisan komputasi tersebut diorganisasi secara formal ke dalam suatu jaringan lengkap? 

Pada **AI Modul 9.2: Artificial Neural Network (ANN)**, kita akan melangkah lebih jauh membedah arsitektur formal **Multi-Layer Perceptron (MLP)**. Kita akan mendalami struktur *Input Layer*, *Hidden Layers*, dan *Output Layer*, merumuskan notasi tensor baku bobot dan bias, serta memformulasikan mekanisme propagasi maju (*forward propagation*) dalam notasi aljabar linier matriks yang teroptimasi secara komputasional.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. (Bab 1: Pengantar dan Latar Belakang Komputasi).
2. Cybenko, G. (1989). *Approximation by superpositions of a sigmoidal function*. Mathematics of Control, Signals and Systems, 2(4), 303-314.
3. Hornik, K., Stinchcombe, M., & White, H. (1989). *Multilayer feedforward networks are universal approximators*. Neural Networks, 2(5), 359-366.
4. LeCun, Y., Bengio, Y., & Hinton, G. (2015). *Deep learning*. Nature, 521(7553), 436-444.
5. Kamilaris, A., & Prenafeta-Boldú, F. X. (2018). *Deep learning in agriculture: A survey*. Computers and Electronics in Agriculture, 147, 70-90.
"""
    validate_text(md_content, "AI_Modul_9.1_Konsep_Deep_Learning.md")
    with open("docs/part-09/AI_Modul_9.1_Konsep_Deep_Learning.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-09/AI_Modul_9.1_Konsep_Deep_Learning.md")

    # Notebook 9.1
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 9.1: Praktikum Konsep Deep Learning\n",
                    "**Mata Kuliah:** Kecerdasan Buatan Terapan & Deep Learning  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Memahami perbedaan mendasar antara representasi linier dangkal (*shallow*) dan representasi hierarkis (*deep*).\n",
                    "2. Mengimplementasikan ekstraksi fitur hierarkis bertingkat menggunakan aljabar matriks NumPy murni.\n",
                    "3. Mendemonstrasikan Teorema Aproksimasi Universal untuk mendekati fungsi non-linier kompleks sensor tanaman.\n",
                    "4. Menganalisis efisiensi komputasi dan perilaku aproksimasi pada variasi kapasitas lapisan tersembunyi.\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "# Konfigurasi visualisasi\n",
                    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                    "print(f'NumPy Version: {np.__version__}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Simulasi Fitur Sensor Tanaman dan Ekstraksi Hierarkis\n",
                    "Membuat representasi sensor 8 kanal (pantulan spektral kanopi kelapa sawit) dan mengekstraksi representasi fitur laten melalui transformasi bertingkat."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "np.random.seed(42)\n",
                    "n_samples = 100\n",
                    "n_channels = 8  # 8 panjang gelombang spektral\n",
                    "\n",
                    "# Data spektral sintetik daun sawit [0.0 - 1.0]\n",
                    "X_raw = np.random.uniform(0.1, 0.9, size=(n_samples, n_channels))\n",
                    "\n",
                    "# Definisi bobot 2 lapisan ekstraksi fitur\n",
                    "W1 = np.random.randn(16, n_channels) * np.sqrt(2.0 / n_channels)\n",
                    "b1 = np.zeros((1, 16))\n",
                    "W2 = np.random.randn(8, 16) * np.sqrt(2.0 / 16)\n",
                    "b2 = np.zeros((1, 8))\n",
                    "\n",
                    "# Forward pass ekstraksi fitur hierarkis\n",
                    "def relu(z):\n",
                    "    return np.maximum(0, z)\n",
                    "\n",
                    "H1 = relu(np.dot(X_raw, W1.T) + b1)  # Fitur representasi rendah\n",
                    "H2 = relu(np.dot(H1, W2.T) + b2)     # Fitur representasi tinggi\n",
                    "\n",
                    "print('Dimensi data masukan mentah :', X_raw.shape)\n",
                    "print('Dimensi representasi lapisan 1:', H1.shape)\n",
                    "print('Dimensi representasi lapisan 2:', H2.shape)\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Uji Teorema Aproksimasi Universal (Universal Approximation Theorem)\n",
                    "Mendemonstrasikan kemampuan jaringan saraf 1 lapisan tersembunyi dengan aktivasi non-linier dalam mengaproksimasi fungsi respon klorofil non-linier."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Membuat fungsi non-linier target agronomis\n",
                    "X_val = np.linspace(-3, 3, 200).reshape(-1, 1)\n",
                    "y_true = np.sin(2.5 * X_val) + 0.4 * np.cos(X_val) + 0.15 * X_val**2\n",
                    "\n",
                    "class UniversalApproximator:\n",
                    "    def __init__(self, n_hidden=32, lr=0.03):\n",
                    "        np.random.seed(42)\n",
                    "        self.W1 = np.random.randn(n_hidden, 1) * 0.5\n",
                    "        self.b1 = np.zeros((1, n_hidden))\n",
                    "        self.W2 = np.random.randn(1, n_hidden) * 0.5\n",
                    "        self.b2 = np.zeros((1, 1))\n",
                    "        self.lr = lr\n",
                    "        \n",
                    "    def fit(self, X, y, epochs=1500):\n",
                    "        m = X.shape[0]\n",
                    "        history = []\n",
                    "        for ep in range(epochs):\n",
                    "            # Forward\n",
                    "            Z1 = np.dot(X, self.W1.T) + self.b1\n",
                    "            A1 = np.tanh(Z1)\n",
                    "            y_hat = np.dot(A1, self.W2.T) + self.b2\n",
                    "            \n",
                    "            loss = np.mean((y_hat - y)**2)\n",
                    "            history.append(loss)\n",
                    "            \n",
                    "            # Backward\n",
                    "            dy = 2 * (y_hat - y) / m\n",
                    "            dW2 = np.dot(dy.T, A1)\n",
                    "            db2 = np.sum(dy, axis=0, keepdims=True)\n",
                    "            \n",
                    "            dA1 = np.dot(dy, self.W2)\n",
                    "            dZ1 = dA1 * (1 - A1**2)\n",
                    "            dW1 = np.dot(dZ1.T, X)\n",
                    "            db1 = np.sum(dZ1, axis=0, keepdims=True)\n",
                    "            \n",
                    "            # Gradient update\n",
                    "            self.W2 -= self.lr * dW2\n",
                    "            self.b2 -= self.lr * db2\n",
                    "            self.W1 -= self.lr * dW1\n",
                    "            self.b1 -= self.lr * db1\n",
                    "        return history\n",
                    "        \n",
                    "    def predict(self, X):\n",
                    "        Z1 = np.dot(X, self.W1.T) + self.b1\n",
                    "        A1 = np.tanh(Z1)\n",
                    "        return np.dot(A1, self.W2.T) + self.b2\n",
                    "\n",
                    "model = UniversalApproximator(n_hidden=48, lr=0.03)\n",
                    "loss_history = model.fit(X_val, y_true, epochs=2000)\n",
                    "y_pred = model.predict(X_val)\n",
                    "rmse = np.sqrt(np.mean((y_pred - y_true)**2))\n",
                    "print(f'Training Selesai! Final RMSE: {rmse:.4f}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Hasil Aproksimasi dan Kurva Konvergensi\n",
                    "Menampilkan hasil kurva estimasi model neural network dibandingkan dengan kurva non-linier target aktual."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
                    "\n",
                    "ax1.plot(X_val, y_true, label='Fungsi Aktual Tanaman (Ground Truth)', color='black', linewidth=2.5)\n",
                    "ax1.plot(X_val, y_pred, label=f'Aproksimasi Jaringan Saraf (RMSE: {rmse:.4f})', color='crimson', linestyle='--', linewidth=2)\n",
                    "ax1.set_title('Aproksimasi Fungsi Non-Linier Sensor Kanopi', fontsize=12, fontweight='bold')\n",
                    "ax1.set_xlabel('Variabel Prediktor Terstandarisasi', fontsize=10)\n",
                    "ax1.set_ylabel('Respons Klorofil', fontsize=10)\n",
                    "ax1.legend()\n",
                    "\n",
                    "ax2.plot(loss_history, color='teal', linewidth=2)\n",
                    "ax2.set_title('Dinamika Konvergensi Loss (MSE)', fontsize=12, fontweight='bold')\n",
                    "ax2.set_xlabel('Epoch Iterasi', fontsize=10)\n",
                    "ax2.set_ylabel('Mean Squared Error', fontsize=10)\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_aproksimasi_9_1.png', dpi=150)\n",
                    "plt.show()\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open("notebooks/part-09/AI_Modul_9.1_Praktikum_Konsep_Deep_Learning.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-09/AI_Modul_9.1_Praktikum_Konsep_Deep_Learning.ipynb")

    # Guide 9.1
    guide_content = """# AI Modul 9.1: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-09-01
* **Topik Utama**: Konsep Fundamental Deep Learning & Hierarchical Feature Learning
* **Alokasi Waktu**: 150 Menit (50 Menit Kuliah Interaktif, 70 Menit Praktikum Terbimbing, 30 Menit Diskusi & Evaluasi)
* **Bahan Ajar & Alat**: Slide Presentasi Konsep, Diktat Teori Modul 9.1, Jupyter Notebook Praktikum, Proyektor, Komputer Praktikum dengan Lingkungan Python 3.10.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 20**: Pengantar paradima komputasi kecerdasan buatan: perbedaan mendasar machine learning klasik vs deep learning. Pembahasan studi kasus kegagalan ekstraksi fitur manual pada citra perkebunan skala luas.
* **Menit 20 - 50**: Landasan matematis Teorema Aproksimasi Universal, formulasi komposisi fungsi bertingkat, dan representasi tensor multi-dimensi.
* **Menit 50 - 120**: Praktikum hands-on di laboratorium: menjalankan implementasi ekstraksi fitur bertingkat dan menguji model aproksimator non-linier menggunakan NumPy murni.
* **Menit 120 - 150**: Pembahasan kesalahan umum (*pitfalls*), evaluasi kuis formatif, dan pengantar modul berikutnya (Artificial Neural Network).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teori Komparasi** | Mampu membedakan representasi fitur manual vs otomatis secara terperinci dengan contoh agronomis konkret. | Mampu menjelaskan konsep dasar perbedaan model dangkal dan dalam, namun minim elaborasi teknis. | Gagal membedakan mekanisme kerja machine learning klasik dan deep learning. |
| **Implementasi NumPy** | Mampu menyusun skrip ekstraksi fitur multi-lapisan tanpa error dengan aljabar linier yang efisien. | Mampu menjalankan skrip praktikum namun kesulitan memodifikasi dimensi matriks bobot. | Menghasilkan galat dimensi tensor (*shape mismatch*) tanpa mampu melakukan debugging mandiri. |
| **Analisis Hasil Aproksimasi** | Menginterpretasi kurva aproksimasi dan nilai RMSE secara kuantitatif serta mengaitkannya dengan kapasitas arsitektur. | Menghitung nilai RMSE akhir namun analisis kurva visual masih bersifat umum. | Tidak mampu menyimpulkan konvergensi fungsi dan makna dari nilai loss. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Komposisi Linier
Secara matematis, output dari lapisan linier pertama adalah:
$$a^{(1)} = W^{(1)} x + b^{(1)}$$
Lapisan kedua:
$$a^{(2)} = W^{(2)} a^{(1)} + b^{(2)} = W^{(2)} (W^{(1)} x + b^{(1)}) + b^{(2)} = (W^{(2)} W^{(1)}) x + (W^{(2)} b^{(1)} + b^{(2)})$$
Jika didefinisikan matriks gabungan $W' = W^{(2)} W^{(1)}$ dan vektor bias gabungan $b' = W^{(2)} b^{(1)} + b^{(2)}$, maka:
$$a^{(2)} = W' x + b'$$
Dengan induksi matematika hingga lapisan ke-$L$, seluruh perkalian matriks bobot berurutan dapat diringkas menjadi sebuah matriks linier tunggal:
$$W_{\text{net}} = W^{(L)} W^{(L-1)} \dots W^{(1)} \quad \text{dan} \quad b_{\text{net}} = \sum_{l=1}^{L} \left( \prod_{j=l+1}^{L} W^{(j)} \right) b^{(l)}$$
Dengan demikian, susunan lapisan linier bertingkat tanpa fungsi aktivasi non-linier tidak mampu meningkatkan kapasitas representasi ruang hipotesis dan secara aljabar tereduksi menjadi regresi linier biasa.

### Jawaban Soal Konseptual 2: Kedalaman vs Lebar
Klaim tersebut tidak tepat secara praktis. Meskipun Teorema Aproksimasi Universal membuktikan keberadaan eksistensi aproksimator 1 lapisan tersembunyi, teorema tersebut tidak memberikan jaminan mengenai efisiensi jumlah neuron ($N$). Untuk fungsi non-linier kompleks dan berdimensi tinggi ($d$), jumlah neuron pada 1 lapisan tersembunyi dapat membengkak secara eksponensial ($O(2^d)$). Sebaliknya, arsitektur dalam (*deep architectures*) memanfaatkan hierarki komposisionalitas (*compositionality*), di mana fitur tingkat tinggi dibangun dari kombinasi fitur tingkat rendah, sehingga mereduksi jumlah parameter yang dibutuhkan menjadi polinomial serta meningkatkan generalisasi pada data lingkungan terbuka.
"""
    validate_text(guide_content, "AI_Modul_9.1_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-09/AI_Modul_9.1_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-09/AI_Modul_9.1_Panduan_Instruktur_dan_Kunci_Solusi.md")

if __name__ == '__main__':
    create_modul_9_1()
