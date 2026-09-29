"""Script to generate high-resolution (300 DPI) diagrams for AI Modul 3.10
Penggunaan Package Manager (pip) dan Ekosistem Pustaka AI:
1. arsitektur_manajemen_dependensi_pip_ai.png
2. taksonomi_ekosistem_pustaka_ai_agribisnis.png
"""

import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directories exist
os.makedirs("docs/assets", exist_ok=True)
artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"

def generate_diagram_pip_dependency():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "ARSITEKTUR MANAJEMEN DEPENDENSI PIP & ALUR DETERMINISTIK AI", 
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Dari Repositori PyPI ke Lingkungan Terisolasi: Resolusi Pohon Dependensi & Penguncian Hash Integritas", 
            ha="center", va="center", fontsize=8.5, style="italic", color="#4a5568")

    # Step 1: PyPI Cloud Repository
    rect_pypi = patches.FancyBboxPatch((4, 52), 24, 34, boxstyle="round,pad=1.0", 
                                       facecolor="#eff6ff", edgecolor="#2563eb", linewidth=1.8)
    ax.add_patch(rect_pypi)
    ax.text(16, 81, "1. REPOSITORI PyPI", ha="center", fontsize=9.5, fontweight="bold", color="#1e40af")
    ax.text(16, 75, "Python Package Index", ha="center", fontsize=7.5, color="#1d4ed8")
    ax.text(16, 64, "Format Distribusi:\n• Wheel (.whl) [Pra-Kompilasi]\n• Source Dist (.tar.gz) [sdist]\n• Metadata SHA-256 Hashes", 
            ha="center", fontsize=7, color="#1e3a8a")

    # Arrow PyPI to Pip Resolver
    ax.annotate("", xy=(37, 69), xytext=(28, 69), arrowprops=dict(facecolor="#2563eb", width=2, headwidth=6))
    ax.text(32.5, 72, "Download\nMetadata", ha="center", fontsize=7, fontweight="bold", color="#1e40af")

    # Step 2: pip Resolver & SAT Solver
    rect_pip = patches.FancyBboxPatch((37, 52), 26, 34, boxstyle="round,pad=1.0", 
                                      facecolor="#fef3c7", edgecolor="#d97706", linewidth=1.8)
    ax.add_patch(rect_pip)
    ax.text(50, 81, "2. PIP RESOLVER", ha="center", fontsize=9.5, fontweight="bold", color="#92400e")
    ax.text(50, 75, "Mesin Resolusi Dependensi", ha="center", fontsize=7.5, color="#b45309")
    ax.text(50, 64, "• Penganalisis Pohon Konflik\n• Resolusi SemVer (~=, >=, ==)\n• Validasi Kompatibilitas ABI\n  (cp310-win_amd64)", 
            ha="center", fontsize=7, color="#78350f")

    # Arrow Pip Resolver to Target Env
    ax.annotate("", xy=(72, 69), xytext=(63, 69), arrowprops=dict(facecolor="#d97706", width=2, headwidth=6))
    ax.text(67.5, 72, "Install\nBinaries", ha="center", fontsize=7, fontweight="bold", color="#b45309")

    # Step 3: Target Virtual Environment
    rect_venv = patches.FancyBboxPatch((72, 52), 24, 34, boxstyle="round,pad=1.0", 
                                       facecolor="#ecfdf5", edgecolor="#059669", linewidth=1.8)
    ax.add_patch(rect_venv)
    ax.text(84, 81, "3. VIRTUAL ENV (.venv)", ha="center", fontsize=9.5, fontweight="bold", color="#065f46")
    ax.text(84, 75, "Isolasi Lib/site-packages", ha="center", fontsize=7.5, color="#047857")
    ax.text(84, 64, "• Paket Terinstalasi Nyata\n• Eksekutor Skrip Scripts/\n• Tanpa Konflik Global OS\n  (Zero Global Pollution)", 
            ha="center", fontsize=7, color="#064e3b")

    # Bottom Container: Manifests & Locking Mechanisms
    rect_man = patches.FancyBboxPatch((4, 12), 92, 34, boxstyle="round,pad=1.0", 
                                      facecolor="#f8fafc", edgecolor="#475569", linewidth=2.0)
    ax.add_patch(rect_man)
    ax.text(50, 41, "MANIFES DEPENDENSI: DARI PERMINTAAN LONGGAR MENUJU PENGUNCIAN DETERMINISTIK", 
            ha="center", fontsize=9.5, fontweight="bold", color="#1e293b")

    # Manifest Boxes
    # 1. pyproject.toml / requirements.in
    rect_m1 = patches.Rectangle((8, 17), 26, 20, facecolor="#eff6ff", edgecolor="#3b82f6", lw=1.2)
    ax.add_patch(rect_m1)
    ax.text(21, 33, "A. Manifes Deklaratif", ha="center", fontsize=8, fontweight="bold", color="#1d4ed8")
    ax.text(21, 28, "pyproject.toml / requirements.in", ha="center", fontsize=6.8, fontfamily="monospace", color="#1e40af")
    ax.text(21, 21, "numpy >= 1.24.0\npandas >= 2.0.0\nscikit-learn ~= 1.3.0", ha="center", fontsize=6.8, fontfamily="monospace", color="#334155")

    # Arrow 1 -> 2
    ax.annotate("", xy=(40, 27), xytext=(34, 27), arrowprops=dict(facecolor="#2563eb", width=1.5, headwidth=5))
    ax.text(37, 29, "pip-compile\n/ uv lock", ha="center", fontsize=6.5, fontweight="bold", color="#2563eb")

    # 2. requirements.lock / pinned requirements.txt
    rect_m2 = patches.Rectangle((40, 17), 52, 20, facecolor="#f0fdf4", edgecolor="#16a34a", lw=1.2)
    ax.add_patch(rect_m2)
    ax.text(66, 33, "B. Manifes Terkunci Deterministik (Pinned Lockfile with SHA-256)", ha="center", fontsize=8, fontweight="bold", color="#15803d")
    ax.text(66, 28, "requirements.txt (Produksi Server PKS Bebas Drift)", ha="center", fontsize=6.8, color="#166534")
    ax.text(66, 21, "numpy==1.26.4 --hash=sha256:7b49...\npandas==2.2.1 --hash=sha256:e3b0...\nscikit-learn==1.4.1.post1 --hash=sha256:4a8c...", 
            ha="center", fontsize=6.5, fontfamily="monospace", color="#14532d")

    # Bottom Footer
    ax.text(50, 5, "Keuntungan Manifes Terkunci: Menggaransi 100% reproduktibilitas hasil inferensi AI di server cloud dan laptop mahasiswa.", 
            ha="center", fontsize=7.5, style="italic", color="#475569")

    plt.tight_layout()
    target_path = "docs/assets/arsitektur_manajemen_dependensi_pip_ai.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")
    shutil.copy(target_path, os.path.join(artifact_dir, "arsitektur_manajemen_dependensi_pip_ai.png"))


def generate_diagram_ai_ecosystem():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "TAKSONOMI ARSITEKTUR EKOSISTEM PUSTAKA KECERDASAN BUATAN AGRIBISNIS", 
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Integrasi Berjenjang: Dari Lapisan Aljabar Matriks NumPy hingga Aplikasi Cerdas Kelapa Sawit INSTIPER", 
            ha="center", va="center", fontsize=8.5, style="italic", color="#4a5568")

    layers = [
        {
            "tier": "LAPISAN 5: APLIKASI KECERDASAN BUATAN AGRIBISNIS INSTIPER",
            "desc": "Sortasi Fraksi TBS Otomatis • Sensus Spasial Kanopi Sawit • Prediksi Yield CPO • Kendali Irigasi Presisi",
            "c": "#fef2f2", "bc": "#dc2626", "tc": "#991b1b", "y": 75, "h": 12
        },
        {
            "tier": "LAPISAN 4: PEMODELAN AI, MACHINE LEARNING, & VISI KOMPUTER",
            "desc": "Scikit-Learn (Regresi/Klasifikasi/K-Means) • OpenCV & Pillow (Pemrosesan Citra Drone Multispektral)",
            "c": "#fff7ed", "bc": "#ea580c", "tc": "#9a3412", "y": 59, "h": 12
        },
        {
            "tier": "LAPISAN 3: ANALITIKA DATA TABULAR & VISUALISASI ILMIAH",
            "desc": "Pandas (DataFrame Sensus & Deret Waktu Telemetri) • Matplotlib & Seaborn (Visualisasi Statistik Kebun)",
            "c": "#fefce8", "bc": "#ca8a04", "tc": "#854d0e", "y": 43, "h": 12
        },
        {
            "tier": "LAPISAN 2: FONDASI KOMPUTASI NUMERIK VEKTORISASI (NUMPY)",
            "desc": "NumPy (ndarray C-Order Contiguous Memory, Operasi Aljabar Linier BLAS/LAPACK, Penyiaran / Broadcasting)",
            "c": "#f0fdf4", "bc": "#16a34a", "tc": "#14532d", "y": 27, "h": 12
        },
        {
            "tier": "LAPISAN 1: PUSTAKA STANDAR PYTHON & INTERPRETER CPYTHON",
            "desc": "CPython Runtime • Modul Bawaan (math, collections, io, csv, json, pickle, logging, sys, os)",
            "c": "#eff6ff", "bc": "#2563eb", "tc": "#1e40af", "y": 11, "h": 12
        }
    ]

    for l in layers:
        rect = patches.FancyBboxPatch((5, l["y"]), 90, l["h"], boxstyle="round,pad=0.8", 
                                      facecolor=l["c"], edgecolor=l["bc"], linewidth=1.8)
        ax.add_patch(rect)
        ax.text(50, l["y"] + 8, l["tier"], ha="center", fontsize=8.5, fontweight="bold", color=l["tc"])
        ax.text(50, l["y"] + 3.2, l["desc"], ha="center", fontsize=7.2, color="#334155")

    # Side Arrows showing dependency inheritance
    ax.annotate("", xy=(97, 85), xytext=(97, 13), arrowprops=dict(facecolor="#475569", width=2.5, headwidth=7))
    ax.text(98.5, 50, "Pewarisan Ketergantungan\n(Bottom-Up Stack)", va="center", rotation=270, fontsize=7.5, fontweight="bold", color="#334155")

    plt.tight_layout()
    target_path = "docs/assets/taksonomi_ekosistem_pustaka_ai_agribisnis.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")
    shutil.copy(target_path, os.path.join(artifact_dir, "taksonomi_ekosistem_pustaka_ai_agribisnis.png"))


if __name__ == "__main__":
    generate_diagram_pip_dependency()
    generate_diagram_ai_ecosystem()
    print("All Modul 3.10 diagrams generated successfully!")
