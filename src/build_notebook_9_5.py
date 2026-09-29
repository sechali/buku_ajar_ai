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

add_md('''# Praktikum AI Modul 9.5: Operasi Filter Spasial dan Konvolusi 2D
**Program Studi Teknik Pertanian / Agroteknologi - Fakultas Pertanian & Teknologi Pertanian**  
*Materi: Konvolusi 2D Diskrit, Boundary Padding, Filter Linier (Box & Gaussian Separable), Filter Non-Linier (Median & Bilateral Filter), serta Penajaman Unsharp Masking pada Citra Daun Kelapa Sawit.*

---
### Tujuan Praktikum
1. Memahami mekanisme operasi konvolusi spasial 2D manual dan penanganan batas (*boundary padding*).
2. Membandingkan karakteristik reduksi derau antara filter linier (*Box, Gaussian*) dan filter non-linier (*Median, Bilateral*).
3. Membuktikan keunggulan *Median Filter* dalam mengeliminasi derau impulsif (*salt-and-pepper*) pada sensor drone.
4. Menganalisis sifat preservasi tepi (*edge-preserving*) pada *Bilateral Filter* menggunakan profil penampang intensitas 1D.
5. Mengimplementasikan penajaman kontur pelepah sawit menggunakan teknik *Unsharp Masking* bebas aritmatika *overflow*.''')

add_code('''import cv2
import numpy as np
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print(f"OpenCV Version : {cv2.__version__}")
print(f"NumPy Version  : {np.__version__}")''')

add_md('''## 1. Pembuatan Dataset Sintetis: Daun Sawit Bersih dan Tercemar Derau Impulsif
Kita memodelkan daun kelapa sawit dengan tulang daun utama (*rachis*), urat-urat daun lateral, dan menyimulasikan kontaminasi derau *salt-and-pepper* akibat panas sensor drone perkebunan.''')

add_code('''def generate_palm_leaf_dataset():
    np.random.seed(42)
    h, w = 240, 240
    Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    
    # 1. Background tanah gelap
    clean_leaf = np.ones((h, w), dtype=np.uint8) * 45
    
    # 2. Helaian daun kelapa sawit (lamina)
    blade = (Y >= 30) & (Y <= 210) & (np.abs(X - 120) <= 65 * np.sin((Y - 30) * np.pi / 180))
    clean_leaf[blade] = 130
    
    # 3. Rachis (tulang daun tengah) yang terang
    clean_leaf[blade & (np.abs(X - 120) <= 3)] = 230
    
    # 4. Pola urat pelepah lateral bersudut
    for y_pos in range(45, 200, 18):
        l1 = np.abs((Y - y_pos) - 0.5 * (X - 120))
        l2 = np.abs((Y - y_pos) + 0.5 * (X - 120))
        clean_leaf[blade & ((l1 < 1.5) | (l2 < 1.5))] = 175
        
    # 5. Tambahkan derau Salt-and-Pepper
    noisy_leaf = clean_leaf.copy()
    num_noise = 600
    # Salt (Piksel rusak putih 255)
    ys = np.random.randint(0, h, num_noise)
    xs = np.random.randint(0, w, num_noise)
    noisy_leaf[ys, xs] = 255
    # Pepper (Piksel rusak hitam 0)
    yp = np.random.randint(0, h, num_noise)
    xp = np.random.randint(0, w, num_noise)
    noisy_leaf[yp, xp] = 0
    
    return clean_leaf, noisy_leaf

clean_leaf, noisy_leaf = generate_palm_leaf_dataset()
print(f"Dataset berhasil dibuat: clean_leaf min={clean_leaf.min()}, max={clean_leaf.max()}")
print(f"Jumlah piksel garam/lada: {np.sum((noisy_leaf == 255) | (noisy_leaf == 0))} piksel")''')

add_md('''## 2. Implementasi Konvolusi 2D Diskrit Manual vs OpenCV `filter2D`
Kita mengonstruksi fungsi konvolusi manual dengan *replicate padding* untuk memahami kalkulasi matematis *sliding window*, lalu membandingkan hasil numerik dan kecepatannya terhadap `cv2.filter2D`.''')

add_code('''def manual_convolution_2d(image, kernel):
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h = kh // 2
    pad_w = kw // 2
    
    # Replicate padding (meniru cv2.BORDER_REPLICATE)
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge').astype(np.float32)
    output = np.zeros((h, w), dtype=np.float32)
    
    # Rotasi kernel 180 derajat untuk konvolusi murni
    flipped_kernel = np.flipud(np.fliplr(kernel))
    
    for i in range(h):
        for j in range(w):
            roi = padded[i : i + kh, j : j + kw]
            output[i, j] = np.sum(roi * flipped_kernel)
            
    return np.clip(output, 0, 255).astype(np.uint8)

# Uji dengan kernel penajam 3x3
sharpen_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
], dtype=np.float32)

t0 = time.perf_counter()
res_manual = manual_convolution_2d(clean_leaf, sharpen_kernel)
t_manual = time.perf_counter() - t0

t0 = time.perf_counter()
for _ in range(50):
    res_cv2 = cv2.filter2D(clean_leaf, -1, sharpen_kernel, borderType=cv2.BORDER_REPLICATE)
t_cv2 = (time.perf_counter() - t0) / 50.0

max_diff = np.max(np.abs(res_manual.astype(np.int32) - res_cv2.astype(np.int32)))
speedup = t_manual / max(t_cv2, 1e-6)
print(f"Hasil Manual vs OpenCV: Perbedaan Maksimum = {max_diff} piksel (Identik!)")
print(f"Waktu Manual Python : {t_manual:.4f} detik")
print(f"Waktu OpenCV C++    : {t_cv2:.6f} detik (Percepatan ~{speedup:.1f}x)")''')

add_md('''## 3. Komparasi Filter Linier (Box, Gaussian) vs Non-Linier (Median, Bilateral)
Kita menguji performa keempat filter dalam meredam derau sensor *salt-and-pepper* pada citra daun sawit.''')

add_code('''# 1. Box Filter 5x5
img_box = cv2.blur(noisy_leaf, (5, 5))

# 2. Gaussian Blur 5x5 (sigma=1.5)
img_gaussian = cv2.GaussianBlur(noisy_leaf, (5, 5), sigmaX=1.5)

# 3. Median Filter 5x5
img_median = cv2.medianBlur(noisy_leaf, 5)

# 4. Bilateral Filter (d=9, sigmaColor=75, sigmaSpace=75)
img_bilateral = cv2.bilateralFilter(noisy_leaf, d=9, sigmaColor=75, sigmaSpace=75)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

axes[0, 0].imshow(clean_leaf, cmap='YlGn', vmin=0, vmax=255)
axes[0, 0].set_title("Ground Truth Daun Bersih")

axes[0, 1].imshow(noisy_leaf, cmap='YlGn', vmin=0, vmax=255)
axes[0, 1].set_title("Tercemar Derau Impulsif (Input)")

axes[0, 2].imshow(img_box, cmap='YlGn', vmin=0, vmax=255)
axes[0, 2].set_title("Box Filter 5x5 (Derau Melebar!)")

axes[1, 0].imshow(img_gaussian, cmap='YlGn', vmin=0, vmax=255)
axes[1, 0].set_title("Gaussian Blur 5x5 (Derau Sisa)")

axes[1, 1].imshow(img_median, cmap='YlGn', vmin=0, vmax=255)
axes[1, 1].set_title("Median Filter 5x5 (Derau Hilang Total!)")

axes[1, 2].imshow(img_bilateral, cmap='YlGn', vmin=0, vmax=255)
axes[1, 2].set_title("Bilateral Filter (Tepi Tetap Tajam)")

for ax in axes.ravel():
    ax.axis('off')

plt.tight_layout()
plt.savefig('docs/assets/notebook_9_5_filtering_comparison.png', dpi=150)
plt.close()
print("Hasil visualisasi filtering tersimpan di docs/assets/notebook_9_5_filtering_comparison.png")''')

add_md('''## 4. Analisis Penampang Melintang 1D (Edge Preservation Analysis)
Kita mengambil profil intensitas satu baris horizontal ($y = 110$) yang memotong batas luar lamina daun dan tulang daun pusat (*rachis*) untuk membuktikan preservasi tepi secara kuantitatif.''')

add_code('''y_slice = 110
x_range = np.arange(60, 180)

plt.figure(figsize=(12, 5))
plt.plot(x_range, clean_leaf[y_slice, x_range], label='Ground Truth Bersih', color='black', lw=2.5)
plt.plot(x_range, img_box[y_slice, x_range], label='Box Filter (Tepi Tumpul)', color='#e74c3c', lw=1.8, linestyle='--')
plt.plot(x_range, img_median[y_slice, x_range], label='Median Filter (Presisi Optimal)', color='#27ae60', lw=2.0)
plt.plot(x_range, img_bilateral[y_slice, x_range], label='Bilateral Filter', color='#2980b9', lw=1.8, linestyle=':')

plt.title("Profil Intensitas Penampang Melintang Pelepah Daun Sawit (y=110)", fontsize=12, fontweight='bold')
plt.xlabel("Posisi Piksel Horizontal (X)", fontsize=10)
plt.ylabel("Nilai Intensitas [0 - 255]", fontsize=10)
plt.axvline(120, color='orange', linestyle='--', alpha=0.7, label='Pusat Rachis (X=120)')
plt.legend(fontsize=9, loc='upper right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/assets/notebook_9_5_edge_profile.png', dpi=150)
plt.close()
print("Grafik profil tepi tersimpan di docs/assets/notebook_9_5_edge_profile.png")''')

add_md('''## 5. Implementasi Penajaman Citra: Unsharp Masking
Kita mengimplementasikan algoritma *Unsharp Masking* bebas *integer overflow* untuk menonjolkan urat daun pelepah sawit.''')

add_code('''def unsharp_mask(image, sigma=1.5, strength=1.5):
    # 1. Pelembutan Gaussian
    blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=sigma)
    
    # 2. Masker detail (High-pass) menggunakan float32
    mask = image.astype(np.float32) - blurred.astype(np.float32)
    
    # 3. Penajaman dan clipping saturasi
    sharpened = image.astype(np.float32) + strength * mask
    sharpened_uint8 = np.clip(sharpened, 0, 255).astype(np.uint8)
    
    # Normalisasi masker untuk visualisasi
    mask_vis = np.clip(mask + 128, 0, 255).astype(np.uint8)
    return sharpened_uint8, mask_vis

leaf_sharp, highpass_mask = unsharp_mask(clean_leaf, sigma=1.5, strength=1.8)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].imshow(clean_leaf, cmap='YlGn', vmin=0, vmax=255)
axes[0].set_title("Citra Daun Asli")
axes[1].imshow(highpass_mask, cmap='gray')
axes[1].set_title("Masker Detail Frekuensi Tinggi")
axes[2].imshow(leaf_sharp, cmap='YlGn', vmin=0, vmax=255)
axes[2].set_title("Hasil Unsharp Masking (Urat Tajam)")

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.savefig('docs/assets/notebook_9_5_unsharp_masking.png', dpi=150)
plt.close()
print("Hasil unsharp masking tersimpan di docs/assets/notebook_9_5_unsharp_masking.png")''')

add_md('''## 6. Latihan Mandiri dan Evaluasi Kuantitatif Metrik PSNR

### Latihan 1: Evaluasi Kualitas Reduksi Derau Berbasis PSNR (*Peak Signal-to-Noise Ratio*)
Hitung nilai metrik PSNR antara citra hasil restorasi (*Box, Gaussian, Median, Bilateral*) terhadap citra asli bersih (*Ground Truth*):

$$MSE = \\frac{1}{H \\times W} \\sum_{i=1}^{H} \\sum_{j=1}^{W} [f_{\\text{clean}}(i, j) - f_{\\text{filtered}}(i, j)]^2$$
$$PSNR = 10 \\cdot \\log_{10}\\left( \\frac{255^2}{MSE} \\right) \\quad [\\text{dB}]$$''')

add_code('''# Solusi Latihan 1: Kalkulasi PSNR Komparatif
def calculate_psnr(clean_img, test_img):
    mse = np.mean((clean_img.astype(np.float64) - test_img.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    return 10.0 * np.log10((max_pixel ** 2) / mse)

psnr_noisy = calculate_psnr(clean_leaf, noisy_leaf)
psnr_box = calculate_psnr(clean_leaf, img_box)
psnr_gaussian = calculate_psnr(clean_leaf, img_gaussian)
psnr_median = calculate_psnr(clean_leaf, img_median)
psnr_bilateral = calculate_psnr(clean_leaf, img_bilateral)

print("=== EVALUASI KUANTITATIF KUALITAS RESTORASI CITRA ===")
print(f"PSNR Citra Berderau (Input) : {psnr_noisy:.2f} dB")
print(f"PSNR Box Filter 5x5         : {psnr_box:.2f} dB")
print(f"PSNR Gaussian Filter 5x5    : {psnr_gaussian:.2f} dB")
print(f"PSNR Bilateral Filter       : {psnr_bilateral:.2f} dB")
print(f"PSNR Median Filter 5x5      : {psnr_median:.2f} dB (PERFORMA TERTINGGI!)")''')

with open('notebooks/part-09/AI_Modul_9.5_Praktikum_Operasi_Filter_Spasial_dan_Konvolusi_2D.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print('Notebook Modul 9.5 berhasil dibuat!')
