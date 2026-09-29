# Panduan Instruktur & Kunci Solusi: AI Modul 2.4
## Variabel dan Tipe Data: Model Memori Objek, Presisi IEEE 754, dan Parsing Telemetri Perkebunan

---

**Kode Modul:** AI Modul 2.4  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Dasar Algoritma & Logika Pemrograman untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi & Analogi PKS: Gudang Logistik & Kontainer Bertiket Loading Ramp | Analisis alur logistik pabrik sawit, Diskusi terarah | Membedah konsep: Mengapa variabel hanyalah label tiket, bukan wadahnya? |
| **Menit 026 - 065** | Model Memori Python (Heap, Stack, Reference Counting, Mutabilitas) | Diagram visual memori, Eksperimen fungsi `id()` | Membuktikan bahwa modifikasi integer menciptakan objek baru di memori Heap. |
| **Menit 066 - 100** | Standar IEEE 754 Double Precision & Pembuktian Galat $0.1 + 0.2 \ne 0.3$ | Bedah formula bit biner, Live interpreter Python | Menjelaskan bahaya finansial jika timbangan CPO memakai komparasi `==`. |
| **Menit 101 - 130** | Sistem Pengetikan Python (Dynamic, Strong) & Type Hinting PEP 484 | Demonstrasi anotasi fungsi dengan `typing` | Melatih mahasiswa menulis kode beranotasi tipe ketat untuk data pipeline AI. |
| **Menit 131 - 150** | Refleksi Teori & Pengantar Tantangan Praktikum Laboratorium | Tanya jawab HOTS, Review format CSV cuaca AWS | Menekankan prinsip *defensive type casting* saat membaca data sensor IoT. |
| **Praktikum (150m)**| Eksperimen Jupyter: Profiling Memori, Uji Presisi, & Parser TBS | Hands-on coding terbimbing di Jupyter Notebook | Membimbing implementasi pembersih teks berat dan parser telemetri AWS. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Menganggap Variabel sebagai "Kotak Fisik Penyimpan Nilai"
* **Gejala Mahasiswa:** Mengira saat menulis `b = a`, nilai `a` disalin ke wadah baru `b`. Ketika memodifikasi list `b.append(10)`, mahasiswa heran mengapa isi list `a` ikut berubah.
* **Strategi Remedial:** Tunjukkan visualisasi pointer referensi memori: `a` dan `b` adalah dua tiket identitas yang digantungkan pada keranjang belanja yang sama di Heap. Jika ingin menyalin keranjang baru, wajib menggunakan *shallow/deep copy*: `b = a.copy()`.

### Miskonsepsi 2: Menggunakan Argumen Default Objek Mutabel (`def f(data=[])`)
* **Gejala Mahasiswa:** Mendefinisikan list kosong sebagai nilai default parameter fungsi, lalu bingung mengapa data dari eksekusi sebelumnya masih tersimpan di eksekusi berikutnya.
* **Strategi Remedial:** Jelaskan bahwa ekspresi default parameter hanya dievaluasi **satu kali saat definisi fungsi dimuat ke memori**, bukan setiap kali fungsi dipanggil. Gunakan pola idiomatis Python: `def f(data: Optional[List] = None): if data is None: data = []`.

### Miskonsepsi 3: Mengira Pecahan $0.1$ Bersifat Eksak dalam Komputer
* **Gejala Mahasiswa:** Menulis `if total_berat == 1.0:` setelah melakukan penjumlahan bertahap `0.1` sebanyak 10 kali, lalu program gagal karena kondisi bernilai `False`.
* **Strategi Remedial:** Buka tab kalkulator pecahan biner IEEE 754. Tunjukkan bahwa $0.1$ dalam biner adalah pecahan berulang tak hingga $0.000110011..._2$. Selalu wajibkan mahasiswa menggunakan `math.isclose(a, b)` atau pustaka `decimal.Decimal` untuk data finansial perkebunan.

### Miskonsepsi 4: Mengira Python Melakukan Konversi Tipe Otomatis secara Lemah (*Weak Typing*)
* **Gejala Mahasiswa:** Mengharapkan `'Panen ke-' + 5` menghasilkan `'Panen ke-5'` seperti pada bahasa JavaScript atau PHP.
* **Strategi Remedial:** Tegaskan bahwa Python adalah bahasa **Strongly Typed**. Python menolak konversi implisit yang ambigu antara teks dan angka untuk mencegah galat tersembunyi. Tunjukkan sintaks konversi eksplisit: `f"Panen ke-{5}"` atau `'Panen ke-' + str(5)`.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Bahaya Mutable Default Argument
* **Masalah:**
  ```python
  def tambahkan_batch_sensor(fitur_baru: float, batch_data: list = []) -> list:
      batch_data.append(fitur_baru)
      return batch_data
  ```
* **Dekonstruksi Memori:** Objek `[]` dibuat di memori Heap tepat satu kali saat modul Python dikompilasi ke bytecode. Parameter default `batch_data` menunjuk ke alamat memori list tersebut. Setiap kali fungsi dipanggil tanpa argumen kedua, list yang sama dimodifikasi *in-place*. Akibatnya, data batch dari perkebunan Blok A akan tercampur baur dengan data batch dari Blok B, merusak integritas dataset model AI.
* **Solusi Idiomatis Standar Industri:**
  ```python
  from typing import List, Optional


  def tambahkan_batch_sensor(
      fitur_baru: float, batch_data: Optional[List[float]] = None
  ) -> List[float]:
      if batch_data is None:
          batch_data = []  # Alokasi list baru secara independen per pemanggilan
      batch_data.append(fitur_baru)
      return batch_data
  ```

---

### Pertanyaan 2: Audit Dampak Finansial Galat IEEE 754 pada Pabrik Kelapa Sawit
* **Analisis Data:**
  - $10.000$ transaksi/bulan $= 120.000$ transaksi/tahun.
  - Rata-rata muatan: $15.5 \text{ ton}$ per truk.
  - Deviasi pembulatan per kalkulasi: $+0.00000015 \text{ ton}$.
  - Akumulasi deviasi per tahun: $120.000 \times 0.00000015 = 0.018 \text{ ton} = 18 \text{ kg}$ CPO.
  - Meskipun secara fisik $18 \text{ kg}$ terlihat kecil, dalam audit akuntansi finansial berstandar SAP/ERP, ketidakcocokan antara timbangan bruto-tara dengan neraca massa tangki timbun CPO akan memicu *unreconciled variance* yang menggagalkan audit sertifikasi ISPO/RSPO.
* **Kapan `decimal.Decimal` Wajib Digunakan:**
  Pada sistem penagihan faktur pembayaran pekebun sawit, kalkulasi royalti bibit unggul, dan rekonsiliasi stok tangki ekspor CPO. Untuk kalkulasi fitur model machine learning (seperti tensor citra daun), `float` 64-bit atau `float32` tetap dipilih karena membutuhkan akselerasi perangkat keras GPU.

---

### Pertanyaan 3: Mitigasi Bug Dynamic Typing pada Telemetri LiDAR Drone
* **Arsitektur Pertahanan Sensor (*Defensive Type Ingestion*):**
  ```python
  from typing import Optional, Tuple


  def validasi_jarak_lidar(raw_telemetry: object) -> Tuple[bool, float]:
      """Memvalidasi dan mengonversi masukan sensor LiDAR ke float aman."""
      try:
          # Mencoba konversi ke float
          jarak = float(raw_telemetry)
          # Menguji apakah nilainya bukan NaN atau tak hingga
          if math.isnan(jarak) or math.isinf(jarak):
              return False, 0.0
          # Memeriksa batas fisik realistis ketinggian drone (0.2m s.d. 50.0m)
          if 0.2 <= jarak <= 50.0:
              return True, jarak
          return False, 0.0
      except (ValueError, TypeError):
          return False, 0.0
  ```
  Jika fungsi mengembalikan `False`, sistem kendali penerbangan drone langsung mengabaikan pembacaan tersebut dan beralih ke sensor barometer cadangan (*fail-over sensor*).

---

## 4. Kunci Solusi Lengkap Tantangan Pemrograman Scaffolded

### Solusi Tantangan 2 (Tingkat Menengah): Parser Baris CSV Cuaca AWS Perkebunan

```python
from typing import Any, Dict, Optional


def parse_baris_aws(baris_csv: str) -> Optional[Dict[str, Any]]:
    """Memecah dan memvalidasi baris CSV telemetri cuaca stasiun AWS perkebunan."""
    if not isinstance(baris_csv, str):
        return None

    kolom = [k.strip() for k in baris_csv.split(",")]
    if len(kolom) != 5:
        return None  # Jumlah kolom tidak sesuai spesifikasi

    waktu_str, raw_t, raw_rh, raw_solar, raw_hujan = kolom

    try:
        # 1. Parsing Suhu (Celsius)
        suhu_c = float(raw_t)
        if not (-10.0 <= suhu_c <= 60.0):
            return None  # Batas fisik suhu tropis

        # 2. Parsing Kelembaban Relatif (Persen)
        rh = float(raw_rh)
        if not (0.0 <= rh <= 100.0):
            return None  # RH tidak boleh melebihi 100%

        # 3. Parsing Status Solar Panel (Boolean)
        status_solar = raw_solar in ("1", "True", "true", "TRUE")

        # 4. Parsing Curah Hujan (mm)
        curah_hujan = float(raw_hujan)
        if curah_hujan < 0.0:
            return None  # Curah hujan tidak boleh negatif

        return {
            "waktu": waktu_str,
            "suhu_c": suhu_c,
            "rh_persen": rh,
            "solar_aktif": status_solar,
            "curah_hujan_mm": curah_hujan,
        }

    except ValueError:
        return None  # Terjadi kegagalan casting numerik


# Pengujian
baris_valid = "2026-09-28 14:00, 32.4, 85.2, 1, 0.0"
res = parse_baris_aws(baris_valid)
assert res is not None
assert res["suhu_c"] == 32.4
assert res["solar_aktif"] is True

baris_invalid = "2026-09-28 14:00, 32.4, 150.0, 1, 0.0"  # RH 150% out of bounds
assert parse_baris_aws(baris_invalid) is None
print("[OK] Solusi Tantangan 2 (Parser AWS) lulus seluruh pengujian!")
```

---

### Solusi Tantangan 3 (Tingkat Mahir): Engine Akumulator CPO Presisi Decimal

```python
import decimal
from typing import Any, Dict, List, Union


class AkumulatorCPODecimal:
    """Mesin akumulasi tonase CPO dengan presisi desimal mutlak (Bebas Galat IEEE 754)."""

    def __init__(self, tarif_ppn_persen: float = 11.0):
        # Mengatur konteks presisi desimal 28 digit dengan pembulatan ROUND_HALF_EVEN
        decimal.getcontext().prec = 28
        decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN

        self.transaksi: List[decimal.Decimal] = []
        self.tarif_ppn = (
            decimal.Decimal(str(tarif_ppn_persen)) / decimal.Decimal("100.0")
        )

    def catat_transaksi(self, nilai_tonase: Union[str, float, int]) -> None:
        """Mengonversi nilai masukan secara aman ke decimal.Decimal."""
        # Wajib mengonversi float ke string terlebih dahulu untuk mencegah transfer galat biner
        d_val = decimal.Decimal(str(nilai_tonase))
        if d_val <= decimal.Decimal("0.0"):
            raise ValueError(f"Nilai tonase harus positif: {d_val}")
        self.transaksi.append(d_val)

    def hitung_neraca(self, harga_per_ton_idr: int) -> Dict[str, Any]:
        """Menghitung total tonase, nilai rupiah kotor, PPN, dan nilai bersih."""
        total_ton = sum(self.transaksi)
        harga_d = decimal.Decimal(str(harga_per_ton_idr))

        nilai_bruto = total_ton * harga_d
        nilai_ppn = (nilai_bruto * self.tarif_ppn).quantize(
            decimal.Decimal("1")
        )  # Bulatkan ke rupiah terdekat
        nilai_netto = nilai_bruto + nilai_ppn

        return {
            "total_tonase": total_ton,
            "jumlah_transaksi": len(self.transaksi),
            "nilai_bruto_idr": int(nilai_bruto),
            "ppn_idr": int(nilai_ppn),
            "total_pembayaran_idr": int(nilai_netto),
        }


# Pengujian Akumulator
akumulator = AkumulatorCPODecimal(tarif_ppn_persen=11.0)
# Memasukkan 10 kali transaksi 0.1 ton
for _ in range(10):
    akumulator.catat_transaksi("0.1")

neraca = akumulator.hitung_neraca(harga_per_ton_idr=12_500_000)
# Total tonase HARUS tepat 1.0 murni tanpa deviasi 0.00000000000000004
assert neraca["total_tonase"] == decimal.Decimal("1.0")
assert neraca["nilai_bruto_idr"] == 12_500_000
assert neraca["ppn_idr"] == 1_375_000
assert neraca["total_pembayaran_idr"] == 13_875_000
print(
    "[OK] Solusi Tantangan 3 (Akumulator CPO Decimal) lulus verifikasi akuntansi 100%!"
)
```

---

## 5. Rubrik Penilaian Praktikum Mahasiswa

Total Bobot: **100 Poin**

| Kriteria Penilaian | Bobot | Indikator Kinerja Unggul (Poin Penuh) | Indikator Kinerja Kurang (Poin Minimal) |
| :--- | :---: | :--- | :--- |
| **Pemahaman Model Memori Objek** | **25%** | Mampu membedakan operator `is` dan `==`; mendemonstrasikan mutasi *in-place*; tidak menggunakan *mutable default argument*. | Mengira `b = a` menyalin data; tidak memahami sifat imutabilitas; gagal menjelaskan fungsi `id()`. |
| **Penguasaan Presisi Pecahan IEEE 754** | **25%** | Memahami akar penyebab biner $0.1 + 0.2 \ne 0.3$; selalu menggunakan `math.isclose()` atau `Decimal` saat komparasi float. | Membandingkan bilangan float dengan kesetaraan ketat `==`; mengabaikan galat pembulatan. |
| **Ketahanan Parsing & Sanitasi Tipe** | **25%** | Menerapkan *defensive casting* bertingkat; memvalidasi rentang fisik data IoT; menangani nilai string kotor tanpa crash. | Kode melempar *ValueError* atau *TypeError* saat diberi data string tak terduga; tidak ada sanitasi spasi. |
| **Penerapan Type Hinting & Clean Code** | **25%** | Seluruh fungsi memiliki anotasi tipe parameter dan return value (PEP 484); struktur data rapi; 100% lulus seluruh *unit test*. | Tidak ada type hinting; fungsi monolitik tanpa penanganan eksepsi; penamaan variabel ambigu. |
