# Panduan Instruktur & Kunci Solusi: AI Modul 1.7

**Kode Modul:** AI Modul 1.7  
**Mata Kuliah:** Kecerdasan Buatan (Artificial Intelligence)  
**Judul Modul:** Etika, Keadilan Algoritmik, dan Tata Kelola dalam Penggunaan Artificial Intelligence (Responsible AI & Governance)  
**Target Pengajar:** Dosen Pengampu, Asisten Praktikum, Pengajar Laboratorium AI / Etika Komputasi  

---

## 1. Panduan Pedagogis & Strategi Pengajaran (Pedagogical Blueprint)

Modul 1.7 adalah modul pemungkas dari **Bagian 1: Pengantar Artificial Intelligence**. Banyak mahasiswa menganggap topik etika dan regulasi sebagai "materi hafalan non-teknis". Peran instruktur adalah mendemonstrasikan bahwa etika di era AI modern adalah **disiplin rekayasa kuantitatif (*Quantitative Engineering Discipline*)** yang dapat diuji dengan rumus matematika (*DIR, EOD, Shapley Value*) dan memiliki konsekuensi hukum pidana/perdata nyata (UU PDP No. 27/2022).

### 1.1. Konsep Kunci yang Wajib Ditekankan
1. **Bias Bukan Kesalahan Model, Melainkan Cerminan Masa Lalu**: Tekankan bahwa algoritma hanya meminimalkan fungsi kerugian (*loss function*). Jika data masa lalu penuh diskriminasi terhadap petani kecil atau kelompok marjinal, algoritma yang "sangat cerdas" justru akan menjadi "sangat diskriminatif" secara optimal.
2. **Kerapuhan 'Fairness through Unawareness'**: Jelaskan mengapa sekadar menghapus kolom gender atau status petani dari dataset tidak menyelesaikan bias. Algoritma akan mencari variabel proksi (seperti kelengkapan dokumen jaminan formal atau kode pos) untuk merekonstruksi diskriminasi yang sama.
3. **Kepatuhan Terhadap UU PDP Pasal 40**: Soroti hak hukum subjek data di Indonesia untuk menolak keputusan otomatis penuh (*automated decision-making*) dan kewajiban menyediakan kanal intervensi manusia (*Human-in-the-Loop*).
4. **Bahaya Sistem 'Black-Box' Tanpa Penjelasan (Skandal Robodebt)**: Gunakan studi kasus Robodebt Australia (AUD $1.8 Miliar) untuk menunjukkan bagaimana ketiadaan hak penjelasan (*Right to Explanation*) dapat meremukkan harkat martabat dan kehidupan warga negara miskin.
5. **Dilema Penggunaan Ganda (Dual-Use) & Deepfake**: Diskusikan kasus eksperimen MegaSyn (40.000 senjata kimia dalam 6 jam) dan voice cloning CEO untuk memperingatkan mahasiswa bahwa keahlian teknis AI tanpa landasan etika berpotensi melahirkan senjata pemusnah atau alat kejahatan siber.
6. **Green AI & Jejak Ekologis**: Sadarkan mahasiswa bahwa model kecerdasan buatan bukanlah tanpa dampak fisik; ribuan GPU menghasilkan ratusan ton emisi $CO_2$ dan meminum jutaan liter air pendingin. Arsitektur hemat energi (*Efficient Edge AI*) adalah keharusan moral.
7. **Integritas Akademik & 'Ghost Workers'**: Bahas etika penggunaan LLM bagi mahasiswa (larangan plagiarisme dan bahaya halusinasi sitasi palsu) serta soroti sisi gelap industri anotasi data murah di negara berkembang (*the ghost workers*).

### 1.2. Miskonsepsi Umum Mahasiswa (*Common Student Pitfalls*)
* **Miskonsepsi**: "Keadilan selalu merusak akurasi bisnis secara drastis."  
  *Koreksi Pengajar*: Tunjukkan bukti praktikum kita di mana penerapan *Sample Reweighting* mampu menaikkan DIR dari $0.566$ ke $1.009$ (adil sempurna) dengan akurasi global tetap identik pada $65.50\%$. Keadilan yang dirancang dengan baik sering kali memperbaiki generalisasi jangka panjang.
* **Miskonsepsi**: "Jika AI melakukan kesalahan fatal atau mencelakakan orang, algoritma AI itulah yang bersalah."  
  *Koreksi Pengajar*: AI adalah artefak kode, bukan subjek hukum. Tanggung jawab hukum (*liability*) selalu berada di pundak korporasi pengguna, pimpinan proyek, dan tim pengembang perangkat lunak.

---

## 2. Kunci Jawaban Lengkap Pertanyaan HOTS

### Pertanyaan 1: Analisis Proksi Bias dan Ilusi 'Fairness through Unawareness'
* **Analisis Akar Masalah**:  
  Menghapus variabel sensitif $A$ (*Fairness through Unawareness*) adalah ilusi karena adanya korelasi multivariat laten antara variabel sensitif dengan fitur masukan lainnya (*Proxy Features* atau *Redlining*). Dalam studi kasus perkebunan:
  * Variabel "Kelengkapan Agunan Sertifikat Formal" sangat berkorelasi positif dengan petani korporasi ($A=1$) karena mereka memiliki divisi legal formal, sedangkan petani swadaya ($A=0$) menggarap tanah ulayat atau girik adat yang sah secara agronomis namun tidak memiliki sertifikat bank formal.
  * Model yang dilatih tanpa kolom $A$ akan memberi bobot tinggi pada fitur agunan sebagai pembeda kelulusan pinjaman, mereproduksi diskriminasi yang persis sama ($DIR < 0.80$).
* **Rekomendasi Perbaikan**:  
  Variabel sensitif $A$ justru **wajib dikumpulkan dan diaudit secara eksplisit** selama fase pelatihan guna menghitung metrik disparitas ($DIR, EOD$) dan mengalibrasi bobot sampel (*Reweighting*), meskipun saat inferensi produksi atribut $A$ tidak boleh dijadikan dasar diskriminasi langsung.

### Pertanyaan 2: Dilema Mobil Otonom Perkebunan (The Trolley Problem in AI)
* **Tinjauan Etika Utilitarianisme (Jeremy Bentham)**:  
  Prinsip utilitarianisme menuntut tindakan yang memaksimalkan utilitas total dan meminimalkan jumlah korban jiwa (*The greatest happiness for the greatest number*). Utilitarian akan memilih **Opsi Jalur Kanan** (membelokkan truk ke parit) karena membatasi korban jiwa pada 1 orang operator kabin daripada mengorbankan 3 orang petugas di pos jaga kiri ($1 < 3$).
* **Tinjauan Etika Deontologi (Immanuel Kant)**:  
  Prinsip deontologi menolak memperlakukan manusia semata-mata sebagai sarana (*instrumental means*). Kant menyatakan bahwa membunuh seseorang secara sengaja (dengan sengaja membelokkan truk ke parit untuk mengorbankan teknisi yang tidak bersalah) adalah pelanggaran imperatif kategoris. Penganut etika deontologi berpendapat sistem otonom tidak berhak "memilih siapa yang harus mati", melainkan harus fokus pada prosedur keselamatan murni (misalnya mengaktifkan pengereman darurat maksimal di jalurnya sendiri).
* **Pertanggungjawaban Hukum Menurut UU PDP & Regulasi AI**:  
  Menurut hukum Indonesia dan regulasi AI internasional, tanggung jawab pidana dan perdata berada pada **Penyelenggara Sistem Elektronik (Korporasi Perkebunan)** dan **Produsen Truk Otonom** atas dasar kelalaian (*negligence*) dalam pemeliharaan rem serta ketiadaan protokol keselamatan darurat yang memadai.

---

## 3. Solusi Lengkap Tantangan Praktik (Hands-On Challenges)

### Solusi Tingkat 1: Perhitungan Equal Opportunity Difference ($\Delta\text{TPR}$)
```python
# Evaluasi True Positive Rate (TPR) pada masing-masing kelompok data uji
def hitung_tpr(y_asli, y_ramalan, A_kelompok):
    # TPR = TP / (TP + FN) = Kasus layak kredit yang berhasil disetujui
    mask_priv = (A_kelompok == 1) & (y_asli == 1)
    mask_unpriv = (A_kelompok == 0) & (y_asli == 1)
    
    tpr_priv = np.sum((y_ramalan == 1) & mask_priv) / np.sum(mask_priv)
    tpr_unpriv = np.sum((y_ramalan == 1) & mask_unpriv) / np.sum(mask_unpriv)
    delta_tpr = abs(tpr_priv - tpr_unpriv)
    return tpr_priv, tpr_unpriv, delta_tpr

tpr_p1, tpr_u1, dtpr1 = hitung_tpr(y_test, y_pred_bias, A_test)
tpr_p2, tpr_u2, dtpr2 = hitung_tpr(y_test, y_pred_fair, A_test)

print(f"Model Awal (Bias) : TPR Priv = {tpr_p1*100:.1f}%, TPR Unpriv = {tpr_u1*100:.1f}% | Delta TPR = {dtpr1:.4f}")
print(f"Model Fair (Adil) : TPR Priv = {tpr_p2*100:.1f}%, TPR Unpriv = {tpr_u2*100:.1f}% | Delta TPR = {dtpr2:.4f}")
# Hasil: Delta TPR turun signifikan menuju nol, membuktikan pemerataan kesempatan!
```

### Solusi Tingkat 2: Mitigasi Post-Processing (Threshold Optimizer)
```python
# Menyesuaikan ambang batas keputusan probabilitas
probs_test = model_bias.predict_proba(X_test)[:, 1]

# Petani korporasi diberi threshold lebih ketat (0.55), petani swadaya diberi threshold adil (0.42)
pred_post_priv = (probs_test[mask_priv_test] >= 0.55).astype(int)
pred_post_unpriv = (probs_test[mask_unpriv_test] >= 0.42).astype(int)

rate_p_post = np.mean(pred_post_priv)
rate_u_post = np.mean(pred_post_unpriv)
dir_post = rate_u_post / rate_p_post

print(f"DIR Hasil Optimasi Threshold: {dir_post:.4f} (Lolos Batas Legalitas 0.80)")
```

### Solusi Tingkat 3: Sistem Pelaporan Transparansi Subjek Data (UU PDP Pasal 40)
```python
import json

def generate_laporan_transparansi_pdp(pemohon_id, skor_agro, rasio_arus, keputusan_disetujui):
    rekomendasi = []
    if rasio_arus < 2.5:
        rekomendasi.append({"faktor": "Rasio Arus Kas", "status": "Kurang Memadai", "solusi": "Tingkatkan cadangan kas"})
    if skor_agro < 65.0:
        rekomendasi.append({"faktor": "Kesehatan Kebun", "status": "Perlu Pemupukan", "solusi": "Lakukan pemupukan NPK"})
        
    laporan = {
        "pemohon_id": pemohon_id,
        "keputusan": "DISETUJUI" if keputusan_disetujui else "DITOLAK",
        "hak_subjek_data_uu_pdp": {
            "dasar_hukum": "Pasal 40 UU No. 27 Tahun 2022",
            "hak_banding_manusia": True,
            "kontak_petugas_verifikasi": "layanan-keberatan-kredit@instiper.ac.id"
        },
        "analisis_kontribusi_faktor": rekomendasi
    }
    return json.dumps(laporan, indent=2)

print(generate_laporan_transparansi_pdp("TANI-099", 58.0, 2.1, False))
```

---

## 4. Rubrik Asesmen Praktikum

| Kriteria Penilaian | Bobot (%) | Kinerja Kurang (0-59) | Kinerja Cukup (60-79) | Kinerja Sangat Baik (80-100) |
| :--- | :---: | :--- | :--- | :--- |
| **Pemahaman Metrik DIR & EOD** | 25% | Tidak memahami konsep Disparate Impact atau salah menghitung rasio Four-Fifths Rule. | Mampu menghitung DIR namun belum memahami keterbatasan metrik keadilan yang berbeda. | Mampu menghitung rumus matematis DIR & EOD, mengaitkannya dengan batas hukum 0.80, dan mengaudit bias. |
| **Penerapan Algoritma Mitigasi (Reweighting)** | 35% | Gagal mengimplementasikan rumus Kamiran & Calders atau salah memasukkan bobot sampel. | Berhasil menjalankan reweighting namun tidak memverifikasi pemulihan metrik DIR pasca-latih. | Mengimplementasikan kalkulasi bobot sampel secara mandiri dan membuktikan pemulihan keadilan di atas 0.80. |
| **Analisis Kritis HOTS (Hukum & Etika)** | 25% | Jawaban sangat normatif tanpa analisis teknis proxy feature atau pasal UU PDP. | Mampu menjelaskan masalah proxy feature namun lemah dalam analisis hukum pertanggungjawaban. | Menganalisis fenomena redlining, menautkan pasal 40 UU PDP, dan menyajikan sintesis filsafat etika yang tajam. |
| **Penyelesaian Tantangan Praktik** | 15% | Hanya mencoba tantangan tingkat 1. | Mampu menyelesaikan tantangan tingkat 1 dan 2 dengan benar. | Menyelesaikan seluruh tantangan hingga perancangan laporan audit kepatuhan subjek data (Tingkat 3). |
