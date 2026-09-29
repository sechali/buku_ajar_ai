import matplotlib
matplotlib.use('Agg')

import numpy as np
import cv2
import matplotlib.pyplot as plt

# Konfigurasi visualisasi
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
print(f'OpenCV Version : {cv2.__version__}')
print(f'NumPy Version  : {np.__version__}')


width, height = 300, 300
palm_fruit = np.ones((height, width, 3), dtype=np.uint8) * 35  # Background gelap

Y, X = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
cy, cx = height // 2, width // 2

# Geometri elips brondolan sawit
a, b = 100.0, 70.0
mask = ((X - cx) / b)**2 + ((Y - cy) / a)**2 <= 1.0

y_norm = np.clip((Y - (cy - a)) / (2 * a), 0.0, 1.0)
# Saluran Merah (R): Tinggi di badan buah
palm_fruit[mask, 0] = np.clip(180 + 75 * (1.0 - y_norm[mask]), 0, 255).astype(np.uint8)
# Saluran Hijau (G): Gradasi kematangan menuju dasar
palm_fruit[mask, 1] = np.clip(35 + 85 * (1.0 - y_norm[mask]**2), 0, 255).astype(np.uint8)
# Saluran Biru (B): Rendah khas buah sawit matang
palm_fruit[mask, 2] = np.clip(15 + 15 * y_norm[mask], 0, 255).astype(np.uint8)

print('=== PROFIL TENSOR CITRA SAWIT ===')
print(f'Dimensi Array (H, W, C) : {palm_fruit.shape}')
print(f'Tipe Data Elemen        : {palm_fruit.dtype}')
print(f'Ukuran Memori Total     : {palm_fruit.nbytes:,} Bytes ({palm_fruit.nbytes / 1024:.2f} KB)')
print(f'Rentang Nilai Intensitas: Min = {palm_fruit.min()}, Max = {palm_fruit.max()}')


# Ekstraksi ROI Bagian Inti Buah Sawit Menggunakan .copy()
ymin, ymax = 100, 200
xmin, xmax = 100, 200
roi_safe = palm_fruit[ymin:ymax, xmin:xmax].copy()

# Ekstraksi ROI View (Referensi Berbahaya)
fruit_demo = palm_fruit.copy()
roi_view = fruit_demo[ymin:ymax, xmin:xmax]
# Mengubah ROI view menjadi putih pekat
roi_view[:, :] = [255, 255, 255]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].imshow(palm_fruit)
axes[0].set_title('(A) Citra Asli Utuh')
axes[0].axis('off')

axes[1].imshow(roi_safe)
axes[1].set_title(f'(B) ROI Terisolasi (.copy()) {roi_safe.shape}')
axes[1].axis('off')

axes[2].imshow(fruit_demo)
axes[2].set_title('(C) Dampak Mutasi Memori pada View')
axes[2].axis('off')
plt.tight_layout()
plt.show()


# Uji Penambahan Kecerahan +60 pada Citra Sawit
brightness_bias = 60

# Alternatif A: NumPy Add (Modulo 256)
img_numpy_overflow = palm_fruit + brightness_bias

# Alternatif B: OpenCV Add (Saturasi [0, 255])
bias_array = np.full(palm_fruit.shape, brightness_bias, dtype=np.uint8)
img_opencv_saturated = cv2.add(palm_fruit, bias_array)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].imshow(palm_fruit)
axes[0].set_title('(A) Citra Asli (Rerata = {:.1f})'.format(palm_fruit.mean()))
axes[0].axis('off')

axes[1].imshow(img_numpy_overflow)
axes[1].set_title('(B) NumPy Add (Cacat Overflow Modulo)')
axes[1].axis('off')

axes[2].imshow(img_opencv_saturated)
axes[2].set_title('(C) OpenCV Add (Saturasi Sempurna)')
axes[2].axis('off')
plt.tight_layout()
plt.show()


def gamma_correction(image, gamma=1.0):
    inv_gamma = 1.0 / gamma
    lut = np.array([
        np.clip(((i / 255.0) ** inv_gamma) * 255.0, 0, 255)
        for i in range(256)
    ], dtype=np.uint8)
    return cv2.LUT(image, lut)

# Uji Tiga Nilai Gamma
fruit_gamma_05 = gamma_correction(palm_fruit, gamma=0.5)  # Meredam silau / menggelapkan
fruit_gamma_10 = gamma_correction(palm_fruit, gamma=1.0)  # Identitas
fruit_gamma_22 = gamma_correction(palm_fruit, gamma=2.2)  # Mencerahkan bayangan gelap

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].imshow(fruit_gamma_05)
axes[0].set_title('(A) Gamma = 0.5 (Peredaman Highlights)')
axes[0].axis('off')

axes[1].imshow(fruit_gamma_10)
axes[1].set_title('(B) Gamma = 1.0 (Identitas Asli)')
axes[1].axis('off')

axes[2].imshow(fruit_gamma_22)
axes[2].set_title('(C) Gamma = 2.2 (Pencerahan Detail Bayangan)')
axes[2].axis('off')
plt.tight_layout()
plt.show()


def quantize_bits(image, bits):
    levels = 2 ** bits
    step = 256 // levels
    return ((image // step) * step).astype(np.uint8)

fruit_8bit = palm_fruit
fruit_4bit = quantize_bits(palm_fruit, bits=4)  # 16 Level
fruit_2bit = quantize_bits(palm_fruit, bits=2)  # 4 Level

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].imshow(fruit_8bit)
axes[0].set_title('(A) Kedalaman 8-bit (256 Tingkat Warna)')
axes[0].axis('off')

axes[1].imshow(fruit_4bit)
axes[1].set_title('(B) Kedalaman 4-bit (16 Tingkat: Muncul Banding)')
axes[1].axis('off')

axes[2].imshow(fruit_2bit)
axes[2].set_title('(C) Kedalaman 2-bit (4 Tingkat: Kontur Palsu Parah)')
axes[2].axis('off')
plt.tight_layout()
plt.show()
