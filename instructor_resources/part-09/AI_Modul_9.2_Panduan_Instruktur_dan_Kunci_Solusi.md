# AI Modul 9.2: Panduan Instruktur dan Kunci Solusi

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
   * Matriks Masukan $X \in \mathbb{R}^{64 	imes 10}$
   * Matriks Bobot $W^{[1]} \in \mathbb{R}^{32 	imes 10}$
   * Vektor Bias $b^{[1]} \in \mathbb{R}^{1 	imes 32}$ (atau $\mathbb{R}^{32 	imes 1}$)
   * Matriks Net Input $Z^{[1]} = X (W^{[1]})^	op + b^{[1]} \in \mathbb{R}^{64 	imes 32}$
2. **Lapisan Tersembunyi 2**:
   * Matriks Bobot $W^{[2]} \in \mathbb{R}^{16 	imes 32}$
   * Vektor Bias $b^{[2]} \in \mathbb{R}^{1 	imes 16}$
   * Matriks Aktivasi $A^{[2]} = 	ext{ReLU}(A^{[1]} (W^{[2]})^	op + b^{[2]}) \in \mathbb{R}^{64 	imes 16}$
3. **Lapisan Keluaran (Lapisan 3)**:
   * Matriks Bobot $W^{[3]} \in \mathbb{R}^{4 	imes 16}$
   * Vektor Bias $b^{[3]} \in \mathbb{R}^{1 	imes 4}$
   * Matriks Probabilitas Keluaran $A^{[3]} = 	ext{Softmax}(A^{[2]} (W^{[3]})^	op + b^{[3]}) \in \mathbb{R}^{64 	imes 4}$

### Jawaban Soal Konseptual 2: Analisis Simetri Bobot
Jika semua bobot diinisialisasi sama ($W_{ij} = c$), maka untuk setiap neuron $j$ dan $k$ pada lapisan tersembunyi yang sama:
$$z_j^{[1]} = \sum_{i} x_i c + b = z_k^{[1]}$$
Akibatnya, nilai aktivasi $a_j^{[1]} = \sigma(z_j^{[1]})$ akan persis sama dengan $a_k^{[1]}$. Pada fase backpropagation, gradien terhadap bobot $\frac{\partial L}{\partial W_{ji}^{[1]}}$ juga akan bernilai sama untuk seluruh neuron. Akibatnya, seluruh neuron tersembunyi akan terus diperbarui dengan nilai yang identik sepanjang iterasi training. Keberadaan 32 neuron tersembunyi tersebut secara matematis tidak lebih bermanfaat daripada memiliki 1 neuron tunggal, karena tidak terjadi pemecahan simetri (*symmetry breaking*). Inilah sebabnya inisialisasi acak berbobot kecil (*random initialization*) merupakan prasyarat mutlak.
