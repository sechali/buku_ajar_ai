"""Script to generate high-resolution (300 DPI) diagrams for AI Modul 3.6
Fungsi dan Modularisasi:
1. arsitektur_ruang_lingkup_legb_python.png
2. anatomi_fungsi_dan_dekorator_sawit.png
"""

import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directories exist
os.makedirs("docs/assets", exist_ok=True)
artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"

def generate_diagram_legb():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "ARSITEKTUR RESOLUSI RUANG LINGKUP LEGB PYTHON", 
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Urutan Pencarian Variabel: Local -> Enclosing -> Global -> Built-in (CPython Symbol Resolution)", 
            ha="center", va="center", fontsize=9, style="italic", color="#4a5568")

    # Nested rounded boxes for LEGB
    # 1. Built-in (Outer)
    rect_b = patches.FancyBboxPatch((5, 8), 90, 80, boxstyle="round,pad=1.5", 
                                    facecolor="#eef2ff", edgecolor="#4338ca", linewidth=2.5)
    ax.add_patch(rect_b)
    ax.text(10, 84, "B: BUILT-IN SCOPE", fontsize=11, fontweight="bold", color="#312e81")
    ax.text(10, 80, "Fungsi & konstanta bawaan Python: len(), range(), print(), ValueError, __name__", 
            fontsize=8, color="#4338ca")

    # 2. Global (Module Level)
    rect_g = patches.FancyBboxPatch((12, 14), 76, 62, boxstyle="round,pad=1.5", 
                                    facecolor="#f0fdf4", edgecolor="#15803d", linewidth=2.2)
    ax.add_patch(rect_g)
    ax.text(17, 72, "G: GLOBAL SCOPE (Module Level)", fontsize=10.5, fontweight="bold", color="#14532d")
    ax.text(17, 68, "Konstanta modul, fungsi tingkat atas, deklarasi 'global X': AMBANG_FFA = 3.0", 
            fontsize=8, color="#166534")

    # 3. Enclosing (Closure / Nested Function)
    rect_e = patches.FancyBboxPatch((20, 20), 60, 44, boxstyle="round,pad=1.5", 
                                    facecolor="#fffbeb", edgecolor="#b45309", linewidth=2.0)
    ax.add_patch(rect_e)
    ax.text(25, 60, "E: ENCLOSING SCOPE (Fungsi Pembungkus)", fontsize=10, fontweight="bold", color="#78350f")
    ax.text(25, 56, "Ruang lingkup fungsi luar pada closure / dekorator: 'nonlocal faktor_skala'", 
            fontsize=7.5, color="#92400e")

    # 4. Local (Innermost)
    rect_l = patches.FancyBboxPatch((28, 26), 44, 26, boxstyle="round,pad=1.5", 
                                    facecolor="#fef2f2", edgecolor="#b91c1c", linewidth=2.0)
    ax.add_patch(rect_l)
    ax.text(50, 46, "L: LOCAL SCOPE", ha="center", fontsize=10.5, fontweight="bold", color="#7f1d1d")
    ax.text(50, 41, "Variabel lokal & parameter fungsi:", ha="center", fontsize=8, color="#991b1b")
    ax.text(50, 36, "def hitung_ndvi(nir, red):\n    ndvi = (nir - red) / (nir + red)\n    return ndvi", 
            ha="center", fontsize=7.5, fontfamily="monospace", color="#450a0a",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fee2e2", edgecolor="#ef4444", lw=1))

    # Search flow arrows
    ax.annotate("Prioritas 1\n(Paling Awal)", xy=(28, 39), xytext=(15, 39),
                arrowprops=dict(facecolor="#b91c1c", edgecolor="#7f1d1d", width=1.5, headwidth=6),
                fontsize=8, fontweight="bold", color="#7f1d1d", ha="center", va="center")

    ax.annotate("Prioritas 2\n(Closure)", xy=(20, 52), xytext=(8, 52),
                arrowprops=dict(facecolor="#b45309", edgecolor="#78350f", width=1.5, headwidth=6),
                fontsize=8, fontweight="bold", color="#78350f", ha="center", va="center")

    ax.annotate("Prioritas 3\n(Modul)", xy=(88, 55), xytext=(78, 67),
                arrowprops=dict(facecolor="#15803d", edgecolor="#14532d", width=1.5, headwidth=6),
                fontsize=8, fontweight="bold", color="#14532d", ha="center", va="center")

    ax.annotate("Prioritas 4\n(Fallback Terakhir)", xy=(95, 78), xytext=(82, 83),
                arrowprops=dict(facecolor="#4338ca", edgecolor="#312e81", width=1.5, headwidth=6),
                fontsize=8, fontweight="bold", color="#312e81", ha="center", va="center")

    # Bottom notes
    ax.text(50, 3, "Catatan: Kata kunci 'global' memaksa binding ke Global Scope; kata kunci 'nonlocal' mengikat variabel ke Enclosing terdekat.", 
            ha="center", fontsize=7.5, fontweight="bold", color="#374151")

    plt.tight_layout()
    target_path = "docs/assets/arsitektur_ruang_lingkup_legb_python.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")

    # Copy to artifact dir
    shutil.copy(target_path, os.path.join(artifact_dir, "arsitektur_ruang_lingkup_legb_python.png"))


def generate_diagram_decorator():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "ANATOMI DEKORATOR DAN WRAPPER PIPELINE TELEMETRI SAWIT", 
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Pola Higher-Order Functions: Menginjeksikan Audit Eksekusi & Validasi Tanpa Mengubah Fungsi Inti", 
            ha="center", va="center", fontsize=9, style="italic", color="#4a5568")

    # Outer Box: Dekorator Wrapper (@audit_telemetri)
    rect_outer = patches.FancyBboxPatch((8, 14), 84, 74, boxstyle="round,pad=1.5", 
                                        facecolor="#f8fafc", edgecolor="#334155", linewidth=2.2, linestyle="--")
    ax.add_patch(rect_outer)
    ax.text(12, 84, "DEKORATOR: @audit_telemetri (Fungsi Tingkat Tinggi / Higher-Order Function)", 
            fontsize=10.5, fontweight="bold", color="#1e293b")

    # Pre-execution Hook Box
    rect_pre = patches.FancyBboxPatch((12, 54), 34, 25, boxstyle="round,pad=1.0", 
                                      facecolor="#ecfdf5", edgecolor="#059669", linewidth=1.8)
    ax.add_patch(rect_pre)
    ax.text(29, 74, "1. PRA-EKSEKUSI (Pre-Hook)", ha="center", fontsize=9.5, fontweight="bold", color="#065f46")
    ax.text(29, 68, "• Mulai timer presisi (time.perf_counter())\n• Validasi rentang sinyal *args & **kwargs\n• Log identitas sensor & payload masuk", 
            ha="center", fontsize=7.5, color="#047857")

    # Core Function Box (Inner)
    rect_core = patches.FancyBboxPatch((54, 38), 34, 41, boxstyle="round,pad=1.2", 
                                       facecolor="#eff6ff", edgecolor="#2563eb", linewidth=2.2)
    ax.add_patch(rect_core)
    ax.text(71, 74, "2. FUNGSI TARGET (Core Logic)", ha="center", fontsize=10, fontweight="bold", color="#1e40af")
    ax.text(71, 67, "def hitung_indeks_kanopi(nir, red, /):\n    \"\"\"Menghitung NDVI murni\"\"\"\n    return (nir - red) / (nir + red)", 
            ha="center", fontsize=7.5, fontfamily="monospace", color="#1e3a8a",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#dbeafe", edgecolor="#3b82f6", lw=1))
    ax.text(71, 46, "Eksekusi logika domain inti murni:\nTanpa polusi kode logging atau stopwatch!", 
            ha="center", fontsize=7.5, style="italic", color="#1d4ed8")

    # Post-execution Hook Box
    rect_post = patches.FancyBboxPatch((12, 20), 34, 28, boxstyle="round,pad=1.0", 
                                       facecolor="#fef3c7", edgecolor="#d97706", linewidth=1.8)
    ax.add_patch(rect_post)
    ax.text(29, 43, "3. PASCA-EKSEKUSI (Post-Hook)", ha="center", fontsize=9.5, fontweight="bold", color="#92400e")
    ax.text(29, 36, "• Hitung durasi latensi: t_akhir - t_awal\n• Filter nilai output / penanganan anomali\n• Rekam metrik ke database audit PKS\n• Kembalikan hasil asli (return result)", 
            ha="center", fontsize=7.5, color="#b45309")

    # Connecting Flow Arrows
    ax.annotate("", xy=(54, 66), xytext=(46, 66),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#1d4ed8", width=2, headwidth=7))
    ax.text(50, 69, "Panggil", ha="center", fontsize=7.5, fontweight="bold", color="#1d4ed8")

    ax.annotate("", xy=(46, 34), xytext=(54, 50),
                arrowprops=dict(facecolor="#d97706", edgecolor="#b45309", width=2, headwidth=7))
    ax.text(53, 39, "Output", ha="center", fontsize=7.5, fontweight="bold", color="#b45309")

    # Signature call
    ax.text(50, 6, "Sintaksis Ekivalen: hitung_indeks_kanopi = audit_telemetri(hitung_indeks_kanopi)", 
            ha="center", fontsize=8.5, fontfamily="monospace", fontweight="bold", color="#111827",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f3f4f6", edgecolor="#9ca3af", lw=1.2))

    plt.tight_layout()
    target_path = "docs/assets/anatomi_fungsi_dan_dekorator_sawit.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")

    # Copy to artifact dir
    shutil.copy(target_path, os.path.join(artifact_dir, "anatomi_fungsi_dan_dekorator_sawit.png"))


if __name__ == "__main__":
    generate_diagram_legb()
    generate_diagram_decorator()
    print("All Modul 3.6 diagrams generated successfully!")
