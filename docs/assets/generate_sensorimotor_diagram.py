import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), dpi=300)

for ax in [ax1, ax2]:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

# --- Panel 1: Sistem Biologis Manusia ---
ax1.set_title('(A) Sistem Sensorik-Motorik Manusia (Biologis)', fontsize=11, fontweight='bold', pad=10, color='#1A5276')

b_stimulus = patches.FancyBboxPatch((0.4, 1.2), 1.8, 2.0, boxstyle='round,pad=0.1', facecolor='#EAECEE', edgecolor='#7F8C8D', lw=1.5)
b_sensor = patches.FancyBboxPatch((2.7, 1.2), 2.0, 2.0, boxstyle='round,pad=0.1', facecolor='#FCF3CF', edgecolor='#F39C12', lw=1.5)
b_brain = patches.FancyBboxPatch((5.2, 1.2), 2.0, 2.0, boxstyle='round,pad=0.1', facecolor='#FADBD8', edgecolor='#C0392B', lw=1.5)
b_motor = patches.FancyBboxPatch((7.7, 1.2), 1.9, 2.0, boxstyle='round,pad=0.1', facecolor='#D5F5E3', edgecolor='#27AE60', lw=1.5)

for b in [b_stimulus, b_sensor, b_brain, b_motor]: ax1.add_patch(b)

ax1.text(1.3, 2.2, 'STIMULUS\nLINGKUNGAN\n(Cahaya, Suara,\nSuhu, Tekanan)', ha='center', va='center', fontweight='bold', fontsize=8.5)
ax1.text(3.7, 2.2, 'RESEPTOR\nSENSORIK\n(Mata, Telinga,\nKulit, Hidung)', ha='center', va='center', fontweight='bold', fontsize=8.5)
ax1.text(6.2, 2.2, 'SUSUNAN SARAF\nPUSAT (OTAK)\n(Kognisi, Memori,\nPengambilan Keputusan)', ha='center', va='center', fontweight='bold', fontsize=8.5)
ax1.text(8.65, 2.2, 'EFEKTOR\nMOTORIK\n(Otot Rangka,\nKelenjar Tubuh)', ha='center', va='center', fontweight='bold', fontsize=8.5)

ax1.annotate('', xy=(2.6, 2.2), xytext=(2.3, 2.2), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax1.annotate('', xy=(5.1, 2.2), xytext=(4.8, 2.2), arrowprops=dict(facecolor='#D35400', width=1.5, headwidth=6))
ax1.text(4.95, 2.5, 'Saraf Aferen\n(Sensorik)', ha='center', fontsize=7.5, color='#D35400', fontweight='bold')
ax1.annotate('', xy=(7.6, 2.2), xytext=(7.3, 2.2), arrowprops=dict(facecolor='#27AE60', width=1.5, headwidth=6))
ax1.text(7.45, 2.5, 'Saraf Eferen\n(Motorik)', ha='center', fontsize=7.5, color='#27AE60', fontweight='bold')


# --- Panel 2: Arsitektur Artificial Intelligence ---
ax2.set_title('(B) Arsitektur Sistem Artificial Intelligence (Komputasional)', fontsize=11, fontweight='bold', pad=10, color='#196F3D')

b_env = patches.FancyBboxPatch((0.4, 1.2), 1.8, 2.0, boxstyle='round,pad=0.1', facecolor='#EBF5FB', edgecolor='#2980B9', lw=1.5)
b_aisensor = patches.FancyBboxPatch((2.7, 1.2), 2.0, 2.0, boxstyle='round,pad=0.1', facecolor='#FCF3CF', edgecolor='#F39C12', lw=1.5)
b_aicpu = patches.FancyBboxPatch((5.2, 1.2), 2.0, 2.0, boxstyle='round,pad=0.1', facecolor='#FADBD8', edgecolor='#C0392B', lw=1.5)
b_aiactuator = patches.FancyBboxPatch((7.7, 1.9), 1.9, 2.0, boxstyle='round,pad=0.1', facecolor='#E8DAEF', edgecolor='#8E44AD', lw=1.5)

for b in [b_env, b_aisensor, b_aicpu, b_aiactuator]: ax2.add_patch(b)

ax2.text(1.3, 2.2, 'ENVIRONMENT\n(Lingkungan Fisik,\nCitra Daun, CCTV,\nDatabase)', ha='center', va='center', fontweight='bold', fontsize=8.5)
ax2.text(3.7, 2.2, 'SENSORS\n(Kamera Optik,\nSensor IoT, LiDAR,\nMicrophone)', ha='center', va='center', fontweight='bold', fontsize=8.5)
ax2.text(6.2, 2.2, 'MODEL AI / INFERENSI\n(Neural Net, SVM,\nLLM, Logika Agen\nf: P* -> A)', ha='center', va='center', fontweight='bold', fontsize=8.5)
ax2.text(8.65, 2.9, 'ACTUATORS\n(Relay, Motor Servo,\nNozel Sprinkler,\nDisplay / API)', ha='center', va='center', fontweight='bold', fontsize=8.5)

ax2.annotate('', xy=(2.6, 2.2), xytext=(2.3, 2.2), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax2.annotate('', xy=(5.1, 2.2), xytext=(4.8, 2.2), arrowprops=dict(facecolor='#D35400', width=1.5, headwidth=6))
ax2.text(4.95, 2.5, 'Sinyal Digital\n(Percept)', ha='center', fontsize=7.5, color='#D35400', fontweight='bold')
ax2.annotate('', xy=(7.6, 2.2), xytext=(7.3, 2.2), arrowprops=dict(facecolor='#8E44AD', width=1.5, headwidth=6))
ax2.text(7.45, 2.5, 'Perintah Aksi\n(Control Signal)', ha='center', fontsize=7.5, color='#8E44AD', fontweight='bold')

# Feedback loop arrow from actuator back to environment
ax2.annotate('', xy=(1.3, 1.1), xytext=(8.65, 1.8),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.25", color='#2980B9', lw=2))
ax2.text(5.0, 0.4, 'Umpan Balik Perubahan Lingkungan (Closed-Loop Feedback)', ha='center', fontsize=8.5, color='#2980B9', fontweight='bold')

plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/analogi_sensorik_motorik.png', dpi=300)
print('Sensorimotor analogy diagram generated successfully!')
