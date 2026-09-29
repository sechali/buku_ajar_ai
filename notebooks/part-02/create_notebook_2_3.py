import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a href=\"https://colab.research.google.com/\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>\n",
    "\n",
    "# AI Modul 2.3: Praktikum Struktur Logika Pemrograman\n",
    "### Simulasi Aljabar Boolean, Analisis Evaluasi Short-Circuit, Audit Truthiness, dan Mesin Pengunci Keselamatan (Safety Interlock) Agro-Industri\n",
    "\n",
    "---\n",
    "\n",
    "> **Diktat Terkait:** [AI_Modul_2.3_Struktur_Logika_Pemrograman.md](../../docs/part-02/AI_Modul_2.3_Struktur_Logika_Pemrograman.md)  \n",
    "> **Outputs:** Script generator tabel kebenaran interaktif, mesin pembuktian evaluasi *short-circuit* berpresisi mikrodetik, serta implementasi sistem kendali logika predikat multi-sensor untuk greenhouse pembibitan kelapa sawit.  \n",
    "> **Outcomes:** Mahasiswa terampil menyusun ekspresi logika Boolean majemuk, mencegah galat runtime menggunakan *guard pattern*, serta merancang struktur keputusan komputasional yang tangguh dan efisien.  \n",
    "> **Impacts:** Terciptanya sistem otomasi industri perkebunan yang bebas dari kegagalan aktuasi fisik (*failsafe operation*), meminimalisir risiko kerusakan mesin industri bertekanan tinggi, dan mengoptimalkan efisiensi daya komputasi perangkat *Edge AI*.\n",
    ">\n",
    "> **Tujuan Praktikum:**  \n",
    "> 1. Membangun generator tabel kebenaran otomatis untuk operator logika `AND`, `OR`, `NOT`, `XOR`, `NAND`, dan `NOR`.  \n",
    "> 2. Mengukur secara empiris efisiensi waktu eksekusi dan pencegahan galat (*guard pattern*) melalui mekanisme *short-circuit evaluation*.  \n",
    "> 3. Mengaudit nilai *truthiness* dan *falsiness* berbagai tipe data bawaan Python.  \n",
    "> 4. Mengimplementasikan simulasi kontrol keselamatan (*interlock safety*) bejana perebusan (*sterilizer*) dan greenhouse agro-industri."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Persiapan Environment & Pemuatan Library\n",
    "Jalankan sel berikut untuk memuat modul interpreter, pencatat waktu presisi, dan konfigurasi lingkungan:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Mengimpor modul metadata sistem\n",
    "import sys\n",
    "\n",
    "# Mengimpor modul pencatat waktu mikrodetik\n",
    "import time\n",
    "\n",
    "# Mengimpor modul tipe data terstruktur\n",
    "from typing import Dict, List, Tuple, Any, Callable\n",
    "\n",
    "# Mengimpor pustaka numerik dan visualisasi\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Mengatur konfigurasi visualisasi grafik\n",
    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
    "plt.rcParams['figure.dpi'] = 120\n",
    "\n",
    "# Menampilkan informasi versi Python\n",
    "print(f\"Python Version : {sys.version.split()[0]}\")\n",
    "print(\"[OK] Environment praktikum logika komputasi siap digunakan!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Generator Tabel Kebenaran Interaktif (Truth Table Generator)\n",
    "Sel berikut mengimplementasikan mesin pembuat tabel kebenaran untuk menguji semua kemungkinan kombinasi masukan biner terhadap berbagai operator logika."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def tampilkan_tabel_kebenaran_lengkap() -> None:\n",
    "    \"\"\"Menghasilkan tabel kebenaran komparatif untuk 6 gerbang logika utama.\"\"\"\n",
    "    kombinasi_input = [(False, False), (False, True), (True, False), (True, True)]\n",
    "    \n",
    "    print(\"=\" * 85)\n",
    "    print(\"TABEL KEBENARAN KOMPARATIF OPERATOR LOGIKA BOOLEAN\")\n",
    "    print(\"=\" * 85)\n",
    "    header = f\"{'A':<6} | {'B':<6} | {'AND':<7} | {'OR':<7} | {'XOR':<7} | {'NAND':<7} | {'NOR':<7} | {'NOT A'}\"\n",
    "    print(header)\n",
    "    print(\"-\" * 85)\n",
    "    \n",
    "    for a, b in kombinasi_input:\n",
    "        val_and  = a and b\n",
    "        val_or   = a or b\n",
    "        val_xor  = a != b  # XOR biner dalam Python dinyatakan sebagai a != b\n",
    "        val_nand = not (a and b)\n",
    "        val_nor  = not (a or b)\n",
    "        val_nota = not a\n",
    "        \n",
    "        print(f\"{str(a):<6} | {str(b):<6} | {str(val_and):<7} | {str(val_or):<7} | \"\n",
    "              f\"{str(val_xor):<7} | {str(val_nand):<7} | {str(val_nor):<7} | {str(val_nota)}\")\n",
    "        \n",
    "    print(\"=\" * 85)\n",
    "    print(\"[INFO] Seluruh kombinasi kondisi biner terverifikasi konsisten.\\n\")\n",
    "\n",
    "# Menjalankan fungsi tabel kebenaran\n",
    "tampilkan_tabel_kebenaran_lengkap()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Investigasi Efek Evaluasi Short-Circuit & Guard Pattern\n",
    "Kita akan menguji secara empiris bahwa Python menghentikan evaluasi jika operan pertama sudah menentukan hasil akhir."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def fungsi_komputasi_berat(label: str, hasil_return: bool, delay_ms: float = 20.0) -> bool:\n",
    "    \"\"\"Mensimulasikan fungsi inferensi model AI yang membutuhkan waktu pemrosesan.\"\"\"\n",
    "    print(f\"   --> [EKSEKUSI INTENSIF] Model AI '{label}' sedang memproses data...\")\n",
    "    time.sleep(delay_ms / 1000.0)  # Simulasi latensi komputasi\n",
    "    return hasil_return\n",
    "\n",
    "print(\"=\" * 75)\n",
    "print(\"UJI KASUS 1: SHORT-CIRCUIT PADA OPERASI 'AND'\")\n",
    "print(\"=\" * 75)\n",
    "print(\"Skenario A: Operan pertama bernilai FALSE (Short-Circuit Aktif)\")\n",
    "t_awal = time.perf_counter()\n",
    "# Karena False, fungsi_komputasi_berat TIDAK AKAN PERNAH dipanggil!\n",
    "hasil_a = False and fungsi_komputasi_berat(\"Deteksi_YOLO\", True)\n",
    "t_akhir = time.perf_counter()\n",
    "print(f\"Hasil Evaluasi: {hasil_a} | Durasi: {(t_akhir - t_awal)*1000:.4f} ms (Sangat Instan!)\")\n",
    "\n",
    "print(\"\\nSkenario B: Operan pertama bernilai TRUE (Short-Circuit Tidak Aktif)\")\n",
    "t_awal = time.perf_counter()\n",
    "# Karena True, operan kedua HARUS dievaluasi!\n",
    "hasil_b = True and fungsi_komputasi_berat(\"Deteksi_YOLO\", True)\n",
    "t_akhir = time.perf_counter()\n",
    "print(f\"Hasil Evaluasi: {hasil_b} | Durasi: {(t_akhir - t_awal)*1000:.2f} ms (Ada Latensi Sensor)\")\n",
    "\n",
    "print(\"\\n\" + \"=\" * 75)\n",
    "print(\"UJI KASUS 2: PENCEGAHAN ERROR RUNTIME DENGAN GUARD PATTERN\")\n",
    "print(\"=\" * 75)\n",
    "# Mencegah ZeroDivisionError saat sensor mengirimkan jumlah sampel nol\n",
    "sampel_data = []\n",
    "# Guard condition: len(sampel_data) > 0 diletakkan di kiri\n",
    "if len(sampel_data) > 0 and (sum(sampel_data) / len(sampel_data)) > 50.0:\n",
    "    print(\"Rata-rata memenuhi ambang batas\")\n",
    "else:\n",
    "    print(\"[AMAL PROTEKSI] ZeroDivisionError berhasil dicegah secara otomatis oleh Short-Circuit!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Audit Nilai Truthiness dan Falsiness Objek Python\n",
    "Dalam Python, berbagai struktur data memiliki nilai kebenaran implisit. Mari kita audit beberapa objek lingkungan agro-industri:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "daftar_objek_uji = [\n",
    "    (\"Angka Nol (0)\", 0),\n",
    "    (\"Float Nol (0.0)\", 0.0),\n",
    "    (\"Angka Positif (42)\", 42),\n",
    "    (\"Angka Negatif (-15.5)\", -15.5),\n",
    "    (\"String Kosong ('')\", \"\"),\n",
    "    (\"String Berisi Spasi (' ')\", \" \"),\n",
    "    (\"String Teks ('Sawit')\", \"Sawit\"),\n",
    "    (\"List Kosong ([])\", []),\n",
    "    (\"List Berisi Elemen ([0])\", [0]),\n",
    "    (\"Konstanta None\", None)\n",
    "]\n",
    "\n",
    "print(\"=\" * 70)\n",
    "print(\"AUDIT NILAI TRUTHINESS & FALSINESS PADA TIPE DATA PYTHON\")\n",
    "print(\"=\" * 70)\n",
    "print(f\"{'Deskripsi Objek':<28} | {'Tipe Data':<14} | {'Evaluasi Boolean'}\")\n",
    "print(\"-\" * 70)\n",
    "for desc, obj in daftar_objek_uji:\n",
    "    bool_val = bool(obj)\n",
    "    status_str = \"[TRUTHY] -> True\" if bool_val else \"[FALSY]  -> False\"\n",
    "    print(f\"{desc:<28} | {type(obj).__name__:<14} | {status_str}\")\n",
    "print(\"=\" * 70)\n",
    "print(\"[INFO] Pemahaman truthiness mencegah bug kondisional implisit.\\n\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Studi Kasus Agro-Industri: Mesin Logika Kontrol Greenhouse Multi-Sensor\n",
    "Kita mengimplementasikan fungsi evaluasi logika kendali mikroklimat pembibitan kelapa sawit yang memadukan parameter agronomis dan pengunci keselamatan fisik (*safety interlock*)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def kontrol_greenhouse_sawit(suhu: float, rh: float, hujan: bool, level_air: float) -> Tuple[bool, str]:\n",
    "    \"\"\"\n",
    "    Mengevaluasi keputusan aktuasi pompa kabut pendingin berbasis aljabar Boolean.\n",
    "    \n",
    "    Formula Boolean:\n",
    "        Y = (Suhu > 32.0 and RH < 50.0 and not Hujan) and (Level_Air >= 20.0)\n",
    "    \"\"\"\n",
    "    # Evaluasi Predikat Sensorik\n",
    "    butuh_pendingin = (suhu > 32.0) and (rh < 50.0) and (not hujan)\n",
    "    izin_air_aman = (level_air >= 20.0)\n",
    "    \n",
    "    # Keputusan Akhir Interlock\n",
    "    pompa_aktif = butuh_pendingin and izin_air_aman\n",
    "    \n",
    "    # Penentuan Status Diagnostik\n",
    "    if pompa_aktif:\n",
    "        pesan = \"POMPA ON: Mendinginkan kanopi bibit sawit (Kondisi Panas-Kering, Air Cukup)\"\n",
    "    elif butuh_pendingin and not izin_air_aman:\n",
    "        pesan = \"ALARM AIR KOSONG: Bibit butuh air, tetapi level tangki di bawah 20%!\"\n",
    "    elif hujan:\n",
    "        pesan = \"STANDBY HUJAN: Irigasi alami eksternal sedang berlangsung\"\n",
    "    else:\n",
    "        pesan = \"STANDBY NORMAL: Iklim mikro berada dalam rentang pertumbuhan optimal\"\n",
    "        \n",
    "    return pompa_aktif, pesan\n",
    "\n",
    "# Dataset Pengujian Empiris\n",
    "skenario_uji = [\n",
    "    {\"blok\": \"GH-1\", \"T\": 35.5, \"RH\": 42.0, \"Hujan\": False, \"Air\": 70.0},  # Harus ON\n",
    "    {\"blok\": \"GH-2\", \"T\": 36.0, \"RH\": 38.0, \"Hujan\": False, \"Air\": 10.0},  # Proteksi Air (OFF)\n",
    "    {\"blok\": \"GH-3\", \"T\": 33.5, \"RH\": 45.0, \"Hujan\": True,  \"Air\": 85.0},  # Hujan (OFF)\n",
    "    {\"blok\": \"GH-4\", \"T\": 28.0, \"RH\": 75.0, \"Hujan\": False, \"Air\": 90.0},  # Nyaman (OFF)\n",
    "]\n",
    "\n",
    "print(\"=\" * 90)\n",
    "print(\"HASIL SIMULASI LOGIKA KONTROL IKLIM MIKRO GREENHOUSE SAWIT INSTIPER\")\n",
    "print(\"=\" * 90)\n",
    "for s in skenario_uji:\n",
    "    aktif, log = kontrol_greenhouse_sawit(s[\"T\"], s[\"RH\"], s[\"Hujan\"], s[\"Air\"])\n",
    "    status_tag = \"[POMPA ON] \" if aktif else \"[POMPA OFF]\"\n",
    "    print(f\"Blok: {s['blok']} | T: {s['T']:4.1f}C | RH: {s['RH']:4.1f}% | Hujan: {str(s['Hujan']):<5} | Air: {s['Air']:4.1f}% | {status_tag} -> {log}\")\n",
    "print(\"=\" * 90)\n",
    "print(\"[OK] Seluruh evaluasi logika kontrol berhasil disimulasikan!\\n\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Tantangan Pemrograman Mandiri (Scaffolded Challenges)\n",
    "\n",
    "### Tantangan: Sistem Pengunci Keselamatan (Safety Interlock) Sterilizer PKS\n",
    "Rancanglah sebuah fungsi logika Python `cek_keselamatan_buka_sterilizer` yang menentukan apakah pintu bejana perebusan buah sawit aman untuk dibuka oleh operator pabrik.\n",
    "\n",
    "**Spesifikasi Aturan:**\n",
    "- Masukan:\n",
    "  - `tekanan_bar` (float, satuan bar)\n",
    "  - `suhu_celsius` (float, satuan derajat Celsius)\n",
    "  - `katup_uap_masuk_terbuka` (boolean)\n",
    "  - `tombol_darurat_aktif` (boolean)\n",
    "- Aturan Keamanan Mutlak:\n",
    "  - Pintu **HANYA BOLEH DIBUKA (`True`)** jika: `tekanan_bar <= 0.1` **DAN** `suhu_celsius <= 50.0` **DAN** `not katup_uap_masuk_terbuka` **DAN** `not tombol_darurat_aktif`.\n",
    "  - Jika salah satu kondisi tidak aman, pintu **WAJIB TERKUNCI (`False`)**."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def cek_keselamatan_buka_sterilizer(tekanan_bar: float, suhu_c: float, \n",
    "                                    katup_uap_buka: bool, darurat: bool) -> Tuple[bool, str]:\n",
    "    \"\"\"\n",
    "    Menentukan kelayakan pembukaan pintu bejana sterilizer pabrik kelapa sawit.\n",
    "    \"\"\"\n",
    "    # Evaluasi Predikat Keamanan Atomik\n",
    "    tekanan_aman = (tekanan_bar <= 0.1)\n",
    "    suhu_aman    = (suhu_c <= 50.0)\n",
    "    uap_mati     = not katup_uap_buka\n",
    "    sistem_siap  = not darurat\n",
    "    \n",
    "    # Konjungsi Seluruh Prasyarat Keamanan\n",
    "    izin_buka = tekanan_aman and suhu_aman and uap_mati and sistem_siap\n",
    "    \n",
    "    if izin_buka:\n",
    "        pesan = \"IZIN DIBERIKAN: Bejana berada dalam status dingin dan bertekanan atmosfer normal.\"\n",
    "    else:\n",
    "        bahaya = []\n",
    "        if not tekanan_aman:\n",
    "            bahaya.append(f\"Tekanan sisa berbahaya ({tekanan_bar:.2f} bar)\")\n",
    "        if not suhu_aman:\n",
    "            bahaya.append(f\"Suhu internal panas ({suhu_c:.1f} C)\")\n",
    "        if not uap_mati:\n",
    "            bahaya.append(\"Katup suplai uap masih terbuka\")\n",
    "        if not sistem_siap:\n",
    "            bahaya.append(\"Tombol darurat sedang ditekan\")\n",
    "        pesan = f\"PINTU TERKUNCI OTOMATIS! Bahaya: {', '.join(bahaya)}\"\n",
    "        \n",
    "    return izin_buka, pesan\n",
    "\n",
    "\n",
    "# Pengujian Unit Otomatis (Test Suite)\n",
    "kasus_uji = [\n",
    "    (0.05, 45.0, False, False, True),   # Aman mutlak -> Buka\n",
    "    (0.80, 45.0, False, False, False),  # Tekanan masih tinggi -> Kunci\n",
    "    (0.05, 95.0, False, False, False),  # Suhu masih panas -> Kunci\n",
    "    (0.05, 45.0, True,  False, False),  # Katup uap masih masuk -> Kunci\n",
    "    (0.05, 45.0, False, True,  False),  # Status darurat -> Kunci\n",
    "]\n",
    "\n",
    "print(\"=\" * 80)\n",
    "print(\"VERIFIKASI PENGUJIAN UNIT LOGIKA SAFETY INTERLOCK STERILIZER PKS\")\n",
    "print(\"=\" * 80)\n",
    "semua_lulus = True\n",
    "for idx, (p, t, k, em, expected) in enumerate(kasus_uji, 1):\n",
    "    hasil, msg = cek_keselamatan_buka_sterilizer(p, t, k, em)\n",
    "    lulus = (hasil == expected)\n",
    "    status_tag = \"LULUS\" if lulus else \"GAGAL\"\n",
    "    print(f\"Uji #{idx} | Tekanan: {p:4.2f} bar | Suhu: {t:4.1f} C | [{status_tag}] -> {msg}\")\n",
    "    if not lulus:\n",
    "        semua_lulus = False\n",
    "\n",
    "print(\"=\" * 80)\n",
    "if semua_lulus:\n",
    "    print(\"[SUCCESS] 100% Kasus Uji Interlock Keselamatan Lulus Sempurna!\")\n",
    "else:\n",
    "    print(\"[ALERT] Ditemukan kegagalan pada pengujian keselamatan.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Rangkuman & Refleksi Praktikum\n",
    "\n",
    "Melalui praktikum ini, kita telah membuktikan secara nyata bahwa:\n",
    "1. **Aljabar Boolean** adalah bahasa formal dari keputusan komputasional. Logika `AND` mengontrol proteksi ketat, sedangkan `OR` mengontrol sistem peringatan redundan.\n",
    "2. **Evaluasi Short-Circuit** bukan sekadar fitur sintaksis, melainkan arsitektur optimasi latensi dan instrumen keamanan (*guard pattern*) untuk mencegah error komputasi yang merusak sistem.\n",
    "3. Logika predikat dalam agro-industri menjamin bahwa aktuator fisik di pabrik sawit dan greenhouse hanya bergerak ketika kondisi agronomis dan persyaratan keselamatan terpenuhi secara mutlak.\n",
    "\n",
    "Lanjutkan eksplorasi ke modul berikutnya: **AI Modul 2.4: Variabel dan Tipe Data** untuk mendalami representasi memori dan sistem pengetikan data!"
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
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

output_path = r"e:\Project Buku\notebooks\part-02\AI_Modul_2.3_Praktikum_Struktur_Logika_Pemrograman.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"Notebook successfully written to {output_path}")
