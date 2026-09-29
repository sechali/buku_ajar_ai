# Panduan Instruktur & Kunci Solusi: AI Modul 5.7 - Evaluasi Model dalam Machine Learning

**Program Studi Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian**  
**Fakultas Teknologi Pertanian, Institut Pertanian STIPER Yogyakarta**

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) Sesi 3 SKS (150 Menit)

| Alokasi Waktu | Aktivitas Pembelajaran | Metode & Media | Peran Instruktur | Target Capaian Mahasiswa |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20 Menit) | **Pendahuluan & Apersepsi Konseptual**: Membedah paradoks akurasi melalui tebakan naif pada penyakit tanaman berprevalensi rendah ($5\%$). | Diskusi interaktif, Studi kasus wabah *Ganoderma* kelapa sawit, Polling kelas. | Membimbing mahasiswa menyadari bahwa metrik akurasi tinggi dapat menutupi kegagalan fatal di lapangan. | Memahami keterbatasan metrik akurasi standar dan pentingnya analisis matriks konfusi. |
| **00:20 - 01:00** (40 Menit) | **Eksplorasi Teori & Perumusan Matematis**: Penurunan metrik regresi (MAE, RMSE, $R^2$, Adjusted $R^2$) dan klasifikasi (*Precision*, *Recall*, $F_\beta$-Score, ROC-AUC, PR-AUC). | Kuliah mimbar, Penurunan rumus matematis, Bedah diagram perbandingan ROC vs PR. | Menjelaskan secara analitis kapan menggunakan kurva ROC dan kapan kurva PR menjadi instrumen wajib. | Menguasai perumusan matematis seluruh metrik evaluasi dan trade-off ambang batas keputusan. |
| **01:00 - 02:00** (60 Menit) | **Praktikum Terbimbing di Laboratorium Komputer**: Eksekusi notebook komputasi, visualisasi matriks konfusi, kurva ROC-AUC, dan simulasi penentuan ambang batas optimal berbasis matriks biaya finansial. | Live coding terbimbing di JupyterLab, Eksperimen parameter *threshold*. | Mendampingi mahasiswa mengonstruksi matriks biaya riil perkebunan dan memverifikasi perhitungan metrik manual. | Menghasilkan kode Python evaluasi komprehensif dan membuktikan penghematan biaya puluhan juta rupiah. |
| **02:00 - 02:30** (30 Menit) | **Diskusi Analitis HOTS & Evaluasi OBE**: Analisis mendalam terhadap penurunan parameter $\beta$, kontaminasi aflatoksin kakao, dan validasi silang spasial blok kebun (Soal 8.1 - 8.3). | Diskusi panel mahasiswa, Pemaparan argumen solusi teknis, Umpan balik instruktur. | Menilai ketajaman analisis kritis mahasiswa dalam menjustifikasi pemilihan metrik berbasis dampak ekonomi nyata. | Mampu merancang kerangka evaluasi model AI yang robust, etis, dan selaras dengan risiko bisnis industri. |

---

## 2. Identifikasi Miskonsepsi Umum Mahasiswa & Strategi Intervensi

### Miskonsepsi 1: "Akurasi 95% selalu menandakan bahwa model klasifikasi sudah sangat hebat."
- **Kenyataan Ilmiah**: Pada dataset tidak seimbang (*imbalanced data*) dengan proporsi kelas positif hanya 5%, sebuah model naif yang selalu menebak "Negatif" (Sehat) akan secara otomatis mencetak akurasi 95%, padahal nilai Recall-nya adalah 0.0% (gagal mendeteksi satu pun tanaman yang sakit).
- **Intervensi Pedagogis**: Tampilkan perbandingan pada Cell #2 notebook: model naif mencetak akurasi 94.67% namun meloloskan seluruh 30 pohon sakit di data uji.

### Miskonsepsi 2: "Nilai Root Mean Squared Error (RMSE) selalu sama atau identik dengan Mean Absolute Error (MAE)."
- **Kenyataan Ilmiah**: RMSE selalu bernilai lebih besar atau sama dengan MAE ($\text{RMSE} \ge \text{MAE}$). Karena residu kesalahan dikuadratkan terlebih dahulu sebelum dirata-ratakan dan diakarkan, RMSE memberikan bobot penalti yang jauh lebih berat terhadap kesalahan-kesalahan besar (*outliers*). Selisih yang lebar antara RMSE dan MAE mengindikasikan adanya variansi kesalahan yang besar atau keberadaan pencilan ekstrem pada data.
- **Intervensi Pedagogis**: Perlihatkan tabel hasil praktikum Cell #1 di mana keberadaan 2 pencilan membuat nilai RMSE (2.23) melonjak signifikan di atas nilai MAE (1.52).

### Miskonsepsi 3: "Ambang batas klasifikasi probabilitas harus selalu dipatok pada angka 0.50."
- **Kenyataan Ilmiah**: Ambang batas $\tau = 0.50$ hanyalah konvensi simetris yang mengasumsikan biaya Galat Tipe I (FP) sama persis dengan biaya Galat Tipe II (FN). Dalam dunia agribisnis nyata, membiarkan pohon sakit lolos (FN) berbiaya 100 kali lebih mahal daripada alarm palsu (FP). Menurunkan ambang batas ke $\tau = 0.05$ secara drastis menekan kerugian finansial total.
- **Intervensi Pedagogis**: Mintalah mahasiswa mencermati Cell #5 di mana penggeseran ambang dari 0.50 ke 0.046 menghemat biaya kebun sebesar Rp 58.000.000,-.

### Miskonsepsi 4: "Kurva ROC-AUC adalah metrik evaluasi terbaik untuk semua jenis masalah klasifikasi biner."
- **Kenyataan Ilmiah**: Pada data dengan ketimpangan kelas yang sangat ekstrem (misal prevalensi 0.1%), kurva ROC dapat memberikan ilusi performa prima (AUC > 0.90) karena jumlah True Negative ($TN$) yang melimpah menjaga nilai False Positive Rate ($FPR$) tetap rendah. Pada kasus ini, kurva *Precision-Recall* (PR-AUC) adalah metrik wajib yang jauh lebih informatif karena tidak memuat suku $TN$.
- **Intervensi Pedagogis**: Analisis Soal HOTS 8.2 secara mendalam untuk memperlihatkan bagaimana dua model dengan ROC-AUC identik 0.94 memiliki PR-AUC yang jomplang (0.78 vs 0.29).

---

## 3. Kunci Jawaban Lengkap & Pembahasan Mendalam Latihan HOTS

### Pembahasan Soal 8.1: Analisis Kritis Paradoks Akurasi dan Formulasi Parameter $\beta$
1. **Bukti Matematis Paradoks Akurasi**:
   Diberikan populasi pohon sawit $N = 10.000$ dengan prevalensi ulat api $P(Y=1) = 0.02$ ($2\%$).
   Maka jumlah pohon terinfeksi $N_+ = 200$ pohon, dan pohon sehat $N_- = 9.800$ pohon.
   Sebuah model naif $\mathcal{M}_{\text{dummy}}$ yang memprediksi seluruh pohon sehat ($\hat{y}_i = 0, \forall i$) menghasilkan:
   - $\text{TP} = 0$, $\text{FP} = 0$, $\text{FN} = 200$, $\text{TN} = 9.800$.
   - $\text{Akurasi} = \frac{TP + TN}{N} = \frac{0 + 9800}{10000} = 98.0\%$.
   Secara matematis, akurasi $98\%$ adalah ilusi, karena fungsi kerugian operasional yang sebenarnya mengukur keberhasilan deteksi hama memiliki nilai nol mutlak:
   $$\text{Recall} = \frac{TP}{TP + FN} = \frac{0}{200} = 0.0\%$$
   Seluruh 200 populasi ulat api diabaikan, yang dalam hitungan hari akan merusak ribuan pelepah daun sawit lainnya.
2. **Formulasi Nilai Parameter $\beta$ pada $F_\beta$-Score**:
   Metrik $F_\beta$-Score didefinisikan sebagai:
   $$F_\beta = (1 + \beta^2) \frac{\text{Precision} \cdot \text{Recall}}{(\beta^2 \cdot \text{Precision}) + \text{Recall}}$$
   Parameter $\beta$ merepresentasikan seberapa kali lipat *Recall* dianggap lebih berharga (*weighted*) dibandingkan *Precision*.
   Karena manajemen menetapkan bahwa meloloskan ulat api (FN $\implies$ menurunkan Recall) bernilai $5 \times$ lebih merugikan secara finansial dibandingkan salah mengecek kanopi sehat (FP $\implies$ menurunkan Precision), maka:
   $$\beta = 5.0$$
   Dengan memilih $\beta = 5.0$, rumus menjadi:
   $$F_5 = (1 + 25) \frac{\text{Precision} \cdot \text{Recall}}{(25 \cdot \text{Precision}) + \text{Recall}} = 26 \frac{P \cdot R}{25 P + R}$$
   Model yang dipilih wajib memaksimumkan nilai $F_5$-Score, yang secara agresif memprioritaskan sensitivitas penangkapan ulat api.

### Pembahasan Soal 8.2: Evaluasi Komparatif Kurva ROC vs Kurva Precision-Recall
1. **Penyebab Kegagalan ROC-AUC Mendeteksi Perbedaan Kualitas**:
   Sumbu horizontal kurva ROC adalah False Positive Rate:
   $$\text{FPR} = \frac{\text{FP}}{\text{TN} + \text{FP}}$$
   Pada prevalensi kontaminasi sangat rendah ($0.2\%$, misal 100 biji kakao terkontaminasi dan 49.900 biji bersih dalam $50.000$ sampel uji), nilai $\text{TN} \approx 49.000$.
   Jika Model B menghasilkan $1.000$ alarm palsu ($\text{FP} = 1000$), nilai $\text{FPR}$ tetap sangat kecil:
   $$\text{FPR}_B = \frac{1000}{49000 + 1000} = 0.02 \quad (2\%)$$
   Karena FPR sangat kecil, kurva ROC Model B tetap menempel di dekat sumbu vertikal kiri, menghasilkan nilai AUC-ROC tinggi sebesar $0.94$.
   Sebaliknya, pada kurva Precision-Recall:
   $$\text{Precision}_B = \frac{\text{TP}}{\text{TP} + \text{FP}} = \frac{80}{80 + 1000} \approx 0.074 \quad (7.4\%)$$
   Presisi Model B ambruk menjadi hanya $7.4\%$. Kurva PR-AUC secara tegas memperlihatkan kelemahan ini dengan nilai PR-AUC yang terpuruk pada $0.29$.
2. **Keputusan Manajer Quality Assurance**:
   Manajer QA **wajib memilih Model A**.
   Meskipun kedua model memiliki AUC-ROC identik ($0.94$), Model A menghasilkan PR-AUC $0.78$ (jauh melampaui Model B sebesar $0.29$). Dalam konteks ekspor komoditas kakao, Model B akan menghasilkan ribuan alarm palsu yang memicu penolakan kontainer ekspor atau biaya pengujian laboratorium ulang yang sangat mahal. Model A memiliki kemurnian deteksi (*Precision*) yang jauh lebih tinggi pada tingkat penangkapan kontaminan yang setara.

### Pembahasan Soal 8.3: Desain Evaluasi Validasi Silang Multi-Metrik Regresi Sawit
1. **Protokol Validasi Silang Spasial (*Spatial Block Cross-Validation*)**:
   - Petak-petak kebun di dalam satu afdeling memiliki korelasi spasial tinggi (jenis tanah, curah hujan mikro, dan manajemen pemupukan yang seragam).
   - Jika diterapkan *K-Fold Cross-Validation* acak biasa, sampel dari petak yang bersebelahan akan terbagi ke dalam set latih dan set uji, menyebabkan kebocoran informasi geografis (*spatial data leakage*) dan nilai $R^2$ yang melambung semu.
   - **Solusi**: Gunakan `GroupKFold` dengan membagi data berdasarkan kesatuan geografis utuh (*Afdeling Block*). Pada setiap lipatan (*fold*), 1 atau 2 afdeling utuh diisolasi sepenuhnya sebagai data uji, sementara model dilatih pada afdeling yang berbeda. Hal ini memastikan model diuji pada lanskap kebun yang benar-benar baru.
2. **Alasan Wajib Melaporkan Kombinasi MAE, RMSE, dan $R^2_{\text{adj}}$**:
   - **MAE**: Menyediakan besaran kesalahan dalam satuan fisik riil yang intuitif bagi manajer perkebunan (misal: "rata-rata prediksi meleset $\pm 1.5$ ton TBS/ha"), berguna untuk estimasi kapasitas truk angkut.
   - **RMSE**: Mendeteksi apakah model menghasilkan kesalahan prediksi ekstrem di beberapa petak tertentu yang berisiko mengacaukan jadwal pengolahan pabrik kelapa sawit (*mill processing scheduling*).
   - **Adjusted $R^2$**: Menjamin bahwa akurasi penjelasan variansi model tidak dipalsukan oleh penambahan variabel prediktor yang tidak relevan secara agronomis.

---

## 4. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Aspek Penilaian | Bobot | Sangat Memuaskan (85 - 100) | Memuaskan (70 - 84) | Cukup / Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Metrik Regresi & Klasifikasi (C3/C4)** | 25% | Mampu menghitung seluruh metrik secara akurat; menjelaskan perbedaan filosofis MAE vs RMSE; menguraikan Adjusted $R^2$ dengan tepat. | Menghitung metrik dengan benar namun kurang mendalam dalam menjelaskan implikasi penalti kuadratik RMSE. | Terjadi kesalahan formula metrik dasar atau keliru menafsirkan koefisien determinasi $R^2$. |
| **Analisis Kritis Paradoks Akurasi (C4/C5)** | 25% | Membuktikan paradoks akurasi pada data imbalanced secara matematis; merumuskan nilai $\beta$ pada $F_\beta$ yang selaras dengan rasio biaya operasional. | Mengenali bahaya akurasi pada data tidak seimbang namun perumusan parameter $\beta$ masih kurang presisi. | Masih menganggap akurasi tinggi sebagai jaminan mutlak keberhasilan model tanpa memeriksa matriks konfusi. |
| **Evaluasi Kurva Diskriminasi ROC vs PR (C4)** | 25% | Menguraikan secara tajam mengapa ROC-AUC gagal pada prevalensi sangat rendah; membandingkan trade-off Precision vs Recall; menjelaskan indeks Youden $J$. | Memahami bentuk kurva ROC dan PR namun kurang mendalam dalam menganalisis pengaruh besaran True Negative ($TN$). | Tidak mampu membedakan sumbu pada kurva ROC dan kurva PR atau salah membaca nilai AUC. |
| **Optimasi Ambang Batas Berbasis Biaya (C5)** | 25% | Mengonstruksi matriks biaya finansial riil; mengidentifikasi ambang batas optimal yang meminimalkan kerugian ekonomi; menghitung penghematan biaya secara konkret. | Mampu menyetel ambang batas keputusan namun model biaya yang dibuat masih bersifat konseptual tanpa kuantifikasi moneter. | Mengabaikan konsep penyesuaian threshold dan hanya terpaku pada ambang batas bawaan 0.50. |
