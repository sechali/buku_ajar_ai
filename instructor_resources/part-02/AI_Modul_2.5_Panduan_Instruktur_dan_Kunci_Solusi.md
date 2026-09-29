# Panduan Instruktur & Kunci Solusi: AI Modul 2.5
## Operator Matematika dan Logika: Aritmetika Presisi, Presedensi, Logika Boolean, dan Transformasi Fitur Sensor AI

---

**Kode Modul:** AI Modul 2.5  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Dasar Algoritma & Logika Pemrograman untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Komputasi: Teorema Euclidean dalam Distribusi Logistik Perkebunan | Analogi alur distribusi pupuk PKS, Diskusi interaktif | Menjelaskan relasi matematis pembagian riil (`/`), floor division (`//`), dan modulo (`%`). |
| **Menit 026 - 060** | Hierarki Presedensi Operator & Fenomena Bahaya Overdosis Kimia | Bedah diagram presedensi, Live kalkulasi Python | Mendemonstrasikan bahaya agronomis saat ekspresi dievaluasi tanpa tanda kurung eksplisit. |
| **Menit 061 - 095** | Logika Komparasi Berantai (*Chained Comparison*) & *Short-Circuit Evaluation* | Simulasi status telemetri greenhouse, Traceback kode | Mengajarkan optimasi efisiensi baterai IoT sensor melalui evaluasi hubung singkat (`and`/`or`). |
| **Menit 096 - 125** | Perbedaan Semantik `==` vs `is` & Akselerasi Keanggotaan Hash Table (`in`) | Visualisasi diagram memori Heap, Benchmark performa | Membedah kompleksitas waktu $\mathcal{O}(N)$ pada `list` vs $\mathcal{O}(1)$ pada `set`. |
| **Menit 126 - 150** | Refleksi Teori & Desain Transformasi Fitur AI (*Min-Max* & *Z-Score*) | Diskusi pra-pemrosesan data AI, Review HOTS | Membimbing perancangan proteksi singularitas pembagian dengan nol (*Zero-Division Guard*). |
| **Praktikum (150m)**| Eksperimen Jupyter: Benchmark Operator, Mesin Fertigasi, & Deteksi Anomali | Hands-on coding terbimbing di Jupyter Notebook | Memfasilitasi mahasiswa menyelesaikan 3 tantangan pemrograman berjenjang. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Menyamakan Floor Division (`//`) dengan Pembulatan Matematika (`round()`)
* **Gejala Mahasiswa:** Mahasiswa mengira bahwa `7 // 2` menghasilkan `4` karena mengira terjadi pembulatan ke atas (round to nearest). Mahasiswa juga kaget ketika `-7 // 2` menghasilkan `-4` (bukan `-3`).
* **Strategi Remedial:** Tunjukkan garis bilangan riil. Jelaskan bahwa *floor division* selalu membulatkan **ke arah minus tak hingga** ($\lfloor x \rfloor$), yaitu bilangan bulat terbesar yang lebih kecil atau sama dengan hasil bagi. Bandingkan dengan bahasa C/Java yang menggunakan *truncation towards zero*.

### Miskonsepsi 2: Mengabaikan Presedensi Operator pada Formulasi Gabungan Aritmetika dan Logika
* **Gejala Mahasiswa:** Menulis ekspresi `if a + b > 10 and c * d < 5:` tanpa memahami bahwa operator aritmetika (`+`, `*`) dievaluasi terlebih dahulu sebelum relasional (`>`, `<`), dan relasional mendahului logika (`and`). Kerancuan memuncak ketika melibatkan operator bitwise `&` yang memiliki presedensi lebih tinggi daripada relasional.
* **Strategi Remedial:** Wajibkan mahasiswa menerapkan prinsip PEP 8: "Jika ragu atau melibatkan lebih dari 2 jenis operator, selalu gunakan tanda kurung `()`". Tanda kurung tidak menimbulkan *overhead* performa dan meningkatkan keterbacaan kode (*readability*).

### Miskonsepsi 3: Menggunakan Operator Identitas `is` untuk Menguji Kesetaraan Nilai (`==`)
* **Gejala Mahasiswa:** Mahasiswa menulis `if status_sensor is "AKTIF":` atau `if skor_ndvi is 0.75:`. Terkadang berhasil pada string pendek atau integer kecil karena mekanisme *interning*, tetapi mendadak gagal pada angka pecahan atau string hasil gabungan dinamis.
* **Strategi Remedial:** Berikan analogi sederhana: `==` memeriksa apakah dua orang memiliki **nama yang sama**, sedangkan `is` memeriksa apakah dua orang tersebut adalah **orang fisik yang persis sama (satu jiwa/satu KTP)**. Gunakan `is` hanya untuk memeriksa konstanta singleton seperti `x is None` atau `x is True`.

### Miskonsepsi 4: Mengira Semua Kondisi dalam Pernyataan `and`/`or` Selalu Dieksekusi
* **Gejala Mahasiswa:** Menulis logika `if cek_status() and eksekusi_pompa():` dan bingung mengapa pompa air tidak pernah menyala ketika `cek_status()` menghasilkan `False`.
* **Strategi Remedial:** Demonstrasikan konsep *Short-Circuit Evaluation*: Jika operand pertama dari `and` bernilai `False`, Python tidak akan pernah mengevaluasi operand kedua karena ekspresi tersebut mustahil bernilai `True`. Demikian pula untuk `or`: jika operand pertama `True`, operand kedua langsung dilewati.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Anomali Algoritma Modulo pada Indeks Memori Melingkar (*Circular Buffer*)
* **Soal:** Kapasitas buffer $K = 8$. Indeks `idx = langkah % 8`. Jika `langkah = -3`, hitung nilai `idx` di Python! Mengapa berbeda dengan C/Java (`-3 % 8 == -3`), dan mana yang lebih aman?
* **Jawaban Komprehensif:**
  1. **Hasil Komputasi Python:**
     Di Python, definisi pembagian Euclidean menetapkan bahwa sisa $r$ selalu memiliki tanda yang sama dengan pembagi $b$ ($0 \le r < b$ untuk $b > 0$).
     $$\lfloor -3 / 8 \rfloor = \lfloor -0.375 \rfloor = -1$$
     $$r = a - b \times q = -3 - (8 \times -1) = -3 - (-8) = +5$$
     Sehingga di Python: `-3 % 8 == 5`.
  2. **Perbedaan dengan C / Java:**
     Bahasa C (standar C99 ke atas) dan Java menggunakan pembagian terpotong menuju nol (*truncated division*):
     $$q = \text{trunc}(-3 / 8) = 0$$
     $$r = -3 - (8 \times 0) = -3$$
     Sehingga di C/Java: `-3 % 8 == -3`.
  3. **Tinjauan Keamanan Memori (*Memory Safety*):**
     Implementasi Python jauh lebih aman untuk pengindeksan array buffer melingkar. Dalam struktur data siklik, melangkah mundur 3 langkah dari posisi nol secara fisik mendarat pada indeks ke-5 (indeks: 0, 7, 6, 5). Di C/Java, indeks negatif `-3` akan memicu *out-of-bounds array access* atau *Segmentation Fault* kecuali jika pemrogram menambahkan koreksi manual `(langkah % 8 + 8) % 8`.

---

### Pertanyaan 2: Audit Dampak Presedensi Operator pada Formulasi Dosis Kimia
* **Soal:** Diberikan data `pupuk_a = 50.0`, `pupuk_b = 50.0`, `faktor_kelarutan = 0.8`, `volume_air = 200.0`. Hitung `dosis_a` dan `dosis_b` serta jelaskan dampak agronomisnya!
* **Jawaban Komprehensif:**
  1. **Perhitungan Numerik:**
     - **Versi A (Tanpa Kurung):**
       ```python
       dosis_a = pupuk_a + pupuk_b * faktor_kelarutan / volume_air
       # Presedensi: Perkalian dan pembagian dievaluasi dari kiri ke kanan sebelum penjumlahan
       # Langkah 1: pupuk_b * faktor_kelarutan = 50.0 * 0.8 = 40.0
       # Langkah 2: 40.0 / volume_air = 40.0 / 200.0 = 0.2
       # Langkah 3: pupuk_a + 0.2 = 50.0 + 0.2 = 50.2 gram/liter
       ```
     - **Versi B (Dengan Tanda Kurung Eksplisit):**
       ```python
       dosis_b = (pupuk_a + pupuk_b) * faktor_kelarutan / volume_air
       # Langkah 1: (pupuk_a + pupuk_b) = 50.0 + 50.0 = 100.0
       # Langkah 2: 100.0 * 0.8 = 80.0
       # Langkah 3: 80.0 / 200.0 = 0.4 gram/liter
       ```
  2. **Dampak Agronomis:**
     Rasio kesalahan: $\frac{50.2}{0.4} = 125.5\times$ lipat overdosis.
     Batas fitotoksisitas larutan pupuk daun sawit umumnya berada di kisaran $1.0\text{--}2.0\text{ g/L}$. Konsentrasi sebesar $50.2\text{ g/L}$ menciptakan tekanan osmotik ekstrem di luar sel daun (*hipertonik*), menarik air keluar dari jaringan tanaman (*plasmolisis*), memicu nekrosis daun (*foliar scorching* / daun terbakar), dan mengakibatkan kematian bibit kelapa sawit secara massal di area pembibitan (*nursery*).

---

### Pertanyaan 3: Sintesis Desain Z-Score Waktu-Nyata (*Welford's Algorithm*)
* **Soal:** Jelaskan bagaimana operator rekursif dapat digunakan untuk menghitung rata-rata dan varians Z-score secara *online* per kedatangan data sensor baru tanpa menyimpan seluruh riwayat di RAM!
* **Jawaban Komprehensif:**
  Algoritma Welford (1962) memungkinkan pembaruan rata-rata ($\mu_k$) dan jumlah kuadrat deviasi ($M_{2,k}$) secara rekursif dalam kompleksitas ruang $\mathcal{O}(1)$:
  $$\mu_k = \mu_{k-1} + \frac{x_k - \mu_{k-1}}{k}$$
  $$M_{2,k} = M_{2,k-1} + (x_k - \mu_{k-1})(x_k - \mu_k)$$
  $$\sigma_k = \sqrt{\frac{M_{2,k}}{k}}$$
  Dengan arsitektur ini, mikrokontroler tepi perkebunan (seperti ESP32) hanya perlu menyimpan 3 variabel skalar (`count`, `mean`, `M2`), menghemat 99.9% kapasitas RAM dibandingkan menyimpan ratusan ribu titik data telemetri historis.

---

## 4. Kunci Solusi Tantangan Pemrograman Berjenjang

### Solusi Tantangan 1: Konversi Satuan Suhu dan Titik Embun
```python
def fahrenheit_ke_celsius(f_val: float) -> float:
  """Mengonversi nilai temperatur Fahrenheit ke Celsius secara presisi.

  Presedensi operator dilindungi oleh tanda kurung: (F - 32) * (5/9).
  """
  c_val = (f_val - 32.0) * (5.0 / 9.0)
  return round(c_val, 2)


# Pengujian Titik Kritis
assert fahrenheit_ke_celsius(32.0) == 0.00, 'Gagal pada titik beku'
assert fahrenheit_ke_celsius(212.0) == 100.00, 'Gagal pada titik didih'
assert fahrenheit_ke_celsius(86.0) == 30.00, 'Gagal pada suhu kerja 86 F'
```

---

### Solusi Tantangan 2: Partisi Batch Mini Pelatihan Model AI (*Mini-Batch Slicer*)
```python
from typing import Dict


def hitung_partisi_batch(total_sampel: int, batch_size: int) -> Dict[str, int]:
  """Menghitung partisi mini-batch pelatihan citra daun sawit menggunakan

  operator pembagian Euclidean murni tanpa percabangan if.
  """
  batch_penuh = total_sampel // batch_size
  sisa_sampel = total_sampel % batch_size

  # Trik aljabar Boolean-to-Integer: int(sisa_sampel > 0) menghasilkan 1 jika ada sisa
  total_iterasi = batch_penuh + int(sisa_sampel > 0)

  return {
      'total_sampel': total_sampel,
      'batch_size': batch_size,
      'batch_penuh': batch_penuh,
      'sisa_sampel_terakhir': sisa_sampel,
      'total_iterasi_per_epoch': total_iterasi,
  }
```

---

### Solusi Tantangan 3: Engine Deteksi Anomali Sensor dengan Z-Score Dinamis
```python
import math
from typing import List, Tuple


class DetectorAnomaliZScore:
  """Detektor anomali gas metana (CH4) berbasis aturan 3-sigma Z-Score

  menggunakan operator relasional dan logika.
  """

  def __init__(self, ambang_batas_z: float = 3.0) -> None:
    self.ambang_batas = float(ambang_batas_z)
    self.riwayat_sensor: List[float] = []

  def perbarui_dan_deteksi(self, nilai_baru: float) -> Tuple[float, bool]:
    self.riwayat_sensor.append(nilai_baru)
    n = len(self.riwayat_sensor)

    if n < 3:  # Perlu minimal 3 titik data agar estimasi varians bermakna
      return 0.0, False

    mu = sum(self.riwayat_sensor) / n
    var = sum((x - mu) ** 2 for x in self.riwayat_sensor) / n
    sigma = math.sqrt(var)

    if math.isclose(sigma, 0.0):
      return 0.0, False  # Perlindungan singularitas pembagian nol

    z_score = (nilai_baru - mu) / sigma
    is_anomali = (z_score > self.ambang_batas) or (z_score < -self.ambang_batas)
    return round(z_score, 2), is_anomali
```

---

## 5. Rubrik Penilaian Praktikum (Standar OBE & Akreditasi Unggul)

| Dimensi Penilaian | Bobot | Kriteria Sangat Baik (85 - 100) | Kriteria Cukup (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :---: | :--- | :--- | :--- |
| **Kebenaran Presedensi & Aritmetika** | 30% | Rumus konversi dan partisi batch 100% presisi matematis, kurung diterapkan secara benar tanpa redundansi berlebih. | Rumus menghasilkan nilai benar namun penulisan kurung tidak konsisten atau membingungkan. | Terjadi kesalahan presedensi operator aritmetika yang memicu hasil salah fatal. |
| **Penguasaan Logika & Keanggotaan** | 25% | Menggunakan `==` dan `is` secara tepat sasaran; memanfaatkan struktur `set` untuk pencarian $\mathcal{O}(1)$. | Memahami logika boolean namun masih menggunakan linear search pada list untuk dataset besar. | Menyamakan semantik `is` dengan `==` atau gagal memanfaatkan sifat *short-circuit*. |
| **Proteksi Kode (*Zero-Division Guard*)** | 20% | Menyediakan penanganan defensif terhadap $x_{\text{max}} == x_{\text{min}}$ atau $\sigma == 0$ dengan `math.isclose()`. | Menggunakan `try-except` generik tanpa proteksi nilai ambang numerik. | Kode melempar *ZeroDivisionError* saat diuji dengan data konstan. |
| **Analisis Hasil & Kualitas Grafik** | 15% | Grafik menampilkan kurva telemetri, titik anomali, garis batas $\pm 3\sigma$, legenda, serta label sumbu lengkap. | Visualisasi grafik benar namun tata letak atau label kurang informatif. | Tidak menyertakan visualisasi atau grafik gagal dirender. |
| **Struktur & Dokumentasi Kode** | 10% | Kode memiliki *type hint*, docstring jelas, penamaan variabel deskriptif (PEP 8), dan modular. | Penamaan variabel cukup baik namun tidak menyertakan *type hints*. | Kode berantakan (*spaghetti code*), tanpa dokumentasi dan tanpa komentar fungsional. |
