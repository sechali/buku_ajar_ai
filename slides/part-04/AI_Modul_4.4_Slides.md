---
marp: true
theme: default
paginate: true
header: "Bagian 4: Pengolahan, Analisis, dan Visualisasi Data Ilmiah • AI Modul 4.4"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 4.4: Data Cleaning dan Preprocessing
### Bagian 4: Pengolahan, Analisis, dan Visualisasi Data Ilmiah
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Mendiagnosis (C4) anomali data mentah: data hilang (Missing Data MCAR, MAR, MNAR), data duplikat, dan ketidakkonsistenan tipe data.
- Menerapkan (C3) strategi imputasi nilai hilang (rerata, median, interpolasi temporal, dan imputasi KNN) pada telemetri cuaca kebun.
- Menganalisis (C4) keberadaan nilai pencilan (Outliers) menggunakan metode parametrik (Z-Score) dan non-parametrik (Interquartile Range / IQR).
- Merancang (C3) pipeline prapemrosesan pembersihan data yang terisolasi untuk mencegah kebocoran informasi (data leakage) sebelum pelatihan model.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Data Cleaning dan Preprocessing.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$P(M \mid Y_{\text{obs}}, Y_{\text{mis}}) = P(M)$$

- Pemetaan fitur masukan ke ruang representasi laten.
- Pemandu gradien menuju titik konvergensi stabil.

---

# Arsitektur Komputasi & Diagram Alir Pipeline

1. **Tahap 1: Ingesti Data Sensor / Citra** - Akuisisi data mentah dari sensor perkebunan, CCTV sortasi TBS, atau drone.
2. **Tahap 2: Preprocessing & Normalisasi** - Transformasi citra, filtering noise, standardisasi rentang fitur.
3. **Tahap 3: Mesin Inferensi & Ekstraksi** - Propagasi maju melewati arsitektur pemodelan komputasi.
4. **Tahap 4: Post-processing & Aksi Kontrol** - Thresholding analitis, verifikasi toleransi, dan pemicuan aktuator otomatis.

---

# Implementasi Komputasional Berstandar Industri

```python
### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini, mahasiswa dan pembelajar diharapkan mampu:
1. **Mendiagnosis (C4)** anomali data mentah: data hilang (*Missing Data* MCAR, MAR, MNAR), data duplikat, dan ketidakkonsistenan tipe data.
2. **Menerapkan (C3)** strategi imputasi nilai hilang (rerata, median, interpolasi temporal, dan imputasi KNN) pada telemetri cuaca kebun.
3. **Menganalisis (C4)** keberadaan nilai pencilan (*Outliers*) menggunakan metode parametrik ($Z$-Score) dan non-parametrik (*Interquartile Range* / IQR).
4. **Merancang (C3)** pipeline prapemrosesan pembersihan data yang terisolasi untuk mencegah kebocoran informasi (*data leakage*) sebelum pelatihan model.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Mendiagnosis tiga mekanisme formal data hilang (*Missing Completely at Random* - MCAR, *Missing at Random* - MAR, dan *Missing Not at Random* - MNAR) pada data perkebunan kelapa sawit.
  * Memilih dan mengimplementasikan strategi imputasi yang tepat (median univariat, *K-Nearest Neighbors Imputer*, atau *Multivariate Imputation by Chained Equations* - MICE).
  * Mendeteksi anomali pencilan univariat dan multivariat menggunakan metode parametrik ($Z$-score), non-parametrik (rentang interkuartil Tukey IQR), dan *Modified Z-Score* berbasis *Median Absolute Deviation* (MAD).
  * Melakukan mitigasi pencilan melalui teknik *Winsorizing* (kliping batas kuartil) tanpa membuang baris data penting.
  * Membangun alur pra-pemrosesan data yang modular dan kebal kebocoran data (*leak-free*) menggunakan `sklearn.pipeline.Pipeline` dan `sklearn.compose.ColumnTransformer`.
# ... [lanjutan pipeline teroptimasi]
```

- **Kompleksitas Waktu**: $O(N \cdot d)$ pada tahap pelatihan; $O(d)$ deterministik pada fase inferensi real-time.
- **Kompleksitas Memori**: Efisien melalui tensor chunking dan batch generators.
- **Latensi Inferensi**: $< 35\text{ ms}$ pada edge hardware industrial.

---

# Aplikasi Nyata Industri & Studi Kasus Agrokompleks

### Tantangan Operasional (PKS & Perkebunan Sawit)
- Fluktuasi pencahayaan alami matahari dan partikel debu di area sortasi loading ramp PKS.
- Throughput masif 45-60 ton TBS per jam menuntut keputusan klasifikasi instan tanpa jeda antrean armada truk.
- Subjektivitas operator sortasi manual memicu variasi standar mutu dan potensi buah mentah terolah.

### Solusi AI & Dampak Bisnis Terukur
- Integrasi sistem inferensi real-time berbasis Data Cleaning dan Preprocessing.
- Akurasi klasifikasi kematangan $> 94.5\%$ dengan F1-score seimbang.
- Penurunan fraksi buah mentah $< 2\%$, menjaga kadar Asam Lemak Bebas (ALB) tetap rendah dan memaksimalkan rendemen CPO.

---

# Kekeliruan Metodologis & Protokol Mitigasi Teruji

1. **Kekeliruan #1: Data Leakage & Spatial Autocorrelation**
   - *Masalah*: Random train-test split pada data spasial bertetangga menimbulkan evaluasi over-optimistik.
   - *Mitigasi*: Terapkan *Spatial Block Cross-Validation* berdasarkan isolasi fisik afdeling kebun.
2. **Kekeliruan #2: Numerical Instability & Parameter Saturation**
   - *Masalah*: Melewatkan scaling fitur memicu ledakan gradien atau saturasi nilai aktivasi.
   - *Mitigasi*: Gunakan *StandardScaler* terisolasi, inisialisasi bobot He/Xavier, dan *Gradient Clipping*.
3. **Kekeliruan #3: Covariate Shift pada Deployment Lapangan**
   - *Masalah*: Model dilatih hanya pada musim kemarau, akurasi anjlok drastis saat musim hujan.
   - *Mitigasi*: Terapkan augmentasi fotometrik agresif (*ColorJitter*, CLAHE) dan pipeline monitoring drift.

---

# Sintesis Modul & Evaluasi Kritis

### Intisari Pembelajaran (Key Takeaways)
- Kecerdasan komputasi memadukan fondasi matematika analitis dengan standar rekayasa perangkat lunak tangguh.
- Arsitektur sistem harus mengoptimalkan keseimbangan daya representasi vs latensi komputasi.
- Nilai nyata AI di perkebunan ditentukan oleh ketahanan operasional dan dampak finansial terukur.

### Diskusi Kritis (HOTS)
- Bagaimana merancang mekanisme fallback deterministik apabila model menghadapi anomali sensor ekstrem?
- Kapan komputasi edge lokal lebih diunggulkan dibanding komputasi cloud pada perkebunan remote?
- Metrik kuantitatif apa selain akurasi yang paling krusial untuk membuktikan kelayakan operasional modul ini di PKS?
