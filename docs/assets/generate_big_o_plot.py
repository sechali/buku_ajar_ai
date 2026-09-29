import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)

n = np.linspace(1, 20, 400)

# Complexity functions
o_1 = np.ones_like(n)
o_logn = np.log2(n)
o_n = n
o_nlogn = n * np.log2(n)
o_n2 = n**2
o_2n = 2**n

# Plotting curves
ax.plot(n, o_1, label='O(1) - Konstan (Luar Biasa)', color='#1a9850', linewidth=2.5)
ax.plot(n, o_logn, label='O(log N) - Logaritmik (Sangat Baik)', color='#66bd63', linewidth=2.5)
ax.plot(n, o_n, label='O(N) - Linier (Adil / Cukup)', color='#fee08b', linewidth=2.5)
ax.plot(n, o_nlogn, label='O(N log N) - Kuasilinier (Batas Optimal Sorting)', color='#fdae61', linewidth=2.5)
ax.plot(n, o_n2, label='O(N^2) - Kuadratik (Buruk)', color='#f46d43', linewidth=2.5)
ax.plot(n, o_2n, label='O(2^N) - Eksponensial (Katastrofik / Tidak Layak)', color='#d73027', linewidth=2.5, linestyle='--')

ax.set_ylim(0, 100)
ax.set_xlim(1, 16)

# Background color zones
ax.axhspan(0, 15, color='#1a9850', alpha=0.10)
ax.text(1.2, 5, "ZONA AMAN (Efisiensi Tinggi / Skalabilitas Skala Besar)", fontsize=9.5, fontweight='bold', color='#006837')

ax.axhspan(15, 50, color='#fdae61', alpha=0.10)
ax.text(1.2, 30, "ZONA MENENGAH (Wajar untuk Pemrosesan Batch Data)", fontsize=9.5, fontweight='bold', color='#a6611a')

ax.axhspan(50, 100, color='#d73027', alpha=0.10)
ax.text(1.2, 85, "ZONA KRITIS / BAHAYA (Sistem Crash pada Big Data & Edge Device)", fontsize=9.5, fontweight='bold', color='#a50026')

ax.set_title("Analisis Asimtotik Kompleksitas Waktu Algoritma (Notasi Big-O)", fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel("Ukuran Masukan Data (N Elemen)", fontsize=10.5, fontweight='bold')
ax.set_ylabel("Jumlah Operasi Komputasi Relatif", fontsize=10.5, fontweight='bold')
ax.legend(loc='upper left', fontsize=9.5, frameon=True)

plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\kurva_kompleksitas_big_o.png", dpi=300, bbox_inches='tight')
plt.close()
print("Big-O complexity plot generated successfully.")
