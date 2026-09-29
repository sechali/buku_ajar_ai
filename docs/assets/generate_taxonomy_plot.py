import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

sectors = [
    "1. Pertanian Presisi\n(Smart Agriculture)",
    "2. Keamanan & Pengawasan\n(Smart Surveillance)",
    "3. Kesehatan & Medis\n(Healthcare & Genomics)",
    "4. Manufaktur Industri\n(Industry 4.0 / PKS)",
    "5. Finansial & Perbankan\n(Fintech & Fraud)",
    "6. Pendidikan & Layanan\n(EdTech & Public)"
]

paradigms = [
    "Computer Vision\n(Citra & Video)",
    "Tabular & Sensor ML\n(IoT & Time-Series)",
    "Natural Language\nProcessing (NLP)",
    "Reinforcement\nLearning & Control"
]

# Matrix values: 0 = Low, 1 = Medium, 2 = Core/High
# Shape: (sectors, paradigms)
matrix = np.array([
    [2, 2, 0, 1], # Pertanian: CV drone, Sensor cuaca tanah, NLP low, RL traktor/irigasi
    [2, 1, 1, 1], # Keamanan: CV kamera, Sensor radar/perimeter, NLP transkrip radio, RL navigasi drone
    [2, 2, 2, 1], # Medis: Radiologi CV, Sensor biomarker EHR, NLP klinis, RL drug synthesis
    [2, 2, 0, 2], # Manufaktur: AOI inspeksi, Sensor getaran turbin, NLP low, RL robotika industri
    [1, 2, 2, 1], # Finansial: OCR dokumen, Tabular transaksi fraud, NLP analisa berita, RL robo-trading
    [1, 1, 2, 1]  # Pendidikan: Proctoring visual, Analisis nilai siswa, NLP Chatbot tutor, RL kurikulum adaptif
])

# Plot heatmap
cax = ax.matshow(matrix, cmap='YlGnBu', vmin=0, vmax=2)

# Formatting ticks
ax.set_xticks(range(len(paradigms)))
ax.set_yticks(range(len(sectors)))
ax.set_xticklabels(paradigms, fontsize=10, fontweight='bold')
ax.set_yticklabels(sectors, fontsize=10, fontweight='bold')

# Loop over data dimensions and create text annotations.
labels = {0: "Pendukung\n(Rendah)", 1: "Signifikan\n(Menengah)", 2: "Pilar Utama\n(Sangat Tinggi)"}
text_colors = {0: "#555555", 1: "#003366", 2: "#ffffff"}

for i in range(len(sectors)):
    for j in range(len(paradigms)):
        val = matrix[i, j]
        ax.text(j, i, labels[val], ha="center", va="center", 
                color=text_colors[val], fontsize=9, fontweight='bold')

# Styling
plt.title("Matriks Taksonomi Penerapan AI Berdasarkan Sektor Industri & Modalitas AI", 
          fontsize=13, fontweight='bold', pad=25)
ax.grid(False)

# Add legend box below
cbar = fig.colorbar(cax, ticks=[0, 1, 2], orientation='horizontal', pad=0.12, shrink=0.6)
cbar.ax.set_xticklabels(['Penggunaan Pendukung (0)', 'Penggunaan Signifikan (1)', 'Pilar Teknologi Utama (2)'])
cbar.ax.tick_params(labelsize=9)

plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\taksonomi_penerapan_ai.png", dpi=300)
plt.close()
print("Taxonomy matrix generated successfully.")
