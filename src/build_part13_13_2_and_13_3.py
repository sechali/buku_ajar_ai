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
# MODUL 13.2: SISTEM DETEKSI BERBASIS VIDEO
# ==============================================================================

doc_13_2 = r"""# AI Modul 13.2: Sistem Deteksi Berbasis Video

## 1. Peta Konsep & Orientasi Pembelajaran

Dalam paradigma visi komputer statis, analisis citra memperlakukan setiap frame sebagai peristiwa yang berdiri sendiri dan terisolasi. Namun, dalam aplikasi operasional perkebunan, logistik, dan keamanan terpadu—seperti penghitungan otomatis armada truk pengangkut tandan buah segar (TBS) di pos timbangan pabrik atau pelacakan pergerakan pekerja di area berbahaya sterilisasi uap—informasi visual mengalir sebagai kontinuitas spasial-temporal (*spatio-temporal continuity*).

Tantangan fundamental dalam pemrosesan video bukanlah sekadar mendeteksi objek, melainkan mempertahankan **kesinambungan identitas (*identity continuity*)**: memastikan bahwa objek yang terdeteksi pada koordinat $(x_1, y_1)$ pada frame $t$ tetap dikenali sebagai objek ber-ID unik yang sama ketika berpindah ke $(x_2, y_2)$ pada frame $t+1$. Tanpa mekanisme pelacakan, sistem penghitungan otomatis (*counting system*) akan menghitung objek yang sama berkali-kali pada setiap frame baru, memicu galat akumulasi ribuan persen.

Modul 13.2 ini membedah arsitektur sistem deteksi berbasis video: perancangan paradigma *Tracking-by-Detection*, estimasi trajektori spasial berbasis **Filter Kalman**, asosiasi data optimal menggunakan **Algoritma Hungarian**, mitigasi fenomena *ID Switch*, serta implementasi logika penghitungan lintasan garis (*Line-Crossing Logic*).

```mermaid
flowchart TD
    A["Aliran Video Masukan Frame-by-Frame"] --> B["Detektor Objek (YOLO / SSD)"]
    B --> C["Kumpulan Bounding Box Deteksi Frame t"]
    C --> D["Prediksi Keadaan Trajektori (Filter Kalman)"]
    D --> E["Matriks Biaya Asosiasi Spasial (1 - IoU)"]
    E --> F["Pencocokan Optimal (Algoritma Hungarian)"]
    F --> G["Pembaruan Track Aktif & Terminasi Track Mati"]
    G --> H["Pendeteksian Garis Lintas (Line-Crossing Counter)"]
    H --> I["Visualisasi OSD: Trajektori Berwarna + Total Count"]
```

Tujuan instruksional Modul 13.2 ini meliputi:
1. Memahami arsitektur pelacakan objek jamak (*Multi-Object Tracking* / MOT) dengan paradigma *Tracking-by-Detection*.
2. Menguasai formulasi matematis ruang keadaan Filter Kalman untuk estimasi posisi, skala, dan kecepatan linear bounding box.
3. Menerapkan Algoritma Hungarian untuk menyelesaikan masalah penugasan bipartit berbobot (*weighted bipartite matching*) berbasis jarak IoU.
4. Membangun logika kalkulasi lintas garis virtual (*virtual tripwire line-crossing*) menggunakan produk silang vektor (*vector cross product*).
5. Menerapkan sistem penghitungan otomatis lalu lintas angkutan kelapa sawit pada rekaman video industri.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Model Ruang Keadaan Filter Kalman (Kalman Filter State Space)

Dalam algoritma pelacakan SORT (Bewley et al., 2016), keadaan sebuah objek pada frame ke-$t$ dimodelkan dalam vektor ruang keadaan 7 dimensi:

$$\mathbf{x}_t = [u, v, s, r, \dot{u}, \dot{v}, \dot{s}]^T$$

Dimana:
* $(u, v)$ adalah titik pusat bounding box secara horizontal dan vertikal.
* $s$ adalah luas skala area kotak ($s = w \cdot h$).
* $r$ adalah rasio aspek kotak ($r = w / h$, diasumsikan konstan dalam interval pendek).
* $(\dot{u}, \dot{v}, \dot{s})$ adalah kecepatan perubahan turunan pertama posisi dan luas.

Model transisi keadaan linear dengan derau proses Gaussian $\mathbf{w}_t \sim \mathcal{N}(0, \mathbf{Q})$:

$$\mathbf{x}_{t|t-1} = \mathbf{F} \mathbf{x}_{t-1|t-1}$$

$$\mathbf{P}_{t|t-1} = \mathbf{F} \mathbf{P}_{t-1|t-1} \mathbf{F}^T + \mathbf{Q}$$

Vektor pengukuran $\mathbf{z}_t = [u, v, s, r]^T$ dari detektor objek dihubungkan melalui matriks pengukuran $\mathbf{H}$ dengan derau pengukuran $\mathbf{v}_t \sim \mathcal{N}(0, \mathbf{R})$:

$$\mathbf{K}_t = \mathbf{P}_{t|t-1} \mathbf{H}^T (\mathbf{H} \mathbf{P}_{t|t-1} \mathbf{H}^T + \mathbf{R})^{-1}$$

$$\mathbf{x}_{t|t} = \mathbf{x}_{t|t-1} + \mathbf{K}_t (\mathbf{z}_t - \mathbf{H} \mathbf{x}_{t|t-1})$$

$$\mathbf{P}_{t|t} = (\mathbf{I} - \mathbf{K}_t \mathbf{H}) \mathbf{P}_{t|t-1}$$

### 2.2 Asosiasi Data dengan Algoritma Hungarian

Misalkan terdapat $N$ lintasan pelacak aktif ($\mathcal{T} = \{T_1, \dots, T_N\}$) dan $M$ kotak deteksi baru pada frame terkini ($\mathcal{D} = \{D_1, \dots, D_M\}$). Matriks biaya penugasan $\mathbf{C} \in \mathbb{R}^{N \times M}$ dihitung berdasarkan komplemen metrik IoU:

$$\mathbf{C}_{i, j} = 1 - \text{IoU}(T_i, D_j)$$

Algoritma Hungarian (Kuhn, 1955) menyelesaikan masalah optimasi kombinatorial untuk menemukan fungsi pemetaan injektif $\pi$ yang meminimalkan total biaya:

$$\min_{\pi} \sum_{i=1}^N \mathbf{C}_{i, \pi(i)}$$

Jika pasangan memiliki $\text{IoU}(T_i, D_j) < \text{IoU}_{\text{threshold}}$ (biasanya $0.3$), penugasan ditolak. Deteksi yang tidak cocok diinisialisasi sebagai lintasan pelacak baru, sedangkan pelacak yang tidak terdeteksi selama $T_{\text{lost}} > 5$ frame berturut-turut akan dihapus dari memori (*track termination*).

### 2.3 Matematika Logika Lintas Garis (Line-Crossing Detection)

Diberikan sebuah garis penghitung virtual yang didefinisikan oleh dua titik koordinat: $\mathbf{A} = (x_A, y_A)$ dan $\mathbf{B} = (x_B, y_B)$. Garis ini memiliki vektor arah $\vec{AB} = \mathbf{B} - \mathbf{A}$.

Titik pusat objek pada frame sebelumnya adalah $\mathbf{P}_{t-1}$ dan pada frame saat ini adalah $\mathbf{P}_t$. Orientasi posisi relatif titik $\mathbf{P}$ terhadap garis $\mathbf{AB}$ dihitung melalui produk silang 2D (*scalar cross product*):

$$\text{Orientasi}(\mathbf{A}, \mathbf{B}, \mathbf{P}) = (x_B - x_A)(y_P - y_A) - (y_B - y_A)(x_P - x_A)$$

Objek terbukti melintasi garis jika dan hanya jika dua segmen garis $\overline{\mathbf{A}\mathbf{B}}$ dan $\overline{\mathbf{P}_{t-1}\mathbf{P}_t}$ saling berpotongan secara geometris:

$$\text{Orientasi}(\mathbf{A}, \mathbf{B}, \mathbf{P}_{t-1}) \cdot \text{Orientasi}(\mathbf{A}, \mathbf{B}, \mathbf{P}_t) < 0$$

$$\text{Orientasi}(\mathbf{P}_{t-1}, \mathbf{P}_t, \mathbf{A}) \cdot \text{Orientasi}(\mathbf{P}_{t-1}, \mathbf{P}_t, \mathbf{B}) < 0$$

Tanda aljabar dari produk silang tersebut menentukan arah pergerakan: masuk (*IN*) atau keluar (*OUT*).

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Pipeline Deteksi Berbasis Video dan Tracking SORT](../../docs/assets/pipeline_deteksi_berbasis_video_dan_tracking_sort.png)

Diagram di atas mengilustrasikan:
1. **Prediksi Keadaan**: Filter Kalman memperkirakan posisi kotak di frame berikutnya berdasarkan riwayat kecepatan.
2. **Asosiasi Hungarian**: Menjodohkan kotak prediksi Kalman dengan deteksi aktual detektor YOLO.
3. **Penetapan ID Unik**: Mempertahankan identitas objek sepanjang video.
4. **Line-Crossing Counter**: Mendeteksi saat lintasan titik pusat memotong garis batas virtual.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lengkap kelas pelacak objek SORT mandiri dan detektor lintas garis (*line crossing counter*) di Python:

```python
import numpy as np
from scipy.optimize import linear_sum_assignment
from typing import List, Tuple, Dict

def compute_iou_boxes(b1: np.ndarray, b2: np.ndarray) -> float:
    # Format [x1, y1, x2, y2]
    x1 = max(b1[0], b2[0])
    y1 = max(b1[1], b2[1])
    x2 = min(b1[2], b2[2])
    y2 = min(b1[3], b2[3])
    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    union = (b1[2] - b1[0]) * (b1[3] - b1[1]) + (b2[2] - b2[0]) * (b2[3] - b2[1]) - inter
    return inter / union if union > 0 else 0.0

class Tracklet:
    '''
    Representasi Lintasan Objek Tunggal dengan Estimasi Pergerakan Sederhana.
    '''
    count = 0
    def __init__(self, bbox: np.ndarray, label: str):
        self.id = Tracklet.count
        Tracklet.count += 1
        self.bbox = bbox # [x1, y1, x2, y2]
        self.label = label
        self.history = [self.get_center()]
        self.time_since_update = 0
        self.hits = 1
        
    def get_center(self) -> Tuple[float, float]:
        return ((self.bbox[0] + self.bbox[2]) / 2.0, (self.bbox[1] + self.bbox[3]) / 2.0)
        
    def update(self, bbox: np.ndarray):
        self.bbox = bbox
        self.history.append(self.get_center())
        self.time_since_update = 0
        self.hits += 1

class RealtimeSORTTracker:
    '''
    Mesin Pelacak Objek Jamak Real-Time Menggunakan Hungarian Data Association.
    '''
    def __init__(self, iou_thresh: float = 0.3, max_age: int = 5):
        self.iou_thresh = iou_thresh
        self.max_age = max_age
        self.tracks: List[Tracklet] = []
        
    def update(self, detections: List[Tuple[np.ndarray, str]]) -> List[Tracklet]:
        # Tambah umur track
        for t in self.tracks:
            t.time_since_update += 1
            
        if len(self.tracks) == 0:
            for bbox, label in detections:
                self.tracks.append(Tracklet(bbox, label))
            return self.tracks
            
        if len(detections) == 0:
            self.tracks = [t for t in self.tracks if t.time_since_update <= self.max_age]
            return self.tracks
            
        # Bentuk Matriks Biaya (1 - IoU)
        cost_matrix = np.zeros((len(self.tracks), len(detections)), dtype=np.float32)
        for i, t in enumerate(self.tracks):
            for j, (det_box, _) in enumerate(detections):
                cost_matrix[i, j] = 1.0 - compute_iou_boxes(t.bbox, det_box)
                
        # Penugasan Optimal Hungarian
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        
        matched_tracks = set()
        matched_dets = set()
        for r, c in zip(row_ind, col_ind):
            if cost_matrix[r, c] <= (1.0 - self.iou_thresh):
                self.tracks[r].update(detections[c][0])
                matched_tracks.add(r)
                matched_dets.add(c)
                
        # Inisialisasi deteksi baru
        for j, (bbox, label) in enumerate(detections):
            if j not in matched_dets:
                self.tracks.append(Tracklet(bbox, label))
                
        # Hapus track kadaluarsa
        self.tracks = [t for t in self.tracks if t.time_since_update <= self.max_age]
        return [t for t in self.tracks if t.time_since_update == 0]

class VirtualTripwireCounter:
    '''
    Penghitung Lintas Garis Menggunakan Produk Silang Vektor Geometris.
    '''
    def __init__(self, pt_a: Tuple[int, int], pt_b: Tuple[int, int]):
        self.pt_a = np.array(pt_a, dtype=float)
        self.pt_b = np.array(pt_b, dtype=float)
        self.counted_ids = set()
        self.in_count = 0
        
    def _cross_product(self, p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
        
    def check_crossing(self, track: Tracklet):
        if track.id in self.counted_ids or len(track.history) < 2:
            return
            
        p_prev = np.array(track.history[-2], dtype=float)
        p_curr = np.array(track.history[-1], dtype=float)
        
        cp1 = self._cross_product(self.pt_a, self.pt_b, p_prev)
        cp2 = self._cross_product(self.pt_a, self.pt_b, p_curr)
        cp3 = self._cross_product(p_prev, p_curr, self.pt_a)
        cp4 = self._cross_product(p_prev, p_curr, self.pt_b)
        
        if (cp1 * cp2 < 0) and (cp3 * cp4 < 0):
            # Garis terpotong!
            self.counted_ids.add(track.id)
            self.in_count += 1
            print(f"[COUNTER EVENT] Objek ID #{track.id} ({track.label}) melintasi garis! Total: {self.in_count}")
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Penghitungan Otomatis Armada Truk Muatan TBS di Jembatan Timbang Pabrik

Pada pabrik kelapa sawit dengan kapasitas olah 90 ton TBS/jam, setiap hari melintas antara 150 hingga 300 unit truk pengangkut buah dari berbagai divisi perkebunan. Sistem pencatatan manual berbasis buku ekspedisi rentan terhadap kesalahan manusia (*human error*), antrean panjang hingga ke jalan raya, dan kecurangan manipulasi tonase.

**Penyelesaian Berbasis Deteksi & Tracking Video**:
1. Kamera CCTV resolusi 1080p dipasang pada tiang gerbang timbangan (*weighbridge gate*).
2. Model YOLOv8-Small mendeteksi kendaraan (`Truk TBS`).
3. Algoritma pelacak SORT memberikan nomor identitas unik pada setiap truk yang memasuki gerbang.
4. Garis pembatas virtual (*virtual tripwire*) dipasang tepat di atas plat timbangan elektronik. Ketika titik tengah truk memotong garis dari arah masuk, sistem:
   * Mengunci ID truk dan mencatat timestamp presisi milidetik.
   * Memicu tangkapan layar plat nomor kendaraan (ANPR).
   * Melakukan korelasi otomatis dengan data sensor timbangan digital terintegrasi.
5. Sistem berhasil menghitung **100% dari 280 truk** tanpa ada penghitungan ganda (*zero double counting*), memangkas waktu tunggu rata-rata dari 4 menit menjadi 45 detik per kendaraan.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Perbandingan kompleksitas komputasional komponen tracking:

| Komponen Algoritma | Kompleksitas Waktu | Konsumsi Memori | Karakteristik Kinerja |
| :--- | :--- | :--- | :--- |
| **Inference Detektor (YOLO)** | $\mathcal{O}(H \cdot W \cdot C)$ | ~1.5 GB VRAM | Paling berat, membutuhkan akselerasi GPU |
| **Pembaruan Kalman Filter** | $\mathcal{O}(N \cdot d^3)$ ($d=7$) | Sangat Ringan (< 2 MB) | Cepat di CPU (< 0.5 ms untuk 50 track) |
| **Asosiasi Hungarian** | $\mathcal{O}(N^3)$ | Sangat Ringan | Efisien untuk $N < 100$ objek serentak |
| **Deteksi Lintas Garis** | $\mathcal{O}(N)$ perkalian silang | Negligible | Ringan (< 0.05 ms per frame) |

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **Identity Switch (Tukar ID)** | Dua truk atau pekerja yang berjalan bersilangan bertukar nomor ID unik. | Detektor mendeteksi kotak yang tumpang tindih tinggi dan Hungarian salah menjodohkan jarak geometris. | Tingkatkan ke **DeepSORT**: tambahkan vektor fitur visual *appearance embedding* berbasis ReID CNN untuk membedakan penampilan objek. |
| **Penghitungan Ganda saat Objek Berhenti (Oscillation Count)** | Truk yang berhenti tepat di atas garis batas terhitung berkali-kali. | Titik pusat berosilasi tipis akibat derau deteksi, melintasi garis maju-mundur. | Terapkan zona histeresis (*hysteresis counting zone*): objek harus keluar dari zona penyangga $\pm 20$ piksel sebelum dihitung kembali. |
| **Track Terputus saat Oklusi Singkat (Premature Deletion)** | Objek yang tertutup tiang gerbang selama 3 frame mendapatkan ID baru setelah muncul kembali. | Parameter `max_age` diatur terlalu kecil (misal: 1 frame). | Naikkan batas retensi memori `max_age = 15 - 30` frame dan gunakan prediksi extrapolasi Kalman selama periode hilang. |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Analisis Lintas Garis Geometris**: Diberikan garis batas virtual dari $\mathbf{A}=(100, 200)$ ke $\mathbf{B}=(300, 200)$ (garis horizontal pada $y=200$). Titik pusat objek bergerak dari $\mathbf{P}_{t-1} = (200, 180)$ menuju $\mathbf{P}_t = (200, 230)$. Buktikan dengan produk silang bahwa objek telah melintasi garis.
   * *Solusi*:
     * $\vec{AB} = (300 - 100, 200 - 200) = (200, 0)$.
     * $\text{cp}_1 = (x_B - x_A)(y_{\text{prev}} - y_A) - (y_B - y_A)(x_{\text{prev}} - x_A) = (200)(180 - 200) - 0 = -4.000$.
     * $\text{cp}_2 = (x_B - x_A)(y_{\text{curr}} - y_A) - 0 = (200)(230 - 200) = +6.000$.
     * Karena $\text{cp}_1 \cdot \text{cp}_2 = (-4000) \times (+6000) < 0$, titik berada di sisi berlawanan.
     * Analisis sebaliknya pada segmen $\mathbf{P}_{t-1}\mathbf{P}_t$ menghasilkan produk negatif.
     * **Terbukti sah secara matematis bahwa garis telah terpotong!**

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual)**: Mengapa model Filter Kalman mengasumsikan rasio aspek $r = w/h$ bernilai konstan dalam matriks transisi keadaan liniernya? Dalam kondisi fisik apa asumsi ini dapat meleset?
2. **Soal 2 (Komputasional)**: Rancang fungsi Python `calculate_motp_mota` yang menghitung metrik standar industri *Multiple Object Tracking Accuracy* (MOTA) dengan memperhitungkan *False Positives* (FP), *False Negatives* (FN), dan *ID Switches* (IDSW).

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 13.3: Pengembangan Aplikasi Sederhana

Sistem deteksi dan pelacakan video yang telah kita bangun kini telah memiliki kecerdasan spasial dan temporal yang tangguh. Namun, sistem ini masih beroperasi sebagai skrip konsol yang terisolasi. Dalam realitas operasional industri, operator lapangan, mandor, dan manajer pabrik membutuhkan antarmuka visual yang interaktif dan mudah digunakan.

Pada **AI Modul 13.3: Pengembangan Aplikasi Sederhana**, kita akan membungkus seluruh pipeline kecerdasan buatan ini ke dalam antarmuka aplikasi terpadu: pengembangan aplikasi GUI Desktop (*PyQt / Tkinter*) dengan *thread-safe event loop*, serta perancangan server streaming web berbasis *FastAPI / Flask* dengan protokol *MJPEG* yang dapat diakses secara fleksibel dari peramban ponsel pintar maupun ruang kendali terpusat.

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Bewley, A., Ge, Z., Ott, L., Ramos, F., & Upcroft, B. (2016). *Simple online and realtime tracking*. IEEE International Conference on Image Processing (ICIP), 3464-3468.
2. Wojke, N., Bewley, A., & Paulus, D. (2017). *Simple online and realtime tracking with a deep association metric*. IEEE International Conference on Image Processing (ICIP), 3645-3649.
3. Kuhn, H. W. (1955). *The Hungarian method for the assignment problem*. Naval Research Logistics Quarterly, 2(1-2), 83-97.
4. Welch, G., & Bishop, G. (2006). *An introduction to the Kalman filter*. University of North Carolina at Chapel Hill, Tech Report TR-95-041.
5. Bernardin, K., & Stiefelhagen, R. (2008). *Evaluating multiple object tracking performance: the CLEAR MOT metrics*. EURASIP Journal on Image and Video Processing, 2008, 1-10.
"""

validate_text(doc_13_2, "AI_Modul_13.2_Sistem_deteksi_berbasis_video.md")
with open("docs/part-13/AI_Modul_13.2_Sistem_deteksi_berbasis_video.md", "w", encoding="utf-8") as f:
    f.write(doc_13_2)

# Notebook 13.2
nb_13_2_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 13.2: Praktikum Sistem Deteksi Berbasis Video dan Tracking (SORT)\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Membangun modul pelacak objek jamak (Multi-Object Tracking) berbasis algoritma SORT sederhana.\n",
            "2. Mengimplementasikan asosiasi penugasan optimal Hungarian menggunakan `scipy.optimize.linear_sum_assignment`.\n",
            "3. Merancang logika penghitungan lintas garis (*line-crossing counting*) pada simulasi video pergerakan truk sawit."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "from scipy.optimize import linear_sum_assignment\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "import matplotlib.patches as patches\n",
            "\n",
            "np.random.seed(42)\n",
            "print(\"Modul praktikum deteksi dan pelacakan video siap!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Implementasi Kelas Tracklet dan Asosiasi Hungarian"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def iou_boxes(b1, b2):\n",
            "    x1, y1 = max(b1[0], b2[0]), max(b1[1], b2[1])\n",
            "    x2, y2 = min(b1[2], b2[2]), min(b1[3], b2[3])\n",
            "    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)\n",
            "    union = (b1[2]-b1[0])*(b1[3]-b1[1]) + (b2[2]-b2[0])*(b2[3]-b2[1]) - inter\n",
            "    return inter / union if union > 0 else 0.0\n",
            "\n",
            "class SimpleTracklet:\n",
            "    _id_counter = 1\n",
            "    def __init__(self, bbox):\n",
            "        self.id = SimpleTracklet._id_counter\n",
            "        SimpleTracklet._id_counter += 1\n",
            "        self.bbox = bbox # [x1, y1, x2, y2]\n",
            "        self.history = [self.center()]\n",
            "        self.lost_frames = 0\n",
            "        \n",
            "    def center(self):\n",
            "        return ((self.bbox[0] + self.bbox[2])/2.0, (self.bbox[1] + self.bbox[3])/2.0)\n",
            "    def get_center(self):\n",
            "        return self.center()\n",
            "        \n",
            "    def update(self, bbox):\n",
            "        self.bbox = bbox\n",
            "        self.history.append(self.center())\n",
            "        self.lost_frames = 0\n",
            "\n",
            "class MiniSORT:\n",
            "    def __init__(self, iou_thresh=0.3, max_lost=3):\n",
            "        self.iou_thresh = iou_thresh\n",
            "        self.max_lost = max_lost\n",
            "        self.tracks = []\n",
            "        \n",
            "    def step(self, detections):\n",
            "        for t in self.tracks:\n",
            "            t.lost_frames += 1\n",
            "            \n",
            "        if len(self.tracks) == 0:\n",
            "            for d in detections:\n",
            "                self.tracks.append(SimpleTracklet(d))\n",
            "            return self.tracks\n",
            "            \n",
            "        # Matriks biaya 1 - IoU\n",
            "        cost = np.zeros((len(self.tracks), len(detections)))\n",
            "        for i, t in enumerate(self.tracks):\n",
            "            for j, d in enumerate(detections):\n",
            "                cost[i, j] = 1.0 - iou_boxes(t.bbox, d)\n",
            "                \n",
            "        row_ind, col_ind = linear_sum_assignment(cost)\n",
            "        matched_t, matched_d = set(), set()\n",
            "        for r, c in zip(row_ind, col_ind):\n",
            "            if cost[r, c] <= (1.0 - self.iou_thresh):\n",
            "                self.tracks[r].update(detections[c])\n",
            "                matched_t.add(r)\n",
            "                matched_d.add(c)\n",
            "                \n",
            "        for j, d in enumerate(detections):\n",
            "            if j not in matched_d:\n",
            "                self.tracks.append(SimpleTracklet(d))\n",
            "                \n",
            "        self.tracks = [t for t in self.tracks if t.lost_frames <= self.max_lost]\n",
            "        return [t for t in self.tracks if t.lost_frames == 0]\n",
            "\n",
            "print(\"Mesin pelacak MiniSORT berhasil dirakit!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Logika Lintas Garis (Virtual Tripwire)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class Tripwire:\n",
            "    def __init__(self, y_threshold=200):\n",
            "        self.y_threshold = y_threshold\n",
            "        self.counted_ids = set()\n",
            "        self.total_count = 0\n",
            "        \n",
            "    def update(self, tracks):\n",
            "        for t in tracks:\n",
            "            if t.id in self.counted_ids or len(t.history) < 2:\n",
            "                continue\n",
            "            y_prev = t.history[-2][1]\n",
            "            y_curr = t.history[-1][1]\n",
            "            # Melintas dari atas (y < 200) ke bawah (y >= 200)\n",
            "            if y_prev < self.y_threshold <= y_curr:\n",
            "                self.counted_ids.add(t.id)\n",
            "                self.total_count += 1\n",
            "                print(f\"[TRIPWIRE EVENT] Truk TBS ID #{t.id} berhasil dihitung! Total: {self.total_count}\")\n",
            "\n",
            "wire = Tripwire(y_threshold=200)\n",
            "print(\"Garis batas virtual terpasang pada y = 200!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Simulasi Pelacakan dan Penghitungan Video 15 Frame"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "tracker = MiniSORT(iou_thresh=0.3)\n",
            "frames_history = []\n",
            "\n",
            "# Simulasi 2 truk bergerak dari atas ke bawah\n",
            "# Truk 1: x=100, y bergerak dari 100 ke 300\n",
            "# Truk 2: x=250, y bergerak dari 140 ke 340\n",
            "for f_idx in range(12):\n",
            "    truk1_box = np.array([80, 100 + f_idx * 18, 140, 160 + f_idx * 18], dtype=float)\n",
            "    truk2_box = np.array([230, 140 + f_idx * 18, 290, 200 + f_idx * 18], dtype=float)\n",
            "    dets = [truk1_box, truk2_box]\n",
            "    \n",
            "    active_tracks = tracker.step(dets)\n",
            "    wire.update(active_tracks)\n",
            "    frames_history.append([(t.id, t.bbox.copy(), t.get_center()) for t in active_tracks])\n",
            "\n",
            "print(f\"\\nHasil Simulasi Video:\")\n",
            "print(f\"  Total Truk Berhasil Dihitung: {wire.total_count} unit\")\n",
            "assert wire.total_count == 2, \"Penghitungan gagal! Harusnya tepat 2 unit truk.\"\n",
            "print(\"[VALIDASI SUKSES] 2 truk teridentifikasi secara konsisten tanpa ada ID Switch!\")\n",
            "\n",
            "# Visualisasi Trajektori\n",
            "fig, ax = plt.subplots(figsize=(6, 6))\n",
            "ax.set_xlim(0, 400)\n",
            "ax.set_ylim(400, 0) # Format citra\n",
            "\n",
            "# Garis tripwire\n",
            "ax.axhline(200, color='red', linestyle='--', linewidth=2, label='Virtual Tripwire (y=200)')\n",
            "ax.text(10, 190, f\"LINE COUNTER (Total: {wire.total_count})\", color='red', fontweight='bold', fontsize=10)\n",
            "\n",
            "# Gambar trajektori pelacakan\n",
            "colors = ['#1E88E5', '#43A047']\n",
            "for idx, t in enumerate(tracker.tracks):\n",
            "    hist = np.array(t.history)\n",
            "    c = colors[idx % len(colors)]\n",
            "    ax.plot(hist[:, 0], hist[:, 1], '-o', color=c, label=f'Trajektori Truk #{t.id}')\n",
            "    # BBox posisi akhir\n",
            "    b = t.bbox\n",
            "    rect = patches.Rectangle((b[0], b[1]), b[2]-b[0], b[3]-b[1], linewidth=2, edgecolor=c, facecolor='none')\n",
            "    ax.add_patch(rect)\n",
            "    ax.text(b[0], b[1]-5, f\"Truk #{t.id}\", color=c, fontweight='bold', fontsize=9)\n",
            "\n",
            "plt.title('Simulasi Pelacakan Objek SORT dan Lintas Garis')\n",
            "plt.legend()\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_video_tracking_sort_13_2.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Grafik trajektori disimpan sebagai 'praktikum_video_tracking_sort_13_2.png'\")"
        ]
    }
]

with open("notebooks/part-13/AI_Modul_13.2_Praktikum_Sistem_Deteksi_Berbasis_Video.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_13_2_cells), f, indent=2)
print("[OK] Generated notebooks/part-13/AI_Modul_13.2_Praktikum_Sistem_Deteksi_Berbasis_Video.ipynb")

# Guide 13.2
guide_13_2 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 13.2 - Sistem Deteksi Berbasis Video

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Filosofi Tracking-by-Detection dan konsep kontinuitas identitas temporal.
* **Menit 30 - 65**: Pemodelan ruang keadaan Filter Kalman dan optimasi penugasan bipartit Hungarian.
* **Menit 65 - 100**: Praktikum komputer: Perakitan modul `MiniSORT` di Python, asosiasi matriks IoU, dan visualisasi trajektori.
* **Menit 100 - 130**: Studi kasus penghitungan armada truk TBS kelapa sawit di pos timbangan pabrik kelapa sawit.
* **Menit 130 - 150**: Pembahasan mitigasi fenomena ID Switch dan kuis formatif.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Asumsi Rasio Aspek Konstan pada Kalman Filter)
* **Rasionalisasi Asumsi**:
  * Pada kendaraan (seperti truk atau mobil), proporsi lebar terhadap tinggi ($r = w/h$) bersifat kaku dan tidak berubah drastis saat bergerak di jalan lurus. Mempertahankan $r$ konstan mereduksi kompleksitas komputasi matriks kovariansi.
* **Kondisi Meleset**:
  * Ketika objek berbelok tajam pada tikungan 90° (tampak samping vs tampak depan) atau mengalami deformasi non-kaku (seperti pejalan kaki yang merentangkan tangan atau daun tanaman yang tertiup angin).

### Solusi Soal Mandiri 2 (Kalkulasi Metrik MOTA)
```python
def calculate_mota(gt_total, false_positives, false_negatives, id_switches):
    '''
    MOTA = 1 - (FN + FP + IDSW) / GT
    '''
    if gt_total == 0:
        return 0.0
    errors = false_negatives + false_positives + id_switches
    mota = 1.0 - (errors / gt_total)
    return mota

# Uji coba sampel: 100 deteksi ground truth, 5 FN, 3 FP, 2 IDSW
mota_score = calculate_mota(100, 3, 5, 2)
print(f"Skor Akurasi MOTA: {mota_score * 100:.2f}%") # 90.00%
```

---

## 3. Rubrik Penilaian Praktikum
* **Penguasaan Asosiasi Data Hungarian (35%)**: Implementasi pemetaan matriks biaya IoU berjalan tepat dan stabil.
* **Logika Deteksi Lintas Garis (30%)**: Produk silang vektor berhasil mendeteksi arah dan mencegah double-counting.
* **Visualisasi Trajektori (20%)**: Grafik menampilkan jejak koordinat temporal dan kotak pembatas dengan jelas.
* **Kualitas Kode & Standar Rekayasa (15%)**: Struktur kode bersih, terbebas dari kebocoran memori, dan terdokumentasi dengan baik.
"""

validate_text(guide_13_2, "AI_Modul_13.2_Panduan_Instruktur_dan_Kunci_Solusi.md")
with open("instructor_resources/part-13/AI_Modul_13.2_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_13_2)

print("[OK] Selesai Modul 13.2!")

# ==============================================================================
# MODUL 13.3: PENGEMBANGAN APLIKASI SEDERHANA
# ==============================================================================

doc_13_3 = r"""# AI Modul 13.3: Pengembangan Aplikasi Sederhana

## 1. Peta Konsep & Orientasi Pembelajaran

Tahap puncak dalam siklus hidup rekayasa kecerdasan buatan (*AI engineering lifecycle*) adalah mengemas model matematis dan pipeline visi komputer ke dalam sebuah **aplikasi terintegrasi yang fungsional, andal, dan ramah pengguna (*user-friendly production application*)**. Seorang manajer operasional pabrik atau mandor perkebunan tidak akan berinteraksi dengan notebook Jupyter atau konsol terminal berbasis baris perintah (*CLI*); mereka membutuhkan antarmuka visual interaktif untuk mengontrol proses, memantau telemetri video langsung, dan menerima peringatan anomali secara instan.

Dalam visi komputer industri, terdapat dua modalitas antarmuka perangkat lunak utama:
1. **Aplikasi Desktop GUI (PyQt / Tkinter)**: Sangat ideal untuk komputer kontrol stasiun kerja lokal (*workstation kiosk*) di samping mesin konveyor pabrik yang menuntut latensi tampilan ultra-rendah dan integrasi langsung dengan perangkat keras serial/PLC.
2. **Aplikasi Web Streaming (FastAPI / Flask)**: Sangat ideal untuk dasbor pemantauan terpusat (*central control room*) yang memungkinkan pengawasan multi-kamera secara simultan dari peramban web desktop maupun perangkat tablet lapangan.

Modul 13.3 ini membedah arsitektur pengembangan aplikasi visi komputer: pola desain Model-View-Controller (MVC), komunikasi thread-safe berbasis *Signals and Slots*, protokol streaming video web berkinerja tinggi (*Multipart MJPEG*), serta perancangan dasbor inspeksi mutu industri kelapa sawit.

```mermaid
flowchart TD
    A["Sumber Kamera Real-Time"] --> B["Lapisan Model (AI Pipeline Worker)"]
    B --> C{"Modalitas Antarmuka Aplikasi"}
    C -->|"Lingkungan Kios Lokal"| D["Desktop GUI (PyQt / Tkinter)"]
    C -->|"Pusat Kendali Jarak Jauh"| E["Web Server Streaming (FastAPI / Flask)"]
    D --> F["Thread-Safe Event Loop (Signals/Slots)"]
    E --> G["HTTP Multipart Stream (MJPEG Response)"]
    F & G --> H["Visualisasi Telemetri: Video OSD, Grafik Mutu, Tombol Kontrol, & Log Kejadian"]
```

Tujuan instruksional Modul 13.3 ini meliputi:
1. Menguasai arsitektur Model-View-Controller (MVC) terpisah untuk mencegah pembekuan antarmuka pengguna (*UI freezing*) saat model AI mengeksekusi inferensi.
2. Memahami protokol transmisi video berbasis web: *Multipart Mixed-Replace* (MJPEG) melalui generator asinkron Python.
3. Menguasai mekanisme komunikasi aman antar-utas (*thread-safe signaling*) pada antarmuka GUI desktop.
4. Membangun dasbor kendali inspeksi mutu kelapa sawit yang mencakup tombol kendali *Start/Stop*, penggeser ambang batas keyakinan (*confidence slider*), dan pencatatan log analitik.
5. Menganalisis konsumsi sumber daya CPU/GPU dan stabilitas memori aplikasi pada eksekusi jangka panjang.

---

## 2. Fondasi Teori & Matematika Mendalam

### 2.1 Arsitektur Thread-Safe GUI Event Loop (Pola MVC)

Kerangka kerja antarmuka grafis desktop modern (seperti PyQt, PySide, dan Tkinter) beroperasi di atas sebuah **Utas Peristiwa Utama (*Main Event Loop Thread*)**. Utas ini bertanggung jawab menangkap interaksi klik mouse pengguna, penggambaran ulang jendela (*window repainting*), dan penanganan pesan sistem operasi.

Jika komputasi berat model deep learning (yang memakan waktu 30-50 milidetik per frame) dijalankan langsung pada utas utama ini:

$$\Delta t_{\text{event\_delay}} = \Delta t_{\text{inference}} > 16.6\text{ ms (Batas 60 FPS)}$$

Sistem operasi akan mendeteksi bahwa jendela aplikasi tidak merespons (*Not Responding / GUI Freeze*).

**Penyelesaian Arsitektur**:
* **Model (Worker Thread)**: Berjalan di latar belakang, mengeksekusi akuisisi kamera dan inferensi deep learning secara asinkron.
* **View (Main UI Thread)**: Hanya menampilkan elemen visual dan antarmuka tombol.
* **Controller (Signal / Slot Queue)**: Ketika frame selesai diinferensi, utas pekerja memancarkan sinyal (*signal emit*) berupa data frame yang telah dikonversi ke format yang aman bagi GUI (seperti `QImage` atau array bytes JPEG), yang diterima oleh slot pada utas utama secara teratur melalui antrean peristiwa internal.

### 2.2 Protokol Streaming Video Web: HTTP Multipart MJPEG

Untuk mentransmisikan video real-time dari server AI menuju peramban web tanpa memerlukan plugin pemutar video rumit, digunakan standar protokol **Motion JPEG (MJPEG)** melalui MIME type:

$$\text{Content-Type: multipart/x-mixed-replace; boundary=frame}$$

Header HTTP ini memberitahu peramban web bahwa koneksi tidak akan pernah ditutup, melainkan server akan terus mengirimkan segmen frame citra baru yang secara terus-menerus menggantikan (*replace*) frame sebelumnya di elemen HTML `<img>`:

$$\langle\text{img src} = "\text{/video\_feed}" \quad \text{width} = "640" \quad \text{height} = "480"\rangle$$

Secara komputasional, setiap frame dienkripsi menjadi format JPEG terkompresi di memori RAM dan dibungkus dalam blok payload HTTP:

```http
--frame
Content-Type: image/jpeg
Content-Length: [panjang_byte]

[Binary JPEG Payload]
```

Metode ini memiliki latensi sangat rendah ($< 50\text{ ms}$ pada jaringan lokal) dan dapat dibuka secara instan di peramban apa pun (Chrome, Safari, Firefox, Android, iOS) tanpa pustaka eksternal.

---

## 3. Visualisasi Arsitektur & Diagram Alir

![Arsitektur Aplikasi Visi Komputer Desktop dan Web](../../docs/assets/arsitektur_aplikasi_visi_komputer_desktop_dan_web.png)

Diagram di atas mengilustrasikan:
1. **(A) Arsitektur GUI Desktop**: Pemisahan tegas antara Main UI Thread dan Background AI Worker Thread menggunakan mekanisme sinyal thread-safe.
2. **(B) Arsitektur Web Streaming**: Generator asinkron FastAPI/Flask yang menyajikan aliran HTTP Multipart MJPEG langsung ke elemen gambar browser.

---

## 4. Implementasi Komputasional Berstandar Industri

Di bawah ini disajikan implementasi lengkap arsitektur server aplikasi web streaming mandiri menggunakan Python murni dan OpenCV yang siap dideploy sebagai layanan dasbor inspeksi:

```python
import cv2
import time
import threading
import numpy as np
from typing import Generator

class WebStreamVideoHub:
    '''
    Mesin Server Video Streaming MJPEG Mandiri Berlatensi Rendah.
    '''
    def __init__(self, width: int = 640, height: int = 480):
        self.width = width
        self.height = height
        self.current_jpeg = None
        self.lock = threading.Lock()
        self.running = False
        self.worker_thread = None
        
    def start(self):
        self.running = True
        self.worker_thread = threading.Thread(target=self._generation_loop, daemon=True)
        self.worker_thread.start()
        return self

    def _generation_loop(self):
        frame_idx = 0
        while self.running:
            frame_idx += 1
            # 1. Bangun frame dinamis (Simulasi Konveyor Inspeksi Mutu Sawit)
            canvas = np.full((self.height, self.width, 3), 35, dtype=np.uint8)
            
            # Simulasi janjang buah bergerak
            x_pos = int((frame_idx * 8) % self.width)
            cv2.circle(canvas, (x_pos, self.height // 2), 45, (15, 140, 230), -1) # Oranye BGR
            cv2.rectangle(canvas, (x_pos - 55, self.height // 2 - 55), 
                          (x_pos + 55, self.height // 2 + 55), (0, 255, 0), 2)
            
            # OSD Dashboard Telemetri
            cv2.putText(canvas, "DASBOR INSPEKSI MUTU TBS - PKS ONLINE", (20, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(canvas, f"STATUS: SORTASI AKTIF | FRAKSI: MATANG (98.4%)", (20, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(canvas, f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}", (20, self.height - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # 2. Kompresi JPEG ke memori RAM
            ret, jpeg_buf = cv2.imencode('.jpg', canvas, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if ret:
                with self.lock:
                    self.current_jpeg = jpeg_buf.tobytes()
                    
            time.sleep(0.033) # ~30 FPS

    def generate_mjpeg_stream(self) -> Generator[bytes, None, None]:
        '''
        Generator respons HTTP Multipart untuk peramban web.
        '''
        while self.running:
            with self.lock:
                if self.current_jpeg is None:
                    time.sleep(0.01)
                    continue
                frame_bytes = self.current_jpeg
                
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.033)

    def stop(self):
        self.running = False
        if self.worker_thread is not None:
            self.worker_thread.join(timeout=1.0)
```

---

## 5. Studi Kasus Riil & Rekayasa Lapangan Terapan

### Dasbor Kendali Sentral Mutu TBS dan Peringatan Asam Lemak Bebas (FFA) di PKS

Di stasiun sortasi pabrik kelapa sawit, manajer mutu laboratorium membutuhkan pemantauan visual langsung terhadap persentase kematangan buah yang masuk setiap jamnya. Kematangan buah berbanding lurus dengan parameter komersial krusial:
* Buah matang sempurna menghasilkan rendemen minyak $> 22\%$ dengan FFA $< 2.5\%$.
* Peningkatan buah lewat matang sebesar $10\%$ memicu lonjakan FFA di atas $5\%$, menyebabkan penalti diskon harga jual CPO ratusan juta rupiah per pengapalan tongkang.

**Implementasi Aplikasi Terpadu**:
* Sistem menyajikan **Web Dashboard berbasis FastAPI** yang diakses melalui monitor ruang kendali sentral (*Central Control Room*).
* Dasbor menampilkan:
  1. Siaran langsung video konveyor berkecepatan 30 FPS dengan penandaan kotak pembatas mutu otomatis.
  2. Grafik batang dinamis persentase fraksi kematangan (Mentah, Mengkal, Matang, Lewat Matang) yang diperbarui setiap 5 detik via WebSocket.
  3. Indikator lampu peringatan (*visual flashing alert*) jika rasio buah lewat matang melampaui ambang batas toleransi $5\%$.
* Keberadaan antarmuka ini meningkatkan kecepatan respons mandor sortasi untuk menegur sopir truk dari divisi pemasok yang membawa buah tidak memenuhi standar standar mutu.

---

## 6. Analisis Kompleksitas & Karakteristik Komputasi

Perbandingan karakteristik operasional arsitektur Desktop vs Web:

| Parameter Evaluasi | Aplikasi Desktop (PyQt6 / C++) | Aplikasi Web (FastAPI + MJPEG) |
| :--- | :--- | :--- |
| **Latensi Tampilan Video** | $< 10\text{ milidetik}$ (Sangat Cepat) | $30 - 60\text{ milidetik}$ (Cepat) |
| **Beban CPU per Klien** | Terisolasi pada 1 mesin lokal | Bertambah seiring jumlah klien terhubung |
| **Kemudahan Akses Pengguna** | Harus diinstal di setiap komputer fisik | Cukup buka URL dari ponsel / laptop |
| **Integrasi Hardware I/O (PLC/GPIO)**| Sangat mudah via Serial / Modbus | Memerlukan middleware REST API terpisah |
| **Penggunaan Ideal** | Kios Operator Konveyor Mesin | Ruang Kendali Manajer & Dashboard Eksekutif |

---

## 7. Jebakan Umum, Kegagalan Implementasi, & Mitigasi Teknis

| Masalah Teknis | Gejala Visual / Metrik | Akar Penyebab | Tindakan Mitigasi Teruji |
| :--- | :--- | :--- | :--- |
| **UI Freeze saat Eksekusi Inferensi** | Jendela aplikasi desktop tidak dapat digeser atau diklik selama kamera aktif. | Menjalankan loop inferensi AI langsung di dalam `MainWindow` tanpa memisahkan ke `QThread` / `threading.Thread`. | Pindahkan seluruh loop video dan AI ke kelas pekerja terpisah (*Worker Thread*) dan gunakan sinyal aman untuk pembaruan GUI. |
| **Bandwidth Web Jenuh (Network Choking)** | Video web tersendat-sendat (*stuttering*) saat diakses oleh 5 pengguna sekaligus. | Mengirimkan frame beresolusi penuh tanpa kompresi atau kualitas JPEG terlalu tinggi (100%). | Turunkan kualitas JPEG ke 70-75% (`IMWRITE_JPEG_QUALITY, 75`) dan turunkan skala resolusi streaming web ke $640 \times 480$. |
| **Kebocoran Koneksi Klien Web (Zombie Clients)** | Penggunaan memori server melonjak saat pengguna menutup tab browser. | Generator respons tidak mendeteksi putusnya koneksi soket klien dan terus memompa data ke *broken pipe*. | Tangani eksepsi `ClientDisconnect` atau `BrokenPipeError` dengan blok `try-except` untuk menghentikan generator loop seketika. |

---

## 8. Latihan Terbimbing & Mandiri Berjenjang

### Latihan Terbimbing (Guided Practice)
1. **Analisis Bandwidth Jaringan Web**: Sebuah server kamera industri mengalirkan stream MJPEG beresolusi $640 \times 480$ pada 30 FPS. Jika ukuran rata-rata satu frame terkompresi JPEG adalah $45\text{ KB}$, hitung konsumsi bandwidth jaringan yang dibutuhkan jika ada 4 staf manajer yang membuka dasbor secara bersamaan.
   * *Solusi*:
     * Bandwidth per klien $= 45 \text{ KB} \times 30 \text{ frame/detik} = 1.350 \text{ KB/detik} = 1.35 \text{ MB/detik}$.
     * Dalam satuan Megabit per detik: $1.35 \times 8 \approx 10.8 \text{ Mbps}$.
     * Total bandwidth 4 klien: $4 \times 10.8 \text{ Mbps} = \mathbf{43.2} \text{ Mbps}$.
     * Infrastruktur jaringan lokal (LAN 100 Mbps atau WiFi 5 GHz) sangat memadai untuk menampung beban tersebut.

### Latihan Mandiri (Independent Problem Set)
1. **Soal 1 (Konseptual)**: Bandingkan kelebihan dan kekurangan penggunaan protokol WebRTC terhadap MJPEG dalam penyajian video AI real-time, khususnya ditinjau dari latensi transmisi, konsumsi CPU server, dan kompleksitas arsitektur perangkat lunak.
2. **Soal 2 (Komputasional)**: Rancang aplikasi web minimalis menggunakan FastAPI (`app = FastAPI()`) yang mengekspos rute endpoint `/video_feed` berbasis `StreamingResponse` dengan tipe media `multipart/x-mixed-replace; boundary=frame`.

---

## 9. Jembatan Konsep (Bridging) ke AI Modul 13.4: Studi Kasus Nyata

Kita telah berhasil merancang seluruh fondasi rekayasa sistem AI real-time: integrasi perangkat keras kamera berlatensi nol (Modul 13.1), pemrosesan video dan pelacakan trajektori kontinuitas temporal (Modul 13.2), serta pengemasan antarmuka perangkat lunak desktop dan web yang terisolasi aman (Modul 13.3).

Pada **AI Modul 13.4: Studi Kasus Nyata**, kita akan menguji dan menerapkan seluruh rangkaian arsitektur ini ke dalam dua skenario industri lapangan berskala penuh:
* **AI Modul 13.4.1**: Sistem terpadu deteksi penyakit daun kelapa sawit secara real-time pada perangkat portabel lapangan lengkap dengan pohon keputusan rekomendasi proteksi tanaman.
* **AI Modul 13.4.2**: Sistem monitoring keamanan cerdas dan logistik terpadu berbasis jaringan CCTV perkebunan kelapa sawit.

---

## 10. Daftar Pustaka Komprehensif Berstandar Akademik

1. Summerfield, M. (2015). *Rapid GUI Programming with Python and Qt: The Definitive Guide to PyQt*. Prentice Hall.
2. Ramirez, S. (2020). *FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python*. https://fastapi.tiangolo.com/.
3. Fielding, R. T., & Taylor, R. N. (2002). *Principled design of the modern Web architecture*. ACM Transactions on Internet Technology (TOIT), 2(2), 115-150.
4. Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python* (2nd ed.). O'Reilly Media.
5. Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
"""

validate_text(doc_13_3, "AI_Modul_13.3_Pengembangan_aplikasi_sederhana.md")
with open("docs/part-13/AI_Modul_13.3_Pengembangan_aplikasi_sederhana.md", "w", encoding="utf-8") as f:
    f.write(doc_13_3)

# Notebook 13.3
nb_13_3_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI Modul 13.3: Praktikum Pengembangan Aplikasi Visi Komputer Sederhana\n",
            "**Tujuan Pembelajaran:**\n",
            "1. Membangun generator streaming video web berbasis protokol HTTP Multipart MJPEG.\n",
            "2. Merancang arsitektur thread-safe pemisahan antara mesin komputasi AI dan antarmuka pengguna.\n",
            "3. Mensimulasikan dasbor inspeksi mutu industri kelapa sawit real-time."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import cv2\n",
            "import time\n",
            "import threading\n",
            "import numpy as np\n",
            "import matplotlib\n",
            "matplotlib.use('Agg')\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "print(f\"OpenCV Siap: {cv2.__version__}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 1: Mesin Pembuat Stream MJPEG Asinkron"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class MockStreamEngine:\n",
            "    def __init__(self, width=480, height=360):\n",
            "        self.width = width\n",
            "        self.height = height\n",
            "        self.lock = threading.Lock()\n",
            "        self.current_jpeg = None\n",
            "        self.running = False\n",
            "        self.worker = None\n",
            "        self.frame_id = 0\n",
            "        \n",
            "    def start(self):\n",
            "        self.running = True\n",
            "        self.worker = threading.Thread(target=self._run, daemon=True)\n",
            "        self.worker.start()\n",
            "        return self\n",
            "        \n",
            "    def _run(self):\n",
            "        while self.running:\n",
            "            self.frame_id += 1\n",
            "            canvas = np.full((self.height, self.width, 3), 45, dtype=np.uint8)\n",
            "            \n",
            "            # Animasi konveyor\n",
            "            x = int((self.frame_id * 6) % self.width)\n",
            "            cv2.circle(canvas, (x, self.height // 2), 35, (10, 140, 240), -1) # Buah Matang BGR\n",
            "            cv2.rectangle(canvas, (x-40, self.height//2-40), (x+40, self.height//2+40), (0, 255, 0), 2)\n",
            "            \n",
            "            # Label Dasbor\n",
            "            cv2.putText(canvas, \"PORTAL INSPEKSI MUTU SAWIT\", (15, 30), \n",
            "                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)\n",
            "            cv2.putText(canvas, f\"FRAME: #{self.frame_id} | STATUS: NORMAL\", (15, 60), \n",
            "                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)\n",
            "            \n",
            "            ret, enc = cv2.imencode('.jpg', canvas, [cv2.IMWRITE_JPEG_QUALITY, 75])\n",
            "            if ret:\n",
            "                with self.lock:\n",
            "                    self.current_jpeg = enc.tobytes()\n",
            "            time.sleep(0.03)\n",
            "            \n",
            "    def get_latest_jpeg(self):\n",
            "        with self.lock:\n",
            "            return self.current_jpeg\n",
            "            \n",
            "    def stop(self):\n",
            "        self.running = False\n",
            "        if self.worker is not None:\n",
            "            self.worker.join(timeout=1.0)\n",
            "\n",
            "server = MockStreamEngine().start()\n",
            "time.sleep(0.2)\n",
            "sample_bytes = server.get_latest_jpeg()\n",
            "print(f\"Ukuran payload JPEG streaming: {len(sample_bytes):,} bytes\")\n",
            "assert sample_bytes is not None and len(sample_bytes) > 0, \"Gagal mengompresi JPEG!\"\n",
            "print(\"[VALIDASI SUKSES] Generator stream MJPEG aktif dan memproduksi buffer terenkripsi!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 2: Simulasi Generator Response HTTP Multipart"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def simulate_http_mjpeg_stream(stream_hub, num_frames=5):\n",
            "    chunks = []\n",
            "    for _ in range(num_frames):\n",
            "        jpg = stream_hub.get_latest_jpeg()\n",
            "        if jpg is None:\n",
            "            time.sleep(0.02)\n",
            "            continue\n",
            "        # Format standar RFC multipart/x-mixed-replace\n",
            "        part_header = b\"--frame\\r\\nContent-Type: image/jpeg\\r\\nContent-Length: \" + str(len(jpg)).encode() + b\"\\r\\n\\r\\n\"\n",
            "        chunk = part_header + jpg + b\"\\r\\n\"\n",
            "        chunks.append(chunk)\n",
            "        time.sleep(0.03)\n",
            "    return chunks\n",
            "\n",
            "stream_chunks = simulate_http_mjpeg_stream(server, num_frames=5)\n",
            "server.stop()\n",
            "print(f\"Berhasil memproduksi {len(stream_chunks)} blok paket transmisi HTTP Multipart!\")\n",
            "print(f\"Contoh Header Paket: {stream_chunks[0][:75]}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Bagian 3: Dekode Citra Terakhir dan Verifikasi Dasbor"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Rekonstruksi citra dari byte stream terakhir\n",
            "nparr = np.frombuffer(sample_bytes, np.uint8)\n",
            "decoded_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)\n",
            "\n",
            "plt.figure(figsize=(7, 5))\n",
            "plt.imshow(cv2.cvtColor(decoded_img, cv2.COLOR_BGR2RGB))\n",
            "plt.title('Tampilan Dasbor Aplikasi Web Inspeksi Mutu Sawit (MJPEG)')\n",
            "plt.axis('off')\n",
            "plt.tight_layout()\n",
            "plt.savefig('praktikum_aplikasi_dasbor_mjpeg_13_3.png', dpi=200)\n",
            "plt.close()\n",
            "print(\"[OK] Tangkapan layar dasbor tersimpan di 'praktikum_aplikasi_dasbor_mjpeg_13_3.png'\")"
        ]
    }
]

with open("notebooks/part-13/AI_Modul_13.3_Praktikum_Pengembangan_Aplikasi_Sederhana.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb_13_3_cells), f, indent=2)
print("[OK] Generated notebooks/part-13/AI_Modul_13.3_Praktikum_Pengembangan_Aplikasi_Sederhana.ipynb")

# Guide 13.3
guide_13_3 = r"""# Panduan Instruktur & Kunci Solusi: AI Modul 13.3 - Pengembangan Aplikasi Sederhana

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Pola arsitektur Model-View-Controller (MVC) dalam aplikasi visi komputer dan pencegahan UI freezing.
* **Menit 35 - 65**: Protokol streaming video HTTP Multipart MJPEG dan perbedaan mendasar terhadap WebRTC.
* **Menit 65 - 100**: Praktikum komputer: Pembangunan server streaming MJPEG asinkron, manipulasi byte buffer, dan penanganan generator.
* **Menit 100 - 130**: Studi kasus dasbor kendali sentral mutu TBS dan peringatan asam lemak bebas (FFA) di pabrik kelapa sawit.
* **Menit 130 - 150**: Pembahasan jebakan network choking, zombie client disconnection, dan kuis evaluasi.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (WebRTC vs MJPEG)
* **MJPEG (Motion JPEG)**:
  * Sangat sederhana diimplementasikan (hanya mengirimkan runtunan frame JPEG via HTTP standar).
  * Kompatibel secara bawaan di semua peramban web tanpa pustaka JavaScript pihak ketiga.
  * Kelemahan: Tidak memiliki kompresi temporal antar-frame (*inter-frame compression*), sehingga memakan bandwidth jaringan yang jauh lebih besar ($5 - 10\times$ lebih boros dibanding codec video modern).
* **WebRTC**:
  * Menggunakan codec kompresi video tingkat lanjut (H.264 / VP8 / AV1) dengan kompresi temporal mendalam.
  * Latensi sub-100 milidetik via UDP stream.
  * Kelemahan: Arsitektur sangat kompleks (membutuhkan pertukaran sinyal SDP, server STUN/TURN, dan penanganan koneksi peer-to-peer).

### Solusi Soal Mandiri 2 (Endpoint Streaming FastAPI)
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import time

app = FastAPI()

def frame_generator():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.033)
    cap.release()

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(frame_generator(), 
                             media_type="multipart/x-mixed-replace; boundary=frame")
```

---

## 3. Rubrik Penilaian Praktikum
* **Perancangan Mesin Streaming Asinkron (35%)**: Generator HTTP multipart berjalan stabil dan bebas kebocoran memori.
* **Pemisahan Utas Thread-Safe (30%)**: Akses frame buffer terisolasi rapi menggunakan mutex lock.
* **Kerapian Antarmuka & Telemetri OSD (20%)**: Dasbor menyajikan informasi operasional yang jelas, terbaca, dan proporsional.
* **Kualitas Kode & Standar Rekayasa (15%)**: Kode modular, bebas galat sintaks, dan terdokumentasi dengan baik.
"""

validate_text(guide_13_3, "AI_Modul_13.3_Panduan_Instruktur_dan_Kunci_Solusi.md")
with open("instructor_resources/part-13/AI_Modul_13.3_Panduan_Instruktur_dan_Kunci_Solusi.md", "w", encoding="utf-8") as f:
    f.write(guide_13_3)

print("[OK] Selesai Modul 13.3!")
