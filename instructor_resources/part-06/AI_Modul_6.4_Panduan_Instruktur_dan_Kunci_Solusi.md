# AI Modul 6.4: Panduan Instruktur dan Kunci Solusi Perbandingan Performa Model

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) dan Panduan Pedagogis

### 1.1 Informasi Umum Modul
- **Mata Kuliah:** Kecerdasan Buatan dan Sains Data Pertanian Presisi
- **Modul:** 6.4 (Perbandingan Performa Model: Uji Signifikansi Statistik dan Evaluasi Multi-Kriteria)
- **Sasaran Peserta:** Mahasiswa Program Studi Agroteknologi, Agribisnis, dan Teknik Pertanian INSTIPER Yogyakarta
- **Alokasi Waktu:** 150 Menit (1 Sesi Tatap Muka / Praktikum Komputasi)

### 1.2 Tujuan Instruksional Khusus (TIK)
Pada akhir sesi pembelajaran ini, mahasiswa diharapkan mampu:
1. Membedah kurva ROC (*Receiver Operating Characteristic*) dan menghitung indeks Youden ($J$) guna menetapkan ambang batas keputusan operasional di kebun.
2. Mengidentifikasi kelemahan mendasar uji *paired t-test* standar pada validasi silang akibat pelanggaran asumsi independensi.
3. Menghitung statistik $t$ terkoreksi Nadeau-Bengio dan statistik uji non-parametrik *Wilcoxon Signed-Rank Test*.
4. Menganalisis kompromi multi-kriteria (*accuracy vs latency vs power consumption*) untuk penerapan model kecerdasan buatan pada perangkat komputasi tepi (*edge AI*) drone dan traktor otonom.

### 1.3 Alokasi Waktu Pembelajaran (150 Menit)

| Sesi | Durasi | Aktivitas Instruktur | Aktivitas Mahasiswa | Output / Indikator |
| :---: | :---: | :--- | :--- | :--- |
| **I** | 20 Menit | **Apersepsi Industri:** Mengulas bahaya memilih model hanya berdasarkan selisih akurasi $1\%$ tanpa uji signifikansi statistik. | Berdiskusi mengenai risiko investasi hardware jutaan rupiah pada model yang belum teruji keunggulannya. | Mahasiswa memahami urgensi verifikasi inferensi statistik. |
| **II** | 35 Menit | **Teori Inferensi Komparatif:** Membedah kurva ROC, Youden's J, t-test terkoreksi Nadeau-Bengio, dan uji Wilcoxon/Friedman. | Mencatat formulasi, menelaah keterangan simbol, dan melafalkan cara membaca rumus. | Penguasaan matematis notasi koreksi varians dan ranking bertanda. |
| **III** | 50 Menit | **Hands-On Coding Lab:** Memandu eksekusi Jupyter Notebook `AI_Modul_6.4_Perbandingan_Performa_Model.ipynb`. | Menjalankan 10-fold CV untuk 4 model, memplot ROC, menghitung koreksi Nadeau-Bengio, dan skor utilitas. | Skrip berjalan lancar (0 error) dan grafik komparasi tersimpan. |
| **IV** | 30 Menit | **Bedah Kasus HOTS:** Diskusi kelompok komputasi manual koreksi Nadeau-Bengio dan kalkulasi drone edge AI. | Menghitung statistik $t$ manual dan memecahkan dilema kecepatan vs latensi respon nosel. | Mahasiswa mampu mengambil keputusan engineering yang tepat. |
| **V** | 15 Menit | **Refleksi & Sintesis:** Merangkum seluruh pembelajaran Part 6 dan mengantarkan jembatan konsep ke Part 7 (Machine Learning). | Menyusun rangkuman portofolio evaluasi model dan evaluasi mandiri. | Kesiapan menyeluruh menuju algoritma supervised learning. |

---

## 2. Kunci Jawaban Lengkap dan Pembahasan Evaluasi Mandiri Mahasiswa

### 2.1 Pembahasan Latihan 9.1: Komputasi Paired t-Test Terkoreksi Nadeau-Bengio

**Data Selisih Performa $R^2$ CatBoost (A) vs Random Forest (B) pada 10-Fold CV:**
$d = [0{,}03; 0{,}03; 0{,}01; 0{,}03; 0{,}02; 0{,}03; 0{,}01; 0{,}03; 0{,}00; 0{,}02]$
- Jumlah lipatan: $K = 10$
- Sampel uji per lipatan: $n_{\text{test}} = 100$
- Sampel latih per lipatan: $n_{\text{train}} = 900$

---

#### Butir 1: Rerata Selisih ($\bar{d}$) dan Varians Sampel Selisih ($s_d^2$)

$$\bar{d} = \frac{1}{K} \sum_{k=1}^{K} d_k$$

$$\sum_{k=1}^{10} d_k = (5 \times 0{,}03) + (2 \times 0{,}02) + (2 \times 0{,}01) + (1 \times 0{,}00) = 0{,}15 + 0{,}04 + 0{,}02 + 0{,}00 = 0{,}21$$

$$\bar{d} = \frac{0{,}21}{10} = 0{,}0210$$

**Kalkulasi Deviasi Kuadrat $(d_k - \bar{d})^2$:**
- Untuk $d_k = 0{,}03$ ($5$ kali): $(0{,}03 - 0{,}021)^2 = (0{,}009)^2 = 0{,}000081 \times 5 = 0{,}000405$
- Untuk $d_k = 0{,}02$ ($2$ kali): $(0{,}02 - 0{,}021)^2 = (-0{,}001)^2 = 0{,}000001 \times 2 = 0{,}000002$
- Untuk $d_k = 0{,}01$ ($2$ kali): $(0{,}01 - 0{,}021)^2 = (-0{,}011)^2 = 0{,}000121 \times 2 = 0{,}000242$
- Untuk $d_k = 0{,}00$ ($1$ kali): $(0{,}00 - 0{,}021)^2 = (-0{,}021)^2 = 0{,}000441 \times 1 = 0{,}000441$

$$\sum_{k=1}^{10} (d_k - \bar{d})^2 = 0{,}000405 + 0{,}000002 + 0{,}000242 + 0{,}000441 = 0{,}001090$$

$$s_d^2 = \frac{1}{K - 1} \sum_{k=1}^{10} (d_k - \bar{d})^2 = \frac{0{,}001090}{9} \approx 0{,}00012111$$

$$s_d = \sqrt{0{,}00012111} \approx 0{,}011005$$

---

#### Butir 2: Statistik Uji $t_{\text{standar}}$ Tanpa Koreksi

$$t_{\text{standar}} = \frac{\bar{d}}{\sqrt{\frac{s_d^2}{K}}}$$

**Keterangan Komponen Simbol:**
- $t_{\text{standar}}$: Nilai statistik uji $t$ berpasangan konvensional tanpa koreksi tumpang tindih data.
- $\bar{d}$: Rerata empiris selisih skor kedua model ($\bar{d} = 0{,}0210$).
- $\frac{s_d^2}{K}$: Estimasi varians dari rerata selisih sampel independen.

**Cara Membaca Rumus:**  
"Statistik uji t standar sama dengan rerata selisih bar d dibagi dengan akar dari varians sampel s kuadrat sub d per K."

**Kalkulasi Numerik:**
$$\text{SE}_{\text{standar}} = \sqrt{\frac{0{,}00012111}{10}} = \sqrt{0{,}000012111} \approx 0{,}003480$$

$$t_{\text{standar}} = \frac{0{,}0210}{0{,}003480} \approx 6{,}034$$

**Keputusan Uji Standar:**
- Derajat kebebasan: $\nu = K - 1 = 9$.
- Nilai kritis dua arah pada $\alpha = 0{,}05$: $t_{0{,}025; 9} = 2{,}262$.
- Karena $|t_{\text{standar}}| = 6{,}034 > 2{,}262$ ($p\text{-value} \approx 0{,}00019 < 0{,}05$), uji standar menolak hipotesis nol secara sangat mutlak.

---

#### Butir 3: Faktor Koreksi dan Statistik Uji $t_{\text{Nadeau-Bengio}}$

$$\text{Faktor Koreksi} = \frac{1}{K} + \frac{n_{\text{test}}}{n_{\text{train}}} = \frac{1}{10} + \frac{100}{900} = 0{,}1000 + 0{,}1111 = 0{,}2111$$

$$\sigma_{\text{corr}}^2 = s_d^2 \left( \frac{1}{K} + \frac{n_{\text{test}}}{n_{\text{train}}} \right) = 0{,}00012111 \times 0{,}21111 \approx 0{,}000025567$$

$$\text{SE}_{\text{corrected}} = \sqrt{\sigma_{\text{corr}}^2} = \sqrt{0{,}000025567} \approx 0{,}005056$$

$$t_{\text{Nadeau-Bengio}} = \frac{\bar{d}}{\text{SE}_{\text{corrected}}} = \frac{0{,}0210}{0{,}005056} \approx 4{,}153$$

**Keterangan Komponen Simbol:**
- $t_{\text{Nadeau-Bengio}}$: Nilai statistik uji $t$ yang dikoreksi terhadap ketergantungan observasi validasi silang.
- $\sigma_{\text{corr}}^2$: Varians selisih yang diperluas dengan memperhitungkan fraksi data latih yang tumpang tindih.

**Cara Membaca Rumus:**  
"Statistik t Nadeau Bengio sama dengan rerata selisih bar d dibagi dengan akar dari varians sampel s kuadrat sub d dikalikan faktor satu per K ditambah n test per n train."

---

#### Butir 4: Perbandingan dan Kesimpulan Ilmiah
- **Mengapa $t_{\text{Nadeau-Bengio}}$ ($4{,}153$) Lebih Kecil Dibanding $t_{\text{standar}}$ ($6{,}034$):**  
  Pada uji standar, faktor pembagi varians adalah $\frac{1}{K} = 0{,}1000$. Sedangkan pada koreksi Nadeau-Bengio, faktor pembagi menjadi $0{,}1000 + 0{,}1111 = 0{,}2111$ (lebih dari dua kali lipat lebih besar). Koreksi ini memasukkan penalti terhadap fakta bahwa $10$ model yang diuji saling berbagi $89\%$ data latih yang sama di setiap lipatan. Akibatnya, galat baku membengkak dari $0{,}00348$ menjadi $0{,}00506$, mengoreksi optimisme semu uji konvensional.
- **Kesimpulan Inferensi Statistik:**  
  Meskipun nilai statistik $t$ mengalami penurunan dari $6{,}034$ menjadi $4{,}153$, nilai $|t_{\text{Nadeau-Bengio}}| = 4{,}153$ **tetap jauh melampaui** nilai kritis $t_{0{,}025; 9} = 2{,}262$ ($p\text{-value} \approx 0{,}0025 < 0{,}05$).  
  **Keputusan Resmi:** Hipotesis nol $H_0$ tetap ditolak secara meyakinkan. Model **CatBoost terbukti secara signifikan lebih unggul daripada Random Forest** dalam memprediksi kadar air daun sawit, dan keunggulan tersebut bukan sekadar kebetulan statistik partisi data.

---

### 2.2 Pembahasan Latihan 9.2: Analisis Trade-off Komputasi & Ambang Batas Drone Edge AI

#### Butir 1: Analisis Kegagalan Fisik Model X (ResNet-50)
- **Parameter Operasional Drone:**
  - Kecepatan terbang drone: $v = 10 \text{ m/detik}$.
  - Waktu interval tangkapan kamera ($5 \text{ frame/detik}$): $t_{\text{frame}} = \frac{1}{5} \text{ detik} = 200 \text{ ms}$.
- **Analisis Waktu Reaksi Total Model X:**
  - Latensi inferensi model AI pada hardware Jetson Nano = $185\text{ ms}$.
  - Waktu respon fisik katup hidrolik nosel = $100\text{ ms}$.
  - Total waktu reaksi sistem sebelum cairan kimia disemprotkan:
    $$t_{\text{reaksi}} = 185\text{ ms} + 100\text{ ms} = 285\text{ ms} = 0{,}285\text{ detik}$$
- **Jarak Geser Fisik (*Physical Displacement Error*):**
  $$\Delta x = v \times t_{\text{reaksi}} = 10 \text{ m/detik} \times 0{,}285 \text{ detik} = 2{,}85\text{ meter}$$
- **Konsekuensi Agronomis Lapangan:**  
  Saat katup nosel terbuka dan menyemprotkan herbisida, posisi drone telah melesat sejauh **$2{,}85\text{ meter}$ melewati lokasi fisik gulma**! Semprotan racun gulma akan mengenai tanaman tebu produktif atau tanah kosong, sementara gulma target tidak tersentuh. Selain itu, konsumsi daya $10\text{ Watt}$ mempercepat habisnya baterai drone hingga $40\%$, memangkas durasi jelajah terbang per baterai dari $25$ menit menjadi hanya $15$ menit. Oleh karena itu, Model X secara fisik **mustahil diterapkan di lapangan**.

---

#### Butir 2: Komputasi Fungsi Utilitas Multi-Kriteria untuk Model Y dan Model Z

**Formulasi Fungsi Utilitas Terbobot:**
$$U(m) = w_1 \cdot \text{AUC}(m) + w_2 \cdot \left(1 - \frac{\text{Latensi}(m)}{\text{Latensi}_{\max}}\right) + w_3 \cdot \left(1 - \frac{\text{Daya}(m)}{\text{Daya}_{\max}}\right)$$

Dengan parameter:
- $w_1 = 0{,}50, \quad w_2 = 0{,}30, \quad w_3 = 0{,}20$
- $\text{Latensi}_{\max} = 100\text{ ms}$
- $\text{Daya}_{\max} = 10\text{ Watt}$

**1. Kalkulasi untuk Model Y (MobileNet-V3):**
- $\text{AUC}(Y) = 0{,}91$
- Skor Efisiensi Latensi: $u_{\text{lat}} = 1 - \frac{35}{100} = 1 - 0{,}35 = 0{,}65$
- Skor Efisiensi Daya: $u_{\text{daya}} = 1 - \frac{4}{10} = 1 - 0{,}40 = 0{,}60$

$$U(Y) = (0{,}50 \times 0{,}91) + (0{,}30 \times 0{,}65) + (0{,}20 \times 0{,}60)$$
$$U(Y) = 0{,}4550 + 0{,}1950 + 0{,}1200 = 0{,}7700$$

**2. Kalkulasi untuk Model Z (SVM Citra Klasik):**
- $\text{AUC}(Z) = 0{,}82$
- Skor Efisiensi Latensi: $u_{\text{lat}} = 1 - \frac{8}{100} = 1 - 0{,}08 = 0{,}92$
- Skor Efisiensi Daya: $u_{\text{daya}} = 1 - \frac{2}{10} = 1 - 0{,}20 = 0{,}80$

$$U(Z) = (0{,}50 \times 0{,}82) + (0{,}30 \times 0{,}92) + (0{,}20 \times 0{,}80)$$
$$U(Z) = 0{,}4100 + 0{,}2760 + 0{,}1600 = 0{,}8460$$

**Keputusan Manajerial Agribisnis:**
- Skor Utilitas Model Z ($0{,}8460$) **lebih tinggi** secara signifikan dibandingkan Model Y ($0{,}7700$).
- Pemenang objektif untuk implementasi komersial pada drone penyemprot herbisida adalah **Model Z (SVM Citra Klasik)**.
- **Rasionalisasi:** Dalam komputasi tepi (*edge AI*), latensi super cepat ($8\text{ ms}$) dan efisiensi daya baterai ($2\text{ Watt}$) memberikan keunggulan operasional yang jauh lebih krusial dibandingkan keunggulan margin AUC sebesar $0{,}09$ pada Model Y. Total waktu reaksi Model Z hanyalah $8\text{ ms} + 100\text{ ms} = 108\text{ ms}$ (geseran drone hanya $1{,}08\text{ meter}$, masih berada di dalam cakupan kerucut semprot nosel selebar $1{,}5\text{ meter}$).

---

## 3. Rubrik Penilaian Holistik & Analitik

| Kriteria Evaluasi | Bobot | Kinerja Luar Biasa (A: 85 - 100) | Kinerja Memadai (B: 70 - 84) | Kinerja Kurang (C: < 70) |
| :--- | :---: | :--- | :--- | :--- |
| **Kalkulasi Uji Nadeau-Bengio** | 40% | Menghitung $\bar{d}$, $s_d^2$, $t_{\text{standar}}$, faktor koreksi, dan $t_{\text{Nadeau-Bengio}}$ dengan ketelitian desimal tepat 100% serta menguraikan alasan penurunan nilai $t$. | Mampu menghitung uji standar dan Nadeau-Bengio namun ada kesalahan aritmatika kecil pada faktor koreksi $n_{\text{test}}/n_{\text{train}}$. | Gagal menerapkan faktor koreksi Nadeau-Bengio atau salah dalam menghitung varians selisih. |
| **Analisis Dinamika Fisik Drone** | 30% | Menghitung waktu reaksi total ($185+100\text{ ms}$), mengonversi ke pergeseran spasial fisik ($2{,}85\text{ m}$), dan menjelaskan implikasi agronomis semprotan herbisida. | Menyadari latensi terlalu lambat namun gagal mengaitkan secara kuantitatif dengan kecepatan drone ($v=10\text{ m/s}$). | Tidak mampu menghubungkan waktu komputasi perangkat lunak dengan respon fisik katup nosel. |
| **Optimasi Utilitas Multi-Kriteria** | 20% | Menghitung skor utilitas Model Y ($0{,}7700$) dan Model Z ($0{,}8460$) secara akurat dan memberikan rekomendasi manajerial yang tajam. | Menghitung skor utilitas dengan benar namun simpulan rekomendasi pemilihan model kurang didukung angka efisiensi. | Salah menyusun rumus fungsi utilitas atau salah memilih model pemenang. |
| **Kerapian Dokumentasi & Argumentasi** | 10% | Laporan terstruktur rapi, bahasa ilmiah baku, argumentasi didukung data statistik dan pertimbangan rekayasa pertanian. | Laporan cukup lengkap namun penarikan simpulan kurang sistematis. | Format berantakan, tidak mencantumkan satuan fisik atau derajat kebebasan uji. |

---

## 4. Tips Instruktur dan Mitigasi Kekeliruan Praktikum

1. **Kekeliruan Pemilihan Uji t Dua Sampel vs Berpasangan:**
   - Ingatkan mahasiswa bahwa model yang dievaluasi pada lipatan CV yang sama WAJIB diuji menggunakan uji berpasangan (*paired test*), BUKAN uji dua sampel independen (*two-sample independent t-test*), karena kedua model dievaluasi pada data uji yang persis sama.
2. **Koreksi Nadeau-Bengio untuk Leave-One-Out CV:**
   - Diskusikan bersama mahasiswa: *"Apa yang terjadi pada rasio $n_{\text{test}}/n_{\text{train}}$ jika kita menggunakan Leave-One-Out CV ($n_{\text{test}}=1$)? Rasio tersebut mendekati nol, sehingga faktor koreksi mendekati $1/K$."*
3. **Penyelarasan Ambang Batas Probabilitas vs Utilitas Bisnis:**
   - Tunjukkan bahwa titik Youden's $J$ mengasumsikan biaya kesalahan FP dan FN berbobot sama. Jika di lapangan biaya tanaman mati (FN) jauh lebih mahal daripada biaya penyemprotan berlebih (FP), titik ambang batas harus digeser ke kiri mendekati sensitivitas $100\%$.
