---
marp: true
theme: default
paginate: true
header: "Bagian 7: Machine Learning - Konsep dan Algoritma Klasik • AI Modul 7.10"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 7.10: Gradient Boosting
### Bagian 7: Machine Learning - Konsep dan Algoritma Klasik
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Memahami (C2) prinsip dasar pembelajaran ansambel terarah (sequential boosting), konsep penurunan gradien dalam ruang fungsi (gradient descent in function space), formulasi matematis pseudo-residuals, mekanisme penyusutan (shrinkage / learning rate), serta dekomposisi Hessian tingkat dua pada XGBoost.
- Menerapkan (C3) pustaka Scikit-Learn (`GradientBoostingRegressor` dan `GradientBoostingClassifier`) untuk memodelkan peramalan tonase panen Tandan Buah Segar (TBS) bulanan dan mengklasifikasikan risiko anomali rendemen pabrik kelapa sawit.
- Menganalisis (C4) interaksi dinamis antara parameter laju pembelajaran (\eta) dan jumlah pohon (M), mendiagnosis kurva galat latih vs uji untuk mitigasi overfitting, serta membandingkan karakteristik keunggulan arsitektural antara Bagging (Random Forest) versus Boosting (Gradient Boosting).

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Gradient Boosting.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$F_M(\mathbf{x}) = F_0(\mathbf{x}) + \sum_{m=1}^M \eta h_m(\mathbf{x})$$

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
Setelah menyelesaikan modul pamungkas Part 7 ini secara komprehensif, mahasiswa diharapkan mampu:
1. **Memahami (C2)** prinsip dasar pembelajaran ansambel terarah (*sequential boosting*), konsep penurunan gradien dalam ruang fungsi (*gradient descent in function space*), formulasi matematis *pseudo-residuals*, mekanisme penyusutan (*shrinkage / learning rate*), serta dekomposisi Hessian tingkat dua pada XGBoost.
2. **Menerapkan (C3)** pustaka Scikit-Learn (`GradientBoostingRegressor` dan `GradientBoostingClassifier`) untuk memodelkan peramalan tonase panen Tandan Buah Segar (TBS) bulanan dan mengklasifikasikan risiko anomali rendemen pabrik kelapa sawit.
3. **Menganalisis (C4)** interaksi dinamis antara parameter laju pembelajaran ($\eta$) dan jumlah pohon ($M$), mendiagnosis kurva galat latih vs uji untuk mitigasi *overfitting*, serta membandingkan karakteristik keunggulan arsitektural antara *Bagging* (Random Forest) versus *Boosting* (Gradient Boosting).

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan analitik fungsi objektif penurunan gradien $\min_F \sum L(y_i, F(\mathbf{x}_i))$, turunan parsial *pseudo-residuals* $r_{im} = -\left[\frac{\partial L}{\partial F}\right]$, formula pembaruan model $F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta h_m(\mathbf{x})$, dan penalti kompleksitas daun XGBoost $\Omega(f)$.
  * Skrip Python berstandar PEP 8 untuk pipeline Gradient Boosting teroptimasi, penentuan *early stopping*, serta ekstraksi peringkat *feature importance gain*.
  * Laporan komparasi metrik kinerja (RMSE, MAE, R²) antara Regresi Linier, Random Forest, dan Gradient Boosting pada dataset produksi perkebunan.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian merancang model prediktif kelas dunia dengan akurasi *state-of-the-art* yang mampu menangkap interaksi variabel agronomi dan iklim non-linier yang rumit.
  * Kemampuan mengoptimalkan penjadwalan pemupukan dan logistik armada truk pengangkut TBS berbasis peramalan panen mingguan yang sangat presisi.
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
- Integrasi sistem inferensi real-time berbasis Gradient Boosting.
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
