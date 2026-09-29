---
marp: true
theme: default
paginate: true
header: "Bagian 4: Pengolahan, Analisis, dan Visualisasi Data Ilmiah • AI Modul 4.2"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 4.2: NumPy untuk Komputasi Numerik
### Bagian 4: Pengolahan, Analisis, dan Visualisasi Data Ilmiah
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Menguraikan (C2) arsitektur internal larik ndarray NumPy: blok memori kontinu C, strides, dan penentuan tipe data homogen (dtypes).
- Menerapkan (C3) operasi larik tervektorisasi (vectorization) dan aturan penyiaran (broadcasting) untuk komputasi aljabar linier bebas loop Python.
- Menganalisis (C4) perbandingan efisiensi waktu eksekusi dan konsumsi cache CPU antara list bawaan Python versus NumPy ndarray.
- Menghitung (C3) indeks vegetasi multispektral UAV (seperti NDVI dan SAVI) secara terprogram menggunakan operasi matriks tervektorisasi.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada NumPy untuk Komputasi Numerik.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\text{Strides}_{\text{C-order}} = (N \times 8, 8)$$

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
1. **Menguraikan (C2)** arsitektur internal larik ndarray NumPy: blok memori kontinu C, *strides*, dan penentuan tipe data homogen (*dtypes*).
2. **Menerapkan (C3)** operasi larik tervektorisasi (*vectorization*) dan aturan penyiaran (*broadcasting*) untuk komputasi aljabar linier bebas loop Python.
3. **Menganalisis (C4)** perbandingan efisiensi waktu eksekusi dan konsumsi cache CPU antara list bawaan Python versus NumPy ndarray.
4. **Menghitung (C3)** indeks vegetasi multispektral UAV (seperti NDVI dan SAVI) secara terprogram menggunakan operasi matriks tervektorisasi.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Menjelaskan perbedaan arsitektur memori antara Python `list` (larik penunjuk objek heterogen) dan NumPy `ndarray` (blok penyangga kontigu homogen).
  * Menghitung langkah memori (*strides*) dan memproyeksikan alamat fisik elemen matriks berdasarkan tata letak *C-contiguous* dan *Fortran-contiguous*.
  * Menerapkan tiga aturan formal kompatibilitas dimensi *broadcasting* pada operasi aritmatika larik multi-dimensi tanpa menduplikasi alokasi RAM fisik.
  * Melakukan operasi pengirisan tingkat lanjut (*advanced slicing*), penyaringan boolean (*boolean masking*), dan pengindeksan cerdas (*fancy indexing*).
  * Menyelesaikan sistem persamaan linier simultan ($A \mathbf{x} = \mathbf{b}$) untuk formulasi optimasi nutrisi pupuk menggunakan modul `numpy.linalg`.
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
- Integrasi sistem inferensi real-time berbasis NumPy untuk Komputasi Numerik.
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
