# Panduan Instruktur & Kunci Solusi: AI Modul 1.6

**Kode Modul:** AI Modul 1.6  
**Mata Kuliah:** Kecerdasan Buatan (Artificial Intelligence)  
**Judul Modul:** Workflow Pengembangan Proyek Artificial Intelligence (AI Project Lifecycle)  
**Target Pengajar:** Dosen Pengampu, Asisten Praktikum, Pengajar Laboratorium AI / MLOps  

---

## 1. Panduan Pedagogis & Strategi Pengajaran (Pedagogical Blueprint)

Modul 1.6 mengajarkan paradigma rekayasa perangkat lunak modern untuk AI (*Machine Learning Operations / MLOps*). Sering kali mahasiswa berpikir bahwa membuat model AI hanyalah menulis kode pelatihan 3 baris. Modul ini bertujuan menanamkan disiplin rekayasa industri tingkat tinggi.

### 1.1. Konsep Kunci yang Wajib Ditekankan
1. **Bahaya Mengerikan Data Leakage**: Tunjukkan secara visual dan konseptual apa yang terjadi jika `StandardScaler` dipanggil pada seluruh data sebelum `train_test_split`. Jelaskan bahwa model tidak lagi belajar generalisasi, melainkan "melihat bocoran masa depan".
2. **Kekuatan Enkapsulasi `sklearn.pipeline.Pipeline`**: Tunjukkan bahwa Pipeline adalah dinding pertahanan terbaik pengembang perangkat lunak untuk memastikan preprocessing dan estimator dieksekusi secara atomik.
3. **Model di Produksi Tidak Pernah Statis (*The Drift Reality*)**: Ingatkan mahasiswa bahwa model AI di dunia nyata tidak seperti kalkulator matematika yang hasilnya selalu konstan. Dunia berubah, cuaca berganti, perilaku konsumen berevolusi. Tanpa sistem pemantauan seperti *Population Stability Index* (PSI), model AI yang tadinya pintar akan perlahan menjadi usang dan merugikan organisasi.

### 1.2. Miskonsepsi Umum Mahasiswa (*Common Student Pitfalls*)
* **Miskonsepsi**: "Saya mendapatkan akurasi 99% pada data uji setelah melakukan imputasi missing value dengan rata-rata satu tabel penuh. Model saya luar biasa!"  
  *Koreksi Pengajar*: Itu adalah data leakage klasik. Model menghafal informasi data uji melalui nilai rata-rata global.
* **Miskonsepsi**: "Jika model mengalami penurunan akurasi di produksi, kita langsung menghapus model lama dan melatih model baru hanya dari data kemarin."  
  *Koreksi Pengajar*: Menghapus data lama memicu *Catastrophic Forgetting*. Pola musiman masa lalu akan hilang. Solusi yang benar adalah penggabungan bertimbang (*weighted data replay*) atau ensemble modeling.

---

## 2. Kunci Jawaban Lengkap Pertanyaan HOTS

### Pertanyaan 1: Analisis Akar Masalah Data Leakage Imputasi Global
* **Analisis Akar Masalah**:  
  Ketika `df.fillna(df.mean())` dipanggil sebelum pembagian data, nilai rata-rata $\mu_{\text{total}}$ dihitung dari gabungan data latih dan data uji:
  $$\mu_{\text{total}} = \frac{N_{\text{train}} \cdot \mu_{\text{train}} + N_{\text{test}} \cdot \mu_{\text{test}}}{N_{\text{total}}}$$
  Nilai rata-rata ini menyusupkan informasi distribusi masa depan ke baris-baris data latih yang kosong. Saat pengujian lokal, model seolah-olah mengenali pola data uji dengan $R^2 = 96\%$. Namun di pabrik nyata pada bulan berikutnya, data baru memiliki $\mu_{\text{masa depan}}$ yang sama sekali tidak diketahui oleh model, sehingga nilai pengganti yang dipelajari model tidak lagi relevan dan akurasi runtuh menjadi $R^2 = 58\%$.
* **Solusi Perbaikan Prosedural**:  
  Pemisahan data harus dilakukan pada detik pertama. Imputasi harus dibungkus di dalam objek `SimpleImputer()` di dalam `Pipeline` sehingga ia hanya mempelajari `mean` dari $X_{\text{train}}$ dan menerapkannya secara pasif ke $X_{\text{test}}$ dan data produksi baru.

### Pertanyaan 2: Dilema Retraining: Mengatasi Drift vs Melupakan Pola Historis
* **Analisis Risiko**:  
  Menghapus seluruh data historis lama dan hanya menyisakan data 3 bulan terakhir saat musim hujan ekstrem akan menyebabkan model mengalami **Catastrophic Forgetting**. Model hanya akan mengenali karakteristik tanah basah dan langit mendung. Begitu cuaca kembali normal ke musim kemarau di bulan ke-4, model akan lumpuh total karena tidak lagi mengingat bagaimana perilaku tanaman saat kelembaban tanah rendah dan suhu tinggi.
* **Strategi yang Bijaksana**:  
  1. *Weighted Sample Replay*: Menggabungkan data baru (misal berbobot $70\%$) dengan sampel representatif data historis lama ($30\%$).
  2. *Ensemble Stacking*: Mempertahankan model basis historis dan menggabungkannya dengan model adaptasi lokal menggunakan pembobotan *Exponential Moving Average* (EMA).

---

## 3. Solusi Lengkap Tantangan Praktik (Hands-On Challenges)

### Solusi Tingkat 1: Eksplorasi Penalti Regularisasi $\alpha$ Ridge
```python
alphas = [0.001, 1.0, 100.0, 10000.0]
for a in alphas:
    pipe = Pipeline([('scaler', StandardScaler()), ('reg', Ridge(alpha=a))])
    pipe.fit(X_train, y_train)
    r2_tr = pipe.score(X_train, y_train)
    r2_te = pipe.score(X_test, y_test)
    print(f"Alpha: {a:<7} | R2 Train: {r2_tr*100:.2f}% | R2 Test: {r2_te*100:.2f}%")
```
*Hasil & Interpretasi*: Pada $\alpha = 0.001$ dan $1.0$, $R^2$ optimal stabil di $\sim 96.5\%$. Pada $\alpha = 10000.0$, penalti regularisasi terlalu menekan koefisien bobot mendekati nol ($\mathbf{w} \to \mathbf{0}$), sehingga $R^2$ anjlok drastis ke $< 10\%$ (*underfitting parah*).

### Solusi Tingkat 2: Pembersihan Outlier Menggunakan Z-Score Higienis
```python
def bersihkan_outlier_train(X_tr, y_tr, threshold=3.0):
    # Hitung rata-rata dan deviasi standar HANYA dari data latih
    mu = np.mean(X_tr, axis=0)
    sigma = np.std(X_tr, axis=0)
    z_scores = np.abs((X_tr - mu) / sigma)
    # Ambil indeks baris yang tidak memiliki fitur dengan z-score > 3.0
    baris_bersih = np.all(z_scores < threshold, axis=1)
    return X_tr[baris_bersih], y_tr[baris_bersih]

X_train_bersih, y_train_bersih = bersihkan_outlier_train(X_train, y_train)
print(f"Baris tersisa setelah pembersihan outlier: {len(y_train_bersih)} dari {len(y_train)}")
```

### Solusi Tingkat 3: Kelas `AutoMLOpsOrchestrator`
```python
class AutoMLOpsOrchestrator:
    def __init__(self, baseline_dist, pipeline_model):
        self.baseline_dist = baseline_dist
        self.model = pipeline_model
        self.versi = 1

    def monitor_and_update(self, data_baru_X, data_baru_y, suhu_kolom_idx=1):
        suhu_baru = data_baru_X[:, suhu_kolom_idx]
        psi = hitung_psi(self.baseline_dist, suhu_baru)
        print(f"-> Audit PSI Terkini: {psi:.4f}")
        
        if psi <= 0.25:
            print(f"[STATUS] Model v{self.versi} Sehat & Stabil. Tidak perlu retraining.")
        else:
            print(f"[ALERT] Drift Signifikan Terdeteksi (PSI={psi:.4f})! Memicu Automated Retraining...")
            # Menggabungkan data latih lama dan baru
            X_gabung = np.vstack([X_train, data_baru_X])
            y_gabung = np.concatenate([y_train, data_baru_y])
            # Re-fit pipeline
            self.model.fit(X_gabung, y_gabung)
            self.versi += 1
            # Perbarui baseline
            self.baseline_dist = X_gabung[:, suhu_kolom_idx]
            print(f"[SUKSES] Model berhasil dilatih ulang dan dipromosikan ke Versi v{self.versi}!")
```

---

## 4. Rubrik Asesmen Praktikum

| Kriteria Penilaian | Bobot (%) | Kinerja Kurang (0-59) | Kinerja Cukup (60-79) | Kinerja Sangat Baik (80-100) |
| :--- | :---: | :--- | :--- | :--- |
| **Pemahaman Metrik PSI & Drift** | 25% | Tidak memahami konsep drift atau salah menginterpretasikan angka PSI. | Mampu menghitung PSI namun kurang memahami perbedaan Data Drift vs Concept Drift. | Mampu menghitung rumus PSI, membedakan drift, dan mengaitkannya dengan ambang batas tindakan MLOps. |
| **Penerapan Pipeline & Anti-Leakage** | 35% | Masih melakukan normalisasi sebelum pembagian data latih-uji (*data leakage*). | Menggunakan Pipeline namun belum memahami parameter serialisasi atau partisi higienis. | Mengimplementasikan `Pipeline` scikit-learn secara atomik, bebas kebocoran, dan sukses diserialisasi. |
| **Analisis Kritis HOTS** | 25% | Gagal menganalisis akar masalah kebocoran data pada skenario studi kasus. | Mengetahui letak kebocoran namun gagal memberikan formulasi perbaikan sistematis. | Memberikan analisis mathematically sound tentang propagasi bias dan perancangan pipeline yang tangguh. |
| **Penyelesaian Tantangan** | 15% | Hanya mencoba tantangan tingkat 1. | Menyelesaikan hingga tantangan tingkat 2 dengan benar. | Menyelesaikan seluruh tantangan hingga perancangan kelas orkestrator retraining otomatis (Tingkat 3). |
