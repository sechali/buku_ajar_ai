import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13, 5.5), dpi=300)

for ax in [ax1, ax2, ax3]:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

arrow_style = dict(arrowstyle="->", color="#333333", lw=2, mutation_scale=15)

# 1. SEKUANSIAL (Sequence)
ax1.set_title("1. Struktur Sekuensial\n(Eksekusi Berurutan Garis Lurus)", fontsize=11, fontweight='bold', pad=10)
b1 = patches.FancyBboxPatch((1.5, 7.5), 7, 1.5, boxstyle="round,pad=0.2", fc="#1f77b4", alpha=0.2, ec="#1f77b4", lw=2)
b2 = patches.FancyBboxPatch((1.5, 4.5), 7, 1.5, boxstyle="round,pad=0.2", fc="#1f77b4", alpha=0.2, ec="#1f77b4", lw=2)
b3 = patches.FancyBboxPatch((1.5, 1.5), 7, 1.5, boxstyle="round,pad=0.2", fc="#1f77b4", alpha=0.2, ec="#1f77b4", lw=2)

for b in [b1, b2, b3]: ax1.add_patch(b)
ax1.text(5, 8.25, "Langkah 1: Baca Sensor IoT\n(Suhu & Kelembaban Tanah)", ha='center', va='center', fontsize=8.5, fontweight='bold')
ax1.text(5, 5.25, "Langkah 2: Normalisasi Skala Data\n(Transformasi Z-Score Fitur)", ha='center', va='center', fontsize=8.5, fontweight='bold')
ax1.text(5, 2.25, "Langkah 3: Simpan ke Buffer Memori\n(Array Vektor 1D)", ha='center', va='center', fontsize=8.5, fontweight='bold')

ax1.annotate("", xy=(5, 6.0), xytext=(5, 7.5), arrowprops=arrow_style)
ax1.annotate("", xy=(5, 3.0), xytext=(5, 4.5), arrowprops=arrow_style)

# 2. PERCABANGAN (Selection / Branching)
ax2.set_title("2. Struktur Percabangan\n(Logika Seleksi Kondisional)", fontsize=11, fontweight='bold', pad=10)
# Diamond decision
diamond = patches.Polygon([[5, 8.5], [8.5, 6.5], [5, 4.5], [1.5, 6.5]], closed=True, fc="#ff7f0e", alpha=0.25, ec="#ff7f0e", lw=2)
ax2.add_patch(diamond)
ax2.text(5, 6.5, "Apakah Kelembaban\n< 45% ?", ha='center', va='center', fontsize=8.5, fontweight='bold')

box_yes = patches.FancyBboxPatch((0.5, 1.5), 4, 1.8, boxstyle="round,pad=0.2", fc="#2ca02c", alpha=0.2, ec="#2ca02c", lw=2)
box_no = patches.FancyBboxPatch((5.5, 1.5), 4, 1.8, boxstyle="round,pad=0.2", fc="#d62728", alpha=0.2, ec="#d62728", lw=2)
ax2.add_patch(box_yes)
ax2.add_patch(box_no)

ax2.text(2.5, 2.4, "BENAR (True):\nBuka Katup Irigasi\nPompa Air Nyala", ha='center', va='center', fontsize=8, fontweight='bold', color="#1b7837")
ax2.text(7.5, 2.4, "SALAH (False):\nKatup Tetap Tutup\nMode Standby Hemat", ha='center', va='center', fontsize=8, fontweight='bold', color="#b2182b")

ax2.annotate("", xy=(2.5, 3.3), xytext=(3.0, 5.5), arrowprops=arrow_style)
ax2.text(2.2, 4.5, "Ya", fontsize=9, fontweight='bold', color="green")
ax2.annotate("", xy=(7.5, 3.3), xytext=(7.0, 5.5), arrowprops=arrow_style)
ax2.text(7.4, 4.5, "Tidak", fontsize=9, fontweight='bold', color="red")

# 3. PERULANGAN (Iteration / Loop)
ax3.set_title("3. Struktur Perulangan\n(Iterasi Konvergensi Model AI)", fontsize=11, fontweight='bold', pad=10)
box_init = patches.FancyBboxPatch((2, 8.2), 6, 1.2, boxstyle="round,pad=0.2", fc="#9467bd", alpha=0.2, ec="#9467bd", lw=2)
diamond_loop = patches.Polygon([[5, 7.2], [8.5, 5.5], [5, 3.8], [1.5, 5.5]], closed=True, fc="#9467bd", alpha=0.25, ec="#9467bd", lw=2)
box_step = patches.FancyBboxPatch((1.5, 1.2), 7, 1.6, boxstyle="round,pad=0.2", fc="#9467bd", alpha=0.2, ec="#9467bd", lw=2)

ax3.add_patch(box_init)
ax3.add_patch(diamond_loop)
ax3.add_patch(box_step)

ax3.text(5, 8.8, "Inisialisasi Epoch = 1, Error = 1.0", ha='center', va='center', fontsize=8, fontweight='bold')
ax3.text(5, 5.5, "Error > 0.01 &\nEpoch <= 100 ?", ha='center', va='center', fontsize=8.5, fontweight='bold')
ax3.text(5, 2.0, "Update Bobot Model via Gradien:\nw = w - lr * dJ/dw; Epoch += 1", ha='center', va='center', fontsize=8, fontweight='bold')

ax3.annotate("", xy=(5, 7.2), xytext=(5, 8.2), arrowprops=arrow_style)
ax3.annotate("", xy=(5, 2.8), xytext=(5, 3.8), arrowprops=arrow_style)
ax3.text(5.2, 3.3, "Ya (Ulangi)", fontsize=8.5, fontweight='bold', color="purple")

# Loop back arrow from bottom to diamond
loop_arrow = dict(arrowstyle="->", color="#9467bd", lw=2, connectionstyle="arc3,rad=-0.8", mutation_scale=15)
ax3.annotate("", xy=(1.5, 5.5), xytext=(1.5, 2.0), arrowprops=loop_arrow)

plt.suptitle("Tiga Struktur Kontrol Logika Fondasi Pemrograman Algoritmik AI", fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\struktur_kontrol_algoritma_ai.png", dpi=300, bbox_inches='tight')
plt.close()
print("Control structures plot generated successfully.")
