---
marp: true
theme: default
paginate: true
header: "Bagian 7: Machine Learning - Konsep dan Algoritma Klasik • AI Modul 7.5"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 7.5: Random Forest
### Bagian 7: Machine Learning - Konsep dan Algoritma Klasik
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Memahami (C2) prinsip dasar pembelajaran ansambel (ensemble learning), teorema agregasi bagging (Bootstrap Aggregating), konsep limit matematis sampel out-of-bag (OOB), serta mekanisme pengacakan fitur (random subspace method).
- Menerapkan (C3) pustaka Scikit-Learn (`RandomForestClassifier` dan `RandomForestRegressor`) untuk memodelkan klasifikasi mutu Tandan Buah Segar (TBS) dan memprediksi rendemen ekstraksi minyak kelapa sawit (Oil Extraction Rate / OER) dengan validasi internal OOB.
- Menganalisis (C4) signifikansi kontribusi variabel agronomi melalui Mean Decrease in Impurity (MDI) dan Permutation Importance, mendiagnosis konvergensi jumlah estimator, serta mengevaluasi trade-off antara reduksi varians dan latensi komputasi inferensi di lapangan.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Random Forest.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$P_{\text{ansambel}} = \sum_{k=\lfloor B/2 \rfloor + 1}^{B} \binom{B}{k} p^k (1 - p)^{B - k}$$

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
1. **Memahami (C2)** prinsip dasar pembelajaran ansambel (*ensemble learning*), teorema agregasi *bagging* (Bootstrap Aggregating), konsep limit matematis sampel *out-of-bag* (OOB), serta mekanisme pengacakan fitur (*random subspace method*).
2. **Menerapkan (C3)** pustaka Scikit-Learn (`RandomForestClassifier` dan `RandomForestRegressor`) untuk memodelkan klasifikasi mutu Tandan Buah Segar (TBS) dan memprediksi rendemen ekstraksi minyak kelapa sawit (*Oil Extraction Rate* / OER) dengan validasi internal OOB.
3. **Menganalisis (C4)** signifikansi kontribusi variabel agronomi melalui *Mean Decrease in Impurity* (MDI) dan *Permutation Importance*, mendiagnosis konvergensi jumlah estimator, serta mengevaluasi trade-off antara reduksi varians dan latensi komputasi inferensi di lapangan.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Pemahaman mendalam mengenai formulasi analitik Teorema Juri Condorcet, reduksi varians model agregat $\text{Var}(\bar{X}) = \rho \sigma^2 + \frac{1-\rho}{B}\sigma^2$, pembuktian limit $1/e \approx 36.8\%$, dan metrik MDI.
  * Skrip Python berstandar PEP 8 untuk konstruksi model Random Forest teroptimasi, komputasi evaluasi OOB, serta visualisasi grafik *feature importance*.
  * Laporan komparasi stabilitas dan akurasi antara pohon tunggal (*Decision Tree*) versus hutan acak (*Random Forest*).
* **Outcomes (Kompetensi Aplikatif)**:
  * Kemampuan membangun model prediktif perkebunan berkinerja tinggi yang tangguh terhadap derau sensor (*noise-tolerant*) tanpa memerlukan proses pemangkasan manual yang melelahkan.
  * Keahlian dalam memanfaatkan validasi internal OOB untuk menghemat siklus komputasi validasi silang pada dataset agro-industri berukuran masif.
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
- Integrasi sistem inferensi real-time berbasis Random Forest.
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
