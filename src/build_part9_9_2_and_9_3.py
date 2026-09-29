import os
import json
import re

BANNED_WORDS = ['taksonomi', 'tripartit', 'ontologis', 'epistemologis', 'dialektika', 'manifestasi dependensi', 'de facto']

def validate_text(text, filename):
    lower = text.lower()
    for w in BANNED_WORDS:
        if w in lower:
            raise ValueError(f"BANNED WORD FOUND in {filename}: '{w}'")
    print(f"[VALIDATED] 0 banned words in {filename}")

# ==============================================================================
# MODUL 9.2: Artificial Neural Network (ANN)
# ==============================================================================
def create_modul_9_2():
    md_content = """# AI Modul 9.2: Artificial Neural Network (ANN)

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-09-02
* **Mata Kuliah**: Kecerdasan Buatan Terapan & Deep Learning (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Ganjil)
* **Prasyarat**: AI Modul 9.1 (Konsep Deep Learning)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pemodelan Matriks Bobot W & Bias b, Skrip Vectorized Forward Pass, Visualisasi Ruang Laten"] --> B["OUTCOMES: Kemampuan Merancang & Mengimplementasikan Arsitektur Multi-Layer Perceptron"]
    B --> C["IMPACTS: Solusi Otomasi Klasifikasi Kesesuaian Lahan & Karakterisasi Tanah Presisi"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** arsitektur komputasi Multi-Layer Perceptron (MLP) yang terdiri dari lapisan masukan (*input layer*), lapisan tersembunyi (*hidden layers*), dan lapisan keluaran (*output layer*).
2. **Menerapkan (C3)** representasi aljabar linier dalam formulasi propagasi maju (*vectorized forward propagation*) menggunakan matriks bobot, vektor bias, dan fungsi aktivasi non-linier dengan pustaka NumPy.
3. **Menganalisis (C4)** transformasi ruang fitur berdimensi tinggi menuju ruang representasi laten (*latent feature space*) dalam mengatasi permasalahan pemisahan non-linier pada evaluasi kesesuaian lahan perkebunan.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan notasi matematis baku untuk tensor bobot antar-lapisan $W^{[l]}$, vektor bias $b^{[l]}$, dan vektor aktivasi $a^{[l]}$.
  * Skrip modul Python terstruktur untuk eksekusi propagasi maju tervektorisasi pada sekumpulan data batch.
  * Visualisasi garis batas keputusan (*decision boundary*) non-linier pada ruang fitur tanah perkebunan.
* **Outcomes (Kompetensi Aplikatif)**:
  * Kemampuan menentukan dimensi dan konfigurasi lapisan neural network berdasarkan struktur data tabel sensorik agrokompleks.
  * Keahlian dalam memetakan interaksi non-linier antar-parameter fisikokimia tanah terhadap produktivitas tanaman.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Peningkatan akurasi pemetaan kesesuaian lahan untuk ekspansi dan peremajaan (*replanting*) kebun kelapa sawit secara terukur dan berkelanjutan.

---

## 2. Profil Fundamental Artificial Neural Network: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Artificial Neural Network (ANN) tipe Multi-Layer Perceptron adalah model komputasi terarah (*feedforward*) yang memetakan masukan $x \in \mathbb{R}^{n_x}$ menjadi keluaran $\hat{y} \in \mathbb{R}^{n_y}$ melalui serangkaian lapisan pemrosesan paralel:
1. **Transformasi Afina Berantai**: Di setiap lapisan $l \in \{1, 2, \dots, L\}$, sinyal dari lapisan sebelumnya dikalikan dengan matriks bobot $W^{[l]}$ dan ditambahkan dengan vektor bias $b^{[l]}$:
   $$z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}$$
2. **Transformasi Non-Linier Elemen-demi-Elemen**: Sinyal pra-aktivasi $z^{[l]}$ ditransformasikan melalui fungsi aktivasi $\sigma^{[l]}$ untuk menghasilkan vektor aktivasi $a^{[l]}$:
   $$a^{[l]} = \sigma^{[l]}(z^{[l]})$$
   di mana $a^{[0]} = x$ adalah vektor masukan awal.
3. **Distribusi Probabilitas Keluaran**: Pada lapisan terakhir ($L$), keluaran ditransformasikan menjadi estimasi kontinu (regresi) atau probabilitas multikelas menggunakan fungsi Softmax.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Zonasi Kesesuaian Lahan Otomatis**: Memproses kombinasi data pH tanah, tekstur liat-pasir-debu, kapasitas tukar kation (KTK), ketebalan gambut, dan curah hujan untuk mengklasifikasikan kelas kesesuaian lahan (S1, S2, S3, N).
* **Prediksi Rendemen Minyak Sawit (CPO)**: Memetakan variabel pemupukan, umur tegakan pohon, dan curah hujan kumulatif terhadap rendemen ekstraksi pabrik kelapa sawit.
* **Estimasi Kebutuhan Dosis Pemupukan Presisi**: Merekomendasikan rekomendasi takaran N-P-K-Mg berbasis riwayat daun dan sifat tanah per blok perkebunan.

### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan
1. **Menangkap Interaksi Non-Linier Multi-Variabel**: Dalam agronomi tanah, pengaruh pH terhadap serapan nutrisi tidak bersifat linier terpisah, melainkan berinteraksi secara kompleks dengan kadar bahan organik dan kelembapan. ANN mampu memodelkan interaksi sinergis ini secara alami di lapisan tersembunyi.
2. **Kapasitas Generalisasi Tinggi pada Data Tabular & Sensorik**: Arsitektur *fully connected* memberikan fleksibilitas penuh bagi setiap neuron untuk menimbang kontribusi dari seluruh variabel input secara simultan.

### 2.4 Analisis Kelebihan dan Kekurangan (Tabel Komparasi)

| Aspek Komparasi | Regresi Multivariat Konvensional | Multi-Layer Perceptron (ANN) | Implikasi Agrokompleks |
| :--- | :--- | :--- | :--- |
| **Batas Keputusan** | Dibatasi oleh bidang datar hiperlinier (*linear hyperplane*). | Bidang batas keputusan lengkung non-linier sangat fleksibel. | Mampu memisahkan kelas tanah marginal yang memiliki ambang batas bersilangan. |
| **Interaksi Fitur** | Harus dirumuskan manual melalui perkalian suku (*interaction terms*). | Dipelajari secara otomatis oleh neuron-neuron di lapisan tersembunyi. | Memodelkan relasi tak terduga antara iklim mikro dan serapan pupuk. |
| **Kebutuhan Sampel** | Bekerja stabil pada sampel puluhan hingga ratusan. | Memerlukan data ratusan hingga ribuan sampel untuk konvergen optimal. | Perlu pengumpulan riwayat data kebun multi-musim. |
| **Kepekaan Penskalaan** | Cenderung tahan jika parameter dianalisis secara parsial. | Sangat sensitif terhadap skala data, wajib normalisasi ketat. | Wajib standarisasi seluruh variabel tanah sebelum inferensi. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Divisi Agronomi Perkebunan Kelapa Sawit mengumpulkan data dari 1.200 petak ukur tanah yang mencakup 6 parameter: pH, KTK, C-Organik, Rasio Pasir-Liat, Kedalaman Muka Air Tanah, dan Ketinggian Tempat. Tujuannya adalah mengklasifikasikan petak ukur ke dalam 3 kategori kesesuaian: Sangat Sesuai (S1), Cukup Sesuai (S2), dan Tidak Sesuai (N). Menggunakan Multi-Layer Perceptron dengan struktur $6 \rightarrow 16 \rightarrow 8 \rightarrow 3$, model mampu memetakan interaksi antara muka air tanah dangkal dan tekstur liat tinggi yang selama ini sulit dimodelkan secara linier.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Pemilihan Dimensi Hidden Layer**: Terlalu sedikit neuron menyebabkan *underfitting* (model gagal menangkap kompleksitas tanah), sedangkan terlalu banyak neuron memicu *overfitting* dan konsumsi memori berlebih.
2. **Inisialisasi Bobot yang Tepat**: Menginisialisasi seluruh bobot dengan angka nol akan menyebabkan simetri matematis (*symmetry breaking failure*), di mana seluruh neuron di lapisan yang sama menghitung gradien yang identik.

---

## 3. Landasan Teori & Konsep Matematis Artificial Neural Network

![Arsitektur Artificial Neural Network Multi-Layer Perceptron](../assets/arsitektur_artificial_neural_network_multi_layer_perceptron.png)

### 3.1 Notasi Baku Matematika Aljabar Linier
Untuk jaringan dengan $L$ lapisan:
* $n^{[l]}$ menyatakan jumlah neuron pada lapisan $l$, dengan $n^{[0]} = n_x$ (jumlah fitur masukan) dan $n^{[L]} = n_y$ (jumlah unit keluaran).
* $W^{[l]} \in \mathbb{R}^{n^{[l]} \times n^{[l-1]}}$ adalah matriks bobot yang menghubungkan lapisan $l-1$ ke lapisan $l$.
* $b^{[l]} \in \mathbb{R}^{n^{[l]} \times 1}$ adalah vektor bias untuk lapisan $l$.
* $z^{[l]} \in \mathbb{R}^{n^{[l]} \times 1}$ adalah vektor net input sebelum aktivasi pada lapisan $l$.
* $a^{[l]} \in \mathbb{R}^{n^{[l]} \times 1}$ adalah vektor aktivasi pasca-fungsi aktivasi pada lapisan $l$.

### 3.2 Formulasi Vektorisasi Batch (*Vectorized Batch Forward Propagation*)
Ketika memproses satu batch yang berisi $m$ sampel data perkebunan sekaligus, vektor-vektor kolom digabungkan menjadi matriks masukan $X \in \mathbb{R}^{m \times n^{[0]}}$ (di mana setiap baris mewakili satu sampel kebun). Formulasi propagasi maju untuk seluruh sampel dirumuskan sebagai berikut:

$$Z^{[l]} = A^{[l-1]} (W^{[l]})^\top + \mathbf{1}_m (b^{[l]})^\top$$

$$A^{[l]} = \sigma^{[l]}(Z^{[l]})$$

di mana:
* $A^{[0]} = X \in \mathbb{R}^{m \times n^{[0]}}$
* $Z^{[l]} \in \mathbb{R}^{m \times n^{[l]}}$
* $A^{[l]} \in \mathbb{R}^{m \times n^{[l]}}$
* $\mathbf{1}_m$ adalah vektor kolom berukuran $m \times 1$ yang seluruh elemennya bernilai $1$.

### 3.3 Transformasi Ruang Fitur Menuju Ruang Laten (*Latent Space*)
Secara geometris, setiap lapisan tersembunyi melakukan distorsi dan rotasi non-linier terhadap ruang masukan. Jika data tanah pada ruang awal $\mathbb{R}^2$ atau $\mathbb{R}^6$ tidak dapat dipisahkan oleh bidang datar (*non-linearly separable*), lapisan tersembunyi memetakan titik-titik sampel tersebut ke dalam ruang laten berdimensi baru di mana batas pemisah antar-kelas menjadi linier (*linearly separable*).

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Batch Input X: Matriks m x n[0]"] --> B["Lapisan 1: Z1 = X * W1.T + b1"]
    B --> C["Aktivasi 1: A1 = ReLU(Z1)"]
    C --> D["Lapisan 2: Z2 = A1 * W2.T + b2"]
    D --> E["Aktivasi 2: A2 = ReLU(Z2)"]
    E --> F["Lapisan Output: Z3 = A2 * W3.T + b3"]
    F --> G["Softmax: P(y=k|X) = exp(Z3_k) / sum(exp(Z3))"]
```

Implementasi Multi-Layer Perceptron berorientasi objek menggunakan NumPy murni:

```python
import numpy as np

class MultiLayerPerceptron:
    def __init__(self, layer_dims, seed=42):
        np.random.seed(seed)
        self.layer_dims = layer_dims
        self.num_layers = len(layer_dims) - 1
        self.parameters = {}
        
        # Inisialisasi bobot He (Kaiming) dan bias nol
        for l in range(1, len(layer_dims)):
            self.parameters[f'W{l}'] = np.random.randn(layer_dims[l], layer_dims[l-1]) * np.sqrt(2.0 / layer_dims[l-1])
            self.parameters[f'b{l}'] = np.zeros((1, layer_dims[l]))
            
    def relu(self, Z):
        return np.maximum(0, Z)
        
    def softmax(self, Z):
        # Penanganan kestabilan numerik dengan mengurangi nilai maksimum per baris
        exp_Z = np.exp(Z - np.max(Z, axis=1, keepdims=True))
        return exp_Z / np.sum(exp_Z, axis=1, keepdims=True)
        
    def forward(self, X):
        cache = {'A0': X}
        A = X
        
        # Lapisan tersembunyi dengan aktivasi ReLU
        for l in range(1, self.num_layers):
            W = self.parameters[f'W{l}']
            b = self.parameters[f'b{l}']
            Z = np.dot(A, W.T) + b
            A = self.relu(Z)
            cache[f'Z{l}'] = Z
            cache[f'A{l}'] = A
            
        # Lapisan keluaran dengan aktivasi Softmax
        W_out = self.parameters[f'W{self.num_layers}']
        b_out = self.parameters[f'b{self.num_layers}']
        Z_out = np.dot(A, W_out.T) + b_out
        A_out = self.softmax(Z_out)
        cache[f'Z{self.num_layers}'] = Z_out
        cache[f'A{self.num_layers}'] = A_out
        
        return A_out, cache

# Inisialisasi arsitektur: 6 fitur tanah -> 12 neuron (H1) -> 8 neuron (H2) -> 3 kelas kesesuaian
mlp_model = MultiLayerPerceptron(layer_dims=[6, 12, 8, 3])
X_dummy = np.random.randn(10, 6) # 10 sampel petak ukur tanah
probas, cache = mlp_model.forward(X_dummy)

print("Bentuk Matriks Probabilitas Output :", probas.shape)
print("Jumlah Probabilitas Baris Pertama  :", np.sum(probas[0]))
print("Prediksi Kelas Terbesar Baris 1    :", np.argmax(probas[0]))
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Klasifikasi Kesesuaian Lahan Sawit

### 5.1 Karakteristik Dataset Tanah Perkebunan
Dataset mencakup 4 parameter fisikokimia utama:
1. $x_1$: Derajat Keasaman Tanah (pH) [$4.0 - 6.5$]
2. $x_2$: Kapasitas Tukar Kation (KTK, meq/100g) [$8.0 - 28.0$]
3. $x_3$: Kandungan C-Organik (%) [$0.8 - 4.5$]
4. $x_4$: Kejenuhan Basa (%) [$15.0 - 65.0$]

Target keluaran dibagi menjadi 3 kelas:
* Kelas 0: S1 (Sangat Sesuai - produksi $> 25$ ton TBS/ha/thn)
* Kelas 1: S2 (Cukup Sesuai - produksi $18 - 25$ ton TBS/ha/thn)
* Kelas 2: S3/N (Marginal/Tidak Sesuai - produksi $< 18$ ton TBS/ha/thn)

### 5.2 Evaluasi Komparasi Batas Keputusan Non-Linier
```python
# Simulasi pembangkitan data tanah sintetis dengan batas non-linier
np.random.seed(42)
N_per_class = 150
# Kelas 0: pH optimal & KTK tinggi
c0 = np.random.multivariate_normal([5.5, 22.0], [[0.2, 0.1], [0.1, 4.0]], N_per_class)
# Kelas 1: pH sedang & KTK sedang
c1 = np.random.multivariate_normal([4.8, 15.0], [[0.2, -0.1], [-0.1, 3.0]], N_per_class)
# Kelas 2: pH masam ekstrem / KTK rendah
c2 = np.random.multivariate_normal([4.2, 9.0], [[0.15, 0.05], [0.05, 2.5]], N_per_class)

X_soil = np.vstack([c0, c1, c2])
y_soil = np.array([0]*N_per_class + [1]*N_per_class + [2]*N_per_class)

# Standarisasi Z-score
X_soil_std = (X_soil - np.mean(X_soil, axis=0)) / np.std(X_soil, axis=0)

# MLP Model Evaluasi
model_soil = MultiLayerPerceptron(layer_dims=[2, 8, 4, 3])
probs, _ = model_soil.forward(X_soil_std)
preds = np.argmax(probs, axis=1)

print(f"Total Sampel Tanah Dievaluasi : {len(y_soil)}")
print(f"Bentuk Matriks Bobot Lapisan 1: {model_soil.parameters['W1'].shape}")
print(f"Distribusi Prediksi Awal     : {np.bincount(preds)}")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Mengabaikan Penanganan Overflow pada Softmax**: Menghitung $\exp(z_i)$ secara langsung tanpa mengurangi nilai maksimum $\max(z)$ dapat memicu nilai *Infinity* atau `NaN` ketika nilai $z_i$ besar.
2. **Bobot Diinisialisasi Identik**: Mengisi seluruh bobot dengan nilai konstanta sama menyebabkan setiap neuron tersembunyi memiliki aktivasi dan pembaruan gradien yang identik (*symmetry failure*).
3. **Data Leakage dalam Penskalaan**: Menghitung rata-rata dan deviasi standar penskalaan pada keseluruhan dataset (gabungan train dan test) sebelum proses pemisahan.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Inisialisasi Kaiming/He atau Xavier/Glorot**: Gunakan varians inisialisasi $\text{Var}(W) = \frac{2}{n_{\text{in}}}$ untuk lapisan dengan aktivasi ReLU guna menjaga kestabilan magnitudo sinyal antar-lapisan.
2. **Penskalaan Data Berdasarkan Training Set**: Hitung $\mu_{\text{train}}$ dan $\sigma_{\text{train}}$ hanya dari data latih, lalu terapkan parameter tersebut pada data uji dan data operasional baru.
3. **Penyusunan Arsitektur Piramida Terbalik**: Secara umum, konfigurasi jumlah neuron yang berkurang secara bertahap dari lapisan input menuju output (misalnya $64 \rightarrow 32 \rightarrow 16 \rightarrow C$) membantu jaringan mengompresi representasi secara elegan.

---

## 7. Rangkuman Modul

* Artificial Neural Network Multi-Layer Perceptron (MLP) memperluas kapasitas model linier melalui susunan lapisan tersembunyi dengan fungsi aktivasi non-linier.
* Notasi tensor baku memfasilitasi formulasi propagasi maju secara tervektorisasi: $Z^{[l]} = A^{[l-1]} (W^{[l]})^\top + \mathbf{1} (b^{[l]})^\top$ dan $A^{[l]} = \sigma(Z^{[l]})$.
* Lapisan tersembunyi berfungsi sebagai pemeta ruang fitur masukan ke dalam ruang representasi laten yang memungkinkan pemisahan kelas non-linier yang rumit.
* Kestabilan numerik fungsi Softmax pada lapisan keluaran wajib dijaga melalui teknik pergeseran skalar (*log-sum-exp stabilization trick*).

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Analisis Dimensi Tensor (Bloom C3)**: Sebuah jaringan saraf tiruan dirancang untuk memproses data sensorik kebun dengan 10 variabel prediktor. Jaringan memiliki 2 lapisan tersembunyi masing-masing berukuran 32 neuron dan 16 neuron, serta 4 kelas keluaran. Jika ukuran mini-batch yang dialirkan adalah $m = 64$ sampel, tentukan dimensi eksak dari:
   * Matriks $X$, $W^{[1]}$, $b^{[1]}$, dan $Z^{[1]}$
   * Matriks $W^{[2]}$, $b^{[2]}$, dan $A^{[2]}$
   * Matriks $W^{[3]}$, $b^{[3]}$, dan $A^{[3]}$!
2. **Analisis Simetri Bobot (Bloom C4)**: Jelaskan secara matematis apa yang terjadi jika seluruh bobot pada lapisan tersembunyi diinisialisasi dengan angka yang persis sama (misalnya $0.5$)! Mengapa fenomena ini melumpuhkan kapasitas multi-neuron pada MLP?

### Tugas Pemrograman Mandiri
Lengkapi kode kelas `MultiLayerPerceptron` agar mampu menerima argumen aktivasi yang fleksibel (`'relu'`, `'tanh'`, atau `'sigmoid'`) pada setiap lapisan tersembunyi. Jalankan pengujian pada dataset tanah sintetis dan hitung waktu komputasi (*latency*) forward pass untuk 10.000 sampel!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 9.3: Struktur Neuron

Kita telah memahami bagaimana kumpulan neuron diorganisasi ke dalam lapisan-lapisan Multi-Layer Perceptron untuk memproses data secara simultan. Namun, bagaimana sesungguhnya cara kerja sebuah unit komputasi terkecil tersebut? 

Pada **AI Modul 9.3: Struktur Neuron**, kita akan membedah secara mendalam **anatomi neuron komputasional**, membandingkannya dengan neuron biologis manusia, menelusuri model seminal McCulloch-Pitts dan Perceptron Rosenblatt, serta mengkaji secara analitis batas kemampuan matematis sebuah neuron tunggal dalam menghadapi gerbang logika non-linier XOR.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. (Bab 6: Deep Feedforward Networks).
2. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. (Bab 5: Neural Networks).
3. He, K., Zhang, X., Ren, S., & Sun, J. (2015). *Delving deep into rectifiers: Surpassing human-level performance on ImageNet classification*. Proceedings of the IEEE International Conference on Computer Vision, 1026-1034.
4. Glorot, X., & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. Proceedings of the Thirteenth International Conference on Artificial Intelligence and Statistics, 249-256.
"""
    validate_text(md_content, "AI_Modul_9.2_Artificial_Neural_Network.md")
    with open("docs/part-09/AI_Modul_9.2_Artificial_Neural_Network.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-09/AI_Modul_9.2_Artificial_Neural_Network.md")

    # Notebook 9.2
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 9.2: Praktikum Artificial Neural Network (ANN)\n",
                    "**Mata Kuliah:** Kecerdasan Buatan Terapan & Deep Learning  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Membangun kelas arsitektur Multi-Layer Perceptron (MLP) tervektorisasi menggunakan NumPy murni.\n",
                    "2. Mengimplementasikan inisialisasi bobot He (Kaiming) dan propagasi maju terstruktur.\n",
                    "3. Menguji aktivasi Softmax dengan stabilisasi numerik pada data evaluasi kesesuaian lahan kelapa sawit.\n",
                    "4. Memvisualisasikan batas keputusan dan menganalisis representasi ruang laten.\n"
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
                    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                    "print(f'NumPy Version: {np.__version__}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Pembangkitan Data Sintetis Sifat Tanah dan Kesesuaian Lahan\n",
                    "Mensimulasikan 400 sampel petak tanah perkebunan dengan dua fitur utama: Derajat Keasaman Tanah (pH) dan Kapasitas Tukar Kation (KTK)."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "np.random.seed(42)\n",
                    "n_per_class = 120\n",
                    "\n",
                    "# Kelas 0: S1 (Sangat Sesuai)\n",
                    "c0 = np.random.multivariate_normal([5.8, 22.0], [[0.15, 0.1], [0.1, 3.0]], n_per_class)\n",
                    "# Kelas 1: S2 (Cukup Sesuai)\n",
                    "c1 = np.random.multivariate_normal([5.0, 15.0], [[0.2, -0.05], [-0.05, 2.5]], n_per_class)\n",
                    "# Kelas 2: S3/N (Marginal/Tidak Sesuai)\n",
                    "c2 = np.random.multivariate_normal([4.3, 9.0], [[0.15, 0.05], [0.05, 2.0]], n_per_class)\n",
                    "\n",
                    "X_raw = np.vstack([c0, c1, c2])\n",
                    "y_true = np.array([0]*n_per_class + [1]*n_per_class + [2]*n_per_class)\n",
                    "\n",
                    "# Standarisasi Fitur\n",
                    "X_std = (X_raw - np.mean(X_raw, axis=0)) / np.std(X_raw, axis=0)\n",
                    "\n",
                    "print('Bentuk Matriks Fitur Tanah:', X_std.shape)\n",
                    "print('Distribusi Label Target   :', np.bincount(y_true))\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Implementasi Kelas Multi-Layer Perceptron (Pure NumPy)\n",
                    "Membangun kelas jaringan saraf dengan konfigurasi lapisan fleksibel, aktivasi ReLU tersembunyi, dan Softmax keluaran."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "class MultiLayerPerceptron:\n",
                    "    def __init__(self, layer_dims, seed=42):\n",
                    "        np.random.seed(seed)\n",
                    "        self.layer_dims = layer_dims\n",
                    "        self.num_layers = len(layer_dims) - 1\n",
                    "        self.parameters = {}\n",
                    "        \n",
                    "        for l in range(1, len(layer_dims)):\n",
                    "            # Inisialisasi He (Kaiming)\n",
                    "            self.parameters[f'W{l}'] = np.random.randn(layer_dims[l], layer_dims[l-1]) * np.sqrt(2.0 / layer_dims[l-1])\n",
                    "            self.parameters[f'b{l}'] = np.zeros((1, layer_dims[l]))\n",
                    "            \n",
                    "    def relu(self, Z):\n",
                    "        return np.maximum(0, Z)\n",
                    "        \n",
                    "    def softmax(self, Z):\n",
                    "        exp_Z = np.exp(Z - np.max(Z, axis=1, keepdims=True))\n",
                    "        return exp_Z / np.sum(exp_Z, axis=1, keepdims=True)\n",
                    "        \n",
                    "    def forward(self, X):\n",
                    "        A = X\n",
                    "        cache = {'A0': X}\n",
                    "        for l in range(1, self.num_layers):\n",
                    "            W = self.parameters[f'W{l}']\n",
                    "            b = self.parameters[f'b{l}']\n",
                    "            Z = np.dot(A, W.T) + b\n",
                    "            A = self.relu(Z)\n",
                    "            cache[f'Z{l}'] = Z\n",
                    "            cache[f'A{l}'] = A\n",
                    "            \n",
                    "        # Output layer\n",
                    "        W_out = self.parameters[f'W{self.num_layers}']\n",
                    "        b_out = self.parameters[f'b{self.num_layers}']\n",
                    "        Z_out = np.dot(A, W_out.T) + b_out\n",
                    "        A_out = self.softmax(Z_out)\n",
                    "        cache[f'Z{self.num_layers}'] = Z_out\n",
                    "        cache[f'A{self.num_layers}'] = A_out\n",
                    "        return A_out, cache\n",
                    "\n",
                    "model = MultiLayerPerceptron(layer_dims=[2, 8, 4, 3])\n",
                    "probs, cache = model.forward(X_std)\n",
                    "preds = np.argmax(probs, axis=1)\n",
                    "print(f'Forward pass berhasil dieksekusi! Output shape: {probs.shape}')\n",
                    "print('Contoh 3 estimasi probabilitas pertama:\\n', probs[:3])\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Sebaran Fitur Tanah dan Ruang Keputusan\n",
                    "Memetakan sebaran sampel tanah dan ruang klasifikasi kesesuaian lahan."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, ax = plt.subplots(figsize=(8, 6))\n",
                    "scatter = ax.scatter(X_std[:, 0], X_std[:, 1], c=y_true, cmap='viridis', edgecolors='k', s=60, alpha=0.85)\n",
                    "ax.set_title('Distribusi Karakteristik Tanah Perkebunan (pH vs KTK)', fontsize=12, fontweight='bold')\n",
                    "ax.set_xlabel('Derajat Keasaman Tanah (pH Terstandarisasi)', fontsize=10)\n",
                    "ax.set_ylabel('Kapasitas Tukar Kation (KTK Terstandarisasi)', fontsize=10)\n",
                    "legend1 = ax.legend(*scatter.legend_elements(), title='Kelas Lahan', loc='upper left')\n",
                    "ax.add_artist(legend1)\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_sebaran_tanah_9_2.png', dpi=150)\n",
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
    with open("notebooks/part-09/AI_Modul_9.2_Praktikum_Artificial_Neural_Network.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-09/AI_Modul_9.2_Praktikum_Artificial_Neural_Network.ipynb")

    # Guide 9.2
    guide_content = """# AI Modul 9.2: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-09-02
* **Topik Utama**: Artificial Neural Network & Multi-Layer Perceptron (MLP)
* **Alokasi Waktu**: 150 Menit (50 Menit Kuliah Teori, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 9.2, Jupyter Notebook Praktikum, Proyektor, Komputer Praktikum.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Penjelasan arsitektur formal MLP: Input Layer, Hidden Layer, Output Layer. Analogi pengolahan data tanah perkebunan.
* **Menit 25 - 50**: Formulasi aljabar linier tervektorisasi: matriks $W$, vektor $b$, notasi kurung siku berindeks lapisan, dan aktivasi Softmax dengan proteksi overflow.
* **Menit 50 - 120**: Praktikum komputer: implementasi kelas MLP berbasis NumPy murni, perancangan dimensi tensor, dan pengujian forward pass pada data kesesuaian lahan sawit.
* **Menit 120 - 150**: Asesmen formatif, evaluasi pemahaman simetri bobot, dan pemberian tugas terstruktur.

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Penguasaan Dimensi Tensor** | Menentukan dimensi matriks bobot dan vektor bias untuk setiap konfigurasi lapisan tanpa galat. | Mampu menghitung dimensi lapisan sederhana, namun ragu pada dimensi operasi batch masukan. | Sering mengalami galat ketidakcocokan bentuk matriks (*shape mismatch*). |
| **Koding Vectorized Forward** | Menulis fungsi propagasi maju berbasis perkalian matriks tervektorisasi yang bersih dan mangkus. | Menjalankan kode praktikum dengan baik namun kurang memahami penanganan overflow pada Softmax. | Menggunakan perulangan manual for-loop pada sampel data yang tidak tervektorisasi. |
| **Analisis Ruang Laten** | Menguraikan bagaimana transformasi non-linier memetakan fitur masukan menjadi representasi terpisah secara logis. | Menjelaskan fungsi aktivasi secara umum tanpa mengaitkannya dengan transformasi geometris. | Menganggap lapisan tersembunyi bekerja serupa dengan regresi linier bertumpuk. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Dimensi Tensor
Diketahui: $n^{[0]} = 10$, $n^{[1]} = 32$, $n^{[2]} = 16$, $n^{[3]} = 4$, ukuran batch $m = 64$.
1. **Lapisan Masukan & Lapisan 1**:
   * Matriks Masukan $X \in \mathbb{R}^{64 \times 10}$
   * Matriks Bobot $W^{[1]} \in \mathbb{R}^{32 \times 10}$
   * Vektor Bias $b^{[1]} \in \mathbb{R}^{1 \times 32}$ (atau $\mathbb{R}^{32 \times 1}$)
   * Matriks Net Input $Z^{[1]} = X (W^{[1]})^\top + b^{[1]} \in \mathbb{R}^{64 \times 32}$
2. **Lapisan Tersembunyi 2**:
   * Matriks Bobot $W^{[2]} \in \mathbb{R}^{16 \times 32}$
   * Vektor Bias $b^{[2]} \in \mathbb{R}^{1 \times 16}$
   * Matriks Aktivasi $A^{[2]} = \text{ReLU}(A^{[1]} (W^{[2]})^\top + b^{[2]}) \in \mathbb{R}^{64 \times 16}$
3. **Lapisan Keluaran (Lapisan 3)**:
   * Matriks Bobot $W^{[3]} \in \mathbb{R}^{4 \times 16}$
   * Vektor Bias $b^{[3]} \in \mathbb{R}^{1 \times 4}$
   * Matriks Probabilitas Keluaran $A^{[3]} = \text{Softmax}(A^{[2]} (W^{[3]})^\top + b^{[3]}) \in \mathbb{R}^{64 \times 4}$

### Jawaban Soal Konseptual 2: Analisis Simetri Bobot
Jika semua bobot diinisialisasi sama ($W_{ij} = c$), maka untuk setiap neuron $j$ dan $k$ pada lapisan tersembunyi yang sama:
$$z_j^{[1]} = \sum_{i} x_i c + b = z_k^{[1]}$$
Akibatnya, nilai aktivasi $a_j^{[1]} = \sigma(z_j^{[1]})$ akan persis sama dengan $a_k^{[1]}$. Pada fase backpropagation, gradien terhadap bobot $\frac{\partial L}{\partial W_{ji}^{[1]}}$ juga akan bernilai sama untuk seluruh neuron. Akibatnya, seluruh neuron tersembunyi akan terus diperbarui dengan nilai yang identik sepanjang iterasi training. Keberadaan 32 neuron tersembunyi tersebut secara matematis tidak lebih bermanfaat daripada memiliki 1 neuron tunggal, karena tidak terjadi pemecahan simetri (*symmetry breaking*). Inilah sebabnya inisialisasi acak berbobot kecil (*random initialization*) merupakan prasyarat mutlak.
"""
    validate_text(guide_content, "AI_Modul_9.2_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-09/AI_Modul_9.2_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-09/AI_Modul_9.2_Panduan_Instruktur_dan_Kunci_Solusi.md")

# ==============================================================================
# MODUL 9.3: Struktur Neuron
# ==============================================================================
def create_modul_9_3():
    md_content = """# AI Modul 9.3: Struktur Neuron

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-09-03
* **Mata Kuliah**: Kecerdasan Buatan Terapan & Deep Learning (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Ganjil)
* **Prasyarat**: AI Modul 9.2 (Artificial Neural Network)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pemodelan Matematika Neuron Komputasi, Skrip Single Perceptron, Visualisasi Hiperbidang Pemisah"] --> B["OUTCOMES: Pemahaman Mendalam Dinamika Pembelajaran Neuron & Keterbatasan Matematis Linier"]
    B --> C["IMPACTS: Pondasi Teoretis Kuat untuk Perancangan Sistem Pemilahan Komoditas Pertanian"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** analogi struktural dan fungsional antara neuron biologis (dendrit, soma, akson, sinapsis) dengan neuron komputasional (vektor masukan, bobot sinaptik, fungsi akumulator, bias, dan fungsi aktivasi).
2. **Menerapkan (C3)** aturan pembelajaran Perceptron (*Perceptron Learning Rule*) yang diperkenalkan oleh Frank Rosenblatt untuk mengklasifikasikan data biner dua dimensi secara iteratif menggunakan pustaka NumPy.
3. **Menganalisis (C4)** keterbatasan matematis pemisahan linier (*linear separability*) pada neuron tunggal serta membuktikan secara analitis kegagalan Perceptron dalam menyelesaikan persoalan gerbang logika non-linier XOR (Minsky & Papert, 1969).

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Pemahaman analitik komparasi model McCulloch-Pitts (1943) dan model Perceptron Rosenblatt (1958).
  * Skrip Python modular implementasi Single Perceptron dari dasar (*from scratch*) tanpa pustaka machine learning pihak ketiga.
  * Plot visual dinamis pergeseran garis pemisah (*separating hyperplane*) per iterasi *epoch*.
* **Outcomes (Kompetensi Aplikatif)**:
  * Kemampuan mengidentifikasi apakah suatu permasalahan pemilahan agro-industri bersifat *linearly separable* atau membutuhkan jaringan multi-neuron.
  * Keahlian merumuskan aturan pembaruan bobot berbasis sinyal galat diskrit.
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Pengetahuan fundamental yang mencegah praktisi perkebunan salah menerapkan arsitektur linier pada permasalahan biologi lapangan yang sarat dengan dinamika non-linier.

---

## 2. Profil Fundamental Struktur Neuron: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Neuron buatan (*artificial neuron*) adalah unit komputasi elementer yang meniru mekanisme kerja sel saraf biologis dalam memproses rangsangan:
1. **Penerimaan & Pembobotan Sinyal**: Menerima serangkaian sinyal masukan $x = (x_1, x_2, \dots, x_n)^\top$ di mana setiap jalur masukan dimodulasi oleh bobot sinaptik $w_i \in \mathbb{R}$.
2. **Akumulasi Spasial Net Input**: Menghitung kombinasi linier dari sinyal masukan terbobot dan menambahkan nilai ambang batas (*threshold*) internal berupa bias $b$:
   $$z = \sum_{i=1}^{n} w_i x_i + b = w^\top x + b$$
3. **Penembakan Potensial Aksi (*Activation Firing*)**: Menyalurkan sinyal net input $z$ ke dalam fungsi aktivasi $\phi(z)$ untuk menghasilkan keluaran biner $\hat{y} \in \{0, 1\}$ atau $\{-1, +1\}$:
   $$\hat{y} = \phi(z) = \begin{cases} 1, & \text{jika } z \ge 0 \\ 0, & \text{jika } z < 0 \end{cases}$$

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
Meskipun sederhana, neuron tunggal merupakan fondasi operasional bagi:
* **Sensor Biner Sortasi Mutu Sederhana**: Pemilahan biji kopi bermutu tinggi vs afkir berdasarkan rasio densitas dan pantulan cahaya merah-hijau yang terpisah secara linier.
* **Deteksi Ambang Batas Defisiensi Air**: Menentukan keputusan biner aktivasi katup irigasi tetes (*drip irrigation*) berdasarkan kombinasi pembacaan kadar air tanah dan suhu kanopi.

### 2.3 Rationale: Alasan Mengapa Materi Ini Dipelajari
Memahami struktur neuron tunggal adalah prasyarat untuk memahami cara kerja jaringan saraf yang lebih dalam. Kegagalan historis Perceptron dalam menyelesaikan persoalan gerbang logika non-linier XOR (yang memicu periode *AI Winter* pertama setelah buku Minsky & Papert terbit tahun 1969) memberikan wawasan fundamental mengenai mengapa arsitektur berlapis banyak (*multi-layer*) dengan aktivasi non-linier mutlak dibutuhkan dalam pemodelan data dunia nyata.

### 2.4 Analisis Kelebihan dan Kekurangan (Tabel Komparasi)

| Aspek Evaluasi | Model McCulloch-Pitts (1943) | Perceptron Rosenblatt (1958) | Multi-Layer Network Modern |
| :--- | :--- | :--- | :--- |
| **Tipe Bobot** | Bobot bernilai biner atau tetap, ditentukan secara manual. | Bobot kontinu riil yang dapat dipelajari secara otomatis (*learning rule*). | Bobot matriks multi-lapisan dipelajari via backpropagation. |
| **Mekanisme Belajar** | Tidak memiliki algoritma pembelajaran mandiri. | Algoritma koreksi galat (*error-correction learning rule*). | Gradient descent berbasis diferensiasi fungsi objektif. |
| **Kapasitas Pemisahan** | Hanya fungsi logika biner linier sederhana. | Terbatas pada pemisahan linier (*linear separability*). | Pemisahan non-linier kontinu sembarang (*universal*). |
| **Kelemahan Kritis** | Kaku, tidak dapat beradaptasi terhadap derau data. | Gagal total memecahkan masalah non-linier (XOR). | Kebutuhan komputasi dan data yang jauh lebih besar. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Sebuah stasiun pemilahan tandan buah sawit ingin memilah daun normal vs daun terserang hama ulat kantung berdasarkan dua indeks reflektansi: $x_1$ (pantulan pada 680 nm) dan $x_2$ (pantulan pada 800 nm). Jika kedua kelas tersebut dapat dipisahkan secara sempurna oleh garis lurus pada bidang $(x_1, x_2)$, maka Single Perceptron Rosenblatt terbukti secara matematis mampu menemukan garis pemisah tersebut dalam sejumlah iterasi terhingga (*Perceptron Convergence Theorem*).

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Teorema Konvergensi Perceptron**: Jika dataset bersifat *linearly separable*, algoritma Rosenblatt dijamin akan konvergen ke sebuah solusi bobot dalam sejumlah langkah terhingga. Namun jika data tidak dapat dipisahkan secara linier, algoritma akan mengalami osilasi tanpa henti (*infinite loop*).
2. **Ketiadaan Gradien pada Fungsi Tangga**: Fungsi tangga biner Heaviside memiliki turunan nol di semua titik kecuali di titik nol (di mana turunannya tidak terdefinisi). Ketiadaan gradien kontinu inilah yang mencegah penggunaan *gradient descent* pada Perceptron klasik.

---

## 3. Landasan Teori & Konsep Matematis Struktur Neuron

![Anatomi Neuron Biologis vs Neuron Buatan Perceptron](../assets/anatomi_neuron_biologis_vs_neuron_buatan_perceptron.png)

### 3.1 Komparasi Anatomi Biologis vs Komputasional

| Komponen Biologis | Komponen Neuron Buatan | Deskripsi Matematis & Komputasi |
| :--- | :--- | :--- |
| **Dendrit** | Vektor Masukan ($x_i$) | Saluran penerima sinyal rangsangan dari lingkungan atau neuron lain. |
| **Sinapsis** | Bobot Koneksi ($w_i$) | Kekuatan transmisi sinyal; bobot positif memperkuat, negatif menghambat. |
| **Badan Sel (Soma)** | Fungsi Akumulator ($\sum$) | Penjumlahan linier seluruh sinyal terbobot: $\sum_{i=1}^n w_i x_i$. |
| **Bukit Akson (Axon Hillock)** | Nilai Bias ($b$) | Nilai ambang internal yang menentukan tingkat kemudahan neuron terpicu. |
| **Akson** | Jalur Transmisi Sinyal | Menghantarkan potensial aksi keluaran menuju neuron target berikutnya. |
| **Potensial Aksi** | Fungsi Aktivasi ($\phi(z)$) | Transformasi sinyal kontinu menjadi impuls keluaran diskrit atau terdistorsi. |

### 3.2 Aturan Pembelajaran Perceptron (*Perceptron Learning Rule*)
Diberikan himpunan data latih $\mathcal{D} = \{(x^{(j)}, y^{(j)})\}_{j=1}^m$ di mana $y^{(j)} \in \{0, 1\}$. Untuk setiap sampel $j$:
1. Hitung keluaran prediksi:
   $$\hat{y}^{(j)} = \phi(w^\top x^{(j)} + b)$$
2. Hitung galat prediksi:
   $$e^{(j)} = y^{(j)} - \hat{y}^{(j)}$$
3. Perbarui vektor bobot dan bias dengan laju pembelajaran (*learning rate*) $\eta \in (0, 1]$:
   $$w \leftarrow w + \eta \cdot e^{(j)} \cdot x^{(j)}$$
   $$b \leftarrow b + \eta \cdot e^{(j)}$$

Jika prediksi benar ($e^{(j)} = 0$), bobot tidak berubah. Jika $y=1$ namun $\hat{y}=0$ ($e=1$), bobot ditambahkan ke arah vektor masukan $x^{(j)}$. Jika $y=0$ namun $\hat{y}=1$ ($e=-1$), bobot dikurangi menjauhi arah vektor masukan.

### 3.3 Pembuktian Matematis Kegagalan Gerbang Non-Linier XOR
Tinjau tabel kebenaran gerbang XOR dengan masukan biner $(x_1, x_2) \in \{0, 1\}^2$:

| $x_1$ | $x_2$ | Target $y$ | Syarat Hiperbidang Pemisah ($w_1 x_1 + w_2 x_2 + b$) |
| :---: | :---: | :---: | :---: |
| 0 | 0 | 0 | $w_1(0) + w_2(0) + b < 0 \implies b < 0$ |
| 0 | 1 | 1 | $w_1(0) + w_2(1) + b \ge 0 \implies w_2 + b \ge 0$ |
| 1 | 0 | 1 | $w_1(1) + w_2(0) + b \ge 0 \implies w_1 + b \ge 0$ |
| 1 | 1 | 0 | $w_1(1) + w_2(1) + b < 0 \implies w_1 + w_2 + b < 0$ |

Jumlahkan pertidaksamaan untuk baris kedua dan ketiga:
$$(w_1 + b) + (w_2 + b) \ge 0 \implies w_1 + w_2 + 2b \ge 0$$

Dari baris keempat diketahui $w_1 + w_2 + b < 0$. Substitusikan ke dalam pertidaksamaan penjumlahan:
$$(w_1 + w_2 + b) + b \ge 0$$
Karena $(w_1 + w_2 + b) < 0$ dan dari baris pertama $b < 0$, maka penjumlahan dua bilangan negatif tersebut **haruslah negatif** ($< 0$). Hal ini memicu kontradiksi matematis:
$$< 0 \ge 0 \quad (\text{Kontradiksi Absolut!})$$

Kontradiksi ini membuktikan secara analitis bahwa tidak ada pasangan bobot $(w_1, w_2, b)$ berapapun yang dapat memenuhi keempat kondisi gerbang XOR secara simultan. Sebuah neuron tunggal hanya mampu menciptakan satu garis pemisah lurus, sedangkan gerbang XOR membutuhkan minimal dua garis pemisah non-linier.

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Input Sinyal: x1, x2, ..., xn"] --> B["Modulasi Bobot: x_i * w_i"]
    B --> C["Akumulasi Net Input: z = sum(w_i * x_i) + b"]
    C --> D["Fungsi Aktivasi Tangga: y_hat = 1 jika z >= 0 else 0"]
    D --> E["Evaluasi Galat: e = y - y_hat"]
    E --> F["Pembaruan Bobot: w = w + eta * e * x"]
```

Implementasi Single Perceptron Rosenblatt dari dasar menggunakan NumPy:

```python
import numpy as np

class RosenblattPerceptron:
    def __init__(self, n_features, learning_rate=0.1, max_epochs=100, seed=42):
        np.random.seed(seed)
        self.w = np.zeros(n_features)
        self.b = 0.0
        self.lr = learning_rate
        self.max_epochs = max_epochs
        self.history_errors = []
        
    def step_function(self, z):
        return np.where(z >= 0.0, 1, 0)
        
    def predict(self, X):
        z = np.dot(X, self.w) + self.b
        return self.step_function(z)
        
    def fit(self, X, y):
        m = X.shape[0]
        for epoch in range(self.max_epochs):
            total_error = 0
            for i in range(m):
                y_hat = self.predict(X[i])
                error = y[i] - y_hat
                if error != 0:
                    self.w += self.lr * error * X[i]
                    self.b += self.lr * error
                    total_error += abs(error)
            self.history_errors.append(total_error)
            # Berhenti jika konvergen sempurna
            if total_error == 0:
                print(f"Perceptron Konvergen pada Epoch ke-{epoch+1}!")
                break
        return self

# Pengujian pada Gerbang AND (Linearly Separable)
X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1])

p_and = RosenblattPerceptron(n_features=2, learning_rate=0.2)
p_and.fit(X_and, y_and)
print("Bobot Akhir w   :", p_and.w)
print("Bias Akhir b    :", p_and.b)
print("Prediksi Output :", p_and.predict(X_and))
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Pemilahan Reflektansi Daun Sehat vs Klorosis

### 5.1 Pengukuran Spektrometri Lapangan
Diperoleh data rasio pantulan spektral kanopi kelapa sawit pada dua pita gelombang:
* $x_1$: Pantulan Cahaya Merah (Red Band, 660 nm) - terserap kuat oleh klorofil normal.
* $x_2$: Pantulan Inframerah Dekat (NIR Band, 850 nm) - dipantulkan kuat oleh struktur sel mesofil daun sehat.

Daun sehat ($y=1$) memiliki serapan merah tinggi (pantulan merah rendah) dan pantulan NIR tinggi. Daun mengalami klorosis/malnutrisi ($y=0$) memiliki pantulan merah tinggi dan pantulan NIR rendah.

### 5.2 Implementasi dan Garis Pemisah Hiperbidang
```python
# Simulasi sampel pengukuran lapangan
np.random.seed(42)
n_samples = 40
# Daun Klorosis (y = 0): Red tinggi [0.4 - 0.7], NIR rendah [0.1 - 0.4]
X_klorosis = np.column_stack([np.random.uniform(0.4, 0.7, n_samples), np.random.uniform(0.1, 0.4, n_samples)])
# Daun Sehat (y = 1): Red rendah [0.1 - 0.35], NIR tinggi [0.5 - 0.85]
X_sehat = np.column_stack([np.random.uniform(0.1, 0.35, n_samples), np.random.uniform(0.5, 0.85, n_samples)])

X_daun = np.vstack([X_klorosis, X_sehat])
y_daun = np.array([0]*n_samples + [1]*n_samples)

perceptron_daun = RosenblattPerceptron(n_features=2, learning_rate=0.1, max_epochs=50)
perceptron_daun.fit(X_daun, y_daun)
akurasi = np.mean(perceptron_daun.predict(X_daun) == y_daun) * 100
print(f"Akurasi Pemilahan Daun: {akurasi:.1f}%")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Memaksakan Perceptron pada Data Non-Linier**: Menjalankan Perceptron pada data dengan pola beririsan atau non-linier akan menyebabkan algoritma melakukan iterasi hingga batas epoch maksimum tanpa konvergen (*infinite cycling*).
2. **Laju Pembelajaran Terlalu Besar**: Memilih $\eta$ yang terlalu besar dapat menyebabkan hiperbidang pemisah berosilasi melompati posisi batas keputusan optimal.
3. **Mengabaikan Normalisasi Data Input**: Nilai fitur input dengan magnitudo sangat besar akan mendominasi pembaruan bobot secara tidak proporsional.

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Pemeriksaan Visual Pemisahan Linier**: Untuk data 2D atau 3D, plot sebaran data terlebih dahulu sebelum memutuskan menggunakan model linear perceptron.
2. **Kriteria Penghentian Tambahan (*Early Stopping / Pocket Algorithm*)**: Simpan bobot terbaik yang menghasilkan kesalahan terendah (*pocket algorithm*) untuk mengantisipasi data yang memiliki sedikit derau (*overlapping noise*).
3. **Transisi ke Fungsi Aktivasi Diferensiabel**: Ganti fungsi tangga biner Heaviside dengan Sigmoid atau ReLU bila ingin melatih jaringan menggunakan algoritma penurunan gradien (*gradient descent*).

---

## 7. Rangkuman Modul

* Struktur neuron buatan meniru mekanisme dasar neuron biologis: dendrit (masukan), sinapsis (bobot), soma (akumulasi net input), dan akson (keluaran teraktivasi).
* Perceptron Rosenblatt memperkenalkan aturan pembelajaran koreksi galat (*error-correction rule*) yang memperbarui bobot secara terarah berdasarkan selisih target dan prediksi.
* Teorema Konvergensi Perceptron membuktikan bahwa model dijamin menemukan pemisah sempurna jika data bersifat *linearly separable*.
* Analisis matematis membuktikan kegagalan absolut Single Perceptron dalam memisahkan persoalan non-linier seperti gerbang XOR, yang mendasari keharusan pengembangan arsitektur jaringan saraf berlapis banyak (*Multi-Layer Perceptron*).

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Perhitungan Pembaruan Bobot Manual (Bloom C3)**: Diberikan sebuah Perceptron dengan bobot awal $w_1 = 0.2$, $w_2 = -0.4$, bias $b = 0.1$, dan laju pembelajaran $\eta = 0.5$. Jika disajikan sampel masukan $x = (1, 2)$ dengan label target $y = 1$:
   * Hitung nilai net input $z$ dan prediksi $\hat{y}$ menggunakan fungsi tangga ($z \ge 0 \implies 1$, $z < 0 \implies 0$)!
   * Hitung nilai galat $e$!
   * Hitung vektor bobot baru $w$ dan bias baru $b$ pasca-pembaruan!
2. **Analisis Batas Pemisah Geometris (Bloom C4)**: Persamaan garis batas keputusan suatu Perceptron adalah $w_1 x_1 + w_2 x_2 + b = 0$. Turunkan persamaan kemiringan (*slope*) garis $m$ dan titik potong sumbu-vertikal (*intercept*) $c$ dalam variabel $w_1, w_2,$ dan $b$! Bagaimana pengaruh pembesaran nilai bias $b$ terhadap posisi garis batas keputusan pada bidang kartesius?

### Tugas Pemrograman Mandiri
Ujilah algoritma `RosenblattPerceptron` pada dataset gerbang logika XOR:
`X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])`, `y_xor = np.array([0, 1, 1, 0])`.
Catat dinamika total galat per epoch selama 50 epoch dan buat plot kurvanya. Analisis secara mendalam mengapa kurva galat tersebut mengalami osilasi tanpa pernah mencapai angka nol!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 9.4: Activation Function

Kita telah membuktikan bahwa keterbatasan utama Perceptron klasik terletak pada fungsi tangga biner Heaviside yang kaku dan tidak terdiferensiasi, sehingga membatasi model hanya pada pemisahan linier. Bagaimana cara membuat neuron mampu mengalirkan informasi gradien kontinu dan menyusun pemetaan non-linier yang kaya?

Pada **AI Modul 9.4: Activation Function**, kita akan mengeksplorasi spektrum luas **fungsi aktivasi non-linier** modern: dari fungsi klasik Sigmoid dan Tanh, menuju era keemasan ReLU, hingga varian mutakhir seperti Leaky ReLU, ELU, GELU, dan Swish. Kita juga akan menganalisis fenomena krusial hilangnya gradien (*vanishing gradient problem*) dan fenomena kematian neuron (*dying ReLU*).

---

## 10. Daftar Pustaka dan Referensi Akademik

1. McCulloch, W. S., & Pitts, W. (1943). *A logical calculus of the ideas immanent in nervous activity*. The Bulletin of Mathematical Biophysics, 5(4), 115-133.
2. Rosenblatt, F. (1958). *The perceptron: a probabilistic model for information storage and organization in the brain*. Psychological Review, 65(6), 386-408.
3. Minsky, M., & Papert, S. A. (1969). *Perceptrons: An Introduction to Computational Geometry*. MIT Press.
4. Novikoff, A. B. (1962). *On convergence proofs on perceptrons*. Proceedings of the Symposium on the Mathematical Theory of Automata, 12, 615-622.
"""
    validate_text(md_content, "AI_Modul_9.3_Struktur_Neuron.md")
    with open("docs/part-09/AI_Modul_9.3_Struktur_Neuron.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-09/AI_Modul_9.3_Struktur_Neuron.md")

    # Notebook 9.3
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 9.3: Praktikum Struktur Neuron\n",
                    "**Mata Kuliah:** Kecerdasan Buatan Terapan & Deep Learning  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Membangun model Single Perceptron Rosenblatt dari dasar menggunakan NumPy murni.\n",
                    "2. Mengimplementasikan aturan pembelajaran Perceptron (*Perceptron Learning Rule*) dan fungsi aktivasi tangga Heaviside.\n",
                    "3. Menguji pemisahan linier pada gerbang logika AND dan OR serta mendemonstrasikan kegagalan konvergensi pada gerbang XOR.\n",
                    "4. Memvisualisasikan garis batas keputusan (*separating hyperplane*) dinamis pada data reflektansi daun sawit.\n"
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
                    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                    "print(f'NumPy Version: {np.__version__}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Implementasi Kelas Single Perceptron Rosenblatt\n",
                    "Membuat kelas Perceptron dari awal dengan fungsi tangga Heaviside dan pembaruan bobot berbasis galat biner."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "class RosenblattPerceptron:\n",
                    "    def __init__(self, n_features, learning_rate=0.1, max_epochs=50, seed=42):\n",
                    "        np.random.seed(seed)\n",
                    "        self.w = np.zeros(n_features)\n",
                    "        self.b = 0.0\n",
                    "        self.lr = learning_rate\n",
                    "        self.max_epochs = max_epochs\n",
                    "        self.history_errors = []\n",
                    "        \n",
                    "    def step_function(self, z):\n",
                    "        return np.where(z >= 0.0, 1, 0)\n",
                    "        \n",
                    "    def predict(self, X):\n",
                    "        z = np.dot(X, self.w) + self.b\n",
                    "        return self.step_function(z)\n",
                    "        \n",
                    "    def fit(self, X, y):\n",
                    "        m = X.shape[0]\n",
                    "        for epoch in range(self.max_epochs):\n",
                    "            total_error = 0\n",
                    "            for i in range(m):\n",
                    "                y_hat = self.predict(X[i])\n",
                    "                error = y[i] - y_hat\n",
                    "                if error != 0:\n",
                    "                    self.w += self.lr * error * X[i]\n",
                    "                    self.b += self.lr * error\n",
                    "                    total_error += abs(error)\n",
                    "            self.history_errors.append(total_error)\n",
                    "            if total_error == 0:\n",
                    "                break\n",
                    "        return self\n",
                    "\n",
                    "print('Kelas RosenblattPerceptron berhasil didefinisikan!')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Pengujian pada Gerbang Linier (AND) vs Gerbang Non-Linier (XOR)\n",
                    "Menguji keterbatasan matematis perceptron tunggal terhadap gerbang logika biner."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])\n",
                    "y_and = np.array([0, 0, 0, 1])\n",
                    "y_xor = np.array([0, 1, 1, 0])\n",
                    "\n",
                    "# Training pada Gerbang AND\n",
                    "p_and = RosenblattPerceptron(n_features=2, learning_rate=0.2, max_epochs=20)\n",
                    "p_and.fit(X, y_and)\n",
                    "print('=== HASIL GERBANG AND (Linearly Separable) ===')\n",
                    "print('Bobot Akhir w   :', p_and.w)\n",
                    "print('Bias Akhir b    :', p_and.b)\n",
                    "print('Prediksi Output :', p_and.predict(X))\n",
                    "print('Konvergen Epoch :', len(p_and.history_errors))\n",
                    "\n",
                    "# Training pada Gerbang XOR\n",
                    "p_xor = RosenblattPerceptron(n_features=2, learning_rate=0.2, max_epochs=30)\n",
                    "p_xor.fit(X, y_xor)\n",
                    "print('\\n=== HASIL GERBANG XOR (Non-Linearly Separable) ===')\n",
                    "print('Bobot Akhir w   :', p_xor.w)\n",
                    "print('Bias Akhir b    :', p_xor.b)\n",
                    "print('Prediksi Output :', p_xor.predict(X))\n",
                    "print('Total Error Akhir:', p_xor.history_errors[-1])\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Visualisasi Dinamika Galat Perceptron pada Gerbang XOR\n",
                    "Menampilkan kegagalan konvergensi berupa osilasi galat tak berujung pada data non-linier XOR."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, ax = plt.subplots(figsize=(8, 4.5))\n",
                    "ax.plot(p_and.history_errors, marker='o', label='Gerbang AND (Konvergen ke 0)', color='forestgreen', linewidth=2)\n",
                    "ax.plot(p_xor.history_errors, marker='s', label='Gerbang XOR (Osilasi / Gagal Konvergen)', color='crimson', linewidth=2)\n",
                    "ax.set_title('Dinamika Konvergensi Perceptron: AND vs XOR', fontsize=12, fontweight='bold')\n",
                    "ax.set_xlabel('Epoch Iterasi', fontsize=10)\n",
                    "ax.set_ylabel('Jumlah Kesalahan Klasifikasi', fontsize=10)\n",
                    "ax.legend()\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_and_vs_xor_9_3.png', dpi=150)\n",
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
    with open("notebooks/part-09/AI_Modul_9.3_Praktikum_Struktur_Neuron.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-09/AI_Modul_9.3_Praktikum_Struktur_Neuron.ipynb")

    # Guide 9.3
    guide_content = """# AI Modul 9.3: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-09-03
* **Topik Utama**: Struktur Neuron, Anatomi Komputasi, dan Batas Pemisahan Linier
* **Alokasi Waktu**: 150 Menit (50 Menit Kuliah Teori & Pembuktian, 70 Menit Praktikum Terbimbing, 30 Menit Diskusi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 9.3, Jupyter Notebook Praktikum, Proyektor, Komputer Praktikum.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Anatomi biologis vs komputasi: peran dendrit, soma, akson, sinapsis, dan formulasi net input $z = w^\top x + b$.
* **Menit 25 - 50**: Pembuktian analitis kegagalan gerbang XOR (Minsky & Papert 1969) di papan tulis, demonstrasi kontradiksi aljabar pertidaksamaan linear.
* **Menit 50 - 120**: Praktikum komputer: koding Single Perceptron dari scratch, pengujian gerbang AND, dan pengamatan kegagalan osilasi pada gerbang XOR.
* **Menit 120 - 150**: Pembahasan hasil osilasi galat, solusi penambahan hidden layer, dan jembatan ke Modul 9.4 (Fungsi Aktivasi).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Analogi Biologis** | Menjelaskan padanan matematis dari setiap organel sel saraf secara akurat dan mendalam. | Menyebutkan dendrit dan akson namun kurang tepat menjelaskan fungsi matematis bukit akson (*bias*). | Tertukar antara konsep bobot sinaptik dan sinyal aktivasi. |
| **Pembuktian Paradoks XOR** | Mampu merekonstruksi sistem pertidaksamaan linier dan membuktikan kontradiksi $< 0 \ge 0$ secara runut. | Memahami konsep bahwa XOR tidak dapat dipisahkan garis lurus, namun gagal menyusun bukti aljabar. | Tidak memahami alasan matematis kegagalan perceptron pada gerbang non-linier. |
| **Koding & Debugging Perceptron** | Menulis skrip Perceptron scratch dengan aturan pembaruan bobot yang tepat dan visualisasi konvergensi. | Menjalankan kode praktikum dengan baik namun bingung ketika kode mengalami perulangan pada XOR. | Salah mengimplementasikan rumus pembaruan bobot ($w \leftarrow w + \eta e x$). |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Pembaruan Bobot Manual
Diketahui: $w = (0.2, -0.4)$, $b = 0.1$, $\eta = 0.5$.
Sampel masukan: $x = (1, 2)$, label target: $y = 1$.
1. **Net Input $z$**:
   $$z = w_1 x_1 + w_2 x_2 + b = (0.2)(1) + (-0.4)(2) + 0.1 = 0.2 - 0.8 + 0.1 = -0.5$$
2. **Prediksi $\hat{y}$**:
   Karena $z = -0.5 < 0$, maka $\hat{y} = 0$.
3. **Galat Prediksi $e$**:
   $$e = y - \hat{y} = 1 - 0 = 1$$
4. **Pembaruan Bobot & Bias**:
   $$w_1 \leftarrow w_1 + \eta \cdot e \cdot x_1 = 0.2 + (0.5)(1)(1) = 0.2 + 0.5 = 0.7$$
   $$w_2 \leftarrow w_2 + \eta \cdot e \cdot x_2 = -0.4 + (0.5)(1)(2) = -0.4 + 1.0 = 0.6$$
   $$b \leftarrow b + \eta \cdot e = 0.1 + (0.5)(1) = 0.6$$
Vektor bobot baru adalah $w = (0.7, 0.6)$ dan bias baru $b = 0.6$.

### Jawaban Soal Konseptual 2: Analisis Geometris Batas Pemisah
Persamaan garis batas keputusan adalah:
$$w_1 x_1 + w_2 x_2 + b = 0 \implies w_2 x_2 = -w_1 x_1 - b \implies x_2 = -\frac{w_1}{w_2} x_1 - \frac{b}{w_2}$$
Maka:
* Kemiringan garis (*slope*) $m = -\frac{w_1}{w_2}$
* Titik potong sumbu vertikal (*intercept*) $c = -\frac{b}{w_2}$
Pengaruh nilai bias $b$: Membesarkan nilai bias $b$ menggeser posisi garis batas keputusan secara translasi sejajar di sepanjang sumbu ruang fitur tanpa mengubah sudut kemiringan (*slope*) garis pemisah.
"""
    validate_text(guide_content, "AI_Modul_9.3_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-09/AI_Modul_9.3_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-09/AI_Modul_9.3_Panduan_Instruktur_dan_Kunci_Solusi.md")

if __name__ == '__main__':
    create_modul_9_2()
    create_modul_9_3()
