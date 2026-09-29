# Panduan Instruktur & Kunci Solusi: AI Modul 3.3
## Sintaks Dasar Python: Aturan Leksikal dan Tokenisasi, Indentasi Signifikan (Off-Side Rule), Standar Rekayasa Kode Bersih PEP 8, Sistem Dokumentasi PEP 257, dan Pemodelan Neraca Air Lahan Sawit

---

**Kode Modul:** AI Modul 3.3  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Pemrograman Python Dasar untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi: Keterbacaan Kode Sebagai Standar Rekayasa AI Industri | Bedah perbandingan kode spaghetti vs kode bersih berstandar PEP 8 | Menanamkan paradigma bahwa kode AI dibaca jauh lebih sering daripada ditulis; keterbacaan menentukan kecepatan riset. |
| **Menit 026 - 060** | Struktur Leksikal: Token, Reserved Keywords, & Aturan Identifier | Eksplorasi interaktif modul `keyword` dan metode `str.isidentifier()` | Membimbing mahasiswa mengenali 35 kata kunci resmi dan membedakan nama yang sah secara sintaksis vs nama yang elegan secara semantik. |
| **Menit 061 - 095** | Teori Kompilator: Mekanisme Tumpukan Indentasi (*Indent Stack*) & Off-Side Rule | Diagram visual tumpukan lexer, Demonstrasi langsung modul `tokenize` | Membuktikan bagaimana interpreter mengemisikan token `INDENT` dan `DEDENT` serta mengeliminasi ambiguitas *dangling-else*. |
| **Menit 096 - 125** | Standar PEP 8 & PEP 257: Konvensi Penamaan dan Google Style Docstrings | Analisis berkas skrip agroteknologi, Introspeksi `__doc__` & `help()` | Melatih mahasiswa menyusun docstrings terstruktur lengkap dengan seksi `Args:`, `Returns:`, dan `Raises:`. |
| **Menit 126 - 150** | Refleksi Teori & Bedah Masalah Tingkat Tinggi (HOTS) | Diskusi panel integrasi Linter (Ruff/Flake8) dan Formatter (Black) | Mengarahkan mahasiswa memahami peran otomatisasi audit sintaksis pada pipeline integrasi berkelanjutan (CI/CD). |
| **Praktikum (150m)**| Eksperimen Jupyter: Tokenisasi Leksikal, Model Neraca Air, & Linter Mandiri | Hands-on coding terbimbing di Jupyter Notebook | Memfasilitasi mahasiswa membedah token kode dan membangun auditor kepatuhan PEP 8 dengan target 100% lulus. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Menganggap Karakter Tab (`\t`) dan 4 Spasi Adalah Hal yang Sama Karena Tampak Mirip
* **Gejala Mahasiswa:** Menekan tombol Tab pada satu baris dan tombol Spasi pada baris berikutnya, lalu heran mengapa interpreter Python 3 melempar `TabError: inconsistent use of tabs and spaces in indentation`.
* **Strategi Remedial:** Tunjukkan tampilan karakter tak terlihat (*Render Whitespace*) di Visual Studio Code: karakter tab ditampilkan sebagai panah panjang (`→`), sedangkan spasi ditampilkan sebagai titik kecil (`·`). Jelaskan bahwa lebar tab bergantung pada konfigurasi editor pengguna (bisa 2, 4, atau 8 kolom), sementara spasi bersifat absolut. Wajibkan pengaturan *"Editor: Insert Spaces"* aktif pada VS Code.

### Miskonsepsi 2: Berasumsi Bahwa Nama yang Sah Secara Sintaksis Selalu Merupakan Nama yang Baik
* **Gejala Mahasiswa:** Menggunakan nama variabel acak satu huruf (`x`, `y1`, `temp2`, `data_a`) atau mencampur huruf kapital tanpa aturan (`SuhuKanopiSawit` untuk variabel lokal biasa) dengan dalih kode tetap bisa dieksekusi (*valid syntax*).
* **Strategi Remedial:** Bedah pedoman PEP 8: sintaksis legal hanyalah syarat minimal kompiler, sedangkan konvensi komunitas adalah syarat profesionalisme. Tunjukkan kode simulasi neraca air: variabel `defisit_mm` jauh lebih mudah dipahami dan bebas dari risiko salah tafsir satuan dibanding variabel `d`. Tanamkan konvensi `snake_case` untuk variabel dan fungsi, serta `PascalCase` untuk kelas.

### Miskonsepsi 3: Mengira Komentar Biasa (`#`) Berfungsi Sebagai Dokumentasi Resmi Fungsi
* **Gejala Mahasiswa:** Menuliskan penjelasan rumus matematika di atas fungsi menggunakan `# Komentar baris`, lalu terkejut saat fungsi `help(nama_fungsi)` atau perintah introspeksi `print(nama_fungsi.__doc__)` mengembalikan nilai `None`.
* **Strategi Remedial:** Jelaskan perbedaan fase kompilasi CPython: komentar tanda pagar (`#`) langsung dibuang oleh *lexer* saat kode diubah menjadi token, sehingga tidak pernah sampai ke memori runtime. Sebaliknya, string literal tripel kutip `"""..."""` di awal tubuh fungsi diikatkan oleh kompilator ke atribut `__doc__` milik objek fungsi di memori Heap, memungkinkan sistem dokumentasi otomatis bekerja.

### Miskonsepsi 4: Menyambungkan Baris Panjang Menggunakan Backslash (`\`) Secara Berlebihan
* **Gejala Mahasiswa:** Memecah formula matematika panjang dengan menyisipkan karakter `\` di ujung setiap baris fisik (`hasil = a + \ \n b + \ \n c`).
* **Strategi Remedial:** Tunjukkan kerapuhan karakter backslash: jika pemrogram secara tidak sengaja menekan spasi setelah tanda `\`, Python akan melempar `SyntaxError: unexpected character after line continuation character`. Tanamkan kaidah baku PEP 8: manfaatkan **penyambungan baris implisit (*implicit continuation*)** dengan membungkus seluruh ekspresi matematika di dalam tanda kurung biasa `(...)`.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Leksikal CPython: Mekanisme Tumpukan Indentasi dan Penanganan Emisi Token `DEDENT` Berantai
* **Soal:**
  1. Bagaimana Lexer CPython memanipulasi *Indentation Stack* dari state `[0, 4, 8, 12]` kembali ke tingkat `[0, 4]`?
  2. Berapa token `DEDENT` yang diemisikan?
  3. Mengapa spasi ganjil (misal 6 spasi) langsung memicu `IndentationError` sebelum runtime?
* **Jawaban Komprehensif:**
  1. **Manipulasi Indentation Stack:**
     - Lexer membaca baris baru dan menghitung spasi di awal baris (*leading spaces*), mendeteksi nilai $4$ spasi.
     - Lexer membandingkan nilai $4$ dengan puncak stack saat ini ($12$). Karena $4 < 12$, lexer memulai siklus penarikan (*unindenting*).
     - Elemen $12$ di-pop dari stack. Stack menjadi `[0, 4, 8]`.
     - Lexer membandingkan kembali $4$ dengan puncak stack baru ($8$). Karena $4 < 8$, elemen $8$ di-pop dari stack. Stack menjadi `[0, 4]`.
     - Puncak stack kini bernilai $4$, yang cocok (*match*) dengan spasi baris baru. Siklus unindenting berhenti.
  2. **Jumlah Token DEDENT yang Diemisikan:**  
     Tepat **2 token `DEDENT`** diemisikan ke parser (satu token untuk penutupan blok kolom 12, dan satu token untuk penutupan blok kolom 8).
  3. **Penyebab Terjadinya IndentationError:**  
     Jika baris baru memiliki 6 spasi: setelah nilai $12$ dan $8$ di-pop, nilai puncak stack berikutnya adalah $4$. Karena angka $6$ tidak pernah ada di dalam riwayat stack `[0, 4]`, CPython tidak dapat menentukan blok hierarki mana yang dituju oleh baris tersebut. Oleh karena itu, *lexer* segera membatalkan proses kompilasi leksikal dan melempar `IndentationError: unindent does not match any outer indentation level` secara dini (*compile-time error*).

---

### Pertanyaan 2: Dekonstruksi Keunggulan Arsitektur: Resolusi Inheren Ambiguitas *Dangling Else*
* **Soal:** Jelaskan mengapa C/Java ambigu pada klausa percabangan bersarang, dan buktikan bagaimana aturan *Off-Side* Python mengeliminasi ambiguitas tersebut!
* **Jawaban Komprehensif:**
  1. **Ambiguitas pada Bahasa Bebas Format (Free-Form Languages):**  
     Pada bahasa seperti C dan Java, karakter spasi dan baris baru diabaikan oleh kompilator (*insignificant whitespace*). Dalam tata bahasa bebas konteks (*Context-Free Grammar*) standar bahasa C, aturan percabangan dirumuskan sebagai:
     $$\text{Statement} \rightarrow \mathbf{if} \ (\text{Expr}) \ \text{Statement} \ | \ \mathbf{if} \ (\text{Expr}) \ \text{Statement} \ \mathbf{else} \ \text{Statement}$$
     Ketika menemui konstruksi `if (A) if (B) S1; else S2;`, kompilator menghadapi dua pohon derivasi yang sama-sama valid secara sintaksis: mengaitkan `else` ke `if (A)` atau ke `if (B)`. Untuk memecahkan ambiguitas ini, kompiler C terpaksa menambahkan aturan ad-hoc buatan (*disambiguating rule*): *"Klausa else selalu dipasangkan dengan if terdekat sebelumnya"*, yang sering kali bertentangan dengan visualisasi indentasi pemrogram manusia.
  2. **Resolusi Deterministik Berbasis Off-Side Rule Python:**  
     Dalam tata bahasa resmi Python, aturan percabangan tidak menggunakan kata kunci penutup, melainkan blok terikat token:
     $$\text{if\_stmt} \rightarrow \mathbf{if} \ \text{test} : \mathbf{suite} \ [\mathbf{else} : \mathbf{suite}]$$
     $$\mathbf{suite} \rightarrow \text{simple\_stmt} \ | \ \mathbf{NEWLINE} \ \mathbf{INDENT} \ \text{stmt}^+ \ \mathbf{DEDENT}$$
     Karena blok pernyataan diwajibkan diawali oleh token `INDENT` dan ditutup oleh token `DEDENT`, posisi kata kunci `else:` terhadap token `DEDENT` secara matematis menentukan pasangannya:
     - Jika `else:` muncul sebelum token `DEDENT` dari blok luar, maka parser secara deterministik mengaitkannya ke `if` bagian dalam.
     - Jika token `DEDENT` diemisikan terlebih dahulu sebelum `else:`, blok `if` bagian dalam telah dinyatakan selesai (*closed grammar unit*), sehingga `else:` secara mutlak hanya dapat dipasangkan dengan `if` bagian luar.  
     Dengan demikian, tata bahasa Python berkarakteristik deterministik murni tanpa ambiguitas.

---

### Pertanyaan 3: Audit Kualitas Perangkat Lunak: Linter Otomatis vs Pemformat Kode (*Black*)
* **Soal:** Analisis perbedaan peran Linter Statis (Flake8/Ruff) vs Formatter Otomatis (Black) dan dampaknya terhadap efisiensi *Code Review* pada tim AI agribisnis!
* **Jawaban Komprehensif:**
  1. **Perbedaan Peran Fungsional:**
     - **Linter Statis (*Flake8 / Ruff*):** Berperan sebagai inspektur logika dan standar. Linter memeriksa kode sumber terhadap potensi galat (*undefined variables*, variabel yang tidak digunakan, impor modul yang salah, percabangan yang tidak pernah tercapai), serta mencatat pelanggaran gaya penulisan PEP 8 tanpa mengubah teks berkas secara mandiri (bersifat *read-only diagnostic*).
     - **Opinionated Formatter (*Black*):** Berperan sebagai eksekutor tata letak fisik. Black membaca AST kode dan memformat ulang seluruh teks berkas dari nol sesuai satu aturan baku absolut (panjang baris 88 karakter, penataan koma trailing konsisten, pembersihan spasi berlebih). Black mengabaikan preferensi visual pemrogram demi keseragaman 100% (*deterministic AST-preserving code generation*).
  2. **Dampak terhadap Efisiensi Code Review Tim Riset:**
     Pada proyek tim AI agribisnis berskala besar (misal gabungan periset sensorik, pemroses citra drone, dan analis data pabrik):
     - Tanpa otomatisasi, sekitar 30–50% komentar pada sesi *Pull Request Code Review* habis hanya untuk memperdebatkan hal-hal superfisial (seperti spasi sebelum tanda kurung, baris terlalu panjang, atau penempatan tanda kutip).
     - Dengan menerapkan *pre-commit hooks* berbasis Black dan Ruff di repositori Git, seluruh perdebatan gaya kode dihilangkan sebelum kode diunggah ke peladen.
     - Tim peninjau (*reviewers*) dapat memfokuskan 100% perhatian kognitif mereka pada **substansi ilmiah**: kebenaran matematis algoritma model, efisiensi alokasi memori tensor, dan validitas agronomis data lapang.

---

## 4. Kunci Solusi Tantangan Pemrograman Berjenjang

### Solusi Tantangan 1: Pemeriksa Keabsahan Identifier Python
```python
import keyword
from typing import Any, Dict


def validasi_identifier_python(nama_variabel: str) -> Dict[str, Any]:
  """Memvalidasi apakah nama_variabel memenuhi kaidah identifier legal pada Python."""
  if not isinstance(nama_variabel, str):
    return {
        "nama": str(nama_variabel),
        "is_valid": False,
        "alasan": "Input bukan string.",
    }

  if keyword.iskeyword(nama_variabel):
    return {
        "nama": nama_variabel,
        "is_valid": False,
        "alasan": "Merupakan kata kunci resmi (Reserved Keyword).",
    }

  if not nama_variabel.isidentifier():
    if nama_variabel and nama_variabel[0].isdigit():
      alasan = "Identifier tidak boleh diawali oleh angka."
    else:
      alasan = "Mengandung karakter khusus ilegal atau spasi."
    return {"nama": nama_variabel, "is_valid": False, "alasan": alasan}

  return {
      "nama": nama_variabel,
      "is_valid": True,
      "alasan": "Identifier sah dan valid.",
  }
```

---

### Solusi Tantangan 2: Penganalisis Aliran Token Kode Sumber via Modul `tokenize`
```python
import io
import token
import tokenize
from typing import Any, Dict


def analisis_aliran_token(potongan_kode: str) -> Dict[str, Any]:
  """Mengekstraksi token leksikal dan menghitung distribusi frekuensi opcodenya."""
  stream_byte = io.BytesIO(potongan_kode.encode("utf-8"))
  frekuensi_token: Dict[str, int] = {}
  total_token = 0

  for tok in tokenize.tokenize(stream_byte.readline):
    nama_tipe = token.tok_name.get(tok.type, str(tok.type))
    if nama_tipe not in ["ENCODING", "ENDMARKER"]:
      frekuensi_token[nama_tipe] = frekuensi_token.get(nama_tipe, 0) + 1
      total_token += 1

  return {"total_token": total_token, "distribusi_token": frekuensi_token}
```

---

### Solusi Tantangan 3: Auditor Kepatuhan PEP 8 Sederhana (*Linter Checker*)
```python
from typing import Any, Dict, List, Tuple


class AuditorSintaksPEP8:
  """Linter sederhana untuk mengevaluasi kepatuhan kode Python terhadap aturan format PEP 8."""

  def __init__(self, batas_panjang_baris: int = 79) -> None:
    self.batas_panjang = batas_panjang_baris

  def audit_kode(self, kode_sumber: str) -> Dict[str, Any]:
    """Menganalisis baris kode sumber terhadap pelanggaran panjang baris, tab, dan trailing spasi."""
    baris_list = kode_sumber.splitlines()
    total_baris = len(baris_list)
    pelanggaran_panjang: List[Tuple[int, int]] = []
    pelanggaran_tab: List[int] = []
    pelanggaran_trailing_spasi: List[int] = []

    for idx, baris in enumerate(baris_list, start=1):
      # 1. Batas Panjang Baris
      if len(baris) > self.batas_panjang:
        pelanggaran_panjang.append((idx, len(baris)))

      # 2. Leading Tab
      if baris.startswith("\t") or "\t" in baris[: len(baris) - len(baris.lstrip())]:
        pelanggaran_tab.append(idx)

      # 3. Trailing Whitespace di ujung baris
      if baris.endswith(" ") or baris.endswith("\t"):
        pelanggaran_trailing_spasi.append(idx)

    total_pelanggaran = (
        len(pelanggaran_panjang)
        + len(pelanggaran_tab)
        + len(pelanggaran_trailing_spasi)
    )
    skor = max(
        0.0,
        round((1.0 - (total_pelanggaran / max(1, total_baris))) * 100.0, 1),
    )

    return {
        "total_baris": total_baris,
        "baris_melebihi_batas": pelanggaran_panjang,
        "baris_memuat_tab": pelanggaran_tab,
        "baris_trailing_spasi": pelanggaran_trailing_spasi,
        "total_pelanggaran": total_pelanggaran,
        "skor_kepatuhan_persen": skor,
    }
```

---

## 5. Rubrik Asesmen Berbasis Capaian (Outcome-Based Education / OBE)

| Kriteria Penilaian | Bobot | Skor 85 - 100 (Sangat Memuaskan) | Skor 70 - 84 (Memuaskan) | Skor 55 - 69 (Cukup) | Skor < 55 (Perlu Bimbingan) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Pemahaman Struktur Leksikal & Tokenisasi** | 25% | Mampu menguraikan mekanisme tumpukan indentasi lexer, klasifikasi token, dan resolusi bebas *dangling else* secara mendalam dan matematis. | Memahami alur tokenisasi dan peran INDENT/DEDENT, namun penjelasan teoritis tumpukan lexer masih bersifat umum. | Mengetahui Python memakai spasi bukan kurung kurawal, tetapi tidak memahami peran token dalam proses kompilasi. | Gagal membedakan antara karakter teks mentah, token leksikal, dan struktur blok program. |
| **Penerapan Standar PEP 8 & PEP 257** | 25% | Konsisten menerapkan konvensi penamaan (`snake_case`, `PascalCase`, `UPPER_CASE`), tata letak spasi, batas baris, dan docstrings format Google Style 100%. | Menerapkan konvensi penamaan dan docstrings dengan baik, namun terdapat inkonsistensi minor pada spasi operator atau baris kosong. | Docstrings tidak lengkap (hanya satu baris tanpa seksi Args/Returns) dan penamaan variabel masih campur aduk. | Mengabaikan kaidah PEP 8, kode berantakan tanpa dokumentasi dan tidak mematuhi konvensi penamaan. |
| **Rekayasa Model Perkebunan & Anotasi Tipe** | 25% | Implementasi kelas neraca air sawit mematuhi prinsip Clean Code, tipe data teranotasi penuh (PEP 484), dan kalkulasi fisik agronomis presisi. | Implementasi kalkulasi neraca air benar dan teranotasi, namun penanganan eksepsi atau batasan fisik belum optimal. | Logika neraca air berjalan namun struktur kelas monolitik dan minim anotasi tipe data. | Kode model gagal dieksekusi atau menghasilkan kalkulasi air yang menyimpang dari formula fisik. |
| **Penyelesaian Tantangan Scaffolded** | 25% | Menyelesaikan seluruh 3 tantangan mandiri dengan kode yang modular, efisien, terdokumentasi rapi, dan lolos uji 100% 0 galat. | Menyelesaikan 3 tantangan dengan benar, namun algoritma linter auditor masih menyisakan sedikit redundansi. | Menyelesaikan 1–2 tantangan awal; pembuatan auditor kepatuhan PEP 8 mengalami kendala logika. | Gagal menyelesaikan tugas tantangan praktikum yang diberikan instruktur. |
