import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
ax.set_xlim(0, 14)
ax.set_ylim(0, 8.5)
ax.axis('off')

# 7 Dimensions of AI Ethics with real-world case studies
dimensions = [
    {
        "x": 0.5, "y": 5.8, "w": 3.9, "h": 2.2, "color": "#1f77b4",
        "title": "1. Keadilan (Fairness)",
        "case": "Kasus Nyata: Amazon Recruitment AI\n& COMPAS Recidivism Tool.\nDiskriminasi gender & rasial akibat\ndata historis yang timpang.",
        "icon": "⚖️"
    },
    {
        "x": 4.9, "y": 5.8, "w": 3.9, "h": 2.2, "color": "#ff7f0e",
        "title": "2. Transparansi & XAI",
        "case": "Kasus Nyata: Skandal Robodebt Australia\n(Denda AUD $1.8 Miliar).\nAlgoritma otomatis menagih bansos tanpa\npenjelasan (Black-Box Dilemma).",
        "icon": "🔍"
    },
    {
        "x": 9.3, "y": 5.8, "w": 4.2, "h": 2.2, "color": "#2ca02c",
        "title": "3. Privasi & UU PDP",
        "case": "Kasus Nyata: Clearview AI 30 Miliar Wajah\nScraping media sosial tanpa izin.\nPelanggaran hak biometrik & hak menolak\nkeputusan otomatis (Pasal 40 UU PDP).",
        "icon": "🛡️"
    },
    {
        "x": 0.5, "y": 3.1, "w": 3.9, "h": 2.2, "color": "#d62728",
        "title": "4. Akuntabilitas & Liabilitas",
        "case": "Kasus Nyata: Mobil Otonom Uber Fatal\nKecelakaan fatal pejalan kaki di Tempe.\nSiapa bertanggung jawab? Operator,\nmanajer software, atau produsen AI?",
        "icon": "🏛️"
    },
    {
        "x": 4.9, "y": 3.1, "w": 3.9, "h": 2.2, "color": "#9467bd",
        "title": "5. Keselamatan & Dual-Use",
        "case": "Kasus Nyata: MegaSyn Biochemical AI\nAI penemu obat dibalik menjadi perancang\n40.000 senjata kimia dalam 6 jam.\nAncaman Deepfake & Voice Phishing.",
        "icon": "☣️"
    },
    {
        "x": 9.3, "y": 3.1, "w": 4.2, "h": 2.2, "color": "#8c564b",
        "title": "6. Green AI & Lingkungan",
        "case": "Kasus Nyata: Emisi Data Center LLM\nPelatihan model masif menghasilkan ratusan\nton CO2 & jutaan liter air pendingin.\nUrgensi komputasi hemat energi (Edge AI).",
        "icon": "🌱"
    },
    {
        "x": 2.7, "y": 0.4, "w": 8.5, "h": 2.2, "color": "#e377c2",
        "title": "7. Hak Cipta, Integritas Intelektual & Etika Ketenagakerjaan",
        "case": "Kasus Nyata: Tuntutan Seniman/Getty Images vs Model Generatif AI + Eksploitasi 'Ghost Workers' Anotator Data.\nKewajiban sitasi, pencegahan plagiarisme halusinasi, dan perlindungan upah layak bagi pelabel data manusia.",
        "icon": "📜"
    }
]

for d in dimensions:
    rect = patches.FancyBboxPatch((d["x"], d["y"]), d["w"], d["h"], boxstyle="round,pad=0.2",
                                  facecolor=d["color"], alpha=0.15, edgecolor=d["color"], linewidth=2)
    ax.add_patch(rect)
    
    # Title
    ax.text(d["x"] + 0.3, d["y"] + d["h"] - 0.4, f"{d['title']}", 
            fontsize=10.5, fontweight='bold', color=d["color"])
    
    # Case study text
    ax.text(d["x"] + 0.3, d["y"] + d["h"]/2 - 0.25, d["case"], 
            fontsize=8.5, color='#222222', linespacing=1.35)

plt.suptitle("Taksonomi 7 Dimensi Etika Penggunaan AI & Ragam Studi Kasus Nyata Dunia", 
             fontsize=13, fontweight='bold', y=0.98)

plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\dimensi_etika_ai_dan_kasus.png", dpi=300, bbox_inches='tight')
plt.close()
print("Ethics dimensions and case studies plot generated successfully.")
