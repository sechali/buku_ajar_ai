# AI Modul 8.3: Panduan Instruktur dan Kunci Solusi Komputasi
## Evaluasi Model

**Mata Kuliah:** Kecerdasan Buatan dalam Agrokompleks  
**Kode Mata Kuliah / SKS:** AGR-4108 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Semester Ganjil / Tahun Ke-4  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER Yogyakarta  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 8.3 menanamkan standar integritas saintifik dan ketelitian metodologis dalam menguji performa model *deep learning*. Instruktur bertugas mengikis kebiasaan mahasiswa yang hanya mengandalkan satu metrik tunggal (seperti akurasi atau MSE agregat) tanpa membedah keabsahan distribusi galat.

Poin penekanan pedagogis utama instruktur pada modul ini meliputi:
1. **Analisis Dekomposisi Bias-Variance:** Mahasiswa diarahkan untuk memahami bahwa galat total generalisasi adalah penjumlahan dari kuadrat bias (kekeliruan kapasitas model), varians (kerentanan terhadap fluktuasi sampel), dan derau acak tak tereduksi. Hal ini melatih mahasiswa mengetahui tindakan rekayasa apa yang harus diambil saat model gagal berkinerja baik.
2. **Pentingnya Pemeriksaan Residual (*Residual Diagnostics*):** Instruktur harus mendemonstrasikan bahwa sebuah model dapat memiliki nilai $R^2$ yang tinggi namun memiliki cacat tersembunyi berupa heteroskedastisitas (galat membesar pada rendemen tinggi).
3. **Standar Toleransi Operasional Industri:** Mahasiswa dibimbing untuk mengukur performa model bukan hanya secara matematis teoritis, tetapi dikaitkan dengan batas toleransi fisik operasional pabrik perkebunan (misal $\pm 0.8\%$ rendemen CPO).

### 1.2 Alokasi Waktu Pembelajaran (Total 380 Menit)
1. **Kuliah Teori Interaktif (100 Menit):**
   - 00–25 Menit: Landasan matematis dekomposisi *Bias-Variance Tradeoff* dan batas derau acak tak tereduksi.
   - 25–55 Menit: Metrik evaluasi regresi (RMSE, MAE, MAPE, $R^2$) vs metrik klasifikasi (Confusion Matrix, ROC-AUC, PR-AUC).
   - 55–80 Menit: Asumsi klasik residual (homoskedastisitas, normalitas Q-Q, uji Shapiro-Wilk).
   - 80–100 Menit: Metodologi pengujian stres ketahanan (*robustness stress testing*) terhadap gangguan instrumen lapangan.
2. **Sesi Praktikum Komputasi Mandiri Laboratorium (180 Menit):**
   - 00–30 Menit: Pengujian inferensi data uji independen (Afdeling 9 dan 10) menggunakan `model.eval()`.
   - 30–80 Menit: Kalkulasi metrik kuantitatif dan visualisasi panel ganda (*Actual vs Pred* dan *Residual vs Fitted*).
   - 80–130 Menit: Uji hipotesis statistik formal (uji Shapiro-Wilk dan korelasi rank Spearman).
   - 130–180 Menit: Rekayasa modul uji stres derau Gaussian dan analisis kurva degradasi performa.
3. **Refleksi & Diskusi Evaluasi HOTS (100 Menit):**
   - Pembahasan studi kasus mandiri audit kelayakan deployment pabrik kelapa sawit, bedah anomali residual, dan evaluasi rubrik asesmen.

---

## 2. Kunci Solusi Komprehensif Tugas & Proyek Mandiri Mahasiswa

### 2.1 Solusi Penurunan Analitis Dekomposisi Bias-Variance
Mahasiswa diminta membuktikan secara analitis bahwa ekspektasi galat kuadratik prediksi terdekomposisi menjadi kuadrat bias, varians, dan derau intrinsik.

**Langkah Penurunan Solusi:**
Diberikan target sejati $y = f(\mathbf{x}) + \epsilon$, dengan $\mathbb{E}[\epsilon] = 0$ dan $\text{Var}(\epsilon) = \sigma_{\epsilon}^2$.  
Estimator yang dihasilkan oleh algoritma pada himpunan data latih $\mathcal{D}$ dinotasikan sebagai $\hat{f}(\mathbf{x})$.  
Maka ekspektasi galat kuadratik terhadap distribusi himpunan data dan derau adalah:
$$\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] = \mathbb{E}[ (f(\mathbf{x}) + \epsilon - \hat{f}(\mathbf{x}))^2 ]$$
Tambahkan dan kurangkan suku $\mathbb{E}[\hat{f}(\mathbf{x})]$:
$$\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] = \mathbb{E}\left[ \Big( (f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})]) + (\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x})) + \epsilon \Big)^2 \right]$$
Ekspansikan bentuk kuadrat trinomial tersebut:
$$\begin{aligned}
\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] &= (f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2 + \mathbb{E}[(\hat{f}(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2] + \mathbb{E}[\epsilon^2] \\
&\quad + 2(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})]) \cdot \mathbb{E}[\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x})] \\
&\quad + 2(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})]) \cdot \mathbb{E}[\epsilon] \\
&\quad + 2\mathbb{E}[(\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x})) \cdot \epsilon]
\end{aligned}$$
Karena:
1. $\mathbb{E}[\mathbb{E}[\hat{f}(\mathbf{x})] - \hat{f}(\mathbf{x})] = \mathbb{E}[\hat{f}(\mathbf{x})] - \mathbb{E}[\hat{f}(\mathbf{x})] = 0$,
2. $\mathbb{E}[\epsilon] = 0$, dan derau $\epsilon$ independen terhadap model estimator $\hat{f}$, sehingga seluruh suku perkalian silang bernilai nol.
3. $\mathbb{E}[\epsilon^2] = \text{Var}(\epsilon) = \sigma_{\epsilon}^2$.

Maka persamaan menyisakan tiga suku murni:
$$\mathbb{E}[(y - \hat{f}(\mathbf{x}))^2] = \underbrace{(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2}_{\text{Bias}[\hat{f}(\mathbf{x})]^2} + \underbrace{\mathbb{E}[(\hat{f}(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2]}_{\text{Var}[\hat{f}(\mathbf{x})]} + \underbrace{\sigma_{\epsilon}^2}_{\text{Derau Tak Tereduksi}} \quad \blacksquare$$
*Kesimpulan Pedagogis:* Persamaan ini membuktikan bahwa tidak ada model yang dapat mencapai galat lebih rendah dari $\sigma_{\epsilon}^2$. Rekayasa arsitektur dan regularisasi bertujuan mencari titik keseimbangan optimal antara bias dan varians.

---

### 2.2 Solusi Kode Komputasi Proyek Mandiri: Audit Kelayakan Pabrik
Berikut adalah implementasi acuan instruktur untuk memvalidasi pengerjaan proyek mandiri mahasiswa:

```python
import numpy as np
import scipy.stats as stats

class PalmFactoryModelAudit:
    """Implementasi solusi acuan instruktur untuk audit kelayakan pabrik kelapa sawit."""
    def __init__(self, y_true, y_pred, threshold_tolerance=0.8):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.residuals = self.y_true - self.y_pred
        self.tol = threshold_tolerance

    def generate_executive_audit_report(self):
        rmse = np.sqrt(np.mean(self.residuals**2))
        mae = np.mean(np.abs(self.residuals))
        r2 = 1.0 - np.sum(self.residuals**2) / np.sum((self.y_true - np.mean(self.y_true))**2)
        compliance = np.mean(np.abs(self.residuals) <= self.tol) * 100.0
        
        # Uji normalitas residual
        _, p_norm = stats.shapiro(self.residuals)
        
        # Uji korelasi residual terhadap nilai target (bias rentang)
        corr_bias, p_bias = stats.spearmanr(self.residuals, self.y_true)
        
        is_deployable = (compliance >= 80.0) and (p_norm > 0.01) and (abs(corr_bias) < 0.3)
        
        return {
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2,
            'Compliance_Rate_Pct': compliance,
            'Normality_p_val': p_norm,
            'Range_Bias_Corr': corr_bias,
            'Deployment_Recommendation': "LAYAK DEPLOY" if is_deployable else "PERLU PENALAAN ULANG"
        }
```

---

## 3. Panduan Diagnostik & Solusi Penanganan Kendala Mahasiswa

Berikut adalah matriks diagnostik kendala teknis dan konseptual yang sering dialami mahasiswa selama praktikum:

| Gejala Kendala / Galat | Akar Penyebab (*Root Cause*) | Tindakan Korektif & Arahan Pedagogis |
| :--- | :--- | :--- |
| **Nilai $R^2$ bernilai negatif (misal $R^2 = -1.5$).** | Mahasiswa kebingungan mengapa $R^2$ bisa negatif. Hal ini terjadi karena model menghasilkan prediksi yang sangat buruk di luar distribusi data latih, sehingga jumlah kuadrat residualnya lebih besar dibanding memprediksi rata-rata konstan $\bar{y}$. | Jelaskan arti matematis $R^2$: ingatkan bahwa $R^2$ mengukur peningkatan performa terhadap garis horizontal rata-rata; periksa apakah standarisasi fitur data uji telah menggunakan parameter $\mu$ dan $\sigma$ data latih yang benar. |
| **Plot residual memperlihatkan bentuk kurva parabola atau huruf 'U'.** | Jaringan saraf tiruan kekurangan kapasitas non-linier atau fitur masukan kuadratik krusial belum terakomodasi (*High Bias / Underfitting*). | Arahkan mahasiswa untuk menambah jumlah neuron pada lapisan tersembunyi atau melatih model dengan laju belajar yang lebih adaptif. |
| **Uji Shapiro-Wilk menghasilkan $p$-value sangat kecil ($p < 0.001$).** | Terdapat beberapa pencilan data uji ekstrem yang merusak simetri distribusi galat. | Tunjukkan cara mengidentifikasi titik pencilan pada plot residual dan diskusikan apakah pencilan tersebut berasal dari kesalahan instrumen sensor atau buah sawit yang memang busuk. |
| **Model runtuh total saat diuji stres dengan derau kecil ($\sigma = 0.02$).** | Model mengalami *overfitting* pada kombinasi pita spektral tertentu yang sangat sensitif tanpa dibekali regularisasi Dropout saat pelatihan. | Tekankan pentingnya lapisan *Dropout* dan *Weight Decay* yang telah dipelajari pada Modul 8.6 untuk menjaga ketahanan (*noise immunity*). |

---

## 4. Rubrik Asesmen Berbasis Kinerja (Holistik & Analitik)

| Dimensi Penilaian | Bobot (%) | Kriteria Sangat Memuaskan (85 - 100) | Kriteria Memuaskan (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Teori Dekomposisi Galat (C2)** | 25% | Mampu menurunkan pembuktian analitis Bias-Variance, menjelaskan asumsi homoskedastisitas, serta menguraikan implikasi metrik industri secara presisi. | Memahami konsep dasar dekomposisi galat namun penurunan matematis trinomial atau uji normalitas residual kurang lengkap. | Gagal menjelaskan peran bias vs varians atau salah mengartikan rumus $R^2$. |
| **Implementasi Suite Audit & Visualisasi (C3)** | 35% | Mengonstruksi modul evaluasi komprehensif, visualisasi residual panel ganda, dan modul uji stres derau secara modular dan bebas galat. | Kode evaluasi berjalan baik tetapi visualisasi belum menyertakan koridor toleransi industri atau uji stres belum otomatis. | Program menghasilkan galat runtime atau evaluasi dilakukan pada data yang bocor. |
| **Analisis Diagnostik & Solusi Lapangan (C4)** | 40% | Mahasiswa mampu membaca anomali corong residual, mengevaluasi kurva degradasi uji stres, dan merumuskan kelayakan deployment industri secara kritis. | Mampu menganalisis metrik dasar namun interpretasi uji ketahanan terhadap derau sensor belum mendalam. | Gagal menginterpretasikan plot residual atau mengabaikan keberadaan heteroskedastisitas. |

---

## 5. Jembatan Pedagogis (Pedagogical Bridging) Menuju Modul 8.10

Sebagai penutup sesi praktikum Modul 8.3, instruktur memandu refleksi kritis mahasiswa:  
*"Kita telah memiliki audit kinerja yang sangat lengkap: kita tahu persis nilai RMSE model kita adalah 0.67%, 73% sampel memenuhi batas toleransi industri, residual berdistribusi normal, dan model tahan terhadap derau hingga deviasi 0.05. Tetapi bayangkan Anda sedang mempresentasikan hasil ini di hadapan Kepala Agronomi Perkebunan. Pertanyaan pertama beliau bukanlah berapa RMSE Anda, melainkan: **Mengapa model Anda menyimpulkan bahwa blok kebun ini akan menghasilkan rendemen rendah? Sensor apa yang mendasarinya?**"*

Jika kita hanya menjawab bahwa model terdiri dari ribuan perkalian matriks non-linier, para agronom tidak akan mempercayai rekomendasi AI kita. Di sinilah pentingnya **Explainable AI (XAI)**.

Oleh karena itu, pada **AI Modul 8.10: Interpretasi Hasil & Transparansi Model (*Explainable AI*)**, mahasiswa akan dibimbing untuk membuka isi "kotak hitam" jaringan saraf tiruan: mengukur tingkat kepentingan fitur (*Permutation Feature Importance*), melacak atribusi gradien ke setiap panjang gelombang (*Gradient-based Saliency*), dan memetakan ruang representasi tersembunyi dengan t-SNE untuk membuktikan bahwa JST benar-benar mempelajari konsep biologis tanaman kelapa sawit secara cerdas.
