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

add_md('''# Praktikum AI Modul 9.7: Ekstraksi Fitur dan Morfologi Citra (Morphological Operations and Feature Extraction)
**Program Studi Teknik Pertanian / Agroteknologi - Fakultas Pertanian & Teknologi Pertanian**  
*Materi: Morfologi Matematika Biner (Erosi, Dilasi, Opening, Closing, Gradien Morfologis), Pelacakan Kontur 2D Suzuki-Abe, Momen Spasial, dan Analisis Morfometri Kanopi Kelapa Sawit (CPA, Centroid, Circularity).*

---
### Tujuan Praktikum
1. Memahami prinsip operasi morfologi matematika (Erosi, Dilasi, Opening, Closing) menggunakan elemen penstruktur eliptikal (`MORPH_ELLIPSE`).
2. Menghilangkan derau bintik luar (*speckles*) dan menutup lubang bayangan internal pada masker biner kanopi tanaman.
3. Melacak batas luar objek menggunakan algoritma kontur `cv2.findContours` dan menganalisis struktur hirarki topologinya.
4. Mengekstraksi parameter morfometri kuantitatif: Luas Area ($A$), Perimeter ($P$), Titik Pusat Massa / Centroid ($c_x, c_y$), dan Rasio Kebulatan (*Circularity*).
5. Menerapkan ekstraksi fitur geometris untuk sensus otomatis tegakan pohon sawit dan estimasi luas tajuk (*Crown Projection Area*) dari citra drone.''')

add_code('''import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print(f"OpenCV Version : {cv2.__version__}")
print(f"NumPy Version  : {np.__version__}")''')

add_md('''## 1. Pembuatan Dataset Sintetis: Masker Biner Kanopi Pohon Sawit dengan Cacat Topologi
Kita mensimulasikan dua kanopi kelapa sawit yang memiliki cacat spasial tipikal lapangan: lubang bayangan internal (*internal holes*) dan bintik-bintik gulma tanah eksternal (*speckle noise*).''')

add_code('''def generate_binary_canopy_scene():
    np.random.seed(42)
    h, w = 300, 300
    Y, X = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    
    # 1. Objek Pohon Sawit 1 (Kiri: Elips a=55, b=65)
    tree1 = ((X - 95)**2 / 55**2 + (Y - 115)**2 / 65**2) <= 1.0
    
    # 2. Objek Pohon Sawit 2 (Kanan: Elips a=60, b=70)
    tree2 = ((X - 205)**2 / 60**2 + (Y - 185)**2 / 70**2) <= 1.0
    
    raw_mask = (tree1 | tree2).astype(np.uint8) * 255
    
    # 3. Tambahkan lubang bayangan internal
    hole1 = ((X - 95)**2 + (Y - 115)**2) <= 14**2
    hole2 = ((X - 205)**2 + (Y - 185)**2) <= 16**2
    raw_mask[hole1 | hole2] = 0
    
    # 4. Tambahkan derau gulma acak di luar kanopi
    noise = (np.random.rand(h, w) > 0.988) & (~(tree1 | tree2))
    raw_mask[noise] = 255
    
    return raw_mask

raw_mask = generate_binary_canopy_scene()
print(f"Masker biner berhasil digenerasi: resolusi {raw_mask.shape}, total piksel aktif={np.sum(raw_mask > 0)}")''')

add_md('''## 2. Operasi Morfologi Biner: Opening, Closing, dan Gradien Morfologis
Kita menerapkan:
1. **Opening (Erosi dilanjutkan Dilasi)**: Membuang derau bintik luar tanpa mengubah ukuran pohon.
2. **Closing (Dilasi dilanjutkan Erosi)**: Menutup lubang bayangan internal kanopi.
3. **Gradien Morfologis (Dilasi - Erosi)**: Mengekstrak garis batas siluet luar objek.''')

add_code('''# Elemen penstruktur eliptikal ukuran 9x9
se_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

# 1. Opening untuk eliminasi derau eksternal
mask_opened = cv2.morphologyEx(raw_mask, cv2.MORPH_OPEN, se_ellipse)

# 2. Closing pada hasil opening untuk menutup lubang internal
mask_clean = cv2.morphologyEx(mask_opened, cv2.MORPH_CLOSE, se_ellipse)

# 3. Gradien Morfologis untuk mengekstrak kontur batas
mask_gradient = cv2.morphologyEx(mask_clean, cv2.MORPH_GRADIENT, se_ellipse)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
axes[0].imshow(raw_mask, cmap='gray')
axes[0].set_title("Mask Biner Mentah\\n(Lubang & Derau Luar)")

axes[1].imshow(mask_opened, cmap='gray')
axes[1].set_title("Opening (Erosi -> Dilasi)\\n(Derau Luar Lenyap)")

axes[2].imshow(mask_clean, cmap='gray')
axes[2].set_title("Closing (Dilasi -> Erosi)\\n(Lubang Internal Tertutup)")

axes[3].imshow(mask_gradient, cmap='inferno')
axes[3].set_title("Gradien Morfologis\\n(Siluet Batas Luar Presisi)")

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.savefig('docs/assets/notebook_9_7_morphology_pipeline.png', dpi=150)
plt.close()
print("Hasil visualisasi morfologi tersimpan di docs/assets/notebook_9_7_morphology_pipeline.png")''')

add_md('''## 3. Pelacakan Kontur 2D Suzuki-Abe dan Estimasi Titik Pusat Massa (Centroid)
Kita melacak seluruh kontur luar objek (`cv2.RETR_EXTERNAL`) dan menghitung titik koordinat pusat massa (*centroid*) menggunakan rumus momen spasial:
$$c_x = \\frac{m_{10}}{m_{00}}, \\quad c_y = \\frac{m_{01}}{m_{00}}$$''')

add_code('''# Deteksi kontur eksternal
contours, hierarchy = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Jumlah kontur pohon sawit terdeteksi: {len(contours)}")

vis_contours = cv2.cvtColor(mask_clean, cv2.COLOR_GRAY2BGR)

tree_data = []
for idx, cnt in enumerate(contours):
    area_px = cv2.contourArea(cnt)
    perimeter_px = cv2.arcLength(cnt, closed=True)
    
    # Hitung momen spasial
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00']) if M['m00'] > 0 else 0
    cy = int(M['m01'] / M['m00']) if M['m00'] > 0 else 0
    
    # Rasio kebulatan (Circularity)
    circularity = (4.0 * np.pi * area_px) / (perimeter_px**2) if perimeter_px > 0 else 0
    
    # Gambar kontur (kuning) dan titik centroid (merah)
    cv2.drawContours(vis_contours, [cnt], -1, (0, 255, 255), 2)
    cv2.circle(vis_contours, (cx, cy), 5, (0, 0, 255), -1)
    cv2.putText(vis_contours, f"Pohon #{idx+1} ({cx},{cy})", (cx - 45, cy - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    
    tree_data.append({
        'id': idx + 1,
        'centroid': (cx, cy),
        'area_px': area_px,
        'perimeter_px': perimeter_px,
        'circularity': circularity
    })

plt.figure(figsize=(6, 6))
plt.imshow(cv2.cvtColor(vis_contours, cv2.COLOR_BGR2RGB))
plt.title("Pelacakan Kontur & Titik Centroid Pohon Sawit", fontsize=11, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('docs/assets/notebook_9_7_contour_centroids.png', dpi=150)
plt.close()
print("Hasil visualisasi kontur tersimpan di docs/assets/notebook_9_7_contour_centroids.png")''')

add_md('''## 4. Ekstraksi Kotak Pembatas Berorientasi (*Rotated Rect*) dan Lingkaran Minimum
Untuk memodelkan orientasi tajuk pelepah pohon sawit, kita memadukan:
1. **Rotated Bounding Box** (`cv2.minAreaRect`)
2. **Minimum Enclosing Circle** (`cv2.minEnclosingCircle`)''')

add_code('''vis_geometry = cv2.cvtColor(mask_clean, cv2.COLOR_GRAY2BGR)

for cnt in contours:
    # 1. Oriented Rotated Bounding Box
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    cv2.drawContours(vis_geometry, [box], 0, (0, 255, 0), 2)  # Hijau
    
    # 2. Minimum Enclosing Circle
    (xc, yc), radius = cv2.minEnclosingCircle(cnt)
    cv2.circle(vis_geometry, (int(xc), int(yc)), int(radius), (255, 140, 0), 2)  # Oranye

plt.figure(figsize=(6, 6))
plt.imshow(cv2.cvtColor(vis_geometry, cv2.COLOR_BGR2RGB))
plt.title("Fitting Geometri: Rotated Box (Hijau) & Min Circle (Oranye)", fontsize=11, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('docs/assets/notebook_9_7_geometric_fitting.png', dpi=150)
plt.close()
print("Hasil visualisasi geometri fitting tersimpan di docs/assets/notebook_9_7_geometric_fitting.png")''')

add_md('''## 5. Latihan Mandiri: Sensus Pohon dan Estimasi Luas Tajuk (*Crown Area*)
Konversikan luas area piksel seluruh pohon terdeteksi ke dalam satuan fisik riil ($\text{m}^2$) jika citra drone memiliki resolusi spasial $\text{GSD} = 3.5\text{ cm/piksel}$.''')

add_code('''# Solusi Latihan: Kalkulasi Crown Projection Area (CPA)
gsd_cm = 3.5
gsd_meter = gsd_cm / 100.0

print("=== REKAPITULASI SENSUS TEGAKAN DAN MORFOMETRI KANOPI ===")
for tree in tree_data:
    area_m2 = tree['area_px'] * (gsd_meter ** 2)
    perimeter_m = tree['perimeter_px'] * gsd_meter
    
    print(f"Pohon ID #{tree['id']}:")
    print(f"  - Koordinat Batang (Centroid) : {tree['centroid']}")
    print(f"  - Crown Projection Area (CPA) : {area_m2:.2f} m^2 ({tree['area_px']:.0f} piksel)")
    print(f"  - Keliling Perimeter Tajuk    : {perimeter_m:.2f} meter")
    print(f"  - Rasio Kebulatan (Circularity): {tree['circularity']:.3f}")
    if tree['circularity'] >= 0.80:
        print("  - Diagnosis Kesehatan         : Tajuk Sangat Simetris (Prima)")
    else:
        print("  - Diagnosis Kesehatan         : Tajuk Asimetris / Gejala Pelepah Rusak")''')

with open('notebooks/part-09/AI_Modul_9.7_Praktikum_Ekstraksi_Fitur_dan_Morfologi_Citra.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print('Notebook Modul 9.7 berhasil dibuat!')
