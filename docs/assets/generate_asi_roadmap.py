import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

# Backbone stairs / ramp
ax.plot([1.0, 3.2, 5.5, 7.8, 10.5], [1.2, 2.2, 3.5, 4.8, 6.2], color='#7F8C8D', linestyle='--', lw=2, zorder=1)

# Stage boxes
stages = [
    (1.0, 1.2, "TAHAP 1: CONVERSATIONAL & REASONING AI\n(Status: Realita 2024-2026)\n• LLM Multimodal & Model Penalaran (CoT)\n• Test-Time Compute (Thinking Models)\n• Asisten Coding & Tool Calling", '#EBF5FB', '#2980B9', '#1B4F72'),
    (3.2, 2.2, "TAHAP 2: AUTONOMOUS AGENTS & EMBODIED AI\n(Status: Transisi Menuju AGI)\n• Agen Otonom Multi-Langkah (Agentic Workflow)\n• Integrasi Robotik Fisik (Humanoid / VLA)\n• Perencanaan Jangka Panjang Mandiri", '#D5F5E3', '#27AE60', '#1E8449'),
    (5.5, 3.5, "TAHAP 3: ARTIFICIAL GENERAL INTELLIGENCE (AGI)\n(Status: Ambang Batas Manusia)\n• Setara Kognisi Manusia Dewasa Semua Bidang\n• Penalaran Kausal, Akal Sehat (Common Sense)\n• Transfer Learning Lintas Disiplin Tanpa Lupa", '#FCF3CF', '#F39C12', '#7D6608'),
    (7.8, 4.8, "TAHAP 4: RECURSIVE SELF-IMPROVEMENT (RSI)\n(Status: Mesin Ledakan Inteligensi)\n• AI Meriset & Memprogram AI Lebih Cerdas\n• Otomatisasi Riset Sains (Autonomous Science)\n• Sintesis Teori Baru Tanpa Bimbingan Manusia", '#FADBD8', '#C0392B', '#922B21'),
    (10.5, 6.2, "TAHAP 5: ARTIFICIAL SUPERINTELLIGENCE (ASI)\n(Status: Titik Singularitas Peradaban)\n• Melampaui Totalitas Genius Manusia\n• Eksponensial Tak Terkendali (Super-Kreatif)\n• Tantangan Eksistensial: Superalignment", '#E8DAEF', '#8E44AD', '#512E5F')
]

for x, y, text, fcolor, ecolor, tcolor in stages:
    box = patches.FancyBboxPatch((x - 1.0, y - 0.7), 2.2, 1.4, boxstyle='round,pad=0.15', facecolor=fcolor, edgecolor=ecolor, lw=2, zorder=2)
    ax.add_patch(box)
    ax.text(x + 0.1, y, text, ha='center', va='center', fontsize=6.8, fontweight='bold', color=tcolor, zorder=3)
    # Circle node
    circle = patches.Circle((x, y - 0.7), 0.15, facecolor=ecolor, edgecolor='white', lw=1.5, zorder=4)
    ax.add_patch(circle)

# Milestone labels
ax.text(1.1, 0.2, 'Narrow AI Canggih', ha='center', fontsize=8, fontweight='bold', color='#1B4F72')
ax.text(3.3, 1.1, 'Broad Agentic AI', ha='center', fontsize=8, fontweight='bold', color='#1E8449')
ax.text(5.6, 2.4, 'Level Manusia (AGI)', ha='center', fontsize=8, fontweight='bold', color='#7D6608')
ax.text(7.9, 3.7, 'Intelligence Explosion', ha='center', fontsize=8, fontweight='bold', color='#922B21')
ax.text(10.6, 5.0, 'Singularitas (ASI)', ha='center', fontsize=8, fontweight='bold', color='#512E5F')

plt.title('Lintasan Peta Jalan (Roadmap) Evolusi Kecerdasan Buatan: Dari AI Saat Ini Menuju ASI', fontsize=12, fontweight='bold', pad=15, color='#2C3E50')
plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/roadmap_menuju_asi.png', dpi=300)
plt.close()
print('Roadmap diagram generated successfully!')
