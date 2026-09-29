---
marp: true
theme: default
paginate: true
header: "Bagian 5: Matematika dan Sains Data untuk AI • AI Modul 5.5"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 5.5: Overfitting dan Underfitting dalam Machine Learning
### Bagian 5: Matematika dan Sains Data untuk AI
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Mendekonstruksi (C4) dekomposisi bias-varians (Bias-Variance Trade-off) dan membuktikan pengaruh kapasitas model terhadap galat generalisasi.
- Mendiagnosis (C4) gejala Underfitting (bias tinggi) dan Overfitting (varians tinggi) melalui analisis visual kurva pembelajaran (Learning Curves).
- Menerapkan (C3) teknik mitigasi overfitting: penambahan data (Data Augmentation), penyederhanaan model, dan metode penghentian dini (Early Stopping).
- Mengevaluasi (C4) penerapan teknik regularisasi parameter (L_1 Lasso dan L_2 Ridge) untuk membatasi kompleksitas bobot model.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Overfitting dan Underfitting dalam Machine Learning.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$y = f(\mathbf{x}) + \epsilon, \quad \mathbb{E}[\epsilon] = 0, \quad \text{Var}(\epsilon) = \sigma^2$$

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
1. **Mendekonstruksi (C4)** dekomposisi bias-varians (*Bias-Variance Trade-off*) dan membuktikan pengaruh kapasitas model terhadap galat generalisasi.
2. **Mendiagnosis (C4)** gejala *Underfitting* (bias tinggi) dan *Overfitting* (varians tinggi) melalui analisis visual kurva pembelajaran (*Learning Curves*).
3. **Menerapkan (C3)** teknik mitigasi overfitting: penambahan data (*Data Augmentation*), penyederhanaan model, dan metode penghentian dini (*Early Stopping*).
4. **Mengevaluasi (C4)** penerapan teknik regularisasi parameter ($L_1$ Lasso dan $L_2$ Ridge) untuk membatasi kompleksitas bobot model.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Menurunkan secara matematis dekomposisi galat generalisasi menjadi komponen bias kuadrat, variansi, dan derau tak tereduksi (*irreducible error*).
  * Mengidentifikasi karakteristik empiris dari kondisi *underfitting* (bias tinggi) dan *overfitting* (variansi tinggi) pada data pelatihan versus data validasi.
  * Mengonstruksi dan menafsirkan grafik kurva pembelajaran (*learning curves*) terhadap variasi ukuran sampel data dan kapasitas model.
  * Menerapkan teknik mitigasi matematis meliputi penalti regularisasi $\ell_1$ (Lasso), $\ell_2$ (Ridge), *Elastic Net*, serta pemangkasan pohon (*cost-complexity pruning*).
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
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
- Integrasi sistem inferensi real-time berbasis Overfitting dan Underfitting dalam Machine Learning.
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
