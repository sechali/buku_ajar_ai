---
marp: true
theme: default
paginate: true
header: "Bagian 2: Logika Komputasi dan Pemrograman Dasar • AI Modul 2.2"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 2.2: Flowchart dan Pseudocode
### Bagian 2: Logika Komputasi dan Pemrograman Dasar
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Mengidentifikasi (C2) standar simbol grafis diagram alir ANSI/ISO dan konvensi penulisan pseudocode terstruktur.
- Menganalisis (C4) alur proses fisik sortasi TBS dan sistem interlock keselamatan pabrik kelapa sawit ke dalam representasi logika grafis.
- Merancang (C3) diagram alir (flowchart) dan teks pseudocode sistem kendali otomasi agro-industri yang bebas ambiguitas.
- Mentransformasikan (C3) rancangan diagram alir dan pseudocode menjadi kode program Python yang siap dieksekusi.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Flowchart dan Pseudocode.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\theta_{\text{high}} = 0.85, \quad \theta_{\text{low}} = 0.50$$

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
1. **Mengidentifikasi (C2)** standar simbol grafis diagram alir ANSI/ISO dan konvensi penulisan *pseudocode* terstruktur.
2. **Menganalisis (C4)** alur proses fisik sortasi TBS dan sistem interlock keselamatan pabrik kelapa sawit ke dalam representasi logika grafis.
3. **Merancang (C3)** diagram alir (*flowchart*) dan teks *pseudocode* sistem kendali otomasi agro-industri yang bebas ambiguitas.
4. **Mentransformasikan (C3)** rancangan diagram alir dan pseudocode menjadi kode program Python yang siap dieksekusi.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * **Dokumen Spesifikasi Diagram Alir ANSI/ISO 5807**: Penguasaan perancangan alur pemrosesan cerdas berstandar internasional yang mencakup penggunaan presisi 8 simbol utama (*Terminator*, *Process*, *Decision*, *Input/Output*, *Preparation*, *Connector On-Page*, *Predefined Process*, dan *Off-Page Connector*).
  * **Dokumen Pseudocode Formal Terstruktur**: Spesifikasi tekstual independen bahasa menggunakan konvensi akademik baku (kata kunci kapital `START`, `INPUT`, `COMPUTE`, `IF-THEN-ELSE`, `WHILE-DO`, `END`), indentasi hierarkis 4 spasi, deklarasi tipe data terstruktur, dan penamaan variabel deskriptif.
  * **Matriks Tabel Jejak (*Dry-Run Trace Table Engine*)**: Lembar audit pengujian kering langkah-demi-langkah yang memetakan mutasi status variabel, evaluasi predikat kondisional (*Boolean branch*), serta pembuktian mekanisme *short-circuit evaluation* pada data uji heterogen.
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
  * **Kompetensi Perancangan Cetak Biru Logika (*Algorithmic Blueprinting*)**: Mahasiswa mampu memvisualisasikan masalah agronomis kompleks (seperti sortasi tandan buah segar dan penanganan sensor anomali) ke dalam skema diagramatik yang rapi dan terverifikasi sebelum menulis satu baris pun kode sintaks bahasa pemrograman.
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
- Integrasi sistem inferensi real-time berbasis Flowchart dan Pseudocode.
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
