"""
Script to standardize and align Module 8.6 to 8.11 diktat files with Part 7 conventions.
Converts each module into the exact 10-section structure:
1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)
2. Profil Fundamental ...: Fungsi, Manfaat, dan Keunggulan-Kelemahan
3. Landasan Teori Matematis & Statistik
4. Visualisasi Arsitektur & Pipeline Komputasi
5. Studi Kasus Komputasi & Implementasi PyTorch
6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)
7. Rangkuman Modul
8. Latihan Soal & Tugas Analitis HOTS
9. Jembatan Konsep (Bridging) ke AI Modul ...
10. Daftar Pustaka dan Referensi Akademik
"""

import os
import re

MODULE_CONFIGS = {
    "8.6": {
        "file": "docs/part-08/AI_Modul_8.6_Regularisasi_dan_Generalisasi_Deep_Learning.md",
        "title": "# AI Modul 8.6: Regularisasi & Generalisasi Deep Learning",
        "code": "AI-08-06",
        "course": "Kecerdasan Buatan dalam Agrokompleks (INSTIPER)",
        "prereq": "AI Modul 8.5 (Optimasi Gradient Descent Lanjut)",
        "mermaid": """flowchart LR
    A["OUTPUTS: Skrip NumPy & PyTorch Regularisasi (Weight Decay, Dropout, BatchNorm, Early Stopping)"] --> B["OUTCOMES: Mitigasi Overfitting & Stabilisasi Generalisasi Model"]
    B --> C["IMPACTS: Model Deep Learning Tangguh untuk Variasi Lapangan Agrokompleks"]""",
        "sec2_title": "## 2. Profil Fundamental Regularisasi dan Generalisasi: Fungsi, Manfaat, dan Keunggulan-Kelemahan",
        "sec4_title": "## 4. Visualisasi Arsitektur & Prosedur Komputasi Numerik",
        "sec5_title": "## 5. Studi Kasus Komputasi & Dataset Agrokompleks",
        "sec6_title": "## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)",
        "summary": [
            "**Dilema Generalisasi vs Hafalan**: Model deep learning berkapasitas tinggi rentan mengalami *overfitting* pada variasi musiman data agrokompleks, menuntut regulasi kapasitas efektif jaringan.",
            "**Penalti Bobot $L_2$ dan $L_1$**: *Weight Decay* ($L_2$) meredam magnitudo bobot secara proporsional menuju nol melalui peluruhan eksponensial, sedangkan Lasso ($L_1$) mendorong bobot bernilai nol eksak sehingga menciptakan seleksi fitur (*sparsity*).",
            "**Inverted Dropout**: Teknik regularisasi stokastik yang menonaktifkan neuron secara acak dengan probabilitas $p$ saat pelatihan, diskalakan dengan faktor $1/(1-p)$ sehingga fase evaluasi (`model.eval()`) berjalan deterministik tanpa komputasi tambahan.",
            "**Batch Normalization**: Menstabilkan distribusi aktivasi internal per mini-batch menggunakan rata-rata dan varians sampel, mereduksi sensitivitas inisialisasi bobot, serta berfungsi sebagai regularizer implisit yang mempercepat konvergensi.",
            "**Early Stopping & Checkpointing**: Mekanisme pemantauan galat validasi dengan batas kesabaran (*patience*) yang secara otomatis memulihkan bobot terbaik (*best checkpoint restore*), mencegah pemborosan komputasi saat model mulai menghafal derau."
        ],
        "bridging_title": "## 9. Jembatan Konsep (Bridging) ke AI Modul 8.7: Preprocessing Dataset",
        "bridging_text": """Dengan dituntaskannya Modul 8.6 ini, seluruh fondasi arsitektur Jaringan Saraf Tiruan (*Deep Neural Networks* / MLP), kalkulus propagasi maju dan mundur (*Backpropagation*), algoritma optimasi penurunan gradien adaptif (SGD, Momentum, RMSprop, Adam), serta teknik-teknik pengendalian generalisasi (*Weight Decay, Inverted Dropout, Batch Normalization, Early Stopping*) telah dikuasai secara mendalam.

Meskipun demikian, sebuah model dengan regularisasi paling canggih sekalipun akan gagal total jika kualitas representasi data masukan tidak dikelola dengan benar (*Garbage In, Garbage Out*). Dalam domain agrokompleks nyata—yang melibatkan ratusan pita reflektansi spektral Vis-NIR, sensor IoT kelembaban tanah, dan perbedaan afdeling perkebunan—terdapat bahaya laten yang sangat merusak: **autokorelasi spasial** dan **kebocoran data (*data leakage*)**. Membagi data secara acak tanpa memperhatikan batas geografis blok kebun akan memicu optimisme performa semu yang runtuh seketika saat diuji di afdeling baru.

Oleh karena itu, pada **AI Modul 8.7: Preprocessing Dataset**, kita akan beralih dari teori arsitektur murni menuju rekayasa alur kerja data (*data workflow engineering*) khusus deep learning:
* **Partisi Spasial Blok Kebun (*Spatial Block Partitioning*)**: Membagi data latih, validasi, dan uji berbasis blok geografis nyata guna menjamin validitas evaluasi generalisasi.
* **Isolasi Parameter Skala (*Strict Zero-Leakage Rule*)**: Memastikan seluruh transformasi skala ($Z$-score, Robust Scaler) dihitung (*fit*) murni dari data latih.
* **Konstruksi PyTorch Dataset & DataLoader Kustom**: Membangun generator mini-batch berkinerja tinggi lengkap dengan mekanisme *shuffling*, penanganan ketidakseimbangan kelas (*Weighted Random Sampling*), dan alokasi memori GPU (`pin_memory`)."""
    },

    "8.7": {
        "file": "docs/part-08/AI_Modul_8.7_Preprocessing_Dataset.md",
        "title": "# AI Modul 8.7: Preprocessing Dataset",
        "code": "AI-08-07",
        "course": "Kecerdasan Buatan dalam Agrokompleks (INSTIPER)",
        "prereq": "AI Modul 8.6 (Regularisasi & Generalisasi Deep Learning)",
        "mermaid": """flowchart LR
    A["OUTPUTS: Modul Preprocessing, Skrip PyTorch Dataset/DataLoader, Partisi Spasial"] --> B["OUTCOMES: Standardisasi Multivariat & Pencegahan Kebocoran Data Lapangan"]
    B --> C["IMPACTS: Keandalan Model Deep Learning pada Variasi Afdeling Kebun Baru"]""",
        "sec2_title": "## 2. Profil Fundamental Preprocessing Dataset: Fungsi, Manfaat, dan Keunggulan-Kelemahan",
        "sec4_title": "## 4. Visualisasi Pipeline Data dan Partisi Spasial",
        "sec5_title": "## 5. Studi Kasus Komputasi & Implementasi PyTorch Dataset/DataLoader",
        "sec6_title": "## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)",
        "summary": [
            "**Standarisasi Fitur & Rasio Kondisi Hessian**: Penskalaan fitur masukan ($Z$-score atau Robust Scaling) merotasi elips kontur fungsi rugi menjadi sirkular ($\\kappa(\\mathbf{H}) \\approx 1$), melipatgandakan kecepatan konvergensi gradien.",
            "**Mitigasi Kebocoran Data Spasial**: Pohon-pohon dalam satu afdeling memiliki autokorelasi spasial tinggi. Pembagian data wajib menggunakan partisi blok geografis (*Spatial Block Partitioning*), bukan pengacakan murni (*random split*).",
            "**Aturan Mutlak Tanpa Kebocoran (*Zero-Leakage Rule*)**: Parameter transformasi ($\mu, \\sigma, x_{\min}, x_{\max}$) wajib diestimasi murni dari data latih, lalu diaplikasikan secara pasif ke data validasi dan uji.",
            "**Enkapsulasi PyTorch Dataset**: Kelas turunan `torch.utils.data.Dataset` mengintegrasikan pemanggilan indeks `__getitem__` dan ukuran `__len__`, menjamin konversi data tabular ke tensor `torch.float32` secara konsisten.",
            "**Orkestrasi DataLoader Modern**: Mengelola pembentukan mini-batch, pengacakan per epoch (`shuffle=True`), penyeimbangan kelas via `WeightedRandomSampler`, dan akselerasi transfer memori GPU (`pin_memory=True`)."
        ],
        "bridging_title": "## 9. Jembatan Konsep (Bridging) ke AI Modul 8.8: Training Model",
        "bridging_text": """Melalui penuntasan Modul 8.7 ini, fondasi hulu rekayasa data *deep learning* telah kokoh: data mentah spektral dan sensor tanah telah dibersihkan dari pencilan, dipartisi berdasarkan batas blok geografis kebun untuk mencegah kebocoran spasial, distandarisasi secara matematis untuk menjamin kelengkungan fungsi rugi yang simetris, serta dienkapsulasi ke dalam generator batch `torch.utils.data.DataLoader` yang efisien secara memori.

Namun, tensor mini-batch yang mengalir dari `DataLoader` belum memiliki arah tujuan komputasi jika belum ada sistem penggerak terorkestrasi. Menyuapkan tensor ke model jaringan secara manual menggunakan loop sederhana rentan memicu ledakan gradien, pembaruan parameter yang tidak terkontrol, serta ketidakmampuan melacak kemajuan belajar model.

Pada **AI Modul 8.8: Training Model**, kita akan melangkah memasuki jantung komputasi pelatihan model. Kita akan merancang dan mengimplementasikan siklus pelatihan (*training loop*) kelas industri lengkap dengan teknik pemotongan gradien (*gradient clipping*), penjadwal laju pembelajaran dinamis (*learning rate scheduler*), serta sistem pemantauan dan pencadangan otomatis bobot model terbaik (*model checkpointing*)."""
    },

    "8.8": {
        "file": "docs/part-08/AI_Modul_8.8_Training_Model.md",
        "title": "# AI Modul 8.8: Training Model",
        "code": "AI-08-08",
        "course": "Kecerdasan Buatan dalam Agrokompleks (INSTIPER)",
        "prereq": "AI Modul 8.7 (Preprocessing Dataset)",
        "mermaid": """flowchart LR
    A["OUTPUTS: Pipeline Mesin Pelatihan Terpadu PyTorch (Clip, Scheduler, Checkpointing)"] --> B["OUTCOMES: Konvergensi Latih Cepat & Pencegahan Ledakan Gradien Numerik"]
    B --> C["IMPACTS: Model Terlatih Optimum & Siap Audit Evaluasi Produksi PKS"]""",
        "sec2_title": "## 2. Profil Fundamental Training Model: Fungsi, Manfaat, dan Keunggulan-Kelemahan",
        "sec4_title": "## 4. Visualisasi Alur Pelatihan dan Dinamika Gradien",
        "sec5_title": "## 5. Studi Kasus Komputasi Terpadu: Pelatihan Model Rendemen CPO",
        "sec6_title": "## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)",
        "summary": [
            "**Arsitektur Mesin Pelatihan Terstruktur**: Siklus pelatihan (*training loop*) profesional mengorganisasikan alur kerja menjadi fase pelatihan terawasi (`train`) dan fase validasi nir-gradien (`torch.no_grad()`).",
            "**Gradient Clipping**: Mencegah instabilitas numerik dan fenomena *exploding gradients* dengan membatasi norma vektor gradien $\|\\mathbf{g}\|_2 \le \theta$ sebelum eksekusi langkah optimizer.",
            "**Penjadwalan Laju Pembelajaran Dinamis**: Penggunaan teknik seperti *Cosine Annealing* atau *ReduceLROnPlateau* memfasilitasi konvergensi presisi tinggi di dasar lembah loss fungsi rugi.",
            "**Model Checkpointing**: Mekanisme penyimpanan kamus keadaan (*state dictionary*) bobot jaringan secara otomatis setiap kali metrik validasi mencatat rekor terbaik baru.",
            "**Reproduktifitas Eksperimen Saintifik**: Pengendalian benih acak (`torch.manual_seed`) dan determinisme algoritma CUDA menjamin setiap siklus pelatihan menghasilkan temuan yang dapat diulang."
        ],
        "bridging_title": "## 9. Jembatan Konsep (Bridging) ke AI Modul 8.9: Evaluasi Model",
        "bridging_text": """Setelah menyelesaikan Modul 8.8, model *deep learning* telah berhasil dilatih melalui siklus pelatihan yang terorkestrasi secara profesional. Parameter bobot optimum telah tersimpan dalam berkas *checkpoint*, laju pembelajaran telah diturunkan secara mulus melalui scheduler, dan gradien telah terlindungi dari ledakan komputasi.

Namun, apakah nilai fungsi rugi validasi yang rendah cukup untuk membuktikan bahwa model siap dioperasikan di industri perkebunan? Jawabannya adalah **tidak**. Sebuah model yang memiliki rata-rata eror kecil masih mungkin mengalami heteroskedastisitas (eror membesar pada buah bernilai ekonomi tinggi), bias pada afdeling tertentu, atau kegagalan fatal saat menghadapi pergeseran distribusi musiman (*seasonal distribution shift*).

Pada **AI Modul 8.9: Evaluasi Model**, kita akan melakukan audit diagnostik menyeluruh terhadap kinerja model:
* **Dekomposisi Bias-Varians**: Menguraikan galat model menjadi bias inheren vs sensitivitas varians.
* **Diagnostik Residual Komprehensif**: Menguji normalitas galat, ketiadaan autokorelasi, dan uji homoskedastisitas Breusch-Pagan.
* **Metrik Evaluasi Multi-Dimensi**: Menghitung MAE, RMSE, MAPE, $R^2$, serta kurva ROC-AUC dan PR-AUC untuk klasifikasi ambang mutu.
* **Uji Ketahanan Lapangan (*Robustness Stress Testing*)**: Menguji ketahanan prediksi model terhadap derau sensorik dan anomali data lapangan."""
    },

    "8.9": {
        "file": "docs/part-08/AI_Modul_8.9_Evaluasi_Model.md",
        "title": "# AI Modul 8.9: Evaluasi Model",
        "code": "AI-08-09",
        "course": "Kecerdasan Buatan dalam Agrokompleks (INSTIPER)",
        "prereq": "AI Modul 8.8 (Training Model)",
        "mermaid": """flowchart LR
    A["OUTPUTS: Suite Diagnostik Evaluasi (Residual, ROC-AUC, Breusch-Pagan, Stress Test)"] --> B["OUTCOMES: Deteksi Bias Tersembunyi & Validasi Keandalan Lintas-Blok Kebun"]
    B --> C["IMPACTS: Transparansi Risiko Prediktif Sebelum Deployment Pabrik Kelapa Sawit"]""",
        "sec2_title": "## 2. Profil Fundamental Evaluasi Model: Fungsi, Manfaat, dan Keunggulan-Kelemahan",
        "sec4_title": "## 4. Visualisasi Panel Diagnostik dan Evaluasi Kinerja",
        "sec5_title": "## 5. Studi Kasus Komputasi Terpadu: Audit Model Rendemen Sawit",
        "sec6_title": "## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)",
        "summary": [
            "**Dekomposisi Bias-Varians**: Galat generalisasi model tersusun atas kuadrat bias, varians model, dan varians derau acak tak tereduksi ($\\sigma_\\epsilon^2$).",
            "**Metrik Evaluasi Komplementer**: MAE memberikan estimasi selisih riil satuan fisik, RMSE memberi penalti kuadratik atas eror fatal, sedangkan $R^2$ mengukur proporsi varians target yang diterangkan.",
            "**Evaluasi Klasifikasi Terkalibrasi**: Pada kasus deteksi penyakit tanaman, kurva ROC-AUC dan PR-AUC memberikan evaluasi daya pemisah kelas yang kebal terhadap ketidakseimbangan sampel.",
            "**Pemeriksaan Diagnostik Residual**: Residual yang ideal wajib menyerupai distribusi normal derau putih ($\\epsilon \sim \\mathcal{N}(0, \\sigma^2)$) tanpa pola corong heteroskedastisitas.",
            "**Uji Stres Ketahanan Model**: Pengujian model terhadap penambahan derau Gaussian dan pergeseran distribusi membuktikan batas toleransi operasional di lapangan perkebunan."
        ],
        "bridging_title": "## 9. Jembatan Konsep (Bridging) ke AI Modul 8.10: Interpretasi Hasil Model",
        "bridging_text": """Melalui Modul 8.9, kita telah melaksanakan audit komprehensif terhadap performa kuantitatif model. Kita mengetahui secara presisi nilai RMSE, rentang toleransi residu, serta keandalan model saat menghadapi derau sensorik.

Kendati demikian, dalam ranah pengambilan keputusan industri perkebunan, metrik angka tinggi seperti $R^2 = 0.94$ sering kali belum cukup untuk meyakinkan manajer kebun dan auditor agronomi. Muncul pertanyaan fundamental: *"Mengapa jaringan saraf tiruan memberikan prediksi rendemen rendah pada blok tertentu? Apakah model benar-benar memahami respon fisiologis tanaman, atau sekadar menghafal artefak data kebetulan?"*

Pada **AI Modul 8.10: Interpretasi Hasil Model**, kita akan membongkar sifat kotak hitam (*black box*) deep learning menggunakan paradigma *Explainable AI* (XAI):
* **Permutation Feature Importance (PFI)**: Mengukur kontribusi global setiap fitur terhadap kualitas prediksi secara model-agnostik.
* **Vanilla Saliency Maps & Integrated Gradients**: Menghitung atribusi gradien lokal untuk melihat fitur spektral mana yang menjadi pemicu keputusan model per sampel.
* **Visualisasi Ruang Representasi Laten (t-SNE)**: Memproyeksikan vektor embedding lapisan tersembunyi untuk memeriksa keterpisahan kluster mutu kelapa sawit secara biologis."""
    },

    "8.10": {
        "file": "docs/part-08/AI_Modul_8.10_Interpretasi_Hasil_Model.md",
        "title": "# AI Modul 8.10: Interpretasi Hasil Model",
        "code": "AI-08-10",
        "course": "Kecerdasan Buatan dalam Agrokompleks (INSTIPER)",
        "prereq": "AI Modul 8.9 (Evaluasi Model)",
        "mermaid": """flowchart LR
    A["OUTPUTS: Skrip XAI Terintegrasi (PFI, Saliency Maps, Integrated Gradients, t-SNE)"] --> B["OUTCOMES: Transparansi Alasan Prediksi & Validasi Keselarasan Fisiologi Tanaman"]
    B --> C["IMPACTS: Kepercayaan Penuh Agronom & Keputusan Panen Sawit yang Akuntabel"]""",
        "sec2_title": "## 2. Profil Fundamental Interpretasi Hasil Model: Fungsi, Manfaat, dan Keunggulan-Kelemahan",
        "sec4_title": "## 4. Visualisasi Profil Keterjelasan dan Ruang Laten",
        "sec5_title": "## 5. Studi Kasus Komputasi Terpadu: Membongkar Model Rendemen CPO",
        "sec6_title": "## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)",
        "summary": [
            "**Urgensi Akuntabilitas XAI**: Membuka kotak hitam (*black box*) jaringan saraf tiruan merupakan syarat mutlak agar rekomendasi AI dapat diadopsi secara etis dan ilmiah oleh agronom.",
            "**Permutation Feature Importance**: Teknik evaluasi global yang mengukur kenaikan fungsi rugi ketika nilai fitur diacak secara independen, memetakan pengaruh makro setiap variabel agronomi.",
            "**Vanilla Saliency & Saturasi Gradien**: Peta saliensi menghitung gradien luaran terhadap masukan ($\\partial \\hat{y} / \\partial x_i$), namun rentan mengalami saturasi pada aktivasi tak-linier ekstrem.",
            "**Aksioma Integrated Gradients**: Mengakumulasikan gradien di sepanjang lintasan garis lurus dari data dasar (*baseline*) menuju sampel riil, menjamin pemenuhan aksioma kelengkapan (*completeness*).",
            "**Inspeksi Geometri Ruang Laten**: Reduksi dimensi non-linier t-SNE memverifikasi bahwa representasi internal model berhasil mengelompokkan sampel berdasarkan karakteristik fenotipik tanaman yang koheren."
        ],
        "bridging_title": "## 9. Jembatan Konsep (Bridging) ke AI Modul 8.11: Pembuatan Sistem Prediksi Sederhana",
        "bridging_text": """Setelah menyelesaikan Modul 8.10, arsitektur model deep learning kita tidak lagi menjadi entitas kotak hitam yang misterius. Kita telah membuktikan secara empiris bahwa keputusan model selaras dengan hukum fisiologi tanaman dan serapan spektrometri NIR.

Namun, model yang akurat dan transparan tidak akan membawa dampak bisnis nyata jika hanya tersimpan di dalam notebook Jupyter laboratorium komputasi. Operator sortasi di loading ramp pabrik kelapa sawit atau asisten kebun di lapangan membutuhkan antarmuka yang cepat, mudah digunakan, dan dapat dioperasikan secara mandiri tanpa memerlukan instalasi pustaka komputasi yang rumit.

Pada **AI Modul 8.11: Pembuatan Sistem Prediksi Sederhana**, kita akan merampungkan seluruh siklus rekayasa AI:
* **Serialisasi Model Portabel**: Mengekspor model PyTorch ke format kompilasi cepat *TorchScript* dan *ONNX Runtime*.
* **Enkapsulasi Mesin Inferensi (*Inference Engine*)**: Membangun kelas Python modular yang mengotomatisasi validasi input, standarisasi tanpa kebocoran data, eksekusi model, dan pemetaan kategori keputusan mutu.
* **Perancangan Antarmuka Interaktif**: Membangun aplikasi antarmuka grafis (Web GUI dan CLI) berbasis Gradio/Streamlit untuk sortasi mutu TBS sawit secara real-time."""
    },

    "8.11": {
        "file": "docs/part-08/AI_Modul_8.11_Pembuatan_Sistem_Prediksi_Sederhana.md",
        "title": "# AI Modul 8.11: Pembuatan Sistem Prediksi Sederhana",
        "code": "AI-08-11",
        "course": "Kecerdasan Buatan dalam Agrokompleks (INSTIPER)",
        "prereq": "AI Modul 8.10 (Interpretasi Hasil Model)",
        "mermaid": """flowchart LR
    A["OUTPUTS: Mesin Inferensi Portabel TorchScript/ONNX & Prototipe Web GUI Interaktif"] --> B["OUTCOMES: Eksekusi Prediksi Sub-Milidetik & Pengoperasian Mudah bagi Operator Pabrik"]
    B --> C["IMPACTS: Transformasi Sortasi Manual Menuju Presisi Otomasi Pabrik Kelapa Sawit"]""",
        "sec2_title": "## 2. Profil Fundamental Pembuatan Sistem Prediksi Sederhana: Fungsi, Manfaat, dan Keunggulan-Kelemahan",
        "sec4_title": "## 4. Visualisasi Pipeline Inferensi dan Antarmuka Pengguna",
        "sec5_title": "## 5. Studi Kasus Komputasi Terpadu: Perakitan Sistem Prediksi Sortasi Sawit",
        "sec6_title": "## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)",
        "summary": [
            "**Serialisasi Model Produksi**: Format portabel seperti TorchScript JIT (`torch.jit.trace`) dan ONNX Runtime melepaskan ketergantungan model dari runtime interpreter Python, memangkas latensi komputasi.",
            "**Enkapsulasi Mesin Inferensi Modular**: Kelas `InferenceEngine` membungkus seluruh siklus operasional: validasi rentang fisik fitur, standarisasi menggunakan parameter latih terbekukan, eksekusi inferensi, dan klasifikasi mutu.",
            "**Optimasi Latensi Eksekusi**: Pemanfaatan mode evaluasi (`model.eval()`), penghentian pelacakan gradien (`torch.no_grad()`), dan kompilasi grafik grafis memungkinkan inferensi tingkat sub-milidetik pada perangkat edge.",
            "**Antarmuka Pengguna Berorientasi Operator**: Perancangan antarmuka visual interaktif berbasis Web GUI (Streamlit / Gradio) memudahkan operator stasiun sortasi pabrik tanpa memerlukan keahlian pemrograman.",
            "**Protokol Penanganan Kegagalan Anggun (*Graceful Error Handling*)**: Sistem inferensi tangguh wajib mendeteksi masukan anomali atau data kosong dan memberikan pesan peringatan operasional alih-alih mengalami kerusakan sistem (*crash*)."
        ],
        "bridging_title": "## 9. Jembatan Konsep (Bridging) Puncak Menuju Bagian 9: Visi Komputer & Convolutional Neural Networks (CNN)",
        "bridging_text": """Dengan tuntasnya Modul 8.11 ini, kita telah menyelesaikan secara paripurna seluruh siklus rekayasa *Deep Learning* berbasis data tabular, deret waktu, dan spektral—mulai dari fondasi matematis Perceptron, arsitektur Multi-Layer Perceptron (MLP), forward-backward propagation, optimasi gradien lanjut, teknik regularisasi komposit, pembersihan data terpadu, orkestrasi pelatihan, audit diagnostik evaluasi, transparansi interpretasi XAI, hingga pembuatan sistem prediksi operasional siap pakai.

Namun, seluruh arsitektur jaringan saraf tiruan lapis penuh (*Fully-Connected Neural Networks*) yang telah kita pelajari memiliki satu kelemahan arsitektural fundamental: **ketidakmampuan menangkap struktur topologi spasial 2 dimensi**. Jika kita memaksakan data citra visual resolusi tinggi (misalnya citra kanopi kelapa sawit dari kamera drone atau foto daun terserang bercak penyakit) menjadi satu vektor baris panjang (*flattening*), dua malapetaka komputasi akan terjadi:
1. **Kehancuran Korelasi Spasial**: Hubungan ketetanggaan piksel yang membentuk pola tepi (*edges*), tekstur, dan bentuk visual daun akan hilang seketika.
2. **Ledakan Parameter Komputasi**: Citra beresolusi sedang $512 \times 512 \times 3$ menghasilkan 786.432 fitur masukan. Menghubungkannya ke lapisan tersembunyi dengan 512 neuron akan menciptakan lebih dari 400 juta parameter bobot yang memicu *overfitting* parah dan kehabisan memori VRAM.

Untuk menjawab tantangan spasial visual tersebut, kita melangkah menuju **Bagian 9: Visi Komputer & Jaringan Saraf Konvolusional (*Computer Vision & CNN*)**. Pada bagian berikutnya, kita akan membedah prinsip pemakaian bobot bersama (*weight sharing*), operasi konvolusi spasial 2D (*spatial convolution*), dan pereduksian dimensi *pooling* yang merevolusi cara komputer mengenali objek di dunia nyata—membuka era otomasi deteksi pohon sawit, sortasi kematangan tandan buah secara visual, dan pemetaan defisiensi hara skala perkebunan berbasis citra udara satelit dan drone."""
    }
}


def process_module(mod_num, cfg):
    fpath = cfg["file"]
    print(f"\nProcessing Module {mod_num}: {fpath}...")
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into sections by ## \d+\.
    sections = re.split(r'\n(?=## \d+\. )', text)
    if len(sections) != 12:
        print(f"Error: expected 12 sections, found {len(sections)} in {fpath}")
        return

    # Extract sub-components
    # sections[0]: top title header
    # sections[1]: Section 1: Identitas
    # sections[2]: Section 2: Profil Fundamental
    # sections[3]: Section 3: Landasan Teori
    # sections[4]: Section 4: Visualisasi
    # sections[5]: Section 5: Algoritma
    # sections[6]: Section 6: Studi Kasus
    # sections[7]: Section 7: Kekeliruan Metodologis
    # sections[8]: Section 8: Studi Kasus Terapan / Proyek Mandiri
    # sections[9]: Section 9: Panduan Asesmen / Rubrik
    # sections[10]: Section 10: Jembatan Konsep
    # sections[11]: Section 11: Daftar Pustaka

    # 1. Standardize Header 1 & Section 1
    # Extract Sub-CPMK, Indikator, Luaran from sections[1]
    sec1_text = sections[1]
    subcpmk_match = re.search(r'(### Capaian Pembelajaran Modul \(Sub-CPMK\).*?)(?=\n### Indikator|\n### Luaran|\n```mermaid|$)', sec1_text, re.DOTALL)
    subcpmk_body = subcpmk_match.group(1).strip() if subcpmk_match else ""
    # Rename header in subcpmk
    subcpmk_body = re.sub(r'### Capaian Pembelajaran Modul \(Sub-CPMK\)', '### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)', subcpmk_body)

    outputs_match = re.search(r'(### Luaran Pembelajaran \(Outputs, Outcomes, Impacts\).*?)(?=\n```mermaid|$)', sec1_text, re.DOTALL)
    outputs_body = outputs_match.group(1).strip() if outputs_match else ""
    outputs_body = re.sub(r'### Luaran Pembelajaran \(Outputs, Outcomes, Impacts\)', '### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)', outputs_body)

    new_sec1 = f"""## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: {cfg['code']}
* **Mata Kuliah**: {cfg['course']}
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Ganjil)
* **Prasyarat**: {cfg['prereq']}
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```{cfg['mermaid']}
```

{subcpmk_body}

{outputs_body}"""

    # 2. Section 2: Profil Fundamental
    sec2_body = re.sub(r'^## 2\. [^\n]+', cfg['sec2_title'], sections[2].strip())
    # Standardize 2.1 to 2.6 subheaders if needed
    sec2_body = re.sub(r'### 2\.1 [^\n]+', '### 2.1 Fungsi Komputasi & Pemodelan Matematis', sec2_body)
    sec2_body = re.sub(r'### 2\.2 [^\n]+', '### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis', sec2_body)
    sec2_body = re.sub(r'### 2\.3 [^\n]+', '### 2.3 Rationale: Alasan Mengapa Metode Ini Digunakan', sec2_body)
    sec2_body = re.sub(r'### 2\.4 [^\n]+', '### 2.4 Analisis Kelebihan dan Kekurangan', sec2_body)
    sec2_body = re.sub(r'### 2\.5 [^\n]+', '### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri', sec2_body)
    sec2_body = re.sub(r'### 2\.6 [^\n]+', '### 2.6 Aspek Kritis & Catatan Penting Metode (*Key Critical Insights*)', sec2_body)

    # 3. Section 3: Landasan Teori
    sec3_body = sections[3].strip()

    # 4. Section 4: Visualisasi & Prosedur Komputasi
    # Merge sections[4] and sections[5]
    sec4_content = re.sub(r'^## 4\. [^\n]+', cfg['sec4_title'], sections[4].strip())
    sec5_content = re.sub(r'^## 5\. [^\n]+', '### Prosedur Komputasi & Alur Algoritma Numerik', sections[5].strip())
    merged_sec4 = f"{sec4_content}\n\n{sec5_content}"

    # 5. Section 5: Studi Kasus Komputasi & Implementasi PyTorch
    sec5_body = re.sub(r'^## 6\. [^\n]+', cfg['sec5_title'], sections[6].strip())
    # Clean up any stray single-hash headers inside python code or text
    sec5_body = re.sub(r'\n# (\d+\. [^\n]+)', r'\n#### \1', sec5_body)
    sec5_body = re.sub(r'\n# (Eksekusi Pipeline[^\n]*)', r'\n#### \1', sec5_body)
    sec5_body = re.sub(r'\n# (Fitting Scaler[^\n]*)', r'\n#### \1', sec5_body)
    sec5_body = re.sub(r'\n# (Pembuatan DataLoaders[^\n]*)', r'\n#### \1', sec5_body)

    # 6. Section 6: Kekeliruan Metodologis
    sec6_body = re.sub(r'^## 7\. [^\n]+', cfg['sec6_title'], sections[7].strip())
    sec6_body = re.sub(r'### 7\.1 ', '### 6.1 ', sec6_body)
    sec6_body = re.sub(r'### 7\.2 ', '### 6.2 ', sec6_body)
    sec6_body = re.sub(r'### 7\.3 ', '### 6.3 ', sec6_body)

    # 7. Section 7: Rangkuman Modul (NEW standard)
    summary_items = "\n".join([f"{i+1}. {item}" for i, item in enumerate(cfg['summary'])])
    new_sec7 = f"""## 7. Rangkuman Modul

{summary_items}"""

    # 8. Section 8: Latihan Soal & Tugas Analitis HOTS (Merge sections[8] and sections[9])
    sec8_part = re.sub(r'^## 8\. [^\n]+', '', sections[8].strip()).strip()
    sec9_part = re.sub(r'^## 9\. [^\n]+', '', sections[9].strip()).strip()
    new_sec8 = f"""## 8. Latihan Soal & Tugas Analitis HOTS

{sec8_part}

{sec9_part}"""

    # 9. Section 9: Jembatan Konsep (Bridging)
    new_sec9 = f"""{cfg['bridging_title']}

{cfg['bridging_text']}"""

    # 10. Section 10: Daftar Pustaka dan Referensi Akademik
    sec10_body = re.sub(r'^## 11\. [^\n]+', '## 10. Daftar Pustaka dan Referensi Akademik', sections[11].strip())

    # Assemble final document
    final_doc = f"""{cfg['title']}

---

{new_sec1}

---

{sec2_body}

---

{sec3_body}

---

{merged_sec4}

---

{sec5_body}

---

{sec6_body}

---

{new_sec7}

---

{new_sec8}

---

{new_sec9}

---

{sec10_body}
"""

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(final_doc)
    print(f"Successfully aligned: {fpath}")


if __name__ == "__main__":
    for mod_num, cfg in MODULE_CONFIGS.items():
        process_module(mod_num, cfg)
    print("\nAll 6 modules (8.6 to 8.11) successfully aligned with Part 7 conventions!")
