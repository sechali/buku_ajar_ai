# AI Modul 9.3: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-09-03
* **Topik Utama**: Struktur Neuron, Anatomi Komputasi, dan Batas Pemisahan Linier
* **Alokasi Waktu**: 150 Menit (50 Menit Kuliah Teori & Pembuktian, 70 Menit Praktikum Terbimbing, 30 Menit Diskusi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 9.3, Jupyter Notebook Praktikum, Proyektor, Komputer Praktikum.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Anatomi biologis vs komputasi: peran dendrit, soma, akson, sinapsis, dan formulasi net input $z = w^	op x + b$.
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
