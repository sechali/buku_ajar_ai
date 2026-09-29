"""Script to generate high-resolution (300 DPI) diagrams for AI Modul 3.7
Struktur Data Lanjut: List, Tuple, Dictionary, dan Set
1. arsitektur_memori_list_vs_tuple.png
2. mekanisme_hash_table_dict_python.png
"""

import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directories exist
os.makedirs("docs/assets", exist_ok=True)
artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"

def generate_diagram_list_vs_tuple():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "KOMPARASI MODEL MEMORI CPYTHON: LIST VS TUPLE", 
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Larik Dinamis Beralokasi Lebih (Over-allocated Dynamic Array) vs Struktur Tetap Imutabel (Fixed Struct)", 
            ha="center", va="center", fontsize=8.5, style="italic", color="#4a5568")

    # Left Container: PyListObject (Dynamic Array)
    rect_list = patches.FancyBboxPatch((4, 12), 43, 76, boxstyle="round,pad=1.2", 
                                       facecolor="#fef2f2", edgecolor="#dc2626", linewidth=2.0)
    ax.add_patch(rect_list)
    ax.text(25.5, 84, "PyListObject (Mutabel)", ha="center", fontsize=11, fontweight="bold", color="#991b1b")
    ax.text(25.5, 80, "Larik Dinamis dengan Over-allocation", ha="center", fontsize=8, color="#b91c1c")

    # List Header components
    ax.text(7, 74, "Header PyObject_VAR_HEAD:", fontsize=8, fontweight="bold", color="#7f1d1d")
    ax.text(9, 70, "• ob_refcnt: 1\n• ob_type: &PyList_Type\n• ob_size: 3 (elemen aktif)\n• allocated: 6 (kapasitas slot fisik)", 
            fontsize=7.5, fontfamily="monospace", color="#450a0a")

    # List Pointer Slots
    ax.text(7, 52, "Larik Pointer Fisik (ob_item):", fontsize=8, fontweight="bold", color="#7f1d1d")
    slots = ["PTR -> #1", "PTR -> #2", "PTR -> #3", "SLOT KOSONG", "SLOT KOSONG", "SLOT KOSONG"]
    colors = ["#fca5a5", "#fca5a5", "#fca5a5", "#e5e7eb", "#e5e7eb", "#e5e7eb"]
    for i, (slot, c) in enumerate(zip(slots, colors)):
        y = 45 - i * 5
        rect_s = patches.Rectangle((8, y), 35, 4.2, facecolor=c, edgecolor="#991b1b" if i<3 else "#9ca3af", lw=1)
        ax.add_patch(rect_s)
        txt_c = "#7f1d1d" if i<3 else "#6b7280"
        ax.text(9.5, y + 2.1, f"[{i}] {slot}", va="center", fontsize=7.5, fontfamily="monospace", fontweight="bold", color=txt_c)

    ax.text(25.5, 14, "Biaya: Ukuran memori lebih besar untuk menampung\noperasi append() instan O(1) amortized.", 
            ha="center", fontsize=7, style="italic", color="#7f1d1d")

    # Right Container: PyTupleObject (Fixed Compact Struct)
    rect_tup = patches.FancyBboxPatch((53, 12), 43, 76, boxstyle="round,pad=1.2", 
                                      facecolor="#eff6ff", edgecolor="#2563eb", linewidth=2.0)
    ax.add_patch(rect_tup)
    ax.text(74.5, 84, "PyTupleObject (Imutabel)", ha="center", fontsize=11, fontweight="bold", color="#1e40af")
    ax.text(74.5, 80, "Struktur Ramping Pas Ukuran (Zero Over-allocation)", ha="center", fontsize=8, color="#1d4ed8")

    # Tuple Header components
    ax.text(56, 74, "Header PyObject_VAR_HEAD:", fontsize=8, fontweight="bold", color="#1e3a8a")
    ax.text(58, 70, "• ob_refcnt: 1\n• ob_type: &PyTuple_Type\n• ob_size: 3 (elemen tetap)\n• (Tanpa atribut allocated)", 
            fontsize=7.5, fontfamily="monospace", color="#172554")

    # Tuple Pointer Slots
    ax.text(56, 52, "Larik Pointer Fisik Terintegrasi (ob_item):", fontsize=8, fontweight="bold", color="#1e3a8a")
    t_slots = ["PTR -> #1", "PTR -> #2", "PTR -> #3"]
    t_colors = ["#93c5fd", "#93c5fd", "#93c5fd"]
    for i, (slot, c) in enumerate(zip(t_slots, t_colors)):
        y = 45 - i * 5
        rect_s = patches.Rectangle((57, y), 35, 4.2, facecolor=c, edgecolor="#1e40af", lw=1)
        ax.add_patch(rect_s)
        ax.text(58.5, y + 2.1, f"[{i}] {slot}", va="center", fontsize=7.5, fontfamily="monospace", fontweight="bold", color="#1e3a8a")

    ax.text(74.5, 26, "[Hemat Memori & Cache-Friendly]", ha="center", fontsize=8, fontweight="bold", color="#1e40af")
    ax.text(74.5, 20, "Alokasi satu blok memori contiguous.\nTidak dapat diubah (append/pop dilarang).\nDioptimasi melalui tuple caching global.", 
            ha="center", fontsize=7.5, color="#1d4ed8")

    ax.text(74.5, 14, "Keuntungan: Ukuran RAM minimal, akses super cepat,\nserta dapat dijadikan kunci Dictionary.", 
            ha="center", fontsize=7, style="italic", color="#1e3a8a")

    plt.tight_layout()
    target_path = "docs/assets/arsitektur_memori_list_vs_tuple.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")
    shutil.copy(target_path, os.path.join(artifact_dir, "arsitektur_memori_list_vs_tuple.png"))


def generate_diagram_hash_table():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "ARSITEKTUR HASH TABLE DICTIONARY PYTHON (PEP 468 COMPACT DICT)", 
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Pemisahan Tabel Indeks Jarang (Sparse Indices) dan Larik Entri Padat (Dense Entries Array) untuk Akses O(1)", 
            ha="center", va="center", fontsize=8.5, style="italic", color="#4a5568")

    # Key Input & Hash function
    rect_k = patches.FancyBboxPatch((4, 48), 22, 34, boxstyle="round,pad=0.8", 
                                    facecolor="#fef3c7", edgecolor="#d97706", linewidth=1.8)
    ax.add_patch(rect_k)
    ax.text(15, 77, "1. KUNCI INPUT", ha="center", fontsize=9.5, fontweight="bold", color="#92400e")
    ax.text(15, 71, 'kunci = "BLOK-A01"', ha="center", fontsize=8, fontfamily="monospace", color="#78350f")
    ax.text(15, 62, "hash(\"BLOK-A01\")\n= 849204128491", ha="center", fontsize=7.5, fontfamily="monospace", color="#b45309")
    ax.text(15, 52, "Indeks Hash (Mod 8):\n849... & 0x07 = 3", ha="center", fontsize=7.5, fontfamily="monospace", fontweight="bold", color="#b45309")

    # Arrow from Key to Sparse Table
    ax.annotate("", xy=(30, 65), xytext=(26, 65),
                arrowprops=dict(facecolor="#d97706", edgecolor="#92400e", width=1.5, headwidth=6))

    # Sparse Indices Array (Table 1)
    rect_sp = patches.FancyBboxPatch((30, 20), 22, 64, boxstyle="round,pad=1.0", 
                                     facecolor="#f0fdf4", edgecolor="#16a34a", linewidth=2.0)
    ax.add_patch(rect_sp)
    ax.text(41, 79, "2. SPARSE INDICES", ha="center", fontsize=9.5, fontweight="bold", color="#14532d")
    ax.text(41, 75, "Larik Indeks Hash (Kecil)", ha="center", fontsize=7.5, color="#15803d")

    sparse_vals = ["-1 (Kosong)", "-1 (Kosong)", "Entri #1", "Entri #0", "-1 (Kosong)", "Entri #2", "-1 (Kosong)", "-1 (Kosong)"]
    for i, sv in enumerate(sparse_vals):
        y = 68 - i * 5.8
        is_hit = (i == 3)
        c = "#bbf7d0" if is_hit else "#ffffff"
        bc = "#15803d" if is_hit else "#cbd5e1"
        rect_row = patches.Rectangle((32, y), 18, 4.8, facecolor=c, edgecolor=bc, lw=1.2)
        ax.add_patch(rect_row)
        txt_style = "bold" if is_hit else "normal"
        ax.text(33.5, y + 2.4, f"[{i}] {sv}", va="center", fontsize=7, fontfamily="monospace", fontweight=txt_style, color="#14532d" if is_hit else "#64748b")

    # Arrow from Sparse to Dense Table
    ax.annotate("", xy=(57, 51), xytext=(50, 51),
                arrowprops=dict(facecolor="#16a34a", edgecolor="#14532d", width=2, headwidth=6))
    ax.text(53.5, 54, "Pointer", ha="center", fontsize=7, fontweight="bold", color="#14532d")

    # Dense Entries Array (Table 2 - Memory ordered insertion)
    rect_de = patches.FancyBboxPatch((57, 20), 39, 64, boxstyle="round,pad=1.0", 
                                     facecolor="#f5f3ff", edgecolor="#7c3aed", linewidth=2.0)
    ax.add_patch(rect_de)
    ax.text(76.5, 79, "3. DENSE ENTRIES ARRAY", ha="center", fontsize=9.5, fontweight="bold", color="#5b21b6")
    ax.text(76.5, 75, "Larik Padat Terurut Waktu Penyisipan (Preserves Order)", ha="center", fontsize=7.5, color="#6d28d9")

    # Columns header
    ax.text(59, 69, "Index | Hash Value  | Key Pointer | Value Pointer", fontsize=7.5, fontfamily="monospace", fontweight="bold", color="#4c1d95")

    dense_rows = [
        ("0", "849204128491", '"BLOK-A01"', "NDVI: 0.82 (Sehat)"),
        ("1", "410294819284", '"BLOK-B02"', "NDVI: 0.45 (Stres)"),
        ("2", "719385018293", '"BLOK-C03"', "NDVI: 0.78 (Sehat)"),
    ]
    for i, (idx, hv, k, v) in enumerate(dense_rows):
        y = 60 - i * 11
        is_target = (i == 0)
        c = "#ddd6fe" if is_target else "#ffffff"
        bc = "#7c3aed" if is_target else "#cbd5e1"
        rect_row = patches.Rectangle((59, y), 35, 9.5, facecolor=c, edgecolor=bc, lw=1.2)
        ax.add_patch(rect_row)
        ax.text(60.5, y + 6.5, f"Entri #{idx}: Hash={hv[:6]}...", fontsize=7.5, fontfamily="monospace", fontweight="bold", color="#4c1d95")
        ax.text(60.5, y + 2.5, f"  Key: {k} -> Val: {v}", fontsize=7, fontfamily="monospace", color="#5b21b6")

    # Bottom Explanation
    rect_bot = patches.Rectangle((4, 4), 92, 12, facecolor="#f8fafc", edgecolor="#94a3b8", lw=1)
    ax.add_patch(rect_bot)
    ax.text(50, 11, "Keuntungan Desain PEP 468 (Python 3.6+):", ha="center", fontsize=8, fontweight="bold", color="#0f172a")
    ax.text(50, 7, "1. Penghematan Memori 30-40% karena tabel jarang hanya menyimpan integer indeks.\n2. Iterasi Dictionary secara deterministik menjamin urutan penyisipan (Insertion-Order Preservation).", 
            ha="center", fontsize=7.5, color="#334155")

    plt.tight_layout()
    target_path = "docs/assets/mekanisme_hash_table_dict_python.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")
    shutil.copy(target_path, os.path.join(artifact_dir, "mekanisme_hash_table_dict_python.png"))


if __name__ == "__main__":
    generate_diagram_list_vs_tuple()
    generate_diagram_hash_table()
    print("All Modul 3.7 diagrams generated successfully!")
