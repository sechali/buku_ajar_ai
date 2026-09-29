# Panduan Instruktur dan Kunci Solusi
# AI Modul 4.7: Membaca Dataset (CSV/Excel)

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) Berbasis OBE (3 SKS / 150 Menit)

Modul ini membekali mahasiswa Sarjana Sains Data, Kecerdasan Buatan, dan Teknik Pertanian dengan kecakapan teknis dalam mengekstrak, mengonfigurasi skema tipe data, mengatasi anomali berkas, serta melakukan ingesti data berskala besar dari format berkas terdelimitasi (CSV), buku kerja lembar sebar (Excel XLSX), hingga format biner kolumnar modern (Apache Parquet).

### 1.1 Matriks Alokasi Waktu Sesi Perkuliahan (150 Menit)

| Alokasi Waktu | Aktivitas Pembelajaran | Metode & Media | Peran Instruktur | Target Capaian Mahasiswa |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20 menit) | **Refleksi & *Problem Framing*:** Studi kasus kegagalan migrasi data pabrik kelapa sawit akibat *Out-Of-Memory* (OOM) dan *UnicodeDecodeError*. | Presentasi interaktif & bedah kasus korupsi I/O. | Memantik diskusi kritis terkait integritas I/O pada sistem analitik kebun. | Mahasiswa memahami bahwa pembacaan data bukan sekadar memanggil `read_csv()`, melainkan melibatkan manajemen skema memori. |
| **00:20 - 00:50** (30 menit) | **Dekonstruksi Teori & Arsitektur Mesin Parser:** Bedah C Engine vs Python Engine vs PyArrow Engine, serta perbandingan CSV vs Excel vs Parquet. | Ceramah teknis, demonstrasi skema diagram arsitektur. | Menjelaskan *trade-off* antara latensi eksekusi, kebutuhan RAM, dan portabilitas format. | Mahasiswa memetakan karakteristik struktural berkas teks datar vs arsip XML terkompresi ZIP. |
| **00:50 - 01:25** (35 menit) | **Praktikum Terbimbing (Hands-on Lab):** Eksperimen parameter kritis `pd.read_csv()`, ingesti multi-sheet via `pd.ExcelFile`, dan implementasi *chunking iterator*. | Live coding terbimbing di Jupyter Notebook. | Mendampingi mahasiswa mengonfigurasi `sep`, `dtype`, `decimal`, dan iterator bongkahan. | Mahasiswa sukses menjalankan skrip ekstraksi data multi-sumber tanpa galat sintaksis. |
| **01:25 - 02:10** (45 menit) | **Penyelesaian Kasus HOTS Mandiri:** Pengerjaan tantangan parsing berkas korup (9.1) dan *streaming aggregator* telemetri sensor iklim 15 juta baris (9.2). | Kerja mandiri berpasangan (*pair programming*). | Berkeliling memfasilitasi *debugging*, memeriksa profil konsumsi RAM mahasiswa. | Mahasiswa mampu menulis algoritma agregasi bertahap dengan batas memori ketat. |
| **02:10 - 02:30** (20 menit) | **Evaluasi Formatif & Sintesis Solusi:** Pembahasan solusi kunci, analisis kompleksitas waktu/ruang, dan pengenalan format Apache Parquet. | Diskusi pleno, *code review* silang antar kelompok. | Menyimpulkan prinsip *clean I/O pipeline* dan memberikan umpan balik OBE terukur. | Mahasiswa menginternalisasi standar profesional penanganan data berskala terabyte. |

---

## 2. Matriks Identifikasi & Remedi Miskonsepsi Umum Mahasiswa

| No | Miskonsepsi Mahasiswa | Realitas Teknis & Konseptual | Pendekatan Remedi Instruktur |
| :--- | :--- | :--- | :--- |
| 1 | "Fungsi `pd.read_csv()` selalu dapat menebak tipe data kolom secara otomatis dengan sempurna tanpa perlu campur tangan pengguna." | Pandas menerapkan *type inference* berdasar sampel baris awal. Kolom kode pos atau ID sensor yang diawali angka nol (misal `'00452'`) akan terkonversi menjadi integer (`452`), menghilangkan angka nol di depan secara permanen (*silent data corruption*). | Tunjukkan contoh nyata di mana ID tiket timbangan kehilangan presisi. Wajibkan mahasiswa selalu mendefinisikan kamus `dtype` secara eksplisit untuk atribut identitas unik dan data kategorikal. |
| 2 | "Format Microsoft Excel (.xlsx) lebih unggul dan lebih andal dibanding CSV untuk menyimpan dataset analitik kecerdasan buatan karena tampilannya rapi dan mendukung rumus." | Berkas XLSX adalah arsip XML terkompresi yang memiliki batas fisik $1.048.576$ baris, overhead dekompresi sangat tinggi (memakan waktu $10\times - 50\times$ lebih lambat dari CSV/Parquet), dan memicu lonjakan RAM masif saat diurai oleh *openpyxl*. | Jalankan benchmark langsung di depan kelas yang membandingkan waktu baca berkas 100 ribu baris antara Excel, CSV, dan Parquet. Tunjukkan bahwa Excel ditujukan untuk laporan operasional manusia, bukan untuk *pipeline* AI berskala besar. |
| 3 | "Jika dataset terlalu besar untuk dimuat ke RAM, kita harus segera membeli server berkapasitas RAM ratusan gigabita atau menggunakan klaster komputasi terdistribusi." | Sebagian besar tugas analitika (seperti perhitungan total tonase, rata-rata curah hujan, frekuensi kategori) bersifat komutatif dan asosiatif, sehingga dapat diselesaikan pada komputer berspesifikasi rendah menggunakan strategi **Bongkahan (*Chunking Iterator*)**. | Berikan analogi *pompa air dan ember*: Anda tidak perlu memindahkan seluruh isi danau sekaligus ke dalam ruangan, cukup alirkan air melalui pipa per 10 liter secara berurutan. Pandu mahasiswa membangun agregator bertahap dengan parameter `chunksize`. |
| 4 | "Menyimpan data hasil pra-pemrosesan kembali ke format CSV adalah praktik terbaik karena CSV mudah dibuka di aplikasi mana pun." | Berkas CSV membuang semua informasi tipe data yang sudah diproses (semua kembali menjadi teks nir-tipe) dan tidak terkompresi. Ketika dimuat kembali pada sesi berikutnya, Pandas harus mengulang seluruh proses inferensi tipe yang lambat. | Wajibkan mahasiswa menggunakan format **Apache Parquet**. Jelaskan konsep *embedded schema* dan *column projection pushdown* yang mempercepat pemuatan data pelatihan model AI hingga belasan kali lipat. |

---

## 3. Panduan Solusi Lengkap Latihan HOTS (Higher-Order Thinking Skills)

### 3.1 Solusi Tantangan 9.1: Diagnosa Kerusakan File dan Parsing I/O (Bobot: 30%)

#### 1. Analisis `UnicodeDecodeError` dan Deteksi Karakter Enkoding Programatis:
- **Akar Masalah:** Mesin parser Pandas secara baku mengasumsikan berkas berenkoding `UTF-8`. Byte heksadesimal `0xe9` pada posisi 1450 merupakan representasi karakter beraksen seperti `é` dalam standar pengkodean halaman Windows barat (*Windows-1252 / CP1252*) atau *ISO-8859-1 (Latin-1)*. Dalam UTF-8, karakter multithreaded non-ASCII harus diawali oleh pasangan *lead byte* dan *continuation byte*. Munculnya `0xe9` tunggal melanggar tata bahasa UTF-8, memicu `UnicodeDecodeError`.
- **Deteksi Programatis Menggunakan Python:**
```python
import charset_normalizer

def deteksi_enkoding(file_path, n_bytes=200000):
    with open(file_path, 'rb') as f:
        raw_data = f.read(n_bytes)
    hasil = charset_normalizer.from_bytes(raw_data).best()
    if hasil is not None:
        return hasil.encoding
    return 'latin-1' # Fallback yang aman untuk karakter byte 0-255

enc = deteksi_enkoding('data_timbangan_pks_2025.csv')
print(f'Enkoding terdeteksi: {enc}')
```

#### 2. Penyebab Baris 4520 Menghasilkan 8 Kolom (Padahal Skema 6 Kolom):
- **Akar Masalah:** Terjadi fenomena *unquoted comma in free-text field* (pemisah koma tanpa tanda kutip di dalam kolom teks bebas).
- **Skenario Lapangan Agribisnis Riil:** Kolom ke-6 adalah `Catatan_Supir`. Pada baris 4520, supir menulis keterangan: `"TBS mentah, restan 2 hari, afdeling Charlie"`. Jika sistem input timbangan di PKS tidak membungkus teks tersebut dengan tanda petik ganda (`"`), parser C akan menganggap koma di dalam kalimat sebagai pembatas kolom baru, sehingga 1 baris terbelah menjadi 8 kolom (*field count mismatch*).

#### 3. Sintaks `pd.read_csv()` yang Tangguh dan Toleran Galat:
```python
import pandas as pd

df_kebun = pd.read_csv(
    'data_timbangan_pks_2025.csv',
    encoding='latin-1',            # Mengatasi UnicodeDecodeError
    on_bad_lines='warn',           # Mengabaikan baris korup & mencatat peringatan
    engine='c',                    # Kecepatan maksimal C engine
    dtype={'ID_Tiket': 'string', 'Kode_Afdeling': 'category', 'Berat_Kg': 'float32'}
)
print(f'Total baris valid yang berhasil dimuat: {len(df_kebun)}')
```

---

### 3.2 Solusi Tantangan 9.2: Arsitektur Pemrosesan Streaming Data Sensor Masif (Bobot: 40%)

```python
import os
import pandas as pd
import numpy as np

def proses_streaming_telemetri(file_csv, ukuran_bongkahan=100000):
    """
    Memproses dataset telemetri sensor 15 juta baris (6.5 GB) 
    pada komputer dengan RAM 4 GB (puncak konsumsi RAM < 300 MB).
    """
    kolom_relevan = ['Afdeling', 'Curah_Hujan', 'Baterai_Volt']
    skema_tipe = {
        'Afdeling': 'category',
        'Curah_Hujan': 'float32',
        'Baterai_Volt': 'float32'
    }
    
    # Inisialisasi struktur akumulator analitik
    akumulator = {}
    
    # Iterator bongkahan memori terkontrol
    chunk_iterator = pd.read_csv(
        file_csv,
        usecols=kolom_relevan,
        dtype=skema_tipe,
        chunksize=ukuran_bongkahan,
        engine='c'
    )
    
    total_baris_terproses = 0
    for i, chunk in enumerate(chunk_iterator):
        total_baris_terproses += len(chunk)
        
        # Buat indikator baterai lemah (vektor boolean cepat)
        chunk['Baterai_Lemah'] = (chunk['Baterai_Volt'] < 3.2).astype(np.int8)
        
        # Agregasi per afdeling pada bongkahan saat ini
        sub_agg = chunk.groupby('Afdeling', observed=False).agg(
            total_hujan=('Curah_Hujan', 'sum'),
            cacah_bacaan=('Curah_Hujan', 'count'),
            total_baterai_lemah=('Baterai_Lemah', 'sum')
        )
        
        # Akumulasikan ke rekapitulasi global
        for afd, row in sub_agg.iterrows():
            if afd not in akumulator:
                akumulator[afd] = {'total_hujan': 0.0, 'cacah': 0, 'baterai_lemah': 0}
            akumulator[afd]['total_hujan'] += row['total_hujan']
            akumulator[afd]['cacah'] += int(row['cacah_bacaan'])
            akumulator[afd]['baterai_lemah'] += int(row['total_baterai_lemah'])
            
    # Kalkulasi metrik final per afdeling
    daftar_hasil = []
    for afd, data in akumulator.items():
        if data['cacah'] > 0:
            rata_hujan = data['total_hujan'] / data['cacah']
            persen_baterai_lemah = (data['baterai_lemah'] / data['cacah']) * 100.0
            daftar_hasil.append({
                'Afdeling': afd,
                'Total_Pengukuran': data['cacah'],
                'Rata_Curah_Hujan_mm': round(rata_hujan, 3),
                'Persentase_Baterai_Lemah': round(persen_baterai_lemah, 2)
            })
            
    df_ringkasan = pd.DataFrame(daftar_hasil).sort_values('Afdeling').reset_index(drop=True)
    return df_ringkasan
```

- **Justifikasi Teknis Efisiensi Memori:**
  1. *Projection Pushdown (`usecols`):* Dari 7 kolom asal, hanya 3 kolom yang dibaca. Hal ini secara langsung memangkas alokasi I/O hingga $\approx 57\%$.
  2. *Spesifikasi Presisi Rendah (`float32`):* Mengurangi kebutuhan byte per float dari 8 byte (float64) menjadi 4 byte (float32).
  3. *Ukuran Bongkahan ($100.000$ baris):* Tiap bongkahan hanya membutuhkan memori kerja sekitar $\approx 100.000 \times 12 \text{ byte} \approx 1.2 \text{ MB}$, jauh di bawah batas toleransi $300 \text{ MB}$.

---

### 3.3 Solusi Tantangan 9.3: Evaluasi Efisiensi Format Data (Bobot: 30%)

#### 1. Perbedaan Row-Oriented vs Column-Oriented:
- **Row-Oriented (CSV):** Data tersimpan baris demi baris berurutan secara fisik di disk (`baris1_kolom1, baris1_kolom2, ..., baris2_kolom1`). Untuk membaca satu kolom tertentu (misal hanya kolom `Tonase`), sistem operasi terpaksa memindai dan membaca seluruh isi baris dari disk ke RAM.
- **Column-Oriented (Apache Parquet):** Data disusun per kolom (`kolom1_baris1, kolom1_baris2, ...`). Nilai pada kolom yang sama disimpan bersebelahan secara fisik di blok memori. Ini memungkinkan kompresi data homogen yang sangat tinggi serta pembacaan selektif (*projection pushdown*) tanpa menyentuh kolom lain di disk.

#### 2. Keuntungan Parquet bagi Algoritma Machine Learning (Random Forest / XGBoost):
1. **Fitur Proyeksi Selektif:** Algoritma pelatihan model kerap hanya membutuhkan subset fitur numerik hasil seleksi (*feature selection*). Parser Parquet melompati blok data kolom yang tidak relevan secara fisik di disk, memotong waktu I/O hingga $80\%-90\%$.
2. **Penyimpanan Skema Biner (*Zero Parsing Overhead*):** Nilai numerik integer dan float disimpan dalam format biner IEEE-754 asli. Komputer tidak perlu menjalankan fungsi konversi string teks ke representasi biner angka (*zero-copy parsing*).
3. **Penyaringan Statistik Blok (*Predicate Pushdown*):** Berkas Parquet menyimpan metadata nilai minimum dan maksimum per blok data. Jika skrip melakukan filtering `WHERE Afdeling == 'OA'`, blok data afdeling lain tidak pernah dimuat ke RAM.

#### 3. Kalkulasi Penghematan Ruang Disk:
- Ukuran data asal (CSV): $12 \text{ GB}$.
- Rasio kompresi rata-rata numerik Snappy Parquet: $1 : 4.5$.
$$\text{Ukuran Parquet Baru} = \frac{12 \text{ GB}}{4.5} \approx 2.67 \text{ GB}$$
$$\text{Penghematan Kapasitas (GB)} = 12 \text{ GB} - 2.67 \text{ GB} = 9.33 \text{ GB}$$
$$\text{Persentase Penghematan Disk} = \left( 1 - \frac{1}{4.5} \right) \times 100\% = \left( 1 - 0.2222 \right) \times 100\% \approx 77.78\%$$
Korporasi perkebunan menghemat sekitar **77.78% (atau 9.33 GB)** dari alokasi ruang penyimpanan disk mereka.

---

## 4. Rubrik Penilaian Portofolio Praktikum Berbasis OBE

| Kriteria Penilaian | Bobot | Sangat Memuaskan (85 - 100) | Memuaskan (70 - 84) | Kurang Memuaskan (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Ketepatan Konfigurasi I/O & Enkoding** | 25% | Mengidentifikasi enkoding non-standar, delimiter ganjil, dan koma desimal secara tepat dengan kode Python yang bersih dan otomatis. | Mampu membaca berkas dengan benar namun memerlukan *hard-coding* berulang dan *trial-and-error* manual. | Gagal menangani `UnicodeDecodeError` atau data tergeser kolom akibat pemisah tidak terkonfigurasi. |
| **Efisiensi Manajemen Memori & Skema Data** | 25% | Mendefinisikan kamus skema tipe data `dtype` eksplisit (`category`, `int32`, `float32`) dan proyeksi kolom `usecols` secara optimal. | Mendefinisikan tipe data namun masih ada redundansi tipe default float64/int64 yang memboroskan RAM. | Membaca seluruh kolom tanpa filter dengan tipe baku `object`, menyebabkan beban memori berlebih. |
| **Arsitektur Pemrosesan Data Masif (Chunking)** | 30% | Membangun *chunking iterator* bertahap yang modular, mampu mengagregasi data jutaan baris dengan batas konsumsi RAM rendah. | Menerapkan `chunksize` namun menyimpan seluruh chunk ke dalam satu list memori (masih memicu lonjakan RAM). | Tidak memahami mekanisme *chunking*, kode mengalami *MemoryError* saat membaca dataset besar. |
| **Analisis Performa & Format Parquet** | 20% | Mampu menyajikan benchmark kuantitatif (waktu baca/tulis dan ukuran disk) serta memberikan justifikasi migrasi Parquet berbasis komputasi cerdas. | Melakukan ekspor Parquet namun interpretasi manfaat teknis format kolumnar belum mendalam. | Gagal melakukan konversi format atau salah menginterpretasikan hasil benchmark I/O. |
