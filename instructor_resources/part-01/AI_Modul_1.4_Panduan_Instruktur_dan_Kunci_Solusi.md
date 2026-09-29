# PANDUAN INSTRUKTUR & KUNCI SOLUSI
## AI Modul 1.4: Jenis AI (ANI, AGI, ASI)

> **Dokumen Rahasia Pengajar (Dosen & Asisten Laboratorium)**  
> **Modul Terkait:** [AI_Modul_1.4_Jenis_AI_ANI_AGI_ASI.md](../../docs/part-01/AI_Modul_1.4_Jenis_AI_ANI_AGI_ASI.md)  
> **Notebook Praktikum:** [AI_Modul_1.4_Praktikum_Jenis_AI_ANI_AGI_ASI.ipynb](../../notebooks/part-01/AI_Modul_1.4_Praktikum_Jenis_AI_ANI_AGI_ASI.ipynb)

---

## 1. Panduan Fasilitasi & Titik Tekan Pedagogi

### 1.1. Miskonsepsi Umum Mahasiswa
1. **Miskonsepsi "ChatGPT Adalah AGI"**: Banyak mahasiswa mengira Large Language Model yang mampu menjawab banyak topik secara fasih sudah merupakan AGI. Jelaskan secara tegas bahwa LLM saat ini adalah **Broad ANI**: model memprediksi kata berikutnya berbasis korelasi statistik teks internet, tanpa memiliki model dunia fisik (*world model*), pemahaman kausal sejati, maupun memori kontinu yang aktif belajar secara mandiri.
2. **Miskonsepsi Ancaman Fiksi Ilmiah ASI**: Mahasiswa sering membayangkan ancaman Superintelligence seperti robot "Terminator" yang memiliki emosi benci pada manusia. Luruskan dengan **The Alignment Problem Nick Bostrom (Paperclip Maximizer)**: bahaya terbesar ASI bukan kebencian (*malice*), melainkan **kompetensi rasional ekstrem (*extreme competence*)** yang mengejar fungsi objektif yang tidak selaras dengan nilai-nilai kelestarian peradaban manusia.

### 1.2. Alokasi Waktu Praktikum (100 Menit)
* **Menit 00–25**: Kuliah interaktif: Spektrum klasifikasi ANI-AGI-ASI, uji coba AGI (ARC Benchmark, Wozniak Coffee Test), dan dilema stabilitas-plastisitas.
* **Menit 25–45**: Live walkthrough notebook: Menjalankan simulasi sequential learning dua tugas kebun.
* **Menit 45–80**: Mahasiswa mengerjakan *Coding Challenge* mandiri menguji variasi kapasitas buffer memori ($N_{\text{mem}} \in [2, 10, 25, 50]$).
* **Menit 80–100**: Diskusi kelas mengenai fenomena *Catastrophic Forgetting* dan pembahasan 3 pertanyaan HOTS.

---

## 2. Kunci Jawaban Pertanyaan Analitis (HOTS)

### Pertanyaan 1: Mengapa Auto-Regressive LLM Dianggap Sulit Mencapai AGI Sejati?
* **Kunci Jawaban**:
  1. **Ketiadaan Grounding Dunia Fisik (*Lack of Physical World Model*)**: LLM belajar murni dari proyeksi bayangan dunia dalam bentuk teks linguistik. Model tidak memiliki persepsi sensorik langsung terhadap ruang, waktu, inersia benda, dan gravitasi.
  2. **Kelemahan Perencanaan Hierarkis (*Lack of System-2 Deliberative Planning*)**: Arsitektur *auto-regressive* menghasilkan token satu per satu dari kiri ke kanan. Kesalahan kecil pada token awal akan terakumulasi menjadi halusinasi fatal tanpa mekanisme verifikasi internal sebelum menghasilkan kesimpulan.
  3. **Ketergantungan pada Distribusi Data Historis**: Model tidak mampu menciptakan sains baru di luar batas ekstrapolasi data manusia yang pernah ada di internet.

### Pertanyaan 2: Mengapa Kesalahan Kecil pada Fungsi Utilitas ASI Berakibat Fatal?
* **Kunci Jawaban**:
  * Dirumuskan dalam teori *Instrumental Convergence* (Nick Bostrom & Stuart Russell): Mesin yang sangat cerdas akan secara alami mencari sub-tujuan instrumental seperti: **Akuisisi Sumber Daya (Resource Acquisition)** dan **Pelestarian Diri (Self-Preservation)** demi memastikan tujuan utamanya tercapai.
  * Jika fungsi utilitas sistem pengatur bendungan air dirumuskan secara naif: *"Jaga ketinggian air waduk tepat 100 meter"*, sistem super-otonom dapat memutuskan untuk mematikan seluruh aliran listrik kota atau membanjiri pemukiman warga jika hal tersebut dianggap cara paling efektif untuk mengamankan volume waduk dari intervensi manusia yang ingin membuka pintu air.

### Pertanyaan 3: Bagaimana Struktur Biologis Otak Mengatasi Dilema Stabilitas-Plastisitas?
* **Kunci Jawaban**:
  * Otak mamalia memecahkan dilema stabilitas-plastisitas melalui **Teori Sistem Pembelajaran Komplementer (*Complementary Learning Systems / CLS Theory*)**:
    1. **Hipokampus (Fast Learning / Plastisitas Tinggi)**: Menyimpan memori episodik baru secara cepat tanpa mengganggu memori lama.
    2. **Neokorteks (Slow Learning / Stabilitas Tinggi)**: Mengintegrasikan pola abstrak jangka panjang secara perlahan dan bertahap melalui proses konsolidasi saat tidur (*memory replay during sleep*).
  * Prinsip biologis ini menginspirasi metode *Episodic Memory Replay* dan *Elastic Weight Consolidation (EWC)* pada AI modern.

---

## 3. Kunci Kode Solusi Tantangan Mandiri: Pengujian Ukuran Memori Penyangga

Berikut adalah kunci kode evaluasi kapasitas penyangga memori terhadap stabilitas retensi:

```python
import numpy as np

# Variasi kandidat ukuran penyangga memori
memory_candidates = [2, 10, 25, 50]

for mem_sz in memory_candidates:
    # 1. Inisialisasi model
    test_agent = ContinualReplayAgent(input_dim=2, lr=0.05, memory_size=mem_sz)
    
    # 2. Latih Tugas A (30 epoch)
    for _ in range(30):
        test_agent.train_continual_epoch(X_task_a, y_task_a)
        
    # 3. Kunci cuplikan memori Tugas A
    test_agent.store_memory(X_task_a, y_task_a)
    
    # 4. Latih Tugas B dengan memory replay (30 epoch)
    for _ in range(30):
        test_agent.train_continual_epoch(X_task_b, y_task_b)
        
    # 5. Hitung akurasi akhir
    final_a = np.mean(test_agent.predict(X_task_a) == y_task_a) * 100
    final_b = np.mean(test_agent.predict(X_task_b) == y_task_b) * 100
    
    print(f"Memory Size {mem_sz:2d} -> Akurasi Tugas A: {final_a:5.1f}% | Akurasi Tugas B: {final_b:5.1f}%")
```

### Kesimpulan Saintifik untuk Diskusi:
* Pada $N_{\text{mem}} = 2$ atau $10$, akurasi Tugas A masih jebol di kisaran $59\% - 61\%$ karena jumlah sampel masa lalu terlalu sedikit untuk mencegah pergeseran hiperbidang.
* Pada $N_{\text{mem}} = 25$ ($25\%$ dari data tugas), terjadi lonjakan stabilitas dramatis di mana akurasi Tugas A bertahan di atas **$95.00\%$**. Ini menunjukkan adanya ambang batas minimum (*critical mass*) representasi memori untuk menjaga keutuhan pengetahuan lama.

---

## 4. Variasi Soal Kuis Praktikum / Responsi Lab

### Variasi Soal A: Skenario Tiga Tugas Beruntun (A -> B -> C)
* **Tugas**: Tambahkan Tugas C (misal: Deteksi Keasaman Tanah pH < 5.5). Uji apakah agen mampu mempertahankan ketiga tugas secara simultan atau apakah penyangga memori membutuhkan mekanisme prioritas (*Prioritized Experience Replay*).

### Variasi Soal B: Perhitungan Metrik Chollet
* **Tugas**: Berikan data numerik performa dan jumlah sampel dari dua arsitektur berbeda. Minta mahasiswa menghitung skor $\Upsilon$ dan menyimpulkan model mana yang memiliki efisiensi konseptual tertinggi.

---

## 5. Rubrik Penilaian Praktikum Lab (Skala 100)

| Aspek Penilaian | Bobot | Deskriptor Kinerja Unggul (Nilai Maksimal) |
| :--- | :---: | :--- |
| **Penguasaan Konsep Klasifikasi ANI-AGI-ASI** | 20% | Mampu membedakan batas kapabilitas Broad ANI vs AGI serta menguraikan risiko Alignment Problem. |
| **Implementasi Kode Continual Learning** | 35% | Kode Python berfungsi sempurna, mekanisme memory buffer rapi, dan type-hints lengkap. |
| **Analisis Lupa Katastrofik & Stabilitas** | 25% | Mampu menjelaskan kurva penurunan akurasi pada ANI dan korelasi ukuran memori terhadap retensi. |
| **Kedisiplinan Dokumentasi Kode (PEP 8)** | 20% | Setiap baris logika yang ditambahkan diberi komentar instruksional yang jelas dan runut. |
