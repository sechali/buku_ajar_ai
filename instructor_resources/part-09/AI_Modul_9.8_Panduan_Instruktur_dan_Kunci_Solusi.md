# AI Modul 9.8: Panduan Instruktur dan Kunci Solusi Komputasi
## Regularisasi & Generalisasi Deep Learning

**Mata Kuliah:** Kecerdasan Buatan dalam Agrokompleks  
**Kode Mata Kuliah / SKS:** AGR-4108 / 3 SKS  
**Sasaran Sasaran Jenjang:** Mahasiswa Semester Ganjil / Tahun Ke-4  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER Yogyakarta  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 9.8 merupakan puncak dari modul pembelajaran *Deep Learning & Jaringan Saraf Tiruan* (Bagian 8). Sasaran utama instruktur adalah menjembatani pemahaman mahasiswa dari sekadar "melatih model hingga konvergen" menjadi "melatih model agar berdaya generalisasi tinggi di lingkungan nyata".

Instruktur perlu menekankan bahwa dalam aplikasi agrokompleks (perkebunan kelapa sawit, kehutanan, dan pertanian presisi), data latih sering kali memiliki sifat multikolinearitas tinggi dengan ukuran sampel yang terbatas. Jika model dibiarkan menghafal sampel latih (*empirical risk minimization* murni), model akan mengalami kegagalan fatal saat dideploy pada sensor lapangan atau drone survei.

### 1.2 Alokasi Waktu Pembelajaran (Total 380 Menit)
1. **Kuliah Teori Interaktif (100 Menit):**
   - 00–25 Menit: Disparitas galat empiris vs galat generalisasi, prinsip *bias-variance tradeoff*, dan rasionalisasi Bayesian prior ($L_1$ Laplace vs $L_2$ Gaussian).
   - 25–55 Menit: Analisis matematis *Inverted Dropout* (pembuktian invarian ekspektasi $\mathbb{E}[\mathbf{\tilde{a}}] = \mathbf{a}$) dan pembongkaran mekanisme 4-tahap *Batch Normalization*.
   - 55–80 Menit: Algoritma *Early Stopping*, pemantauan *patience*, dan teknik pemulihan bobot terbaik (*model checkpointing*).
   - 80–100 Menit: Bedah studi kasus industri perkebunan dan diskusi interaktif mengenai anomali interaksi *Dropout* dan *Batch Normalization*.
2. **Sesi Praktikum Komputasi Mandiri Laboratorium (180 Menit):**
   - 00–30 Menit: Setup dataset spektrometri daun kelapa sawit sintetis (120 kanal pita spektral, $N=400$).
   - 30–90 Menit: Rekayasa modul mandiri *InvertedDropout*, *BatchNormalization*, dan *EarlyStopping* menggunakan NumPy murni.
   - 90–150 Menit: Pelatihan komparasi Model A (Baseline tanpa regularisasi) vs Model B (Regularized: L2 + Dropout + BatchNorm + Early Stopping).
   - 150–180 Menit: Visualisasi kurva evaluasi *overfitting*, perbandingan dispersi bobot histogram, serta evaluasi pada data uji independen.
3. **Refleksi & Diskusi Evaluasi HOTS (100 Menit):**
   - Pembahasan kunci solusi studi kasus mandiri, analisis galat komputasi, dan pemaparan rubrik asesmen tugas akhir bagian.

---

## 2. Kunci Solusi Komprehensif Tugas & Proyek Mandiri Mahasiswa

### 2.1 Solusi Pembuktian Analitis Ekspektasi Inverted Dropout
Mahasiswa diminta membuktikan bahwa aktivasi setelah *Inverted Dropout* memenuhi $\mathbb{E}[\mathbf{\tilde{a}}] = \mathbf{a}$.

**Langkah Penurunan Solusi:**
Diberikan vektor aktivasi sebelum dropout $\mathbf{a}$ dan vektor penutup Bernoulli $\mathbf{r} \sim \text{Bernoulli}(1-p)$, di mana:
$$P(r_i = 1) = 1 - p \quad \text{dan} \quad P(r_i = 0) = p$$
Lapisan *Inverted Dropout* mendefinisikan vektor keluaran sebagai:
$$\tilde{a}_i = \frac{a_i \cdot r_i}{1 - p}$$
Maka nilai ekspektasi dari $\tilde{a}_i$ adalah:
$$\mathbb{E}[\tilde{a}_i] = \mathbb{E}\left[ \frac{a_i \cdot r_i}{1 - p} \right] = \frac{a_i}{1 - p} \cdot \mathbb{E}[r_i]$$
Karena $r_i$ adalah peubah acak Bernoulli dengan parameter $(1 - p)$, maka nilai harapannya adalah:
$$\mathbb{E}[r_i] = 1 \cdot P(r_i = 1) + 0 \cdot P(r_i = 0) = 1 \cdot (1 - p) + 0 = 1 - p$$
Substitusikan kembali ke persamaan ekspektasi:
$$\mathbb{E}[\tilde{a}_i] = \frac{a_i}{1 - p} \cdot (1 - p) = a_i \quad \blacksquare$$
*Kesimpulan Pedagogis:* Dengan membagi aktivasi terpotong dengan faktor $(1-p)$ selama pelatihan, skala rata-rata magnitudo aktivasi tidak berubah. Oleh karena itu, pada saat inferensi, model dapat langsung menggunakan $\mathbf{a}$ murni tanpa penyesuaian bobot tambahan.

---

### 2.2 Solusi Kode Komputasi Lengkap: Proyek Mandiri Kromatografi Gas Minyak Atsiri
Berikut adalah implementasi acuan dosen untuk memvalidasi pengerjaan proyek mandiri mahasiswa:

```python
import numpy as np

class MandiriMinyakAtsiriEvaluator:
    """Implementasi solusi acuan instruktur untuk evaluasi model kromatografi gas minyak atsiri."""
    def __init__(self, n_features=80, n_samples=450):
        np.random.seed(101)
        self.X = np.random.randn(n_samples, n_features)
        # Menghasilkan multikolinearitas antar puncak kromatogram
        for j in range(1, 10):
            self.X[:, j] = 0.8 * self.X[:, j-1] + 0.2 * np.random.randn(n_samples)
        
        # Target kemurnian sitronelal (%)
        true_beta = np.zeros(n_features)
        true_beta[3] = 3.5
        true_beta[12] = -2.8
        true_beta[45] = 1.9
        self.y = np.dot(self.X, true_beta) + 50.0 + np.random.normal(0, 0.5, n_samples)
        self.y = self.y.reshape(-1, 1)

    def evaluate_weight_shrinkage(self, w_initial, w_final_unreg, w_final_reg):
        """Menghitung persentase kompresi norma bobot parameter."""
        norm_init = np.linalg.norm(w_initial)
        norm_unreg = np.linalg.norm(w_final_unreg)
        norm_reg = np.linalg.norm(w_final_reg)
        
        return {
            'norm_initial': norm_init,
            'norm_unreg': norm_unreg,
            'norm_reg': norm_reg,
            'shrinkage_ratio': (norm_unreg - norm_reg) / norm_unreg * 100.0
        }
```

---

## 3. Panduan Diagnostik & Solusi Penanganan Kendala Mahasiswa

Berikut adalah matriks diagnostik kendala teknis dan konseptual yang sering dialami mahasiswa selama praktikum:

| Gejala Kendala / Galat | Akar Penyebab (*Root Cause*) | Tindakan Korektif & Arahan Pedagogis |
| :--- | :--- | :--- |
| **Metrik data uji sangat buruk padahal galat pelatihan dan validasi sangat rendah.** | Mahasiswa lupa mengganti parameter `mode='eval'` saat melakukan prediksi pada data validasi/uji, sehingga *Dropout* tetap mematikan neuron secara acak. | Arahkan mahasiswa untuk memeriksa pemanggilan fungsi `.forward()`. Tunjukkan bahwa pada fase pengujian, masker dropout wajib dimatikan ($R = 1$) dan statistik *BatchNorm* wajib menggunakan `running_mean` dan `running_var`. |
| **Nilai fungsi rugi bernilai `NaN` saat mengaktifkan Batch Normalization.** | Pembagian dengan nol pada saat varians mini-batch $\sigma_{\mathcal{B}}^2$ bernilai sangat kecil atau nol, disebabkan tidak adanya konstanta stabilitas numerik $\epsilon$. | Pastikan penyebut pada standarisasi z-score memuat suku penstabil: `np.sqrt(var + 1e-5)`. |
| **Kurva galat validasi menunjukkan lonjakan osilasi liar saat menggunakan Dropout.** | *Dropout rate* ditetapkan terlalu agresif ($p > 0.6$) pada lapisan dengan neuron sedikit ($n \le 16$). | Berikan panduan empiris: untuk lapisan tersembunyi berukuran sedang-besar, nilai $p$ ideal adalah $0.2 - 0.5$. Pada lapisan masukan atau lapisan dengan simpul sedikit, hindari dropout tinggi. |
| **Early Stopping berhenti terlalu dini pada epoch awal (misal epoch 5).** | Ambang batas kesabaran (`patience`) disetel terlalu kecil (misal $patience = 2$) atau toleransi `min_delta` terlalu besar di tengah kurva yang masih fluktuatif. | Jelaskan konsep *warm-up*. Naikkan nilai `patience` menjadi $15 - 30$ epoch agar model memiliki kesempatan keluar dari lembah fluktuatif sebelum dihentikan paksa. |

---

## 4. Rubrik Asesmen Berbasis Kinerja (Holistik & Analitik)

| Dimensi Penilaian | Bobot (%) | Kriteria Sangat Memuaskan (85 - 100) | Kriteria Memuaskan (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Teori & Kalkulus (C2)** | 25% | Mampu menguraikan secara analitis penurunan gradien $L_1/L_2$, membuktikan invarian ekspektasi dropout, dan merumuskan operasi affine *BatchNorm*. | Memahami formula dasar tetapi terdapat ketidakakuratan kecil dalam penjelasan statistik berjalan atau sub-gradien $L_1$. | Tidak memahami perbedaan penalti $L_1$ vs $L_2$ dan salah mengartikan fungsi normalisasi batch. |
| **Keterampilan Pemrograman & Modularitas (C3)** | 35% | Kode NumPy modular, terstruktur dalam kelas yang rapi, transisi `train/eval` bekerja sempurna, notebook dieksekusi dengan 0 galat. | Kode berfungsi tetapi logika transisi inferensi belum sepenuhnya modular atau masih menggunakan variabel global. | Kode menghasilkan galat saat dieksekusi atau gagal menerapkan penskalaan balik $1/(1-p)$. |
| **Analisis Diagnostik & Solusi Lapangan (C4)** | 40% | Mahasiswa mampu membaca anomali kurva belajar, menjelaskan bukti penyusutan bobot, dan merumuskan strategi penanganan disparitas data agrokompleks secara kritis. | Mampu menganalisis kurva umum tetapi kurang mendalam dalam mengevaluasi interaksi Dropout dan BatchNorm. | Gagal menarik kesimpulan dari kurva evaluasi dan tidak mampu mengidentifikasi *overfitting*. |

---

## 5. Jembatan Pedagogis (Pedagogical Bridging) Menuju Bagian 9

Sebagai penutup Bagian 8, instruktur wajib menyampaikan rangkuman evaluatif perjalanan kurikulum:
1. Mahasiswa telah menguasai anatomi neuron dan keterbatasan XOR (Modul 8.1),
2. Memahami dinamika non-linearitas dan kapasitas representasi MLP (Modul 8.2),
3. Menguasai kalkulus propagasi maju dan formulasi *loss* (Modul 8.3),
4. Membedah tuntas penurunan gradien rantai kalkulus *Backpropagation* (Modul 8.4),
5. Menavigasi lanskap fungsi rugi menggunakan optimasi adaptif modern seperti Adam (Modul 8.5), serta
6. Menjinakkan kapasitas model dengan regularisasi komposit mutakhir (Modul 9.8).

**Pintu Gerbang Menuju Bagian 9:**  
Ajak mahasiswa berefleksi: *"Bagaimana jika input data kita adalah citra kanopi kelapa sawit berukuran $1000 \times 1000$ piksel berwarna RGB?"*  
Jika diratakan menjadi vektor MLP, input tersebut memiliki $3.000.000$ simpul! Satu lapisan tersembunyi dengan 1.000 neuron saja akan membutuhkan 3 miliar parameter bobot. Hal ini mustahil secara memori dan mengabaikan korelasi ketetanggaan spasial 2D.

Oleh karena itu, pada **Bagian 9: Visi Komputer & Jaringan Saraf Konvolusional (*Computer Vision & CNN*)**, mahasiswa akan diperkenalkan pada revolusi komputasi visual spasial melalui operasi konvolusi, *weight sharing*, dan ekstraksi fitur hirarkis yang menjadi tulang punggung revolusi kecerdasan buatan visual modern di sektor agrokompleks.
