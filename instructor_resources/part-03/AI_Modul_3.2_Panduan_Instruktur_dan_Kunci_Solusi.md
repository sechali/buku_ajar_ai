# Panduan Instruktur & Kunci Solusi: AI Modul 3.2
## Instalasi dan Environment: Manajemen Instalasi Python, Isolasi Lingkungan Virtual (venv & Conda), Konfigurasi IDE VS Code, Ekosistem Kernel Jupyter, dan Reproduksibilitas Dependensi Proyek AI Agribisnis

---

**Kode Modul:** AI Modul 3.2  
**Target Pengguna:** Dosen Pengampu, Asisten Laboratorium, dan Instruktur Praktikum AI INSTIPER  
**Mata Kuliah Terkait:** Pemrograman Python Dasar untuk Kecerdasan Buatan  
**Alokasi Waktu:** 150 Menit Tatap Muka Teori + 150 Menit Praktikum Komputasi Terbimbing  

---

## 1. Rencana Pelaksanaan Pembelajaran (Lesson Plan)

| Sesi / Menit | Fokus Aktivitas Pembelajaran | Metode & Media Pembelajaran | Peran Instruktur |
| :--- | :--- | :--- | :--- |
| **Menit 001 - 025** | Apersepsi Komputasi: Krisis Reproduksibilitas (*"Works on My Machine"*) di Industri | Studi kasus kegagalan deployment model deteksi sawit di edge computing | Menggugah kesadaran mahasiswa: Mengapa algoritma dengan akurasi 99% tidak berguna jika gagal diinstal pada server pabrik? |
| **Menit 026 - 060** | Arsitektur Variabel Sistem (`PATH`, `PYTHONPATH`, `PYTHONHOME`) & Shebang | Demonstrasi terminal multi-OS (Windows & Linux), Bagan resolusi shell | Membedah mekanisme bagaimana sistem operasi menemukan biner CPython dan bahaya konflik path instalasi global. |
| **Menit 061 - 095** | Isolasi Lingkungan Komputasi: Komparasi Teknis `venv` vs `conda` vs Modern `uv` | Visualisasi diagram isolasi memori dan direktori *site-packages* | Membimbing mahasiswa memahami kapan harus menggunakan `venv` (ringan, edge IoT) versus `conda` (dukungan biner GPU CUDA terisolasi). |
| **Menit 096 - 125** | Manajemen Dependensi: Semantic Versioning, `requirements.txt`, & Pendaftaran Kernel | Live terminal: `venv`, `pip freeze`, dan pendaftaran `ipykernel` | Memandu mahasiswa menghubungkan interpreter virtual lokal ke Visual Studio Code dan Jupyter Notebook. |
| **Menit 126 - 150** | Refleksi Teori & Bedah Masalah Algoritmik Tingkat Tinggi (HOTS) | Diskusi panel ancaman Typosquatting PyPI dan komparasi Docker container | Mengarahkan mahasiswa menganalisis keamanan rantai pasok perangkat lunak (*software supply chain security*). |
| **Praktikum (150m)**| Eksperimen Jupyter: Audit Programatis venv, Parser Manifest, & Snapshot Manager | Hands-on coding terbimbing di Jupyter Notebook | Memfasilitasi mahasiswa memvalidasi status isolasi sistem, membedah requirements.txt, dan mengeksekusi 3 tantangan mandiri. |

---

## 2. Miskonsepsi Umum Mahasiswa & Strategi Remedial

### Miskonsepsi 1: Mengira Memasang Paket Secara Global Lebih Praktis Tanpa Dampak Negatif
* **Gejala Mahasiswa:** Selalu menjalankan `pip install <nama-paket>` secara langsung di terminal utama tanpa membuat atau mengaktifkan virtual environment terlebih dahulu.
* **Strategi Remedial:** Tunjukkan skenario tabrakan versi nyata: mintalah mahasiswa membayangkan Proyek A butuh `NumPy 1.21` (karena arsitektur model lama) dan Proyek B butuh `NumPy 2.0` (karena pustaka visualisasi baru). Tunjukkan bagaimana instalasi global akan saling merusak dan menimpa dependensi tersebut, memaksa instalasi ulang berulang kali (*Dependency Hell*).

### Miskonsepsi 2: Meng-commit Direktori `.venv/` ke dalam Repositori Git Proyek
* **Gejala Mahasiswa:** Melakukan `git add .` dan mengunggah ribuan berkas di dalam folder `.venv/` ke GitHub dengan alasan agar anggota kelompok praktikum tidak perlu menginstal pustaka lagi.
* **Strategi Remedial:** Tunjukkan model internal berkas virtual environment: berkas di dalam `.venv/` memuat *absolute symlink* dan ekstensi biner terkompilasi spesifik untuk sistem operasi dan arsitektur CPU pengunggah (misal biner `.pyd` untuk Windows 64-bit yang mutlak tidak bisa dieksekusi di Linux Ubuntu atau Mac Apple Silicon). Jelaskan aturan baku: **.venv wajib masuk ke `.gitignore`**, dan yang dibagikan hanyalah **manifest deklaratif `requirements.txt`**.

### Miskonsepsi 3: Mengasumsikan Aktivasi Virtualenv di Terminal Otomatis Mengubah Kernel Jupyter
* **Gejala Mahasiswa:** Mengaktifkan `.venv` di terminal, membuka Jupyter Notebook, lalu bingung mengapa perintah `import cv2` tetap menghasilkan `ModuleNotFoundError`.
* **Strategi Remedial:** Jelaskan arsitektur client-server Jupyter: Jupyter menjalankan *notebook server* yang dapat terhubung ke berbagai *kernel* independen. Mengaktifkan virtualenv di terminal shell tidak secara otomatis mendaftarkan environment tersebut ke daftar kernel Jupyter. Ajarkan prosedur pendaftaran resmi:
  `python -m ipykernel install --user --name=sawit-env --display-name="Python (Sawit Env)"`.

### Miskonsepsi 4: Menggunakan `pip freeze` Tanpa Pembersihan untuk Membangun Requirements Produksi
* **Gejala Mahasiswa:** Menjalankan `pip freeze > requirements.txt` pada lingkungan yang sudah tercampur dengan berbagai paket eksperimen acak, sehingga puluhan paket tidak relevan ikut terkunci.
* **Strategi Remedial:** Jelaskan konsep dependensi bersih: lingkungan produksi harus hanya memuat pustaka yang benar-benar diimpor oleh kode aplikasi. Tunjukkan praktik terbaik: selalu inisialisasi virtualenv baru yang bersih khusus untuk proyek tersebut sebelum membekukan requirements, atau manfaatkan pustaka pemindai impor seperti `pipreqs`.

---

## 3. Kunci Jawaban Lengkap Evaluasi HOTS

### Pertanyaan 1: Analisis Kebijakan Version Control: Larangan Commit Virtual Environment dan Prinsip "Infrastructure as Code"
* **Soal:** Mengapa folder `.venv/` dilarang keras di-commit ke Git? Analisis bahaya portabilitas biner dan jelaskan penerapan prinsip *Infrastructure as Code* (IaC) via requirements lockfile!
* **Jawaban Komprehensif:**
  1. **Bahaya Portabilitas Biner dan Kerapuhan Jalur Absolut:**
     - Direktori virtual environment memuat ribuan berkas biner pustaka terkompilasi (seperti berkas Dynamic Link Library `.dll` dan Python Extension Module `.pyd` pada Windows, atau Shared Objects `.so` pada Linux). Biner ini terikat secara kaku pada arsitektur prosesor (x86_64 vs ARM64) dan versi compiler C sistem operasi pengembang. Jika di-commit ke Git dan di-pull oleh rekan kerja dengan sistem operasi berbeda, program akan mengalami *Segmentation Fault* atau kegagalan pemuatan biner seketika.
     - Di dalam skrip aktivasi (`activate` / `activate.ps1`) dan header berkas biner Python lokal, CPython menanamkan **jalur absolut direktori** (`C:\Users\Pengembang\Proyek\.venv\...`). Jika folder dipindahkan atau dibuka pada komputer lain dengan nama pengguna berbeda, seluruh symlink dan pointer interpreter akan putus (*broken links*).
     - Meng-commit `.venv/` membebani repositori Git hingga ratusan megabyte dengan ribuan berkas kecil yang tidak perlu (*repository bloat*).
  2. **Penerapan Prinsip Infrastructure as Code (IaC):**
     Prinsip IaC menyatakan bahwa spesifikasi lingkungan komputasi harus didefinisikan dalam bentuk teks deklaratif yang dapat dikontrol versinya (*version-controlled declarative manifest*), bukan dalam bentuk artefak biner fisik. Berkas `requirements.txt` (atau `poetry.lock` / `conda environment.yml`) bertindak sebagai "cetak biru arsitektural". Siapa pun dapat merekonstruksi infrastruktur komputasi yang 100% identik kapan saja secara otomatis melalui satu perintah reproduksi baku (`pip install -r requirements.txt`).

---

### Pertanyaan 2: Evaluasi Arsitektur Isolasi: `venv` vs Kontainerisasi Docker pada Sistem Edge AI Perkebunan
* **Soal:** Sebuah gerbang IoT cerdas berbasis NVIDIA Jetson dipasang di pos timbangan sawit. Jelaskan perbedaan mendasar tingkat isolasi `venv` vs *Docker Container*, dan mengapa `venv` tidak cukup jika proyek butuh driver GPU CUDA, GStreamer, dan `libGL.so`!
* **Jawaban Komprehensif:**
  1. **Tingkat Isolasi Virtualenv vs Kontainer Docker:**
     - **Python `venv` (Isolasi Tingkat User Space Aplikasi):** Hanya mengisolasi biner interpreter Python dan folder `site-packages`. Virtualenv sama sekali tidak mengisolasi sistem operasi host: ia tetap berbagi pustaka dinamis sistem C/C++ (`glibc`), variabel lingkungan sistem operasi, kernel Linux, dan driver perangkat keras host.
     - **Docker Container (Isolasi Tingkat Kernel Namespace & Cgroups):** Mengisolasi seluruh *root filesystem*, pustaka bersama tingkat OS (*system shared libraries*), alokasi memori, proses, dan antarmuka jaringan menggunakan fitur kernel Linux (*namespaces* dan *control groups*), tanpa overhead virtualisasi penuh (*hypervisor*).
  2. **Mengapa `venv` Gagal Menangani Kebutuhan Edge AI:**
     Pada aplikasi visi komputer cerdas tepi (seperti deteksi mutu buah sawit menggunakan kamera industri resolusi tinggi), performa sangat bergantung pada:
     - Driver grafis perangkat keras: NVIDIA CUDA Driver dan pustaka TensorRT.
     - Pustaka multimedia sistem: Pustaka C++ `GStreamer` untuk akuisisi video RTSP kamera secara real-time.
     - Dependensi grafis OpenGL: Pustaka sistem tingkat OS seperti `libGL.so` dan `libgthread-2.0.so`.
     Pustaka-pustaka tersebut adalah dependensi biner tingkat sistem operasi (*system-level shared objects*), bukan paket Python murni yang bisa dipasang via `pip`. Jika modul Python `opencv-python` membutuhkan `libGL.so` tetapi pustaka tersebut tidak terpasang di OS Jetson, virtualenv akan melempar galat fatal `ImportError: libGL.so.1: cannot open shared object file`. Kontainer Docker membungkus seluruh lapisan pustaka sistem operasi ini ke dalam satu *image* yang utuh, menjamin sistem inferensi berjalan mulus tanpa bergantung pada konfigurasi OS host fisik.

---

### Pertanyaan 3: Audit Keamanan Rantai Pasok (*Supply Chain Attack & Typosquatting*) pada PyPI
* **Soal:** Jelaskan bahaya serangan *Typosquatting* saat memasang pustaka OpenCV (`pip install opencv` vs `opencv-python`), dan bagaimana opsi `--require-hashes` memitigasinya!
* **Jawaban Komprehensif:**
  1. **Mekanisme dan Bahaya Serangan Typosquatting:**
     - *Typosquatting* adalah teknik rekayasa sosial di mana penyerang mendaftarkan paket berbahaya di repositori publik (PyPI) dengan nama yang sangat mirip atau merupakan kesalahan ketik umum (*common typographical error*) dari paket populer (misalnya: mendaftarkan `opencv` untuk mengecoh pengguna yang seharusnya menginstal `opencv-python`, atau `requsts` untuk `requests`).
     - Ketika pengguna mengeksekusi `pip install opencv`, skrip instalasi internal paket (`setup.py` atau build backend) dieksekusi secara otomatis di komputer pengguna dengan hak akses penuh pengguna (*arbitrary code execution*). Peretas dapat menyisipkan kode *malware* tersembunyi yang membaca kunci API cloud kebun, token autentikasi basis data timbangan sawit, atau menanamkan pintu belakang (*backdoor / reverse shell*) ke jaringan intranet perusahaan agribisnis.
  2. **Mitigasi Melalui Mode Pemeriksaan Hash Kriptografis (`--require-hashes`):**
     - Opsi `pip install --require-hashes -r requirements.txt` mewajibkan setiap paket di dalam berkas manifest diverifikasi terhadap nilai intisari kriptografis (*cryptographic digest / SHA-256 hash*) yang telah ditentukan sebelumnya secara eksplisit:
       ```text
       numpy==1.26.4 --hash=sha256:7b7d609210e74b59c256037a34e06821d3f94...
       ```
     - Mekanisme ini memberikan proteksi ganda:
       1. **Integritas Paket (*Anti-Tampering*):** Jika penyerang menyusup ke repositori atau peladen mirror dan mengganti berkas roda biner (`.whl`) dengan versi yang disusupi malware, proses instalasi akan dibatalkan seketika karena nilai hash berkas yang diunduh tidak cocok dengan hash resmi pada manifest.
       2. **Pencegahan Serangan Man-in-the-Middle (MitM):** Mencegah injeksi paket berbahaya saat data melintasi jaringan internet publik yang tidak aman.

---

## 4. Kunci Solusi Tantangan Pemrograman Berjenjang

### Solusi Tantangan 1: Pendeteksi Otomatis Status Virtual Environment
```python
import sys
from typing import Any, Dict


def verifikasi_status_virtualenv() -> Dict[str, Any]:
  """Memvalidasi isolasi environment dan menyediakan instruksi setup terminal yang tepat."""
  is_venv = sys.prefix != sys.base_prefix
  os_name = sys.platform

  if is_venv:
    rekomendasi = (
        "Lingkungan virtual aktif dan aman untuk instalasi dependensi."
    )
  else:
    if os_name == "win32":
      rekomendasi = (
          "Jalankan: python -m venv .venv lalu .venv\\Scripts\\Activate.ps1"
      )
    else:
      rekomendasi = (
          "Jalankan: python3 -m venv .venv lalu source .venv/bin/activate"
      )

  return {
      "terisolasi": is_venv,
      "platform": os_name,
      "direktori_prefix": sys.prefix,
      "rekomendasi_tindakan": rekomendasi,
  }
```

---

### Solusi Tantangan 2: Parser & Validator Berkas Manifest `requirements.txt`
```python
import importlib.metadata
from pathlib import Path
from typing import Any, Dict


def validasi_manifest_requirements(jalur_file: str) -> Dict[str, Any]:
  """Membaca dan memvalidasi integritas pustaka yang tercantum pada requirements.txt."""
  path = Path(jalur_file)
  if not path.exists():
    return {"sukses": False, "pesan": f"Berkas {jalur_file} tidak ditemukan."}

  paket_valid = []
  paket_hilang = []
  paket_mismatch = []

  with path.open("r", encoding="utf-8") as f:
    for baris in f:
      baris = baris.strip()
      if not baris or baris.startswith("#"):
        continue

      if "==" in baris:
        nama, versi_diminta = baris.split("==", 1)
        op = "=="
      elif ">=" in baris:
        nama, versi_diminta = baris.split(">=", 1)
        op = ">="
      else:
        nama, versi_diminta, op = baris, "-", "any"

      nama = nama.strip()
      versi_diminta = versi_diminta.strip()

      try:
        versi_aktif = importlib.metadata.version(nama)
        if op == "==" and versi_aktif != versi_diminta:
          paket_mismatch.append((nama, versi_diminta, versi_aktif))
        else:
          paket_valid.append((nama, versi_aktif))
      except importlib.metadata.PackageNotFoundError:
        paket_hilang.append((nama, versi_diminta))

  return {
      "sukses": True,
      "paket_valid": paket_valid,
      "paket_mismatch": paket_mismatch,
      "paket_hilang": paket_hilang,
      "status_reproduksi_penuh": (
          len(paket_hilang) == 0 and len(paket_mismatch) == 0
      ),
  }
```

---

### Solusi Tantangan 3: Manajer Snapshot dan Penjaga Kompatibilitas Versi Dependensi
```python
import importlib.metadata
from pathlib import Path
from typing import Any, Dict, List


class SnapshotEnvironmentManager:
  """Manajer pelacak snapshot versi pustaka untuk mendeteksi anomali pembaruan dependensi."""

  @staticmethod
  def ambil_snapshot_aktif(daftar_paket: List[str]) -> Dict[str, str]:
    """Merekam snapshot versi dari paket yang terpasang."""
    snapshot: Dict[str, str] = {}
    for pkg in daftar_paket:
      try:
        snapshot[pkg] = importlib.metadata.version(pkg)
      except importlib.metadata.PackageNotFoundError:
        snapshot[pkg] = "TIDAK_TERPASANG"
    return snapshot

  @staticmethod
  def bandingkan_snapshot(
      snapshot_lama: Dict[str, str], snapshot_baru: Dict[str, str]
  ) -> Dict[str, Any]:
    """Membandingkan dua snapshot untuk mendeteksi upgrade, downgrade, atau paket baru."""
    perubahan = []
    seluruh_kunci = set(snapshot_lama.keys()) | set(snapshot_baru.keys())

    for k in sorted(list(seluruh_kunci)):
      v_lama = snapshot_lama.get(k, "BELUM_ADA")
      v_baru = snapshot_baru.get(k, "DIHAPUS")
      if v_lama != v_baru:
        perubahan.append({"paket": k, "lama": v_lama, "baru": v_baru})

    return {"total_perubahan": len(perubahan), "detail_perubahan": perubahan}

  @staticmethod
  def simpan_manifest_terkunci(
      jalur_output: str, snapshot: Dict[str, str]
  ) -> None:
    """Mengekspor snapshot ke berkas teks requirements terkunci."""
    konten = [
        f"{pkg}=={ver}"
        for pkg, ver in snapshot.items()
        if ver != "TIDAK_TERPASANG"
    ]
    Path(jalur_output).write_text("\n".join(konten) + "\n", encoding="utf-8")
```

---

## 5. Rubrik Asesmen Berbasis Capaian (Outcome-Based Education / OBE)

| Kriteria Penilaian | Bobot | Skor 85 - 100 (Sangat Memuaskan) | Skor 70 - 84 (Memuaskan) | Skor 55 - 69 (Cukup) | Skor < 55 (Perlu Bimbingan) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Pemahaman Arsitektur Isolasi Runtime** | 25% | Mampu menganalisis disparitas `sys.prefix` vs `sys.base_prefix`, batasan `venv` vs Docker, serta peran variabel `PATH` secara mendalam. | Memahami fungsi isolasi virtual environment dan variabel `PATH`, namun komparasi biner OS masih bersifat umum. | Mengetahui perintah pembuatan venv tetapi tidak memahami mekanisme internal alokasi direktori *site-packages*. | Gagal memahami konsep dasar virtual environment dan masih mengandalkan instalasi global. |
| **Manajemen Dependensi & Reproduksibilitas** | 25% | Mahir menyusun `requirements.txt` dengan semantic versioning yang presisi, mengonfigurasi VS Code `.vscode/settings.json`, dan registrasi kernel Jupyter. | Mampu membuat manifes dependensi dan registrasi kernel, namun penulisan operator versi belum optimal. | Mampu menjalankan `pip freeze` tetapi manifes memuat paket redundan yang tidak diperlukan proyek. | Tidak mampu mengelola dependensi dan mengabaikan pembuatan berkas manifes. |
| **Audit Programatis & Penanganan Galat** | 25% | Menulis kode audit berbasis `importlib.metadata` yang elegan, modular, dan menangani eksepsi `PackageNotFoundError` secara tangguh. | Mampu melakukan audit paket dengan benar, namun masih menyisakan sedikit redundansi logika. | Menggunakan pendekatan impor modul langsung (`import pkg`) yang berisiko memperlambat komputasi. | Kode audit menghasilkan galat fatal dan gagal mendeteksi status pustaka pihak ketiga. |
| **Penyelesaian Tantangan Scaffolded** | 25% | Menyelesaikan seluruh 3 tantangan mandiri dengan arsitektur kode modular, tipe data teranotasi penuh, dan tervalidasi 100% 0 galat. | Menyelesaikan 3 tantangan dengan benar, namun ada kekurangan kecil pada dokumentasi atau penanganan kasus tepi. | Menyelesaikan 1–2 tantangan dasar; tantangan kelas `SnapshotEnvironmentManager` belum selesai sempurna. | Gagal menyelesaikan tantangan pemrograman praktikum yang ditugaskan. |
