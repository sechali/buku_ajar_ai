---
marp: true
theme: default
paginate: true
header: "Bagian 1: Pengantar Kecerdasan Buatan & Paradigma AI • AI Modul 1.2"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 1.2: Sejarah dan Perkembangan Artificial Intelligence
### Bagian 1: Pengantar Kecerdasan Buatan & Paradigma AI
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Menguraikan (C2) periodisasi kronologis sejarah perkembangan AI dari era embrio (1943) hingga era Foundation Models dan Generative AI modern.
- Menganalisis (C4) faktor teknologi, ekonomi, dan batasan teoretis yang memicu terjadinya dua kali periode pembekuan riset (First AI Winter 1974–1980 dan Second AI Winter 1987–1993).
- Membuktikan secara matematis dan geometris (C4) keterbatasan pemisahan linier pada model Perceptron Rosenblatt (1958) untuk gerbang logika XOR yang dirumuskan oleh Minsky & Papert (1969).
- Mengimplementasikan (C3) algoritma pelatihan Perceptron klasik dari nol menggunakan bahasa Python dengan dokumentasi komentar per baris yang komprehensif.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Sejarah dan Perkembangan Artificial Intelligence.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$z = \sum_{i=1}^{n} w_i x_i + b = \mathbf{w}^T \mathbf{x} + b$$

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
1. **Menguraikan (C2)** periodisasi kronologis sejarah perkembangan AI dari era embrio (1943) hingga era *Foundation Models* dan *Generative AI* modern.
2. **Menganalisis (C4)** faktor teknologi, ekonomi, dan batasan teoretis yang memicu terjadinya dua kali periode pembekuan riset (*First AI Winter* 1974–1980 dan *Second AI Winter* 1987–1993).
3. **Membuktikan secara matematis dan geometris (C4)** keterbatasan pemisahan linier pada model Perceptron Rosenblatt (1958) untuk gerbang logika XOR yang dirumuskan oleh Minsky & Papert (1969).
4. **Mengimplementasikan (C3)** algoritma pelatihan Perceptron klasik dari nol menggunakan bahasa Python dengan dokumentasi komentar per baris yang komprehensif.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Dokumen pembuktian aljabar matematis mengenai ketidakmungkinan fungsi linier memisahkan problem non-linier XOR.
  * Berkas kode program Python mandiri yang mereplikasi model *Rosenblatt Perceptron* klasik lengkap dengan visualisasi batas keputusan (*decision boundary*).
  * Laporan komparasi konvergensi pelatihan Perceptron pada gerbang AND (berhasil dalam beberapa iterasi) vs gerbang XOR (osilasi tanpa batas / gagal konvergen).
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
  * Mahasiswa memiliki perspektif kritis terhadap kurva sensasi (*hype curve*) teknologi AI sehingga mampu membedakan antara ekspektasi yang realistis dengan janji berlebihan (*overpromising*).
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
- Integrasi sistem inferensi real-time berbasis Sejarah dan Perkembangan Artificial Intelligence.
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
