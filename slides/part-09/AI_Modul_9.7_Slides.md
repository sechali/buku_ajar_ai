---
marp: true
theme: default
paginate: true
header: "Bagian 9: Fondasi Deep Learning dan Arsitektur Jaringan Saraf Tiruan • AI Modul 9.7"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 9.7: Training Neural Network
### Bagian 9: Fondasi Deep Learning dan Arsitektur Jaringan Saraf Tiruan
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Menguraikan (C2) prinsip kerja dan keterbatasan mendasar algoritma Batch Gradient Descent, Stochastic Gradient Descent (SGD), dan Mini-Batch GD dalam mengarungi lanskap fungsi rugi non-konveks berdimensi tinggi.
- Menerapkan (C3) formulasi matematika algoritma Momentum, RMSprop, dan Adam (Adaptive Moment Estimation) lengkap dengan perhitungan koreksi bias analitik untuk mempercepat konvergensi model AI perkebunan presisi.
- Menganalisis (C4) perbandingan trajektori optimasi pada permukaan jurang sempit (ravine landscapes), mengevaluasi dinamika peluruhan laju pembelajaran (Learning Rate Schedules seperti Cosine Annealing), serta mendiagnosis anomali divergensi pelatihan akibat hiperparameter yang tidak terkalibrasi.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Training Neural Network.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \Delta \boldsymbol{\theta}_t$$

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
Setelah menuntaskan modul ini, mahasiswa dan pembelajar diharapkan mampu:
1. **Menguraikan (C2)** prinsip kerja dan keterbatasan mendasar algoritma *Batch Gradient Descent*, *Stochastic Gradient Descent* (SGD), dan *Mini-Batch GD* dalam mengarungi lanskap fungsi rugi non-konveks berdimensi tinggi.
2. **Menerapkan (C3)** formulasi matematika algoritma *Momentum*, *RMSprop*, dan *Adam* (*Adaptive Moment Estimation*) lengkap dengan perhitungan koreksi bias analitik untuk mempercepat konvergensi model AI perkebunan presisi.
3. **Menganalisis (C4)** perbandingan trajektori optimasi pada permukaan jurang sempit (*ravine landscapes*), mengevaluasi dinamika peluruhan laju pembelajaran (*Learning Rate Schedules* seperti *Cosine Annealing*), serta mendiagnosis anomali divergensi pelatihan akibat hiperparameter yang tidak terkalibrasi.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Berkas kode program Python mandiri yang mengimplementasikan empat kelas optimizer (`SGD`, `Momentum`, `RMSprop`, `Adam`) murni dari nol dengan NumPy.
  * Grafik visualisasi perbandingan lintasan optimasi 2D pada permukaan fungsi uji non-konveks yang memperlihatkan eliminasi osilasi zig-zag.
  * Laporan perbandingan laju penurunan kerugian dan efisiensi waktu pelatihan pada model peramalan defisit air tanah multi-blok.
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
  * Mahasiswa terampil memilih optimizer yang paling tepat berdasarkan ukuran dataset, arsitektur jaringan, dan karakteristik derau data pertanian.
  * Mahasiswa memahami secara mendalam peran momen pertama (kecepatan gerak) dan momen kedua (redaman varians adaptif) pada algoritma Adam.
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
- Integrasi sistem inferensi real-time berbasis Training Neural Network.
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
