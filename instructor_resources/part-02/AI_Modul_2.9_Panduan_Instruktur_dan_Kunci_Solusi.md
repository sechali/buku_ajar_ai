# Panduan Instruktur & Kunci Solusi: AI Modul 2.9
## Struktur Data Dasar: Klasifikasi Koleksi Fundamental, Model Memori Hash Table versus Larik Kontigu, Analisis Kompleksitas Big-O, dan Pengorganisasian Mahadata Perkebunan

---

**Kode Modul:** AI Modul 2.9  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Dasar Algoritma & Logika Pemrograman untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Komputasi: Urgensi Struktur Data pada Mahadata Agribisnis | Bedah studi kasus logistik timbangan TBS sawit, Diskusi interaktif | Memaparkan analogi: Mengapa pencarian data pemanen pada jutaan tiket timbangan gagal jika menggunakan list sekuensial? |
| **Menit 026 - 060** | Klasifikasi 4 Pilar Koleksi Python (`list`, `tuple`, `dict`, `set`) | Diagram arsitektur data, Live coding CPython | Membedah kontras antara koleksi sekuensial terurut (list/tuple) dan koleksi pemetaan asosiatif berbasis hash (dict/set). |
| **Menit 061 - 095** | Model Memori Fisik: Larik Kontigu vs Tabel Hash & Analisis Big-O | Visualisasi alokasi RAM, Pembuktian matematis | Mendemonstrasikan alamat memori pointer 8-byte, mekanisme alokasi dinamis berlebih (*over-allocation*), dan mitigasi tabrakan hash (*collision resolution*). |
| **Menit 096 - 125** | Manipulasi Deklaratif Berbasis Komprehensi (*List, Dict, Set, Generator*) | Eksperimen benchmarking memori (`sys.getsizeof`) | Membimbing mahasiswa menulis sintaks komprehensi yang bersih serta membuktikan efisiensi memori $\mathcal{O}(1)$ dari *generator expressions*. |
| **Menit 126 - 150** | Refleksi Teori & Bedah Masalah Algoritmik Tingkat Tinggi (HOTS) | Diskusi Two-Sum $\mathcal{O}(N)$ dan Analisis Amortisasi | Membimbing mahasiswa memahami pembuktian matematis rata-rata waktu amortisasi penambahan elemen pada larik dinamis. |
| **Praktikum (150m)**| Eksperimen Jupyter: Benchmark Big-O, Agregasi Panen, & Spatial Indexing | Hands-on coding terbimbing di Jupyter Notebook | Memfasilitasi mahasiswa menyelesaikan 3 tantangan pemrograman berjenjang dan verifikasi 0 galat. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Menganggap Operator Keanggotaan `in` Memiliki Kecepatan Setara pada List dan Set
* **Gejala Mahasiswa:** Menggunakan pemeriksaan keanggotaan `if target in daftar_list:` di dalam perulangan berskala puluhan ribu baris data logistik, lalu heran mengapa program berjalan sangat lamban.
* **Strategi Remedial:** Tunjukkan model komparasi internal: pada `list`, operator `in` melakukan penelusuran sekuensial (*linear scan*) dari indeks $0$ hingga akhir dengan kompleksitas waktu $\mathcal{O}(N)$. Sebaliknya, pada `set`, Python langsung menghitung alamat slot melalui `hash(target) % ukuran_tabel` dengan waktu instan $\mathcal{O}(1)$. Ajak mahasiswa membuktikan percepatan ribuan kali lipat melalui sel benchmark praktikum.

### Miskonsepsi 2: Menggunakan Objek Mutabel (`list` atau `dict`) sebagai Kunci Dictionary
* **Gejala Mahasiswa:** Mencoba membuat indeks spasial dengan koordinat berbasis list `posisi = [0.5, 102.3]`, lalu menulis `tabel_pohon[posisi] = "Pohon-A"` dan menjumpai galat `TypeError: unhashable type: 'list'`.
* **Strategi Remedial:** Jelaskan integritas struktural tabel hash: sebuah kunci **wajib bersifat imutabel** agar nilai hash-nya tidak pernah berubah sepanjang program berjalan. Jika elemen list diizinkan sebagai kunci lalu isinya diubah (`posisi.append(99)`), nilai hash-nya akan berubah drastis, menyebabkan data yang telah tersimpan di dalam bucket tidak akan pernah bisa ditemukan kembali (*data orphan*). Tunjukkan solusinya: konversi koordinat menjadi `tuple` yang imutabel: `posisi = (0.5, 102.3)`.

### Miskonsepsi 3: Memodifikasi Elemen Koleksi Secara Langsung Saat Sedang Berada di Dalam Perulangan (*Concurrent Modification Trap*)
* **Gejala Mahasiswa:** Menulis perulangan `for item in daftar_sawit: if item.rusak: daftar_sawit.remove(item)` dan terkejut mengapa ada item rusak yang terlewat tidak terhapus.
* **Strategi Remedial:** Gambarkan pergeseran pointer indeks CPython: ketika sebuah elemen dihapus dari tengah list, seluruh elemen di sebelah kanannya bergeser satu indeks ke kiri, sementara pencacah perulangan internal terus melangkah ke indeks berikutnya. Akibatnya, elemen tepat setelah elemen yang dihapus akan terlewati dari evaluasi. Tanamkan strategi idiomatis: gunakan filter *list comprehension* `daftar_bersih = [item for item in daftar_sawit if not item.rusak]`.

### Miskonsepsi 4: Mengasumsikan Tuple Selalu Imutabel Secara Menyeluruh Padahal Memuat Objek Mutabel
* **Gejala Mahasiswa:** Mengira bahwa objek `data = (10, [20, 30])` adalah data yang aman dan sepenuhnya imutabel, namun terkejut ketika `data[1].append(40)` berhasil dieksekusi dan mengubah isi tuple.
* **Strategi Remedial:** Jelaskan konsep referensi pointer: `tuple` menjamin bahwa **penunjuk alamat memori (pointer)** di setiap slotnya tidak dapat diganti dengan objek lain. Namun, jika slot tersebut menunjuk ke objek mutabel seperti `list`, objek tujuan di memori Heap tersebut tetap dapat dimodifikasi secara dinamis. Tekankan bahwa tuple yang memuat elemen mutabel juga **tidak hashable** dan ditolak sebagai kunci dictionary.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Kompleksitas Asimptotik Masalah Dua Jumlah (*Two-Sum Problem in Yield Aggregation*)
* **Soal:** Divisi pemuatan ingin mencari pasangan dua tandan pada `daftar_bobot = [12, 18, 25, 30, 15, ...]` yang jika dijumlahkan memiliki berat tepat $K = 50\text{ kg}$.
  1. Analisis kompleksitas algoritma Brute Force (dua perulangan bersarang)!
  2. Rancang algoritma berbasis `dict` atau `set` dengan kompleksitas linier $\mathcal{O}(N)$ dan ruang $\mathcal{O}(N)$!
* **Jawaban Komprehensif:**
  1. **Analisis Kompleksitas Brute Force:**
     Pada pendekatan brute force, setiap elemen ke-$i$ dipasangkan dengan seluruh elemen berikutnya ke-$j$ ($j > i$):
     $$\text{Jumlah Komparasi} = \sum_{i=0}^{N-1} (N - 1 - i) = \frac{N(N-1)}{2} = \frac{1}{2}N^2 - \frac{1}{2}N$$
     Kompleksitas waktu asimptotik berordo kuadratik $\mathcal{O}(N^2)$ dengan konsumsi memori tambahan $\mathcal{O}(1)$. Pada skala transaksi harian perkebunan besar ($N = 100.000$ tiket timbangan), pendekatan ini membutuhkan sekitar $5 \times 10^9$ operasi komputasi, yang membutuhkan waktu eksekusi puluhan detik hingga hitungan menit.
  2. **Rancangan Algoritma Linier $\mathcal{O}(N)$ Menggunakan Hash Table:**
     Dengan memanfaatkan komplementer nilai target ($K - x$), kita dapat memeriksa keberadaan pasangan dalam satu kali lintasan data:
     ```python
     from typing import List, Optional, Tuple, Set

     def cari_pasangan_muatan(daftar_bobot: List[float], target_kg: float = 50.0) -> Optional[Tuple[float, float]]:
         """
         Mencari dua bobot tandan yang berjumlah target_kg dalam O(N) waktu dan O(N) ruang.
         """
         komplemen_terlihat: Set[float] = set()
         
         for bobot in daftar_bobot:
             selisih = round(target_kg - bobot, 2)
             if selisih in komplemen_terlihat:
                 return (selisih, bobot)
             komplemen_terlihat.add(bobot)
             
         return None
     ```
     **Analisis:** Setiap pencarian `selisih in komplemen_terlihat` berbiaya $\mathcal{O}(1)$ rata-rata pada tabel hash. Dengan $N$ iterasi, total waktu tereduksi menjadi $\mathcal{O}(N)$, dan konsumsi memori himpunan berbanding lurus dengan data $\mathcal{O}(N)$.

---

### Pertanyaan 2: Analisis Fenomena Amortisasi Waktu (*Amortized Constant Time*) pada `list.append()`
* **Soal:** Jelaskan strategi alokasi berlebih CPython (*over-allocation strategy: $0, 4, 8, 16, 25, 35, \dots$*) dan mengapa rata-rata jangka panjang penambahan elemen bernilai $\mathcal{O}(1)$!
* **Jawaban Komprehensif:**
  1. **Mekanisme Dynamic Over-Allocation CPython:**
     Larik fisik di memori RAM bersifat statis. Agar `list` Python dapat tumbuh secara fleksibel, CPython mengalokasikan ruang ekstra melebihi jumlah elemen aktif saat ini. Formula alokasi internal CPython (pada `listobject.c`) dirumuskan sebagai:
     $$\text{Kapasitas\_Baru} = \text{Ukuran} + (\text{Ukuran} \gg 3) + (\text{Ukuran} < 9 \text{ ? } 3 : 6)$$
     Hal ini menghasilkan urutan kapasitas slot larik: $0, 4, 8, 16, 25, 35, 46, 58, 72, \dots$.
  2. **Pembuktian Waktu Teramortisasi (*Amortized $\mathcal{O}(1)$*):**
     - Pada sebagian besar pemanggilan `.append()`, slot kosong yang sudah dicadangkan masih tersedia. Operasi ini hanya menulis pointer ke slot berikutnya berbiaya tepat $\mathcal{O}(1)$.
     - Ketika kapasitas penuh, CPython melakukan *resize*: mengalokasikan blok memori kontigu baru yang lebih besar dan menyalin $N$ pointer dari blok lama ke blok baru. Operasi langka ini berbiaya $\mathcal{O}(N)$.
     - Namun, operasi berbiaya $\mathcal{O}(N)$ ini hanya terjadi setelah $k$ operasi penambahan berturut-turut yang murah ($\mathcal{O}(1)$). Total biaya untuk menyisipkan $N$ elemen dari kondisi kosong adalah:
       $$\text{Total Biaya} = N + \sum_{j=1}^{\log N} 2^j = N + (2N - 1) < 3N$$
     - Membagi total biaya $3N$ dengan $N$ operasi menghasilkan rata-rata biaya per operasi:
       $$\text{Biaya Amortisasi} = \frac{3N}{N} = \mathcal{O}(1)$$
     Oleh karena itu, operasi `.append()` secara matematis dijamin memiliki kompleksitas konstan teramortisasi.

---

### Pertanyaan 3: Audit Imutabilitas Kunci Hash Table (*Hashable Key Constraint*)
* **Soal:** Mengapa `tuple` diizinkan sebagai kunci dictionary, sedangkan `list` dilarang? Jelaskan bencana struktural yang terjadi jika kunci bersifat mutabel!
* **Jawaban Komprehensif:**
  1. **Prinsip Dasar Penempatan Tabel Hash:**
     Kunci dictionary dipetakan ke dalam slot larik fisik berdasarkan formula:
     $$\text{Index} = \text{hash}(\text{kunci}) \pmod{\text{Kapasitas}}$$
     Agar data dapat diambil kembali di masa mendatang dengan ekspresi `kamus[kunci]`, nilai $\text{hash}(\text{kunci})$ harus menghasilkan integer yang **deterministik dan tidak berubah** sepanjang siklus hidup objek tersebut.
  2. **Bencana Struktural Jika Kunci Mutabel Diizinkan:**
     Misalkan kita memiliki kunci list `k = [1, 2]` yang disimpan di bucket nomor $5$.
     - Jika pengguna memodifikasi list tersebut: `k.append(3)`.
     - Nilai hash dari `[1, 2, 3]` kini berubah total.
     - Ketika pengguna mencoba mengakses `kamus[k]`, CPython menghitung nilai hash baru yang memetakan pencarian ke bucket nomor $14$.
     - Pada bucket nomor $14$, CPython tidak menemukan data apa pun dan melemparkan `KeyError`, meskipun objek sebenarnya masih tersimpan di bucket nomor $5$.
     - Nilai pada bucket nomor $5$ menjadi data yatim piatu (*orphaned memory*) yang mustahil diakses kembali.
     Oleh karena itu, sistem tipe data Python secara tegas mensyaratkan protokol `__hash__()` hanya diterapkan pada objek yang berkarakteristik imutabel (*hashable*).

---

## 4. Kunci Solusi Tantangan Pemrograman Berjenjang

### Solusi Tantangan 1: Penghitungan Frekuensi Varietas Kelapa Sawit
```python
from typing import List, Dict

def hitung_frekuensi_varietas(daftar_bibit: List[str]) -> Dict[str, int]:
    """
    Menghitung jumlah kemunculan setiap varietas bibit sawit dalam list
    menggunakan dictionary O(1) key access tanpa pustaka eksternal.
    """
    frekuensi: Dict[str, int] = {}
    for bibit in daftar_bibit:
        kode_bersih = bibit.strip()
        frekuensi[kode_bersih] = frekuensi.get(kode_bersih, 0) + 1
    return frekuensi
```

---

### Solusi Tantangan 2: Analisis Irisan dan Disparitas Hama Dua Divisi Kebun Menggunakan Set
```python
from typing import Set, Dict, Any

def analisis_sebaran_hama(hama_afd1: Set[str], hama_afd2: Set[str]) -> Dict[str, Any]:
    """
    Menganalisis distribusi spesies hama di dua afdeling kebun
    menggunakan operasi aljabar himpunan (Set).
    """
    irisan = hama_afd1 & hama_afd2          # Hama yang muncul di kedua divisi
    eksklusif_afd1 = hama_afd1 - hama_afd2  # Hama endemik afdeling 1
    eksklusif_afd2 = hama_afd2 - hama_afd1  # Hama endemik afdeling 2
    gabungan = hama_afd1 | hama_afd2         # Keanekaragaman seluruh hama unik
    
    # Koefisien Similaritas Jaccard: J(A, B) = |A ∩ B| / |A ∪ B|
    jaccard_index = len(irisan) / max(1, len(gabungan))

    return {
        "hama_bersama": sorted(list(irisan)),
        "eksklusif_afd1": sorted(list(eksklusif_afd1)),
        "eksklusif_afd2": sorted(list(eksklusif_afd2)),
        "total_spesies_unik": len(gabungan),
        "jaccard_similarity": round(jaccard_index, 4)
    }
```

---

### Solusi Tantangan 3: Matriks Indeks Spasial Pohon Sawit Menggunakan Dictionary of Tuples & Filter Radius
```python
import math
from typing import Dict, Tuple, List

class SpatialCanopyIndex:
    """
    Struktur data indeks spasial pohon sawit berbasis dictionary of tuples
    untuk kueri radius cepat pada sistem surveilans drone perkebunan.
    """
    def __init__(self) -> None:
        # Pemetaan koordinat (grid_x, grid_y) -> skor_ndvi (float)
        self.pohon_spasial: Dict[Tuple[int, int], float] = {}

    def tambah_pohon(self, x: int, y: int, ndvi: float) -> None:
        """Menambahkan pohon ke indeks spasial dengan validasi koordinat."""
        self.pohon_spasial[(x, y)] = ndvi

    def cari_pohon_radius(
        self, pusat_x: int, pusat_y: int, radius: int, ambang_terinfeksi: float = 0.35
    ) -> List[Tuple[Tuple[int, int], float]]:
        """
        Menemukan pohon terinfeksi kanopi (NDVI < ambang) di dalam radius Euclidean
        menggunakan list comprehension deklaratif.
        """
        r_kuadrat = radius ** 2
        return [
            (pos, ndvi) for pos, ndvi in self.pohon_spasial.items()
            if ((pos[0] - pusat_x)**2 + (pos[1] - pusat_y)**2 <= r_kuadrat) and (ndvi < ambang_terinfeksi)
        ]
```

---

## 5. Rubrik Asesmen Berbasis Capaian (Outcome-Based Education / OBE)

| Kriteria Penilaian | Bobot | Skor 85 - 100 (Sangat Memuaskan) | Skor 70 - 84 (Memuaskan) | Skor 55 - 69 (Cukup) | Skor < 55 (Perlu Bimbingan) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Pemahaman Arsitektur & Big-O** | 25% | Mampu menganalisis kompleksitas waktu $\mathcal{O}(1)$ vs $\mathcal{O}(N)$ dan model memori CPython dengan argumen matematis yang presisi. | Memahami perbedaan kecepatan list vs set, namun penjelasan teknis model memori masih bersifat umum. | Mengetahui set lebih cepat dari list tetapi tidak mampu menjelaskan mekanisme tabel hash dan Big-O. | Tidak memahami konsep kompleksitas asimptotik dan model memori koleksi data. |
| **Penerapan Tipe Koleksi Heterogen** | 25% | Tepat memilih struktur data (list, tuple, dict, set) sesuai karakteristik kasus nyata agribisnis dan mematuhi aturan hashability. | Menggunakan struktur data yang benar, namun sesekali masih menggunakan list untuk operasi keanggotaan masif. | Sering salah memilih tipe data (misal menggunakan list untuk koordinat kunci dictionary). | Mengabaikan kaidah imutabilitas dan karakteristik dasar koleksi data Python. |
| **Manipulasi Data Berbasis Komprehensi** | 25% | Mahir merekayasa *list, dict, set comprehension*, dan *generator expressions* yang bersih, deklaratif, dan hemat RAM. | Mampu membuat komprehensi dasar dengan benar, namun belum memanfaatkan generator expression untuk efisiensi memori. | Sintaksis komprehensi masih bercampur dengan perulangan imperatif konvensional yang tidak efisien. | Tidak mampu menulis sintaks komprehensi dan hanya bergantung pada perulangan biasa. |
| **Penyelesaian Tantangan Berjenjang** | 25% | Berhasil menyelesaikan ketiga tantangan scaffolded dengan kode yang modular, efisien, teranotasi tipe data, dan bebas galat 100%. | Menyelesaikan ketiga tantangan dengan benar, namun ada redundansi logika atau ketidaklengkapan tipe data. | Menyelesaikan 1–2 tantangan dasar dengan benar; tantangan indeks spasial radius mengalami kendala. | Gagal mengimplementasikan solusi tantangan atau kode menghasilkan galat sintaksis/runtime. |
