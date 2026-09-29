# Panduan Instruktur & Kunci Solusi: AI Modul 2.8
## Fungsi dalam Pemrograman: Prinsip Modularitas, Resolusi Ruang Lingkup LEGB, dan Pipeline Uji Mutu CPO

---

**Kode Modul:** AI Modul 2.8  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Dasar Algoritma & Logika Pemrograman untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Komputasi: Dekomposisi Masalah & Analisis Laboratorium Pabrik Sawit | Bedah alur uji mutu CPO pelabuhan, Diskusi terarah | Membedah kelemahan skrip monolitik: Mengapa prosedur panjang tanpa fungsi rentan memicu galat kritis? |
| **Menit 026 - 060** | Anatomi Tanda Tangan Fungsi, Tipe Data Teranotasi, & Parameter Fleksibel | Diagram anatomi fungsi, Live interpreter Python | Menjelaskan kaidah penempatan parameter posisional, nilai baku (*default*), serta variadik (`*args`, `**kwargs`). |
| **Menit 061 - 095** | Model Memori Call Stack, Frame Activation Records, & Aturan LEGB | Visualisasi diagram konsentris LEGB, Eksperimen memori | Membuktikan bagaimana Python menyelesaikan referensi variabel dan mengisolasi variabel lokal. |
| **Menit 096 - 125** | Paradigma Pemrograman Fungsional: Fungsi Murni (*Pure*) vs Efek Samping | Uji komparasi destruktif vs non-destruktif | Mendemonstrasikan bahaya distorsi data jika fungsi memodifikasi objek koleksi masukan secara *in-place*. |
| **Menit 126 - 150** | Refleksi Teori & Desain Fungsi Tingkat Tinggi (*Higher-Order Functions*) | Pembahasan soal HOTS, Review konsep penutupan leksikal | Membimbing mahasiswa merancang generator pipeline transformasi fitur (*function composition*). |
| **Praktikum (150m)**| Eksperimen Jupyter: Closure Spektro, Pipeline CPO, & Evaluator NDVI | Hands-on coding terbimbing di Jupyter Notebook | Memfasilitasi mahasiswa menyelesaikan 3 tantangan pemrograman berjenjang. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Menempatkan Parameter Bernilai Baku (*Default Parameter*) Sebelum Parameter Wajib
* **Gejala Mahasiswa:** Menulis `def hitung_dosis(faktor=1.2, luas_hektar):` dan bingung ketika Python melempar `SyntaxError: non-default argument follows default argument`.
* **Strategi Remedial:** Jelaskan ambiguitas pemanggilan: jika pengguna memanggil `hitung_dosis(50.0)`, interpreter tidak dapat menentukan apakah `50.0` ditujukan untuk mengisi `faktor` atau `luas_hektar`. Wajibkan parameter non-default selalu ditempatkan paling depan.

### Miskonsepsi 2: Menggunakan Objek Mutabel sebagai Nilai Default Parameter
* **Gejala Mahasiswa:** Menulis `def catat_log(pesan, riwayat=[]): riwayat.append(pesan); return riwayat`, lalu heran mengapa pemanggilan kedua masih menyimpan data dari pemanggilan pertama.
* **Strategi Remedial:** Tunjukkan model siklus hidup objek di memori CPython: argumen default dievaluasi **hanya satu kali saat fungsi dikompilasi**, bukan per pemanggilan. Tanamkan pola idiomatis: `def catat_log(pesan, riwayat=None): if riwayat is None: riwayat = []`.

### Miskonsepsi 3: Memodifikasi Variabel Koleksi Masukan secara Langsung (Efek Samping Tidak Diinginkan)
* **Gejala Mahasiswa:** Mengubah elemen list argumen dengan indeks `data[i] = ...` di dalam fungsi pembantu, yang tanpa sengaja merusak dataset asli di memori pemanggil.
* **Strategi Remedial:** Bedah perbedaan antara fungsi murni (*pure function*) dan prosedur dengan efek samping (*side effects*). Wajibkan mahasiswa menghasilkan koleksi data baru (misalnya dengan *list comprehension* `[f(x) for x in data]`) daripada memutasi variabel masukan secara destruktif.

### Miskonsepsi 4: Menyalahgunakan Kata Kunci `global` untuk Berbagi Data Antar-Fungsi
* **Gejala Mahasiswa:** Mendeklarasikan `global status_mutu` di setiap fungsi agar nilainya dapat dibaca di fungsi lain, menciptakan ketergantungan tersembunyi (*hidden coupling*).
* **Strategi Remedial:** Tekankan prinsip desain modular: fungsi harus bersifat mandiri (*self-contained*). Komunikasi antar-fungsi harus terjadi secara eksplisit melalui **parameter masukan** dan **nilai kembalian (*return values*)**.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Bahaya Efek Samping pada Pemrosesan Aliran Data Sensor
* **Soal:** Mengapa fungsi normalisasi dengan `data_sensor[i] = ...` bukan fungsi murni? Apa bahayanya jika dipanggil dua kali pada variabel yang sama? Tuliskan refaktorisasinya.
* **Jawaban Komprehensif:**
  1. **Penyebab Ketidakmurnian (*Impure*):**
     Fungsi tersebut memodifikasi (*in-place mutation*) objek `list` yang dilewatkan melalui referensi memori, menimbulkan efek samping (*side effect*) pada lingkungan luar pemanggil fungsi.
  2. **Bahaya Sistemik Pemanggilan Berulang:**
     Jika data mentah awal bernilai `[60.0]`:
     - Pemanggilan ke-1: $(60.0 - 10.0) / 50.0 = 1.0$ (Normalisasi benar).
     - Pemanggilan ke-2 (misal oleh modul dasbor lain): $(1.0 - 10.0) / 50.0 = -0.18$ (Data rusak terdistorsi dua kali lipat!).
     Hal ini memicu anomali fatal pada sistem inferensi AI hilir.
  3. **Refaktorisasi Menjadi Fungsi Murni:**
     ```python
     def normalisasi_lapangan(data_sensor: List[float]) -> List[float]:
       """Fungsi murni: Menghasilkan list baru tanpa memodifikasi list masukan."""
       return [round((x - 10.0) / 50.0, 4) for x in data_sensor]
     ```

---

### Pertanyaan 2: Dekonstruksi Mekanisme Penutupan Leksikal (*Closures*)
* **Soal:** Bagaimana `buat_kalibrator_sensor` memanfaatkan *Enclosing Scope* untuk menyimpan status? Jelaskan struktur memori *Closure Object* saat fungsi luar telah selesai dieksekusi!
* **Jawaban Komprehensif:**
  1. **Pemanfaatan Enclosing Scope:**
     Fungsi dalam `kalibrasi` mereferensikan variabel `faktor_gain` yang dideklarasikan pada fungsi luar `buat_kalibrator_sensor`.
  2. **Struktur Memori Closure Object:**
     Ketika fungsi luar selesai dieksekusi dan frame-nya dikeluarkan dari Call Stack, nilai `faktor_gain` tidak dihancurkan oleh Garbage Collector. CPython membungkus variabel tersebut ke dalam objek khusus bernama **Cell Object** yang ditautkan ke atribut `__closure__` milik fungsi `kalibrasi` di memori Heap. Dengan demikian, fungsi turunan tetap mempertahankan akses ke variabel lingkungan asalnya (*lexical scoping persistence*).

---

### Pertanyaan 3: Audit Dampak Pernyataan `global` pada Komputasi Paralel
* **Soal:** Mengapa kata kunci `global` dilarang dalam arsitektur AI modern? Jelaskan fenomena *Race Condition* pada multi-threading!
* **Jawaban Komprehensif:**
  1. **Larangan Penggunaan `global`:**
     Variabel global merusak prediktabilitas fungsi, memicu keterikatan erat antar-modul (*tight coupling*), serta menghambat paralelisasi algoritma karena status variabel dapat diubah oleh fungsi apa pun kapan saja.
  2. **Fenomena Kondisi Perlombaan (*Race Condition*):**
     Ketika beberapa utas (*threads*) mengeksekusi operasi baca-modifikasi-tulis (`global_counter += 1`) secara bersamaan tanpa mekanisme penguncian (*mutex/lock*), perpindahan konteks eksekusi CPU di tengah instruksi bytecode dapat menyebabkan pembaruan nilai saling menimpa (*lost updates*). Akibatnya, hasil kalkulasi metrik telemetri satelit menjadi tidak deterministik dan berubah-ubah secara acak.

---

## 4. Kunci Solusi Tantangan Pemrograman Berjenjang

### Solusi Tantangan 1: Kalkulator Indeks Vegetasi NDVI Berbasis Fungsi Murni
```python
import math


def hitung_ndvi(nir: float, red: float) -> float:
  """Menghitung Normalized Difference Vegetation Index (NDVI) secara deterministik.

  Parameter:
      nir (float): Nilai reflektansi Near-Infrared (>= 0.0).
      red (float): Nilai reflektansi Red (>= 0.0).

  Kembalian:
      float: Indeks NDVI dalam rentang baku [-1.0, 1.0].
  """
  penyebut = nir + red
  if math.isclose(penyebut, 0.0):
    return 0.0  # Proteksi pembagian nol

  ndvi_raw = (nir - red) / penyebut
  ndvi_terjepit = max(-1.0, min(1.0, ndvi_raw))
  return round(ndvi_terjepit, 4)
```

---

### Solusi Tantangan 2: Pipeline Modular Penaksir Kebutuhan Dosis Pupuk NPK
```python
from typing import Any, Dict


def hitung_defisit_hara(kadar_tanah: float, kebutuhan_standar: float) -> float:
  """Menghitung selisih defisit unsur hara dalam kg/ha."""
  return max(0.0, kebutuhan_standar - kadar_tanah)


def hitung_kebutuhan_pupuk(
    defisit_hara: float, efisiensi_serapan: float = 0.6
) -> float:
  """Mengonversi defisit hara murni ke bobot komersial pupuk."""
  if efisiensi_serapan <= 0.0:
    raise ValueError("Efisiensi serapan harus bernilai positif.")
  return round(defisit_hara / efisiensi_serapan, 2)


def agregator_rekomendasi_pemupukan(
    id_blok: str, target_ton_ha: float, data_tanah: Dict[str, float]
) -> Dict[str, Any]:
  """Menyusun rekomendasi pupuk terpadu tanpa efek samping modifikasi."""
  skala = target_ton_ha / 25.0
  standar_n, standar_p, standar_k = 120.0 * skala, 45.0 * skala, 160.0 * skala

  def_n = hitung_defisit_hara(data_tanah.get("N", 0.0), standar_n)
  def_p = hitung_defisit_hara(data_tanah.get("P", 0.0), standar_p)
  def_k = hitung_defisit_hara(data_tanah.get("K", 0.0), standar_k)

  return {
      "id_blok": id_blok,
      "target_produksi_ton_ha": target_ton_ha,
      "rekomendasi_urea_kg_ha": hitung_kebutuhan_pupuk(
          def_n, efisiensi_serapan=0.55
      ),
      "rekomendasi_sp36_kg_ha": hitung_kebutuhan_pupuk(
          def_p, efisiensi_serapan=0.45
      ),
      "rekomendasi_mop_kg_ha": hitung_kebutuhan_pupuk(
          def_k, efisiensi_serapan=0.65
      ),
  }
```

---

### Solusi Tantangan 3: Sistem Pipa Transformasi Fitur Berbasis Higher-Order Functions
```python
from typing import Callable, List


def buat_pipeline_transformasi(
    *tahapan_fungsi: Callable[[float], float],
) -> Callable[[List[float]], List[float]]:
  """Higher-order function yang merangkai komposisi fungsi secara deterministik."""

  def eksekusi_pipeline(kumpulan_data: List[float]) -> List[float]:
    hasil = []
    for x in kumpulan_data:
      val = x
      for fn in tahapan_fungsi:
        val = fn(val)
      hasil.append(round(val, 4))
    return hasil

  return eksekusi_pipeline
```

---

## 5. Rubrik Penilaian Praktikum (Standar OBE & Akreditasi Unggul)

| Dimensi Penilaian | Bobot | Kriteria Sangat Baik (85 - 100) | Kriteria Cukup (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :---: | :--- | :--- | :--- |
| **Dekomposisi Fungsional & Desain Murni** | 30% | Memisahkan tanggung jawab fungsi secara atomik, 100% bebas efek samping (*pure functions*), dan mematuhi prinsip DRY. | Fungsi modular namun masih memodifikasi objek argumen masukan secara langsung pada beberapa baris. | Kode monolitik, mencampuradukkan input, proses, dan output tanpa dekomposisi fungsi. |
| **Pengelolaan Ruang Lingkup LEGB & Closure** | 25% | Menguasai resolusi variabel LEGB tanpa variabel global; implementasi factory function dan closure berjalan tepat. | Memahami scope variabel namun masih menggunakan kata kunci `global` untuk berbagi status data. | Terjadi tabrakan penamaan variabel (*namespace collision*) atau kegagalan pemahaman *closure*. |
| **Anotasi Pengetikan & Standar PEP 484/257** | 20% | Menuliskan *type hints* lengkap untuk parameter dan nilai kembalian, disertai *docstring* berstandar ilmiah. | Menyertakan tipe data pada sebagian fungsi namun dokumentasi docstring tidak lengkap. | Tidak menyertakan *type hints* sama sekali dan tanpa dokumentasi fungsi. |
| **Kualitas Visualisasi Grafik Transformasi** | 15% | Grafik menampilkan kurva sinyal sebelum dan sesudah transformasi komparatif, legenda, dan penanda titik yang informatif. | Grafik menampilkan data dengan benar namun format teks atau tata letak sumbu kurang rapi. | Tidak menyertakan visualisasi atau grafik gagal disimpan ke direktori aset. |
| **Kerapian & Kepatuhan Standar (PEP 8)** | 10% | Penamaan fungsi deskriptif (*snake_case*), penanganan indentasi 4 spasi konsisten, dan struktur kode sangat bersih. | Kode berjalan dengan baik namun memiliki sedikit ketidakkonsistenan spasi atau penamaan parameter. | Kode tidak terstruktur (*unstructured code*), tanpa dokumentasi fungsional dan sulit dipahami. |
