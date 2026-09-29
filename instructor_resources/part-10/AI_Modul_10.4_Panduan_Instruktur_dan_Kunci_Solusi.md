# AI Modul 10.4: Panduan Instruktur dan Kunci Solusi Komputasi
## Preprocessing Citra (Image Preprocessing)

**Mata Kuliah:** Visi Komputer dan Kecerdasan Buatan Terapan  
**Kode Mata Kuliah / SKS:** AI-10-04 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Sarjana Pertanian / Informatika Agro-Industri (INSTIPER Yogyakarta)  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 10.4 menjembatani tahap pembentukan citra mentah dengan tahap analisis fitur tingkat tinggi dan pemodelan kecerdasan buatan. Instruktur perlu menekankan bahwa kesalahan pra-pemrosesan data (*data preprocessing leakage* atau distorsi spasial) akan berdampak sistemik ke seluruh tahapan hilir. Kualitas inferensi model *Deep Learning* tidak dapat melampaui kualitas data yang disuapkan ke dalamnya (*garbage in, garbage out*).

Tiga pilar pedagogis utama yang wajib dikuasai mahasiswa:
1. **Dinamika Interpolasi Spasial**: Mahasiswa harus memahami perbedaan esensial antara interpolasi untuk data visual kontinu (*Bicubic* atau *Bilinear*) versus data label kategorikal (*Nearest Neighbor*). Instruktur wajib mendemonstrasikan bagaimana interpolasi linier merusak integritas masker segmentasi semantik.
2. **Koreksi Kontras Berbasis Fisika**: Menjelaskan mengapa penerapan perataan histogram langsung pada citra BGR merupakan kesalahan fatal di industri, dan mengapa pemisahan ke kanal $L^*$ pada ruang CIE $L^*a^*b^*$ sebelum penerapan CLAHE menjaga kemurnian informasi biokimiawi tanaman kelapa sawit.
3. **Standarisasi Alur Pipa Tensor**: Memastikan mahasiswa memahami alasan di balik setiap langkah pra-pemrosesan masukan model: penskalaan $[0.0, 1.0]$, standarisasi skor-$Z$ ImageNet, dan penataan dimensi memori *channel-first* $(C, H, W)$ untuk optimasi akselerasi GPU.

### 1.2 Miskonsepsi Umum Mahasiswa & Strategi Remedi
* **Miskonsepsi 1: Menggunakan interpolasi Bicubic saat mengubah resolusi citra masker segmentasi (*ground truth masks*).**
  * *Penjelasan Korektif*: Interpolasi Bicubic dan Bilinear melakukan pembobotan linier antar-piksel bertetangga. Jika kelas $0$ (tanah) bertetangga dengan kelas $2$ (pelepah sawit), interpolasi akan menghasilkan nilai pecahan seperti $0.8$ atau $1.4$. Saat disimpan kembali, tercipta kelas semu yang merusak proses pelatihan jaringan saraf. Remedinya adalah mewajibkan penggunaan `cv2.INTER_NEAREST` pada seluruh data berlabel diskret.
* **Miskonsepsi 2: Menganggap CLAHE sama dengan perataan histogram biasa yang hanya dipotong batasnya.**
  * *Penjelasan Korektif*: CLAHE membagi citra ke dalam kisi-kisi kontekstual (*tiles*), menghitung histogram lokal, memotong kelebihan frekuensi di atas *clip limit*, mendistribusikan piksel berlebih secara merata ke seluruh *bins*, dan menyatukan kembali batas antar-*tile* menggunakan interpolasi bilinear. Proses multi-tahap ini mencegah fenomena batas blok (*blocking artifacts*) dan mengisolasi amplifikasi derau.
* **Miskonsepsi 3: Melakukan standardisasi $Z$-Score pada tensor berurutan BGR dengan konstanta mean/std ImageNet.**
  * *Penjelasan Korektif*: Bobot pra-latih ImageNet dihitung berdasarkan urutan kanal RGB ($\mu_R = 0.485, \mu_G = 0.456, \mu_B = 0.406$). Jika urutan kanal masih BGR, maka saluran biru akan dinormalisasi dengan statistik merah, yang menurunkan akurasi model secara tajam. Instruktur wajib memverifikasi pemanggilan `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` sebelum langkah normalisasi.

---

## 2. Kunci Jawaban Lengkap & Pembahasan Soal Analitis HOTS

### Pembahasan Soal 1: Analisis Komputasi Interpolasi Bilinear pada Sub-Piksel Drone (C3)
**Data Diberikan:**
* Koordinat kontinu sub-piksel: $(x = 45.30, y = 82.70)$
* Nilai grid integer terdekat:
  * $f(45, 82) = 110$
  * $f(46, 82) = 140$
  * $f(45, 83) = 90$
  * $f(46, 83) = 160$

**Langkah Penyelesaian Analitis:**
1. **Kalkulasi Bobot Selisih Pecahan $\alpha$ dan $\beta$:**
   * $x_0 = \lfloor 45.30 \rfloor = 45 \implies \alpha = 45.30 - 45 = 0.30$
   * $y_0 = \lfloor 82.70 \rfloor = 82 \implies \beta = 82.70 - 82 = 0.70$

2. **Kalkulasi Intensitas Terinterpolasi Bilinear:**
   * *Tahap 1: Interpolasi horizontal pada baris $y = 82$:*
     $$f(x, 82) = (1 - 0.30)(110) + 0.30(140) = 0.70(110) + 0.30(140) = 77.0 + 42.0 = 119.0$$
   * *Tahap 2: Interpolasi horizontal pada baris $y = 83$:*
     $$f(x, 83) = (1 - 0.30)(90) + 0.30(160) = 0.70(90) + 0.30(160) = 63.0 + 48.0 = 111.0$$
   * *Tahap 3: Interpolasi vertikal antara baris 82 dan 83:*
     $$f(45.30, 82.70) = (1 - 0.70) f(x, 82) + 0.70 f(x, 83) = 0.30(119.0) + 0.70(111.0)$$
     $$f(45.30, 82.70) = 35.70 + 77.70 = 113.40$$

3. **Komparasi dengan Interpolasi Tetangga Terdekat (*Nearest Neighbor*):**
   * Pembulatan integer: $\text{round}(45.30) = 45$, $\text{round}(82.70) = 83$.
   * Nilai yang dipilih adalah piksel grid $(45, 83)$, yaitu $f(45, 83) = 90$.
   * Selisih galat absolut:
     $$\Delta_{\text{error}} = |113.40 - 90.00| = 23.40$$
   * **Analisis Rekayasa**: Galat sebesar $23.40$ unit intensitas (lebih dari $9\%$ skala 8-bit) membuktikan bahwa interpolasi tetangga terdekat menimbulkan diskontinuitas nilai yang tajam, sangat merusak kehalusan tekstur daun sawit pada perbesaran citra.

---

### Pembahasan Soal 2: Dekomposisi Matriks Transformasi Affine Koreksi Sudut Barisan Sawit (C3)
**Data Diberikan:**
* Dimensi citra: $1000 \times 1000$, pusat rotasi $(c_x = 500, c_y = 500)$
* Sudut rotasi berlawanan arah jarum jam: $\theta = +30^\circ$
* Skala: $s = 1.0$, dengan $\cos(30^\circ) = 0.8660$ dan $\sin(30^\circ) = 0.5000$.

**Langkah Penyelesaian Analitis:**
1. **Menghitung Koefisien $\alpha$ dan $\beta$:**
   * $\alpha = s \cdot \cos(30^\circ) = 1.0 \times 0.8660 = 0.8660$
   * $\beta = s \cdot \sin(30^\circ) = 1.0 \times 0.5000 = 0.5000$

2. **Menghitung Nilai Translasi Offset $b_1$ dan $b_2$:**
   * $b_1 = (1 - \alpha) c_x - \beta c_y = (1 - 0.8660)(500) - 0.5000(500) = 0.1340(500) - 250.0 = 67.0 - 250.0 = -183.0$
   * $b_2 = \beta c_x + (1 - \alpha) c_y = 0.5000(500) + (1 - 0.8660)(500) = 250.0 + 67.0 = +317.0$

3. **Matriks Transformasi Affine Lengkap $\mathbf{M}_{\text{affine}}$:**
   $$\mathbf{M}_{\text{affine}} = \begin{bmatrix} 0.8660 & 0.5000 & -183.0 \\ -0.5000 & 0.8660 & 317.0 \end{bmatrix}$$

---

### Pembahasan Soal 3: Diagnostik Algoritma CLAHE pada Citra Kanopi Berkabut (C4)
**Data Diberikan:**
* Ukuran tile: $N_t = 64$ piksel, derajat keabuan $L = 8$ bins
* Histogram awal: $h = [2, 4, 22, 18, 10, 4, 2, 2]$
* Parameter *clip limit*: $\beta_{\text{clip}} = 1.5$.

**Langkah Penyelesaian Analitis:**
1. **Kalkulasi Rata-rata ($N_{\text{avg}}$) dan Ambang Pemotongan ($N_{\text{clip}}$):**
   * $N_{\text{avg}} = \frac{N_t}{L} = \frac{64}{8} = 8.0\text{ piksel/bin}$
   * $N_{\text{clip}} = \beta_{\text{clip}} \times N_{\text{avg}} = 1.5 \times 8.0 = 12.0\text{ piksel}$

2. **Kalkulasi Total Piksel Berlebih ($N_{\text{excess}}$):**
   * Bin yang melampaui $N_{\text{clip}} = 12$:
     * Bin 2 ($h_2 = 22$): kelebihan = $22 - 12 = 10\text{ piksel}$
     * Bin 3 ($h_3 = 18$): kelebihan = $18 - 12 = 6\text{ piksel}$
     * Seluruh bin lainnya $\le 12$, kelebihan = $0$.
   * $N_{\text{excess}} = 10 + 6 = 16\text{ piksel}$.

3. **Redistribusi Merata dan Pembentukan Histogram Akhir $h_k'$:**
   * Penambahan per bin: $\frac{N_{\text{excess}}}{L} = \frac{16}{8} = 2.0\text{ piksel/bin}$
   * Nilai histogram akhir:
     * $h_0' = 2 + 2 = 4$
     * $h_1' = 4 + 2 = 6$
     * $h_2' = 12 + 2 = 14$ (dipotong ke batas 12 lalu ditambah 2)
     * $h_3' = 12 + 2 = 14$ (dipotong ke batas 12 lalu ditambah 2)
     * $h_4' = 10 + 2 = 12$
     * $h_5' = 4 + 2 = 6$
     * $h_6' = 2 + 2 = 4$
     * $h_7' = 2 + 2 = 4$
   * **Verifikasi Konservasi Massa Piksel**: $\sum h_k' = 4 + 6 + 14 + 14 + 12 + 6 + 4 + 4 = 64$ piksel.
   * **Argumentasi Saintifik**: Dengan membatasi frekuensi puncak dari 22 menjadi 14, kemiringan fungsi distribusi kumulatif (CDF) lokal menjadi terkendali. Hal ini mencegah amplifikasi derau frekuensi tinggi pada area homogen kanopi berkabut.

---

## 3. Kunci Jawaban & Implementasi Kode Solusi Praktikum

```python
import cv2
import numpy as np

def adaptive_drone_preprocessing(image_bgr, target_size=(256, 256), clip_limit=2.0):
    """
    Fungsi lengkap pra-pemrosesan citra drone perkebunan kelapa sawit:
    1. Koreksi kontras berkabut via CLAHE pada ruang CIE L*a*b*
    2. Resizing menggunakan interpolasi Bicubic
    3. Normalisasi Min-Max dan standardisasi Z-score ImageNet
    4. Pengubahan susunan memori ke (1, C, H, W) float32
    """
    # 1. Peningkatan kontras adaptif tanpa merusak krominans
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    L, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    L_enhanced = clahe.apply(L)
    bgr_enhanced = cv2.cvtColor(cv2.merge([L_enhanced, a, b]), cv2.COLOR_LAB2BGR)
    
    # 2. Resizing spasial berkualitas tinggi
    resized = cv2.resize(bgr_enhanced, target_size, interpolation=cv2.INTER_CUBIC)
    
    # 3. Konversi format kanal BGR -> RGB
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    
    # 4. Normalisasi Float32 & Z-Score ImageNet
    tensor = rgb.astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    tensor_std = (tensor - mean) / std
    
    # 5. Permutasi HWC -> CHW dan penambahan dimensi batch
    tensor_chw = np.transpose(tensor_std, (2, 0, 1))
    tensor_batch = np.expand_dims(tensor_chw, axis=0)
    
    return tensor_batch
```

---

## 4. Rubrik Penilaian Holistik & Pedoman Skoring

| Komponen Evaluasi | Bobot (%) | Indikator Kinerja Utama |
|:---|:---:|:---|
| **Ketepatan Teori Interpolasi & CLAHE** | 25% | Mampu membedakan peruntukan interpolasi Nearest vs Bicubic dan menjelaskan mekanisme redistribusi CLAHE. |
| **Kalkulasi Numerik HOTS** | 30% | Menghitung interpolasi bilinear sub-piksel, matriks affine rotasi, dan pembagian frekuensi CLAHE secara presisi. |
| **Implementasi Pipeline OpenCV/NumPy** | 35% | Mengembangkan fungsi pra-pemrosesan modular dengan konversi CIE Lab, CLAHE L*, dan permutasi tensor (C, H, W). |
| **Kerapian & Kepatuhan Format** | 10% | Menuliskan dokumentasi kode bersih, bebas dari istilah yang dilarang, dan berorientasi terapan agrokompleks. |
