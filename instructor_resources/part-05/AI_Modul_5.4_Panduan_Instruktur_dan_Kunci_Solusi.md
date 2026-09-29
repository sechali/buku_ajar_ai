# Panduan Instruktur & Kunci Solusi: AI Modul 5.4 - Features dan Labels dalam Machine Learning

**Program Studi Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian**  
**Fakultas Teknologi Pertanian, Institut Pertanian STIPER Yogyakarta**

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) Sesi 3 SKS (150 Menit)

| Alokasi Waktu | Aktivitas Pembelajaran | Metode & Media | Peran Instruktur | Target Capaian Mahasiswa |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20 Menit) | **Pendahuluan & Apersepsi Konseptual**: Analogi representasi data dunia nyata ke dalam format aljabar linier ($X$ dan $y$). Diskusi fenomena kegagalan model akibat kebocoran data. | Ceramah interaktif, Studi kasus panen kelapa sawit, Polling kelas. | Menstimulasi nalar kritis mahasiswa mengenai perbedaan mendasar antara data mentah (*raw data*) dan matriks terstruktur. | Memahami kedudukan matriks desain $X$ dan vektor target $y$ dalam alur kerja machine learning. |
| **00:20 - 01:00** (40 Menit) | **Eksplorasi Teori & Perumusan Matematis**: Pembahasan tipologi skala pengukuran fitur, *Curse of Dimensionality*, konsentrasi jarak Euclidean, serta 3 paradigma seleksi fitur (*Filter*, *Wrapper*, *Embedded*). | Presentasi visual dengan proyektor, Penurunan rumus matematis, Bedah diagram arsitektur. | Membimbing pembuktian matematis kelangkaan spasial pada hiperkubus berdimensi tinggi ($s = v^{1/d}$). | Menguasai kelebihan dan kompromi komputasi antara metode *Filter*, *Wrapper*, dan *Embedded*. |
| **01:00 - 02:00** (60 Menit) | **Praktikum Terbimbing di Laboratorium Komputer**: Eksekusi notebook praktikum, rekayasa encoding kategorikal, simulasi numerik *curse of dimensionality*, dan perbandingan akurasi seleksi fitur. | Live coding terbimbing di JupyterLab, Scikit-Learn Pipeline. | Berkeliling laboratorium, mendeteksi galat sintaksis, memfasilitasi mahasiswa yang mengalami kendala teknis *ColumnTransformer*. | Menghasilkan kode Python modular yang mengeksekusi seleksi fitur dan membuktikan keruntuhan akurasi saat *target leakage* terjadi. |
| **02:00 - 02:30** (30 Menit) | **Diskusi Analitis HOTS & Evaluasi OBE**: Pembahasan mendalam terhadap studi kasus kelapa sawit dan spektrometri reflektansi daun (Soal 8.1 - 8.3). | Presentasi perwakilan kelompok, Diskusi panel interaktif, Umpan balik formatif. | Menilai kedalaman argumen teknis mahasiswa berdasarkan rubrik OBE dan meluruskan miskonsepsi yang tersisa. | Mampu merancang pipeline pemrosesan fitur yang bebas dari kebocoran data dan optimal secara komputasi. |

---

## 2. Identifikasi Miskonsepsi Umum Mahasiswa & Strategi Intervensi

### Miskonsepsi 1: "Semakin banyak fitur yang dimasukkan ke dalam model, semakin pintar dan akurat model tersebut."
- **Kenyataan Ilmiah**: Menambah fitur yang tidak relevan atau hanya berupa *noise* akan meningkatkan variansi model, memperbesar risiko *overfitting*, memperlambat waktu komputasi, dan memicu *curse of dimensionality* di mana titik data menjadi sangat terisolasi dalam ruang berdimensi tinggi.
- **Intervensi Pedagogis**: Tampilkan hasil eksperimen praktikum di mana model dengan 50 fitur menghasilkan akurasi lebih rendah (81.1%) dibandingkan model yang hanya memilih 10 fitur informatif melalui *Embedded Random Forest* (82.8%).

### Miskonsepsi 2: "Variabel kategorikal bertingkat cukup di-encode dengan integer berurutan (0, 1, 2) untuk menghemat memori."
- **Kenyataan Ilmiah**: Menggunakan *Label Encoding* / integer pada variabel kategorikal nominal (misal: Varietas Kelapa Sawit `Dumpy=0, Yangambi=1, Avros=2`) memaksa model linier atau jarak untuk mengasumsikan bahwa `Avros` bernilai 2 kali lipat dari `Yangambi`, atau bahwa jarak `Dumpy` ke `Avros` adalah 2 unit. Ini memperkenalkan relasi metrik palsu.
- **Intervensi Pedagogis**: Tekankan perbedaan tegas antara data ordinal (yang memiliki hierarki alami seperti kelas lereng) dan nominal (yang wajib diubah via *One-Hot Encoding*).

### Miskonsepsi 3: "Akurasi pelatihan dan pengujian 99.8% membuktikan model siap diluncurkan ke sistem operasional perkebunan."
- **Kenyataan Ilmiah**: Kinerja mendekati sempurna pada tahap eksperimen lab hampir selalu merupakan gejala patologis *target leakage* (*kebocoran target*), di mana fitur input secara tidak sengaja memuat variabel pascakejadian.
- **Intervensi Pedagogis**: Minta mahasiswa menjalankan Cell #5 pada notebook untuk melihat sendiri bagaimana model dengan akurasi 100% di pengujian langsung ambruk menjadi 48.3% ketika diuji dengan variasi data lapangan tanpa fitur bocor.

### Miskonsepsi 4: "Seleksi fitur sama persis dengan reduksi dimensi berbasis ekstraksi fitur seperti PCA."
- **Kenyataan Ilmiah**: Seleksi fitur (*feature selection*) mempertahankan representasi asli variabel fisik (misal: tetap memilih variabel curah hujan dan kadar air tanah), sehingga model tetap memiliki kemampuan interpretabilitas tinggi. Reduksi dimensi berbasis ekstraksi (*feature extraction* seperti PCA) memproyeksikan fitur ke ruang ortogonal baru yang merupakan kombinasi linier dari seluruh variabel asli, sehingga menghilangkan arti fisik variabel input.
- **Intervensi Pedagogis**: Tekankan kebutuhan agronomis perkebunan: praktisi lapangan membutuhkan rekomendasi spesifik (misal: "tambah dosis pupuk fosfat"), bukan informasi "tingkatkan komponen utama 1".

---

## 3. Kunci Jawaban Lengkap & Pembahasan Mendalam Latihan HOTS

### Pembahasan Soal 8.1: Evaluasi Kritis Bahaya Target Leakage pada Model Agro-IoT
1. **Analisis Penyebab Kebocoran Target**:
   Variabel "status penyemprotan fungisida kuratif" baru dicatat atau dilakukan *setelah* pohon terdeteksi secara visual atau klinis terinfeksi jamur *Ganoderma boninense*. Memasukkan variabel ini sebagai fitur input prediktor merupakan kesalahan kausalitas temporal. Model tidak belajar mendeteksi gejala awal infeksi dari sensor tanah atau satelit, melainkan hanya menghafal fakta bahwa jika pohon disemprot fungisida kuratif, maka pohon tersebut pasti sakit ($Y=1$).
2. **Pembuktian Formal Kerusakan Probabilitas Posterior $P(Y=1 \mid X)$**:
   Misalkan $X = \{X_{\text{sensor}}, X_{\text{fungisida}}\}$. Variabel $X_{\text{fungisida}}$ memiliki ketergantungan deterministik terhadap label target:
   $$P(X_{\text{fungisida}} = 1 \mid Y = 1) \approx 1.0 \quad \text{dan} \quad P(X_{\text{fungisida}} = 1 \mid Y = 0) = 0.0$$
   Berdasarkan Teorema Bayes:
   $$P(Y = 1 \mid X_{\text{sensor}}, X_{\text{fungisida}} = 1) = \frac{P(X_{\text{sensor}} \mid Y=1) P(X_{\text{fungisida}}=1 \mid Y=1) P(Y=1)}{\sum_{y \in \{0,1\}} P(X_{\text{sensor}} \mid Y=y) P(X_{\text{fungisida}}=1 \mid Y=y) P(Y=y)} = 1.0$$
   Pada kondisi operasional lapangan, sistem ditugaskan mendeteksi pohon yang *belum* disemprot ($X_{\text{fungisida}} = 0$). Karena selama fase latihan model mengasosiasikan status tanpa semprotan dengan tanaman sehat, maka model akan memprediksi probabilitas infeksi mendekati 0 untuk semua tanaman, menyebabkan kegagalan deteksi total (*false negative rate* 100%).

### Pembahasan Soal 8.2: Desain Eksperimental Penanganan Multikolinearitas dan Dimensi Tinggi
1. **Kegagalan OLS pada Dimensi $d > n$**:
   Pada kasus spektrometri $d = 1.200$ panjang gelombang dan $n = 150$ sampel, matriks desain $X \in \mathbb{R}^{150 \times 1200}$. Matriks kovariansi $\mathbf{X}^T \mathbf{X} \in \mathbb{R}^{1200 \times 1200}$ memiliki *rank* maksimum $\min(n, d) = 150$. Karena *rank* (150) jauh lebih kecil dari dimensi matriks (1200), matriks $\mathbf{X}^T \mathbf{X}$ bersifat **singular** (determinan bernilai 0) dan tidak memiliki invers:
   $$\hat{\mathbf{w}}_{\text{OLS}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y} \quad \text{(Tidak terdefinisi / Tidak dapat dihitung)}$$
   Selain itu, panjang gelombang yang berdekatan memiliki korelasi sangat mendekati 1.0 (*multikolinearitas ekstrem*), menyebabkan nilai eigen mendekati nol dan melipatgandakan variansi estimasi parameter ke tak hingga.
2. **Rancangan Komparasi Arsitektur Mitigasi**:
   - **Pendekatan Regularisasi Elastic Net**:
     $$\min_{\mathbf{w}} \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \lambda_1 \|\mathbf{w}\|_1 + \frac{\lambda_2}{2} \|\mathbf{w}\|_2^2$$
     Penalti $\ell_2$ menstabilkan invers matriks $(\mathbf{X}^T \mathbf{X} + \lambda_2 \mathbf{I})^{-1}$ sehingga selalu nonsingular, sementara penalti $\ell_1$ menyeleksi sekelompok panjang gelombang paling informatif yang berkorelasi (*grouped selection*). Keunggulan: mempertahankan interpretabilitas pita spektral fisik (misal: pita 680 nm dan 720 nm yang berkaitan langsung dengan serapan klorofil).
   - **Pendekatan Principal Component Regression (PCR)**:
     Melakukan dekomposisi nilai singular (SVD) $\mathbf{X} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$, memilih $k$ komponen utama pertama ($k \ll n$), lalu meregresikan target pada skor proyeksi $\mathbf{Z} = \mathbf{X}\mathbf{V}_k$. Keunggulan: secara definitif meniadakan multikolinearitas karena kolom-kolom $\mathbf{Z}$ bersifat ortogonal murni ($Z^T Z$ diagonal).

### Pembahasan Soal 8.3: Komparasi Algoritmik Filter vs Wrapper vs Embedded
1. **Analisis Ketertelusuran Komputasi Wrapper RFE**:
   Pada $d = 50.000$ dan $n = 500$, kompleksitas komputasi pelatihan satu unit model Support Vector Machine (SVM) dengan solver kuadratik berskala antara $\mathcal{O}(n^2 d)$ hingga $\mathcal{O}(n^3)$. 
   Jika RFE mengeliminasi 1 fitur per langkah, maka dibutuhkan 50.000 iterasi pelatihan model SVM:
   $$\text{Total Operasi Komputasi} \approx \sum_{k=1}^{50000} \mathcal{O}(n^2 k) \approx \mathcal{O}\left( n^2 \frac{d^2}{2} \right) \approx 250.000 \times \frac{2.5 \times 10^9}{2} \approx 3.125 \times 10^{14} \text{ operasi}$$
   Beban ini memerlukan waktu komputasi berhari-hari hingga berminggu-minggu pada komputer standar dan sangat rentan memicu kehabisan alokasi memori (*Out Of Memory* / OOM).
2. **Rekomendasi Pipeline Hibrida Dua Tahap (*Two-Stage Hybrid*)**:
   - **Tahap 1 (Screening Skala Besar / Filter)**: Gunakan uji statistik ANOVA F-Value atau *Mutual Information* yang berkecepatan $\mathcal{O}(nd)$ untuk memangkas 50.000 fitur SNP menjadi 500 kandidat teratas dalam hitungan detik.
   - **Tahap 2 (Optimasi Relasi Non-linier / Embedded/Wrapper Ringkas)**: Terapkan *Random Forest Feature Importance* atau RFE dengan *step-size* pangkas 20% pada 500 fitur kandidat tersebut untuk mendapatkan 30 penanda SNP paling esensial.

---

## 4. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Aspek Penilaian | Bobot | Sangat Memuaskan (85 - 100) | Memuaskan (70 - 84) | Cukup / Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Representasi & Transformasi Fitur (C3)** | 25% | Matriks desain $X$ dan target $y$ disusun dengan akurat; encoding ordinal dan nominal diterapkan dengan tepat tanpa kebocoran data; normalisasi terisolasi dalam pipeline. | Data di-encode dengan benar namun ada sedikit ketidaktepatan dalam pemisahan data latih/uji pada tahap pra-pemrosesan. | Menerapkan label encoding sembarangan pada data nominal atau terjadi pelanggaran dimensi matriks. |
| **Pemahaman Teori & Curse of Dimensionality (C4)** | 25% | Mampu menguraikan secara matematis konsep kelangkaan hiperkubus ($s = v^{1/d}$) dan dampak konsentrasi jarak Euclidean terhadap algoritma spasial. | Memahami konsep kutukan dimensi secara konseptual namun kurang mendalam dalam penjabaran formulasinya. | Tidak mampu menjelaskan kaitan antara penambahan dimensi dan degradasi metrik jarak. |
| **Implementasi Seleksi Fitur (C4/C5)** | 30% | Berhasil mengimplementasikan metode Filter, Wrapper, dan Embedded dalam pipeline Scikit-Learn; menganalisis kompromi performa dan efisiensi waktu komputasi secara tajam. | Mengimplementasikan minimal dua metode seleksi fitur dengan hasil akurasi yang valid namun tanpa analisis perbandingan mendalam. | Kode seleksi fitur gagal berjalan atau tidak menunjukkan reduksi dimensi yang terukur. |
| **Analisis Forensik Target Leakage & Etika Data (C5)** | 20% | Mampu mendeteksi secara kritis keberadaan variabel bocor pada studi kasus, membuktikan kegagalan operasionalnya, dan merancang protokol isolasi temporal. | Mengenali adanya variabel yang tidak realistis namun argumen mitigasinya kurang terstruktur secara metodologis. | Menganggap akurasi 100% pada model bocor sebagai keberhasilan tanpa menyadari bahaya fatalnya. |
