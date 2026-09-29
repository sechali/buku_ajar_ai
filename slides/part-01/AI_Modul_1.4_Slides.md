---
marp: true
theme: default
paginate: true
header: "Bagian 1: Pengantar Kecerdasan Buatan & Paradigma AI • AI Modul 1.4"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 1.4: Jenis AI (ANI, AGI, ASI)
### Bagian 1: Pengantar Kecerdasan Buatan & Paradigma AI
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Menguraikan (C2) klasifikasi tiga tingkat kapabilitas kecerdasan buatan: Artificial Narrow Intelligence (ANI), Artificial General Intelligence (AGI), dan Artificial Superintelligence (ASI).
- Menganalisis secara kritis (C4) posisi teknologi mutakhir saat ini (Large Language Models dan model multimodal) dalam kontinum transisi menuju AGI.
- Mengevaluasi (C4) keterbatasan mendasar arsitektur ANI, khususnya fenomena lupa katastrofik (Catastrophic Forgetting) dan dilema stabilitas-plastisitas (Stability-Plasticity Dilemma).
- Menghitung dan menginterpretasikan (C3) metrik efisiensi kecerdasan konseptual François Chollet (\Upsilon) serta mengimplementasikan simulasi transfer adaptif multi-tugas sederhana dalam Python.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Jenis AI (ANI, AGI, ASI).
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\text{Model}_{t+1} = \text{Optimize}(\text{Model}_t)$$

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
1. **Menguraikan (C2)** klasifikasi tiga tingkat kapabilitas kecerdasan buatan: *Artificial Narrow Intelligence* (ANI), *Artificial General Intelligence* (AGI), dan *Artificial Superintelligence* (ASI).
2. **Menganalisis secara kritis (C4)** posisi teknologi mutakhir saat ini (*Large Language Models* dan model multimodal) dalam kontinum transisi menuju AGI.
3. **Mengevaluasi (C4)** keterbatasan mendasar arsitektur ANI, khususnya fenomena lupa katastrofik (*Catastrophic Forgetting*) dan dilema stabilitas-plastisitas (*Stability-Plasticity Dilemma*).
4. **Menghitung dan menginterpretasikan (C3)** metrik efisiensi kecerdasan konseptual François Chollet ($\Upsilon$) serta mengimplementasikan simulasi transfer adaptif multi-tugas sederhana dalam Python.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Diagram pemetaan spektrum kapabilitas AI beserta tabel matriks komparasi 6 parameter penentu antara ANI, AGI, dan ASI.
  * Berkas kode program Python mandiri yang mendemonstrasikan fenomena *Catastrophic Forgetting* pada jaringan syaraf dan teknik proteksi retensi bobot (*Elastic Weight Consolidation / Feature Preserving*).
  * Laporan analisis evaluasi kritis uji kelayakan AGI (seperti *ARC Benchmark* dan *Wozniak Coffee Test*).
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
  * Mahasiswa tidak mudah terjebak oleh sensasi (*hype*) industri: mampu membedakan sistem yang sekadar memiliki bank memori masif (*Broad Narrow AI*) dengan sistem yang benar-benar memiliki penalaran kausal umum (*General Intelligence*).
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
- Integrasi sistem inferensi real-time berbasis Jenis AI (ANI, AGI, ASI).
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
