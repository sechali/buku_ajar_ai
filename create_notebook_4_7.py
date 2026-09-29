import json
import os

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AI Modul 4.7: Praktikum Membaca Dataset (CSV/Excel)\n",
                "## Ekstraksi Data Tabular, Ingesti Multi-Sheet, Chunking Streaming, dan Optimasi Parquet\n",
                "\n",
                "Notebook ini menyajikan implementasi praktis penanganan berbagai variasi berkas tabular mentah di industri perkebunan kelapa sawit: pembacaan CSV format regional (titik koma & koma desimal), pembacaan buku kerja Excel multi-lembar (*multi-sheets*), teknik *chunking* untuk dataset raksasa ber-RAM terbatas, serta benchmark migrasi ke format kolumnar modern **Apache Parquet**.\n",
                "\n",
                "### Agenda Praktikum:\n",
                "1. **Inisialisasi Lingkungan & Pembuatan Berkas Uji Coba (CSV & XLSX)**\n",
                "2. **Teknik Parsing CSV Regional: Enkoding, Delimiter, dan Deklarasi Dtype**\n",
                "3. **Ingesti Buku Kerja Excel Multi-Sheet Efisien Menggunakan `pd.ExcelFile`**\n",
                "4. **Pemrosesan Dataset Masif dengan Streaming Chunking Iterator (`chunksize`)**\n",
                "5. **Benchmark Performa I/O & Ukuran Disk: CSV Teks vs Apache Parquet Biner**\n",
                "6. **Pembersihan Berkas Sementara & Ringkasan Praktikum**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Inisialisasi Environment & Import Pustaka\n",
                "import os\n",
                "os.environ['MPLBACKEND'] = 'Agg'  # Backend non-interaktif\n",
                "\n",
                "import time\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "import openpyxl\n",
                "import pyarrow\n",
                "\n",
                "os.makedirs('e:/Project Buku/data/sandbox_4_7', exist_ok=True)\n",
                "print(f\"Versi Pandas   : {pd.__version__}\")\n",
                "print(f\"Versi OpenPyXL : {openpyxl.__version__}\")\n",
                "print(f\"Versi PyArrow  : {pyarrow.__version__}\")\n",
                "print(\"Lingkungan Praktikum I/O Data siap digunakan!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Pembuatan Berkas Uji Coba: CSV Regional & Excel Multi-Sheet\n",
                "\n",
                "Kita menyimulasikan data tiket timbangan PKS berformat regional (pemisah titik koma `;` dan desimal koma `,`), serta buku kerja Excel berisi lembar kerja `Afdeling_A`, `Afdeling_B`, dan `Rekap_Estate`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Membuat Berkas CSV Regional Indonesia/Eropa (sep=';', decimal=',')\n",
                "csv_path = 'e:/Project Buku/data/sandbox_4_7/tiket_timbangan_pks.csv'\n",
                "with open(csv_path, 'w', encoding='utf-8') as f:\n",
                "    f.write(\"Tiket_ID;Tanggal;Afdeling;Berat_Bruto_Ton;Berat_Tarra_Ton;Kadar_FFA_pct\\n\")\n",
                "    f.write(\"TKT-001;2026-03-01;AFD-A;12,45;4,20;2,35\\n\")\n",
                "    f.write(\"TKT-002;2026-03-01;AFD-B;14,80;4,35;3,10\\n\")\n",
                "    f.write(\"TKT-003;2026-03-02;AFD-A;11,90;4,15;2,15\\n\")\n",
                "    f.write(\"TKT-004;2026-03-02;AFD-C;16,25;4,50;4,20\\n\")\n",
                "    f.write(\"TKT-005;2026-03-03;AFD-B;13,75;4,25;2,85\\n\")\n",
                "\n",
                "# 2. Membuat Berkas Excel Multi-Sheet\n",
                "xlsx_path = 'e:/Project Buku/data/sandbox_4_7/rekap_panen_multi_sheet.xlsx'\n",
                "with pd.ExcelWriter(xlsx_path, engine='openpyxl') as writer:\n",
                "    df_afd_a = pd.DataFrame({\n",
                "        'Blok_ID': ['BLK-A01', 'BLK-A02', 'BLK-A03'],\n",
                "        'Luas_Ha': [25.0, 30.0, 28.5],\n",
                "        'Tonase_TBS': [24.5, 29.8, 27.2]\n",
                "    })\n",
                "    df_afd_b = pd.DataFrame({\n",
                "        'Blok_ID': ['BLK-B01', 'BLK-B02', 'BLK-B03'],\n",
                "        'Luas_Ha': [22.0, 32.0, 26.0],\n",
                "        'Tonase_TBS': [19.2, 31.5, 24.8]\n",
                "    })\n",
                "    df_afd_a.to_excel(writer, sheet_name='Afdeling_A', index=False)\n",
                "    df_afd_b.to_excel(writer, sheet_name='Afdeling_B', index=False)\n",
                "\n",
                "print(\"Berkas CSV regional dan Excel multi-sheet berhasil dibuat!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Pembacaan CSV Format Regional & Deklarasi Tipe Data Eksplisit"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Membaca dengan parameter sep=';', decimal=',', dan dtype spesifik\n",
                "skema_dtype = {\n",
                "    'Tiket_ID': 'string',\n",
                "    'Afdeling': 'category',\n",
                "    'Berat_Bruto_Ton': 'float32',\n",
                "    'Berat_Tarra_Ton': 'float32',\n",
                "    'Kadar_FFA_pct': 'float32'\n",
                "}\n",
                "\n",
                "df_tiket = pd.read_csv(\n",
                "    csv_path,\n",
                "    sep=';',\n",
                "    decimal=',',\n",
                "    dtype=skema_dtype,\n",
                "    parse_dates=['Tanggal']\n",
                ")\n",
                "\n",
                "# Hitung Berat Bersih (Netto) TBS\n",
                "df_tiket['Berat_Netto_Ton'] = (df_tiket['Berat_Bruto_Ton'] - df_tiket['Berat_Tarra_Ton']).round(2)\n",
                "\n",
                "print(\"Dataframe Tiket Timbangan PKS Hasil Parsing:\")\n",
                "print(df_tiket)\n",
                "print(\"\\nTipe Data Kolom:\")\n",
                "print(df_tiket.dtypes)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Ingesti Berkas Excel Multi-Sheet Efisien dengan `pd.ExcelFile`\n",
                "\n",
                "Membuka buku kerja Excel hanya satu kali dan menggabungkan seluruh lembar afdeling secara dinamis."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Menggunakan objek pd.ExcelFile untuk dekompresi tunggal\n",
                "daftar_afdeling = []\n",
                "\n",
                "with pd.ExcelFile(xlsx_path, engine='openpyxl') as xls:\n",
                "    print(f\"Daftar Lembar Kerja yang Ditemukan: {xls.sheet_names}\")\n",
                "    for sheet in xls.sheet_names:\n",
                "        if sheet.startswith('Afdeling_'):\n",
                "            df_lembar = pd.read_excel(xls, sheet_name=sheet)\n",
                "            df_lembar['Divisi'] = sheet\n",
                "            daftar_afdeling.append(df_lembar)\n",
                "\n",
                "df_kebun_konsolidasi = pd.concat(daftar_afdeling, ignore_index=True)\n",
                "df_kebun_konsolidasi['Yield_Ton_Ha'] = (df_kebun_konsolidasi['Tonase_TBS'] / df_kebun_konsolidasi['Luas_Ha']).round(2)\n",
                "\n",
                "print(\"\\nHasil Konsolidasi Seluruh Afdeling dari Excel:\")\n",
                "print(df_kebun_konsolidasi)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Pemrosesan Data Masif Menggunakan Chunking Iterator\n",
                "\n",
                "Kita menyimulasikan 50.000 rekaman sensor cuaca, lalu memprosesnya dalam bongkahan 10.000 baris per iterasi untuk membuktikan efisiensi memori."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Membuat Berkas CSV Besar Sintetis (50.000 Baris)\n",
                "big_csv_path = 'e:/Project Buku/data/sandbox_4_7/sensor_telemetri_besar.csv'\n",
                "N_BIG = 50_000\n",
                "\n",
                "np.random.seed(42)\n",
                "df_big_sim = pd.DataFrame({\n",
                "    'Timestamp': pd.date_range('2026-01-01', periods=N_BIG, freq='min'),\n",
                "    'Afdeling': np.random.choice(['AFD-01', 'AFD-02', 'AFD-03'], size=N_BIG),\n",
                "    'Curah_Hujan_mm': np.random.uniform(0.0, 45.0, size=N_BIG).round(2),\n",
                "    'Suhu_C': np.random.uniform(22.0, 37.0, size=N_BIG).round(1)\n",
                "})\n",
                "df_big_sim.to_csv(big_csv_path, index=False)\n",
                "print(f\"Ukuran Berkas CSV di Disk: {os.path.getsize(big_csv_path) / (1024*1024):.2f} MB\")\n",
                "\n",
                "# Pemrosesan Streaming Berbasis Chunk (10.000 baris per iterasi)\n",
                "CHUNK_SIZE = 10_000\n",
                "total_hujan = 0.0\n",
                "total_baris = 0\n",
                "hujan_ekstrem_count = 0\n",
                "\n",
                "t0 = time.perf_counter()\n",
                "for i, chunk in enumerate(pd.read_csv(big_csv_path, chunksize=CHUNK_SIZE, usecols=['Curah_Hujan_mm'])):\n",
                "    total_hujan += chunk['Curah_Hujan_mm'].sum()\n",
                "    total_baris += len(chunk)\n",
                "    hujan_ekstrem_count += (chunk['Curah_Hujan_mm'] > 35.0).sum()\n",
                "    # Memori chunk langsung dibebaskan di setiap iterasi\n",
                "\n",
                "waktu_chunk = time.perf_counter() - t0\n",
                "rerata_hujan = total_hujan / total_baris\n",
                "\n",
                "print(f\"\\n=== Hasil Pemrosesan Streaming Chunking ===\")\n",
                "print(f\"Total Baris Diproses      : {total_baris:,} baris\")\n",
                "print(f\"Rerata Curah Hujan Global : {rerata_hujan:.2f} mm\")\n",
                "print(f\"Jumlah Kejadian Hujan >35mm: {hujan_ekstrem_count:,} kali\")\n",
                "print(f\"Waktu Eksekusi            : {waktu_chunk:.3f} detik\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Benchmark Performa & Ukuran: CSV Teks vs Apache Parquet Biner\n",
                "\n",
                "Kita mengonversi dataset 50.000 baris ke format **Apache Parquet** terkompresi `snappy`, lalu membandingkan ukuran disk dan kecepatan baca."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "parquet_path = 'e:/Project Buku/data/sandbox_4_7/sensor_telemetri.parquet'\n",
                "\n",
                "# 1. Ekspor ke Format Parquet (Snappy Compression)\n",
                "df_big_sim.to_parquet(parquet_path, engine='pyarrow', compression='snappy')\n",
                "\n",
                "ukuran_csv = os.path.getsize(big_csv_path) / (1024 * 1024)\n",
                "ukuran_parquet = os.path.getsize(parquet_path) / (1024 * 1024)\n",
                "kompresi_rasio = ((ukuran_csv - ukuran_parquet) / ukuran_csv) * 100\n",
                "\n",
                "# 2. Uji Kecepatan Baca Kolom Tertentu (Projection Pushdown)\n",
                "# Uji Baca CSV (usecols)\n",
                "t0 = time.perf_counter()\n",
                "df_c_csv = pd.read_csv(big_csv_path, usecols=['Curah_Hujan_mm', 'Suhu_C'])\n",
                "t_csv = time.perf_counter() - t0\n",
                "\n",
                "# Uji Baca Parquet (columns)\n",
                "t0 = time.perf_counter()\n",
                "df_c_parquet = pd.read_parquet(parquet_path, columns=['Curah_Hujan_mm', 'Suhu_C'])\n",
                "t_parquet = time.perf_counter() - t0\n",
                "\n",
                "speedup = t_csv / t_parquet\n",
                "\n",
                "print(\"=== Komparasi CSV vs Apache Parquet ===\")\n",
                "print(f\"• Ukuran Berkas CSV     : {ukuran_csv:.2f} MB\")\n",
                "print(f\"• Ukuran Berkas Parquet : {ukuran_parquet:.2f} MB (Penghematan: {kompresi_rasio:.1f}%)\")\n",
                "print(f\"• Waktu Baca CSV        : {t_csv*1000:.2f} ms\")\n",
                "print(f\"• Waktu Baca Parquet    : {t_parquet*1000:.2f} ms\")\n",
                "print(f\"--> Kecepatan Baca Parquet: {speedup:.1f}x LEBIH CEPAT!\")\n",
                "\n",
                "# Pembersihan berkas sandbox sementara\n",
                "for f in [csv_path, xlsx_path, big_csv_path, parquet_path]:\n",
                "    if os.path.exists(f):\n",
                "        os.remove(f)\n",
                "os.rmdir('e:/Project Buku/data/sandbox_4_7')\n",
                "print(\"\\nBerkas sandbox berhasil dibersihkan.\")\n",
                "print(\"Praktikum Modul 4.7 Selesai dengan Sukses!\")"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbformat": 4,
            "nbformat_minor": 2,
            "version": "3.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

target_nb = r'e:\Project Buku\notebooks\part-04\AI_Modul_4.7_Praktikum_Membaca_Dataset_CSV_dan_Excel.ipynb'
with open(target_nb, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Jupyter Notebook successfully written to {target_nb}")
