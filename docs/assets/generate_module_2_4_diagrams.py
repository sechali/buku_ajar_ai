import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

out_dir = r'e:\Project Buku\docs\assets'
os.makedirs(out_dir, exist_ok=True)

# 1. Diagram Model Memori Objek Python
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 7.5)
ax.axis('off')

ax.text(6, 7.1, 'MODEL MEMORI VARIABEL PYTHON: NAMA VARIABEL & REFERENSI OBJEK (HEAP)', 
        ha='center', va='center', fontsize=13, fontweight='bold', color='#1A365D')

frame_box = patches.FancyBboxPatch((0.5, 0.8), 3.8, 5.8, boxstyle='round,pad=0.2', fc='#EDF2F7', ec='#4A5568', lw=2)
ax.add_patch(frame_box)
ax.text(2.4, 6.2, 'Ruang Nama Variabel (Namespace)\n[Label Pengenal / Pointer]', ha='center', va='center', fontsize=10, fontweight='bold', color='#2D3748')

var_items = [
    (2.4, 5.0, 'suhu_reaktor', '#2B6CB0', '#EBF8FF'),
    (2.4, 3.8, 'kuota_tbs', '#276749', '#F0FFF4'),
    (2.4, 2.6, 'kode_blok', '#C53030', '#FFF5F5'),
    (2.4, 1.4, 'daftar_sensor', '#6B46C1', '#FAF5FF')
]

for x, y, name, ec, bg in var_items:
    p = patches.FancyBboxPatch((x-1.5, y-0.35), 3.0, 0.7, boxstyle='round,pad=0.15', fc=bg, ec=ec, lw=1.8)
    ax.add_patch(p)
    ax.text(x, y, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color=ec)

heap_box = patches.FancyBboxPatch((7.5, 0.8), 4.0, 5.8, boxstyle='round,pad=0.2', fc='#FFFDF5', ec='#D69E2E', lw=2)
ax.add_patch(heap_box)
ax.text(9.5, 6.2, 'Memori Objek (Heap Memory)\n[Nilai, Tipe, & Reference Count]', ha='center', va='center', fontsize=10, fontweight='bold', color='#744210')

obj_items = [
    (9.5, 5.0, 'Objek: float\nNilai: 135.5\nid: 0x7fa21a4', '#2B6CB0', '#EBF8FF', 'Immutable'),
    (9.5, 3.8, 'Objek: int\nNilai: 5000\nid: 0x7fa21b8', '#276749', '#F0FFF4', 'Immutable'),
    (9.5, 2.6, 'Objek: str\nNilai: \'BLOK-C4\'\nid: 0x7fa21cc', '#C53030', '#FFF5F5', 'Immutable'),
    (9.5, 1.4, 'Objek: list\nNilai: [28.5, 31.0]\nid: 0x7fa21e0', '#6B46C1', '#FAF5FF', 'Mutable')
]

for x, y, desc, ec, bg, mut in obj_items:
    p = patches.FancyBboxPatch((x-1.7, y-0.45), 3.4, 0.9, boxstyle='round,pad=0.15', fc=bg, ec=ec, lw=1.8)
    ax.add_patch(p)
    ax.text(x-0.2, y, desc, ha='center', va='center', fontsize=8, color='#2D3748')
    ax.text(x+1.3, y, mut, ha='center', va='center', fontsize=7, fontweight='bold', 
            bbox=dict(boxstyle='square,pad=0.2', fc='#FFFFFF', ec=ec, lw=1))

arr = dict(arrowstyle='->', lw=2.2, color='#4A5568')
ax.annotate('', xy=(7.7, 5.0), xytext=(4.0, 5.0), arrowprops=arr)
ax.annotate('', xy=(7.7, 3.8), xytext=(4.0, 3.8), arrowprops=arr)
ax.annotate('', xy=(7.7, 2.6), xytext=(4.0, 2.6), arrowprops=arr)
ax.annotate('', xy=(7.7, 1.4), xytext=(4.0, 1.4), arrowprops=arr)

ax.text(5.8, 5.3, 'Pointer Referensi', ha='center', va='bottom', fontsize=8, color='#718096')
ax.text(5.8, 4.1, 'Pointer Referensi', ha='center', va='bottom', fontsize=8, color='#718096')
ax.text(5.8, 2.9, 'Pointer Referensi', ha='center', va='bottom', fontsize=8, color='#718096')
ax.text(5.8, 1.7, 'Pointer Referensi', ha='center', va='bottom', fontsize=8, color='#718096')

plt.tight_layout()
out1 = os.path.join(out_dir, 'arsitektur_memori_variabel_python.png')
plt.savefig(out1, dpi=300)
plt.close()
print(f'Saved {out1}')

# 2. Taksonomi Tipe Data Python dalam Pemrosesan AI
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 7.5)
ax.axis('off')

ax.text(6, 7.1, 'TAKSONOMI TIPE DATA PYTHON UNTUK PIPELINE ARTIFICIAL INTELLIGENCE', 
        ha='center', va='center', fontsize=13, fontweight='bold', color='#1A365D')

p_root = patches.FancyBboxPatch((4.5, 5.8), 3.0, 0.8, boxstyle='round,pad=0.2', fc='#1A365D', ec='#0F2942', lw=2)
ax.add_patch(p_root)
ax.text(6, 6.2, 'TIPE DATA PYTHON\n(Python Data Types)', ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF')

p_prim = patches.FancyBboxPatch((0.8, 4.2), 4.8, 0.7, boxstyle='round,pad=0.2', fc='#EBF8FF', ec='#3182CE', lw=2)
ax.add_patch(p_prim)
ax.text(3.2, 4.55, 'TIPE PRIMITIF / SKALAR (Immutable)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#2B6CB0')

p_comp = patches.FancyBboxPatch((6.4, 4.2), 4.8, 0.7, boxstyle='round,pad=0.2', fc='#F0FFF4', ec='#38A169', lw=2)
ax.add_patch(p_comp)
ax.text(8.8, 4.55, 'TIPE KOLEKSI / KOMPOSIT', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#22543D')

prim_sub = [
    (1.4, 2.3, 'int (Integer)', 'Bilangan Bulat\nContoh: 42, 1000\n(Biner, Cacah Buah)'),
    (2.6, 2.3, 'float (Float)', 'Pecahan IEEE 754\nContoh: 34.5, 0.94\n(Suhu, Probabilitas)'),
    (3.8, 2.3, 'bool (Boolean)', 'Logika Biner\nContoh: True, False\n(Status Sakelar)'),
    (5.0, 2.3, 'str (String)', 'Karakter UTF-8\nContoh: "SAWIT-A1"\n(Label, Kode Sensor)')
]

for x, y, name, desc in prim_sub:
    p = patches.Rectangle((x-0.55, y-1.3), 1.1, 2.6, fc='#FFFFFF', ec='#3182CE', lw=1.5)
    ax.add_patch(p)
    ax.text(x, y+0.9, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#2B6CB0')
    ax.text(x, y-0.1, desc, ha='center', va='center', fontsize=7.5, color='#4A5568')

comp_sub = [
    (7.0, 2.3, 'list (Daftar)', 'Mutable (Bisa Berubah)\nContoh: [1.2, 3.4]\n(Batch Fitur AI)'),
    (8.2, 2.3, 'tuple (Tupel)', 'Immutable (Tetap)\nContoh: (224, 224, 3)\n(Dimensi Citra Tensor)'),
    (9.4, 2.3, 'dict (Kamus)', 'Key-Value Mapping\nContoh: {"pH": 6.5}\n(Objek Telemetri IoT)'),
    (10.6, 2.3, 'set (Himpunan)', 'Unik & Tak Berurut\nContoh: {"ulat", "ulat"}\n(Daftar Hama Unik)')
]

for x, y, name, desc in comp_sub:
    p = patches.Rectangle((x-0.55, y-1.3), 1.1, 2.6, fc='#FFFFFF', ec='#38A169', lw=1.5)
    ax.add_patch(p)
    ax.text(x, y+0.9, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#22543D')
    ax.text(x, y-0.1, desc, ha='center', va='center', fontsize=7.5, color='#4A5568')

ax.annotate('', xy=(3.2, 4.9), xytext=(5.0, 5.8), arrowprops=dict(arrowstyle='->', lw=1.8, color='#2D3748'))
ax.annotate('', xy=(8.8, 4.9), xytext=(7.0, 5.8), arrowprops=dict(arrowstyle='->', lw=1.8, color='#2D3748'))

plt.tight_layout()
out2 = os.path.join(out_dir, 'taksonomi_tipe_data_ai.png')
plt.savefig(out2, dpi=300)
plt.close()
print(f'Saved {out2}')
