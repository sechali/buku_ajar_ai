# AI Modul 10.7: Panduan Instruktur dan Kunci Solusi Komputasi
## Ekstraksi Fitur dan Morfologi Citra (Morphological Operations and Feature Extraction)

**Mata Kuliah:** Visi Komputer dan Kecerdasan Buatan Terapan  
**Kode Mata Kuliah / SKS:** AI-10-07 / 3 SKS  
**Sasaran Jenjang:** Mahasiswa Sarjana Pertanian / Informatika Agro-Industri (INSTIPER Yogyakarta)  
**Penyusun:** Tim Pengampu Laboratorium Komputasi & AI INSTIPER  

---

## 1. Panduan Pedagogis & Strategi Pengajaran Instruktur

### 1.1 Fokus Pembelajaran Konseptual & Praktis
Modul 10.7 merupakan sintesis komprehensif dari seluruh kompetensi visi komputer dasar (Part 11). Instruktur diharapkan membimbing mahasiswa mentransformasikan citra biner mentah menjadi **besaran agronomis berbobot keputusan manajemen perkebunan** (seperti sensus populasi pohon, peta titik tumbuh batang pohon, dan grading simetri tajuk).

Tiga pilar pedagogis utama:
1. **Dinamika Himpunan Morfologi**: Memastikan mahasiswa memahami secara intuitif bahwa operasi *Opening* adalah pembersih pulau-pulau kecil di luar kanopi tanpa merusak luas pohon, sedangkan *Closing* adalah penambal lubang bayangan di dalam kanopi tanpa memperluas dimensi terluar tajuk.
2. **Kesesuaian Geometri Elemen Penstruktur**: Menanamkan etika rekayasa bahwa objek biologis (daun, pohon, buah sawit) memiliki topologi melengkung. Penggunaan elemen penstruktur kotak (`MORPH_RECT`) adalah kesalahan konseptual fatal yang merusak kelengkungan alami; elemen elips (`MORPH_ELLIPSE`) harus dijadikan standar baku.
3. **Kalibrasi Dimensi Fisik (GSD)**: Mahasiswa wajib mengaitkan setiap metrik piksel dengan skala spasial nyata lapangan ($\text{cm/piksel}$ atau $\text{m/piksel}$). Visi komputer tanpa kalibrasi spasial tidak memiliki nilai terapan di industri pertanian presisi.

### 1.2 Miskonsepsi Umum Mahasiswa & Strategi Remedi
* **Miskonsepsi 1: Mengira urutan operasi Opening dan Closing dapat dipertukarkan secara bebas.**
  * *Penjelasan Korektif*: Jika sebuah citra memiliki derau bintik luar yang berdekatan dengan lubang internal, melakukan *Closing* terlebih dahulu akan merekatkan bintik derau ke tepi objek utama, sehingga operasi *Opening* berikutnya gagal membuangnya. Alur standar yang benar adalah: bersihkan derau luar via *Opening* terlebih dahulu, kemudian tambal lubang dalam via *Closing*.
* **Miskonsepsi 2: Menggunakan mode kontur `cv2.RETR_TREE` lalu menjumlahkan semua area kontur.**
  * *Penjelasan Korektif*: `RETR_TREE` mendeteksi kontur luar dan kontur lubang internal secara terpisah. Jika sebuah pohon sawit memiliki lubang bayangan di tengahnya, menjumlahkan semua kontur akan menghitung luas pohon ditambah luas lubang (bahkan menduplikasi hitungan). Remedinya adalah menggunakan `cv2.RETR_EXTERNAL` jika hanya membutuhkan jejak tapak kanopi luar.
* **Miskonsepsi 3: Mengira Rasio Kebulatan (*Circularity*) hanya berguna untuk mendeteksi bola atau lingkaran.**
  * *Penjelasan Korektif*: Circularity adalah pengukur derajat deformasi batas. Pada tajuk sawit sehat, susunan pelepah radial menghasilkan bentuk bundar simetris ($C \approx 0.85 - 0.95$). Ketika ulat api atau kumbang *Oryctes* memakan pelepah satu sisi, keliling perimeter membengkak drastis sementara luas area menyusut, menjatuhkan nilai $C < 0.50$. Circularity adalah indikator diagnostik kesehatan tegakan yang sangat peka.

---

## 2. Kunci Jawaban Lengkap & Pembahasan Soal Analitis HOTS

### Pembahasan Soal 1: Analisis Matematis Operasi Erosi dan Dilasi 1D (C3)
**Data Diberikan:**
* Array biner masukan: $A = [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]$ (panjang 10, indeks $0 - 9$).
* Elemen penstruktur: $B = [1, \mathbf{1}, 1]$ (radius 1 piksel, himpunan pergeseran $\{-1, 0, +1\}$).

**Langkah Penyelesaian Analitis:**
1. **Himpunan Indeks Piksel Aktif pada Masukan $A$:**
   $$A = \{2, 3, 4, 5, 6, 7\}$$

2. **Kalkulasi Erosi $A \ominus B$:**
   Suatu indeks $z$ bernilai $1$ jika dan hanya jika seluruh elemen $(B)_z = \{z-1, z, z+1\} \subseteq A$.
   * $z = 2$: $\{1, 2, 3\} \not\subseteq A$ karena $1 \notin A \implies 0$.
   * $z = 3$: $\{2, 3, 4\} \subseteq A \implies 1$.
   * $z = 4$: $\{3, 4, 5\} \subseteq A \implies 1$.
   * $z = 5$: $\{4, 5, 6\} \subseteq A \implies 1$.
   * $z = 6$: $\{5, 6, 7\} \subseteq A \implies 1$.
   * $z = 7$: $\{6, 7, 8\} \not\subseteq A$ karena $8 \notin A \implies 0$.
   * **Hasil Erosi**:
     $$A \ominus B = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0] \quad (\text{Indeks } \{3, 4, 5, 6\})$$
   * *Penjelasan*: Batas tepi objek terkikis tepat 1 piksel di sisi kiri (indeks 2) dan 1 piksel di sisi kanan (indeks 7).

3. **Kalkulasi Dilasi $A \oplus B$:**
   Suatu indeks $z$ bernilai $1$ jika setidaknya ada satu elemen $(\hat{B})_z \cap A \neq \emptyset$.
   Semua titik yang berada pada jarak $\le 1$ dari himpunan $A$ akan aktif:
   $$\text{Indeks aktif} = \{1, 2, 3, 4, 5, 6, 7, 8\}$$
   * **Hasil Dilasi**:
     $$A \oplus B = [0, 1, 1, 1, 1, 1, 1, 1, 1, 0] \quad (\text{Indeks } \{1, 2, 3, 4, 5, 6, 7, 8\})$$
   * *Penjelasan*: Batas tepi objek menebal tepat 1 piksel ke arah luar di sisi kiri (indeks 1) dan sisi kanan (indeks 8).

4. **Kalkulasi Gradien Morfologis $G = (A \oplus B) - (A \ominus B)$:**
   $$G = [0, 1, 1, 1, 1, 1, 1, 1, 1, 0] - [0, 0, 0, 1, 1, 1, 1, 0, 0, 0] = [0, 1, 1, 0, 0, 0, 0, 1, 1, 0]$$
   * *Penjelasan*: Gradien morfologis mengekstrak pita batas objek biner setebal 2 piksel (indeks $\{1, 2\}$ dan $\{7, 8\}$).

---

### Pembahasan Soal 2: Kalkulasi Titik Pusat Massa (Centroid) dan Luas Area Tajuk Pohon Sawit (C3)
**Data Diberikan:**
* Himpunan koordinat piksel tajuk sawit $\Omega$:
  $$\Omega = \{(10, 20), (11, 20), (12, 20), (10, 21), (11, 21), (12, 21), (11, 22)\}$$
* Ground Sampling Distance: $\text{GSD} = 4.0\text{ cm/piksel} = 0.04\text{ m/piksel}$.

**Langkah Penyelesaian Analitis:**
1. **Momen Spasial Orde Nol ($m_{00}$ / Luas Piksel):**
   $$m_{00} = \sum_{(x, y) \in \Omega} 1 = 7\text{ piksel}$$

2. **Momen Spasial Orde Pertama ($m_{10}$ dan $m_{01}$):**
   $$m_{10} = \sum x = 10 + 11 + 12 + 10 + 11 + 12 + 11 = 77$$
   $$m_{01} = \sum y = 20 + 20 + 20 + 21 + 21 + 21 + 22 = 145$$

3. **Titik Pusat Massa / Centroid $(c_x, c_y)$:**
   $$c_x = \frac{m_{10}}{m_{00}} = \frac{77}{7} = 11.00$$
   $$c_y = \frac{m_{01}}{m_{00}} = \frac{145}{7} \approx 20.71$$
   *Koordinat titik tumbuh kanopi pohon*: $(11.00, 20.71)$.

4. **Kalkulasi Crown Projection Area (CPA) Fisik Riil:**
   * Luas 1 piksel = $4.0\text{ cm} \times 4.0\text{ cm} = 16.0\text{ cm}^2 = 0.0016\text{ m}^2$.
   * $\text{CPA} = 7 \times 16.0\text{ cm}^2 = 112.00\text{ cm}^2$.
   * $\text{CPA} = 7 \times 0.0016\text{ m}^2 = 0.0112\text{ m}^2$.

---

### Pembahasan Soal 3: Diagnostik Deskriptor Kebulatan (Circularity) pada Deteksi Kerusakan Tajuk (C4)
**Data Diberikan:**
* Pohon A (Sehat Normal): $A_A = 28.27\text{ m}^2, P_A = 18.85\text{ m}$.
* Pohon B (Terserang Hama Oryctes): $A_B = 28.27\text{ m}^2, P_B = 32.50\text{ m}$.
* $\pi \approx 3.14159$.

**Langkah Penyelesaian Analitis:**
1. **Kalkulasi Rasio Kebulatan Pohon A ($C_A$):**
   $$C_A = \frac{4\pi A_A}{P_A^2} = \frac{4 \times 3.14159 \times 28.27}{(18.85)^2} = \frac{355.249}{355.3225} \approx 0.9998 \approx 1.00$$
   *(Bentuk kanopi bundar simetris sempurna, indikasi tanaman sehat tanpa gangguan pertumbuhan).*

2. **Kalkulasi Rasio Kebulatan Pohon B ($C_B$):**
   $$C_B = \frac{4\pi A_B}{P_B^2} = \frac{4 \times 3.14159 \times 28.27}{(32.50)^2} = \frac{355.249}{1056.25} \approx 0.336$$

3. **Analisis Komparatif & Argumentasi Diagnostik Industri:**
   * Nilai rasio kebulatan anjlok drastis dari $1.00$ menjadi $0.336$ (penurunan sebesar $66.4\%$).
   * **Mekanisme Saintifik**: Serangan hama pemakan pelepah (*Oryctes rhinoceros*) atau ulat api memotong sebagian pelepah daun muda, menciptakan lekukan-lekukan patahan yang sangat bergerigi. Lekukan tajam ini melipatgandakan panjang perimeter ($P$ naik dari $18.85\text{ m}$ menjadi $32.50\text{ m}$) meskipun luas tutupan tajuk biomassa masih tampak sama.
   * **Keunggulan Diagnostik**: Karena perimeter dikuadratkan pada penyebut ($P^2$), metrik Circularity bekerja sebagai penguat non-linier yang sangat sensitif terhadap asimetri tajuk. Sistem inspeksi drone otomatis dapat menetapkan ambang batas peringatan dini ($C < 0.70$) untuk mendeteksi pohon yang terserang hama berminggu-minggu sebelum tanaman mengalami defoliasi total.

---

## 3. Kunci Jawaban & Implementasi Kode Solusi Praktikum

```python
import cv2
import numpy as np

def full_canopy_morphology_and_census(raw_binary_mask, gsd_m=0.035, min_area_m2=15.0):
    """
    Pipeline lengkap pembersihan morfologi dan sensus tegakan pohon sawit:
    1. Opening (pembersihan derau gulma)
    2. Closing (penutupan lubang bayangan pelepah)
    3. Ekstraksi kontur luar dan filtering luas area
    4. Perhitungan centroid, CPA (m^2), dan klasifikasi simetri tajuk
    """
    # 1. Elemen penstruktur elips
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    
    # 2. Opening dilanjutkan Closing
    opened = cv2.morphologyEx(raw_binary_mask, cv2.MORPH_OPEN, se)
    cleaned = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, se)
    
    # 3. Deteksi kontur eksternal
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_area_px = min_area_m2 / (gsd_m ** 2)
    census_results = []
    
    for idx, cnt in enumerate(contours):
        area_px = cv2.contourArea(cnt)
        if area_px < min_area_px:
            continue
            
        perimeter_px = cv2.arcLength(cnt, closed=True)
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00']) if M['m00'] > 0 else 0
        cy = int(M['m01'] / M['m00']) if M['m00'] > 0 else 0
        
        circularity = (4.0 * np.pi * area_px) / (perimeter_px**2) if perimeter_px > 0 else 0
        
        census_results.append({
            'tree_id': len(census_results) + 1,
            'centroid': (cx, cy),
            'cpa_m2': area_px * (gsd_m ** 2),
            'circularity': circularity,
            'status': 'Simetris Sehat' if circularity >= 0.80 else 'Asimetris Rusak'
        })
        
    return cleaned, census_results
```

---

## 4. Rubrik Penilaian Holistik & Pedoman Skoring

| Komponen Evaluasi | Bobot (%) | Indikator Kinerja Utama |
|:---|:---:|:---|
| **Ketepatan Teori Morfologi & Momen Spasial** | 25% | Mampu menguraikan prinsip himpunan erosi, dilasi, sifat idempoten opening/closing, serta keterkaitan momen spasial secara mendalam. |
| **Kalkulasi Numerik & Analisis Diagnostik HOTS** | 30% | Menghitung erosi/dilasi 1D, momen centroid, konversi skala GSD, dan evaluasi rasio kebulatan kanopi secara presisi dan sistematis. |
| **Implementasi Kode OpenCV & Rekayasa Fitur** | 35% | Mengembangkan fungsi sensus pohon modular menggunakan kernel elips, filtering kontur berdasar luas, dan ekstraksi geometri lengkap. |
| **Kerapian Dokumentasi & Komentar Ilmiah** | 10% | Menyajikan laporan rapi, bebas dari istilah terlarang, dan berfokus pada pemecahan masalah nyata industri agrokompleks. |
