import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs('docs/assets', exist_ok=True)
dpi = 300

# -------------------------------------------------------------
# 1. arsitektur_integrasi_model_deep_learning_dengan_kamera_real_time.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.5), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7.5)
ax.axis('off')

# Camera Hardware
cam_box = patches.FancyBboxPatch((0.5, 4.2), 3.0, 2.6, boxstyle="round,pad=0.2", edgecolor='#0D47A1', facecolor='#E3F2FD', linewidth=2)
ax.add_patch(cam_box)
ax.text(2.0, 6.1, "1. Camera Source", ha='center', va='center', fontsize=11, fontweight='bold', color='#0D47A1')
ax.text(2.0, 5.0, "• USB Cam / RTSP IP / CSI\n• Driver Buffer V4L2/DShow\n• Resolusi: 1920x1080@30fps\n• Latensi Hardware ~33ms", ha='center', va='center', fontsize=9, color='#1565C0')

# Arrow 1
ax.annotate("", xy=(4.3, 5.5), xytext=(3.5, 5.5), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# Producer Thread (Capture)
prod_box = patches.FancyBboxPatch((4.4, 4.2), 3.8, 2.6, boxstyle="round,pad=0.2", edgecolor='#2E7D32', facecolor='#E8F5E9', linewidth=2)
ax.add_patch(prod_box)
ax.text(6.3, 6.1, "2. Capture Thread (Producer)", ha='center', va='center', fontsize=11, fontweight='bold', color='#1B5E20')
ax.text(6.3, 5.0, "• Thread Asinkron Dedicated\n• Polling cv2.VideoCapture\n• Selalu Menyimpan Frame Terbaru\n• Zero Buffer Lag Mechanism", ha='center', va='center', fontsize=9, color='#2E7D32')

# Arrow 2
ax.annotate("", xy=(9.0, 5.5), xytext=(8.2, 5.5), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# Queue / Ring Buffer
buf_box = patches.FancyBboxPatch((9.1, 4.2), 4.2, 2.6, boxstyle="round,pad=0.2", edgecolor='#E65100', facecolor='#FFF3E0', linewidth=2)
ax.add_patch(buf_box)
ax.text(11.2, 6.1, "3. Ring Buffer / Queue", ha='center', va='center', fontsize=11, fontweight='bold', color='#BF360C')
ax.text(11.2, 5.0, "• queue.Queue(maxsize=1)\n• Mutex Lock / Condition Var\n• Eliminasi Latensi Menumpuk\n• Frame Drop Jika Inferensi Lambat", ha='center', va='center', fontsize=9, color='#BF360C')

# Arrow down
ax.annotate("", xy=(11.2, 3.4), xytext=(11.2, 4.1), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# Inference Worker Thread (Consumer)
inf_box = patches.FancyBboxPatch((7.2, 0.7), 6.1, 2.6, boxstyle="round,pad=0.2", edgecolor='#6A1B9A', facecolor='#F3E5F5', linewidth=2)
ax.add_patch(inf_box)
ax.text(10.25, 2.6, "4. AI Inference Worker Thread (Consumer)", ha='center', va='center', fontsize=11, fontweight='bold', color='#4A148C')
ax.text(10.25, 1.5, "• Preprocessing: Resize, Normalize, CHW Tensor\n• ONNX Runtime / TensorRT / PyTorch GPU\n• Non-Maximum Suppression (NMS)\n• Latensi Model ~15ms (Throughput > 60 FPS)", ha='center', va='center', fontsize=9, color='#4A148C')

# Arrow left to display
ax.annotate("", xy=(6.3, 2.0), xytext=(7.1, 2.0), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# OSD & Display
osd_box = patches.FancyBboxPatch((0.5, 0.7), 5.7, 2.6, boxstyle="round,pad=0.2", edgecolor='#B71C1C', facecolor='#FFEBEE', linewidth=2)
ax.add_patch(osd_box)
ax.text(3.35, 2.6, "5. Display & OSD Telemetry", ha='center', va='center', fontsize=11, fontweight='bold', color='#B71C1C')
ax.text(3.35, 1.5, "• Gambar Bounding Box, Label, Confidence\n• Real-Time FPS Counter & Thermal Gauge\n• Output: GUI Desktop / Video Stream / MQTT\n• Sinkronisasi Audio/Visual Alarm", ha='center', va='center', fontsize=9, color='#B71C1C')

plt.title("Arsitektur Multithreaded Pipeline Integrasi Deep Learning dengan Kamera Real-Time", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/arsitektur_integrasi_model_deep_learning_dengan_kamera_real_time.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 2. pipeline_deteksi_berbasis_video_dan_tracking_sort.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

steps = [
    ("Frame Ingestion", "Video Stream Decoding\nFrame Dropping\nDownscaling (640x640)", "#BBDEFB", "#0D47A1"),
    ("Deteksi Objek", "YOLO / SSD Detector\nInferensi Tiap N Frame\nBBox [x, y, w, h] + Conf", "#C8E6C9", "#1B5E20"),
    ("Kalman Filter", "Prediksi Kecepatan & Posisi\nState: [x, y, s, r, vx, vy, vs]\nEstimasi Trajektori", "#FFE0B2", "#E65100"),
    ("Pencocokan Asosiasi", "Hungarian Algorithm\nBiaya Jarak: (1 - IoU)\nThreshold IoU = 0.3", "#E1BEE7", "#4A148C"),
    ("ID Tracking & Count", "Penetapan Unique ID\nLine Crossing Logic\nPenghitungan Akumulatif", "#FFCDD2", "#B71C1C")
]

x_pos = [0.6, 3.3, 6.0, 8.7, 11.4]
for idx, (title, desc, bg, fg) in enumerate(steps):
    box = patches.FancyBboxPatch((x_pos[idx], 1.6), 2.2, 3.8, boxstyle="round,pad=0.15", edgecolor=fg, facecolor=bg, linewidth=2)
    ax.add_patch(box)
    ax.text(x_pos[idx] + 1.1, 4.8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=fg)
    ax.text(x_pos[idx] + 1.1, 3.0, desc, ha='center', va='center', fontsize=8.8, color='#212121')
    
    if idx < 4:
        ax.annotate("", xy=(x_pos[idx+1], 3.5), xytext=(x_pos[idx] + 2.2, 3.5),
                    arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

eval_box = patches.FancyBboxPatch((1.5, 0.4), 11.0, 0.8, boxstyle="round,pad=0.1", edgecolor='#37474F', facecolor='#ECEFF1', linewidth=1.5)
ax.add_patch(eval_box)
ax.text(7.0, 0.8, "Algoritma SORT (Simple Online and Realtime Tracking): Kalman Filter + Hungarian Data Association", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#263238')

plt.title("Pipeline Sistem Deteksi Berbasis Video dan Pelacakan Objek Jamak (SORT)", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/pipeline_deteksi_berbasis_video_dan_tracking_sort.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 3. arsitektur_aplikasi_visi_komputer_desktop_dan_web.png
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=dpi)

# Left: Desktop GUI Architecture
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title("(A) Arsitektur GUI Desktop (PyQt / Tkinter)", fontsize=11, fontweight='bold')

bg1 = patches.FancyBboxPatch((0.5, 0.5), 9.0, 8.8, boxstyle="round,pad=0.2", edgecolor='#1565C0', facecolor='#E3F2FD', linewidth=1.5)
ax1.add_patch(bg1)

b_gui = patches.Rectangle((1.0, 6.5), 8.0, 2.2, edgecolor='#0D47A1', facecolor='#BBDEFB')
ax1.add_patch(b_gui)
ax1.text(5.0, 8.0, "Main UI Thread (Event Loop)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0D47A1')
ax1.text(5.0, 7.1, "• Window Canvas (QLabel / Tk.Canvas)\n• Tombol Start/Stop, Ambang Batas Slider\n• OSD Telemetri (FPS, Deteksi Counter)", ha='center', va='center', fontsize=8.5)

ax1.annotate("", xy=(5.0, 5.0), xytext=(5.0, 6.4), arrowprops=dict(arrowstyle="<->", lw=2, color='#0D47A1'))
ax1.text(5.2, 5.7, "PyQt Signal/Slot (Thread-Safe)", fontsize=8.5, fontweight='bold', color='#0D47A1')

b_work = patches.Rectangle((1.0, 1.2), 8.0, 3.5, edgecolor='#2E7D32', facecolor='#C8E6C9')
ax1.add_patch(b_work)
ax1.text(5.0, 4.0, "Worker Thread (Video & AI)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1B5E20')
ax1.text(5.0, 2.5, "• Background QThread / threading.Thread\n• Loop cv2.VideoCapture Asinkron\n• AI Inference Model (PyTorch / ONNX)\n• Emisi Frame QImage ke UI Thread", ha='center', va='center', fontsize=8.5)

# Right: Web Streaming Architecture
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title("(B) Arsitektur Web Stream (FastAPI / Flask MJPEG)", fontsize=11, fontweight='bold')

bg2 = patches.FancyBboxPatch((0.5, 0.5), 9.0, 8.8, boxstyle="round,pad=0.2", edgecolor='#E65100', facecolor='#FFF3E0', linewidth=1.5)
ax2.add_patch(bg2)

b_client = patches.Rectangle((1.0, 6.5), 8.0, 2.2, edgecolor='#BF360C', facecolor='#FFE0B2')
ax2.add_patch(b_client)
ax2.text(5.0, 8.0, "Web Browser Clients", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#BF360C')
ax2.text(5.0, 7.1, "• HTML5 <img> Tag (<img src=\"/video_feed\">\n• Responsive Mobile / Dashboard Web\n• Websocket untuk Telemetri Alert & Log", ha='center', va='center', fontsize=8.5)

ax2.annotate("", xy=(5.0, 5.0), xytext=(5.0, 6.4), arrowprops=dict(arrowstyle="<->", lw=2, color='#E65100'))
ax2.text(5.2, 5.7, "HTTP Multipart Stream (MJPEG)", fontsize=8.5, fontweight='bold', color='#E65100')

b_serv = patches.Rectangle((1.0, 1.2), 8.0, 3.5, edgecolor='#6A1B9A', facecolor='#E1BEE7')
ax2.add_patch(b_serv)
ax2.text(5.0, 4.0, "FastAPI / Flask Server Engine", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#4A148C')
ax2.text(5.0, 2.5, "• Asynchronous Video Generator (`yield (b'--frame...')`)\n• Shared Global Camera Ingestion\n• ONNX Inference Pipeline Pool\n• REST API Endpoint (/predict, /status)", ha='center', va='center', fontsize=8.5)

plt.tight_layout()
plt.savefig('docs/assets/arsitektur_aplikasi_visi_komputer_desktop_dan_web.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 4. sistem_deteksi_penyakit_daun_kelapa_sawit_real_time.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

leaf_steps = [
    ("1. Ingestion Citra", "Kamera Ponsel / Handheld\nROI Focusing\nResolusi 640x480\nPencahayaan Alami", "#BBDEFB", "#0D47A1"),
    ("2. Deep Learning", "Model ResNet / YOLO\nLokalisasi Bercak Daun\nIdentifikasi Patogen:\nCurvularia / Hawar", "#C8E6C9", "#1B5E20"),
    ("3. Severity Scoring", "Kalkulasi Luas Lesi (%)\nLevel Serangan:\n• Ringan (< 5%)\n• Sedang (5-20%)\n• Berat (> 20%)", "#FFE0B2", "#E65100"),
    ("4. Rekomendasi Aksi", "Pohon Keputusan Agronomi:\n• Karantina Polybag\n• Fungisida Mankozeb 2g/L\n• Penyesuaian Irigasi", "#FFCDD2", "#B71C1C")
]

x_l = [0.6, 3.9, 7.2, 10.5]
for i, (title, content, bg, fg) in enumerate(leaf_steps):
    box = patches.FancyBboxPatch((x_l[i], 1.5), 2.9, 3.8, boxstyle="round,pad=0.15", edgecolor=fg, facecolor=bg, linewidth=2)
    ax.add_patch(box)
    ax.text(x_l[i] + 1.45, 4.8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=fg)
    ax.text(x_l[i] + 1.45, 3.0, content, ha='center', va='center', fontsize=8.8, color='#212121')
    
    if i < 3:
        ax.annotate("", xy=(x_l[i+1], 3.4), xytext=(x_l[i] + 2.9, 3.4),
                    arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

foot_box = patches.FancyBboxPatch((1.5, 0.3), 11.0, 0.8, boxstyle="round,pad=0.1", edgecolor='#2E7D32', facecolor='#E8F5E9', linewidth=1.5)
ax.add_patch(foot_box)
ax.text(7.0, 0.7, "Solusi Lapangan Terintegrasi: Deteksi Visual Real-Time + Kuantifikasi Keparahan + Rekomendasi Proteksi Tanaman", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1B5E20')

plt.title("Sistem Terpadu Deteksi Penyakit Daun Kelapa Sawit Real-Time dan Rekomendasi Agronomi", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/sistem_deteksi_penyakit_daun_kelapa_sawit_real_time.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 5. arsitektur_monitoring_cctv_keamanan_dan_logistik_perkebunan.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.5), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7.5)
ax.axis('off')

# Multi-stream inputs
cctv_box = patches.FancyBboxPatch((0.5, 4.2), 3.2, 2.7, boxstyle="round,pad=0.2", edgecolor='#1565C0', facecolor='#E3F2FD', linewidth=2)
ax.add_patch(cctv_box)
ax.text(2.1, 6.3, "Multi-Camera RTSP Streams", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0D47A1')
ax.text(2.1, 5.1, "• CCTV Pos Gerbang Utama\n• CCTV Loading Ramp Pabrik\n• CCTV Timbangan TBS\n• CCTV Perimeter Batas Blok", ha='center', va='center', fontsize=8.5, color='#1565C0')

# Arrow to Video Hub
ax.annotate("", xy=(4.6, 5.5), xytext=(3.8, 5.5), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# Processing Hub
hub_box = patches.FancyBboxPatch((4.7, 4.2), 4.3, 2.7, boxstyle="round,pad=0.2", edgecolor='#2E7D32', facecolor='#E8F5E9', linewidth=2)
ax.add_patch(hub_box)
ax.text(6.85, 6.3, "Edge AI Inference Server", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1B5E20')
ax.text(6.85, 5.1, "• YOLOv8 Multi-Class Detector\n• Pelacakan DeepSORT (ID Tracking)\n• Polygon ROI Intrusion Checking\n• Line-Crossing Counter (In/Out)", ha='center', va='center', fontsize=8.5, color='#1B5E20')

# Arrow to Operations
ax.annotate("", xy=(9.8, 5.5), xytext=(9.1, 5.5), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# Analytical Modules
app_box = patches.FancyBboxPatch((9.9, 4.2), 3.6, 2.7, boxstyle="round,pad=0.2", edgecolor='#E65100', facecolor='#FFF3E0', linewidth=2)
ax.add_patch(app_box)
ax.text(11.7, 6.3, "Operational Modules", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#BF360C')
ax.text(11.7, 5.1, "• Modul 1: Sensus Truk TBS\n• Modul 2: Pelanggaran APD K3\n• Modul 3: Intrusi Batas Liar\n• Modul 4: Estimasi Antrean", ha='center', va='center', fontsize=8.5, color='#BF360C')

# Central Dashboard & Notification Bottom
dash_box = patches.FancyBboxPatch((2.0, 0.7), 10.0, 2.8, boxstyle="round,pad=0.2", edgecolor='#6A1B9A', facecolor='#F3E5F5', linewidth=2)
ax.add_patch(dash_box)
ax.text(7.0, 3.0, "Enterprise Plantation Dashboard & Automated Dispatch", ha='center', va='center', fontsize=11, fontweight='bold', color='#4A148C')
ax.text(7.0, 1.8, "• WebSocket Real-Time Alert ke Ruang Kendali (Central Command Room)\n• Integrasi Database PostgreSQL / SAP ERP Perkebunan\n• Notifikasi Otomatis via Bot Telegram / WhatsApp ke Mandor Keamanan\n• Rekaman Snapshot Bukti Kejadian (Event-Based Video Clipping)", ha='center', va='center', fontsize=9, color='#4A148C')

# Arrows down to dashboard
ax.annotate("", xy=(5.0, 3.6), xytext=(6.5, 4.1), arrowprops=dict(arrowstyle="->", lw=2, color='#424242'))
ax.annotate("", xy=(9.0, 3.6), xytext=(11.5, 4.1), arrowprops=dict(arrowstyle="->", lw=2, color='#424242'))

plt.title("Arsitektur Monitoring CCTV Cerdas: Keamanan Perimeter dan Logistik Angkutan TBS", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/arsitektur_monitoring_cctv_keamanan_dan_logistik_perkebunan.png', dpi=dpi)
plt.close()

print("[OK] Selesai menghasilkan 5 diagram arsitektur Part 13 beresolusi 300 DPI!")
