# AI Modul 4.5: Panduan Instruktur dan Kunci Solusi
## Exploratory Data Analysis (EDA): Momen Distribusi, Korelasi Non-Linier, dan Paradoks Simpson

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

| Komponen | Rincian Instruksional |
| :--- | :--- |
| **Mata Kuliah** | Sains Data & Kecerdasan Buatan Terapan |
| **Kode Modul** | AI Modul 4.5 |
| **Topik Pembelajaran** | Filosofi EDA John Tukey, Analisis Univariat/Bivariat/Multivariat, Kuartet Anscombe, dan Paradoks Simpson |
| **Alokasi Waktu** | 3 SKS (150 Menit Tatap Muka/Laboratorium + 180 Menit Belajar Mandiri) |
| **Prasyarat** | AI Modul 4.4 (Data Cleaning dan Preprocessing) |
| **Target OBE** | Sub-CPMK 4.5: Mahasiswa mampu menerapkan investigasi grafis tiga tingkat (univariat, bivariat, multivariat), mengevaluasi bentuk distribusi via 4 momen statistik, serta mendeteksi pembalikan tren akibat Paradoks Simpson pada data perkebunan. |

### Matriks Distribusi Jam Pembelajaran (150 Menit)
1. **Sesi Pembuka & Refleksi Filosofis (30 Menit):**
   - Filosofi detektif data John W. Tukey vs pendekatan uji hipotesis konfirmatori klasik.
   - Bedah bahaya *"blind statistics"* melalui Kuartet Anscombe: mengapa mean, varians, dan garis regresi yang identik bisa memiliki realitas fisik data yang bertolak belakang.
2. **Sesi Telaah Konseptual & Matematika Momen (30 Menit):**
   - Pembuktian rumus empat momen statistik formal (mean, varians, skewness Fisher-Pearson, dan excess kurtosis).
   - Pembedaan mendasar antara korelasi linier Pearson ($r$) dan korelasi monotonik peringkat Spearman ($r_s$).
3. **Praktikum Laboratorium Terbimbing (60 Menit):**
   - Eksplorasi berkas `notebooks/part-04/AI_Modul_4.5_Praktikum_Exploratory_Data_Analysis.ipynb`.
   - Menghitung dan memvisualisasikan skewness curah hujan gamma vs tonase panen.
   - Uji komparasi Pearson vs Spearman pada respon saturasi logaritmik kadar minyak sawit (OER).
   - Eksekusi eksperimen langsung Paradoks Simpson: pembuktian korelasi semu negatif global ($r = -0.60$) vs korelasi nyata positif lokal ($r = +0.80$).
4. **Sesi Evaluasi & Diskusi HOTS (30 Menit):**
   - Presentasi kasus Paradoks Simpson pada uji efektivitas herbisida (Rawa Basah vs Bukit Kering).
   - Rekomendasi transformasi data miring (Log / Box-Cox) sebelum pemodelan AI.

---

## 2. Strategi Pedagogis dan Panduan Fasilitasi Kelas

### 2.1 Eksperimen Pemicu: "Guess the Correlation"
Sebelum memulai materi, proyeksikan plot Kuartet Anscombe ke layar tanpa menampilkan titik data (hanya tampilkan persamaan regresi $y = 3.0 + 0.5x$ dan $R^2 = 0.67$):
- Mintalah mahasiswa menebak apakah model regresi linier tersebut sudah akurat untuk semua dataset.
- Setelah mahasiswa sepakat bahwa modelnya "bagus", buka plot aslinya (menampilkan kurva parabola, titik pencilan ekstrem, dan titik leverage).
- Simpulkan pelajaran kuncinya: *"Angka ringkasan statistik dapat menipu, grafik visual tidak pernah berbohong."*

### 2.2 Panduan Analisis Causal AI: Membongkar Confounding Factor
Tanamkan prinsip kausalitas Judea Pearl saat membahas Paradoks Simpson:
> *"Ketika Anda menemukan korelasi yang berlawanan dengan akal sehat agronomi (misalnya pupuk menyebabkan penurunan produksi), jangan salahkan tanamannya. Cari variabel pengganggu ketiga (confounding variable)—seperti tipe tanah, ketinggian lahan, atau usia tanaman—yang mengendalikan kedua variabel tersebut secara simultan."*

---

## 3. Identifikasi dan Remediasi Miskonsepsi Mahasiswa

### Miskonsepsi 1: "Korelasi Pearson yang mendekati nol ($r \approx 0$) berarti kedua variabel tidak memiliki hubungan."
- **Koreksi Konseptual:** Korelasi Pearson hanya mengukur hubungan **linier**. Jika dua variabel memiliki hubungan non-linier kuadratik sempurna ($Y = X^2$ pada rentang $-10 \le X \le 10$), nilai Pearson akan persis $0.00$. Mahasiswa harus selalu memverifikasi bentuk hubungan secara visual melalui *scatter plot* atau menggunakan korelasi non-parametrik (Spearman/Kendall).

### Miskonsepsi 2: "Korelasi agregat global selalu merefleksikan tren di setiap sub-kelompok."
- **Koreksi Konseptual:** Ini adalah anomali *Simpson's Paradox*. Menggabungkan populasi heterogen tanpa stratifikasi dapat membalikkan arah korelasi positif menjadi negatif (atau sebaliknya). Analis wajib melakukan dekomposisi data berdasarkan faktor demografis atau agronomis penting.

### Miskonsepsi 3: "Histogram dan Bar Chart (Diagram Batang) adalah grafik yang sama."
- **Koreksi Konseptual:** Bar chart digunakan untuk variabel diskrit kategorikal (batang terpisah dengan celah spasi; urutan kategori bisa diubah bebas). Sedangkan Histogram digunakan untuk variabel kontinu numerik (batang saling menempel tanpa celah; sumbu horizontal terikat pada skala interval numerik berkesinambungan).

### Miskonsepsi 4: "Eksplorasi data selesai setelah menghitung `df.describe()`."
- **Koreksi Konseptual:** `describe()` hanya menampilkan ringkasan univariat dasar (mean, std, min, max, kuartil). Fungsi ini tidak memperlihatkan bentuk kemencengan (*skewness*), keruncingan (*kurtosis*), keberadaan multi-modalitas (puncak ganda), maupun matriks korelasi antar-fitur.

---

## 4. Kunci Solusi dan Pembahasan Soal Latihan & HOTS

### 4.1 Pembahasan Analisis Distribusi dan Momen Statistik (Bobot: 30%)
Diketahui data sensus janjang panen sawit:
- Rerata ($\bar{x}$) = $14.2$
- Median ($\tilde{x}$) = $11.5$
- Modus = $9.0$
- Koefisien Kemencengan (*Skewness*) $g_1 = +1.45$
- Excess Kurtosis $g_2 = +2.80$

**1. Karakterisasi Bentuk Sebaran:**
- Karena $g_1 = +1.45 > 0.5$, distribusi data bersifat **menceng ke kanan (*Right-Skewed / Positively Skewed*)**.
- Hubungan urutan nilai sentral mematuhi hukum empiris distribusi menceng kanan:
  $$\mathbf{\text{Modus } (9.0) < \text{Median } (11.5) < \text{Rerata } (14.2)}$$
- Puncak kurva frekuensi berada di sebelah kiri ($9.0$), dengan ekor panjang yang menjulur ke sisi kanan atas.

**2. Implikasi Agronomi Terhadap Logistik Truk:**
- Nilai *skewness* positif menunjukkan bahwa **sebagian besar pokok sawit ($> 50\%$) menghasilkan janjang di bawah rata-rata** (hanya sekitar $9 - 11$ janjang/pokok). Namun, terdapat sebagian kecil pokok sawit unggul yang menghasilkan janjang luar biasa banyak yang menarik nilai rerata ke atas menjadi $14.2$.
- Nilai kurtosis leptokurtik ($g_2 = +2.80 > 0$) mengindikasikan adanya ekor tebal (*fat tails*), yaitu adanya konsentrasi titik-titik panen raya ekstrem pada blok-blok tertentu.
- *Implikasi Operasional:* Alokasi armada truk tidak boleh didasarkan semata-mata pada perkalian rata-rata global ($14.2 \times \text{jumlah pokok}$), karena akan memicu kekurangan armada truk yang parah pada blok-blok panen raya ekstrem dan pemborosan truk pada blok-blok yang produksinya rendah.

**3. Rekomendasi Transformasi Penormalan Distribusi:**
Karena data menceng ke kanan dengan nilai positif, transformasi yang direkomendasikan adalah:
- **Transformasi Logaritmik:** $y = \ln(x)$ atau $y = \log_{10}(x + 1)$ (paling praktis untuk mereduksi rentang nilai ekor kanan).
- **Transformasi Pangkat Box-Cox:** Menemukan parameter optimal $\lambda$ secara otomatis:
  $$y^{(\lambda)} = \begin{cases} \frac{x^\lambda - 1}{\lambda}, & \text{jika } \lambda \ne 0 \\ \ln(x), & \text{jika } \lambda = 0 \end{cases}$$

---

### 4.2 Pembahasan Investigasi Bivariat Pearson vs Spearman (Bobot: 30%)
Data dosis KCl ($X$) dan kadar OER ($Y$):
$$X = \{ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 \}$$
$$Y = \{ 18.0, 21.5, 23.8, 24.9, 25.2, 25.3 \}$$
Ukuran sampel $n = 6$.

**1. Perhitungan Korelasi Peringkat Spearman ($r_s$):**
- Peringkat variabel $X$ (sudah terurut naik): $\text{Rank}(X) = [1, 2, 3, 4, 5, 6]$.
- Peringkat variabel $Y$ (karena nilai $Y$ juga meningkat secara monoton sempurna: $18.0 < 21.5 < 23.8 < 24.9 < 25.2 < 25.3$):
  $$\text{Rank}(Y) = [1, 2, 3, 4, 5, 6]$$
- Selisih peringkat $d_i = \text{Rank}(X_i) - \text{Rank}(Y_i) = [0, 0, 0, 0, 0, 0]$.
- Jumlah kuadrat selisih $\sum d_i^2 = 0$.
- Nilai Korelasi Spearman:
  $$r_s = 1 - \frac{6 \times 0}{6(36 - 1)} = \mathbf{1.0000 \text{ (Monotonik Positif Sempurna)}}$$

**2. Perhitungan Korelasi Linier Pearson ($r$):**
- $\bar{x} = \frac{1+2+3+4+5+6}{6} = 3.5$
- $\bar{y} = \frac{18.0 + 21.5 + 23.8 + 24.9 + 25.2 + 25.3}{6} = \frac{138.7}{6} \approx 23.117$
- Menghitung deviasi dan perkalian:
  $$\sum (x_i - \bar{x})^2 = (-2.5)^2 + (-1.5)^2 + (-0.5)^2 + (0.5)^2 + (1.5)^2 + (2.5)^2 = 17.5$$
  $$\sum (y_i - \bar{y})^2 = (-5.117)^2 + (-1.617)^2 + (0.683)^2 + (1.783)^2 + (2.083)^2 + (2.183)^2 \approx 41.568$$
  $$\sum (x_i - \bar{x})(y_i - \bar{y}) = (-2.5)(-5.117) + (-1.5)(-1.617) + (-0.5)(0.683) + (0.5)(1.783) + (1.5)(2.083) + (2.5)(2.183) \approx 24.45$$
- Koefisien Pearson:
  $$r = \frac{24.45}{\sqrt{17.5 \times 41.568}} = \frac{24.45}{\sqrt{727.44}} = \frac{24.45}{26.97} \approx \mathbf{0.9065}$$

**3. Analisis Komparasi:**
- Nilai $r_s = 1.000 > r = 0.9065$. Spearman bernilai sempurna ($1.0$) karena hubungan matematis kedua variabel bersifat **monoton murni** (setiap kenaikan dosis selalu menghasilkan kenaikan kadar minyak, tanpa pernah menurun).
- Nilai Pearson lebih rendah ($0.9065$) karena respon biologis tanaman mengalami **hukum hasil yang semakin menurun (*Law of Diminishing Returns*)**: penambahan pupuk dari $1 \to 2 \text{ kg}$ melonjakkan OER sebesar $+3.5\%$, namun penambahan dari $5 \to 6 \text{ kg}$ hanya menaikkan OER sebesar $+0.1\%$. Garis lurus Pearson tidak mampu menangkap lengkungan kurva saturasi ini secara sempurna.

---

### 4.3 Pembahasan Dekonstruksi Paradoks Simpson (Bobot: 40%)

**1. Pembuktian Matematis Paradoks Simpson:**
- **Analisis Lokal per Divisi:**
  - *Divisi Rawa Basah:*
    - Herbisida Baru: $\frac{180}{300} = \mathbf{60.0\%}$
    - Herbisida Lama: $\frac{35}{70} = \mathbf{50.0\%}$
    - **Pemenang: Herbisida Formula Baru LEBIH UNGGUL ($+10.0\%$)!**
  - *Divisi Bukit Kering:*
    - Herbisida Baru: $\frac{95}{100} = \mathbf{95.0\%}$
    - Herbisida Lama: $\frac{270}{300} = \mathbf{90.0\%}$
    - **Pemenang: Herbisida Formula Baru LEBIH UNGGUL ($+5.0\%$)!**
- **Analisis Agregat Global (Gabungan Seluruh Kebun):**
  - Herbisida Baru: $\frac{275}{400} = \mathbf{68.75\%}$
  - Herbisida Lama: $\frac{305}{370} = \mathbf{82.43\%}$
  - **Pemenang: Herbisida Formula Lama SEOLAH-OLAH LEBIH UNGGUL ($+13.68\%$)!**
- **Kesimpulan:** Terbukti secara sah terjadi **Paradoks Simpson**, di mana Formula Baru menang di setiap divisi individual, namun kalah telak saat data digabungkan secara global.

**2. Identifikasi Confounding Factor:**
- Faktor pengganggunya adalah **Tingkat Kesulitan Medan Lingkungan (Rawa Basah vs Bukit Kering)** dan **Alokasi Sampel yang Sangat Tidak Proporsional**:
  - Divisi Rawa Basah merupakan medan yang jauh lebih sulit dibasmi gulmanya (efektivitas rata-rata hanya $\approx 50 - 60\%$).
  - Divisi Bukit Kering merupakan medan yang sangat mudah (efektivitas rata-rata $\approx 90 - 95\%$).
  - Herbisida Baru diuji mayoritas di medan yang sangat sulit (300 dari 400 petak $= 75\%$ di Rawa Basah).
  - Sebaliknya, Herbisida Lama diuji mayoritas di medan yang sangat mudah (300 dari 370 petak $= 81\%$ di Bukit Kering).

**3. Rekomendasi kepada Direksi Manajemen:**
- **Rekomendasi Mutlak: PILIH HERBISIDA FORMULA BARU!**
- **Argumentasi Ilmiah:** Angka agregat global $82.43\%$ vs $68.75\%$ adalah ilusi statistik akibat bias alokasi sampel. Jika Herbisida Baru diterapkan pada kondisi medan yang setara, efektivitasnya selalu mengungguli Formula Lama (unggul $+10\%$ di lahan basah dan unggul $+5\%$ di lahan kering). Mengadopsi Formula Baru dijamin meningkatkan efisiensi operasional kebun secara nyata.

---

## 5. Rubrik Penilaian Berbasis Capaian (OBE Assessment Rubric)

| Dimensi Penilaian | Sangat Kurang (< 50) | Cukup (50 - 69) | Baik (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Filosofi EDA & 4 Momen (Kognitif)** | Tidak memahami filosofi Tukey; hanya mengandalkan nilai rerata tanpa memeriksa sebaran grafis. | Mengetahui konsep skewness namun keliru mengidentifikasi urutan mean, median, modus pada data miring. | Mampu menghitung 4 momen distribusi statistik dan menginterpretasikan implikasi fisiknya pada operasional kebun. | Menguasai estimasi skewness Fisher-Pearson, excess kurtosis, serta mampu merekomendasikan formula transformasi penormalan yang tepat. |
| **Keterampilan Analisis Bivariat & Multivariat (Psikomotorik)** | Mengacaukan korelasi Pearson dan Spearman; mengabaikan asumsi linearitas bivariat. | Menghitung korelasi dengan benar namun tidak dapat menjelaskan mengapa Spearman bernilai lebih tinggi pada kurva saturasi. | Mampu menghitung $r$ dan $r_s$ secara presisi serta membangun matriks heatmap korelasi multivariat yang rapi. | Menganalisis respon saturasi biologis secara mendalam, mendeteksi multikolinieritas antar-fitur iklim, dan memvisualisasikan data secara elegan. |
| **Penalaran Kausalitas & Paradoks Simpson (Afektif & Kritis)** | Terjebak dalam angka agregat global dan menyimpulkan herbisida yang salah; tidak memahami Paradoks Simpson. | Menyadari adanya pembalikan tren namun gagal mengidentifikasi variabel pengganggu (*confounding factor*). | Membuktikan Paradoks Simpson secara matematis dan menjelaskan peran alokasi sampel yang tidak seimbang. | Memberikan rekomendasi bisnis manajerial tingkat eksekutif yang solid, berbasis inferensi kausalitas terbukti, dan tak terbantahkan. |
