---
marp: true
theme: default
paginate: true
header: "Bagian 10: Pelatihan, Optimasi, dan Regularisasi Deep Learning • AI Modul 10.2"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 10.2: Representasi Citra Digital dan Matriks Piksel
### Bagian 10: Pelatihan, Optimasi, dan Regularisasi Deep Learning
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Memahami (C2) prinsip diskritisasi spasial (sampling) dan diskritisasi intensitas (quantization), konsep kedalaman bit (bit depth, 1\text{-bit}, 8\text{-bit}, 16\text{-bit}, 32\text{-bit float}), struktur memori array kontigu (row-major layout), serta perbedaan representasi monokromatik (Grayscale) vs polikromatik (RGB, BGR, dan Multispektral).
- Menerapkan (C3) operasi manipulasi matriks piksel murni berbasis pustaka NumPy dan OpenCV—mencakup pengindeksan koordinat (y, x), pemotongan wilayah minat (Region of Interest / ROI slicing), aritmatika citra bersaturasi vs modulo, serta penyesuaian kontras-kecerahan linier dan non-linier (Gamma Correction)—pada citra kanopi dan buah kelapa sawit.
- Menganalisis (C4) patologi kuantisasi (false contouring), distorsi pereduksian resolusi (spatial aliasing), bahaya aritmatika integer overflow/underflow pada tipe data `uint8`, serta mengestimasi kebutuhan kapasitas memori RAM/VRAM untuk pemrosesan citra drone resolusi tinggi di lapangan perkebunan.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Representasi Citra Digital dan Matriks Piksel.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$f_s \ge 2 f_{\max}$$

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
Setelah menyelesaikan modul ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** prinsip diskritisasi spasial (*sampling*) dan diskritisasi intensitas (*quantization*), konsep kedalaman bit (*bit depth*, $1\text{-bit}$, $8\text{-bit}$, $16\text{-bit}$, $32\text{-bit float}$), struktur memori array kontigu (*row-major layout*), serta perbedaan representasi monokromatik (Grayscale) vs polikromatik (RGB, BGR, dan Multispektral).
2. **Menerapkan (C3)** operasi manipulasi matriks piksel murni berbasis pustaka NumPy dan OpenCV—mencakup pengindeksan koordinat $(y, x)$, pemotongan wilayah minat (*Region of Interest / ROI slicing*), aritmatika citra bersaturasi vs modulo, serta penyesuaian kontras-kecerahan linier dan non-linier (*Gamma Correction*)—pada citra kanopi dan buah kelapa sawit.
3. **Menganalisis (C4)** patologi kuantisasi (*false contouring*), distorsi pereduksian resolusi (*spatial aliasing*), bahaya aritmatika *integer overflow/underflow* pada tipe data `uint8`, serta mengestimasi kebutuhan kapasitas memori RAM/VRAM untuk pemrosesan citra drone resolusi tinggi di lapangan perkebunan.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Pemahaman mendalam mengenai struktur data array piksel multidimensi dalam arsitektur komputer modern.
  * Skrip Python berstandar PEP 8 untuk manipulasi piksel, pemotongan ROI brondolan kelapa sawit, dan algoritma koreksi gamma adaptif.
  * Laporan komparasi kuantitatif konsumsi memori dan histogram intensitas citra pada variasi kedalaman bit ($8\text{-bit}$ vs $16\text{-bit}$).
* **Outcomes (Kompetensi Aplikatif)**:
  * Kemampuan mengelola representasi citra digital secara efisien tanpa membebani memori kerja sistem komputer tepi (*edge computing device*).
  * Keahlian dalam mengisolasi wilayah objek tanaman penting dan memperbaiki kualitas citra yang mengalami *underexposure* pada bayangan kanopi kelapa sawit.
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
- Integrasi sistem inferensi real-time berbasis Representasi Citra Digital dan Matriks Piksel.
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
