# AI Modul 7.5: Panduan Instruktur & Kunci Solusi
## Random Forest

---

## 1. Identitas Modul & Kerangka Pembelajaran

* **Kode Modul**: AI-07-05-INS
* **Mata Kuliah**: Kecerdasan Buatan & Pembelajaran Mesin Terapan (INSTIPER)
* **Target Pembaca**: Dosen Pengampu, Asisten Praktikum, dan Laboran
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Ansambel, Bagging, & OOB; 70 Menit Praktikum Scikit-Learn & Analisis MDI; 30 Menit Evaluasi Kasus Pabrik Kelapa Sawit)
* **Karakteristik Modul**: Pembelajaran Ansambel Terawasi (*Supervised Ensemble Learning*), Reduksi Varians, Validasi Internal Out-of-Bag (OOB)

---

## 2. Panduan Pedagogis & Strategi Pengajaran

### 2.1 Peta Konseptual & Alur Pembelajaran
Random Forest adalah transisi krusial dari model individu menuju model kolektif (*ensemble learning*):
1. **Dari Instabilitas ke Ketangguhan Kolektif**: Pada AI Modul 7.4, mahasiswa melihat bagaimana pohon keputusan tunggal sangat rapuh terhadap variasi data kecil (*high variance*). Pada AI Modul 7.5, instruktur mengarahkan mahasiswa untuk memahami analogi "Dewan Pertimbangan Perkebunan": satu mandor mungkin keliru menilai satu truk sawit, namun kesepakatan dari 150 mandor independen hampir pasti menghasilkan keputusan yang objektif dan tepat.
2. **Peran Kunci Random Subspace**: Tekankan bahwa *Bagging* saja tidak cukup jika ada satu variabel yang terlalu dominan (misalnya *Kadar Brondolan Lepas*). Algoritma Random Forest memaksa setiap pemisahan simpul hanya memilih $m = \sqrt{p}$ fitur acak agar pohon-pohon lain terpaksa melihat variabel lain (seperti jam tunda atau kadar asam), menciptakan keanekaragaman perspektif yang menurunkan korelasi antar-pohon ($\rho$).

### 2.2 Miskonsepsi Umum Mahasiswa (*Common Misconceptions*)
* **Miskonsepsi 1: "Menambah jumlah pohon dari 100 menjadi 1000 akan menyebabkan model mengalami overfitting."**
  * *Koreksi Instruktur*: Buktikan secara matematis melalui Teorema Breiman bahwa penambahan pohon pada Random Forest **tidak pernah memicu overfitting**. Kurva galat generalisasi akan melandai secara asimtotik menuju batas konvergen. Pembatasan jumlah pohon semata-mata dilakukan demi efisiensi memori dan kecepatan inferensi.
* **Miskonsepsi 2: "Skor validasi internal OOB lebih rendah nilainya daripada akurasi data latih, berarti model memiliki galat tinggi."**
  * *Koreksi Instruktur*: Jelaskan bahwa akurasi data latih pada pohon tanpa pruning selalu mendekati 100% karena memorisasi. Skor OOB bukanlah skor data latih, melainkan hasil evaluasi pada data yang *tidak pernah dilihat* oleh masing-masing pohon (ekuivalen secara teoritis dengan $K$-Fold Cross Validation).
* **Miskonsepsi 3: "Skor Feature Importance (MDI) adalah kebenaran mutlak hubungan sebab-akibat agronomi."**
  * *Koreksi Instruktur*: Tunjukkan bahwa MDI memiliki bias buatan terhadap fitur kontinu yang memiliki banyak desimal unik. Instruktur wajib mengajarkan mahasiswa cara memverifikasi MDI menggunakan *Permutation Importance* sebelum mengambil keputusan manajerial perkebunan.

---

## 3. Kunci Jawaban & Pembahasan Latihan Soal HOTS Diktat

### Soal 1: Analisis Matematis Teorema Juri Condorcet (C3)
Parameter sistem inspeksi tandan sawit:
* Jumlah pohon juri independen: $B = 5$
* Probabilitas ketepatan tiap juri: $p = 0.70$, sehingga probabilitas galat $q = 1 - p = 0.30$.

#### Langkah 1: Menentukan Ambang Mayoritas
Keputusan mayoritas tercapai jika lebih dari separuh juri menjawab benar:
$$k_{\text{min}} = \left\lfloor \frac{B}{2} \right\rfloor + 1 = \left\lfloor \frac{5}{2} \right\rfloor + 1 = 2 + 1 = \mathbf{3 \text{ juri}}$$

#### Langkah 2: Menghitung Probabilitas Ansambel ($P_{\text{ansambel}}$)
Probabilitas total adalah jumlah probabilitas kondisi di mana tepat 3, 4, atau 5 juri menjawab benar:
$$P_{\text{ansambel}} = \sum_{k=3}^5 \binom{5}{k} (0.70)^k (0.30)^{5-k}$$

1. **Kasus Tepat 3 Juri Benar ($k = 3$)**:
   $$\binom{5}{3} (0.70)^3 (0.30)^2 = 10 \times 0.343 \times 0.09 = \mathbf{0.30870}$$
2. **Kasus Tepat 4 Juri Benar ($k = 4$)**:
   $$\binom{5}{4} (0.70)^4 (0.30)^1 = 5 \times 0.2401 \times 0.30 = \mathbf{0.36015}$$
3. **Kasus Seluruh 5 Juri Benar ($k = 5$)**:
   $$\binom{5}{5} (0.70)^5 (0.30)^0 = 1 \times 0.16807 \times 1.0 = \mathbf{0.16807}$$

Jumlahkan ketiga probabilitas tersebut:
$$P_{\text{ansambel}} = 0.30870 + 0.36015 + 0.16807 = \mathbf{0.83692 \text{ (atau } \approx 83.69\%)}$$

#### Langkah 3: Komparasi dan Kesimpulan
Akurasi meningkat drastis dari **70.00%** (pohon tunggal) menjadi **83.69%** (ansambel 5 pohon), dengan penurunan tingkat kesalahan dari $30.00\%$ menjadi $16.31\%$ (berkurang hampir separuhnya). Ini membuktikan keunggulan matematis pemungutan suara mayoritas.

---

### Soal 2: Penurunan Limit Sampel Out-of-Bag (OOB) (C4)
Formulasi probabilitas sampel tidak terpilih dalam $N$ tarikan dengan pengembalian:
$$P_{\text{OOB}}(N) = \left(1 - \frac{1}{N}\right)^N$$

#### Langkah 1: Perhitungan Eksak untuk $N = 2, 5, 10$
* Untuk $N = 2$:
  $$P(2) = \left(1 - \frac{1}{2}\right)^2 = (0.5)^2 = \mathbf{0.25000 \text{ (25.0\%)}}$$
* Untuk $N = 5$:
  $$P(5) = \left(1 - \frac{1}{5}\right)^5 = (0.8)^5 = \mathbf{0.32768 \text{ (32.8\%)}}$$
* Untuk $N = 10$:
  $$P(10) = \left(1 - \frac{1}{10}\right)^{10} = (0.9)^{10} = \mathbf{0.348678 \text{ (34.9\%)}}$$

#### Langkah 2: Pembuktian Analitik Limit Menuju $e^{-1}$
Misalkan $L = \lim_{N \to \infty} \left(1 - \frac{1}{N}\right)^N$. Ambil logaritma natural ($\ln$) pada kedua sisi:
$$\ln L = \lim_{N \to \infty} \ln \left[\left(1 - \frac{1}{N}\right)^N\right] = \lim_{N \to \infty} N \ln \left(1 - \frac{1}{N}\right)$$

Ubah ke bentuk tak tentu $\frac{0}{0}$ dengan memisalkan $h = \frac{1}{N}$, di mana saat $N \to \infty$, maka $h \to 0$:
$$\ln L = \lim_{h \to 0} \frac{\ln(1 - h)}{h}$$

Terapkan Aturan L'Hôpital (turunkan pembilang dan penyebut terhadap $h$):
$$\ln L = \lim_{h \to 0} \frac{\frac{d}{dh}[\ln(1 - h)]}{\frac{d}{dh}[h]} = \lim_{h \to 0} \frac{\frac{-1}{1 - h}}{1} = \frac{-1}{1 - 0} = -1$$

Kembalikan ke fungsi eksponensial:
$$L = e^{-1} = \frac{1}{e} \approx \mathbf{0.367879 \dots \approx 36.8\% \quad \text{[TERBUKTI]}}$$

#### Langkah 3: Konsekuensi Praktis di Industri Sawit
Limit $36.8\%$ menjamin bahwa pada dataset operasional kebun berskala besar ($N > 1000$), setiap pohon selalu menyisakan sekitar sepertiga data yang tidak pernah tersentuh proses pelatihan. Model dapat memanfaatkan sampel ini untuk menghitung validasi internal OOB secara gratis, menghemat waktu komputasi tanpa memerlukan pembagian 10-Fold Cross Validation yang memakan waktu lama.

---

### Soal 3: Formulasi Penurunan Varians dan Efek Korelasi Antar-Pohon (C4)
Diketahui parameter regresi tonase TBS:
* Varians pohon tunggal: $\sigma^2 = 16.0\text{ (ton)}^2$
* Korelasi rata-rata awal: $\rho = 0.25$
* Jumlah pohon: $B = 100$

#### Langkah 1: Perhitungan Varians Ansambel ($B = 100$)
$$\text{Var}(\bar{f}(x)) = \rho \sigma^2 + \frac{1 - \rho}{B} \sigma^2$$
$$\text{Var}(\bar{f}(x)) = (0.25 \times 16.0) + \left(\frac{1 - 0.25}{100} \times 16.0\right) = 4.0 + \left(\frac{0.75}{100} \times 16.0\right) = 4.0 + 0.12 = \mathbf{4.12 \text{ (ton)}^2}$$

#### Langkah 2: Batas Varians Minimum Teoretis ($B \to \infty$)
Saat $B \to \infty$, suku kedua lenyap:
$$\lim_{B \to \infty} \text{Var}(\bar{f}(x)) = \rho \sigma^2 = 0.25 \times 16.0 = \mathbf{4.00 \text{ (ton)}^2}$$
Artinya, menambah pohon dari 100 ke 10.000 hanya mampu menurunkan varians dari 4.12 ke 4.00 (penurunan marjinal yang tidak sebanding dengan beban memori).

#### Langkah 3: Pengaruh Penurunan Korelasi ke $\rho = 0.10$
Jika analis menerapkan pengacakan fitur agresif sehingga $\rho$ turun ke $0.10$:
$$\text{Var}_{\text{min}} = \rho \sigma^2 = 0.10 \times 16.0 = \mathbf{1.60 \text{ (ton)}^2}$$
*Implikasi Agronomi*: Penurunan varians dari $4.00$ ke $1.60\text{ (ton)}^2$ mempersempit simpangan baku galat taksiran dari $\pm 2.0$ ton menjadi $\pm 1.26$ ton. Ini membuktikan bahwa **menurunkan korelasi antar-pohon jauh lebih berdaya guna dalam menstabilkan model daripada sekadar menambah jumlah pohon estimator**.

---

## 4. Kunci Solusi Tugas Praktikum Notebook

### 4.1 Eksplorasi Pengaruh Parameter `max_features`
```python
for mf in ['sqrt', 'log2', None]:
    rf = RandomForestClassifier(n_estimators=100, max_features=mf, oob_score=True, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    print(f"max_features={str(mf):<6} | OOB Score: {rf.oob_score_*100:.2f}% | Test Acc: {rf.score(X_test, y_test)*100:.2f}%")
```
*Temuan*: `max_features='sqrt'` menghasilkan skor uji terbaik karena memaksa keragaman percabangan, sedangkan `max_features=None` (bagging murni tanpa subspace) menghasilkan korelasi pohon yang lebih tinggi dan generalisasi yang lebih rendah.

### 4.2 Simulasi Penilaian Mutu Truk Baru
```python
truk_uji = pd.DataFrame([
    {'Brondolan_Lepas_%': 28.5, 'Kadar_FFA_%': 2.1, 'Kadar_Air_%': 18.0, 'Jam_Tunda_Angkut': 6.0, 'Berat_Tandan_kg': 26.0, 'Ketinggian_Blok': 85.0},
    {'Brondolan_Lepas_%': 4.2,  'Kadar_FFA_%': 7.8, 'Kadar_Air_%': 29.5, 'Jam_Tunda_Angkut': 42.0, 'Berat_Tandan_kg': 12.0, 'Ketinggian_Blok': 310.0}
])
pred_kelas = rf_clf.predict(truk_uji)
pred_prob = rf_clf.predict_proba(truk_uji)

label_map = {0: 'Afkir/Mentah', 1: 'Standar', 2: 'Matang Prima'}
for i, (k, p) in enumerate(zip(pred_kelas, pred_prob)):
    print(f"Truk {i+1}: {label_map[k]} (Probabilitas Konsensus: {p[k]*100:.1f}%)")
```

### 4.3 Analisis Kritis Limitasi Ekstrapolasi Regresi
Pohon keputusan dan Random Forest membagi ruang fitur menjadi hiper-persegi panjang ortogonal dengan prediksi konstan di setiap daun. Ketika sampel uji memiliki brondolan = 60%, sampel tersebut akan jatuh ke simpul daun paling kanan yang dilatih pada nilai maksimum historis data latih (~35%). Oleh karena itu, Random Forest tidak akan pernah memprediksi rendemen di atas nilai batas atas data latihnya.

---

## 5. Rubrik Penilaian Berbasis Outcome-Based Education (OBE)

| Ranah Kognitif | Kriteria Penilaian | Bobot (%) | Indikator Kinerja Luaran |
|:---:|:---|:---:|:---|
| **C2 (Pemahaman)** | Teori Ansambel, Bagging, & Limit OOB | 25% | Mampu menguraikan Teorema Juri Condorcet, menurunkan limit matematis $1/e$, dan menjelaskan fungsi pengacakan *random subspace*. |
| **C3 (Penerapan)** | Implementasi Pemodelan & Validasi OOB | 35% | Mampu mengimplementasikan `RandomForestClassifier` dan `Regressor`, mengaktifkan OOB score, serta mengekstraksi metrik MDI secara akurat. |
| **C4 (Analisis)** | Diagnosis Varians, Konvergensi, & Kepentingan Fitur | 40% | Mampu menganalisis kurva konvergensi jumlah estimator, membedah disparitas MDI vs Permutation Importance, dan merancang mitigasi bias di PKS. |

---

## 6. Jembatan Pedagogis ke AI Modul 7.6 (Naive Bayes)

Di akhir praktikum, instruktur disarankan membuka wawasan mahasiswa mengenai batas efisiensi Random Forest:
1. **Tinjauan Bebas Komputasi**: Random Forest luar biasa akurat dan stabil, namun modelnya berat dan rakus memori karena harus memelihara ratusan struktur pohon. Tanyakan: *"Bagaimana jika sistem AI harus ditanamkan pada mikrokontroler sensor di tengah kebun sawit yang hanya bertenaga baterai surya kecil?"*
2. **Ketiadaan Inferensi Probabilitas Murni**: Random Forest menghitung skor probabilitas dari frekuensi voting daun, bukan dari hukum probabilitas analitik sejati.
3. **Mengantarkan Pendekatan Bayesian**: Sampaikan bahwa pada pertemuan berikutnya (**AI Modul 7.6: Naive Bayes**), mahasiswa akan mempelajari pendekatan klasifikasi probabilitas bersyarat yang sangat ringan, beroperasi secepat kilat dengan operasi aritmetika dasar, dan menjadi fondasi diagnostik cepat di perkebunan modern.

---

## 7. Daftar Pustaka dan Referensi Akademik

1. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5-32.
2. Breiman, L. (1996). Bagging predictors. *Machine Learning*, 24(2), 123-140.
3. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. [Tersedia di koleksi src/]
4. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media. [Tersedia di koleksi src/]
5. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer. [Tersedia di koleksi src/]
6. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning: with Applications in R* (2nd ed.). Springer. [Tersedia di koleksi src/]
7. Louppe, G. (2014). Understanding random forests: From theory to practice. *arXiv preprint arXiv:1407.7502*.
