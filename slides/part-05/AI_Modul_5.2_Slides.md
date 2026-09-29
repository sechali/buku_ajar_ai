---
marp: true
theme: default
paginate: true
header: "Bagian 5: Matematika dan Sains Data untuk AI • AI Modul 5.2"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 5.2: Jenis Machine Learning (Supervised, Unsupervised, Reinforcement Learning)
### Bagian 5: Matematika dan Sains Data untuk AI
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Mengklasifikasikan (C2) tiga paradigma utama machine learning: Supervised Learning, Unsupervised Learning, dan Reinforcement Learning (RL) serta varian semi-supervised.
- Menganalisis (C4) perbedaan karakteristik data masukan (label diskret, target kontinu, ketiadaan label, dan sinyal reward) pada rantai agro-industri.
- Mengevaluasi (C4) trade-off antara eksplorasi dan eksploitasi (Exploration-Exploitation Dilemma) pada agen RL kendali penyiraman cerdas.
- Menentukan (C3) paradigma machine learning yang paling tepat dan efisien untuk menyelesaikan permasalahan spesifik di pabrik kelapa sawit dan lahan kebun.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Jenis Machine Learning (Supervised, Unsupervised, Reinforcement Learning).
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\mathcal{D}_{\text{train}} = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \dots, (\mathbf{x}_n, y_n)\}$$

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
1. **Mengklasifikasikan (C2)** tiga paradigma utama machine learning: *Supervised Learning*, *Unsupervised Learning*, dan *Reinforcement Learning* (RL) serta varian semi-supervised.
2. **Menganalisis (C4)** perbedaan karakteristik data masukan (label diskret, target kontinu, ketiadaan label, dan sinyal *reward*) pada rantai agro-industri.
3. **Mengevaluasi (C4)** trade-off antara eksplorasi dan eksploitasi (*Exploration-Exploitation Dilemma*) pada agen RL kendali penyiraman cerdas.
4. **Menentukan (C3)** paradigma machine learning yang paling tepat dan efisien untuk menyelesaikan permasalahan spesifik di pabrik kelapa sawit dan lahan kebun.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Membedakan karakteristik matematis, bentuk masukan (*inputs*), bentuk keluaran (*outputs*), dan sinyal umpan balik (*feedback signal*) dari tiga pilar machine learning: *Supervised*, *Unsupervised*, dan *Reinforcement Learning*.
  * Memformulasikan persoalan **Supervised Learning** ke dalam sub-domain Regresi ($y \in \mathbb{R}$) dan Klasifikasi ($y \in \{1, \dots, C\}$) beserta fungsi objektif optimasinya (*Mean Squared Error* dan *Cross-Entropy*).
  * Menguraikan mekanisme **Unsupervised Learning** dalam menemukan struktur intrinsik $p(\mathbf{x})$, meliputi klastering (*clustering*), reduksi dimensi (*dimensionality reduction*), dan deteksi anomali (*anomaly detection*).
  * Menjelaskan komponen formal **Reinforcement Learning** berbasis kerangka *Markov Decision Process* (MDP): himpunan status ($\mathcal{S}$), aksi ($\mathcal{A}$), probabilitas transisi ($\mathcal{P}$), fungsi imbalan ($\mathcal{R}$), faktor diskon ($\gamma$), kebijakan ($\pi$), serta Persamaan Bellman.
  * Membandingkan kelebihan, kekurangan, dan kompromi komputasional (*computational trade-offs*) dari masing-masing paradigma saat diterapkan pada data agribisnis riil.
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
- Integrasi sistem inferensi real-time berbasis Jenis Machine Learning (Supervised, Unsupervised, Reinforcement Learning).
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
