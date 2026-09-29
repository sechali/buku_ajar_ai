# Panduan Instruktur & Kunci Solusi: AI Modul 5.5 - Overfitting dan Underfitting dalam Machine Learning

**Program Studi Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian**  
**Fakultas Teknologi Pertanian, Institut Pertanian STIPER Yogyakarta**

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) Sesi 3 SKS (150 Menit)

| Alokasi Waktu | Aktivitas Pembelajaran | Metode & Media | Peran Instruktur | Target Capaian Mahasiswa |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20 Menit) | **Pendahuluan & Apersepsi Konseptual**: Analogi "menghafal kunci jawaban ujian vs memahami konsep". Diskusi mengapa model pintar di laboratorium sering gagal di perkebunan nyata. | Diskusi interaktif, Studi kasus presisi agronomi, Papan tulis / Slide. | Mengarahkan pemikiran mahasiswa bahwa akurasi latih 100% bukan tanda keberhasilan melainkan potensi bahaya. | Memahami definisi mendasar daya generalisasi dan bahaya penghafalan derau data (*noise memorization*). |
| **00:20 - 01:00** (40 Menit) | **Eksplorasi Teori & Penurunan Matematis**: Penurunan aljabar dekomposisi bias-variansi, bedah kurva U total error, diagnostik *learning curves*, dan formulasi penalti penekan variansi ($\ell_1, \ell_2$). | Kuliah mimbar, Penurunan rumus matematis di papan tulis, Analisis diagram komparasi. | Menjelaskan secara bertahap asumsi ekspektasi derau $\mathbb{E}[\epsilon]=0$ dan independensi kesalahan pengamatan. | Mampu merinci trade-off bias-variansi dan membaca pola kurva pembelajaran secara diagnostik. |
| **01:00 - 02:00** (60 Menit) | **Praktikum Terbimbing di Laboratorium Komputer**: Eksekusi notebook komputasi: simulasi bootstrap pembuktian bias-variansi, diagnosis *learning curves*, serta mitigasi Ridge, Lasso, dan *Cost-Complexity Pruning*. | Live coding terbimbing di JupyterLab, Eksperimen interaktif parameter. | Mendampingi mahasiswa saat melakukan penyetelan $\alpha$ regularisasi dan interpretasi grafik hasil dekomposisi. | Mahasiswa berhasil mengontrol osilasi liar polinomial derajat tinggi menggunakan penalti Ridge dan pemangkasan pohon. |
| **02:00 - 02:30** (30 Menit) | **Diskusi Analitis HOTS & Evaluasi OBE**: Analisis mendalam terhadap penurunan formal bias-variansi, studi kasus spektrometri daun sawit, dan kriteria *early stopping* (Soal 8.1 - 8.3). | Presentasi perwakilan kelompok mahasiswa, Umpan balik formatif, Rubrik analitik. | Menguji ketajaman argumentasi matematis dan rekayasa mahasiswa dalam memilih strategi perbaikan model. | Mahasiswa mampu mengambil keputusan mitigasi yang tepat (kapan menambah data vs kapan membatasi model). |

---

## 2. Identifikasi Miskonsepsi Umum Mahasiswa & Strategi Intervensi

### Miskonsepsi 1: "Tujuan pelatihan model AI adalah mencapai Mean Squared Error (MSE) sebesar 0.0 pada data latih."
- **Kenyataan Ilmiah**: MSE latih sama dengan nol hampir selalu mengindikasikan bahwa model memiliki derajat kebebasan yang terlalu tinggi sehingga menghafal fluktuasi derau acak data sampel (*overfitting* ekstrem). Ketika dihadapkan pada data baru di lapangan, galat model akan meledak.
- **Intervensi Pedagogis**: Tunjukkan grafik polinomial derajat 14 pada notebook di mana kurva memotong tepat setiap titik sampel namun berosilasi liar hingga bernilai negatif pada interval antar-titik.

### Miskonsepsi 2: "Jika model berkinerja buruk, solusi terbaik selalu menambahkan lebih banyak data latih."
- **Kenyataan Ilmiah**: Penambahan data hanya efektif mengatasi *overfitting* (variansi tinggi). Jika model mengalami *underfitting* (bias tinggi, misalnya menggunakan garis lurus linier untuk fenomena kuadratik), penambahan sejuta data pun tidak akan memperbaiki performa karena ruang hipotesis model terlalu kaku secara fundamental.
- **Intervensi Pedagogis**: Rujuk grafik *Learning Curves* skenario Underfitting di mana kurva latih dan validasi konvergen pada tingkat galat yang sama-sama tinggi (*high plateau*).

### Miskonsepsi 3: "Regularisasi Ridge dan Lasso menghasilkan efek seleksi model yang sama persis."
- **Kenyataan Ilmiah**: Regularisasi Ridge ($\ell_2$) hanya menyusutkan koefisien mendekati nol tanpa pernah membuatnya tepat nol, sehingga seluruh fitur tetap aktif dalam model. Sebaliknya, Lasso ($\ell_1$) memiliki sifat geometris yang memaksa koefisien fitur bernilai nol eksak, sehingga sekaligus berfungsi sebagai seleksi fitur otomatis.
- **Intervensi Pedagogis**: Perlihatkan hasil praktikum Cell #4 di mana Lasso secara otomatis menonaktifkan 12 dari 14 fitur polinomial dan menyisakan hanya 2 fitur esensial.

### Miskonsepsi 4: "Pohon keputusan (Decision Tree) selalu lebih tahan terhadap overfitting dibandingkan regresi polinomial."
- **Kenyataan Ilmiah**: Pohon keputusan non-parametrik yang tidak dibatasi kedalamannya (*unconstrained tree*) akan terus membelah simpul hingga mencapai daun murni (*pure leaf*), yang menghasilkan $R^2 = 1.0$ pada data latih namun gagal total pada data uji.
- **Intervensi Pedagogis**: Tunjukkan hasil *Cost-Complexity Pruning* pada Cell #5: pohon tanpa pemangkasan memiliki 30 daun terminal yang menghafal sampel, sedangkan pohon terpangkas hanya membutuhkan daun terminal secukupnya untuk generalisasi yang baik.

---

## 3. Kunci Jawaban Lengkap & Pembahasan Mendalam Latihan HOTS

### Pembahasan Soal 8.1: Penurunan Aljabar Formal Bias-Variansi
Diberikan model data $y = f(x) + \epsilon$, dengan $\mathbb{E}[\epsilon] = 0$ dan $\text{Var}(\epsilon) = \mathbb{E}[\epsilon^2] = \sigma^2$. Misalkan $\hat{f}(x)$ adalah fungsi estimasi yang dihasilkan dari himpunan latih $\mathcal{D}$.
Untuk menyederhanakan notasi, tulis $f = f(x)$ dan $\hat{f} = \hat{f}(x)$.

Tinjau ekspansi ekspektasi galat kuadrat:
$$\mathbb{E}[(y - \hat{f})^2] = \mathbb{E}[((f + \epsilon) - \hat{f})^2] = \mathbb{E}[( (f - \hat{f}) + \epsilon )^2]$$
$$\mathbb{E}[(y - \hat{f})^2] = \mathbb{E}[(f - \hat{f})^2] + 2 \mathbb{E}[(f - \hat{f})\epsilon] + \mathbb{E}[\epsilon^2]$$

Karena derau $\epsilon$ bersifat independen terhadap proses pembentukan model $\hat{f}$ dan terhadap data historis latih:
$$\mathbb{E}[(f - \hat{f})\epsilon] = \mathbb{E}[f - \hat{f}] \cdot \mathbb{E}[\epsilon] = \mathbb{E}[f - \hat{f}] \cdot 0 = 0$$
$$\mathbb{E}[\epsilon^2] = \text{Var}(\epsilon) = \sigma^2$$

Sekarang kita uraikan suku pertama $\mathbb{E}[(f - \hat{f})^2]$. Tambahkan dan kurangkan $\mathbb{E}[\hat{f}]$:
$$\mathbb{E}[(f - \hat{f})^2] = \mathbb{E}[\{ (f - \mathbb{E}[\hat{f}]) + (\mathbb{E}[\hat{f}] - \hat{f}) \}^2]$$
$$= \mathbb{E}[(f - \mathbb{E}[\hat{f}])^2] + 2 (f - \mathbb{E}[\hat{f}]) \mathbb{E}[\mathbb{E}[\hat{f}] - \hat{f}] + \mathbb{E}[(\hat{f} - \mathbb{E}[\hat{f}])^2]$$

Perhatikan suku tengah:
$$\mathbb{E}[\mathbb{E}[\hat{f}] - \hat{f}] = \mathbb{E}[\hat{f}] - \mathbb{E}[\hat{f}] = 0$$

Maka tersisa dua suku:
1. $(f - \mathbb{E}[\hat{f}])^2 = (\mathbb{E}[\hat{f}] - f)^2 = \text{Bias}^2(\hat{f})$
2. $\mathbb{E}[(\hat{f} - \mathbb{E}[\hat{f}])^2] = \text{Var}(\hat{f})$

Dengan menggabungkan seluruh komponen:
$$\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}^2(\hat{f}(x)) + \text{Var}(\hat{f}(x)) + \sigma^2 \quad \blacksquare$$

**Asumsi Independensi Derau**: Asumsi $\mathbb{E}[(f - \hat{f})\epsilon] = \mathbb{E}[f - \hat{f}]\mathbb{E}[\epsilon] = 0$ diterapkan secara kritis saat mengeliminasi suku perkalian silang antara kesalahan model dan derau lingkungan. Jika instrumen sensor mengalami kerusakan berkorelasi dengan sinyal masukan, asumsi ini runtuh dan dekomposisi standar tidak lagi berlaku.

### Pembahasan Soal 8.2: Diagnostik Kasus Sensor Spektroskopi
1. **Diagnosis Patologi Model**:
   Model mengalami patologi **Variansi Tinggi (*Overfitting*) Ekstrem**. Indikator utamanya adalah terjadinya jurang pemisah performa (*Generalization Gap*) yang sangat masif: nilai $R^2$ latih mencapai $0.995$ (RMSE $0.08$), namun anjlok drastis menjadi $0.540$ (RMSE $1.42$) pada validasi silang. Model tidak mempelajari hubungan spektral serapan biokimiawi, melainkan menghafal derau fotonika pada 200 pita spektral.
2. **Evaluasi Dua Strategi Perbaikan**:
   - **Strategi (a) Menggandakan data latih dari blok kebun yang sama**: Kurang efektif. Jika sampel tambahan diambil dari blok kebun yang sama, data tersebut membawa karakteristik autokorelasi spasial, kondisi tanah, dan mikroklimat yang identik. Ini tidak menyediakan variasi populasi baru, sehingga model tetap mengalami *overfitting* terhadap blok tersebut.
   - **Strategi (b) Membatasi `max_depth` dan menaikkan `min_samples_leaf`**: **Sangat Efektif (Rekomendasi Utama)**. Pembatasan ini secara langsung menurunkan kapasitas ruang hipotesis model (*regularisasi struktural*). Dengan memaksa setiap daun memiliki minimal sejumlah sampel yang representatif (misal `min_samples_leaf=10`), pohon terhalang untuk membelah simpul guna mengakomodasi *noise* individual, sehingga variansi model tereduksi tajam dan akurasi validasi meningkat.

### Pembahasan Soal 8.3: Desain Eksperimental Penyetelan Regularisasi dan Early Stopping
1. **Rancangan Partisi dan Alur Kerja**:
   - **Data Training (60%)**: Digunakan oleh algoritma optimasi (*Adam* atau *SGD*) untuk memperbarui bobot parameter jaringan dengan penalti $\ell_2$ ($\lambda \sum w_j^2$).
   - **Data Validation (20%)**: Tidak pernah digunakan untuk pembaruan gradien. Setiap akhir siklus (*epoch*), nilai fungsi kerugian validasi ($\mathcal{L}_{\text{val}}$) dihitung untuk mengevaluasi daya generalisasi dan memandu mekanisme *early stopping*.
   - **Data Test (20%)**: Diisolasi sepenuhnya dalam lemari pendingin analitik (*vault*). Hanya dievaluasi satu kali pada arsitektur terbaik akhir untuk estimasi performa riil sebelum *deployment*.
2. **Mekanisme Kriteria Penghentian Berbasis *Patience***:
   Fungsi kerugian validasi pada jaringan syaraf tiruan sering kali menunjukkan osilasi stokastik lokal akibat dinamika *mini-batch*. Kriteria penghentian dengan *patience* $P$ (misal $P = 15$ epoch) beroperasi sebagai berikut:
   - Pantau nilai minimum kerugian validasi terbaik $\mathcal{L}_{\text{val}}^* = \min_{t} \mathcal{L}_{\text{val}}^{(t)}$.
   - Jika pada epoch ke-$t$, $\mathcal{L}_{\text{val}}^{(t)} < \mathcal{L}_{\text{val}}^* - \delta$ (terdapat perbaikan melampaui toleransi minimum $\delta$), simpan *checkpoint* bobot model $\mathbf{W}^* \leftarrow \mathbf{W}^{(t)}$ dan reset pencacah kegagalan $k \leftarrow 0$.
   - Jika $\mathcal{L}_{\text{val}}^{(t)} \ge \mathcal{L}_{\text{val}}^* - \delta$, naikkan pencacah $k \leftarrow k + 1$.
   - Pelatihan dihentikan tepat ketika $k = P$. Bobot model yang dikembalikan adalah bobot pada saat *checkpoint* terbaik $\mathbf{W}^*$, bukan bobot pada epoch penghentian terakhir. Mekanisme ini mencegah algoritma tertipu oleh kenaikan galat sementara (*local noise fluctuation*).

---

## 4. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Aspek Penilaian | Bobot | Sangat Memuaskan (85 - 100) | Memuaskan (70 - 84) | Cukup / Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penurunan Matematis Bias-Variansi (C4)** | 25% | Menurunkan formula secara runtut tanpa cacat aljabar; mengidentifikasi peran krusial independensi derau aditif; menguraikan implikasi $\sigma^2$. | Penurunan aljabar benar secara umum namun terdapat langkah eliminasi suku kovariansi yang kurang dijelaskan secara eksplisit. | Terjadi kesalahan faktual dalam ekspansi kuadratik atau tidak memahami perbedaan antara bias dan variansi. |
| **Analisis Kurva Pembelajaran (C4/C5)** | 25% | Menginterpretasikan grafik *learning curves* dengan tepat; mengidentifikasi *generalization gap*; merumuskan rekomendasi rekayasa yang presisi sesuai diagnosis. | Mampu mengenali kondisi underfit/overfit dari kurva namun usulan perbaikannya masih bersifat generik. | Salah menafsirkan arah kurva galat atau keliru membedakan antara kurva latih dan validasi. |
| **Implementasi Regularisasi Komputasi (C3/C4)** | 30% | Berhasil mengimplementasikan penalti Ridge, Lasso, dan *Cost-Complexity Pruning*; membandingkan koefisien bobot parameter sebelum dan sesudah regularisasi. | Menerapkan salah satu teknik regularisasi dengan benar dan menghasilkan visualisasi prediksi yang layak. | Kode mengalami kegagalan eksekusi atau parameter regularisasi tidak berpengaruh terhadap model. |
| **Perumusan Strategi Mitigasi Operasional (C5)** | 20% | Mampu merancang protokol eksperimen terpadu (*early stopping*, *weight decay*, partisi 3-arah) untuk studi kasus agro-biosains riil dengan argumentasi ilmiah yang kokoh. | Menjelaskan konsep *early stopping* dan partisi data secara konseptual namun kurang rinci pada aspek parameter kontrol (*patience*). | Menyarankan solusi yang keliru (misalnya menambah data pada kasus underfitting ekstrem). |
