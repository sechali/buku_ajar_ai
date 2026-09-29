import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Background boxes
env_box = patches.FancyBboxPatch((0.5, 0.5), 9.0, 1.4, boxstyle='round,pad=0.2', facecolor='#EBF5FB', edgecolor='#2980B9', linewidth=2)
agent_box = patches.FancyBboxPatch((1.2, 2.7), 7.6, 2.8, boxstyle='round,pad=0.3', facecolor='#EAFAF1', edgecolor='#27AE60', linewidth=2)

ax.add_patch(env_box)
ax.add_patch(agent_box)

# Labels for main containers
ax.text(5.0, 1.2, 'ENVIRONMENT (LINGKUNGAN LUAR)\nObjek fisik, citra daun, suhu kebun, ruang tertutup, kamera CCTV', 
        ha='center', va='center', fontsize=11, fontweight='bold', color='#1B4F72')
ax.text(5.0, 5.15, 'INTELLIGENT AGENT (AGEN CERDAS)', 
        ha='center', va='center', fontsize=12, fontweight='bold', color='#1E8449')

# Internal Agent components
sensor_box = patches.FancyBboxPatch((1.6, 3.2), 2.0, 1.3, boxstyle='round,pad=0.1', facecolor='#FCF3CF', edgecolor='#F39C12', linewidth=1.5)
brain_box = patches.FancyBboxPatch((4.0, 3.2), 2.0, 1.3, boxstyle='round,pad=0.1', facecolor='#FADBD8', edgecolor='#C0392B', linewidth=1.5)
actuator_box = patches.FancyBboxPatch((6.4, 3.2), 2.0, 1.3, boxstyle='round,pad=0.1', facecolor='#E8DAEF', edgecolor='#8E44AD', linewidth=1.5)

ax.add_patch(sensor_box)
ax.add_patch(brain_box)
ax.add_patch(actuator_box)

ax.text(2.6, 3.85, 'SENSORS\n(Kamera, IoT,\nSensor Suhu/pH)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#7D6608')
ax.text(5.0, 3.85, 'PROGRAM AGENT\n(Arsitektur AI &\nFungsi Keputusan)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#78281F')
ax.text(7.4, 3.85, 'ACTUATORS\n(Sprinkler, Display,\nAlarm, Solenoid)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#512E5F')

# Arrows
# 1. Environment to Sensor (Percepts)
ax.annotate('', xy=(2.6, 3.1), xytext=(2.6, 1.95),
            arrowprops=dict(facecolor='#2980B9', edgecolor='#2980B9', width=2.5, headwidth=8))
ax.text(2.2, 2.45, 'Persepsi (Percept)\nData Sensor p(t)', ha='right', va='center', fontsize=9.5, fontweight='bold', color='#2980B9')

# 2. Sensor to Brain
ax.annotate('', xy=(3.9, 3.85), xytext=(3.7, 3.85),
            arrowprops=dict(facecolor='#333333', edgecolor='#333333', width=1.5, headwidth=6))

# 3. Brain to Actuator
ax.annotate('', xy=(6.3, 3.85), xytext=(6.1, 3.85),
            arrowprops=dict(facecolor='#333333', edgecolor='#333333', width=1.5, headwidth=6))

# 4. Actuator to Environment (Action)
ax.annotate('', xy=(7.4, 1.95), xytext=(7.4, 3.1),
            arrowprops=dict(facecolor='#C0392B', edgecolor='#C0392B', width=2.5, headwidth=8))
ax.text(7.8, 2.45, 'Tindakan (Action)\nEksekusi Fisik a(t)', ha='left', va='center', fontsize=9.5, fontweight='bold', color='#C0392B')

plt.title('Siklus Persepsi-Aksi Agen Cerdas (Intelligent Agent Cycle)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/flowchart_agen_ai.png', dpi=300)
print('Flowchart image successfully created!')
