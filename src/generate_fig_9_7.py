import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cv2

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(16, 9), dpi=300)

gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.25, left=0.06, right=0.96, top=0.92, bottom=0.08)

# 1. Synthesize Binary Oil Palm Fruit Bunch / Canopy with Holes & Noise
np.random.seed(42)
h, w = 240, 240
Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')

# True Object: 3 palm fruit spikelets / canopy crowns
obj1 = ((X - 80)**2 / 45**2 + (Y - 90)**2 / 55**2) <= 1.0
obj2 = ((X - 160)**2 / 50**2 + (Y - 140)**2 / 60**2) <= 1.0
raw_binary = (obj1 | obj2).astype(np.uint8) * 255

# Add internal holes (defects / shadow occlusions)
holes = ((X - 80)**2 + (Y - 90)**2 <= 12**2) | ((X - 160)**2 + (Y - 145)**2 <= 14**2)
raw_binary[holes] = 0

# Add external small noise specks (weeds / dust)
noise_specks = (np.random.rand(h, w) > 0.985) & (~(obj1 | obj2))
raw_binary[noise_specks] = 255

# Morphological Operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

# Opening (Erosion then Dilation): removes external noise
opened = cv2.morphologyEx(raw_binary, cv2.MORPH_OPEN, kernel)

# Closing (Dilation then Erosion): closes internal holes
closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

# Morphological Gradient (Dilation - Erosion): boundary extraction
dilated = cv2.dilate(closed, kernel)
eroded = cv2.erode(closed, kernel)
morph_grad = dilated - eroded

# Contours & Geometric Fitting
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_vis = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)

for cnt in contours:
    # Centroid
    M = cv2.moments(cnt)
    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(contour_vis, (cx, cy), 4, (0, 0, 255), -1)
        
    # Oriented Bounding Box (Rotated Rect)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(contour_vis, [box], 0, (0, 255, 0), 2)
    
    # Minimum Enclosing Circle
    (x_c, y_c), radius = cv2.minEnclosingCircle(cnt)
    cv2.circle(contour_vis, (int(x_c), int(y_c)), int(radius), (255, 120, 0), 1)

# Panel 1: Citra Biner Mentah dengan Lubang & Derau
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(raw_binary, cmap='gray')
ax1.set_title('(a) Mask Biner Mentah Kanopi/Buah\n(Tercemar Lubang & Derau Luar)', fontsize=11, fontweight='bold', pad=8)
ax1.axis('off')

# Panel 2: Operasi Pembukaan (Opening)
ax2 = fig.add_subplot(gs[0, 1])
ax2.imshow(opened, cmap='gray')
ax2.set_title('(b) Morfologi Opening (Erosi -> Dilasi)\n(Derau Luar Tereliminasi Bersih)', fontsize=11, fontweight='bold', pad=8)
ax2.axis('off')

# Panel 3: Operasi Penutupan (Closing)
ax3 = fig.add_subplot(gs[0, 2])
ax3.imshow(closed, cmap='gray')
ax3.set_title('(c) Morfologi Closing (Dilasi -> Erosi)\n(Lubang Internal Tertutup Sempurna)', fontsize=11, fontweight='bold', pad=8)
ax3.axis('off')

# Panel 4: Gradien Morfologis
ax4 = fig.add_subplot(gs[1, 0])
ax4.imshow(morph_grad, cmap='inferno')
ax4.set_title('(d) Gradien Morfologis (Dilasi - Erosi)\n(Garis Batas Objek Biner Presisi)', fontsize=11, fontweight='bold', pad=8)
ax4.axis('off')

# Panel 5: Kontur & Deskriptor Bentuk Geometris
ax5 = fig.add_subplot(gs[1, 1])
ax5.imshow(cv2.cvtColor(contour_vis, cv2.COLOR_BGR2RGB))
ax5.set_title('(e) Ekstraksi Morfometri Geometri\n(Hijau: Rotated Box, Oranye: Min Circle, Merah: Centroid)', fontsize=10, fontweight='bold', pad=8)
ax5.axis('off')

# Panel 6: Metrik Deskriptor Bentuk
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
desc_text = (
    "DESKRIPTOR MORFOMETRI CITRA AGROKOMPLEKS\n"
    "====================================================\n\n"
    "1. Luas Area Tajuk / Buah (Area A):\n"
    "   - A = cv2.contourArea(cnt) [piksel^2]\n"
    "   - A_riil = A * GSD^2 [m^2] (Crown Projection Area)\n\n"
    "2. Keliling Perimeter (P):\n"
    "   - P = cv2.arcLength(cnt, closed=True) [piksel]\n\n"
    "3. Titik Pusat Massa / Centroid (cx, cy):\n"
    "   - cx = m_10 / m_00, cy = m_01 / m_00\n"
    "   - Koordinat spasial posisi batang pohon sawit\n\n"
    "4. Rasio Kebulatan (Circularity C):\n"
    "   - C = (4 * pi * A) / (P^2)\n"
    "   - C = 1.0 (Lingkaran sempurna / Sawit sehat simetris)\n"
    "   - C << 1.0 (Elongasi / Tandan buah pipih / Tajuk rusak)\n\n"
    "5. Kerapatan Kontur (Solidity S):\n"
    "   - S = Area / ConvexHull_Area (Deteksi lekukan pelepah)"
)
ax6.text(0.02, 0.95, desc_text, fontsize=8.2, family='monospace', va='top', ha='left',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8f9fa', edgecolor='#bdc3c7', lw=1.5))
ax6.set_title('(f) Deskriptor Bentuk Agronomi', fontsize=11, fontweight='bold', pad=8)

plt.suptitle('METODOLOGI EKSTRAKSI FITUR DAN OPERASI MORFOLOGI CITRA AGROKOMPLEKS:\nPEMBERSIHAN MASKER, PELACAKAN KONTUR, DAN ANALISIS MORFOMETRI KANOPI',
             fontsize=13, fontweight='bold', y=0.98)

output_path = 'docs/assets/ekstraksi_fitur_dan_morfologi_citra_agrokompleks.png'
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Gambar berhasil dibuat di {output_path} (300 DPI)")
