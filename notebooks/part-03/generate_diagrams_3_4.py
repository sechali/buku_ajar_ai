import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
import os

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def buat_diagram_arsitektur_pyobject():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Judul
    ax.text(5.5, 5.8, "Arsitektur Memori CPython: Model Objek PyObject & Pengikatan Referensi", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.45, "Konsep Fundamental: Variabel Hanyalah Label Pointer (Tag) Menuju PyObject di Memori Heap", 
            ha='center', va='center', fontsize=9, style='italic', color='#4a5568')

    # Sisi Kiri: Stack Frame (Variabel / Nama)
    rect_stack = patches.FancyBboxPatch((0.6, 0.9), 3.2, 4.2, boxstyle="round,pad=0.15", 
                                        facecolor="#ebf8ff", edgecolor="#3182ce", linewidth=2)
    ax.add_patch(rect_stack)
    ax.text(2.2, 4.75, "STACK FRAME\n(Namespace Variabel / Label)", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#2b6cb0')

    # Label-label variabel
    labels = [
        {"name": "suhu_kanopi", "y": 3.7, "color": "#2c5282"},
        {"name": "bacaan_sensor", "y": 2.5, "color": "#2c5282"},
        {"name": "id_blok", "y": 1.4, "color": "#2c5282"},
    ]
    for lbl in labels:
        box = patches.FancyBboxPatch((0.9, lbl["y"]-0.3), 2.6, 0.6, boxstyle="round,pad=0.08", 
                                      facecolor="#ffffff", edgecolor=lbl["color"], linewidth=1.5)
        ax.add_patch(box)
        ax.text(2.2, lbl["y"], lbl["name"], ha='center', va='center', fontsize=8.5, family='monospace', fontweight='bold', color=lbl["color"])

    # Sisi Kanan: Heap Memory (PyObject Sebenarnya)
    rect_heap = patches.FancyBboxPatch((5.0, 0.9), 5.4, 4.2, boxstyle="round,pad=0.15", 
                                       facecolor="#f7fafc", edgecolor="#4a5568", linewidth=2)
    ax.add_patch(rect_heap)
    ax.text(7.7, 4.75, "HEAP MEMORY (Struktur Internal PyObject)", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#1a202c')

    # Objek 1: PyFloatObject (suhu_kanopi & bacaan_sensor sama-sama menunjuk ke sini)
    obj1 = patches.FancyBboxPatch((5.3, 2.3), 4.8, 1.9, boxstyle="round,pad=0.1", 
                                 facecolor="#feebc8", edgecolor="#dd6b20", linewidth=1.5)
    ax.add_patch(obj1)
    ax.text(7.7, 3.9, "PyFloatObject (Alamat: 0x000001FA...)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#7b341e')
    ax.text(5.5, 3.4, "* ob_refcnt : 2 (Dua variabel merujuk ke objek ini)", fontsize=8, color='#2d3748')
    ax.text(5.5, 3.0, "* ob_type   : <class 'float'> (Pointer ke Type Descriptor)", fontsize=8, color='#2d3748')
    ax.text(5.5, 2.6, "* ob_fval   : 31.75 (Nilai Pecahan Desimal 64-Bit)", fontsize=8, fontweight='bold', color='#c05621')

    # Objek 2: PyUnicodeObject (id_blok)
    obj2 = patches.FancyBboxPatch((5.3, 1.1), 4.8, 0.9, boxstyle="round,pad=0.1", 
                                 facecolor="#c6f6d5", edgecolor="#276749", linewidth=1.5)
    ax.add_patch(obj2)
    ax.text(7.7, 1.7, "PyUnicodeObject: 'BLOK-A01' | refcnt: 1 | type: <str>", ha='center', va='center', fontsize=8, fontweight='bold', color='#22543d')
    ax.text(7.7, 1.35, "Nilai Teks Imutabel (UTF-8 Representation)", ha='center', va='center', fontsize=7.5, color='#276749')

    # Panah Referensi Pointer
    arrow_props = dict(facecolor='#dd6b20', edgecolor='#dd6b20', width=1.5, headwidth=6, shrink=0.05)
    ax.annotate('', xy=(5.3, 3.3), xytext=(3.5, 3.7), arrowprops=arrow_props)
    ax.annotate('', xy=(5.3, 3.1), xytext=(3.5, 2.5), arrowprops=arrow_props)

    arrow_str = dict(facecolor='#276749', edgecolor='#276749', width=1.5, headwidth=6, shrink=0.05)
    ax.annotate('', xy=(5.3, 1.55), xytext=(3.5, 1.4), arrowprops=arrow_str)

    # Catatan Bawah
    ax.text(5.5, 0.45, "Prinsip: Variabel di Python BUKAN wadah penyimpan nilai, melainkan penunjuk referensi memori (Pointer Binding).", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#2b6cb0',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#edf2f7', edgecolor='#cbd5e0'))

    plt.tight_layout()
    output_path = "docs/assets/arsitektur_memori_pyobject_python.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 1 disimpan ke {output_path}")

def buat_diagram_taksonomi_tipe_data():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Judul
    ax.text(5.5, 5.8, "Taksonomi Tipe Data Skalar Fundamental Python dalam Sistem Kecerdasan Buatan", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.45, "Karakteristik: Imutabilitas Objek, Alokasi Memori Fisik, & Perilaku Konversi Tipe", 
            ha='center', va='center', fontsize=9, style='italic', color='#4a5568')

    types_data = [
        {"x": 0.5, "y": 1.2, "w": 1.8, "h": 3.8, "title": "INTEGER (int)", 
         "prop": "Bilangan Bulat\nArbitrary Precision\nTanpa Overflow\nSmall Int Cache\n(-5 s/d 256)", 
         "contoh": "jumlah_tbs = 85\njanjang = -12", "bg": "#ebf8ff", "border": "#3182ce"},
        
        {"x": 2.6, "y": 1.2, "w": 1.8, "h": 3.8, "title": "FLOAT (float)", 
         "prop": "Pecahan Desimal\nIEEE 754 (64-bit)\n53-bit mantissa\n11-bit eksponen\nPresisi Terbatas", 
         "contoh": "suhu_c = 28.5\ne_to = 4.12", "bg": "#feebc8", "border": "#dd6b20"},

        {"x": 4.7, "y": 1.2, "w": 1.8, "h": 3.8, "title": "BOOLEAN (bool)", 
         "prop": "Nilai Logika\nSubkelas dari int\nTrue == 1\nFalse == 0\nOperasi Aljabar", 
         "contoh": "pompa_on = True\nstres_air = False", "bg": "#c6f6d5", "border": "#276749"},

        {"x": 6.8, "y": 1.2, "w": 1.8, "h": 3.8, "title": "STRING (str)", 
         "prop": "Deret Karakter\nImutabel Murni\nUTF-8 Unicode\nText Sequence\nIndexing O(1)", 
         "contoh": "kode = 'BLOK-A'\nvarietas = 'DxP'", "bg": "#fefcbf", "border": "#d69e2e"},

        {"x": 8.9, "y": 1.2, "w": 1.6, "h": 3.8, "title": "NONE (NoneType)", 
         "prop": "Objek Tunggal\n(Singleton)\nMissing Value\nNull Pointer\nIdentitas via `is`", 
         "contoh": "sensor = None\nerr = None", "bg": "#edf2f7", "border": "#4a5568"},
    ]

    for td in types_data:
        rect = patches.FancyBboxPatch((td["x"], td["y"]), td["w"], td["h"], boxstyle="round,pad=0.1", 
                                      facecolor=td["bg"], edgecolor=td["border"], linewidth=2)
        ax.add_patch(rect)
        ax.text(td["x"] + td["w"]/2, td["y"] + td["h"] - 0.35, td["title"], 
                ha='center', va='center', fontsize=9, fontweight='bold', color='#1a202c')
        ax.text(td["x"] + td["w"]/2, td["y"] + 2.1, td["prop"], 
                ha='center', va='center', fontsize=7.5, color='#2d3748', linespacing=1.3)
        
        # Kotak contoh kode kecil di bawah
        c_box = patches.FancyBboxPatch((td["x"]+0.1, td["y"]+0.2), td["w"]-0.2, 0.9, boxstyle="round,pad=0.05", 
                                       facecolor="#ffffff", edgecolor="#cbd5e0", linewidth=1)
        ax.add_patch(c_box)
        ax.text(td["x"] + td["w"]/2, td["y"] + 0.65, td["contoh"], 
                ha='center', va='center', fontsize=7, family='monospace', color='#4a5568')

    # Keterangan Bawah
    ax.text(5.5, 0.5, "Seluruh Tipe Data Skalar di Atas Bersifat IMUTABEL (Tidak Dapat Dimodifikasi Nilai Internalnya Setelah Instansiasi)", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#c53030',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff5f5', edgecolor='#feb2b2'))

    plt.tight_layout()
    output_path = "docs/assets/taksonomi_tipe_data_skalar_ai.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 2 disimpan ke {output_path}")

if __name__ == '__main__':
    os.makedirs('docs/assets', exist_ok=True)
    buat_diagram_arsitektur_pyobject()
    buat_diagram_taksonomi_tipe_data()
    
    artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"
    shutil.copy("docs/assets/arsitektur_memori_pyobject_python.png", os.path.join(artifact_dir, "arsitektur_memori_pyobject_python.png"))
    shutil.copy("docs/assets/taksonomi_tipe_data_skalar_ai.png", os.path.join(artifact_dir, "taksonomi_tipe_data_skalar_ai.png"))
    print("[OK] Seluruh diagram berhasil disalin ke artifacts directory.")
