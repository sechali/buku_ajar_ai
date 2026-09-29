import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Figure 11.1: Arsitektur dan Modul Inti OpenCV
def fig_11_1():
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=300)
    ax.set_title("Arsitektur Sistem & Struktur Modul Inti OpenCV untuk Pengolahan Citra", fontsize=14, fontweight='bold', pad=18)
    
    # Layer 1: Application Layer
    ax.add_patch(FancyBboxPatch((0.05, 0.80), 0.90, 0.14, boxstyle="round,pad=0.02", facecolor="#E3F2FD", edgecolor="#1565C0", linewidth=2))
    ax.text(0.5, 0.87, "Lapisan Aplikasi Pertanian & Industri (Python Script, GUI, Edge AI, ROS, Web API)", ha='center', va='center', fontsize=11, fontweight='bold', color="#0D47A1")
    
    # Layer 2: Language Bindings
    ax.add_patch(FancyBboxPatch((0.05, 0.62), 0.90, 0.12, boxstyle="round,pad=0.02", facecolor="#E8F5E9", edgecolor="#2E7D32", linewidth=2))
    ax.text(0.5, 0.68, "OpenCV Language Bindings (Python C-API / NumPy Array Bridge, C++, Java, Julia)", ha='center', va='center', fontsize=11, fontweight='bold', color="#1B5E20")
    
    # Layer 3: OpenCV Core Modules
    modules = [
        ("core", "Struktur Data Mat,\nOperasi Vektor &\nAljabar Matriks", "#FFF3E0", "#E65100"),
        ("imgproc", "Filter, Transformasi,\nColor Conversion &\nDeteksi Kontur", "#FCE4EC", "#C2185B"),
        ("video", "Motion Analysis,\nBackground Subtraction\n& Optical Flow", "#EDE7F6", "#512DA8"),
        ("highgui & videoio", "I/O Citra, VideoCapture,\nGUI Display &\nVideoWriter", "#E0F7FA", "#00838F"),
        ("objdetect & dnn", "Haar Cascade,\nHOG & Deep Learning\nInference Engine", "#F1F8E9", "#33691E")
    ]
    for i, (name, desc, bg, border) in enumerate(modules):
        x = 0.05 + i * 0.184
        ax.add_patch(FancyBboxPatch((x, 0.32), 0.168, 0.24, boxstyle="round,pad=0.02", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(x + 0.084, 0.51, name, ha='center', va='center', fontsize=10.5, fontweight='bold', color=border)
        ax.text(x + 0.084, 0.41, desc, ha='center', va='center', fontsize=8.5, color='#37474F')
        
    # Layer 4: Hardware Acceleration Layer
    ax.add_patch(FancyBboxPatch((0.05, 0.10), 0.90, 0.15, boxstyle="round,pad=0.02", facecolor="#ECEFF1", edgecolor="#455A64", linewidth=2))
    ax.text(0.5, 0.175, "Lapisan Akselerasi Perangkat Keras (Intel TBB, IPP, OpenCL, NVIDIA CUDA, ARM NEON)", ha='center', va='center', fontsize=11, fontweight='bold', color="#263238")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('docs/assets/arsitektur_dan_modul_inti_opencv.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/arsitektur_dan_modul_inti_opencv.png")

# 2. Figure 11.2: Koordinat dan Manipulasi Matriks Citra OpenCV
def fig_11_2():
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), dpi=300)
    
    # Left: OpenCV Coordinate System vs NumPy Slicing
    ax = axes[0]
    ax.set_title("Sistem Koordinat Citra OpenCV (X, Y) vs NumPy Indexing (Row, Col)", fontsize=11.5, fontweight='bold', pad=12)
    ax.add_patch(Rectangle((0.15, 0.15), 0.7, 0.7, facecolor="#F5F5F5", edgecolor="#424242", linewidth=2))
    
    # Arrows for X and Y
    ax.annotate("", xy=(0.9, 0.85), xytext=(0.15, 0.85), arrowprops=dict(arrowstyle="->", lw=2.5, color="#D32F2F"))
    ax.text(0.52, 0.88, "Sumbu X (Lebar / Width / Kolom: x = 0 ... W-1)", ha='center', fontsize=9, fontweight='bold', color="#D32F2F")
    
    ax.annotate("", xy=(0.15, 0.1), xytext=(0.15, 0.85), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1976D2"))
    ax.text(0.12, 0.48, "Sumbu Y (Tinggi / Height / Baris: y = 0 ... H-1)", ha='right', va='center', rotation=90, fontsize=9, fontweight='bold', color="#1976D2")
    
    # ROI Patch
    ax.add_patch(Rectangle((0.35, 0.35), 0.35, 0.35, facecolor="#FFE082", edgecolor="#FF8F00", linewidth=2, linestyle="--"))
    ax.text(0.525, 0.525, "Region of Interest (ROI)\nimage[y1:y2, x1:x2]", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#E65100")
    
    ax.text(0.15, 0.86, "(0, 0)", fontsize=9, fontweight='bold', color='#212121')
    ax.text(0.85, 0.13, "(W, H)", fontsize=9, fontweight='bold', color='#212121')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Right: BGR vs RGB Channel Slices
    ax = axes[1]
    ax.set_title("Susunan Kanal Warna Citra Digital: OpenCV (BGR) vs Standar (RGB)", fontsize=11.5, fontweight='bold', pad=12)
    channels_bgr = [
        ("Kanal 0: Biru (Blue)", "#BBDEFB", "#0D47A1", 0.65),
        ("Kanal 1: Hijau (Green)", "#C8E6C9", "#1B5E20", 0.42),
        ("Kanal 2: Merah (Red)", "#FFCDD2", "#B71C1C", 0.19)
    ]
    for label, bg, border, y in channels_bgr:
        ax.add_patch(FancyBboxPatch((0.15, y), 0.70, 0.17, boxstyle="round,pad=0.02", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(0.5, y + 0.085, label, ha='center', va='center', fontsize=10, fontweight='bold', color=border)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('docs/assets/koordinat_dan_manipulasi_matriks_citra_opencv.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/koordinat_dan_manipulasi_matriks_citra_opencv.png")

# 3. Figure 11.3: Konversi Ruang Warna OpenCV
def fig_11_3():
    fig, axes = plt.subplots(1, 4, figsize=(14, 4.5), dpi=300)
    
    spaces = [
        ("BGR (Default OpenCV)", "Blue, Green, Red\nSensitif terhadap fluktuasi\niluminasi cahaya lapangan", "#E3F2FD", "#1565C0"),
        ("RGB (Matplotlib/PIL)", "Red, Green, Blue\nStandar display visual monitor\n& pustaka deep learning", "#FFEBEE", "#C62828"),
        ("HSV (Silinder Warna)", "Hue (Corak 0-179),\nSaturation (Kejenuhan 0-255),\nValue (Kecerahan 0-255)\nIdeal untuk segmentasi kanopi", "#E8F5E9", "#2E7D32"),
        ("CIELAB (Perceptual)", "L* (Luminansi Cahaya),\na* (Hijau ke Magenta),\nb* (Biru ke Kuning)\nTahan variasi bayangan pohon", "#FFF8E1", "#F57F17")
    ]
    
    for ax, (title, desc, bg, border) in zip(axes, spaces):
        ax.set_title(title, fontsize=10.5, fontweight='bold', pad=10)
        ax.add_patch(FancyBboxPatch((0.08, 0.15), 0.84, 0.75, boxstyle="round,pad=0.03", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(0.5, 0.52, desc, ha='center', va='center', fontsize=9, fontweight='bold', color=border, multialignment='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
    plt.tight_layout()
    plt.savefig('docs/assets/diagram_konversi_ruang_warna_opencv_bgr_rgb_hsv_lab.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/diagram_konversi_ruang_warna_opencv_bgr_rgb_hsv_lab.png")

# 4. Figure 11.4: Komparasi Thresholding OpenCV
def fig_11_4():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), dpi=300)
    
    techs = [
        ("Simple Global Threshold", "Ambang Batas Statis Tunggal T\n$dst(x,y) = maxval$ if $src(x,y) > T$ else $0$\nGagal jika ada gradien bayangan tajuk", "#E3F2FD", "#1565C0"),
        ("Otsu's Bimodal Threshold", "Pencarian Otomatis Ambang $T^*$\nMeminimalkan varians intra-kelas:\n$\\sigma_w^2(T) = \\omega_0 \\sigma_0^2 + \\omega_1 \\sigma_1^2$\nOptimal untuk histogram bimodal", "#E8F5E9", "#2E7D32"),
        ("Adaptive Local Threshold", "Ambang Dinamis per Jendela Lingkungan\n$T(x,y) = \\text{Mean / Gauss}(N(x,y)) - C$\nSangat tahan terhadap variasi pencahayaan\nkanopi kelapa sawit di lapangan", "#FFF3E0", "#E65100")
    ]
    for ax, (title, desc, bg, border) in zip(axes, techs):
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
        ax.add_patch(FancyBboxPatch((0.06, 0.12), 0.88, 0.78, boxstyle="round,pad=0.03", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(0.5, 0.51, desc, ha='center', va='center', fontsize=9, fontweight='bold', color=border, multialignment='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
    plt.tight_layout()
    plt.savefig('docs/assets/komparasi_metode_thresholding_biner_otsu_adaptif.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/komparasi_metode_thresholding_biner_otsu_adaptif.png")

# 5. Figure 11.5: Hierarki Kontur dan Aproksimasi Geometri
def fig_11_5():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.set_title("Analisis Kontur Geometris & Ekstraksi Morfometri Tanaman OpenCV", fontsize=13, fontweight='bold', pad=15)
    
    # Outer circle (Canopy)
    c_out = Circle((0.35, 0.5), 0.28, facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2.5, linestyle='-')
    ax.add_patch(c_out)
    
    # Inner irregular shape (Defect / Fruit core)
    pts = np.array([[0.25, 0.45], [0.32, 0.60], [0.42, 0.58], [0.45, 0.42], [0.35, 0.35]])
    poly = plt.Polygon(pts, facecolor='#FFEBEE', edgecolor='#C62828', linewidth=2, linestyle='--')
    ax.add_patch(poly)
    
    # Bounding Box
    rect = Rectangle((0.07, 0.22), 0.56, 0.56, fill=False, edgecolor='#1565C0', linewidth=1.8, linestyle=':')
    ax.add_patch(rect)
    
    ax.text(0.35, 0.80, "Bounding Box: cv2.boundingRect()", color='#1565C0', fontweight='bold', fontsize=9.5)
    ax.text(0.35, 0.24, "Kontur Eksternal Kanopi: cv2.findContours()", color='#2E7D32', fontweight='bold', fontsize=9.5)
    ax.text(0.35, 0.48, "Kontur Internal\n(Defek/Bercak)", color='#C62828', fontweight='bold', fontsize=8.5, ha='center')
    
    # Metrics Table on the Right
    ax.add_patch(FancyBboxPatch((0.68, 0.15), 0.30, 0.70, boxstyle="round,pad=0.02", facecolor="#F5F5F5", edgecolor="#616161", linewidth=1.5))
    metrics_text = (
        "Parameter Morfometri:\n\n"
        "• Luas Area (A):\n  cv2.contourArea(cnt)\n\n"
        "• Keliling Perimeter (P):\n  cv2.arcLength(cnt, True)\n\n"
        "• Rasio Kebulatan:\n  C = 4*pi*A / P^2\n\n"
        "• Titik Pusat (Centroid):\n  Cx = M10/M00, Cy = M01/M00\n\n"
        "• Convex Hull:\n  cv2.convexHull(cnt)"
    )
    ax.text(0.70, 0.50, metrics_text, va='center', fontsize=9, color='#212121')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('docs/assets/hierarki_kontur_dan_aproksimasi_geometri_opencv.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/hierarki_kontur_dan_aproksimasi_geometri_opencv.png")

# 6. Figure 11.6: Face Detection Haar Cascade
def fig_11_6():
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=300)
    ax.set_title("Arsitektur Deteksi Wajah & Fitur Haar Cascade (Viola-Jones Framework)", fontsize=13, fontweight='bold', pad=15)
    
    steps = [
        ("1. Citra Masukan Grayscale\n(Wajah Pekerja Kebun / Operator PKS)", "#E3F2FD", "#1565C0"),
        ("2. Integral Image Computation\n$ii(x,y) = \\sum_{x' \\leq x, y' \\leq y} i(x',y')$\nEvaluasi fitur konstan $O(1)$", "#E0F7FA", "#00838F"),
        ("3. Ekstraksi Fitur Haar\n(Edge, Line, & Center-Surround Features)", "#FFF8E1", "#F57F17"),
        ("4. Cascaded AdaBoost Classifiers\nEliminasi kandidat negatif secara bertingkat", "#FCE4EC", "#C2185B"),
        ("5. Bounding Box Deteksi Wajah\n(cv2.CascadeClassifier)", "#E8F5E9", "#2E7D32")
    ]
    for i, (title, bg, border) in enumerate(steps):
        x = 0.04 + i * 0.192
        ax.add_patch(FancyBboxPatch((x, 0.20), 0.176, 0.60, boxstyle="round,pad=0.02", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(x + 0.088, 0.50, title, ha='center', va='center', fontsize=9, fontweight='bold', color=border, multialignment='center')
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 0.188, 0.50), xytext=(x + 0.176, 0.50),
                        arrowprops=dict(arrowstyle="->", lw=2.5, color='#455A64'))
            
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('docs/assets/arsitektur_haar_cascade_dan_integral_image_face_detection.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/arsitektur_haar_cascade_dan_integral_image_face_detection.png")

# 7. Figure 11.7: Video Processing Pipeline
def fig_11_7():
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=300)
    ax.set_title("Pipeline Arsitektur Video Processing OpenCV: VideoCapture ke VideoWriter", fontsize=13, fontweight='bold', pad=15)
    
    stages = [
        ("Input Stream\n(Kamera Drone / CCTV PKS / File MP4)", "#E3F2FD", "#1565C0"),
        ("cv2.VideoCapture\n• cap.read() -> ret, frame\n• Demuxing & Decoding Frame", "#E0F2F1", "#00796B"),
        ("Frame Processing Loop\n• Color conversion / Filter\n• Deteksi Objek / Tracking\n• Profiling FPS per Frame", "#FFF3E0", "#E65100"),
        ("Overlay & Visualisasi\n• cv2.putText() / Bounding Box\n• OSD Metrik & Status Alarm", "#F3E5F5", "#6A1B9A"),
        ("Output Stream\n• cv2.imshow() / GUI\n• cv2.VideoWriter (Codec mp4v)", "#E8F5E9", "#2E7D32")
    ]
    for i, (title, bg, border) in enumerate(stages):
        x = 0.04 + i * 0.192
        ax.add_patch(FancyBboxPatch((x, 0.20), 0.176, 0.60, boxstyle="round,pad=0.02", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(x + 0.088, 0.50, title, ha='center', va='center', fontsize=9, fontweight='bold', color=border, multialignment='center')
        if i < len(stages) - 1:
            ax.annotate("", xy=(x + 0.188, 0.50), xytext=(x + 0.176, 0.50),
                        arrowprops=dict(arrowstyle="->", lw=2.5, color='#1565C0'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('docs/assets/pipeline_video_processing_videocapture_dan_fps_profiling.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/pipeline_video_processing_videocapture_dan_fps_profiling.png")

# 8. Figure 11.8: Motion Detection Frame Differencing
def fig_11_8():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), dpi=300)
    
    methods = [
        ("Absolute Frame Differencing", "| Frame(t) - Frame(t-1) |\nKelebihan: Komputasi sangat ringan\nKekurangan: Objek berhenti mendadak hilang,\nsensitif terhadap derau goyangan daun", "#E3F2FD", "#1565C0"),
        ("Background Subtraction (MOG2)", "Gaussian Mixture-based Model\nMemodelkan latar belakang dinamis\ndan bayangan (*shadow detection*)\nOptimal untuk CCTV konveyor pabrik", "#E8F5E9", "#2E7D32"),
        ("Optical Flow (Lucas-Kanade)", "Estimasi Vektor Kecepatan $(u, v)$\nBerdasarkan asumsi kecerahan konstan:\n$I_x u + I_y v + I_t = 0$\nMendeteksi arah dan magnitudo gerak", "#FFF3E0", "#E65100")
    ]
    for ax, (title, desc, bg, border) in zip(axes, methods):
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
        ax.add_patch(FancyBboxPatch((0.06, 0.12), 0.88, 0.78, boxstyle="round,pad=0.03", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(0.5, 0.51, desc, ha='center', va='center', fontsize=9, fontweight='bold', color=border, multialignment='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
    plt.tight_layout()
    plt.savefig('docs/assets/mekanisme_frame_differencing_dan_optical_flow_motion_detection.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/mekanisme_frame_differencing_dan_optical_flow_motion_detection.png")

# 9. Figure 11.9: Real-time Threaded Camera Stream
def fig_11_9():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.set_title("Arsitektur Threaded Camera Streamer OpenCV untuk Eliminasi Buffer Lag Real-Time", fontsize=13, fontweight='bold', pad=15)
    
    # Thread 1: Dedicated Frame Reader
    ax.add_patch(FancyBboxPatch((0.08, 0.55), 0.38, 0.35, boxstyle="round,pad=0.02", facecolor="#E1F5FE", edgecolor="#0288D1", linewidth=2))
    ax.text(0.27, 0.82, "Thread 1: Camera I/O Thread", ha='center', fontsize=11, fontweight='bold', color="#01579B")
    ax.text(0.27, 0.68, "• cv2.VideoCapture(0).read()\n• Selalu memperbarui frame terbaru\n• Mengosongkan buffer internal driver\n• Operasi non-blocking bagi proses utama", ha='center', fontsize=9, color="#0277BD")
    
    # Shared Memory / Queue
    ax.add_patch(FancyBboxPatch((0.48, 0.62), 0.14, 0.20, boxstyle="round,pad=0.02", facecolor="#FFFDE7", edgecolor="#FBC02D", linewidth=2))
    ax.text(0.55, 0.72, "Thread-Safe\nLatest Frame\nBuffer", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#F57F17")
    
    # Thread 2: Main Processing Thread
    ax.add_patch(FancyBboxPatch((0.64, 0.55), 0.30, 0.35, boxstyle="round,pad=0.02", facecolor="#E8F5E9", edgecolor="#388E3C", linewidth=2))
    ax.text(0.79, 0.82, "Thread Utama (Processing)", ha='center', fontsize=11, fontweight='bold', color="#1B5E20")
    ax.text(0.79, 0.68, "• Mengambil frame terbaru\n• Inferensi AI / Deteksi\n• Latensi nol (Zero lag)\n• Display & Logging", ha='center', fontsize=9, color="#2E7D32")
    
    # Bottom Note
    ax.add_patch(FancyBboxPatch((0.08, 0.12), 0.86, 0.30, boxstyle="round,pad=0.02", facecolor="#ECEFF1", edgecolor="#455A64", linewidth=1.5))
    benefit_text = (
        "Manfaat Rekayasa Perkebunan:\n"
        "1. Menghilangkan delay 2 - 5 detik yang sering terjadi pada RTSP stream kamera CCTV perkebunan kelapa sawit.\n"
        "2. Memastikan pemantauan konveyor TBS berkecepatan 1.5 m/detik tidak melewatkan buah tanpa pemrosesan.\n"
        "3. Memisahkan komputasi berat deteksi objek dari pembacaan soket jaringan perangkat kamera IP."
    )
    ax.text(0.11, 0.27, benefit_text, va='center', fontsize=9.5, color="#263238")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('docs/assets/arsitektur_real_time_multithreaded_camera_stream_opencv.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/arsitektur_real_time_multithreaded_camera_stream_opencv.png")

if __name__ == '__main__':
    fig_11_1()
    fig_11_2()
    fig_11_3()
    fig_11_4()
    fig_11_5()
    fig_11_6()
    fig_11_7()
    fig_11_8()
    fig_11_9()
