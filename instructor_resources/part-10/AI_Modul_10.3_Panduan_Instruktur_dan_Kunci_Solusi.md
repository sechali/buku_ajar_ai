# AI Modul 10.3: Panduan Instruktur dan Kunci Solusi Komputasi
## Piksel dan Ruang Warna (Color Spaces)

**Mata Kuliah:** Visi Komputer dan Kecerdasan Buatan Terapan  
**Kode Mata Kuliah / SKS:** AI-10-03 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Sarjana Pertanian / Informatika Agro-Industri (INSTIPER Yogyakarta)  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 10.3 berfokus pada transisi krusial dari representasi citra perangkat keras mentah (RGB/BGR) menuju **ruang warna yang memisahkan krominans (warna murni) dari luminans (intensitas cahaya)**. Dalam aplikasi agrokompleks (perkebunan kelapa sawit, monitoring drone kehutanan, sortasi mutu buah di pabrik kelapa sawit), fluktuasi pencahayaan alami akibat awan, bayangan pelepah, atau posisi sudut matahari merupakan tantangan terbesar yang sering menggagalkan algoritma visi komputer sederhana.

Tiga fokus pedagogis utama:
1. **Pemisahan Dimensi Krominans vs Luminans**: Mahasiswa harus memahami mengapa ruang warna RGB sangat rentan terhadap variasi iluminasi (karena ketiga kanal $R, G, B$ berfluktuasi serempak saat intensitas cahaya berubah), sedangkan ruang HSV dan CIE $L^*a^*b^*$ mengisolasi intensitas ke kanal tunggal ($V$ atau $L^*$).
2. **Topologi Melingkar Kanal Hue (Circular Hue Wrap-Around)**: Menanamkan pemahaman geometris bahwa sudut warna merah membentang melintasi batas diskontinuitas numerik ($0^\circ \equiv 360^\circ$, atau $[0, 14]$ dan $[168, 179]$ pada uint8 OpenCV). Mahasiswa harus terbiasa menggunakan operasi logika OR ganda (`cv2.bitwise_or`).
3. **Keseragaman Persepsi (Perceptual Uniformity) CIE $L^*a^*b^*$**: Memahami bahwa jarak Euclidean pada ruang Lab ($\Delta E_{ab}^*$) merefleksikan sensitivitas fisiologis mata manusia, menjadikannya standar industri dalam sortasi dan kendali mutu CPO serta produk pascapanen.

### 1.2 Miskonsepsi Umum Mahasiswa & Strategi Remedi
* **Miskonsepsi 1: Mengira rentang nilai Hue di OpenCV adalah $0 - 360^\circ$.**
  * *Penjelasan Korektif*: Format citra 8-bit (`uint8`) hanya mampu menampung nilai bilangan bulat $0 - 255$. Karena $360 > 255$, pengembang pustaka OpenCV membagi derajat Hue dengan $2$, sehingga rentang OpenCV menjadi $[0, 179]$. Jika mahasiswa menuliskan `upper_hue = 360`, variabel tersebut akan mengalami *overflow* atau menghasilkan perilaku tak terduga.
* **Miskonsepsi 2: Mengira segmentasi buah sawit matang (jingga-merah) cukup dengan satu pemanggilan `cv2.inRange([0, S_min, V_min], [30, 255, 255])`.**
  * *Penjelasan Korektif*: Warna merah tua matang sering kali memiliki nilai Hue di atas $340^\circ$ (atau $170 - 179$ di OpenCV). Jika hanya menggunakan batas bawah $[0, 15]$, separuh brondolan sawit yang berwarna merah pekat akan tereliminasi sebagai latar belakang gelap. Remedinya adalah mendemonstrasikan penggabungan dua mask biner dengan `cv2.bitwise_or()`.
* **Miskonsepsi 3: Menghitung $\Delta E_{ab}^*$ langsung dari array `cv2.cvtColor(img, cv2.COLOR_BGR2LAB)` tanpa penyesuaian offset.**
  * *Penjelasan Korektif*: OpenCV menggeser dan menskalakan nilai $L^* \in [0, 255]$ ($L \times 255/100$), $a^* \in [0, 255]$ ($a + 128$), dan $b^* \in [0, 255]$ ($b + 128$) agar muat di dalam `uint8`. Jika jarak Euclidean dihitung langsung, pembobotan dimensi $L^*$ menjadi tidak proporsional. Mahasiswa wajib mengonversi kembali ke koordinat asli CIE sebelum menghitung $\Delta E$.

---

## 2. Kunci Jawaban Lengkap & Pembahasan Soal Analitis HOTS

### Pembahasan Soal 1: Analisis Konversi Grayscale Fisiologis vs Aritmatika Sederhana (C3)
**Data Diberikan:**
* Piksel daun klorosis: $I_{\text{klorosis}} = [R=210, G=200, B=30]$
* Piksel daun sehat: $I_{\text{sehat}} = [R=50, G=180, B=40]$

**Langkah Penyelesaian Analitis:**
1. **Rata-rata Aritmatika Sederhana ($Y_{\text{rata}} = \frac{R + G + B}{3}$):**
   * $Y_{\text{rata, klorosis}} = \frac{210 + 200 + 30}{3} = \frac{440}{3} \approx 146.67$
   * $Y_{\text{rata, sehat}} = \frac{50 + 180 + 40}{3} = \frac{270}{3} = 90.00$
   * Selisih kontras aritmatika:
     $$\Delta Y_{\text{rata}} = |146.67 - 90.00| = 56.67$$

2. **Formula Fisiologis Berbobot ITU-R BT.601 ($Y_{\text{fisiologis}} = 0.299R + 0.587G + 0.114B$):**
   * $Y_{\text{fisiologis, klorosis}} = 0.299(210) + 0.587(200) + 0.114(30) = 62.79 + 117.40 + 3.42 = 183.61$
   * $Y_{\text{fisiologis, sehat}} = 0.299(50) + 0.587(180) + 0.114(40) = 14.95 + 105.66 + 4.56 = 125.17$
   * Selisih kontras fisiologis:
     $$\Delta Y_{\text{fisiologis}} = |183.61 - 125.17| = 58.44$$

3. **Interpretasi & Keunggulan Saintifik:**
   Formula fisiologis menghasilkan selisih kecerahan yang lebih tegas ($\Delta Y = 58.44$) dan merefleksikan persepsi fotopik manusia secara akurat. Karena mata manusia paling sensitif terhadap spektrum hijau (pembobot $0.587$), kontribusi pigmen klorofil pada daun sehat ($G=180$) memberikan nilai luminans yang proporsional, sementara hilangnya klorofil yang digantikan oleh pigmen karotenoid/xantofil pada daun klorosis ($R=210, G=200$) menghasilkan lonjakan luminans yang sangat signifikan. Penggunaan formula fisiologis mencegah distorsi kontras dan memudahkan algoritma deteksi tepi mengenali lesi daun sakit.

---

### Pembahasan Soal 2: Dekomposisi Analitik Ruang Warna HSV Buah Kelapa Sawit (C3)
**Data Diberikan:**
* Nilai piksel ternormalisasi: $R = 0.80$, $G = 0.30$, $B = 0.10$.

**Langkah Penyelesaian Analitis:**
1. **Perhitungan $M$, $m$, dan $\Delta$:**
   * Nilai maksimum ($M$): $M = \max(0.80, 0.30, 0.10) = 0.80$
   * Nilai minimum ($m$): $m = \min(0.80, 0.30, 0.10) = 0.10$
   * Rentang dinamis ($\Delta$): $\Delta = M - m = 0.80 - 0.10 = 0.70$

2. **Perhitungan Metrik $V$ (Value) dan $S$ (Saturation):**
   * $V = M = 0.80$ (atau $80\%$)
   * $S = \frac{\Delta}{M} = \frac{0.70}{0.80} = 0.875$ (atau $87.5\%$)

3. **Perhitungan Sudut Hue ($H$):**
   Karena $M = R$, formula sudut Hue adalah:
   $$H = 60^\circ \times \left(\frac{G - B}{\Delta} \pmod 6\right)$$
   $$\frac{G - B}{\Delta} = \frac{0.30 - 0.10}{0.70} = \frac{0.20}{0.70} \approx 0.2857$$
   $$H = 60^\circ \times 0.2857 \approx 17.14^\circ$$
   *(Sudut $17.14^\circ$ berada tepat pada sektor spektral jingga-kemerahan khas brondolan sawit matang).*

4. **Konversi ke Skala $8\text{-bit}$ Standar OpenCV:**
   * $H_{\text{OpenCV}} = \text{round}\left(\frac{H}{2}\right) = \text{round}\left(\frac{17.14}{2}\right) = \text{round}(8.57) = 9$
   * $S_{\text{OpenCV}} = \text{round}(S \times 255) = \text{round}(0.875 \times 255) = \text{round}(223.125) = 223$
   * $V_{\text{OpenCV}} = \text{round}(V \times 255) = \text{round}(0.80 \times 255) = \text{round}(204.0) = 204$
   * **Vektor HSV OpenCV**: $[H=9, S=223, V=204]$.

---

### Pembahasan Soal 3: Diagnostik Perbedaan Persepsi Warna CPO via Metrik CIE Delta-E (C4)
**Data Diberikan:**
* Sampel 1 (Standar Ekspor Prima): $L_1^* = 65.0, a_1^* = 35.0, b_1^* = 55.0$
* Sampel 2 (CPO Terdegradasi): $L_2^* = 58.0, a_2^* = 42.0, b_2^* = 46.0$

**Langkah Penyelesaian Analitis:**
1. **Kalkulasi Selisih Komponen Warna:**
   * $\Delta L^* = L_2^* - L_1^* = 58.0 - 65.0 = -7.0$ (Minyak menjadi lebih gelap)
   * $\Delta a^* = a_2^* - a_1^* = 42.0 - 35.0 = +7.0$ (Minyak bergeser ke arah merah pekat)
   * $\Delta b^* = b_2^* - b_1^* = 46.0 - 55.0 = -9.0$ (Minyak kehilangan kejernihan kuning)

2. **Kalkulasi Jarak Warna Euclidean $\Delta E_{ab}^*$:**
   $$\Delta E_{ab}^* = \sqrt{(\Delta L^*)^2 + (\Delta a^*)^2 + (\Delta b^*)^2}$$
   $$\Delta E_{ab}^* = \sqrt{(-7.0)^2 + (7.0)^2 + (-9.0)^2} = \sqrt{49.0 + 49.0 + 81.0} = \sqrt{179.0} \approx 13.38$$

3. **Analisis Kriteria Persepsi Industri & Argumentasi Saintifik:**
   * Standar internasional persepsi warna CIE menetapkan kriteria:
     * $\Delta E < 1.0$: Perbedaan tidak terdeteksi oleh mata manusia (*imperceptible*).
     * $1.0 \le \Delta E \le 2.0$: Hanya terdeteksi oleh pengamat berpengalaman.
     * $2.0 < \Delta E \le 10.0$: Perbedaan terlihat jelas pada pengamatan sekilas.
     * $\Delta E > 10.0$: **Perbedaan warna sangat mencolok (*very obvious difference*)**.
   * **Kesimpulan Industri**: Karena nilai $\Delta E_{ab}^* = 13.38 \gg 10.0$, perbedaan mutu antara kedua sampel CPO tersebut **pasti dapat dibedakan secara kasat mata** oleh inspektur mutu pabrik tanpa memerlukan instrumen spektrofotometer. Sampel 2 tampak jauh lebih kusam/gelap dan kemerahan keruh akibat degradasi termal atau oksidasi asam lemak bebas (FFA).

---

## 3. Kunci Jawaban & Implementasi Kode Solusi Praktikum

### Solusi Latihan 1: Segmentasi Klorosis Daun Sawit pada Pembibitan
```python
import cv2
import numpy as np

def segment_foliar_chlorosis(image_bgr):
    """
    Memisahkan area daun sehat (hijau segar) dari area klorosis (kuning pucat)
    menggunakan segmentasi ruang warna HSV.
    """
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    # 1. Rentang Daun Sehat (Hijau subur)
    # Hue: 35 - 85 (Hijau muda hingga hijau tua)
    lower_healthy = np.array([35, 50, 40], dtype=np.uint8)
    upper_healthy = np.array([85, 255, 255], dtype=np.uint8)
    mask_healthy = cv2.inRange(hsv, lower_healthy, upper_healthy)
    
    # 2. Rentang Daun Klorosis (Kuning defisiensi N)
    # Hue: 18 - 34 (Kuning lemon hingga jingga-kuning)
    lower_chlorosis = np.array([18, 60, 70], dtype=np.uint8)
    upper_chlorosis = np.array([34, 255, 255], dtype=np.uint8)
    mask_chlorosis = cv2.inRange(hsv, lower_chlorosis, upper_chlorosis)
    
    # Kalkulasi rasio keparahan klorosis
    total_canopy = np.sum(mask_healthy > 0) + np.sum(mask_chlorosis > 0)
    if total_canopy == 0:
        return 0.0, mask_healthy, mask_chlorosis
        
    severity_ratio = (np.sum(mask_chlorosis > 0) / total_canopy) * 100.0
    return severity_ratio, mask_healthy, mask_chlorosis
```

---

## 4. Rubrik Penilaian Holistik & Pedoman Skoring

| Komponen Evaluasi | Bobot (%) | Indikator Kinerja Utama |
|:---|:---:|:---|
| **Ketepatan Konseptual Ruang Warna** | 25% | Mampu menguraikan alasan kegagalan RGB di bawah bayangan dan keuntungan HSV/Lab dalam memisahkan krominans-luminans. |
| **Kalkulasi Matematis HOTS** | 30% | Menghitung konversi Grayscale fisiologis, dekomposisi analitis HSV, dan $\Delta E_{ab}^*$ secara presisi dengan satuan dan rumus yang benar. |
| **Implementasi Kode OpenCV** | 35% | Mengembangkan skrip segmentasi dual-range HSV untuk red hue wrap-around dan transformasi koordinat CIE Lab tanpa galat indeks. |
| **Etika Kode & Dokumentasi** | 10% | Menyusun kode bersih, modular, dilengkapi komentar penjelas berorientasi rekayasa agrokompleks. |
