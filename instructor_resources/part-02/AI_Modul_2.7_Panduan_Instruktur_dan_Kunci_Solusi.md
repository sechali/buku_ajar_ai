# Panduan Instruktur & Kunci Solusi: AI Modul 2.7
## Perulangan (for, while): Arsitektur Iterasi Komputasional, Protokol Iterator, dan Pemrosesan Telemetri Perkebunan

---

**Kode Modul:** AI Modul 2.7  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Dasar Algoritma & Logika Pemrograman untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Komputasi: Otomasi Pemrosesan Telemetri Massal Perkebunan Sawit | Analisis aliran data AWS & sensor IoT, Diskusi terarah | Membedah kebutuhan iterasi: Mengapa pemrosesan sekuensial manual tidak mungkin dilakukan pada jutaan data? |
| **Menit 026 - 060** | Klasifikasi Loop (Definite vs Indefinite) & Protokol Iterator (`iter()`, `next()`) | Diagram protokol iterator, Live interaktif terminal | Membedah internal CPython: Bagaimana `for` menangkap sinyal `StopIteration` di balik layar. |
| **Menit 061 - 095** | Kontrol Alur Iterasi: Sinergi `break`, `continue`, dan Pola Unik Loop-`else` | Demonstrasi live code validasi batch sawit | Menjelaskan semantik klausa `else` yang sering disalahpahami mahasiswa sebagai kondisi negasi. |
| **Menit 096 - 125** | Algoritma Jendela Geser (*Sliding Window Moving Average*) & Bahaya Memori | Visualisasi pergeseran jendela data waktu nyata | Membandingkan kompleksitas memori sub-list slicing versus antrean berbatas `collections.deque`. |
| **Menit 126 - 150** | Refleksi Teori & Mitigasi Loop Bersarang (*Nested Loops & Big-O*) | Pembahasan soal HOTS, Review kompleksitas waktu | Melatih mahasiswa mengidentifikasi potensi bottleneck $\mathcal{O}(N \times M)$ pada algoritma spasial. |
| **Praktikum (150m)**| Eksperimen Jupyter: Protokol Iterator, Pengendali Irigasi, & Detektor Hotspot | Hands-on coding terbimbing di Jupyter Notebook | Memfasilitasi mahasiswa menyelesaikan 3 tantangan pemrograman berjenjang. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Modifikasi Struktur List Selama Proses Iterasi (*Concurrent Modification*)
* **Gejala Mahasiswa:** Menulis `for item in daftar_sensor: if item.rusak(): daftar_sensor.remove(item)` lalu heran mengapa ada sensor rusak berurutan yang lolos dari penghapusan.
* **Strategi Remedial:** Jelaskan model pointer internal CPython: ketika elemen ke-$i$ dihapus, elemen ke-$(i+1)$ bergeser ke kiri menempati indeks $i$, sementara penunjuk loop melangkah ke indeks $(i+1)$, sehingga elemen yang bergeser terlewati. Tunjukkan solusi idiomatis: *List Comprehension* `[x for x in data if not x.rusak()]`.

### Miskonsepsi 2: Mengira Klausa `else` pada Loop Bekerja Seperti `if-else`
* **Gejala Mahasiswa:** Mengira blok `else` pada `for` atau `while` hanya dieksekusi jika kondisi perulangan bernilai `False` sejak awal. Mahasiswa heran mengapa blok `else` tetap dieksekusi setelah loop `for i in range(5)` selesai berjalan normal.
* **Strategi Remedial:** Tekankan analogi semantik: "Klausa `else` pada perulangan adalah singkatan dari **'No Break'** (Selesaikan Secara Tuntas Tanpa Interupsi)." Tunjukkan bahwa blok ini adalah fitur brilian Python untuk pola pencarian (*search-and-verify*).

### Miskonsepsi 3: Terjebak dalam *Infinite Loop* karena Lupa Memutasi Variabel Sentinel pada `while`
* **Gejala Mahasiswa:** Menulis `while volume < target:` namun di dalam tubuh loop lupa menambahkan baris `volume += debit`. Program mengalami *freeze* dan terminal tidak merespon.
* **Strategi Remedial:** Ajarkan mahasiswa selalu menuliskan baris mutasi sentinel tepat setelah menulis baris `while`. Tanamkan kebiasaan menambahkan *watchdog counter* atau batasan iterasi maksimum (`if loop_count > MAX: break`) pada setiap loop bersyarat.

### Miskonsepsi 4: Mengiris Sub-List Berulang Kali pada Data Telemetri Aliran Kontinu
* **Gejala Mahasiswa:** Menggunakan `data[i:i+k]` di dalam perulangan jutaan kali untuk menghitung moving average, memicu lonjakan konsumsi memori dan perlambatan drastis akibat *garbage collection overhead*.
* **Strategi Remedial:** Kenalkan struktur data `collections.deque(maxlen=k)`. Jelaskan bahwa `deque` mengelola buffer melingkar di tingkat C (*C-level circular buffer*) dengan operasi penambahan dan pembuangan instan $\mathcal{O}(1)$ tanpa alokasi memori berulang.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Efisiensi Memori: List Slicing vs `collections.deque`
* **Soal:** Aliran kontinu $N = 10.000.000$ data dengan jendela $k = 100$. Hitung alokasi memori yang terbuang pada list slicing! Mengapa `deque(maxlen=k)` atau algoritma akumulator selisih jauh lebih unggul?
* **Jawaban Komprehensif:**
  1. **Pemborosan Alokasi Memori List Slicing:**
     Pada setiap langkah iterasi, operasi *slicing* `data[i:i+k]` mengalokasikan objek `list` baru berukuran 100 elemen di memori Heap.
     Setiap objek `list` 100 referensi di Python 64-bit mengonsumsi sekitar $856 \text{ byte}$.
     Total pemborosan memori temporer:
     $$10.000.000 \times 856 \text{ byte} \approx 8.56 \text{ Gigabyte!}$$
     Hal ini menyebabkan fragmentasi RAM ekstrem dan memicu siklus *Garbage Collector* secara masif yang melumpuhkan eksekusi waktu-nyata (*latency spikes*).
  2. **Keunggulan `deque(maxlen=k)` dan Akumulator Selisih:**
     - `collections.deque(maxlen=100)` mengalokasikan memori tetap satu kali saja ($\mathcal{O}(1)$ space), dengan operasi penambahan elemen baru sekaligus pembuangan elemen terlama dalam kompleksitas $\mathcal{O}(1)$ time.
     - Rumus pembaruan akumulator selisih:
       $$MA_{\text{baru}} = MA_{\text{lama}} + \frac{x_{\text{masuk}} - x_{\text{keluar}}}{k}$$
       Rumus ini hanya membutuhkan 2 operasi aritmetika per langkah tanpa menjumlahkan ulang seluruh 100 elemen, memangkas kompleksitas waktu dari $\mathcal{O}(k)$ menjadi murni $\mathcal{O}(1)$.

---

### Pertanyaan 2: Dekonstruksi Semantik Perilaku Klausa `else` pada Loop
* **Soal:** Mengapa pada kode `for i in range(0): if i == 5: break else: print(...)` blok else tetap dieksekusi?
* **Jawaban Komprehensif:**
  Pesan `"Blok ELSE Dieksekusi!"` **pasti akan dicetak ke konsol**.
  Alasan formal rancangan Python:
  - Iterator `range(0)` langsung menghasilkan eksepsi `StopIteration` pada panggilan pertama karena tidak memiliki elemen.
  - Perulangan berakhir secara normal (alami) tanpa pernah menyentuh kondisi `i == 5` dan tanpa memicu pernyataan `break`.
  - Karena aturan formal CPython menyatakan bahwa blok `else` dieksekusi setiap kali perulangan berakhir tanpa interupsi `break`, maka blok `else` dieksekusi secara sah. Konsep ini konsisten dengan logika matematika: *kondisi vakum (vacuous truth)* tidak pernah melanggar premis.

---

### Pertanyaan 3: Audit Risiko Iterasi Bersarang ($N \times M$) & Spatial Partitioning
* **Soal:** $N = 50.000$ pohon dan $M = 10.000$ titik sebaran hama dengan loop bersarang. Hitung total komparasi dan jelaskan solusi spatial partitioning!
* **Jawaban Komprehensif:**
  1. **Total Operasi Komparasi Brute Force:**
     $$\text{Operasi} = N \times M = 50.000 \times 10.000 = 500.000.000 \text{ operasi jarak Euclidean}$$
     Pada prosesor single-thread, kalkulasi akar kuadrat dan perpangkatan sebanyak 500 juta kali membutuhkan waktu sekitar 20–45 detik, mustahil dijalankan secara waktu-nyata di atas drone.
  2. **Solusi Spatial Partitioning (Grid Binning / KD-Tree):**
     - Area perkebunan dibagi ke dalam grid spasial (misalnya ukuran petak $100\text{ m} \times 100\text{ m}$).
     - Pohon dan hama dikelompokkan ke dalam grid menggunakan indeks *hash table* $\mathcal{O}(1)$.
     - Pencarian jarak hanya dilakukan terhadap hama yang berada di dalam petak grid yang sama atau tetangga langsung (maksimal 9 petak).
     - Hal ini memangkas pencarian dari $\mathcal{O}(N \times M)$ menjadi $\mathcal{O}(N \log M)$ atau rata-rata $\mathcal{O}(N \times c)$ di mana $c$ adalah konstanta kecil jumlah hama per petak, mereduksi waktu eksekusi menjadi kurang dari 0.2 detik.

---

## 4. Kunci Solusi Tantangan Pemrograman Berjenjang

### Solusi Tantangan 1: Agregator Curah Hujan Bulanan
```python
from typing import Any, Dict, List


def analisis_curah_hujan(data_harian: List[float]) -> Dict[str, Any]:
  """Menghitung akumulasi curah hujan bulanan, rata-rata, dan hari hujan lebat

  menggunakan perulangan 'for' dan 'enumerate'.
  """
  total_hujan = 0.0
  hari_hujan_lebat = []
  hari_dengan_hujan = 0

  for hari, curah in enumerate(data_harian, start=1):
    if curah <= 0.0:
      continue  # Hari tanpa hujan dilewati

    total_hujan += curah
    hari_dengan_hujan += 1

    if curah > 50.0:
      hari_hujan_lebat.append((hari, curah))

  rata_rata = total_hujan / len(data_harian) if data_harian else 0.0

  return {
      'total_akumulasi_mm': round(total_hujan, 2),
      'rata_rata_harian_mm': round(rata_rata, 2),
      'jumlah_hari_hujan': hari_dengan_hujan,
      'daftar_hari_hujan_lebat': hari_hujan_lebat,
  }
```

---

### Solusi Tantangan 2: Simulasi Konvergensi Infiltrasi Air (While Loop)
```python
from typing import Tuple


def simulasi_konvergensi_infiltrasi(
    debit_awal: float, batas_toleransi: float = 0.001
) -> Tuple[int, float]:
  """Menghitung konvergensi persamaan laju peresapan air tanah menuju kondisi steady-state."""
  q_saat_ini = debit_awal
  iterasi = 0
  maks_iterasi = 500

  while iterasi < maks_iterasi:
    iterasi += 1
    q_berikutnya = (0.85 * q_saat_ini) + (0.15 * 2.0)
    selisih = abs(q_berikutnya - q_saat_ini)

    if selisih < batas_toleransi:
      return iterasi, round(q_berikutnya, 4)

    q_saat_ini = q_berikutnya

  return iterasi, round(q_saat_ini, 4)
```

---

### Solusi Tantangan 3: Detektor Hotspot Kanopi Sawit dengan Deque
```python
from collections import deque
from typing import List, Optional, Tuple


class CanopyHotspotDetector:
  """Detektor titik panas kanopi sawit drone termal berbasis sliding window deque(maxlen=5)."""

  def __init__(self, ambang_kenaikan_c: float = 3.0) -> None:
    self.ambang = ambang_kenaikan_c
    self.jendela_suhu = deque(maxlen=5)
    self.daftar_hotspot: List[Tuple[int, float, float]] = []

  def proses_titik(self, t: int, suhu: float) -> Tuple[Optional[float], bool]:
    if len(self.jendela_suhu) < 5:
      self.jendela_suhu.append(suhu)
      return None, False

    ma = sum(self.jendela_suhu) / len(self.jendela_suhu)
    is_hotspot = suhu > (ma + self.ambang)
    if is_hotspot:
      self.daftar_hotspot.append((t, suhu, ma))

    self.jendela_suhu.append(suhu)  # Deque otomatis membuang elemen tertua O(1)
    return round(ma, 2), is_hotspot
```

---

## 5. Rubrik Penilaian Praktikum (Standar OBE & Akreditasi Unggul)

| Dimensi Penilaian | Bobot | Kriteria Sangat Baik (85 - 100) | Kriteria Cukup (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :---: | :--- | :--- | :--- |
| **Kebenaran Struktur Iterasi & Kontrol** | 30% | Memilih `for` dan `while` secara proporsional, menerapkan `break`, `continue`, dan klausa `else` secara presisi tanpa logika redundan. | Alur perulangan benar namun penggunaan pernyataan kontrol kurang efisien atau tidak memanfaatkan klausa `else`. | Terjadi kesalahan kontrol perulangan yang memicu *infinite loop* atau kesalahan pergeseran batas (*off-by-one*). |
| **Efisiensi Algoritma Jendela Geser** | 25% | Mengimplementasikan sliding window dengan penanganan batas array yang aman; memahami pemanfaatan `deque` untuk efisiensi memori. | Algoritma moving average menghasilkan angka benar namun menggunakan alokasi sub-list berulang tanpa batas. | Logika sliding window menghasilkan *IndexError* saat mencapai ujung larik data. |
| **Proteksi Kode & Watchdog Safety** | 20% | Menyediakan *watchdog timer* batas iterasi maksimal pada setiap `while loop` dan filter defensif untuk data korup. | Memiliki penanganan batas namun tidak menyertakan pelaporan log status interupsi kondisi ambang secara jelas. | Tidak menyertakan proteksi loop sama sekali, berisiko mengunci CPU saat data anomali masuk. |
| **Kualitas Visualisasi Grafik** | 15% | Grafik menampilkan kurva deret waktu aktual, garis putus-putus moving average, titik penanda hotspot kontras, legenda, dan label sumbu rapi. | Grafik menampilkan data dengan benar namun label sumbu atau format legenda kurang informatif. | Tidak menyertakan grafik visualisasi atau proses penyimpanan berkas gambar gagal. |
| **Standar Kerapian Kode (PEP 8)** | 10% | Kode memiliki *type hint*, docstring komprehensif, penamaan variabel deskriptif, dan mematuhi batas panjang baris. | Kode dapat berjalan namun terdapat inkonsistensi format penamaan variabel. | Kode tidak terstruktur (*unstructured code*), tanpa dokumentasi fungsional dan tanpa anotasi tipe. |
