import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

for ax in [ax1, ax2]:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

# --- Panel 1: Sistem Tradisional (Rule-based) ---
ax1.set_title('(A) Paradigma Pemrograman Tradisional', fontsize=11, fontweight='bold', pad=10)

b_data1 = patches.FancyBboxPatch((1, 7), 3.5, 1.6, boxstyle='round,pad=0.1', facecolor='#D6EAF8', edgecolor='#2980B9', lw=1.5)
b_rules1 = patches.FancyBboxPatch((1, 4), 3.5, 1.6, boxstyle='round,pad=0.1', facecolor='#D6EAF8', edgecolor='#2980B9', lw=1.5)
b_comp1 = patches.FancyBboxPatch((5.5, 4.8), 3.8, 3.0, boxstyle='round,pad=0.15', facecolor='#FCF3CF', edgecolor='#D4AC0D', lw=1.5)
b_out1 = patches.FancyBboxPatch((5.5, 1.2), 3.8, 1.8, boxstyle='round,pad=0.1', facecolor='#D5F5E3', edgecolor='#27AE60', lw=1.5)

for b in [b_data1, b_rules1, b_comp1, b_out1]: ax1.add_patch(b)

ax1.text(2.75, 7.8, 'DATA INPUT\n(Fakta / Angka)', ha='center', va='center', fontweight='bold', fontsize=9)
ax1.text(2.75, 4.8, 'RULES (ATURAN)\n(Ditulis Manual oleh\nProgrammer / Pakar)', ha='center', va='center', fontweight='bold', fontsize=9)
ax1.text(7.4, 6.3, 'KOMPUTER /\nMESIN ATURAN\n(Eksekusi Logika If-Else)', ha='center', va='center', fontweight='bold', fontsize=9.5)
ax1.text(7.4, 2.1, 'OUTPUT / KEPUTUSAN\n(Jawaban Pasti)', ha='center', va='center', fontweight='bold', fontsize=9.5)

ax1.annotate('', xy=(5.4, 7.5), xytext=(4.6, 7.5), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax1.annotate('', xy=(5.4, 5.0), xytext=(4.6, 5.0), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax1.annotate('', xy=(7.4, 3.1), xytext=(7.4, 4.7), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))

# --- Panel 2: Paradigma AI / Machine Learning ---
ax2.set_title('(B) Paradigma Artificial Intelligence / ML', fontsize=11, fontweight='bold', pad=10)

b_data2 = patches.FancyBboxPatch((1, 7), 3.5, 1.6, boxstyle='round,pad=0.1', facecolor='#D6EAF8', edgecolor='#2980B9', lw=1.5)
b_out2 = patches.FancyBboxPatch((1, 4), 3.5, 1.6, boxstyle='round,pad=0.1', facecolor='#D5F5E3', edgecolor='#27AE60', lw=1.5)
b_comp2 = patches.FancyBboxPatch((5.5, 4.8), 3.8, 3.0, boxstyle='round,pad=0.15', facecolor='#FADBD8', edgecolor='#C0392B', lw=1.5)
b_rules2 = patches.FancyBboxPatch((5.5, 1.2), 3.8, 1.8, boxstyle='round,pad=0.1', facecolor='#E8DAEF', edgecolor='#8E44AD', lw=1.5)

for b in [b_data2, b_out2, b_comp2, b_rules2]: ax2.add_patch(b)

ax2.text(2.75, 7.8, 'DATA INPUT\n(Fitur, Gambar, Sensor)', ha='center', va='center', fontweight='bold', fontsize=9)
ax2.text(2.75, 4.8, 'OUTPUT / LABEL\n(Target / Jawaban Riil)', ha='center', va='center', fontweight='bold', fontsize=9)
ax2.text(7.4, 6.3, 'ALGORITMA AI / ML\n(Optimasi & Belajar Pola\nMinimasi Error Loss)', ha='center', va='center', fontweight='bold', fontsize=9.5)
ax2.text(7.4, 2.1, 'MODEL / RULES TERPELAJAR\n(Aturan Terbentuk Otomatis)', ha='center', va='center', fontweight='bold', fontsize=9.5)

ax2.annotate('', xy=(5.4, 7.5), xytext=(4.6, 7.5), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax2.annotate('', xy=(5.4, 5.0), xytext=(4.6, 5.0), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax2.annotate('', xy=(7.4, 3.1), xytext=(7.4, 4.7), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))

plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/flowchart_aturan_vs_ai.png', dpi=300)
print('Panel comparison diagram successfully created!')
