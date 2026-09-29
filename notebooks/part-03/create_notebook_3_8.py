"""Script to generate AI_Modul_3.8_Praktikum_Penanganan_Berkas.ipynb
Modul 3.8: Penanganan Berkas (File Handling: Text, CSV, JSON, Pickle, Context Managers)
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
    add_md(r"""# AI Modul 3.8: Praktikum Penanganan Berkas (File Handling & I/O)
### Arsitektur Aliran Stream CPython, Manajer Konteks Protokol with, Pemrosesan Streaming Data Teks & Tabular CSV, Serialisasi Terstruktur JSON/GeoJSON, Format Biner Pickle, dan Manajemen Persistensi Cerdas Perkebunan

---
**Program Studi**: Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian  
**Institusi**: Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Kompatibilitas**: Python 3.10+ (Standar PEP 343, RFC 4180, RFC 7946)

---
### Capaian Pembelajaran Praktikum:
1. **Outputs**: Membangun pipeline pencatatan log transaksi timbangan lori TBS, ekspor data sensus tabular CSV, penyimpanan poligon batas blok GeoJSON, dan serialisasi biner model AI.
2. **Outcomes**: Menguasai protokol manajer konteks (`__enter__` & `__exit__`), pemrosesan aliran berkas streaming berjejak memori $\mathcal{O}(1)$, serta audit keamanan format serialisasi biner.
3. **Impacts**: Mencegah kebocoran berkas deskriptor sistem operasi (*file descriptor exhaustion*) dan menjamin integritas data transaksi pabrik kelapa sawit secara permanen.""")

    # Section 1: Inisialisasi Environment & Dependensi
    add_md(r"""## 1. Inisialisasi Environment dan Dependensi
Kita mengimpor modul I/O bawaan Python (`os`, `csv`, `json`, `pickle`, `shutil`), modul waktu (`time`), serta pustaka visualisasi data (`matplotlib.pyplot`).""")

    add_code("""import csv
import json
import os
import pickle
import shutil
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt

print(f"Versi Python: {sys.version}")
sandbox_dir = "sandbox_praktikum_3_8"
os.makedirs(sandbox_dir, exist_ok=True)
print(f"Status: Direktori kerja '{sandbox_dir}' siap digunakan.")""")

    # Section 2: Arsitektur I/O & Protokol Context Manager
    add_md(r"""## 2. Arsitektur I/O CPython dan Protokol Manajer Konteks (`with`)
Kita memverifikasi properti objek stream (`encoding`, `mode`, `fileno`) dan membuktikan jaminan penutupan berkas deskriptor via manajer konteks.""")

    add_code("""# Demonstrasi 1: Eksplorasi Properti Stream dan Penyandian UTF-8
nama_berkas_tes = os.path.join(sandbox_dir, "uji_stream.txt")

with open(nama_berkas_tes, mode="w", encoding="utf-8") as f:
    f.write("Pencatatan Sensor Iklim Kebun INSTIPER\\n")
    f.write("Koordinat: 0.53° LU, 101.42° BT\\n")
    print(f"Tipe Objek Stream : {type(f)}")
    print(f"Penyandian Teks   : {f.encoding}")
    print(f"Mode Operasi      : {f.mode}")
    print(f"File Descriptor OS: {f.fileno()} (Nomor indeks tabel kernel)")

# Di luar blok with, f.__exit__() telah dipanggil
print(f"Status Berkas Tertutup: {f.closed} (Berkas deskriptor berhasil dikembalikan ke OS!)")""")

    # Section 3: Pemrosesan Berkas Teks & Streaming Reading
    add_md(r"""## 3. Pemrosesan Berkas Teks: Streaming Iterator vs `readlines()`
Kita membuktikan keunggulan pembacaan sebaris demi sebaris (*streaming iterator*) yang menjaga jejak memori tetap konstan $\mathcal{O}(1)$ tanpa memuat seluruh berkas ke RAM.""")

    add_code("""# Membuat berkas log transaksi sintetis 1000 baris
path_log_sintetis = os.path.join(sandbox_dir, "log_timbangan_panen.log")
with open(path_log_sintetis, "w", encoding="utf-8") as f:
    for i in range(1, 1001):
        status = "DITERIMA" if i % 10 != 0 else "PENALTI_MENTAH"
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] LORI-{i:04d} | BERAT:{3500 + (i % 500)} kg | STATUS:{status}\\n")

# Pembacaan Streaming O(1) Memori (Sangat Efisien)
cacah_diterima = 0
cacah_penalti = 0

with open(path_log_sintetis, "r", encoding="utf-8") as f:
    for baris in f:  # Lazy stream: Membaca satu baris per iterasi
        if "STATUS:DITERIMA" in baris:
            cacah_diterima += 1
        elif "STATUS:PENALTI_MENTAH" in baris:
            cacah_penalti += 1

print(f"Hasil Audit Streaming Berkas Log:")
print(f"  Total Lori Diterima : {cacah_diterima} lori")
print(f"  Total Lori Berpenalti: {cacah_penalti} lori")""")

    # Section 4: Pemrosesan Tabular CSV
    add_md(r"""## 4. Pemrosesan Tabular CSV via `csv.DictReader` dan `csv.DictWriter`
Kita mempraktikkan penulisan dan pembacaan CSV ber-header secara aman dengan parameter `newline=""`.""")

    add_code("""# Menulis data telemetri cuaca ke CSV
path_csv_cuaca = os.path.join(sandbox_dir, "telemetri_stasiun_cuaca.csv")
data_telemetri = [
    {"waktu": "08:00", "stasiun": "AWS-01", "suhu_c": 28.5, "kelembaban_pct": 85.0, "curah_hujan_mm": 0.0},
    {"waktu": "10:00", "stasiun": "AWS-01", "suhu_c": 31.2, "kelembaban_pct": 74.5, "curah_hujan_mm": 0.0},
    {"waktu": "12:00", "stasiun": "AWS-01", "suhu_c": 34.0, "kelembaban_pct": 62.0, "curah_hujan_mm": 0.0},
    {"waktu": "14:00", "stasiun": "AWS-01", "suhu_c": 33.5, "kelembaban_pct": 65.0, "curah_hujan_mm": 12.5},
    {"waktu": "16:00", "stasiun": "AWS-01", "suhu_c": 29.8, "kelembaban_pct": 82.0, "curah_hujan_mm": 24.0},
]

fieldnames = ["waktu", "stasiun", "suhu_c", "kelembaban_pct", "curah_hujan_mm"]

with open(path_csv_cuaca, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_telemetri)

print(f"Sukses menulis {len(data_telemetri)} baris ke CSV.")

# Membaca kembali menggunakan csv.DictReader
data_terbaca: List[Dict[str, Any]] = []
with open(path_csv_cuaca, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Konversi tipe data dari string ke numerik
        row["suhu_c"] = float(row["suhu_c"])
        row["kelembaban_pct"] = float(row["kelembaban_pct"])
        row["curah_hujan_mm"] = float(row["curah_hujan_mm"])
        data_terbaca.append(row)

print("Sampel Baris Terbaca Pertama:", data_terbaca[0])""")

    # Section 5: Serialisasi Terstruktur JSON & GeoJSON
    add_md(r"""## 5. Serialisasi Terstruktur JSON dan Format Spasial GeoJSON
Kita menyusun berkas representasi spasial poligon kebun format GeoJSON (RFC 7946) menggunakan `json.dump` terformat.""")

    add_code("""# Menyusun struktur GeoJSON poligon blok perkebunan sawit
geojson_afdeling = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [101.420, 0.530],
                        [101.435, 0.530],
                        [101.435, 0.518],
                        [101.420, 0.518],
                        [101.420, 0.530]
                    ]
                ]
            },
            "properties": {
                "id_blok": "BLOK-INTI-A01",
                "afdeling": "AFD-01",
                "luas_ha": 32.5,
                "varietas": "Tenera Dami",
                "populasi_pohon": 4350,
                "status_irigasi": "Aktif"
            }
        }
    ]
}

path_geojson = os.path.join(sandbox_dir, "peta_blok_a01.geojson")
with open(path_geojson, mode="w", encoding="utf-8") as f:
    json.dump(geojson_afdeling, f, indent=2, ensure_ascii=False)

print(f"Berkas Spasial GeoJSON berhasil diekspor ke: {path_geojson}")

# Membaca kembali via json.load()
with open(path_geojson, mode="r", encoding="utf-8") as f:
    data_geo = json.load(f)

prop = data_geo["features"][0]["properties"]
print(f"Metadata Blok Terbaca: {prop['id_blok']} (Luas: {prop['luas_ha']} ha, Populasi: {prop['populasi_pohon']} pokok)")""")

    # Section 6: Serialisasi Objek AI dengan pickle & Audit Keamanan
    add_md(r"""## 6. Serialisasi Objek AI dengan `pickle` dan Audit Keamanan
Kita mendemonstrasikan penyimpanan status model kelas kustom ke format biner `pickle` dan membedah risiko keamanan eksekusi kode berbahaya via metode dunder `__reduce__`.""")

    add_code("""# Definisi Model AI Kalibrasi Dosis Pupuk
class ModelKalibrasiPupuk:
    def __init__(self, koefisien_n: float, bias_dasar: float):
        self.koefisien_n = koefisien_n
        self.bias_dasar = bias_dasar
        self.versi = "1.0-INSTIPER"

    def hitung_dosis(self, ndvi_kanopi: float) -> float:
        # Defisit klorofil: semakin rendah NDVI, semakin tinggi kebutuhan pupuk Urea
        defisit = max(0.0, 0.85 - ndvi_kanopi)
        return round((self.koefisien_n * defisit) + self.bias_dasar, 2)

model_siap = ModelKalibrasiPupuk(koefisien_n=4.5, bias_dasar=1.2)
path_model_pkl = os.path.join(sandbox_dir, "model_pupuk_v1.pkl")

# Serialisasi ke Biner (wb)
with open(path_model_pkl, "wb") as f:
    pickle.dump(model_siap, f, protocol=pickle.HIGHEST_PROTOCOL)
print(f"Model berhasil diserialisasi ke biner ({os.path.getsize(path_model_pkl)} byte).")

# Deserialisasi dari Biner (rb)
with open(path_model_pkl, "rb") as f:
    model_dimuat: ModelKalibrasiPupuk = pickle.load(f)

print(f"Model Dimuat Kembali! Versi: {model_dimuat.versi}")
print(f"Rekomendasi Pupuk untuk NDVI 0.45: {model_dimuat.hitung_dosis(0.45)} kg Urea/pokok")""")

    # Section 7: Visualisasi Telemetri dari Berkas CSV
    add_md(r"""## 7. Visualisasi Telemetri Deret Waktu yang Dimuat dari Berkas CSV
Kita memvisualisasikan data telemetri cuaca yang dibaca dari berkas CSV untuk mengonfirmasi integritas pemrosesan I/O.""")

    add_code("""# Plot profil suhu dan curah hujan dari data CSV yang dibaca sebelumnya
jam = [d["waktu"] for d in data_terbaca]
suhu = [d["suhu_c"] for d in data_terbaca]
hujan = [d["curah_hujan_mm"] for d in data_terbaca]

fig, ax1 = plt.subplots(figsize=(10, 4.5))

color = '#dc2626'
ax1.set_xlabel('Waktu Pengamatan (Jam)', fontsize=10)
ax1.set_ylabel('Suhu Udara (°C)', color=color, fontsize=10)
ax1.plot(jam, suhu, color=color, marker='o', linewidth=2.2, label='Suhu Udara (°C)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle=':', alpha=0.6)

# Sumbu kedua untuk curah hujan
ax2 = ax1.twinx()
color = '#2563eb'
ax2.set_ylabel('Curah Hujan (mm)', color=color, fontsize=10)
ax2.bar(jam, hujan, color=color, alpha=0.35, width=0.35, label='Curah Hujan (mm)')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 35)

plt.title("Profil Mikroklimat Stasiun Cuaca Kebun Sawit (Hasil Pembacaan Berkas CSV)", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()""")

    # Section 8: Solusi Tantangan Mandiri Berjenjang
    add_md(r"""## 8. Solusi Tantangan Mandiri Berjenjang (Scaffolded Challenges)

### Tantangan 1 (Dasar): Penghitung Baris Berkas Log Streaming Hemat Memori
Membangun fungsi `hitung_peringatan_streaming(path_berkas: str, kata_kunci: str = "WARNING") -> int` yang membaca berkas secara streaming $\mathcal{O}(1)$ memori.""")

    add_code("""def hitung_peringatan_streaming(path_berkas: str, kata_kunci: str = "WARNING") -> int:
    \"\"\"Menghitung kemunculan kata kunci peringatan dalam berkas log secara streaming.
    
    Args:
        path_berkas: Lokasi fisik berkas log pada media penyimpanan.
        kata_kunci: Kata kunci pencarian (default: 'WARNING').
        
    Returns:
        int: Total jumlah baris yang memuat kata kunci.
    \"\"\"
    cacah = 0
    with open(path_berkas, mode="r", encoding="utf-8") as f:
        for baris in f:  # Pola streaming: O(1) RAM
            if kata_kunci in baris:
                cacah += 1
    return cacah

# Uji Coba Tantangan 1 pada berkas log sintetis yang telah dibuat
jumlah_penalti = hitung_peringatan_streaming(path_log_sintetis, "PENALTI_MENTAH")
print("HASIL PENGUJIAN TANTANGAN 1:")
print(f"  Ditemukan {jumlah_penalti} baris anomali lori berpenalti dalam log.")""")

    add_md(r"""### Tantangan 2 (Menengah): Sanitasi dan Agregasi CSV Telemetri Sensorik
Membangun fungsi `sanitasi_dan_rekap_suhu_csv(path_input: str, path_output: str) -> Dict[str, float]` yang menyaring data suhu valid dan menulis ulang berkas bersih.""")

    add_code("""# Siapkan data CSV kotor dengan data NULL dan angka negatif ekstrem
path_csv_kotor = os.path.join(sandbox_dir, "telemetri_kotor.csv")
with open(path_csv_kotor, "w", newline="", encoding="utf-8") as f:
    f.write("sensor_id,suhu_c\\n")
    f.write("S-01,31.5\\n")
    f.write("S-02,NULL\\n")
    f.write("S-03,-999.0\\n")
    f.write("S-04,33.2\\n")
    f.write("S-05,29.8\\n")

def sanitasi_dan_rekap_suhu_csv(path_input: str, path_output: str) -> Dict[str, float]:
    \"\"\"Menyaring baris korup pada berkas CSV dan menghasilkan rekapitulasi numerik.
    
    Args:
        path_input: Berkas CSV mentah yang berpotensi memuat anomali.
        path_output: Lokasi berkas CSV hasil sanitasi bersih.
        
    Returns:
        Dict[str, float]: Rangkuman metrik suhu_rata_rata, maksimum, dan baris valid.
    \"\"\"
    baris_bersih: List[Dict[str, Any]] = []
    daftar_suhu: List[float] = []

    with open(path_input, mode="r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            try:
                nilai_suhu = float(row["suhu_c"])
                # Aturan validasi: Suhu kebun harus berada dalam batas wajar [10.0, 50.0] °C
                if 10.0 <= nilai_suhu <= 50.0:
                    baris_bersih.append({"sensor_id": row["sensor_id"], "suhu_c": nilai_suhu})
                    daftar_suhu.append(nilai_suhu)
            except (ValueError, TypeError):
                # Baris korup seperti 'NULL' secara senyap diabaikan
                continue

    # Tulis data bersih ke path_output
    if baris_bersih:
        with open(path_output, mode="w", newline="", encoding="utf-8") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=["sensor_id", "suhu_c"])
            writer.writeheader()
            writer.writerows(baris_bersih)

    rata_rata = sum(daftar_suhu) / len(daftar_suhu) if daftar_suhu else 0.0
    maksimum = max(daftar_suhu) if daftar_suhu else 0.0

    return {
        "total_baris_valid": float(len(baris_bersih)),
        "suhu_rata_rata": round(rata_rata, 2),
        "suhu_maksimum": round(maksimum, 2)
    }

# Uji Coba Tantangan 2
path_csv_bersih = os.path.join(sandbox_dir, "telemetri_bersih.csv")
rekap_suhu = sanitasi_dan_rekap_suhu_csv(path_csv_kotor, path_csv_bersih)
print("HASIL SANITASI CSV TANTANGAN 2:")
for k, v in rekap_suhu.items():
    print(f"  {k:<20}: {v}")""")

    add_md(r"""### Tantangan 3 (Mahir): Manajer Konteks Kustom Pengukur Waktu I/O Berkas & Auto-Backup
Membangun kelas manajer konteks `PencatatDanCadanganAman` yang mengimplementasikan protokol `__enter__` dan `__exit__` untuk durasi audit dan auto-backup.""")

    add_code("""class PencatatDanCadanganAman:
    \"\"\"Manajer Konteks Kustom dengan audit durasi I/O dan pencadangan otomatis.\"\"\"
    
    def __init__(self, path_berkas: str, mode: str = "w", encoding: str = "utf-8"):
        self.path_berkas = path_berkas
        self.mode = mode
        self.encoding = encoding
        self.file_handle = None
        self.t_awal = 0.0

    def __enter__(self):
        \"\"\"Dieksekusi saat memasuki blok with: mulai timer dan buka stream.\"\"\"
        self.t_awal = time.perf_counter()
        self.file_handle = open(self.path_berkas, mode=self.mode, encoding=self.encoding)
        return self.file_handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        \"\"\"Dieksekusi saat keluar dari blok with: tutup berkas dan buat berkas cadangan.\"\"\"
        # 1. Pastikan berkas ditutup dan buffer ter-flush
        if self.file_handle and not self.file_handle.closed:
            self.file_handle.close()

        durasi_ms = (time.perf_counter() - self.t_awal) * 1000.0
        print(f"[AUDIT I/O] Operasi berkas '{os.path.basename(self.path_berkas)}' selesai dalam {durasi_ms:.3f} ms")

        # 2. Jika tidak ada eksepsi dan mode menulis, buat berkas cadangan (.bak)
        if exc_type is None and ("w" in self.mode or "a" in self.mode):
            path_bak = self.path_berkas + ".bak"
            shutil.copyfile(self.path_berkas, path_bak)
            print(f"[CADANGAN SUKSES] Berkas cadangan otomatis dibuat di: {path_bak}")

        # Kembalikan False agar eksepsi (jika ada) diteruskan ke pemanggil
        return False

# Uji Coba Tantangan 3
path_laporan_penting = os.path.join(sandbox_dir, "laporan_keuangan_sawit.txt")

with PencatatDanCadanganAman(path_laporan_penting, mode="w") as f:
    f.write("REKAPITULASI PENDAPATAN HARIAN PKS INSTIPER\\n")
    f.write("Total CPO Terjual: 450.5 Ton | ALB Rata-rata: 2.1%\\n")

# Verifikasi keberadaan berkas master dan berkas .bak
print(f"Berkas Master Ada : {os.path.exists(path_laporan_penting)}")
print(f"Berkas Backup Ada : {os.path.exists(path_laporan_penting + '.bak')}")""")

    # Output path
    output_path = r"e:\Project Buku\notebooks\part-03\AI_Modul_3.8_Praktikum_Penanganan_Berkas.ipynb"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Berhasil membuat notebook di: {output_path}")

if __name__ == "__main__":
    create_notebook()
