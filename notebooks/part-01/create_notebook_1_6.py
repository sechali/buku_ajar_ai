import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a href=\"https://colab.research.google.com/\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>\n",
    "\n",
    "# AI Modul 1.6: Praktikum Workflow Pengembangan Proyek AI (MLOps Lifecycle)\n",
    "### Implementasi Pipeline Terpadu: Partisi Higienis Anti-Leakage, Regularisasi Ridge, Serialisasi Joblib, dan Deteksi Data Drift (PSI)\n",
    "\n",
    "---\n",
    "\n",
    "> **Diktat Terkait:** [AI_Modul_1.6_Workflow_Pengembangan_Proyek_AI.md](../../docs/part-01/AI_Modul_1.6_Workflow_Pengembangan_Proyek_AI.md)  \n",
    "> **Outputs:** Kode program pipeline MLOps lengkap dengan komentar per baris, evaluasi metrik regresi terpadu, dan fungsi deteksi degradasi data di produksi menggunakan Population Stability Index (PSI).  \n",
    "> **Outcomes:** Mahasiswa terampil menyusun pipeline machine learning yang kebal dari kebocoran data (*data leakage*), mampu melakukan serialisasi model untuk produksi, dan mendeteksi pergeseran distribusi data (*data drift*).  \n",
    "> **Impacts:** Mengurangi resiko kegagalan operasional (*technical debt*) sistem AI di lantai industri nyata dan menjamin keandalan prediksi jangka panjang.\n",
    ">\n",
    "> **Tujuan Pembelajaran:**  \n",
    "> 1. Mempraktikkan pemisahan partisi data latih-uji yang higienis untuk mencegah *Data Leakage*.  \n",
    "> 2. Mengenkapsulasi tahapan transformasi data dan model regresi Ridge ke dalam `sklearn.pipeline.Pipeline`.  \n",
    "> 3. Melakukan serialisasi artifak model ke dalam berkas biner `.joblib`.  \n",
    "> 4. Menghitung Population Stability Index (PSI) untuk mendeteksi *Data Drift* pada sensor cuaca perkebunan."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Persiapan Environment & Import Library\n",
    "Jalankan sel berikut untuk memuat pustaka komputasi numerik, pemodelan statistik, dan metrik MLOps:"
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
    "# Mengimpor modul os untuk manajemen direktori dan berkas artifak model\n",
    "import os\n",
    "\n",
    "# Mengimpor pustaka numpy untuk operasi vektor dan kalkulasi matriks numerik\n",
    "import numpy as np\n",
    "\n",
    "# Mengimpor pustaka matplotlib untuk membuat visualisasi grafik evaluasi\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Mengimpor pustaka joblib untuk serialisasi dan persistensi model machine learning\n",
    "import joblib\n",
    "\n",
    "# Mengimpor fungsi pemisahan data latih dan uji dari pustaka scikit-learn\n",
    "from sklearn.model_selection import train_test_split\n",
    "\n",
    "# Mengimpor StandardScaler untuk standardisasi fitur data numerik\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "\n",
    "# Mengimpor algoritma Ridge Regression untuk pemodelan linier teraturisasi\n",
    "from sklearn.linear_model import Ridge\n",
    "\n",
    "# Mengimpor kelas Pipeline untuk menyatukan tahapan preprocessing dan pemodelan secara atomik\n",
    "from sklearn.pipeline import Pipeline\n",
    "\n",
    "# Mengimpor metrik evaluasi regresi: mean squared error dan koefisien determinasi R2\n",
    "from sklearn.metrics import mean_squared_error, r2_score\n",
    "\n",
    "# Menetapkan nilai seed acak agar hasil simulasi numerik selalu konsisten saat diuji ulang\n",
    "np.random.seed(42)\n",
    "\n",
    "# Mengatur gaya grafik visualisasi\n",
    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
    "plt.rcParams['figure.dpi'] = 120\n",
    "\n",
    "# Menampilkan versi interpreter Python\n",
    "print(f\"Python Version : {sys.version.split()[0]}\")\n",
    "print(\"[OK] Seluruh pustaka MLOps berhasil dimuat dengan sukses!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Fase 1 & 2: Rekayasa Data & Partisi Higienis (Pencegahan Data Leakage)\n",
    "\n",
    "Kita membangkitkan 500 sampel observasi sensor perkebunan kelapa sawit yang terdiri dari:\n",
    "1. **Kelembaban Tanah** ($40\\% - 85\\%$)\n",
    "2. **Suhu Udara** ($28 \\pm 2.5^\\circ\\text{C}$)\n",
    "3. **Radiasi Sinar Matahari** ($200 - 900\\text{ W/m}^2$)\n",
    "\n",
    "Target $y$ adalah **Rendemen CPO (%)**. Kita segera memisahkan data menjadi $80\\%$ latih dan $20\\%$ uji **sebelum** melakukan transformasi skala apa pun."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Menentukan jumlah sampel observasi perkebunan\n",
    "n_samples = 500\n",
    "\n",
    "# Membangkitkan fitur kelembaban tanah perkebunan (%)\n",
    "kelembaban = np.random.uniform(40.0, 85.0, size=(n_samples, 1))\n",
    "\n",
    "# Membangkitkan fitur suhu udara perkebunan (°C)\n",
    "suhu = np.random.normal(loc=28.0, scale=2.5, size=(n_samples, 1))\n",
    "\n",
    "# Membangkitkan fitur intensitas radiasi matahari (W/m2)\n",
    "radiasi = np.random.uniform(200.0, 900.0, size=(n_samples, 1))\n",
    "\n",
    "# Menggabungkan seluruh variabel masukan menjadi matriks fitur X\n",
    "X = np.hstack([kelembaban, suhu, radiasi])\n",
    "\n",
    "# Membangkitkan target rendemen CPO buah sawit (%) berdasarkan relasi fisik + derau acak\n",
    "y = (0.15 * X[:, 0] - 0.20 * X[:, 1] + 0.01 * X[:, 2] + 12.0) + np.random.normal(0, 0.5, size=n_samples)\n",
    "\n",
    "# Memisahkan dataset menjadi data latih (80%) dan data uji (20%) secara dini\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)\n",
    "\n",
    "print(\"=\" * 65)\n",
    "print(\"PARTISI DATASET HIGIENIS (ANTI DATA-LEAKAGE)\")\n",
    "print(\"=\" * 65)\n",
    "print(f\"-> Jumlah Data Latih (Train Set): {X_train.shape[0]} observasi kebun\")\n",
    "print(f\"-> Jumlah Data Uji   (Test Set) : {X_test.shape[0]} observasi kebun\")\n",
    "print(f\"-> Dimensi Fitur Masukan        : {X_train.shape[1]} variabel sensor\")\n",
    "print(\"=\" * 65)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Fase 3 & 4: Membangun Pipeline Atomik & Melatih Model Teraturisasi (Ridge)\n",
    "\n",
    "Menggunakan `sklearn.pipeline.Pipeline`, kita menyatukan `StandardScaler` dan `Ridge(alpha=1.0)`.\n",
    "Hal ini menjamin statistik $\\mu$ dan $\\sigma$ hanya dipelajari dari `X_train`, sehingga informasi data uji terlindungi sepenuhnya."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Membangun Pipeline terpadu: Transformasi Skala diikuti Estimator Ridge Regression\n",
    "pipeline_model = Pipeline([\n",
    "    ('scaler', StandardScaler()),\n",
    "    ('regressor', Ridge(alpha=1.0, random_state=42))\n",
    "])\n",
    "\n",
    "# Melatih pipeline secara atomik hanya pada data latih\n",
    "pipeline_model.fit(X_train, y_train)\n",
    "\n",
    "# Melakukan inferensi pada data uji yang belum pernah dilihat sebelumnya\n",
    "y_pred = pipeline_model.predict(X_test)\n",
    "\n",
    "# Mengambil koefisien bobot model terlatih untuk inspeksi pengaruh fitur sensor\n",
    "bobot_fitur = pipeline_model.named_steps['regressor'].coef_\n",
    "nama_fitur = [\"Kelembaban Tanah\", \"Suhu Udara\", \"Radiasi Surya\"]\n",
    "\n",
    "print(\"=\" * 65)\n",
    "print(\"HASIL PELATIHAN PIPELINE MODEL RIDGE\")\n",
    "print(\"=\" * 65)\n",
    "for nama, w in zip(nama_fitur, bobot_fitur):\n",
    "    print(f\"-> Bobot Relatif {nama:<18} : {w:+.4f}\")\n",
    "print(\"=\" * 65)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Fase 5: Evaluasi Kinerja Holistik & Analisis Residual\n",
    "\n",
    "Kita menguji performa model menggunakan dua metrik utama:\n",
    "* **Root Mean Squared Error (RMSE)**: Rata-rata deviasi estimasi rendemen dalam satuan aslinya (%).\n",
    "* **Koefisien Determinasi ($R^2$)**: Proporsi variabilitas data target yang berhasil dijelaskan oleh model."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Menghitung Root Mean Squared Error (RMSE) pada data uji\n",
    "rmse = np.sqrt(mean_squared_error(y_test, y_pred))\n",
    "\n",
    "# Menghitung koefisien determinasi R2 pada data uji\n",
    "r2 = r2_score(y_test, y_pred)\n",
    "\n",
    "print(\"=\" * 65)\n",
    "print(\"METRIK EVALUASI KINERJA PADA DATA UJI (TEST SET)\")\n",
    "print(\"=\" * 65)\n",
    "print(f\"-> R2 Score Model  : {r2 * 100:.2f}%\")\n",
    "print(f\"-> RMSE Rendemen   : {rmse:.4f}% CPO\")\n",
    "print(\"=\" * 65)\n",
    "\n",
    "# Visualisasi Residual Plot (Perbandingan Nilai Aktual vs Nilai Prediksi)\n",
    "fig, ax = plt.subplots(figsize=(7.5, 5))\n",
    "ax.scatter(y_test, y_pred, color='#1f77b4', alpha=0.7, edgecolors='k', label='Sampel Uji')\n",
    "\n",
    "# Garis diagonal ideal (y = y_pred)\n",
    "min_val = min(y_test.min(), y_pred.min())\n",
    "max_val = max(y_test.max(), y_pred.max())\n",
    "ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Garis Prediksi Sempurna')\n",
    "\n",
    "ax.set_title(\"Evaluasi Prediksi Rendemen CPO: Aktual vs Prediksi AI\", fontsize=12, fontweight='bold')\n",
    "ax.set_xlabel(\"Rendemen Sebenarnya (%)\", fontsize=10, fontweight='bold')\n",
    "ax.set_ylabel(\"Rendemen Prediksi AI (%)\", fontsize=10, fontweight='bold')\n",
    "ax.legend(loc='upper left')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Fase 6A: MLOps Deployment (Serialisasi Model ke Berkas Biner)\n",
    "\n",
    "Model yang siap dikirim ke stasiun timbang pabrik atau drone kebun diekspor menggunakan pustaka `joblib`.\n",
    "Berkas ini membekukan parameter model dan transformer skala secara utuh."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Menentukan nama berkas penyimpanan model\n",
    "model_filename = \"model_rendemen_sawit_v1.joblib\"\n",
    "\n",
    "# Menyimpan objek pipeline utuh ke media penyimpanan lokal\n",
    "joblib.dump(pipeline_model, model_filename)\n",
    "\n",
    "# Memverifikasi ukuran berkas biner yang dihasilkan\n",
    "file_size_kb = os.path.getsize(model_filename) / 1024.0\n",
    "print(\"=\" * 65)\n",
    "print(\"SERIALISASI MODEL ARTIFAK (MLOps PACKAGING)\")\n",
    "print(\"=\" * 65)\n",
    "print(f\"-> Berkas Tersimpan  : {model_filename}\")\n",
    "print(f\"-> Ukuran Artifak    : {file_size_kb:.2f} KB (Sangat ringan untuk Edge AI)\")\n",
    "\n",
    "# Menguji muat ulang (re-loading) model di server produksi hipotesis\n",
    "loaded_model = joblib.load(model_filename)\n",
    "test_input = np.array([[65.0, 27.5, 550.0]]) # 65% kelembaban, 27.5°C, 550 W/m2\n",
    "prediksi_ujicoba = loaded_model.predict(test_input)[0]\n",
    "print(f\"-> Uji Inferensi Baru: Estimasi Rendemen CPO = {prediksi_ujicoba:.2f}%\")\n",
    "print(\"=\" * 65)\n",
    "\n",
    "# Membersihkan berkas sementara\n",
    "if os.path.exists(model_filename):\n",
    "    os.remove(model_filename)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Fase 6B: Continuous Monitoring (Deteksi Data Drift Menggunakan Metrik PSI)\n",
    "\n",
    "Formula matematis **Population Stability Index (PSI)**:\n",
    "\n",
    "$$\\text{PSI} = \\sum_{i=1}^{k} \\left( P_i - Q_i \\right) \\times \\ln\\left( \\frac{P_i}{Q_i} \\right)$$\n",
    "\n",
    "Mari kita buktikan ketajaman fungsi PSI saat kondisi stabil vs saat terjadi gelombang panas El Niño:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Mendefinisikan fungsi perhitungan Population Stability Index (PSI)\n",
    "def hitung_psi(distribusi_baseline, distribusi_aktual, num_bins=10):\n",
    "    batas_bin = np.percentile(distribusi_baseline, np.linspace(0, 100, num_bins + 1))\n",
    "    batas_bin[0] -= 1e-5\n",
    "    batas_bin[-1] += 1e-5\n",
    "    \n",
    "    hitung_baseline, _ = np.histogram(distribusi_baseline, bins=batas_bin)\n",
    "    hitung_aktual, _ = np.histogram(distribusi_aktual, bins=batas_bin)\n",
    "    \n",
    "    Q = hitung_baseline / len(distribusi_baseline)\n",
    "    P = hitung_aktual / len(distribusi_aktual)\n",
    "    \n",
    "    eps = 1e-4\n",
    "    Q = np.where(Q == 0, eps, Q)\n",
    "    P = np.where(P == 0, eps, P)\n",
    "    \n",
    "    nilai_psi = np.sum((P - Q) * np.log(P / Q))\n",
    "    return nilai_psi\n",
    "\n",
    "# Ambil fitur suhu latih sebagai baseline referensi\n",
    "suhu_baseline = X_train[:, 1]\n",
    "\n",
    "# Skenario 1: Suhu produksi pada musim normal\n",
    "suhu_normal_prod = np.random.normal(loc=28.1, scale=2.4, size=200)\n",
    "psi_normal = hitung_psi(suhu_baseline, suhu_normal_prod)\n",
    "\n",
    "# Skenario 2: Suhu produksi saat gelombang panas El Nino ekstrem\n",
    "suhu_elnino_prod = np.random.normal(loc=34.5, scale=3.2, size=200)\n",
    "psi_drift = hitung_psi(suhu_baseline, suhu_elnino_prod)\n",
    "\n",
    "print(\"=\" * 65)\n",
    "print(\"HASIL MONITORING OPERASIONAL DATA DRIFT (PSI)\")\n",
    "print(\"=\" * 65)\n",
    "print(f\"-> Skenario Normal Cuaca : PSI = {psi_normal:.4f}\")\n",
    "if psi_normal < 0.1:\n",
    "    print(\"   Status: [STABIL] Distribusi data aman, model beroperasi normal.\")\n",
    "else:\n",
    "    print(\"   Status: [PERINGATAN] Terjadi pergeseran data.\")\n",
    "\n",
    "print(f\"-> Skenario Musim El Nino: PSI = {psi_drift:.4f}\")\n",
    "if psi_drift > 0.25:\n",
    "    print(\"   Status: [SIGNIFICANT DRIFT!] Pemicu otomatis retraining model aktif!\")\n",
    "else:\n",
    "    print(\"   Status: [MODERAT] Pergeseran ringan terdeteksi.\")\n",
    "print(\"=\" * 65)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Tugas Mandiri & Eksplorasi Mahasiswa\n",
    "\n",
    "1. **Eksplorasi Alpha Ridge**: Ubah parameter `alpha` pada `Ridge` menjadi `alpha=100.0`. Amati perubahan koefisien bobot sensor! Mengapa penalti regularisasi yang terlalu besar menyebabkan *underfitting*?\n",
    "2. **Simulasi Drift Multivariat**: Modifikasilah skrip monitoring di atas untuk menghitung nilai PSI pada variabel **Kelembaban Tanah** ketika musim kemarau ekstrem (misal rata-rata kelembaban turun dari $62\\%$ menjadi $35\\%$). Berapa skor PSI yang Anda dapatkan?"
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

output_path = r"e:\Project Buku\notebooks\part-01\AI_Modul_1.6_Praktikum_Workflow_Proyek_AI.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"Notebook successfully written to {output_path}")
