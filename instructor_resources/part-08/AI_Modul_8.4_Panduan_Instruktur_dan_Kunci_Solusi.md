# AI Modul 8.4: Panduan Instruktur dan Kunci Solusi Komputasi
## Interpretasi Hasil Model

**Mata Kuliah:** Kecerdasan Buatan dalam Agrokompleks  
**Kode Mata Kuliah / SKS:** AGR-4108 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Semester Ganjil / Tahun Ke-4  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER Yogyakarta  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 8.4 menjembatani dunia kecerdasan buatan murni dengan disiplin ilmu agronomi dan biologi tanaman kelapa sawit. Sasaran utama instruktur adalah mengubah pola pikir mahasiswa dari sekadar "pemburu akurasi tinggi" menjadi peneliti yang kritis terhadap alasan di balik setiap angka prediksi yang dihasilkan model (*Decision Transparency*).

Instruktur wajib menekankan tiga pilar pemahaman pada modul ini:
1. **Bahaya Efek *Clever Hans*:** Model jaringan saraf tiruan dapat mencapai akurasi tinggi di laboratorium dengan memanfaatkan derau atau artefak yang salah pada data latih. Instruktur harus membimbing mahasiswa membuktikan bahwa model mereka benar-benar memprioritaskan fitur fisiologis tanaman (panjang gelombang klorofil dan air), bukan kebetulan derau instrumen.
2. **Kekuatan Aksiomatik *Integrated Gradients*:** Mahasiswa diarahkan untuk memahami mengapa turunan parsial sederhana (*Vanilla Saliency*) tidak cukup karena mengalami saturasi gradien, dan bagaimana *Integrated Gradients* memecahkan masalah ini dengan memenuhi aksioma kelengkapan secara presisi.
3. **Pemberdayaan Pemangku Kepentingan Non-Teknis:** Memberikan wawasan kepada mahasiswa bahwa bahasa XAI adalah media komunikasi vital untuk meyakinkan pimpinan perkebunan dan petani kelapa sawit agar bersedia mengadopsi rekomendasi sistem kecerdasan buatan.

### 1.2 Alokasi Waktu Pembelajaran (Total 380 Menit)
1. **Kuliah Teori Interaktif (100 Menit):**
   - 00–25 Menit: Urgensi transparansi AI dalam agrokompleks, konsep atribusi fitur, dan fenomena korelasi palsu (*spurious correlations*).
   - 25–55 Menit: Formulasi matematis *Permutation Feature Importance* (PFI) vs *Vanilla Saliency* vs *Integrated Gradients* (aksioma kelengkapan).
   - 55–80 Menit: Landasan matematis reduksi dimensi manifold non-linier t-SNE untuk eksplorasi ruang laten lapisan tersembunyi.
   - 80–100 Menit: Diskusi interaktif mengenai pemilihan titik acuan dasar (*baseline*) pada data spektrometri daun sawit terstandar.
2. **Sesi Praktikum Komputasi Mandiri Laboratorium (180 Menit):**
   - 00–30 Menit: Penyiapan model terlatih `OilPalmYieldMLP` dan data uji independen.
   - 30–80 Menit: Implementasi dan visualisasi *Permutation Feature Importance* untuk meranking variabel penentu.
   - 80–130 Menit: Pemrograman algoritma *Integrated Gradients* berbasis integral Riemann dan verifikasi pembuktian numerik aksioma kelengkapan.
   - 130–180 Menit: Ekstraksi representasi laten 32-dimensi dan visualisasi proyeksi klaster kualitas rendemen menggunakan t-SNE.
3. **Refleksi & Diskusi Evaluasi HOTS (100 Menit):**
   - Pembahasan kunci solusi studi kasus mandiri atribusi defisiensi hara, telaah keselarasan profil spektral dengan kurva serapan klorofil, dan evaluasi rubrik asesmen.

---

## 2. Kunci Solusi Komprehensif Tugas & Proyek Mandiri Mahasiswa

### 2.1 Solusi Pembuktian Analitis Aksioma Kelengkapan Integrated Gradients
Mahasiswa diminta membuktikan bahwa jumlahan nilai atribusi *Integrated Gradients* di seluruh fitur secara eksak sama dengan selisih antara nilai prediksi sampel aktual dengan prediksi titik acuan baseline: $\sum_{j=1}^{d} IG_j(\mathbf{x}) = f(\mathbf{x}) - f(\mathbf{x}')$.

**Langkah Penurunan Solusi:**
Diberikan fungsi jaringan saraf terdiferensiasi $f: \mathbb{R}^d \rightarrow \mathbb{R}$, titik masukan $\mathbf{x} \in \mathbb{R}^d$, dan titik acuan dasar $\mathbf{x}' \in \mathbb{R}^d$.  
Definisikan lintasan garis lurus terparameterisasi $\gamma: [0, 1] \rightarrow \mathbb{R}^d$ sebagai:
$$\boldsymbol{\gamma}(\alpha) = \mathbf{x}' + \alpha (\mathbf{x} - \mathbf{x}') \quad \text{untuk } \alpha \in [0, 1]$$
Perhatikan bahwa pada $\alpha = 0$, $\boldsymbol{\gamma}(0) = \mathbf{x}'$; dan pada $\alpha = 1$, $\boldsymbol{\gamma}(1) = \mathbf{x}$.  
Berdasarkan aturan rantai kalkulus multivariat (*multivariate chain rule*), turunan dari fungsi komposit $h(\alpha) = f(\boldsymbol{\gamma}(\alpha))$ terhadap skalar $\alpha$ adalah:
$$\frac{d f(\boldsymbol{\gamma}(\alpha))}{d\alpha} = \sum_{j=1}^{d} \frac{\partial f(\boldsymbol{\gamma}(\alpha))}{\partial \gamma_j} \cdot \frac{d \gamma_j(\alpha)}{d\alpha}$$
Karena $\gamma_j(\alpha) = x'_j + \alpha(x_j - x'_j)$, maka turunan parsialnya terhadap $\alpha$ adalah:
$$\frac{d \gamma_j(\alpha)}{d\alpha} = x_j - x'_j$$
Substitusikan ke persamaan turunan rantai:
$$\frac{d f(\boldsymbol{\gamma}(\alpha))}{d\alpha} = \sum_{j=1}^{d} (x_j - x'_j) \frac{\partial f(\boldsymbol{\gamma}(\alpha))}{\partial \gamma_j}$$
Berdasarkan Teorema Dasar Kalkulus (*Fundamental Theorem of Calculus*):
$$f(\mathbf{x}) - f(\mathbf{x}') = f(\boldsymbol{\gamma}(1)) - f(\boldsymbol{\gamma}(0)) = \int_{0}^{1} \frac{d f(\boldsymbol{\gamma}(\alpha))}{d\alpha} \, d\alpha$$
Substitusikan turunan rantai ke dalam integral:
$$f(\mathbf{x}) - f(\mathbf{x}') = \int_{0}^{1} \left( \sum_{j=1}^{d} (x_j - x'_j) \frac{\partial f(\mathbf{x}' + \alpha(\mathbf{x} - \mathbf{x}'))}{\partial x_j} \right) d\alpha$$
Karena integral adalah operator linier, kita dapat menukar urutan penjumlahan dan integral:
$$f(\mathbf{x}) - f(\mathbf{x}') = \sum_{j=1}^{d} \underbrace{(x_j - x'_j) \int_{0}^{1} \frac{\partial f(\mathbf{x}' + \alpha(\mathbf{x} - \mathbf{x}'))}{\partial x_j} \, d\alpha}_{IG_j(\mathbf{x})}$$
Sehingga terbukti secara analitis bahwa:
$$\sum_{j=1}^{d} IG_j(\mathbf{x}) = f(\mathbf{x}) - f(\mathbf{x}') \quad \blacksquare$$
*Kesimpulan Pedagogis:* Pembuktian analitis ini menunjukkan keunggulan mendasar *Integrated Gradients* dibanding metode gradien sederhana: tidak ada sedikit pun informasi kontribusi prediksi yang "hilang" atau tidak terjelaskan.

---

### 2.2 Solusi Kode Komputasi Proyek Mandiri: Audit Atribusi Sampel Ekstrem
Berikut adalah implementasi acuan instruktur untuk memvalidasi pengerjaan proyek mandiri mahasiswa:

```python
import torch
import numpy as np

def audit_extreme_samples_attribution(model, X_test, y_test, wavelengths):
    """Implementasi acuan instruktur untuk komparasi atribusi pohon sawit rendemen super vs rendah."""
    model.eval()
    device = next(model.parameters()).device
    
    # Identifikasi indeks sampel ekstrem
    idx_max = np.argmax(y_test)
    idx_min = np.argmin(y_test)
    
    x_high = torch.tensor(X_test[idx_max:idx_max+1], dtype=torch.float32).to(device)
    x_low  = torch.tensor(X_test[idx_min:idx_min+1], dtype=torch.float32).to(device)
    x_base = torch.zeros_like(x_high)
    
    def compute_ig(x_in):
        accum = torch.zeros_like(x_in)
        steps = 40
        for k in range(1, steps + 1):
            alpha = k / steps
            x_step = (x_base + alpha * (x_in - x_base)).requires_grad_(True)
            out = model(x_step)
            grad = torch.autograd.grad(out, x_step)[0]
            accum += grad
        return ((x_in - x_base) * (accum / steps)).detach().cpu().numpy().flatten()
        
    attr_high = compute_ig(x_high)
    attr_low  = compute_ig(x_low)
    
    # Dominasi red-edge (panjang gelombang 700 - 740 nm berada pada indeks 60 - 68)
    red_edge_slice = slice(60, 68)
    high_red_edge_contribution = np.sum(attr_high[red_edge_slice])
    low_red_edge_contribution  = np.sum(attr_low[red_edge_slice])
    
    return {
        'Yield_High_Actual': y_test[idx_max][0],
        'Yield_Low_Actual': y_test[idx_min][0],
        'Red_Edge_Contribution_High_Yield': high_red_edge_contribution,
        'Red_Edge_Contribution_Low_Yield': low_red_edge_contribution,
        'Biochemical_Consistency': high_red_edge_contribution > low_red_edge_contribution
    }
```

---

## 3. Panduan Diagnostik & Solusi Penanganan Kendala Mahasiswa

Berikut adalah matriks diagnostik kendala teknis dan konseptual yang sering dialami mahasiswa selama praktikum:

| Gejala Kendala / Galat | Akar Penyebab (*Root Cause*) | Tindakan Korektif & Arahan Pedagogis |
| :--- | :--- | :--- |
| **`RuntimeError: One of the differentiated Tensors does not require grad`** | Mahasiswa lupa mengaktifkan pelacakan gradien pada titik interpolasi (`x_step.requires_grad_(True)`) saat menghitung *Integrated Gradients*. | Jelaskan bahwa PyTorch memerlukan penanda eksplisit bahwa tensor masukan interpolasi adalah simpul daun yang memerlukan diferensiasi parsial. |
| **Selisih galat kelengkapan (*gap error*) pada IG sangat besar (misal $> 1.0$).** | Jumlah langkah interpolasi Riemann terlalu sedikit ($m < 10$) atau fungsi aktivasi memiliki ketidaklinieran terjal di sepanjang lintasan. | Naikkan jumlah langkah interpolasi Riemann menjadi $m = 40$ atau $50$ langkah untuk menghasilkan aproksimasi numerik integral yang halus. |
| **PFI menghasilkan skor negatif pada beberapa fitur.** | Pengacakan fitur secara acak kebetulan mereduksi sedikit *noise* yang ada pada data uji, sehingga galat sedikit menurun. | Jelaskan konsep fluktuasi stokastik; fitur dengan nilai $\Delta \text{RMSE} \le 0$ dapat diinterpretasikan sebagai fitur nir-pengaruh (*noise variables*). |
| **Plot t-SNE tidak memperlihatkan pemisahan klaster sama sekali.** | Mahasiswa salah mengekstrak keluaran: yang diekstrak adalah lapisan masukan mentah $\mathbf{x}$, bukan lapisan aktivasi laten sebelum regresi akhir $\mathbf{h}$. | Arahkan mahasiswa untuk memeriksa arsitektur model dan memastikan pemanggilan `sub-network` fitur extractor yang mengambil aktivasi 32-dimensi. |

---

## 4. Rubrik Asesmen Berbasis Kinerja (Holistik & Analitik)

| Dimensi Penilaian | Bobot (%) | Kriteria Sangat Memuaskan (85 - 100) | Kriteria Memuaskan (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Teori Keterjelasan XAI (C2)** | 25% | Mampu menurunkan pembuktian analitis aksioma kelengkapan IG, menjelaskan mekanisme PFI, dan menguraikan fungsi divergensi KL t-SNE secara presisi. | Memahami konsep keterjelasan dengan baik namun penurunan matematis aksioma kelengkapan IG kurang lengkap. | Gagal menjelaskan peran atribusi fitur atau tidak memahami konsep *explainability*. |
| **Implementasi Komputasi & Visualisasi (C3)** | 35% | Mengonstruksi modul komputasi PFI, Integrated Gradients, dan ekstraksi representasi laten t-SNE secara modular, bebas galat, serta memverifikasi kelengkapan numerik. | Kode XAI berjalan baik namun visualisasi profil atribusi belum jelas atau jumlah langkah interpolasi IG terlalu rendah. | Program menghasilkan galat runtime atau implementasi autograd IG keliru. |
| **Analisis Diagnostik & Keselarasan Agronomi (C4)** | 40% | Mahasiswa mampu menelaah keselarasan biokimia tanaman (red-edge, klorofil, air) dengan fitur berbobot tinggi dan mendiagnosis keterpisahan klaster laten t-SNE secara kritis. | Mampu membaca grafik PFI dasar namun interpretasi hubungan spektral dengan fisiologi kelapa sawit belum mendalam. | Gagal menginterpretasikan hasil XAI atau menarik kesimpulan yang bertentangan dengan prinsip biologi tanaman. |

---

## 5. Jembatan Pedagogis (Pedagogical Bridging) Menuju Modul 8.11

Sebagai penutup sesi praktikum Modul 8.4, instruktur memandu refleksi puncak dari siklus pembelajaran:  
*"Kita telah membuktikan bahwa model JST kita bukan sekadar menghafal angka, melainkan benar-benar memahami bahwa pita red-edge dan hara nitrogen adalah penentu utama rendemen minyak kelapa sawit. Model kita akurat, teraturisasi, tahan derau, dan transparan secara ilmiah. Namun, jika model ini hanya tersimpan sebagai file `.pt` di dalam notebook Jupyter ini, siapakah yang dapat memanfaatkannya di perkebunan?"*

Mandor panen di kebun dan operator sortasi di pabrik kelapa sawit tidak akan membuka Jupyter Notebook untuk menjalankan kode Python. Mereka membutuhkan **antarmuka sistem prediksi yang ramah pengguna, cepat, dan siap pakai**.

Oleh karena itu, pada modul pamungkas dari Bagian 8, yaitu **AI Modul 8.11: Pembuatan Sistem Prediksi Sederhana & Inferensi Terpadu**, mahasiswa akan mengemas seluruh hasil kerja dari Modul 8.7 hingga 8.10 menjadi aplikasi inferensi nyata: mengekspor model ke format portabel industri (*TorchScript* / *ONNX*), merancang validasi masukan data lapangan, dan membangun prototipe sistem prediksi cerdas berbasis antarmuka grafis interaktif.
