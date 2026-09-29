import os
import json
import re

BANNED_WORDS = ['taksonomi', 'tripartit', 'ontologis', 'epistemologis', 'dialektika', 'manifestasi dependensi', 'de facto']

def validate_text(text, filename):
    lower = text.lower()
    for w in BANNED_WORDS:
        if w in lower:
            raise ValueError(f"BANNED WORD FOUND in {filename}: '{w}'")
    print(f"[VALIDATED] 0 banned words in {filename}")

def build_modul_9_7():
    # Modul 9.7 from staged 8.5
    with open("staging_dl/AI_Modul_8.5_Optimasi_Gradient_Descent_Lanjut.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    content = re.sub(r'^# AI Modul 8\.\d+:.*$', '# AI Modul 9.7: Training Neural Network', content, flags=re.MULTILINE)
    content = re.sub(r'\* \*\*Kode Modul\*\*: AI-08-\d+', '* **Kode Modul**: AI-09-07', content)
    content = re.sub(r'\* \*\*Prasyarat\*\*:.*$', '* **Prasyarat**: AI Modul 9.6 (Backpropagation)', content, flags=re.MULTILINE)
    content = re.sub(r'Sub-CPMK 8\.5\.', 'Sub-CPMK 9.7.', content)
    content = re.sub(r'AI-08-05', 'AI-09-07', content)
    content = re.sub(r'AI-08-5', 'AI-09-07', content)
    content = re.sub(r'AI-09-05', 'AI-09-07', content)
    content = re.sub(r'## 9\. Jembatan Konsep \(Bridging\).*$', '## 9. Jembatan Konsep (Bridging) ke AI Modul 9.8: Hyperparameter Tuning', content, flags=re.MULTILINE)
    
    out_md = "docs/part-09/AI_Modul_9.7_Training_Neural_Network.md"
    validate_text(content, out_md)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Generated {out_md}")
    
    # Notebook 9.7
    with open("staging_dl/AI_Modul_8.5_Praktikum_Optimasi_Gradient_Descent_Lanjut.ipynb", "r", encoding="utf-8") as f:
        nb_str = f.read()
    nb_str = nb_str.replace("Modul 8.5", "Modul 9.7")
    nb_str = nb_str.replace("AI-08-05", "AI-09-07")
    nb_str = nb_str.replace("Praktikum Optimasi Gradient Descent Lanjut", "Praktikum Training Neural Network")
    out_nb = "notebooks/part-09/AI_Modul_9.7_Praktikum_Training_Neural_Network.ipynb"
    with open(out_nb, "w", encoding="utf-8") as f:
        f.write(nb_str)
    print(f"[OK] Generated {out_nb}")
    
    # Guide 9.7
    with open("staging_dl/AI_Modul_8.5_Panduan_Instruktur_dan_Kunci_Solusi.md", "r", encoding="utf-8") as f:
        g_str = f.read()
    g_str = re.sub(r'^# AI Modul 8\.\d+:', '# AI Modul 9.7:', g_str, flags=re.MULTILINE)
    g_str = g_str.replace("AI-08-05", "AI-09-07")
    g_str = g_str.replace("Modul 8.5", "Modul 9.7")
    out_g = "instructor_resources/part-09/AI_Modul_9.7_Panduan_Instruktur_dan_Kunci_Solusi.md"
    validate_text(g_str, out_g)
    with open(out_g, "w", encoding="utf-8") as f:
        f.write(g_str)
    print(f"[OK] Generated {out_g}")

def build_modul_9_8():
    # Modul 9.8 from staged 8.6
    with open("staging_dl/AI_Modul_8.6_Regularisasi_dan_Generalisasi_Deep_Learning.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    content = re.sub(r'^# AI Modul 8\.\d+:.*$', '# AI Modul 9.8: Hyperparameter Tuning', content, flags=re.MULTILINE)
    content = re.sub(r'\* \*\*Kode Modul\*\*: AI-08-\d+', '* **Kode Modul**: AI-09-08', content)
    content = re.sub(r'\* \*\*Prasyarat\*\*:.*$', '* **Prasyarat**: AI Modul 9.7 (Training Neural Network)', content, flags=re.MULTILINE)
    content = re.sub(r'Sub-CPMK 8\.6\.', 'Sub-CPMK 9.8.', content)
    content = re.sub(r'AI-08-06', 'AI-09-08', content)
    content = re.sub(r'AI-08-6', 'AI-09-08', content)
    content = re.sub(r'AI-09-06', 'AI-09-08', content)
    content = re.sub(r'## 9\. Jembatan Konsep \(Bridging\).*$', '## 9. Jembatan Konsep (Bridging) ke AI Modul 9.9: Framework Deep Learning (TensorFlow & PyTorch)', content, flags=re.MULTILINE)
    
    out_md = "docs/part-09/AI_Modul_9.8_Hyperparameter_Tuning.md"
    validate_text(content, out_md)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Generated {out_md}")
    
    # Notebook 9.8
    with open("staging_dl/AI_Modul_8.6_Praktikum_Regularisasi_dan_Generalisasi_Deep_Learning.ipynb", "r", encoding="utf-8") as f:
        nb_str = f.read()
    nb_str = nb_str.replace("Modul 8.6", "Modul 9.8")
    nb_str = nb_str.replace("AI-08-06", "AI-09-08")
    nb_str = nb_str.replace("Praktikum Regularisasi dan Generalisasi Deep Learning", "Praktikum Hyperparameter Tuning")
    out_nb = "notebooks/part-09/AI_Modul_9.8_Praktikum_Hyperparameter_Tuning.ipynb"
    with open(out_nb, "w", encoding="utf-8") as f:
        f.write(nb_str)
    print(f"[OK] Generated {out_nb}")
    
    # Guide 9.8
    with open("staging_dl/AI_Modul_8.6_Panduan_Instruktur_dan_Kunci_Solusi.md", "r", encoding="utf-8") as f:
        g_str = f.read()
    g_str = re.sub(r'^# AI Modul 8\.\d+:', '# AI Modul 9.8:', g_str, flags=re.MULTILINE)
    g_str = g_str.replace("AI-08-06", "AI-09-08")
    g_str = g_str.replace("Modul 8.6", "Modul 9.8")
    out_g = "instructor_resources/part-09/AI_Modul_9.8_Panduan_Instruktur_dan_Kunci_Solusi.md"
    validate_text(g_str, out_g)
    with open(out_g, "w", encoding="utf-8") as f:
        f.write(g_str)
    print(f"[OK] Generated {out_g}")

def build_modul_9_9():
    md_content = """# AI Modul 9.9: Framework Deep Learning (TensorFlow & PyTorch)

---

## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**: AI-09-09
* **Mata Kuliah**: Kecerdasan Buatan Terapan & Deep Learning (INSTIPER)
* **Alokasi Waktu**: 3 x 50 Menit (Teori & Praktikum Terbimbing)
* **Beban SKS**: 3 SKS (Semester Ganjil)
* **Prasyarat**: AI Modul 9.8 (Hyperparameter Tuning)
* **Level Kognitif**: Bloom C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)

```mermaid
flowchart LR
    A["OUTPUTS: Pemahaman Paradigma Dynamic vs Static Graph, Model PyTorch nn.Module, Pipeline DataLoader"] --> B["OUTCOMES: Kemampuan Membangun & Melatih Jaringan Saraf Modern Menggunakan Framework Standar Industri"]
    B --> C["IMPACTS: Kesiapan Implementasi Solusi Computer Vision & AI Real-Time pada Perkebunan Skala Industri"]
```

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
* **Impacts (Dampak Strategis Jangka Panjang)**:
  * Standardisasi pengembangan model AI di lingkungan agro-industri berbasis framework standar industri internasional yang siap diintegrasikan ke platform IoT dan edge computing lapangan.

---

## 2. Profil Fundamental Framework Deep Learning: Fungsi, Manfaat, dan Keunggulan-Kelemahan

### 2.1 Fungsi Komputasi & Pemodelan Matematis
Framework deep learning menyediakan abstraksi perangkat lunak tingkat tinggi di atas komputasi aljabar linier perangkat keras GPU:
1. **Mesin Diferensiasi Otomatis (*Automatic Differentiation / Autograd*)**: Melacak seluruh operasi matematika pada tensor secara dinamis dan membangun graf asiklik terarah (*Directed Acyclic Graph* - DAG). Gradien analitik dihitung secara otomatis menggunakan algoritma akumulasi balik (*reverse-mode automatic differentiation*) tanpa intervensi pengguna.
2. **Akselerasi Perangkat Keras Paralel (*Hardware Acceleration via CUDA/cuDNN*)**: Menjembatani kode Python tingkat tinggi dengan instruksi kernel tingkat rendah NVIDIA CUDA dan cuDNN, memungkinkan eksekusi perkalian matriks tensor berkecepatan puluhan TFLOPS.
3. **Abstraksi Pemuatan Data Multi-Utas (*Multi-Threaded Data Loading*)**: Menyediakan modul `DataLoader` yang membagi pemrosesan I/O (pembacaan disk, dekompresi, augmentasi) secara paralel di beberapa proses CPU (`workers`), sehingga memori GPU tidak mengalami *idling* menunggu data masukan.

### 2.2 Manfaat Nyata di Industri Perkebunan & Agribisnis
* **Percepatan Siklus Riset Menuju Produksi**: Agronom dan data engineer dapat menguji hipotesis pemodelan baru (seperti arsitektur baru prediksi klorofil atau deteksi tajuk) dalam hitungan jam menggunakan modul siap pakai (`torch.nn.Linear`, `torch.nn.CrossEntropyLoss`).
* **Deploy Model ke Perangkat Nir-Daya Rendah (*Edge AI*)**: Model yang dilatih di workstation GPU dapat diekspor ke format ONNX atau TorchScript dan dijalankan pada unit komputer mini (NVIDIA Jetson, Raspberry Pi) yang dipasang pada traktor atau drone inspeksi kebun.
* **Ekosistem Pustaka Visi Komputer Mutakhir**: Membuka akses langsung ke model-model pretrained canggih pada pustaka `torchvision` (ResNet, EfficientNet, YOLO, Vision Transformer) untuk tugas Computer Vision pada Part 10 hingga Part 12.

### 2.3 Rationale: Alasan Mengapa Materi Ini Dipelajari
Meskipun pemahaman *from-scratch* menggunakan NumPy pada Modul 9.1 hingga 9.8 sangat krusial untuk menguasai intuisi matematika, penerapan industri skala nyata mustahil dilakukan secara manual. Menulis derivasi balik analitis untuk arsitektur modern yang memiliki puluhan juta bobot akan memakan waktu berbulan-bulan dan rentan terhadap kesalahan numerik. Menguasai framework formal adalah prasyarat mutlak bagi praktisi AI modern.

### 2.4 Analisis Kelebihan dan Kekurangan: PyTorch vs TensorFlow

| Parameter Evaluasi | PyTorch | TensorFlow / Keras | Implikasi untuk Industri Perkebunan |
| :--- | :--- | :--- | :--- |
| **Paradigma Graf** | Dinamis (*Define-by-Run* / Eager Execution). | Statis / Hibrida (*Define-and-Run* via `tf.function`). | PyTorch lebih intuitif untuk debugging visual data kebun. |
| **Gaya Pemrograman** | Sangat bernuansa Pythonic dan berorientasi objek (`OOP`). | Deklaratif tingkat tinggi (`Sequential`, `Functional API`). | Pemula menyukai Keras, praktisi riset menyukai PyTorch. |
| **Ekosistem Riset** | Dominan di komunitas riset akademis dan paper CV terkini. | Didukung kuat oleh Google, stabil di ekosistem perbankan/cloud. | PyTorch memudahkan replikasi riset agronomi global terbaru. |
| **Deployment Mobile/Edge** | TorchScript, ExecuTorch, ONNX. | TensorFlow Lite, TF Serving, Coral TPU. | TF Lite sangat matang untuk mikroprosesor embedded berdaya rendah. |
| **Kemudahan Debugging** | Sangat mudah: dapat di-debug menggunakan `pdb` atau print biasa. | Debugging graf simbolik memerlukan penanganan khusus. | Memudahkan pelacakan kesalahan dimensi sensor pertanian. |

### 2.5 Contoh Kasus Penggunaan Konkret di Sektor Agro-Industri
Pabrik Kelapa Sawit (PKS) membangun sistem pemantauan konveyor TBS berbasis AI. Tim data scientist menggunakan PyTorch di fase penelitian untuk merancang jaringan pendeteksi buah lewat matang, memanfaatkan `torchvision` dan autograd dinamis untuk eksperimen hiperparameter. Setelah model mencapai akurasi $96.5\%$, model diekspor ke format ONNX dan dioptimalkan dengan TensorRT pada komputer industri tepi jalan (*edge computer*) untuk inferensi dengan latensi di bawah 15 milidetik per frame konveyor.

### 2.6 Aspek Kritis & Catatan Penting Arsitektur
1. **Pengelolaan State Mode Evaluasi**: Model wajib dialihkan ke mode evaluasi (`model.eval()`) sebelum inferensi dan kembali ke mode latih (`model.train()`) saat pelatihan. Mengabaikan langkah ini akan menyebabkan lapisan Dropout dan Batch Normalization beroperasi secara salah.
2. **Pembersihan Gradien Akumulatif**: PyTorch secara default mengakumulasikan gradien pada tensor. Praktisi wajib memanggil `optimizer.zero_grad()` sebelum pemanggilan `loss.backward()` pada setiap iterasi mini-batch.

---

## 3. Landasan Teori & Konsep Matematis Framework Deep Learning

![Komparasi Arsitektur Framework PyTorch vs TensorFlow](../assets/komparasi_arsitektur_framework_pytorch_vs_tensorflow.png)

### 3.1 Teori Komputasi Graf Asiklik Terarah (*DAG Autograd*)
Dalam PyTorch, setiap kali suatu operasi komputasi diterapkan pada tensor dengan atribut `requires_grad=True`, engine Autograd merekam operasi tersebut ke dalam graf komputasi asiklik terarah (DAG).
* Node daun (*leaf nodes*) adalah parameter yang dapat dilatih ($W, b$) atau tensor masukan ($X$).
* Node operator adalah fungsi matematika (penjumlahan matriks, perkalian dot, aktivasi).
* Setiap node memiliki referensi fungsi turunan balik (`grad_fn`).

Ketika fungsi `loss.backward()` dipanggil, Autograd mengeksekusi aturan rantai kalkulus dari node akar (loss skalar) bergerak mundur ke seluruh node daun:

$$\frac{\partial L}{\partial w_i} = \sum_{\text{semua jalur } p} \prod_{(u, v) \in p} \frac{\partial v}{\partial u}$$

Secara komputasional, seluruh proses diferensiasi ini dilakukan dalam kompleksitas waktu linier $O(|V| + |E|)$ terhadap jumlah simpul dan busur graf.

### 3.2 Siklus Pelatihan Kanonik (*Canonical Training Loop*)
Siklus pelatihan formal pada PyTorch terdiri dari lima langkah berurutan yang dieksekusi per mini-batch:
1. **Zero Grad**: Mengosongkan buffer akumulasi gradien parameter:
   $$\nabla_\theta L \leftarrow 0 \quad (\text{optimizer.zero\_grad}())$$
2. **Forward Pass**: Mengalirkan batch input melalui arsitektur:
   $$\hat{y} = f(X; \theta) \quad (\text{outputs} = \text{model}(\text{inputs}))$$
3. **Loss Computation**: Menghitung deviasi terhadap target aktual:
   $$L = \mathcal{L}(\hat{y}, y) \quad (\text{loss} = \text{criterion}(\text{outputs}, \text{labels}))$$
4. **Backward Pass (Autograd)**: Menghitung gradien parsial untuk seluruh parameter:
   $$\nabla_\theta L = \frac{\partial L}{\partial \theta} \quad (\text{loss.backward}())$$
5. **Optimizer Step**: Memperbarui nilai parameter menggunakan algoritma optimasi (misalnya AdamW):
   $$\theta \leftarrow \theta - \eta \cdot \text{step}(\nabla_\theta L) \quad (\text{optimizer.step}())$$

---

## 4. Arsitektur Komputasi & Pipeline Praktis Python

```mermaid
flowchart TD
    A["Dataset Mentah: Pembacaan Sensor Kebun"] --> B["torch.utils.data.Dataset Custom"]
    B --> C["DataLoader: Mini-Batching & Multi-Thread Shuffling"]
    C --> D["Model torch.nn.Module (Forward Computation)"]
    D --> E["Loss Function: torch.nn.CrossEntropyLoss"]
    E --> F["Autograd: loss.backward() -> Menghitung Gradien"]
    F --> G["Optimizer: torch.optim.AdamW -> optimizer.step()"]
    G --> H["Model Checkpoint: torch.save(model.state_dict())"]
```

Implementasi lengkap Multi-Layer Perceptron menggunakan PyTorch modern:

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import numpy as np

# 1. Definisi Arsitektur Model berbasis torch.nn.Module
class AgriculturalMLP(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=32, num_classes=3, dropout_rate=0.2):
        super(AgriculturalMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.BatchNorm1d(hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, num_classes)
        )
        
    def forward(self, x):
        return self.network(x)

# 2. Pembangkitan Data Sintetis Sensor Perkebunan
torch.manual_seed(42)
N_samples = 600
X_dummy = torch.randn(N_samples, 8) # 8 variabel sensor tanah & iklim
y_dummy = torch.randint(0, 3, (N_samples,)) # 3 kelas kesesuaian

# 3. Pipeline DataLoader
dataset = TensorDataset(X_dummy, y_dummy)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# 4. Inisialisasi Model, Loss, dan Optimizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = AgriculturalMLP(input_dim=8, hidden_dim=32, num_classes=3).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=0.005, weight_decay=1e-4)

# 5. Eksekusi Training Loop Kanonik
model.train()
epochs = 5
for epoch in range(epochs):
    running_loss = 0.0
    correct = 0
    total = 0
    for batch_X, batch_y in train_loader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * batch_X.size(0)
        _, predicted = torch.max(outputs, 1)
        total += batch_y.size(0)
        correct += (predicted == batch_y).sum().item()
        
    epoch_loss = running_loss / total
    epoch_acc = (correct / total) * 100
    print(f"Epoch [{epoch+1}/{epochs}] - Loss: {epoch_loss:.4f} - Akurasi: {epoch_acc:.2f}%")
```

---

## 5. Studi Kasus Komprehensif Agro-Industri: Klasifikasi Varietas Bibit Kelapa Sawit

### 5.1 Spesifikasi Masalah Agronomis
Pada stasiun pembibitan (*pre-nursery & main-nursery*), pemilahan varietas bibit kelapa sawit (Dura, Pisifera, dan Tenera) secara akurat sangat krusial untuk mencegah tercampurnya varietas non-produktif (Dura dengan cangkang tebal atau Pisifera yang steril tanpa cangkang) ke area komersial. Data morphometri bibit mencakup 6 fitur: tinggi bibit, diameter batang leher akar, jumlah pelepah, panjang pelepah ke-3, rasio lebar helai anak daun, dan kandungan klorofil SPAD.

### 5.2 Implementasi Evaluasi & Ekspor Model ke ONNX
```python
# Mode Evaluasi
model.eval()
with torch.no_grad():
    sample_input = torch.randn(1, 8).to(device)
    raw_logits = model(sample_input)
    probabilities = torch.softmax(raw_logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    
print(f"Probabilitas Inferensi Satu Sampel: {probabilities.cpu().numpy()[0]}")
print(f"Prediksi Kelas Varietas Terpilih   : {predicted_class}")

# Ekspor Model ke Standar ONNX untuk Deployment Lapangan
dummy_input = torch.randn(1, 8, device=device)
onnx_filename = "model_agro_mlp.onnx"
torch.onnx.export(
    model, 
    dummy_input, 
    onnx_filename, 
    export_params=True,
    opset_version=14,
    input_names=['fitur_sensor_tanaman'],
    output_names=['probabilitas_kelas']
)
print(f"Model berhasil diekspor ke format terbuka: {onnx_filename}")
```

---

## 6. Kekeliruan Metodologis dan Praktik Terbaik (*Common Pitfalls & Best Practices*)

### 6.1 Kekeliruan Umum Metodologis (*Common Pitfalls*)
1. **Lupa Memanggil `optimizer.zero_grad()`**: Kegagalan mengosongkan gradien menyebabkan gradien dari batch sebelumnya terakumulasi ke batch saat ini, merusak arah penurunan gradien.
2. **Kebocoran Memori akibat Akumulasi Tensor Loss**: Menuliskan `total_loss += loss` alih-alih `total_loss += loss.item()` akan menahan seluruh riwayat komputasi graf pada memori RAM/VRAM sehingga memicu galat *Out of Memory* (OOM).
3. **Ketidakcocokan Perangkat (*Device Mismatch*)**: Menyajikan tensor input yang berada di CPU ke model yang berada di GPU (`RuntimeError: Expected all tensors to be on the same device`).

### 6.2 Praktik Terbaik (*Best Practices*)
1. **Kapsulasi Data dengan `Dataset` & `DataLoader`**: Gunakan `DataLoader` dengan `pin_memory=True` dan `num_workers > 0` untuk memaksimalkan efisiensi transfer data dari host RAM ke VRAM GPU.
2. **Penggunaan Context Manager `torch.no_grad()` saat Validasi**: Selalu nonaktifkan pelacakan autograd saat inferensi dan validasi guna menghemat alokasi memori hingga $60\%$ dan mempercepat komputasi.
3. **Penyimpanan Checkpoint Lengkap**: Simpan tidak hanya bobot model (`model.state_dict()`), melainkan juga status optimizer (`optimizer.state_dict()`), nomor epoch, dan loss validasi terbaik.

---

## 7. Rangkuman Modul

* Framework deep learning modern seperti PyTorch dan TensorFlow menyediakan abstraksi komputasi tingkat tinggi melalui engine diferensiasi otomatis (Autograd) dan akselerasi CUDA GPU.
* PyTorch mengadopsi paradigma graf dinamis (*define-by-run*) yang intuitif dan sangat ramah terhadap proses penelusuran galat (*debugging*).
* Siklus pelatihan kanonik terdiri dari 5 tahapan terstruktur: pembersihan gradien (`zero_grad`), propagasi maju (`model(x)`), kalkulasi loss (`criterion`), propagasi mundur (`backward`), dan pembaruan bobot (`step`).
* Pustaka `Dataset` dan `DataLoader` memungkinkan pembacaan dan pemrosesan data sensor secara multi-threaded yang mencegah bottleneck komputasi.
* Ekspor model ke format terbuka seperti ONNX memfasilitasi penerapan model ke berbagai lingkungan perangkat keras produksi dan perangkat cerdas terpasang (*edge devices*).

---

## 8. Latihan Soal & Tugas Analitis HOTS (Bloom C3-C5)

### Soal Konseptual & Analitis
1. **Analisis Graf Komputasi (Bloom C4)**: Bandingkan secara mendalam perbedaan mekanisme kerja graf dinamis (*Dynamic Computation Graph*) pada PyTorch dengan graf statis (*Static Graph*) pada TensorFlow 1.x! Mengapa graf dinamis jauh lebih fleksibel untuk menangani input data tanaman dengan panjang deret waktu yang bervariasi (*variable-length sequences*)?
2. **Analisis Kebocoran Memori (Bloom C4)**: Perhatikan potongan kode berikut:
   ```python
   epoch_loss = 0
   for x, y in loader:
       out = model(x)
       loss = criterion(out, y)
       loss.backward()
       optimizer.step()
       epoch_loss += loss  # Masalah ada di sini!
   ```
   Jelaskan mengapa penulisan `epoch_loss += loss` di atas dapat menyebabkan program terhenti akibat kehabisan memori VRAM GPU setelah beberapa puluh epoch! Solusi apa yang harus diterapkan?

### Tugas Pemrograman Mandiri
Rancang sebuah model PyTorch `VegetationPredictor` yang memiliki 3 lapisan linier dengan aktivasi ReLU dan lapisan Dropout ($p = 0.3$). Latih model tersebut menggunakan optimizer AdamW pada dataset tabular sintetis selama 10 epoch. Terapkan mekanisme penyimpanan checkpoint model terbaik (`best_model.pth`) berdasarkan nilai loss validasi terendah!

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 10.1: Konsep Computer Vision

Selamat! Anda telah menyelesaikan seluruh rangkaian fondasi mendalam pada **Part 9: Deep Learning Fundamental**?"mulai dari konsep dasar representasi hierarkis, arsitektur multi-layer perceptron, struktur neuron, fungsi aktivasi, fungsi rugi, backpropagation, algoritma training, hyperparameter tuning, hingga penguasaan framework industri PyTorch.

Lalu, ke manakah seluruh kekuatan representasi bertingkat ini akan kita arahkan? Bidang di mana Deep Learning mengalami revolusi terbesar dan memberikan dampak paling transformatif adalah **Visi Komputer (*Computer Vision*)**!

Pada bagian selanjutnya, yaitu **Part 10: Computer Vision Dasar**, kita akan memasuki era pemrosesan citra digital. Kita akan memulai perjalanan ini di **AI Modul 10.1: Konsep dan Fundamental Computer Vision**, di mana kita akan mempelajari bagaimana fluks foton optik ditangkap oleh sensor kamera drone, bagaimana mata biologis dibandingkan dengan sensor digital, serta bagaimana memodelkan geometri pembentukan citra untuk inspeksi kebun sawit masa depan.

---

## 10. Daftar Pustaka dan Referensi Akademik

1. Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., ... & Chintala, S. (2019). *PyTorch: An imperative style, high-performance deep learning library*. Advances in Neural Information Processing Systems (NeurIPS), 32, 8026-8037.
2. Abadi, M., Barham, P., Chen, J., Chen, Z., Davis, A., Dean, J., ... & Zheng, X. (2016). *TensorFlow: A system for large-scale machine learning*. 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16), 265-283.
3. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. (Bab 12: Applications - Computer Vision & Speech Recognition).
4. Ketkar, N., & Moolayil, J. (2021). *Deep Learning with Python: A Hands-on Introduction to PyTorch*. Apress.
"""
    validate_text(md_content, "AI_Modul_9.9_Framework_Deep_Learning.md")
    with open("docs/part-09/AI_Modul_9.9_Framework_Deep_Learning.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("[OK] Generated docs/part-09/AI_Modul_9.9_Framework_Deep_Learning.md")

    # Notebook 9.9
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# AI Modul 9.9: Praktikum Framework Deep Learning (PyTorch)\n",
                    "**Mata Kuliah:** Kecerdasan Buatan Terapan & Deep Learning  \n",
                    "**Institut Pertanian Stiper (INSTIPER) Yogyakarta**  \n",
                    "\n",
                    "---\n",
                    "\n",
                    "### Capaian Pembelajaran Praktikum:\n",
                    "1. Membangun model Multi-Layer Perceptron berorientasi objek menggunakan `torch.nn.Module`.\n",
                    "2. Mengonfigurasi pipeline pemuatan data efisien menggunakan `TensorDataset` dan `DataLoader`.\n",
                    "3. Mengimplementasikan siklus pelatihan kanonik (*canonical training loop*) dengan Autograd dan optimizer AdamW.\n",
                    "4. Mengevaluasi performa klasifikasi bibit sawit dan mengekspor model ke format standar ONNX.\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import torch\n",
                    "import torch.nn as nn\n",
                    "import torch.optim as optim\n",
                    "from torch.utils.data import TensorDataset, DataLoader\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                    "print(f'PyTorch Version : {torch.__version__}')\n",
                    "print(f'CUDA Tersedia   : {torch.cuda.is_available()}')\n",
                    "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
                    "print(f'Perangkat Aktif : {device}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Pembangkitan Data Varietas Bibit Sawit dan Pipa Pemuatan Data (DataLoader)\n",
                    "Membuat dataset 6 fitur morfometri bibit kelapa sawit (tinggi, diameter batang, helai daun, dll.) untuk 3 varietas: Dura, Pisifera, dan Tenera."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "torch.manual_seed(42)\n",
                    "np.random.seed(42)\n",
                    "\n",
                    "n_samples = 600\n",
                    "n_features = 6\n",
                    "\n",
                    "# Pembangkitan data sintetis terdistribusi normal\n",
                    "X_data = torch.randn(n_samples, n_features, dtype=torch.float32)\n",
                    "y_data = torch.randint(0, 3, (n_samples,), dtype=torch.long)\n",
                    "\n",
                    "# Pemisahan Train (80%) dan Test (20%)\n",
                    "train_size = int(0.8 * n_samples)\n",
                    "X_train, X_test = X_data[:train_size], X_data[train_size:]\n",
                    "y_train, y_test = y_data[:train_size], y_data[train_size:]\n",
                    "\n",
                    "# Pembungkusan DataLoader\n",
                    "train_dataset = TensorDataset(X_train, y_train)\n",
                    "test_dataset = TensorDataset(X_test, y_test)\n",
                    "\n",
                    "train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)\n",
                    "test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)\n",
                    "\n",
                    "print(f'Jumlah Data Latih: {len(train_dataset)}, Data Uji: {len(test_dataset)}')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Perancangan Model PyTorch (AgriculturalMLP)\n",
                    "Membangun arsitektur jaringan saraf berorientasi objek dengan Batch Normalization, ReLU, dan Dropout."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "class AgriculturalMLP(nn.Module):\n",
                    "    def __init__(self, input_dim=6, hidden_dim=32, num_classes=3, dropout_rate=0.2):\n",
                    "        super(AgriculturalMLP, self).__init__()\n",
                    "        self.net = nn.Sequential(\n",
                    "            nn.Linear(input_dim, hidden_dim),\n",
                    "            nn.BatchNorm1d(hidden_dim),\n",
                    "            nn.ReLU(),\n",
                    "            nn.Dropout(dropout_rate),\n",
                    "            nn.Linear(hidden_dim, 16),\n",
                    "            nn.BatchNorm1d(16),\n",
                    "            nn.ReLU(),\n",
                    "            nn.Linear(16, num_classes)\n",
                    "        )\n",
                    "        \n",
                    "    def forward(self, x):\n",
                    "        return self.net(x)\n",
                    "\n",
                    "model = AgriculturalMLP(input_dim=6, hidden_dim=32, num_classes=3).to(device)\n",
                    "criterion = nn.CrossEntropyLoss()\n",
                    "optimizer = optim.AdamW(model.parameters(), lr=0.01, weight_decay=1e-4)\n",
                    "print(model)\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Eksekusi Training Loop Kanonik dan Evaluasi\n",
                    "Melatih model selama 15 epoch dan mencatat dinamika loss serta akurasi."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "epochs = 15\n",
                    "history_loss = []\n",
                    "history_acc = []\n",
                    "\n",
                    "for epoch in range(epochs):\n",
                    "    model.train()\n",
                    "    total_loss = 0.0\n",
                    "    correct = 0\n",
                    "    total = 0\n",
                    "    \n",
                    "    for batch_x, batch_y in train_loader:\n",
                    "        batch_x, batch_y = batch_x.to(device), batch_y.to(device)\n",
                    "        \n",
                    "        optimizer.zero_grad()\n",
                    "        outputs = model(batch_x)\n",
                    "        loss = criterion(outputs, batch_y)\n",
                    "        loss.backward()\n",
                    "        optimizer.step()\n",
                    "        \n",
                    "        total_loss += loss.item() * batch_x.size(0)\n",
                    "        _, preds = torch.max(outputs, 1)\n",
                    "        total += batch_y.size(0)\n",
                    "        correct += (preds == batch_y).sum().item()\n",
                    "        \n",
                    "    epoch_loss = total_loss / total\n",
                    "    epoch_acc = (correct / total) * 100\n",
                    "    history_loss.append(epoch_loss)\n",
                    "    history_acc.append(epoch_acc)\n",
                    "    \n",
                    "print(f'Training Selesai! Final Train Loss: {history_loss[-1]:.4f} - Akurasi: {history_acc[-1]:.1f}%')\n",
                    "\n",
                    "# Evaluasi pada Data Uji\n",
                    "model.eval()\n",
                    "test_correct = 0\n",
                    "with torch.no_grad():\n",
                    "    for batch_x, batch_y in test_loader:\n",
                    "        batch_x, batch_y = batch_x.to(device), batch_y.to(device)\n",
                    "        outputs = model(batch_x)\n",
                    "        _, preds = torch.max(outputs, 1)\n",
                    "        test_correct += (preds == batch_y).sum().item()\n",
                    "\n",
                    "test_acc = (test_correct / len(test_dataset)) * 100\n",
                    "print(f'Akurasi Evaluasi Test Set: {test_acc:.1f}%')\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. Visualisasi Kurva Pembelajaran dan Ekspor ke ONNX\n",
                    "Menampilkan grafik konvergensi pelatihan dan mengekspor model teruji ke format terbuka ONNX."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))\n",
                    "ax1.plot(history_loss, color='crimson', linewidth=2)\n",
                    "ax1.set_title('Dinamika Training Loss (Cross-Entropy)', fontweight='bold')\n",
                    "ax1.set_xlabel('Epoch')\n",
                    "ax1.set_ylabel('Loss')\n",
                    "\n",
                    "ax2.plot(history_acc, color='forestgreen', linewidth=2)\n",
                    "ax2.set_title('Peningkatan Akurasi Pelatihan (%)', fontweight='bold')\n",
                    "ax2.set_xlabel('Epoch')\n",
                    "ax2.set_ylabel('Akurasi (%)')\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.savefig('praktikum_pytorch_training_9_9.png', dpi=150)\n",
                    "plt.show()\n",
                    "\n",
                    "# Ekspor model ke ONNX\n",
                    "dummy_in = torch.randn(1, 6, device=device)\n",
                    "onnx_path = 'model_bibit_sawit.onnx'\n",
                    "torch.onnx.export(\n",
                    "    model,\n",
                    "    dummy_in,\n",
                    "    onnx_path,\n",
                    "    export_params=True,\n",
                    "    opset_version=14,\n",
                    "    input_names=['fitur_bibit'],\n",
                    "    output_names=['prediksi_varietas']\n",
                    ")\n",
                    "print(f'[OK] Model PyTorch berhasil diekspor ke: {onnx_path}')\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open("notebooks/part-09/AI_Modul_9.9_Praktikum_Framework_Deep_Learning.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("[OK] Generated notebooks/part-09/AI_Modul_9.9_Praktikum_Framework_Deep_Learning.ipynb")

    # Guide 9.9
    guide_content = """# AI Modul 9.9: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-09-09
* **Topik Utama**: Framework Deep Learning (PyTorch & TensorFlow)
* **Alokasi Waktu**: 150 Menit (50 Menit Kuliah Teori Arsitektur Framework, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 9.9, Jupyter Notebook Praktikum, Proyektor, Komputer Praktikum dengan PyTorch 2.x terpasang.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Arsitektur software deep learning: Autograd DAG, perbandingan imperatif PyTorch vs deklaratif TensorFlow, dan akselerasi GPU CUDA.
* **Menit 25 - 50**: Bedah anatomi kode PyTorch: subclassing `nn.Module`, konstruksi pipeline `Dataset` dan `DataLoader`, serta 5 langkah kanonik training loop.
* **Menit 50 - 120**: Praktikum hands-on: membangun model klasifikasi varietas bibit sawit, melatih model, evaluasi dengan `torch.no_grad()`, dan mengekspor model ke ONNX.
* **Menit 120 - 150**: Pembahasan kesalahan umum (lupa `zero_grad`, memory leak akumulasi tensor), ulasan transisi ke Computer Vision (Part 10).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Arsitektur PyTorch** | Mampu menguraikan peran Autograd, DAG, dan siklus kanonik training loop secara tepat tanpa kesalahan konsep. | Memahami langkah training loop dasar namun kurang memahami mekanisme kerja Autograd di belakang layar. | Mengabaikan langkah penting seperti pembersihan gradien atau mode evaluasi. |
| **Implementasi Kode PyTorch** | Menulis kelas `nn.Module`, pipeline `DataLoader`, dan training loop kustom yang bersih dan bebas galat. | Mampu menjalankan praktikum namun kesulitan saat mengonfigurasi dimensi lapisan atau tipe data tensor. | Terjadi galat ketidakcocokan perangkat (`CPU vs GPU mismatch`) tanpa tahu cara memperbaikinya. |
| **Ekspor & Evaluasi Model** | Berhasil melakukan evaluasi menggunakan `torch.no_grad()` dan mengekspor model ke format ONNX secara mandiri. | Mampu mengeksekusi evaluasi namun tidak memahami format pertukaran model terbuka seperti ONNX. | Lupa mengubah mode model ke `eval()` saat melakukan pengujian pada data uji. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Graf Dinamis vs Statis
Pada graf statis (TensorFlow 1.x), struktur jaringan didefinisikan terlebih dahulu secara deklaratif sebagai cetak biru simbolik, lalu dikompilasi dan dieksekusi di dalam sesi (`tf.Session()`). Kelemahannya adalah kaku dan sulit didebug karena variabel Python biasa tidak dapat diinspeksi secara langsung di tengah eksekusi graf.
Sebaliknya, pada graf dinamis (PyTorch), graf komputasi dibangun secara instan (*on-the-fly*) pada saat baris kode dieksekusi (*define-by-run*). Setiap iterasi dapat memiliki struktur graf yang berbeda. Hal ini sangat menguntungkan untuk data perkebunan yang memiliki panjang deret waktu bervariasi (*variable-length time-series*) atau citra dengan dimensi tidak seragam, karena struktur loop dan percabangan kondisi Python asli (`if/else`, `for`) dapat langsung mengendalikan aliran tensor tanpa perlu operator kontrol simbolik yang rumit.

### Jawaban Soal Konseptual 2: Analisis Kebocoran Memori
Pernyataan `epoch_loss += loss` menahan objek tensor PyTorch `loss` ke dalam variabel skalar Python. Karena tensor `loss` terhubung ke seluruh graf komputasi Autograd (melalui atribut `grad_fn`), variabel `epoch_loss` secara tidak sengaja mempertahankan seluruh riwayat komputasi graf dari seluruh batch di dalam memori VRAM GPU. Seiring bertambahnya batch dan epoch, alokasi memori membengkak secara eksponensial hingga memicu galat `CUDA out of memory` (OOM).
Solusi yang benar adalah mengekstrak nilai float numerik mentah dari tensor skalar menggunakan method `.item()`:
```python
epoch_loss += loss.item() * batch_x.size(0)
```
Dengan memanggil `.item()`, hanya nilai skalar Python murni yang diakumulasikan, sehingga graf komputasi Autograd untuk batch tersebut dapat langsung dihapus dari memori GPU oleh garbage collector.
"""
    validate_text(guide_content, "AI_Modul_9.9_Panduan_Instruktur_dan_Kunci_Solusi.md")
    with open("instructor_resources/part-09/AI_Modul_9.9_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    print("[OK] Generated instructor_resources/part-09/AI_Modul_9.9_Panduan_Instruktur_dan_Kunci_Solusi.md")

if __name__ == '__main__':
    build_modul_9_7()
    build_modul_9_8()
    build_modul_9_9()
