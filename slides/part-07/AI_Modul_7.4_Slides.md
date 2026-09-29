---
marp: true
theme: default
paginate: true
header: "Bagian 7: Machine Learning - Konsep dan Algoritma Klasik • AI Modul 7.4"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 7.4: Decision Tree
### Bagian 7: Machine Learning - Konsep dan Algoritma Klasik
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Memahami (C2) prinsip matematis pembentukan pohon keputusan (decision tree), konsep ketidakmurnian simpul (node impurity) melalui Entropi Informasi Shannon dan Indeks Ketidakmurnian Gini, serta kriteria perolehan informasi (Information Gain).
- Menerapkan (C3) algoritma Classification and Regression Trees (CART) menggunakan pustaka Scikit-Learn untuk membangun sistem sortasi fraksi kematangan Tandan Buah Segar (TBS) kelapa sawit dan mengekstrak aturan logika eksplisit (If-Then Rules).
- Menganalisis (C4) fenomena overfitting pada pohon yang tumbuh tanpa batas, menerapkan teknik pemangkasan (pre-pruning dan cost-complexity post-pruning), serta mengevaluasi trade-off antara keterpahaman model (explainability) dan akurasi prediksi.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Decision Tree.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$p_c = \frac{1}{|D|} \sum_{i \in D} \mathbb{I}(y_i = c)$$

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
1. **Memahami (C2)** prinsip matematis pembentukan pohon keputusan (*decision tree*), konsep ketidakmurnian simpul (*node impurity*) melalui Entropi Informasi Shannon dan Indeks Ketidakmurnian Gini, serta kriteria perolehan informasi (*Information Gain*).
2. **Menerapkan (C3)** algoritma Classification and Regression Trees (CART) menggunakan pustaka Scikit-Learn untuk membangun sistem sortasi fraksi kematangan Tandan Buah Segar (TBS) kelapa sawit dan mengekstrak aturan logika eksplisit (*If-Then Rules*).
3. **Menganalisis (C4)** fenomena *overfitting* pada pohon yang tumbuh tanpa batas, menerapkan teknik pemangkasan (*pre-pruning* dan *cost-complexity post-pruning*), serta mengevaluasi trade-off antara keterpahaman model (*explainability*) dan akurasi prediksi.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan formulasi analitik Entropi Shannon, Ketidakmurnian Gini, Information Gain, dan fungsi penalti kompleksitas biaya $R_\alpha(T)$.
  * Skrip Python berstandar PEP 8 untuk konstruksi pohon keputusan, optimasi kedalaman pohon, dan visualisasi grafis diagram alir simpul keputusan.
  * Dokumen daftar aturan logika kondisional (*business rule set*) yang siap diintegrasikan pada sistem timbangan dan sortasi pabrik.
* **Outcomes (Kompetensi Aplikatif)**:
  * Kemampuan merancang model kecerdasan buatan transparan (*White-Box AI*) yang dapat diaudit, diverifikasi, dan diterima langsung oleh mandor panen dan manajemen pabrik kelapa sawit.
  * Keahlian dalam mendiagnosis kedalaman pohon optimal guna mencegah memorisasi derau data lapangan.
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
- Integrasi sistem inferensi real-time berbasis Decision Tree.
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
