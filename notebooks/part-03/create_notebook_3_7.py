"""Script to generate AI_Modul_3.7_Praktikum_Struktur_Data_Lanjut.ipynb
Modul 3.7: Struktur Data Lanjut (List, Tuple, Dict, Set, collections, Comprehensions)
"""
import json
import os

def create_notebook():
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    def add_md(source):
        nb["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source.split("\n")]
        })

    def add_code(source):
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source.split("\n")]
        })

    # Header
    add_md(r"""# AI Modul 3.7: Praktikum Struktur Data Lanjut
### Arsitektur Memori Larik Dinamis (List) vs Imutabilitas Tuple, Mekanisme Hash Table Kompak (PEP 468) Dictionary & Set, Salinan Dangkal vs Mendalam, Komprehensi Tingkat Lanjut, dan Struktur Performa Tinggi collections

---
**Program Studi**: Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian  
**Institusi**: Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Kompatibilitas**: Python 3.10+ (Standar PEP 468, PEP 484)

---
### Capaian Pembelajaran Praktikum:
1. **Outputs**: Membangun engine manajemen sensus tanaman dengan `namedtuple` dan `dict`, buffer lori PKS dengan `collections.deque`, serta agregasi spasial via *Dict/Set Comprehensions*.
2. **Outcomes**: Menganalisis secara empiris kompleksitas waktu $\mathcal{O}(1)$ vs $\mathcal{O}(n)$, memverifikasi pertumbuhan alokasi berlebih (*over-allocation*) list, serta mengeliminasi bug mutabilitas (*aliasing & shallow copy*).
3. **Impacts**: Menjamin skalabilitas sistem kecerdasan buatan perkebunan dalam memproses jutaan titik koordinat pohon dan antrean pabrik tanpa kegagalan memori.""")

    # Section 1: Inisialisasi Environment & Dependensi
    add_md(r"""## 1. Inisialisasi Environment dan Dependensi
Kita mengimpor pustaka standar untuk audit memori dan performa (`sys`, `time`, `copy`, `collections`), pustaka komputasi numerik (`numpy`), dan modul visualisasi (`matplotlib.pyplot`).""")

    add_code("""from collections import Counter, defaultdict, deque, namedtuple
import copy
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple
import matplotlib.pyplot as plt
import numpy as np

print(f"Versi Python: {sys.version}")
print("Status: Lingkungan komputasi siap untuk analisis struktur data lanjut.")""")

    # Section 2: Eksperimen Memori & Over-allocation List vs Tuple
    add_md(r"""## 2. Eksperimen Jejak Memori & Pola Pertumbuhan Larik Dinamis CPython
Pada bagian ini, kita melacak bagaimana CPython menambah ukuran alokasi memori fisik (`allocated`) saat list bertambah elemen, membuktikan pola *over-allocation* dan mengomparasikannya dengan `tuple`.""")

    add_code("""# Eksperimen 1: Pelacakan Over-allocation List CPython
larik_uji: List[int] = []
ukuran_tercatat: List[int] = []
jumlah_elemen = 30

print("Pertumbuhan Ukuran Objek List CPython (PyListObject):")
print("-" * 55)
print("Elemen ke- | Kapasitas Elemen | Jejak Memori (Byte) | Status Perubahan")
print("-" * 55)

ukuran_sebelumnya = sys.getsizeof(larik_uji)
for i in range(jumlah_elemen):
    larik_uji.append(i)
    ukuran_sekarang = sys.getsizeof(larik_uji)
    ukuran_tercatat.append(ukuran_sekarang)
    status = "REALLOC (Kapasitas Bertambah!)" if ukuran_sekarang != ukuran_sebelumnya else "Slot Tersedia"
    if ukuran_sekarang != ukuran_sebelumnya or i < 5:
        print(f"  {i+1:02d}       |       {len(larik_uji):02d}         |       {ukuran_sekarang:3d} byte     | {status}")
    ukuran_sebelumnya = ukuran_sekarang""")

    add_code("""# Eksperimen 2: Komparasi Jejak Memori List vs Tuple
data_angka = list(range(1000))
tuple_angka = tuple(data_angka)

memori_list = sys.getsizeof(data_angka)
memori_tuple = sys.getsizeof(tuple_angka)
penghematan_pct = ((memori_list - memori_tuple) / memori_list) * 100.0

print(f"Jejak Memori List  (1000 int): {memori_list:,} byte")
print(f"Jejak Memori Tuple (1000 int): {memori_tuple:,} byte")
print(f"Efisiensi Ruang Tuple         : {penghematan_pct:.2f}% lebih hemat memori!")""")

    # Section 3: Benchmark Kecepatan Akses: List vs Set (O(n) vs O(1))
    add_md(r"""## 3. Benchmark Empiris Kecepatan Pencarian: List vs Set ($\mathcal{O}(n)$ vs $\mathcal{O}(1)$)
Kita membuktikan perbedaan kinerja pencarian keanggotaan `in` antara pencarian sekuensial pada `list` dan pencarian berbasis *Hash Table* pada `set`.""")

    add_code("""# Pembuatan data skala 100.000 pokok sawit
N = 100_000
daftar_id_list = [f"POKOK-SAWIT-{i:06d}" for i in range(N)]
himpunan_id_set = set(daftar_id_list)

kunci_uji = "POKOK-SAWIT-099999"  # Berada di posisi paling akhir (Kasus Terburuk List)

# 1. Benchmark Pencarian pada List (O(n))
t_awal = time.perf_counter()
ada_di_list = kunci_uji in daftar_id_list
t_akhir = time.perf_counter()
durasi_list_us = (t_akhir - t_awal) * 1_000_000.0

# 2. Benchmark Pencarian pada Set (O(1))
t_awal = time.perf_counter()
ada_di_set = kunci_uji in himpunan_id_set
t_akhir = time.perf_counter()
durasi_set_us = (t_akhir - t_awal) * 1_000_000.0

print(f"Waktu Pencarian List O(n): {durasi_list_us:9.2f} mikrodetik")
print(f"Waktu Pencarian Set  O(1): {durasi_set_us:9.2f} mikrodetik")
print(f"Faktor Akselerasi Hash   : {durasi_list_us / durasi_set_us:.1f}x LEBIH CEPAT!")""")

    # Section 4: Audit Mutabilitas, Aliasing, dan Salinan Memori
    add_md(r"""## 4. Audit Mutabilitas: Aliasing Trap, Shallow Copy, dan Deep Copy
Kita membuktikan secara eksperimental bahaya penugasan referensi (*aliasing*) dan perbedaan salinan dangkal (*shallow copy*) versus salinan mendalam (*deep copy*) pada struktur bersarang.""")

    add_code("""# Demonstrasi Aliasing vs Shallow Copy vs Deep Copy
sensus_awal = [
    {"id": "P-01", "riwayat_pupuk": [15, 20]},
    {"id": "P-02", "riwayat_pupuk": [18, 22]}
]

# 1. Salinan Dangkal (Shallow Copy)
salinan_dangkal = sensus_awal.copy()

# 2. Salinan Mendalam (Deep Copy)
salinan_mendalam = copy.deepcopy(sensus_awal)

# Modifikasi pada data anak bersarang di salinan dangkal
salinan_dangkal[0]["riwayat_pupuk"].append(999)

print("HASIL AUDIT MUTABILITAS SETELAH MEMODIFIKASI SALINAN DANGKAL:")
print(f"  Data Asli             -> P-01 Pupuk: {sensus_awal[0]['riwayat_pupuk']} (IKUT TERCEMAR!)")
print(f"  Salinan Dangkal       -> P-01 Pupuk: {salinan_dangkal[0]['riwayat_pupuk']}")
print(f"  Salinan Mendalam (Aman)-> P-01 Pupuk: {salinan_mendalam[0]['riwayat_pupuk']} (TERISOLASI SEMPURNA)")""")

    # Section 5: Komprehensi Mutakhir & Generator Expression
    add_md(r"""## 5. Komprehensi Mutakhir (*Comprehensions*) dan Generator Expressions
Di bawah ini kita membandingkan List, Dict, dan Set Comprehension serta membuktikan jejak memori $\mathcal{O}(1)$ dari *Generator Expression*.""")

    add_code("""# Sampel data sensus kesehatan kanopi tanaman
sensus_pokok = [
    {"id": "P-01", "varietas": "Tenera", "ndvi": 0.82, "alb": 1.2},
    {"id": "P-02", "varietas": "Dura",   "ndvi": 0.45, "alb": 4.1},
    {"id": "P-03", "varietas": "Tenera", "ndvi": 0.78, "alb": 1.5},
    {"id": "P-04", "varietas": "Pisifera","ndvi": 0.35, "alb": 5.2},
    {"id": "P-05", "varietas": "Tenera", "ndvi": 0.88, "alb": 0.9},
]

# 1. List Comprehension: Filter pokok kanopi sehat
pokok_sehat = [p["id"] for p in sensus_pokok if p["ndvi"] >= 0.70]
print(f"List Comprehension (Pokok Sehat) : {pokok_sehat}")

# 2. Dict Comprehension: Pemetaan ID -> Status Kebugaran
peta_kebugaran = {p["id"]: ("OPTIMAL" if p["ndvi"] >= 0.70 else "STRES") for p in sensus_pokok}
print(f"Dict Comprehension (Peta Status) : {peta_kebugaran}")

# 3. Set Comprehension: Ekstraksi varietas unik tanpa duplikasi
varietas_kebun = {p["varietas"] for p in sensus_pokok}
print(f"Set Comprehension  (Varietas)    : {varietas_kebun}")

# 4. Generator Expression vs List Comprehension Memory
jutaan_iterasi = 5_000_000
gen_exp = (x * 2 for x in range(jutaan_iterasi))
print(f"\\nJejak Memori Generator Expression (5 juta data): {sys.getsizeof(gen_exp)} byte (Konstan O(1)!)")""")

    # Section 6: Struktur Data Berperforma Tinggi collections
    add_md(r"""## 6. Struktur Data Spesifik Industri: Modul collections
Kita mendemonstrasikan keunggulan `namedtuple` (hemat RAM), `deque` (antrean FIFO $\mathcal{O}(1)$), `Counter` (agregasi otomatis), dan `defaultdict` (pengelompokan data).""")

    add_code("""# Demonstrasi 1: namedtuple (Ringan dan Berlabel)
PokokKompak = namedtuple("PokokKompak", ["id_pokok", "blok", "ndvi", "varietas"])
p1 = PokokKompak("P-101", "BLOK-A", 0.84, "Tenera")
print(f"Namedtuple: {p1.id_pokok} di {p1.blok}, NDVI={p1.ndvi} (Akses atribut intuitif)")
print(f"Jejak Memori namedtuple: {sys.getsizeof(p1)} byte vs Dict standar: {sys.getsizeof({'id_pokok': 'P-101', 'blok': 'BLOK-A', 'ndvi': 0.84, 'varietas': 'Tenera'})} byte")

# Demonstrasi 2: collections.deque (Antrean Lori Pabrik)
antrean_lori = deque(maxlen=3)
antrean_lori.append("Lori-1")
antrean_lori.append("Lori-2")
antrean_lori.append("Lori-3")
print(f"\\nIsi Buffer Lori: {list(antrean_lori)}")
antrean_lori.append("Lori-4")  # Lori-1 tergeser otomatis karena maxlen=3
print(f"Setelah Lori-4 Masuk: {list(antrean_lori)} (Lori-1 keluar dari ujung kiri secara otomatis)")

# Demonstrasi 3: collections.Counter (Statistik Penyakit Kebun)
sampel_penyakit = ["Ulat Api", "Ganoderma", "Ulat Api", "Bercak Daun", "Ulat Api", "Ganoderma"]
cacah_hama = Counter(sampel_penyakit)
print(f"\\nStatistik Hama via Counter : {dict(cacah_hama)}")
print(f"Hama Paling Parah          : {cacah_hama.most_common(1)[0]}")

# Demonstrasi 4: collections.defaultdict (Pengelompokan Otomatis)
panen_afdeling = [("AFD-1", 4.2), ("AFD-2", 5.1), ("AFD-1", 3.8), ("AFD-3", 6.0), ("AFD-2", 4.5)]
rekap_blok = defaultdict(list)
for afd, ton in panen_afdeling:
    rekap_blok[afd].append(ton)
print(f"\\nRekap Afdeling via defaultdict: {dict(rekap_blok)}")""")

    # Section 7: Kasus Nyata: Pipeline Manajemen Sensus & Antrean Lori PKS
    add_md(r"""## 7. Implementasi Kasus Nyata: Pipeline Manajemen Sensus & Antrean Lori PKS
Di bawah ini kita mengintegrasikan seluruh konsep ke dalam pipeline terpadu `ManajemenSensusKebun` dan `PengendaliLoadingRampPKS` serta memvisualisasikan dinamika antrean lori.""")

    add_code("""# Inisialisasi Engine Sensus dan Buffer Pabrik
LoriTBS = namedtuple("LoriTBS", ["id_lori", "afdeling", "berat_kg", "fraksi"])

antrean_pks = deque(maxlen=4)
log_antrean_masuk: List[int] = []
waktu_simulasi = list(range(1, 9))

# Simulasi kedatangan dan pemrosesan lori TBS
muatan_masuk = [
    LoriTBS("L-01", "AFD-A", 3800, 2),
    LoriTBS("L-02", "AFD-A", 4100, 3),
    LoriTBS("L-03", "AFD-B", 3900, 2),
    LoriTBS("L-04", "AFD-B", 4200, 2),
    LoriTBS("L-05", "AFD-C", 4000, 1),
    LoriTBS("L-06", "AFD-C", 4300, 2),
    LoriTBS("L-07", "AFD-A", 3950, 2),
    LoriTBS("L-08", "AFD-B", 4050, 3),
]

print("SIMULASI DINAMIKA BUFFER ANTREAN LORI PKS:")
print("-" * 60)
for step, lori in enumerate(muatan_masuk, start=1):
    # Setiap 2 siklus, 1 lori dialirkan ke sterilizer
    if step % 2 == 0 and len(antrean_pks) > 0:
        selesai = antrean_pks.popleft()
        print(f"[Waktu {step:02d}] Lori {selesai.id_lori} SELESAI diproses ke sterilizer.")
        
    antrean_pks.append(lori)
    log_antrean_masuk.append(len(antrean_pks))
    print(f"[Waktu {step:02d}] Lori {lori.id_lori} MASUK buffer. Buffer terisi: {len(antrean_pks)}/{antrean_pks.maxlen}")""")

    add_code("""# Visualisasi Dinamika Kapasitas Buffer Antrean Lori PKS
plt.figure(figsize=(10, 4.5))
plt.plot(waktu_simulasi, log_antrean_masuk, marker='o', color='#2563eb', linewidth=2.5, label='Jumlah Lori dalam Buffer')
plt.axhline(4, color='#dc2626', linestyle='--', linewidth=1.5, label='Kapasitas Maksimum Buffer (4 Lori)')

plt.title("Dinamika Okupansi Buffer Loading Ramp PKS Sawit (collections.deque)", fontsize=12, fontweight='bold')
plt.xlabel("Langkah Waktu Operasional (Time-Step)", fontsize=10)
plt.ylabel("Jumlah Lori dalam Antrean", fontsize=10)
plt.ylim(0, 5)
plt.xticks(waktu_simulasi)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()""")

    # Section 8: Solusi Tantangan Mandiri Berjenjang
    add_md(r"""## 8. Solusi Tantangan Mandiri Berjenjang (Scaffolded Challenges)

### Tantangan 1 (Dasar): Pemfilteran Data Telemetri dengan Dict Comprehension
Membangun fungsi `filter_afdeling_kritis(data_suhu: Dict[str, float], ambang_batas: float = 33.0) -> Dict[str, float]` menggunakan Dict Comprehension.""")

    add_code("""def filter_afdeling_kritis(data_suhu: Dict[str, float], ambang_batas: float = 33.0) -> Dict[str, float]:
    \"\"\"Menyaring afdeling dengan suhu melampaui batas menggunakan Dict Comprehension.
    
    Args:
        data_suhu: Pemetaan ID afdeling ke suhu tanah (°C).
        ambang_batas: Batas toleransi panas tanah (default: 33.0°C).
        
    Returns:
        Dict[str, float]: Afdeling kritis dengan nilai suhu dibulatkan 1 desimal.
    \"\"\"
    return {afd: round(suhu, 1) for afd, suhu in data_suhu.items() if suhu > ambang_batas}

# Uji Coba Tantangan 1
data_suhu_lapangan = {"AFD-1": 29.54, "AFD-2": 35.21, "AFD-3": 28.10, "AFD-4": 36.85, "AFD-5": 32.90}
afdeling_waspada = filter_afdeling_kritis(data_suhu_lapangan, 33.0)
print("HASIL FILTER DICT COMPREHENSION TANTANGAN 1:")
for afd, suhu in afdeling_waspada.items():
    print(f"  {afd} -> Suhu Kritis: {suhu}°C")""")

    add_md(r"""### Tantangan 2 (Menengah): Deteksi Duplikasi Sensorik via Operasi Set Aljabar
Membangun fungsi `analisis_rekonsiliasi_drone(set_alpha: Set[Tuple[int, int]], set_beta: Set[Tuple[int, int]]) -> Dict[str, Any]` menggunakan operasi himpunan.""")

    add_code("""def analisis_rekonsiliasi_drone(
    set_alpha: Set[Tuple[int, int]], 
    set_beta: Set[Tuple[int, int]]
) -> Dict[str, Any]:
    \"\"\"Melakukan rekonsiliasi spasial hasil pemindaian dua drone menggunakan aljabar Set.
    
    Args:
        set_alpha: Himpunan koordinat (baris, pohon) dari Drone Alpha.
        set_beta: Himpunan koordinat (baris, pohon) dari Drone Beta.
        
    Returns:
        Dict[str, Any]: Laporan irisan, selisih, gabungan, dan beda simetris.
    \"\"\"
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

# Uji Coba Tantangan 2
temuan_drone_a = {(1, 4), (1, 5), (2, 10), (3, 12)}
temuan_drone_b = {(1, 5), (2, 10), (3, 15), (4, 8)}

laporan_rekonsiliasi = analisis_rekonsiliasi_drone(temuan_drone_a, temuan_drone_b)
print("HASIL OPERASI SET ALJABAR TANTANGAN 2:")
print(f"  Pohon Terkonfirmasi Bersama : {laporan_rekonsiliasi['terkonfirmasi_kedua']}")
print(f"  Pohon Hanya di Drone Alpha  : {laporan_rekonsiliasi['hanya_alpha']}")
print(f"  Total Gabungan Unik         : {laporan_rekonsiliasi['total_gabungan']}")
print(f"  Persentase Kesepakatan      : {laporan_rekonsiliasi['persentase_kesepakatan']}%")""")

    add_md(r"""### Tantangan 3 (Mahir): Pipa Agregasi Spasial Multi-Tingkat Menggunakan collections
Membangun kelas `RekapitulasiPanenSpasial` berbasis `defaultdict(lambda: defaultdict(list))`.""")

    add_code("""class RekapitulasiPanenSpasial:
    \"\"\"Pipa agregasi spasial bertingkat: Afdeling -> Mandor -> Data Tonase.\"\"\"
    
    def __init__(self) -> None:
        # defaultdict bertingkat dua
        self.data_hirarki: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))

    def catat_tiket_panen(self, id_afdeling: str, nama_mandor: str, tonase_truk: float) -> None:
        \"\"\"Menambahkan rekaman panen tanpa risiko KeyError.\"\"\"
        self.data_hirarki[id_afdeling][nama_mandor].append(tonase_truk)

    def hitung_ringkasan(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        \"\"\"Menghasilkan ringkasan total tonase dan rata-rata tonase per mandor.\"\"\"
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

# Uji Coba Tantangan 3
engine_rekap = RekapitulasiPanenSpasial()
engine_rekap.catat_tiket_panen("AFD-01", "Mandor Joko", 8.2)
engine_rekap.catat_tiket_panen("AFD-01", "Mandor Joko", 7.9)
engine_rekap.catat_tiket_panen("AFD-01", "Mandor Siti", 9.1)
engine_rekap.catat_tiket_panen("AFD-02", "Mandor Agus", 6.8)
engine_rekap.catat_tiket_panen("AFD-02", "Mandor Agus", 7.4)

ringkasan_panen = engine_rekap.hitung_ringkasan()
print("HASIL AGREGASI SPASIAL BERTINGKAT TANTANGAN 3:")
for afd, mandor_dict in ringkasan_panen.items():
    print(f"[{afd}]")
    for mandor, metrik in mandor_dict.items():
        print(f"  {mandor:<12}: Total={metrik['total_ton']:4.1f} ton | Rata={metrik['rata_ton_per_truk']:4.1f} ton/truk ({metrik['ritase']} rit)")""")

    # Output path
    output_path = r"e:\Project Buku\notebooks\part-03\AI_Modul_3.7_Praktikum_Struktur_Data_Lanjut.ipynb"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Berhasil membuat notebook di: {output_path}")

if __name__ == "__main__":
    create_notebook()
