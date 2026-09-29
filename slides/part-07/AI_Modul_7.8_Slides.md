---
marp: true
theme: default
paginate: true
header: "Bagian 7: Machine Learning - Konsep dan Algoritma Klasik • AI Modul 7.8"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 7.8: K-Means Clustering
### Bagian 7: Machine Learning - Konsep dan Algoritma Klasik
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Memahami (C2) prinsip dasar pembelajaran tak terawasi (unsupervised learning), formulasi matematis fungsi objektif inersia / Within-Cluster Sum of Squares (WCSS), mekanisme dua fase algoritma Lloyd (penugasan dan pembaruan centroid), serta teknik inisialisasi probabilistik K-Means++.
- Menerapkan (C3) pustaka Scikit-Learn (`KMeans` dan `StandardScaler`) untuk mengelompokkan data survei hara tanah perkebunan (N, P, K, pH, kelembapan) ke dalam zona kesuburan homogen tanpa panduan label target awal.
- Menganalisis (C4) penentuan jumlah klaster optimal (K) menggunakan Metode Siku (Elbow Method) dan Koefisien Silhouette, mendiagnosis fenomena konvergensi ke optimum lokal sub-optimal, serta mengevaluasi dampak penskalaan fitur terhadap geometri partisi klaster.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada K-Means Clustering.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$X = \{\mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_N\}, \quad \mathbf{x}_i \in \mathbb{R}^p$$

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
1. **Memahami (C2)** prinsip dasar pembelajaran tak terawasi (*unsupervised learning*), formulasi matematis fungsi objektif inersia / *Within-Cluster Sum of Squares* (WCSS), mekanisme dua fase algoritma Lloyd (penugasan dan pembaruan centroid), serta teknik inisialisasi probabilistik K-Means++.
2. **Menerapkan (C3)** pustaka Scikit-Learn (`KMeans` dan `StandardScaler`) untuk mengelompokkan data survei hara tanah perkebunan (N, P, K, pH, kelembapan) ke dalam zona kesuburan homogen tanpa panduan label target awal.
3. **Menganalisis (C4)** penentuan jumlah klaster optimal ($K$) menggunakan Metode Siku (*Elbow Method*) dan Koefisien Silhouette, mendiagnosis fenomena konvergensi ke optimum lokal sub-optimal, serta mengevaluasi dampak penskalaan fitur terhadap geometri partisi klaster.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Penguasaan analitik fungsi objektif WCSS $J = \sum_{k=1}^K \sum_{i \in S_k} \|\mathbf{x}_i - \boldsymbol{\mu}_k\|^2$, aturan pergeseran centroid, probabilitas inisialisasi K-Means++, dan formulasi koefisien Silhouette $s(i)$.
  * Skrip Python berstandar PEP 8 untuk pipeline klasterisasi otomatis, visualisasi kurva evaluasi Elbow, dan pemetaan sebaran spasial klaster tanah 2D.
  * Dokumen rekomendasi pemupukan presisi terzonasi (*Variable Rate Fertilization*) berbasis centroid hara tanah.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian merancang sistem segmentasi data perkebunan berskala besar secara mandiri tanpa terhambat oleh ketiadaan label manual dari pakar agronomi (*unsupervised capability*).
  * Kemampuan mengidentifikasi zona anomali lahan (seperti kantong tanah masam atau defisiensi kalium kritis) yang tidak terlihat pada analisis agregat rata-rata afdeling.
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
- Integrasi sistem inferensi real-time berbasis K-Means Clustering.
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
