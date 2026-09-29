"""Script to generate AI_Modul_3.5_Praktikum_Struktur_Kontrol.ipynb
Modul 3.5: Struktur Kontrol (Percabangan, Guard Clauses, match-case Python 3.10+, Iterasi, for-else)
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
    add_md(r"""# AI Modul 3.5: Praktikum Struktur Kontrol
### Alur Kendali Algoritma, Percabangan Kondisional & Guard Clauses, Structural Pattern Matching (match-case) Python 3.10+, Mekanisme Iterasi Iterator Protocol, dan Otomasi Sortasi Mutu Kelapa Sawit

---
**Program Studi**: Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian  
**Institusi**: Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Kompatibilitas**: Python 3.10+ (Fitur PEP 634/635/636 `match-case`)

---
### Capaian Pembelajaran Praktikum:
1. **Outputs**: Membangun engine sortasi tandan buah segar (TBS) sawit dengan `match-case`, skrip audit sensorik dengan `for-else`, dan simulator irigasi presisi dengan *guard clauses*.
2. **Outcomes**: Menguasai pencocokan pola struktural dekonstruksi objek, eliminasi *deeply nested conditionals*, serta efisiensi memori iterator $\mathcal{O}(1)$.
3. **Impacts**: Menyiapkan fondasi logika komputasi deterministik untuk sistem otomasi pabrik kelapa sawit (PKS) dan manajemen cerdas perkebunan presisi.""")

    # Section 1: Inisialisasi Environment & Dependensi
    add_md(r"""## 1. Inisialisasi Environment dan Dependensi
Kita memverifikasi versi Python (wajib $\ge 3.10$ untuk mendukung *structural pattern matching*) dan mengimpor modul bawaan serta pustaka visualisasi.""")

    add_code("""import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np

print(f"Versi Python: {sys.version}")
assert sys.version_info >= (3, 10), "Modul ini membutuhkan Python 3.10+ untuk fitur match-case!"
print("Status: Lingkungan komputasi siap dan mendukung Structural Pattern Matching.")""")

    # Section 2: Percabangan Kondisional & Guard Clauses Pattern
    add_md("""## 2. Percabangan Kondisional Konvensional vs Pola Klausa Penjaga (Guard Clauses)
Pada bagian ini, kita membandingkan anti-pola percabangan bersarang (*deeply nested conditionals*) dengan pola rekayasa perangkat lunak modern: **Guard Clauses Pattern** (*early return*).""")

    add_code("""# Demonstrasi 1: Evaluasi Hubung Singkat (Short-Circuit Evaluation)
class SensorTanah:
    def __init__(self, nilai_suhu: Optional[float]):
        self.suhu = nilai_suhu

    def baca_suhu(self) -> float:
        if self.suhu is None:
            raise ValueError("Sensor rusak atau belum terkalibrasi!")
        return self.suhu

# Sensor terhubung normal
sensor_normal = SensorTanah(36.5)
# Sensor belum terpasang (None)
sensor_lepas = None

# Short-circuit menjamin 'sensor.baca_suhu()' TIDAK dieksekusi jika sensor is None
def periksa_kondisi_pendingin(sensor: Optional[SensorTanah]) -> str:
    if sensor is not None and sensor.baca_suhu() > 35.0:
        return "AKTIFKAN_PENDINGIN_GREENHOUSE"
    return "PENDINGIN_STANDBY"

print(f"Status Sensor Normal : {periksa_kondisi_pendingin(sensor_normal)}")
print(f"Status Sensor Lepas  : {periksa_kondisi_pendingin(sensor_lepas)} (Terhindar dari AttributeError)")""")

    add_code("""# Demonstrasi 2: Refaktorisasi Anti-Pola Percabangan Bersarang ke Guard Clauses Pattern
@dataclass
class TiketTrukPanen:
    nomor_polisi: str
    memiliki_tiket: bool
    berat_muatan_kg: float
    sopir_terdaftar: bool
    tujuan_pks: str

# Implementasi Bersih: Guard Clauses Pattern (Flat is better than nested)
def validasi_truk_masuk_pks(truk: TiketTrukPanen) -> Tuple[bool, str]:
    # Guard 1: Validasi keberadaan tiket
    if not truk.memiliki_tiket:
        return False, "TOLAK: Truk tidak memiliki tiket timbang digital resmi"
    
    # Guard 2: Validasi berat timbangan minimal
    if truk.berat_muatan_kg <= 1000.0:
        return False, "TOLAK: Berat muatan di bawah batas minimum muatan lori (1000 kg)"
        
    # Guard 3: Validasi legalitas sopir
    if not truk.sopir_terdaftar:
        return False, "TOLAK: Sopir tidak terdaftar dalam RFID database afdeling"
        
    # Guard 4: Validasi PKS tujuan
    if truk.tujuan_pks != "PKS-INSTIPER-01":
        return False, f"TOLAK: Truk dialokasikan ke unit lain ({truk.tujuan_pks})"
        
    # Happy Path (Nominal Path) berada di kedalaman indentasi nol
    return True, "DISETUJUI: Truk dipersilakan menuju loading ramp"

# Uji coba armada truk panen
truk_a = TiketTrukPanen("AB 1234 XY", True, 4500.0, True, "PKS-INSTIPER-01")
truk_b = TiketTrukPanen("BK 5678 Z", True, 800.0, True, "PKS-INSTIPER-01")
truk_c = TiketTrukPanen("BM 9012 AA", True, 5200.0, False, "PKS-INSTIPER-01")

for t in [truk_a, truk_b, truk_c]:
    status, pesan = validasi_truk_masuk_pks(t)
    print(f"[{t.nomor_polisi}] Valid: {status:<5} -> {pesan}")""")

    # Section 3: Structural Pattern Matching (match-case) Python 3.10+
    add_md("""## 3. Structural Pattern Matching (`match-case`) pada Sortasi TBS Sawit
Python 3.10 memperkenalkan PEP 634/635/636. Di sini kita mendekonstruksi objek data secara deklaratif dengan *dataclass pattern matching*, *or-patterns*, dan *pattern guards*.""")

    add_code("""@dataclass(frozen=True)
class JanjangTBS:
    id_janjang: str
    kode_blok: str
    berat_kg: float
    fraksi: int
    persen_brondolan: float
    terdapat_sampah: bool

def evaluasi_mutu_janjang(janjang: JanjangTBS) -> Dict[str, Any]:
    \"\"\"Klasifikasi fraksi TBS menggunakan Structural Pattern Matching.\"\"\"
    match janjang:
        # Pola 1: Kontaminasi sampah/gagang panjang (Prioritas Tertinggi)
        case JanjangTBS(terdapat_sampah=True):
            kategori = "REJECT_KONTAMINASI"
            faktor_harga = 0.0
            catatan = "Janjang terkontaminasi batu/pasir/gagang panjang berlebih"
            
        # Pola 2: Buah Sangat Mentah (Fraksi 0 dengan brondolan < 12.5%)
        case JanjangTBS(fraksi=0, persen_brondolan=b) if b < 12.5:
            kategori = "PENALTI_MENTAH"
            faktor_harga = 0.50
            catatan = "Buah mentah (Fraksi 0). Rendemen minyak sangat rendah"
            
        # Pola 3: Buah Matang Optimal (Fraksi 1, 2, atau 3 dengan brondolan 12.5 - 75%)
        case JanjangTBS(fraksi=f, persen_brondolan=b) if f in (1, 2, 3) and 12.5 <= b <= 75.0:
            kategori = "MUTU_PRIMA_OPTIMAL"
            faktor_harga = 1.00
            catatan = "Kematangan optimal. Rendemen CPO maksimal dan ALB < 2%"
            
        # Pola 4: Or-Pattern untuk Fraksi 4 (Lewat Matang) dan Fraksi 5 (Busuk)
        case JanjangTBS(fraksi=4 | 5):
            kategori = "PENALTI_LEWAT_MATANG"
            faktor_harga = 0.70
            catatan = "Buah lewat matang/busuk. Risiko asam lemak bebas (ALB) tinggi"
            
        # Pola 5: Wildcard Fallback untuk data inkonsisten
        case _:
            kategori = "DATA_ANOMALI"
            faktor_harga = 0.0
            catatan = "Kombinasi parameter fisik janjang di luar spesifikasi teknis"

    return {
        "id_janjang": janjang.id_janjang,
        "blok": janjang.kode_blok,
        "kategori": kategori,
        "faktor_harga": faktor_harga,
        "catatan": catatan
    }

# Uji coba pemilahan beberapa janjang
sampel_janjang = [
    JanjangTBS("JJG-01", "BLOK-A01", 24.0, fraksi=2, persen_brondolan=35.0, terdapat_sampah=False),
    JanjangTBS("JJG-02", "BLOK-A01", 18.5, fraksi=0, persen_brondolan=5.0, terdapat_sampah=False),
    JanjangTBS("JJG-03", "BLOK-B02", 22.0, fraksi=4, persen_brondolan=80.0, terdapat_sampah=False),
    JanjangTBS("JJG-04", "BLOK-C01", 26.0, fraksi=2, persen_brondolan=40.0, terdapat_sampah=True),
]

for j in sampel_janjang:
    res = evaluasi_mutu_janjang(j)
    print(f"Janjang {res['id_janjang']} -> Mutu: {res['kategori']:<20} | Faktor: {res['faktor_harga']:.2f}")""")

    # Section 4: Perulangan dan Protokol Iterator CPython
    add_md(r"""## 4. Mekanisme Iterasi, Protokol Iterator, dan Efisiensi Memori range()
Kita membuktikan secara empiris protokol iterator CPython (`__iter__`, `__next__`), konsumsi memori konstan $\mathcal{O}(1)$ dari fungsi `range()`, serta fungsi pembantu `enumerate()` dan `zip()`.""")

    add_code("""# Demonstrasi Iterator Protocol secara Eksplisit
panen_harian = ["Blok-A1", "Blok-A2", "Blok-B1"]

# 1. Dapatkan iterator dari koleksi list
iterator_panen = iter(panen_harian)
print(f"Tipe objek iterator: {type(iterator_panen)}")

# 2. Ambil elemen satu per satu via next()
print("Elemen 1:", next(iterator_panen))
print("Elemen 2:", next(iterator_panen))
print("Elemen 3:", next(iterator_panen))

# 3. Pemanggilan berikutnya akan memicu StopIteration
try:
    next(iterator_panen)
except StopIteration:
    print("StopIteration tertangkap! Iterator telah habis.")""")

    add_code("""# Pembuktian Efisiensi Memori O(1) pada range() Python 3
import sys

range_kecil = range(10)
range_sedang = range(1_000_000)
range_raksasa = range(1_000_000_000_000)

print(f"Jejak memori range(10)               : {sys.getsizeof(range_kecil)} byte")
print(f"Jejak memori range(1.000.000)        : {sys.getsizeof(range_sedang)} byte")
print(f"Jejak memori range(1.000.000.000.000): {sys.getsizeof(range_raksasa)} byte")

# Bandingkan dengan alokasi list nyata
list_seratus_ribu = list(range(100_000))
print(f"Jejak memori list nyata 100.000 int   : {sys.getsizeof(list_seratus_ribu):,} byte (~{sys.getsizeof(list_seratus_ribu)/(1024*1024):.2f} MB)")""")

    add_code("""# Penggunaan enumerate() dan zip() Idiomatis
blok_kebun = ["Blok-A01", "Blok-A02", "Blok-B01", "Blok-B02"]
target_tonase = [45.0, 52.5, 38.0, 60.0]
realisasi_tonase = [44.2, 54.0, 32.5, 61.2]

print("REKAPITULASI CAPAIAN PANEN PER BLOK:")
print("-" * 65)
for i, (blok, target, realisasi) in enumerate(zip(blok_kebun, target_tonase, realisasi_tonase), start=1):
    capaian_pct = (realisasi / target) * 100.0
    status = "TERCAPAI" if capaian_pct >= 100.0 else "DEFISIT"
    print(f"[{i:02d}] {blok:<10} | Target: {target:4.1f} ton | Realisasi: {realisasi:4.1f} ton | {capaian_pct:5.1f}% [{status}]")""")

    # Section 5: Implementasi Pipeline Industri & for-else Semantics
    add_md("""## 5. Implementasi Pipeline Otomasi Industri & Pola for-else
Di bawah ini kita mengintegrasikan seluruh konsep ke dalam pipeline kelas `EngineSortasiSawit` lengkap dengan visualisasi distribusi mutu dan penggunaan semantik klausa `for-else`.""")

    add_code("""class EngineSortasiSawit:
    \"\"\"Mesin klasifikasi mutu panen sawit berbasis Structural Pattern Matching
    dan algoritma pengawasan anomali batch panen PKS.
    \"\"\"
    def __init__(self, nama_pks: str = "PKS-INSTIPER-01") -> None:
        self.nama_pks: str = nama_pks

    def audit_inspeksi_batch(self, daftar_janjang: List[JanjangTBS]) -> Dict[str, Any]:
        total_berat = 0.0
        cacah_kategori: Dict[str, int] = {
            "MUTU_PRIMA_OPTIMAL": 0,
            "PENALTI_MENTAH": 0,
            "PENALTI_LEWAT_MATANG": 0,
            "REJECT_KONTAMINASI": 0,
            "DATA_ANOMALI": 0
        }
        tandan_ditolak: List[str] = []
        bobot_per_kategori: Dict[str, float] = {k: 0.0 for k in cacah_kategori}

        print("=== MEMULAI AUDIT PEMINDAIAN BAN BERJALAN PKS ===")
        for no_urut, janjang in enumerate(daftar_janjang, start=1):
            hasil = evaluasi_mutu_janjang(janjang)
            kat = hasil["kategori"]
            cacah_kategori[kat] = cacah_kategori.get(kat, 0) + 1
            bobot_per_kategori[kat] = bobot_per_kategori.get(kat, 0.0) + janjang.berat_kg
            total_berat += janjang.berat_kg

            if hasil["faktor_harga"] < 1.0:
                tandan_ditolak.append(janjang.id_janjang)

            print(f"[{no_urut:02d}] Janjang {janjang.id_janjang:<8} | Blok: {janjang.kode_blok:<8} | "
                  f"Fraksi: {janjang.fraksi} | Mutu: {kat:<20} | Bobot: {janjang.berat_kg:4.1f} kg")

        # Implementasi Algoritma Deteksi Batch via Pola for-else
        # Memeriksa apakah ada janjang anomali ekstrim (> 45 kg)
        for janjang in daftar_janjang:
            if janjang.berat_kg > 45.0:
                print(f"\\n[PERINGATAN KRITIS] Anomali terdeteksi pada {janjang.id_janjang} ({janjang.berat_kg} kg)! "
                      f"Muatan diinterupsi.")
                status_batch = "BATCH_DITAHAN_UNTUK_AUDIT"
                break
        else:
            # Dieksekusi HANYA jika loop selesai tanpa break
            print("\\n[VERIFIKASI SUKSES] Seluruh janjang berada dalam rentang bobot wajar pabrik.")
            status_batch = "BATCH_LOLOS_PENGOLAHAN_STERILIZER"

        rasio_prima = (cacah_kategori["MUTU_PRIMA_OPTIMAL"] / len(daftar_janjang)) * 100.0 if daftar_janjang else 0.0

        return {
            "total_janjang": len(daftar_janjang),
            "total_berat_kg": round(total_berat, 2),
            "cacah_kategori": cacah_kategori,
            "bobot_per_kategori": bobot_per_kategori,
            "rasio_prima_persen": round(rasio_prima, 2),
            "janjang_berpenalti": tandan_ditolak,
            "status_batch": status_batch
        }

# Jalankan pengujian pada simulasi batch panen
muatan_lori = [
    JanjangTBS("JJG-001", "BLOK-A01", 24.5, fraksi=2, persen_brondolan=35.0, terdapat_sampah=False),
    JanjangTBS("JJG-002", "BLOK-A01", 28.0, fraksi=0, persen_brondolan=5.0, terdapat_sampah=False),
    JanjangTBS("JJG-003", "BLOK-B02", 22.0, fraksi=3, persen_brondolan=60.0, terdapat_sampah=False),
    JanjangTBS("JJG-004", "BLOK-B01", 19.5, fraksi=5, persen_brondolan=95.0, terdapat_sampah=False),
    JanjangTBS("JJG-005", "BLOK-A02", 26.0, fraksi=2, persen_brondolan=40.0, terdapat_sampah=True),
    JanjangTBS("JJG-006", "BLOK-A01", 25.5, fraksi=2, persen_brondolan=30.0, terdapat_sampah=False),
    JanjangTBS("JJG-007", "BLOK-C03", 21.0, fraksi=1, persen_brondolan=20.0, terdapat_sampah=False),
    JanjangTBS("JJG-008", "BLOK-C01", 23.5, fraksi=2, persen_brondolan=45.0, terdapat_sampah=False),
]

engine = EngineSortasiSawit()
laporan = engine.audit_inspeksi_batch(muatan_lori)

print("\\n" + "=" * 60)
print(f"Total Janjang    : {laporan['total_janjang']}")
print(f"Total Berat (kg) : {laporan['total_berat_kg']} kg")
print(f"Rasio Prima CPO  : {laporan['rasio_prima_persen']}%")
print(f"Status Alur PKS  : {laporan['status_batch']}")
print("=" * 60)""")

    add_code("""# Visualisasi Distribusi Mutu TBS dan Proporsi Bobot Panen
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Bar chart cacah janjang per kategori mutu
kategori_labels = [k.replace('_', ' ') for k in laporan["cacah_kategori"].keys()]
kategori_counts = list(laporan["cacah_kategori"].values())
warna = ['#2ca02c', '#d62728', '#ff7f0e', '#7f7f7f', '#9467bd']

ax1.bar(kategori_labels, kategori_counts, color=warna, edgecolor='black', alpha=0.85)
ax1.set_title("Distribusi Jumlah Janjang per Kategori Mutu", fontsize=12, fontweight='bold')
ax1.set_ylabel("Jumlah Janjang")
ax1.set_xticks(range(len(kategori_labels)))
ax1.set_xticklabels(kategori_labels, rotation=25, ha='right', fontsize=9)
ax1.grid(axis='y', linestyle='--', alpha=0.5)

for i, count in enumerate(kategori_counts):
    ax1.text(i, count + 0.1, str(count), ha='center', va='bottom', fontweight='bold')

# Subplot 2: Pie chart proporsi bobot panen (kg)
labels_pie = []
values_pie = []
warna_pie = []
for k, v in laporan["bobot_per_kategori"].items():
    if v > 0:
        labels_pie.append(k.replace('_', ' '))
        values_pie.append(v)
        warna_pie.append(warna[list(laporan["bobot_per_kategori"].keys()).index(k)])

ax2.pie(values_pie, labels=labels_pie, autopct='%1.1f%%', colors=warna_pie, startangle=140,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1})
ax2.set_title(f"Proporsi Bobot Panen (Total: {laporan['total_berat_kg']} kg)", fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()""")

    # Section 6: Solusi Tantangan Mandiri Berjenjang (Scaffolded Challenges)
    add_md("""## 6. Solusi Tantangan Mandiri Berjenjang (Scaffolded Challenges)

### Tantangan 1 (Dasar): Pengklasifikasi Fraksi TBS Menggunakan match-case
Membangun fungsi `klasifikasi_fraksi_tbs(fraksi: int, brondol_pct: float) -> Tuple[str, float]` yang mengembalikan status mutu dan persentase diskon.""")

    add_code("""def klasifikasi_fraksi_tbs(fraksi: int, brondol_pct: float) -> Tuple[str, float]:
    \"\"\"Mengklasifikasikan fraksi TBS ke dalam status mutu dan persentase penalti harga.
    
    Args:
        fraksi: Nomor kode fraksi kematangan (0 s/d 5).
        brondol_pct: Persentase brondolan lepas (0 - 100%).
        
    Returns:
        Tuple[str, float]: (status_mutu, diskon_persen)
    \"\"\"
    match fraksi:
        case 0:
            return ("Mentah", 50.0)
        case 1:
            return ("Mengkal", 15.0)
        case 2 | 3:
            return ("Matang Prima", 0.0)
        case 4:
            return ("Lewat Matang", 25.0)
        case 5:
            return ("Busuk", 75.0)
        case _:
            return ("Anomali", 100.0)

# Verifikasi Solusi Tantangan 1
kasus_uji_fraksi = [
    (0, 5.0),
    (1, 15.0),
    (2, 35.0),
    (3, 65.0),
    (4, 85.0),
    (5, 95.0),
    (99, 0.0)
]

print("HASIL PENGUJIAN TANTANGAN 1:")
for f, b in kasus_uji_fraksi:
    mutu, diskon = klasifikasi_fraksi_tbs(f, b)
    print(f"Fraksi {f:2d} (Brondol: {b:4.1f}%) -> Status: {mutu:<15} | Diskon: {diskon:5.1f}%")""")

    add_md("""### Tantangan 2 (Menengah): Deteksi Anomali Aliran Sensorik via Pola for-else
Membangun fungsi `cari_anomali_telemetri(daftar_tekanan: List[float], ambang_batas: float = 3.5) -> Dict[str, Any]` menggunakan `for-else` untuk menemukan lonjakan tekanan (*pressure spike*).""")

    add_code("""def cari_anomali_telemetri(daftar_tekanan: List[float], ambang_batas: float = 3.5) -> Dict[str, Any]:
    \"\"\"Mendeteksi keberadaan anomali tekanan pipa irigasi menggunakan pola for-else.
    
    Args:
        daftar_tekanan: Daftar deret waktu pembacaan sensor tekanan (bar).
        ambang_batas: Batas aman maksimum tekanan operasi (bar).
        
    Returns:
        Dict[str, Any]: Laporan status stabilitas jaringan pipa.
    \"\"\"
    for indeks, tekanan in enumerate(daftar_tekanan):
        if tekanan > ambang_batas:
            # Anomali ditemukan, hentikan pencarian segera
            return {
                "status_jaringan": "BAHAYA_LONJAKAN_TEKANAN",
                "indeks_anomali": indeks,
                "nilai_tekanan_bar": tekanan,
                "ambang_batas": ambang_batas,
                "tindakan": f"Segera buka katup pembuang darurat di sensor titik #{indeks}"
            }
    else:
        # Dieksekusi jika seluruh elemen diperiksa tanpa melanggar ambang batas
        return {
            "status_jaringan": "STABIL_NORMAL",
            "indeks_anomali": None,
            "nilai_tekanan_bar": max(daftar_tekanan) if daftar_tekanan else 0.0,
            "ambang_batas": ambang_batas,
            "tindakan": "Pertahankan laju alir pompa normal"
        }

# Kasus Uji 1: Aliran data mengandung lonjakan tekanan
telemetri_bocor = [2.1, 2.3, 2.2, 4.8, 2.0]
hasil_uji_1 = cari_anomali_telemetri(telemetri_bocor, 3.5)
print("Uji 1 (Lonjakan Tekanan):")
print(f"  Status   : {hasil_uji_1['status_jaringan']}")
print(f"  Titik #{hasil_uji_1['indeks_anomali']} : {hasil_uji_1['nilai_tekanan_bar']} bar -> {hasil_uji_1['tindakan']}")

# Kasus Uji 2: Aliran data stabil normal
telemetri_stabil = [2.1, 2.2, 2.4, 2.3, 2.2, 2.5]
hasil_uji_2 = cari_anomali_telemetri(telemetri_stabil, 3.5)
print("\\nUji 2 (Normal):")
print(f"  Status   : {hasil_uji_2['status_jaringan']}")
print(f"  Puncak   : {hasil_uji_2['nilai_tekanan_bar']} bar -> {hasil_uji_2['tindakan']}")""")

    add_md("""### Tantangan 3 (Mahir): Simulator Irigasi Presisi Multi-Blok Berbasis Guard Clauses
Mengonstruksi kelas `SimulatorIrigasiPresisi` dengan metode evaluasi blok berbasis *guard clauses* dan visualisasi status aktuator tiap blok kebun.""")

    add_code("""class SimulatorIrigasiPresisi:
    \"\"\"Sistem otomasi fertigasi cerdas kebun kelapa sawit multi-blok.\"\"\"
    
    def __init__(self, ambang_kelembaban_min: float = 60.0) -> None:
        self.ambang_kelembaban_min = ambang_kelembaban_min

    def evaluasi_blok(self, data_blok: Dict[str, Any]) -> str:
        \"\"\"Menerapkan Guard Clauses Pattern untuk menentukan aktivasi katup irigasi.
        
        Aturan Prioritas Pengambilan Keputusan:
        1. Guard 1: Sensor mati/offline -> SKIP_SENSOR_RUSAK
        2. Guard 2: Sedang dalam siklus pemupukan -> HOLD_JADWAL_PUPUK
        3. Guard 3: Kelembaban tanah masih mencukupi (>= 60%) -> HOLD_TANAH_LEMBAB
        4. Nominal Path: Seluruh syarat lolos -> AKTIFKAN_KATUP_IRIGASI
        \"\"\"
        # Guard 1: Validasi status operasional sensor telemetri
        if not data_blok.get("sensor_aktif", False):
            return "SKIP_SENSOR_RUSAK"

        # Guard 2: Hindari pencucian pupuk (leaching) jika sedang pemupukan
        if data_blok.get("sedang_pupuk", False):
            return "HOLD_JADWAL_PUPUK"

        # Guard 3: Efisiensi air - cek kecukupan kadar lengas tanah
        if data_blok.get("kelembaban", 0.0) >= self.ambang_kelembaban_min:
            return "HOLD_TANAH_LEMBAB"

        # Happy Path / Nominal Path
        return "AKTIFKAN_KATUP_IRIGASI"

    def jalankan_inspeksi_kebun(self, kumpulan_blok: List[Dict[str, Any]]) -> Dict[str, Any]:
        \"\"\"Melakukan iterasi audit terhadap seluruh blok kebun binaan.\"\"\"
        keputusan_blok: Dict[str, str] = {}
        katup_aktif: List[str] = []

        for blok in kumpulan_blok:
            id_b = blok["id_blok"]
            aksi = self.evaluasi_blok(blok)
            keputusan_blok[id_b] = aksi
            if aksi == "AKTIFKAN_KATUP_IRIGASI":
                katup_aktif.append(id_b)

        return {
            "total_blok_diperiksa": len(kumpulan_blok),
            "blok_teririgasi": katup_aktif,
            "rasio_aktivasi_persen": round((len(katup_aktif) / len(kumpulan_blok)) * 100.0, 2) if kumpulan_blok else 0.0,
            "rincian_keputusan": keputusan_blok
        }

# Data telemetri 8 blok kebun kelapa sawit
data_lahan_sawit = [
    {"id_blok": "Blok-01", "sensor_aktif": True,  "kelembaban": 45.2, "sedang_pupuk": False},
    {"id_blok": "Blok-02", "sensor_aktif": True,  "kelembaban": 68.0, "sedang_pupuk": False},
    {"id_blok": "Blok-03", "sensor_aktif": False, "kelembaban": 35.0, "sedang_pupuk": False},
    {"id_blok": "Blok-04", "sensor_aktif": True,  "kelembaban": 42.0, "sedang_pupuk": True},
    {"id_blok": "Blok-05", "sensor_aktif": True,  "kelembaban": 55.4, "sedang_pupuk": False},
    {"id_blok": "Blok-06", "sensor_aktif": True,  "kelembaban": 72.1, "sedang_pupuk": False},
    {"id_blok": "Blok-07", "sensor_aktif": True,  "kelembaban": 38.9, "sedang_pupuk": False},
    {"id_blok": "Blok-08", "sensor_aktif": True,  "kelembaban": 49.0, "sedang_pupuk": False},
]

simulator = SimulatorIrigasiPresisi(ambang_kelembaban_min=60.0)
laporan_irigasi = simulator.jalankan_inspeksi_kebun(data_lahan_sawit)

print("HASIL AUDIT SIMULATOR IRIGASI PRESISI:")
print(f"Total Blok Diperiksa : {laporan_irigasi['total_blok_diperiksa']}")
print(f"Blok Katup Aktif     : {laporan_irigasi['blok_teririgasi']}")
print(f"Rasio Irigasi Aktif  : {laporan_irigasi['rasio_aktivasi_persen']}%\\n")

for b_id, aksi in laporan_irigasi["rincian_keputusan"].items():
    print(f"  {b_id:<8} -> Keputusan: {aksi}")""")

    add_code("""# Visualisasi Status Operasional Irigasi Multi-Blok
blok_ids = [b["id_blok"] for b in data_lahan_sawit]
kelembaban_vals = [b["kelembaban"] for b in data_lahan_sawit]
keputusan_vals = [laporan_irigasi["rincian_keputusan"][b_id] for b_id in blok_ids]

warna_map = {
    "AKTIFKAN_KATUP_IRIGASI": "#1f77b4",  # Biru
    "HOLD_TANAH_LEMBAB": "#2ca02c",       # Hijau
    "HOLD_JADWAL_PUPUK": "#ff7f0e",       # Oranye
    "SKIP_SENSOR_RUSAK": "#d62728"        # Merah
}
bar_colors = [warna_map[k] for k in keputusan_vals]

plt.figure(figsize=(12, 5))
bars = plt.bar(blok_ids, kelembaban_vals, color=bar_colors, edgecolor='black', alpha=0.85)
plt.axhline(60.0, color='red', linestyle='--', linewidth=1.5, label='Ambang Batas Kelembaban Cukup (60%)')

plt.title("Status Sensor Kelembaban Tanah dan Keputusan Aktuator Irigasi", fontsize=12, fontweight='bold')
plt.xlabel("ID Blok Perkebunan Sawit", fontsize=10)
plt.ylabel("Kelembaban Tanah (%)", fontsize=10)
plt.ylim(0, 100)

# Tambahkan label keputusan di atas bar
for bar, b_id, k in zip(bars, blok_ids, keputusan_vals):
    y_pos = bar.get_height()
    label_singkat = k.replace("AKTIFKAN_KATUP_IRIGASI", "IRIGASI ON").replace("HOLD_TANAH_LEMBAB", "LEMBAB").replace("HOLD_JADWAL_PUPUK", "PUPUK").replace("SKIP_SENSOR_RUSAK", "RUSAK")
    plt.text(bar.get_x() + bar.get_width()/2, y_pos + 2, label_singkat, ha='center', va='bottom', fontsize=8, fontweight='bold')

# Custom Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#1f77b4', edgecolor='black', label='Irigasi Aktif (<60%)'),
    Patch(facecolor='#2ca02c', edgecolor='black', label='Tanah Cukup Lembab (>=60%)'),
    Patch(facecolor='#ff7f0e', edgecolor='black', label='Sedang Dipupuk (Hold)'),
    Patch(facecolor='#d62728', edgecolor='black', label='Sensor Rusak/Offline'),
]
plt.legend(handles=legend_elements, loc='upper right')
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

    # Output path
    output_path = r"e:\Project Buku\notebooks\part-03\AI_Modul_3.5_Praktikum_Struktur_Kontrol.ipynb"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Berhasil membuat notebook di: {output_path}")

if __name__ == "__main__":
    create_notebook()
