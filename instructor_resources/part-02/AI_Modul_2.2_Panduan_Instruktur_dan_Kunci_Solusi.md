# Panduan Instruktur & Kunci Solusi: AI Modul 2.2
## Flowchart dan Pseudocode: Desain Logika Komputasional & Pipeline Inferensi AI

---

**Kode Modul:** AI Modul 2.2  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Dasar Algoritma & Logika Pemrograman untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi & Analogi PKS: Mengapa kita butuh cetak biru diagramatik sebelum coding? | Ceramah interaktif, Studi kasus pabrik kelapa sawit modern | Memicu diskusi: Apa yang terjadi jika teknisi membangun pabrik tanpa PFD? |
| **Menit 026 - 065** | Standar ANSI/ISO 5807, Makna Simbol, dan Larangan Struktural | Presentasi visual, Bedah diagram benar vs salah | Menjelaskan batas toleransi bentuk simbol dan integritas percabangan. |
| **Menit 066 - 100** | Sintaksis Pseudocode Formal & Translasi Logika Piecewise | Papan tulis/Live markdown, Dekonstruksi notasi matematika | Membimbing mahasiswa menulis pseudocode dengan indentasi teratur. |
| **Menit 101 - 130** | Praktik Penelusuran Kering (*Dry-Run Trace Table*) | Lembar kerja manual (*paper & pencil exercise*) | Mengawasi mahasiswa mengisi tabel status variabel untuk menemukan *edge case*. |
| **Menit 131 - 150** | Refleksi Teori & Pengantar Tantangan Praktikum | Tanya jawab HOTS, Pengenalan environment Jupyter | Merangkum prinsip *defensive programming* dan *short-circuit evaluation*. |
| **Praktikum (150m)**| Implementasi Python: Visualisasi Flowchart & Engine Simulator | Hands-on coding di Jupyter Notebook / Google Colab | Memandu penyelesaian tantangan berjenjang (Dasar, Menengah, Mahir). |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Menyamakan Diagram Alir (*Flowchart*) dengan *Data Flow Diagram* (DFD)
* **Gejala Mahasiswa:** Menghubungkan panah dari satu kotak proses ke kotak proses lain dengan maksud menggambarkan "aliran perpindahan data/file" bukan "urutan waktu eksekusi instruksi kontrol".
* **Strategi Remedial:** Tegaskan bahwa panah dalam *flowchart* adalah **Aliran Kendali (*Control Flow*)** yang merepresentasikan perpindahan *Program Counter* (PC) CPU dari satu langkah ke langkah berikutnya. Untuk aliran data murni tanpa sekuensial waktu kontrol, gunakan DFD.

### Miskonsepsi 2: Mengabaikan Label Cabang pada Simbol *Decision*
* **Gejala Mahasiswa:** Menggambar belah ketupat keputusan dengan dua panah keluar, namun tidak menuliskan teks "Ya/True" atau "Tidak/False".
* **Strategi Remedial:** Tunjukkan bahwa komputer adalah mesin deterministik biner. Tanpa label eksplisit, interpreter atau penerjemah logika tidak tahu cabang mana yang dieksekusi saat evaluasi predikat bernilai *True*. Setiap belah ketupat yang tidak berlabel wajib langsung diberi nilai nol pada aspek sintaksis.

### Miskonsepsi 3: Pengujian Kesetaraan Ketat (`==` atau `!=`) pada Variabel *Floating-Point*
* **Gejala Mahasiswa:** Menulis kondisi perulangan seperti `WHILE posisi != 15.0 DO posisi = posisi + 0.7`.
* **Strategi Remedial:** Ingatkan representasi bilangan pecahan biner IEEE 754. Penambahan $0.7$ berulang kali mengakibatkan akumulasi galat pembulatan (*round-off error*), misalnya $14.999999999999998$ lalu melompat ke $15.699999999999998$. Nilai tidak pernah tepat sama dengan $15.0$, memicu **Infinite Loop**. Mahasiswa harus dilatih menggunakan operator relasional bertoleransi: `WHILE posisi < 15.0 - epsilon`.

### Miskonsepsi 4: Mengira Pseudocode Harus Mengikuti Sintaksis Python Murni
* **Gejala Mahasiswa:** Menolak menuliskan tipe data atau menuliskan kode Python dengan titik dua (`:`) dan *list comprehension* rumit dalam lembar pseudocode.
* **Strategi Remedial:** Jelaskan bahwa pembaca pseudocode bisa jadi adalah insinyur elektro pengembang PLC (C/C++ atau Ladder Logic) atau analis bisnis. Pseudocode harus netral bahasa dan fokus pada kejernihan logika struktural tingkat tinggi.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Infinite Loop pada Kalibrasi Robot Lengan
* **Inti Masalah:** Kondisi `WHILE posisi_lengan != 15.0 DO posisi_lengan <- posisi_lengan + 0.7`. Dimulai dari $10.0$:
  - Langkah 1: $10.0 + 0.7 = 10.7$
  - Langkah 2: $10.7 + 0.7 = 11.4$
  - ...
  - Langkah 7: $14.2 + 0.7 = 14.9$
  - Langkah 8: $14.9 + 0.7 = 15.6$
  - Nilai $15.0$ terlewati! Nilai variabel melompat dari $14.9$ ke $15.6$. Karena predikat komparasi adalah kesetaraan ketat ketaksamaan (`!=`), kondisi terus bernilai `TRUE` selamanya. Lengan robot akan terus bergerak tanpa batas dan dapat merusak aktuator mekanis atau menabrak dinding penampung buah.
* **Solusi Perbaikan Diagram & Pseudocode:**
  Ganti simbol operator dari `!=` menjadi batas relasional toleransi:
  ```text
  SET target_posisi <- 15.0
  SET toleransi <- 0.05
  WHILE posisi_lengan < (target_posisi - toleransi) DO
      posisi_lengan <- posisi_lengan + 0.7
  ENDWHILE
  ```

### Pertanyaan 2: Evaluasi Ketahanan Ambang Batas Akibat Penurunan Cahaya (*Data Drift*)
* **Analisis Dampak Operasional:** Jika intensitas cahaya mendung menurunkan output probabilitas model $P(x)$ sebesar $15\%$ secara sistemik:
  - Buah yang seharusnya bernilai $P = 0.88$ (Grade A) akan terbaca sebagai $0.88 \times 0.85 = 0.748$.
  - Akibatnya: Buah Grade A yang matang sempurna salah disortir (*misclassified*) menjadi Grade B (Mengkal) dan dialihkan ke area pemeraman. Ini menimbulkan kerugian finansial karena keterlambatan waktu olah di stasiun perebusan (*sterilizer*).
* **Solusi Modifikasi Arsitektur Flowchart:**
  Tambahkan modul **Predefined Process: Kalibrasi Cahaya Adaptif** sebelum modul ekstraksi citra:
  1. Pasang sensor lux meter atau baca histogram luminansi rata-rata frame citra.
  2. Hitung faktor koreksi pencahayaan $\gamma$.
  3. Lakukan normalisasi kontras (*Histogram Equalization* / *Gamma Correction*) sebelum citra diumpankan ke model AI, ATAU sesuaikan nilai ambang batas $\theta$ secara dinamis: $\theta_{\text{high}}^{\text{adj}} = \theta_{\text{high}} \times (1 - \text{drift\_factor})$.

### Pertanyaan 3: Sintesis Desain Subrutin (*Modular Architecture*)
* **Analisis & Solusi:**
  Dalam sistem kendali penyemprotan drone otonom perkebunan kelapa sawit, satu diagram raksasa akan menimbulkan *cognitive overload*. Kita menerapkan prinsip **Dekomposisi Fungsional**:
  - **Diagram Alir Utama (*Main Orchestrator*):** Hanya memuat loop navigasi global:
    `[START] -> [Predefined: NavigasiWaypoint()] -> [Predefined: DeteksiHama()] -> [Predefined: KendaliSprayer()] -> [Decision: BateraiHabis?] -> [STOP]`.
  - **Diagram Subrutin Terpisah:**
    Masing-masing modul didokumentasikan dalam lembar tersendiri dengan pintu masuk Terminator subrutin `START DeteksiHama(frame)` dan pintu keluar `RETURN koordinat_hama, skor_keparahan`.
  - **Keuntungan Industri:** Memungkinkan tim pengembang perangkat keras, tim visi komputer, dan tim navigasi bekerja secara paralel pada berkas modul yang terisolasi.

---

## 4. Kunci Solusi Lengkap Tantangan Pemrograman Scaffolded

### Solusi Tantangan 2 (Tingkat Menengah): Deteksi Anomali GPS Drone dengan Fault Counter

#### Representasi Pseudocode Terstruktur:
```text
ALGORITMA Deteksi_Anomali_GPS_Drone
DEKLARASI:
    counter_kegagalan : Integer
    maks_toleransi    : Integer
    status_gps        : Boolean
    status_terbang    : Boolean
    koordinat_saat_ini: Vector_Geo

INISIALISASI:
    SET counter_kegagalan <- 0
    SET maks_toleransi    <- 3
    SET status_terbang    <- True

START
    WHILE status_terbang == True DO
        INPUT status_gps, koordinat_saat_ini DARI Receiver_GPS
        
        IF status_gps == True THEN
            // Sinyal normal: Reset counter kegagalan ke nol
            SET counter_kegagalan <- 0
            PRINT "GPS Terkunci: Navigasi ke Koordinat ", koordinat_saat_ini
            CALL Lanjutkan_Penerbangan_Misi()
        ELSE
            // Pembacaan anomali terdeteksi
            SET counter_kegagalan <- counter_kegagalan + 1
            PRINT "[PERINGATAN] Sinyal GPS Terputus! Jumlah Gagal Berturut-turut: ", counter_kegagalan
            
            // Evaluasi ambang batas kegagalan kritis
            IF counter_kegagalan >= maks_toleransi THEN
                PRINT "[BAHAYA] Ambang Batas Tercapai! Memulai Protokol Pendaratan Darurat."
                CALL Protokol_Emergency_Landing()
                SET status_terbang <- False
            ELSE
                PRINT "Mengaktifkan Sensor Inertial (IMU) Dead-Reckoning Sementara."
                CALL Tahan_Posisi_Hover()
            ENDIF
        ENDIF
        
        WAIT 0.5 DETIK
    ENDWHILE
    
    PRINT "Misi Penerbangan Dihentikan."
END
```

#### Implementasi Python Deterministik:
```python
import time
from typing import List, Tuple


def simulasi_anomali_gps(sinyal_gps_stream: List[bool]) -> None:
    counter_kegagalan = 0
    maks_toleransi = 3
    status_terbang = True

    print("=" * 70)
    print("SIMULASI FAULT TOLERANCE KONTROL PENERBANGAN DRONE PERKEBUNAN")
    print("=" * 70)

    for detik, sinyal_gps in enumerate(sinyal_gps_stream, 1):
        if not status_terbang:
            break

        print(
            f"T+{detik*0.5:04.1f}s | Status Sinyal GPS: {'TERKUNCI' if sinyal_gps else 'HILANG':<8} | ",
            end="",
        )

        if sinyal_gps:
            counter_kegagalan = 0
            print(
                f"Counter Gagal: {counter_kegagalan} | Navigasi Normal (Waypoint Aktif)"
            )
        else:
            counter_kegagalan += 1
            print(
                f"Counter Gagal: {counter_kegagalan} | [PERINGATAN] Glitch Sensor Terdeteksi"
            )

            if counter_kegagalan >= maks_toleransi:
                print(
                    f"       --> [EMERGENCY] Gagal berturut-turut {maks_toleransi}x! Pendaratan Darurat Diaktifkan!"
                )
                status_terbang = False
            else:
                print(
                    f"       --> Bertahan di Udara (Hover IMU Mode). Menunggu sinyal pulih..."
                )

    print("=" * 70)
    print(
        f"Status Akhir Drone: {'TERBANG NORMAL' if status_terbang else 'MENDARAT DARURAT (FAIL-SAFE)'}\n"
    )


# Uji Kasus: Gagal 2x lalu pulih, kemudian gagal 3x berturut-turut
stream_uji = [
    True,
    True,
    False,
    False,
    True,
    False,
    False,
    False,
    True,
]  # Harusnya darurat di indeks ke-7
simulasi_anomali_gps(stream_uji)
```

---

### Solusi Tantangan 3 (Tingkat Mahir): Multi-Kriteria Kernel Sawit (FFA & Kadar Air)

```python
from typing import Any, Dict, List, Tuple


def evaluasi_mutu_kernel(ffa_input: Any, air_input: Any) -> Tuple[str, str]:
    """Mengklasifikasikan mutu inti sawit berdasarkan kadar FFA dan Air dengan validasi tipe data."""
    # 1. Validasi Keamanan Masukan (Defensive Type Checking)
    try:
        ffa = float(ffa_input)
        air = float(air_input)
    except (ValueError, TypeError):
        return "DATA_INVALID", "REJECT_DATA: Nilai masukan bukan numerik valid"

    if ffa < 0.0 or air < 0.0 or ffa > 100.0 or air > 100.0:
        return (
            "OUT_OF_BOUNDS",
            "REJECT_DATA: Persentase di luar rentang fisik (0-100%)",
        )

    # 2. Percabangan Hierarkis Penentuan Mutu
    # Mutu Super: FFA <= 2.5% DAN Air <= 6.0%
    if ffa <= 2.5 and air <= 6.0:
        return "MUTU_SUPER", "SIMPAN_KE_SILO_EKSPOR_GRADE_1"
    # Mutu Standar: FFA <= 4.0% DAN Air <= 8.0%
    elif ffa <= 4.0 and air <= 8.0:
        return "MUTU_STANDAR", "SIMPAN_KE_SILO_DOMESTIK"
    # Mutu Rendah: Melebihi batas standar
    else:
        alasan = []
        if ffa > 4.0:
            alasan.append(f"FFA tinggi ({ffa:.1f}%)")
        if air > 8.0:
            alasan.append(f"Air tinggi ({air:.1f}%)")
        return "MUTU_RENDAH", f"REJECT_PENGOLAHAN: {', '.join(alasan)}"


# Pengujian Komprehensif
sampel_kernel = [
    {"batch": "KRN-01", "ffa": 1.8, "air": 5.2},  # Super
    {"batch": "KRN-02", "ffa": 3.2, "air": 7.1},  # Standar
    {"batch": "KRN-03", "ffa": 4.8, "air": 5.5},  # Rendah (FFA)
    {"batch": "KRN-04", "ffa": 2.1, "air": 9.0},  # Rendah (Air)
    {"batch": "KRN-05", "ffa": "RUSAK", "air": 6.0},  # Invalid non-numeric
    {"batch": "KRN-06", "ffa": -2.0, "air": 5.0},  # Out of bounds
]

print("=" * 85)
print("HASIL EVALUASI MUTU KERNEL SAWIT MULTI-KRITERIA (FFA & KADAR AIR)")
print("=" * 85)
for s in sampel_kernel:
    grade, aksi = evaluasi_mutu_kernel(s["ffa"], s["air"])
    print(
        f"Batch: {s['batch']} | FFA: {str(s['ffa']):<6} | Air: {str(s['air']):<6} | Kategori: {grade:<14} | Aksi: {aksi}"
    )
print("=" * 85)
```

---

## 5. Rubrik Penilaian Praktikum Mahasiswa

Total Bobot: **100 Poin**

| Kriteria Penilaian | Bobot | Indikator Kinerja Unggul (Poin Penuh) | Indikator Kinerja Kurang (Poin Minimal) |
| :--- | :---: | :--- | :--- |
| **Kesesuaian Simbol ANSI/ISO** | **25%** | Menggunakan bentuk geometris yang tepat; semua panah keputusan memiliki label `Ya/Tidak`; hanya memiliki 1 `START` dan `STOP`. | Menggunakan kotak biasa untuk percabangan; panah keluar tanpa label; garis saling silang tanpa konektor. |
| **Struktur & Konvensi Pseudocode** | **25%** | Kata kunci huruf besar terstruktur; indentasi 4 spasi konsisten; penutup blok eksplisit (`ENDIF`, `ENDWHILE`); nama variabel deskriptif. | Menulis paragraf bebas; mencampurkan sintaksis spesifik Python tanpa struktur hierarkis yang jelas. |
| **Akurasi Logika & Trace Table** | **25%** | Tabel jejak mencatat perubahan nilai variabel dengan tepat; mendeteksi *short-circuit evaluation*; mampu mengidentifikasi *edge case*. | Perhitungan manual salah; tidak memahami urutan evaluasi kondisi majemuk; gagal menemukan *infinite loop*. |
| **Kualitas Kode Python & Ketahanan** | **25%** | Kode bersih beranotasi tipe (*type hinting*); menerapkan *defensive programming*; 100% lulus seluruh *test suite* tanpa *runtime error*. | Kode tidak modular; memicu *ValueError* atau *KeyError* saat diberi masukan tak biasa; penamaan variabel tidak jelas. |
