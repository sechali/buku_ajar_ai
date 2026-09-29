# AI Modul 8.2: Panduan Instruktur dan Kunci Solusi Komputasi
## Training Model

**Mata Kuliah:** Kecerdasan Buatan dalam Agrokompleks  
**Kode Mata Kuliah / SKS:** AGR-4108 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Semester Ganjil / Tahun Ke-4  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER Yogyakarta  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 8.2 berfokus pada transisi mahasiswa dari sekadar memahami persamaan matematika menjadi pengembang sistem kecerdasan buatan yang mampu mengorkestrasi siklus pelatihan berskala produksi.

Tiga pilar pedagogis utama yang wajib ditekankan oleh instruktur adalah:
1. **Disiplin State Model (`train()` vs `eval()`):** Mahasiswa sering mengabaikan fakta bahwa lapisan *Dropout* dan *Batch Normalization* mengubah perilaku komputasinya secara drastis antara pelatihan dan evaluasi. Instruktur harus membuktikan bahwa lupa mengubah status model menghasilkan evaluasi yang cacat.
2. **Kestabilan Aliran Gradien (*Gradient Stability*):** Data agrokompleks sering memuat anomali sensorik yang menghasilkan lonjakan gradien sesaat. Mahasiswa diarahkan untuk selalu menyertakan pemotongan gradien global (`clip_grad_norm_`) sebagai sabuk pengaman komputasi.
3. **Penyelamatan Bobot Teroptimal (*Model Checkpointing*):** Menanamkan prinsip bahwa epoch terakhir pelatihan jarang sekali merupakan model terbaik. Mahasiswa dilatih membuat mekanisme otomatis yang menyimpan kamus bobot (`state_dict`) setiap kali metrik validasi mencatatkan rekor terbaik baru.

### 1.2 Alokasi Waktu Pembelajaran (Total 380 Menit)
1. **Kuliah Teori Interaktif (100 Menit):**
   - 00–25 Menit: Anatomi siklus pelatihan modern, alur graf komputasi terarah, dan teorema konvergensi Robbins-Monro.
   - 25–55 Menit: Landasan matematis *Gradient Clipping* (norma $\ell_2$ global) dan penjadwalan laju belajar adaptif (`ReduceLROnPlateau`).
   - 55–80 Menit: Manajemen memori graf dengan `torch.no_grad()` dan mekanisme serialisasi *checkpoint*.
   - 80–100 Menit: Diskusi interaktif mengenai galat umum pemrograman PyTorch (*silent bugs* seperti lupa `zero_grad`).
2. **Sesi Praktikum Komputasi Mandiri Laboratorium (180 Menit):**
   - 00–30 Menit: Penghubungan DataLoader terpadu dari Modul 8.7 ke arsitektur PyTorch `OilPalmYieldMLP`.
   - 30–90 Menit: Konstruksi kelas mandiri `DeepLearningTrainer` lengkap dengan fungsi isolasi autograd dan pemotongan gradien.
   - 90–150 Menit: Pelatihan model selama 50 epoch dan visualisasi kurva evaluasi serta dinamika penurunan laju belajar.
   - 150–180 Menit: Pemulihan bobot terbaik dari file `best_oilpalm_model.pt` dan evaluasi generalisasi pada data uji independen.
3. **Refleksi & Diskusi Evaluasi HOTS (100 Menit):**
   - Pembahasan kunci solusi proyek mandiri prediksi pigmen daun multi-output, analisis perbandingan laju belajar tetap vs adaptif, dan evaluasi rubrik asesmen.

---

## 2. Kunci Solusi Komprehensif Tugas & Proyek Mandiri Mahasiswa

### 2.1 Solusi Pembuktian Analitis Sifat Invarian Arah Gradient Clipping
Mahasiswa diminta membuktikan bahwa pemotongan gradien berbasis norma $\ell_2$ global tidak mengubah arah vektor gradien, melainkan hanya membatasi panjang langkahnya.

**Langkah Penurunan Solusi:**
Diberikan vektor gradien global $\mathbf{g} \in \mathbb{R}^P$ dan ambang batas skalar $\theta > 0$.  
Arah dari vektor gradien didefinisikan oleh vektor satuan (*unit vector*):
$$\hat{\mathbf{u}}_{\mathbf{g}} = \frac{\mathbf{g}}{\|\mathbf{g}\|_2}$$
Ketika norma gradien melebihi ambang batas ($\|\mathbf{g}\|_2 > \theta$), aturan pemotongan menetapkan:
$$\mathbf{g}_{\text{clipped}} = \frac{\theta}{\|\mathbf{g}\|_2} \mathbf{g} = \theta \cdot \left( \frac{\mathbf{g}}{\|\mathbf{g}\|_2} \right) = \theta \cdot \hat{\mathbf{u}}_{\mathbf{g}}$$
Arah dari vektor gradien yang telah dipotong adalah:
$$\hat{\mathbf{u}}_{\mathbf{g}_{\text{clipped}}} = \frac{\mathbf{g}_{\text{clipped}}}{\|\mathbf{g}_{\text{clipped}}\|_2} = \frac{\theta \cdot \hat{\mathbf{u}}_{\mathbf{g}}}{\|\theta \cdot \hat{\mathbf{u}}_{\mathbf{g}}\|_2} = \frac{\theta \cdot \hat{\mathbf{u}}_{\mathbf{g}}}{\theta \cdot \|\hat{\mathbf{u}}_{\mathbf{g}}\|_2} = \frac{\hat{\mathbf{u}}_{\mathbf{g}}}{1} = \hat{\mathbf{u}}_{\mathbf{g}} \quad \blacksquare$$
*Kesimpulan Pedagogis:* Persamaan di atas membuktikan secara mutlak bahwa $\hat{\mathbf{u}}_{\mathbf{g}_{\text{clipped}}} \equiv \hat{\mathbf{u}}_{\mathbf{g}}$. Optimasi penurunan gradien tetap bergerak ke arah penurunan tercepat yang sama persis seperti yang dihitung oleh kalkulus *backpropagation*, namun magnitudo langkah dibatasi secara aman paling tinggi sebesar $\theta$.

---

### 2.2 Solusi Kode Komputasi Proyek Mandiri: Multi-Output Pigment Net
Berikut adalah implementasi acuan instruktur untuk memvalidasi pengerjaan proyek mandiri mahasiswa:

```python
import torch
import torch.nn as nn
import torch.optim as optim

class DeepPigmentNet(nn.Module):
    """Arsitektur multi-output untuk estimasi klorofil dan karotenoid."""
    def __init__(self, in_features=155, hidden=64, out_features=3):
        super(DeepPigmentNet, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(in_features, hidden),
            nn.BatchNorm1d(hidden),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Dropout(p=0.15),
            
            nn.Linear(hidden, hidden // 2),
            nn.BatchNorm1d(hidden // 2),
            nn.LeakyReLU(negative_slope=0.01),
            
            nn.Linear(hidden // 2, out_features)
        )
        
    def forward(self, x):
        return self.network(x)

def run_modular_training(model, train_loader, val_loader, epochs=40):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.003, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=3, factor=0.3)
    
    best_loss = float('inf')
    
    for epoch in range(1, epochs + 1):
        # 1. Training Phase
        model.train()
        for bx, by in train_loader:
            bx, by = bx.to(device), by.to(device)
            optimizer.zero_grad()
            preds = model(bx)
            loss = criterion(preds, by)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.5)
            optimizer.step()
            
        # 2. Validation Phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for bx, by in val_loader:
                bx, by = bx.to(device), by.to(device)
                preds = model(bx)
                val_loss += criterion(preds, by).item() * bx.size(0)
        avg_val_loss = val_loss / len(val_loader.dataset)
        
        # 3. Scheduler & Checkpoint
        scheduler.step(avg_val_loss)
        if avg_val_loss < best_loss:
            best_loss = avg_val_loss
            torch.save({'model': model.state_dict(), 'loss': best_loss}, 'best_pigment_net.pt')
            
    return best_loss
```

---

## 3. Panduan Diagnostik & Solusi Penanganan Kendala Mahasiswa

Berikut adalah matriks diagnostik kendala teknis dan konseptual yang sering dialami mahasiswa selama praktikum:

| Gejala Kendala / Galat | Akar Penyebab (*Root Cause*) | Tindakan Korektif & Arahan Pedagogis |
| :--- | :--- | :--- |
| **Nilai loss tidak kunjung turun atau langsung melonjak menjadi `NaN` pada epoch pertama.** | Mahasiswa lupa memanggil `optimizer.zero_grad()` sebelum `loss.backward()`, mengakibatkan gradien terakumulasi terus menerus hingga meledak. | Wajibkan mahasiswa memeriksa urutan eksekusi: selalu letakkan `optimizer.zero_grad()` tepat sebelum evaluasi `loss.backward()`. |
| **Galat `CUDA out of memory` muncul setelah beberapa epoch berjalan.** | Mahasiswa lupa menyertakan blok `with torch.no_grad():` saat loop validasi, atau melakukan penambahan loss menggunakan `running_loss += loss` (menyimpan seluruh graf autograd) alih-alih `loss.item()`. | Jelaskan perbedaan antara tensor graf dan skalar float murni: gunakan `loss.item()` saat akumulasi metrik log dan bungkus validasi dengan `torch.no_grad()`. |
| **Laju pembelajaran tidak pernah turun padahal kurva validasi sudah stagnan puluhan epoch.** | Penjadwal `ReduceLROnPlateau` dipanggil tanpa memasukkan argumen metrik validasi, atau parameter `mode` salah disetel (`mode='max'` untuk MSE). | Ingatkan bahwa untuk metrik kerugian (MSE/Loss), parameter wajib disetel `mode='min'` dan panggilan harus menyertakan metrik: `scheduler.step(val_loss)`. |
| **Model yang dimuat dari file `.pt` menghasilkan prediksi acak saat diuji.** | Mahasiswa lupa memanggil `model.eval()` setelah memulihkan bobot dari checkpoint, sehingga *Dropout* tetap mematikan simpul secara stokastik. | Tegaskan kembali bahwa setiap kali model dipulihkan untuk inferensi, baris perintah `model.eval()` adalah mutlak wajib dijalankan. |

---

## 4. Rubrik Asesmen Berbasis Kinerja (Holistik & Analitik)

| Dimensi Penilaian | Bobot (%) | Kriteria Sangat Memuaskan (85 - 100) | Kriteria Memuaskan (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Teori Alur Pelatihan (C2)** | 25% | Mampu menguraikan secara analitis invarian arah pemotongan gradien, formulasi peluruhan laju belajar adaptif, serta mekanisme alokasi memori autograd. | Memahami alur kerja pelatihan dengan baik namun penjelasan analitis pemotongan gradien atau kondisi Robbins-Monro kurang lengkap. | Gagal menjelaskan peran `zero_grad()` atau salah memahami fungsi kerja *learning rate scheduler*. |
| **Konstruksi Pipeline & Modularitas PyTorch (C3)** | 35% | Mengonstruksi kelas pelatihan modular yang mengintegrasikan `clip_grad_norm_`, scheduler, dan mekanisme serialisasi *checkpoint* secara bebas galat. | Pipeline pelatihan berjalan baik namun penanganan checkpoint atau perekaman log metrik belum sepenuhnya rapi. | Program menghasilkan galat runtime atau lupa menonaktifkan gradien pada saat validasi. |
| **Analisis Diagnostik & Solusi Konvergensi (C4)** | 40% | Mahasiswa mampu membaca anomali osilasi loss, menganalisis efek adaptasi laju belajar, dan membuktikan keunggulan checkpoint terbaik dibanding epoch terakhir. | Mampu menganalisis kurva konvergensi dasar namun interpretasi efek pemotongan gradien belum komprehensif. | Tidak mampu menginterpretasikan grafik konvergensi atau membiarkan model mengalami divergensi gradien. |

---

## 5. Jembatan Pedagogis (Pedagogical Bridging) Menuju Modul 8.9

Sebagai penutup sesi praktikum Modul 8.2, instruktur mengajak mahasiswa untuk merefleksikan pencapaian yang telah diraih:  
*"Kita telah berhasil melatih model multi-lapisan hingga tuntas dan mengamankan bobot dengan MSE terendah dalam file `best_oilpalm_model.pt`. Namun, apakah satu angka rata-rata MSE sebesar 0.39 ini sudah cukup untuk meyakinkan pimpinan perkebunan bahwa model aman dipasang pada mesin pabrik?"*

Jawabannya adalah **belum**. Dalam praktik industri nyata, sebuah model regresi bisa saja memiliki rata-rata MSE yang rendah, tetapi memiliki bias tersembunyi (misalnya selalu meremehkan rendemen pada buah kualitas super, atau memiliki galat residual yang mengelompok pada kondisi kelembaban tertentu).

Oleh karena itu, pada **AI Modul 8.9: Evaluasi Komprehensif & Diagnostik Kinerja Model Deep Learning**, mahasiswa akan diajak membedah kotak peralatan audit model secara menyeluruh: menganalisis plot sebaran residual, kurva diagnostik *Bias-Variance*, *Confusion Matrix*, kurva *ROC-AUC* / *Precision-Recall*, serta melakukan uji stres ketahanan model terhadap anomali data lapangan (*Robustness Stress Testing*).
