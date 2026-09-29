import json
import os

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AI Modul 4.2: Praktikum NumPy untuk Komputasi Numerik\n",
                "## Komputasi Array Tervektorisasi Kinerja Tinggi pada Data Pertanian Presisi\n",
                "\n",
                "Notebook ini menyajikan implementasi praktis penggunaan **NumPy** (*Numerical Python*) untuk komputasi data spasial, telemetri sensor, dan aljabar linier terapan di perkebunan modern.\n",
                "\n",
                "### Agenda Praktikum:\n",
                "1. **Inspeksi Anatomi Memori `ndarray`, Strides, dan Flags**\n",
                "2. **Benchmark Vektorisasi SIMD vs Perulangan Python Standar**\n",
                "3. **Mekanisme Aturan Penyiaran (*Broadcasting Rules*) Multi-Dimensi**\n",
                "4. **Disiplin Slicing: Verifikasi *View* vs *Copy* Memori**\n",
                "5. **Boolean Masking & Penyaringan Data Anomali Sensor Lapangan**\n",
                "6. **Aljabar Linear `numpy.linalg`: Pemecahan Sistem Persamaan Linier Turbin PKS**\n",
                "7. **Studi Kasus: Pemrosesan Grid Spasial Citra NDVI Kanopi Kebun Sawit**"
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
                "import matplotlib.pyplot as plt\n",
                "\n",
                "print(f\"Versi NumPy Terpasang : {np.__version__}\")\n",
                "print(f\"Konfigurasi BLAS/LAPACK:\\n{np.__config__.show()}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Anatomi Memori Objek `ndarray`, Strides, dan Tata Letak Fisik\n",
                "\n",
                "Kita akan memeriksa atribut internal NumPy: `shape`, `dtype`, `itemsize`, `nbytes`, dan `strides`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Membuat matriks telemetri kebun 4 baris x 5 kolom (float64)\n",
                "data_sensor = np.array([\n",
                "    [28.5, 30.1, 29.4, 31.2, 28.9],\n",
                "    [32.0, 31.8, 30.5, 29.8, 33.1],\n",
                "    [27.4, 28.2, 29.0, 30.4, 31.0],\n",
                "    [33.5, 34.2, 32.1, 31.5, 30.8]\n",
                "], dtype=np.float64)\n",
                "\n",
                "print(\"=== Metadata ndarray ===\")\n",
                "print(f\"Dimensi (ndim)      : {data_sensor.ndim}\")\n",
                "print(f\"Bentuk (shape)      : {data_sensor.shape}\")\n",
                "print(f\"Tipe Data (dtype)   : {data_sensor.dtype}\")\n",
                "print(f\"Ukuran Item (bytes) : {data_sensor.itemsize} bytes per elemen\")\n",
                "print(f\"Total Memori (bytes): {data_sensor.nbytes} bytes\")\n",
                "print(f\"Langkah (strides)   : {data_sensor.strides} -> (Lompat {data_sensor.strides[0]}B per baris, {data_sensor.strides[1]}B per kolom)\")\n",
                "\n",
                "# Periksa Bendera Memori (Flags)\n",
                "print(\"\\n=== Status Bendera Memori (Flags) ===\")\n",
                "print(f\"C-Contiguous (Row-major) : {data_sensor.flags.c_contiguous}\")\n",
                "print(f\"F-Contiguous (Col-major) : {data_sensor.flags.f_contiguous}\")\n",
                "print(f\"Owns Data (Memiliki RAM) : {data_sensor.flags.owndata}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Benchmark Kinerja: Vektorisasi SIMD vs Perulangan Python Murni\n",
                "\n",
                "Kita membandingkan kecepatan kalkulasi koreksi kalibrasi sensor pada 500.000 titik data telemetri."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Uji Komparasi Waktu Eksekusi (500.000 Titik Telemetri)\n",
                "N = 500_000\n",
                "data_raw = np.random.uniform(20.0, 45.0, size=N)\n",
                "data_list = list(data_raw)\n",
                "\n",
                "# Metode 1: Loop Python Murni (Standard CPython)\n",
                "t0 = time.perf_counter()\n",
                "hasil_loop = []\n",
                "for val in data_list:\n",
                "    hasil_loop.append((val * 1.05) - 2.3)\n",
                "t_loop = (time.perf_counter() - t0) * 1000\n",
                "\n",
                "# Metode 2: List Comprehension\n",
                "t0 = time.perf_counter()\n",
                "hasil_comp = [(val * 1.05) - 2.3 for val in data_list]\n",
                "t_comp = (time.perf_counter() - t0) * 1000\n",
                "\n",
                "# Metode 3: Vektorisasi SIMD NumPy\n",
                "t0 = time.perf_counter()\n",
                "hasil_numpy = (data_raw * 1.05) - 2.3\n",
                "t_numpy = (time.perf_counter() - t0) * 1000\n",
                "\n",
                "speedup = t_loop / t_numpy\n",
                "print(f\"Waktu Loop Python Murni : {t_loop:.2f} ms\")\n",
                "print(f\"Waktu List Comprehension: {t_comp:.2f} ms\")\n",
                "print(f\"Waktu Vektorisasi NumPy : {t_numpy:.2f} ms\")\n",
                "print(f\"--> Percepatan Komputasi NumPy: {speedup:.1f}x LEBIH CEPAT!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Mekanisme Penyiaran (*Broadcasting Rules*)\n",
                "\n",
                "Operasi penambahan matriks dosis pupuk $(4, 1)$ dengan faktor koreksi cuaca afdeling $(1, 3)$ menghasilkan matriks $(4, 3)$ tanpa duplikasi data fisik."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Matriks A: Dosis Pupuk Dasar 4 Blok (Shape: 4 x 1)\n",
                "dosis_dasar = np.array([[2.5], [3.0], [3.8], [4.2]]) # kg/pokok\n",
                "\n",
                "# Larik B: Faktor Koreksi Keasaman Tanah 3 Afdeling (Shape: 1 x 3)\n",
                "faktor_koreksi = np.array([[0.1, 0.25, -0.15]])\n",
                "\n",
                "# Broadcasting otomatis\n",
                "dosis_efektif = dosis_dasar + faktor_koreksi\n",
                "\n",
                "print(f\"Shape Dosis Dasar   : {dosis_dasar.shape}\")\n",
                "print(f\"Shape Faktor Koreksi: {faktor_koreksi.shape}\")\n",
                "print(f\"Shape Dosis Efektif : {dosis_efektif.shape}\")\n",
                "print(\"\\nMatriks Hasil Dosis Efektif (kg/pokok):\")\n",
                "print(np.round(dosis_efektif, 2))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Disiplin Memori: Pembuktian *View* vs *Copy*\n",
                "\n",
                "Memahami perbedaan antara *view* yang berbagi memori dengan *copy* yang independen sangat penting untuk mencegah efek samping mutasi data."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "induk_array = np.array([10.0, 20.0, 30.0, 40.0, 50.0])\n",
                "\n",
                "# 1. Slicing menghasilkan VIEW\n",
                "view_irisan = induk_array[1:4]\n",
                "print(\"Apakah view_irisan berbagi memori dengan induk?\", np.shares_memory(induk_array, view_irisan))\n",
                "\n",
                "# Mutasi pada view mengubah data induk!\n",
                "view_irisan[0] = 999.0\n",
                "print(\"Nilai Array Induk Pasca-Mutasi View:\", induk_array)\n",
                "\n",
                "# 2. Copy menghasilkan ALOKASI MEMORI BARU\n",
                "copy_aman = induk_array[1:4].copy()\n",
                "print(\"Apakah copy_aman berbagi memori dengan induk?\", np.shares_memory(induk_array, copy_aman))\n",
                "copy_aman[0] = -555.0\n",
                "print(\"Array Induk Tetap Aman:\", induk_array)\n",
                "print(\"Array Copy Termodifikasi:\", copy_aman)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Aljabar Linear Terapan (`numpy.linalg`)\n",
                "\n",
                "Pemecahan sistem persamaan simultan produksi uap energi tiga stasiun turbin pabrik kelapa sawit ($A \\mathbf{x} = \\mathbf{b}$)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Matriks Koefisien A dan Vektor Hasil b\n",
                "A = np.array([\n",
                "    [2.0, 3.0, 1.0],\n",
                "    [4.0, 1.0, 2.0],\n",
                "    [3.0, 2.0, 4.0]\n",
                "])\n",
                "b = np.array([2800.0, 3200.0, 4200.0])\n",
                "\n",
                "# 1. Hitung Determinan Matriks A\n",
                "det_A = np.linalg.det(A)\n",
                "print(f\"Determinan Matriks A: {det_A:.2f}\")\n",
                "\n",
                "if np.abs(det_A) > 1e-6:\n",
                "    # 2. Selesaikan Sistem Persamaan Linier\n",
                "    solusi_turbin = np.linalg.solve(A, b)\n",
                "    print(f\"Daya Turbin 1 (T1) : {solusi_turbin[0]:.2f} kWh\")\n",
                "    print(f\"Daya Turbin 2 (T2) : {solusi_turbin[1]:.2f} kWh\")\n",
                "    print(f\"Daya Turbin 3 (T3) : {solusi_turbin[2]:.2f} kWh\")\n",
                "    \n",
                "    # 3. Verifikasi Solusi (A @ x - b == 0)\n",
                "    residu = np.allclose(A @ solusi_turbin, b)\n",
                "    print(f\"Apakah solusi valid dan terverifikasi? {residu}\")\n",
                "else:\n",
                "    print(\"Matriks singular, tidak ada solusi unik tunggal!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Studi Kasus Komputasi Grid: Kalkulasi Cepat Citra NDVI Kanopi\n",
                "\n",
                "Simulasi kalkulasi indeks vegetasi kanopi kebun berdimensi $100 \\times 100$ piksel (10.000 titik observasi spasial)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Membuat Grid Reflektansi NIR dan RED\n",
                "np.random.seed(101)\n",
                "grid_size = 100\n",
                "nir_band = np.random.uniform(0.35, 0.90, size=(grid_size, grid_size)).astype(np.float32)\n",
                "red_band = np.random.uniform(0.05, 0.30, size=(grid_size, grid_size)).astype(np.float32)\n",
                "\n",
                "# Suntikkan zona genangan air/tanah terbuka (NIR rendah, RED tinggi)\n",
                "nir_band[20:40, 20:40] = 0.12\n",
                "red_band[20:40, 20:40] = 0.28\n",
                "\n",
                "# Kalkulasi Tervektorisasi NDVI dengan Proteksi Epsilon Pembagian Nol\n",
                "eps = 1e-7\n",
                "ndvi = (nir_band - red_band) / (nir_band + red_band + eps)\n",
                "\n",
                "# Boolean Masking: Identifikasi Kanopi Sehat (NDVI >= 0.65)\n",
                "mask_sehat = ndvi >= 0.65\n",
                "rasio_sehat = (np.sum(mask_sehat) / ndvi.size) * 100\n",
                "\n",
                "print(f\"Rentang Nilai NDVI : [{ndvi.min():.3f}, {ndvi.max():.3f}]\")\n",
                "print(f\"Rata-rata NDVI     : {ndvi.mean():.3f}\")\n",
                "print(f\"Persentase Kanopi Sehat (NDVI >= 0.65): {rasio_sehat:.2f}%\")\n",
                "\n",
                "# Visualisasi Peta Spasial NDVI\n",
                "plt.figure(figsize=(8, 6), dpi=150)\n",
                "plt.imshow(ndvi, cmap='RdYlGn', vmin=-0.5, vmax=1.0)\n",
                "plt.colorbar(label='Indeks Vegetasi NDVI')\n",
                "plt.title('Peta Spasial NDVI Kanopi Kelapa Sawit (100x100 Grid)', fontsize=12, fontweight='bold', pad=12)\n",
                "plt.tight_layout()\n",
                "plt.savefig('e:/Project Buku/docs/assets/praktikum_4_2_ndvi.png', dpi=150)\n",
                "print(\"Peta NDVI berhasil disimpan ke docs/assets/praktikum_4_2_ndvi.png\")\n",
                "print(\"Praktikum Modul 4.2 Selesai dengan Sukses!\")"
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

target_nb = r'e:\Project Buku\notebooks\part-04\AI_Modul_4.2_Praktikum_NumPy_Komputasi_Numerik.ipynb'
with open(target_nb, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Jupyter Notebook successfully written to {target_nb}")
