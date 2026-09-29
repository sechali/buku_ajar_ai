import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

# 1. DATA DRIFT (Perubahan Distribusi Fitur P(X))
np.random.seed(42)
x_baseline = np.random.normal(loc=28.0, scale=3.0, size=1000)  # Suhu rata-rata musim normal
x_drift = np.random.normal(loc=35.0, scale=4.0, size=1000)     # Suhu akibat fenomena El Nino ekstrem

ax1.hist(x_baseline, bins=30, alpha=0.6, color='#1f77b4', density=True, label='Data Latih Baseline P(X)\n(Musim Normal: 28°C)')
ax1.hist(x_drift, bins=30, alpha=0.6, color='#d62728', density=True, label='Data Produksi Terkini P(X)\n(El Nino: 35°C - Data Drift!)')
ax1.set_title("A. Data Drift (Covariate Shift)\nDistribusi Input P(X) Bergeser Signifikan", fontsize=11, fontweight='bold')
ax1.set_xlabel("Suhu Permukaan (°C)", fontsize=10, fontweight='bold')
ax1.set_ylabel("Densitas Probabilitas", fontsize=10, fontweight='bold')
ax1.legend(loc='upper right', fontsize=9)
ax1.axvline(28.0, color='#1f77b4', linestyle='--', linewidth=1.5)
ax1.axvline(35.0, color='#d62728', linestyle='--', linewidth=1.5)

# 2. CONCEPT DRIFT (Perubahan Relasi P(Y|X))
x_line = np.linspace(20, 45, 100)
# Hubungan lama: Kenaikan suhu meningkatkan evapotranspirasi secara linier
y_concept_old = 2.5 * x_line - 30
# Hubungan baru: Terjadi saturasi kekeringan stomata daun menutup (hubungan non-linear baru)
y_concept_new = 40 * np.sin((x_line - 20) / 10) + 20

ax2.plot(x_line, y_concept_old, color='#2ca02c', linewidth=2.5, label='Relasi Asli P(Y|X)\n(Model Pelatihan)')
ax2.plot(x_line, y_concept_new, color='#9467bd', linewidth=2.5, linestyle='-.', label='Relasi Baru Nyata P(Y|X)\n(Dinamika Iklim Baru - Concept Drift!)')
ax2.set_title("B. Concept Drift\nRelasi Pemetaan P(Y|X) Mengalami Perubahan Fundamental", fontsize=11, fontweight='bold')
ax2.set_xlabel("Suhu Permukaan (°C)", fontsize=10, fontweight='bold')
ax2.set_ylabel("Tingkat Stres Air Tanaman (Skor Y)", fontsize=10, fontweight='bold')
ax2.legend(loc='lower right', fontsize=9)

plt.suptitle("Dinamika Degradasi Model di Lingkungan Produksi: Data Drift vs Concept Drift", fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\data_drift_vs_concept_drift.png", dpi=300, bbox_inches='tight')
plt.close()
print("Data Drift vs Concept Drift diagram generated successfully.")
