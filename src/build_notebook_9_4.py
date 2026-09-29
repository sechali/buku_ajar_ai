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

add_md('''# Praktikum AI Modul 9.4: Preprocessing Citra (Image Preprocessing)
**Program Studi Teknik Pertanian / Agroteknologi - Fakultas Pertanian & Teknologi Pertanian**  
*Materi: Transformasi Geometris (Interpolasi Nearest, Bilinear, Bicubic), Transformasi Affine (Rotasi & ROI Cropping), Perbaikan Kontras Adaptif (CLAHE pada CIE Lab), dan Normalisasi Tensor Deep Learning.*

---
### Tujuan Praktikum
1. Menganalisis perbedaan kualitas spasial dan beban komputasi dari metode interpolasi Nearest Neighbor, Bilinear, dan Bicubic.
2. Mengembangkan fungsi transformasi affine 2D untuk mengoreksi sudut kemiringan barisan tanaman kelapa sawit pada citra drone.
3. Mengoreksi citra ortofoto berkabut menggunakan algoritma CLAHE pada kanal Luminans ($L^*$) tanpa merusak rasio krominans biokimia daun.
4. Membangun alur pipa pra-pemrosesan tensor terstandarisasi ($Z$-score dan format memori *channel-first*) yang siap diintegrasikan ke arsitektur Deep Learning.
5. Membuktikan pentingnya integritas kelas pada data masker segmentasi kategorikal saat proses resizing.''')

add_code('''import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print(f"OpenCV Version : {cv2.__version__}")
print(f"NumPy Version  : {np.__version__}")''')

add_md('''## 1. Pembuatan Dataset Sintetis: Ortofoto Drone Kanopi Kelapa Sawit Berkabut
Kita mensimulasikan citra ortofoto perkebunan kelapa sawit berdimensi $400 \\times 400$ piksel dengan kondisi kabut radiasi pagi hari (kontras rendah: intensitas piksel mengumpul pada rentang sempit $[70, 130]$).''')

add_code('''def generate_foggy_palm_canopy():
    np.random.seed(42)
    h, w = 400, 400
    Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    
    # 1. Base canopy texture (low contrast foliage)
    base_green = 90 + 15 * np.sin(X / 15.0) * np.cos(Y / 15.0) + np.random.normal(0, 4, (h, w))
    
    # 2. Tambahkan struktur pelepah radial kanopi pohon sawit di pusat
    cx, cy = 200, 200
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        # Garis pelepah
        line_dist = np.abs(np.cos(angle) * (X - cx) + np.sin(angle) * (Y - cy))
        radial_dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
        frond_mask = (line_dist < 4) & (radial_dist < 150)
        base_green[frond_mask] += 22 * (1.0 - radial_dist[frond_mask] / 150.0)
        
    # 3. Bentuk citra BGR berkabut (kontras rendah)
    foggy_bgr = np.zeros((h, w, 3), dtype=np.uint8)
    foggy_bgr[:, :, 0] = np.clip(base_green * 0.7 + 35, 0, 255).astype(np.uint8)  # Blue
    foggy_bgr[:, :, 1] = np.clip(base_green * 1.1 + 10, 0, 255).astype(np.uint8)  # Green
    foggy_bgr[:, :, 2] = np.clip(base_green * 0.6 + 25, 0, 255).astype(np.uint8)  # Red
    
    # 4. Tambahkan masker ground truth segmentasi (0: Tanah, 1: Kanopi Sawit)
    palm_mask = (np.sqrt((X - cx)**2 + (Y - cy)**2) <= 140).astype(np.uint8)
    
    return foggy_bgr, palm_mask

foggy_bgr, true_palm_mask = generate_foggy_palm_canopy()
foggy_rgb = cv2.cvtColor(foggy_bgr, cv2.COLOR_BGR2RGB)
print(f"Citra sintetis berhasil digenerasi: shape={foggy_bgr.shape}, dtype={foggy_bgr.dtype}")
print(f"Rentang intensitas: min={foggy_bgr.min()}, max={foggy_bgr.max()}")''')

add_md('''## 2. Eksperimen Interpolasi Spasial pada Penskalaan Citra (Resizing)
Kita menguji tiga algoritma interpolasi pada pembesaran detail pelepah daun sawit ($4\\times$ zoom):
1. **Nearest Neighbor** (`cv2.INTER_NEAREST`)
2. **Bilinear** (`cv2.INTER_LINEAR`)
3. **Bicubic** (`cv2.INTER_CUBIC`)''')

add_code('''# Ekstrak patch detail pelepah berukuran 50x50 di dekat pusat
patch = foggy_rgb[180:230, 180:230]

# Upscaling 4x (50x50 -> 200x200)
patch_nearest = cv2.resize(patch, (200, 200), interpolation=cv2.INTER_NEAREST)
patch_bilinear = cv2.resize(patch, (200, 200), interpolation=cv2.INTER_LINEAR)
patch_bicubic = cv2.resize(patch, (200, 200), interpolation=cv2.INTER_CUBIC)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
axes[0].imshow(patch)
axes[0].set_title(f"Patch Asli ({patch.shape[0]}x{patch.shape[1]})")
axes[1].imshow(patch_nearest)
axes[1].set_title("Nearest Neighbor (Tampak Blok/Tangga)")
axes[2].imshow(patch_bilinear)
axes[2].set_title("Bilinear (Cukup Halus)")
axes[3].imshow(patch_bicubic)
axes[3].set_title("Bicubic (Paling Halus & Natural)")

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.savefig('docs/assets/notebook_9_4_interpolations.png', dpi=150)
plt.close()
print("Hasil visualisasi interpolasi tersimpan di docs/assets/notebook_9_4_interpolations.png")''')

add_md('''## 3. Transformasi Affine: Koreksi Sudut Orientasi Kanopi & ROI Cropping
Kita memformulasikan matriks rotasi $2 \\times 3$ untuk menyelaraskan pelepah sawit yang miring $25^\\circ$ terhadap sumbu referensi ortogonal.''')

add_code('''# Koreksi rotasi 25 derajat terhadap pusat citra (cx=200, cy=200)
cx, cy = 200, 200
angle = 25.0
scale = 1.0

# Dapatkan matriks affine 2x3 dari OpenCV
M_rot = cv2.getRotationMatrix2D((cx, cy), angle, scale)
print("Matriks Transformasi Affine 2x3:\\n", M_rot)

# Terapkan transformasi affine
rotated_canopy = cv2.warpAffine(foggy_bgr, M_rot, (400, 400), flags=cv2.INTER_LINEAR)

# Ekstraksi Region of Interest (ROI) kanopi inti 200x200
roi_canopy = rotated_canopy[100:300, 100:300].copy()

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
axes[0].imshow(cv2.cvtColor(foggy_bgr, cv2.COLOR_BGR2RGB))
axes[0].set_title("Citra Asli Miring")
axes[1].imshow(cv2.cvtColor(rotated_canopy, cv2.COLOR_BGR2RGB))
axes[1].set_title(f"Rotasi Terkoreksi (+{angle} deg)")
axes[2].imshow(cv2.cvtColor(roi_canopy, cv2.COLOR_BGR2RGB))
axes[2].set_title("ROI Cropped (200x200)")

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.savefig('docs/assets/notebook_9_4_affine_crop.png', dpi=150)
plt.close()
print("Hasil rotasi dan cropping tersimpan di docs/assets/notebook_9_4_affine_crop.png")''')

add_md('''## 4. Peningkatan Kontras Adaptif: CLAHE pada Ruang CIE $L^*a^*b^*$ vs Global Histogram Equalization
Kita membandingkan:
1. **Kegagalan Global Histogram Equalization** pada citra berwarna (distorsi warna dan amplifikasi derau).
2. **Keberhasilan CLAHE pada Kanal $L^*$** (mempertahankan kesetiaan warna biokimia daun sambil menonjolkan urat pelepah).''')

add_code('''# 1. Kesalahan fatal: Global Histogram Equalization langsung per kanal BGR
b_eq = cv2.equalizeHist(foggy_bgr[:, :, 0])
g_eq = cv2.equalizeHist(foggy_bgr[:, :, 1])
r_eq = cv2.equalizeHist(foggy_bgr[:, :, 2])
bgr_global_eq = cv2.merge([b_eq, g_eq, r_eq])
rgb_global_eq = cv2.cvtColor(bgr_global_eq, cv2.COLOR_BGR2RGB)

# 2. Metodologi yang benar: CLAHE pada kanal L* di ruang CIE Lab
lab = cv2.cvtColor(foggy_bgr, cv2.COLOR_BGR2LAB)
L_chan, a_chan, b_chan = cv2.split(lab)

clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
L_enhanced = clahe.apply(L_chan)

lab_enhanced = cv2.merge([L_enhanced, a_chan, b_chan])
bgr_clahe = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
rgb_clahe = cv2.cvtColor(bgr_clahe, cv2.COLOR_BGR2RGB)

# Visualisasi dan Analisis Histogram
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

axes[0, 0].imshow(foggy_rgb)
axes[0, 0].set_title("Citra Asli Berkabut")
axes[0, 1].imshow(rgb_global_eq)
axes[0, 1].set_title("Global Eq Per-Kanal\\n(Distorsi Warna Fatal!)")
axes[0, 2].imshow(rgb_clahe)
axes[0, 2].set_title("CLAHE pada Kanal L*\\n(Warna Alami & Kontras Tinggi)")

# Plot Histogram Intensitas Kanal L
h_orig, b_orig = np.histogram(L_chan.ravel(), bins=64, range=(0, 256))
h_clahe, b_clahe = np.histogram(L_enhanced.ravel(), bins=64, range=(0, 256))
bin_centers = 0.5 * (b_orig[:-1] + b_orig[1:])

axes[1, 0].plot(bin_centers, h_orig, color='#7f8c8d', lw=2)
axes[1, 0].set_title("Histogram L* Asli (Sempit)")
axes[1, 0].set_xlim(0, 255)

axes[1, 1].hist(cv2.cvtColor(rgb_global_eq, cv2.COLOR_RGB2GRAY).ravel(), bins=64, range=(0, 256), color='#e74c3c')
axes[1, 1].set_title("Histogram Global Eq (Renggang/Kasar)")
axes[1, 1].set_xlim(0, 255)

axes[1, 2].plot(bin_centers, h_clahe, color='#27ae60', lw=2)
axes[1, 2].set_title("Histogram CLAHE L* (Merata & Teratur)")
axes[1, 2].set_xlim(0, 255)

for ax in axes[0]:
    ax.axis('off')
for ax in axes[1]:
    ax.set_xlabel("Nilai Intensitas")
    ax.set_ylabel("Frekuensi")

plt.tight_layout()
plt.savefig('docs/assets/notebook_9_4_clahe_comparison.png', dpi=150)
plt.close()
print("Hasil komparasi CLAHE tersimpan di docs/assets/notebook_9_4_clahe_comparison.png")''')

add_md('''## 5. Pipeline Standardisasi Tensor Masukan Deep Learning
Citra berdimensi spasial bebas diubah ke ukuran standar arsitektur CNN (misal $224 \\times 224$), dikonversi ke urutan kanal RGB, diskalakan ke rentang $[0.0, 1.0]$, distandarisasi menggunakan statistik ImageNet, dan ditata dengan memori *channel-first* $(1, C, H, W)$.''')

add_code('''def build_preprocessing_pipeline(image_bgr, target_size=(224, 224)):
    # 1. Peningkatan kontras adaptif
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    L, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_lab = cv2.merge([clahe.apply(L), a, b])
    enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # 2. Resizing dengan interpolasi Bicubic berkualitas tinggi
    resized = cv2.resize(enhanced_bgr, target_size, interpolation=cv2.INTER_CUBIC)
    
    # 3. Konversi ke urutan RGB
    rgb_img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    
    # 4. Penskalaan Min-Max [0.0, 1.0] dengan float32
    tensor_float = rgb_img.astype(np.float32) / 255.0
    
    # 5. Standarisasi Z-Score ImageNet
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    tensor_zscore = (tensor_float - mean) / std
    
    # 6. Permutasi HWC -> CHW dan penambahan dimensi batch
    tensor_chw = np.transpose(tensor_zscore, (2, 0, 1))
    tensor_batch = np.expand_dims(tensor_chw, axis=0)
    
    return tensor_batch

input_tensor = build_preprocessing_pipeline(foggy_bgr)

print("=== PROFIL TENSOR INPUT DEEP LEARNING ===")
print(f"Bentuk Tensor (Batch, Channels, Height, Width): {input_tensor.shape}")
print(f"Tipe Data Tensor : {input_tensor.dtype}")
print(f"Rata-rata Tensor : {input_tensor.mean():.4f}")
print(f"Deviasi Standar  : {input_tensor.std():.4f}")
print(f"Rentang Nilai    : [{input_tensor.min():.2f}, {input_tensor.max():.2f}]")''')

add_md('''## 6. Latihan Mandiri dan Tugas Praktikum

### Latihan 1: Integritas Kelas Masker Segmentasi pada Resizing
Buktikan bahaya penggunaan interpolasi linier/kubik pada masker segmentasi kategorikal.
Bandingkan jumlah kelas unik pada masker yang di-resize menggunakan `cv2.INTER_NEAREST` vs `cv2.INTER_LINEAR`.

### Latihan 2: Pengoptimalan Parameter CLAHE untuk Deteksi Pola Urat Pelepah
Uji variasi nilai `clipLimit` ($1.0, 2.5, 5.0$) pada citra kanopi berkabut dan analisis dampaknya terhadap kemunculan derau latar belakang tanah.''')

add_code('''# Implementasi Solusi Latihan 1: Uji Integritas Kelas Masker Segmentasi
mask_small = cv2.resize(true_palm_mask, (64, 64), interpolation=cv2.INTER_NEAREST)

# Resize kembali ke ukuran asli dengan NEAREST vs LINEAR
mask_restored_nearest = cv2.resize(mask_small, (400, 400), interpolation=cv2.INTER_NEAREST)
mask_restored_linear = cv2.resize(mask_small.astype(np.float32), (400, 400), interpolation=cv2.INTER_LINEAR)

classes_original = np.unique(true_palm_mask)
classes_nearest = np.unique(mask_restored_nearest)
classes_linear = np.unique(mask_restored_linear)

print("=== HASIL UJI INTEGRITAS KELAS SEGMENTASI ===")
print(f"Kelas unik pada Ground Truth Asli  : {classes_original} (Total: {len(classes_original)} kelas)")
print(f"Kelas unik dengan INTER_NEAREST     : {classes_nearest} (Total: {len(classes_nearest)} kelas - VALID!)")
print(f"Kelas unik dengan INTER_LINEAR      : Min={classes_linear.min():.2f}, Max={classes_linear.max():.2f}")
print(f"Jumlah nilai unik INTER_LINEAR      : {len(classes_linear)} nilai desimal semu (RUSAK!)")''')

with open('notebooks/part-09/AI_Modul_9.4_Praktikum_Preprocessing_Citra.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print('Notebook Modul 9.4 berhasil dibuat!')
