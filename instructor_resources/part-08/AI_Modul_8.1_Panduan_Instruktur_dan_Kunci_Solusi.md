# AI Modul 8.1: Panduan Instruktur dan Kunci Solusi Komputasi
## Preprocessing Dataset

**Mata Kuliah:** Kecerdasan Buatan dalam Agrokompleks  
**Kode Mata Kuliah / SKS:** AGR-4108 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Semester Ganjil / Tahun Ke-4  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER Yogyakarta  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 8.1 merupakan modul pembuka fase rekayasa alur kerja terapan (*applied end-to-end pipeline*) dalam *Deep Learning*. Setelah mahasiswa memahami prinsip kerja internal algoritma JST pada Modul 8.1 hingga 8.6, instruktur kini membimbing mahasiswa beralih ke ranah rekayasa data profesional berbasis ekosistem PyTorch.

Poin penekanan pedagogis utama instruktur pada modul ini adalah:
1. **Bahaya Kebocoran Data Spasial (*Spatial Data Leakage*):** Mahasiswa pertanian dan kehutanan sering kali terbiasa menggunakan pemisahan acak (`train_test_split`). Instruktur harus mendemonstrasikan secara visual mengapa partisi acak pada pohon kebun yang bertetangga mengakibatkan metrik evaluasi yang menipu (*over-optimistic bias*).
2. **Disiplin Isolasi Statistik Scaler:** Mahasiswa wajib memahami secara ketat bahwa nilai mean $\boldsymbol{\mu}$ dan standar deviasi $\boldsymbol{\sigma}$ hanya boleh dihitung (*fit*) dari data latih, kemudian dibekukan untuk mentransformasi data validasi dan data uji.
3. **Peralihan ke Paradigma PyTorch `Dataset` dan `DataLoader`:** Mahasiswa dibimbing mentransformasikan matriks NumPy menjadi iterator batch yang efisien secara memori dan siap dialirkan ke GPU.

### 1.2 Alokasi Waktu Pembelajaran (Total 380 Menit)
1. **Kuliah Teori Interaktif (100 Menit):**
   - 00–25 Menit: Teorema kurvatur Hessian, rasio kondisi $\kappa(\mathbf{H})$, dan pengaruh standarisasi masukan terhadap percepatan konvergensi optimasi.
   - 25–55 Menit: Autokorelasi spasial dalam domain agrokompleks dan formulasi matematis *Spatial Block Partitioning*.
   - 55–80 Menit: Arsitektur perangkat lunak PyTorch `torch.utils.data.Dataset` dan generator `DataLoader`.
   - 80–100 Menit: Diskusi interaktif mengenai penanganan data hilang (*missing values*), pencilan (*outliers*), dan strategi *Weighted Random Sampling*.
2. **Sesi Praktikum Komputasi Mandiri Laboratorium (180 Menit):**
   - 00–30 Menit: Pembangkitan dataset multivariat (120 kanal spektral + 4 sensor tanah) dari 10 afdeling perkebunan sawit.
   - 30–75 Menit: Implementasi dan visualisasi perbandingan *Random Split* vs *Spatial Block Partitioning*.
   - 75–125 Menit: Konstruksi kelas mandiri `IsolatedStandardScaler` dan pembuktian invarian data uji.
   - 125–180 Menit: Pembuatan kelas kustom `OilPalmSpectralDataset` dan pengujian aliran mini-batch pada `DataLoader`.
3. **Refleksi & Diskusi Evaluasi HOTS (100 Menit):**
   - Pembahasan solusi studi kasus mandiri defisiensi hara NPK multi-output, analisis galat tipe data tensor, dan peninjauan rubrik asesmen.

---

## 2. Kunci Solusi Komprehensif Tugas & Proyek Mandiri Mahasiswa

### 2.1 Solusi Pembuktian Analitis Rasio Kondisi Matriks Hessian
Mahasiswa diminta membuktikan mengapa standarisasi ortogonal fitur masukan mereduksi rasio kondisi matriks Hessian $\kappa(\mathbf{H})$ menuju nilai optimal 1.

**Langkah Penurunan Solusi:**
Diberikan model linier multivariat $f(\mathbf{x}) = \mathbf{w}^T \mathbf{x}$ dengan fungsi rugi Mean Squared Error (MSE):
$$\mathcal{L}(\mathbf{w}) = \frac{1}{2m} \|\mathbf{X}\mathbf{w} - \mathbf{y}\|_2^2$$
Matriks Hessian dari fungsi rugi terhadap parameter $\mathbf{w}$ adalah:
$$\mathbf{H} = \nabla^2 \mathcal{L}(\mathbf{w}) = \frac{1}{m} \mathbf{X}^T \mathbf{X}$$
Jika fitur masukan $\mathbf{X}$ tidak distandarisasi, fitur dengan varians besar $\sigma_1^2 \gg \sigma_2^2$ menghasilkan nilai eigen maksimum $\lambda_{\max} \approx \sigma_1^2$ dan $\lambda_{\min} \approx \sigma_2^2$, sehingga:
$$\kappa(\mathbf{H}) = \frac{\lambda_{\max}}{\lambda_{\min}} \approx \frac{\sigma_1^2}{\sigma_2^2} \gg 1$$
Ketika fitur distandarisasi secara penuh menjadi $\mathbf{Z}$ di mana setiap kolom memiliki rata-rata 0 dan varians 1 serta kovarians antar-fitur mendekati nol (atau didekorlasikan via PCA/whitening):
$$\frac{1}{m} \mathbf{Z}^T \mathbf{Z} \approx \mathbf{I}_d$$
Karena semua nilai eigen dari matriks identitas $\mathbf{I}_d$ adalah $\lambda_1 = \lambda_2 = \dots = \lambda_d = 1$, maka rasio kondisi menjadi:
$$\kappa(\mathbf{H}) = \frac{\lambda_{\max}}{\lambda_{\min}} = \frac{1}{1} = 1 \quad \blacksquare$$
*Kesimpulan Pedagogis:* Rasio kondisi $\kappa = 1$ mengubah kontur elips yang sangat lonjong menjadi lingkaran bola simetris, menjamin vektor negatif gradien mengarah tepat ke titik minimum global tanpa osilasi transversal.

---

### 2.2 Solusi Kode Komputasi Proyek Mandiri: Multi-Output NPK Dataset
Berikut adalah implementasi acuan instruktur untuk memvalidasi pengerjaan proyek mandiri mahasiswa:

```python
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

class MultiModalPalmDataset(Dataset):
    """Kelas Dataset PyTorch kustom untuk prediksi multi-output hara NPK kelapa sawit."""
    def __init__(self, X_features, y_targets):
        # Konversi array numpy menjadi tensor bertipe torch.float32
        self.X = torch.tensor(X_features, dtype=torch.float32)
        self.y = torch.tensor(y_targets, dtype=torch.float32)
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

def run_project_pipeline():
    # Simulasi data mandiri: 800 sampel, 155 fitur (150 spektral + 5 tanah), 3 target hara (N, P, K)
    np.random.seed(123)
    N, D_feat, D_targ = 800, 155, 3
    X_synthetic = np.random.randn(N, D_feat) * 2.5 + 10.0
    y_synthetic = np.random.uniform(1.2, 3.5, (N, D_targ))
    block_ids = np.repeat(np.arange(1, 9), 100) # 8 blok perkebunan
    
    # 1. Partisi Blok Spasial
    train_mask = np.isin(block_ids, [1, 2, 3, 4, 5])
    val_mask   = np.isin(block_ids, [6, 7])
    test_mask  = np.isin(block_ids, [8])
    
    # 2. Fitting Scaler HANYA pada data latih
    mu_tr = np.mean(X_synthetic[train_mask], axis=0, keepdims=True)
    std_tr = np.std(X_synthetic[train_mask], axis=0, keepdims=True) + 1e-8
    
    X_tr_norm = (X_synthetic[train_mask] - mu_tr) / std_tr
    X_va_norm = (X_synthetic[val_mask] - mu_tr) / std_tr
    X_te_norm = (X_synthetic[test_mask] - mu_tr) / std_tr
    
    # 3. Konstruksi PyTorch DataLoader
    train_ds = MultiModalPalmDataset(X_tr_norm, y_synthetic[train_mask])
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
    
    # Verifikasi Batch
    bx, by = next(iter(train_loader))
    return bx.shape, by.shape

# Hasil verifikasi harus: (torch.Size([16, 155]), torch.Size([16, 3]))
```

---

## 3. Panduan Diagnostik & Solusi Penanganan Kendala Mahasiswa

Berikut adalah matriks diagnostik kendala teknis dan konseptual yang sering dialami mahasiswa selama praktikum:

| Gejala Kendala / Galat | Akar Penyebab (*Root Cause*) | Tindakan Korektif & Arahan Pedagogis |
| :--- | :--- | :--- |
| **`RuntimeError: Expected object of scalar type Float but got Double`** | Mahasiswa mengonversi NumPy array ke PyTorch Tensor tanpa menentukan `dtype=torch.float32`. Secara *default*, NumPy membuat array dengan presisi `float64` (*Double*). | Arahkan mahasiswa untuk selalu menyertakan argumen eksplisit: `torch.tensor(data, dtype=torch.float32)`. |
| **Nilai akurasi data uji sangat tinggi saat latihan, tetapi model gagal total saat diuji pada kebun baru.** | Mahasiswa menggunakan `train_test_split(shuffle=True)` biasa, memicu kebocoran data spasial di mana pohon-pohon satu petak bercampur antara data latih dan uji. | Wajibkan mahasiswa mengganti fungsi partisi acak dengan partisi berbasis ID Blok Afdeling perkebunan (*Spatial Block Split*). |
| **Nilai loss menjadi `NaN` pada batch pertama pelatihan.** | Terdapat nilai kosong (`np.nan`) atau tak hingga (`np.inf`) pada fitur sensor yang belum dibersihkan sebelum masuk ke DataLoader. | Ajarkan mahasiswa melakukan audit data awal: `np.isnan(X).sum()` dan terapkan imputasi median atau pembersihan sebelum konversi tensor. |
| **DataLoader sangat lambat saat mengalirkan data ke prosesor.** | Ukuran mini-batch terlalu kecil ($m = 1$) atau penggunaan fungsi transformasi berat di dalam metode `__getitem__` tanpa `num_workers`. | Pindahkan komputasi standarisasi ke luar kelas `Dataset` (lakukan vektorisasi satu kali di awal), dan atur ukuran batch ke angka kelipatan dua ($16, 32, 64$). |

---

## 4. Rubrik Asesmen Berbasis Kinerja (Holistik & Analitik)

| Dimensi Penilaian | Bobot (%) | Kriteria Sangat Memuaskan (85 - 100) | Kriteria Memuaskan (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Teori & Kondisi Matriks (C2)** | 25% | Mampu menguraikan kaitan rasio kondisi matriks Hessian $\kappa(\mathbf{H})$ dengan konvergensi gradien, serta menjelaskan bahaya kebocoran spasial secara mendalam. | Memahami prinsip standarisasi dengan baik namun penurunan matematis kondisi matriks Hessian kurang lengkap. | Gagal menjelaskan tujuan penskalaan data atau tidak memahami autokorelasi spasial. |
| **Konstruksi Pipeline & PyTorch DataLoader (C3)** | 35% | Mengonstruksi kelas `Dataset` dan `DataLoader` PyTorch secara sempurna, mematuhi prinsip isolasi statistik scaler latih, serta bebas galat tipe data. | Pipeline berjalan baik namun terdapat redundansi kode atau penanganan isolasi data uji belum sepenuhnya modular. | Program menghasilkan galat saat dieksekusi atau standarisasi dilakukan pada seluruh data sebelum partisi. |
| **Analisis Diagnostik & Solusi Lapangan (C4)** | 40% | Mahasiswa mampu mendeteksi anomali data lapangan, merumuskan penanganan pencilan berbasis IQR, dan membuktikan ekuivalensi dimensi tensor multi-output. | Mampu menganalisis data dasar namun strategi penanganan pencilan belum optimal. | Gagal mengidentifikasi keberadaan pencilan atau mengabaikan ketidakseimbangan kelas. |

---

## 5. Jembatan Pedagogis (Pedagogical Bridging) Menuju Modul 8.8

Sebagai penutup sesi praktikum Modul 8.1, instruktur mengarahkan mahasiswa untuk melakukan evaluasi reflektif:  
*"Kita telah memiliki generator batch tensor `DataLoader` yang memancarkan pasangan masukan dan target `(batch_x, batch_y)` secara teratur, teracak, dan efisien secara memori. Namun, ke mana tensor-tensor ini akan bermuara?"*

Sebuah sistem *deep learning* yang tangguh memerlukan **orkestrasi siklus pelatihan (*training loop*)** yang kokoh. Jika mahasiswa hanya menulis loop sederhana tanpa teknik pemotongan gradien (*gradient clipping*), laju pembelajaran dinamis (*learning rate scheduler*), dan pencadangan otomatis bobot terbaik (*model checkpointing*), proses pelatihan dapat dengan mudah mengalami ledakan numerik atau konvergensi sub-optimal.

Oleh karena itu, pada **AI Modul 8.8: Rekayasa Alur Pelatihan (*Training Pipeline*) Model Deep Learning**, mahasiswa akan merakit siklus pelatihan kelas industri yang menyambungkan `DataLoader` yang telah dibangun pada modul ini ke dalam arsitektur multi-lapisan, memantau kurva konvergensi secara real-time, dan mengamankan model teroptimal untuk siap dievaluasi.
