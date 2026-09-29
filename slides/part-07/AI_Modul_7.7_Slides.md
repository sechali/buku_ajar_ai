---
marp: true
theme: default
paginate: true
header: "Bagian 7: Machine Learning - Konsep dan Algoritma Klasik • AI Modul 7.7"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 7.7: Support Vector Machine (SVM)
### Bagian 7: Machine Learning - Konsep dan Algoritma Klasik
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Memahami (C2) prinsip geometris hiperbidang pemisah (separating hyperplane), penurunan analitik lebar margin maksimal M = 2/\|\mathbf{w}\|, formulasi optimasi kuadratik konveks hard/soft margin, kondisi Karush-Kuhn-Tucker (KKT), serta fungsi pemetaan non-linier melalui Teorema Mercer (Kernel Trick).
- Menerapkan (C3) pustaka Scikit-Learn (`SVC`) yang diintegrasikan dalam pipeline baku (`StandardScaler`) untuk memproses sinyal reflektansi spektroskopi inframerah dekat (Near-Infrared / NIR) guna mengklasifikasikan kemurnian minyak kelapa sawit mentah (Crude Palm Oil / CPO).
- Menganalisis (C4) interaksi hyperparameter penalti kesalahan C dan lebar jangkauan kernel gamma (\gamma), mendiagnosis pergeseran vektor pendukung (support vectors), serta mengevaluasi trade-off antara kekakuan batas keputusan dan kemampuan generalisasi data lapangan.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Support Vector Machine (SVM).
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\mathbf{w}^T \mathbf{x} + b = 0$$

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
1. **Memahami (C2)** prinsip geometris hiperbidang pemisah (*separating hyperplane*), penurunan analitik lebar margin maksimal $M = 2/\|\mathbf{w}\|$, formulasi optimasi kuadratik konveks *hard/soft margin*, kondisi Karush-Kuhn-Tucker (KKT), serta fungsi pemetaan non-linier melalui Teorema Mercer (*Kernel Trick*).
2. **Menerapkan (C3)** pustaka Scikit-Learn (`SVC`) yang diintegrasikan dalam *pipeline* baku (`StandardScaler`) untuk memproses sinyal reflektansi spektroskopi inframerah dekat (*Near-Infrared / NIR*) guna mengklasifikasikan kemurnian minyak kelapa sawit mentah (*Crude Palm Oil* / CPO).
3. **Menganalisis (C4)** interaksi hyperparameter penalti kesalahan $C$ dan lebar jangkauan kernel gamma ($\gamma$), mendiagnosis pergeseran vektor pendukung (*support vectors*), serta mengevaluasi trade-off antara kekakuan batas keputusan dan kemampuan generalisasi data lapangan.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Pemahaman mendalam mengenai formulasi Lagrangian Primal dan Dual SVM, kondisi komplementer KKT, fungsi kernel RBF $K(\mathbf{x}_i, \mathbf{x}_j) = \exp(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|^2)$, dan mekanisme variabel kelonggaran $\xi_i$.
  * Skrip Python berstandar PEP 8 untuk konstruksi model SVM berkinerja tinggi, visualisasi kontur batas keputusan 2D, dan ekstraksi vektor pendukung kritis.
  * Laporan komparasi kinerja klasifikasi antara Kernel Linier, Polinomial, dan RBF pada data agro-industri kompleks berdimensi tinggi.
* **Outcomes (Kompetensi Aplikatif)**:
  * Kemampuan membangun sistem autentikasi mutu komoditas perkebunan berskala industri yang kebal terhadap kendala optimum lokal (*free from local minima*).
  * Keahlian dalam memproses data instrumen analitik modern (seperti kromatografi gas, spektrometer NIR, atau citra hiperspektral) yang memiliki jumlah variabel jauh lebih banyak daripada jumlah sampel ($p \gg N$).
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
- Integrasi sistem inferensi real-time berbasis Support Vector Machine (SVM).
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
