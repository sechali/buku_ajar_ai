# Panduan Instruktur & Kunci Solusi: AI Modul 13.3 - Pengembangan Aplikasi Sederhana

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Pola arsitektur Model-View-Controller (MVC) dalam aplikasi visi komputer dan pencegahan UI freezing.
* **Menit 35 - 65**: Protokol streaming video HTTP Multipart MJPEG dan perbedaan mendasar terhadap WebRTC.
* **Menit 65 - 100**: Praktikum komputer: Pembangunan server streaming MJPEG asinkron, manipulasi byte buffer, dan penanganan generator.
* **Menit 100 - 130**: Studi kasus dasbor kendali sentral mutu TBS dan peringatan asam lemak bebas (FFA) di pabrik kelapa sawit.
* **Menit 130 - 150**: Pembahasan potensi kendala teknis network choking, zombie client disconnection, dan kuis evaluasi.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (WebRTC vs MJPEG)
* **MJPEG (Motion JPEG)**:
  * Sangat sederhana diimplementasikan (hanya mengirimkan runtunan frame JPEG via HTTP standar).
  * Kompatibel secara bawaan di semua peramban web tanpa pustaka JavaScript pihak ketiga.
  * Kelemahan: Tidak memiliki kompresi temporal antar-frame (*inter-frame compression*), sehingga memakan bandwidth jaringan yang jauh lebih besar ($5 - 10\times$ lebih boros dibanding codec video modern).
* **WebRTC**:
  * Menggunakan codec kompresi video tingkat lanjut (H.264 / VP8 / AV1) dengan kompresi temporal mendalam.
  * Latensi sub-100 milidetik via UDP stream.
  * Kelemahan: Arsitektur sangat kompleks (membutuhkan pertukaran sinyal SDP, server STUN/TURN, dan penanganan koneksi peer-to-peer).

### Solusi Soal Mandiri 2 (Endpoint Streaming FastAPI)
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import time

app = FastAPI()

def frame_generator():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.033)
    cap.release()

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(frame_generator(), 
                             media_type="multipart/x-mixed-replace; boundary=frame")
```

---

## 3. Rubrik Penilaian Praktikum
* **Perancangan Mesin Streaming Asinkron (35%)**: Generator HTTP multipart berjalan stabil dan bebas kebocoran memori.
* **Pemisahan Utas Thread-Safe (30%)**: Akses frame buffer terisolasi rapi menggunakan mutex lock.
* **Kerapian Antarmuka & Telemetri OSD (20%)**: Dasbor menyajikan informasi operasional yang jelas, terbaca, dan proporsional.
* **Kualitas Kode & Standar Rekayasa (15%)**: Kode modular, bebas galat sintaks, dan terdokumentasi dengan baik.
