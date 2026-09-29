import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cv2

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(16, 9), dpi=300)

gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.25, left=0.06, right=0.96, top=0.92, bottom=0.08)

# 1. Synthesize Oil Palm Canopy Drone Patch
np.random.seed(42)
h, w = 240, 240
Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
cx, cy = 120, 120

# Radial canopy with fronds
canopy = np.ones((h, w), dtype=np.float32) * 55
dist_center = np.sqrt((X - cx)**2 + (Y - cy)**2)
crown_mask = dist_center <= 90
canopy[crown_mask] = 125

# Add 8 primary fronds with bright central rachis
for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
    line_dist = np.abs(np.cos(angle)*(X - cx) + np.sin(angle)*(Y - cy))
    radial = np.sqrt((X - cx)**2 + (Y - cy)**2)
    frond = (line_dist <= 3.5) & (radial <= 95)
    canopy[frond] = 210
    # Pinnae leaflets
    for r in range(25, 90, 8):
        leaflet = (np.abs(radial - r) <= 1.5) & (line_dist <= 14) & crown_mask
        canopy[leaflet] = 170

canopy_uint8 = np.clip(canopy + np.random.normal(0, 3, (h, w)), 0, 255).astype(np.uint8)

# Compute Gradients
# Sobel X & Y
sobel_x = cv2.Sobel(canopy_uint8, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(canopy_uint8, cv2.CV_64F, 0, 1, ksize=3)
sobel_mag = np.sqrt(sobel_x**2 + sobel_y**2)
sobel_mag_uint8 = np.clip(sobel_mag / sobel_mag.max() * 255.0, 0, 255).astype(np.uint8)

# Laplacian
blurred = cv2.GaussianBlur(canopy_uint8, (3, 3), 1.0)
laplacian = cv2.Laplacian(blurred, cv2.CV_64F, ksize=3)
laplacian_abs = np.clip(np.abs(laplacian) / np.abs(laplacian).max() * 255.0, 0, 255).astype(np.uint8)

# Canny Edge Detector
canny_edges = cv2.Canny(blurred, 40, 120)

# Panel 1: Original Palm Canopy
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(canopy_uint8, cmap='YlGn', vmin=0, vmax=255)
ax1.set_title('(a) Citra Ortofoto Kanopi Sawit\n(Input Grayscale)', fontsize=11, fontweight='bold', pad=8)
ax1.axis('off')

# Panel 2: Sobel Gradient X & Y Vector
ax2 = fig.add_subplot(gs[0, 1])
# Composite visualization: Sobel X in red channel, Sobel Y in green channel
sob_comp = np.zeros((h, w, 3), dtype=np.uint8)
sob_comp[:, :, 0] = np.clip(np.abs(sobel_x) / (np.abs(sobel_x).max() + 1e-6) * 255, 0, 255).astype(np.uint8) # Red: Horiz gradient
sob_comp[:, :, 1] = np.clip(np.abs(sobel_y) / (np.abs(sobel_y).max() + 1e-6) * 255, 0, 255).astype(np.uint8) # Green: Vert gradient
sob_comp[:, :, 2] = 40
ax2.imshow(sob_comp)
ax2.set_title('(b) Komposisi Gradien Sobel\n(Merah: |Gx|, Hijau: |Gy|)', fontsize=11, fontweight='bold', pad=8)
ax2.axis('off')

# Panel 3: Sobel Magnitude
ax3 = fig.add_subplot(gs[0, 2])
im3 = ax3.imshow(sobel_mag_uint8, cmap='hot')
ax3.set_title('(c) Magnitudo Gradien Sobel\n(||grad f|| = sqrt(Gx^2 + Gy^2))', fontsize=11, fontweight='bold', pad=8)
ax3.axis('off')
cbar3 = fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
cbar3.ax.tick_params(labelsize=8)

# Panel 4: Laplacian
ax4 = fig.add_subplot(gs[1, 0])
ax4.imshow(laplacian_abs, cmap='inferno')
ax4.set_title('(d) Operator Turunan Kedua Laplacian\n(Sensitif Terhadap Fluktuasi Halus)', fontsize=11, fontweight='bold', pad=8)
ax4.axis('off')

# Panel 5: Canny Multi-Stage Edge Detector
ax5 = fig.add_subplot(gs[1, 1])
ax5.imshow(canny_edges, cmap='gray')
ax5.set_title('(e) Canny Edge Detector (NMS + Histeresis)\n(Garis Tepi 1-Piksel Presisi & Kontinu)', fontsize=11, fontweight='bold', pad=8)
ax5.axis('off')

# Panel 6: Tahapan Algoritma Canny
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
canny_steps = (
    "MEKANISME MULTI-TAHAP DETEKTOR TEPI CANNY\n"
    "====================================================\n\n"
    "1. Gaussian Smoothing (sigma = 1.0):\n"
    "   - Mereduksi derau frekuensi tinggi agar tidak memicu\n"
    "     deteksi tepi semu (false positive).\n\n"
    "2. Kalkulasi Gradien Sobel:\n"
    "   - Menghitung magnitudo M(x, y) & orientasi sudut theta.\n"
    "   - theta = arctan(Gy / Gx) dibulatkan ke 4 sektor:\n"
    "     0 deg (Horizontal), 45 deg, 90 deg (Vertikal), 135 deg.\n\n"
    "3. Non-Maximum Suppression (NMS):\n"
    "   - Menipiskan batas tepi menjadi garis setebal 1 piksel.\n"
    "   - Mempertahankan piksel HANYA jika nilainya lokal\n"
    "     maksimum searah vektor gradien normal.\n\n"
    "4. Hysteresis Thresholding (T_low, T_high):\n"
    "   - Tepi kuat (Strong): M >= T_high (pasti tepi).\n"
    "   - Tepi lemah (Weak): T_low <= M < T_high.\n"
    "   - Edge tracking: Tepi lemah dipertahankan HANYA\n"
    "     jika terhubung secara spasial ke tepi kuat."
)
ax6.text(0.02, 0.95, canny_steps, fontsize=8.2, family='monospace', va='top', ha='left',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8f9fa', edgecolor='#bdc3c7', lw=1.5))
ax6.set_title('(f) Alur Algoritma Canny', fontsize=11, fontweight='bold', pad=8)

plt.suptitle('METODOLOGI DETEKSI TEPI DAN ANALISIS GRADIEN CITRA AGROKOMPLEKS:\nKOMPARASI OPERATOR SOBEL, LAPLACIAN, DAN CANNY PADA KANOPI SAWIT',
             fontsize=13, fontweight='bold', y=0.98)

output_path = 'docs/assets/deteksi_tepi_dan_gradien_citra_agrokompleks.png'
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Gambar berhasil dibuat di {output_path} (300 DPI)")
