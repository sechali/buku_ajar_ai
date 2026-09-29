# AI Modul 11.5: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-11-05
* **Topik Utama**: Deteksi Kontur Suzuki-Abe, Momen Spasial, dan Analisis Bentuk
* **Alokasi Waktu**: 150 Menit (50 Menit Teori Topologi Kontur, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 11.5, Jupyter Notebook Praktikum, Proyektor, Python 3.10 + OpenCV.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Konsep topologi kontur vektor, algoritma Suzuki-Abe, dan struktur hierarki kontur pohon.
* **Menit 25 - 50**: Matematika momen spasial $m_{pq}$, penentuan koordinat centroid $(C_x, C_y)$, serta formulasi kebulatan dan soliditas.
* **Menit 50 - 120**: Praktikum komputer: pembuatan citra sintetis sensus pohon sawit, penapisan derau luas area, dan visualisasi bounding box.
* **Menit 120 - 150**: Asesmen formatif dan diskusi pemanfaatan kontur untuk penghitungan populasi pohon sawit skala ribuan hektar.

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Teori Topologi** | Menjelaskan relasi hierarki kontur dan momen spasial centroid secara matematis tanpa galat. | Memahami fungsi `findContours` namun kurang memahami struktur relasi hierarki. | Menganggap kontur sama persis dengan deteksi tepi Canny. |
| **Implementasi Morfometri** | Menulis skrip ekstraksi momen, bounding box, dan rasio kebulatan secara terstruktur dan efisien. | Mampu mengekstrak kontur namun lupa menangani potensi pembagian nol pada momen. | Terjadi galat runtime saat mengekstrak koordinat pusat massa. |
| **Penyaringan Derau & Sensus** | Mengonfigurasi ambang batas luas minimum dan mengklasifikasikan tajuk sehat vs rusak dengan tepat. | Mampu menyaring kontur namun kriteria ambang batas kebulatan belum optimal. | Gagal memisahkan objek pohon dari derau semak mikro. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Kalkulasi Rasio Kebulatan
Rumus rasio kebulatan: $C = \frac{4\pi A}{P^2}$ (dengan $\pi \approx 3.14159$).
1. **Tajuk Pohon A**:
   $$C_1 = \frac{4 \times 3.14159 \times 15400}{450^2} = \frac{193521.95}{202500} \approx 0.956$$
2. **Tajuk Pohon B**:
   $$C_2 = \frac{4 \times 3.14159 \times 12000}{620^2} = \frac{150796.32}{384400} \approx 0.392$$
3. **Analisis Diagnostik Agronomis**:
   Pohon A memiliki nilai $C_1 = 0.956$ (sangat mendekati 1.0), menunjukkan geometri tajuk yang melingkar sempurna dan simetris, mencerminkan pelepah sawit yang utuh, rimbun, dan sehat.
   Sebaliknya, Pohon B memiliki nilai $C_2 = 0.392$ (sangat rendah). Nilai kelilingnya membengkak menjadi $620$ piksel meskipun luasnya lebih kecil ($12.000$ vs $15.400$), mengindikasikan batas tepi tajuk yang sangat berlekuk-lekuk dan tidak teratur. Fenomena ini adalah ciri khas tajuk kelapa sawit yang pelepahnya dimakan oleh hama ulat api (*Setothosea asigna*) atau ulat kantung (*Metisa plana*), sehingga Pohon B harus diprioritaskan untuk tindakan pengendalian hama terpadu.

### Jawaban Soal Konseptual 2: Analisis Hierarki Kontur Pohon
Pada `cv2.RETR_TREE`, relasi kontur diorganisasi dalam pohon hierarki 4 elemen `[Next, Previous, First_Child, Parent]`:
* **Kontur Kulit Luar Buah**: Berada pada tingkat tertinggi (Level 0, akar pohon). Tidak memiliki Parent (`Parent = -1`). Memiliki anak pertama yaitu tempurung cangkang (`First_Child = ID_Tempurung`).
* **Kontur Tempurung Cangkang**: Berada pada Level 1. Memiliki `Parent = ID_Kulit_Luar` dan memiliki anak pertama yaitu inti kernel (`First_Child = ID_Kernel`).
* **Kontur Inti Kernel**: Berada pada Level 2 (daun terdalam). Memiliki `Parent = ID_Tempurung` dan tidak memiliki anak (`First_Child = -1`).
Struktur hierarki bersarang ini memungkinkan algoritma mengukur ketebalan daging buah (*mesocarp*) secara otomatis dengan menghitung selisih luas kontur Level 0 dan Level 1.
