# Panduan Instruktur & Kunci Solusi: AI Modul 5.6 - Proses Training Model dalam Machine Learning

**Program Studi Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian**  
**Fakultas Teknologi Pertanian, Institut Pertanian STIPER Yogyakarta**

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) Sesi 3 SKS (150 Menit)

| Alokasi Waktu | Aktivitas Pembelajaran | Metode & Media | Peran Instruktur | Target Capaian Mahasiswa |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20 Menit) | **Pendahuluan & Apersepsi Konseptual**: Analogi "menuruni lembah berkabut tebal menggunakan ketinggian tanah". Pengenalan konsep optimasi parameter $\boldsymbol{\theta}$. | Diskusi kelas interaktif, Analogi fisik topografi, Slide presentasi. | Mengarahkan mahasiswa melihat pelatihan model sebagai pencarian dasar lembah fungsi biaya secara bertahap. | Memahami perbedaan konseptual antara fungsi kerugian ($\mathcal{L}$) dan fungsi biaya agregat ($J(\boldsymbol{\theta})$). |
| **00:20 - 01:00** (40 Menit) | **Eksplorasi Teori & Penurunan Matematis**: Penurunan vektor gradien $\nabla J(\boldsymbol{\theta})$ untuk MSE, perbandingan BGD vs SGD vs MBGD, peran learning rate $\eta$, dan lanskap kontur eliptik. | Kuliah mimbar, Penurunan kalkulus vektor di papan tulis, Analisis diagram kontur. | Membimbing penurunan turunan parsial $\frac{\partial J}{\partial \boldsymbol{\theta}}$ dan pembuktian matematis batas stabilitas $\eta < \frac{2}{a}$. | Menguasai prinsip komputasi penurunan gradien serta syarat kestabilan konvergensi numerik. |
| **01:00 - 02:00** (60 Menit) | **Praktikum Terbimbing di Laboratorium Komputer**: Implementasi algoritma BGD, SGD, dan MBGD dari dasar (*from scratch*), visualisasi trajektori loss, dan penyetelan `SGDRegressor` dengan *early stopping*. | Live coding terbimbing di JupyterLab, Penyelidikan galat numerik (*overflow*). | Memfasilitasi mahasiswa saat menguji data tanpa standarisasi agar mereka melihat langsung bahaya ledakan gradien. | Mahasiswa terampil menulis kode optimasi numerik dan membaca kurva konvergensi fungsi biaya. |
| **02:00 - 02:30** (30 Menit) | **Diskusi Analitis HOTS & Evaluasi OBE**: Pembahasan mendalam kondisi batas konvergensi, fenomena *gradient explosion*, dan arsitektur *streaming* IoT perkebunan (Soal 8.1 - 8.3). | Diskusi kelompok, Presentasi komparasi teknis, Umpan balik formatif instruktur. | Menilai kemampuan sintesis mahasiswa dalam memilih optimizer yang tepat untuk batasan memori dan kecepatan *edge computing*. | Mampu merancang sistem pelatihan model adaptif untuk data berskala besar di lingkungan produksi pertanian. |

---

## 2. Identifikasi Miskonsepsi Umum Mahasiswa & Strategi Intervensi

### Miskonsepsi 1: "Nilai learning rate ($\eta$) yang semakin besar akan selalu mempercepat waktu pelatihan model."
- **Kenyataan Ilmiah**: Jika nilai $\eta$ melampaui batas kurvatur fungsi biaya ($\eta > 2 / \lambda_{\max}$), algoritma *Gradient Descent* akan melompati lembah minimum dan berosilasi secara divergen (*overshooting*), menyebabkan nilai fungsi biaya meledak ke angka tak hingga (`NaN`).
- **Intervensi Pedagogis**: Mintalah mahasiswa mengeksekusi Cell #4 pada notebook dengan $\eta = 0.95$ dan mengamati kurva galat yang melambung tinggi alih-alih menurun.

### Miskonsepsi 2: "Standarisasi fitur (*feature scaling*) hanyalah tahapan opsional yang tidak memengaruhi hasil akhir pelatihan."
- **Kenyataan Ilmiah**: Pada fitur dengan rentang skala yang sangat timpang (misal radiasi $10 - 25$ vs konsentrasi ppm $0.001 - 0.005$), lanskap fungsi biaya menjadi elips yang sangat pipih (*ill-conditioned*). Vektor gradien akan menunjuk hampir tegak lurus terhadap arah minimum global, memicu osilasi zigzag yang memperlambat konvergensi ribuan kali lipat atau memicu *gradient explosion*.
- **Intervensi Pedagogis**: Tunjukkan diagram lanskap kontur optimasi pada diktat dan instruksikan mahasiswa mencoba fungsi `run_bgd` pada data mentah tanpa `StandardScaler` untuk menyaksikan kegagalan numerik.

### Miskonsepsi 3: "Solusi analitik persamaan normal OLS selalu lebih unggul karena tidak memerlukan iterasi."
- **Kenyataan Ilmiah**: Solusi persamaan normal $\boldsymbol{\theta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$ menuntut inversi matriks berdimensi $d \times d$ dengan kompleksitas komputasi $\mathcal{O}(d^3)$. Pada data modern dengan puluhan ribu fitur (seperti genomik atau spektrometri), metode ini memakan memori teramat besar dan berujung pada kegagalan memori (*Out Of Memory* / OOM).
- **Intervensi Pedagogis**: Bandingkan tabel komparasi pada Bagian 5 diktat: tegaskan bahwa untuk $d > 20.000$, algoritma berbasis Mini-Batch GD merupakan satu-satunya pilihan yang terukur (*scalable*).

### Miskonsepsi 4: "Stochastic Gradient Descent (SGD) dan Batch Gradient Descent (BGD) selalu konvergen ke titik parameter yang identik persis."
- **Kenyataan Ilmiah**: BGD berhenti persis pada titik stasioner di mana $\nabla J(\boldsymbol{\theta}) = \mathbf{0}$. Sebaliknya, SGD menggunakan aproksimasi gradien dari satu sampel acak yang memuat derau statistik tinggi, sehingga parameternya terus melompat-lompat di sekitar wilayah minimum tanpa pernah diam secara permanen, kecuali laju belajar diturunkan bertahap (*learning rate annealing*).
- **Intervensi Pedagogis**: Perlihatkan trajektori bergerigi SGD pada Diagram 1 dan diskusikan peran *Mini-Batch* sebagai jembatan kompromi ideal.

---

## 3. Kunci Jawaban Lengkap & Pembahasan Mendalam Latihan HOTS

### Pembahasan Soal 8.1: Analisis Konvergensi Matematis Kondisi Batas Learning Rate
1. **Penurunan Relasi Rekursif Parameter $\theta^{(t)}$**:
   Fungsi biaya kuadratik:
   $$J(\theta) = \frac{1}{2} a \theta^2, \quad a > 0$$
   Turunan pertama terhadap $\theta$:
   $$\frac{dJ}{d\theta} = a \theta$$
   Aturan pembaruan *Gradient Descent*:
   $$\theta^{(t+1)} = \theta^{(t)} - \eta \frac{dJ}{d\theta}(\theta^{(t)}) = \theta^{(t)} - \eta a \theta^{(t)} = (1 - \eta a) \theta^{(t)}$$
   Dengan menerapkan relasi rekursif ini secara induktif dari $t=0$:
   $$\theta^{(t)} = (1 - \eta a)^t \theta^{(0)}$$
2. **Pembuktian Batas Konvergensi Teoretis**:
   Agar $\lim_{t \to \infty} \theta^{(t)} = 0$ untuk sembarang inisialisasi $\theta^{(0)} \neq 0$, faktor pengali dasar harus memenuhi kondisi kontraktif:
   $$|1 - \eta a| < 1 \iff -1 < 1 - \eta a < 1$$
   - Mengurangkan 1 dari seluruh pertidaksamaan:
     $$-2 < -\eta a < 0$$
   - Mengalikan dengan $-1$ (membalik tanda pertidaksamaan):
     $$0 < \eta a < 2$$
   - Karena $a > 0$, maka rentang nilai tingkat pembelajaran $\eta$ yang menjamin konvergensi stabil adalah:
     $$0 < \eta < \frac{2}{a} \quad \blacksquare$$
   **Perilaku Geometris jika $\eta > \frac{2}{a}$**:
   Faktor $|1 - \eta a| > 1$. Pada setiap langkah pembaruan, tanda nilai $\theta$ berganti-ganti (berosilasi) dengan magnitudo yang semakin membesar secara eksponensial. Secara geometris, langkah pembaruan melompati dasar parabolik dan mendarat pada lereng seberang pada ketinggian yang lebih curam, memicu divergensi numerik menuju $\pm \infty$.

### Pembahasan Soal 8.2: Diagnostik Kasus Komputasi Gradient Explosion
1. **Mekanisme Meledaknya Gradien Tanpa Normalisasi**:
   Residu kesalahan adalah $e_i = (\mathbf{x}_i^T \boldsymbol{\theta} - y_i)$. Vektor gradien untuk satu batch adalah:
   $$\nabla_{\boldsymbol{\theta}} J = \frac{2}{b} \sum_{i=1}^b e_i \mathbf{x}_i$$
   Jika fitur spektral memiliki magnitudo besar ($x_{ij} \sim 4095$), perkalian $\mathbf{x}_i^T \boldsymbol{\theta}$ dan $e_i \mathbf{x}_i$ akan menghasilkan gradien yang berskala jutaan ($\sim 10^7$). Dalam beberapa langkah perkalian $\boldsymbol{\theta}^{(t+1)} = \boldsymbol{\theta}^{(t)} - \eta \nabla J$, nilai bobot berlipat ganda secara eksponensial hingga melampaui batas maksimum representasi *floating point* IEEE 754 (sekitar $1.8 \times 10^{308}$ untuk *float64*), sehingga sistem komputasi mencatatnya sebagai `Inf` lalu menghasilkan operasi tak terdefinisi `NaN`.
2. **Rancangan Solusi Rekayasa Komprehensif Tiga Pilar**:
   - **Pilar 1 (Standarisasi Z-Score Masukan)**:
     $$x_{\text{norm}} = \frac{x - \mu}{\sigma}$$
     Menstandarisasi nilai masukan ke rentang rerata 0 dan variansi 1, sehingga lanskap fungsi biaya memiliki kurvatur simetris melingkar (*isotropic*) dengan nilai eigen kovariansi teratur.
   - **Pilar 2 (Gradient Clipping)**:
     Membatasi norma vektor gradien menggunakan pemotongan norma $\ell_2$:
     $$\mathbf{g} \leftarrow \mathbf{g} \cdot \frac{c}{\max(c, \|\mathbf{g}\|_2)}$$
     dengan ambang batas $c = 1.0$. Jika gradien melonjak tajam akibat sampel anomali, arah gradien tetap dipertahankan namun panjang vektornya dipaksa maksimum sebesar $c$.
   - **Pilar 3 (Optimizer Adaptif Adam)**:
     Mengganti SGD konvensional dengan Adam (*Adaptive Moment Estimation*) yang membagi pembaruan dengan akar rata-rata kuadrat gradien historis ($v_t$), secara otomatis meredam lonjakan gradien besar.

### Pembahasan Soal 8.3: Desain Eksperimental Optimizer Skenario Streaming IoT
1. **Kegagalan BGD dan Persamaan Normal pada Data Aliran (*Streaming*)**:
   - Persamaan normal OLS membutuhkan keberadaan seluruh matriks desain $\mathbf{X} \in \mathbb{R}^{n \times d}$ secara lengkap di dalam memori RAM. Pada aliran data sensor terus menerus ($n \to \infty$), matriks tersebut berukuran tak berhingga sehingga mustahil disimpan dan diinversi.
   - Batch Gradient Descent (BGD) menuntut komputasi rata-rata gradien atas seluruh $n$ sampel sebelum melakukan satu langkah pembaruan parameter. Menunggu seluruh aliran data tiba berarti pembaruan model tidak akan pernah terjadi (*infinite blocking*).
2. **Arsitektur Pembaruan Model Online Streaming Berbasis Adam**:
   - **Alur Kerja Pembaruan**: Setiap paket data mini-batch tiba dari sensor (misal $b = 32$ pembacaan), parameter model diperbarui secara langsung melalui satu langkah inferensi-koreksi (*streaming online update*) tanpa perlu menyimpan riwayat data lampau.
   - **Mekanisme Peluruhan Learning Rate (*Learning Rate Annealing*)**:
     Untuk menjamin algoritma tidak terus berosilasi seiring bertambahnya usia operasional model, diterapkan aturan peluruhan waktu terbalik (*inverse time decay*):
     $$\eta_t = \frac{\eta_0}{1 + \gamma \cdot t}$$
     atau peluruhan eksponensial $\eta_t = \eta_0 \cdot \gamma^{t / T}$, di mana $\eta_0 = 0.01$ adalah laju awal, $\gamma$ adalah faktor peredam, dan $t$ adalah indeks langkah waktu. Aturan ini memenuhi kondisi konvergensi Robbins-Monro:
     $$\sum_{t=1}^\infty \eta_t = \infty \quad \text{dan} \quad \sum_{t=1}^\infty \eta_t^2 < \infty$$
     yang secara teoritis menjamin konvergensi asimtotik stabil menuju parameter optimal global.

---

## 4. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Aspek Penilaian | Bobot | Sangat Memuaskan (85 - 100) | Memuaskan (70 - 84) | Cukup / Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penurunan Formula Gradien & Batas Konvergensi (C4)** | 25% | Menurunkan relasi rekursif parameter dengan tepat; membuktikan batas stabilitas $\eta < 2/a$ secara aljabar; menguraikan kondisi geometris divergensi. | Mampu menurunkan bentuk rekursif namun terdapat celah logika pada pembuktian batas pertidaksamaan. | Terjadi kekeliruan mendasar dalam kalkulus turunan fungsi kuadratik atau gagal memahami arti batas kestabilan. |
| **Implementasi Komputasi Algoritma Optimasi (C3/C4)** | 30% | Berhasil mengimplementasikan BGD, SGD, dan MBGD dari dasar dengan benar; mengelola pengacakan indeks per epoch; menghitung trajektori fungsi biaya. | Mengimplementasikan salah satu algoritma dengan hasil valid namun logika pengacakan batch masih kurang efisien. | Kode optimasi gagal konvergen atau menghasilkan eror eksekusi numerik (`NaN`/`Overflow`). |
| **Analisis Kurva Konvergensi & Hyperparameter (C4/C5)** | 25% | Menganalisis pengaruh $\eta$ secara komparatif; mengidentifikasi kurva stagnan vs divergen; menjelaskan hubungan standarisasi fitur dengan bentuk kontur. | Mampu membaca arah kurva loss namun penjelasan kaitan antara penskalaan data dan bentuk kontur elips kurang mendalam. | Tidak mampu menginterpretasikan grafik skala logaritma loss curve atau keliru menafsirkan tanda-tanda konvergensi. |
| **Perancangan Arsitektur Edge Streaming (C5)** | 20% | Merancang solusi *online update* untuk streaming IoT perkebunan secara komprehensif; menguraikan mekanisme peluruhan laju belajar Robbins-Monro. | Menjelaskan konsep pembaruan online dengan benar namun rancangan penyesuaian laju belajarnya kurang spesifik. | Mengusulkan metode batch yang tidak realistis untuk skenario data streaming kontinu tanpa akhir. |
