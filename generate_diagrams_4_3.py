import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('e:/Project Buku/docs/assets', exist_ok=True)
artifact_dir = r'C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11'

# -------------------------------------------------------------
# Diagram 1: Arsitektur Internal Pandas DataFrame (BlockManager)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 7.5), dpi=300)
ax.set_xlim(0, 15)
ax.set_ylim(0, 9.5)
ax.axis('off')
ax.set_title("Arsitektur Internal Pandas DataFrame: Indeks, Kolom, dan Pengelola Blok (BlockManager)", 
             fontsize=13, fontweight='bold', pad=15, color='#0F172A')

# 1. User View: 2D Table
user_box = patches.FancyBboxPatch((0.5, 3.8), 5.5, 4.8, boxstyle="round,pad=0.2", fc="#EFF6FF", ec="#2563EB", lw=2)
ax.add_patch(user_box)
ax.text(3.25, 8.2, "Tampilan Logis Pengguna (2D Tabular DataFrame)", fontsize=10, fontweight='bold', ha='center', color="#1E40AF")

# Table drawing
cols_table = ["Index", "Blok_ID", "Tonase", "NDVI", "Afdeling"]
x_cols = [1.0, 2.0, 3.1, 4.1, 5.1]
for idx, col in enumerate(cols_table):
    cbox = patches.Rectangle((x_cols[idx]-0.4, 7.3), 0.9, 0.5, fc="#DBEAFE", ec="#1D4ED8", lw=1)
    ax.add_patch(cbox)
    ax.text(x_cols[idx], 7.55, col, fontsize=8, fontweight='bold', ha='center', va='center', color="#1E3A8A")

rows_sample = [
    ("0", "B-01", "24.5", "0.78", "AFD-1"),
    ("1", "B-02", "18.2", "0.65", "AFD-1"),
    ("2", "B-03", "29.1", "0.82", "AFD-2"),
    ("3", "B-04", "15.8", "0.59", "AFD-2")
]
for r_idx, r_data in enumerate(rows_sample):
    y_pos = 6.6 - r_idx*0.6
    for c_idx, val in enumerate(r_data):
        rbox = patches.Rectangle((x_cols[c_idx]-0.4, y_pos), 0.9, 0.45, fc="white", ec="#93C5FD", lw=0.8)
        ax.add_patch(rbox)
        ax.text(x_cols[c_idx], y_pos+0.22, val, fontsize=8, ha='center', va='center', color="#1E293B")

ax.text(3.25, 4.2, "DataFrame = Koleksi Series yang Berbagi Index Baris", 
        fontsize=8.5, ha='center', style='italic', color="#1E40AF")

# Arrow to internal structure
ax.annotate("", xy=(7.2, 6.2), xytext=(6.2, 6.2), 
            arrowprops=dict(arrowstyle="-|>", lw=3, color="#64748B", mutation_scale=22))
ax.text(6.7, 6.6, "Dikelola\nOleh", fontsize=8.5, fontweight='bold', ha='center', color="#475569")

# 2. Internal View: BlockManager
internal_box = patches.FancyBboxPatch((7.5, 0.8), 7.0, 7.8, boxstyle="round,pad=0.2", fc="#F8FAFC", ec="#334155", lw=2)
ax.add_patch(internal_box)
ax.text(11.0, 8.2, "Struktur Fisik Internal: BlockManager & 1D/2D Array", fontsize=10, fontweight='bold', ha='center', color="#0F172A")

# Float Block
f_box = patches.FancyBboxPatch((8.0, 5.7), 6.0, 2.0, boxstyle="round,pad=0.15", fc="#DCFCE7", ec="#16A34A", lw=1.5)
ax.add_patch(f_box)
ax.text(11.0, 7.3, "FloatBlock (2D NumPy Array Contiguous float64)", fontsize=9, fontweight='bold', ha='center', color="#166534")
ax.text(11.0, 6.7, "Kolom: ['Tonase', 'NDVI'] (Shape: 2 x 4)\nAlokasi memori tunggal berurutan, cepat untuk SIMD", fontsize=8.5, ha='center', color="#14532D")
ax.text(11.0, 6.0, "[[24.5, 18.2, 29.1, 15.8], [0.78, 0.65, 0.82, 0.59]]", fontsize=7.5, family='monospace', ha='center', color="#14532D")

# Object/String Block
o_box = patches.FancyBboxPatch((8.0, 3.3), 6.0, 2.0, boxstyle="round,pad=0.15", fc="#FEF3C7", ec="#D97706", lw=1.5)
ax.add_patch(o_box)
ax.text(11.0, 4.9, "ObjectBlock / StringBlock (Pointers Array)", fontsize=9, fontweight='bold', ha='center', color="#92400E")
ax.text(11.0, 4.3, "Kolom: ['Blok_ID', 'Afdeling'] (Shape: 2 x 4)\nBerisi pointer ke objek string Python di heap", fontsize=8.5, ha='center', color="#78350F")
ax.text(11.0, 3.6, "['B-01', 'B-02', ...] & ['AFD-1', 'AFD-1', ...]", fontsize=7.5, family='monospace', ha='center', color="#78350F")

# Index & Columns Metadata
idx_box = patches.FancyBboxPatch((8.0, 1.2), 6.0, 1.7, boxstyle="round,pad=0.15", fc="#EDE9FE", ec="#7C3AED", lw=1.5)
ax.add_patch(idx_box)
ax.text(11.0, 2.5, "Index Metadata (Hash-Map Berkinerja Tinggi)", fontsize=9, fontweight='bold', ha='center', color="#5B21B6")
ax.text(11.0, 1.8, "• Axis 0 (Index Baris): RangeIndex(0, 4)\n• Axis 1 (Index Kolom): Index(['Blok_ID', 'Tonase', ...])\nPencarian O(1) via tabel hash C internal", fontsize=8, ha='center', color="#4C1D95")

# Bottom info
bot_box = patches.FancyBboxPatch((0.5, 0.8), 5.5, 2.5, boxstyle="round,pad=0.15", fc="#FFF1F2", ec="#E11D48", lw=1.5)
ax.add_patch(bot_box)
ax.text(3.25, 2.8, "Wawasan Kinerja Sains Data:", fontsize=9, fontweight='bold', ha='center', color="#9F1239")
ax.text(3.25, 1.8, "Mengelompokkan kolom bertipe data sama\nmenghindari overhead konversi tipe data.\nOperasi numerik kolom 'Tonase' + 'NDVI'\nberjalan secepat C langsung di FloatBlock!", 
        fontsize=8.5, ha='center', color="#881337")

plt.tight_layout()
out1 = 'e:/Project Buku/docs/assets/arsitektur_internal_pandas_dataframe.png'
plt.savefig(out1, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'arsitektur_internal_pandas_dataframe.png'), dpi=300)
plt.close()
print("Saved:", out1)

# -------------------------------------------------------------
# Diagram 2: Mekanisme Split-Apply-Combine pada GroupBy
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 7.5), dpi=300)
ax.set_xlim(0, 15)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_title("Mekanisme Paradigma Split-Apply-Combine pada Operasi GroupBy Agribisnis", 
             fontsize=13, fontweight='bold', pad=15, color='#0F172A')

# 1. Dataset Awal (Tabel Panen)
box1 = patches.FancyBboxPatch((0.5, 2.2), 3.4, 5.2, boxstyle="round,pad=0.15", fc="#EFF6FF", ec="#1D4ED8", lw=2)
ax.add_patch(box1)
ax.text(2.2, 7.0, "1. Dataset Mentah Panen", fontsize=9.5, fontweight='bold', ha='center', color="#1E40AF")

data_rows = [
    ("AFD-A", "24.0"),
    ("AFD-B", "18.5"),
    ("AFD-A", "26.5"),
    ("AFD-B", "20.0"),
    ("AFD-A", "25.0"),
    ("AFD-C", "31.0")
]
y_init = 6.2
for afd, ton in data_rows:
    bg = "#DCFCE7" if afd == "AFD-A" else ("#FEF3C7" if afd == "AFD-B" else "#FCE7F3")
    rbox = patches.Rectangle((0.8, y_init-0.35), 2.8, 0.45, fc=bg, ec="#64748B", lw=1)
    ax.add_patch(rbox)
    ax.text(1.5, y_init-0.12, afd, fontsize=8.5, fontweight='bold', ha='center', color="#1E293B")
    ax.text(2.9, y_init-0.12, f"{ton} Ton", fontsize=8.5, ha='center', color="#1E293B")
    y_init -= 0.65

# SPLIT Phase
ax.annotate("", xy=(5.2, 5.0), xytext=(4.1, 5.0), 
            arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#2563EB", mutation_scale=18))
ax.text(4.65, 5.4, "SPLIT\n(Berdasarkan\nAfdeling)", fontsize=8, fontweight='bold', ha='center', color="#2563EB")

# 2. Split Groups
box_grp_a = patches.FancyBboxPatch((5.4, 5.8), 2.8, 1.8, boxstyle="round,pad=0.1", fc="#DCFCE7", ec="#16A34A", lw=1.5)
ax.add_patch(box_grp_a)
ax.text(6.8, 7.2, "Grup Afdeling A", fontsize=8.5, fontweight='bold', ha='center', color="#166534")
ax.text(6.8, 6.4, "24.0, 26.5, 25.0", fontsize=8, ha='center', color="#14532D")

box_grp_b = patches.FancyBboxPatch((5.4, 3.6), 2.8, 1.8, boxstyle="round,pad=0.1", fc="#FEF3C7", ec="#D97706", lw=1.5)
ax.add_patch(box_grp_b)
ax.text(6.8, 5.0, "Grup Afdeling B", fontsize=8.5, fontweight='bold', ha='center', color="#92400E")
ax.text(6.8, 4.2, "18.5, 20.0", fontsize=8, ha='center', color="#78350F")

box_grp_c = patches.FancyBboxPatch((5.4, 1.4), 2.8, 1.8, boxstyle="round,pad=0.1", fc="#FCE7F3", ec="#DB2777", lw=1.5)
ax.add_patch(box_grp_c)
ax.text(6.8, 2.8, "Grup Afdeling C", fontsize=8.5, fontweight='bold', ha='center', color="#9D174D")
ax.text(6.8, 2.0, "31.0", fontsize=8, ha='center', color="#831843")

# APPLY Phase
for gy in [6.7, 4.5, 2.3]:
    ax.annotate("", xy=(9.7, gy), xytext=(8.4, gy), 
                arrowprops=dict(arrowstyle="-|>", lw=2, color="#059669", mutation_scale=16))
ax.text(9.05, 5.8, "APPLY\n(Fungsi Agregasi\nContoh: Rerata / Sum)", fontsize=8, fontweight='bold', ha='center', color="#059669")

# 3. Apply results
res_a = patches.FancyBboxPatch((9.9, 6.1), 1.6, 1.2, boxstyle="round,pad=0.1", fc="#BBF7D0", ec="#16A34A", lw=1.5)
ax.add_patch(res_a)
ax.text(10.7, 6.7, "Rerata:\n25.17 Ton", fontsize=8, fontweight='bold', ha='center', color="#14532D")

res_b = patches.FancyBboxPatch((9.9, 3.9), 1.6, 1.2, boxstyle="round,pad=0.1", fc="#FDE68A", ec="#D97706", lw=1.5)
ax.add_patch(res_b)
ax.text(10.7, 4.5, "Rerata:\n19.25 Ton", fontsize=8, fontweight='bold', ha='center', color="#78350F")

res_c = patches.FancyBboxPatch((9.9, 1.7), 1.6, 1.2, boxstyle="round,pad=0.1", fc="#FBCFE8", ec="#DB2777", lw=1.5)
ax.add_patch(res_c)
ax.text(10.7, 2.3, "Rerata:\n31.00 Ton", fontsize=8, fontweight='bold', ha='center', color="#831843")

# COMBINE Phase
ax.annotate("", xy=(12.2, 4.5), xytext=(11.7, 6.4), arrowprops=dict(arrowstyle="-|>", lw=2, color="#7C3AED"))
ax.annotate("", xy=(12.2, 4.5), xytext=(11.7, 4.5), arrowprops=dict(arrowstyle="-|>", lw=2, color="#7C3AED"))
ax.annotate("", xy=(12.2, 4.5), xytext=(11.7, 2.6), arrowprops=dict(arrowstyle="-|>", lw=2, color="#7C3AED"))
ax.text(12.0, 5.5, "COMBINE", fontsize=8, fontweight='bold', ha='center', color="#7C3AED")

# 4. Final Aggregated Table
box_final = patches.FancyBboxPatch((12.4, 2.5), 2.3, 4.4, boxstyle="round,pad=0.15", fc="#FAF5FF", ec="#7C3AED", lw=2)
ax.add_patch(box_final)
ax.text(13.55, 6.5, "Rekapitulasi\n(Hasil Akhir)", fontsize=8.5, fontweight='bold', ha='center', color="#5B21B6")

final_rows = [
    ("Afdeling", "Rerata_Ton"),
    ("AFD-A", "25.17"),
    ("AFD-B", "19.25"),
    ("AFD-C", "31.00")
]
fy = 5.6
for f_afd, f_val in final_rows:
    f_bg = "#EDE9FE" if f_afd == "Afdeling" else "white"
    frbox = patches.Rectangle((12.6, fy-0.3), 1.9, 0.45, fc=f_bg, ec="#8B5CF6", lw=0.8)
    ax.add_patch(frbox)
    ax.text(13.0, fy-0.08, f_afd, fontsize=7.5, fontweight='bold' if f_afd == "Afdeling" else 'normal', ha='center', color="#3B0764")
    ax.text(14.0, fy-0.08, f_val, fontsize=7.5, fontweight='bold' if f_afd == "Afdeling" else 'normal', ha='center', color="#3B0764")
    fy -= 0.65

plt.tight_layout()
out2 = 'e:/Project Buku/docs/assets/mekanisme_split_apply_combine_pandas.png'
plt.savefig(out2, dpi=300)
plt.savefig(os.path.join(artifact_dir, 'mekanisme_split_apply_combine_pandas.png'), dpi=300)
plt.close()
print("Saved:", out2)
