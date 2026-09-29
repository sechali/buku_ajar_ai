"""Script to generate AI_Modul_3.6_Praktikum_Fungsi_dan_Modularisasi.ipynb
Modul 3.6: Fungsi dan Modularisasi (Positional/Keyword-Only, LEGB, Closures, Decorators, Packages)
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
    add_md(r"""# AI Modul 3.6: Praktikum Fungsi dan Modularisasi
### Dekomposisi Fungsional, Parameterisasi Lanjut (*args, **kwargs, Positional/Keyword-Only), Resolusi Ruang Lingkup LEGB, Fungsi Tingkat Tinggi & Dekorator, dan Arsitektur Paket Modular Agribisnis Presisi

---
**Program Studi**: Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian  
**Institusi**: Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Kompatibilitas**: Python 3.10+ (Standar PEP 3102, PEP 570, PEP 484)

---
### Capaian Pembelajaran Praktikum:
1. **Outputs**: Membangun modul analisis spektral kanopi sawit (NDVI/EVI) dengan parameter posisional murni (`/`) & kata kunci murni (`*`), pipeline dekorator audit telemetri, dan pabrik fungsi berbasis closure.
2. **Outcomes**: Menguasai resolusi simbol LEGB CPython, dekonstruksi bytecode `LOAD_FAST` vs `LOAD_GLOBAL`, serta rekayasa *Higher-Order Functions* berbasis `@functools.wraps`.
3. **Impacts**: Menerapkan arsitektur perangkat lunak modular skala korporasi untuk mempercepat deployment model AI visi komputer perkebunan dan IoT presisi.""")

    # Section 1: Inisialisasi Environment & Dependensi
    add_md(r"""## 1. Inisialisasi Environment dan Dependensi
Kita mengimpor pustaka standar Python untuk audit fungsi (`functools`, `time`, `dis`, `math`), pustaka komputasi numerik (`numpy`), dan modul visualisasi (`matplotlib.pyplot`).""")

    add_code("""import dis
import functools
import math
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np

print(f"Versi Python: {sys.version}")
print("Status: Lingkungan komputasi siap untuk praktikum fungsi dan modularisasi.")""")

    # Section 2: Parameterisasi Lanjut
    add_md(r"""## 2. Parameterisasi Lanjut: Positional-Only (`/`), Keyword-Only (`*`), dan Variadic (`*args`, `**kwargs`)
Pada bagian ini, kita mempraktikkan tata bahasa tanda tangan fungsi (*function signatures*) modern untuk mendesain API fungsional yang tahan salah (*foolproof*).""")

    add_code("""# Demonstrasi 1: Positional-Only Parameters (PEP 570)
# Menggunakan tanda '/' untuk menandai parameter yang DILARANG menggunakan nama kata kunci
def hitung_rasio_mesokarp(berat_mesokarp: float, berat_tandan: float, /) -> float:
    \"\"\"Menghitung persentase daging buah (mesokarp) sawit terhadap berat tandan fisik.\"\"\"
    return (berat_mesokarp / berat_tandan) * 100.0

# Pemanggilan Benar (Hanya berdasarkan urutan posisi)
rasio_1 = hitung_rasio_mesokarp(14.5, 25.0)
print(f"Rasio Mesokarp Normal: {rasio_1:.2f}%")

# Uji Coba Pelanggaran Sintaksis
try:
    # Memanggil dengan nama kata kunci akan memicu TypeError secara sengaja
    hitung_rasio_mesokarp(berat_mesokarp=14.5, berat_tandan=25.0)
except TypeError as e:
    print(f"Tertangkap TypeError (Desain API Terlindungi): {e}")""")

    add_code("""# Demonstrasi 2: Keyword-Only Parameters (PEP 3102)
# Menggunakan tanda '*' untuk menandai parameter konfigurasi yang WAJIB menyertakan nama
def konfigurasi_inferensi_drone(nama_model: str, *, resolusi_cm: float = 2.5, ambang_deteksi: float = 0.75, simpan_geotiff: bool = True) -> Dict[str, Any]:
    \"\"\"Menetapkan konfigurasi inspeksi kanopi tanpa risiko tertukar parameter boolean.\"\"\"
    return {
        "model": nama_model,
        "gsd_cm": resolusi_cm,
        "threshold": ambang_deteksi,
        "geotiff": simpan_geotiff
    }

# Pemanggilan Benar: Parameter wajib disebut namanya
konfigurasi = konfigurasi_inferensi_drone("YOLOv8-Sawit", resolusi_cm=3.0, ambang_deteksi=0.80, simpan_geotiff=True)
print("Konfigurasi Eksekusi Drone:")
for k, v in konfigurasi.items():
    print(f"  {k:<15}: {v}")""")

    add_code("""# Demonstrasi 3: Variadic Arguments (*args & **kwargs)
def agregasi_panen_multi_afdeling(*tonase_truk: float, kode_pks: str = "PKS-01", **metadata_tambahan: Any) -> Dict[str, Any]:
    \"\"\"Menerima deret bobot truk fleksibel (*args) dan atribut operasional dinamis (**kwargs).\"\"\"
    total_bobot = sum(tonase_truk)
    rata_rata = total_bobot / len(tonase_truk) if tonase_truk else 0.0
    return {
        "pks": kode_pks,
        "jumlah_truk": len(tonase_truk),
        "total_ton": round(total_bobot, 2),
        "rata_ton_per_truk": round(rata_rata, 2),
        "atribut_sistem": metadata_tambahan
    }

laporan_afdeling = agregasi_panen_multi_afdeling(
    7.5, 8.2, 6.9, 9.1, 7.8,
    kode_pks="PKS-INSTIPER-01",
    mandor="Budi Santoso",
    shift="Pagi",
    kondisi_jalan="Kering"
)
print("Laporan Agregasi Panen:")
for k, v in laporan_afdeling.items():
    print(f"  {k:<20}: {v}")""")

    # Section 3: Resolusi Ruang Lingkup LEGB & Bytecode Disassembly
    add_md(r"""## 3. Resolusi Ruang Lingkup LEGB dan Dekonstruksi Bytecode CPython
Kita menelusuri bagaimana CPython mencari simbol variabel melalui aturan LEGB (*Local $\rightarrow$ Enclosing $\rightarrow$ Global $\rightarrow$ Built-in*), serta menganalisis perbedaan instruksi bytecode `LOAD_FAST` vs `LOAD_GLOBAL`.""")

    add_code("""# Demonstrasi Resolusi Simbol CPython dan Bytecode Disassembly
konstanta_global_pks = 42.0

def fungsi_audit_lokal(nilai_sensor: float):
    # 'nilai_sensor' dialokasikan pada tabel array lokal (LOAD_FAST)
    # 'konstanta_global_pks' dicari pada tabel modul global (LOAD_GLOBAL)
    hasil = nilai_sensor + konstanta_global_pks
    return hasil

print("Disassembly Bytecode CPython untuk fungsi_audit_lokal:")
print("-" * 50)
dis.dis(fungsi_audit_lokal)""")

    add_code("""# Demonstrasi Perbedaan 'global' vs 'nonlocal'
def simulator_stasiun_pompa():
    volume_terpompa_liter = 0.0  # Enclosing scope

    def aktifkan_aliran(durasi_menit: float, debit_lpm: float = 50.0) -> float:
        nonlocal volume_terpompa_liter  # Mengikat variabel ke enclosing scope
        penambahan = durasi_menit * debit_lpm
        volume_terpompa_liter += penambahan
        return volume_terpompa_liter

    return aktifkan_aliran

pompa_blok_a = simulator_stasiun_pompa()
print(f"Siklus 1 (10 menit) : {pompa_blok_a(10.0)} liter terpompa")
print(f"Siklus 2 (15 menit) : {pompa_blok_a(15.0)} liter terpompa")
print(f"Siklus 3 (5 menit)  : {pompa_blok_a(5.0)} liter terpompa")""")

    # Section 4: Higher-Order Functions, Closures, dan Dekorator
    add_md(r"""## 4. Higher-Order Functions, Closures, dan Arsitektur Dekorator
Di bawah ini kita mengonstruksi rantai dekorator standar industri berbasis `@functools.wraps` untuk validasi rentang data fisis dan audit latensi komputasi.""")

    add_code("""# Pembangunan Dekorator Audit Waktu Komputasi (Benchmarking Decorator)
def audit_latensi(func: Callable[..., Any]) -> Callable[..., Any]:
    \"\"\"Dekorator berstandar industri dengan preservasi metadata via @functools.wraps.\"\"\"
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        t_mulai = time.perf_counter()
        hasil = func(*args, **kwargs)
        t_selesai = time.perf_counter()
        durasi_us = (t_selesai - t_mulai) * 1_000_000.0
        print(f"[AUDIT PERFORMA] '{func.__name__}' dieksekusi dalam {durasi_us:.2f} mikrodetik")
        return hasil
    return wrapper

# Dekorator Pemeriksa Validitas Domain Fisika Reflektansi [0.0, 1.0]
def validasi_pantulan_optik(func: Callable[..., float]) -> Callable[..., float]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> float:
        for i, val in enumerate(args):
            if isinstance(val, (int, float)) and not (0.0 <= val <= 1.0):
                raise ValueError(f"Anomali Fisika: Argumen #{i} bernilai {val} di luar batas optik [0.0, 1.0]")
        for k, val in kwargs.items():
            if isinstance(val, (int, float)) and not (0.0 <= val <= 1.0):
                raise ValueError(f"Anomali Fisika: Parameter '{k}' bernilai {val} di luar batas optik [0.0, 1.0]")
        return func(*args, **kwargs)
    return wrapper

@audit_latensi
@validasi_pantulan_optik
def hitung_ndvi_terdekorasi(nir: float, red: float, /) -> float:
    \"\"\"Menghitung NDVI ternormalisasi kanopi sawit.\"\"\"
    penyebut = nir + red
    return (nir - red) / penyebut if penyebut > 1e-6 else 0.0

# Uji coba fungsi terdekorasi
nilai_ndvi = hitung_ndvi_terdekorasi(0.82, 0.18)
print(f"Hasil Kalkulasi NDVI: {nilai_ndvi:.4f}")
print(f"Nama Asli Fungsi     : {hitung_ndvi_terdekorasi.__name__} (Terpelihara berkat @functools.wraps)")
print(f"Docstring Asli       : {hitung_ndvi_terdekorasi.__doc__}")""")

    # Section 5: Kasus Nyata: Pipeline Analisis Spektral Kanopi Sawit
    add_md(r"""## 5. Implementasi Kasus Nyata: Pipeline Spektroskopi dan Visualisasi Kanopi Sawit
Kita mengimplementasikan pipeline spektral lengkap: NDVI, EVI (*Enhanced Vegetation Index*), dan SAVI (*Soil-Adjusted Vegetation Index*) serta memvisualisasikan sensitivitas indeks terhadap variasi biomassa kanopi.""")

    add_code("""# Implementasi Tiga Indeks Spektral Pertanian Presisi
def hitung_savi(nir: float, red: float, /, *, faktor_l: float = 0.5) -> float:
    \"\"\"Menghitung Soil-Adjusted Vegetation Index (SAVI).
    Formula: SAVI = ((NIR - RED) / (NIR + RED + L)) * (1 + L)
    \"\"\"
    penyebut = nir + red + faktor_l
    if math.isclose(penyebut, 0.0, abs_tol=1e-6):
        return 0.0
    return ((nir - red) / penyebut) * (1.0 + faktor_l)

def hitung_evi_lengkap(nir: float, red: float, blue: float, /, *, g: float = 2.5, c1: float = 6.0, c2: float = 7.5, l: float = 1.0) -> float:
    \"\"\"Menghitung Enhanced Vegetation Index (EVI).
    Formula: EVI = G * ((NIR - RED) / (NIR + C1*RED - C2*BLUE + L))
    \"\"\"
    penyebut = nir + (c1 * red) - (c2 * blue) + l
    if math.isclose(penyebut, 0.0, abs_tol=1e-6):
        return 0.0
    return g * ((nir - red) / penyebut)

# Simulasi Profil Spektroskopi Pokok Sawit dari Fase Meranggas hingga Kanopi Rimbun
deret_nir = np.linspace(0.20, 0.85, 50)
deret_red = np.linspace(0.35, 0.08, 50)
deret_blue = np.linspace(0.25, 0.05, 50)

list_ndvi = [hitung_ndvi_terdekorasi(n, r) for n, r in zip(deret_nir, deret_red)]
list_savi = [hitung_savi(n, r, faktor_l=0.5) for n, r in zip(deret_nir, deret_red)]
list_evi = [hitung_evi_lengkap(n, r, b, g=2.5, c1=6.0, c2=7.5, l=1.0) for n, r, b in zip(deret_nir, deret_red, deret_blue)]

# Visualisasi Komparasi Respon Spektral Kanopi Sawit
plt.figure(figsize=(10, 5))
plt.plot(deret_nir, list_ndvi, label="NDVI (Standar)", color="#16a34a", linewidth=2.5)
plt.plot(deret_nir, list_savi, label="SAVI (Koreksi Efek Tanah L=0.5)", color="#ca8a04", linewidth=2.0, linestyle="--")
plt.plot(deret_nir, list_evi, label="EVI (Anti-Saturasi Biomassa Rimbun)", color="#2563eb", linewidth=2.0, linestyle="-.")

plt.title("Komparasi Sensitivitas Indeks Spektroskopi Kanopi Kelapa Sawit", fontsize=12, fontweight="bold")
plt.xlabel("Tingkat Reflektansi Near-Infrared (NIR) Kanopi", fontsize=10)
plt.ylabel("Nilai Indeks Vegetasi", fontsize=10)
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper left", frameon=True)
plt.tight_layout()
plt.show()""")

    # Section 6: Solusi Tantangan Mandiri Berjenjang
    add_md(r"""## 6. Solusi Tantangan Mandiri Berjenjang (Scaffolded Challenges)

### Tantangan 1 (Dasar): Kalkulator Pupuk NPK dengan Keyword-Only Parameters
Membangun fungsi `hitung_kebutuhan_pupuk(luas_hektar: float, /, *, dosis_urea: float = 2.0, dosis_tsp: float = 1.5, dosis_mop: float = 1.75) -> Dict[str, float]`.""")

    add_code("""def hitung_kebutuhan_pupuk(
    luas_hektar: float,
    /,
    *,
    dosis_urea: float = 2.0,
    dosis_tsp: float = 1.5,
    dosis_mop: float = 1.75
) -> Dict[str, float]:
    \"\"\"Menghitung total tonase pupuk yang dibutuhkan kebun sawit.
    
    Args:
        luas_hektar: Luas petak lahan kebun (Positional-Only, satuan ha).
        dosis_urea: Rekomendasi dosis Urea (Keyword-Only, kuintal/ha).
        dosis_tsp: Rekomendasi dosis TSP (Keyword-Only, kuintal/ha).
        dosis_mop: Rekomendasi dosis MOP (Keyword-Only, kuintal/ha).
        
    Returns:
        Dict[str, float]: Alokasi kebutuhan pupuk dalam satuan ton.
    \"\"\"
    # Konversi: (dosis kuintal/ha * luas_ha) / 10 = ton
    ton_urea = (dosis_urea * luas_hektar) / 10.0
    ton_tsp = (dosis_tsp * luas_hektar) / 10.0
    ton_mop = (dosis_mop * luas_hektar) / 10.0
    
    return {
        "luas_ha": luas_hektar,
        "kebutuhan_urea_ton": round(ton_urea, 2),
        "kebutuhan_tsp_ton": round(ton_tsp, 2),
        "kebutuhan_mop_ton": round(ton_mop, 2),
        "total_pupuk_ton": round(ton_urea + ton_tsp + ton_mop, 2)
    }

# Uji Coba Tantangan 1
kebutuhan_blok_a = hitung_kebutuhan_pupuk(120.0, dosis_urea=2.2, dosis_tsp=1.4, dosis_mop=1.8)
print("HASIL KALKULASI TANTANGAN 1:")
for k, v in kebutuhan_blok_a.items():
    print(f"  {k:<22}: {v}")""")

    add_md(r"""### Tantangan 2 (Menengah): Generator Pelacak Rata-Rata Bergerak Sinyal Suhu via Closure
Membangun fungsi tingkat tinggi `ciptakan_pelacak_suhu(ukuran_jendela: int = 5) -> Callable[[float], float]` menggunakan paradigma closure dan kata kunci `nonlocal`.""")

    add_code("""def ciptakan_pelacak_suhu(ukuran_jendela: int = 5) -> Callable[[float], float]:
    \"\"\"Pabrik fungsi berbasis closure untuk menghitung moving average telemetri suhu.
    
    Args:
        ukuran_jendela: Batas kapasitas riwayat sampel pembacaan sensor.
        
    Returns:
        Callable[[float], float]: Fungsi akumulator filter derau dinamis.
    \"\"\"
    riwayat_suhu: List[float] = []  # Enclosing scope

    def perbarui_suhu(bacaan_baru: float) -> float:
        nonlocal riwayat_suhu
        riwayat_suhu.append(bacaan_baru)
        # Pertahankan ukuran jendela maksimum
        if len(riwayat_suhu) > ukuran_jendela:
            riwayat_suhu.pop(0)
            
        rata_rata = sum(riwayat_suhu) / len(riwayat_suhu)
        return round(rata_rata, 2)

    return perbarui_suhu

# Uji Coba Tantangan 2
pelacak_greenhouse = ciptakan_pelacak_suhu(ukuran_jendela=4)
aliran_suhu_raw = [28.5, 29.0, 31.5, 33.0, 35.0, 34.2, 33.8]

print("HASIL FILTER MOVING AVERAGE TANTANGAN 2:")
print("-" * 55)
for i, suhu in enumerate(aliran_suhu_raw, start=1):
    suhu_halus = pelacak_greenhouse(suhu)
    print(f"Waktu T+{i:02d} | Suhu Sensor Raw: {suhu:4.1f}°C -> Moving Avg (W=4): {suhu_halus:4.2f}°C")""")

    add_md(r"""### Tantangan 3 (Mahir): Pipeline Dekorator Validasi Vektor dan Pengaman Eksepsi Model AI
Membangun dekorator `@validasi_vektor_spektral(panjang_wajib=4)` dan `@fallback_pada_eksepsi(nilai_default=0.0)` pada fungsi `prediksi_indeks_klorofil`.""")

    add_code("""def validasi_vektor_spektral(panjang_wajib: int = 4):
    \"\"\"Pabrik dekorator untuk memastikan panjang dan integritas numerik vektor pita drone.\"\"\"
    def dekorator(func: Callable[..., float]) -> Callable[..., float]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> float:
            if not args:
                raise ValueError("Fungsi memerlukan setidaknya satu argumen posisional berupa vektor!")
            vektor = args[0]
            if not isinstance(vektor, list) or len(vektor) != panjang_wajib:
                raise ValueError(f"Integritas Data Gagal: Vektor harus berupa list dengan panjang tepat {panjang_wajib}")
            for elem in vektor:
                if math.isnan(elem) or math.isinf(elem):
                    raise ValueError(f"Anomali Numerik: Ditemukan nilai korup (NaN/Inf) dalam vektor {vektor}")
            return func(*args, **kwargs)
        return wrapper
    return dekorator

def fallback_pada_eksepsi(nilai_default: float = 0.0):
    \"\"\"Dekorator pengaman eksepsi untuk menjamin sistem AI tidak lumpuh akibat anomali data.\"\"\"
    def dekorator(func: Callable[..., float]) -> Callable[..., float]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> float:
            try:
                return func(*args, **kwargs)
            except Exception as err:
                print(f"[FALLBACK AKTIF] Tertangkap eksepsi: {err}. Mengembalikan nilai aman: {nilai_default}")
                return nilai_default
        return wrapper
    return dekorator

# Menerapkan Kedua Dekorator pada Fungsi Inferensi Klorofil Daun
@fallback_pada_eksepsi(nilai_default=0.0)
@validasi_vektor_spektral(panjang_wajib=4)
def prediksi_indeks_klorofil(vektor_band: List[float], /) -> float:
    \"\"\"Menghitung estimasi konsentrasi klorofil daun sawit (SPAD index).\"\"\"
    # Model empiris: 45.2 * (NIR / Red) + 12.1 * (RedEdge / Green)
    nir, rededge, red, green = vektor_band[0], vektor_band[1], vektor_band[2], vektor_band[3]
    return 45.2 * (nir / red) + 12.1 * (rededge / green)

# Kasus 1: Vektor Normal (Panjang 4, Angka Valid)
vektor_valid = [0.82, 0.54, 0.15, 0.22]
hasil_1 = prediksi_indeks_klorofil(vektor_valid)
print(f"Uji 1 (Normal)   -> Estimasi Indeks Klorofil: {hasil_1:.2f} SPAD")

# Kasus 2: Vektor Korup (Panjang 3) -> Memicu Fallback Dekorator
vektor_pendek = [0.82, 0.54, 0.15]
hasil_2 = prediksi_indeks_klorofil(vektor_pendek)
print(f"Uji 2 (Pendek)   -> Output: {hasil_2}")

# Kasus 3: Vektor Korup Mengandung NaN -> Memicu Fallback Dekorator
vektor_nan = [0.82, float('nan'), 0.15, 0.22]
hasil_3 = prediksi_indeks_klorofil(vektor_nan)
print(f"Uji 3 (Ada NaN)  -> Output: {hasil_3}")""")

    # Output path
    output_path = r"e:\Project Buku\notebooks\part-03\AI_Modul_3.6_Praktikum_Fungsi_dan_Modularisasi.ipynb"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Berhasil membuat notebook di: {output_path}")

if __name__ == "__main__":
    create_notebook()
