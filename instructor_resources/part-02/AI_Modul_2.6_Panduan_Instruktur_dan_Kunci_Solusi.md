# Panduan Instruktur & Kunci Solusi: AI Modul 2.6
## Percabangan (if-else): Arsitektur Kontrol Alur Eksekusi, Guard Clauses, dan Pipeline Sortasi Mutu TBS Sawit

---

**Kode Modul:** AI Modul 2.6  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Dasar Algoritma & Logika Pemrograman untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Komputasi: Alur Sortasi Loading Ramp Pabrik Kelapa Sawit (PKS) | Bedah foto proses grading TBS di PKS, Diskusi terarah | Membedah kriteria penalti dan diskon harga TBS berdasarkan fraksi kematangan buah. |
| **Menit 026 - 060** | Teorema Bohm-Jacopini, Pohon Keputusan (*Decision Tree*), dan Sintaksis `if-elif-else` | Diagram pohon keputusan, Live interpreter Python | Menjelaskan bagaimana percabangan mempartisi ruang fitur masukan secara ortogonal. |
| **Menit 061 - 095** | Patologi Kode Bersarang (*Deeply Nested Conditionals*) & Refaktorisasi *Guard Clauses* | Refaktorisasi berdampingan (*side-by-side refactoring*) | Menunjukkan reduksi kompleksitas kognitif saat menggunakan pola *Guard Clauses / Early Return*. |
| **Menit 096 - 125** | Perancangan Sistem Klasifikasi Mutu TBS Skala Industri | Bedah kode dataclass, enum, dan metode kelas | Menekankan prinsip *type safety* menggunakan `enum.Enum` dan `dataclass(frozen=True)`. |
| **Menit 126 - 150** | Refleksi Teori & Pengantar Tantangan Praktikum Laboratorium | Diskusi HOTS, Review optimasi urutan cabang | Membimbing mahasiswa menganalisis kompleksitas siklomatis (*McCabe Cyclomatic Complexity*). |
| **Praktikum (150m)**| Eksperimen Jupyter: Validasi Lori, Engine Sortasi TBS, & Triage Multi-Sensor | Hands-on coding terbimbing di Jupyter Notebook | Memfasilitasi mahasiswa menyelesaikan 3 tantangan pemrograman berjenjang. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Mengira `if-elif-else` Mengevaluasi Seluruh Cabang Sekaligus
* **Gejala Mahasiswa:** Menulis urutan kondisi yang tumpang tindih (*overlapping*) seperti `if x > 10: ... elif x > 20: ...` dan heran mengapa input `x = 25` masuk ke blok pertama alih-alih blok kedua.
* **Strategi Remedial:** Jelaskan sifat evaluasi sekuensial *top-down*. Interpreter Python berhenti segera setelah menemukan kondisi pertama yang bernilai `True`. Tunjukkan bahwa urutan cabang harus disusun dari yang paling spesifik/ketat ke yang paling umum, atau menggunakan *guard clauses*.

### Miskonsepsi 2: Menggunakan Serangkaian `if` Mandiri padahal Seharusnya Menggunakan `elif`
* **Gejala Mahasiswa:** Menulis:
  ```python
  if brondol < 12:
    status = "MENTAH"
  if brondol <= 75:
    status = "MATANG"
  if brondol > 75:
    status = "LEWAT MATANG"
  ```
  Ketika `brondol = 8`, variabel `status` awalnya diisi `"MENTAH"`, namun segera tertimpa oleh `"MATANG"` karena `8 <= 75` juga bernilai `True`.
* **Strategi Remedial:** Tekankan perbedaan antara kondisi yang bersifat *mutually exclusive* (pilihan alternatif tunggal dengan `if-elif-else`) dan kondisi independen (beberapa `if` terpisah untuk aksi yang dapat terjadi bersamaan).

### Miskonsepsi 3: Terjebak dalam Struktur Percabangan Bersarang Berlebih (*Deeply Nested Conditionals*)
* **Gejala Mahasiswa:** Menulis kode validasi formulir atau sensor dengan lekukan indentasi 5 hingga 8 tingkat ke kanan. Kode menjadi sulit dibaca, sulit di-*debug*, dan rawan salah blok indentasi.
* **Strategi Remedial:** Ajarkan paradigma *Guard Clauses Pattern*: "Validasi kondisi prasyarat atau anomali di awal fungsi. Jika kondisi batas dilanggar, selesaikan eksekusi seketika (*early return* atau melempar eksepsi). Biarkan alur eksekusi baku berjalan lurus pada tingkat indentasi dasar."

### Miskonsepsi 4: Kebingungan Evaluasi Truthy/Falsy (`if x:` vs `if x is not None:`)
* **Gejala Mahasiswa:** Menulis `if berat:` untuk memeriksa apakah data berat telah diisi. Ketika sensor membaca angka `0.0` kg (misalnya timbangan kosong), Python menganggap `0.0` sebagai `False`, sehingga program keliru menganggap data belum diisi (*missing*).
* **Strategi Remedial:** Tunjukkan tabel nilai Falsy di Python (`None`, `0`, `0.0`, `""`, `[]`). Wajibkan mahasiswa memeriksa `if berat is not None:` saat mengolah data numerik yang secara sah dapat bernilai nol.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Kompleksitas Siklomatis (*Cyclomatic Complexity*)
* **Soal:** Hitung kompleksitas siklomatis fungsi `evaluasi_mutu` pada `EngineSortasiTBS`! Mengapa klausa penjaga (*guard clauses*) lebih unggul dalam pengujian unit dibandingkan struktur percabangan bertingkat bersarang?
* **Jawaban Komprehensif:**
  1. **Perhitungan Kompleksitas Siklomatis (McCabe):**
     Rumus: $M = \pi + 1$, di mana $\pi$ adalah jumlah titik keputusan predikat biner.
     Titik keputusan pada `evaluasi_mutu`:
     - Predikat 1: `tbs.berat_kg < cls.BERAT_MINIMUM_KG`
     - Predikat 2: `tbs.persen_brondol_lepas < cls.BRONDOL_MIN_MATANG`
     - Predikat 3: `tbs.persen_brondol_lepas > cls.BRONDOL_MAX_MATANG`
     - Predikat 4: `tbs.panjang_tangkai_cm > cls.PANJANG_TANGKAI_MAKS_CM`
     - Predikat 5: `tbs.kadar_kotoran_persen > cls.KADAR_KOTORAN_MAKS_PERSEN`
     Jumlah predikat $\pi = 5$.
     Maka: $M = 5 + 1 = 6$ jalur eksekusi independen.
  2. **Keunggulan Pengujian Unit (*Unit Testing*):**
     Pada struktur *guard clauses*, setiap cabang kegagalan bersifat independen dan linier. Pengembang cukup menulis 1 kasus uji per klausa penjaga (total 5 pengujian kegagalan + 1 pengujian jalur utama sukses). Sebaliknya, pada struktur bersarang (*nested conditionals*), pengujian jalur terdalam membutuhkan kombinasi status seluruh kondisi terluar secara simultan, sehingga matriks uji kombinatorial membengkak secara eksponensial.

---

### Pertanyaan 2: Audit Urutan Evaluasi Cabang (*Branch Order Optimization*)
* **Soal:** Jika statistik kegagalan TBS adalah: Mentah (65%), Tangkai Panjang (20%), Underweight (10%), Kotoran (5%). Bagaimana menyusun ulang urutan *guard clauses* agar rata-rata waktu eksekusi CPU per tandan paling minimum?
* **Jawaban Komprehensif:**
  Prinsip optimasi cabang CPU (*Branch Probability Optimization*) menyatakan bahwa kondisi dengan probabilitas terpenuhi tertinggi harus dievaluasi terlebih dahulu untuk memaksimalkan *early exit* dan meminimalkan jumlah instruksi yang dieksekusi.
  Urutan optimal baru:
  1. **Guard 1 (Probabilitas 65%):** Uji Kematangan Mentah (`persen_brondol_lepas < BRONDOL_MIN_MATANG`). Mengeliminasi 65% beban komputasi langsung pada langkah pertama.
  2. **Guard 2 (Probabilitas 20%):** Uji Panjang Tangkai (`panjang_tangkai_cm > PANJANG_TANGKAI_MAKS_CM`).
  3. **Guard 3 (Probabilitas 10%):** Uji Bobot Underweight (`berat_kg < BERAT_MINIMUM_KG`).
  4. **Guard 4 (Probabilitas 5%):** Uji Kadar Kotoran (`kadar_kotoran_persen > KADAR_KOTORAN_MAKS_PERSEN`).
  Dengan arsitektur teroptimasi ini, rata-rata jumlah komparasi per tandan berkurang drastis dari 3.1 komparasi menjadi hanya 1.6 komparasi per tandan.

---

### Pertanyaan 3: Pola *Match-Case* (Python 3.10+) versus *If-Elif-Else*
* **Soal:** Kapan seorang insinyur AI harus memilih rantai `if-elif-else` dibandingkan `match-case`?
* **Jawaban Komprehensif:**
  - **Pilih `if-elif-else`:** Ketika logika keputusan didasarkan pada **rentang numerik kontinu** (misalnya: $1.5 \le P \le 3.0$ atau $\text{Hue} \in [60, 110]$), perbandingan relasional majemuk dengan operator logika (`and`, `or`), atau komparasi objek dinamis.
  - **Pilih `match-case`:** Ketika keputusan didasarkan pada **pencocokan struktur bentuk data** (*structural pattern matching*), dekonstruksi struktur tuple/dictionary/objek, atau pencocokan nilai literal diskret/enum (misalnya membaca paket data JSON telemetri IoT dengan berbagai jenis tipe pesan: `{"tipe": "HEARTBEAT"}`, `{"tipe": "ALERT", "kode": int}`).

---

## 4. Kunci Solusi Tantangan Pemrograman Berjenjang

### Solusi Tantangan 1: Evaluasi Tekanan Uap Sterilizer
```python
def evaluasi_tekanan_sterilizer(tekanan_bar: float) -> str:
  """Mengklasifikasikan status operasional bejana uap perebusan sawit."""
  # Guard: Sensor anomali bernilai negatif
  if tekanan_bar < 0.0:
    return "ERROR: ANOMALI SENSOR (TEKANAN NEGATIF)"

  if tekanan_bar < 1.5:
    return "TEKANAN RENDAH (REBUSAN TIDAK MATANG)"
  elif 1.5 <= tekanan_bar <= 3.0:
    return "TEKANAN OPTIMAL (STERILISASI NORMAL)"
  else:
    return "BAHAYA: OVERPRESSURE (BUKA KATUP DARURAT)"
```

---

### Solusi Tantangan 2: Evaluasi Kematangan Buah Berbasis Warna HSV
```python
def deteksi_kematangan_hsv(hue: float, sat: float) -> str:
  """Mengevaluasi tingkat kematangan buah sawit dari sinyal kamera visi komputer HSV."""
  # Guard 1: Validasi batas rentang fisik ruang warna
  if not (0.0 <= hue <= 360.0 and 0.0 <= sat <= 100.0):
    return "ERROR: PARAMETER HSV DI LUAR JANGKAUAN"

  # Guard 2: Kategori Hijau / Mentah
  if 60.0 <= hue <= 110.0 and sat >= 40.0:
    return "HIJAU / MENTAH (FRAKSI 0/1)"

  # Guard 3: Kategori Oranye / Matang Sempurna
  if 25.0 <= hue <= 59.0 and sat >= 50.0:
    return "ORANYE / MATANG SEMPURNA (FRAKSI 2)"

  # Guard 4: Kategori Merah Tua / Lewat Matang
  if (0.0 <= hue <= 24.0 or hue >= 340.0) and sat >= 40.0:
    return "MERAH TUA / LEWAT MATANG (FRAKSI 3)"

  # Fallback: Anomali spektrum warna
  return "ANOMALI WARNA / PERLU INSPEKSI ULANG"
```

---

### Solusi Tantangan 3: Industrial Emergency Triage Engine
```python
from typing import List


class IndustrialEmergencyTriage:
  """Engine triage darurat stasiun perebusan & turbin PKS multi-sensor."""

  def __init__(self) -> None:
    self.log_insiden: List[str] = []

  def evaluasi_kondisi(
      self, tekanan_bar: float, suhu_c: float, getaran_v_mms: float
  ) -> str:
    # Guard 1: KODE MERAH (Kegagalan Kritis - Shutdown Seketika)
    if tekanan_bar > 3.2 or getaran_v_mms > 7.5:
      pesan = (
          f"KODE MERAH: EMERGENCY SHUTDOWN! (P={tekanan_bar} Bar, V={getaran_v_mms}"
          " mm/s)"
      )
      self.log_insiden.append(pesan)
      return "KODE MERAH"

    # Guard 2: KODE KUNING (Peringatan & Throttling)
    if (tekanan_bar > 2.8) or (getaran_v_mms > 4.5) or (suhu_c > 98.0):
      pesan = (
          f"KODE KUNING: THROTTLING OPERASI (P={tekanan_bar} Bar, T={suhu_c} C,"
          f" V={getaran_v_mms} mm/s)"
      )
      self.log_insiden.append(pesan)
      return "KODE KUNING"

    # Alur Eksekusi Baku: Operasi Pabrik Aman
    return "KODE HIJAU"
```

---

## 5. Rubrik Penilaian Praktikum (Standar OBE & Akreditasi Unggul)

| Dimensi Penilaian | Bobot | Kriteria Sangat Baik (85 - 100) | Kriteria Cukup (70 - 84) | Kriteria Kurang (< 70) |
| :--- | :---: | :--- | :--- | :--- |
| **Penerapan Guard Clauses & Alur Bersih** | 30% | Mengeliminasi percabangan bersarang berlebih secara menyeluruh, mengimplementasikan *early return*, dan alur eksekusi baku berada pada tingkat terluar. | Menggunakan klausa penjaga pada sebagian fungsi namun masih menyisakan percabangan bersarang. | Menggunakan percabangan bersarang dalam (> 3 tingkat lekukan) tanpa pertimbangan arsitektur yang sah. |
| **Kebenaran Logika Kondisi Batas** | 25% | Logika perbandingan berantai dan batas inklusif/eksklusif 100% presisi matematis, aman dari anomali sensor negatif. | Hasil benar pada kasus normal namun gagal pada kasus batas (*boundary conditions*). | Kondisi logika tumpang tindih (*overlapping*) sehingga cabang tertentu tidak pernah dapat dijangkau (*dead code*). |
| **Desain Modular & Tipe Data Terstruktur** | 20% | Menggunakan `Enum` untuk kelas kategori, `dataclass` untuk data telemetri, dan anotasi tipe (*Type Hinting*) PEP 484. | Menggunakan tipe data standar (dictionary/tuple) tanpa `Enum` namun kode tetap modular. | Menggunakan variabel global tersebar tanpa enkapsulasi fungsi atau kelas. |
| **Kualitas Visualisasi Grafik** | 15% | Diagram batang distribusi sortasi menyertakan label kategori lengkap, nilai frekuensi di atas batang, dan pewarnaan tematik. | Grafik menampilkan data dengan benar namun label sumbu atau format teks kurang rapi. | Grafik tidak memiliki judul/label atau gagal disimpan ke format gambar. |
| **Standar Kerapian Kode (PEP 8)** | 10% | Penamaan *snake_case*, indentasi 4 spasi konsisten, docstring komprehensif, dan komentar fungsional bermakna. | Kode berjalan baik namun memiliki sedikit inkonsistensi spasi atau penamaan variabel tidak baku. | Kode tidak rapi, baris kode terlalu panjang (> 100 karakter), tanpa komentar dan tanpa docstring. |
