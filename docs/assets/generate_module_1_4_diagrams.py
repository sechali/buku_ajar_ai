import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 1. Diagram Spektrum Kapabilitas AI: ANI -> AGI -> ASI
fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 6)
ax.axis('off')

# Arrow backbone representing capability spectrum
arrow = patches.FancyArrow(0.8, 1.2, 9.4, 0, width=0.15, head_width=0.4, head_length=0.4, 
                           length_includes_head=True, facecolor='#2C3E50', edgecolor='#1A252F')
ax.add_patch(arrow)

# Stage 1: ANI
b_ani = patches.FancyBboxPatch((0.8, 2.0), 2.8, 3.2, boxstyle='round,pad=0.2', facecolor='#EBF5FB', edgecolor='#2980B9', lw=2)
# Stage 2: Broad ANI / LLM (Transisi)
b_broad = patches.FancyBboxPatch((3.9, 2.0), 2.2, 3.2, boxstyle='round,pad=0.2', facecolor='#FCF3CF', edgecolor='#F39C12', lw=2)
# Stage 3: AGI
b_agi = patches.FancyBboxPatch((6.4, 2.0), 2.0, 3.2, boxstyle='round,pad=0.2', facecolor='#D5F5E3', edgecolor='#27AE60', lw=2)
# Stage 4: ASI
b_asi = patches.FancyBboxPatch((8.7, 2.0), 1.9, 3.2, boxstyle='round,pad=0.2', facecolor='#FADBD8', edgecolor='#C0392B', lw=2)

for b in [b_ani, b_broad, b_agi, b_asi]: ax.add_patch(b)

# Stage 1 Texts
ax.text(2.2, 4.8, 'ARTIFICIAL NARROW\nINTELLIGENCE (ANI)', ha='center', va='center', fontweight='bold', fontsize=9.5, color='#1B4F72')
ax.text(2.2, 3.8, '• Status: REALITA SAAT INI (100%)\n• Sifat: Spesifik domain tunggal\n• Unggul: Catur, AlphaFold, Deteksi Daun, CCTV\n• Keterbatasan: Lumpuh jika pindah domain', 
        ha='center', va='center', fontsize=7.5, color='#2874A6')

# Stage 2 Texts
ax.text(5.0, 4.8, 'BROAD ANI\n(TRANSISI MODERN)', ha='center', va='center', fontweight='bold', fontsize=9, color='#7D6608')
ax.text(5.0, 3.8, '• Model Pondasi (LLM/VLM)\n• Multitask dalam teks/citra\n• Belum memiliki common sense\n• Masih mengalami halusinasi', 
        ha='center', va='center', fontsize=7.2, color='#7D6608')

# Stage 3 Texts
ax.text(7.4, 4.8, 'ARTIFICIAL GENERAL\nINTELLIGENCE (AGI)', ha='center', va='center', fontweight='bold', fontsize=9, color='#1E8449')
ax.text(7.4, 3.8, '• Status: HIPOTETIS / RISET\n• Setara kecerdasan manusia dewasa\n• Penalaran kausal & adaptasi lintas disiplin tanpa diprogram ulang', 
        ha='center', va='center', fontsize=7.2, color='#196F3D')

# Stage 4 Texts
ax.text(9.65, 4.8, 'ARTIFICIAL SUPER\nINTELLIGENCE (ASI)', ha='center', va='center', fontweight='bold', fontsize=9, color='#922B21')
ax.text(9.65, 3.8, '• Status: TEORI MASA DEPAN\n• Melampaui totalitas genius manusia\n• Self-improving recursion\n• Isu: Alignment Problem', 
        ha='center', va='center', fontsize=7.2, color='#78281F')

# Timeline labels below arrow
ax.text(2.2, 0.7, 'Era Sekarang (Revolusi Industri 4.0)', ha='center', fontsize=8, color='#555555', fontweight='bold')
ax.text(5.0, 0.7, 'Era Generative AI (Kini)', ha='center', fontsize=8, color='#555555', fontweight='bold')
ax.text(7.4, 0.7, 'Masa Depan (Target Riset Global)', ha='center', fontsize=8, color='#555555', fontweight='bold')
ax.text(9.65, 0.7, 'Singularitas Teknologi', ha='center', fontsize=8, color='#555555', fontweight='bold')

plt.title('Spektrum Taksonomi Kapabilitas Kecerdasan Buatan: Dari ANI Menuju ASI', fontsize=12, fontweight='bold', pad=15, color='#2C3E50')
plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/spektrum_ani_agi_asi.png', dpi=300)
plt.close()


# 2. Diagram Fenomena Catastrophic Forgetting vs Transfer Learning
fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)

steps = np.linspace(0, 100, 200)

# Tugas A (Pelatihan 0 - 50)
task_a_ani = np.zeros_like(steps)
task_b_ani = np.zeros_like(steps)

task_a_transfer = np.zeros_like(steps)
task_b_transfer = np.zeros_like(steps)

for i, s in enumerate(steps):
    if s <= 50:
        # Melatih Tugas A
        task_a_ani[i] = 95.0 * (1 - np.exp(-0.1 * s))
        task_b_ani[i] = 0.0
        
        task_a_transfer[i] = 95.0 * (1 - np.exp(-0.1 * s))
        task_b_transfer[i] = 0.0
    else:
        # Pindah Melatih Tugas B
        delta = s - 50
        # ANI: lupa tugas A secara instan (Catastrophic Forgetting)
        task_a_ani[i] = 95.0 * np.exp(-0.15 * delta)
        task_b_ani[i] = 92.0 * (1 - np.exp(-0.08 * delta))
        
        # Transfer/Meta Learning: Mempertahankan Tugas A sambil cepat menguasai Tugas B
        task_a_transfer[i] = 88.0 + 7.0 * np.exp(-0.03 * delta)
        task_b_transfer[i] = 94.0 * (1 - np.exp(-0.18 * delta)) # Belajar tugas B jauh lebih cepat!

ax.plot(steps, task_a_ani, label='Performa Tugas A pada ANI (Runtuh / Catastrophic Forgetting)', color='#C0392B', linestyle='--', lw=2.2)
ax.plot(steps, task_b_ani, label='Performa Tugas B pada ANI (Belajar dari Nol Lambat)', color='#E67E22', linestyle=':', lw=2)

ax.plot(steps, task_a_transfer, label='Performa Tugas A pada Agen Adaptif (Pengetahuan Tertahan)', color='#2980B9', lw=2.5)
ax.plot(steps, task_b_transfer, label='Performa Tugas B pada Agen Adaptif (Few-shot Transfer Cepat)', color='#27AE60', lw=2.5)

ax.axvline(50, color='#7F8C8D', linestyle='-', lw=1.5)
ax.text(25, 103, '[FASE 1: PELATIHAN TUGAS A]', ha='center', fontsize=9, fontweight='bold', color='#1A5276')
ax.text(75, 103, '[FASE 2: PINDAH KE TUGAS B]', ha='center', fontsize=9, fontweight='bold', color='#7D6608')

ax.set_title('Fenomena Catastrophic Forgetting pada ANI vs Retensi Pengetahuan pada Agen Adaptif', fontsize=11, fontweight='bold', pad=15)
ax.set_xlabel('Langkah Pembelajaran / Iterasi Waktu', fontsize=9.5)
ax.set_ylabel('Akurasi / Skor Keberhasilan Tugas (%)', fontsize=9.5)
ax.set_ylim(-5, 115)
ax.legend(fontsize=8, loc='lower left')
ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/catastrophic_forgetting.png', dpi=300)
plt.close()

print('All diagrams for AI Modul 1.4 generated successfully!')
