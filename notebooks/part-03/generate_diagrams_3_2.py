import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
import os

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def buat_diagram_isolasi_venv():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Judul
    ax.text(5.5, 5.8, "Arsitektur Isolasi Lingkungan Virtual Python: Mengatasi Konflik Dependensi", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.45, "Perbandingan: Lingkungan Global Monolitik (Kiri) vs Lingkungan Virtual Terisolasi Berbasis Proyek (Kanan)", 
            ha='center', va='center', fontsize=9, style='italic', color='#4a5568')

    # Sisi Kiri: Masalah Lingkungan Global
    rect_kiri = patches.FancyBboxPatch((0.5, 0.8), 4.6, 4.3, boxstyle="round,pad=0.15", 
                                       facecolor="#fff5f5", edgecolor="#e53e3e", linewidth=2)
    ax.add_patch(rect_kiri)
    ax.text(2.8, 4.8, "[X] LINGKUNGAN GLOBAL MONOLITIK\n(Dependency Hell & Kerentanan Sistem)", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#9b2c2c')

    # Detail Kiri
    box_g1 = patches.FancyBboxPatch((0.8, 3.4), 4.0, 0.9, boxstyle="round,pad=0.1", 
                                    facecolor="#fed7d7", edgecolor="#c53030", linewidth=1.2)
    ax.add_patch(box_g1)
    ax.text(2.8, 3.85, "Proyek A: Deteksi Penyakit Sawit\nMembutuhkan: PyTorch 1.12 + NumPy 1.21", 
            ha='center', va='center', fontsize=8, color='#742a2a')

    box_g2 = patches.FancyBboxPatch((0.8, 2.2), 4.0, 0.9, boxstyle="round,pad=0.1", 
                                    facecolor="#fed7d7", edgecolor="#c53030", linewidth=1.2)
    ax.add_patch(box_g2)
    ax.text(2.8, 2.65, "Proyek B: Robotika Traktor Otonom\nMembutuhkan: PyTorch 2.2 + NumPy 1.26", 
            ha='center', va='center', fontsize=8, color='#742a2a')

    ax.text(2.8, 1.35, "KONFLIK FATAL:\nInstalasi Proyek B menimpa dependensi Proyek A!\nSistem operasi global menjadi rusak & tidak stabil.", 
            ha='center', va='center', fontsize=8, fontweight='bold', color='#c53030')

    # Sisi Kanan: Solusi Isolasi Virtual Environment
    rect_kanan = patches.FancyBboxPatch((5.9, 0.8), 4.6, 4.3, boxstyle="round,pad=0.15", 
                                        facecolor="#f0fff4", edgecolor="#38a169", linewidth=2)
    ax.add_patch(rect_kanan)
    ax.text(8.2, 4.8, "[V] LINGKUNGAN VIRTUAL TERISOLASI\n(venv / conda - Best Practice Industri)", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#22543d')

    box_v1 = patches.FancyBboxPatch((6.2, 3.4), 4.0, 0.9, boxstyle="round,pad=0.1", 
                                    facecolor="#c6f6d5", edgecolor="#276749", linewidth=1.2)
    ax.add_patch(box_v1)
    ax.text(8.2, 3.85, "Virtualenv: env_sawit_vision/\n[PyTorch 1.12 | NumPy 1.21 | OpenCV 4.5]\nInterpreter Lokal Mandiri & Bebas Resiko", 
            ha='center', va='center', fontsize=8, color='#1c4532')

    box_v2 = patches.FancyBboxPatch((6.2, 2.2), 4.0, 0.9, boxstyle="round,pad=0.1", 
                                    facecolor="#c6f6d5", edgecolor="#276749", linewidth=1.2)
    ax.add_patch(box_v2)
    ax.text(8.2, 2.65, "Virtualenv: env_traktor_otonom/\n[PyTorch 2.2 | NumPy 1.26 | ROS Bridge]\nInterpreter Lokal Mandiri & Bebas Resiko", 
            ha='center', va='center', fontsize=8, color='#1c4532')

    ax.text(8.2, 1.35, "SOLUSI DETERMINISTIK:\nSetiap proyek memiliki direktori site-packages sendiri.\nReproduksibilitas 100% via requirements.txt.", 
            ha='center', va='center', fontsize=8, fontweight='bold', color='#276749')

    plt.tight_layout()
    output_path = "docs/assets/arsitektur_isolasi_virtual_environment.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 1 disimpan ke {output_path}")

def buat_diagram_workflow_environment():
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.8)
    ax.axis('off')

    # Judul
    ax.text(5.5, 5.4, "Alur Kerja Standar Pengelolaan Environment Proyek AI Agribisnis", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.05, "Standar Rekayasa Perangkat Lunak: Inisialisasi, Isolasi, Manajemen Dependensi, & Distribusi", 
            ha='center', va='center', fontsize=9, style='italic', color='#4a5568')

    steps = [
        {"x": 0.5, "y": 1.8, "w": 1.7, "h": 2.6, "no": "1. INIT", "title": "Struktur Proyek", "cmd": "mkdir proyek_ai\ncd proyek_ai\ngit init", "bg": "#ebf8ff", "border": "#3182ce"},
        {"x": 2.5, "y": 1.8, "w": 1.8, "h": 2.6, "no": "2. ISOLASI", "title": "Buat Virtualenv", "cmd": "python -m venv .venv\n.venv/Scripts/activate\n(Windows / Linux)", "bg": "#e6fffa", "border": "#319795"},
        {"x": 4.6, "y": 1.8, "w": 1.8, "h": 2.6, "no": "3. DEPENDENSI", "title": "Instalasi Paket", "cmd": "pip install --upgrade pip\npip install numpy pandas\npip install opencv-python", "bg": "#fefcbf", "border": "#d69e2e"},
        {"x": 6.7, "y": 1.8, "w": 1.8, "h": 2.6, "no": "4. KERNEL", "title": "Daftarkan Jupyter", "cmd": "python -m ipykernel\ninstall --user\n--name=proyek-env", "bg": "#feebc8", "border": "#dd6b20"},
        {"x": 8.8, "y": 1.8, "w": 1.7, "h": 2.6, "no": "5. FREEZE", "title": "Kunci Versi", "cmd": "pip freeze >\nrequirements.txt\n(Reproducible)", "bg": "#c6f6d5", "border": "#276749"},
    ]

    for s in steps:
        rect = patches.FancyBboxPatch((s["x"], s["y"]), s["w"], s["h"], boxstyle="round,pad=0.12",
                                      facecolor=s["bg"], edgecolor=s["border"], linewidth=2)
        ax.add_patch(rect)
        ax.text(s["x"] + s["w"]/2, s["y"] + s["h"] - 0.35, s["no"], 
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1a202c')
        ax.text(s["x"] + s["w"]/2, s["y"] + s["h"] - 0.75, s["title"], 
                ha='center', va='center', fontsize=8.5, fontweight='bold', color=s["border"])
        ax.text(s["x"] + s["w"]/2, s["y"] + 0.75, s["cmd"], 
                ha='center', va='center', fontsize=7.5, color='#2d3748', family='monospace')

    # Panah Transisi Antar Langkah
    arrow_props = dict(facecolor='#4a5568', edgecolor='#4a5568', width=1.5, headwidth=7, shrink=0.08)
    ax.annotate('', xy=(2.5, 3.1), xytext=(2.2, 3.1), arrowprops=arrow_props)
    ax.annotate('', xy=(4.6, 3.1), xytext=(4.3, 3.1), arrowprops=arrow_props)
    ax.annotate('', xy=(6.7, 3.1), xytext=(6.4, 3.1), arrowprops=arrow_props)
    ax.annotate('', xy=(8.8, 3.1), xytext=(8.5, 3.1), arrowprops=arrow_props)

    # Catatan Bawah
    ax.text(5.5, 0.75, "Kaidah Wajib: Folder lingkungan virtual (.venv/) JANGAN PERNAH di-commit ke Git Repository (Tambahkan ke .gitignore)", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#c53030',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff5f5', edgecolor='#feb2b2'))

    plt.tight_layout()
    output_path = "docs/assets/workflow_manajemen_environment_ai.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 2 disimpan ke {output_path}")

if __name__ == '__main__':
    os.makedirs('docs/assets', exist_ok=True)
    buat_diagram_isolasi_venv()
    buat_diagram_workflow_environment()
    
    artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"
    shutil.copy("docs/assets/arsitektur_isolasi_virtual_environment.png", os.path.join(artifact_dir, "arsitektur_isolasi_virtual_environment.png"))
    shutil.copy("docs/assets/workflow_manajemen_environment_ai.png", os.path.join(artifact_dir, "workflow_manajemen_environment_ai.png"))
    print("[OK] Seluruh diagram berhasil disalin ke artifacts directory.")
