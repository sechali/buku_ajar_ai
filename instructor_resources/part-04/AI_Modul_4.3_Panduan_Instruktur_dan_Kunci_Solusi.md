# AI Modul 4.3: Panduan Instruktur dan Kunci Solusi
## Pandas untuk Manipulasi Data: Arsitektur Tabular, Agregasi Relasional, dan Analitik Deret Waktu Agribisnis

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

| Komponen | Rincian Instruksional |
| :--- | :--- |
| **Mata Kuliah** | Sains Data & Kecerdasan Buatan Terapan |
| **Kode Modul** | AI Modul 4.3 |
| **Topik Pembelajaran** | Manipulasi Data Tabular Pandas, Seleksi Presisi, Split-Apply-Combine, Deret Waktu, dan Optimasi Memori |
| **Alokasi Waktu** | 3 SKS (150 Menit Tatap Muka/Laboratorium + 180 Menit Belajar Mandiri) |
| **Prasyarat** | AI Modul 4.2 (NumPy untuk Komputasi Numerik) |
| **Target OBE** | Sub-CPMK 4.3: Mahasiswa mampu merekayasa dataset tabular agribisnis skala enterprise, mengeliminasi galat mutasi data berantai, serta melakukan analisis agregatif dan runtun waktu cuaca secara optimal. |

### Matriks Distribusi Jam Pembelajaran (150 Menit)
1. **Sesi Pembuka & Refleksi Arsitektural (30 Menit):**
   - Bedah arsitektur internal `DataFrame`: Relasi `Series`, `Index`, dan mekanisme `BlockManager` (*FloatBlock* vs *ObjectBlock*).
   - Mengapa penugasan berantai (*chained assignment*) memicu `SettingWithCopyWarning`.
2. **Sesi Telaah Konseptual & Pola Desain Data (30 Menit):**
   - Paradigma *Split-Apply-Combine* (Hadley Wickham) untuk agregasi hierarkis kebun (*blok $\to$ afdeling $\to$ estate*).
   - Matematika jendela geser (*rolling windows*) dan perata-rataan tren defisit air kebun.
3. **Praktikum Laboratorium Terbimbing (60 Menit):**
   - Eksplorasi berkas `notebooks/part-04/AI_Modul_4.3_Praktikum_Pandas_Manipulasi_Data.ipynb`.
   - Latihan pengindeksan `.loc` vs `.iloc` dan pembuktian mutasi aman.
   - Normalisasi Z-Score tingkat grup menggunakan `groupby().transform()`.
   - Penggabungan (*merge*) tabel panen dengan uji tanah dan restrukturisasi *pivot table*.
   - Resampling deret waktu cuaca jam-ke-harian dan reduksi memori $94\%$ via tipe `category`.
4. **Sesi Evaluasi & Diskusi HOTS (30 Menit):**
   - Pembahasan kasus mutasi data dan mitigasi kebocoran memori pada data penimbangan PKS.
   - Presentasi solusi rekapitulasi rotasi panen dan analisis format *wide* vs *long*.

---

## 2. Strategi Pedagogis dan Panduan Fasilitasi Kelas

### 2.1 Demonstrasi Interaktif "The Silent Bug of Chained Indexing"
Tunjukkan secara langsung di depan kelas bagaimana penugasan berantai dapat membunuh integritas data secara diam-diam:
```python
# Tunjukkan kode ini di terminal:
sub = df[df['Tonase'] < 20]
sub['Catatan'] = 'Kurang'
# Tanyakan ke mahasiswa: "Apakah kolom Catatan muncul di df asli?"
# Tunjukkan bahwa df asli TIDAK BERUBAH sama sekali!
```
Jelaskan bahwa peringatan `SettingWithCopyWarning` bukanlah gangguan teks biasa, melainkan penyelamat dari kesalahan kalkulasi model bisnis bernilai miliaran rupiah.

### 2.2 Aturan Anti-Looping: "Say No to `iterrows()`"
Tegaskan bahwa perulangan `for index, row in df.iterrows():` merupakan anti-pola (*anti-pattern*) terburuk di Pandas karena mengubah setiap baris menjadi objek Series baru di setiap iterasi, memperlambat pemrosesan hingga $1.000\times$ lebih lambat dibandingkan operasi vektorisasi atau `.apply()`.

---

## 3. Identifikasi dan Remediasi Miskonsepsi Mahasiswa

### Miskonsepsi 1: "`.loc` dan `.iloc` itu sama saja, hanya beda selera gaya penulisan."
- **Koreksi Konseptual:** Keduanya memiliki paradigma yang bertolak belakang. `.loc` bekerja berbasis label dan **menyertakan batas akhir (*inclusive*)**, sedangkan `.iloc` bekerja berbasis posisi integer nol dan **mengecualikan batas akhir (*exclusive*)**. Pada indeks numerik non-urut (misal indeks hasil filter: `[10, 5, 2]`), `df.loc[0:2]` dan `df.iloc[0:2]` menghasilkan data yang sama sekali berbeda dan dapat memicu galat fatal jika tertukar.

### Miskonsepsi 2: "`SettingWithCopyWarning` boleh diabaikan jika program masih berjalan lancar."
- **Koreksi Konseptual:** Mengabaikan peringatan ini adalah kesalahan fatal. Ketika peringatan muncul, pengguna tidak memiliki kepastian apakah DataFrame induk berhasil dimodifikasi ataukah modifikasi hanya terjadi pada salinan memori sementara yang langsung musnah setelah eksekusi. Solusi mutlak: gunakan sintaks tunggal `df.loc[kondisi, 'kolom'] = nilai`.

### Miskonsepsi 3: "`pd.merge()` dan `pd.concat()` memiliki fungsi yang identik."
- **Koreksi Konseptual:** `concat()` adalah operasi penumpukan fisik (menempelkan baris di bawah baris lain atau kolom di samping kolom lain berdasarkan keselarasan indeks fisik tanpa peduli isi data). Sedangkan `merge()` adalah operasi aljabar relasional berbasis nilai kecocokan kunci bersama (*join keys*), setara dengan operasi `JOIN` pada SQL database.

### Miskonsepsi 4: "Semua kolom teks harus dibiarkan bertipe `object`."
- **Koreksi Konseptual:** Kolom teks dengan nilai berulang (seperti nama afdeling, kelas mutu buah, jenis pupuk) yang dibiarkan bertipe `object` menyimpan ribuan pointer string yang memboroskan RAM. Mengonversinya ke `category` mengompresi data hingga $90\%+$ dan mempercepat operasi `groupby()` hingga $3\times$.

---

## 4. Kunci Solusi dan Pembahasan Soal Latihan & HOTS

### 4.1 Pembahasan Integritas Pengindeksan & Mekanika Memori (Bobot: 30%)
Diberikan cuplikan kode:
```python
sub_data = df[df['Curah_Hujan_mm'] > 200.0]
sub_data['Status_Kekeringan'] = 'Aman'
```

**1. Analisis Teknis Munculnya Peringatan:**
- Pada baris 1, ekspresi `df[df['Curah_Hujan_mm'] > 200.0]` menghasilkan objek DataFrame perantara (*intermediate object*). Pandas tidak mendefinisikan secara pasti apakah objek ini merupakan *view* yang merujuk pada blok memori `df` asli ataukah alokasi memori salinan (*copy*).
- Pada baris 2, operasi penugasan `sub_data['Status_Kekeringan'] = ...` mencoba memodifikasi objek perantara tersebut. Karena Pandas mendeteksi bahwa `sub_data` adalah turunan dari DataFrame lain tanpa pemutusan ikatan eksplisit, sistem melempar `SettingWithCopyWarning` untuk memperingatkan pengguna bahwa perubahan ini **kemungkinan besar TIDAK termutasi pada `df` asli**. Nilai pada `df` asli tidak berubah sama sekali!

**2. Dua Alternatif Perbaikan Kode:**
- **Pendekatan A (Modifikasi langsung pada DataFrame induk):**
  ```python
  df.loc[df['Curah_Hujan_mm'] > 200.0, 'Status_Kekeringan'] = 'Aman'
  ```
- **Pendekatan B (Pemisahan fisik sebagai DataFrame salinan independen):**
  ```python
  sub_data = df[df['Curah_Hujan_mm'] > 200.0].copy()
  sub_data['Status_Kekeringan'] = 'Aman'
  ```

**3. Perhitungan Penghematan Memori Tipe Data Category:**
- Misalkan kolom memuat $1.000.000$ baris dengan 2 nilai string unik: `"SELESAI"` dan `"BELUM"`.
- **Sebagai `object`:** Setiap baris menyimpan pointer memori 64-bit ($8 \text{ byte}$) di array BlockManager, ditambah overhead objek string di heap ($\approx 56 \text{ byte}$ per string). Konsumsi memori kolom:
  $$\text{Memori}_{\text{object}} \approx 1.000.000 \times 8 \text{ byte} + \text{Heap Overheads} \approx 50 - 60 \text{ MB}$$
- **Sebagai `category`:** Pandas mengodekan 2 kategori unik menggunakan integer terkecil (`int8` = $1 \text{ byte}$ per baris). Ditambah kamus kategori kecil yang hanya memuat 2 string ($< 1 \text{ KB}$).
  $$\text{Memori}_{\text{category}} \approx 1.000.000 \times 1 \text{ byte} \approx 1 \text{ MB}$$
- **Estimasi Efisiensi:** Penghematan memori mencapai **$> 95\%$** (dari $\approx 55 \text{ MB}$ menjadi $\approx 1 \text{ MB}$).

---

### 4.2 Pembahasan Rancang Bangun Agregasi Runtun Waktu (Bobot: 40%)

**a. Downsampling Data Stasiun Cuaca dari 30 Menit ke Harian:**
```python
# Pastikan kolom Timestamp dikonversi ke tipe datetime dan dijadikan Index
df_stasiun_cuaca['Timestamp'] = pd.to_datetime(df_stasiun_cuaca['Timestamp'])
df_cuaca_idx = df_stasiun_cuaca.set_index('Timestamp')

# Agregasi Harian per Afdeling
df_cuaca_harian = df_cuaca_idx.groupby(['Afdeling', pd.Grouper(freq='D')]).agg(
    Hujan_Harian_mm=('Curah_Hujan_mm', 'sum'),
    Radiasi_Rerata_Wm2=('Radiasi_Surya_Wm2', 'mean')
).reset_index()

# Ubah nama kolom Timestamp menjadi Tanggal untuk penyelarasan merge
df_cuaca_harian.rename(columns={'Timestamp': 'Tanggal'}, inplace=True)
df_cuaca_harian['Tanggal'] = df_cuaca_harian['Tanggal'].dt.date
```

**b. Penggabungan Data Panen dengan Cuaca (Left Join):**
```python
# Pastikan kolom Tanggal pada df_panen bertipe date yang selaras
df_panen['Tanggal'] = pd.to_datetime(df_panen['Tanggal']).dt.date

# Penggabungan multi-kunci
df_gabung = pd.merge(
    df_panen,
    df_cuaca_harian,
    on=['Tanggal', 'Afdeling'],
    how='left'
)
```

**c. Perhitungan Akumulasi Curah Hujan 7 Hari (Rolling Sum per Afdeling):**
```python
# Urutkan berdasarkan Afdeling dan Tanggal sebelum rolling window
df_gabung = df_gabung.sort_values(by=['Afdeling', 'Tanggal'])

# Hitung 7-day rolling sum curah hujan di dalam masing-masing kelompok afdeling
df_gabung['Hujan_Rolling_7H'] = df_gabung.groupby('Afdeling')['Hujan_Harian_mm'].rolling(
    window=7, min_periods=1
).sum().reset_index(level=0, drop=True)
```

---

### 4.3 Pembahasan Solusi: Restrukturisasi Matriks Rotasi Panen (Bobot: 30%)

**1. Sintaks `pd.pivot_table()` Matriks Produktivitas:**
```python
# Ekstrak nama bulan dalam bahasa Indonesia atau representasi bulan
df_panen['Bulan'] = pd.to_datetime(df_panen['Tanggal']).dt.strftime('%B')

# Membuat Pivot Table
matriks_panen = pd.pivot_table(
    df_panen,
    index='Afdeling',
    columns='Bulan',
    values='Yield_Ton_Ha',
    aggfunc='mean',
    fill_value=0.0,
    margins=True,
    margins_name='Rerata_Tahunan'
).round(2)

print(matriks_panen)
```

**2. Fungsi `pd.melt()` dan Relevansi untuk Machine Learning:**
- **Fungsi `pd.melt()`:** Merupakan operasi kebalikan dari pivot (*unpivoting*), yaitu mengubah tabel berformat lebar (*wide format*) menjadi tabel berformat panjang (*long format / tidy data*), di mana setiap variabel menempati satu kolom tersendiri dan setiap observasi menempati satu baris tersendiri.
- **Kebutuhan Sebelum Pelatihan Model AI/ML:** Algoritma *Machine Learning* (seperti Scikit-Learn atau XGBoost) mensyaratkan matriks fitur berbentuk 2D teratur di mana baris merepresentasikan sampel data independen dan kolom merepresentasikan fitur prediktor. Matriks pivot dengan bulan sebagai nama kolom tidak dapat langsung diumpankan ke model regresi. Dengan menggunakan `melt()`, data dikembalikan ke struktur kanonik: `['Afdeling', 'Bulan', 'Produktivitas_Yield']`, yang siap direkayasa fiturnya (misal: penambahan fitur *lagged yield* atau *one-hot encoding* bulan).

---

## 5. Rubrik Penilaian Berbasis Capaian (OBE Assessment Rubric)

| Dimensi Penilaian | Sangat Kurang (< 50) | Cukup (50 - 69) | Baik (70 - 84) | Sangat Memuaskan (85 - 100) |
| :--- | :--- | :--- | :--- | :--- |
| **Pemahaman Arsitektur Tabular & Indeks (Kognitif)** | Masih mengacaukan konsep `.loc` dan `.iloc`; tidak memahami bahaya penugasan berantai (*chained indexing*). | Mengetahui perbedaan label vs integer namun tidak mampu menjelaskan mekanisme internal BlockManager. | Mampu menjelaskan penyebab `SettingWithCopyWarning` dan menulis kode mutasi yang aman secara konsisten. | Menguasai mekanika internal BlockManager, mampu menghitung estimasi penghematan memori tipe `category`, serta memahami backend Apache Arrow. |
| **Keterampilan Transformasi & Agregasi (Psikomotorik)** | Masih menggunakan loop `iterrows()` manual untuk menghitung agregat atau transformasi kolom. | Mampu menggunakan `.groupby()` sederhana namun keliru dalam penggabungan *named aggregations* atau `.transform()`. | Berhasil melakukan agregasi multi-tingkat, menggabungkan data multi-sumber via `.merge()`, dan membuat *pivot table*. | Menghasilkan kode pipeline data yang sangat bersih, modular, menerapkan *downsampling* deret waktu, dan kalkulasi *rolling window* multi-grup secara presisi. |
| **Integritas Analisis Data Agribisnis (Afektif & Terapan)** | Mengabaikan nilai hilang (*NaN*) pasca-merge dan tidak melakukan validasi konsistensi kunci gabungan. | Menyadari adanya baris yang hilang namun tidak memeriksa apakah tipe kunci penggabungan tanggal sudah selaras. | Melakukan pembersihan data secara sistematis dan memberikan interpretasi agronomi yang logis terhadap tren deret waktu. | Menunjukkan kepekaan tinggi terhadap akurasi pelaporan kebun, efisiensi komputasi server, dan kesiapan data untuk pemodelan AI. |
