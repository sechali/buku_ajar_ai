# Panduan Instruktur & Kunci Solusi: AI Modul 2.3
## Struktur Logika Pemrograman: Aljabar Boolean, Evaluasi Predikat, dan Safety Interlock Agro-Industri

---

**Kode Modul:** AI Modul 2.3  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Dasar Algoritma & Logika Pemrograman untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi & Analogi PKS: Sistem Pengunci Keselamatan Bejana Sterilizer | Studi kasus bahaya industri, Diskusi terarah | Memancing nalar: Mengapa kesalahan logika pada aktuator fisik berakibat fatal? |
| **Menit 026 - 065** | Fondasi Aljabar Boolean, Gerbang Logika, dan Matriks Tabel Kebenaran | Kuliah interaktif, Pembuktian aljabar di papan tulis | Menjelaskan pemetaan logika biner ke sirkuit fisik dan relai kendali industri. |
| **Menit 066 - 100** | Hukum De Morgan, Presedensi Operator, dan Penyederhanaan Ekspresi | Latihan deduksi matematis terpandu | Membimbing pembuktian ekuivalensi logika menggunakan tabel kebenaran. |
| **Menit 101 - 130** | Investigasi Mendalam Evaluasi Short-Circuit & Guard Pattern | Live coding di IDE, Eksperimen *ZeroDivisionError* | Mendemonstrasikan penghematan waktu eksekusi dan pencegahan *crash*. |
| **Menit 131 - 150** | Refleksi Teori & Penjelasan Kerangka Praktikum Laboratorium | Tanya jawab HOTS, Pengenalan modul simulator | Mengaitkan logika predikat dengan pohon keputusan (*decision tree*) dalam AI. |
| **Praktikum (150m)**| Eksperimen Jupyter: Generator Tabel Kebenaran & Kendali Greenhouse | Hands-on coding terbimbing di Jupyter Notebook | Memandu implementasi logika *safety interlock* dan tantangan berjenjang. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Mengira `if a == 1 or 2:` Ekuivalen dengan `if a == 1 or a == 2:`
* **Gejala Mahasiswa:** Menulis sintaksis bahasa manusia ke Python seperti `if status == "matang" or "mengkal":`.
* **Strategi Remedial:** Tunjukkan bagaimana Python mengurai ekspresi:
  1. `a == 1` dievaluasi menghasilkan `False` (jika $a = 3$).
  2. Ekspresi menjadi `False or 2`.
  3. Angka `2` adalah nilai non-nol (*truthy*), sehingga `False or 2` selalu mengembalikan `2` (yang bernilai `True`). Akibatnya blok `if` selalu dieksekusi terlepas dari nilai $a$. Ajarkan sintaksis formal: `if a == 1 or a == 2:` atau `if a in (1, 2):`.

### Miskonsepsi 2: Mengacaukan Operator Logika (`and`, `or`, `not`) dengan Operator Bitwise (`&`, `|`, `~`)
* **Gejala Mahasiswa:** Menulis `if suhu > 30 & rh < 50:` yang memicu galat sintaksis atau evaluasi prioritas operator yang salah.
* **Strategi Remedial:** Jelaskan bahwa `and`/`or` adalah operator logika boolean dengan sifat *short-circuit*, sedangkan `&`/`|` adalah operator manipulasi bit (*bitwise*). Operator `&` memiliki presedensi lebih tinggi daripada operator relasional `<`, sehingga `30 & rh` dihitung terlebih dahulu sebelum perbandingan.

### Miskonsepsi 3: Salah Menerapkan Hukum De Morgan (Lupa Membalik Operator)
* **Gejala Mahasiswa:** Menulis negasi dari `(A and B)` menjadi `(not A and not B)` alih-alih `(not A or not B)`.
* **Strategi Remedial:** Berikan contoh kalimat nyata: *"Syarat lulus adalah hadir DAN mengerjakan tugas"*. Lawan dari syarat tersebut adalah *"Tidak hadir ATAU tidak mengerjakan tugas"*, bukan harus melakukan kedua pelanggaran tersebut bersamaan.

### Miskonsepsi 4: Mengabaikan Urutan Presedensi dalam Ekspresi Logika Majemuk
* **Gejala Mahasiswa:** Menulis `A or B and C` dan mengira dievaluasi dari kiri ke kanan `(A or B) and C`.
* **Strategi Remedial:** Tegaskan hierarki baku: `not` menduduki prioritas tertinggi, diikuti `and`, dan terakhir `or`. Selalu anjurkan mahasiswa menambahkan tanda kurung eksplisit `( ... )` demi keterbacaan kode (*defensive code styling*).

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Optimasi Gerbang menggunakan Hukum De Morgan
* **Persamaan Awal:**
  $$\text{Alarm} = \neg(\text{Pompa\_Normal} \land \text{Tekanan\_Cukup}) \lor \neg(\text{Katup\_Terbuka} \lor \text{Aliran\_Mendeteksi})$$
* **Langkah Penyederhanaan:**
  1. Terapkan De Morgan pada suku pertama:
     $$\neg(\text{Pompa\_Normal} \land \text{Tekanan\_Cukup}) \iff \neg\text{Pompa\_Normal} \lor \neg\text{Tekanan\_Cukup}$$
  2. Terapkan De Morgan pada suku kedua:
     $$\neg(\text{Katup\_Terbuka} \lor \text{Aliran\_Mendeteksi}) \iff \neg\text{Katup\_Terbuka} \land \neg\text{Aliran\_Mendeteksi}$$
  3. Gabungkan kedua suku:
     $$\text{Alarm} = \neg\text{Pompa\_Normal} \lor \neg\text{Tekanan\_Cukup} \lor (\neg\text{Katup\_Terbuka} \land \neg\text{Aliran\_Mendeteksi})$$
* **Pembuktian Ekuivalensi:** Bentuk yang disederhanakan mengeliminasi 2 gerbang negasi global dan memungkinkan evaluasi *short-circuit* instan: jika pompa tidak normal, sistem langsung membunyikan alarm tanpa memeriksa sensor tekanan, katup, atau aliran.

---

### Pertanyaan 2: Analisis Fail-Safe pada Kerusakan Sensor Jarak
* **Masalah:**
  ```python
  if sensor_jarak.baca_jarak() < 1.0 and robot.hentikan_lengan():
      print("Lengan berhenti aman")
  ```
  Jika pembacaan sensor gagal melempar pengecualian (*exception*), eksekusi terhenti mendadak sebelum lengan sempat dihentikan.
* **Solusi Rekayasa Fail-Safe Mutlak:**
  Pisahkan pengujian sensor ke dalam blok penanganan eksepsi (`try-except`), dan tetapkan status default bahwa jika sensor gagal, sistem berasumsi bahaya (*fail-stop principle*):
  ```python
  try:
      jarak = sensor_jarak.baca_jarak()
      bahaya_tabrakan = jarak < 1.0
  except HardwareTimeoutException:
      # Asumsi terburuk: Sensor rusak dianggap kondisi kritis!
      bahaya_tabrakan = True

  if bahaya_tabrakan:
      robot.hentikan_lengan()
      print("Lengan dihentikan secara aman (Protokol Fail-Safe Aktif)")
  ```

---

### Pertanyaan 3: Sintesis Desain Logika Voting Redundan (Triple Modular Redundancy - TMR)
* **Skenario:** 3 sensor ketinggian ($S_1, S_2, S_3$). Sistem aman jika minimal 2 sensor menyatakan aman ($S = 1$).
* **Penurunan Fungsi Boolean:**
  Kondisi minimal 2 dari 3 sensor bernilai 1 terjadi pada kombinasi:
  - $S_1=1, S_2=1, S_3=0$
  - $S_1=1, S_2=0, S_3=1$
  - $S_1=0, S_2=1, S_3=1$
  - $S_1=1, S_2=1, S_3=1$
* **Bentuk Kanonik Sum of Products (SOP):**
  $$Y = (S_1 \land S_2 \land \neg S_3) \lor (S_1 \land \neg S_2 \land S_3) \lor (\neg S_1 \land S_2 \land S_3) \lor (S_1 \land S_2 \land S_3)$$
* **Penyederhanaan Aljabar Boolean:**
  Kelompokkan suku dengan $(S_1 \land S_2 \land S_3)$ menggunakan sifat idempoten $A \lor A = A$:
  $$Y = (S_1 \land S_2) \lor (S_2 \land S_3) \lor (S_1 \land S_3)$$
* **Kesimpulan:** Output voting mayoritas setara dengan tiga pasang gerbang AND yang di-OR-kan: $Y = (S_1 \land S_2) \lor (S_2 \land S_3) \lor (S_1 \land S_3)$.

---

## 4. Kunci Solusi Lengkap Tantangan Pemrograman Scaffolded

### Solusi Tantangan 1 (Tingkat Dasar): Verifikasi Kelayakan Panen Sawit

```python
from typing import Tuple


def cek_kelayakan_panen(
    brondolan: int, ffa: float, warna_hitam: bool
) -> Tuple[bool, str]:
    """Memvalidasi kriteria panen TBS kelapa sawit berdasarkan 3 parameter agronomis."""
    cukup_brondol = brondolan >= 5
    kadar_ffa_bagus = ffa <= 3.0
    bukan_mentah = not warna_hitam

    layak_panen = cukup_brondol and kadar_ffa_bagus and bukan_mentah

    if layak_panen:
        pesan = "TBS LAYAK PANEN: Memenuhi standar kematangan PKS."
    else:
        alasan = []
        if not cukup_brondol:
            alasan.append(f"Brondolan kurang ({brondolan} < 5)")
        if not kadar_ffa_bagus:
            alasan.append(f"FFA terlalu tinggi ({ffa:.1f}% > 3.0%)")
        if not bukan_mentah:
            alasan.append("Warna buah masih hitam-ungu (Mentah)")
        pesan = f"TBS TIDAK LAYAK PANEN: {', '.join(alasan)}"

    return layak_panen, pesan


# Pengujian
assert cek_kelayakan_panen(8, 2.1, False)[0] is True
assert cek_kelayakan_panen(2, 2.1, False)[0] is False
assert cek_kelayakan_panen(8, 4.5, False)[0] is False
assert cek_kelayakan_panen(8, 2.1, True)[0] is False
print("[OK] Solusi Tantangan 1 lulus seluruh pengujian!")
```

---

### Solusi Tantangan 3 (Tingkat Mahir): Mesin Inferensi Sistem Pakar Defisiensi Hara

```python
from typing import Dict, List, Set


class ExpertSystemDefisiensiSawit:
    """Mesin inferensi sistem pakar forward-chaining untuk diagnosis defisiensi nutrisi kelapa sawit."""

    def __init__(self):
        # Basis Pengetahuan Aturan Produksi (Rule-Based Knowledge Base)
        self.rules = [
            {
                "defisiensi": "Defisiensi Nitrogen (N)",
                "syarat_wajib": {
                    "daun_muda_kuning",
                    "pelepah_pendek_terhambat",
                },
                "syarat_larangan": {"serangan_rayap"},
                "rekomendasi": "Aplikasi pupuk Urea / ZA 2.0 kg/pohon dan perbaikan drainase.",
            },
            {
                "defisiensi": "Defisiensi Kalium (K)",
                "syarat_wajib": {"bercak_oranye_daun_tua", "tepi_daun_kering"},
                "syarat_larangan": set(),
                "rekomendasi": "Aplikasi MOP (Muriate of Potash) / KCl 2.5 kg/pohon secara melingkar.",
            },
            {
                "defisiensi": "Defisiensi Magnesium (Mg)",
                "syarat_wajib": {"daun_tua_kuning_cerah", "tulang_daun_hijau"},
                "syarat_larangan": set(),
                "rekomendasi": "Aplikasi pupuk Kieserit / Dolomit 1.5 kg/pohon di piringan.",
            },
        ]

    def diagnosa(self, gejala_input: Set[str]) -> List[Dict[str, str]]:
        hasil_diagnosa = []

        for rule in self.rules:
            # 1. Evaluasi Logika: Seluruh syarat wajib HARUS terpenuhi (Subset checking)
            syarat_terpenuhi = rule["syarat_wajib"].issubset(gejala_input)

            # 2. Evaluasi Logika: Tidak boleh ada gejala yang masuk dalam syarat larangan
            tidak_ada_larangan = len(rule["syarat_larangan"] & gejala_input) == 0

            # 3. Konjungsi Boolean Aturan
            if syarat_terpenuhi and tidak_ada_larangan:
                hasil_diagnosa.append(
                    {
                        "penyakit": rule["defisiensi"],
                        "rekomendasi": rule["rekomendasi"],
                    }
                )

        if not hasil_diagnosa:
            hasil_diagnosa.append(
                {
                    "penyakit": "Tidak Teridentifikasi / Normal",
                    "rekomendasi": "Lakukan uji laboratorium jaringan daun (Leaf Sampling Unit / LSU).",
                }
            )

        return hasil_diagnosa


# Pengujian Sistem Pakar
pakar = ExpertSystemDefisiensiSawit()

# Uji Kasus: Gejala Defisiensi Nitrogen
gejala_kebun_1 = {"daun_muda_kuning", "pelepah_pendek_terhambat"}
res_1 = pakar.diagnosa(gejala_kebun_1)
assert res_1[0]["penyakit"] == "Defisiensi Nitrogen (N)"

# Uji Kasus: Gejala Nitrogen tetapi ada rayap -> Harus di-reject oleh syarat_larangan
gejala_kebun_2 = {
    "daun_muda_kuning",
    "pelepah_pendek_terhambat",
    "serangan_rayap",
}
res_2 = pakar.diagnosa(gejala_kebun_2)
assert res_2[0]["penyakit"] == "Tidak Teridentifikasi / Normal"

print("[OK] Solusi Tantangan 3 lulus seluruh verifikasi inferensi pakar!")
```

---

## 5. Rubrik Penilaian Praktikum Mahasiswa

Total Bobot: **100 Poin**

| Kriteria Penilaian | Bobot | Indikator Kinerja Unggul (Poin Penuh) | Indikator Kinerja Kurang (Poin Minimal) |
| :--- | :---: | :--- | :--- |
| **Kebenaran Aljabar Boolean** | **25%** | Mampu membuktikan ekuivalensi De Morgan; tabel kebenaran 100% akurat; tidak ada kebingungan antara operator relasional dan logika. | Menyamakan `AND` dengan `OR`; salah mengisi tabel kebenaran dasar; tidak memahami gerbang `XOR`. |
| **Penerapan Short-Circuit & Guard** | **25%** | Mampu mendemonstrasikan penghematan waktu eksekusi; berhasil mencegah *ZeroDivisionError* menggunakan penempatan operan yang aman. | Menempatkan ekspresi berisiko galat di sebelah kiri tanpa proteksi; tidak memahami konsep evaluasi jalur pendek. |
| **Logika Safety Interlock Agro-Industri** | **25%** | Mampu membangun logika multi-kondisi sterilizer dan greenhouse; pemisahan hierarki agronomis vs keselamatan mutlak. | Kondisi darurat terabaikan; logika keselamatan bocor sehingga aktuator tetap menyala saat kondisi bahaya. |
| **Kualitas Kode & Modularitas Python** | **25%** | Kode bersih, menggunakan anotasi pengetikan (`typing`), modular dengan fungsi deskriptif, dan lulus seluruh *unit test suite*. | Kode ditulis monolitik tanpa fungsi; terjadi kesalahan penamaan variabel; memicu *TypeError* saat eksekusi. |
