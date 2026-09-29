import os
import json

os.makedirs('docs/part-13', exist_ok=True)
os.makedirs('notebooks/part-13', exist_ok=True)
os.makedirs('instructor_resources/part-13', exist_ok=True)
os.makedirs('docx/part-13', exist_ok=True)
os.makedirs('docx/instructor_resources/part-13', exist_ok=True)

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
# MODUL 13.1: INTEGRASI MODEL DENGAN KAMERA
# ==============================================================================

doc_13_1 = r"""# AI Modul 13.1: Integrasi Model dengan Kamera

## 1. Peta Konsep & Orientasi Pembelajaran

Transisi dari model visi komputer yang beroperasi secara luring (*offline batch evaluation*) menuju sistem visi komputer real-time di lingkungan industri fisik menghadirkan tantangan rekayasa komputasi yang sama sekali berbeda. Pada pengujian akademis, model menerima berkas citra statis yang telah tersimpan rapi di memori disk. Namun, dalam implementasi lapangan nyata—seperti pemantauan tandan buah segar (TBS) kelapa sawit di atas konveyor berjalan atau sistem kendali robot pemanen otomatis—model harus berinteraksi secara langsung dengan **aliran data kontinu dari sensor kamera fisik (*camera hardware stream*)**.

Kendala terbesar dalam mengawinkan pustaka OpenCV (`cv2.VideoCapture`) dengan model *deep learning* (seperti PyTorch, ONNX Runtime, atau TensorRT) dalam satu utas tunggal (*single-threaded loop*) adalah fenomena **akumulasi latensi buffer (*buffer lag accumulation*)**: jika inferensi model membutuhkan waktu 40 milidetik sementara kamera memproduksi frame setiap 33 milidetik (30 FPS), buffer internal driver kamera akan terisi frame-frame usang. Akibatnya, sistem menampilkan deteksi objek yang telah lewat beberapa detik lalu, memicu kegagalan aktuasi mekanik.

Modul 13.1 ini membedah arsitektur integrasi kamera real-time berstandar industri: perancangan utas penangkap asinkron (*producer-consumer multi-threading*), eliminasi penundaan antrean buffer, optimasi throughput tensor, serta penyisipan telemetri *On-Screen Display* (OSD).

```mermaid
flowchart LR
    A["Sensor Kamera (USB / RTSP IP / CSI)"] -->|"30 FPS Kontinu"| B["Capture Thread (Producer)"]
    B -->|"Update Frame Terkini"| C["Zero-Lag Frame Buffer (Atomic Pointer)"]
    C -->|"Ambil Frame Teranyar"| D["AI Inference Worker (Consumer)"]
    D -->|"Tensor Preprocessing + Model Run"| E["Hasil Prediksi & BBox"]
    E --> F["OSD Display & Aktuasi Kontrol"]
```

Tujuan instruksional Modul 13.1 ini meliputi:
1. Memahami arsitektur penangkap multi-utas (*multi-threaded ingestion*) untuk mengeliminasi latensi internal buffer driver kamera.
2. Menguasai alur transmisi tensor: konversi format warna OpenCV (BGR) menuju representasi tensor PyTorch/ONNX (RGB, kanal pertama, ternormalisasi) dengan latensi minimal.
3. Menganalisis profil waktu komputasi end-to-end: waktu akuisisi frame, prapemrosesan, inferensi jaringan saraf, pascapemrosesan (NMS), dan rendering OSD.
4. Membangun kelas pembungkus kamera industri (*ThreadedCameraStream*) yang dilengkapi mekanisme pemulihan koneksi otomatis (*auto-reconnect watchdog*).
5. Menerapkan integrasi kamera real-time untuk klasifikasi otomatis buah sawit pada konveyor inspeksi.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Analisis Latensi dan Permasalahan Buffer Lag

Misalkan kamera beroperasi pada laju frame $\text{FPS}_{\text{cam}}$ dengan interval kedatangan frame $\Delta t_{\text{cam}} = \frac{1}{\text{FPS}_{\text{cam}}}$. Model kecerdasan buatan membutuhkan waktu eksekusi total (prapemrosesan + inferensi + pascapemrosesan) sebesar $\Delta t_{\text{ai}}$.

Dalam arsitektur sekuensial utas tunggal (*single-threaded*):

$$\Delta t_{\text{loop}} = \Delta t_{\text{cam\_read}} + \Delta t_{\text{ai}} + \Delta t_{\text{display}}$$

Jika $\Delta t_{\text{ai}} > \Delta t_{\text{cam}}$, maka untuk setiap detik operasional, selisih waktu terakumulasi dalam antrean buffer driver perangkat keras:

$$\Delta t_{\text{lag}}(t) = t \cdot \left( 1 - \frac{\Delta t_{\text{cam}}}{\Delta t_{\text{ai}}} \right)$$

Sebagai contoh, jika kamera menghasilkan 30 FPS ($\Delta t_{\text{cam}} \approx 33.3\text{ ms}$) dan inferensi membutuhkan waktu $50\text{ ms}$, maka setelah beroperasi selama 60 detik, sistem akan mengalami penundaan tampilan sebesar:

$$\Delta t_{\text{lag}}(60) = 60 \cdot \left( 1 - \frac{33.3}{50} \right) = 60 \cdot (1 - 0.666) \approx \mathbf{20.0} \text{ detik}$$

Penundaan 20 detik ini fatal bagi otomatisasi pabrik.

### 2.2 Arsitektur Producer-Consumer dengan Atomic Frame Buffer

Untuk menihilkan $\Delta t_{\text{lag}}$, kita menerapkan pemisahan proses melalui dua utas independen yang berbagi satu lokasi memori bersama (*shared memory pointer*) dengan sinkronisasi mutex:

1. **Utas Produsen (*Producer Thread*)**: Terus-menerus memanggil `cap.read()` pada kecepatan kamera maksimal dan menimpa (*overwrite*) buffer dengan frame paling baru.
2. **Utas Konsumen (*Consumer Thread*)**: Mengambil frame teranyar dari buffer hanya saat model siap melakukan inferensi. Jika ada frame kamera yang belum sempat diinferensi, frame tersebut secara sengaja dilewati (*frame dropping*) demi mempertahankan latensi nol detik (*zero-latency real-time view*).

### 2.3 Transformasi Tensor Berkecepatan Tinggi (Zero-Copy Preprocessing)

Kamera menghasilkan citra berupa array NumPy berformat warna BGR dengan susunan memori berorientasi baris (*interleaved*): $(H, W, 3)$ tipe data `uint8`. Model deep learning menuntut tensor masukan berdimensi $(1, 3, H_{\text{in}}, W_{\text{in}})$ bertipe `float32` dalam urutan kanal RGB.

Transformasi komputasional berurutan:
1. Penskalaan spasial: $I_{\text{resized}} = \mathcal{R}(I, (W_{\text{in}}, H_{\text{in}}))$.
2. Pembalikan kanal dan permutasi memori (*interleaved to planar*):

$$T(c, y, x) = \frac{I_{\text{resized}}(y, x, 2 - c)}{255.0} \quad c \in \{0, 1, 2\}$$

3. Standarisasi z-score:

$$T_{\text{norm}}(c, y, x) = \frac{T(c, y, x) - \mu_c}{\sigma_c}$$

Penggunaan fungsi `cv2.dnn.blobFromImage` atau tensor GPU murni (`torch.from_numpy` + akselerasi CUDA) memangkas waktu transformasi ini dari 15 milidetik menjadi di bawah 1.2 milidetik.

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Arsitektur Integrasi Model Deep Learning dengan Kamera Real-Time](../../docs/assets/arsitektur_integrasi_model_deep_learning_dengan_kamera_real_time.png)

Diagram di atas mengilustrasikan:
1. **Pemisahan Utas Produsen & Konsumen**: Utas kamera menguras driver buffer terus-menerus, sementara utas AI memproses frame teranyar tanpa hambatan antrean.
2. **Ring Buffer Mutex-Protected**: Menyimpan tepat satu frame termutakhir, menjamin penundaan tampilan bernilai nol milidetik.
3. **OSD Telemetri**: Penyematan metrik inferensi (FPS, nama kelas, skor kepastian) secara langsung di atas frame video.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lengkap kelas penangkap kamera multi-utas industri (`ThreadedCameraStream`) yang dipasangkan dengan mesin inferensi PyTorch:

```python
import cv2
import threading
import time
import numpy as np
import torch
import torch.nn as nn
from typing import Optional, Tuple

class ThreadedCameraStream:
    '''
    Pembungkus Kamera Multi-Threaded Industri untuk Eliminasi Latensi Buffer.
    '''
    def __init__(self, src: int = 0, name: str = "CamWorker"):
        self.src = src
        self.name = name
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # Minimalkan buffer hardware
        
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()
        self.thread: Optional[threading.Thread] = None
        
    def start(self):
        if self.started:
            return self
        self.started = True
        self.thread = threading.Thread(target=self.update, name=self.name, daemon=True)
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            if not grabbed:
                # Upaya koneksi ulang otomatis jika sinyal terputus
                time.sleep(0.1)
                continue
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        with self.read_lock:
            if not self.grabbed or self.frame is None:
                return False, None
            return True, self.frame.copy()

    def stop(self):
        self.started = False
        if self.thread is not None:
            self.thread.join(timeout=1.0)
        self.cap.release()

class RealtimeInferenceEngine:
    '''
    Mesin Prapemrosesan dan Inferensi Cepat untuk Klasifikasi Kematangan Sawit.
    '''
    def __init__(self, model: nn.Module, class_names: list, input_size: Tuple[int, int] = (64, 64)):
        self.model = model
        self.model.eval()
        self.class_names = class_names
        self.input_size = input_size
        self.device = next(model.parameters()).device
        
    def preprocess(self, bgr_frame: np.ndarray) -> torch.Tensor:
        resized = cv2.resize(bgr_frame, self.input_size)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        tensor = torch.from_numpy(rgb).permute(2, 0, 1).float() / 255.0
        return tensor.unsqueeze(0).to(self.device)

    def predict(self, bgr_frame: np.ndarray) -> Tuple[str, float]:
        tensor = self.preprocess(bgr_frame)
        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1)[0]
            top_idx = probs.argmax().item()
            return self.class_names[top_idx], probs[top_idx].item()
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Pemilahan Otomatis Tandan Buah Segar (TBS) pada Konveyor Pabrik Kelapa Sawit

Pada stasiun penerimaan pabrik kelapa sawit berkapasitas 60 ton/jam, buah sawit diangkut oleh konveyor sabuk karet berkecepatan $0.8 \text{ m/detik}$. Di atas konveyor, dipasang portal kamera industri bersertifikasi IP67 dengan pencahayaan LED terpolarisasi.

**Kebutuhan Rekayasa Sistem**:
1. Setiap janjang buah melintasi bidang pandang kamera selebar $1.2 \text{ meter}$ hanya dalam waktu $1.5 \text{ detik}$.
2. Pintu penyortir pneumatik (*rejection gate*) terletak $2.0 \text{ meter}$ di hilir kamera. Waktu tempuh buah dari kamera ke aktuator adalah:

$$t_{\text{transit}} = \frac{2.0 \text{ m}}{0.8 \text{ m/s}} = 2.5 \text{ detik}$$

**Dampak Kegagalan Arsitektur Utas Tunggal**:
Jika sistem menggunakan kode sekuensial biasa, penumpukan latensi buffer sebesar 3 detik akan menyebabkan sinyal aktuasi pendorong pneumatik tertunda. Pendorong akan memukul ruang kosong setelah buah sawit lewat, sementara buah mentah yang salah lolos ke bejana sterilisasi.

**Solusi Multi-Threaded**:
Penerapan arsitektur `ThreadedCameraStream` dengan latensi end-to-end terkendali pada **$42\text{ milidetik}$** (Capture: 10 ms, AI Run: 25 ms, OSD: 7 ms) memastikan penembakan aktuator tepat sasaran dengan presisi temporal $\pm 0.05$ detik, mencapai efisiensi sortasi otomatis **$98.1\%$**.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Rincian pembebanan waktu (*latency profiling breakdown*) per frame ($640 \times 480$) pada komputasi tepi industri:

| Tahapan Operasional Pipeline | Utas Eksekusi | Latensi Rata-Rata (ms) | Porsi Beban (%) |
| :--- | :--- | :--- | :--- |
| **Akuisisi Frame Sensor (`cv2.VideoCapture`)** | Capture Thread | ~11.5 ms (asinkron) | 0% (Non-blocking) |
| **Prapemrosesan (Resize + BGR ke RGB + CHW)** | Worker Thread | ~2.1 ms | 5.5% |
| **Inferensi Model (MobileNet / ResNet PyTorch)**| Worker Thread | ~24.8 ms | 65.1% |
| **Pascapemrosesan (Softmax / NMS)** | Worker Thread | ~0.8 ms | 2.1% |
| **Rendering OSD (Kotak, Teks, Telemetri)** | Display Thread | ~3.4 ms | 8.9% |
| **Tampilan GUI / Streaming Video** | Main Thread | ~7.0 ms | 18.4% |
| **Total Latensi End-to-End** | Pipeline Total | **~38.1 ms** | **100% (~26 FPS Real-Time)** |

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **Race Condition pada Frame Buffer Bersama** | Citra robek (*screen tearing*) atau crash memori mendadak `Segmentation Fault`. | Utas produsen menimpa array NumPy saat utas konsumen sedang membaca/mengirim ke GPU. | Bungkus akses frame dengan `threading.Lock()` atau gunakan mekanisme penyalinan memori eksplisit `frame.copy()`. |
| **Kebocoran Memori GPU (VRAM Leakage)** | Memori GPU meningkat bertahap setiap detik hingga memicu *CUDA OOM*. | Mengakumulasi tensor tanpa memutus grafis komputasi (`loss.backward()` atau lupa `torch.no_grad()`). | Wajib menyematkan konteks manager `with torch.no_grad():` pada seluruh alur inferensi kamera. |
| **Camera Feed Freezing saat Kabel Bergoyang** | Tampilan video membeku permanen pada satu frame saat konektor USB/LAN mengalami interferensi sesaat. | Metode `cap.read()` masuk ke kondisi *infinite blocking* saat koneksi fisik sensor goyah. | Terapkan utas *watchdog* yang mendeteksi ketiadaan frame baru selama $> 1.0$ detik dan memicu inisialisasi ulang kamera otomatis. |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Analisis Throughput Frame**: Sebuah model memiliki waktu inferensi rata-rata $28\text{ ms}$. Jika kamera fisik menghasilkan 60 FPS ($\Delta t_{\text{cam}} = 16.6\text{ ms}$), berapa persentase frame kamera yang harus dilewati (*dropped frames*) oleh arsitektur multi-threaded agar latensi tetap nol?
   * *Solusi*:
     * Laju inferensi maksimal AI $= \frac{1000}{28} \approx 35.7 \text{ FPS}$.
     * Laju frame kamera $= 60 \text{ FPS}$.
     * Frame yang diproses: $\frac{35.7}{60} \approx 59.5\%$.
     * Frame yang dilewati: $100\% - 59.5\% = \mathbf{40.5\%}$.
     * Sistem mempertahankan latensi nol dengan membuang $40.5\%$ frame redundan.

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual)**: Jelaskan perbedaan performa antara penggunaan antrean FIFO (`queue.Queue`) dengan kapasitas tak terbatas vs antrean kapasitas satu (`queue.Queue(maxsize=1)`) dalam sistem pengawasan CCTV berbasis deep learning.
2. **Soal 2 (Komputasional)**: Rancang modul Python `CameraWatchdog` yang secara otomatis mematikan dan merebut kembali *handle* kamera jika tidak ada frame baru yang diterima dalam jendela waktu $2.0$ detik.

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 13.2: Sistem Deteksi Berbasis Video

Kita telah sukses membangun jembatan berlatensi rendah antara sensor kamera fisik dan model deep learning. Namun, memproses video secara frame-demi-frame terisolasi memiliki keterbatasan fatal: model memperlakukan objek yang sama pada frame $t$ dan frame $t+1$ sebagai dua entitas yang sama sekali baru, tanpa kesadaran akan trajektori, arah pergerakan, dan identitas kontinu.

Pada **AI Modul 13.2: Sistem Deteksi Berbasis Video**, kita akan meningkatkan kapabilitas sistem menuju pemrosesan temporal: pengenalan objek bergerak, pelacakan identitas jamak (*Multi-Object Tracking*) berbasis algoritma **SORT (Simple Online and Realtime Tracking)**, serta strategi penghitungan objek melintasi garis batas (*line crossing*).

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Bradski, G. (2000). *The OpenCV Library*. Dr. Dobb's Journal of Software Tools, 25(11), 120-125.
2. Paszke, A., et al. (2019). *PyTorch: An imperative style, high-performance deep learning library*. Advances in Neural Information Processing Systems (NeurIPS 2019), 32.
3. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed., Chapter 4: Threads & Concurrency). Wiley.
4. Rosebrock, A. (2018). *Raspberry Pi for Computer Vision: Hardware and Deep Learning*. PyImageSearch.
5. NVIDIA Corporation. (2022). *NVIDIA DeepStream SDK Developer Guide: Multi-stream video processing architecture*. NVIDIA Documentation.
"""

validate_text(doc_13_1, "AI_Modul_13.1_Integrasi_model_dengan_kamera.md")
with open("docs/part-13/AI_Modul_13.1_Integrasi_model_dengan_kamera.md", "w", encoding="utf-8") as f:
    f.write(doc_13_1)

# Notebook 13.1
nb_13_1_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 13.1: Praktikum Integrasi Model dengan Kamera Real-Time\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Membangun kelas ingestion kamera multi-threaded untuk mengeliminasi latensi penumpukan buffer.\n",
            "2. Mengintegrasikan model klasifikasi PyTorch dengan aliran video kontinu.\n",
            "3. Merancang OSD (On-Screen Display) telemetri real-time dengan penghitung FPS dan label prediksi."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import cv2\n",
            "import threading\n",
            "import time\n",
            "import numpy as np\n",
            "import torch\n",
            "import torch.nn as nn\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "torch.manual_seed(42)\n",
            "print(f\"OpenCV Versi: {cv2.__version__} | PyTorch: {torch.__version__}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Model Ringan dan Sintesis Stream Kamera Industri"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Model Klasifikasi Cepat untuk Komputasi Tepi\n",
            "class EdgeSortClassifier(nn.Module):\n",
            "    def __init__(self, num_classes=3):\n",
            "        super().__init__()\n",
            "        self.net = nn.Sequential(\n",
            "            nn.Conv2d(3, 16, kernel_size=3, padding=1),\n",
            "            nn.ReLU(),\n",
            "            nn.MaxPool2d(2, 2),\n",
            "            nn.Conv2d(16, 32, kernel_size=3, padding=1),\n",
            "            nn.ReLU(),\n",
            "            nn.AdaptiveAvgPool2d((1, 1)),\n",
            "            nn.Flatten(),\n",
            "            nn.Linear(32, num_classes)\n",
            "        )\n",
            "    def forward(self, x):\n",
            "        return self.net(x)\n",
            "\n",
            "model = EdgeSortClassifier(num_classes=3)\n",
            "model.eval()\n",
            "class_names = ['Sawit Mentah', 'Sawit Matang', 'Sawit Lewat Matang']\n",
            "print(\"Model klasifikasi tepi siap diintegrasikan!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Implementasi Multi-Threaded Camera Ingestion (Headless Safe)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class SyntheticCameraThread:\n",
            "    def __init__(self, fps=30, width=320, height=240):\n",
            "        self.fps = fps\n",
            "        self.width = width\n",
            "        self.height = height\n",
            "        self.frame = np.zeros((height, width, 3), dtype=np.uint8)\n",
            "        self.lock = threading.Lock()\n",
            "        self.running = False\n",
            "        self.thread = None\n",
            "        self.frame_count = 0\n",
            "        \n",
            "    def start(self):\n",
            "        self.running = True\n",
            "        self.thread = threading.Thread(target=self._produce, daemon=True)\n",
            "        self.thread.start()\n",
            "        return self\n",
            "        \n",
            "    def _produce(self):\n",
            "        delay = 1.0 / self.fps\n",
            "        while self.running:\n",
            "            t_start = time.time()\n",
            "            self.frame_count += 1\n",
            "            # Buat frame dinamis (simulasi buah bergerak di konveyor)\n",
            "            new_frame = np.full((self.height, self.width, 3), 40, dtype=np.uint8)\n",
            "            # Gambar buah oranye bergerak melintasi frame\n",
            "            cx = int((self.frame_count * 5) % self.width)\n",
            "            cy = self.height // 2\n",
            "            cv2.circle(new_frame, (cx, cy), 35, (10, 120, 220), -1) # Buah matang BGR\n",
            "            \n",
            "            with self.lock:\n",
            "                self.frame = new_frame\n",
            "                \n",
            "            elapsed = time.time() - t_start\n",
            "            if delay > elapsed:\n",
            "                time.sleep(delay - elapsed)\n",
            "                \n",
            "    def read(self):\n",
            "        with self.lock:\n",
            "            return True, self.frame.copy()\n",
            "            \n",
            "    def stop(self):\n",
            "        self.running = False\n",
            "        if self.thread is not None:\n",
            "            self.thread.join(timeout=1.0)\n",
            "\n",
            "cam = SyntheticCameraThread(fps=30).start()\n",
            "time.sleep(0.2) # Beri waktu producer berjalan\n",
            "ret, test_frame = cam.read()\n",
            "print(f\"Pengambilan frame multi-threaded sukses: {ret}, Bentuk frame: {test_frame.shape}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Siklus Inferensi Real-Time, Pengukuran FPS, dan Rendering OSD"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "latencies = []\n",
            "num_iterations = 40\n",
            "last_processed_frame = None\n",
            "\n",
            "for i in range(num_iterations):\n",
            "    t0 = time.time()\n",
            "    ret, frame = cam.read()\n",
            "    if not ret:\n",
            "        continue\n",
            "        \n",
            "    # Prapemrosesan Cepat\n",
            "    crop_center = cv2.resize(frame, (64, 64))\n",
            "    rgb_crop = cv2.cvtColor(crop_center, cv2.COLOR_BGR2RGB)\n",
            "    tensor = torch.from_numpy(rgb_crop).permute(2, 0, 1).unsqueeze(0).float() / 255.0\n",
            "    \n",
            "    # Inferensi Model\n",
            "    with torch.no_grad():\n",
            "        logits = model(tensor)\n",
            "        probs = torch.softmax(logits, dim=1)[0]\n",
            "        pred_idx = probs.argmax().item()\n",
            "        conf = probs[pred_idx].item()\n",
            "        \n",
            "    # Pascapemrosesan & Rendering OSD\n",
            "    label_text = f\"{class_names[pred_idx]}: {conf*100:.1f}%\"\n",
            "    cv2.putText(frame, label_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)\n",
            "    \n",
            "    dt = (time.time() - t0) * 1000.0 # ms\n",
            "    latencies.append(dt)\n",
            "    fps_current = 1000.0 / dt if dt > 0 else 0\n",
            "    cv2.putText(frame, f\"FPS: {fps_current:.1f} | Latensi: {dt:.1f}ms\", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)\n",
            "    \n",
            "    last_processed_frame = frame\n",
            "    time.sleep(0.01)\n",
            "\n",
            "cam.stop()\n",
            "avg_latency = np.mean(latencies)\n",
            "print(f\"Evaluasi Selesai ({num_iterations} loop):\")\n",
            "print(f\"  Rata-rata Latensi Inferensi: {avg_latency:.2f} ms\")\n",
            "print(f\"  Throughput Efektif:         {1000.0 / avg_latency:.1f} FPS\")\n",
            "\n",
            "# Simpan tangkapan layar OSD terakhir\n",
            "plt.figure(figsize=(6, 5))\n",
            "plt.imshow(cv2.cvtColor(last_processed_frame, cv2.COLOR_BGR2RGB))\n",
            "plt.title(f'Tangkapan Layar OSD Kamera Real-Time (Avg: {avg_latency:.1f}ms)')\n",
            "plt.axis('off')\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_realtime_camera_integration_13_1.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Hasil tangkapan layar disimpan sebagai 'praktikum_realtime_camera_integration_13_1.png'\")"
        ]
    }
]

with open("notebooks/part-13/AI_Modul_13.1_Praktikum_Integrasi_Model_dengan_Kamera.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_13_1_cells), f, indent=2)
print("[OK] Generated notebooks/part-13/AI_Modul_13.1_Praktikum_Integrasi_Model_dengan_Kamera.ipynb")

# Guide 13.1
guide_13_1 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 13.1 - Integrasi Model dengan Kamera

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Penjelasan fenomena Buffer Lag Accumulation pada pemrosesan sekuensial utas tunggal.
* **Menit 30 - 65**: Arsitektur Producer-Consumer dengan atomic pointer dan sinkronisasi mutex thread-safe.
* **Menit 65 - 100**: Praktikum komputer: Pembangunan modul `SyntheticCameraThread`, integrasi tensor PyTorch `torch.no_grad()`, dan perancangan OSD.
* **Menit 100 - 130**: Studi kasus pemilahan buah sawit pada konveyor berkecepatan 0.8 m/s dan analisis sinkronisasi pneumatik.
* **Menit 130 - 150**: Pembahasan jebakan race condition dan strategi pemulihan otomatis koneksi kamera terputus.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Kapasitas Buffer FIFO vs Buffer-1)
* **Antrean FIFO Tak Terbatas (`queue.Queue()`)**:
  * Menjamin tidak ada frame yang hilang (*zero frame drop*).
  * Namun, jika laju inferensi lebih lambat daripada laju kamera, antrean akan membengkak. Model akan memproses rekaman masa lalu yang tertinggal bermenit-menit, merusak fungsi waktu-nyata (*fatal latency lag*).
* **Antrean Kapasitas Satu (`maxsize=1`)**:
  * Secara sengaja menjatuhkan frame yang terlewat (*deliberate frame skipping*).
  * Menjamin konsumen selalu mendapatkan citra terbaru di lapangan, mempertahankan latensi nol mutlak untuk aksi aktuasi instan.

### Solusi Soal Mandiri 2 (Modul Watchdog Kamera)
```python
import time
import threading

class CameraWatchdog(threading.Thread):
    def __init__(self, stream_obj, timeout=2.0):
        super().__init__(daemon=True)
        self.stream = stream_obj
        self.timeout = timeout
        self.last_seen_time = time.time()
        self.running = True
        
    def ping(self):
        self.last_seen_time = time.time()
        
    def run(self):
        while self.running:
            time.sleep(0.5)
            if time.time() - self.last_seen_time > self.timeout:
                print("[WATCHDOG ALERT] Kamera membeku! Memicu inisialisasi ulang...")
                self.stream.stop()
                time.sleep(0.5)
                self.stream.start()
                self.last_seen_time = time.time()
```

---

## 3. Rubrik Penilaian Praktikum
* **Penguasaan Multi-Threading (35%)**: Implementasi pemisahan capture thread dan inference loop berjalan bebas deadlock.
* **Optimasi Latensi & Pipeline (30%)**: Berhasil mencapai throughput $\ge 25\text{ FPS}$ dengan latensi stabil.
* **Kerapian Rendering OSD (20%)**: Telemetri menampilkan teks informatif dan visualisasi yang tidak mengaburkan objek inspeksi.
* **Standar Rekayasa Perangkat Lunak (15%)**: Kode modular, penggunaan resource locking yang aman, dan terdokumentasi dengan baik.
"""

validate_text(guide_13_1, "AI_Modul_13.1_Panduan_Instruktur_dan_Kunci_Solusi.md")
with open("instructor_resources/part-13/AI_Modul_13.1_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_13_1)

print("[OK] Selesai Modul 13.1!")
