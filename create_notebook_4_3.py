import json
import os

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AI Modul 4.3: Praktikum Pandas untuk Manipulasi Data\n",
                "## Rekayasa Data Tabular, Agregasi Relasional, dan Analisis Deret Waktu Agribisnis\n",
                "\n",
                "Notebook ini menyajikan implementasi praktis manipulasi data tabular menggunakan pustaka **Pandas** untuk pengelolaan produksi perkebunan, penggabungan data relasional, agregasi *Split-Apply-Combine*, serta pemrosesan runtun waktu cuaca.\n",
                "\n",
                "### Agenda Praktikum:\n",
                "1. **Inspeksi Struktur DataFrame dan Jejak Memori (*Memory Profiling*)**\n",
                "2. **Seleksi Presisi: Perbandingan `.loc` vs `.iloc` dan Eliminasi `SettingWithCopyWarning`**\n",
                "3. **Agregasi Tingkat Lanjut: Paradigma *Split-Apply-Combine* pada Data Panen Sawit**\n",
                "4. **Operasi Relasional: Penggabungan (*Merge/Join*) Data Panen dan Sensor Tanah**\n",
                "5. **Restrukturisasi Bentuk Data: Matriks Rekapitulasi (*Pivot Table*) dan *Melt***\n",
                "6. **Pengolahan Deret Waktu (*Time Series*): Resampling dan Rata-Rata Bergerak (*Rolling Windows*)**\n",
                "7. **Optimasi Kinerja: Reduksi Memori Drastis dengan Tipe Data `category`**"
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
                "import numpy as np\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "\n",
                "print(f\"Versi Pandas : {pd.__version__}\")\n",
                "print(f\"Versi NumPy  : {np.__version__}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Inspeksi Struktur DataFrame dan Jejak Memori\n",
                "\n",
                "Kita membuat dataset simulasi 100 blok kebun kelapa sawit dan menganalisis konsumsi memori per kolom."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "np.random.seed(42)\n",
                "n_blok = 100\n",
                "\n",
                "df_kebun = pd.DataFrame({\n",
                "    'Blok_ID': [f\"BLK-{i+1:03d}\" for i in range(n_blok)],\n",
                "    'Afdeling': np.random.choice(['AFD-A', 'AFD-B', 'AFD-C', 'AFD-D'], size=n_blok),\n",
                "    'Luas_Ha': np.random.uniform(20.0, 35.0, size=n_blok).round(1),\n",
                "    'Tahun_Tanam': np.random.randint(2005, 2020, size=n_blok),\n",
                "    'Tonase_Panen_Ton': np.random.uniform(15.0, 32.0, size=n_blok).round(2),\n",
                "    'Kadar_FFA_pct': np.random.uniform(1.8, 4.5, size=n_blok).round(2)\n",
                "})\n",
                "\n",
                "print(\"Tampilan 5 Baris Pertama Data Kebun:\")\n",
                "print(df_kebun.head())\n",
                "\n",
                "print(\"\\n=== Profiling Memori Kolom (Bytes) ===\")\n",
                "memori_detail = df_kebun.memory_usage(deep=True)\n",
                "print(memori_detail)\n",
                "print(f\"Total Penggunaan RAM: {memori_detail.sum() / 1024:.2f} KB\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Seleksi Presisi: `.loc` vs `.iloc` dan Pencegahan `SettingWithCopyWarning`\n",
                "\n",
                "Uji coba perbedaan seleksi berbasis label (`.loc`) dan posisi (`.iloc`), serta cara yang benar mengubah nilai tanpa penugasan berantai (*chained assignment*)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Memberikan indeks kustom pada 5 baris pertama\n",
                "df_sub = df_kebun.head().copy()\n",
                "df_sub.index = ['Blok-P', 'Blok-Q', 'Blok-R', 'Blok-S', 'Blok-T']\n",
                "\n",
                "# 1. Seleksi dengan .loc (Label Inklusif)\n",
                "print(\"--- Seleksi Berbasis Label (.loc) ---\")\n",
                "print(df_sub.loc['Blok-P':'Blok-R', ['Afdeling', 'Tonase_Panen_Ton']])\n",
                "\n",
                "# 2. Seleksi dengan .iloc (Posisi Integer Eksklusif Akhir)\n",
                "print(\"\\n--- Seleksi Berbasis Posisi (.iloc) ---\")\n",
                "print(df_sub.iloc[0:2, [1, 4]])\n",
                "\n",
                "# 3. Mutasi Aman Menggunakan .loc Tunggal (Bukan Chained Indexing)\n",
                "# Blok dengan FFA > 4.0% ditandai perlu penanganan segera\n",
                "df_kebun['Status_Mutu'] = 'STANDAR'\n",
                "df_kebun.loc[df_kebun['Kadar_FFA_pct'] > 4.0, 'Status_Mutu'] = 'PERIKSA_FFA_TINGGI'\n",
                "\n",
                "print(\"\\nRekapitulasi Status Mutu Panen TBS:\")\n",
                "print(df_kebun['Status_Mutu'].value_counts())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Agregasi Tingkat Lanjut: Paradigma *Split-Apply-Combine*\n",
                "\n",
                "Mengelompokkan data berdasarkan `Afdeling` dan menghitung statistik multi-metrik (rerata, total, standar deviasi, dan produktivitas per hektar)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Hitung produktivitas per hektar terlebih dahulu\n",
                "df_kebun['Yield_Ton_Ha'] = (df_kebun['Tonase_Panen_Ton'] / df_kebun['Luas_Ha']).round(2)\n",
                "\n",
                "# Agregasi Named Aggregations\n",
                "rekap_afdeling = df_kebun.groupby('Afdeling').agg(\n",
                "    Jumlah_Blok=('Blok_ID', 'count'),\n",
                "    Total_Luas_Ha=('Luas_Ha', 'sum'),\n",
                "    Total_Panen_Ton=('Tonase_Panen_Ton', 'sum'),\n",
                "    Rerata_Yield_Ton_Ha=('Yield_Ton_Ha', 'mean'),\n",
                "    Rerata_FFA=('Kadar_FFA_pct', 'mean')\n",
                ").round(2).reset_index()\n",
                "\n",
                "print(\"Rekapitulasi Produksi dan Mutu per Afdeling:\")\n",
                "print(rekap_afdeling.to_string(index=False))\n",
                "\n",
                "# Group Transformasi: Normalisasi Z-Score Produktivitas Relatif per Afdeling\n",
                "def zscore_grup(x):\n",
                "    return (x - x.mean()) / x.std()\n",
                "\n",
                "df_kebun['Yield_ZScore_Afdeling'] = df_kebun.groupby('Afdeling')['Yield_Ton_Ha'].transform(zscore_grup).round(2)\n",
                "print(\"\\n5 Blok dengan Deviasi Produktivitas Tertinggi terhadap Afdelingnya:\")\n",
                "print(df_kebun[['Blok_ID', 'Afdeling', 'Yield_Ton_Ha', 'Yield_ZScore_Afdeling']].sort_values(by='Yield_ZScore_Afdeling', ascending=False).head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Operasi Relasional & Reshaping: Merge dan Pivot Table\n",
                "\n",
                "Menggabungkan tabel panen dengan tabel hasil uji laboratorium tanah, lalu membuat tabel silang (*pivot table*)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Tabel Kedua: Data Uji Laboratorium Kesuburan Tanah Blok\n",
                "df_tanah = pd.DataFrame({\n",
                "    'ID_Blok': df_kebun['Blok_ID'],\n",
                "    'pH_Tanah': np.random.uniform(4.2, 5.8, size=n_blok).round(2),\n",
                "    'C_Organik_pct': np.random.uniform(1.2, 2.8, size=n_blok).round(2)\n",
                "})\n",
                "\n",
                "# 1. Operasi Relasional Merge (Left Join)\n",
                "df_terpadu = pd.merge(\n",
                "    df_kebun,\n",
                "    df_tanah,\n",
                "    left_on='Blok_ID',\n",
                "    right_on='ID_Blok',\n",
                "    how='left'\n",
                ").drop(columns=['ID_Blok'])\n",
                "\n",
                "print(\"Hasil Penggabungan Data Agronomi dan Uji Tanah (5 Baris):\")\n",
                "print(df_terpadu[['Blok_ID', 'Afdeling', 'Tonase_Panen_Ton', 'pH_Tanah', 'C_Organik_pct']].head())\n",
                "\n",
                "# 2. Reshaping: Pivot Table Matriks Afdeling vs Kategori Umur Tanaman\n",
                "df_terpadu['Kategori_Umur'] = pd.cut(\n",
                "    2026 - df_terpadu['Tahun_Tanam'],\n",
                "    bins=[0, 10, 15, 30],\n",
                "    labels=['Muda (<10th)', 'Remaja (10-15th)', 'Tua (>15th)']\n",
                ")\n",
                "\n",
                "pivot_sawit = pd.pivot_table(\n",
                "    df_terpadu,\n",
                "    index='Afdeling',\n",
                "    columns='Kategori_Umur',\n",
                "    values='Yield_Ton_Ha',\n",
                "    aggfunc='mean',\n",
                "    fill_value=0.0,\n",
                "    margins=True\n",
                ").round(2)\n",
                "\n",
                "print(\"\\nPivot Table Rata-Rata Yield (Ton/Ha) Afdeling vs Kategori Umur:\")\n",
                "print(pivot_sawit)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Analitik Deret Waktu (*Time Series*) & Jendela Geser (*Rolling Windows*)\n",
                "\n",
                "Simulasi data curah hujan per jam selama 90 hari (2.160 jam), melakukan *resampling* harian, dan menghitung akumulasi hujan 7-harian (*rolling sum*)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Membuat Runtun Waktu Curah Hujan 90 Hari (Frekuensi 1 Jam)\n",
                "indeks_jam = pd.date_range(start='2026-01-01 00:00:00', periods=90*24, freq='h')\n",
                "hujan_jam = np.random.choice([0.0, 0.0, 0.0, 1.5, 4.2, 8.5, 15.0], size=len(indeks_jam), p=[0.70, 0.12, 0.08, 0.04, 0.03, 0.02, 0.01])\n",
                "\n",
                "df_cuaca = pd.DataFrame({'Curah_Hujan_mm': hujan_jam}, index=indeks_jam)\n",
                "\n",
                "# 1. Downsampling dari Jam ke Harian\n",
                "df_harian = df_cuaca.resample('D').sum()\n",
                "\n",
                "# 2. Rolling Windows: Akumulasi 7 Hari dan Rata-rata 14 Hari\n",
                "df_harian['Hujan_Akumulasi_7H'] = df_harian['Curah_Hujan_mm'].rolling(window=7, min_periods=1).sum().round(1)\n",
                "df_harian['SMA_Hujan_14H'] = df_harian['Curah_Hujan_mm'].rolling(window=14, min_periods=1).mean().round(2)\n",
                "\n",
                "print(\"Cuplikan 5 Baris Data Cuaca Agregat Harian:\")\n",
                "print(df_harian.head(10))\n",
                "\n",
                "# 3. Visualisasi Tren Runtun Waktu\n",
                "plt.figure(figsize=(10, 4.5), dpi=150)\n",
                "plt.bar(df_harian.index, df_harian['Curah_Hujan_mm'], color='#93C5FD', alpha=0.6, label='Curah Hujan Harian (mm)')\n",
                "plt.plot(df_harian.index, df_harian['SMA_Hujan_14H'], color='#1D4ED8', lw=2, label='SMA 14-Harian Tren')\n",
                "plt.plot(df_harian.index, df_harian['Hujan_Akumulasi_7H'] / 7.0, color='#DC2626', ls='--', lw=1.5, label='Rerata Bergerak 7-Harian')\n",
                "plt.title('Dinamika Deret Waktu Curah Hujan Kebun Sawit (Jan-Mar 2026)', fontsize=11, fontweight='bold', pad=10)\n",
                "plt.ylabel('Curah Hujan (mm)', fontsize=9, fontweight='bold')\n",
                "plt.legend()\n",
                "plt.grid(True, linestyle=':', alpha=0.5)\n",
                "plt.tight_layout()\n",
                "plt.savefig('e:/Project Buku/docs/assets/praktikum_4_3_timeseries.png', dpi=150)\n",
                "print(\"Plot deret waktu berhasil disimpan ke docs/assets/praktikum_4_3_timeseries.png\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Optimasi Kinerja: Reduksi Memori dengan Tipe Data `category`\n",
                "\n",
                "Simulasi dataset transaksi penimbangan 200.000 truk di PKS untuk membandingkan penggunaan RAM tipe `object` vs `category`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Membuat Dataset Skala Besar (200.000 Baris Penimbangan)\n",
                "N_TRUK = 200_000\n",
                "df_timbangan = pd.DataFrame({\n",
                "    'No_Tiket': [f\"TKT-{i+1:06d}\" for i in range(N_TRUK)],\n",
                "    'Status_Fraksi': np.random.choice(['Mentah', 'Kurang_Matang', 'Matang_Optimal', 'Lewat_Matang'], size=N_TRUK),\n",
                "    'Nama_PKS': np.random.choice(['PKS-Sentral', 'PKS-Utara', 'PKS-Selatan'], size=N_TRUK)\n",
                "})\n",
                "\n",
                "memori_sebelum = df_timbangan.memory_usage(deep=True)['Status_Fraksi'] / (1024 * 1024)\n",
                "\n",
                "# Konversi ke Tipe Category\n",
                "df_timbangan['Status_Fraksi'] = df_timbangan['Status_Fraksi'].astype('category')\n",
                "memori_sesudah = df_timbangan.memory_usage(deep=True)['Status_Fraksi'] / (1024 * 1024)\n",
                "\n",
                "penghematan_pct = ((memori_sebelum - memori_sesudah) / memori_sebelum) * 100\n",
                "\n",
                "print(f\"Konsumsi Memori Kolom 'Status_Fraksi' (Object)   : {memori_sebelum:.2f} MB\")\n",
                "print(f\"Konsumsi Memori Kolom 'Status_Fraksi' (Category) : {memori_sesudah:.2f} MB\")\n",
                "print(f\"--> Efisiensi Penghematan RAM: {penghematan_pct:.2f}%\")\n",
                "print(\"\\nPraktikum Modul 4.3 Selesai dengan Sukses!\")"
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

target_nb = r'e:\Project Buku\notebooks\part-04\AI_Modul_4.3_Praktikum_Pandas_Manipulasi_Data.ipynb'
with open(target_nb, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Jupyter Notebook successfully written to {target_nb}")
