import os
import json

os.makedirs('docs/part-12', exist_ok=True)
os.makedirs('notebooks/part-12', exist_ok=True)
os.makedirs('instructor_resources/part-12', exist_ok=True)
os.makedirs('docx/part-12', exist_ok=True)
os.makedirs('docx/instructor_resources/part-12', exist_ok=True)

BANNED_WORDS = ['taksonomi', 'tripartit', 'ontologis', 'epistemologis', 'dialektika', 'manifestasi dependensi', 'de facto']

def validate_text(text, filename):
    lower = text.lower()
    for w in BANNED_WORDS:
        if w in lower:
            raise ValueError(f"BANNED WORD '{w}' found in {filename}!")
    for char, name in [('\x07', 'Bell'), ('\x08', 'Backspace'), ('\x0c', 'Form-feed')]:
        if char in text:
            raise ValueError(f"Control char {name} found in {filename}!")
    print(f"[VALIDATED] 0 banned words & 0 control chars in {filename}")

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

# ==============================================================================
# MODUL 12.5: IMAGE CLASSIFICATION DENGAN CNN
# ==============================================================================

doc_12_5 = r"""# AI Modul 12.5: Image Classification dengan CNN

## 1. Peta Konsep & Orientasi Pembelajaran

Klasifikasi citra (*image classification*) adalah tugas paling mendasar dalam visi komputer di mana model kecerdasan buatan bertugas memetakan citra digital utuh ke dalam salah satu label kategori dari ruang kelas diskrit. Meskipun formulasi tugasnya tampak sederhana, keberhasilan implementasi sistem klasifikasi di lingkungan industri nyata—seperti stasiun sortasi otomatis tandan buah segar (TBS) di pabrik kelapa sawit atau penyortiran mutu biji kopi ekspor—menuntut arsitektur pipeline yang tangguh dan menyeluruh (*end-to-end*).

Sistem produksi modern tidak hanya bertumpu pada arsitektur CNN belaka, melainkan mencakup rantai rekayasa komprehensif: augmentasi data yang mempertahankan karakteristik biologis objek, strategi regularisasi pencegah *overfitting* (seperti *Label Smoothing*), penjadwalan laju pembelajaran adaptif (*Cosine Annealing*), hingga teknik interpretabilitas spasial (*Grad-CAM*) yang memverifikasi bahwa model mengambil keputusan berdasarkan fitur visual yang sahih, bukan korelasi semu latar belakang.

```mermaid
flowchart TD
    A["Citra Mentah dari Kamera Industri"] --> B["Pipeline Augmentasi & Normalisasi (Torchvision / Albumentations)"]
    B --> C["Model Backbone CNN (ResNet / MobileNet)"]
    C --> D["Global Average Pooling & Logits Head"]
    D --> E["Kalkulasi Loss Berbobot + Label Smoothing"]
    E --> F["Backpropagation & Optimasi (AdamW + Cosine Scheduler)"]
    F --> G["Validasi Metrik (Accuracy, F1-Score, Confusion Matrix)"]
    G --> H["Visualisasi Wilayah Atensi (Grad-CAM Saliency)"]
```

Tujuan instruksional Modul 12.5 ini meliputi:
1. Memahami formulasi matematis *Cross-Entropy Loss*, *Label Smoothing*, dan mekanika kalibrasi probabilitas *Softmax*.
2. Membangun pipeline pelatihan end-to-end yang mengintegrasikan augmentasi data, *DataLoader* multi-proses, *learning rate scheduler*, dan *Early Stopping*.
3. Menganalisis kinerja model menggunakan metrik evaluasi komprehensif: *Confusion Matrix*, *Macro/Weighted F1-Score*, dan kurva *ROC-AUC*.
4. Mengimplementasikan visualisasi representasi atensi model menggunakan *Gradient-weighted Class Activation Mapping* (Grad-CAM).
5. Menerapkan sistem klasifikasi mutu kematangan TBS sawit pada lingkungan simulasi industri.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Multi-Class Cross-Entropy Loss dan Softmax

Diberikan sebuah batch citra dengan label kelas sebenarnya $y \in \{1, \dots, K\}$. Model CNN menghasilkan vektor nilai mentah tak ternormalisasi (*logits*) $z \in \mathbb{R}^K$. Fungsi *Softmax* memetakan logits menjadi distribusi probabilitas yang valid $\hat{y} \in (0, 1)^K$:

$$\hat{y}_k = \frac{\exp(z_k / T)}{\sum_{j=1}^K \exp(z_j / T)}$$

Dimana $T > 0$ adalah parameter suhu (*temperature*). Jika $T = 1$, kita memperoleh Softmax standar. Jika $T < 1$, distribusi probabilitas menjadi lebih tajam (*confident*), sedangkan jika $T > 1$, distribusi menjadi lebih merata (*soft*).

Fungsi kerugian *Cross-Entropy* mengukur divergensi antara distribusi ground-truth satu-panas (*one-hot*) $q$ dan prediksi model $\hat{y}$:

$$\mathcal{L}_{\text{CE}} = - \sum_{k=1}^K q_k \log(\hat{y}_k) = - \log(\hat{y}_y)$$

### 2.2 Regulasi Label Smoothing

Dalam pelatihan CNN berkapasitas besar, target satu-panas ekstrem ($q_y = 1, q_{k \neq y} = 0$) memaksa model menghasilkan logits yang menuju tak hingga ($z_y \gg z_k$), yang memicu fenomena *overconfidence* dan degradasi generalisasi.

*Label Smoothing* (Szegedy et al., 2016) memodifikasi target ground-truth dengan parameter penghalusan $\epsilon \in (0, 1)$:

$$q'_k = (1 - \epsilon) \cdot \mathbb{I}(k = y) + \frac{\epsilon}{K}$$

Sehingga fungsi kerugian teraturkan menjadi kombinasi linear antara Cross-Entropy standar dan entropi seragam:

$$\mathcal{L}_{\text{LS}} = (1 - \epsilon) \mathcal{L}_{\text{CE}} + \frac{\epsilon}{K} \sum_{k=1}^K (- \log \hat{y}_k)$$

Regularisasi ini terbukti secara empiris mencegah bobot model tumbuh terlalu besar dan meningkatkan kalibrasi probabilitas sistem pada data dunia nyata.

### 2.3 Formulasi Gradient-weighted Class Activation Mapping (Grad-CAM)

Untuk memvalidasi bahwa model klasifikasi tidak belajar dari artefak latar belakang, Selvaraju et al. (2017) merumuskan Grad-CAM. Grad-CAM menghitung bobot kepentingan $\alpha_k^c$ dari kanal peta fitur ke-$k$ pada lapisan konvolusi terakhir terhadap skor kelas target $y^c$ (sebelum Softmax):

$$\alpha_k^c = \frac{1}{Z} \sum_{i=1}^H \sum_{j=1}^W \frac{\partial y^c}{\partial A_{i, j}^k}$$

Dimana $Z = H \times W$ adalah luas spasial peta fitur. Peta panas visual (*heat-map*) Grad-CAM dihitung melalui kombinasi linear terbobot yang dilewatkan pada fungsi ReLU:

$$L_{\text{Grad-CAM}}^c = \text{ReLU} \left( \sum_{k} \alpha_k^c A^k \right)$$

Fungsi ReLU memastikan bahwa model hanya menyoroti fitur-fitur yang berkontribusi positif terhadap peningkatan probabilitas kelas $c$.

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Pipeline End-to-End Image Classification](../../docs/assets/pipeline_image_classification_end_to_end_cnn.png)

Diagram di atas merangkum seluruh tahapan pipeline klasifikasi citra modern:
1. **Prapemrosesan & Augmentasi**: Rotasi acak, pembalikan horizontal, dan penyesuaian kontras untuk memperkaya variasi data.
2. **Backbone CNN & GAP**: Ekstraksi fitur visual mendalam yang diringkas oleh Global Average Pooling.
3. **Optimasi & Loss**: Penjadwalan laju pembelajaran *Cosine Annealing* dengan regularisasi *weight decay*.
4. **Validasi & Interpretasi**: Verifikasi metrik kuantitatif dan inspeksi kualitatif wilayah atensi Grad-CAM.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lengkap kelas pelatihan terstandarisasi industri yang mencakup pelatihan berulang, pelacakan metrik, dan penyimpanan model terbaik (*checkpointing*).

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Dict, Tuple, List
import copy

class IndustrialCNNTrainer:
    '''
    Mesin Pelatihan CNN Berstandar Industri dengan Early Stopping dan Checkpointing.
    '''
    def __init__(self, model: nn.Module, criterion: nn.Module, optimizer: optim.Optimizer,
                 scheduler: optim.lr_scheduler._LRScheduler, device: torch.device):
        self.model = model.to(device)
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device
        self.best_model_weights = copy.deepcopy(model.state_dict())
        self.best_val_acc = 0.0
        
    def train_epoch(self, dataloader: DataLoader) -> Tuple[float, float]:
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in dataloader:
            images, labels = images.to(self.device), labels.to(self.device)
            
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            
            # Gradient clipping untuk mencegah ledakan gradien
            nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=2.0)
            self.optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
            
        return running_loss / total, correct / total

    def evaluate(self, dataloader: DataLoader) -> Tuple[float, float]:
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in dataloader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                running_loss += loss.item() * images.size(0)
                preds = outputs.argmax(dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)
                
        return running_loss / total, correct / total

    def fit(self, train_loader: DataLoader, val_loader: DataLoader, epochs: int, patience: int = 5) -> Dict[str, List[float]]:
        history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
        epochs_no_improve = 0
        
        for epoch in range(epochs):
            t_loss, t_acc = self.train_epoch(train_loader)
            v_loss, v_acc = self.evaluate(val_loader)
            
            if self.scheduler is not None:
                self.scheduler.step()
                
            history['train_loss'].append(t_loss)
            history['train_acc'].append(t_acc)
            history['val_loss'].append(v_loss)
            history['val_acc'].append(v_acc)
            
            print(f"Epoch [{epoch+1:02d}/{epochs}] - Train Loss: {t_loss:.4f} Acc: {t_acc*100:.1f}% | Val Loss: {v_loss:.4f} Acc: {v_acc*100:.1f}%")
            
            # Checkpoint model terbaik
            if v_acc > self.best_val_acc:
                self.best_val_acc = v_acc
                self.best_model_weights = copy.deepcopy(self.model.state_dict())
                epochs_no_improve = 0
            else:
                epochs_no_improve += 1
                if epochs_no_improve >= patience:
                    print(f"[EARLY STOPPING] Pelatihan dihentikan lebih awal pada epoch {epoch+1}.")
                    break
                    
        self.model.load_state_dict(self.best_model_weights)
        return history
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Sistem Sortasi Otomatis Kematangan Tandan Buah Segar (TBS) di Pabrik Kelapa Sawit

Pada stasiun penerimaan buah (*loading ramp*) di pabrik kelapa sawit berkapasitas 60 ton/jam, truk membongkar ribuan janjang TBS per hari. Standar industri menuntut pemilahan ketat 4 fraksi:
1. **Fraksi 00 & 0 (Mentah)**: Menghasilkan rendemen minyak sangat rendah (< 14%) dan pemborosan uap sterilisasi.
2. **Fraksi 1 & 2 (Mengkal)**: Rendemen minyak 18-20%.
3. **Fraksi 3 & 4 (Matang Sempurna)**: Rendemen minyak optimal (> 22%) dengan kadar asam lemak bebas (FFA) < 3%.
4. **Fraksi 5 (Lewat Matang)**: FFA melonjak drastis (> 5%), mendegradasi kualitas CPO menjadi kualitas rendah (*off-grade*).

**Arsitektur Solusi Rekayasa**:
* Kamera industri berpelindung debu IP67 dipasang di atas konveyor berjalan berkecepatan 0.8 m/s.
* Sistem inferensi berbasis model CNN terdistribusi (*Edge AI Box*) memproses citra setiap janjang buah dalam waktu < 25 milidetik.
* Jika janjang diklasifikasikan sebagai *Mentah* atau *Lewat Matang*, aktuator pneumatik secara otomatis mengalihkan janjang tersebut ke jalur afkir (*rejection chute*).
* Implementasi pipeline menghasilkan akurasi grading sebesar **97.3%**, mengurangi kesalahan sortasi manual manusia hingga **85%**.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Analisis kebutuhan sumber daya komputasi saat inferensi satu citra ($224 \times 224$):

| Arsitektur Model | Ukuran Bobot (FP32) | Latensi CPU (Intel i7) | Latensi GPU (NVIDIA T4) | Throughput (FPS GPU) |
| :--- | :--- | :--- | :--- | :--- |
| **ResNet-18** | 44.7 MB | ~28.4 ms | ~2.8 ms | ~350 FPS |
| **MobileNetV3-Large** | 21.9 MB | ~14.1 ms | ~1.9 ms | ~520 FPS |
| **EfficientNet-B0** | 20.5 MB | ~22.6 ms | ~3.1 ms | ~320 FPS |
| **ConvNeXt-Tiny** | 114.2 MB | ~65.2 ms | ~5.4 ms | ~185 FPS |

Untuk sistem pemilahan konveyor berkecepatan tinggi, **MobileNetV3** dan **ResNet-18** menawarkan keseimbangan ideal antara akurasi tinggi dan latensi rendah di bawah 5 ms.

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **Shortcut Learning (Atensi Semu Latar Belakang)** | Akurasi pengujian laboratorium 99%, namun merosot ke 40% saat diuji di perkebunan nyata. | CNN mengklasifikasikan buah sawit berdasarkan warna terpal truk pengangkut atau warna tanah latar belakang, bukan morfologi buah. | Validasi model menggunakan Grad-CAM untuk memverifikasi area fokus. Terapkan augmentasi *RandomErasing* dan *CutMix* pada area latar belakang. |
| **Class Imbalance Collapse** | Akurasi global tampak tinggi (90%), namun recall kelas minoritas (misal: penyakit langka) adalah 0%. | Dataset didominasi sampel kelas mayoritas, sehingga model selalu memprediksi kelas dominan. | Gunakan fungsi kerugian terbobot (`nn.CrossEntropyLoss(weight=class_weights)`) atau terapkan *Focal Loss*. |
| **Over-Augmentation Distortion** | Model gagal konvergen, loss berfluktuasi tinggi sepanjang epoch. | Augmentasi data terlalu ekstrem (misal: rotasi terbalik 180° pada objek yang memiliki orientasi gravitasi tetap, atau distorsi warna ekstrem yang merusak fitur kematangan). | Sesuaikan parameter augmentasi dengan domain biologis riil (misal: batasi *ColorJitter* saturasi agar tidak mengubah interpretasi warna buah matang). |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Analisis Confusion Matrix**: Diberikan matriks kontingensi 3 kelas mutu TBS (Mentah, Matang, Lewat Matang):
   $$\begin{bmatrix} 45 & 5 & 0 \\ 2 & 90 & 8 \\ 0 & 6 & 44 \end{bmatrix}$$
   Hitung Precision, Recall, dan F1-Score untuk kelas **Matang**.
   * *Solusi*:
     * True Positive (TP) = 90
     * False Positive (FP) = $5 + 6 = 11$
     * False Negative (FN) = $2 + 8 = 10$
     * $\text{Precision} = \frac{90}{90 + 11} = \frac{90}{101} \approx 89.11\%$
     * $\text{Recall} = \frac{90}{90 + 10} = \frac{90}{100} = 90.0\%$
     * $\text{F1-Score} = 2 \times \frac{0.8911 \times 0.90}{0.8911 + 0.90} \approx \mathbf{89.55\%}$

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual & Matematis)**: Turunkan formula matematis gradien Cross-Entropy Loss terhadap logits masukan $\frac{\partial \mathcal{L}}{\partial z_i}$ dan tunjukkan bahwa gradien tersebut sama dengan selisih antara probabilitas prediksi dan label ground truth: $\hat{y}_i - q_i$.
2. **Soal 2 (Komputasional)**: Rancang modul PyTorch `FocalLoss` yang mengintegrasikan faktor modulasi $(1 - p_t)^\gamma$ untuk menangani ketidakseimbangan kelas ekstrem pada dataset inspeksi visual industri.

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 12.6: Object Detection

Pada sistem klasifikasi citra yang telah kita bangun, model mengasumsikan bahwa seluruh bidang citra hanya memuat satu objek dominan yang ingin diklasifikasikan. Namun, dalam skenario operasional perkebunan nyata, sebuah citra dari kamera drone atau CCTV memuat puluhan objek yang tersebar: banyak pohon kelapa sawit, banyak tandan buah, serta keberadaan alat berat dan pekerja.

Pada **AI Modul 12.6: Object Detection**, kita akan melangkah dari klasifikasi tunggal menuju lokalisasi jamak: memprediksi koordinat spasial (*bounding box*) sekaligus kelas objek secara simultan menggunakan metrik evaluasi *Intersection over Union* (IoU) dan algoritma *Non-Maximum Suppression* (NMS).

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J., & Wojna, Z. (2016). *Rethinking the inception architecture for computer vision*. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2818-2826.
2. Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., & Batra, D. (2017). *Grad-CAM: Visual explanations from deep networks via gradient-based localization*. Proceedings of the IEEE International Conference on Computer Vision (ICCV), 618-626.
3. Loshchilov, I., & Hutter, F. (2017). *SGDR: Stochastic gradient descent with warm restarts*. International Conference on Learning Representations (ICLR 2017).
4. Lin, T. Y., Goyal, P., Girshick, R., He, K., & Dollár, P. (2017). *Focal loss for dense object detection*. Proceedings of the IEEE International Conference on Computer Vision (ICCV), 2980-2988.
5. Buslaev, A., et al. (2020). *Albumentations: Fast and flexible image augmentations*. Information, 11(2), 125.
"""

validate_text(doc_12_5, "AI_Modul_12.5_Image_classification_dengan_CNN.md")
with open("docs/part-12/AI_Modul_12.5_Image_classification_dengan_CNN.md", "w", encoding="utf-8") as f:
    f.write(doc_12_5)

# Notebook 12.5
nb_12_5_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 12.5: Praktikum Image Classification End-to-End dengan CNN\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Membangun pipeline pelatihan klasifikasi citra end-to-end lengkap dengan validasi metrik berkala.\n",
            "2. Menerapkan regularisasi *weight decay*, optimasi AdamW, dan penjadwalan *Cosine Annealing*.\n",
            "3. Menghitung dan memvisualisasikan Confusion Matrix multi-kelas untuk evaluasi akurasi sistem industri."
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
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "torch.manual_seed(42)\n",
            "np.random.seed(42)\n",
            "print(f\"PyTorch Versi: {torch.__version__}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Sintesis Dataset Multi-Kelas Mutu Kematangan TBS Sawit (3 Kelas)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 3 Kelas: 0: Mentah, 1: Matang, 2: Lewat Matang\n",
            "def generate_harvest_dataset(num_samples=450):\n",
            "    X = np.zeros((num_samples, 3, 32, 32), dtype=np.float32)\n",
            "    y = np.zeros(num_samples, dtype=np.int64)\n",
            "    \n",
            "    for i in range(num_samples):\n",
            "        cls = i % 3\n",
            "        y[i] = cls\n",
            "        if cls == 0:   # Mentah (Hitam Keunguan)\n",
            "            r, g, b = 0.20, 0.18, 0.22\n",
            "        elif cls == 1: # Matang Sempurna (Oranye Kemerahan)\n",
            "            r, g, b = 0.85, 0.40, 0.10\n",
            "        else:          # Lewat Matang (Merah Tua Kusam)\n",
            "            r, g, b = 0.45, 0.15, 0.08\n",
            "            \n",
            "        noise = np.random.normal(0, 0.04, (3, 32, 32))\n",
            "        X[i, 0, :, :] = r + noise[0]\n",
            "        X[i, 1, :, :] = g + noise[1]\n",
            "        X[i, 2, :, :] = b + noise[2]\n",
            "        \n",
            "    X = np.clip(X, 0.0, 1.0)\n",
            "    return torch.tensor(X), torch.tensor(y)\n",
            "\n",
            "X_data, y_data = generate_harvest_dataset(450)\n",
            "ds_total = TensorDataset(X_data, y_data)\n",
            "train_ds, val_ds = torch.utils.data.random_split(ds_total, [360, 90])\n",
            "\n",
            "train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)\n",
            "val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)\n",
            "print(f\"Dataset siap: Train = {len(train_ds)}, Val = {len(val_ds)}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Membangun Arsitektur dan Melatih Model End-to-End"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class IndustrialClassifier(nn.Module):\n",
            "    def __init__(self, num_classes=3):\n",
            "        super().__init__()\n",
            "        self.features = nn.Sequential(\n",
            "            nn.Conv2d(3, 32, kernel_size=3, padding=1),\n",
            "            nn.BatchNorm2d(32),\n",
            "            nn.ReLU(inplace=True),\n",
            "            nn.MaxPool2d(2, 2),\n",
            "            \n",
            "            nn.Conv2d(32, 64, kernel_size=3, padding=1),\n",
            "            nn.BatchNorm2d(64),\n",
            "            nn.ReLU(inplace=True),\n",
            "            nn.MaxPool2d(2, 2)\n",
            "        )\n",
            "        self.classifier = nn.Sequential(\n",
            "            nn.AdaptiveAvgPool2d((1, 1)),\n",
            "            nn.Flatten(),\n",
            "            nn.Dropout(0.3),\n",
            "            nn.Linear(64, num_classes)\n",
            "        )\n",
            "    def forward(self, x):\n",
            "        return self.classifier(self.features(x))\n",
            "\n",
            "model = IndustrialClassifier(num_classes=3)\n",
            "criterion = nn.CrossEntropyLoss()\n",
            "optimizer = optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-3)\n",
            "scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)\n",
            "\n",
            "epochs = 10\n",
            "train_losses, val_accs = [], []\n",
            "\n",
            "for epoch in range(epochs):\n",
            "    model.train()\n",
            "    running_loss = 0.0\n",
            "    for bx, by in train_loader:\n",
            "        optimizer.zero_grad()\n",
            "        out = model(bx)\n",
            "        loss = criterion(out, by)\n",
            "        loss.backward()\n",
            "        optimizer.step()\n",
            "        running_loss += loss.item() * bx.size(0)\n",
            "        \n",
            "    scheduler.step()\n",
            "    train_loss = running_loss / len(train_loader.dataset)\n",
            "    train_losses.append(train_loss)\n",
            "    \n",
            "    # Evaluasi\n",
            "    model.eval()\n",
            "    correct = 0\n",
            "    with torch.no_grad():\n",
            "        for vx, vy in val_loader:\n",
            "            preds = model(vx).argmax(dim=1)\n",
            "            correct += (preds == vy).sum().item()\n",
            "    acc = correct / len(val_loader.dataset)\n",
            "    val_accs.append(acc)\n",
            "    print(f\"Epoch [{epoch+1:02d}/{epochs}] - Loss: {train_loss:.4f} | Val Accuracy: {acc*100:.2f}%\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Komputasi Confusion Matrix dan Visualisasi"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Evaluasi matriks kontingensi\n",
            "model.eval()\n",
            "all_preds, all_labels = [], []\n",
            "with torch.no_grad():\n",
            "    for vx, vy in val_loader:\n",
            "        preds = model(vx).argmax(dim=1)\n",
            "        all_preds.extend(preds.cpu().numpy())\n",
            "        all_labels.extend(vy.cpu().numpy())\n",
            "\n",
            "num_classes = 3\n",
            "conf_mat = np.zeros((num_classes, num_classes), dtype=int)\n",
            "for true_l, pred_l in zip(all_labels, all_preds):\n",
            "    conf_mat[true_l, pred_l] += 1\n",
            "\n",
            "print(\"Confusion Matrix:\")\n",
            "print(conf_mat)\n",
            "\n",
            "# Visualisasi Matriks\n",
            "class_names = ['Mentah', 'Matang', 'Lewat Matang']\n",
            "fig, ax = plt.subplots(figsize=(6, 5))\n",
            "im = ax.imshow(conf_mat, cmap='Blues')\n",
            "plt.colorbar(im)\n",
            "\n",
            "ax.set_xticks(np.arange(num_classes))\n",
            "ax.set_yticks(np.arange(num_classes))\n",
            "ax.set_xticklabels(class_names)\n",
            "ax.set_yticklabels(class_names)\n",
            "plt.xlabel('Prediksi Model')\n",
            "plt.ylabel('Label Ground Truth')\n",
            "plt.title('Confusion Matrix Sortasi TBS Kelapa Sawit')\n",
            "\n",
            "# Nilai teks pada sel\n",
            "for i in range(num_classes):\n",
            "    for j in range(num_classes):\n",
            "        ax.text(j, i, str(conf_mat[i, j]), ha='center', va='center',\n",
            "                color='white' if conf_mat[i, j] > conf_mat.max()/2 else 'black', fontweight='bold')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_confusion_matrix_12_5.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Confusion matrix disimpan sebagai 'praktikum_confusion_matrix_12_5.png'\")"
        ]
    }
]

with open("notebooks/part-12/AI_Modul_12.5_Praktikum_Image_Classification_dengan_CNN.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_12_5_cells), f, indent=2)
print("[OK] Generated notebooks/part-12/AI_Modul_12.5_Praktikum_Image_Classification_dengan_CNN.ipynb")

# Guide 12.5
guide_12_5 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 12.5 - Image Classification dengan CNN

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Tinjauan pipeline end-to-end klasifikasi citra, fungsi loss Cross-Entropy, dan regularisasi Label Smoothing.
* **Menit 30 - 60**: Penjelasan matematis Grad-CAM untuk memverifikasi atensi spasial model.
* **Menit 60 - 100**: Praktikum komputer: Perakitan mesin pelatih `IndustrialCNNTrainer`, implementasi gradient clipping, checkpointing model terbaik.
* **Menit 100 - 130**: Studi kasus sortasi TBS kelapa sawit di pabrik kelapa sawit dan analisis Confusion Matrix.
* **Menit 130 - 150**: Pembahasan jebakan shortcut learning dan kuis formatif.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Penurunan Gradien Cross-Entropy terhadap Logits)
* Misalkan $z$ adalah logits dan $\hat{y}_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$.
* Loss: $\mathcal{L} = -\sum_k q_k \ln \hat{y}_k$.
* Turunan Softmax: $\frac{\partial \hat{y}_k}{\partial z_i} = \hat{y}_i (\mathbb{I}(i=k) - \hat{y}_k)$.
* Turunan Chain Rule:
  $$\frac{\partial \mathcal{L}}{\partial z_i} = - \sum_k \frac{q_k}{\hat{y}_k} \frac{\partial \hat{y}_k}{\partial z_i} = - \frac{q_i}{\hat{y}_i} \hat{y}_i (1 - \hat{y}_i) - \sum_{k \neq i} \frac{q_k}{\hat{y}_k} (-\hat{y}_i \hat{y}_k)$$
  $$\frac{\partial \mathcal{L}}{\partial z_i} = - q_i (1 - \hat{y}_i) + \hat{y}_i \sum_{k \neq i} q_k = - q_i + q_i \hat{y}_i + \hat{y}_i (1 - q_i) = \hat{y}_i - q_i$$
* Terbukti bahwa gradien adalah selisih langsung probabilitas prediksi terhadap target ($\hat{y}_i - q_i$).

### Solusi Soal Mandiri 2 (Focal Loss PyTorch)
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, alpha=None, gamma=2.0, reduction='mean'):
        super().__init__()
        self.alpha = alpha # Tensor bobot kelas
        self.gamma = gamma
        self.reduction = reduction
        
    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none', weight=self.alpha)
        pt = torch.exp(-ce_loss) # Probabilitas kelas target
        focal_loss = ((1.0 - pt) ** self.gamma) * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss
```

---

## 3. Rubrik Penilaian Praktikum
* **Kelengkapan Pipeline Pelatihan (30%)**: Implementasi loop pelatihan, evaluasi berkala, dan checkpointing model.
* **Metrik Evaluasi & Visualisasi (30%)**: Perhitungan akurat Confusion Matrix dan interpretasi Precision/Recall multi-kelas.
* **Performa Model (25%)**: Model mencapai konvergensi stabil dan akurasi validasi $\ge 90\%$.
* **Kualitas Kode & Standar Rekayasa (15%)**: Kode modular berstandar industri dengan penanganan perangkat (CPU/GPU) yang tepat.
"""

validate_text(guide_12_5, "AI_Modul_12.5_Panduan_Instruktur_dan_Kunci_Solusi.md")
with open("instructor_resources/part-12/AI_Modul_12.5_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_12_5)

print("[OK] Selesai Modul 12.5!")

# ==============================================================================
# MODUL 12.6: OBJECT DETECTION
# ==============================================================================

doc_12_6 = r"""# AI Modul 12.6: Object Detection

## 1. Peta Konsep & Orientasi Pembelajaran

Dalam visi komputer terapan, tugas klasifikasi citra sederhana (Modul 12.5) memiliki keterbatasan mendasar: model hanya mampu menjawab pertanyaan *"objek apa yang mendominasi citra?"*, namun tidak mampu menjawab pertanyaan *"di mana lokasi objek-objek tersebut dan berapa jumlahnya?"*. Pada skenario perkebunan dan kehutanan nyata—seperti sensus pohon kelapa sawit dari udara via drone, deteksi brondolan sawit yang tercecer di piringan, atau pemantauan satwa liar berbasis kamera jebak—sebuah citra tunggal memuat puluhan hingga ratusan objek berukuran heterogen yang tersebar di berbagai koordinat spasial.

**Object Detection (Deteksi Objek)** memadukan dua cabang komputasi sekaligus secara simultan: **Lokalisasi Spasial (*Spatial Localization*)** melalui regresi koordinat kotak pembatas (*bounding box*) dan **Klasifikasi Kategori (*Multi-Class Classification*)**. Modul 12.6 ini meletakkan fondasi teoretis dan komputasional paling mendasar sebelum kita mendalami arsitektur detektor modern (seperti YOLO, SSD, dan Faster R-CNN): memahami representasi koordinat kotak, metrik tumpang tindih spasial *Intersection over Union* (IoU), algoritma penapisan redundansi *Non-Maximum Suppression* (NMS), serta metrik evaluasi standar industri *Mean Average Precision* (mAP).

```mermaid
flowchart TD
    A["Citra Masukan H x W x C"] --> B["Detektor Objek (Backbone + Head)"]
    B --> C["Kandidat Kotak Pembatas Jamak (Ribuan Bounding Boxes)"]
    C --> D["Kalkulasi Nilai Keyakinan (Objectness & Class Probabilities)"]
    D --> E["Filtering Ambang Batas Keyakinan (Confidence Thresholding)"]
    E --> F["Algoritma Non-Maximum Suppression (NMS) via IoU"]
    F --> G["Deteksi Akhir Bersih: Bounding Box Unik + Label + Skor"]
    G --> H["Evaluasi Metrik: Mean Average Precision (mAP@0.5, mAP@0.5:0.95)"]
```

Tujuan instruksional Modul 12.6 ini meliputi:
1. Memahami format representasi kotak pembatas: sudut absolut $(x_{min}, y_{min}, x_{max}, y_{max})$ vs pusat ternormalisasi $(x_c, y_c, w, h)$.
2. Menurunkan formulasi matematis *Intersection over Union* (IoU) dan mengimplementasikannya secara vektorisasi murni.
3. Menguasai logika algoritma *Non-Maximum Suppression* (NMS) klasik dan penanganan objek saling bertumpuk via *Soft-NMS*.
4. Memahami kalkulasi kurva *Precision-Recall*, interpolasi 11-titik, dan *Mean Average Precision* (mAP).
5. Mensimulasikan sistem deteksi dan penghitungan tandan buah kelapa sawit pada tajuk pohon.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Representasi Bounding Box dan Konversi Koordinat

Terdapat dua konvensi standar representasi kotak pembatas (*bounding box*) dua dimensi:
1. **Format Sudut (Pascal VOC / PyTorch standard)**:
   $$B_{\text{corner}} = [x_{\min}, y_{\min}, x_{\max}, y_{\max}]$$
2. **Format Pusat-Dimensi (YOLO standard)**:
   $$B_{\text{center}} = [x_c, y_c, w, h]$$

Hubungan matematis konversi dua arah didefinisikan sebagai:

$$x_c = \frac{x_{\min} + x_{\max}}{2}, \quad y_c = \frac{y_{\min} + y_{\max}}{2}$$

$$w = x_{\max} - x_{\min}, \quad h = y_{\max} - y_{\min}$$

Sebaliknya:

$$x_{\min} = x_c - \frac{w}{2}, \quad y_{\min} = y_c - \frac{h}{2}$$

$$x_{\max} = x_c + \frac{w}{2}, \quad y_{\max} = y_c + \frac{h}{2}$$

Dalam pemrosesan *deep learning*, koordinat ini umumnya dinormalisasi terhadap lebar ($W_{\text{img}}$) dan tinggi ($H_{\text{img}}$) citra ke dalam interval $[0, 1]$ agar invarian terhadap perubahan resolusi masukan.

### 2.2 Formulasi Intersection over Union (IoU)

*Intersection over Union* (IoU) atau indeks Jaccard mengukur tingkat tumpang tindih spasial antara kotak prediksi $B_{\text{pred}}$ dan kotak ground-truth $B_{\text{gt}}$:

$$\text{IoU}(B_{\text{pred}}, B_{\text{gt}}) = \frac{\text{Area}(B_{\text{pred}} \cap B_{\text{gt}})}{\text{Area}(B_{\text{pred}} \cup B_{\text{gt}})} = \frac{\text{Area}(B_{\text{pred}} \cap B_{\text{gt}})}{\text{Area}(B_{\text{pred}}) + \text{Area}(B_{\text{gt}}) - \text{Area}(B_{\text{pred}} \cap B_{\text{gt}})}$$

Untuk dua kotak berformat $[x_{\min}, y_{\min}, x_{\max}, y_{\max}]$, koordinat kotak perpotongan (*intersection*) dihitung melalui:

$$x_1^I = \max(x_{\min}^{\text{pred}}, x_{\min}^{\text{gt}}), \quad y_1^I = \max(y_{\min}^{\text{pred}}, y_{\min}^{\text{gt}})$$

$$x_2^I = \min(x_{\max}^{\text{pred}}, x_{\max}^{\text{gt}}), \quad y_2^I = \min(y_{\max}^{\text{pred}}, y_{\max}^{\text{gt}})$$

Luas perpotongan:

$$\text{Area}_{\text{inter}} = \max(0, x_2^I - x_1^I) \times \max(0, y_2^I - y_1^I)$$

Suatu deteksi dinyatakan sebagai **True Positive (TP)** jika $\text{IoU} \ge \tau$ (ambang batas standar biasanya $\tau = 0.5$ atau $\tau = 0.75$) dan kelas prediksi cocok dengan ground truth. Sebaliknya, jika $\text{IoU} < \tau$, deteksi dinyatakan sebagai **False Positive (FP)**.

### 2.3 Algoritma Non-Maximum Suppression (NMS)

Model deteksi objek dense menghasilkan ribuan kandidat kotak di sekitar satu objek yang sama. Algoritma NMS bertujuan mengeliminasi kotak-kotak redundan tersebut:

**Algoritma NMS Standar**:
1. Masukan: Kumpulan kotak kandidat $\mathcal{B} = \{b_1, \dots, b_N\}$, skor keyakinan $\mathcal{S} = \{s_1, \dots, s_N\}$, dan ambang batas IoU $N_{\text{thresh}} \in [0.3, 0.7]$.
2. Inisialisasi himpunan kotak terpilih $\mathcal{D} \leftarrow \emptyset$.
3. Pilih kotak $b_{\text{max}}$ dengan skor keyakinan tertinggi dalam $\mathcal{B}$.
4. Pindahkan $b_{\text{max}}$ dari $\mathcal{B}$ ke $\mathcal{D}$.
5. Hapus seluruh kotak $b_i \in \mathcal{B}$ yang memiliki $\text{IoU}(b_{\text{max}}, b_i) \ge N_{\text{thresh}}$.
6. Ulangi langkah 3 hingga 5 hingga $\mathcal{B}$ kosong.
7. Kembalikan $\mathcal{D}$ sebagai hasil deteksi akhir.

### 2.4 Metrik Mean Average Precision (mAP)

*Average Precision* (AP) adalah luas area di bawah kurva Precision-Recall:

$$\text{AP} = \int_{0}^{1} p(r) \, dr$$

Dalam standar evaluasi COCO, mAP dihitung sebagai rata-rata AP untuk seluruh kelas $C$ pada 10 ambang batas IoU berbeda dari $0.50$ hingga $0.95$ dengan interval langkah $0.05$:

$$\text{mAP@[0.50:0.95]} = \frac{1}{|C|} \sum_{c \in C} \frac{1}{10} \sum_{\tau \in \{0.50, 0.55, \dots, 0.95\}} \text{AP}_c^\tau$$

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Konsep Dasar Object Detection](../../docs/assets/konsep_dasar_object_detection_bounding_box_iou_nms.png)

Diagram di atas mengilustrasikan:
1. **(A) Intersection over Union (IoU)**: Perbandingan luas perpotongan terhadap luas penggabungan antara kotak ground truth dan prediksi.
2. **(B) Non-Maximum Suppression (NMS)**: Eliminasi kotak-kotak redundan yang memiliki tumpang tindih tinggi ($\text{IoU} > 0.5$) terhadap kotak dengan keyakinan tertinggi.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lengkap kalkulasi IoU dan algoritma NMS murni berbasis NumPy berkecepatan tinggi:

```python
import numpy as np
from typing import List, Tuple

def compute_iou_vectorized(boxes_a: np.ndarray, boxes_b: np.ndarray) -> np.ndarray:
    '''
    Menghitung matriks IoU berukuran (N, M) dari dua kumpulan kotak berformat [xmin, ymin, xmax, ymax].
    boxes_a: array dimensi (N, 4)
    boxes_b: array dimensi (M, 4)
    '''
    N = boxes_a.shape[0]
    M = boxes_b.shape[0]
    
    # Hitung koordinat perpotongan (broadcasting)
    max_xy = np.minimum(boxes_a[:, 2:][:, np.newaxis, :], boxes_b[:, 2:][np.newaxis, :, :]) # (N, M, 2)
    min_xy = np.maximum(boxes_a[:, :2][:, np.newaxis, :], boxes_b[:, :2][np.newaxis, :, :]) # (N, M, 2)
    
    inter = np.clip(max_xy - min_xy, a_min=0, a_max=None)
    area_inter = inter[:, :, 0] * inter[:, :, 1] # (N, M)
    
    area_a = (boxes_a[:, 2] - boxes_a[:, 0]) * (boxes_a[:, 3] - boxes_a[:, 1]) # (N,)
    area_b = (boxes_b[:, 2] - boxes_b[:, 0]) * (boxes_b[:, 3] - boxes_b[:, 1]) # (M,)
    
    area_union = area_a[:, np.newaxis] + area_b[np.newaxis, :] - area_inter
    return area_inter / np.clip(area_union, a_min=1e-8, a_max=None)

def non_max_suppression_fast(boxes: np.ndarray, scores: np.ndarray, iou_threshold: float = 0.5) -> np.ndarray:
    '''
    Implementasi cepat NMS berbasis pengurutan indeks skor.
    boxes: array dimensi (N, 4) [xmin, ymin, xmax, ymax]
    scores: array dimensi (N,) skor keyakinan
    return: array indeks kotak yang dipertahankan
    '''
    if len(boxes) == 0:
        return np.array([], dtype=int)
        
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1] # Urutkan dari skor tertinggi
    
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        
        # Koordinat tumpang tindih terhadap kotak tertinggi saat ini
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        
        iou = inter / (areas[i] + areas[order[1:]] - inter)
        
        # Pertahankan hanya kotak dengan IoU < ambang batas
        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]
        
    return np.array(keep, dtype=int)
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Sensus Estimasi Panen Tandan Buah Segar (TBS) pada Tajuk Kelapa Sawit via Drone

Dalam manajemen operasional perkebunan kelapa sawit skala besar (ribuan hektar), estimasi produksi bulanan bergantung pada sensus tandan buah yang sedang berkembang pada tajuk pohon. Sensus manual dengan menugaskan tenaga kerja berjalan mengelilingi setiap pohon sangat lambat, mahal, dan berbahaya karena risiko gigitan serangga beracun atau sengatan pelepah berduri.

**Penyelesaian Berbasis Object Detection**:
1. Drone nirawak terbang otomatis pada ketinggian 15-20 meter dengan kamera sudut miring (*oblique camera* 45°).
2. Model deteksi objek mendeteksi setiap tandan buah yang terlihat di sela pelepah sawit.
3. **Tantangan Rekayasa**: Banyak tandan tumbuh berdekatan dalam satu ketiak pelepah (*clustered bunches*). Jika ambang batas NMS diatur terlalu longgar ($N_{\text{thresh}} = 0.3$), dua tandan berdampingan akan terhapus salah satunya (*under-counting*). Jika terlalu ketat ($N_{\text{thresh}} = 0.7$), satu tandan akan dihitung ganda (*over-counting*).
4. **Optimasi Lapangan**: Penerapan algoritma *Soft-NMS* dengan ambang batas adaptif menghasilkan akurasi sensus buah mencapai **94.2%**, memangkas waktu sensus dari 14 hari kerja manual menjadi hanya 4 jam penerbangan drone.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Perbandingan kompleksitas algoritma penapisan pasca-pemrosesan:

| Algoritma Pasca-Pemrosesan | Kompleksitas Waktu | Karakteristik Eliminasi | Keberhasilan pada Objek Berkerumun (*Crowded*) |
| :--- | :--- | :--- | :--- |
| **Standard Hard-NMS** | $\mathcal{O}(N^2)$ terburuk, $\mathcal{O}(N \log N)$ rata-rata | Memangkas total kotak jika $\text{IoU} \ge \tau$ | Rentan *false negative* pada objek rapat |
| **Soft-NMS (Gaussian)** | $\mathcal{O}(N^2)$ | Menurunkan skor secara eksponensial kontinu | Sangat baik, mempertahankan objek berdampingan |
| **Batched GPU NMS (`torchvision.ops.nms`)** | $\mathcal{O}(N)$ terakselerasi paralel bitmask | Cepat pada ribuan kotak serentak di VRAM | Standar industri untuk pipeline real-time |

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **Pembalikan Format Koordinat ($xywh$ vs $xyxy$)** | Nilai IoU bernilai 0 atau negatif, loss bounding box meledak (*NaN*). | Salah memasukkan format lebar/tinggi ($w, h$) sebagai koordinat sudut maksimum ($x_{\max}, y_{\max}$). | Buat fungsi konversi eksplisit dengan asersi integritas: `assert (x2 >= x1).all() and (y2 >= y1).all()`. |
| **Pembagian Nol pada Area Union IoU** | Muncul galat numerik `ZeroDivisionError` atau `NaN` pada kotak berdimensi nol. | Luas kotak prediksi nol piksel ($w=0$ atau $h=0$) dan tidak beririsan dengan ground truth. | Tambahkan *epsilon stabilisator*: `iou = inter / (union + 1e-8)`. |
| **Deteksi Ganda pada Objek Berskala Besar** | Satu pohon atau alat berat terdeteksi oleh 3-4 kotak berukuran berbeda. | Ambang batas NMS terlalu tinggi atau fitur multi-skala tidak terintegrasi secara harmonis. | Turunkan ambang batas NMS ke $0.45$ atau terapkan penapisan berbasis *Class-Aware NMS*. |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Perhitungan Manual IoU**: Diberikan dua kotak pembatas:
   * Kotak Ground Truth $B_{\text{gt}} = [10, 10, 50, 50]$
   * Kotak Prediksi $B_{\text{pred}} = [20, 20, 60, 60]$
   Hitung nilai IoU antara kedua kotak tersebut.
   * *Solusi*:
     * $\text{Area}(B_{\text{gt}}) = (50 - 10) \times (50 - 10) = 40 \times 40 = 1600$
     * $\text{Area}(B_{\text{pred}}) = (60 - 20) \times (60 - 20) = 40 \times 40 = 1600$
     * Titik perpotongan: $[\max(10, 20), \max(10, 20), \min(50, 60), \min(50, 60)] = [20, 20, 50, 50]$
     * $\text{Area}_{\text{inter}} = (50 - 20) \times (50 - 20) = 30 \times 30 = 900$
     * $\text{Area}_{\text{union}} = 1600 + 1600 - 900 = 2300$
     * $\text{IoU} = \frac{900}{2300} = \frac{9}{23} \approx \mathbf{0.3913}$

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual & Matematis)**: Turunkan formulasi penalti degradasi skor pada **Soft-NMS** berbasis fungsi Gaussian:
   $$s_i = s_i \exp \left( - \frac{\text{IoU}(M, b_i)^2}{\sigma} \right)$$
   Jelaskan mengapa fungsi kontinu ini jauh lebih unggul dibandingkan fungsi *hard thresholding* pada objek yang saling berdekatan.
2. **Soal 2 (Komputasional)**: Buat implementasi PyTorch murni untuk menghitung Generalized IoU (GIoU) yang memperhitungkan kotak penutup terkecil (*smallest enclosing box*) ketika dua kotak tidak saling beririsan ($\text{IoU} = 0$).

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 12.7: YOLO

Pada modul ini, kita telah memahami bagaimana bounding box didefinisikan, dievaluasi melalui IoU, dan disaring melalui NMS. Namun, bagaimana jaringan saraf menghasilkan prediksi koordinat dan kelas tersebut secara simultan dari citra mentah dalam hitungan milidetik?

Pada **AI Modul 12.7: YOLO (You Only Look Once)**, kita akan membedah salah satu algoritma deteksi objek paling populer dan revolusioner di dunia: pendekatan *Single-Stage Detector* berbasis pembagian kisi spasial (*grid cells*), regresi langsung, dan arsitektur *CSP-Darknet* yang mampu beroperasi secara real-time pada kecepatan tinggi.

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Everingham, M., Van Gool, L., Williams, C. K., Winn, J., & Zisserman, A. (2010). *The Pascal visual object classes (VOC) challenge*. International Journal of Computer Vision, 88(2), 303-338.
2. Lin, T. Y., et al. (2014). *Microsoft COCO: Common objects in context*. European Conference on Computer Vision (ECCV), 740-755.
3. Bodla, N., Singh, B., Chellappa, R., & Davis, L. S. (2017). *Soft-NMS--improving object detection with one line of code*. Proceedings of the IEEE International Conference on Computer Vision (ICCV), 5561-5569.
4. Rezatofighi, H., Tsoi, N., Gwak, J., Sadeghian, A., Reid, I., & Savarese, S. (2019). *Generalized intersection over union: A metric and a loss for bounding box regression*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 658-666.
5. Padfield, D. (2011). *Masked object detection in images*. IEEE Transactions on Pattern Analysis and Machine Intelligence, 34(1), 164-177.
"""

validate_text(doc_12_6, "AI_Modul_12.6_Object_detection.md")
with open("docs/part-12/AI_Modul_12.6_Object_detection.md", "w", encoding="utf-8") as f:
    f.write(doc_12_6)

# Notebook 12.6
nb_12_6_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 12.6: Praktikum Object Detection (Bounding Box, IoU, dan NMS)\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Melakukan konversi format koordinat Bounding Box ($xyxy \\leftrightarrow xywh$).\n",
            "2. Mengimplementasikan kalkulasi vektorisasi Intersection over Union (IoU).\n",
            "3. Membangun dan menguji algoritma Non-Maximum Suppression (NMS) untuk eliminasi deteksi ganda."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "import torch\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "import matplotlib.patches as patches\n",
            "\n",
            "print(\"Modul praktikum deteksi objek siap!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Konversi Koordinat dan Kalkulasi IoU"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def xywh_to_xyxy(boxes_xywh):\n",
            "    xc, yc, w, h = boxes_xywh[:, 0], boxes_xywh[:, 1], boxes_xywh[:, 2], boxes_xywh[:, 3]\n",
            "    x1 = xc - w / 2.0\n",
            "    y1 = yc - h / 2.0\n",
            "    x2 = xc + w / 2.0\n",
            "    y2 = yc + h / 2.0\n",
            "    return np.stack([x1, y1, x2, y2], axis=1)\n",
            "\n",
            "def compute_single_iou(box1, box2):\n",
            "    x1 = max(box1[0], box2[0])\n",
            "    y1 = max(box1[1], box2[1])\n",
            "    x2 = min(box1[2], box2[2])\n",
            "    y2 = min(box1[3], box2[3])\n",
            "    \n",
            "    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)\n",
            "    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])\n",
            "    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])\n",
            "    union = area1 + area2 - inter\n",
            "    return inter / union if union > 0 else 0.0\n",
            "\n",
            "# Uji IoU sampel\n",
            "gt_box = np.array([10, 10, 50, 50], dtype=float)\n",
            "pred_box = np.array([20, 20, 60, 60], dtype=float)\n",
            "iou_val = compute_single_iou(gt_box, pred_box)\n",
            "print(f\"IoU antara GT [10, 10, 50, 50] dan Pred [20, 20, 60, 60]: {iou_val:.4f}\")\n",
            "assert abs(iou_val - (900.0 / 2300.0)) < 1e-4, \"Kalkulasi IoU salah!\"\n",
            "print(\"[VALIDASI SUKSES] Formulasi matematis IoU teruji benar!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Implementasi Algoritma Non-Maximum Suppression (NMS)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def nms_pure_python(boxes, scores, threshold=0.5):\n",
            "    x1 = boxes[:, 0]\n",
            "    y1 = boxes[:, 1]\n",
            "    x2 = boxes[:, 2]\n",
            "    y2 = boxes[:, 3]\n",
            "    areas = (x2 - x1) * (y2 - y1)\n",
            "    order = scores.argsort()[::-1]\n",
            "    \n",
            "    keep = []\n",
            "    while order.size > 0:\n",
            "        i = order[0]\n",
            "        keep.append(i)\n",
            "        \n",
            "        xx1 = np.maximum(x1[i], x1[order[1:]])\n",
            "        yy1 = np.maximum(y1[i], y1[order[1:]])\n",
            "        xx2 = np.minimum(x2[i], x2[order[1:]])\n",
            "        yy2 = np.minimum(y2[i], y2[order[1:]])\n",
            "        \n",
            "        w = np.maximum(0.0, xx2 - xx1)\n",
            "        h = np.maximum(0.0, yy2 - yy1)\n",
            "        inter = w * h\n",
            "        iou = inter / (areas[i] + areas[order[1:]] - inter)\n",
            "        \n",
            "        inds = np.where(iou <= threshold)[0]\n",
            "        order = order[inds + 1]\n",
            "        \n",
            "    return keep\n",
            "\n",
            "# Simulasi beberapa prediksi kotak di sekitar 1 buah sawit\n",
            "sim_boxes = np.array([\n",
            "    [100, 100, 200, 200],  # Box 0: Sangat tepat (Conf 0.95)\n",
            "    [105,  98, 202, 205],  # Box 1: Redundan tumpang tindih tinggi (Conf 0.88)\n",
            "    [ 95, 102, 198, 195],  # Box 2: Redundan tumpang tindih tinggi (Conf 0.76)\n",
            "    [300, 300, 380, 380]   # Box 3: Objek buah lain terpisah (Conf 0.91)\n",
            "], dtype=float)\n",
            "\n",
            "sim_scores = np.array([0.95, 0.88, 0.76, 0.91], dtype=float)\n",
            "\n",
            "kept_indices = nms_pure_python(sim_boxes, sim_scores, threshold=0.5)\n",
            "print(f\"Kotak masukan: {len(sim_boxes)} kotak\")\n",
            "print(f\"Kotak setelah NMS: {len(kept_indices)} kotak (Indeks terpilih: {kept_indices})\")\n",
            "assert 0 in kept_indices and 3 in kept_indices and len(kept_indices) == 2, \"NMS gagal menapis redundansi!\"\n",
            "print(\"[SUKSES] NMS berhasil mempertahankan kotak unik dengan skor tertinggi!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Visualisasi Hasil Deteksi Sebelum vs Sesudah NMS"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))\n",
            "\n",
            "# Sebelum NMS\n",
            "ax1.set_xlim(50, 450)\n",
            "ax1.set_ylim(450, 50) # Invert Y axis seperti citra\n",
            "ax1.set_title(f'Sebelum NMS ({len(sim_boxes)} Kotak Redundan)')\n",
            "for idx, b in enumerate(sim_boxes):\n",
            "    rect = patches.Rectangle((b[0], b[1]), b[2]-b[0], b[3]-b[1], linewidth=2,\n",
            "                             edgecolor='red' if idx != 0 and idx != 3 else 'green', facecolor='none')\n",
            "    ax1.add_patch(rect)\n",
            "    ax1.text(b[0], b[1]-5, f\"Conf: {sim_scores[idx]:.2f}\", fontsize=8, color='black')\n",
            "ax1.grid(True, linestyle='--', alpha=0.5)\n",
            "\n",
            "# Sesudah NMS\n",
            "ax2.set_xlim(50, 450)\n",
            "ax2.set_ylim(450, 50)\n",
            "ax2.set_title(f'Setelah NMS ({len(kept_indices)} Kotak Unik Bersih)')\n",
            "for idx in kept_indices:\n",
            "    b = sim_boxes[idx]\n",
            "    rect = patches.Rectangle((b[0], b[1]), b[2]-b[0], b[3]-b[1], linewidth=2.5,\n",
            "                             edgecolor='green', facecolor='none')\n",
            "    ax2.add_patch(rect)\n",
            "    ax2.text(b[0], b[1]-5, f\"Tandan Sawit: {sim_scores[idx]:.2f}\", fontsize=9, fontweight='bold', color='green')\n",
            "ax2.grid(True, linestyle='--', alpha=0.5)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_nms_bounding_boxes_12_6.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Visualisasi NMS disimpan sebagai 'praktikum_nms_bounding_boxes_12_6.png'\")"
        ]
    }
]

with open("notebooks/part-12/AI_Modul_12.6_Praktikum_Object_Detection.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_12_6_cells), f, indent=2)
print("[OK] Generated notebooks/part-12/AI_Modul_12.6_Praktikum_Object_Detection.ipynb")

# Guide 12.6
guide_12_6 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 12.6 - Object Detection

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Perbedaan konseptual Image Classification, Localization, dan Object Detection.
* **Menit 35 - 65**: Formulasi matematis koordinat bounding box, IoU, dan algoritma Non-Maximum Suppression (NMS).
* **Menit 65 - 100**: Praktikum komputer: Implementasi kalkulasi IoU, konversi format koordinat $xywh \leftrightarrow xyxy$, dan penapisan NMS.
* **Menit 100 - 130**: Studi kasus sensus buah kelapa sawit via drone dan perbandingan Hard-NMS vs Soft-NMS.
* **Menit 130 - 150**: Pembahasan jebakan koordinat dan evaluasi Mean Average Precision (mAP).

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Formulasi Soft-NMS Gaussian)
* Pada Hard-NMS, jika kotak kandidat $b_i$ memiliki $\text{IoU} \ge N_{\text{thresh}}$, skornya langsung diatur menjadi 0 (dihapus seketika). Akibatnya, objek lain yang kebetulan berada sangat dekat akan lenyap (*false negative*).
* Pada **Soft-NMS Gaussian**:
  $$s_i = s_i \exp \left( - \frac{\text{IoU}(M, b_i)^2}{\sigma} \right)$$
* Skor kotak tetangga tidak dihapus melainkan didegradasi secara halus sebanding dengan tingkat tumpang tindihnya. Jika kotak tersebut merepresentasikan objek kedua yang sah, skornya akan tetap berada di atas ambang batas deteksi akhir sehingga objek tetap terdeteksi.

### Solusi Soal Mandiri 2 (Implementasi Generalized IoU / GIoU)
```python
import torch

def generalized_iou(box1, box2):
    '''
    box1, box2: Tensor koordinat (4,) [x1, y1, x2, y2]
    '''
    # 1. Hitung Intersection
    x1 = torch.max(box1[0], box2[0])
    y1 = torch.max(box1[1], box2[1])
    x2 = torch.min(box1[2], box2[2])
    y2 = torch.min(box1[3], box2[3])
    inter = torch.clamp(x2 - x1, min=0) * torch.clamp(y2 - y1, min=0)
    
    # 2. Hitung Union
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - inter
    iou = inter / (union + 1e-8)
    
    # 3. Hitung Smallest Enclosing Box C
    c_x1 = torch.min(box1[0], box2[0])
    c_y1 = torch.min(box1[1], box2[1])
    c_x2 = torch.max(box1[2], box2[2])
    c_y2 = torch.max(box1[3], box2[3])
    c_area = (c_x2 - c_x1) * (c_y2 - c_y1)
    
    # 4. Formula GIoU = IoU - (C - Union) / C
    giou = iou - (c_area - union) / (c_area + 1e-8)
    return giou

# Uji dua kotak terpisah (IoU = 0)
b1 = torch.tensor([0., 0., 10., 10.])
b2 = torch.tensor([20., 20., 30., 30.])
val_giou = generalized_iou(b1, b2)
print(f"GIoU untuk kotak tak beririsan: {val_giou.item():.4f}") # Bernilai negatif, memberikan gradien jarak!
```

---

## 3. Rubrik Penilaian Praktikum
* **Kebenaran Formulasi IoU (30%)**: Implementasi IoU teruji secara analitis dan bebas galat pembagian nol.
* **Implementasi Algoritma NMS (35%)**: Logika pengurutan skor dan eliminasi iteratif berfungsi sempurna.
* **Visualisasi & Interpretasi (20%)**: Menampilkan grafik perbandingan bounding box sebelum vs sesudah NMS dengan jelas.
* **Struktur Kode & Dokumentasi (15%)**: Kode rapi, menggunakan pustaka standar, dan terdokumentasi dengan baik.
"""

validate_text(guide_12_6, "AI_Modul_12.6_Panduan_Instruktur_dan_Kunci_Solusi.md")
with open("instructor_resources/part-12/AI_Modul_12.6_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_12_6)

print("[OK] Selesai Modul 12.6!")
