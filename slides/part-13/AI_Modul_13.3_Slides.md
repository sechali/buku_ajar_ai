---
marp: true
theme: default
paginate: true
header: "Bagian 13: Integrasi Sistem AI, Deployment Edge, dan Studi Kasus Terapan • AI Modul 13.3"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 13.3: Pengembangan Aplikasi Sederhana
### Bagian 13: Integrasi Sistem AI, Deployment Edge, dan Studi Kasus Terapan
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Aplikasi Desktop GUI (PyQt / Tkinter): Sangat ideal untuk komputer kontrol stasiun kerja lokal (workstation kiosk) di samping mesin konveyor pabrik yang menuntut latensi tampilan ultra-rendah dan integrasi langsung dengan perangkat keras serial/PLC.
- Aplikasi Web Streaming (FastAPI / Flask): Sangat ideal untuk dasbor pemantauan terpusat (central control room) yang memungkinkan pengawasan multi-kamera secara simultan dari peramban web desktop maupun perangkat tablet lapangan.
- Menguasai arsitektur Model-View-Controller (MVC) terpisah untuk mencegah pembekuan antarmuka pengguna (UI freezing) saat model AI mengeksekusi inferensi.
- Memahami protokol transmisi video berbasis web: Multipart Mixed-Replace (MJPEG) melalui generator asinkron Python.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Pengembangan Aplikasi Sederhana.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\Delta t_{\text{event\_delay}} = \Delta t_{\text{inference}} > 16.6\text{ ms (Batas 60 FPS)}$$

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
1. Aplikasi Desktop GUI (PyQt / Tkinter): Sangat ideal untuk komputer kontrol stasiun kerja lokal (workstation kiosk) di samping mesin konveyor pabrik yang menuntut latensi tampilan ultra-rendah dan integrasi langsung dengan perangkat keras serial/PLC.
2. Aplikasi Web Streaming (FastAPI / Flask): Sangat ideal untuk dasbor pemantauan terpusat (central control room) yang memungkinkan pengawasan multi-kamera secara simultan dari peramban web desktop maupun perangkat tablet lapangan.
3. Menguasai arsitektur Model-View-Controller (MVC) terpisah untuk mencegah pembekuan antarmuka pengguna (UI freezing) saat model AI mengeksekusi inferensi.
4. Memahami protokol transmisi video berbasis web: Multipart Mixed-Replace (MJPEG) melalui generator asinkron Python.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Dokumen rancangan arsitektur pemrosesan visual dan spesifikasi parameter model Pengembangan Aplikasi Sederhana.
  * Berkas kode program Python modular tervalidasi menggunakan PyTorch/OpenCV yang siap diuji di lapangan.
  * Grafik metrik evaluasi kinerja (akurasi, mAP, latensi inferensi, dan konsumsi memori aktivasi).
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
  * Penguasaan mendalam terhadap formulasi matematika dan mekanisme konvolusi/deteksi objek visual.
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
- Integrasi sistem inferensi real-time berbasis Pengembangan Aplikasi Sederhana.
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
