# Panduan Instruktur & Kunci Solusi: AI Modul 13.1 - Integrasi Model dengan Kamera

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 30**: Penjelasan fenomena Buffer Lag Accumulation pada pemrosesan sekuensial utas tunggal.
* **Menit 30 - 65**: Arsitektur Producer-Consumer dengan atomic pointer dan sinkronisasi mutex thread-safe.
* **Menit 65 - 100**: Praktikum komputer: Pembangunan modul `SyntheticCameraThread`, integrasi tensor PyTorch `torch.no_grad()`, dan perancangan OSD.
* **Menit 100 - 130**: Studi kasus pemilahan buah sawit pada konveyor berkecepatan 0.8 m/s dan analisis sinkronisasi pneumatik.
* **Menit 130 - 150**: Pembahasan potensi kendala race condition dan strategi pemulihan otomatis koneksi kamera terputus.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Kapasitas Buffer FIFO vs Buffer-1)
* **Antrean FIFO Tak Terbatas (`queue.Queue()`)**:
  * Menjamin tidak ada frame yang hilang (*zero frame drop*).
  * Namun, jika laju inferensi lebih lambat daripada laju kamera, antrean akan membengkak. Model akan memproses rekaman masa lalu yang tertinggal bermenit-menit, merusak fungsi waktu-nyata (*fatal latency lag*).
* **Antrean Kapasitas Satu (`maxsize=1`)**:
  * Secara sengaja menjatuhkan frame yang terlewat (*deliberate frame skipping*).
  * Menjamin konsumen selalu mendapatkan citra terbaru di lapangan, mempertahankan latensi nol mutlak untuk aksi aktuasi instan.

### Solusi Soal Mandiri 2 (Modul Watchdog Kamera)
```python
import time
import threading

class CameraWatchdog(threading.Thread):
    def __init__(self, stream_obj, timeout=2.0):
        super().__init__(daemon=True)
        self.stream = stream_obj
        self.timeout = timeout
        self.last_seen_time = time.time()
        self.running = True
        
    def ping(self):
        self.last_seen_time = time.time()
        
    def run(self):
        while self.running:
            time.sleep(0.5)
            if time.time() - self.last_seen_time > self.timeout:
                print("[WATCHDOG ALERT] Kamera membeku! Memicu inisialisasi ulang...")
                self.stream.stop()
                time.sleep(0.5)
                self.stream.start()
                self.last_seen_time = time.time()
```

---

## 3. Rubrik Penilaian Praktikum
* **Penguasaan Multi-Threading (35%)**: Implementasi pemisahan capture thread dan inference loop berjalan bebas deadlock.
* **Optimasi Latensi & Pipeline (30%)**: Berhasil mencapai throughput $\ge 25\text{ FPS}$ dengan latensi stabil.
* **Kerapian Rendering OSD (20%)**: Telemetri menampilkan teks informatif dan visualisasi yang tidak mengaburkan objek inspeksi.
* **Standar Rekayasa Perangkat Lunak (15%)**: Kode modular, penggunaan resource locking yang aman, dan terdokumentasi dengan baik.
