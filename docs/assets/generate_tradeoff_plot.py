import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

# Sektor & Karakteristik
applications = [
    {"name": "Autonomous Drone Kebun (Edge AI)", "latency": 15, "accuracy": 94, "color": "#2ca02c", "category": "Pertanian Presisi"},
    {"name": "Smart CCTV Intrusion (Real-Time)", "latency": 25, "accuracy": 92, "color": "#d62728", "category": "Keamanan & Pengawasan"},
    {"name": "Fraud Detection Perbankan", "latency": 50, "accuracy": 98.5, "color": "#1f77b4", "category": "Finansial"},
    {"name": "Predictive Maintenance Turbin PKS", "latency": 200, "accuracy": 95, "color": "#ff7f0e", "category": "Manufaktur Industri"},
    {"name": "Radiologi Medis (CT/X-Ray)", "latency": 5000, "accuracy": 99.2, "color": "#9467bd", "category": "Kesehatan & Medis"},
    {"name": "Estimasi Hasil Panen Tahunan (Satellite)", "latency": 60000, "accuracy": 89, "color": "#8c564b", "category": "Pertanian Makro"},
    {"name": "LLM Asisten Riset & Admin", "latency": 800, "accuracy": 91, "color": "#e377c2", "category": "Layanan & Pendidikan"}
]

for app in applications:
    ax.scatter(app["latency"], app["accuracy"], color=app["color"], s=280, alpha=0.85, edgecolors='black', linewidth=1.5, zorder=5)
    
    # Text positioning adjustment
    offset_x = 1.15
    offset_y = 0.3
    if "Medis" in app["name"]:
        offset_y = -0.5
    elif "Drone" in app["name"]:
        offset_y = 0.4
    elif "CCTV" in app["name"]:
        offset_y = -0.6
    elif "Satellite" in app["name"]:
        offset_y = 0.4
        
    ax.annotate(f" {app['name']}\n (Acc: {app['accuracy']}%, Lat: {app['latency']}ms)", 
                (app["latency"], app["accuracy"]),
                xytext=(app["latency"] * offset_x, app["accuracy"] + offset_y),
                fontsize=9.5, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc=app["color"], alpha=0.15, ec=app["color"], lw=1),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.1", color=app["color"], lw=1.2),
                zorder=6)

# Logarithmic scale for latency due to huge span (15ms to 60000ms)
ax.set_xscale('log')
ax.set_xlim(5, 200000)
ax.set_ylim(85, 101)

# Annotate regions
ax.axvspan(5, 100, color='green', alpha=0.06, zorder=1)
ax.text(12, 86, "Zona Real-Time Kritis / Edge AI\n(Latensi < 100 ms)", fontsize=10, color='darkgreen', fontweight='bold', fontstyle='italic')

ax.axvspan(100, 2000, color='orange', alpha=0.05, zorder=1)
ax.text(180, 86, "Zona Interaktif Online\n(100 ms - 2 detik)", fontsize=10, color='darkgoldenrod', fontweight='bold', fontstyle='italic')

ax.axvspan(2000, 200000, color='purple', alpha=0.05, zorder=1)
ax.text(8000, 86, "Zona Analisis Offline / Batch Kritis\n(Akurasi Ekstrem & Model Masif)", fontsize=10, color='purple', fontweight='bold', fontstyle='italic')

ax.set_title("Trade-off Kebutuhan Akurasi vs Latensi Inferensi di Berbagai Bidang AI", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Latensi Inferensi Maksimum yang Ditoleransi (milidetik, Skala Logaritmik)", fontsize=11, fontweight='bold')
ax.set_ylabel("Tingkat Akurasi Minimum yang Diharapkan (%)", fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\tradeoff_akurasi_latensi_sektor.png", dpi=300)
plt.close()
print("Trade-off plot generated successfully.")
