# Panduan Instruktur & Kunci Solusi: AI Modul 13.4.2 - Monitoring Berbasis CCTV

## 1. Rencana Pembelajaran & Alokasi Waktu (150 Menit)
* **Menit 00 - 35**: Arsitektur jaringan pemantauan CCTV pintar multi-RTSP pada infrastruktur industri perkebunan.
* **Menit 35 - 65**: Penjelasan matematis Algoritma Ray Casting (Even-Odd Rule) dan kalkulasi Dwell Time.
* **Menit 65 - 100**: Praktikum komputer: Pembangunan fungsi `point_in_polygon`, penjejakan waktu tinggal, dan rendering poligon transparan di OpenCV.
* **Menit 100 - 130**: Studi kasus pengawasan perimeter 24 jam dan keselamatan K3 di pabrik kelapa sawit.
* **Menit 130 - 150**: Rangkuman penutup menyeluruh seluruh buku (Part 1 s.d. Part 13) dan arahan portofolio profesional siswa.

---

## 2. Kunci Jawaban Soal Evaluasi & Mandiri

### Solusi Soal Mandiri 1 (Background Subtraction + YOLO untuk Efisiensi Daya)
* Menjalankan inferensi model deep learning YOLO berkecepatan 30 FPS secara konstan mengonsumsi daya listrik tinggi (30-60 Watt per GPU), yang sangat membebani sistem CCTV tenaga surya di perkebunan terpencil.
* **Solusi Hibrida Hemat Daya**:
  1. Algoritma ringan *Background Subtraction* (MOG2) dijalankan di CPU berdaya rendah (< 2 Watt). Selama tidak ada pergerakan piksel di zona perimeter, GPU berada dalam mode tidur (*sleep/idle mode*).
  2. Begitu terdeteksi pergerakan objek bergerak di zona terlarang, CPU membangunkan GPU untuk menjalankan model detektor YOLO selama beberapa detik guna mengidentifikasi apakah objek tersebut manusia, kendaraan, atau hewan liar.
  3. Menghemat konsumsi baterai hingga **$> 75\%$**, memungkinkan CCTV beroperasi mandiri sepanjang malam.

### Solusi Soal Mandiri 2 (Modul Webhook Telegram Alert)
```python
import urllib.request
import urllib.parse
import json

def send_telegram_security_alert(bot_token, chat_id, message_text):
    '''
    Mengirimkan notifikasi darurat CCTV ke grup Telegram tim pengamanan.
    '''
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown'
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=3.0) as response:
            return response.status == 200
    except Exception as e:
        print(f"Gagal mengirim alert Telegram: {e}")
        return False
```

---

## 3. Rubrik Penilaian Praktikum
* **Kebenaran Geometris Ray Casting (35%)**: Logika Point-in-Polygon terbukti benar untuk titik di dalam maupun luar zona sembarang.
* **Keandalan Dwell Time Thresholding (30%)**: Berhasil memfilter pergerakan sesaat dan memicu alarm tepat waktu.
* **Visualisasi OSD CCTV (20%)**: Poligon zona terlarang dirender secara transparan dan informatif.
* **Kerapian Kode & Standar Rekayasa (15%)**: Kode bersih, modular, dan mematuhi kaidah penulisan industri.
