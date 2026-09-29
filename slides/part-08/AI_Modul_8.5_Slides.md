---
marp: true
theme: default
paginate: true
header: "Bagian 8: Unsupervised Learning dan Reduksi Dimensi • AI Modul 8.5"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 8.5: Pembuatan Sistem Prediksi Sederhana
### Bagian 8: Unsupervised Learning dan Reduksi Dimensi
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Sub-CPMK 8.5.1 (C2): Menguraikan arsitektur serialisasi model portabel (TorchScript JIT dan ONNX Runtime), membedakan mekanisme penelusuran graf (tracing) vs penulisan skrip (scripting), serta merumuskan alur kerja modular enkapsulasi sistem inferensi.
- Sub-CPMK 8.5.2 (C3): Membangun kelas mesin inferensi terpadu (Inference Engine) yang mengotomatisasi validasi batas fisik data sensor lapangan, penyesuaian standarisasi parameter terbekukan, eksekusi model terkompilasi berkecepatan tinggi, dan pasca-pemrosesan kategori mutu panen.
- Sub-CPMK 8.5.3 (C4): Merancang prototipe antarmuka sistem prediksi cerdas interaktif (berbasis CLI dan web GUI) yang siap dioperasikan di stasiun sortasi pabrik kelapa sawit, serta mengevaluasi disparitas latensi komputasi antara PyTorch Eager, TorchScript, dan ONNX.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Pembuatan Sistem Prediksi Sederhana.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\hat{y} = g_{\text{post}}\Big( f_{\text{JIT}}\big( \phi_{\text{scale}}(\mathbf{x}_{\text{raw}}; \boldsymbol{\mu}_{\text{train}}, \boldsymbol{\sigma}_{\text{train}}) \big) \Big)$$

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
Setelah menyelesaikan modul pembelajaran ini secara tuntas, mahasiswa diharapkan memiliki kapabilitas untuk:
1. **Sub-CPMK 8.5.1 (C2):** Menguraikan arsitektur serialisasi model portabel (*TorchScript JIT* dan *ONNX Runtime*), membedakan mekanisme penelusuran graf (*tracing*) vs penulisan skrip (*scripting*), serta merumuskan alur kerja modular enkapsulasi sistem inferensi.
2. **Sub-CPMK 8.5.2 (C3):** Membangun kelas mesin inferensi terpadu (*Inference Engine*) yang mengotomatisasi validasi batas fisik data sensor lapangan, penyesuaian standarisasi parameter terbekukan, eksekusi model terkompilasi berkecepatan tinggi, dan pasca-pemrosesan kategori mutu panen.
3. **Sub-CPMK 8.5.3 (C4):** Merancang prototipe antarmuka sistem prediksi cerdas interaktif (berbasis CLI dan web GUI) yang siap dioperasikan di stasiun sortasi pabrik kelapa sawit, serta mengevaluasi disparitas latensi komputasi antara PyTorch Eager, TorchScript, dan ONNX.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
- **Luaran Langsung (*Outputs*):** Artefak model terkompilasi `oilpalm_predictor_jit.pt`, skrip mesin inferensi mandiri, serta prototipe antarmuka interaktif prediksi rendemen panen perkebunan yang tervalidasi.
- **Dampak Pembelajaran (*Outcomes*):** Mahasiswa memiliki kapabilitas rekayasa perangkat lunak terapan dalam mentransformasikan model riset laboratorium menjadi produk teknologi kecerdasan buatan operasional (*production-ready AI*).
- **Implikasi Jangka Panjang (*Impacts*):** Terciptanya sistem automasi sortasi dan grading komoditas perkebunan presisi yang dapat langsung dimanfaatkan oleh industri kelapa sawit, kehutanan, dan pertanian rakyat guna mendongkrak efisiensi hilirisasi agrokompleks nasional.

---

## 2. Profil Fundamental Pembuatan Sistem Prediksi Sederhana: Fungsi, Manfaat, dan Keunggulan-Kelemahan
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
- Integrasi sistem inferensi real-time berbasis Pembuatan Sistem Prediksi Sederhana.
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
