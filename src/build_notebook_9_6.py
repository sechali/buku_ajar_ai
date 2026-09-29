import json

nb = {
    'cells': [],
    'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3.10.11'}
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

def add_md(text):
    nb['cells'].append({'cell_type': 'markdown', 'metadata': {}, 'source': [line + '\n' for line in text.strip().split('\n')]})

def add_code(text):
    nb['cells'].append({'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': [line + '\n' for line in text.strip().split('\n')]})

add_md('''# Praktikum AI Modul 9.6: Deteksi Tepi dan Gradien Citra (Edge Detection and Image Gradients)
**Program Studi Teknik Pertanian / Agroteknologi - Fakultas Pertanian & Teknologi Pertanian**  
*Materi: Kalkulus Diferensial Citra, Operator Turunan Pertama (Sobel & Scharr), Operator Turunan Kedua (Laplacian of Gaussian), serta Detektor Tepi Optimal Canny pada Kanopi Kelapa Sawit.*

---
### Tujuan Praktikum
1. Memahami perbedaan fundamental respon gradien spasial horizontal ($G_x$) dan vertikal ($G_y$) menggunakan tipe data signed floating-point `CV_64F`.
2. Mengukur magnitudo dan arah orientasi sudut gradien pelepah kelapa sawit dari citra ortofoto drone.
3. Membandingkan sensitivitas detektor orde kedua Laplacian terhadap derau dan keunggulan pelembutan Gaussian (*LoG*).
4. Mengimplementasikan dan menala parameter algoritma Canny Edge Detector (*Non-Maximum Suppression* dan *Hysteresis Thresholding*).
5. Menerapkan ekstraksi kontur tepi untuk estimasi perimeter kanopi pohon sawit.''')

add_code('''import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print(f"OpenCV Version : {cv2.__version__}")
print(f"NumPy Version  : {np.__version__}")''')

add_md('''## 1. Pembuatan Dataset Sintetis: Kanopi Kelapa Sawit dengan Pola Pelepah Radial
Kita memodelkan kanopi pohon kelapa sawit tampak atas (*orthophoto*) dengan 8 pelepah utama dan anak daun (*pinnae*) bersudut.''')

add_code('''def generate_palm_canopy_scene():
    np.random.seed(42)
    h, w = 240, 240
    Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    cx, cy = 120, 120
    
    # 1. Latar belakang tanah perkebunan
    canopy = np.ones((h, w), dtype=np.float32) * 55
    
    # 2. Lingkar tajuk kanopi (crown area)
    radial_dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
    crown_mask = radial_dist <= 90
    canopy[crown_mask] = 125
    
    # 3. 8 pelepah daun radial utama (tulang pelepah terang)
    for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        line_dist = np.abs(np.cos(angle) * (X - cx) + np.sin(angle) * (Y - cy))
        frond_mask = (line_dist <= 3.0) & (radial_dist <= 95)
        canopy[frond_mask] = 220
        # Anak daun lateral (pinnae)
        for r in range(25, 90, 8):
            leaflet = (np.abs(radial_dist - r) <= 1.5) & (line_dist <= 14) & crown_mask
            canopy[leaflet] = 165
            
    # Tambahkan derau halus alami
    canopy_uint8 = np.clip(canopy + np.random.normal(0, 2.5, (h, w)), 0, 255).astype(np.uint8)
    return canopy_uint8

canopy_gray = generate_palm_canopy_scene()
print(f"Citra kanopi sawit berhasil dibuat: resolusi {canopy_gray.shape}, min={canopy_gray.min()}, max={canopy_gray.max()}")''')

add_md('''## 2. Eksperimen Operator Gradien Sobel & Bahaya Pemotongan Tipe Data `uint8`
Kita membuktikan mengapa penghitungan gradien wajib menggunakan tipe data bertanda (`cv2.CV_64F`) dan apa yang terjadi jika menggunakan `cv2.CV_8U` (gradien negatif terpotong menjadi 0).''')

add_code('''# 1. Implementasi yang BENAR: cv2.CV_64F (Preservasi nilai negatif)
sobel_x_64f = cv2.Sobel(canopy_gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y_64f = cv2.Sobel(canopy_gray, cv2.CV_64F, 0, 1, ksize=3)

# Hitung magnitudo gradien eksak
mag_sobel = np.sqrt(sobel_x_64f**2 + sobel_y_64f**2)
mag_sobel_uint8 = np.clip(mag_sobel / (mag_sobel.max() + 1e-6) * 255, 0, 255).astype(np.uint8)

# 2. Implementasi yang SALAH: cv2.CV_8U (Nilai negatif terpotong ke 0)
sobel_x_8u_flawed = cv2.Sobel(canopy_gray, cv2.CV_8U, 1, 0, ksize=3)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
axes[0].imshow(canopy_gray, cmap='gray')
axes[0].set_title("Citra Asli Kanopi")

axes[1].imshow(np.abs(sobel_x_64f), cmap='hot')
axes[1].set_title("Sobel X (CV_64F Mutlak)\\n(Tepi Kiri & Kanan Terdeteksi)")

axes[2].imshow(sobel_x_8u_flawed, cmap='hot')
axes[2].set_title("Sobel X (CV_8U Cacat!)\\n(Separuh Tepi Hilang/Truncated)")

axes[3].imshow(mag_sobel_uint8, cmap='viridis')
axes[3].set_title("Magnitudo Gradien Total ||grad f||")

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.savefig('docs/assets/notebook_9_6_sobel_analysis.png', dpi=150)
plt.close()
print("Hasil visualisasi Sobel tersimpan di docs/assets/notebook_9_6_sobel_analysis.png")''')

add_md('''## 3. Komparasi Operator Orde Pertama (Sobel vs Scharr) dan Orde Kedua (Laplacian vs LoG)
Kita membandingkan ketajaman respons kontur melingkar antara Sobel dan Scharr, serta menganalisis efek pelembutan Gaussian pada operator Laplacian.''')

add_code('''# 1. Operator Scharr (3x3 teroptimasi)
scharr_x = cv2.Scharr(canopy_gray, cv2.CV_64F, 1, 0)
scharr_y = cv2.Scharr(canopy_gray, cv2.CV_64F, 0, 1)
mag_scharr = np.sqrt(scharr_x**2 + scharr_y**2)
scharr_vis = np.clip(mag_scharr / (mag_scharr.max() + 1e-6) * 255, 0, 255).astype(np.uint8)

# 2. Laplacian langsung (tanpa filter, rentan derau)
laplacian_raw = cv2.Laplacian(canopy_gray, cv2.CV_64F, ksize=3)
laplacian_raw_vis = np.clip(np.abs(laplacian_raw) / (np.abs(laplacian_raw).max() + 1e-6) * 255, 0, 255).astype(np.uint8)

# 3. Laplacian of Gaussian (LoG dengan pelembutan awal sigma=1.2)
blurred = cv2.GaussianBlur(canopy_gray, (5, 5), sigmaX=1.2)
laplacian_log = cv2.Laplacian(blurred, cv2.CV_64F, ksize=3)
laplacian_log_vis = np.clip(np.abs(laplacian_log) / (np.abs(laplacian_log).max() + 1e-6) * 255, 0, 255).astype(np.uint8)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
axes[0].imshow(mag_sobel_uint8, cmap='inferno')
axes[0].set_title("Magnitudo Sobel 3x3")

axes[1].imshow(scharr_vis, cmap='inferno')
axes[1].set_title("Magnitudo Scharr 3x3\\n(Kontur Lengkung Lebih Tajam)")

axes[2].imshow(laplacian_raw_vis, cmap='bone')
axes[2].set_title("Laplacian Mentah\\n(Tercemar Derau Latar)")

axes[3].imshow(laplacian_log_vis, cmap='bone')
axes[3].set_title("Laplacian of Gaussian (LoG)\\n(Tepi Bersih & Halus)")

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.savefig('docs/assets/notebook_9_6_gradient_operators.png', dpi=150)
plt.close()
print("Hasil perbandingan operator gradien tersimpan di docs/assets/notebook_9_6_gradient_operators.png")''')

add_md('''## 4. Detektor Tepi Optimal Canny dan Penalaan Ambang Batas Histeresis
Kita menguji algoritma Canny dengan berbagai kombinasi ambang batas histeresis ($T_{\\text{low}}, T_{\\text{high}}$) untuk mendapatkan siluet kontur pelepah sawit yang optimal (kontinu dan tipis setebal 1 piksel).''')

add_code('''# Evaluasi 3 pasangan ambang batas histeresis
canny_low = cv2.Canny(blurred, 20, 60)      # Sangat sensitif: menangkap banyak derau
canny_optimal = cv2.Canny(blurred, 40, 120)  # Optimal: rasio 1:3, garis pelepah kontinu
canny_high = cv2.Canny(blurred, 90, 200)    # Terlalu tinggi: kontur terputus-putus

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
axes[0].imshow(canopy_gray, cmap='gray')
axes[0].set_title("Citra Ortofoto Asli")

axes[1].imshow(canny_low, cmap='gray')
axes[1].set_title("Canny (20, 60)\\n(Over-detection / Derau Semu)")

axes[2].imshow(canny_optimal, cmap='gray')
axes[2].set_title("Canny (40, 120)\\n(Optimal: Kontinu & Presisi 1-px)")

axes[3].imshow(canny_high, cmap='gray')
axes[3].set_title("Canny (90, 200)\\n(Under-detection / Garis Putus)")

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.savefig('docs/assets/notebook_9_6_canny_thresholding.png', dpi=150)
plt.close()
print("Hasil penalaan Canny tersimpan di docs/assets/notebook_9_6_canny_thresholding.png")''')

add_md('''## 5. Latihan Mandiri dan Studi Kasus Terapan

### Latihan 1: Ekstraksi Orientasi Garis Pelepah Menggunakan Histogram Sudut Gradien
Hitung distribusi orientasi sudut $\\theta = \\arctan(G_y / G_x)$ pada piksel-piksel tepi yang lolos ambang batas Canny, dan visualisasikan arah dominan pelepah kanopi sawit.

### Latihan 2: Pengukuran Panjang Keliling Tajuk (*Crown Perimeter*)
Hitung jumlah total piksel tepi pada kontur luar tajuk dan konversikan ke satuan meter riil jika diketahui *Ground Sampling Distance* (GSD) kamera drone adalah $2.5\\text{ cm/piksel}$.''')

add_code('''# Solusi Latihan 2: Kalkulasi Perimeter Tajuk Kanopi Kelapa Sawit
def calculate_crown_perimeter(canny_edge_mask, gsd_cm=2.5):
    # Hitung total piksel tepi
    total_edge_pixels = np.sum(canny_edge_mask > 0)
    
    # Konversi ke dimensi fisik riil (meter)
    perimeter_cm = total_edge_pixels * gsd_cm
    perimeter_meter = perimeter_cm / 100.0
    
    return total_edge_pixels, perimeter_meter

edge_count, perimeter_m = calculate_crown_perimeter(canny_optimal, gsd_cm=2.5)
print("=== HASIL ANALISIS MORFOMETRI KANOPI SAWIT ===")
print(f"Total Piksel Tepi Terdeteksi : {edge_count} piksel")
print(f"GSD Sensor Drone             : 2.5 cm/piksel")
print(f"Estimasi Keliling Tajuk (CPA): {perimeter_m:.2f} meter")''')

with open('notebooks/part-09/AI_Modul_9.6_Praktikum_Deteksi_Tepi_dan_Gradien_Citra.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print('Notebook Modul 9.6 berhasil dibuat!')
