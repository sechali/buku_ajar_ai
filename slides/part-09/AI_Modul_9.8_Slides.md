---
marp: true
theme: default
paginate: true
header: "Bagian 9: Fondasi Deep Learning dan Arsitektur Jaringan Saraf Tiruan • AI Modul 9.8"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# AI Modul 9.8: Hyperparameter Tuning
### Bagian 9: Fondasi Deep Learning dan Arsitektur Jaringan Saraf Tiruan
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
- Sub-CPMK 9.8.1 (C2): Menguraikan dasar teoretis disparitas antara galat empiris (training loss) dan galat generalisasi (validation loss), serta membedah landasan matematis mekanisme penalti bobot (L_1 dan L_2 Weight Decay), Inverted Dropout, Batch Normalization, dan Early Stopping.
- Sub-CPMK 9.8.2 (C3): Mengimplementasikan algoritma Inverted Dropout dan normalisasi lapisan mini-batch (Batch Normalization) lengkap dengan penyesuaian parameter skala (\gamma) dan geser (\beta) serta mekanisme pelacakan statistik berjalan (running statistics) untuk mode inferensi pada arsitektur jaringan saraf tiruan.
- Sub-CPMK 9.8.3 (C4): Mendiagnosis fenomena overfitting, pergeseran kovariat internal (internal covariate shift), dan dinamika divergensi gradien pada data tabular multivariat spektral agrokompleks, lalu merumuskan konfigurasi regularisasi komposit yang optimal guna menjamin reliabilitas prediksi model di lapangan perkebunan.

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada Hyperparameter Tuning.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$$\|\mathbf{W}^{[l]}\|_F^2 = \sum_{i=1}^{n^{[l]}} \sum_{j=1}^{n^{[l-1]}} (W_{i,j}^{[l]})^2$$

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
1. **Sub-CPMK 9.8.1 (C2):** Menguraikan dasar teoretis disparitas antara galat empiris (*training loss*) dan galat generalisasi (*validation loss*), serta membedah landasan matematis mekanisme penalti bobot ($L_1$ dan $L_2$ *Weight Decay*), *Inverted Dropout*, *Batch Normalization*, dan *Early Stopping*.
2. **Sub-CPMK 9.8.2 (C3):** Mengimplementasikan algoritma *Inverted Dropout* dan normalisasi lapisan mini-batch (*Batch Normalization*) lengkap dengan penyesuaian parameter skala ($\gamma$) dan geser ($\beta$) serta mekanisme pelacakan statistik berjalan (*running statistics*) untuk mode inferensi pada arsitektur jaringan saraf tiruan.
3. **Sub-CPMK 9.8.3 (C4):** Mendiagnosis fenomena *overfitting*, pergeseran kovariat internal (*internal covariate shift*), dan dinamika divergensi gradien pada data tabular multivariat spektral agrokompleks, lalu merumuskan konfigurasi regularisasi komposit yang optimal guna menjamin reliabilitas prediksi model di lapangan perkebunan.

### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
- **Luaran Langsung (*Outputs*):** Skrip program Python dan pustaka komputasi numerik murni NumPy serta implementasi PyTorch yang memuat modul regulerisasi (*Weight Decay, Dropout, BatchNorm2d/1d, EarlyStopping*) yang terverifikasi tanpa galat.
- **Dampak Pembelajaran (*Outcomes*):** Mahasiswa memiliki insting rekayasa pembelajaran mesin dalam membedah kapan sebuah model memerlukan penalti pembobotan atau modulasi statistik representasi fitur untuk mencegah fenomena hafalan sampel (*data memorization*).
- **Implikasi Jangka Panjang (*Impacts*):** Terciptanya model kecerdasan buatan berbasis *deep learning* sektor perkebunan dan kehutanan yang tangguh (*robust*), mampu bekerja stabil pada variasi lingkungan musiman baru, serta memiliki daya generalisasi tinggi saat diterapkan pada armada sensor IoT cerdas.

---

## 2. Profil Fundamental Regularisasi dan Generalisasi: Fungsi, Manfaat, dan Keunggulan-Kelemahan
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
- Integrasi sistem inferensi real-time berbasis Hyperparameter Tuning.
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
