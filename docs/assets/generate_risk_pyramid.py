import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Pyramid layers: (bottom, height, x_left_bottom, x_right_bottom, x_left_top, x_right_top)
# We can draw 4 trapezoids / triangles from bottom to top
layers = [
    {
        "y0": 0.5, "y1": 2.2, "x0_l": 0.5, "x0_r": 9.5, "x1_l": 1.7, "x1_r": 8.3,
        "title": "1. RISIKO MINIMAL / TAK BERBAHAYA (Minimal Risk)",
        "desc": "Filter spam, video game AI, optimasi inventaris gudang kebun.\nKewajiban: Kode etik sukarela, bebas beroperasi tanpa regulasi ketat.",
        "color": "#2ca02c", "text_color": "#ffffff"
    },
    {
        "y0": 2.3, "y1": 4.0, "x0_l": 1.75, "x0_r": 8.25, "x1_l": 2.9, "x1_r": 7.1,
        "title": "2. RISIKO TERBATAS (Limited Risk / Transparency)",
        "desc": "Chatbot layanan pelanggan, deepfake, generator konten sintetis.\nKewajiban: Transparansi wajib (pengguna harus tahu sedang bicara dengan AI).",
        "color": "#ffbb78", "text_color": "#333333"
    },
    {
        "y0": 4.1, "y1": 5.8, "x0_l": 2.95, "x0_r": 7.05, "x1_l": 4.0, "x1_r": 6.0,
        "title": "3. RISIKO TINGGI (High Risk)",
        "desc": "Skoring kredit perbankan, rekruitmen SDM, radiologi medis,\npengawasan biometrik publik. Wajib audit bias & kepatuhan UU PDP!",
        "color": "#ff7f0e", "text_color": "#ffffff"
    },
    {
        "y0": 5.9, "y1": 7.5, "x0_l": 4.05, "x0_r": 5.95, "x1_l": 5.0, "x1_r": 5.0,
        "title": "4. RISIKO TAK DAPAT DITERIMA\n(Unacceptable Risk - DILARANG!)",
        "desc": "Social scoring warga negara, manipulasi perilaku subliminal,\neksploitasi kerentanan anak/disabilitas. DILARANG TOTAL SECARA HUKUM.",
        "color": "#d62728", "text_color": "#ffffff"
    }
]

for l in layers:
    poly = patches.Polygon([
        [l["x0_l"], l["y0"]],
        [l["x0_r"], l["y0"]],
        [l["x1_r"], l["y1"]],
        [l["x1_l"], l["y1"]]
    ], closed=True, facecolor=l["color"], edgecolor='black', linewidth=1.5, alpha=0.9)
    ax.add_patch(poly)
    
    # Text in center
    mid_y = (l["y0"] + l["y1"]) / 2
    if "DILARANG" in l["title"]:
        ax.text(5.0, mid_y + 0.35, l["title"], ha='center', va='center', fontsize=9.5, fontweight='bold', color=l["text_color"])
        ax.text(5.0, mid_y - 0.35, l["desc"], ha='center', va='center', fontsize=7.5, color=l["text_color"], multialignment='center')
    else:
        ax.text(5.0, mid_y + 0.35, l["title"], ha='center', va='center', fontsize=9.5, fontweight='bold', color=l["text_color"])
        ax.text(5.0, mid_y - 0.35, l["desc"], ha='center', va='center', fontsize=8, color=l["text_color"], multialignment='center')

plt.title("Piramida Klasifikasi Risiko Regulasi AI (EU AI Act & Penyelarasan UU PDP Indonesia)", 
          fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\piramida_risiko_ai_act.png", dpi=300, bbox_inches='tight')
plt.close()
print("AI Risk Pyramid diagram generated successfully.")
