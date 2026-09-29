# Panduan Instruktur & Kunci Solusi: AI Modul 1.5

**Kode Modul:** AI Modul 1.5  
**Mata Kuliah:** Kecerdasan Buatan (Artificial Intelligence)  
**Judul Modul:** Contoh Penerapan Artificial Intelligence di Berbagai Bidang  
**Target Pengajar:** Dosen Pengampu, Asisten Praktikum, Pengajar Laboratorium AI  

---

## 1. Panduan Pedagogis & Strategi Pengajaran (Pedagogical Blueprint)

Modul 1.5 merupakan jembatan transisi krusial dari ranah konseptual fundamental menuju aplikasi rekayasa nyata di dunia industri. Banyak mahasiswa sering terjebak dalam pemikiran bahwa model AI terbaik adalah model dengan akurasi persentase tertinggi (misal 99%). Tugas instruktur adalah membongkar miskonsepsi ini.

### 1.1. Konsep Kunci yang Wajib Ditekankan
1. **Trade-off Akurasi vs Latensi**: Tunjukkan grafik `tradeoff_akurasi_latensi_sektor.png`. Tekankan bahwa sistem kamera pengawas otonom atau drone kebun tidak memiliki kemewahan komputasi server cloud. Latensi inferensi 30 ms dengan akurasi 92% di edge device jauh lebih berguna daripada model raksasa 99% yang membutuhkan waktu 5 detik untuk merespons melalui internet.
2. **Kesesuaian Masalah (*Problem-Fit Framing*)**: Jangan pernah menggunakan *Deep Learning* jika *Logistic Regression* atau *Isolation Forest* sederhana sudah mampu menyelesaikan masalah dengan biaya komputasi $\frac{1}{1000}$-nya.
3. **Konsekuensi Asimetris Kesalahan (*False Positive vs False Negative*)**: Gunakan analogi pabrik sawit dan tumor medis untuk menjelaskan mengapa nilai $\beta$ pada $F_\beta\text{-score}$ ditentukan oleh *kerugian ekonomi dan keselamatan jiwa*, bukan semata-mata preferensi matematis.

### 1.2. Miskonsepsi Umum Mahasiswa (*Common Student Pitfalls*)
* **Miskonsepsi**: "Model yang baik harus memiliki Precision dan Recall yang sama tingginya ($F_1$). Datanya pasti jelek jika precision rendah."  
  *Koreksi Pengajar*: Pada kasus *Predictive Maintenance*, alarm palsu (*False Positive*) hanya memerlukan teknisi meluangkan waktu 5 menit untuk mengecek baut turbin. Namun jika terjadi kebocoran kerusakan (*False Negative*), turbin seharga miliaran rupiah bisa meledak dan memicu korban jiwa. Oleh karena itu, kita sengaja menoleransi precision rendah demi memaksimumkan recall ($F_2$ atau $F_3$).
* **Miskonsepsi**: "Jika tidak pakai GPU, itu bukan AI."  
  *Koreksi Pengajar*: Tunjukkan bahwa pada perangkat edge perkebunan (seperti stasiun cuaca IoT mikro), model machine learning tabular berbasis CPU mini dapat bertahan hidup berbulan-bulan hanya dengan tenaga baterai surya kecil.

---

## 2. Kunci Jawaban Lengkap Pertanyaan HOTS

### Pertanyaan 1: Analisis Kompromi Edge vs Cloud pada Pertanian Presisi
* **Pertanyaan**: Mengevaluasi Opsi A (Cloud via Starlink, Akurasi 98%, jeda waktu 6 jam) vs Opsi B (Edge AI On-Board Jetson Nano, Akurasi 91%, latensi 30 ms, penyemprotan langsung di udara).
* **Kunci Jawaban & Rubrik Penilaian**:
  * **Pilihan Terbaik**: **Opsi B (Edge AI On-Board)**.
  * **Alasan Analitis**:
    1. *Kecepatan Penanganan Hama*: Serangan ulat api pada tanaman kelapa sawit menyebar secara geometris dalam hitungan jam. Opsi B memungkinkan tindakan kuratif instan (*real-time spraying*) pada saat drone berada tepat di atas tajuk pohon yang terinfeksi.
    2. *Biaya Operasional*: Opsi A membutuhkan penerbangan drone ulang untuk penyemprotan (dua kali kerja: memotret lalu menyemprot), menghabiskan dua kali lipat bahan bakar baterai drone dan biaya transmisi data satelit Starlink.
    3. *Toleransi Kesalahan*: Akurasi 91% sudah sangat cukup di lapangan. Kesalahan klasifikasi sebesar 9% hanya berakibat sedikit kelebihan pestisida lokal, yang jauh lebih kecil biayanya dibandingkan keterlambatan penanganan 6 jam yang berisiko menularkan hama ke 1 blok perkebunan (30 hektar).

### Pertanyaan 2: Dilema Etika dan Finansial dalam Radiologi Medis vs Fraud Finansial
* **Pertanyaan**: Mengapa radiologi tumor otak menetapkan $\beta = 3$, sedangkan rekomendasi produk atau filter iklan menetapkan $\beta = 0.5$?
* **Kunci Jawaban**:
  * **Radiologi Tumor Otak ($\beta = 3$)**: Recall diprioritaskan 3 kali lebih penting ($9 \times$ pada pembobotan kuadrat $\beta^2$). Kegagalan mendeteksi tumor ($FN$) berujung pada kematian pasien karena kanker terlambat ditangani. Sebaliknya, alarm palsu ($FP$) hanya berakibat pemeriksaan biopsi lanjutan yang mungkin mencemaskan namun menyelamatkan nyawa.
  * **Rekomendasi Produk / Filter Promosi ($\beta = 0.5$)**: Presisi diprioritaskan lebih tinggi. Jika sistem salah menandai pesan penting kerja sebagai spam ($FP$), pengguna akan kehilangan peluang bisnis atau informasi krusial. Namun jika 1 email spam lolos ke inbox ($FN$), pengguna hanya perlu menekan tombol *delete* secara mudah tanpa konsekuensi fatal.

---

## 3. Solusi Lengkap Tantangan Praktik (Hands-On Challenges)

### Solusi Tingkat 1: Perhitungan $F_{0.5}\text{-Score}$ pada Sortasi Sawit
```python
# Menghitung F0.5-score pada sortasi sawit
# Formula: (1 + 0.25) * (Prec * Rec) / (0.25 * Prec + Rec)
f05_sawit = fbeta_score(y_sawit, y_pred_sawit, beta=0.5)
print(f"F0.5-Score (Presisi diutamakan): {f05_sawit * 100:.2f}%")
```
*Interpretasi*: Ketika biaya memproses buah mentah meningkat tajam karena merusak mesin peremuk (*digester*), manajemen pabrik menuntut seleksi yang lebih ketat. Nilai $F_{0.5}$ memberikan bobot lebih berat pada *Precision*, memastikan buah yang masuk ke lini pengolahan benar-benar murni matang.

### Solusi Tingkat 2: Perbandingan Utilitas Multi-Objektif
```python
def hitung_utilitas(acc, lat, cost, w_acc=0.5, w_lat=0.3, w_cost=0.2, l_max=100.0, c_max=10.0):
    return (w_acc * acc) - (w_lat * (lat / l_max)) - (w_cost * (cost / c_max))

u_edge = hitung_utilitas(0.92, 15.0, 0.50)
u_cloud = hitung_utilitas(0.97, 85.0, 8.00)

print(f"Utilitas Edge AI : {u_edge:.4f}")   # 0.460 - 0.045 - 0.010 = 0.4050
print(f"Utilitas Cloud AI: {u_cloud:.4f}")  # 0.485 - 0.255 - 0.160 = 0.0700

# Keputusan: Model Edge AI menghasilkan utilitas 0.4050, jauh melampaui Cloud AI (0.0700)
# karena penalti latensi dan biaya server cloud sangat mendegradasi kelayakan bisnis.
```

### Solusi Tingkat 3: Monitoring Real-Time Kelas `SmartFactoryMonitor`
```python
from collections import deque
import json
import time

class SmartFactoryMonitor:
    def __init__(self, mesin_id="TURBIN-PKS-01", window_size=5, ambang_batas=4.5):
        self.mesin_id = mesin_id
        self.window_size = window_size
        self.ambang_batas = ambang_batas
        self.buffer = deque(maxlen=window_size)

    def stream_vibrasi(self, nilai_vibrasi_saat_ini):
        self.buffer.append(nilai_vibrasi_saat_ini)
        rata_rata = sum(self.buffer) / len(self.buffer)
        
        # Peringatan hanya dibunyikan jika buffer sudah penuh dan melampaui ambang batas
        if len(self.buffer) == self.window_size and rata_rata > self.ambang_batas:
            alert = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "mesin_id": self.mesin_id,
                "status": "CRITICAL_ALERT",
                "rata_rata_getaran": round(rata_rata, 2),
                "tindakan_rekomendasi": "Lakukan shutdown darurat dan periksa keausan bearing turbin."
            }
            return json.dumps(alert, indent=2)
        return "STATUS: NORMAL"

# Contoh Eksekusi Uji Coba:
monitor = SmartFactoryMonitor()
for v in [2.4, 2.6, 2.5, 5.2, 5.8, 6.1, 6.4, 6.0]:
    hasil = monitor.stream_vibrasi(v)
    if "CRITICAL_ALERT" in hasil:
        print("[ALARM TRIGGERED]")
        print(hasil)
        break
```

---

## 4. Rubrik Asesmen Praktikum

| Kriteria Penilaian | Bobot (%) | Kinerja Kurang (0-59) | Kinerja Cukup (60-79) | Kinerja Sangat Baik (80-100) |
| :--- | :---: | :--- | :--- | :--- |
| **Ketepatan Formulasi F-Beta & Utilitas** | 30% | Salah menerapkan rumus $F_\beta$ atau tidak memahami fungsi utilitas sistem. | Mampu menghitung rumus matematis namun kurang tepat dalam interpretasi bisnis. | Mampu menghitung rumus dengan tepat serta memberikan interpretasi domain yang mendalam. |
| **Kualitas Implementasi Kode** | 35% | Kode mengandung error eksekusi atau tidak memiliki komentar penjelas. | Kode berjalan dengan baik namun komentar kurang informatif atau minim adaptasi. | Kode berjalan 100% bebas error, terstruktur rapi, dan dilengkapi dokumentasi baris per baris. |
| **Analisis Jawaban HOTS** | 25% | Menjawab tanpa argumentasi logis atau hanya mengandalkan hafalan teks. | Mampu memilih opsi yang benar namun justifikasi teknis dan biayanya dangkal. | Memberikan analisis multi-dimensi (latensi, biaya, risiko, dampak tanaman/mesin) yang sangat tajam. |
| **Tantangan Berscaffolding** | 10% | Tidak mencoba atau hanya menyelesaikan Tantangan Tingkat 1. | Mampu menyelesaikan Tantangan Tingkat 1 dan Tingkat 2 dengan benar. | Menyelesaikan seluruh tantangan hingga perancangan kelas OOP *streaming* (Tingkat 3). |
