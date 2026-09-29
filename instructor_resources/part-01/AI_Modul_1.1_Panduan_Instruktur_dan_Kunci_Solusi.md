# PANDUAN INSTRUKTUR & KUNCI SOLUSI
## AI Modul 1.1: Konsep Dasar Artificial Intelligence

> **Dokumen Rahasia Pengajar (Dosen & Asisten Laboratorium)**  
> **Modul Terkait:** [AI_Modul_1.1_Konsep_Dasar_Artificial_Intelligence.md](../../docs/part-01/AI_Modul_1.1_Konsep_Dasar_Artificial_Intelligence.md)  
> **Notebook Praktikum:** [AI_Modul_1.1_Praktikum_Konsep_Dasar_AI.ipynb](../../notebooks/part-01/AI_Modul_1.1_Praktikum_Konsep_Dasar_AI.ipynb)

---

## 1. Panduan Pedagogi & Fasilitasi Praktikum

### 1.1. Fokus Pembelajaran & Miskonsepsi Umum Mahasiswa
Saat mendampingi mahasiswa pada modul pengantar ini, instruktur perlu mewaspadai beberapa miskonsepsi tipikal:
1. **Miskonsepsi Rasionalitas vs Kemahatahuan (*Omniscience*)**: Mahasiswa sering mengira agen AI yang rasional harus selalu benar 100%. Tekankan bahwa rasionalitas diukur dari *keputusan terbaik berdasarkan informasi yang tersedia saat itu*, bukan kesempurnaan hasil akhir di masa depan yang belum diketahui (*hindsight*).
2. **Kecenderungan Terpaku pada Bias Berbasis Aturan (*Rule-Based Bias*)**: Mahasiswa cenderung ingin menulis puluhan baris percabangan `if-else` bertingkat yang kaku. Ajak mahasiswa melihat bahwa agen cerdas sejati memisahkan antara **persepsi**, **kondisi internal (model)**, dan **fungsi utilitas**.

### 1.2. Alokasi Waktu Sesi (Total 100 Menit Lab)
* **Menit 00–20**: Pemaparan konsep agen cerdas, PEAS, dan biomimikri sensorik-motorik.
* **Menit 20–45**: Live walkthrough notebook Bagian 1 s.d. Bagian 4 (menjalankan simulasi komparasi 3 agen).
* **Menit 45–80**: Mahasiswa mengerjakan *Coding Challenge (SmartCapacityAgent)* secara mandiri.
* **Menit 80–100**: Diskusi kelas, pembahasan pertanyaan analitis HOTS, dan refleksi hasil.

---

## 2. Kunci Jawaban Pertanyaan Analitis (HOTS)

### Pertanyaan 1: Rasionalitas vs Kemahatahuan
* **Pertanyaan**: *Apakah agen yang rasional selalu merupakan agen yang mahatahu (omniscient) dan tidak pernah melakukan kesalahan?*
* **Kunci Jawaban**:
  * **Tidak**. Agen yang rasional **tidak sama** dengan agen yang mahatahu (*omniscient*).
  * Kemahatahuan menuntut pengetahuan mutlak atas hasil aktual dari suatu tindakan sebelum tindakan itu terjadi (sesuatu yang mustahil di alam nyata yang stokastik).
  * Rasionalitas hanya menuntut agen memaksimalkan *ekspektasi performa* berdasarkan riwayat persepsi ($\mathcal{P}^*$) dan basis pengetahuan yang dimilikinya saat itu.
  * **Contoh Kasus Pertanian**: Jika agen mendeteksi kelembaban 85% dan memprediksi tidak butuh siraman, namun 10 menit kemudian terjadi badai panas anomali yang mengeringkan kebun, keputusan agen sebelum badai tetap **rasional** meskipun hasilnya suboptimal karena anomali cuaca tersebut berada di luar ranah persepsi sensor saat keputusan dibuat.

### Pertanyaan 2: Keterbatasan Simple Reflex Agent
* **Pertanyaan**: *Mengapa agen refleks sederhana mudah terjebak dalam infinite loop pada lingkungan partially observable?*
* **Kunci Jawaban**:
  * Karena aturan keputusan agen refleks murni memetakan $p_t \to a$ tanpa mempertimbangkan masa lalu. Jika sensor tidak dapat membedakan dua keadaan dunia yang berbeda (misalnya: petak A saat baru dibersihkan vs petak A yang memang sudah bersih dari awal), agen akan mengulangi aksi yang sama berulang kali.
  * **Solusi Struktural**: Menambahkan memori keadaan internal (*internal state / model-based reflex*) yang merekonstruksi aspek dunia yang tidak teramati saat ini berdasarkan deret persepsi masa lalu.

### Pertanyaan 3: Argumen Kamar Cina (*Chinese Room*) vs LLM Modern
* **Pertanyaan**: *Bagaimana pandangan John Searle mempengaruhi evaluasi Large Language Model (LLM) saat ini?*
* **Kunci Jawaban**:
  * Searle mendemonstrasikan bahwa pemrosesan sintaksis murni (mencocokkan token kata berdasarkan probabilitas statistik/aturan) tidak secara otomatis menghasilkan pemahaman semantik sejati (*intentionality / understanding*).
  * LLM modern (seperti GPT-4 atau Gemini) bekerja melalui prediksi token probabilitas tingkat tinggi. Secara fungsional, LLM sangat cerdas menyelesaikan tugas (*Weak AI yang sangat kapabel*), namun secara hakikat, model tersebut tidak memiliki kesadaran eksistensial mengenai makna dunia yang ia deskripsikan.

### Pertanyaan 4: Sinergi Big Data dan AI
* **Pertanyaan**: *Mengapa pengumpulan data sensor skala terabyte sia-sia tanpa AI? Kaitkan dengan Cognitive Overload.*
* **Kunci Jawaban**:
  * Manusia memiliki keterbatasan pita lebar kognitif (*bounded cognitive bandwidth*), di mana konsentrasi visual menurun drastis setelah 20 menit mengawasi data berulang.
  * Data terabyte yang tersimpan di server hanya menjadi "kuburan data" (*dark data*) jika tidak ada algoritma yang melakukan reduksi dimensi, pemfilteran noise (*veracity*), dan inferensi waktu nyata (*velocity*) untuk mengubah tumpukan angka mentah menjadi perintah intervensi fisik yang bernilai (*value*).

---

## 3. Kunci Kode Solusi Ideal: `SmartCapacityAgent`

Berikut adalah implementasi solusi optimal yang efisien energi dan aman dari penalti kehabisan bahan kimia:

```python
class SmartCapacityAgent:
    """Implementasi Solusi Ideal Agen Sadar Sumber Daya (Resource-Aware Agent)."""
    
    def __init__(self, max_capacity: int = 3):
        self.max_capacity: int = max_capacity
        self.tank_capacity: int = max_capacity
        self.internal_model: Dict[str, str] = {'A': 'UNKNOWN', 'B': 'UNKNOWN'}
        
    def act(self, percept: Tuple[str, str]) -> str:
        location, status = percept
        self.internal_model[location] = status
        
        # 1. ATURAN KRITIS PENGISIAN ULANG:
        # Jika kapasitas tangki kosong (0), agen WAJIB memprioritaskan isi ulang
        if self.tank_capacity == 0:
            if location == 'A':
                # Sedang di markas (A), lakukan isi ulang penuh
                self.tank_capacity = self.max_capacity
                return 'ISI_ULANG'
            else:
                # Sedang di petak B, segera pulang ke A (KIRI)
                return 'KIRI'
                
        # 2. ATURAN INTERVENSI HAMA:
        # Hanya semprot jika ada hama DAN tangki masih berisi (> 0)
        if status == 'TERSERANG_HAMA' and self.tank_capacity > 0:
            self.tank_capacity -= 1
            return 'SEMPROT'
            
        # 3. ATURAN NAVIGASI EFISIENSI:
        # Jika petak ini bersih, periksa petak sebelah
        other_loc = 'B' if location == 'A' else 'A'
        
        # Jika petak sebelah belum bersih, pindah ke sana
        if self.internal_model[other_loc] != 'BERSIH':
            return 'KANAN' if location == 'A' else 'KIRI'
            
        # 4. KELENGKAPAN RASIONALITAS:
        # Jika semua petak sudah bersih, dan tangki tidak penuh, tapi kebun aman: DIAM untuk hemat energi
        return 'DIAM'
```

### Analisis Kompleksitas & Performa:
* **Kompleksitas Waktu (*Time Complexity*)**: $\mathcal{O}(1)$ per langkah waktu karena evaluasi kondisi hanya melibatkan pemetaan kamus berukuran konstan ($N=2$).
* **Kompleksitas Ruang (*Space Complexity*)**: $\mathcal{O}(1)$ memori untuk menyimpan model keadaan dua petak.
* **Performa Penalti**: Menghasilkan **$0\%$ insiden penalti macet** (tidak pernah ada penalti fatal `-10`).

---

## 4. Variasi Soal Ujian Kuis Praktikum / Evaluasi Lab Alternatif

Jika instruktur ingin memberikan soal berbeda untuk sesi kelas paralel atau kuis responsi:

### Variasi Soal A: Batasan Energi Baterai (*Battery-Drain Constraint*)
* **Deskripsi**: Agen memiliki baterai awal `100%`. Setiap pergerakan (`KANAN`/`KIRI`) menghabiskan `5%`, aksi `SEMPROT` menghabiskan `10%`. Jika baterai $\le 15\%$, agen harus kembali ke Petak A untuk `'CHARGE'`. Jika baterai mencapai $0\%$, agen mogok di tengah kebun dan simulasi berhenti dengan penalti **-50 poin**.
* **Tantangan Mahasiswa**: Merancang kalkulasi estimasi jarak pulang agar tidak pernah kehabisan baterai di petak B.

### Variasi Soal B: Keberadaan Rintangan Dinamis (*Dynamic Obstacle*)
* **Deskripsi**: Ditambahkan petak C sehingga ada petak `A - B - C`. Petak B sewaktu-waktu bisa mengalami longsor/terhalang pagar (`TERHALANG`). Jika agen memaksakan diri menabrak petak terhalang, ia mendapat penalti **-15 poin**.
* **Tantangan Mahasiswa**: Agen harus mengingat status rintangan dan berdiam diri atau memilih rute aman.

---

## 5. Rubrik Penilaian Praktikum Lab (Skala 100)

| Aspek Penilaian | Bobot | Deskriptor Kinerja Unggul (Nilai Maksimal) |
| :--- | :---: | :--- |
| **Penerapan Konsep PEAS** | 20% | Mahasiswa mampu merinci metrik performa, lingkungan, aktuator, dan sensor secara saintifik tanpa kerancuan. |
| **Kualitas Logika Pemrograman** | 40% | Kode Python terstruktur rapi, menerapkan type-hints, dan tidak pernah memicu penalti fatal aktuator pada 100 siklus waktu. |
| **Analisis Grafik & Statistik** | 25% | Mahasiswa mampu menjelaskan perbedaan gradien kemiringan kurva skor antar-agen dengan menghubungkannya pada teori efisiensi fungsi utilitas $\mathcal{U}$. |
| **Kedisiplinan Dokumentasi Kode** | 15% | Setiap baris logika yang ditambahkan diberi komentar instruksional yang jelas sesuai kaidah PEP 8. |
