---
marp: true
theme: default
paginate: true
header: "Bagian 2: Logika Komputasi dan Pemrograman Dasar • AI Modul 2.4"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 2.4: Variabel dan Tipe Data
### Bagian 2: Logika Komputasi dan Pemrograman Dasar
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Mengidentifikasi (C2) sistem pengetikan dinamis (Dynamic Typing) dan mekanisme alokasi memori objek pada CPython.
- Menganalisis (C4) perbedaan mutabilitas (Mutability) antara tipe data primitif dan tipe data majemuk serta implikasinya terhadap aliasing bug.
- Menerapkan (C3) konversi tipe data eksplisit (type casting) dan penanganan presisi numerik (integer, float, boolean, string) pada data telemetri sensor kebun.
- Mengevaluasi (C4) jejak memori (memory footprint) objek data menggunakan modul `sys` untuk efisiensi komputasi tepi (Edge AI).

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Variabel dan Tipe Data.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$0.1_{10} = 0.00011001100110011001100110011\dots_2$$

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
1. **Mengidentifikasi (C2)** sistem pengetikan dinamis (*Dynamic Typing*) dan mekanisme alokasi memori objek pada CPython.
2. **Menganalisis (C4)** perbedaan mutabilitas (*Mutability*) antara tipe data primitif dan tipe data majemuk serta implikasinya terhadap *aliasing bug*.
3. **Menerapkan (C3)** konversi tipe data eksplisit (*type casting*) dan penanganan presisi numerik (integer, float, boolean, string) pada data telemetri sensor kebun.
4. **Mengevaluasi (C4)** jejak memori (*memory footprint*) objek data menggunakan modul `sys` untuk efisiensi komputasi tepi (*Edge AI*).

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * **Modul Parser Telemetri Panen Sawit (*Telemetry Ingestion Engine*)**: Skrip Python tingkat produksi beranotasi *Type Hinting* (PEP 484) yang memvalidasi, membersihkan (*sanitizing*), dan mengonversi payload data mentah heterogen dari jembatan timbang dan gerbang RFID PKS.
  * **Alat Uji Profil Alokasi Memori (*Memory Profiling Lab*)**: Program inspeksi alamat memori (`id()`), evaluasi operator identitas vs kesetaraan nilai (`is` vs `==`), pengukuran ukuran byte objek fisik (`sys.getsizeof()`), serta pembuktian fenomena mutasi *in-place*.
  * **Kalkulator Analisis Galat Presisi IEEE 754**: Modul analisis numerik yang membuktikan limitasi representasi 52-bit mantisa pecahan desimal ($0.1 + 0.2 \ne 0.3$) dan mengimplementasikan solusi toleransi mesin `math.isclose()` serta `decimal.Decimal`.
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
  * **Penguasaan Model Referensi Objek (*Object Reference Mastery*)**: Mahasiswa memahami bahwa variabel dalam Python adalah label pointer di memori Heap, membedakan perilaku objek mutabel (`list`, `dict`) versus imutabel (`int`, `float`, `str`), serta menghindari bug *aliasing* dan *mutable default argument*.
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
- Integrasi sistem inferensi real-time berbasis Variabel dan Tipe Data.
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
