# AI Modul 8.5: Panduan Instruktur dan Kunci Solusi Komputasi
## Pembuatan Sistem Prediksi Sederhana

**Mata Kuliah:** Kecerdasan Buatan dalam Agrokompleks  
**Kode Mata Kuliah / SKS:** AGR-4108 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Semester Ganjil / Tahun Ke-4  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER Yogyakarta  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 8.5 merupakan modul pamungkas dari seluruh rangkaian kurikulum *Deep Learning & Jaringan Saraf Tiruan* (Bagian 8). Sasaran instruktur pada modul ini adalah mengantarkan mahasiswa melintasi batas antara "eksperimen riset akademik" menuju "rekayasa produk teknologi siap pakai (*production-grade engineering*)".

Tiga pilar pedagogis utama yang wajib ditekankan oleh instruktur adalah:
1. **Pemisahan Graf dari Kode Sumber Python (*Portability*):** Mahasiswa dibimbing memahami bahwa di lingkungan industri nyata, server inferensi tidak selalu menjalankan Python penuh. Kompilasi TorchScript JIT mengonversi model menjadi representasi graf C++ yang dapat dieksekusi secara instan, aman, dan berlatensi ultra-rendah.
2. **Kekebalan Masukan (*Input Guardrails*):** Menanamkan prinsip kehati-hatian rekayasa bahwa masukan dari pengguna dan sensor lapangan tidak pernah dapat dipercaya $100\%$. Sistem inferensi wajib dibekali fungsi sanitasi dan validasi batas fisik agronomi sebelum tensor dialirkan ke model.
3. **Penyatuan Siklus Hidup Penuh (*Full-Cycle Integration*):** Memandu mahasiswa melihat benang merah utuh: bagaimana data yang dibersihkan pada Modul 8.7, dilatih pada Modul 8.8, diaudit pada Modul 8.9, dan diverifikasi transparan pada Modul 8.10, kini bermuara menjadi aplikasi prediksi yang memberikan nilai tambah ekonomi nyata bagi pabrik kelapa sawit.

### 1.2 Alokasi Waktu Pembelajaran (Total 380 Menit)
1. **Kuliah Teori Interaktif (100 Menit):**
   - 00–25 Menit: Arsitektur *deployment* kecerdasan buatan, trade-off latensi komputasi vs throughput, dan anatomi TorchScript JIT compiler.
   - 25–55 Menit: Teknik *Tracing* (`torch.jit.trace`) vs *Scripting* (`torch.jit.script`) dan isolasi scaler terbekukan (*frozen scaler state*).
   - 55–80 Menit: Perancangan filter validasi masukan fisis (*input guardrails*) dan pasca-pemrosesan kategori mutu bisnis (*grading rules*).
   - 80–100 Menit: Bedah arsitektur antarmuka pengguna interaktif (CLI dan Web Streamlit/Gradio) untuk operator sortasi pabrik.
2. **Sesi Praktikum Komputasi Mandiri Laboratorium (180 Menit):**
   - 00–30 Menit: Pelatihan dan penyimpanan bobot model PyTorch `oilpalm_trained_model.pt`.
   - 30–80 Menit: Kompilasi dan ekspor model ke format TorchScript `oilpalm_predictor_jit.pt` serta verifikasi ekuivalensi numerik output.
   - 80–130 Menit: Konstruksi kelas mandiri `OilPalmInferencePipeline` lengkap dengan filter validasi dan pasca-pemrosesan mutu.
   - 130–180 Menit: Pengujian 3 skenario lapangan (unggul, rendah, cacat sensor) dan benchmark latensi komputasi (Eager vs TorchScript).
3. **Refleksi & Diskusi Evaluasi HOTS (100 Menit):**
   - Presentasi proyek mandiri prototipe antarmuka sortasi kelapa sawit, evaluasi menyeluruh Bagian 8, dan pengantar menuju Bagian 9 (Computer Vision & CNN).

---

## 2. Kunci Solusi Komprehensif Tugas & Proyek Mandiri Mahasiswa

### 2.1 Solusi Pembuktian Analitis Ekuivalensi Numerik TorchScript
Mahasiswa diminta membuktikan secara konseptual mengapa penelusuran graf (*tracing*) pada model linier-sekuensial menghasilkan keluaran numerik yang identik dengan mode PyTorch Eager.

**Langkah Penjelasan Solusi:**
Dalam mode PyTorch Eager, evaluasi model $f(\mathbf{x}) = \mathbf{W}_2 \cdot \text{ReLU}(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1) + \mathbf{b}_2$ dieksekusi melalui pemanggilan runtime interpreter Python untuk setiap baris operasi:
1. Interpreter memanggil binding C++ untuk perkalian matriks $\mathbf{W}_1 \mathbf{x}$,
2. Mengembalikan objek Python baru untuk penjumlahan bias $\mathbf{b}_1$,
3. Memanggil fungsi aktivasi ReLU dengan alokasi tensor baru,
4. Mengulangi langkah serupa untuk lapisan kedua.

Ketika dilakukan *tracing* via `torch.jit.trace(model, dummy_input)`:
1. Kompilator JIT mengeksekusi operasi sekali dengan tensor dummy dan mencatat urutan primitif C++ ATen (*A Tensor Library*) yang terpanggil ke dalam graf perantara (*Intermediate Representation* / IR Node).
2. Di dalam IR, struktur graf direduksi: operator perkalian matriks dan bias digabungkan (*operator fusion*: $\text{Gemm} / \text{Linear}$), alokasi memori tensor perantara disiapkan secara statis, dan seluruh interpreter Python dilewati.
3. Karena operasi matematika yang dijalankan pada level instruksi prosesor adalah perkalian akumulasi titik (*dot-product*) FP32 yang identik tanpa aproksimasi stokastik (dengan `model.eval()`), maka nilai keluaran $f_{\text{Eager}}(\mathbf{x}) \equiv f_{\text{JIT}}(\mathbf{x})$ hingga batas presisi mesin floating-point ($\Delta < 10^{-7}$). $\blacksquare$

---

### 2.2 Solusi Kode Komputasi Proyek Mandiri: Production Inference Service
Berikut adalah implementasi acuan instruktur untuk memvalidasi pengerjaan proyek mandiri mahasiswa:

```python
import torch
import numpy as np

class ProductionInferenceService:
    """Implementasi acuan instruktur untuk layanan inferensi sortasi mandiri."""
    def __init__(self, jit_path, mu_train, sigma_train):
        self.engine = torch.jit.load(jit_path)
        self.engine.eval()
        self.mu = np.array(mu_train, dtype=np.float32).reshape(1, -1)
        self.sigma = np.array(sigma_train, dtype=np.float32).reshape(1, -1)
        self.sigma[self.sigma == 0] = 1.0

    def process_field_batch(self, csv_array):
        """Memproses batch data truk panen kelapa sawit secara massal."""
        results = []
        for idx, row in enumerate(csv_array):
            try:
                # 1. Validasi
                if np.isnan(row).any():
                    results.append({'truk_id': idx+1, 'status': 'DITOLAK', 'alasan': 'Data sensor kosong'})
                    continue
                if row[120] < 3.5 or row[120] > 8.5:
                    results.append({'truk_id': idx+1, 'status': 'DITOLAK', 'alasan': 'pH tanah anomali'})
                    continue
                    
                # 2. Transformasi & Prediksi
                norm_row = (row.reshape(1, -1) - self.mu) / (self.sigma + 1e-8)
                tensor_row = torch.tensor(norm_row, dtype=torch.float32)
                
                with torch.no_grad():
                    pred_cpo = self.engine(tensor_row).item()
                    
                # 3. Kategori Mutu
                grade = "Grade A" if pred_cpo >= 23.0 else ("Grade B" if pred_cpo >= 21.0 else "Grade C")
                results.append({
                    'truk_id': idx+1,
                    'status': 'DITERIMA',
                    'rendemen_cpo': round(pred_cpo, 2),
                    'grade': grade
                })
            except Exception as e:
                results.append({'truk_id': idx+1, 'status': 'ERROR', 'alasan': str(e)})
                
        return results
```

---

## 3. Panduan Diagnostik & Solusi Penanganan Kendala Mahasiswa

Berikut adalah matriks diagnostik kendala teknis dan konseptual yang sering dialami mahasiswa selama praktikum:

| Gejala Kendala / Galat | Akar Penyebab (*Root Cause*) | Tindakan Korektif & Arahan Pedagogis |
| :--- | :--- | :--- |
| **`TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect`** | Model memuat pernyataan kondisi berbasis Python murni (seperti `if x.sum() > 0:`) yang tidak dapat direkam secara statis oleh *tracing*. | Arahkan mahasiswa untuk mengganti pernyataan `if` dinamis dengan operasi tensor PyTorch (`torch.where`) atau beralih ke `torch.jit.script`. |
| **Prediksi model TorchScript menghasilkan nilai acak yang berubah-ubah pada input yang sama.** | Mahasiswa memanggil `torch.jit.trace` saat model masih dalam status `model.train()`, sehingga lapisan *Dropout* terekam aktif di dalam graf TorchScript. | Tegaskan bahwa sebelum proses tracing dilakukan, pemanggilan `model.eval()` adalah mutlak wajib dieksekusi. |
| **Galat pembagian nol atau nilai `inf` saat menstandarisasi sampel baru.** | Terdapat fitur konstan pada data latih yang memiliki nilai standar deviasi $\sigma = 0$. | Tunjukkan cara menambahkan konstanta stabilitas: `sigma[sigma == 0] = 1.0` dan penambahan $\epsilon = 10^{-8}$ pada penyebut. |
| **Antarmuka GUI web mengalami kelambatan (*lag*) parah saat memproses sampel.** | Mahasiswa memuat model TorchScript (`torch.jit.load`) di dalam fungsi tombol prediksi berulang kali setiap kali tombol diklik. | Arahkan mahasiswa untuk menginisialisasi model di luar fungsi interaksi (lakukan pemuatan model satu kali di memori pada saat aplikasi pertama kali dijalankan). |

---

## 4. Rubrik Asesmen Berbasis Kinerja (Holistik & Analitik)

| Dimensi Penilaian | Bobot (%) | Kriteria Sangat Memuaskan (85 - 100) | Kriteria Memuaskan (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Teori Deployment & JIT (C2)** | 25% | Mampu menguraikan arsitektur graf TorchScript IR, membedakan tracing vs scripting, dan menjelaskan prinsip eliminasi overhead Python secara presisi. | Memahami alur kerja ekspor model dengan baik namun penjelasan teknis kompilasi graf C++ kurang mendalam. | Gagal menjelaskan peran serialisasi model atau tidak memahami fungsi `model.eval()`. |
| **Konstruksi Pipeline & Validasi Masukan (C3)** | 35% | Mengonstruksi modul inferensi end-to-end yang memadukan filter validasi fisis, scaler terbekukan, ekspor TorchScript bebas galat, dan pasca-pemrosesan mutu. | Pipeline inferensi berjalan baik namun filter validasi masukan belum mencakup batas fisik sensor tanah. | Program gagal dikompilasi ke TorchScript atau tidak ada mekanisme penanganan data rusak. |
| **Rekayasa Antarmuka & Analisis Latensi (C4)** | 40% | Mahasiswa berhasil merakit prototipe antarmuka yang elegan, membuktikan efisiensi percepatan latensi, dan mengevaluasi keandalan sistem sortasi secara kritis. | Antarmuka berfungsi baik namun analisis komparasi latensi belum disajikan secara kuantitatif. | Antarmuka mengalami crash saat diuji dengan data anomali atau latensi tidak diukur. |

---

## 5. Jembatan Pedagogis (Pedagogical Bridging) Puncak Menuju Bagian 9

Sebagai penutup paripurna dari seluruh rangkaian **Bagian 8: Deep Learning & Jaringan Saraf Tiruan**, instruktur menyampaikan pidato refleksi kurikulum yang menghubungkan pencapaian mahasiswa dengan tantangan teknologi berikutnya:

*"Selamat kepada seluruh mahasiswa! Kalian telah menempuh perjalanan rekayasa kecerdasan buatan yang luar biasa: mulai dari merakit neuron perceptron biologis dari nol, membedah kalkulus aturan rantai backpropagation, menaklukkan algoritma optimasi Adam, mendisiplinkan model dengan regularisasi komposit, hingga mengemas alur kerja penuh dari preprocessing, training, audit diagnostik, XAI, sampai sistem inferensi TorchScript siap pakai untuk pabrik kelapa sawit.*

*Namun, pandanglah sejenak batasan model yang telah kita bangun: seluruh input kita berupa deretan angka 1 dimensi tabular. Jika besok pagi manajemen perkebunan meminta kalian membangun sistem penglihatan robotik yang dapat mendeteksi pohon kelapa sawit terinfeksi jamur Ganoderma langsung dari rekaman video drone beresolusi tinggi 4K—apakah model MLP 1D ini dapat menyelesaikannya?*

*Meratakan citra 4K menjadi satu vektor panjang akan menghasilkan 24 juta simpul masukan, menghancurkan topologi spasial ketetanggaan piksel, dan meledakkan kebutuhan memori hingga ratusan gigabyte.*

*Oleh karena itu, bersiaplah untuk melangkah ke babak revolusi komputasi visual berikutnya: **Bagian 9: Visi Komputer & Jaringan Saraf Konvolusional (Computer Vision & CNN)**. Di sana, kita akan mempelajari bagaimana operator konvolusi spasial 2D, pembagian parameter bobot (*weight sharing*), dan ekstraksi fitur visual hirarkis memungkinkan kecerdasan buatan 'melihat' perkebunan dengan ketajaman mata manusia!"*
