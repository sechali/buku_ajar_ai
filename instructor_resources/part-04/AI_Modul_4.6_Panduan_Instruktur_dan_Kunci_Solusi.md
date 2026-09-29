# AI Modul 4.6: Panduan Instruktur dan Kunci Solusi
## Visualisasi Data (Matplotlib & Seaborn): Desain Ilmiah, Paradigma Berorientasi Objek, dan Aksesibilitas

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

| Komponen | Rincian Instruksional |
| :--- | :--- |
| **Mata Kuliah** | Sains Data & Kecerdasan Buatan Terapan |
| **Kode Modul** | AI Modul 4.6 |
| **Topik Pembelajaran** | Matplotlib OO API, Seaborn Axes vs Figure-Level, Teori Tufte (*Data-Ink Ratio*), Aksesibilitas Warna, dan Visualisasi Spasial |
| **Alokasi Waktu** | 3 SKS (150 Menit Tatap Muka/Laboratorium + 180 Menit Belajar Mandiri) |
| **Prasyarat** | AI Modul 4.5 (Exploratory Data Analysis) |
| **Target OBE** | Sub-CPMK 4.6: Mahasiswa mampu membangun kanvas visualisasi multi-panel beresolusi tinggi (300 DPI) menggunakan Matplotlib OO API, mengintegrasikan fungsi analitik statistik Seaborn, serta menerapkan palet warna ramah buta warna (*colorblind-safe*). |

### Matriks Distribusi Jam Pembelajaran (150 Menit)
1. **Sesi Pembuka & Refleksi Desain Visual (30 Menit):**
   - Mengapa grafik ilmiah penting: Komunikasi visual hasil pemodelan AI tanpa disinformasi.
   - Perbandingan filosofi: *Pyplot State-Machine* (implisit/global) vs *Object-Oriented API* (`fig, ax` eksplisit).
2. **Sesi Telaah Konseptual & Teori Estetika Data (30 Menit):**
   - Teori Rasio Tinta-Data Edward Tufte: Mengeliminasi *chartjunk* dan membuang *spines* yang tidak informatif.
   - Fisiologi penglihatan manusia dan bahaya palet *Rainbow/Jet*; keunggulan matematis palet perseptual seragam (*viridis*, *cividis*).
3. **Praktikum Laboratorium Terbimbing (60 Menit):**
   - Eksplorasi berkas `notebooks/part-04/AI_Modul_4.6_Praktikum_Visualisasi_Data_Matplotlib_Seaborn.ipynb`.
   - Membangun kanvas komposit 3 panel (`fig, (ax1, ax2, ax3)`): Regplot dengan 95% CI, Boxplot dengan batas kritis FFA, dan Heatmap korelasi.
   - Pembedaan fungsi tingkat sumbu (*Axes-level*) vs tingkat figur (*Figure-level* `FacetGrid`).
   - Visualisasi spasial grid kebun $15 \times 15$ blok dengan penandaan poligon klaster anomali klorofil.
4. **Sesi Evaluasi & Diskusi HOTS (30 Menit):**
   - Kritik desain grafik (*figure critique*): Bedah laporan manajerial dengan grafik 3D dan latar kisi-kisi gelap.
   - Presentasi kode multi-panel dan justifikasi pemilihan colormap untuk citra drone kanopi sawit.

---

## 2. Strategi Pedagogis dan Panduan Fasilitasi Kelas

### 2.1 Sesi "Figure Makeover" (Kritik Desain Visual)
Tampilkan grafik laporan bisnis perkebunan yang "buruk" (grafik batang 3D dengan latar belakang hitam, grid pekat, dan palet pelangi).
- Minta mahasiswa berperan sebagai *Art Director / Chief Data Scientist*.
- Identifikasi setiap elemen yang melanggar prinsip Edward Tufte.
- Pandu mahasiswa merekonstruksi grafik tersebut langkah demi langkah menjadi representasi minimalis yang elegan dan profesional.

### 2.2 Panduan Live-Coding: Isolasi Objek `Axes`
Instruktur wajib mendemonstrasikan mengapa sintaks `fig, ax = plt.subplots()` adalah fondasi wajib:
- Tunjukkan bahwa dengan memegang referensi `ax`, instruktur dapat mengoperasikan banyak subplot secara independen tanpa khawatir perintah seperti `plt.xlabel()` salah menimpa sumbu di subplot lain.
- Tunjukkan cara menghubungkan fungsi Seaborn secara elegan: `sns.scatterplot(..., ax=ax1)`.

---

## 3. Identifikasi dan Remediasi Miskonsepsi Mahasiswa

### Miskonsepsi 1: "Mengira `plt.plot()` dan `ax.plot()` itu sama persis."
- **Koreksi Konseptual:** `plt.plot()` menggunakan *state-machine* global (mengubah sumbu aktif terakhir), yang sangat rawan memicu kekacauan tata letak pada proyek multi-grafik. Sebaliknya, `ax.plot()` memodifikasi objek bidang koordinat tertentu secara deterministik dan terisolasi. Dalam rekayasa perangkat lunak modern, selalu gunakan pendekatan berorientasi objek (`ax`).

### Miskonsepsi 2: "Mencoba menyuplai argumen `ax=ax` ke fungsi Figure-Level Seaborn (`sns.relplot`, `sns.displot`)."
- **Koreksi Konseptual:** Fungsi *figure-level* bertugas mengontrol seluruh kanvas figur secara mandiri dan mengembalikan objek `FacetGrid`. Memberikan argumen `ax` akan memicu `TypeError` atau menghasilkan kanvas kosong yang tidak diinginkan. Jika ingin menggambar ke dalam subplot yang telah ada, selalu gunakan fungsi *axes-level* pasangannya (`sns.scatterplot`, `sns.histplot`, `sns.boxplot`).

### Miskonsepsi 3: "Grafik batang 3D dan ornamen warna-warni membuat laporan AI terlihat lebih canggih."
- **Koreksi Konseptual:** Efek 3D semu (*pseudo-3D*) adalah *chartjunk* terburuk karena distorsi perspektif optik membuat pembaca kesulitan menentukan titik puncak batang pada skala nilai yang sebenarnya. Kemiringan sudut 3D dapat membuat batang bernilai kecil terlihat lebih tinggi dari batang bernilai besar.

### Miskonsepsi 4: "Palet spektrum pelangi (*Rainbow/Jet*) adalah pilihan terbaik karena warnanya paling kaya."
- **Koreksi Konseptual:** Palet *Rainbow/Jet* memiliki non-linearitas luminansi yang parah. Warna kuning memiliki kecerahan intrinsik yang jauh lebih tinggi daripada warna hijau atau merah, menciptakan ilusi visual *"batas palsu"* (*false boundaries*) pada area yang sebenarnya memiliki gradien nilai halus. Selain itu, palet ini sepenuhnya tidak terbaca oleh penyandang buta warna *deuteranopia* (merah-hijau).

---

## 4. Kunci Solusi dan Pembahasan Soal Latihan & HOTS

### 4.1 Pembahasan Evaluasi Desain Grafik dan Rasio Tinta-Data (Bobot: 30%)

**1. Empat Elemen Chartjunk pada Deskripsi Kasus:**
1. *Efek 3D Semu (Silinder Berkilau):* Menambah volume visual buatan tanpa menambah dimensi data riil.
2. *Latar Belakang Dinding Kisi-Kisi Hitam Pekat:* Mengonsumsi tinta dalam jumlah besar dan mengurangi kontras keterbacaan data (*violates Data-Ink ratio*).
3. *Pewarnaan Acak Nir-Makna (Rainbow Colors):* Menimbulkan kebingungan kognitif (*cognitive load*) karena pembaca mencari arti kategorikal yang sebenarnya tidak ada.
4. *Kotak Legenda Redundan di Sudut:* Menamai "Bulan 1 hingga Bulan 12" pada legenda padahal nama-nama bulan seharusnya ditempatkan langsung di bawah sumbu horizontal $X$.

**2. Alasan Distorsi Optik Grafik Batang 3D:**
Pada batang 3D, terdapat permukaan depan (*front face*), permukaan atas elips (*top ellipse*), dan efek perspektif menyudut (*isometric projection*). Mata pembaca kesulitan memutuskan apakah ketinggian nilai diukur dari garis dasar depan atau dari pusat elips atas. Penelitian persepsi visual (Cleveland & McGill, 1984) membuktikan bahwa estimasi pembacaan angka pada batang 3D memiliki tingkat galat hingga $300\%$ lebih tinggi dibanding grafik batang 2D datar.

**3. Konsep Desain Ulang (*Redesign Concept*) Berdasarkan Prinsip Tufte:**
- Ganti menjadi **Grafik Batang Datar 2D Horizontal atau Garis Tipis (Lollipop Chart)**.
- Hilangkan latar belakang hitam; gunakan latar belakang putih bersih (`facecolor='white'`).
- Buang *spines* atas dan kanan; buat *spines* bawah dan kiri berwarna abu-abu tipis.
- Terapkan warna tunggal netral yang elegan (misalnya biru tua `#1E40AF`) dengan penyorotan warna aksen hanya pada bulan panen puncak (*peak season*).
- Hapus kotak legenda; tempatkan label nama bulan langsung pada sumbu koordinat.

---

### 4.2 Pembahasan Rancang Bangun Tata Letak Multi-Panel Komposit (Bobot: 40%)

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def buat_dashboard_ilmiah(df):
    """
    Membangun kanvas multi-panel komposit 3 subplot beresolusi tinggi (300 DPI)
    menggunakan pendekatan Matplotlib Object-Oriented API dan Seaborn Axes-Level.
    """
    # 1. Inisialisasi kanvas figur berorientasi objek 1 baris x 3 kolom
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(14, 5), dpi=300)
    fig.suptitle('Dashboard Diagnostik Kinerja dan Mutu Perkebunan Kelapa Sawit', 
                 fontsize=12, fontweight='bold', y=0.98, color='#0F172A')

    # --- SUBPLOT 1: Scatter Plot Regresi dengan 95% CI (ax1) ---
    sns.regplot(
        data=df,
        x='Curah_Hujan_mm',
        y='Tonase_TBS_Ton_Ha',
        ax=ax1,
        color='#1D4ED8',
        scatter_kws={'alpha': 0.5, 's': 25, 'edgecolors': 'none'},
        line_kws={'color': '#DC2626', 'linewidth': 1.8, 'label': 'Garis Tren (95% CI)'}
    )
    ax1.set_title('Respon Curah Hujan terhadap Yield TBS', fontsize=9.5, fontweight='bold', pad=8)
    ax1.set_xlabel('Curah Hujan Bulanan (mm)', fontsize=8.5)
    ax1.set_ylabel('Produksi TBS (Ton/Ha)', fontsize=8.5)
    ax1.legend(loc='upper left', frameon=True, fontsize=7.5)
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # --- SUBPLOT 2: Boxplot Komparatif Mutu FFA (ax2) ---
    sns.boxplot(
        data=df,
        x='Afdeling',
        y='Kadar_FFA_pct',
        hue='Afdeling',
        legend=False,
        ax=ax2,
        palette='colorblind',
        boxprops=dict(alpha=0.85)
    )
    ax2.axhline(3.5, color='#DC2626', linestyle='--', linewidth=1.2, label='Batas Kritis FFA (3.5%)')
    ax2.set_title('Distribusi Mutu Asam Lemak Bebas (FFA)', fontsize=9.5, fontweight='bold', pad=8)
    ax2.set_xlabel('Divisi Afdeling', fontsize=8.5)
    ax2.set_ylabel('Kadar Asam Lemak Bebas (%)', fontsize=8.5)
    ax2.legend(loc='upper left', frameon=True, fontsize=7.5)
    ax2.grid(True, linestyle=':', alpha=0.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # --- SUBPLOT 3: Matriks Heatmap Multivariat (ax3) ---
    fitur_num = ['Curah_Hujan_mm', 'Suhu_C', 'Dosis_NPK_kg', 'Indeks_NDVI', 'Kadar_FFA_pct', 'Tonase_TBS_Ton_Ha']
    mat_corr = df[fitur_num].corr(method='spearman')

    sns.heatmap(
        mat_corr,
        ax=ax3,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        vmin=-1.0,
        vmax=1.0,
        cbar_kws={'label': 'Korelasi Spearman (r)'},
        linewidths=0.5,
        annot_kws={'size': 7.0}
    )
    ax3.set_title('Matriks Korelasi Multivariat Kebun', fontsize=9.5, fontweight='bold', pad=8)
    ax3.set_xticklabels(['Hujan', 'Suhu', 'NPK', 'NDVI', 'FFA', 'Yield'], rotation=45, ha='right', fontsize=7.5)
    ax3.set_yticklabels(['Hujan', 'Suhu', 'NPK', 'NDVI', 'FFA', 'Yield'], rotation=0, fontsize=7.5)

    # Penataan tata letak otomatis dan penyimpanan berkas
    plt.tight_layout()
    plt.savefig('dashboard_agribisnis_publikasi.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Dashboard ilmiah berhasil dibuat dan disimpan ke dashboard_agribisnis_publikasi.png")
```

---

### 4.3 Pembahasan Aksesibilitas Skala Warna dan Distorsi Persepsi (Bobot: 30%)

**1. Alasan Fisiologis Pelarangan Palet Rainbow/Jet:**
Palet warna *Rainbow/Jet* bertransisi melalui spektrum: Biru $\to$ Sian $\to$ Hijau $\to$ Kuning $\to$ Merah. Sistem visual mata manusia tidak memproses panjang gelombang warna secara linier. Reseptor sel kerucut (*cone cells*) pada retina manusia memiliki sensitivitas puncak terhadap spektrum kuning-hijau. Akibatnya, pada pita warna kuning dan sian, terjadi lonjakan kecerahan (*luminance spike*) yang drastis, sementara pada warna biru dan merah gelap tingkat kecerahannya sangat rendah.

**2. Fenomena Batas Palsu (*False Boundaries*):**
Karena adanya lonjakan luminansi pada zona warna kuning dan sian, mata manusia mempersepsikan adanya "garis batas tajam" atau patahan nilai di antara area hijau dan kuning, padahal data asli di lapangan mengalami kenaikan nilai NDVI yang sangat bertahap dan halus (*continuous smooth gradient*). Sebaliknya, pada rentang warna hijau lebar, mata manusia mengalami kesulitan membedakan variasi nilai yang sebenarnya cukup besar. Fenomena ini menyesatkan manajer kebun, membuat mereka mengira ada patahan batas petak lahan yang kritis padahal itu hanya ilusi optik palet warna.

**3. Rekomendasi Palet Alternatif:**
- **Rekomendasi Utama: Palet `viridis` atau `cividis`.**
- **Keunggulan Matematis (*Perceptually Uniform*):**
  - Palet `viridis` dirancang dengan fungsi luminansi yang meningkat secara monotonik linier murni dari ungu gelap ($0$) hingga kuning terang ($1$).
  - Perbedaan nilai data sebesar $\Delta x = 0.1$ akan menghasilkan perbedaan kontras optik yang persis sama di mata manusia di sepanjang seluruh rentang skala warna.
  - Kebal $100\%$ terhadap segala bentuk defisiensi warna (aman bagi penyandang *deuteranopia* dan *protanopia*).
  - Tetap terbaca secara sempurna dan tidak kehilangan informasi saat dicetak pada mesin fotokopi atau kertas monokrom hitam-putih.

---

## 5. Rubrik Penilaian Berbasis Capaian (OBE Assessment Rubric)

| Dimensi Penilaian | Sangat Kurang (< 50) | Cukup (50 - 69) | Baik (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :--- | :--- | :--- | :--- |
| **Penguasaan Arsitektur OO API Matplotlib (Kognitif)** | Masih menggunakan fungsi state-machine global `plt.plot()` serampangan; tidak memahami objek `Figure` dan `Axes`. | Menggunakan `plt.subplots()` namun masih mencampurkan pemanggilan `plt.title()` yang salah sasaran. | Mampu mengonfigurasi multi-plot OO API dengan benar dan mengatur properti sumbu secara mandiri. | Menguasai anatomi mendalam: manipulasi *spines*, *tick formatters*, kustomisasi artist tingkat lanjut, dan layout komposit terisolasi sempurna. |
| **Sinergi dan Integrasi Seaborn (Psikomotorik)** | Mencampurkan fungsi figure-level dan axes-level hingga menghasilkan galat (*error*) atau kanvas kosong. | Menggunakan fungsi Seaborn standar namun tidak membuang elemen chartjunk atau legenda redundan. | Mengintegrasikan fungsi Seaborn axes-level ke dalam kanvas Matplotlib dengan rapi dan fungsional. | Membangun dashboard analitik publikasi multi-panel beresolusi 300 DPI, menyertakan interval kepercayaan 95%, dan grid spasial presisi. |
| **Etika Desain & Aksesibilitas Visual (Afektif & Terapan)** | Menggunakan grafik 3D semu dan palet warna pelangi (*Rainbow/Jet*); mengabaikan buta warna. | Mengetahui konsep chartjunk namun masih menyisakan garis batas dan warna yang tidak bermakna informatif. | Menerapkan prinsip Tufte secara konsisten dan menggunakan palet ramah buta warna (*colorblind palette*). | Memberikan analisis kritis mendalam mengenai non-linearitas luminansi, merancang representasi data perseptual seragam, dan menjunjung tinggi integritas sains visual. |
