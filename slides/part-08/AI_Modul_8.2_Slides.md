---
marp: true
theme: default
paginate: true
header: "Bagian 8: Unsupervised Learning dan Reduksi Dimensi • AI Modul 8.2"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 8.2: Training Model
### Bagian 8: Unsupervised Learning dan Reduksi Dimensi
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Sub-CPMK 8.2.1 (C2): Menguraikan tahapan komputasi dalam siklus pelatihan (training loop) kelas industri, membedah perbedaan mekanisme propagasi antara mode `model.train()` dan `model.eval()`, serta menjelaskan formulasi matematis pemotongan gradien (gradient clipping) dan penjadwalan laju pembelajaran (learning rate scheduling).
- Sub-CPMK 8.2.2 (C3): Membangun skrip alur pelatihan (training pipeline) profesional menggunakan PyTorch yang mengintegrasikan generator mini-batch `DataLoader`, optimasi Adam, pemotongan gradien global, penjadwal adaptif `ReduceLROnPlateau`, dan pencadangan bobot terbaik (Model Checkpointing).
- Sub-CPMK 8.2.3 (C4): Mendiagnosis gejala ledakan gradien (gradient exploding), osilasi liar pada dataran semu (plateau), serta merumuskan strategi penalaan hiperparameter pelatihan adaptif guna menghasilkan bobot model tergeneralisasi tinggi pada kasus data terpadu agrokompleks.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Training Model.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\sum_{t=1}^{\infty} \eta_t = \infty \quad \text{dan} \quad \sum_{t=1}^{\infty} \eta_t^2 < \infty$$

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
1. **Sub-CPMK 8.2.1 (C2):** Menguraikan tahapan komputasi dalam siklus pelatihan (*training loop*) kelas industri, membedah perbedaan mekanisme propagasi antara mode `model.train()` dan `model.eval()`, serta menjelaskan formulasi matematis pemotongan gradien (*gradient clipping*) dan penjadwalan laju pembelajaran (*learning rate scheduling*).
2. **Sub-CPMK 8.2.2 (C3):** Membangun skrip alur pelatihan (*training pipeline*) profesional menggunakan PyTorch yang mengintegrasikan generator mini-batch `DataLoader`, optimasi Adam, pemotongan gradien global, penjadwal adaptif `ReduceLROnPlateau`, dan pencadangan bobot terbaik (*Model Checkpointing*).
3. **Sub-CPMK 8.2.3 (C4):** Mendiagnosis gejala ledakan gradien (*gradient exploding*), osilasi liar pada dataran semu (*plateau*), serta merumuskan strategi penalaan hiperparameter pelatihan adaptif guna menghasilkan bobot model tergeneralisasi tinggi pada kasus data terpadu agrokompleks.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
- **Luaran Langsung (*Outputs*):** Skrip alur pelatihan modular PyTorch berstandar industri, modul *training loop* dengan fungsi pencadangan model otomatis (`.pt`), serta visualisasi dinamika norma gradien dan *learning rate decay*.
- **Dampak Pembelajaran (*Outcomes*):** Mahasiswa memiliki kemahiran rekayasa perangkat lunak dalam melatih model jaringan saraf tiruan secara stabil, disiplin memisahkan fase pelatihan dan validasi, serta kebal terhadap kegagalan numerik.
- **Implikasi Jangka Panjang (*Impacts*):** Terwujudnya sistem komputasi pelatihan model AI perkebunan yang terstandar, dapat direproduksi (*reproducible*), dan siap diotomatisasi pada kluster server komputasi berkinerja tinggi (*High-Performance Computing* / GPU Cloud).

---

## 2. Profil Fundamental Training Model: Fungsi, Manfaat, dan Keunggulan-Kelemahan
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
- Integrasi sistem inferensi real-time berbasis Training Model.
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
