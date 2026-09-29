import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
import os

# Konfigurasi Font dan DPI
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def buat_diagram_arsitektur_cpython():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Judul Diagram
    ax.text(5.5, 5.6, "Arsitektur Model Eksekusi CPython: Dari Kode Sumber ke Mesin Fisik", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.25, "Alur Transformasi: Source Code -> Kompilasi Internal -> Bytecode -> Virtual Machine (PVM) -> CPU", 
            ha='center', va='center', fontsize=9.5, style='italic', color='#4a5568')

    # Kotak Tahapan
    boxes = [
        {"x": 0.5, "y": 2.2, "w": 1.7, "h": 2.2, "title": "Kode Sumber (.py)", "sub": "Teks karakter\n(Human-readable)\nSyntax PEP 8", "bg": "#e6fffa", "border": "#319795"},
        {"x": 2.6, "y": 1.5, "w": 2.1, "h": 3.3, "title": "Kompilasi Internal\n(Compiler Pipeline)", "sub": "1. Tokenizer (Lexer)\n2. Parser (Concrete ST)\n3. AST Generation\n4. Symbol Table\n5. Bytecode Generator", "bg": "#ebf8ff", "border": "#3182ce"},
        {"x": 5.1, "y": 2.2, "w": 1.7, "h": 2.2, "title": "Bytecode (.pyc)", "sub": "Instruksi kompak\nPlatform-independent\nMagic Number\n__pycache__", "bg": "#fefcbf", "border": "#d69e2e"},
        {"x": 7.2, "y": 1.5, "w": 2.0, "h": 3.3, "title": "Python Virtual\nMachine (PVM)", "sub": "1. Evaluation Loop\n2. Call Stack Frame\n3. Object Allocator\n4. Reference Counting\n5. Garbage Collector", "bg": "#feebc8", "border": "#dd6b20"},
        {"x": 9.6, "y": 2.2, "w": 1.7, "h": 2.2, "title": "Perangkat Keras\n(CPU / GPU)", "sub": "Instruksi Biner\nx86-64 / ARM / RISC-V\n(Server / Edge IoT)", "bg": "#fed7d7", "border": "#e53e3e"},
    ]

    for b in boxes:
        rect = patches.FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"], 
                                      boxstyle="round,pad=0.12", 
                                      facecolor=b["bg"], edgecolor=b["border"], linewidth=2)
        ax.add_patch(rect)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"] - 0.45, b["title"], 
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1a202c')
        ax.text(b["x"] + b["w"]/2, b["y"] + (b["h"]-0.7)/2, b["sub"], 
                ha='center', va='center', fontsize=8, color='#2d3748', linespacing=1.3)

    # Panah Transisi Antar-Tahap
    arrow_props = dict(facecolor='#4a5568', edgecolor='#4a5568', width=1.5, headwidth=7, shrink=0.08)
    ax.annotate('', xy=(2.6, 3.3), xytext=(2.2, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(5.1, 3.3), xytext=(4.7, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(7.2, 3.3), xytext=(6.8, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(9.6, 3.3), xytext=(9.2, 3.3), arrowprops=arrow_props)

    # Keterangan Bawah
    ax.text(5.5, 0.65, "[Prinsip Utama: Write Once, Run Anywhere via PVM Execution Engine]", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#2b6cb0',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#edf2f7', edgecolor='#cbd5e0'))

    plt.tight_layout()
    output_path = "docs/assets/arsitektur_eksekusi_cpython.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 1 berhasil disimpan ke {output_path}")

def buat_diagram_ekosistem_ai_agribisnis():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Judul Diagram
    ax.text(5.5, 6.1, "Hierarki Ekosistem Python untuk Kecerdasan Buatan dalam Agribisnis Presisi", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.75, "Integrasi Multi-Layer: Core Interpreter -> Scientific Stack -> Data/ML -> Aplikasi Cerdas Industri", 
            ha='center', va='center', fontsize=9.5, style='italic', color='#4a5568')

    layers = [
        {"y": 4.5, "h": 0.9, "title": "LAPISAN 4: APLIKASI CERDAS PERKEBUNAN INSTIPER", 
         "desc": "Deteksi Defisiensi Nutrisi NPK Daun Sawit | Prediksi Tonase Panen TBS | Navigasi Traktor Otonom | IoT Sensor Telemetri", 
         "bg": "#c6f6d5", "border": "#276749", "title_col": "#22543d"},
        
        {"y": 3.4, "h": 0.9, "title": "LAPISAN 3: FRAMEWORK KECERDASAN BUATAN & COMPUTER VISION", 
         "desc": "PyTorch (Deep Learning) | TensorFlow / Keras | OpenCV (Computer Vision Citra Drone) | Scikit-Learn (Predictive ML)", 
         "bg": "#bee3f8", "border": "#2b6cb0", "title_col": "#2c5282"},

        {"y": 2.3, "h": 0.9, "title": "LAPISAN 2: KOMPUTASI SAINTIFIK & ANALITIKA DATA", 
         "desc": "NumPy (Manipulasi Matriks Tensor C-Optimized) | SciPy (Statistika & Optimasi) | Pandas (Analisis Tabular & Time-Series)", 
         "bg": "#feebc8", "border": "#c05621", "title_col": "#7b341e"},

        {"y": 1.2, "h": 0.9, "title": "LAPISAN 1: PYTHON CORE & C-EXTENSION FOUNDATION", 
         "desc": "CPython Engine 3.10+ | Modul Standar (math, sys, dataclasses, typing) | Dynamic Typing & Auto-Memory (Garbage Collector)", 
         "bg": "#edf2f7", "border": "#4a5568", "title_col": "#2d3748"},
    ]

    for lay in layers:
        rect = patches.FancyBboxPatch((0.8, lay["y"]), 9.4, lay["h"],
                                      boxstyle="round,pad=0.1",
                                      facecolor=lay["bg"], edgecolor=lay["border"], linewidth=2)
        ax.add_patch(rect)
        ax.text(5.5, lay["y"] + lay["h"] - 0.28, lay["title"], 
                ha='center', va='center', fontsize=10, fontweight='bold', color=lay["title_col"])
        ax.text(5.5, lay["y"] + 0.3, lay["desc"], 
                ha='center', va='center', fontsize=8.5, color='#1a202c')

    # Panah Hubungan Bertingkat
    for y_arrow in [4.38, 3.28, 2.18]:
        ax.annotate('', xy=(5.5, y_arrow + 0.1), xytext=(5.5, y_arrow - 0.06),
                    arrowprops=dict(facecolor='#4a5568', edgecolor='#4a5568', width=2, headwidth=8, shrink=0.05))

    # Keterangan Kunci Sukses
    ax.text(5.5, 0.45, "Keunggulan Python di Industri AI: Keterbacaan Tinggi, Kompatibilitas Backend C/C++, dan Ekosistem Pustaka Terbesar di Dunia", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#2b6cb0',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ebf8ff', edgecolor='#90cdf4'))

    plt.tight_layout()
    output_path = "docs/assets/ekosistem_ai_python_agribisnis.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 2 berhasil disimpan ke {output_path}")

if __name__ == '__main__':
    os.makedirs('docs/assets', exist_ok=True)
    buat_diagram_arsitektur_cpython()
    buat_diagram_ekosistem_ai_agribisnis()
    
    # Salin ke folder artifacts
    artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"
    shutil.copy("docs/assets/arsitektur_eksekusi_cpython.png", os.path.join(artifact_dir, "arsitektur_eksekusi_cpython.png"))
    shutil.copy("docs/assets/ekosistem_ai_python_agribisnis.png", os.path.join(artifact_dir, "ekosistem_ai_python_agribisnis.png"))
    print("[OK] Seluruh diagram berhasil disalin ke artifacts directory.")
