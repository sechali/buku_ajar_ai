# PANDUAN INSTRUKTUR & KUNCI SOLUSI
## AI Modul 1.2: Sejarah dan Perkembangan Artificial Intelligence

> **Dokumen Rahasia Pengajar (Dosen & Asisten Laboratorium)**  
> **Modul Terkait:** [AI_Modul_1.2_Sejarah_dan_Perkembangan.md](../../docs/part-01/AI_Modul_1.2_Sejarah_dan_Perkembangan.md)  
> **Notebook Praktikum:** [AI_Modul_1.2_Praktikum_Sejarah_dan_Perkembangan.ipynb](../../notebooks/part-01/AI_Modul_1.2_Praktikum_Sejarah_dan_Perkembangan.ipynb)

---

## 1. Panduan Fasilitasi & Titik Tekan Pedagogi

### 1.1. Miskonsepsi Umum Mahasiswa
1. **Miskonsepsi Perceptron Mampu Segala Hal**: Sebelum 1969, banyak insinyur mengira menambahkan neuron tunggal dapat menyelesaikan segala jenis persepsi visual. Tekankan bahwa keterbatasan *single-layer* murni adalah batasan matematis geometri bidang datar.
2. **Miskonsepsi Mengapa AI Winter Terjadi**: Mahasiswa sering mengira AI Winter terjadi semata-mata karena sainsnya salah. Jelaskan bahwa faktor pemicu utamanya adalah **kesenjangan ekspektasi (*expectation gap*)**: para pionir menjanjikan hal yang melampaui kemampuan hardware dan matematika pada masanya.

### 1.2. Alokasi Waktu Praktikum (100 Menit)
* **Menit 00–25**: Kuliah interaktif: Garis waktu sejarah AI (1943 s.d. era LLM/Transformer) dan anatomi kegagalan AI Winter I & II.
* **Menit 25–45**: Live coding: Pembuktian aljabar limitasi XOR di papan tulis / proyektor dilanjutkan eksekusi notebook.
* **Menit 45–80**: Mahasiswa mengerjakan eksperimen mandiri: mencoba berbagai *learning rate* dan memprogram rekayasa fitur polinomial 3D.
* **Menit 80–100**: Evaluasi hasil visualisasi *decision boundary* dan pembahasan 3 pertanyaan HOTS.

---

## 2. Kunci Jawaban Pertanyaan Analitis (HOTS)

### Pertanyaan 1: Mengapa Riset AI Mati Suri Pasca-Buku Minsky & Papert (1969)?
* **Kunci Jawaban**:
  1. **Ketiadaan Solusi Algoritmik Pelatihan Hidden Layer**: Minsky dan Papert sebenarnya sudah menduga bahwa jaringan bertingkat (*multi-layer networks*) mampu memecahkan XOR. Namun pada tahun 1969, komunitas sains belum menemukan formula kalkulus untuk menghitung bagaimana error di lapisan output dapat dialirkan mundur untuk menyesuaikan bobot di lapisan tersembunyi (*credit assignment problem*). Algoritma *Backpropagation* baru dipopulerkan 17 tahun kemudian (1986).
  2. **Dampak Otoritas Akademik**: Marvin Minsky adalah salah satu tokoh pendiri AI paling berpengaruh di MIT. Kritik tajam dari tokoh sekaliber beliau membuat badan pendana riset militer dan pemerintah (seperti DARPA) berkesimpulan bahwa pendekatan jaringan syaraf tiruan adalah jalan buntu (*dead end*), sehingga dana riset dialihkan seluruhnya ke pendekatan sistem simbolik.

### Pertanyaan 2: Mengapa Deep Learning 2012 Tidak Mengalami AI Winter Seperti Sistem Pakar 1987?
* **Kunci Jawaban**:
  1. **Konvergensi Tiga Faktor (Trifecta)**: Sistem Pakar (1980-an) hanya memiliki algoritma aturan manual tetapi kekurangan data empiris dan berjalan pada komputer LISP mahal yang segera usang. Sebaliknya, revolusi 2012 ditopang oleh tiga pilar simultan yang nyata: (a) Ketersediaan jutaan data berlabel (ImageNet), (b) Akselerasi komputasi grafis paralel berbiaya terjangkau (GPU NVIDIA GeForce/Tesla), dan (c) Regularisasi matematika modern (ReLU, Dropout).
  2. **Daya Generalisasi pada Data Nyata**: Sistem pakar sangat rapuh (*brittle*) bila dihadapkan pada masukan yang sedikit menyimpang dari aturan. *Deep Learning* bersifat probabilistik dan kontinu, sehingga sangat andal (*robust*) mengekstraksi representasi laten dari data tak terstruktur (citra, audio, video).

### Pertanyaan 3: Relevansi Hukum Hebb dengan Pembaruan Bobot Perceptron
* **Kunci Jawaban**:
  * Hukum Hebb (1949) menyatakan: *"Neurons that fire together, wire together"* (jika neuron input dan target aktif bersamaan, bobot sinapsis antar-keduanya diperkuat).
  * Pada rumus Perceptron: $\Delta w_i = \eta \cdot (y - \hat{y}) \cdot x_i$:
    * Jika input aktif ($x_i = 1$) dan target menuntut aktivasi tetapi model masih pasif ($(y - \hat{y}) = +1$), maka nilai $\Delta w_i = +\eta > 0$. Bobot dinaikkan secara langsung memperkuat koneksi sinapsis tersebut, persis seperti postulat Hebbian.
    * Jika input pasif ($x_i = 0$), maka $\Delta w_i = 0$, artinya koneksi sinapsis tidak diubah.

---

## 3. Kunci Kode Solusi Tantangan Mandiri: Rekayasa Fitur XOR

Berikut adalah solusi lengkap bagaimana mentransformasikan ruang sampel XOR dari 2D menjadi 3D agar dapat dipisahkan secara linier oleh Perceptron:

```python
import numpy as np

# 1. Data 2D Asli
X_original = np.array([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
])
y_xor = np.array([0, 1, 1, 0])

# 2. Rekayasa Fitur: Tambahkan dimensi ke-3 x3 = x1 * x2
# Kolom ke-3 merepresentasikan interaksi non-linier antar-variabel
x3 = (X_original[:, 0] * X_original[:, 1]).reshape(-1, 1)
X_3D = np.hstack([X_original, x3])

# 3. Latih Perceptron 3-Dimensi
perceptron_3d = RosenblattPerceptron(input_dim=3, learning_rate=0.1, max_epochs=50)
success, epochs = perceptron_3d.train(X_3D, y_xor)

print("Status:", "Berhasil Konvergen!" if success else "Gagal")
print(f"Epoch: {epochs}")
print(f"Bobot: w1={perceptron_3d.weights[0]:.2f}, w2={perceptron_3d.weights[1]:.2f}, w3={perceptron_3d.weights[2]:.2f}, b={perceptron_3d.bias:.2f}")
```

### Penjelasan Matematis untuk Mahasiswa:
Di ruang 2D, koordinat $(1,1)$ dan $(0,0)$ berada pada satu sumbu diagonal sehingga tidak bisa dipisahkan oleh satu garis dari $(1,0)$ dan $(0,1)$.  
Dengan menambahkan fitur $x_3 = x_1 \cdot x_2$:
* Titik $(0,0) \to (0, 0, 0)$ [Target 0]
* Titik $(1,0) \to (1, 0, 0)$ [Target 1]
* Titik $(0,1) \to (0, 1, 0)$ [Target 1]
* Titik $(1,1) \to (1, 1, 1)$ [Target 0]

Perhatikan bahwa titik $(1,1,1)$ sekarang terangkat ke sumbu $z=1$, sementara titik $(1,0,0)$ dan $(0,1,0)$ berada di bidang dasar $z=0$. Sebuah bidang datar 3D kini dapat menyelip di antara keduanya untuk memisahkan kelas secara sempurna!

---

## 4. Variasi Soal Kuis Praktikum / Ujian Responsi

### Variasi Soal A: Pelatihan Gerbang NOR dan NAND
* **Deskripsi**: Mintalah mahasiswa menguji Perceptron pada gerbang logika NAND (*Not-AND*) dan NOR (*Not-OR*).
* **Target Pembuktian**: Mahasiswa membuktikan bahwa NAND dan NOR bersifat *linearly separable* dan konvergen dalam $\le 6$ epoch.

### Variasi Soal B: Analisis Pengaruh Learning Rate ($\eta$)
* **Deskripsi**: Mintalah mahasiswa melatih Perceptron pada gerbang AND dengan variasi learning rate $\eta \in [1.0, 0.1, 0.01, 0.0001]$.
* **Target Pembuktian**: Mahasiswa menganalisis jumlah epoch yang dibutuhkan untuk mencapai konvergensi dan memahami mengapa $\eta$ yang terlalu kecil memperlambat pelatihan.

---

## 5. Rubrik Penilaian Praktikum Lab (Skala 100)

| Aspek Penilaian | Bobot | Deskriptor Kinerja Unggul (Nilai Maksimal) |
| :--- | :---: | :--- |
| **Pemahaman Teori Sejarah & Konsep** | 20% | Mampu menjelaskan pemicu First & Second AI Winter serta menguraikan kontribusi Minsky-Papert dan Rumelhart. |
| **Implementasi Kode Perceptron** | 35% | Kode Python berfungsi sempurna tanpa library ML eksternal, perhitungan dot-product dan update bobot tepat. |
| **Penyelesaian Tantangan XOR** | 30% | Berhasil merekayasa fitur non-linier $x_1 \cdot x_2$ dan membuktikan konvergensi 100% pada gerbang XOR. |
| **Dokumentasi Komentar & Clean Code** | 15% | Setiap baris kode diberi komentar fungsi yang jelas dan mengikuti standar penulisan kode saintifik (PEP 8). |
