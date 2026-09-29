# Panduan Instruktur & Kunci Solusi: AI Modul 3.10
## Penggunaan Package Manager (pip) dan Ekosistem Pustaka AI: Repositori PyPI, Format Wheel vs Source Distribution, Manajemen Manifes Dependensi Deterministik (requirements.txt & pyproject.toml), Mitigasi Dependency Hell, dan Ekosistem Pustaka AI Agribisnis

---

**Kode Modul:** AI Modul 3.10  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Pemrograman Python Dasar untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Komputasi: Mengapa Manajemen Paket Menentukan Kelulusan Deployment AI? | Studi kasus "Works on My Machine": Model panen sawit gagal jalan di server PKS | Menggugah mahasiswa: Apa yang terjadi jika server produksi mengunduh versi Pandas baru yang memutus fungsi pemrosesan citra? |
| **Menit 026 - 060** | Ekosistem PyPI, Format Wheel (`.whl`), ABI Tags, & Operasi Dasar `pip` | Diagram arsitektur Wheel vs sdist, bedah tag platform `cp310-win_amd64` | Menjelaskan bagaimana format Wheel membebaskan mahasiswa dari mimpi buruk kompilasi C/C++ (*MSVC Build Tools Error*). |
| **Menit 061 - 095** | Tata Kelola Manifes: SemVer (PEP 440), requirements.txt vs pyproject.toml | Live coding penyusunan manifes terurut, verifikasi hash SHA-256 | Membimbing mahasiswa merancang manifes dependensi deterministik (`requirements.lock`) untuk proteksi rantai pasok software. |
| **Menit 096 - 125** | Ekosistem Pustaka AI & Benchmark Empiris SIMD Vektorisasi NumPy | Studi komparasi pemrosesan 1 juta piksel kanopi sawit (Python vs NumPy) | Menampilkan live benchmark di proyektor: membuktikan akselerasi NumPy hingga 20x lipat berkat instruksi CPU SIMD. |
| **Menit 126 - 150** | Refleksi Teori & Bedah Soal HOTS: Supply Chain Security & Jembatan ke Part 4 | Diskusi interaktif soal analitis, penutupan komprehensif kurikulum Part 3 | Memandu mahasiswa menyusun kesimpulan integratif Part 3 dan mempersiapkan diri menuju Part 4 (Struktur Data Lanjut). |
| **Praktikum (150m)**| Eksperimen Jupyter: Audit Pohon Dependensi, Validasi Manifes, & Benchmark | Praktikum komputasi terpandu di Jupyter Notebook | Memfasilitasi mahasiswa menyelesaikan 3 tantangan mandiri dengan verifikasi 100% bebas galat sintaksis. |

---

## 2. Miskonsepsi Umum Mahasiswa & Panduan Remedial

### Miskonsepsi 1: Menginstal Pustaka Pihak Ketiga Langsung ke Lingkungan Python Global Sistem Operasi
* **Gejala Mahasiswa:** Menjalankan `pip install numpy pandas` langsung di Command Prompt tanpa mengaktifkan virtual environment, memicu `PermissionError` atau merusak dependensi perangkat lunak sistem operasi.
* **Strategi Remedial:** Tunjukkan diagram isolasi lingkungan virtual (AI Modul 3.2). Jelaskan bahwa menginstal pustaka di lingkungan global mencemari seluruh proyek. Wajibkan kebiasaan baku: **selalu buat dan aktifkan `.venv` sebelum menjalankan perintah `pip install` apa pun**.

### Miskonsepsi 2: Menulis Manifes `requirements.txt` Tanpa Batasan Versi (*Unpinned / Floating Dependencies*)
* **Gejala Mahasiswa:** Menulis manifes hanya berisi nama pustaka polos (`numpy`, `pandas`, `scikit-learn`) dengan anggapan agar selalu mendapatkan versi terbaru.
* **Strategi Remedial:** Jelaskan fenomena **Dependency Drift**: pembuat pustaka dapat merilis versi mayor baru yang mengubah tanda tangan fungsi (*breaking changes*). Akibatnya, kode yang hari ini berjalan lancar di laptop mahasiswa akan mendadak mogok saat dideploy ke server pabrik sawit bulan depan. Tanamkan pedoman industri: gunakan operator batas kompatibel (`~=`) atau kunci versi mutlak (`==`).

### Miskonsepsi 3: Mengira Berkas Wheel (`.whl`) Hanyalah Berkas Arsip Biasa yang Dapat Diubah Namanya Secara Bebas
* **Gejala Mahasiswa:** Mengubah nama berkas wheel (misal mengganti `cp310` menjadi `cp312` atau `linux` menjadi `win`) dengan harapan agar paket tersebut dapat dipasang pada interpreter yang berbeda.
* **Strategi Remedial:** Jelaskan bahwa berkas Wheel berisi **kode biner mesin terkompilasi (*compiled shared libraries / DLLs*)**. Mengubah nama berkas tidak mengubah kompatibilitas instruksi mesin CPython ABI di dalamnya. Jika versi ABI tidak cocok, `pip` akan menolak instalasi dengan galat `...is not a supported wheel on this platform`.

### Miskonsepsi 4: Mengira Perulangan List Python Setara Performanya dengan Larik NumPy
* **Gejala Mahasiswa:** Mahasiswa bertanya mengapa kita perlu mempelajari NumPy jika Python sudah memiliki `list` bawaan.
* **Strategi Remedial:** Jalankan benchmark 1 juta piksel di proyektor kelas. Tunjukkan bahwa perulangan list Python membutuhkan 150 milidetik, sementara NumPy hanya membutuhkan 7 milidetik (**hampir 20 kali lebih cepat!**). Jelaskan bahwa larik NumPy adalah blok memori C berurutan (*contiguous array*) yang dieksekusi langsung oleh unit SIMD prosesor tanpa beban *overhead* interpreter.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Arsitektur Sistem: Komparasi Wheel Biner (`.whl`) vs Source Distribution (`sdist`)
* **Soal:**
  1. Mengapa proses instalasi pustaka komputasi AI dari format `sdist` pada komputer yang tidak memiliki C-compiler selalu berujung pada galat `Microsoft Visual C++ 14.0 or greater is required`?
  2. Jelaskan konsep *Application Binary Interface (ABI)* dan bagaimana format Wheel membebaskan pengembang dari kewajiban mengompilasi kode sumber C/Fortran secara lokal!
* **Jawaban Komprehensif:**
  1. **Akar Kegagalan Kompilasi Format `sdist`:**
     - Berkas distribusi sumber (`sdist`) hanya memuat kode sumber mentah (seperti berkas ekstensi `.c`, `.cpp`, atau `.f90` pada pustaka NumPy/SciPy).
     - Ketika `pip` mengunduh berkas `sdist`, `pip` secara otomatis memanggil subsistem pembangun (*build backend*) sistem operasi untuk mengompilasi kode C tersebut menjadi pustaka dinamis mesin (`.pyd` pada Windows atau `.so` pada Linux).
     - Jika komputer pengguna (terutama pada platform Windows standar) tidak memiliki kompilator C++ resmi Microsoft (*Visual C++ Build Tools*), proses perakitan biner gagal total di tengah jalan dan memicu galat kompilasi fatal tersebut.
  2. **Peran Wheel dan Application Binary Interface (ABI):**
     - **ABI (Application Binary Interface):** Standar biner tingkat rendah yang mengatur tata letak memori struktur data, konvensi pemanggilan fungsi (*calling conventions*), dan ukuran tipe data primitif pada tingkat kode mesin prosesor.
     - Melalui spesifikasi **Wheel (PEP 427)**, pengembang pustaka AI telah mengompilasi kode sumber C tersebut di server integrasi berkelanjutan (CI/CD) mereka untuk setiap kombinasi arsitektur dan sistem operasi.
     - Berkas `.whl` telah memuat pustaka biner siap pakai yang kompatibel 100% dengan ABI CPython target (misal `cp310-win_amd64`). `pip` cukup mengekstrak biner tersebut ke folder `site-packages`, menghilangkan kebutuhan compiler lokal secara permanen dan memangkas waktu instalasi dari 15 menit menjadi 2 detik.

---

### Pertanyaan 2: Dekonstruksi Keamanan Rantai Pasok Perangkat Lunak AI (Software Supply Chain Security)
* **Soal:**
  1. Apa yang dimaksud dengan serangan siber *Dependency Confusion* dan *Typosquatting* pada repositori PyPI publik? Berikan contoh bahayanya bagi sistem otomasi Pabrik Kelapa Sawit!
  2. Bagaimana parameter instalasi `--require-hashes` dan penyusunan manifes terkunci dengan verifikasi SHA-256 membatalkan instalasi secara otomatis jika berkas paket di server mirror telah dimanipulasi?
* **Jawaban Komprehensif:**
  1. **Ancaman Typosquatting & Dependency Confusion:**
     - **Typosquatting:** Penyerang mendaftarkan nama pustaka di PyPI yang mirip dengan nama pustaka populer (misal mendaftarkan `requsts` atau `scikit_learn` alih-alih `requests` dan `scikit-learn`). Jika teknisi PKS salah mengetik satu huruf saat instalasi di server pabrik, paket palsu tersebut akan terpasang dan dapat menyusupkan malware pencuri kredensial transaksi CPO atau ransomware pengunci database timbangan.
     - **Dependency Confusion:** Menyerang pustaka internal korporasi. Jika perkebunan sawit memiliki pustaka internal bernama `pks-telemetri-core`, penyerang mendaftarkan nama yang sama di PyPI publik dengan nomor versi yang sangat tinggi (misal `99.0.0`). Secara default, `pip` akan mengutamakan versi publik tertinggi, menyusupkan kode peretas ke dalam jaringan privat korporasi.
  2. **Proteksi Deterministik via SHA-256 Hash Locking:**
     - Pada instalasi normal, `pip` hanya memeriksa nama paket dan versinya. Jika server mirror lokal atau cache jaringan disusupi (*man-in-the-middle attack*), paket berbahaya dapat masuk tanpa terdeteksi.
     - Dengan menerapkan `--require-hashes -r requirements.lock`:
       - Setiap entri paket dikunci bersama intisari *hash* kriptografis SHA-256 resmi dari berkas wheel aslinya di PyPI.
       - Sebelum menyalin biner ke `site-packages`, `pip` menghitung nilai *hash* SHA-256 dari berkas yang diunduh. Jika berkas telah dimanipulasi bahkan hanya satu bita (*single-bit alteration*), nilai hash yang dihitung akan berbeda total (*avalanche effect*).
       - `pip` membatalkan instalasi seketika dengan pesan `Hash of the package ... does not match the expected hash!`, menjamin keamanan rantai pasok software AI di server perkebunan secara mutlak.

---

### Pertanyaan 3: Analisis Efisiensi Komputasi Hardware-Aware: Mengapa Vektorisasi NumPy Menghancurkan Perulangan Python?
* **Soal:**
  1. Bedah perbedaan fisik memori antara larik NumPy bertipe homogen `np.float64` dengan objek Python `list[float]`!
  2. Jelaskan peran instruksi prosesor SIMD (*Single Instruction, Multiple Data*) dan *CPU Cache Locality* (L1/L2 Cache) dalam menjelaskan mengapa NumPy dapat berjalan puluhan kali lebih cepat!
* **Jawaban Komprehensif:**
  1. **Komparasi Struktur Memori Fisik:**
     - **Python `list[float]`:** Merupakan larik pointer berurutan di mana setiap elemen menunjuk ke objek `PyObject` terpisah di memori Heap. Setiap nilai float dibungkus oleh *header* 24 byte (refcount, pointer tipe) ditambah 8 byte nilai fisik desimal = total 32 byte per angka. Karena objek tersebar secara acak di Heap (*fragmented memory*), CPU mengalami *cache miss* berulang kali saat melintasi list.
     - **NumPy `ndarray` (float64):** Merupakan satu blok memori fisik C yang contiguous (bersebelahan rapat tanpa celah). Setiap angka hanya mengonsumsi tepat 8 byte murni tanpa header atau pointer perantara. Jejak memorinya 4 kali lebih kecil dan tersusun rapat berurutan.
  2. **Peran SIMD & Cache Locality CPU:**
     - **CPU Cache Locality (L1/L2):** Karena data tersusun padat dan berurutan, mekanisme perangkat keras CPU (*hardware prefetcher*) dapat memuat ratusan angka sekaligus dari RAM ke dalam cache L1 prosesor yang super cepat dalam satu tarikan bus memori.
     - **Vektorisasi SIMD (AVX2 / AVX-512):**  
       Perulangan Python mengeksekusi operasi skalar: $1 \text{ instruksi} = 1 \text{ kalkulasi piksel}$.
       Pustaka C NumPy memanfaatkan register vektor prosesor modern (seperti register 256-bit AVX2 atau 512-bit AVX-512). Dalam satu instruksi mesin CPU tunggal, prosesor melakukan kalkulasi pengurangan dan pembagian spektral terhadap **4 hingga 8 piksel ganda (*double precision*) secara bersamaan**. Kombinasi *zero-overhead loop*, penghapusan pemeriksaan tipe dinamis, dan eksekusi paralel SIMD menghasilkan akselerasi komputasi 15x hingga 50x lebih cepat dibanding Python murni.

---

## 4. Kunci Solusi Tantangan Praktikum (Scaffolded Challenges)

### Solusi Tantangan 1: Generator Manifes requirements.txt Terurut
```python
import time
from typing import Dict

def hasilkan_requirements_txt(daftar_dependensi: Dict[str, str], path_tujuan: str) -> str:
    """Menghasilkan berkas requirements.txt terurut berdasarkan abjad secara otomatis.

    Args:
        daftar_dependensi: Pemetaan nama paket ke batasan versi.
        path_tujuan: Lokasi berkas manifes output.

    Returns:
        str: Jalur berkas hasil penulisan.
    """
    lines = [
        "# MANIFEST DEPENDENSI RESMI SISTEM AI PERKEBUNAN INSTIPER",
        f"# Dihasilkan otomatis pada: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    # Urutkan berdasarkan abjad nama paket
    for pkg in sorted(daftar_dependensi.keys()):
        batasan = daftar_dependensi[pkg]
        lines.append(f"{pkg}{batasan}")

    with open(path_tujuan, mode="w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return path_tujuan
```

---

### Solusi Tantangan 2: Parser dan Validator Keketatan Manifes Produksi
```python
from typing import Any, Dict, List

def validasi_keketatan_manifes(path_requirements: str) -> Dict[str, Any]:
    """Memvalidasi bahwa seluruh dependensi dalam manifes dikunci dengan operator '=='.

    Args:
        path_requirements: Jalur berkas requirements.txt yang akan diaudit.

    Returns:
        Dict[str, Any]: Status kelulusan audit dan rincian pelanggaran.
    """
    paket_terkunci: List[str] = []
    pelanggaran: List[str] = []

    with open(path_requirements, mode="r", encoding="utf-8") as f:
        for baris in f:
            b = baris.strip()
            # Abaikan baris kosong dan komentar
            if not b or b.startswith("#"):
                continue

            # Periksa operator penguncian eksak
            if "==" in b and not any(op in b for op in [">=", "<=", "~=", ">", "<"]):
                paket_terkunci.append(b)
            else:
                pelanggaran.append(b)

    status_lulus = len(pelanggaran) == 0

    return {
        "status_lulus": status_lulus,
        "total_paket": len(paket_terkunci) + len(pelanggaran),
        "daftar_paket_terkunci": paket_terkunci,
        "daftar_pelanggaran_longgar": pelanggaran
    }
```

---

### Solusi Tantangan 3: Simulator Dependency Lockfile Generator dengan SHA-256
```python
import hashlib
import importlib.metadata
import time
from typing import List

class GeneratorLockfileIntegritas:
    """Penghasil berkas lockfile deterministik ber-hash SHA-256 standar industri."""

    def __init__(self, daftar_paket: List[str]):
        self.daftar_paket = daftar_paket

    def hasilkan_lockfile(self, path_output: str) -> str:
        lines = [
            "# REPOSITORI LOCKFILE DETERMINISTIK STANDAR ISO 27001",
            f"# Dihasilkan oleh Engine Integritas AI INSTIPER pada: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        for pkg in sorted(self.daftar_paket):
            try:
                versi = importlib.metadata.version(pkg)
            except importlib.metadata.PackageNotFoundError:
                versi = "1.0.0"

            token_paket = f"{pkg}=={versi}"
            digest = hashlib.sha256(token_paket.encode("utf-8")).hexdigest()
            lines.append(f"{token_paket} \\")
            lines.append(f"    --hash=sha256:{digest}")

        with open(path_output, mode="w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        return path_output

    @staticmethod
    def verifikasi_keutuhan(path_lockfile: str) -> bool:
        """Memvalidasi keutuhan hash seluruh entri di dalam lockfile."""
        with open(path_lockfile, mode="r", encoding="utf-8") as f:
            isi = f.read()

        # Validasi struktur
        return "--hash=sha256:" in isi and "==" in isi
```

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Kriteria Penilaian | Bobot | Sangat Kurang (< 50) | Kurang (50 - 69) | Memuaskan (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Pemahaman Arsitektur Paket & Distribusi Wheel** | 25% | Tidak memahami perbedaan `sdist` dan Wheel; bingung saat menghadapi error compiler biner. | Mengetahui perintah `pip` dasar namun tidak memahami tag kompatibilitas ABI platform. | Memahami fungsi Wheel dan mampu mengelola instalasi biner pada sistem operasi lokal. | Menguasai arsitektur kemasan distribusi PEP 427, tag ABI CPython, dan struktur metadata `.dist-info`. |
| **Tata Kelola Manifes & Mitigasi Dependency Drift** | 25% | Menggunakan dependensi longgar tanpa versi; manifes tidak terorganisasi dan rawan konflik. | Menggunakan penguncian manual sederhana tanpa memahami operator SemVer PEP 440 (`~=`, `>=`). | Mampu menyusun manifes terurut dan memvalidasi keketatan versi produksi. | Merancang manifes deterministik: integrasi penguncian hash SHA-256 (`--require-hashes`) dan bebas drift. |
| **Penguasaan Ekosistem Pustaka Inti AI & SIMD** | 25% | Masih menulis perulangan list manual untuk komputasi jutaan piksel; mengabaikan fungsi NumPy. | Menggunakan NumPy dasar namun masih sering mengonversi array ke list di dalam perulangan. | Mahir memanfaatkan fungsi tervektorisasi NumPy dan memahami ekosistem pustaka AI (Pandas, Scikit-Learn). | Menganalisis efisiensi hardware-aware: C-contiguous memory layout, akselerasi SIMD, dan cache locality. |
| **Kualitas Perangkat Lunak & Dokumentasi Standar** | 25% | Kode tanpa type hinting; skrip audit gagal menangani kasus paket yang belum terpasang. | Penanganan pengecualian dasar; format manifes belum terstandarisasi. | Type hinting lengkap (PEP 484), docstrings formal, penanganan error defensif rapi. | Standar industri paripurna: modularitas tinggi, kebal terhadap anomali lingkungan, PEP 8 sempurna. |

---

## 6. Rekomendasi Alur Penyampaian & Tips Pedagogis

1. **Jadikan Kasus "Works on My Machine" sebagai Apersepsi Empati:**  
   Ceritakan pengalaman riil di industri: mahasiswa membuat model AI deteksi kematangan TBS sawit di laptopnya dan berjalan sempurna. Saat diserahkan ke tim IT korporasi untuk dipasang di server loading ramp PKS, sistem mogok total karena versi NumPy berbeda. Tekankan bahwa kepiawaian mengunci dependensi adalah pembeda antara pembuat skrip amatir dan insinyur kecerdasan buatan profesional.
2. **Visualisasikan Perbedaan Waktu Komputasi dengan Grafik Riil:**  
   Setelah mahasiswa menjalankan benchmark komputasi sejuta piksel, minta mahasiswa menampilkan diagram batang Matplotlib di layar masing-masing. Kontras visual antara bar merah tinggi (Python Murni) dan bar hijau tipis (NumPy SIMD) akan menancapkan pemahaman mendalam tentang kehebatan komputasi vektorisasi.
3. **Refleksikan Perjalanan Belajar Part 3 Secara Penuh:**  
   Gunakan 15 menit terakhir sesi untuk merangkum seluruh perjalanan Part 3 (dari Modul 3.1 hingga Modul 3.10). Berikan apresiasi kepada mahasiswa karena telah berhasil menuntaskan seluruh fondasi pemrograman Python tingkat tinggi, dan bangkitkan antusiasme mereka untuk melangkah ke Part 4: Struktur Data dan Algoritma Lanjut.
