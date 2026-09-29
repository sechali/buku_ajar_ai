import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Set style and DPI
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(16, 9), dpi=300)

# Create 2x3 grid
gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.25, left=0.06, right=0.96, top=0.92, bottom=0.08)

# 1. Generate Synthetic Low-Contrast Canopy Image
np.random.seed(42)
h, w = 200, 200
Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')

# Low-contrast foggy canopy: values clustered in narrow range [80, 130]
canopy_base = 105 + 18 * np.sin(X / 12.0) * np.cos(Y / 12.0) + np.random.normal(0, 5, (h, w))
# Add fronds/rachis structures
for angle in np.linspace(0, np.pi, 8):
    line = np.cos(angle)*(X - 100) + np.sin(angle)*(Y - 100)
    canopy_base += 12 * np.exp(- (line**2) / 40.0)

low_contrast_img = np.clip(canopy_base, 0, 255).astype(np.uint8)

# Global Histogram Equalization
hist_eq_img = cv2.equalizeHist(low_contrast_img)

# CLAHE
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
clahe_img = clahe.apply(low_contrast_img)

# Panel 1: Original Low-Contrast Citra Kanopi
ax1 = fig.add_subplot(gs[0, 0])
im1 = ax1.imshow(low_contrast_img, cmap='YlGn', vmin=0, vmax=255)
ax1.set_title('(a) Citra Asli Kanopi Berkabut\n(Low Dynamic Range)', fontsize=11, fontweight='bold', pad=8)
ax1.axis('off')
cbar1 = fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
cbar1.ax.tick_params(labelsize=8)

# Panel 2: Global Histogram Equalization
ax2 = fig.add_subplot(gs[0, 1])
im2 = ax2.imshow(hist_eq_img, cmap='YlGn', vmin=0, vmax=255)
ax2.set_title('(b) Global Histogram Equalization\n(Derau Latar Teramplifikasi)', fontsize=11, fontweight='bold', pad=8)
ax2.axis('off')
cbar2 = fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
cbar2.ax.tick_params(labelsize=8)

# Panel 3: CLAHE
ax3 = fig.add_subplot(gs[0, 2])
im3 = ax3.imshow(clahe_img, cmap='YlGn', vmin=0, vmax=255)
ax3.set_title('(c) CLAHE (Contrast-Limited Adaptive)\n(Detail Pelepah Optimal & Natural)', fontsize=11, fontweight='bold', pad=8)
ax3.axis('off')
cbar3 = fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
cbar3.ax.tick_params(labelsize=8)

# Panel 4: Perbandingan Histogram Intensitas
ax4 = fig.add_subplot(gs[1, 0])
h_orig, bins = np.histogram(low_contrast_img.ravel(), bins=64, range=(0, 256))
h_glob, _ = np.histogram(hist_eq_img.ravel(), bins=64, range=(0, 256))
h_clahe, _ = np.histogram(clahe_img.ravel(), bins=64, range=(0, 256))

bin_centers = 0.5 * (bins[:-1] + bins[1:])
ax4.plot(bin_centers, h_orig, color='#7f8c8d', lw=2, label='Asli (Terdistribusi Sempit)')
ax4.plot(bin_centers, h_glob, color='#e74c3c', lw=1.8, linestyle='--', label='Global Eq (Sparse/Kasar)')
ax4.plot(bin_centers, h_clahe, color='#27ae60', lw=2.2, label='CLAHE (Merata & Terkontrol)')
ax4.set_title('(d) Profil Distribusi Histogram', fontsize=11, fontweight='bold', pad=8)
ax4.set_xlabel('Intensitas Piksel [0 - 255]', fontsize=9)
ax4.set_ylabel('Frekuensi Piksel', fontsize=9)
ax4.legend(fontsize=8, loc='upper right')
ax4.set_xlim(0, 255)

# Panel 5: Geometri Affine Transform & Interpolasi
ax5 = fig.add_subplot(gs[1, 1])
# Demonstrate geometric interpolation artifacts
small_patch = low_contrast_img[80:120, 80:120]
# Scale up with Nearest vs Bicubic
scale_nearest = cv2.resize(small_patch, (200, 200), interpolation=cv2.INTER_NEAREST)
scale_cubic = cv2.resize(small_patch, (200, 200), interpolation=cv2.INTER_CUBIC)
composite_interp = np.zeros((200, 200), dtype=np.uint8)
composite_interp[:, :100] = scale_nearest[:, :100]
composite_interp[:, 100:] = scale_cubic[:, 100:]
ax5.imshow(composite_interp, cmap='YlGn')
ax5.axvline(100, color='red', linestyle='--', lw=2)
ax5.text(45, 185, 'Nearest\n(Bloky)', color='white', fontweight='bold', ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='black', alpha=0.6))
ax5.text(150, 185, 'Bicubic\n(Halus)', color='white', fontweight='bold', ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='black', alpha=0.6))
ax5.set_title('(e) Komparasi Interpolasi Resizing\n(Nearest Neighbor vs Bicubic)', fontsize=11, fontweight='bold', pad=8)
ax5.axis('off')

# Panel 6: Pipeline Normalisasi Input Deep Learning
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')

pipeline_text = (
    "PIPELINE NORMALISASI TENSOR CITRA AGROKOMPLEKS\n"
    "====================================================\n\n"
    "1. Citra Masukan Kamera / Drone:\n"
    "   - Format: NumPy uint8 [0, 255]\n"
    "   - Dimensi HWC: (H, W, 3)\n\n"
    "2. Penskalaan Rentang Min-Max [0.0, 1.0]:\n"
    "   - Formula: X_norm = X.astype(float32) / 255.0\n"
    "   - Menghindari numeric overflow pada gradien\n\n"
    "3. Standarisasi Distribusi Z-Score:\n"
    "   - Formula: Z = (X_norm - Mean) / Std\n"
    "   - Standar ImageNet:\n"
    "     Mean = [0.485, 0.456, 0.406]\n"
    "     Std  = [0.229, 0.224, 0.225]\n\n"
    "4. Transposisi Layout Tensor (CHW):\n"
    "   - OpenCV (H, W, C) -> PyTorch (C, H, W)\n"
    "   - Optimal untuk akselerasi GPU Tensor Core"
)
ax6.text(0.02, 0.95, pipeline_text, fontsize=8.5, family='monospace', va='top', ha='left',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8f9fa', edgecolor='#bdc3c7', lw=1.5))
ax6.set_title('(f) Arsitektur Normalisasi Data', fontsize=11, fontweight='bold', pad=8)

plt.suptitle('METODOLOGI PREPROCESSING CITRA AGROKOMPLEKS:\nTRANSFORMASI GEOMETRIS, PERBAIKAN KONTRAS (CLAHE), DAN NORMALISASI TENSOR',
             fontsize=13, fontweight='bold', y=0.98)

output_path = 'docs/assets/preprocessing_citra_dan_clahe_agrokompleks.png'
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Gambar berhasil dibuat di {output_path} (300 DPI)")
