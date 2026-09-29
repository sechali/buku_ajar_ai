---
marp: true
theme: default
paginate: true
header: "Bagian 2: Logika Komputasi dan Pemrograman Dasar • AI Modul 2.5"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 2.5: Operator Matematika dan Logika
### Bagian 2: Logika Komputasi dan Pemrograman Dasar
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Mengidentifikasi (C2) presedensi dan asosiativitas operator aritmatika, perbandingan, logika, keanggotaan (membership), dan identitas (identity) di Python.
- Menganalisis (C4) perhitungan neraca massa pupuk NPK presisi dan efisiensi konversi energi pabrik menggunakan operator aritmatika terstruktur.
- Menerapkan (C3) operator logika biner dan bitwise untuk manipulasi sinyal register digital pada aktuator pertanian cerdas.
- Mengevaluasi (C4) perbedaan mendasar operator kesamaan nilai (`==`) versus kesamaan identitas objek memori (`is`).

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Operator Matematika dan Logika.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\text{"UREA-46"} \in \{\text{"UREA-46"}, \text{"ZA-21"}, \text{"KIESERIT"}\}$$

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
1. **Mengidentifikasi (C2)** presedensi dan asosiativitas operator aritmatika, perbandingan, logika, keanggotaan (*membership*), dan identitas (*identity*) di Python.
2. **Menganalisis (C4)** perhitungan neraca massa pupuk NPK presisi dan efisiensi konversi energi pabrik menggunakan operator aritmatika terstruktur.
3. **Menerapkan (C3)** operator logika biner dan bitwise untuk manipulasi sinyal register digital pada aktuator pertanian cerdas.
4. **Mengevaluasi (C4)** perbedaan mendasar operator kesamaan nilai (`==`) versus kesamaan identitas objek memori (`is`).

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * **Modul Analitik Kalkulasi Fertirigasi Presisi (*Fertigation Dosage Engine*)**: Program Python tingkat produksi yang menghitung takaran pupuk N-P-K cair, sisa volume tangki nutrisi, dan laju alir pompa menggunakan kombinasi operator aritmetika standar, pembagian bulat (`//`), modulus (`%`), dan eksponen (`**`).
  * **Skrip Transformasi Normalisasi Fitur Sensor**: Modul pra-pemrosesan data kecerdasan buatan yang mengimplementasikan normalisasi skala Min-Max ($[0, 1]$) dan standarisasi skor z ($\mu = 0, \sigma = 1$) terhadap data telemetri perkebunan kelapa sawit.
  * **Matriks Evaluasi Presedensi & Operator Keanggotaan**: Tabel pembuktian urutan evaluasi hierarki ekspresi majemuk dan komparasi latensi pencarian operator `in` pada koleksi data `list` versus `set`.
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
  * **Penguasaan Hierarki Presedensi Operator (*Operator Precedence Mastery*)**: Mahasiswa mampu membedah dan mengevaluasi ekspresi matematika majemuk multi-operator tanpa ambiguitas, serta memiliki disiplin menggunakan tanda kurung pelindung (*defensive parentheses*).
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
- Integrasi sistem inferensi real-time berbasis Operator Matematika dan Logika.
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
