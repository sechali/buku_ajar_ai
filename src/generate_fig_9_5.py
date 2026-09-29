import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Set style and DPI
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(16, 9), dpi=300)

gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.25, left=0.06, right=0.96, top=0.92, bottom=0.08)

# 1. Synthesize Clean Palm Leaf with Sharp Spine & Veins
np.random.seed(42)
h, w = 220, 220
Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')

clean_leaf = np.ones((h, w), dtype=np.float32) * 60
# Leaf blade mask
blade_mask = (Y >= 40) & (Y <= 180) & (np.abs(X - 110) <= 60 * np.sin((Y - 40) * np.pi / 140))
clean_leaf[blade_mask] = 140

# Central Rachis / Spine (bright line)
rachis_mask = blade_mask & (np.abs(X - 110) <= 3)
clean_leaf[rachis_mask] = 225

# Leaf veins (lateral angled lines)
for y_pos in range(55, 170, 15):
    line1 = np.abs((Y - y_pos) - 0.5 * (X - 110))
    line2 = np.abs((Y - y_pos) + 0.5 * (X - 110))
    clean_leaf[blade_mask & ((line1 < 1.5) | (line2 < 1.5))] = 185

clean_leaf_uint = np.clip(clean_leaf, 0, 255).astype(np.uint8)

# 2. Add Salt-and-Pepper Noise (sensor thermal impulsive noise)
noisy_leaf = clean_leaf_uint.copy()
num_salt = 400
num_pepper = 400
# Salt
y_salt = np.random.randint(0, h, num_salt)
x_salt = np.random.randint(0, w, num_salt)
noisy_leaf[y_salt, x_salt] = 255
# Pepper
y_pep = np.random.randint(0, h, num_pepper)
x_pep = np.random.randint(0, w, num_pepper)
noisy_leaf[y_pep, x_pep] = 0

# 3. Apply Filters
# Box Blur 5x5
box_filtered = cv2.blur(noisy_leaf, (5, 5))
# Gaussian Blur 5x5 (sigma = 1.5)
gaussian_filtered = cv2.GaussianBlur(noisy_leaf, (5, 5), 1.5)
# Median Filter 5x5
median_filtered = cv2.medianBlur(noisy_leaf, 5)
# Bilateral Filter (d=9, sigmaColor=75, sigmaSpace=75)
bilateral_filtered = cv2.bilateralFilter(noisy_leaf, 9, 75, 75)

# Panel 1: Citra Asli dengan Derau Impulsif
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(noisy_leaf, cmap='YlGn', vmin=0, vmax=255)
ax1.set_title('(a) Citra Daun Sawit Tercemar Derau\n(Salt-and-Pepper Sensor Noise)', fontsize=11, fontweight='bold', pad=8)
ax1.axis('off')

# Panel 2: Box Filter (Rata-rata 5x5)
ax2 = fig.add_subplot(gs[0, 1])
ax2.imshow(box_filtered, cmap='YlGn', vmin=0, vmax=255)
ax2.set_title('(b) Box Filter 5x5 (Mean Blur)\n(Derau Melebar, Tepi Menjadi Kabur)', fontsize=11, fontweight='bold', pad=8)
ax2.axis('off')

# Panel 3: Gaussian Filter 5x5
ax3 = fig.add_subplot(gs[0, 2])
ax3.imshow(gaussian_filtered, cmap='YlGn', vmin=0, vmax=255)
ax3.set_title('(c) Gaussian Filter 5x5 (sigma=1.5)\n(Halus Alami, Namun Derau Tetap Ada)', fontsize=11, fontweight='bold', pad=8)
ax3.axis('off')

# Panel 4: Median Filter 5x5
ax4 = fig.add_subplot(gs[1, 0])
ax4.imshow(median_filtered, cmap='YlGn', vmin=0, vmax=255)
ax4.set_title('(d) Median Filter 5x5\n(Derau Impulsif Hilang 100%, Tepi Terjaga)', fontsize=11, fontweight='bold', pad=8)
ax4.axis('off')

# Panel 5: Bilateral Filter
ax5 = fig.add_subplot(gs[1, 1])
ax5.imshow(bilateral_filtered, cmap='YlGn', vmin=0, vmax=255)
ax5.set_title('(e) Bilateral Filter (Edge-Preserving)\n(Permukaan Daun Halus, Tulang Daun Tajam)', fontsize=11, fontweight='bold', pad=8)
ax5.axis('off')

# Panel 6: Profil Intensitas Melintang Penampang Daun (1D Cross-Section Profile)
ax6 = fig.add_subplot(gs[1, 2])
y_line = 110
ax6.plot(clean_leaf_uint[y_line, :], color='black', lw=2.0, label='Asli Bersih (Ground Truth)')
ax6.plot(box_filtered[y_line, :], color='#e74c3c', lw=1.5, linestyle='--', label='Box Filter (Tepi Rusak)')
ax6.plot(median_filtered[y_line, :], color='#27ae60', lw=2.2, label='Median Filter (Presisi Optimal)')
ax6.axvline(110, color='blue', linestyle=':', label='Pusat Pelepah (Rachis)')
ax6.set_title('(f) Profil Intensitas Penampang Melintang Daun', fontsize=11, fontweight='bold', pad=8)
ax6.set_xlabel('Posisi Spasial Piksel Horizontal (X)', fontsize=9)
ax6.set_ylabel('Nilai Intensitas Piksel [0 - 255]', fontsize=9)
ax6.legend(fontsize=8, loc='upper right')
ax6.set_xlim(50, 170)

plt.suptitle('ANALISIS FILTER SPASIAL DAN KONVOLUSI 2D PADA CITRA AGROKOMPLEKS:\nKOMPARASI FILTER LINIER (BOX, GAUSSIAN) VS FILTER NON-LINIER (MEDIAN, BILATERAL)',
             fontsize=13, fontweight='bold', y=0.98)

output_path = 'docs/assets/operasi_filter_spasial_dan_konvolusi_2d_agrokompleks.png'
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Gambar berhasil dibuat di {output_path} (300 DPI)")
