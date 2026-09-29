"""Script to generate AI_Modul_3.9_Praktikum_Penanganan_Pengecualian_dan_Debugging.ipynb
Modul 3.9: Penanganan Pengecualian dan Debugging (try-except-else-finally, Custom Exceptions, Logging, PDB)
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
    add_md(r"""# AI Modul 3.9: Praktikum Penanganan Pengecualian dan Debugging
### Pohon Hierarki Eksepsi CPython, Alur Blok try-except-else-finally, Pengecualian Kustom Domain Agribisnis, Exception Chaining, Arsitektur Logging Terstruktur, dan Debugging Interaktif pdb

---
**Program Studi**: Sarjana Sains Data / Kecerdasan Buatan / Teknik Pertanian  
**Institusi**: Institut Pertanian Stiper (INSTIPER) Yogyakarta  
**Kompatibilitas**: Python 3.10+ (Standar PEP 3134, PEP 282, PEP 553)

---
### Capaian Pembelajaran Praktikum:
1. **Outputs**: Membangun engine monitoring ketel uap PKS kebal crash, taksonomi eksepsi kustom domain kelapa sawit, dan pipeline logging multi-kanal rotasional.
2. **Outcomes**: Menguasai arsitektur 4-blok deterministik `try-except-else-finally`, rantai eksepsi preservasi traceback (`raise ... from ...`), serta teknik isolasi bug via inspeksi stack.
3. **Impacts**: Mencegah kegagalan fatal (*unhandled exceptions*) pada sistem otomasi pabrik kelapa sawit dan memenuhi standar audit forensik operasional K3 industri.""")

    # Section 1: Inisialisasi Environment & Dependensi
    add_md(r"""## 1. Inisialisasi Environment dan Dependensi
Kita mengimpor modul bawaan sistem (`sys`, `os`, `time`, `traceback`, `logging`), handler berkas rotasional, serta pustaka visualisasi Matplotlib.""")

    add_code("""import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt

print(f"Versi Python: {sys.version}")
sandbox_logs = "sandbox_logs_3_9"
os.makedirs(sandbox_logs, exist_ok=True)
print(f"Status: Direktori log '{sandbox_logs}' siap digunakan.")""")

    # Section 2: Hierarki Eksepsi CPython
    add_md(r"""## 2. Eksplorasi Hierarki Eksepsi CPython dan Bahaya Bare Except
Kita membuktikan secara terprogram hubungan pewarisan antara `BaseException`, `Exception`, dan subkelas standar, serta alasan mengapa `BaseException` tidak boleh ditangkap oleh logika aplikasi biasa.""")

    add_code("""# Memeriksa Hubungan Subclassing Eksepsi CPython
print(f"Apakah Exception turunan BaseException?      : {issubclass(Exception, BaseException)}")
print(f"Apakah KeyboardInterrupt turunan Exception?   : {issubclass(KeyboardInterrupt, Exception)}")
print(f"Apakah KeyboardInterrupt turunan BaseException?: {issubclass(KeyboardInterrupt, BaseException)}")
print(f"Apakah ZeroDivisionError turunan Exception?   : {issubclass(ZeroDivisionError, Exception)}")
print(f"Apakah ValueError turunan Exception?          : {issubclass(ValueError, Exception)}")""")

    # Section 3: Alur 4-Blok Deterministik
    add_md(r"""## 3. Alur Kendali 4-Blok Deterministik (`try-except-else-finally`)
Kita menguji siklus pemrosesan sensor stasiun perebusan buah sawit dengan 4 blok terpadu.""")

    add_code("""def simulasi_pembacaan_sensor(nilai_raw: Any) -> float:
    \"\"\"Mendemonstrasikan siklus alur try - except - else - finally.\"\"\"
    status_proses = "INIT"
    hasil_suhu = 0.0
    
    print(f"\\n--- Menguji Input: {repr(nilai_raw)} ---")
    try:
        # Blok 1: Zona Risiko
        hasil_suhu = float(nilai_raw)
        if hasil_suhu < 0.0:
            raise ValueError(f"Suhu bejana tidak boleh negatif ({hasil_suhu}°C)!")
            
    except (ValueError, TypeError) as err:
        # Blok 2: Penanganan Spesifik
        status_proses = f"GALAT: {err}"
        print(f"  [EXCEPT] Menangani kesalahan: {status_proses}")
        hasil_suhu = 25.0  # Fallback default aman
        
    else:
        # Blok 3: Sukses Murni (Dieksekusi HANYA jika try tuntas tanpa error)
        status_proses = "SUKSES_NORMAL"
        print(f"  [ELSE] Validasi berhasil tuntas! Nilai suhu: {hasil_suhu}°C")
        
    finally:
        # Blok 4: Pembersihan Mutlak (PASTI dieksekusi)
        print(f"  [FINALLY] Membersihkan sumber daya. Status akhir: {status_proses}")
        
    return hasil_suhu

# Uji Coba 1: Input Normal
simulasi_pembacaan_sensor("145.5")

# Uji Coba 2: Input Rusak / String Bukan Angka
simulasi_pembacaan_sensor("SENSOR_PUTUS")

# Uji Coba 3: Input Negatif
simulasi_pembacaan_sensor("-15.0")""")

    # Section 4: Eksepsi Kustom & Exception Chaining
    add_md(r"""## 4. Pengecualian Kustom Domain Agribisnis & Exception Chaining (PEP 3134)
Kita merancang kelas eksepsi domain khusus perkebunan dan menghubungkan akar penyebab galat menggunakan sintaksis `raise ... from ...`.""")

    add_code("""# Definisi Taksonomi Eksepsi Khusus PKS Sawit
class PKSOperationalError(Exception):
    \"\"\"Kelas dasar pengecualian operasional PKS.\"\"\"
    pass

class TekananUapKritisError(PKSOperationalError):
    \"\"\"Diterbitkan jika tekanan bejana perebusan melampaui batas toleransi fisik.\"\"\"
    def __init__(self, id_unit: str, tekanan_bar: float, batas_bar: float = 32.0):
        self.id_unit = id_unit
        self.tekanan = tekanan_bar
        self.batas = batas_bar
        super().__init__(f"OVERPRESSURE PADA {id_unit}: {tekanan_bar:.1f} bar (Maks: {batas_bar:.1f} bar)!")

class DataSensorKorupError(PKSOperationalError):
    \"\"\"Diterbitkan jika payload telemetri tidak dapat diurai.\"\"\"
    pass

def proses_sinyal_tekanan(id_boiler: str, string_sinyal: str) -> float:
    \"\"\"Memproses sinyal dan menerapkan Exception Chaining (raise ... from ...).\"\"\"
    try:
        nilai_p = float(string_sinyal)
    except ValueError as err:
        # Hubungkan galat teknis ValueError ke eksepsi domain DataSensorKorupError
        raise DataSensorKorupError(f"Format telemetri dari {id_boiler} rusak: {string_sinyal}") from err
        
    if nilai_p >= 32.0:
        raise TekananUapKritisError(id_boiler, nilai_p, batas_bar=32.0)
        
    return nilai_p

# Uji Coba Rantai Eksepsi
try:
    proses_sinyal_tekanan("BOILER-01", "KORUP_SINYAL")
except DataSensorKorupError as err_domain:
    print(f"Tertangkap Eksepsi Domain: {err_domain}")
    print(f"Penyebab Asal (__cause__) : {repr(err_domain.__cause__)}")""")

    # Section 5: Pipeline Logging Terstruktur
    add_md(r"""## 5. Pipeline Logging Terstruktur Standar Industri
Kita mengonfigurasi logger multi-handler dengan `StreamHandler` untuk konsol dan `RotatingFileHandler` untuk penyimpanan berkas otomatis.""")

    add_code("""# Membangun Logger Produksi PKS
logger_pks = logging.getLogger("PKS_MONITOR")
logger_pks.setLevel(logging.DEBUG)

# Format Terstruktur: [Timestamp] [Level] [Logger] - Pesan
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)-8s] [%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 1. Console Handler (Hanya menampilkan level INFO ke atas)
console_h = logging.StreamHandler(sys.stdout)
console_h.setLevel(logging.INFO)
console_h.setFormatter(formatter)

# 2. Rotating File Handler (Menyimpan seluruh jejak DEBUG ke atas, maks 500 KB)
path_log_file = os.path.join(sandbox_logs, "pks_operasional.log")
file_h = RotatingFileHandler(path_log_file, maxBytes=500_000, backupCount=2, encoding="utf-8")
file_h.setLevel(logging.DEBUG)
file_h.setFormatter(formatter)

# Pasang handlers jika belum terpasang
if not logger_pks.handlers:
    logger_pks.addHandler(console_h)
    logger_pks.addHandler(file_h)

# Uji coba pemancaran log di berbagai level
logger_pks.debug("Sensor kalibrasi nol berhasil dievaluasi.")
logger_pks.info("Turbin uap sinkron dengan jaringan listrik pabrik.")
logger_pks.warning("Suhu bearing generator mendekati 80°C.")
logger_pks.error("Katup suplai air umpan boiler gagal merespon perintah buka.")
logger_pks.critical("TEKANAN UAP OVERLIMIT: Protokol pemadaman darurat aktif!")""")

    # Section 6: Teknik Traceback & Debugging
    add_md(r"""## 6. Teknik Debugging & Introspeksi Tumpukan (*Traceback Formatting*)
Kita mengekstrak jejak tumpukan panggilan secara programatis menggunakan modul `traceback` tanpa menghentikan sistem secara mendadak.""")

    add_code("""def fungsi_tingkat_dalam(x: float) -> float:
    return 100.0 / x

def fungsi_tingkat_menengah(a: float) -> float:
    return fungsi_tingkat_dalam(a)

try:
    fungsi_tingkat_menengah(0.0)
except ZeroDivisionError:
    # Memformat stack trace ke dalam string untuk dikirim ke SIEM/Database log
    stack_trace_str = traceback.format_exc()
    print("Stack Trace Tertangkap Secara Programatis:")
    print("-" * 50)
    print(stack_trace_str)""")

    # Section 7: Implementasi Kasus Nyata: Engine Pengawas Turbin & Ketel PKS
    add_md(r"""## 7. Implementasi Kasus Nyata: Engine Pengawas Turbin & Ketel PKS
Di bawah ini kita mengintegrasikan seluruh konsep ke dalam kelas `EnginePengawasBoiler` dan memvisualisasikan telemetri operasi.""")

    add_code("""class EnginePengawasBoiler:
    \"\"\"Sistem pemantau turbin dan ketel uap PKS dengan pipeline logging industri.\"\"\"
    def __init__(self, nama_unit: str = "BOILER-01"):
        self.nama_unit = nama_unit
        self.riwayat_tekanan: List[float] = []
        self.riwayat_status: List[str] = []

    def audit_titik_waktu(self, tekanan_bar: float) -> str:
        self.riwayat_tekanan.append(tekanan_bar)
        try:
            if tekanan_bar >= 32.0:
                raise TekananUapKritisError(self.nama_unit, tekanan_bar)
            elif tekanan_bar <= 0.0:
                raise ValueError("Tekanan vakum tidak realistis!")
        except TekananUapKritisError as e:
            status = "KRITIS_OVERPRESSURE"
            logger_pks.critical(str(e))
        except ValueError as e:
            status = "SENSOR_ANOMALI"
            logger_pks.error(f"Peringatan Sensor: {e}")
        else:
            status = "NORMAL_STABIL"
            logger_pks.debug(f"{self.nama_unit} bertekanan normal: {tekanan_bar:.1f} bar")
        finally:
            self.riwayat_status.append(status)
            
        return status

# Simulasi 10 titik waktu pemantauan tekanan boiler
engine_boiler = EnginePengawasBoiler("BOILER-01")
data_uji_tekanan = [24.5, 25.2, 26.0, 27.5, 31.0, 33.5, 29.0, 28.2, -5.0, 25.0]

for p in data_uji_tekanan:
    st = engine_boiler.audit_titik_waktu(p)""")

    add_code("""# Visualisasi Profil Tekanan Boiler dan Deteksi Ambang Kritis
plt.figure(figsize=(10, 4.5))
waktu_step = list(range(1, len(data_uji_tekanan) + 1))

# Warna titik berdasarkan status
warna_titik = []
for s in engine_boiler.riwayat_status:
    if s == "KRITIS_OVERPRESSURE":
        warna_titik.append('#dc2626')  # Merah
    elif s == "SENSOR_ANOMALI":
        warna_titik.append('#f59e0b')  # Oranye
    else:
        warna_titik.append('#16a34a')  # Hijau

plt.plot(waktu_step, data_uji_tekanan, color='#2563eb', linestyle='--', linewidth=1.5, alpha=0.7)
plt.scatter(waktu_step, data_uji_tekanan, c=warna_titik, s=80, edgecolors='black', zorder=5)
plt.axhline(32.0, color='#dc2626', linestyle='-', linewidth=2.0, label='Ambang Batas Kritis Bejana (32 bar)')
plt.axhline(0.0, color='#64748b', linestyle=':', linewidth=1.2, label='Batas Vakum Terendah (0 bar)')

plt.title("Profil Pemantauan Tekanan Uap Boiler PKS dengan Deteksi Eksepsi Kritis", fontsize=12, fontweight='bold')
plt.xlabel("Langkah Waktu Telemetri (Detik)", fontsize=10)
plt.ylabel("Tekanan Uap (bar)", fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower left')
plt.tight_layout()
plt.show()""")

    # Section 8: Solusi Tantangan Mandiri Berjenjang
    add_md(r"""## 8. Solusi Tantangan Mandiri Berjenjang (Scaffolded Challenges)

### Tantangan 1 (Dasar): Konversi Telemetri Kebun yang Tangguh
Membangun fungsi `konversi_suhu_tangguh(nilai_str: str, nilai_default: float = 25.0) -> float` menggunakan blok `try-except-else`.""")

    add_code("""def konversi_suhu_tangguh(nilai_str: str, nilai_default: float = 25.0) -> float:
    \"\"\"Mengonversi string telemetri ke float secara tangguh terhadap data korup.
    
    Args:
        nilai_str: String input pembacaan sensorik.
        nilai_default: Nilai pengganti jika konversi gagal.
        
    Returns:
        float: Nilai numerik hasil parsing atau nilai default aman.
    \"\"\"
    try:
        hasil = float(nilai_str)
    except (ValueError, TypeError) as err:
        print(f"[RESCUE] Konversi gagal untuk '{nilai_str}' ({err}). Menggunakan default: {nilai_default}")
        return nilai_default
    else:
        print(f"[SUKSES] Parsing berhasil: {hasil:.2f}°C")
        return hasil

# Uji Coba Tantangan 1
suhu_1 = konversi_suhu_tangguh("32.8")
suhu_2 = konversi_suhu_tangguh("TIMEOUT_ERROR")
suhu_3 = konversi_suhu_tangguh("")
print(f"Hasil Akhir: Suhu 1={suhu_1}, Suhu 2={suhu_2}, Suhu 3={suhu_3}")""")

    add_md(r"""### Tantangan 2 (Menengah): Pemantauan Tekanan Pipa Irigasi dengan Eksepsi Kustom & Rantai Galat
Membangun kelas `TekananPipaIrigasiError` dan fungsi `evaluasi_tekanan_irigasi` dengan *Exception Chaining* (`from err`).""")

    add_code("""class TekananPipaIrigasiError(Exception):
    \"\"\"Pengecualian khusus anomali tekanan jaringan pipa fertigasi kebun.\"\"\"
    pass

def evaluasi_tekanan_irigasi(tekanan_raw: str, ambang_aman: float = 4.0) -> float:
    \"\"\"Memvalidasi tekanan dan merantai eksepsi teknis ke eksepsi domain.\"\"\"
    try:
        nilai = float(tekanan_raw)
    except ValueError as err:
        raise TekananPipaIrigasiError(f"Format telemetri tekanan tidak valid: '{tekanan_raw}'") from err
        
    if nilai > ambang_aman:
        raise TekananPipaIrigasiError(f"Tekanan pipa kritis: {nilai:.2f} bar melebihi batas aman {ambang_aman:.2f} bar!")
        
    return nilai

# Uji Coba Tantangan 2
kasus_uji = ["2.8", "5.4", "RUSAK"]
for k in kasus_uji:
    try:
        p = evaluasi_tekanan_irigasi(k, ambang_aman=4.0)
        print(f"Uji '{k}' -> NORMAL ({p} bar)")
    except TekananPipaIrigasiError as e:
        print(f"Uji '{k}' -> TERTANGKAP: {e}")""")

    add_md(r"""### Tantangan 3 (Mahir): Pipeline Audit Sortasi TBS Terintegrasi Logging Multi-Handler
Membangun kelas `EngineAuditSortasi` dengan logging ganda (Console & Berkas) dan eksepsi kustom `KontaminasiSampahError` & `BuahMentahError`.""")

    add_code("""class KontaminasiSampahError(Exception):
    \"\"\"Diterbitkan jika janjang TBS memuat kotoran sampah batu/pasir berlebih.\"\"\"
    pass

class BuahMentahError(Exception):
    \"\"\"Diterbitkan jika janjang TBS berada pada Fraksi 00/0 (mentah).\"\"\"
    pass

class EngineAuditSortasi:
    \"\"\"Engine pemilah mutu janjang TBS dengan sistem logging terisolasi.\"\"\"
    def __init__(self, nama_pos: str = "SORTASI_RAMP_01"):
        self.logger = logging.getLogger(nama_pos)
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
            # Console handler
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(logging.INFO)
            ch.setFormatter(fmt)
            self.logger.addHandler(ch)
            
            # File handler untuk peringatan/galat
            path_log_penalti = os.path.join(sandbox_logs, "penalti_tbs.log")
            fh = logging.FileHandler(path_log_penalti, encoding="utf-8")
            fh.setLevel(logging.WARNING)
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)

    def inspeksi_janjang(self, id_janjang: str, persen_brondol: float, ada_sampah: bool) -> str:
        keputusan = "BELUM_DITENTUKAN"
        try:
            if ada_sampah:
                self.logger.warning(f"Janjang {id_janjang} terkontaminasi sampah batu/gagang!")
                raise KontaminasiSampahError(f"Kontaminasi berat pada {id_janjang}")
            if persen_brondol < 12.5:
                self.logger.warning(f"Janjang {id_janjang} buah mentah ({persen_brondol}% brondolan)!")
                raise BuahMentahError(f"Buah mentah pada {id_janjang}")
        except KontaminasiSampahError:
            keputusan = "REJECT_KONTAMINASI"
        except BuahMentahError:
            keputusan = "PENALTI_MENTAH"
        else:
            keputusan = "MUTU_PRIMA_DITERIMA"
            self.logger.info(f"Janjang {id_janjang} lolos sortasi mutu prima.")
        finally:
            self.logger.debug(f"Pemeriksaan {id_janjang} selesai. Keputusan: {keputusan}")
            
        return keputusan

# Uji Coba Tantangan 3
engine_sortir = EngineAuditSortasi("POS_SORTIR_01")
print("\\nHASIL PENGUJIAN TANTANGAN 3:")
hasil_a = engine_sortir.inspeksi_janjang("JJG-101", 35.0, False)
hasil_b = engine_sortir.inspeksi_janjang("JJG-102", 5.0, False)
hasil_c = engine_sortir.inspeksi_janjang("JJG-103", 40.0, True)

print(f"Hasil JJG-101: {hasil_a}")
print(f"Hasil JJG-102: {hasil_b}")
print(f"Hasil JJG-103: {hasil_c}")""")

    # Output path
    output_path = r"e:\Project Buku\notebooks\part-03\AI_Modul_3.9_Praktikum_Penanganan_Pengecualian_dan_Debugging.ipynb"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"Berhasil membuat notebook di: {output_path}")

if __name__ == "__main__":
    create_notebook()
