# AI Modul 6.3: Panduan Instruktur dan Kunci Solusi Validasi Silang (Cross-Validation)

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) dan Panduan Pedagogis

### 1.1 Informasi Umum Modul
- **Mata Kuliah:** Kecerdasan Buatan dan Sains Data Pertanian Presisi
- **Modul:** 6.3 (Validasi Silang: K-Fold, Stratifikasi, Grouping, dan Time-Series Split)
- **Sasaran Peserta:** Mahasiswa Program Studi Agroteknologi, Agribisnis, dan Teknik Pertanian INSTIPER Yogyakarta
- **Alokasi Waktu:** 150 Menit (1 Sesi Tatap Muka / Praktikum Komputasi)

### 1.2 Tujuan Instruksional Khusus (TIK)
Pada akhir sesi pembelajaran ini, mahasiswa diharapkan mampu:
1. Menjelaskan secara analitis kelemahan *Hold-Out Validation* dan urgensi statistik prosedur *K-Fold Cross-Validation*.
2. Memilih teknik partisi data yang tepat (*Stratified K-Fold*, *Group K-Fold*, *Time-Series Split*) berdasarkan sifat ketergantungan agronomis data lapangan.
3. Menghitung galat rerata, varians antar-lipatan, dan galat baku (*standard error*) estimasi model secara manual dan terprogram.
4. Menganalisis fenomena kebocoran spasial (*spatial data leakage*) pada pemodelan tanah dan kanopi perkebunan kelapa sawit.

### 1.3 Alokasi Waktu Pembelajaran (150 Menit)

| Sesi | Durasi | Aktivitas Instruktur | Aktivitas Mahasiswa | Output / Indikator |
| :---: | :---: | :--- | :--- | :--- |
| **I** | 20 Menit | **Apersepsi & Refleksi Kritis:** Menunjukkan bahaya evaluasi tunggal (*lucky split*) pada estimasi panen sawit. | Menanggapi pertanyaan pemantik mengenai perbedaan hasil uji acak. | Kesadaran akan risiko optimisme semu pemodelan. |
| **II** | 35 Menit | **Teori Validasi Silang & Struktur Data:** Menjelaskan formulasi $K$-Fold, varians, galat baku, serta isolasi spasial dan temporal. | Mencatat notasi matematis, keterangan komponen, dan melafalkan cara membaca rumus. | Pemahaman mendalam formula $\bar{S}$, $s^2_{\text{CV}}$, dan $\text{SE}(\bar{S})$. |
| **III** | 50 Menit | **Hands-On Coding Lab:** Memandu eksekusi Jupyter Notebook `AI_Modul_6.3_Cross_Validation.ipynb`. | Menjalankan perbandingan K-Fold biasa vs Stratified vs Group K-Fold pada dataset kebun. | Eksekusi 0 error, plot perbandingan varians tersimpan. |
| **IV** | 30 Menit | **Bedah Kasus HOTS:** Diskusi kelompok analisis kebocoran spasial 5 afdeling dan komputasi varians 5-Fold. | Menghitung galat baku manual dan merumuskan hipotesis agronomis Lipatan 3. | Penguasaan analitis mitigasi autokorelasi spasial. |
| **V** | 15 Menit | **Refleksi & Sintesis:** Menegaskan batas toleransi risiko model dan mengantar ke Modul 6.4 (Perbandingan Model). | Menyimpulkan kriteria kelayakan model sebelum produksi. | Mahasiswa siap beralih ke uji signifikansi komparatif. |

---

## 2. Kunci Jawaban Lengkap dan Pembahasan Evaluasi Mandiri Mahasiswa

### 2.1 Pembahasan Latihan 9.1: Analisis Teoretis Kebocoran Spasial Kebun Sawit

#### 1. Penyebab Perbedaan Nilai $R^2$ Mahasiswa A ($0{,}94$) dan Mahasiswa B ($0{,}76$)
- **Fenomena Geospasial:** Terjadi fenomena **Autokorelasi Spasial** (*Spatial Autocorrelation*), yang berakar pada Hukum Pertama Geografi Tobler: *"Segala sesuatu berhubungan dengan hal lainnya, tetapi hal-hal yang berjarak dekat lebih berhubungan erat dibandingkan hal-hal yang berjarak jauh."*
- **Mekanisme Kebocoran Data (*Spatial Data Leakage*):**  
  Pada metode Mahasiswa A (`train_test_split` acak), titik-titik data latih dan data uji diambil secara acak dari afdeling yang sama. Akibatnya, titik uji berjarak hanya beberapa meter dari titik latih dengan karakteristik tanah, kelembaban, dan elevasi yang hampir identik. Model regresi Mahasiswa A tidak mempelajari relasi sebab-akibat kelembaban secara mendasar, melainkan sekadar melakukan "interpolasi tetangga terdekat" (*nearest-neighbor interpolation*). Nilai $R^2 = 0{,}94$ merupakan **optimisme semu** (*overly optimistic evaluation*) yang menyesatkan.
- Sebaliknya, Mahasiswa B mengisolasi seluruh afdeling ke dalam lipatan terpisah (`GroupKFold`). Model dilatih pada 4 afdeling dan diuji pada 1 afdeling utuh yang belum pernah disentuh, sehingga bebas dari kebocoran spasial. Nilai $R^2 = 0{,}76$ mencerminkan daya generalisasi hakiki model.

#### 2. Proyeksi Performa Model Mahasiswa A di Afdeling Baru (Afdeling 6)
- **Perkiraan Performa:** Nilai $R^2$ akan anjlok drastis dan berada di kisaran **$\le 0{,}76$** (bahkan berpotensi lebih rendah jika jenis tanah di Afdeling 6 memiliki karakteristik edafik baru).
- **Argumentasi Ilmiah:** Di Afdeling 6, model Mahasiswa A tidak lagi memiliki titik-titik sampel acak tetangga di data latih untuk "dicontek". Model dipaksa melakukan ekstrapolasi murni pada bentang lahan baru. Fenomena keruntuhan performa saat model dipindahkan ke lokasi baru disebut *spatial out-of-distribution drop*.

#### 3. Keunggulan Metodologi Mahasiswa B bagi Sains Data Pertanian Presisi
Pendekatan Mahasiswa B (*Spatial Group K-Fold*) merepresentasikan skenario operasional dunia nyata perkebunan:
- Dalam manajemen agribisnis komersial, traktor otonom, drone pemupukan, atau sistem sensor IoT akan dipasang pada blok-blok kebun baru tanpa memerlukan pengambilan sampel tanah intensif ulang.
- Validasi berbasis pengelompokan afdeling menjamin bahwa model memiliki ketangguhan terhadap variasi spasial lokal dan memberikan estimasi risiko yang jujur bagi tim manajemen agronomi.

---

### 2.2 Pembahasan Latihan 9.2: Komputasi Varians dan Galat Baku Lintas Lipatan

**Data Hasil 5-Fold Cross-Validation (RMSE dalam Ton/Ha):**
- Lipatan 1 ($k=1$): $RMSE_1 = 1{,}85 \text{ Ton/Ha}$
- Lipatan 2 ($k=2$): $RMSE_2 = 1{,}92 \text{ Ton/Ha}$
- Lipatan 3 ($k=3$): $RMSE_3 = 2{,}45 \text{ Ton/Ha}$
- Lipatan 4 ($k=4$): $RMSE_4 = 1{,}78 \text{ Ton/Ha}$
- Lipatan 5 ($k=5$): $RMSE_5 = 1{,}80 \text{ Ton/Ha}$

#### Butir 1: Rerata Estimasi Galat ($\bar{S}$)

$$\bar{S} = \frac{1}{K} \sum_{k=1}^{K} S_k$$

**Keterangan Komponen Simbol:**
- $\bar{S}$: Rerata skor evaluasi performa model lintas lipatan validasi silang (skalar riil, dalam satuan Ton/Ha).
- $K$: Jumlah total lipatan partisi data ($K = 5$, bilangan bulat positif).
- $S_k$: Nilai metrik performa (RMSE) pada lipatan uji ke-$k$ (skalar riil non-negatif).

**Cara Membaca Rumus:**  
"Nilai rerata skor validasi silang, simbol bar S, dihitung dengan menjumlahkan skor evaluasi S sub k dari lipatan k sama dengan satu sampai K, kemudian dibagi dengan jumlah lipatan K."

**Kalkulasi Numerik:**
$$\bar{S} = \frac{1{,}85 + 1{,}92 + 2{,}45 + 1{,}78 + 1{,}80}{5} = \frac{9{,}80}{5} = 1{,}960 \text{ Ton/Ha}$$

---

#### Butir 2: Varians Sampel ($s^2_{\text{CV}}$), Deviasi Standar ($s_{\text{CV}}$), dan Galat Baku ($\text{SE}(\bar{S})$)

1. **Varians Sampel ($s^2_{\text{CV}}$):**

$$s^2_{\text{CV}} = \frac{1}{K - 1} \sum_{k=1}^{K} (S_k - \bar{S})^2$$

**Keterangan Komponen Simbol:**
- $s^2_{\text{CV}}$: Varians sampel lintas lipatan validasi silang (skalar riil, dalam kuadrat satuan Ton/Ha).
- $K - 1$: Derajat kebebasan sampel Bessel ($5 - 1 = 4$).
- $(S_k - \bar{S})^2$: Kuadrat selisih antara nilai lipatan ke-$k$ dengan rerata keseluruhan.

**Cara Membaca Rumus:**  
"Varians validasi silang, simbol s kuadrat sub C V, dihitung dengan menjumlahkan kuadrat selisih skor tiap lipatan S sub k terhadap rerata bar S, dibagi dengan derajat kebebasan K dikurangi satu."

**Kalkulasi Kuadrat Selisih:**
- $k=1$: $(1{,}85 - 1{,}96)^2 = (-0{,}11)^2 = 0{,}0121$
- $k=2$: $(1{,}92 - 1{,}96)^2 = (-0{,}04)^2 = 0{,}0016$
- $k=3$: $(2{,}45 - 1{,}96)^2 = (+0{,}49)^2 = 0{,}2401$
- $k=4$: $(1{,}78 - 1{,}96)^2 = (-0{,}18)^2 = 0{,}0324$
- $k=5$: $(1{,}80 - 1{,}96)^2 = (-0{,}16)^2 = 0{,}0256$

$$\sum_{k=1}^{5} (S_k - \bar{S})^2 = 0{,}0121 + 0{,}0016 + 0{,}2401 + 0{,}0324 + 0{,}0256 = 0{,}3118$$

$$s^2_{\text{CV}} = \frac{0{,}3118}{4} = 0{,}07795 \approx 0{,}0780 \text{ (Ton/Ha)}^2$$

2. **Deviasi Standar ($s_{\text{CV}}$):**
$$s_{\text{CV}} = \sqrt{s^2_{\text{CV}}} = \sqrt{0{,}07795} \approx 0{,}2792 \text{ Ton/Ha}$$

3. **Galat Baku Rerata ($\text{SE}(\bar{S})$):**

$$\text{SE}(\bar{S}) = \frac{s_{\text{CV}}}{\sqrt{K}}$$

**Keterangan Komponen Simbol:**
- $\text{SE}(\bar{S})$: Galat baku (*standard error*) dari estimasi titik rerata $\bar{S}$ (skalar riil, dalam satuan Ton/Ha).
- $s_{\text{CV}}$: Deviasi standar antar-lipatan validasi silang (Ton/Ha).
- $\sqrt{K}$: Akar kuadrat dari ukuran sampel lipatan ($\sqrt{5} \approx 2{,}2361$).

**Cara Membaca Rumus:**  
"Galat baku rerata estimasi, simbol S E kurung bar S, sama dengan deviasi standar s sub C V dibagi akar kuadrat dari jumlah lipatan K."

**Kalkulasi Numerik:**
$$\text{SE}(\bar{S}) = \frac{0{,}2792}{\sqrt{5}} = \frac{0{,}2792}{2{,}23607} \approx 0{,}1249 \text{ Ton/Ha}$$

---

#### Butir 3: Investigasi Diagnostik Anomali Lipatan 3 ($RMSE_3 = 2{,}45$)
Lipatan 3 menyumbang lebih dari $77\%$ terhadap total kuadrat deviasi varians ($0{,}2401$ dari $0{,}3118$). Lonjakan galat yang tajam ini mengindikasikan ketidaksesuaian representasi data latih terhadap blok uji ketiga.

**Dua Hipotesis Agronomis Lapangan:**
1. **Perbedaan Kondisi Topografi & Drainase Mikro (Stres Genangan Air):**  
   Blok uji pada Lipatan 3 kemungkinan besar berada di area cekungan (*lowland / depression area*) dengan sistem tata air/drainase yang buruk. Genangan air mikro memicu stres klorosis pada daun kelapa sawit, sehingga reflektansi spektral kanopi menyerupai tanaman berproduksi rendah, padahal tanaman sebenarnya menyimpan tandan buah normal.
2. **Heterogenitas Varietas Bibit atau Tingkat Serangan Patogen Lokal:**  
   Blok kebun pada Lipatan 3 mungkin ditanami bibit kelapa sawit generasi berbeda (misalnya DxP Marihat berumur 18 tahun vs blok lain DxP Dami berumur 10 tahun) atau tengah mengalami infestasi penyakit busuk pangkal batang (*Ganoderma boninense*) stadium awal. Serangan ini merusak arsitektur pelepah kanopi sebelum produktivitas tandan buah anjlok secara drastis, membingungkan fitur penglihatan kanopi drone model AI.

---

#### Butir 4: Evaluasi Kriteria Toleransi Manajemen Agribisnis

Manajemen menetapkan batas penerimaan:
$$\bar{S} + 2 \times \text{SE}(\bar{S}) \le 2{,}20 \text{ Ton/Ha}$$

**Kalkulasi Batas Atas Interval Kepercayaan:**
$$\bar{S} + 2 \times \text{SE}(\bar{S}) = 1{,}960 + 2 \times (0{,}1249) = 1{,}960 + 0{,}2498 = 2{,}2098 \approx 2{,}21 \text{ Ton/Ha}$$

**Keputusan Manajerial:**
- Nilai ambang batas atas estimasi risiko model ($2{,}2098 \text{ Ton/Ha}$) **melampaui** ambang toleransi maksimal ($2{,}2000 \text{ Ton/Ha}$) sebesar $0{,}0098 \text{ Ton/Ha}$.
- **Keputusan:** Model AI **BELUM LAYAK DISETUJUI** untuk operasional taksasi panen tahunan skala komersial sebelum anomali pada Lipatan 3 diinvestigasi tuntas.
- **Rekomendasi Tindak Lanjut:** Tim AI agronomi harus melakukan kalibrasi stratifikasi dengan menyertakan fitur kovariat elevasi digital (*Digital Surface Model* / DSM) dan indeks kerapatan tajuk sebelum pengujian validasi silang diulang.

---

## 3. Rubrik Penilaian Holistik & Analitik

| Kriteria Evaluasi | Bobot | Kinerja Luar Biasa (A: 85 - 100) | Kinerja Memadai (B: 70 - 84) | Kinerja Kurang (C: < 70) |
| :--- | :---: | :--- | :--- | :--- |
| **Analisis Kebocoran Spasial** | 40% | Mengaitkan disparitas $R^2$ secara tepat dengan autokorelasi spasial Tobler, menjelaskan mekanisme kebocoran data, dan memproyeksikan performa kebun baru secara saintifik. | Menjelaskan autokorelasi spasial namun argumentasi mengenai performa afdeling baru kurang tajam secara agronomis. | Gagal mengenali fenomena kebocoran spasial; menganggap perbedaan skor semata-mata faktor acak. |
| **Kalkulasi Statistik Lintas Lipatan** | 35% | Menghitung $\bar{S}$, varians Bessel ($K-1$), deviasi standar, dan galat baku dengan ketelitian desimal sempurna tanpa kesalahan rumus. | Mampu menghitung $\bar{S}$ dan deviasi standar namun keliru menggunakan pembagi $K$ alih-alih $K-1$ pada varians. | Salah menghitung varians atau galat baku; tidak memahami arti fisik galat baku. |
| **Diagnostik Lapangan & Kebijakan** | 25% | Merumuskan 2 hipotesis agronomis yang sangat masuk akal (topografi/patogen) dan mengambil keputusan penolakan model secara tegas berdasarkan angka uji. | Memberikan hipotesis lapangan umum namun analisis kelayakan batas toleransi kurang presisi. | Tidak dapat memberikan hipotesis teknis perkebunan dan salah menyimpulkan kelayakan model. |

---

## 4. Tips Instruktur dan Mitigasi Kekeliruan Praktikum

1. **Kekeliruan Pembagi Derajat Kebebasan Bessel ($K-1$):**
   - Banyak mahasiswa membagi jumlah kuadrat deviasi dengan $K=5$ alih-alih $K-1=4$. Tekankan bahwa pada sampel kecil ($K=5$ atau $K=10$), penggunaan pembagi Bessel $K-1$ adalah wajib secara statistik agar varians tidak mengalami bias estimasi ke bawah (*underestimation*).
2. **Klarifikasi Perbedaan Standard Deviation vs Standard Error:**
   - Jelaskan bahwa deviasi standar $s_{\text{CV}}$ mengukur variabilitas performa antar-lipatan, sedangkan galat baku $\text{SE}(\bar{S})$ mengukur ketidakpastian seputar rerata performa estimasi $\bar{S}$.
3. **Peringatan Penting tentang Preprocessing di Dalam Lipatan:**
   - Ingatkan mahasiswa agar seluruh proses penskalaan fitur (`StandardScaler`, `MinMaxScaler`) dimasukkan ke dalam `Pipeline` Scikit-Learn agar `fit()` hanya dijalankan pada data latih di dalam tiap lipatan, mencegah kebocoran data (*data leakage*).
