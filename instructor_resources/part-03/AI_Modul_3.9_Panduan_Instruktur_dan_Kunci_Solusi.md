# Panduan Instruktur & Kunci Solusi: AI Modul 3.9
## Penanganan Pengecualian dan Debugging: Pohon Hierarki Eksepsi CPython, Alur Blok try-except-else-finally, Pengecualian Kustom Domain Agribisnis, Exception Chaining, Arsitektur Logging Terstruktur, dan Debugging Interaktif pdb

---

**Kode Modul:** AI Modul 3.9  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Pemrograman Python Dasar untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Ketahanan Sistem: Mengapa Sistem Cerdas PKS Tidak Boleh Mogok? | Studi kasus ledakan bejana uap & kegagalan sensor telemetri PKS | Menggugah mahasiswa: Apa dampaknya jika sensor suhu turbin bernilai `None` dan program langsung crash tanpa mitigasi? |
| **Menit 026 - 060** | Arsitektur Pohon Eksepsi CPython & Siklus 4-Blok Deterministik | Diagram hierarki `BaseException`, live coding `try-except-else-finally` | Menekankan bahaya *bare except* dan melatih pemisahan alur sukses murni (`else`) dari zona risiko (`try`). |
| **Menit 061 - 095** | Hierarki Eksepsi Kustom Domain Sawit & Exception Chaining (PEP 3134) | Live coding pembuatan kelas turunan, demonstrasi `raise ... from ...` | Menunjukkan bagaimana mengemas galat teknis tingkat rendah ke dalam bahasa agronomis tanpa menghilangkan jejak stack trace asli. |
| **Menit 096 - 125** | Arsitektur Logging Terstruktur Multi-Handler: Mengapa `print()` Dilarang? | Konfigurasi `RotatingFileHandler` & `StreamHandler`, simulasi rotasi berkas | Membimbing mahasiswa membangun pipeline monitoring industri yang kebal terhadap kepenuhan hard disk (*disk full*). |
| **Menit 126 - 150** | Refleksi Teori & Bedah Soal HOTS: PDB Interaktif, `__cause__`, & Forensik K3 | Analisis tumpukan panggilan (*traceback*), latihan perintah dasar `pdb` | Memandu mahasiswa memahami teknik stepping kode di runtime menggunakan `breakpoint()`. |
| **Praktikum (150m)**| Eksperimen Jupyter: Monitoring Boiler PKS, Sanitasi Sinyal, & Audit TBS | Praktikum komputasi terpandu di Jupyter Notebook | Memfasilitasi mahasiswa menyelesaikan 3 tantangan mandiri dengan verifikasi 100% bebas galat sintaksis. |

---

## 2. Miskonsepsi Umum Mahasiswa & Panduan Remedial

### Miskonsepsi 1: Menulis Pernyataan `except:` Kosong (*Bare Except Anti-Pattern*)
* **Gejala Mahasiswa:** Menulis `try: ... except: pass` dengan alasan agar *"program tidak pernah mengeluarkan pesan error"*.
* **Strategi Remedial:** Tunjukkan demonstrasi langsung di terminal kelas: jalankan loop tanpa akhir di dalam blok `except: pass`. Minta mahasiswa menekan `Ctrl+C`. Program **TIDAK AKAN BISA DIHENTIKAN** karena `except:` kosong menangkap `KeyboardInterrupt` yang diturunkan dari `BaseException`. Mahasiswa terpaksa mematikan terminal secara paksa lewat Task Manager. Tanamkan prinsip mutlak: **selalu tangkap kelas `Exception` atau subkelas spesifiknya, dan jangan pernah menggunakan bare except**.

### Miskonsepsi 2: Menelan Eksepsi Secara Senyap (*Swallowing Exceptions Anti-Pattern*)
* **Gejala Mahasiswa:** Menulis `except Exception as e: pass` sehingga ketika terjadi galat fatal, program tetap berjalan dengan variabel bernilai kosong atau korup, memicu kegagalan berantai di modul lain yang jauh lebih sulit dilacak.
* **Strategi Remedial:** Ajarkan bahwa menangkap eksepsi bertujuan untuk **memitigasi atau mencatat**, bukan menyembunyikan masalah. Jika program tidak tahu cara memperbaiki galat tersebut, program wajib mencatatnya ke logger (`logger.error(..., exc_info=True)`) atau melemparkannya kembali (*re-raise*) agar operator sistem menyadari adanya kerusakan perangkat keras.

### Miskonsepsi 3: Mengira Blok `finally:` Tidak Akan Dieksekusi Jika Ada `return` di Blok `try:`
* **Gejala Mahasiswa:** Khawatir bahwa katup penutup darurat di blok `finally:` tidak akan dieksekusi jika fungsi telah mengembalikan nilai lebih awal (*early return*) di dalam blok `try:`.
* **Strategi Remedial:** Lakukan live coding fungsi sederhana yang memuat `return 1` di dalam `try:`, dan `print("FINALLY JALAN")` di dalam `finally:`. Buktikan bahwa pesan *"FINALLY JALAN"* tetap muncul sebelum nilai `1` diterima oleh pemanggil. Jelaskan aturan CPython: interpreter menahan nilai kembalian di register, mengeksekusi seluruh instruksi di dalam `finally:` hingga tuntas, baru kemudian menyelesaikan lompatan keluar fungsi.

### Miskonsepsi 4: Menggunakan `print()` untuk Menampilkan Pesan Kesalahan di Server Produksi
* **Gejala Mahasiswa:** Menggunakan `print("Error: Sensor mati")` untuk mencatat anomali sistem IoT kebun.
* **Strategi Remedial:** Tunjukkan kelemahan fatal `print()`: tidak memiliki timestamp detik, tidak mencatat nama modul atau nomor baris, tidak dapat disaring berdasarkan tingkat keparahan (*severity filter*), dan hilang tanpa bekas jika aplikasi berjalan di latar belakang (*daemon process*). Ajarkan standardisasi modul **`logging`** industri dengan rotasi berkas otomatis.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Semantik Arsitektur CPython: Mengapa `BaseException` Dilarang Ditangkap dalam Logika Bisnis?
* **Soal:**
  1. Jelaskan struktur pewarisan antara `BaseException`, `KeyboardInterrupt`, `SystemExit`, dan `Exception`!
  2. Apa dampak fatal yang terjadi pada sistem otomasi pabrik kelapa sawit jika seorang programmer menulis `try: ... except BaseException: pass` pada loop kontrol mesin konveyor buah?
* **Jawaban Komprehensif:**
  1. **Hierarki Kelas dan Desain Pemisahan PEP 352:**
     - Dalam Python 2, `KeyboardInterrupt` dan `SystemExit` diturunkan dari `Exception`. Hal ini sering menyebabkan kode `except Exception:` secara tidak sengaja menangkap sinyal terminasi sistem.
     - Sejak Python 3.0 (PEP 352), CPython merestrukturisasi hierarki dengan memperkenalkan **`BaseException`** sebagai kelas akar tertinggi:
       - `BaseException` menurunkan langsung: `SystemExit`, `KeyboardInterrupt`, `GeneratorExit`, dan `Exception`.
       - `Exception` menjadi induk dari seluruh galat komputasi normal (`ValueError`, `TypeError`, `OSError`, dll).
     - Pemisahan ini dirancang agar penangkapan `except Exception:` secara aman hanya menangkap galat aplikasi tanpa mengganggu sinyal kontrol sistem operasi.
  2. **Dampak Fatal Bare BaseException pada Pabrik Sawit:**
     - Jika programmer menulis `except BaseException: pass` pada kontrol konveyor:
       - Saat terjadi keadaan darurat (misal tangan pekerja tersangkut atau motor overheating) dan operator menekan tombol stop darurat terminal (`Ctrl+C`), sinyal `KeyboardInterrupt` akan **ditelan dan diabaikan** oleh loop, konveyor tetap melaju!
       - Saat sistem operasi atau pengawas proses (*process supervisor* seperti systemd/supervisord) mengirim sinyal `SIGTERM` / `SystemExit` untuk mematikan mesin secara teratur, program menolak mati, menjadi proses zombie yang tidak dapat dihentikan kecuali melalui pembunuhan paksa kernel (`kill -9`).

---

### Pertanyaan 2: Dekonstruksi Mekanisme Exception Chaining: `__cause__` vs `__context__` (PEP 3134)
* **Soal:**
  1. Jelaskan perbedaan semantik antara atribut eksepsi `__cause__` dan `__context__` pada Python modern!
  2. Bagaimana penulisan `raise NewError from None` digunakan untuk menekan jejak stack trace lama (*traceback suppression*) demi keamanan sistem?
* **Jawaban Komprehensif:**
  1. **Semantik `__cause__` vs `__context__`:**
     - **`__cause__` (Eksplisit via `raise ... from err`):**  
       Menunjukkan bahwa pemrogram secara sadar dan sengaja mentransformasikan satu eksepsi menjadi eksepsi lain (*Explicit Exception Chaining*). Atribut `__cause__` menyimpan referensi ke `err`. Traceback akan menampilkan: *"The above exception was the direct cause of the following exception"*.
     - **`__context__` (Implisit / Tak Sengaja):**  
       Jika di dalam blok `except E1:` terjadi eksepsi baru `E2` secara tidak sengaja (misal mencoba menulis log ke disk tapi disk penuh), CPython secara otomatis mengikatkan `E1` ke atribut `E2.__context__`. Traceback akan menampilkan: *"During handling of the above exception, another exception occurred"*.
  2. **Pencegahan Kebocoran Informasi via `raise NewError from None`:**
     - Jika sebuah fungsi API pabrik sawit menangkap galat internal yang memuat informasi sensitif (seperti path direktori server, password database timbangan, atau query SQL mentah), menampilkan seluruh jejak stack trace asli ke pengguna luar merupakan celah keamanan (*Information Disclosure Vulnerability*).
     - Dengan menulis `raise AutentikasiGagalError("Kredensial tidak valid") from None`, CPython secara eksplisit memutus rantai `__suppress_context__ = True` dan menyetel `__cause__ = None`. Jejak stack trace teknis tingkat rendah akan disembunyikan secara permanen dari layar, hanya menyisakan pesan eksepsi publik yang bersih dan aman.

---

### Pertanyaan 3: Analisis Rekayasa Keandalan Perangkat Lunak: Logging vs Print & Disk Saturation
* **Soal:**
  1. Analisislah mengapa penggunaan pernyataan `print()` untuk debugging dapat melumpuhkan performa I/O sistem AI yang memproses ribuan telemetri per detik!
  2. Jelaskan konsep *Buffer Flushing* dan mekanisme kerja `RotatingFileHandler` dalam mencegah terjadinya kegagalan *Disk Full Emergency* pada server PKS!
* **Jawaban Komprehensif:**
  1. **Dampak Performa I/O Pernyataan `print()`:**
     - Secara default, fungsi `print()` menulis ke aliran `sys.stdout` yang terikat pada konsol terminal atau antarmuka GUI.
     - Penulisan ke terminal adalah operasi sinkron yang sangat lambat karena melibatkan rendering grafis font teks dan scrolling baris pada kartu grafis/jendela konsol. Jika sebuah model AI memproses 10.000 pembacaan sensor per detik dan setiap pembacaan mencetak `print()`, CPU akan menghabiskan lebih dari 90% waktu komputasinya hanya menunggu terminal menyelesaikan render teks (*I/O bound bottleneck*), melumpuhkan throughput model AI.
  2. **Mekanisme Buffer Flushing & RotatingFileHandler:**
     - **Buffer Flushing:** Modul `logging` mengumpulkan rekaman log di buffer memori RAM dan mengeluarkannya ke disk secara berkala dalam blok-blok besar. Ini meminimalkan overhead *system call* ke media penyimpanan SSD/HDD.
     - **Pencegahan Disk Full via `RotatingFileHandler`:**  
       Jika server PKS di pelosok kebun dibiarkan mencatat log ke satu berkas tanpa batas, dalam beberapa bulan berkas log akan membesar hingga puluhan gigabyte dan menghabiskan sisa kapasitas partisi sistem operasi (*Disk Full Emergency*), menyebabkan crash fatal pada database pabrik.
       `RotatingFileHandler(maxBytes=5_000_000, backupCount=3)` secara otomatis memantau ukuran berkas. Saat berkas mencapai 5 MB, berkas ditutup dan diganti namanya menjadi `.log.1`, berkas lama digeser ke `.log.2`, dan berkas paling tua di atas `backupCount` akan dihapus secara otomatis. Total konsumsi memori disk dijamin **terkunci rapat maksimal $\approx 20$ MB**, menjamin server kebun dapat beroperasi tanpa henti selama bertahun-tahun.

---

## 4. Kunci Solusi Tantangan Praktikum (Scaffolded Challenges)

### Solusi Tantangan 1: Konversi Telemetri Kebun yang Tangguh
```python
def konversi_suhu_tangguh(nilai_str: str, nilai_default: float = 25.0) -> float:
    """Mengonversi string telemetri ke float secara tangguh terhadap data korup.

    Args:
        nilai_str: String input pembacaan sensorik.
        nilai_default: Nilai pengganti jika konversi gagal.

    Returns:
        float: Nilai numerik hasil parsing atau nilai default aman.
    """
    try:
        hasil = float(nilai_str)
    except (ValueError, TypeError) as err:
        print(f"[RESCUE] Konversi gagal untuk '{nilai_str}' ({err}). Menggunakan default: {nilai_default}")
        return nilai_default
    else:
        print(f"[SUKSES] Parsing berhasil: {hasil:.2f}°C")
        return hasil
```

---

### Solusi Tantangan 2: Pemantauan Tekanan Pipa Irigasi dengan Eksepsi Kustom & Rantai Galat
```python
class TekananPipaIrigasiError(Exception):
    """Pengecualian khusus anomali tekanan jaringan pipa fertigasi kebun."""
    pass

def evaluasi_tekanan_irigasi(tekanan_raw: str, ambang_aman: float = 4.0) -> float:
    """Memvalidasi tekanan dan merantai eksepsi teknis ke eksepsi domain."""
    try:
        nilai = float(tekanan_raw)
    except ValueError as err:
        # Merantai ValueError ke TekananPipaIrigasiError
        raise TekananPipaIrigasiError(f"Format telemetri tekanan tidak valid: '{tekanan_raw}'") from err

    if nilai > ambang_aman:
        raise TekananPipaIrigasiError(f"Tekanan pipa kritis: {nilai:.2f} bar melebihi batas aman {ambang_aman:.2f} bar!")

    return nilai
```

---

### Solusi Tantangan 3: Pipeline Audit Sortasi TBS Terintegrasi Logging Multi-Handler
```python
import logging
import os
import sys

class KontaminasiSampahError(Exception):
    """Diterbitkan jika janjang TBS memuat kotoran sampah batu/pasir berlebih."""
    pass

class BuahMentahError(Exception):
    """Diterbitkan jika janjang TBS berada pada Fraksi 00/0 (mentah)."""
    pass

class EngineAuditSortasi:
    """Engine pemilah mutu janjang TBS dengan sistem logging terisolasi."""
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
            os.makedirs("sandbox_logs", exist_ok=True)
            path_log_penalti = os.path.join("sandbox_logs", "penalti_tbs.log")
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
```

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Kriteria Penilaian | Bobot | Sangat Kurang (< 50) | Kurang (50 - 69) | Memuaskan (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Arsitektur Penanganan Eksepsi (4-Blok)** | 25% | Menggunakan `except:` kosong; alur program rentan crash mendadak atau menelan KeyboardInterrupt. | Menggunakan `try-except` sederhana tanpa memanfaatkan blok `else` dan `finally`. | Menerapkan `try-except-else-finally` secara fungsional pada validasi operasi berisiko. | Arsitektur penanganan eksepsi paripurna: alur deterministik, pembersihan sumber daya mutlak, kebal terhadap crash. |
| **Perancangan Eksepsi Kustom & Chaining** | 25% | Hanya melempar `Exception` bawaan umum; pesan kesalahan tidak terstruktur. | Membuat kelas eksepsi kustom namun tidak menggunakan rantai galat (`raise ... from ...`). | Mampu membuat hierarki eksepsi agribisnis dan mengaitkan penyebab asal via `raise ... from err`. | Hierarki eksepsi domain komprehensif, metadata kesalahan kaya konteks, dan preservasi stack trace sempurna. |
| **Pipeline Logging Terstruktur Standar Industri** | 25% | Masih mengandalkan pernyataan `print()` untuk monitoring dan penanganan error. | Menggunakan modul `logging` tetapi hanya konfigurasi dasar tanpa handler terpisah. | Mampu mengonfigurasi logger dengan `StreamHandler` dan `FileHandler` serta format waktu rapi. | Merancang pipeline logging enterprise: integrasi `RotatingFileHandler`, filter level ketat, dan pelacakan exc_info. |
| **Teknik Debugging & Kualitas Perangkat Lunak** | 25% | Tidak mampu membaca traceback; debugging dilakukan dengan menebak baris kode. | Membaca traceback dasar namun tidak menguasai fungsi modul `traceback` atau `breakpoint()`. | Mampu mengisolasi lokasi terjadinya galat dan memformat traceback secara programatis. | Mahir melakukan debugging interaktif via `pdb` (`breakpoint()`), kode memenuhi standar PEP 8, bersih, dan tangguh. |

---

## 6. Rekomendasi Alur Penyampaian & Tips Pedagogis

1. **Jadikan Skenario "Ketel Uap Meledak" sebagai Pengingat Disiplin Kode:**  
   Tekankan kepada mahasiswa bahwa dalam dunia komputasi industri agribisnis (PKS, irigasi, drone pemetaan), galat program bukan sekadar layar biru di monitor, melainkan dapat memicu ledakan fisik mesin uap bersuhu $300^\circ\text{C}$ atau kerusakan pompa bernilai ratusan juta rupiah. Disiplin penanganan eksepsi adalah bagian dari etika profesi insinyur kecerdasan buatan.
2. **Praktikkan Sesi "Live Debugging via PDB":**  
   Sisipkan perintah `breakpoint()` di tengah fungsi evaluasi boiler. Ketika terminal beralih ke prompt `(Pdb)`, pandu mahasiswa mengetik `p tekanan`, `n`, dan `w`. Pengalaman interaktif ini akan menghilangkan ketakutan mahasiswa terhadap pesan galat merah dan menumbuhkan rasa percaya diri dalam menginvestigasi bug sistemik.
3. **Bandingkan Berkas Log Sebelum dan Sesudah Rotasi:**  
   Buka folder log di proyektor kelas. Tunjukkan bagaimana sebuah berkas log yang terus bertambah akan otomatis berganti nama menjadi `.log.1` dan file baru terbentuk. Mahasiswa akan langsung memahami betapa elegan dan amannya modul `logging` dibandingkan penulisan berkas teks manual `f.write()`.
