# AI Modul 9.9: Panduan Instruktur dan Kunci Solusi

---

## 1. Rencana Pelaksanaan Pembelajaran (RPP)

* **Kode Modul**: AI-09-09
* **Topik Utama**: Framework Deep Learning (PyTorch & TensorFlow)
* **Alokasi Waktu**: 150 Menit (50 Menit Kuliah Teori Arsitektur Framework, 70 Menit Praktikum Terbimbing, 30 Menit Evaluasi)
* **Bahan Ajar & Alat**: Slide Perkuliahan, Diktat Teori Modul 9.9, Jupyter Notebook Praktikum, Proyektor, Komputer Praktikum dengan PyTorch 2.x terpasang.

### 1.1 Garis Waktu Instruksional
* **Menit 00 - 25**: Arsitektur software deep learning: Autograd DAG, perbandingan imperatif PyTorch vs deklaratif TensorFlow, dan akselerasi GPU CUDA.
* **Menit 25 - 50**: Bedah anatomi kode PyTorch: subclassing `nn.Module`, konstruksi pipeline `Dataset` dan `DataLoader`, serta 5 langkah kanonik training loop.
* **Menit 50 - 120**: Praktikum hands-on: membangun model klasifikasi varietas bibit sawit, melatih model, evaluasi dengan `torch.no_grad()`, dan mengekspor model ke ONNX.
* **Menit 120 - 150**: Pembahasan kesalahan umum (lupa `zero_grad`, memory leak akumulasi tensor), ulasan transisi ke Computer Vision (Part 10).

---

## 2. Rubrik Asesmen & Evaluasi Kinerja Mahasiswa

| Kriteria Penilaian | Skor Sangat Memuaskan (85 - 100) | Skor Cukup (70 - 84) | Skor Perlu Perbaikan (< 70) |
| :--- | :--- | :--- | :--- |
| **Pemahaman Arsitektur PyTorch** | Mampu menguraikan peran Autograd, DAG, dan siklus kanonik training loop secara tepat tanpa kesalahan konsep. | Memahami langkah training loop dasar namun kurang memahami mekanisme kerja Autograd di belakang layar. | Mengabaikan langkah penting seperti pembersihan gradien atau mode evaluasi. |
| **Implementasi Kode PyTorch** | Menulis kelas `nn.Module`, pipeline `DataLoader`, dan training loop kustom yang bersih dan bebas galat. | Mampu menjalankan praktikum namun kesulitan saat mengonfigurasi dimensi lapisan atau tipe data tensor. | Terjadi galat ketidakcocokan perangkat (`CPU vs GPU mismatch`) tanpa tahu cara memperbaikinya. |
| **Ekspor & Evaluasi Model** | Berhasil melakukan evaluasi menggunakan `torch.no_grad()` dan mengekspor model ke format ONNX secara mandiri. | Mampu mengeksekusi evaluasi namun tidak memahami format pertukaran model terbuka seperti ONNX. | Lupa mengubah mode model ke `eval()` saat melakukan pengujian pada data uji. |

---

## 3. Kunci Jawaban Soal Latihan & Evaluasi Mandiri

### Jawaban Soal Konseptual 1: Graf Dinamis vs Statis
Pada graf statis (TensorFlow 1.x), struktur jaringan didefinisikan terlebih dahulu secara deklaratif sebagai cetak biru simbolik, lalu dikompilasi dan dieksekusi di dalam sesi (`tf.Session()`). Kelemahannya adalah kaku dan sulit didebug karena variabel Python biasa tidak dapat diinspeksi secara langsung di tengah eksekusi graf.
Sebaliknya, pada graf dinamis (PyTorch), graf komputasi dibangun secara instan (*on-the-fly*) pada saat baris kode dieksekusi (*define-by-run*). Setiap iterasi dapat memiliki struktur graf yang berbeda. Hal ini sangat menguntungkan untuk data perkebunan yang memiliki panjang deret waktu bervariasi (*variable-length time-series*) atau citra dengan dimensi tidak seragam, karena struktur loop dan percabangan kondisi Python asli (`if/else`, `for`) dapat langsung mengendalikan aliran tensor tanpa perlu operator kontrol simbolik yang rumit.

### Jawaban Soal Konseptual 2: Analisis Kebocoran Memori
Pernyataan `epoch_loss += loss` menahan objek tensor PyTorch `loss` ke dalam variabel skalar Python. Karena tensor `loss` terhubung ke seluruh graf komputasi Autograd (melalui atribut `grad_fn`), variabel `epoch_loss` secara tidak sengaja mempertahankan seluruh riwayat komputasi graf dari seluruh batch di dalam memori VRAM GPU. Seiring bertambahnya batch dan epoch, alokasi memori membengkak secara eksponensial hingga memicu galat `CUDA out of memory` (OOM).
Solusi yang benar adalah mengekstrak nilai float numerik mentah dari tensor skalar menggunakan method `.item()`:
```python
epoch_loss += loss.item() * batch_x.size(0)
```
Dengan memanggil `.item()`, hanya nilai skalar Python murni yang diakumulasikan, sehingga graf komputasi Autograd untuk batch tersebut dapat langsung dihapus dari memori GPU oleh garbage collector.
