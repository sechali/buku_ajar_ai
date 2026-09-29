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

add_md('''# Praktikum AI Modul 9.3: Piksel dan Ruang Warna (Color Spaces)
**Program Studi Teknik Pertanian / Agroteknologi - Fakultas Pertanian & Teknologi Pertanian**  
*Materi: Konversi Ruang Warna (BGR, RGB, HSV, Lab), Dekomposisi Kanal, Segmentasi Kematangan Buah Sawit (TBS), dan Robustness terhadap Variasi Pencahayaan.*

---
### Tujuan Praktikum
1. Memahami perbedaan mendasar struktur kanal citra digital antara BGR (OpenCV), RGB, HSV, dan CIE L*a*b*.
2. Mengimplementasikan dekomposisi kanal warna dan visualisasi distribusi spektral kanopi dan buah kelapa sawit.
3. Mengembangkan algoritma segmentasi buah sawit matang (Ripe) vs mentah (Unripe) menggunakan ruang warna HSV dengan penanganan circular hue wrap-around.
4. Mengukur jarak persepsi warna menggunakan metrik Delta E_ab* pada ruang CIE L*a*b* untuk grading objektif.
5. Membandingkan ketahanan (robustness) segmentasi berbasis RGB vs HSV/Lab di bawah variasi pencahayaan ekstrem (terang terik vs bayangan gelap).''')

add_code('''import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print(f"OpenCV Version: {cv2.__version__}")
print(f"NumPy Version: {np.__version__}")''')

add_md('''## 1. Pembuatan Dataset Sintetis: Tandan Buah Segar (TBS) Kelapa Sawit
Kita membuat citra simulasi resolusi tinggi (400 x 600 piksel) yang merepresentasikan:
1. Latar belakang kanopi/pelepah hijau kelapa sawit.
2. Area buah sawit mentah (warna hitam keunguan pekat / nigrescens unripe).
3. Area buah sawit matang (warna jingga kemerahan cerah / rutilant ripe).
4. Variasi intensitas tekstur dan bayangan alami.''')

add_code('''def generate_synthetic_oil_palm_scene():
    np.random.seed(42)
    h, w = 400, 600
    
    # Background: Daun dan pelepah hijau
    img_bgr = np.zeros((h, w, 3), dtype=np.uint8)
    img_bgr[:, :, 0] = np.random.randint(15, 35, (h, w), dtype=np.uint8)    # B
    img_bgr[:, :, 1] = np.random.randint(70, 130, (h, w), dtype=np.uint8)   # G
    img_bgr[:, :, 2] = np.random.randint(25, 55, (h, w), dtype=np.uint8)    # R
    
    # Buat latar tekstur tanah/pelepah kering di bawah
    img_bgr[320:, :] = [25, 45, 65]
    
    # Koordinat grid
    Y, X = np.ogrid[:h, :w]
    
    # Buah mentah (Unripe): Lonjong di sisi kiri tengah (warna hitam/keunguan pekat)
    # BGR untuk hitam-ungu mentah: B ~ 40, G ~ 25, R ~ 50
    mask_unripe = ((X - 220)**2 / 70**2 + (Y - 180)**2 / 100**2) <= 1.0
    img_bgr[mask_unripe] = [45, 30, 60]
    
    # Buah matang (Ripe): Lonjong di sisi kanan tengah (warna jingga kemerahan cerah)
    # BGR untuk jingga kemerahan: B ~ 15, G ~ 65, R ~ 215
    mask_ripe = ((X - 380)**2 / 80**2 + (Y - 200)**2 / 110**2) <= 1.0
    img_bgr[mask_ripe] = [15, 75, 220]
    
    # Tambahkan spikelet buah individual (tekstur bintik-bintik buah)
    for _ in range(120):
        rx = np.random.randint(160, 280)
        ry = np.random.randint(100, 260)
        if mask_unripe[ry, rx]:
            cv2.circle(img_bgr, (rx, ry), np.random.randint(4, 9), (60, 40, 80), -1)
            
    for _ in range(140):
        rx = np.random.randint(310, 450)
        ry = np.random.randint(110, 290)
        if mask_ripe[ry, rx]:
            # Variasi jingga hingga merah tua
            r_val = np.random.randint(190, 255)
            g_val = np.random.randint(40, 100)
            b_val = np.random.randint(10, 30)
            cv2.circle(img_bgr, (rx, ry), np.random.randint(5, 11), (b_val, g_val, r_val), -1)
            
    return img_bgr, mask_unripe, mask_ripe

sample_bgr, true_unripe_mask, true_ripe_mask = generate_synthetic_oil_palm_scene()
sample_rgb = cv2.cvtColor(sample_bgr, cv2.COLOR_BGR2RGB)
print("Citra sintetis berhasil digenerasi. Dimensi:", sample_bgr.shape)''')

add_md('''## 2. Dekomposisi Kanal Warna: Perbandingan BGR, RGB, HSV, dan CIE Lab
Kita memisahkan kanal pada tiap ruang warna untuk memahami informasi visual yang dikandung masing-masing dimensi spektral.''')

add_code('''# Konversi ruang warna
sample_hsv = cv2.cvtColor(sample_bgr, cv2.COLOR_BGR2HSV)
sample_lab = cv2.cvtColor(sample_bgr, cv2.COLOR_BGR2LAB)
sample_gray = cv2.cvtColor(sample_bgr, cv2.COLOR_BGR2GRAY)

fig, axes = plt.subplots(3, 4, figsize=(16, 11))

# Baris 1: RGB
axes[0, 0].imshow(sample_rgb)
axes[0, 0].set_title("Citra Asli (RGB)")
axes[0, 1].imshow(sample_rgb[:, :, 0], cmap='Reds')
axes[0, 1].set_title("Kanal R (Red)")
axes[0, 2].imshow(sample_rgb[:, :, 1], cmap='Greens')
axes[0, 2].set_title("Kanal G (Green)")
axes[0, 3].imshow(sample_rgb[:, :, 2], cmap='Blues')
axes[0, 3].set_title("Kanal B (Blue)")

# Baris 2: HSV
axes[1, 0].imshow(sample_gray, cmap='gray')
axes[1, 0].set_title("Grayscale (Luminansi)")
axes[1, 1].imshow(sample_hsv[:, :, 0], cmap='hsv')
axes[1, 1].set_title("Kanal H (Hue [0-179])")
axes[1, 2].imshow(sample_hsv[:, :, 1], cmap='bone')
axes[1, 2].set_title("Kanal S (Saturation [0-255])")
axes[1, 3].imshow(sample_hsv[:, :, 2], cmap='gray')
axes[1, 3].set_title("Kanal V (Value [0-255])")

# Baris 3: CIE Lab
axes[2, 0].imshow(sample_lab[:, :, 0], cmap='gray')
axes[2, 0].set_title("Kanal L* (Lightness)")
axes[2, 1].imshow(sample_lab[:, :, 1], cmap='coolwarm')
axes[2, 1].set_title("Kanal a* (Hijau - Merah)")
axes[2, 2].imshow(sample_lab[:, :, 2], cmap='YlGnBu')
axes[2, 2].set_title("Kanal b* (Biru - Kuning)")
axes[2, 3].axis('off')

for ax in axes.ravel():
    ax.axis('off')

plt.tight_layout()
plt.savefig('docs/assets/notebook_9_3_channel_decomposition.png', dpi=150)
plt.close()
print("Visualisasi dekomposisi kanal tersimpan di docs/assets/notebook_9_3_channel_decomposition.png")''')

add_md('''## 3. Segmentasi Kematangan Sawit Menggunakan Ruang Warna HSV
Warna merah-oranye buah sawit matang berada pada nilai Hue rendah (0 - 14) dan Hue sangat tinggi (168 - 179) karena sifat melingkar (wrap-around 0 deg = 360 deg).
Oleh karena itu, segmentasi akurat mewajibkan penggunaan dua rentang inRange yang digabungkan dengan operasi logika OR (`cv2.bitwise_or`).''')

add_code('''# Rentang HSV untuk buah matang (Ripe: Jingga-Merah)
lower_red1 = np.array([0, 100, 100], dtype=np.uint8)
upper_red1 = np.array([14, 255, 255], dtype=np.uint8)
lower_red2 = np.array([168, 100, 100], dtype=np.uint8)
upper_red2 = np.array([179, 255, 255], dtype=np.uint8)

mask_ripe_part1 = cv2.inRange(sample_hsv, lower_red1, upper_red1)
mask_ripe_part2 = cv2.inRange(sample_hsv, lower_red2, upper_red2)
segmented_ripe_hsv = cv2.bitwise_or(mask_ripe_part1, mask_ripe_part2)

# Rentang HSV untuk kanopi daun hijau
lower_green = np.array([35, 40, 40], dtype=np.uint8)
upper_green = np.array([85, 255, 255], dtype=np.uint8)
segmented_canopy_hsv = cv2.inRange(sample_hsv, lower_green, upper_green)

# Rentang HSV untuk buah mentah (gelap, saturasi rendah-sedang, hue ungu/hitam)
lower_unripe = np.array([120, 20, 20], dtype=np.uint8)
upper_unripe = np.array([170, 120, 90], dtype=np.uint8)
segmented_unripe_hsv = cv2.inRange(sample_hsv, lower_unripe, upper_unripe)

# Masking visual pada citra RGB
res_ripe = cv2.bitwise_and(sample_rgb, sample_rgb, mask=segmented_ripe_hsv)
res_unripe = cv2.bitwise_and(sample_rgb, sample_rgb, mask=segmented_unripe_hsv)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
axes[0].imshow(sample_rgb)
axes[0].set_title("Citra Asli TBS")
axes[1].imshow(segmented_ripe_hsv, cmap='gray')
axes[1].set_title("Mask Buah Matang (HSV)")
axes[2].imshow(res_ripe)
axes[2].set_title("Ekstraksi Buah Matang")
axes[3].imshow(res_unripe)
axes[3].set_title("Ekstraksi Buah Mentah")

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.savefig('docs/assets/notebook_9_3_hsv_segmentation.png', dpi=150)
plt.close()
print("Hasil segmentasi HSV tersimpan di docs/assets/notebook_9_3_hsv_segmentation.png")''')

add_md('''## 4. Analisis Persepsi Warna Berbasis CIE L*a*b* dan Perhitungan Delta E_ab*
Pada ruang CIE L*a*b*, jarak Euclidean antara dua vektor warna memodelkan perbedaan visual yang dirasakan mata manusia secara proporsional (perceptual uniformity).

Delta E_ab* = sqrt((L1* - L2*)^2 + (a1* - a2*)^2 + (b1* - b2*)^2)

Kita menetapkan target standar buah sawit matang ideal dari laboratorium sortasi PKS, lalu menghitung peta jarak warna Delta E* seluruh piksel.''')

add_code('''# Target Lab buah sawit matang standar (konversi ke skala asli CIE: L:[0,100], a:[-128,127], b:[-128,127])
# Di OpenCV: L_cv = L * 255 / 100, a_cv = a + 128, b_cv = b + 128
target_bgr_sample = np.uint8([[[15, 75, 220]]])
target_lab = cv2.cvtColor(target_bgr_sample, cv2.COLOR_BGR2LAB)[0, 0].astype(np.float32)

L_t = target_lab[0] * (100.0 / 255.0)
a_t = target_lab[1] - 128.0
b_t = target_lab[2] - 128.0

# Konversi seluruh citra ke koordinat CIE Lab standar
img_lab_float = sample_lab.astype(np.float32)
L_img = img_lab_float[:, :, 0] * (100.0 / 255.0)
a_img = img_lab_float[:, :, 1] - 128.0
b_img = img_lab_float[:, :, 2] - 128.0

# Hitung Delta E_ab terhadap warna referensi
delta_E = np.sqrt((L_img - L_t)**2 + (a_img - a_t)**2 + (b_img - b_t)**2)

# Segmentasi berbasis ambang batas toleransi delta E <= 35
mask_lab_ripe = (delta_E <= 35.0).astype(np.uint8) * 255

min_de = float(delta_E.min())
max_de = float(delta_E.max())
print(f"Target CIE Lab: L*={L_t:.1f}, a*={a_t:.1f}, b*={b_t:.1f}")
print(f"Min Delta E: {min_de:.2f}, Max Delta E: {max_de:.2f}")

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].imshow(sample_rgb)
axes[0].set_title("Citra TBS")
im = axes[1].imshow(delta_E, cmap='viridis_r')
axes[1].set_title("Peta Jarak Warna Delta E_ab*")
fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
axes[2].imshow(mask_lab_ripe, cmap='gray')
axes[2].set_title("Segmentasi Delta E_ab* <= 35")

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.savefig('docs/assets/notebook_9_3_delta_e_map.png', dpi=150)
plt.close()
print("Peta Delta E tersimpan di docs/assets/notebook_9_3_delta_e_map.png")''')

add_md('''## 5. Uji Ketahanan (Robustness) Terhadap Variasi Pencahayaan
Di perkebunan terbuka, intensitas cahaya matahari berubah drastis akibat tutupan awan atau naungan pelepah.
Kita menguji ketahanan segmentasi berbasis RGB vs HSV saat citra mengalami:
1. Reduksi pencahayaan (Bayangan/Underexposure): Faktor 0.4x.
2. Peningkatan pencahayaan (Terik Matahari/Overexposure): Faktor 1.7x.''')

add_code('''# Simulasikan kondisi gelap (shadow) dan terang terik (sunlight)
img_dark = cv2.convertScaleAbs(sample_bgr, alpha=0.4, beta=0)
img_bright = cv2.convertScaleAbs(sample_bgr, alpha=1.7, beta=20)

# Segmentasi RGB murni: R > 150, G < 100, B < 60
def segment_rgb(img_b):
    r = img_b[:, :, 2]
    g = img_b[:, :, 1]
    b = img_b[:, :, 0]
    return ((r > 150) & (g < 100) & (b < 60)).astype(np.uint8) * 255

# Segmentasi HSV robust: Hue dalam range merah/jingga & Saturation cukup
def segment_hsv_robust(img_b):
    hsv = cv2.cvtColor(img_b, cv2.COLOR_BGR2HSV)
    m1 = cv2.inRange(hsv, np.array([0, 70, 30]), np.array([14, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([168, 70, 30]), np.array([179, 255, 255]))
    return cv2.bitwise_or(m1, m2)

# Evaluasi pada citra normal, gelap, dan terang
scenes = [('Normal', sample_bgr), ('Gelap (Bayangan)', img_dark), ('Terang (Terik)', img_bright)]

fig, axes = plt.subplots(3, 3, figsize=(14, 12))

for row_idx, (label, scene) in enumerate(scenes):
    rgb_view = cv2.cvtColor(scene, cv2.COLOR_BGR2RGB)
    mask_rgb = segment_rgb(scene)
    mask_hsv = segment_hsv_robust(scene)
    
    # Hitung akurasi deteksi piksel matang terhadap true ripe mask
    iou_rgb = np.sum((mask_rgb > 0) & true_ripe_mask) / (np.sum((mask_rgb > 0) | true_ripe_mask) + 1e-6)
    iou_hsv = np.sum((mask_hsv > 0) & true_ripe_mask) / (np.sum((mask_hsv > 0) | true_ripe_mask) + 1e-6)
    
    axes[row_idx, 0].imshow(rgb_view)
    axes[row_idx, 0].set_title(f"{label}")
    axes[row_idx, 1].imshow(mask_rgb, cmap='gray')
    axes[row_idx, 1].set_title(f"RGB Rule (IoU: {iou_rgb:.2f})")
    axes[row_idx, 2].imshow(mask_hsv, cmap='gray')
    axes[row_idx, 2].set_title(f"HSV Dual-Range (IoU: {iou_hsv:.2f})")
    
    for ax in axes[row_idx]:
        ax.axis('off')

plt.tight_layout()
plt.savefig('docs/assets/notebook_9_3_lighting_robustness.png', dpi=150)
plt.close()
print("Hasil uji robustness pencahayaan tersimpan di docs/assets/notebook_9_3_lighting_robustness.png")''')

add_md('''## 6. Latihan Mandiri dan Tugas Terapan

### Latihan 1: Segmentasi Gejala Klorosis Daun Sawit (Defisiensi Nitrogen)
Di kebun pembibitan (nursery), daun sawit yang kekurangan nitrogen mengalami klorosis (menguning).
Tentukan rentang nilai HSV yang memisahkan daun sehat (hijau segar) dari daun yang mengalami klorosis (kuning pucat).

### Latihan 2: Pengukuran Fraksi Luas Buah Matang (Ripeness Index)
Buat fungsi yang menerima citra TBS, menghasilkan luas area buah matang dalam persentase, dan mengklasifikasikan tandan ke dalam salah satu kelas fraksi:
- Fraksi 00 (Sangat Mentah): 0% brondolan matang.
- Fraksi 0 (Mentah): 1 - 12.5% brondolan matang.
- Fraksi 1 - 3 (Matang Optimal): 12.5 - 75% brondolan matang.
- Fraksi 4 - 5 (Lewat Matang/Overripe): > 75% brondolan matang.''')

add_code('''# Implementasi Solusi Latihan 2: Ripeness Index Calculator
def calculate_ripeness_fraction(image_bgr):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    # Mask buah matang (jingga/merah)
    m1 = cv2.inRange(hsv, np.array([0, 70, 30]), np.array([14, 255, 255]))
    m2 = cv2.inRange(hsv, np.array([168, 70, 30]), np.array([179, 255, 255]))
    mask_ripe = cv2.bitwise_or(m1, m2)
    
    # Mask buah mentah (ungu tua / hitam)
    mask_unripe = cv2.inRange(hsv, np.array([115, 15, 15]), np.array([175, 130, 95]))
    
    total_fruit_pixels = np.sum(mask_ripe > 0) + np.sum(mask_unripe > 0)
    if total_fruit_pixels == 0:
        return 0.0, "Objek TBS Tidak Terdeteksi"
        
    ripe_percentage = (np.sum(mask_ripe > 0) / total_fruit_pixels) * 100.0
    
    if ripe_percentage == 0:
        grade = "Fraksi 00 (Sangat Mentah)"
    elif ripe_percentage < 12.5:
        grade = "Fraksi 0 (Mentah)"
    elif ripe_percentage <= 75.0:
        grade = "Fraksi 1-3 (Matang Optimal / Standar Olah PKS)"
    else:
        grade = "Fraksi 4-5 (Lewat Matang / Asam Lemak Bebas Tinggi)"
        
    return ripe_percentage, grade

pct, grade = calculate_ripeness_fraction(sample_bgr)
print(f"Analisis Tandan Buah Segar:\\n- Persentase Kematangan: {pct:.2f}%\\n- Klasifikasi Mutu: {grade}")''')

with open('notebooks/part-09/AI_Modul_9.3_Praktikum_Piksel_dan_Ruang_Warna.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print('Notebook Modul 9.3 berhasil dibuat!')
