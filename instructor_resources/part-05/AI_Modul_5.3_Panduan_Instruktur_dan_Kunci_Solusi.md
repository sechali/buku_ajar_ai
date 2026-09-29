# Panduan Instruktur dan Kunci Solusi
# AI Modul 5.3: Dataset (Training dan Testing)

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP) Berbasis OBE (3 SKS / 150 Menit)

Modul ini membekali mahasiswa Sarjana Sains Data, Kecerdasan Buatan, dan Teknik Pertanian dengan disiplin metodologis tingkat tinggi dalam merekayasa partisi dataset. Instruktur bertugas melatih kepekaan mahasiswa dalam mengenali risiko kebocoran data (*data leakage*), autokorelasi spasial, serta pemilihan skema validasi silang yang selaras dengan karakteristik data operasional perkebunan kelapa sawit.

### 1.1 Matriks Alokasi Waktu Sesi Perkuliahan (150 Menit)

| Alokasi Waktu | Aktivitas Pembelajaran | Metode & Media | Peran Instruktur | Target Capaian Mahasiswa |
| :--- | :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20 menit) | **Refleksi & *Problem Framing*:** Studi kasus audit model prediksi panen vendor yang membanggakan akurasi 99.9% namun gagal total saat diterapkan di kebun. | Presentasi kasus industri & bedah naskah kode bocor. | Memandu mahasiswa menemukan baris kode penyebab kebocoran data pada skrip vendor. | Mahasiswa memahami bahwa metrik evaluasi fantastis sering kali merupakan gejala kebocoran data, bukan kecerdasan model. |
| **00:20 - 00:50** (30 menit) | **Dekonstruksi Teori & Skema Partisi:** Holdout 3 tingkat, K-Fold, Stratified K-Fold, TimeSeriesSplit, dan GroupKFold berbasis Hukum Tobler. | Ceramah konsep mendalam, perbandingan diagram alur partisi. | Menjelaskan bahaya *lookahead bias* pada data runtun waktu dan bias autokorelasi spasial kebun. | Mahasiswa mampu memetakan skema partisi yang tepat berdasarkan dependensi temporal dan spasial data. |
| **00:50 - 01:25** (35 menit) | **Praktikum Terbimbing (Hands-on Lab):** Eksperimen komparasi K-Fold vs Stratified (kasus Ganoderma), TimeSeriesSplit, dan isolasi blok GroupKFold. | *Live coding* di Jupyter Notebook. | Mendampingi mahasiswa mengamati fenomena *Zero-Shot Trap* pada K-Fold biasa dan membuktikan efektivitas GroupKFold. | Mahasiswa sukses mengeksekusi empat skema partisi data tanpa galat sintaksis. |
| **01:25 - 02:10** (45 menit) | **Penyelesaian Kasus HOTS Mandiri:** Pengerjaan tantangan audit forensik konsultan (8.1), desain partisi panen 5 tahun (8.2), dan mitigasi autokorelasi ulat api (8.3). | Kerja mandiri berbasis tim (*collaborative inquiry*). | Berkeliling memfasilitasi diskusi kritis, memeriksa integritas pipeline mahasiswa. | Mahasiswa mampu mengaudit kode pihak ketiga dan merekonstruksi pipeline bebas bocor. |
| **02:10 - 02:30** (20 menit) | **Evaluasi Formatif & Refleksi:** Pembahasan solusi kunci, sintesis protokol pertahanan tiga lapis, dan pengantar Modul 5.4 (Features dan Labels). | Diskusi kelas pleno, *code review* silang. | Menyimpulkan prinsip *scientific integrity* dalam sains data dan memberikan umpan balik OBE terukur. | Mahasiswa siap melangkah ke rekayasa fitur dan seleksi variabel prediktor pada modul berikutnya. |

---

## 2. Matriks Identifikasi & Remedi Miskonsepsi Umum Mahasiswa

| No | Miskonsepsi Mahasiswa | Realitas Teknis & Konseptual | Pendekatan Remedi Instruktur |
| :--- | :--- | :--- | :--- |
| 1 | "Semakin tinggi nilai $R^2$ atau Akurasi pada data uji (misal $R^2 > 0.99$), sudah pasti model tersebut semakin hebat dan sempurna." | Pada masalah agribisnis riil yang penuh noise alamiah, nilai $R^2 > 0.98$ hampir selalu merupakan **tanda bahaya (*red flag*) terjadinya kebocoran data (*target leakage*)**, di mana fitur input memuat informasi yang merupakan fungsi langsung dari target. | Tunjukkan eksperimen notebook: fitur `Upah_Borongan` menghasilkan $R^2 = 1.0000$ palsu karena upah dihitung langsung dari tonase panen. Jelaskan konsep kausalitas temporal. |
| 2 | "Mengacak data deret waktu (*time-series*) menggunakan fungsi `shuffle=True` adalah praktik baik agar data latih dan data uji memiliki sebaran yang sama." | Mengacak data kronologis melanggar hukum kausalitas waktu, memicu fenomena **Temporal Leakage / Lookahead Bias**. Model belajar memprediksi kondisi masa lalu menggunakan pola dari masa depan yang di dunia nyata belum terjadi. | Tunjukkan analogi saham atau cuaca: Anda tidak boleh menggunakan data suhu esok hari untuk memprediksi suhu hari ini. Wajibkan penggunaan **TimeSeriesSplit (Forward Chaining)** untuk data berkala. |
| 3 | "Melakukan pembersihan data, pengisian nilai kosong (imputasi), dan normalisasi skala fitur sebelum memanggil `train_test_split()` adalah hal yang efisien dan rapi." | Tindakan ini menyebabkan **Preprocessing Leakage**. Nilai statistik mean dan deviasi standar yang dihitung mencakup informasi dari data uji, sehingga data uji tidak lagi murni independen (*unseen*). | Tanamkan Aturan Emas: **Pecah dataset terlebih dahulu!** Parameter statistik $\mu$ dan $\sigma$ hanya boleh dipelajari dari $X_{\text{train}}$ via `.fit()`, lalu diaplikasikan ke $X_{\text{test}}$ via `.transform()`. |
| 4 | "Jika kita memiliki ribuan data pohon sawit, kita cukup menggunakan `train_test_split()` acak biasa tanpa perlu memikirkan lokasi blok kebun pohon tersebut." | Berdasarkan Hukum Tobler, pohon-pohon di dalam satu blok memiliki autokorelasi tanah dan cuaca yang kuat. Pembagian acak membuat pohon dari blok yang sama terpecah ke train dan test, melatih model menghafal lingkungan blok, bukan pola penyakit. | Tunjukkan bahwa model yang dilatih dengan *random split* akan jatuh performanya saat diuji pada afdeling baru. Wajibkan penggunaan **GroupKFold** untuk data berkelompok geografis. |

---

## 3. Panduan Solusi Lengkap Latihan HOTS (Higher-Order Thinking Skills)

### 3.1 Solusi Tantangan 8.1: Audit Forensik Kebocoran Data Konsultan (Bobot: 35%)

#### 1. Dua Kebocoran Data Fatal pada Naskah Kode Konsultan:
- **Kebocoran 1 (Target Leakage pada Fitur):** Kolom `Tonase_Total_PKS` disertakan sebagai variabel prediktor untuk memprediksi `Produksi_Ton_Ha`. Di pabrik kelapa sawit, tonase total PKS adalah hasil penimbangan fisik dari seluruh truk yang membawa panen dari blok tersebut. Secara matematis:
  $$\text{Produksi\_Ton\_Ha} = \frac{\text{Tonase\_Total\_PKS}}{\text{Luas\_Ha}}$$
  Menyertakan `Tonase_Total_PKS` dan `Luas_Ha` sekaligus membuat algoritma hanya menghitung operasi pembagian aritmatika sederhana, bukan melakukan prediksi biologis pertumbuhan tanaman! Model ini tidak bisa dipakai untuk meramalkan panen sebelum buah dipetik dan ditimbang.
- **Kebocoran 2 (Preprocessing Leakage pada Normalisasi):** Baris `scaler.fit_transform(X)` dieksekusi secara global sebelum proses validasi silang `cross_val_score()`. Akibatnya, pada setiap lipatan fold, data validasi telah mengontaminasi perhitungan nilai mean dan deviasi standar data latih.

#### 2. Naskah Kode Perbaikan Bebas Bocor:
```python
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor

df = pd.read_csv('riwayat_panen_kebun.csv')

# LANGKAH PERBAIKAN 1: Buang fitur target leakage ('Tonase_Total_PKS')!
fitur_valid = ['Luas_Ha', 'Suhu', 'Hujan', 'Dosis_NPK']
X = df[fitur_valid]
y = df['Produksi_Ton_Ha']

# LANGKAH PERBAIKAN 2: Bungkus dalam Pipeline untuk mencegah kontaminasi K-Fold
pipeline_bersih = Pipeline([
    ('scaler', StandardScaler()),
    ('model', GradientBoostingRegressor(random_state=42))
])

# Evaluasi obyektif murni
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
scores_bersih = cross_val_score(pipeline_bersih, X, y, cv=kfold, scoring='r2')

print(f"Rata-rata R2 Score Obyektif (Bebas Bocor): {scores_bersih.mean():.4f}")
print("Hasil ini merefleksikan daya generalisasi ilmiah model yang sesungguhnya.")
```

---

### 3.2 Solusi Tantangan 8.2: Desain Skema Partisi TimeSeriesSplit (Bobot: 35%)

#### 1. Bahaya K-Fold Acak pada Data Runtun Waktu (*Temporal Lookahead Bias*):
Jika data 5 tahun (2021-2025) diacak secara bebas:
- Model berpotensi dilatih menggunakan data panen bulan Desember 2024 untuk memprediksi panen bulan Maret 2022.
- Di dunia nyata, faktor cuaca ekstrem El Nino tahun 2024 atau tren kenaikan produktivitas akibat bertambahnya usia pohon belum pernah terjadi pada tahun 2022.
- Pengacakan waktu membuat model "mengetahui masa depan", menghasilkan ilusi akurasi yang tinggi saat evaluasi namun gagal memprediksi semester kedua 2025.

#### 2. Skema Partisi TimeSeriesSplit (Forward Chaining) 5-Lipatan:
```
Split 1: [ Latih: Tahun 2021 ] ──────────────► [ Uji: Tahun 2022 ]
Split 2: [ Latih: Tahun 2021 - 2022 ] ───────► [ Uji: Tahun 2023 ]
Split 3: [ Latih: Tahun 2021 - 2023 ] ───────► [ Uji: Tahun 2024 ]
Split 4: [ Latih: Tahun 2021 - 2024 ] ───────► [ Uji: Sm. 1 2025 ]
Split 5: [ Latih: Tahun 2021 - Sm. 1 2025 ] ─► [ Uji: Sm. 2 2025 (Target Akhir) ]
```
Skema ini merefleksikan cara kerja sistem di lapangan: model hanya boleh memanfaatkan riwayat historis masa lalu untuk meramalkan masa depan.

#### 3. Sintaks Konfigurasi Scikit-Learn:
```python
from sklearn.model_selection import TimeSeriesSplit

# Konfigurasi 5 lipatan forward chaining
tscv = TimeSeriesSplit(n_splits=5)

for split_no, (train_index, test_index) in enumerate(tscv.split(X)):
    print(f"Split {split_no + 1}: Data Latih = {len(train_index)} baris, Data Uji = {len(test_index)} baris")
```

---

### 3.3 Solusi Tantangan 8.3: Mitigasi Kebocoran Spasial (Bobot: 30%)

#### 1. Penerapan Hukum Tobler pada Kebocoran Spasial Pohon Sawit:
Pohon-pohon di dalam satu blok afdeling yang sama memiliki kedekatan geografis, tipe tanah (misal tanah gambut pedalaman), ketinggian lereng, dan paparan cuaca mikro yang identik. Jika pohon dari Blok A diacak ke data latih dan data uji sekaligus:
- Pohon di data uji memiliki kondisi tanah yang hampir identik dengan pohon di data latih.
- Model cukup menghafal "karakteristik lingkungan Blok A" untuk menebak ada/tidaknya ulat api, bukan mempelajari gejala visual defoliasi daun sawit yang sesungguhnya.

#### 2. Peran Kunci `GroupKFold`:
Dengan menetapkan `groups=df['Kode_Blok']`, algoritma GroupKFold memastikan bahwa:
$$\text{Blok}_{\text{Train}} \cap \text{Blok}_{\text{Test}} = \emptyset$$
Seluruh 500 pohon dari Blok A akan berada utuh di data latih, atau utuh di data uji. Saat data Blok A berada di data uji, model dievaluasi pada lingkungan geografis yang sama sekali baru (*unseen geographic domain*).

#### 3. Risiko Performa dan Integritas Saintifik:
- **Penurunan Metrik Akurasi:** Nilai akurasi pada pengujian GroupKFold biasanya akan turun (misal dari $95\%$ pada random split menjadi $83\%$).
- **Justifikasi Saintifik:** Penurunan akurasi ini **bukan kabar buruk, melainkan kabar baik bagi integritas riset**. Akurasi $83\%$ pada GroupKFold adalah **akurasi jujur** yang mencerminkan performa nyata model saat drone diterbangkan di afdeling baru yang belum pernah disurvei sebelumnya. Sebaliknya, akurasi $95\%$ pada random split adalah akurasi semu akibat kebocoran autokorelasi spasial.

---

## 4. Rubrik Penilaian Portofolio Praktikum Berbasis OBE

| Kriteria Penilaian | Bobot | Sangat Memuaskan (85 - 100) | Memuaskan (70 - 84) | Kurang Memuaskan (< 70) |
| :--- | :--- | :--- | :--- | :--- |
| **Identifikasi & Pencegahan Kebocoran Data** | 30% | Mampu mendiagnosis target leakage dan preprocessing leakage secara forensik serta membangun Scikit-Learn Pipeline bebas bocor yang terbukti secara empiris. | Memahami konsep kebocoran data namun masih melakukan pemisahan manual di luar struktur Pipeline. | Gagal mengidentifikasi target leakage; memanggil normalisasi secara global sebelum partisi train-test. |
| **Penerapan Skema Validasi Silang Terarah** | 25% | Mengonfigurasi Stratified K-Fold pada data kelas tidak seimbang dengan pembuktian matematis distribusi fold yang proporsional. | Menggunakan Stratified K-Fold namun belum mampu menganalisis risiko zero-shot fold trap pada K-Fold biasa. | Mengabaikan ketidakseimbangan kelas sehingga lipatan fold uji tidak memuat sampel kelas minoritas. |
| **Penanganan Dependensi Temporal & Spasial** | 25% | Mengonfigurasi TimeSeriesSplit untuk data runtun waktu dan GroupKFold untuk data spasial kebun dengan justifikasi kausalitas ilmiah yang kuat. | Mampu menjalankan TimeSeriesSplit atau GroupKFold namun argumentasi teoretis Hukum Tobler masih kurang mendalam. | Mengacak data waktu secara bebas (*shuffle time-series*) atau membiarkan sampel satu blok terdistribusi ke latih dan uji. |
| **Kualitas Kode & Ketelitian Analisis Metrik** | 20% | Naskah kode terstruktur rapi, bebas galat eksekusi, analisis komparasi metrik disajikan secara kritis dan obyektif. | Kode berjalan dengan baik namun dokumentasi naratif pada markdown minim analisis data. | Kode mengalami galat eksekusi atau salah menyimpulkan hasil benchmark performa model. |
