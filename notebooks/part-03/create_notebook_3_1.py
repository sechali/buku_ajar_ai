import json
import os
import sys

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a href=\"https://colab.research.google.com/\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>\n",
    "\n",
    "# AI Modul 3.1: Praktikum Pengenalan Bahasa Python\n",
    "### Filosofi Perancangan PEP 20, Arsitektur Mesin Virtual CPython, Komparasi Paradigma Eksekusi, dan Ekosistem Saintifik untuk Pertanian Cerdas\n",
    "\n",
    "---\n",
    "\n",
    "> **Diktat Terkait:** [AI_Modul_3.1_Pengenalan_Bahasa_Python.md](../../docs/part-03/AI_Modul_3.1_Pengenalan_Bahasa_Python.md)  \n",
    "> **Outputs:** Skrip audit spesifikasi interpreter CPython, inspeksi alur eksekusi bytecode via modul `dis`, serta pipeline uji latensi komputasi numerik telemetri sensor iklim mikro perkebunan kelapa sawit.  \n",
    "> **Outcomes:** Mahasiswa menguasai 19 aforisme *The Zen of Python* (PEP 20), memahami rantai kompilasi internal CPython (Token -> AST -> Bytecode -> PVM), dan mampu menganalisis peran strategis Python sebagai bahasa perekat (*glue language*) ekosistem AI.  \n",
    "> **Impacts:** Terciptanya kode prototipe AI agriteknologi yang modular, mudah dipelihara, hemat sumber daya komputasi tepi (*Edge AI*), dan siap diskalakan ke kerangka kerja deep learning industri.\n",
    ">\n",
    "> **Tujuan Praktikum:**  \n",
    "> 1. Mengaudit profil dan konfigurasi memori interpreter Python aktif.  \n",
    "> 2. Membedah instruksi mesin virtual (PVM bytecode) menggunakan modul standar `dis`.  \n",
    "> 3. Mengukur komparasi latensi komputasi antara perulangan standar, list comprehension, dan vektorisasi numerik.  \n",
    "> 4. Menjalankan pipeline diagnostik industri `AuditorSistemAI`.  \n",
    "> 5. Menyelesaikan 3 tantangan scaffolded: verifikator versi sistem, analisis frekuensi opcode bytecode, dan komparator performa telemetri sensorik."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Persiapan Environment & Pemuatan Library\n",
    "Jalankan sel berikut untuk memuat pustaka bawaan CPython dan modul visualisasi saintifik:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import dis\n",
    "import sys\n",
    "import os\n",
    "import platform\n",
    "import time\n",
    "from dataclasses import dataclass\n",
    "from typing import Any, Dict, List, Tuple\n",
    "\n",
    "# Modul saintifik numerik & visualisasi\n",
    "import numpy as np\n",
    "import matplotlib\n",
    "matplotlib.use('Agg')\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Konfigurasi visualisasi grafik\n",
    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
    "plt.rcParams['figure.dpi'] = 120\n",
    "plt.rcParams['font.size'] = 10\n",
    "\n",
    "print(\"[OK] Seluruh pustaka dasar dan analitika berhasil diinisialisasi.\")\n",
    "print(f\"[INFO] Interpreter Aktif : {sys.executable}\")\n",
    "print(f\"[INFO] Versi CPython     : {sys.version.split()[0]} ({platform.architecture()[0]})\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Eksplorasi Filosofi PEP 20 (*The Zen of Python*) & Audit Runtime\n",
    "Menampilkan pedoman desain resmi Python dan memverifikasi arsitektur perangkat keras serta kapasitas memori interpreter."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Memanggil filosofi resmi The Zen of Python (PEP 20)\n",
    "import this\n",
    "\n",
    "# 2. Audit Konfigurasi Tingkat Rendah Runtime\n",
    "print(\"\\n\" + \"=\" * 65)\n",
    "print(\"AUDIT KONFIGURASI SISTEM RUNTIME CPYTHON\")\n",
    "print(\"=\" * 65)\n",
    "print(f\"Nama Sistem Operasi   : {os.name} ({sys.platform})\")\n",
    "print(f\"Kernel Rilis Platform : {platform.platform()}\")\n",
    "print(f\"Arsitektur Byte-Order : {sys.byteorder.upper()} Endian\")\n",
    "print(f\"Batas Maksimum Integer: {sys.maxsize:,} (Indikator Sistem 64-Bit)\")\n",
    "print(f\"Implementasi Python   : {platform.python_implementation()} {platform.python_version()}\")\n",
    "print(f\"Build Compiler C      : {platform.python_compiler()}\")\n",
    "print(\"=\" * 65)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Pembedahan Bytecode CPython Menggunakan Modul `dis`\n",
    "Membuktikan secara empiris bahwa Python mengompilasi kode program menjadi instruksi perantara (*bytecode*) sebelum dieksekusi oleh mesin virtual (*PVM*)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Definisi fungsi agronomis: Koreksi Kalibrasi Resistor Sensor Tanah\n",
    "def kalibrasi_sensor_tanah(adc_raw: float, offset: float) -> float:\n",
    "    return (adc_raw * 0.05) + offset\n",
    "\n",
    "print(\"=== PEMBEDAAN BYTECODE CPYTHON (DISASSEMBLER) ===\")\n",
    "print(f\"Nama Objek Fungsi: {kalibrasi_sensor_tanah.__name__}\")\n",
    "print(\"Instruksi Bytecode Python Virtual Machine (PVM):\\n\")\n",
    "dis.dis(kalibrasi_sensor_tanah)\n",
    "\n",
    "# Inspeksi Atribut Internal Kode Objek (__code__)\n",
    "kode_objek = kalibrasi_sensor_tanah.__code__\n",
    "print(\"\\n=== INSPEKSI METADATA KODE OBJEK (PyCodeObject) ===\")\n",
    "print(f\"Konstanta Terikat (co_consts) : {kode_objek.co_consts}\")\n",
    "print(f\"Variabel Lokal (co_varnames)  : {kode_objek.co_varnames}\")\n",
    "print(f\"Jumlah Argumen (co_argcount)  : {kode_objek.co_argcount}\")\n",
    "print(f\"Ukuran Stack Maks (co_stacksize): {kode_objek.co_stacksize}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Analisis Latensi Komputasi Numerik Aliran Telemetri Perkebunan\n",
    "Membandingkan efisiensi waktu pemrosesan antara perulangan imperatif `for` standar, deklaratif `list comprehension`, dan vektorisasi larik `NumPy` pada $N = 500.000$ titik data telemetri kelembaban tanah."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "N_SAMPEL = 500_000\n",
    "print(f\"[INFO] Membangkitkan dataset telemetri tiruan ({N_SAMPEL:,} sampel)...\")\n",
    "data_sensor_list = [20.0 + (i % 30) * 0.5 for i in range(N_SAMPEL)]\n",
    "data_sensor_np = np.array(data_sensor_list, dtype=np.float64)\n",
    "\n",
    "# 1. Pendekatan Imperatif: Perulangan For Standar dengan list.append()\n",
    "t0 = time.perf_counter()\n",
    "hasil_loop = []\n",
    "for val in data_sensor_list:\n",
    "    norm = (val - 20.0) / 15.0\n",
    "    hasil_loop.append(norm)\n",
    "t_loop = (time.perf_counter() - t0) * 1000.0  # milidetik\n",
    "\n",
    "# 2. Pendekatan Deklaratif: List Comprehension\n",
    "t0 = time.perf_counter()\n",
    "hasil_comp = [(val - 20.0) / 15.0 for val in data_sensor_list]\n",
    "t_comp = (time.perf_counter() - t0) * 1000.0  # milidetik\n",
    "\n",
    "# 3. Pendekatan Vektorisasi Saintifik: NumPy SIMD Array\n",
    "t0 = time.perf_counter()\n",
    "hasil_np = (data_sensor_np - 20.0) / 15.0\n",
    "t_np = (time.perf_counter() - t0) * 1000.0    # milidetik\n",
    "\n",
    "print(\"\\n\" + \"=\" * 75)\n",
    "print(f\"{'Metode Komputasi Numerik':<30} | {'Waktu (ms)':<15} | {'Faktor Percepatan'}\")\n",
    "print(\"-\" * 75)\n",
    "print(f\"{'1. Perulangan For Standar':<30} | {t_loop:<15.3f} | {'Baseline (1.0x)'}\")\n",
    "print(f\"{'2. List Comprehension':<30} | {t_comp:<15.3f} | {t_loop/t_comp:>13.2f}x\")\n",
    "print(f\"{'3. Vektorisasi NumPy (SIMD)':<30} | {t_np:<15.3f} | {t_loop/max(t_np, 1e-6):>13.2f}x\")\n",
    "print(\"=\" * 75)\n",
    "\n",
    "# Visualisasi Komparasi Latensi Komputasi\n",
    "metode_labels = ['Perulangan For\\n(append)', 'List\\nComprehension', 'NumPy Array\\n(SIMD C-Kernel)']\n",
    "durasi_values = [t_loop, t_comp, t_np]\n",
    "warna = ['indianred', 'steelblue', 'forestgreen']\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(8, 4.5))\n",
    "bars = ax.bar(metode_labels, durasi_values, color=warna, edgecolor='black', width=0.5)\n",
    "ax.set_ylabel('Waktu Eksekusi (milidetik)', fontweight='bold')\n",
    "ax.set_title(f'Komparasi Latensi Komputasi Numerik Python (N = {N_SAMPEL:,} Sampel)', fontweight='bold', fontsize=11)\n",
    "\n",
    "for bar in bars:\n",
    "    h = bar.get_height()\n",
    "    ax.text(bar.get_x() + bar.get_width()/2., h + max(durasi_values)*0.02,\n",
    "            f'{h:.2f} ms', ha='center', va='bottom', fontweight='bold', fontsize=9)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig('docs/assets/komparasi_latensi_komputasi_python.png', dpi=150)\n",
    "print(\"\\n[INFO] Grafik komparasi performa berhasil disimpan ke 'docs/assets/komparasi_latensi_komputasi_python.png'.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Implementasi Terpadu Pipeline Industri: `AuditorSistemAI`\n",
    "Mengeksekusi sistem audit terintegrasi berbasis dataclass dan clean architecture untuk memverifikasi kesiapan lingkungan komputasi cerdas."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "@dataclass(frozen=True)\n",
    "class ProfilInterpreter:\n",
    "    \"\"\"Objek data audit lingkungan eksekusi interpreter CPython.\"\"\"\n",
    "    versi_python: str\n",
    "    arsitektur_os: str\n",
    "    nama_platform: str\n",
    "    jalur_eksekusi: str\n",
    "    dukungan_64bit: bool\n",
    "\n",
    "\n",
    "class AuditorSistemAI:\n",
    "    \"\"\"\n",
    "    Auditor infrastruktur komputasi untuk memastikan kesiapan sistem\n",
    "    sebelum menjalankan model kecerdasan buatan perkebunan.\n",
    "    \"\"\"\n",
    "    @staticmethod\n",
    "    def periksa_profil_interpreter() -> ProfilInterpreter:\n",
    "        \"\"\"Mengidentifikasi rincian platform dan lingkungan kerja interpreter aktif.\"\"\"\n",
    "        return ProfilInterpreter(\n",
    "            versi_python=sys.version.split()[0],\n",
    "            arsitektur_os=platform.architecture()[0],\n",
    "            nama_platform=platform.platform(),\n",
    "            jalur_eksekusi=sys.executable,\n",
    "            dukungan_64bit=sys.maxsize > 2**32\n",
    "        )\n",
    "\n",
    "    @staticmethod\n",
    "    def benchmark_komputasi_telemetri(n_sampel: int = 100_000) -> Dict[str, float]:\n",
    "        \"\"\"Menguji throughput pemrosesan data sensor perkebunan.\"\"\"\n",
    "        pembacaan_sensor = [round(20.0 + (i % 30) * 0.5, 2) for i in range(n_sampel)]\n",
    "        waktu_mulai = time.perf_counter()\n",
    "        hasil = [(nilai - 20.0) / 15.0 for nilai in pembacaan_sensor]\n",
    "        durasi = time.perf_counter() - waktu_mulai\n",
    "        return {\n",
    "            \"jumlah_sampel\": float(n_sampel),\n",
    "            \"total_waktu_detik\": round(durasi, 6),\n",
    "            \"rerata_latensi_us\": round((durasi / n_sampel) * 1_000_000.0, 4),\n",
    "            \"throughput_sampel_per_detik\": round(n_sampel / max(durasi, 1e-9), 2)\n",
    "        }\n",
    "\n",
    "# Eksekusi Audit Sistem\nauditor = AuditorSistemAI()\n",
    "profil_sistem = auditor.periksa_profil_interpreter()\n",
    "hasil_telemetri = auditor.benchmark_komputasi_telemetri(200_000)\n",
    "\n",
    "print(\"=\" * 75)\n",
    "print(\"LAPORAN AUDIT KESIAPAN INFRASTRUKTUR AI INSTIPER\")\n",
    "print(\"=\" * 75)\n",
    "print(f\"Versi Runtime Python : {profil_sistem.versi_python} (64-Bit: {profil_sistem.dukungan_64bit})\")\n",
    "print(f\"Platform Kernel Host : {profil_sistem.nama_platform}\")\n",
    "print(f\"Throughput Pemrosesan: {hasil_telemetri['throughput_sampel_per_detik']:,} data sensor/detik\")\n",
    "print(f\"Latensi Per Titik    : {hasil_telemetri['rerata_latensi_us']} mikrodetik\")\n",
    "print(\"=\" * 75)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Solusi Lengkap Tantangan Pemrograman Berjenjang\n",
    "Berikut adalah implementasi komprehensif dari ketiga tantangan mandiri yang terdapat pada diktat perkuliahan:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Tantangan 1 (Tingkat Dasar): Verifikator Integritas Lingkungan Komputasi AI Kebun\n",
    "Memeriksa kesesuaian versi minimal Python (>= 3.10) dan arsitektur 64-bit sebelum menjalankan pipeline AI."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def audit_lingkungan_komputasi(min_versi_mayor: int = 3, min_versi_minor: int = 10) -> Dict[str, Any]:\n",
    "    \"\"\"\n",
    "    Memvalidasi apakah interpreter Python memenuhi spesifikasi minimal praktikum AI.\n",
    "    \"\"\"\n",
    "    v = sys.version_info\n",
    "    is_version_ok = (v.major > min_versi_mayor) or (v.major == min_versi_mayor and v.minor >= min_versi_minor)\n",
    "    is_64bit = sys.maxsize > 2**32\n",
    "    status_layak = is_version_ok and is_64bit\n",
    "    \n",
    "    pesan = \"Lingkungan Komputasi Terverifikasi Layak untuk AI Perkebunan.\"\n",
    "    if not is_version_ok:\n",
    "        pesan = f\"Versi Python tidak memadai ({v.major}.{v.minor}). Dibutuhkan minimal Python {min_versi_mayor}.{min_versi_minor}.\"\n",
    "    elif not is_64bit:\n",
    "        pesan = \"Sistem berjalan pada 32-bit. Diperlukan arsitektur 64-bit untuk menangani alokasi memori tensor.\"\n",
    "        \n",
    "    return {\n",
    "        \"status_layak\": status_layak,\n",
    "        \"versi_aktif\": f\"{v.major}.{v.minor}.{v.micro}\",\n",
    "        \"arsitektur\": \"64-Bit\" if is_64bit else \"32-Bit\",\n",
    "        \"pesan_diagnostik\": pesan\n",
    "    }\n",
    "\n",
    "# Pengujian Tantangan 1\nhasil_audit = audit_lingkungan_komputasi()\n",
    "print(\"=== TANTANGAN 1: AUDIT INTEGRITAS LINGKUNGAN KOMPUTASI ===\")\n",
    "print(f\"Status Kelayakan : {hasil_audit['status_layak']}\")\n",
    "print(f\"Versi Terdeteksi : {hasil_audit['versi_aktif']} ({hasil_audit['arsitektur']})\")\n",
    "print(f\"Pesan Diagnostik : {hasil_audit['pesan_diagnostik']}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Tantangan 2 (Tingkat Menengah): Analis Pola Bytecode Instruksi Aritmetika Sensor via Modul `dis`\n",
    "Memanfaatkan `dis.get_instructions()` untuk mengekstraksi dan menghitung distribusi opcode pada fungsi penghitung indeks defisit air."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def hitung_instruksi_bytecode(fungsi_target: Any) -> Dict[str, Any]:\n",
    "    \"\"\"\n",
    "    Menganalisis dan mengelompokkan instruksi bytecode PVM pada objek fungsi Python.\n",
    "    \"\"\"\n",
    "    instruksi = list(dis.get_instructions(fungsi_target))\n",
    "    frekuensi_opcode: Dict[str, int] = {}\n",
    "    \n",
    "    for inst in instruksi:\n",
    "        op = inst.opname\n",
    "        frekuensi_opcode[op] = frekuensi_opcode.get(op, 0) + 1\n",
    "        \n",
    "    return {\n",
    "        \"nama_fungsi\": fungsi_target.__name__,\n",
    "        \"total_instruksi\": len(instruksi),\n",
    "        \"distribusi_opcode\": frekuensi_opcode,\n",
    "        \"daftar_urutan_opname\": [inst.opname for inst in instruksi]\n",
    "    }\n",
    "\n",
    "# Definisi fungsi uji: Indeks Defisit Air Lahan (Water Deficit Index)\n",
    "def hitung_defisit_air_manual(evapotranspirasi: float, curah_hujan: float) -> float:\n",
    "    defisit = evapotranspirasi - curah_hujan\n",
    "    if defisit > 0.0:\n",
    "        return defisit\n",
    "    return 0.0\n",
    "\n",
    "def hitung_defisit_air_ringkas(evapotranspirasi: float, curah_hujan: float) -> float:\n",
    "    return max(0.0, evapotranspirasi - curah_hujan)\n",
    "\n",
    "hasil_bc_manual = hitung_instruksi_bytecode(hitung_defisit_air_manual)\n",
    "hasil_bc_ringkas = hitung_instruksi_bytecode(hitung_defisit_air_ringkas)\n",
    "\n",
    "print(\"=== TANTANGAN 2: ANALISIS DISTRIBUSI BYTECODE INSTRUKSI ===\")\n",
    "print(f\"1. Fungsi Manual ({hasil_bc_manual['nama_fungsi']}):\")\n",
    "print(f\"   - Total Instruksi : {hasil_bc_manual['total_instruksi']} opcode\")\n",
    "print(f\"   - Distribusi Opcode: {hasil_bc_manual['distribusi_opcode']}\")\n",
    "\n",
    "print(f\"\\n2. Fungsi Ringkas ({hasil_bc_ringkas['nama_fungsi']}):\")\n",
    "print(f\"   - Total Instruksi : {hasil_bc_ringkas['total_instruksi']} opcode\")\n",
    "print(f\"   - Distribusi Opcode: {hasil_bc_ringkas['distribusi_opcode']}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Tantangan 3 (Tingkat Mahir): Simulator Komparasi Latensi Komputasi Aliran Sensorik\n",
    "Membangun kelas `KomparatorPerformaNumerik` yang membandingkan perulangan standar imperatif versus list comprehension deklaratif pada skala $N = 500.000$ telemetri sensor."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "class KomparatorPerformaNumerik:\n",
    "    \"\"\"\n",
    "    Simulator komparasi latensi komputasi transformasi data sensorik perkebunan\n",
    "    skala ratusan ribu sampel antara perulangan imperatif dan komprehensi deklaratif.\n",
    "    \"\"\"\n",
    "    def __init__(self, data_mentah: List[float]) -> None:\n",
    "        self.data_mentah = data_mentah\n",
    "        self.n_elemen = len(data_mentah)\n",
    "\n",
    "    def transformasi_imperatif_loop(self) -> Tuple[List[float], float]:\n",
    "        \"\"\"Transformasi normalisasi menggunakan perulangan for dan append().\"\"\"\n",
    "        t0 = time.perf_counter()\n",
    "        hasil = []\n",
    "        for x in self.data_mentah:\n",
    "            hasil.append((x * 1.08) - 1.5)\n",
    "        durasi_ms = (time.perf_counter() - t0) * 1000.0\n",
    "        return hasil, durasi_ms\n",
    "\n",
    "    def transformasi_deklaratif_comprehension(self) -> Tuple[List[float], float]:\n",
    "        \"\"\"Transformasi normalisasi menggunakan ekspresi List Comprehension.\"\"\"\n",
    "        t0 = time.perf_counter()\n",
    "        hasil = [(x * 1.08) - 1.5 for x in self.data_mentah]\n",
    "        durasi_ms = (time.perf_counter() - t0) * 1000.0\n",
    "        return hasil, durasi_ms\n",
    "\n",
    "    def jalankan_komparasi(self) -> Dict[str, Any]:\n",
    "        _, t_loop = self.transformasi_imperatif_loop()\n",
    "        _, t_comp = self.transformasi_deklaratif_comprehension()\n",
    "        \n",
    "        efisiensi_persen = ((t_loop - t_comp) / max(t_loop, 1e-9)) * 100.0\n",
    "        speedup = t_loop / max(t_comp, 1e-9)\n",
    "        \n",
    "        return {\n",
    "            \"jumlah_sampel\": self.n_elemen,\n",
    "            \"waktu_loop_ms\": round(t_loop, 3),\n",
    "            \"waktu_comprehension_ms\": round(t_comp, 3),\n",
    "            \"speedup_factor\": round(speedup, 2),\n",
    "            \"efisiensi_waktu_persen\": round(efisiensi_persen, 2)\n",
    "        }\n",
    "\n",
    "# Pengujian Tantangan 3\n",
    "dataset_telemetri = [25.0 + (i % 50) * 0.2 for i in range(500_000)]\n",
    "komparator = KomparatorPerformaNumerik(dataset_telemetri)\n",
    "laporan_komparasi = komparator.jalankan_komparasi()\n",
    "\n",
    "print(\"=== TANTANGAN 3: KOMPARASI PERFORMA NUMERIK KOMPREHENSI ===\")\n",
    "print(f\"Ukuran Dataset      : {laporan_komparasi['jumlah_sampel']:,} sampel\")\n",
    "print(f\"Waktu Loop Imperatif: {laporan_komparasi['waktu_loop_ms']} ms\")\n",
    "print(f\"Waktu Comprehension : {laporan_komparasi['waktu_comprehension_ms']} ms\")\n",
    "print(f\"Faktor Percepatan   : {laporan_komparasi['speedup_factor']}x lebih cepat\")\n",
    "print(f\"Reduksi Waktu Latensi: {laporan_komparasi['efisiensi_waktu_persen']}% hemat\")"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

output_path = "notebooks/part-03/AI_Modul_3.1_Praktikum_Pengenalan_Bahasa_Python.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"[BERHASIL] File Jupyter Notebook tersimpan di: {output_path}")
