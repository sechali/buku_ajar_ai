# AI Modul 4.1: Panduan Instruktur dan Kunci Solusi
## Pengantar Data Science: Metodologi, Ekosistem, dan Pipeline Agribisnis

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

| Komponen | Rincian Instruksional |
| :--- | :--- |
| **Mata Kuliah** | Sains Data & Kecerdasan Buatan Terapan |
| **Kode Modul** | AI Modul 4.1 |
| **Topik Pembelajaran** | Pengantar Data Science, Siklus Hidup CRISP-DM, dan Arsitektur Pipeline Agribisnis |
| **Alokasi Waktu** | 3 SKS (150 Menit Tatap Muka/Laboratorium + 180 Menit Belajar Mandiri) |
| **Prasyarat** | AI Modul 3.1 - 3.10 (Pemrograman Python Dasar) |
| **Target OBE** | Sub-CPMK 4.1: Mahasiswa mampu merumuskan problem bisnis kebun ke dalam metodologi CRISP-DM dan membedakan peran profesi data dalam arsitektur agribisnis 4.0. |

### Matriks Distribusi Jam Pembelajaran (150 Menit)
1. **Sesi Pembuka & Refleksi Teoretis (30 Menit):**
   - Bedah Venn Diagram Sains Data dan analisis keterkaitan tiga domain (CS, Math/Stat, Agribisnis).
   - Penjelasan enam tahapan CRISP-DM dengan studi kasus nyata operasional kelapa sawit dan PKS.
2. **Sesi Interaktif & Analisis Arsitektur (30 Menit):**
   - Diskusi diferensiasi peran 4 profesi data (*Data Engineer, Analyst, Scientist, ML Engineer*).
   - Telaah arsitektur pipeline data telemetri cuaca AWS dan citra drone kebun.
3. **Praktikum Laboratorium Terbimbing (60 Menit):**
   - Eksplorasi berkas `notebooks/part-04/AI_Modul_4.1_Praktikum_Pengantar_Data_Science.ipynb`.
   - Profiling dataset blok sawit, imputasi nilai hilang, dan mitigasi *sensor spike* menggunakan metode IQR.
   - Pelatihan baseline regresi linier dan visualisasi matriks korelasi Pearson.
4. **Sesi Evaluasi & Diskusi HOTS (30 Menit):**
   - Presentasi mini kelompok perwakilan kelas mengenai rancangan alur CRISP-DM untuk menekan angka FFA.
   - Evaluasi kesimpulan statistika dan penegasan bahaya *spurious correlation*.

---

## 2. Strategi Pedagogis dan Panduan Fasilitasi Kelas

### 2.1 Pendekatan Socratic Questioning
Gunakan pertanyaan pemicu kritis sebelum membuka slide atau notebook praktikum:
- *"Jika model AI memprediksi bahwa semakin banyak pupuk ditabur maka produksi TBS terus meningkat tanpa batas, apakah kita bisa langsung mempercayai model tersebut? Hukum biologi apa yang dilanggar?"* (Pemicu untuk menghubungkan *Law of Diminishing Returns* dalam agronomi dengan batasan regresi linier).
- *"Mengapa seorang Data Scientist tidak bisa bekerja optimal jika Data Engineer belum menyelesaikan pekerjaannya?"*

### 2.2 Panduan Live-Coding dan Manajemen Error Praktikum
1. **Pastikan Non-GUI Backend Diaktifkan:**
   Ingatkan mahasiswa bahwa saat mengeksekusi script secara mandiri di server atau background terminal Windows, deklarasi `os.environ['MPLBACKEND'] = 'Agg'` mencegah jendela pop-up Matplotlib membekukan proses komputasi.
2. **Konsistensi Tipe Data Input Model:**
   Tekankan pentingnya menyuplai data prediksi dengan skema kolom yang identik (`pd.DataFrame(..., columns=X.columns)`) untuk mematuhi standar Scikit-Learn terbaru dan mencegah terjadinya *silent warning*.

---

## 3. Identifikasi dan Remediasi Miskonsepsi Mahasiswa

### Miskonsepsi 1: "Data Science identik dengan penguasaan syntax pustaka (library) Python semata."
- **Koreksi Konseptual:** *Library* seperti Pandas dan Scikit-Learn hanyalah alat komputasi. Tanpa pemahaman statistika (distribusi data, asumsi homokedastisitas, multikolinieritas) dan pemahaman biologis agronomi, model yang dihasilkan akan mengalami fenomena *"Garbage In, Garbage Out"*. Model prediktif yang dibangun di atas data cacat justru menyesatkan pengambilan keputusan kebun.

### Miskonsepsi 2: "Siklus hidup CRISP-DM bersifat linier sekuensial (waterfall)."
- **Koreksi Konseptual:** CRISP-DM adalah kerangka iteratif. Fase pemodelan (*Modeling*) hampir selalu memicu praktisi untuk kembali ke fase *Data Preparation* (misal: merekayasa ulang variabel lag cuaca) atau bahkan kembali ke fase *Data Understanding* jika ditemukan anomali distribusi data baru.

### Miskonsepsi 3: "Setiap baris data yang mengandung missing values harus langsung dihapus (dropna)."
- **Koreksi Konseptual:** Pada lingkungan perkebunan tropis, putusnya data sering disebabkan oleh sinyal telemetri seluler yang hilang secara periodik di pedalaman. Menghapus baris secara serampangan (*listwise deletion*) akan membuang 30-50% data penting dan menyebabkan bias sistemik. Teknik imputasi (median bergerak, interpolasi deret waktu) jauh lebih tepat secara ilmiah.

### Miskonsepsi 4: "Nilai korelasi Pearson tinggi ($r \approx 0.9$) membuktikan adanya hubungan sebab-akibat (kausalitas)."
- **Koreksi Konseptual:** *Correlation does not imply causation*. Dua variabel bisa berkorelasi tinggi secara kebetulan (*spurious correlation*) atau karena dipengaruhi variabel pengganggu ketiga (*confounding variable*). Misalnya, peningkatan penjualan es krim di kota dan peningkatan serangan hama ulat api di kebun mungkin berkorelasi karena keduanya sama-sama dipicu oleh kenaikan temperatur musim kemarau ekstrem.

---

## 4. Kunci Solusi dan Pembahasan Soal Latihan & HOTS

### 4.1 Pembahasan Soal Konseptual (Bobot: 30%)
1. **Dampak Data Understanding Dangkal terhadap Modeling:**
   - **Data Leakage (Kebocoran Data):** Terjadi jika fitur prediktor secara tidak sengaja memuat informasi yang baru tersedia di masa depan (setelah target terjadi). Contoh: memasukkan data berat fraksi brondolan di pabrik untuk memprediksi tonase panen di pohon. Akibatnya, skor evaluasi model saat latihan tampak sempurna ($R^2 \approx 1.0$), namun gagal total saat diterapkan di lapangan.
   - **Spurious Correlation (Korelasi Semu):** Menghubungkan variabel acak tanpa dasar agronomi. Jika analis tidak mengaudit data cuaca secara seksama, model mungkin mengasosiasikan lonjakan panen dengan penurunan tekanan udara harian yang sebenarnya merupakan fluktuasi instrumen biasa.
2. **Diferensiasi Peran Data Engineer vs ML Engineer:**
   - **Data Engineer:** Bertanggung jawab atas kelaikan transmisi data dari kamera pintar di lapangan ke penyimpanan awan/server lokal. Fokus pada *bandwidth*, konkurensi streaming RTSP, pembersihan paket data yang korup, dan penyimpanan di *data lake*.
   - **ML Engineer:** Bertanggung jawab mengonversi model deteksi citra (misalnya YOLOv8) ke format inferensi ringan (*TensorRT/ONNX*), memasangnya ke mikrokomputer *edge AI* (misal NVIDIA Jetson di pos satpam kebun), mengoptimalkan latensi inferensi (< 100 ms), serta memantau penurunan akurasi model (*model drift*).

### 4.2 Pembahasan Studi Kasus CRISP-DM: Mitigasi Lonjakan FFA (Bobot: 40%)
- **a. Fase Business Understanding:**
  - *Pertanyaan Bisnis:* "Bagaimana cara memprediksi estimasi tonase panen per blok afdeling 24 jam sebelum panen agar armada truk dapat dialokasikan tepat waktu sehingga waktu tunggu TBS di TPH tidak melebihi 24 jam?"
  - *Metrik Keberhasilan:* Teknis: MAPE estimasi tonase $< 10\%$. Bisnis: Penurunan rata-rata waktu inap TBS di TPH dari 36 jam menjadi $< 18$ jam, dan kadar FFA CPO di PKS stabil $< 3.0\%$.
- **b. Fase Data Understanding (4 Sumber Data Heterogen):**
  1. *Data Sensor AWS:* Curah hujan harian kumulatif dan kelembaban udara per afdeling.
  2. *Data Buku Mandor (Logbook Panen):* Jumlah tenaga pemanen aktif, taksasi kerapatan matang buah (AKP - Angka Kerapatan Panen).
  3. *Data Telematika GPS Truk:* Waktu tempuh armada dari TPH ke jembatan timbang PKS beserta kapasitas riil angkut.
  4. *Data Historis Laboratorium PKS:* Rekam jejak kadar FFA dan persentase buah mentah/masak per nomor blok pengirim.
- **c. Fase Data Preparation (2 Strategi Feature Engineering Agronomis):**
  1. *Indeks Kematangan Buah Terintegrasi:* $\text{Indeks AKP} = \frac{\text{Jumlah Janjang Masak Terhitung}}{\text{Total Pokok Sensus}} \times 100\%$.
  2. *Waktu Tunggu Kumulatif Proyeksi:* Menghitung selisih waktu antara estimasi jam potong buah pertama mandor dengan jadwal tibanya truk penjemput berdasarkan jarak tempuh kilometer dan kondisi jalan kebun (aspal vs jalan tanah merah).

### 4.3 Pembahasan Tantangan Komputasi Matematis (Bobot: 30%)
Diberikan himpunan data kelembaban tanah:
$$X = \{ 32.5, 34.0, 31.8, 33.2, 58.0, 32.1 \}$$

**Langkah 1: Perhitungan Rerata Aritmatika ($\bar{x}$):**
$$\sum_{i=1}^6 x_i = 32.5 + 34.0 + 31.8 + 33.2 + 58.0 + 32.1 = 221.6$$
$$\bar{x} = \frac{221.6}{6} \approx 36.93\%$$

**Langkah 2: Perhitungan Median ($\tilde{x}$):**
Urutkan data secara menaik (*ascending order*):
$$X_{\text{sorted}} = \{ 31.8, 32.1, 32.5, 33.2, 34.0, 58.0 \}$$
Karena ukuran sampel genap ($n = 6$), median adalah nilai tengah antara data ke-3 dan ke-4:
$$\tilde{x} = \frac{X_{(3)} + X_{(4)}}{2} = \frac{32.5 + 33.2}{2} = \frac{65.7}{2} = 32.85\%$$

**Langkah 3: Analisis Representasi dan Outlier:**
- **Metrik Paling Representatif:** Nilai **Median (32.85%)** jauh lebih representatif dibanding rerata (36.93%). Rerata tertarik secara signifikan ke arah kanan akibat adanya nilai ekstrim 58.0%.
- **Alasan Matematis Outlier:** Mayoritas data terkonsentrasi sangat rapat pada rentang $31.8\% - 34.0\%$ (rentang hanya $2.2\%$). Nilai 58.0% berjarak lebih dari $24\%$ dari kelompok utama.
- **Tindakan Data Scientist:** Nilai 58.0% kemungkinan besar merupakan artefak fisik (sensor terendam genangan air sesaat setelah hujan lokal atau korsleting probe tanah). Pada fase *Data Preparation*, nilai ini tidak boleh dibiarkan karena akan merusak perhitungan koefisien gradien regresi. Solusi: melakukan kliping menggunakan batas atas Tukey ($Q_3 + 1.5 \times \text{IQR}$) atau menggantinya dengan nilai median lokal afdeling tersebut.

---

## 5. Rubrik Penilaian Berbasis Capaian (OBE Assessment Rubric)

| Dimensi Penilaian | Sangat Kurang (< 50) | Cukup (50 - 69) | Baik (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Metodologi CRISP-DM (Kognitif)** | Tidak memahami tahapan dan menganggap alur analisis data bersifat sekuensial mutlak tanpa validasi. | Menyebutkan 6 tahapan CRISP-DM namun gagal mengaitkannya dengan masalah perkebunan sawit. | Mampu memetakan tahapan ke skenario agribisnis namun kurang mendalam pada fase rekayasa fitur. | Mampu merancang dokumen kerja CRISP-DM lengkap dengan perumusan metrik bisnis, audit data multi-sumber, dan deployment. |
| **Eksekusi Komputasi & Profiling (Psikomotorik)** | Script notebook gagal dieksekusi, terdapat galat (*syntax/runtime error*), tidak ada pembersihan data. | Notebook berjalan namun pembersihan nilai hilang hanya menggunakan `dropna` tanpa pertimbangan statistika. | Berhasil mengimputasi nilai hilang dan outlier dengan benar serta menampilkan grafik korelasi dengan rapi. | Mampu mengeksekusi end-to-end pipeline, menghasilkan visualisasi analitik berkualitas tinggi, dan membangun fungsi deployment. |
| **Integritas Ilmiah & Ketelitian Analisis (Afektif)** | Mengabaikan interpretasi data ekstrim dan menarik kesimpulan kausalitas semu secara serampangan. | Menyadari keberadaan outlier namun tidak memberikan justifikasi penanganan secara ilmiah. | Menjelaskan implikasi outlier terhadap rerata vs median dengan argumentasi logis. | Menunjukkan kepekaan ilmiah tinggi terhadap etika data, bias sensorik, serta validitas biologi tanaman sawit. |
