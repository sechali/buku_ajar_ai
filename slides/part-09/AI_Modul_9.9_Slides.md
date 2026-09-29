---
marp: true
theme: default
paginate: true
header: "Bagian 9: Fondasi Deep Learning dan Arsitektur Jaringan Saraf Tiruan • AI Modul 9.9"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 9.9: Framework Deep Learning (TensorFlow & PyTorch)
### Bagian 9: Fondasi Deep Learning dan Arsitektur Jaringan Saraf Tiruan
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Memahami (C2) prinsip kerja arsitektur framework deep learning modern, perbedaan mendasar antara graf komputasi dinamis (dynamic define-by-run) pada PyTorch dan graf komputasi statis/simbolik (static define-and-run) pada TensorFlow, serta peran engine diferensiasi otomatis (automatic differentiation engine).
- Menerapkan (C3) pustaka PyTorch untuk merancang arsitektur Multi-Layer Perceptron berorientasi objek (`torch.nn.Module`), mengonfigurasi pipeline pemuatan data efisien (`torch.utils.data.Dataset` dan `DataLoader`), serta mengeksekusi siklus pelatihan kustom (custom training loop).
- Menganalisis (C4) profil performa eksekusi model (penggunaan memori VRAM GPU, throughput batch per detik, latensi inferensi) serta prosedur ekspor model ke format produksi standar (ONNX dan TorchScript) untuk penerapan terpasang (edge deployment).

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Framework Deep Learning (TensorFlow & PyTorch).
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\frac{\partial L}{\partial w_i} = \sum_{	ext{semua jalur } p} \prod_{(u, v) \in p} \frac{\partial v}{\partial u}$$

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
1. **Memahami (C2)** prinsip kerja arsitektur framework deep learning modern, perbedaan mendasar antara graf komputasi dinamis (*dynamic define-by-run*) pada PyTorch dan graf komputasi statis/simbolik (*static define-and-run*) pada TensorFlow, serta peran engine diferensiasi otomatis (*automatic differentiation engine*).
2. **Menerapkan (C3)** pustaka PyTorch untuk merancang arsitektur Multi-Layer Perceptron berorientasi objek (`torch.nn.Module`), mengonfigurasi pipeline pemuatan data efisien (`torch.utils.data.Dataset` dan `DataLoader`), serta mengeksekusi siklus pelatihan kustom (*custom training loop*).
3. **Menganalisis (C4)** profil performa eksekusi model (penggunaan memori VRAM GPU, throughput batch per detik, latensi inferensi) serta prosedur ekspor model ke format produksi standar (ONNX dan TorchScript) untuk penerapan terpasang (*edge deployment*).

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Langsung)**:
  * Pemahaman mendalam mengenai ekosistem software deep learning: PyTorch, TorchVision, TensorFlow, Keras, dan ONNX Runtime.
  * Skrip Python modular berstandar PEP 8 untuk pipeline end-to-end data loading, training loop, evaluasi metrik, dan penyimpanan checkpoint menggunakan PyTorch.
  * Laporan perbandingan latensi inferensi model pada CPU dan GPU.
* **Outcomes (Kompetensi Aplikatif)**:
  * Keahlian membangun arsitektur deep learning mutakhir tanpa perlu menuliskan derivasi kalkulus manual dari dasar.
  * Kemampuan mengoptimalkan throughput pipeline data untuk mencegah bottleneck I/O saat melatih model pada ribuan citra sensor perkebunan.
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
- Integrasi sistem inferensi real-time berbasis Framework Deep Learning (TensorFlow & PyTorch).
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
