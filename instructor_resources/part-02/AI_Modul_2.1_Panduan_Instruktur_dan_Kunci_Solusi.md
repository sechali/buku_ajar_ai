# Panduan Instruktur & Kunci Solusi: AI Modul 2.1

**Kode Modul:** AI Modul 2.1  
**Mata Kuliah:** Kecerdasan Buatan (Artificial Intelligence)  
**Judul Modul:** Konsep Algoritma  
**Target Pengajar:** Dosen Pengampu, Asisten Praktikum, Pengajar Laboratorium Algoritma & Struktur Data  

---

## 1. Panduan Pedagogis & Strategi Pengajaran (Pedagogical Blueprint)

Modul 2.1 adalah pintu masuk menuju **Bagian 2: Dasar Algoritma dan Logika Pemrograman**. Sering kali mahasiswa yang tertarik pada kecerdasan buatan ingin langsung melompat ke library modern (*PyTorch, TensorFlow, Scikit-Learn*) tanpa memahami apa yang terjadi di balik layar komputasi CPU dan alokasi memori.

### 1.1. Konsep Kunci yang Wajib Ditekankan
1. **Perbedaan 'Waktu Stopwatch' vs 'Notasi Asimtotik'**: Jelaskan bahwa mengukur kecepatan algoritma semata-mata dengan stopwatch laptop sangat menyesatkan (karena bergantung pada spesifikasi hardware). Tunjukkan bahwa Notasi Big-O mengukur **laju pertumbuhan operasi murni matematika** yang independen dari mesin.
2. **Kekuatan Eksponensial Binary Search**: Tekankan demonstrasi numerik di mana pencarian pada 1 juta data dipangkas dari 1.000.000 langkah menjadi hanya 20 langkah! Berikan analogi menebak halaman buku tebal (buka di tengah, bukan membalik lembar per lembar dari halaman 1).
3. **Mengapa Bubble Sort Tidak Boleh Digunakan di Industri**: Tunjukkan grafik `kurva_kompleksitas_big_o.png` dan jelaskan mengapa algoritma kuadratik $\mathcal{O}(N^2)$ merupakan bencana bagi sistem AI yang memproses jutaan sensor atau citra streaming.

### 1.2. Miskonsepsi Umum Mahasiswa (*Common Student Pitfalls*)
* **Miskonsepsi**: "Komputer modern zaman sekarang prosesornya sudah sangat cepat, jadi kita tidak perlu memikirkan Big-O lagi."  
  *Koreksi Pengajar*: Tunjukkan bahwa pada algoritma eksponensial $\mathcal{O}(2^N)$, jika $N=100$, jumlah operasi melampaui jumlah atom di seluruh alam semesta! Komputer tercepat di dunia pun akan membutuhkan miliaran tahun untuk menyelesaikannya.
* **Miskonsepsi**: "Binary Search selalu lebih baik daripada Linear Search dalam segala situasi."  
  *Koreksi Pengajar*: Binary Search **hanya bisa bekerja jika data sudah terurut**. Jika data belum terurut, biaya mengurutkannya terlebih dahulu ($\mathcal{O}(N \log N)$) lebih mahal daripada sekadar 1 kali Linear Search ($\mathcal{O}(N)$).

---

## 2. Kunci Jawaban Lengkap Pertanyaan HOTS

### Pertanyaan 1: Analisis Skalabilitas Edge Drone Pertanian
* **Pertanyaan**: Mengevaluasi Algoritma A ($\mathcal{O}(N \log N)$ Waktu, $\mathcal{O}(1)$ Memori) vs Algoritma B ($\mathcal{O}(N)$ Waktu, $\mathcal{O}(N^2)$ Memori) pada modul mikroprosesor drone dengan RAM terbatas $512\text{ MB}$ untuk $N = 100.000$ vektor daun.
* **Kunci Jawaban & Analisis Memori**:
  * **Pilihan yang Berhasil Berjalan**: **Algoritma A**.
  * **Pilihan yang Mengalami Crash (OOM)**: **Algoritma B**.
  * **Perhitungan Matematis Memori**:
    * Pada Algoritma B, kompleksitas memori kuadratik $\mathcal{O}(N^2)$ membutuhkan matriks berukuran $100.000 \times 100.000 = 10^{10}$ elemen.
    * Jika setiap elemen adalah floating-point standar 4-byte (float32):
      $$\text{Kebutuhan RAM} = 10^{10} \times 4\text{ bytes} \approx 40.000.000.000\text{ bytes} \approx \mathbf{40\text{ Gigabyte (GB)}}!$$
    * Karena RAM drone hanya $512\text{ MB}$ ($0.512\text{ GB}$), Algoritma B akan seketika membunuh proses (*Kernel OOM Killer*) dan menyebabkan kegagalan sistem terbang drone.
    * Sebaliknya, Algoritma A hanya membutuhkan memori konstan $\mathcal{O}(1)$ (beberapa kilobyte), dan waktu eksekusinya $N \log_2 N \approx 100.000 \times 16.6 \approx 1.66 \times 10^6$ operasi, yang diselesaikan prosesor dalam waktu kurang dari $0.1$ detik.

### Pertanyaan 2: Dilema Rekursif vs Iteratif dalam Komputasi AI
* **Analisis Rekursi vs Iterasi**:
  * **Kelemahan Rekursi pada Edge Device**: Setiap pemanggilan fungsi rekursif mengalokasikan bingkai tumpukan (*Stack Frame*) baru di memori RAM untuk menyimpan alamat kembali (*return address*), register lokal, dan variabel. Jika pohon keputusan (*Decision Tree*) memiliki kedalaman $1.000+$ tingkatan, tumpukan memori akan terlampaui dan memicu galat kritis **`RecursionError: maximum recursion depth exceeded`** atau *Segmentation Fault (Stack Overflow)*.
  * **Keunggulan Pendekatan Iteratif**: Menggunakan perulangan `while` dengan struktur tumpukan eksplisit (*Explicit Stack Heap Allocation*) menjaga konsumsi memori tetap terkendali, deterministik, dan bebas dari batas kedalaman tumpukan pemanggilan interpreter Python.

---

## 3. Solusi Lengkap Tantangan Praktik (Hands-On Challenges)

### Solusi Tingkat 1: Skenario Terbaik (*Best-Case*) Binary Search
```python
# Mencari target yang tepat berada di indeks tengah
target_tengah = katalog_bibit[len(katalog_bibit) // 2]
posisi, langkah = binary_search(katalog_bibit, target_tengah)

print(f"Target di Tengah Array -> Ditemukan di indeks {posisi} hanya dalam {langkah} langkah!")
# Output: 1 langkah!
# Penjelasan: Pada iterasi pertama, nilai tengah langsung cocok dengan target (Best-Case = O(1)).
```

### Solusi Tingkat 2: Implementasi Insertion Sort pada Data Sensor
```python
def insertion_sort(arr_input):
    arr = list(arr_input)
    for i in range(1, len(arr)):
        kunci = arr[i]
        j = i - 1
        # Geser elemen yang lebih besar dari kunci ke kanan
        while j >= 0 and arr[j] > kunci:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = kunci
    return arr

# Menguji pada data yang hampir terurut
data_hampir_urut = [20.1, 20.4, 21.0, 21.2, 22.5, 22.0, 23.1]
print("Hasil Insertion Sort:", insertion_sort(data_hampir_urut))
# Pada data yang hampir terurut, loop 'while' jarang dieksekusi, menghasilkan performa linear O(N)!
```

### Solusi Tingkat 3: FSM Traktor Kebun Otonom (`AutonomousTractorFSM`)
```python
class AutonomousTractorFSM:
    def __init__(self, rute_panen, lokasi_halangan):
        self.rute = rute_panen # List tuple koordinat [(0,0), (0,1), ...]
        self.halangan = set(lokasi_halangan)
        self.posisi_saat_ini = (0, 0)
        self.state = "IDLE"
        self.log_perjalanan = []

    def jalankan_misi(self):
        self.state = "NAVIGATING"
        print(f"[STATUS] Misi Panen Dimulai. Traktor beralih ke state: {self.state}")
        
        for titik in self.rute:
            # Evaluasi percabangan rintangan
            if titik in self.halangan:
                self.state = "OBSTACLE_AVOIDANCE"
                print(f"  [PERINGATAN] Rintangan terdeteksi di {titik}! Beralih ke {self.state}")
                # Melakukan manuver memutar (bypass)
                titik_bypass = (titik[0] + 1, titik[1])
                print(f"  -> Manuver menghindari halangan melewati koordinat aman: {titik_bypass}")
                self.log_perjalanan.append(titik_bypass)
            
            # Kembali ke pemanenan normal
            self.state = "HARVESTING"
            self.posisi_saat_ini = titik
            self.log_perjalanan.append(titik)
            print(f"  -> Memanen di koordinat: {self.posisi_saat_ini} | State: {self.state}")
            
        self.state = "IDLE"
        print(f"[SELESAI] Seluruh blok kebun selesai dipanen. State akhir: {self.state}")

# Uji Coba:
traktor = AutonomousTractorFSM(rute_panen=[(0,0), (0,1), (0,2), (0,3)], lokasi_halangan=[(0,2)])
traktor.jalankan_misi()
```

---

## 4. Rubrik Asesmen Praktikum

| Kriteria Penilaian | Bobot (%) | Kinerja Kurang (0-59) | Kinerja Cukup (60-79) | Kinerja Sangat Baik (80-100) |
| :--- | :---: | :--- | :--- | :--- |
| **Pemahaman Teori Asimtotik Big-O** | 25% | Mengacaukan notasi Big-O dengan waktu stopwatch atau salah menghitung kompleksitas. | Mengetahui kelas kompleksitas namun belum mampu membuktikan secara matematis/numerik. | Menguasai definisi formal limit/batas atas dan mampu memprediksi laju pertumbuhan algoritma. |
| **Implementasi Struktur Kontrol & Benchmark** | 35% | Kode mengandung perulangan tak berhingga (*infinite loop*) atau salah logika seleksi. | Kode berjalan dengan baik namun pemisahan struktur kontrol kurang modular dan bersih. | Kode berjalan 100% bebas error, rapi, terdokumentasi per baris, dan membandingkan waktu mikrodetik. |
| **Analisis Kritis HOTS** | 25% | Menjawab tanpa kalkulasi kuantitatif kapasitas RAM dan batas memori fisik perangkat. | Mengetahui algoritma yang crash namun justifikasi perhitungannya tidak lengkap. | Memberikan bukti matematis detail ukuran matriks memori ($40\text{ GB}$ vs $512\text{ MB}$) dan analisis stack. |
| **Penyelesaian Tantangan Berscaffolding** | 15% | Hanya mencoba tantangan tingkat 1. | Mampu menyelesaikan tantangan tingkat 1 dan 2 dengan benar. | Menyelesaikan seluruh tantangan hingga perancangan model Finite State Machine robotik (Tingkat 3). |
