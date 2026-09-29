import matplotlib.pyplot as plt
import numpy as np

# 1. Diagram Garis Waktu (Timeline) Pasang Surut AI
fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
ax.set_xlim(1940, 2030)
ax.set_ylim(-3, 4.5)
ax.axis('off')

# Baseline axis line
ax.axhline(0, color='#7F8C8D', linewidth=1.5, linestyle='-')

# Data timeline: (Tahun, Nilai_Y, Label_Atas, Label_Bawah, Warna, Status)
events = [
    (1950, 2.5, "1950: Turing Test\nKarya Alan Turing", "Era Fondasi\n(1943-1955)", "#2980B9"),
    (1956, 3.5, "1956: Konferensi Dartmouth\nKelahiran Istilah AI", "Kelahiran Resmi", "#1F618D"),
    (1958, 2.0, "1958: Rosenblatt Perceptron\nModel Belajar Pertama", "Gelombang 1: Optimisme", "#27AE60"),
    (1974, -2.2, "1974-1980: AI WINTER I\nKritik XOR Minsky & Lighthill", "Pembekuan Dana Riset", "#C0392B"),
    (1982, 2.5, "1980-an: Expert Systems & Backprop\nSistem Pakar XCON & MLP", "Gelombang 2: Boom Industri", "#D4AC0D"),
    (1988, -2.2, "1987-1993: AI WINTER II\nKeruntuhan Pasar Hardware LISP", "Kekecewaan Ekspektasi", "#922B21"),
    (1997, 2.0, "1997: IBM Deep Blue\nKalahkan Juara Dunia Catur", "Statistik & Machine Learning", "#2E86C1"),
    (2012, 3.5, "2012: AlexNet & Deep Learning\nRevolusi GPU & ImageNet", "Gelombang 3: Deep Learning", "#16A085"),
    (2017, 2.2, "2017: Transformer (Attention)\nVaswani et al.", "Fondasi Model Bahasa", "#8E44AD"),
    (2023, 3.8, "2023-Kini: Foundation Models & GenAI\nChatGPT, Claude, Gemini, Agentic AI", "Era Kecerdasan Modern", "#6C3483")
]

for year, y_val, top_text, btm_text, color in events:
    # Stem line
    ax.plot([year, year], [0, y_val], color=color, linewidth=1.5, linestyle='--')
    # Marker dot
    ax.plot(year, 0, marker='o', markersize=7, color=color)
    ax.plot(year, y_val, marker='s', markersize=6, color=color)
    
    # Text annotation
    if y_val > 0:
        ax.text(year, y_val + 0.15, top_text, ha='center', va='bottom', fontsize=8, fontweight='bold', color=color)
        ax.text(year, -0.4, btm_text, ha='center', va='top', fontsize=7, color='#555555')
    else:
        ax.text(year, y_val - 0.15, top_text, ha='center', va='top', fontsize=8, fontweight='bold', color=color)
        ax.text(year, 0.4, btm_text, ha='center', va='bottom', fontsize=7, color='#555555')

plt.title('Kronologi Pasang Surut Sejarah Artificial Intelligence (1950 - Era Modern)', fontsize=13, fontweight='bold', pad=25, color='#2C3E50')
plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/timeline_sejarah_ai.png', dpi=300)
plt.close()

# 2. Diagram Limitasi XOR (Minsky & Papert 1969)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)

# Panel A: Gerbang AND (Linear Separable)
ax1.set_xlim(-0.5, 1.5)
ax1.set_ylim(-0.5, 1.5)
ax1.axhline(0, color='#CCC', lw=1)
ax1.axvline(0, color='#CCC', lw=1)
ax1.scatter([0, 0, 1], [0, 1, 0], color='#C0392B', s=100, label='Kelas 0 (Salah)', zorder=4)
ax1.scatter([1], [1], color='#27AE60', s=120, marker='^', label='Kelas 1 (Benar)', zorder=4)
x_vals = np.linspace(-0.2, 1.5, 100)
ax1.plot(x_vals, 1.5 - x_vals, color='#2980B9', lw=2, linestyle='--', label='Garis Pemisah Linier')
ax1.set_title('(A) Gerbang Logika AND\n(Linearly Separable - Berhasil)', fontsize=10, fontweight='bold', color='#1E8449')
ax1.set_xlabel('Input $x_1$')
ax1.set_ylabel('Input $x_2$')
ax1.legend(fontsize=8, loc='upper left')
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel B: Gerbang XOR (Non-Linearly Separable)
ax2.set_xlim(-0.5, 1.5)
ax2.set_ylim(-0.5, 1.5)
ax2.axhline(0, color='#CCC', lw=1)
ax2.axvline(0, color='#CCC', lw=1)
ax2.scatter([0, 1], [0, 1], color='#C0392B', s=100, label='Kelas 0 (Input Sama)', zorder=4)
ax2.scatter([0, 1], [1, 0], color='#27AE60', s=120, marker='^', label='Kelas 1 (Input Berbeda)', zorder=4)
ax2.text(0.5, 0.5, 'TIDAK DAPAT\nDIPISAHKAN OLEH\nSATU GARIS LURUS!', ha='center', va='center', 
         fontsize=9, fontweight='bold', color='#922B21', bbox=dict(boxstyle='round,pad=0.3', facecolor='#FADBD8', edgecolor='#C0392B'))
ax2.set_title('(B) Problem XOR (Minsky & Papert 1969)\n(Non-Linearly Separable - Pemicu AI Winter I)', fontsize=10, fontweight='bold', color='#922B21')
ax2.set_xlabel('Input $x_1$')
ax2.set_ylabel('Input $x_2$')
ax2.legend(fontsize=8, loc='upper left')
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/xor_limitation.png', dpi=300)
plt.close()
print('History and XOR diagrams generated successfully!')
