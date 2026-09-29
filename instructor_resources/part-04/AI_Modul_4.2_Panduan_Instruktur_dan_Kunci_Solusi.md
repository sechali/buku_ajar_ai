# AI Modul 4.2: Panduan Instruktur dan Kunci Solusi
## NumPy untuk Komputasi Numerik: Arsitektur Memori, Vektorisasi, dan Aljabar Linier Agribisnis

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

| Komponen | Rincian Instruksional |
| :--- | :--- |
| **Mata Kuliah** | Sains Data & Kecerdasan Buatan Terapan |
| **Kode Modul** | AI Modul 4.2 |
| **Topik Pembelajaran** | Arsitektur Internal NumPy, Manipulasi `ndarray`, Strides, Broadcasting, dan Aljabar Linier Terapan |
| **Alokasi Waktu** | 3 SKS (150 Menit Tatap Muka/Laboratorium + 180 Menit Belajar Mandiri) |
| **Prasyarat** | AI Modul 4.1 (Pengantar Data Science) |
| **Target OBE** | Sub-CPMK 4.2: Mahasiswa mampu mengeliminasi perulangan lambat dengan operasi vektorisasi SIMD, menghitung langkah memori (*strides*), serta menyelesaikan persoalan optimasi sumber daya kebun menggunakan aljabar linier NumPy. |

### Matriks Distribusi Jam Pembelajaran (150 Menit)
1. **Sesi Pembuka & Refleksi Arsitektural (30 Menit):**
   - Perbandingan mikroskopis memori Python List vs NumPy `ndarray`.
   - Mengapa NumPy cepat: Penyangga kontigu C, CPU cache locality, dan instruksi SIMD (AVX-512).
2. **Sesi Telaah Konseptual & Pembuktian Rumus (30 Menit):**
   - Perhitungan formal tupel *strides* pada tata letak *Row-Major* (C) vs *Column-Major* (Fortran).
   - Tiga aturan formal penyiaran dimensi (*broadcasting rules*) dan pembuktian matematisnya.
3. **Praktikum Laboratorium Terbimbing (60 Menit):**
   - Eksplorasi berkas `notebooks/part-04/AI_Modul_4.2_Praktikum_NumPy_Komputasi_Numerik.ipynb`.
   - Menjalankan uji benchmark kecepatan vektorisasi SIMD vs loop murni.
   - Eksperimen bahaya mutasi data pada *view* vs keamanan *copy* (`np.shares_memory`).
   - Penyelesaian sistem persamaan linier daya turbin PKS dan visualisasi spasial grid citra NDVI.
4. **Sesi Evaluasi & Diskusi HOTS (30 Menit):**
   - Evaluasi solusi latihan HOTS (perhitungan alamat heksadesimal memori dan eliminasi loop).
   - Ulasan peran NumPy sebagai fondasi utama sebelum mempelajari pustaka Pandas dan PyTorch.

---

## 2. Strategi Pedagogis dan Panduan Fasilitasi Kelas

### 2.1 Demonstrasi Interaktif "Inspect the RAM"
Tampilkan atribut memori secara langsung di proyektor kelas:
- Perintahkan mahasiswa mengecek `array.nbytes`, `array.itemsize`, dan `array.strides`.
- Tunjukkan bahwa array berdimensi $(1000, 1000)$ bertipe `float64` membutuhkan memori $8 \text{ MB}$, sedangkan list Python dengan ukuran yang sama menghabiskan $> 64 \text{ MB}$ karena overhead penunjuk dan objek skalar `PyFloatObject`.

### 2.2 Aturan Baku Penulisan Kode Berkinerja Tinggi
Tanamkan aturan emas dalam kelas komputasi numerik:
> *"Jika Anda menuliskan kata kunci `for` atau `while` untuk memproses elemen data numerik satu per satu di Python, 99% kemungkinan Anda sedang menulis kode yang tidak efisien. Cari fungsi primitif tervektorisasi di NumPy!"*

---

## 3. Identifikasi dan Remediasi Miskonsepsi Mahasiswa

### Miskonsepsi 1: "Slicing pada NumPy selalu menduplikasi data seperti slicing pada Python List."
- **Koreksi Konseptual:** Pada Python list, `sub = data[1:4]` membuat list baru. Namun pada NumPy `ndarray`, slicing dasar **hanya membuat VIEW** (objek header baru yang merujuk pada alamat memori fisik yang sama). Jika elemen `sub` diubah, data pada array induk ikut berubah! Gunakan metode `.copy()` jika ingin duplikasi independen.

### Miskonsepsi 2: "Proses Broadcasting menggandakan elemen array di RAM hingga ukurannya sama."
- **Koreksi Konseptual:** Broadcasting sama sekali **tidak menyalin atau mereplikasi data di RAM**. NumPy hanya memanipulasi metadata *strides* dengan menetapkan nilai stride pada dimensi yang diregangkan bernilai **0 byte**. Artinya, saat iterator bergerak di sepanjang dimensi tersebut, CPU terus membaca alamat fisik memori yang sama.

### Miskonsepsi 3: "Menggunakan loop Python biasa untuk mengisi elemen NumPy array secara iteratif."
- **Koreksi Konseptual:** Menulis `for i in range(len(arr)): arr[i] = ...` menghilangkan seluruh keunggulan kecepatan C. Eksekusi ini memaksa CPython beralih bolak-balik antara runtime C dan interpreter Python (*crossing the C-Python boundary*), yang justru lebih lambat dibanding mengoperasikan list murni.

### Miskonsepsi 4: "Operator `*` digunakan untuk perkalian matriks aljabar linier."
- **Koreksi Konseptual:** Operator `*` adalah *Hadamard product* (perkalian elemen per elemen: $A_{ij} \times B_{ij}$). Untuk perkalian aljabar linier matriks matematika ($C = A B$), mahasiswa wajib menggunakan operator `@` atau fungsi `np.dot(A, B)`.

---

## 4. Kunci Solusi dan Pembahasan Soal Latihan & HOTS

### 4.1 Pembahasan Soal Arsitektur Memori dan Strides (Bobot: 30%)
Matriks $M$ bertipe `float64` (8 byte per elemen) dengan shape $(4, 6)$ berformat *C-contiguous*.

**1. Perhitungan Tupel Strides:**
- Dalam format *C-order* (row-major), elemen dalam baris yang sama bersebelahan (jarak 8 byte).
- Satu baris terdiri dari 6 kolom, sehingga untuk melompat ke baris berikutnya dibutuhkan:
  $$\text{stride}_0 = 6 \times 8 = 48 \text{ byte}$$
  $$\text{stride}_1 = 1 \times 8 = 8 \text{ byte}$$
- Maka tupel langkah memori:
  $$\mathbf{\text{Strides}(M) = (48, 8)}$$

**2. Karakteristik Matriks Transposisi $M_T = M.T$:**
- Transposisi menukar dimensi baris dan kolom:
  $$\text{Shape}(M_T) = (6, 4)$$
- Transposisi menukar tupel langkah memori tanpa menyalin memori:
  $$\text{Strides}(M_T) = (8, 48)$$
- **Karakteristik Alokasi:** Operasi transposisi **TIDAK mengalokasikan memori baru** di RAM. Ini adalah *strided view* murni dengan bendera `c_contiguous = False` dan `f_contiguous = True`.

**3. Perhitungan Alamat Memori Fisik $M[2, 4]$:**
- Diketahui alamat awal $\text{Base\_Address} = \text{0x1000}$ (dalam desimal: $4096_{10}$).
- Indeks yang dicari: baris $i = 2$, kolom $j = 4$.
- Formula pergeseran *offset* byte:
  $$\text{Offset} = (i \times \text{stride}_0) + (j \times \text{stride}_1)$$
  $$\text{Offset} = (2 \times 48) + (4 \times 8) = 96 + 32 = 128 \text{ byte}$$
- Dalam heksadesimal, $128_{10} = \text{0x80}$.
- Alamat fisik:
  $$\text{Address}(M[2, 4]) = \text{0x1000} + \text{0x80} = \mathbf{\text{0x1080}}$$

### 4.2 Pembahasan Algoritma Vektorisasi Spasial Kebun (Bobot: 40%)
Matriks `NIR` dan `RED` berukuran $1000 \times 1000$ bertipe `float32`.

**a. Kode Vektorisasi Satu Baris Aman (Safe NDVI):**
```python
ndvi = np.where((nir + red) == 0, 0.0, (nir - red) / (nir + red + 1e-7))
```

**b. Boolean Masking Kanopi Sehat & Persentase Luas:**
```python
mask_sehat = ndvi >= 0.70
luas_sehat_ha = np.sum(mask_sehat) * (1000.0 / ndvi.size)  # Total 1.000 Ha
persentase_sehat = (np.sum(mask_sehat) / ndvi.size) * 100.0

print(f"Persentase Kanopi Sehat : {persentase_sehat:.2f}%")
print(f"Estimasi Luas Area Sehat: {luas_sehat_ha:.2f} Hektar")
```

**c. Analisis Komparasi Kompleksitas Waktu & Memori:**
- **Kompleksitas Waktu:** Keduanya secara teoretis bernilai $\mathcal{O}(N \times M)$ dengan $1.000.000$ operasi. Namun, implementasi Python murni mengalami penundaan besar akibat pencarian tipe objek (*type introspection*) di setiap piksel, membutuhkan waktu $\approx 350 - 500 \text{ ms}$. Implementasi NumPy memanfaatkan instruksi SIMD AVX2 prosesor yang memproses 8 piksel `float32` per siklus jam secara paralel, selesai dalam waktu $< 2 \text{ ms}$ (percepatan $> 200\times$).
- **Efisiensi Memori:** Matriks NumPy `float32` hanya mengonsumsi $1000 \times 1000 \times 4 \text{ byte} = 4 \text{ MB}$ RAM. Bandingkan dengan list 2 dimensi Python yang membutuhkan pointer dan objek `PyFloatObject` dengan total konsumsi $> 32 \text{ MB}$ RAM ($8\times$ lebih boros).

### 4.3 Pembahasan Pemecahan Masalah Aljabar Linier Terapan (Bobot: 30%)
Sistem Persamaan Linier Turbin PKS:
$$\begin{aligned}
2T_1 + 3T_2 + T_3 &= 2800 \\
4T_1 + T_2 + 2T_3 &= 3200 \\
3T_1 + 2T_2 + 4T_3 &= 4200
\end{aligned}$$

**1. Notasi Matriks Kanonik $A \mathbf{x} = \mathbf{b}$:**
$$\begin{bmatrix} 2 & 3 & 1 \\ 4 & 1 & 2 \\ 3 & 2 & 4 \end{bmatrix} \begin{bmatrix} T_1 \\ T_2 \\ T_3 \end{bmatrix} = \begin{bmatrix} 2800 \\ 3200 \\ 4200 \end{bmatrix}$$

**2. Perhitungan Determinan Matriks $A$:**
Gunakan metode ekspansi kofaktor pada baris pertama:
$$\det(A) = 2 \begin{vmatrix} 1 & 2 \\ 2 & 4 \end{vmatrix} - 3 \begin{vmatrix} 4 & 2 \\ 3 & 4 \end{vmatrix} + 1 \begin{vmatrix} 4 & 1 \\ 3 & 2 \end{vmatrix}$$
$$\begin{vmatrix} 1 & 2 \\ 2 & 4 \end{vmatrix} = (1 \times 4) - (2 \times 2) = 4 - 4 = 0$$
$$\begin{vmatrix} 4 & 2 \\ 3 & 4 \end{vmatrix} = (4 \times 4) - (2 \times 3) = 16 - 6 = 10$$
$$\begin{vmatrix} 4 & 1 \\ 3 & 2 \end{vmatrix} = (4 \times 2) - (1 \times 3) = 8 - 3 = 5$$
$$\det(A) = 2(0) - 3(10) + 1(5) = 0 - 30 + 5 = \mathbf{-25}$$
- **Kesimpulan Keunikan Solusi:** Karena $\det(A) = -25 \ne 0$, matriks $A$ bersifat non-singular (*invertible*). Dengan demikian, sistem persamaan linier dijamin **memiliki tepat satu solusi unik tunggal**!

**3. Blok Kode NumPy Penyelesaian Solusi:**
```python
import numpy as np

A = np.array([[2.0, 3.0, 1.0],
              [4.0, 1.0, 2.0],
              [3.0, 2.0, 4.0]])
b = np.array([2800.0, 3200.0, 4200.0])

# Menghitung solusi eksak x = A^-1 * b
x = np.linalg.solve(A, b)

print(f"Output Turbin 1 (T1) = {x[0]:.1f} kWh")
print(f"Output Turbin 2 (T2) = {x[1]:.1f} kWh")
print(f"Output Turbin 3 (T3) = {x[2]:.1f} kWh")
```
*Hasil Komputasi:*
- $T_1 = 440.0 \text{ kWh}$
- $T_2 = 480.0 \text{ kWh}$
- $T_3 = 480.0 \text{ kWh}$

---

## 5. Rubrik Penilaian Berbasis Capaian (OBE Assessment Rubric)

| Dimensi Penilaian | Sangat Kurang (< 50) | Cukup (50 - 69) | Baik (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :--- | :--- | :--- | :--- |
| **Pemahaman Arsitektur Memori & Strides (Kognitif)** | Tidak memahami konsep buffer kontigu dan strides; mengira numpy array identik dengan list python. | Mampu menghitung ukuran memori skalar namun keliru menentukan tupel strides multi-dimensi. | Mampu menghitung strides dengan benar namun kurang tepat dalam menghitung kalkulasi alamat fisik memori heksadesimal. | Menguasai hubungan antara strides, C vs F order, alamat memori absolut heksadesimal, serta mekanisme 0-stride pada broadcasting. |
| **Kemampuan Vektorisasi SIMD (Psikomotorik)** | Masih menggunakan loop bersarang Python murni untuk memproses array data numerik. | Mampu menuliskan operasi vektorisasi dasar namun masih menggunakan list comprehension pada filter spasial. | Mengeliminasi seluruh loop dengan operasi vektorisasi NumPy dan boolean masking secara tepat. | Menghasilkan kode tervektorisasi berkinerja tinggi, menerapkan proteksi pembagian nol yang elegan, dan mengoptimalkan tipe data (*downcasting*). |
| **Penalaran Aljabar Linier Terapan (Afektif & Analisis)** | Tidak dapat menyusun sistem persamaan linier dan mengacaukan perkalian dot dengan hadamard. | Mampu menuliskan kode `np.linalg.solve` namun tidak dapat membuktikan keunikan solusi via determinan. | Menghitung determinan secara benar dan memberikan interpretasi fisis output daya turbin pabrik. | Memberikan analisis mendalam mengenai kestabilan matriks (*condition number*), pembuktian eksak non-singularitas, dan verifikasi residu solusi. |
