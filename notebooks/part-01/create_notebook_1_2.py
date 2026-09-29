import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a href=\"https://colab.research.google.com/\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>\n",
    "\n",
    "# AI Modul 1.2: Praktikum Sejarah dan Perkembangan Artificial Intelligence\n",
    "### Eksperimen Historis: Rosenblatt Perceptron (1958) dan Pembuktian Batasan XOR (Minsky & Papert 1969)\n",
    "\n",
    "---\n",
    "\n",
    "> **Diktat Terkait:** [AI_Modul_1.2_Sejarah_dan_Perkembangan.md](../../docs/part-01/AI_Modul_1.2_Sejarah_dan_Perkembangan.md)  \n",
    "> **Outputs:** Kode program implementasi Perceptron dari nol dengan komentar per baris, visualisasi grafik batas keputusan (*decision boundary*) linier, dan simulasi pembuktian kegagalan XOR.  \n",
    "> **Outcomes:** Pemahaman praktis mengapa jaringan syaraf tiruan lapis tunggal gagal pada problem non-linier dan bagaimana penambahan fitur/lapisan tersembunyi menjadi penyelamat sejarah AI.  \n",
    "> **Impacts:** Penguasaan fondasi komputasi paling mendasar dari seluruh arsitektur jaringan saraf modern (*Deep Learning*).  \n",
    ">\n",
    "> **Tujuan Pembelajaran:**  \n",
    "> 1. Memprogram model komputasi *Rosenblatt Perceptron* dari nol (*from scratch*) tanpa pustaka machine learning pihak ketiga.  \n",
    "> 2. Mengamati konvergensi bobot pada fungsi linier (gerbang AND dan OR).  \n",
    "> 3. Memvisualisasikan kegagalan pemisahan linier pada gerbang XOR yang memicu masa kelam *The First AI Winter*."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Persiapan Environment & Import Library\n",
    "Jalankan sel di bawah ini untuk memuat pustaka matematika numerik dan visualisasi grafik:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Mengimpor modul sys untuk membaca metadata sistem Python\n",
    "import sys\n",
    "\n",
    "# Mengimpor modul numpy untuk operasi vektor aljabar linier dan pembuatan grid koordinat\n",
    "import numpy as np\n",
    "\n",
    "# Mengimpor modul matplotlib.pyplot untuk merender grafik sebaran data dan garis pemisah\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Mengimpor Tuple dan List dari typing untuk penegasan tipe data fungsi\n",
    "from typing import List, Tuple\n",
    "\n",
    "# Menampilkan versi interpreter Python\n",
    "print(f\"Python Version : {sys.version.split()[0]}\")\n",
    "\n",
    "# Menampilkan status kesiapan lingkungan komputasi\n",
    "print(\"Environment siap digunakan untuk simulasi historis Perceptron!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Pembahasan Penggunaan Kode 1:\n",
    "- Kita sengaja tidak menggunakan `scikit-learn` atau `PyTorch` pada modul ini agar mahasiswa memahami secara murni bagaimana aljabar perkalian titik $\\mathbf{w}^T \\mathbf{x} + b$ dihitung langsung dari tingkat instruksi dasar."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Implementasi Model Perceptron Klasik (Rosenblatt, 1958)\n",
    "Perhatikan setiap baris implementasi kelas `RosenblattPerceptron` berikut:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "class RosenblattPerceptron:\n",
    "    \"\"\"Model neuron tiruan lapis tunggal dengan aturan pembaharuan bobot Perceptron.\"\"\"\n",
    "    \n",
    "    def __init__(self, input_dim: int, learning_rate: float = 0.1, max_epochs: int = 25):\n",
    "        # Baris ini menyimpan jumlah variabel masukan (fitur)\n",
    "        self.input_dim: int = input_dim\n",
    "        # Baris ini menetapkan konstanta laju pembelajaran (eta)\n",
    "        self.learning_rate: float = learning_rate\n",
    "        # Baris ini menetapkan batas maksimum iterasi epoch\n",
    "        self.max_epochs: int = max_epochs\n",
    "        # Baris ini menginisialisasi vektor bobot awal dengan angka nol sebanyak input_dim\n",
    "        self.weights: np.ndarray = np.zeros(input_dim, dtype=np.float64)\n",
    "        # Baris ini menginisialisasi nilai skalar bias awal dengan angka nol\n",
    "        self.bias: float = 0.0\n",
    "        # Baris ini mencatat riwayat jumlah error per epoch untuk analisis konvergensi\n",
    "        self.error_history: List[int] = []\n",
    "\n",
    "    def predict(self, x: np.ndarray) -> int:\n",
    "        \"\"\"Menghitung nilai keluaran aktivasi undak biner: y = 1 jika (w . x + b) >= 0 else 0.\"\"\"\n",
    "        # Menghitung perkalian titik vektor bobot dengan vektor masukan ditambah bias skalar\n",
    "        net_input: float = np.dot(self.weights, x) + self.bias\n",
    "        # Mengembalikan 1 jika hasil kombinasi linier >= 0.0, selainnya mengembalikan 0\n",
    "        return 1 if net_input >= 0.0 else 0\n",
    "\n",
    "    def train(self, X: np.ndarray, y: np.ndarray) -> Tuple[bool, int]:\n",
    "        \"\"\"Melatih bobot model menggunakan Perceptron Learning Rule.\"\"\"\n",
    "        # Mengosongkan riwayat rekaman error dari proses pelatihan sebelumnya\n",
    "        self.error_history = []\n",
    "        \n",
    "        # Memulai iterasi pelatihan dari epoch 1 sampai batas maksimum max_epochs\n",
    "        for epoch in range(1, self.max_epochs + 1):\n",
    "            # Variabel pencatat total sampel yang salah diprediksi pada epoch ini\n",
    "            errors: int = 0\n",
    "            \n",
    "            # Melakukan perulangan untuk setiap baris sampel data dan label targetnya\n",
    "            for xi, target in zip(X, y):\n",
    "                # Menghitung estimasi prediksi model saat ini\n",
    "                prediction: int = self.predict(xi)\n",
    "                # Menghitung selisih galat (error = target aktual - prediksi model)\n",
    "                error: int = target - prediction\n",
    "                \n",
    "                # Jika terjadi kesalahan prediksi (error tidak sama dengan nol)\n",
    "                if error != 0:\n",
    "                    # Menambahkan penghitung kesalahan\n",
    "                    errors += 1\n",
    "                    # Menghitung faktor skala pergeseran: delta = learning_rate * error\n",
    "                    delta: float = self.learning_rate * error\n",
    "                    # Memperbarui vektor bobot: w_baru = w_lama + eta * error * x\n",
    "                    self.weights += delta * xi\n",
    "                    # Memperbarui nilai bias: b_baru = b_lama + eta * error\n",
    "                    self.bias += delta\n",
    "            \n",
    "            # Menyimpan jumlah kesalahan pada epoch ini ke dalam riwayat rekaman\n",
    "            self.error_history.append(errors)\n",
    "            \n",
    "            # Jika tidak ada satu pun sampel yang salah (pelatihan konvergen sempurna)\n",
    "            if errors == 0:\n",
    "                # Mengembalikan status sukses konvergen dan jumlah epoch yang dibutuhkan\n",
    "                return True, epoch\n",
    "                \n",
    "        # Mengembalikan status gagal jika batas epoch habis namun masih ada error\n",
    "        return False, self.max_epochs"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Pembahasan Penggunaan Kode 2:\n",
    "- `np.dot(self.weights, x) + self.bias`: Menggantikan perulangan manual menjadi komputasi aljabar linier vektor berkecepatan tinggi.\n",
    "- `self.weights += delta * xi`: Merealisasikan kaidah pembaruan bobot Rosenblatt. Jika $x_i = 0$, fitur tersebut tidak menyumbang pergeseran bobot; jika $x_i = 1$, bobot digeser sebanding dengan nilai `learning_rate`."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Eksperimen 1: Pelatihan Gerbang AND dan OR (Linearly Separable)\n",
    "Kita menguji kemampuan Perceptron memisahkan gerbang logika AND dan OR yang bersifat *linearly separable*."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Definisi Data Masukan (4 kemungkinan kombinasi biner)\n",
    "X_data = np.array([\n",
    "    [0.0, 0.0],\n",
    "    [0.0, 1.0],\n",
    "    [1.0, 0.0],\n",
    "    [1.0, 1.0]\n",
    "])\n",
    "\n",
    "# Target kebenaran Gerbang AND: hanya bernilai 1 jika kedua masukan adalah 1\n",
    "y_and = np.array([0, 0, 0, 1])\n",
    "\n",
    "# Target kebenaran Gerbang OR: bernilai 1 jika salah satu atau kedua masukan adalah 1\n",
    "y_or  = np.array([0, 1, 1, 1])\n",
    "\n",
    "# Inisialisasi dan latih model Perceptron untuk gerbang AND\n",
    "model_and = RosenblattPerceptron(input_dim=2, learning_rate=0.1, max_epochs=20)\n",
    "konvergen_and, epoch_and = model_and.train(X_data, y_and)\n",
    "\n",
    "# Inisialisasi dan latih model Perceptron untuk gerbang OR\n",
    "model_or = RosenblattPerceptron(input_dim=2, learning_rate=0.1, max_epochs=20)\n",
    "konvergen_or, epoch_or = model_or.train(X_data, y_or)\n",
    "\n",
    "print(f\"Gerbang AND: {'SUKSES KONVERGEN' if konvergen_and else 'GAGAL'} dalam {epoch_and} epoch\")\n",
    "print(f\"  Bobot Terpelajar: w1={model_and.weights[0]:.2f}, w2={model_and.weights[1]:.2f}, b={model_and.bias:.2f}\")\n",
    "\n",
    "print(f\"\\nGerbang OR : {'SUKSES KONVERGEN' if konvergen_or else 'GAGAL'} dalam {epoch_or} epoch\")\n",
    "print(f\"  Bobot Terpelajar: w1={model_or.weights[0]:.2f}, w2={model_or.weights[1]:.2f}, b={model_or.bias:.2f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Eksperimen 2: Kegagalan Gerbang XOR (Pemicu AI Winter I)\n",
    "Sekarang kita latih model Perceptron pada Gerbang XOR (*Exclusive-OR*) yang bernilai 1 hanya jika kedua input berbeda:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Target kebenaran Gerbang XOR: [0, 0]->0, [0, 1]->1, [1, 0]->1, [1, 1]->0\n",
    "y_xor = np.array([0, 1, 1, 0])\n",
    "\n",
    "# Inisialisasi dan latih model Perceptron untuk gerbang XOR\n",
    "model_xor = RosenblattPerceptron(input_dim=2, learning_rate=0.1, max_epochs=20)\n",
    "konvergen_xor, epoch_xor = model_xor.train(X_data, y_xor)\n",
    "\n",
    "print(f\"Gerbang XOR: {'SUKSES' if konvergen_xor else 'GAGAL KONVERGEN (AI Winter Trigger)'}\")\n",
    "print(f\"Jumlah Kesalahan per Epoch pada XOR: {model_xor.error_history}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Visualisasi Batas Keputusan Linier (*Decision Boundary*)\n",
    "Fungsi di bawah ini merender bidang ruang koordinat 2D untuk membandingkan secara gamblang mengapa garis pemisah lurus berhasil pada AND dan OR, namun mustahil pada XOR:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_decision_boundary(ax, model, X, y, title):\n",
    "    \"\"\"Merender sebaran titik sampel dan garis batas keputusan hiperbidang linier.\"\"\"\n",
    "    # Mengatur batas rentang sumbu koordinat x dan y\n",
    "    ax.set_xlim(-0.5, 1.5)\n",
    "    ax.set_ylim(-0.5, 1.5)\n",
    "    ax.axhline(0, color='#CCC', lw=1)\n",
    "    ax.axvline(0, color='#CCC', lw=1)\n",
    "    \n",
    "    # Memplot titik-titik sampel dengan label 0 (merah bulat)\n",
    "    ax.scatter(X[y == 0, 0], X[y == 0, 1], color='#C0392B', s=120, label='Kelas 0 (Output 0)', zorder=5)\n",
    "    # Memplot titik-titik sampel dengan label 1 (hijau segitiga)\n",
    "    ax.scatter(X[y == 1, 0], X[y == 1, 1], color='#27AE60', s=140, marker='^', label='Kelas 1 (Output 1)', zorder=5)\n",
    "    \n",
    "    # Menghitung persamaan garis pembatas linier: w1*x1 + w2*x2 + b = 0 => x2 = -(w1*x1 + b) / w2\n",
    "    w1, w2 = model.weights\n",
    "    b = model.bias\n",
    "    \n",
    "    # Menghindari pembagian dengan nol jika w2 bernilai 0\n",
    "    if abs(w2) > 1e-5:\n",
    "        x_vals = np.linspace(-0.5, 1.5, 100)\n",
    "        y_vals = -(w1 * x_vals + b) / w2\n",
    "        ax.plot(x_vals, y_vals, color='#2980B9', linestyle='--', linewidth=2.5, label='Batas Linier w^T x + b = 0')\n",
    "    \n",
    "    ax.set_title(title, fontsize=10, fontweight='bold')\n",
    "    ax.set_xlabel('Fitur $x_1$')\n",
    "    ax.set_ylabel('Fitur $x_2$')\n",
    "    ax.legend(fontsize=8, loc='upper left')\n",
    "    ax.grid(True, linestyle=':', alpha=0.6)\n",
    "\n",
    "# Membuat figur kanvas dengan 3 subplot berdampingan\n",
    "fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=150)\n",
    "\n",
    "# 1. Plot Gerbang AND\n",
    "plot_decision_boundary(axes[0], model_and, X_data, y_and, 'Gerbang AND (Berhasil Linier)')\n",
    "\n",
    "# 2. Plot Gerbang OR\n",
    "plot_decision_boundary(axes[1], model_or, X_data, y_or, 'Gerbang OR (Berhasil Linier)')\n",
    "\n",
    "# 3. Plot Gerbang XOR\n",
    "plot_decision_boundary(axes[2], model_xor, X_data, y_xor, 'Problem XOR (Gagal Dipisahkan Linier)')\n",
    "\n",
    "plt.suptitle('Replikasi Historis Limitasi Geometris Perceptron (Minsky & Papert 1969)', fontsize=12, fontweight='bold', y=1.03)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Pembahasan Penggunaan Kode 3:\n",
    "- Perhatikan panel ketiga (Gerbang XOR). Titik hijau berada di posisi diagonal $(0,1)$ dan $(1,0)$, sementara titik merah berada di diagonal sebaliknya $(0,0)$ dan $(1,1)$.\n",
    "- Secara geometris, tidak ada satu pun garis lurus datar di bidang dua dimensi yang mampu memisahkan titik hijau dari titik merah tanpa memotong salah satu kelas. Inilah bukti visual yang memicu pembekuan dana riset *First AI Winter* (1974–1980)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Tugas Mandiri Pemrograman (Coding Challenge)\n",
    "\n",
    "### Bagaimana Memecahkan Limitasi XOR Tanpa Multi-Layer Perceptron?\n",
    "Salah satu trik matematika klasik untuk mengatasi problem non-linier adalah **Rekayasa Fitur Polinomial (*Kernel Trick / Feature Engineering*)**.  \n",
    "Jika kita menambahkan fitur buatan ke-3: \n",
    "$$x_3 = x_1 \\cdot x_2$$\n",
    "maka ruang masukan bertransformasi dari 2D menjadi 3D: $[x_1, x_2, x_3]$.\n",
    "\n",
    "**Tugas Anda:**  \n",
    "1. Buat array masukan baru `X_transformed` dengan 3 kolom: $[x_1, x_2, x_1 \\cdot x_2]$.  \n",
    "2. Latih objek `RosenblattPerceptron(input_dim=3)` pada data yang telah ditransformasikan tersebut.  \n",
    "3. Buktikan apakah Perceptron kini mampu konvergen sempurna pada Gerbang XOR!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# ======================================================================\n",
    "# TUGAS MAHASISWA: Lengkapi blok kode rekayasa fitur di bawah ini:\n",
    "# ======================================================================\n",
    "\n",
    "# 1. Menghitung fitur interaksi non-linier x1 * x2\n",
    "x3_feature = (X_data[:, 0] * X_data[:, 1]).reshape(-1, 1)\n",
    "\n",
    "# 2. Menggabungkan fitur asli dengan fitur baru menjadi matriks 4x3\n",
    "X_transformed = np.hstack([X_data, x3_feature])\n",
    "\n",
    "# Menampilkan bentuk matriks fitur baru\n",
    "print(\"Matriks Fitur Tertransformasi (x1, x2, x1*x2):\")\n",
    "print(X_transformed)\n",
    "\n",
    "# 3. Inisialisasi Perceptron dengan dimensi masukan 3\n",
    "model_xor_solved = RosenblattPerceptron(input_dim=3, learning_rate=0.1, max_epochs=30)\n",
    "\n",
    "# 4. Latih model pada fitur tertransformasi dan target XOR\n",
    "solved_success, solved_epochs = model_xor_solved.train(X_transformed, y_xor)\n",
    "\n",
    "# 5. Cetak hasil pembuktian\n",
    "print(f\"\\nHasil Pelatihan XOR Tertransformasi: {'BERHASIL KONVERGEN!' if solved_success else 'GAGAL'}\")\n",
    "print(f\"Epoch Dibutuhkan : {solved_epochs}\")\n",
    "print(f\"Bobot Akhir      : w1={model_xor_solved.weights[0]:.2f}, w2={model_xor_solved.weights[1]:.2f}, w3={model_xor_solved.weights[2]:.2f}, b={model_xor_solved.bias:.2f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Rubrik Penilaian Praktikum Mandiri\n",
    "\n",
    "| Aspek Penilaian | Bobot | Kriteria Capaian |\n",
    "| :--- | :---: | :--- |\n",
    "| **Kerapihan Kode & Komentar** | 25% | Mahasiswa menyertakan penjelasan per baris pada setiap penambahan kode baru. |\n",
    "| **Ketepatan Rekayasa Fitur** | 45% | Fitur interaksi $x_1 \\cdot x_2$ berhasil dibentuk dan Perceptron terbukti konvergen 100% pada gerbang XOR. |\n",
    "| **Interpretasi Matematika** | 30% | Mahasiswa mampu menjelaskan pada sesi responsi mengapa penambahan dimensi ke-3 mengubah orientasi hiperbidang pemisah. |"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("e:/Project Buku/notebooks/part-01/AI_Modul_1.2_Praktikum_Sejarah_dan_Perkembangan.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print("Notebook 1.2 successfully generated!")
