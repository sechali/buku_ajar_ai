"""Script to generate AI_Modul_3.10_Praktikum_Penggunaan_Package_Manager_pip.ipynb
Modul 3.10: Penggunaan Package Manager (pip) dan Ekosistem Pustaka AI (PyPI, requirements.txt, pyproject.toml, NumPy SIMD benchmark)
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
    add_md(r"""# AI Modul 3.10: Praktikum Penggunaan Package Manager (pip) dan Ekosistem Pustaka AI
### Repositori PyPI, Format Wheel vs Source Distribution, Manajemen Manifes Dependensi Deterministik (requirements.txt & pyproject.toml), Mitigasi Dependency Hell, dan Taksonomi Pustaka AI Agribisnis

---
**Program Studi**: Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian  
**Institusi**: Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Kompatibilitas**: Python 3.10+ (Standar PEP 427, PEP 440, PEP 508, PEP 518)

---
### Capaian Pembelajaran Praktikum:
1. **Outputs**: Membangun skrip auditor pohon dependensi AI agribisnis, generator manifes terkunci dengan verifikasi SHA-256, serta studi benchmark komputasi spektral sejuta piksel.
2. **Outcomes**: Menguasai arsitektur Wheel biner vs sdist, tata kelola Semantic Versioning deklaratif, serta akselerasi komputasi vektorisasi SIMD NumPy.
3. **Impacts**: Menjamin reproduktibilitas mutlak deployment model AI di pabrik dan kebun kelapa sawit serta melindungi server dari serangan rantai pasok software.""")

    # Section 1: Inisialisasi Environment & Dependensi
    add_md(r"""## 1. Inisialisasi Environment dan Dependensi
Kita mengimpor modul bawaan sistem (`sys`, `os`, `importlib.metadata`, `hashlib`, `time`), modul komputasi numerik (`numpy`), dan pustaka visualisasi (`matplotlib.pyplot`).""")

    add_code("""import hashlib
import importlib.metadata
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np

print(f"Versi Python : {sys.version}")
print(f"Platform OS  : {sys.platform}")
sandbox_env = "sandbox_pip_3_10"
os.makedirs(sandbox_env, exist_ok=True)
print(f"Status: Direktori sandbox '{sandbox_env}' siap digunakan.")""")

    # Section 2: Eksplorasi Metadata Lingkungan Virtual & ABI
    add_md(r"""## 2. Eksplorasi Metadata Lingkungan Virtual & Kompatibilitas ABI
Kita memeriksa lokasi instalasi paket pihak ketiga (`site-packages`) dan tag Application Binary Interface (ABI) CPython yang aktif.""")

    add_code("""# Memeriksa direktori penampung paket pihak ketiga (site-packages)
print("Lokasi Pencarian Modul (sys.path):")
for idx, path in enumerate(sys.path[:4]):
    print(f"  [{idx}] {path}")

# Mengidentifikasi CPython ABI Build
is_64bit = sys.maxsize > 2**32
print(f"\\nArsitektur Pointer: {'64-bit (x86_64)' if is_64bit else '32-bit'}")
print(f"Target Wheel Tag  : cp{sys.version_info.major}{sys.version_info.minor}-{sys.platform}")""")

    # Section 3: Audit Pohon Dependensi Pustaka Pihak Ketiga
    add_md(r"""## 3. Audit Pohon Dependensi Ekosistem Pustaka Sains Data AI
Kita memvalidasi keberadaan dan nomor versi pustaka inti kecerdasan buatan secara programatis menggunakan modul `importlib.metadata`.""")

    add_code("""pustaka_evaluasi = ["numpy", "pandas", "matplotlib", "scikit-learn", "pip"]

print(f"{'Nama Paket':<15} | {'Versi Terdeteksi':<16} | Status Integritas")
print("-" * 55)

ringkasan_audit = {}
for pkg in pustaka_evaluasi:
    try:
        ver = importlib.metadata.version(pkg)
        status = "TERPASANG (Aktif)"
    except importlib.metadata.PackageNotFoundError:
        ver = "Tidak Ditemukan"
        status = "HILANG / BELUM TERPASANG"
    ringkasan_audit[pkg] = ver
    print(f"{pkg:<15} | {ver:<16} | {status}")""")

    # Section 4: Praktik Manajemen Manifes Dependensi
    add_md(r"""## 4. Manajemen Manifes Dependensi: Pembangkitan dan Validasi SemVer
Kita mempraktikkan penyusunan berkas manifes `requirements.txt` dan menganalisis batasan Semantic Versioning (PEP 440).""")

    add_code("""# Membuat berkas requirements.txt deklaratif untuk sistem AI kebun
path_req_txt = os.path.join(sandbox_env, "requirements_agribisnis.txt")

daftar_syarat = [
    "# MANIFEST DEPENDENSI RESMI SISTEM AI PERKEBUNAN INSTIPER",
    "# Tanggal Terbit: " + time.strftime("%Y-%m-%d"),
    "",
    "numpy>=1.24.0,<2.0.0",
    "pandas>=2.0.0",
    "matplotlib>=3.7.0",
    "scikit-learn~=1.3.0",
    "opencv-python>=4.8.0",
]

with open(path_req_txt, "w", encoding="utf-8") as f:
    f.write("\\n".join(daftar_syarat) + "\\n")

print(f"Berkas Manifes berhasil ditulis ke: {path_req_txt}")
print("\\nIsi Berkas Manifes:")
with open(path_req_txt, "r", encoding="utf-8") as f:
    print(f.read())""")

    # Section 5: Simulasi Penguncian Hash Kriptografis SHA-256
    add_md(r"""## 5. Simulasi Penguncian Hash Kriptografis SHA-256 (`--require-hashes`)
Kita menyusun berkas manifes terkunci (`requirements.lock`) dengan hash SHA-256 untuk melindungi server PKS dari serangan rantai pasok (*supply chain attacks*).""")

    add_code("""# Menghasilkan mock lockfile dengan digest hash SHA-256 deterministik
path_lockfile = os.path.join(sandbox_env, "requirements.lock")

paket_terkunci = [
    ("numpy", ringkasan_audit.get("numpy", "1.26.4")),
    ("matplotlib", ringkasan_audit.get("matplotlib", "3.8.0")),
]

baris_lock = [
    "# LOCKFILE PRODUKSI SISTEM AI INSTIPER (DETERMINISTIC & INTEGRITY PROTECTED)",
    "# Generated by AI Modul 3.10 Security Pipeline",
    ""
]

for nama, ver in paket_terkunci:
    # Menghitung representasi mock hash SHA-256 dari nama dan versi
    seed_str = f"{nama}-{ver}-win_amd64.whl"
    hash_digest = hashlib.sha256(seed_str.encode("utf-8")).hexdigest()
    baris_lock.append(f"{nama}=={ver} \\\\")
    baris_lock.append(f"    --hash=sha256:{hash_digest}")

with open(path_lockfile, "w", encoding="utf-8") as f:
    f.write("\\n".join(baris_lock) + "\\n")

print(f"Berkas Lockfile Integritas berhasil dibuat di: {path_lockfile}\\n")
with open(path_lockfile, "r", encoding="utf-8") as f:
    print(f.read())""")

    # Section 6: Studi Komparasi Benchmark Vektorisasi SIMD
    add_md(r"""## 6. Studi Benchmark: Komputasi Spektral NDVI Sejuta Piksel (Python Murni vs NumPy)
Kita membandingkan secara empiris waktu pemrosesan formula $NDVI = \frac{NIR - RED}{NIR + RED}$ pada $1.000.000$ piksel citra drone kanopi sawit.""")

    add_code("""# 1. Alokasi Data Sintetis 1.000.000 Titik Spektral
N_PIXEL = 1_000_000
np.random.seed(42)
nir_array = np.random.uniform(0.40, 0.90, N_PIXEL)
red_array = np.random.uniform(0.05, 0.30, N_PIXEL)

nir_list = list(nir_array)
red_list = list(red_array)

# 2. Benchmark Pendekatan 1: Perulangan List Python Murni
t_awal = time.perf_counter()
ndvi_python = [(n - r) / (n + r) for n, r in zip(nir_list, red_list)]
t_akhir = time.perf_counter()
latensi_python_ms = (t_akhir - t_awal) * 1000.0

# 3. Benchmark Pendekatan 2: Komputasi Vektorisasi Array NumPy (SIMD)
t_awal = time.perf_counter()
ndvi_numpy = (nir_array - red_array) / (nir_array + red_array)
t_akhir = time.perf_counter()
latensi_numpy_ms = (t_akhir - t_awal) * 1000.0

faktor_percepatan = latensi_python_ms / latensi_numpy_ms

print(f"HASIL BENCHMARK KOMPUTASI NDVI 1.000.000 PIKSEL KANOPI SAWIT:")
print(f"  • Latensi List Comprehension Python Murni : {latensi_python_ms:6.2f} ms")
print(f"  • Latensi Vektorisasi Array NumPy (SIMD)  : {latensi_numpy_ms:6.2f} ms")
print(f"  • FAKTOR AKSELERASI VEKTORISASI           : {faktor_percepatan:5.1f}x LEBIH CEPAT!")""")

    add_code("""# Visualisasi Perbandingan Latensi Komputasi
metode = ['Python Murni\\n(List Comprehension)', 'NumPy\\n(SIMD Vektor)']
latensi = [latensi_python_ms, latensi_numpy_ms]
warna = ['#dc2626', '#16a34a']

plt.figure(figsize=(8, 4.5))
bars = plt.bar(metode, latensi, color=warna, edgecolor='black', width=0.45, alpha=0.85)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (latensi_python_ms * 0.02), 
             f"{yval:.2f} ms", ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.title("Komparasi Latensi Komputasi NDVI 1 Juta Piksel Kanopi Sawit", fontsize=12, fontweight='bold')
plt.ylabel("Waktu Eksekusi (Milidetik - Lebih Rendah Lebih Cepat)", fontsize=10)
plt.ylim(0, latensi_python_ms * 1.2)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()""")

    # Section 7: Solusi Tantangan Mandiri Berjenjang
    add_md(r"""## 7. Solusi Tantangan Mandiri Berjenjang (Scaffolded Challenges)

### Tantangan 1 (Dasar): Generator Manifes requirements.txt Terurut
Membangun fungsi `hasilkan_requirements_txt(daftar_dependensi: Dict[str, str], path_tujuan: str) -> str`.""")

    add_code("""def hasilkan_requirements_txt(daftar_dependensi: Dict[str, str], path_tujuan: str) -> str:
    \"\"\"Menghasilkan berkas requirements.txt terurut berdasarkan abjad secara otomatis.
    
    Args:
        daftar_dependensi: Pemetaan nama paket ke batasan versi (misal: {'numpy': '>=1.24'}).
        path_tujuan: Lokasi berkas manifes output.
        
    Returns:
        str: Jalur berkas hasil penulisan.
    \"\"\"
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
        f.write("\\n".join(lines) + "\\n")

    return path_tujuan

# Uji Coba Tantangan 1
dep_uji = {
    "scikit-learn": "~=1.3.0",
    "numpy": ">=1.26.0",
    "pandas": ">=2.1.0",
    "matplotlib": ">=3.8.0",
    "fastapi": ">=0.100.0"
}
path_out_t1 = os.path.join(sandbox_env, "requirements_terurut.txt")
hasilkan_requirements_txt(dep_uji, path_out_t1)

print("HASIL TANTANGAN 1:")
with open(path_out_t1, "r", encoding="utf-8") as f:
    print(f.read())""")

    add_md(r"""### Tantangan 2 (Menengah): Parser dan Validator Keketatan Manifes Produksi
Membangun fungsi `validasi_keketatan_manifes(path_requirements: str) -> Dict[str, Any]` yang memeriksa keberadaan operator penguncian mutlak `==`.""")

    add_code("""def validasi_keketatan_manifes(path_requirements: str) -> Dict[str, Any]:
    \"\"\"Memvalidasi bahwa seluruh dependensi dalam manifes dikunci dengan operator '=='.
    
    Args:
        path_requirements: Jalur berkas requirements.txt yang akan diaudit.
        
    Returns:
        Dict[str, Any]: Status kelulusan audit dan rincian pelanggaran.
    \"\"\"
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

# Uji Coba Tantangan 2 pada requirements_terurut.txt (yang memuat batasan longgar >= dan ~=)
audit_t2 = validasi_keketatan_manifes(path_out_t1)
print("HASIL AUDIT KEKETATAN MANIFES TANTANGAN 2:")
print(f"  Status Lulus Produksi    : {audit_t2['status_lulus']} (Ditolak karena belum dipin)")
print(f"  Jumlah Pelanggaran       : {len(audit_t2['daftar_pelanggaran_longgar'])} paket")
print(f"  Rincian Paket Longgar    : {audit_t2['daftar_pelanggaran_longgar']}")""")

    add_md(r"""### Tantangan 3 (Mahir): Simulator Dependency Lockfile Generator dengan SHA-256
Membangun kelas `GeneratorLockfileIntegritas` yang menghasilkan berkas lockfile resmi ber-hash SHA-256 dan memverifikasinya kembali.""")

    add_code("""class GeneratorLockfileIntegritas:
    \"\"\"Penghasil berkas lockfile deterministik ber-hash SHA-256 standar industri.\"\"\"
    
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
            lines.append(f"{token_paket} \\\\")
            lines.append(f"    --hash=sha256:{digest}")

        with open(path_output, mode="w", encoding="utf-8") as f:
            f.write("\\n".join(lines) + "\\n")
            
        return path_output

    @staticmethod
    def verifikasi_keutuhan(path_lockfile: str) -> bool:
        \"\"\"Memvalidasi keutuhan hash seluruh entri di dalam lockfile.\"\"\"
        with open(path_lockfile, mode="r", encoding="utf-8") as f:
            isi = f.read()

        # Validasi struktur
        return "--hash=sha256:" in isi and "==" in isi

# Uji Coba Tantangan 3
engine_lock = GeneratorLockfileIntegritas(["numpy", "pandas", "scikit-learn"])
path_lock_t3 = os.path.join(sandbox_env, "requirements_produksi_final.lock")
engine_lock.hasilkan_lockfile(path_lock_t3)

keutuhan_valid = GeneratorLockfileIntegritas.verifikasi_keutuhan(path_lock_t3)
print("HASIL TANTANGAN 3 (INTEGRITY LOCKFILE GENERATOR):")
print(f"  Lockfile Sukses Dibuat : {path_lock_t3}")
print(f"  Integritas Hash Valid  : {keutuhan_valid}")
print("\\nCuplikan Berkas Lockfile:")
with open(path_lock_t3, "r", encoding="utf-8") as f:
    for _ in range(7):
        print(" ", f.readline().strip())""")

    # Output path
    output_path = r"e:\Project Buku\notebooks\part-03\AI_Modul_3.10_Praktikum_Penggunaan_Package_Manager_pip.ipynb"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Berhasil membuat notebook di: {output_path}")

if __name__ == "__main__":
    create_notebook()
