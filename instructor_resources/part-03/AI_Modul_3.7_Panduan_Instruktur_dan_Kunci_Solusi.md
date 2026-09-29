# Panduan Instruktur & Kunci Solusi: AI Modul 3.7
## Struktur Data Lanjut: Arsitektur Memori Larik Dinamis (List) vs Imutabilitas Tuple, Mekanisme Hash Table Kompak (PEP 468) Dictionary & Set, Salinan Dangkal vs Mendalam, Komprehensi Tingkat Lanjut, dan Struktur Performa Tinggi collections

---

**Kode Modul:** AI Modul 3.7  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Pemrograman Python Dasar untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Komputasi: Mengapa Struktur Data Menentukan Kecepatan AI? | Simulasi perbandingan pencarian ID pokok sawit di 100.000 data | Menggugah mahasiswa: Mengapa pencarian pada `set` selesai dalam 1 mikrodetik sementara pada `list` butuh 1.000 mikrodetik? |
| **Menit 026 - 060** | Arsitektur Memori: Larik Dinamis `list` vs Struktur Kompak `tuple` | Bedah diagram memori Heap, audit pola alokasi berlebih (*over-allocation*) | Membedah ilusi array: Mengapa `list` membutuhkan alokasi cadangan dan mengapa `tuple` jauh lebih efisien untuk data statis. |
| **Menit 061 - 095** | Terobosan Tabel Hash CPython: Compact Dict (PEP 468) & Himpunan `set` | Diagram pemisahan Sparse Indices dan Dense Entries, pembuktian O(1) | Menjelaskan bagaimana Python 3.6+ memangkas 40% memori kamus dan menjamin keterurutan data (*insertion order*). |
| **Menit 096 - 125** | Kekeliruan Mutabilitas: Aliasing, Shallow Copy vs Deep Copy, & collections | Live coding pencemaran data bersarang, eksplorasi `deque` dan `Counter` | Membimbing mahasiswa merekayasa antrean lori sterilizer bebas bottleneck $\mathcal{O}(1)$ via `collections.deque`. |
| **Menit 126 - 150** | Refleksi Teori & Bedah Soal HOTS: Hash Collision, Lost Key Bug, & RAM | Pembahasan interaktif soal analitis, analisis memori Generator vs List | Menuntun mahasiswa menyusun argumen teoretis dan justifikasi rekayasa perangkat lunak skala enterprise. |
| **Praktikum (150m)**| Eksperimen Jupyter: Benchmark List vs Set, Buffer Lori PKS, & Agregasi | Praktikum komputasi terpandu di Jupyter Notebook | Memfasilitasi mahasiswa menyelesaikan 3 tantangan mandiri dengan verifikasi 100% bebas galat sintaksis. |

---

## 2. Miskonsepsi Umum Mahasiswa & Panduan Remedial

### Miskonsepsi 1: Menggunakan `list` Standar untuk Mengimplementasikan Antrean FIFO (*First-In, First-Out*)
* **Gejala Mahasiswa:** Menggunakan `list.append()` untuk antrean masuk lori TBS dan `list.pop(0)` untuk mengeluarkan lori yang selesai direbus. Mahasiswa heran mengapa sistem melambat drastis saat antrean mencapai ribuan lori.
* **Strategi Remedial:** Jelaskan arsitektur memori CPython: `list` adalah array pointer contiguous. Ketika `pop(0)` dipanggil, CPython harus menggeser seluruh $n-1$ pointer elemen lainnya satu per satu ke kiri di memori RAM, menghasilkan kompleksitas waktu **$\mathcal{O}(n)$ linier yang sangat lambat**. Tunjukkan solusinya: gunakan **`collections.deque`** yang dirancang sebagai senarai berantai ganda terblokir (*doubly linked list of blocks*), menjamin operasi `popleft()` dan `append()` berjalan dalam waktu instan **$\mathcal{O}(1)$ konstan**.

### Miskonsepsi 2: Mengira Operator Slicing `[:]` atau `.copy()` Menghasilkan Salinan Data yang Aman pada Struktur Bersarang
* **Gejala Mahasiswa:** Melakukan penyalinan data sensus kebun yang berisi list koordinat pupuk menggunakan `data_baru = data_lama.copy()`. Saat memodifikasi list pupuk di `data_baru`, data asli di `data_lama` ikut berubah secara misterius.
* **Strategi Remedial:** Gambarkan diagram memori pointer. Tunjukkan bahwa `.copy()` atau `[:]` adalah **Salinan Dangkal (*Shallow Copy*)**: ia hanya menduplikasi kontainer terluar, sementara objek anak di dalamnya tetap menunjuk ke alamat memori fisik yang sama (*shared memory reference*). Tanamkan aturan baku: jika struktur data memiliki kedalaman bersarang $\ge 2$, selalu gunakan **`copy.deepcopy()`** untuk menghasilkan klon data independen sejati.

### Miskonsepsi 3: Mengira Dictionary Python Tidak Memiliki Urutan Data (*Unordered*)
* **Gejala Mahasiswa:** Mahasiswa yang belajar dari buku teks Python versi lama (Python 2 atau $\le 3.5$) meyakini bahwa iterasi kamus bersifat acak dan tidak dapat diprediksi.
* **Strategi Remedial:** Demonstrasikan arsitektur **Compact Dict (PEP 468)** yang diadopsi sejak Python 3.6+. Tunjukkan bahwa entri disimpan berurutan di dalam *Dense Entries Array*, sehingga urutan iterasi `for k, v in dict.items():` dijamin **100% deterministik mengikuti kronologi waktu penyisipan (*insertion-order preservation*)**.

### Miskonsepsi 4: Mengira Objek Mutabel Seperti `list` Dapat Dijadikan Kunci Dictionary
* **Gejala Mahasiswa:** Menulis `peta_kebun = {[baris, pohon]: "Tenera"}` dan mengalami kebingungan saat muncul pesan galat `TypeError: unhashable type: 'list'`.
* **Strategi Remedial:** Jelaskan konsep *Hash Invariance*: sebuah kunci kamus harus memiliki nilai hash yang konstan sepanjang hidupnya agar lokasinya di tabel hash dapat ditemukan kembali. Karena elemen `list` dapat diubah kapan saja (*mutabel*), nilai hash-nya akan berubah dan merusak integritas tabel hash. Tunjukkan solusinya: ubah koordinat menjadi struktur imutabel **`tuple`** `{(baris, pohon): "Tenera"}`.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Teoretis Kompleksitas Waktu & Memori: Operasi Pencarian `in` pada List vs Set
* **Soal:**
  1. Mengapa operasi `x in daftar_list` memiliki kompleksitas waktu terburuk $\mathcal{O}(n)$, sedangkan `x in himpunan_set` memiliki kompleksitas waktu rata-rata $\mathcal{O}(1)$?
  2. Apa yang terjadi pada kompleksitas waktu `set` jika seluruh $n$ elemen yang disisipkan menghasilkan nilai hash yang bertabrakan (*Hash Collision Storm*)? Bagaimana Python memitigasi serangan degradasi kompleksitas ini?
* **Jawaban Komprehensif:**
  1. **Akar Perbedaan Mekanisme Pencarian:**
     - **Pencarian Linier pada `list` ($\mathcal{O}(n)$):**  
       Objek `list` menyimpan elemen dalam urutan acak tanpa indeks pencarian. Untuk memverifikasi apakah `x` ada di dalam list, CPython harus membandingkan `x` dengan setiap elemen dari indeks $0$ hingga $n-1$ satu per satu menggunakan operator kesetaraan `__eq__()`. Jika elemen berada di ujung akhir atau tidak ada, algoritma membutuhkan tepat $n$ perbandingan.
     - **Pencarian Berbasis Hash pada `set` ($\mathcal{O}(1)$):**  
       Objek `set` mengimplementasikan tabel cincang (*Hash Table*). Alih-alih memindai seluruh elemen, CPython menghitung nilai `hash(x)` secara matematis, lalu melakukan operasi modulo bitwise `hash(x) & (mask)` untuk mendapatkan alamat slot secara langsung. CPU melompat ke alamat memori tersebut dalam waktu konstan tanpa memedulikan apakah set berisi 10 atau 10.000.000 elemen.
  2. **Fenomena Hash Collision Storm & Mitigasi CPython:**
     - Jika seluruh $n$ elemen memiliki nilai hash yang bertabrakan atau menempati slot yang sama, algoritma resolusi tabrakan (*open addressing*) terpaksa menelusuri rantai slot perturbasi berulang kali. Dalam skenario terburuk ekstrem ini, kompleksitas waktu pencarian dan penyisipan set/dict akan terdegradasi dari $\mathcal{O}(1)$ menjadi **$\mathcal{O}(n)$ linier**, melumpuhkan throughput sistem (*algorithmic complexity denial-of-service / HashDoS*).
     - **Mitigasi CPython:**  
       Sejak Python 3.3 (PEP 456), CPython mengadopsi algoritma **SipHash-2-4** yang menginjeksikan benih acak kriptografis rahasia (*randomized secret hash seed*) sebesar 128-bit pada setiap kali proses Python baru dimulai. Karena benih acak ini tidak dapat ditebak oleh penyerang eksternal, mustahil bagi pihak luar untuk merekayasa sekumpulan data kunci yang secara sengaja memicu tabrakan massal pada server kebun.

---

### Pertanyaan 2: Dekonstruksi Semantik CPython: Mengapa Kunci Dictionary Wajib Bersifat Hashable?
* **Soal:**
  1. Jelaskan hubungan logis antara metode dunder `__hash__()` dan `__eq__()` pada model objek Python! Mengapa sebuah objek mutabel dilarang keras dijadikan kunci pada dictionary?
  2. Jika sebuah objek dapat dimodifikasi setelah dimasukkan sebagai kunci dictionary, jelaskan fenomena "kunci hilang" (*Lost Key Bug*) yang akan melumpuhkan pencarian data di memori!
* **Jawaban Komprehensif:**
  1. **Kontrak Matematis Hashable (`__hash__` dan `__eq__`):**
     - Dalam spesifikasi model data Python, sebuah objek dikatakan *hashable* jika memenuhi dua syarat mutlak:
       1. Nilai kembalian dari metode `__hash__()` tidak pernah berubah sepanjang masa hidup objek tersebut (*immutable hash*).
       2. Jika dua objek dianggap sama menurut metode kesetaraan (`a == b` atau `a.__eq__(b) is True`), maka nilai hash keduanya **wajib identik** (`hash(a) == hash(b)`).
     - Objek mutabel (seperti `list` atau `dict`) memiliki isi yang dapat ditambah atau diubah sewaktu-waktu. Jika dihitung hash-nya, nilai hash tersebut harus berubah mengikuti pergeseran isi objek. Hal ini melanggar aksioma imutabilitas nilai hash, sehingga CPython secara eksplisit menyetel `__hash__ = None` pada tipe-tipe mutabel.
  2. **Fenomena "Kunci Hilang" (*Lost Key Bug*):**
     - Misalkan Python mengizinkan list `k = [1, 2]` menjadi kunci dictionary, dan `data[k] = "Sensus-A"`. CPython menghitung `hash([1, 2]) = 1050` dan menyimpan pointer nilai pada ember (*bucket*) slot 1050.
     - Kemudian kode memodifikasi list tersebut: `k.append(3)`. Nilai logika list kini menjadi `[1, 2, 3]`.
     - Ketika program mencoba membaca kembali: `nilai = data[k]`, CPython menghitung ulang nilai hash dari `[1, 2, 3]` yang kini menghasilkan `hash = 4820`. CPython kemudian memeriksa slot ember 4820 di memori dan mendapati slot tersebut kosong!
     - Interpreter melemparkan eksepsi `KeyError: [1, 2, 3]`, padahal objek fisik `k` yang sama persis masih berada di dalam kamus. Kunci tersebut menjadi "hantu" di memori yang tidak dapat ditemukan maupun dihapus (*memory leak* permanen).

---

### Pertanyaan 3: Analisis Rekayasa Memori: Trade-Off List Comprehension vs Generator Expression
* **Soal:**
  1. Dalam pemrosesan citra satelit tutupan kanopi $10.000.000$ piksel: analisislah konsekuensi komputasi antara sintaksis `[proses(px) for px in piksel]` dan `(proses(px) for px in piksel)`!
  2. Kapan seorang insinyur kecerdasan buatan wajib menggunakan List Comprehension dan kapan wajib mempertahankan Generator Expression?
* **Jawaban Komprehensif:**
  1. **Konsekuensi Alokasi Memori dan Cache CPU:**
     - **List Comprehension `[proses(px) for px in piksel]`:**  
       Mengevaluasi seluruh 10 juta piksel secara instan (*eager evaluation*) dan mengalokasikan memori fisik untuk larik 10 juta pointer di RAM:
       $$\text{Memori Pointer} \approx 10.000.000 \times 8 \text{ byte} = 80 \text{ MB} + \text{Over-allocation} \approx 115 \text{ MB RAM}$$
       Jika setiap hasil proses berupa objek skalar baru, jejak memori total dapat membengkak hingga ratusan megabyte atau gigabyte. Pada gerbang IoT tepi (*edge devices*), ini dapat memicu crash *Out of Memory*.
     - **Generator Expression `(proses(px) for px in piksel)`:**  
       Menerapkan evaluasi malas (*lazy evaluation*). Generator tidak mengalokasikan data apa pun di memori, melainkan hanya mengembalikan sebuah objek iterator berukuran tetap **konstan 208 byte** di RAM. Piksel diproses satu per satu di register CPU hanya saat fungsi konsumer (seperti `sum()` atau perulangan `for`) memintanya.
  2. **Pedoman Arsitektur Penggunaan:**
     - **Wajib Menggunakan Generator Expression jika:**
       - Aliran data berukuran masif atau deret waktu tak berhingga (*infinite streams*).
       - Data hanya perlu dilintasi satu kali (*single-pass consumption*), misal untuk agregasi skalar: `rata_rata = sum(...) / n` atau pencarian elemen pertama.
       - Membangun pipeline pemrosesan berantai (*generator pipelines*) untuk meminimalkan beban bandwidth memori.
     - **Wajib Menggunakan List Comprehension jika:**
       - Data perlu diakses berulang kali secara acak berdasarkan indeks (`data[i]`).
       - Memerlukan operasi mutasi in-place seperti `.sort()`, `.reverse()`, atau `.pop()`.
       - Data perlu dilewatkan ke pustaka aljabar linier C seperti NumPy atau PyTorch yang membutuhkan memori contiguous nyata untuk vektorisasi SIMD.

---

## 4. Kunci Solusi Tantangan Praktikum (Scaffolded Challenges)

### Solusi Tantangan 1: Pemfilteran Data Telemetri dengan Dict Comprehension
```python
from typing import Dict

def filter_afdeling_kritis(data_suhu: Dict[str, float], ambang_batas: float = 33.0) -> Dict[str, float]:
    """Menyaring afdeling dengan suhu melampaui batas menggunakan Dict Comprehension.

    Args:
        data_suhu: Pemetaan ID afdeling ke suhu tanah (°C).
        ambang_batas: Batas toleransi panas tanah (default: 33.0°C).

    Returns:
        Dict[str, float]: Afdeling kritis dengan nilai suhu dibulatkan 1 desimal.
    """
    return {afd: round(suhu, 1) for afd, suhu in data_suhu.items() if suhu > ambang_batas}
```

---

### Solusi Tantangan 2: Deteksi Duplikasi Sensorik via Operasi Set Aljabar
```python
from typing import Any, Dict, Set, Tuple

def analisis_rekonsiliasi_drone(
    set_alpha: Set[Tuple[int, int]], 
    set_beta: Set[Tuple[int, int]]
) -> Dict[str, Any]:
    """Melakukan rekonsiliasi spasial hasil pemindaian dua drone menggunakan aljabar Set.

    Args:
        set_alpha: Himpunan koordinat (baris, pohon) dari Drone Alpha.
        set_beta: Himpunan koordinat (baris, pohon) dari Drone Beta.

    Returns:
        Dict[str, Any]: Laporan irisan, selisih, gabungan, dan beda simetris.
    """
    terkonfirmasi_kedua = set_alpha & set_beta            # Irisan (Intersection)
    hanya_alpha = set_alpha - set_beta                    # Selisih (Difference)
    total_gabungan = set_alpha | set_beta                 # Gabungan (Union)
    berselisih_pendapat = set_alpha ^ set_beta            # Beda Simetris (Symmetric Difference)

    return {
        "terkonfirmasi_kedua": terkonfirmasi_kedua,
        "hanya_alpha": hanya_alpha,
        "total_gabungan": total_gabungan,
        "berselisih_pendapat": berselisih_pendapat,
        "persentase_kesepakatan": round((len(terkonfirmasi_kedua) / len(total_gabungan)) * 100.0, 2) if total_gabungan else 0.0
    }
```

---

### Solusi Tantangan 3: Pipa Agregasi Spasial Multi-Tingkat Menggunakan collections
```python
from collections import defaultdict
from typing import Dict, List

class RekapitulasiPanenSpasial:
    """Pipa agregasi spasial bertingkat: Afdeling -> Mandor -> Data Tonase."""

    def __init__(self) -> None:
        # defaultdict bertingkat dua untuk mengeliminasi KeyError
        self.data_hirarki: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))

    def catat_tiket_panen(self, id_afdeling: str, nama_mandor: str, tonase_truk: float) -> None:
        """Menambahkan rekaman panen tanpa percabangan defensif manual."""
        self.data_hirarki[id_afdeling][nama_mandor].append(tonase_truk)

    def hitung_ringkasan(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Menghasilkan ringkasan total tonase dan rata-rata tonase per mandor."""
        laporan_akhir: Dict[str, Dict[str, Dict[str, float]]] = {}

        for afd, dict_mandor in self.data_hirarki.items():
            laporan_akhir[afd] = {}
            for mandor, list_ton in dict_mandor.items():
                total = sum(list_ton)
                rata = total / len(list_ton) if list_ton else 0.0
                laporan_akhir[afd][mandor] = {
                    "total_ton": round(total, 2),
                    "rata_ton_per_truk": round(rata, 2),
                    "ritase": len(list_ton)
                }
        return laporan_akhir
```

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Kriteria Penilaian | Bobot | Sangat Kurang (< 50) | Kurang (50 - 69) | Memuaskan (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Pemilihan Struktur Data & Kompleksitas Waktu** | 25% | Menggunakan `list` untuk seluruh kasus (termasuk antrean FIFO dan pencarian kunci massal). | Memahami perbedaan struktur data dasar namun keliru dalam memilih struktur khusus `collections`. | Tepat memilih `dict` dan `set` untuk pencarian $\mathcal{O}(1)$, serta `deque` untuk antrean. | Menganalisis kompleksitas komputasi secara matematis, mengoptimalkan throughput dan penggunaan memori RAM. |
| **Penguasaan Tabel Hash & Sifat Hashability** | 25% | Mencoba menggunakan objek mutabel sebagai kunci kamus dan bingung saat memicu TypeError. | Memahami kamus secara praktis namun tidak memahami prinsip Compact Dict (PEP 468) dan tabrakan hash. | Memahami syarat hashability (`__hash__` & `__eq__`) dan keunggulan deterministik insertion-order. | Menguasai arsitektur Sparse vs Dense Array, resolusi tabrakan open addressing, dan teknik mitigasi HashDoS. |
| **Penanganan Mutabilitas & Pencegahan Bug Kloning** | 25% | Terjebak dalam aliasing bug (`b = a`); memodifikasi salinan merusak data master tanpa disadari. | Menggunakan shallow copy pada data bersarang sehingga menimbulkan kebocoran referensi mutabel. | Menggunakan `copy.deepcopy()` secara tepat saat memproses struktur data pohon bersarang. | Merancang arsitektur aliran data yang mengisolasi status mutabel secara elegan dan aman (*defensive cloning*). |
| **Kualitas Perangkat Lunak, collections, & PEP 8** | 25% | Kode bertele-tele dengan nested loops manual; tanpa type hinting dan tanpa docstrings. | Menggunakan komprehensi dasar namun kurang efisien; sebagian standar PEP 8 terabaikan. | Mahir memanfaatkan `namedtuple`, `Counter`, `defaultdict`, serta Dict/Set Comprehensions rapi. | Kode memenuhi standar profesional industri: PEP 8 sempurna, PEP 484 tipe ketat, modular, dan berperforma tinggi. |

---

## 6. Rekomendasi Alur Penyampaian & Tips Pedagogis

1. **Jalankan Benchmark Kecepatan Akses Secara Langsung di Depan Mahasiswa:**  
   Buka terminal atau Jupyter Notebook interaktif. Buat list 100.000 elemen dan set 100.000 elemen. Jalankan `kunci in list` dan `kunci in set` menggunakan modul `time`. Tampilkan angka perbedaan kecepatan yang mencapai hampir **1.000 kali lipat**! Bukti empiris ini akan mengubah paradigma berpikir mahasiswa selamanya tentang pentingnya efisiensi algoritma.
2. **Visualisasikan Salinan Dangkal Menggunakan Diagram Tali Pointer:**  
   Banyak mahasiswa kesulitan membedakan salinan pointer dan salinan nilai fisik. Gambarkan di papan tulis: kotak luar diduplikasi, tetapi tali penunjuk di dalam kotak tetap terikat ke barang yang sama di gudang. Mahasiswa akan langsung memahami mengapa mengubah barang di kotak B ikut merusak barang di kotak A.
3. **Kaitkan collections dengan Alur Fisik Pabrik Kelapa Sawit:**  
   Gunakan metafora nyata: `collections.deque` adalah ban berjalan lori TBS di *loading ramp*, `collections.Counter` adalah papan tulis mandor yang mencatat fraksi buah janjang, dan `collections.defaultdict` adalah loker berkas afdeling yang otomatis membuka folder baru saat truk dari afdeling baru tiba.
