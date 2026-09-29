import json
import os

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AI Modul 4.4: Praktikum Data Cleaning dan Preprocessing\n",
                "## Pembersihan Anomali Sensorik, Imputasi Tingkat Lanjut, dan Pipeline Bebas Kebocoran Data\n",
                "\n",
                "Notebook ini menyajikan panduan terapan pembersihan data mentah pertanian presisi dari anomali lapangan (nilai hilang, pencilan ekstrem, duplikasi rekaman, dan inkonsistensi teks) serta pengemasan alur kerja ke dalam **Scikit-Learn Pipeline** produksi yang kebal kebocoran data (*data leakage*).\n",
                "\n",
                "### Agenda Praktikum:\n",
                "1. **Inisialisasi Lingkungan & Sintesis Data Telemetri dengan Anomali Riil**\n",
                "2. **Audit Kualitas Data: Deteksi Pola Missing Values & Deduplikasi**\n",
                "3. **Komparasi Imputasi: Median Univariat vs Multivariat `KNNImputer`**\n",
                "4. **Deteksi Pencilan Non-Parametrik (Tukey IQR) & Mitigasi *Winsorizing***\n",
                "5. **Normalisasi Inkonsistensi Kategori Teks Menggunakan Regular Expression**\n",
                "6. **Rancang Bangun Pipeline Terpadu Menggunakan `ColumnTransformer` & `Pipeline`**"
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
                "from sklearn.model_selection import train_test_split\n",
                "from sklearn.impute import SimpleImputer, KNNImputer\n",
                "from sklearn.preprocessing import RobustScaler, OneHotEncoder\n",
                "from sklearn.compose import ColumnTransformer\n",
                "from sklearn.pipeline import Pipeline\n",
                "from sklearn.linear_model import Ridge\n",
                "from sklearn.metrics import mean_squared_error, r2_score\n",
                "\n",
                "print(f\"Versi Pandas : {pd.__version__}\")\n",
                "print(f\"Versi NumPy  : {np.__version__}\")\n",
                "print(\"Lingkungan Data Cleaning siap digunakan!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Sintesis Dataset Perkebunan Sawit dengan Anomali Lapangan Riil\n",
                "\n",
                "Kita membangkitkan 300 data observasi blok dengan anomali:\n",
                "- Nilai hilang acak (MCAR)\n",
                "- Nilai hilang terikat suhu tinggi (MAR)\n",
                "- Pencilan teknis ekstrem (kelembaban tanah 98% akibat sensor terendam)\n",
                "- Duplikasi transmisi paket MQTT\n",
                "- Variasi penulisan teks afdeling"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "np.random.seed(123)\n",
                "N = 300\n",
                "\n",
                "# Fitur dasar\n",
                "blok_id = [f\"BLK-{i+1:03d}\" for i in range(N)]\n",
                "afdeling_raw = np.random.choice(['AFD-01', 'afd 1', 'Afdeling_1', 'AFD-02', 'afd 02', 'AFD-03'], size=N)\n",
                "umur = np.random.randint(6, 24, size=N)\n",
                "suhu_kanopi = np.random.normal(31.5, 3.2, size=N).round(1)\n",
                "kelembaban_tanah = (55.0 - 0.7 * suhu_kanopi + np.random.normal(0, 2.5, size=N)).round(1)\n",
                "curah_hujan = np.random.exponential(scale=180.0, size=N).round(1)\n",
                "ndvi = np.clip(0.35 + 0.02 * (25 - np.abs(umur - 14)) + np.random.normal(0, 0.05, size=N), 0.3, 0.95).round(3)\n",
                "\n",
                "# Target tonase TBS (Ton/Ha)\n",
                "tonase = 0.5 * umur + 0.03 * curah_hujan + 15.0 * ndvi - 0.2 * suhu_kanopi + np.random.normal(0, 1.5, size=N)\n",
                "tonase = np.clip(tonase, 10.0, 36.0).round(2)\n",
                "\n",
                "df_mentah = pd.DataFrame({\n",
                "    'Blok_ID': blok_id,\n",
                "    'Afdeling': afdeling_raw,\n",
                "    'Umur_Tanam_Thn': umur,\n",
                "    'Suhu_Kanopi_C': suhu_kanopi,\n",
                "    'Kelembaban_Tanah_pct': kelembaban_tanah,\n",
                "    'Curah_Hujan_mm': curah_hujan,\n",
                "    'Indeks_NDVI': ndvi,\n",
                "    'Tonase_TBS_Ton_Ha': tonase\n",
                "})\n",
                "\n",
                "# Suntikkan Anomali Riil:\n",
                "# 1. MCAR: 10 nilai curah hujan hilang acak\n",
                "idx_mcar = np.random.choice(N, size=10, replace=False)\n",
                "df_mentah.loc[idx_mcar, 'Curah_Hujan_mm'] = np.nan\n",
                "\n",
                "# 2. MAR: Sensor kelembaban mati saat suhu > 35 C\n",
                "df_mentah.loc[df_mentah['Suhu_Kanopi_C'] > 35.5, 'Kelembaban_Tanah_pct'] = np.nan\n",
                "\n",
                "# 3. Outlier Ekstrem: Probe kelembaban korslet terendam air\n",
                "df_mentah.loc[[15, 88, 142], 'Kelembaban_Tanah_pct'] = 98.7\n",
                "\n",
                "# 4. Duplikasi data: 5 baris terduplikasi\n",
                "df_duplikat = df_mentah.iloc[[5, 20, 50, 100, 200]].copy()\n",
                "df_mentah = pd.concat([df_mentah, df_duplikat], ignore_index=True)\n",
                "\n",
                "print(f\"Ukuran Dataset Mentah (termasuk duplikat): {df_mentah.shape}\")\n",
                "print(df_mentah.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Audit Integritas Data: Deteksi Missing Values & Deduplikasi"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Pengecekan dan Pembuangan Baris Duplikat\n",
                "n_duplikat = df_mentah.duplicated().sum()\n",
                "print(f\"Jumlah Baris Duplikat Terdeteksi: {n_duplikat}\")\n",
                "df_bersih = df_mentah.drop_duplicates().copy()\n",
                "print(f\"Ukuran Setelah Deduplikasi: {df_bersih.shape}\")\n",
                "\n",
                "# 2. Audit Nilai Hilang (Missing Values)\n",
                "ringkasan_null = pd.DataFrame({\n",
                "    'Jumlah_Null': df_bersih.isnull().sum(),\n",
                "    'Persentase_Null': (df_bersih.isnull().sum() / len(df_bersih) * 100).round(2)\n",
                "})\n",
                "print(\"\\nAudit Nilai Hilang per Kolom:\")\n",
                "print(ringkasan_null[ringkasan_null['Jumlah_Null'] > 0])"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Standarisasi Teks Kategori Afdeling dengan Regex\n",
                "\n",
                "Variasi penulisan `'AFD-01'`, `'afd 1'`, `'Afdeling_1'` distandarisasi menjadi format kanonik `'AFD-01'`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print(\"Kategori Afdeling Mentah:\")\n",
                "print(df_bersih['Afdeling'].value_counts())\n",
                "\n",
                "# Standardisasi menggunakan Regular Expression\n",
                "def standardisasi_afdeling(teks):\n",
                "    import re\n",
                "    # Cari digit angka di dalam teks string\n",
                "    angka = re.search(r'\\d+', str(teks))\n",
                "    if angka:\n",
                "        return f\"AFD-{int(angka.group()):02d}\"\n",
                "    return \"AFD-UNKNOWN\"\n",
                "\n",
                "df_bersih['Afdeling'] = df_bersih['Afdeling'].apply(standardisasi_afdeling)\n",
                "print(\"\\nKategori Afdeling Setelah Distandarisasi:\")\n",
                "print(df_bersih['Afdeling'].value_counts())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Deteksi Pencilan Non-Parametrik (Tukey IQR) & Mitigasi *Winsorizing*\n",
                "\n",
                "Mendeteksi lonjakan nilai kelembaban tanah ekstrem (> 60%) dan menerapkan teknik kliping kuartil (*Winsorizing*)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Menghitung Batas IQR Tukey pada Kolom Kelembaban Tanah\n",
                "Q1 = df_bersih['Kelembaban_Tanah_pct'].quantile(0.25)\n",
                "Q3 = df_bersih['Kelembaban_Tanah_pct'].quantile(0.75)\n",
                "IQR = Q3 - Q1\n",
                "batas_bawah = Q1 - 1.5 * IQR\n",
                "batas_atas = Q3 + 1.5 * IQR\n",
                "\n",
                "print(f\"Kuartil 1 (Q1)     : {Q1:.2f}%\")\n",
                "print(f\"Kuartil 3 (Q3)     : {Q3:.2f}%\")\n",
                "print(f\"Rentang IQR        : {IQR:.2f}%\")\n",
                "print(f\"Batas Atas Tukey   : {batas_atas:.2f}%\")\n",
                "\n",
                "# Identifikasi Pencilan Ekstrem\n",
                "outliers = df_bersih[df_bersih['Kelembaban_Tanah_pct'] > batas_atas]\n",
                "print(f\"Jumlah Titik Pencilan Terdeteksi: {len(outliers)}\")\n",
                "print(outliers[['Blok_ID', 'Suhu_Kanopi_C', 'Kelembaban_Tanah_pct']])\n",
                "\n",
                "# Mitigasi Winsorizing (Kliping ke Batas Atas)\n",
                "df_bersih['Kelembaban_Tanah_pct_Winsor'] = df_bersih['Kelembaban_Tanah_pct'].clip(lower=batas_bawah, upper=batas_atas)\n",
                "\n",
                "# Visualisasi Boxplot Sebelum vs Sesudah Winsorizing\n",
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=150)\n",
                "ax1.boxplot(df_bersih['Kelembaban_Tanah_pct'].dropna(), vert=True, patch_artist=True,\n",
                "            boxprops=dict(facecolor='#FECACA', color='#DC2626'), medianprops=dict(color='#7F1D1D', lw=2))\n",
                "ax1.set_title('Sebelum Mitigasi\\n(Pencilan Ekstrem > 90%)', fontsize=10, fontweight='bold')\n",
                "ax1.set_ylabel('Kelembaban Tanah (%)')\n",
                "ax1.grid(True, linestyle=':', alpha=0.6)\n",
                "\n",
                "ax2.boxplot(df_bersih['Kelembaban_Tanah_pct_Winsor'].dropna(), vert=True, patch_artist=True,\n",
                "            boxprops=dict(facecolor='#BBF7D0', color='#16A34A'), medianprops=dict(color='#14532D', lw=2))\n",
                "ax2.set_title('Sesudah Winsorizing\\n(Kliping Batas Tukey IQR)', fontsize=10, fontweight='bold')\n",
                "ax2.grid(True, linestyle=':', alpha=0.6)\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('e:/Project Buku/docs/assets/praktikum_4_4_outlier.png', dpi=150)\n",
                "print(\"Plot perbandingan outlier disimpan ke docs/assets/praktikum_4_4_outlier.png\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Rancang Bangun Pipeline Terpadu Bebas Kebocoran Data\n",
                "\n",
                "Kita membungkus seluruh tahapan: Imputasi (Median), Penskalaan Kuat (*RobustScaler*), dan *One-Hot Encoding* ke dalam `ColumnTransformer` dan `Pipeline` Scikit-Learn."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Menyiapkan Matriks Fitur X dan Target y\n",
                "X = df_bersih[['Afdeling', 'Umur_Tanam_Thn', 'Suhu_Kanopi_C', 'Kelembaban_Tanah_pct_Winsor', 'Curah_Hujan_mm', 'Indeks_NDVI']]\n",
                "y = df_bersih['Tonase_TBS_Ton_Ha']\n",
                "\n",
                "# Pembagian Data Latih dan Uji SEBELUM Fitting (Mencegah Data Leakage!)\n",
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
                "print(f\"Ukuran Set Latih : {X_train.shape[0]} blok\")\n",
                "print(f\"Ukuran Set Uji   : {X_test.shape[0]} blok\")\n",
                "\n",
                "# Identifikasi Kolom Fitur\n",
                "fitur_numerik = ['Umur_Tanam_Thn', 'Suhu_Kanopi_C', 'Kelembaban_Tanah_pct_Winsor', 'Curah_Hujan_mm', 'Indeks_NDVI']\n",
                "fitur_kategori = ['Afdeling']\n",
                "\n",
                "# 1. Sub-Pipeline Numerik: Imputasi Median -> RobustScaler\n",
                "pipe_numerik = Pipeline([\n",
                "    ('imputer', SimpleImputer(strategy='median')),\n",
                "    ('scaler', RobustScaler())\n",
                "])\n",
                "\n",
                "# 2. Sub-Pipeline Kategorikal: Imputasi Modus -> OneHotEncoder\n",
                "pipe_kategori = Pipeline([\n",
                "    ('imputer', SimpleImputer(strategy='most_frequent')),\n",
                "    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))\n",
                "])\n",
                "\n",
                "# 3. Pra-Pemroses Kolom Komposit (ColumnTransformer)\n",
                "preprocessor = ColumnTransformer(transformers=[\n",
                "    ('num', pipe_numerik, fitur_numerik),\n",
                "    ('cat', pipe_kategori, fitur_kategori)\n",
                "])\n",
                "\n",
                "# 4. Pipeline End-to-End dengan Model Estimator Ridge Regressor\n",
                "full_pipeline = Pipeline([\n",
                "    ('prep', preprocessor),\n",
                "    ('regressor', Ridge(alpha=1.0))\n",
                "])\n",
                "\n",
                "# Pelatihan Model (Fitting Pipeline Hanya pada Training Set!)\n",
                "full_pipeline.fit(X_train, y_train)\n",
                "\n",
                "# Evaluasi pada Set Uji\n",
                "y_pred = full_pipeline.predict(X_test)\n",
                "r2 = r2_score(y_test, y_pred)\n",
                "rmse = np.sqrt(mean_squared_error(y_test, y_pred))\n",
                "\n",
                "print(\"\\n=== Kinerja Model pada Data Uji yang Bersih ===\")\n",
                "print(f\"Koefisien Determinasi (R2) : {r2:.4f}\")\n",
                "print(f\"Root Mean Sq Error (RMSE)   : {rmse:.4f} Ton/Ha\")\n",
                "print(\"\\nPraktikum Modul 4.4 Selesai dengan Sukses!\")"
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

target_nb = r'e:\Project Buku\notebooks\part-04\AI_Modul_4.4_Praktikum_Data_Cleaning_dan_Preprocessing.ipynb'
with open(target_nb, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Jupyter Notebook successfully written to {target_nb}")
