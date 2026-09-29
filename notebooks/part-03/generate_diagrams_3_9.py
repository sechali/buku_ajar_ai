"""Script to generate high-resolution (300 DPI) diagrams for AI Modul 3.9
Penanganan Pengecualian dan Debugging:
1. hierarki_eksepsi_cpython_dan_alur_try_except.png
2. arsitektur_logging_dan_debugging_ai.png
"""

import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directories exist
os.makedirs("docs/assets", exist_ok=True)
artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"

def generate_diagram_exception_hierarchy():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "HIERARKI POHON KELAS EKSEPSI CPYTHON DAN ALUR BLOK TRY-EXCEPT-ELSE-FINALLY", 
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Struktur Pewarisan BaseException hingga Eksepsi Domain Kustom Agribisnis & Siklus Penanganan Deterministik", 
            ha="center", va="center", fontsize=8.5, style="italic", color="#4a5568")

    # Left Container: Exception Class Tree (Hierarki Kelas)
    rect_tree = patches.FancyBboxPatch((3, 14), 48, 74, boxstyle="round,pad=1.0", 
                                       facecolor="#f8fafc", edgecolor="#334155", linewidth=2.0)
    ax.add_patch(rect_tree)
    ax.text(27, 84, "POHON HIERARKI KELAS EKSEPSI (CPython)", ha="center", fontsize=10, fontweight="bold", color="#0f172a")

    # Nodes
    # BaseException
    rect_base = patches.Rectangle((12, 74), 30, 6, facecolor="#fee2e2", edgecolor="#dc2626", lw=1.5)
    ax.add_patch(rect_base)
    ax.text(27, 77, "BaseException (Akar Teratas)", ha="center", va="center", fontsize=8, fontweight="bold", color="#991b1b")

    # Non-system exits branching out
    ax.text(44, 71, "(KeyboardInterrupt, SystemExit)", fontsize=6.8, style="italic", color="#b91c1c")

    # Exception
    rect_exc = patches.Rectangle((12, 58), 30, 6, facecolor="#ffedd5", edgecolor="#ea580c", lw=1.5)
    ax.add_patch(rect_exc)
    ax.text(27, 61, "Exception (Akar Seluruh Galat Aplikasi)", ha="center", va="center", fontsize=8, fontweight="bold", color="#9a3412")

    # Arrow BaseException -> Exception
    ax.annotate("", xy=(27, 64), xytext=(27, 74), arrowprops=dict(facecolor="#ea580c", width=1.5, headwidth=5))

    # Standard Subclasses
    subclasses = [
        ("ValueError", "Konversi gagal (float('abc'))", 44),
        ("TypeError", "Operasi tipe salah (str + int)", 36),
        ("LookupError (KeyError, IndexError)", "Kunci/indeks tidak ditemukan", 28),
        ("OSError (FileNotFoundError, PermissionError)", "Kegagalan I/O sistem operasi", 20),
    ]
    for name, desc, y in subclasses:
        rect_sub = patches.Rectangle((5, y), 42, 6, facecolor="#f1f5f9", edgecolor="#64748b", lw=1)
        ax.add_patch(rect_sub)
        ax.text(6.5, y + 3.2, f"• {name}", fontsize=7.2, fontweight="bold", color="#1e293b")
        ax.text(6.5, y + 1.2, f"  {desc}", fontsize=6.3, color="#475569")

    # Custom Agribisnis Exception Box
    rect_cust = patches.Rectangle((5, 15), 42, 3.8, facecolor="#dcfce7", edgecolor="#16a34a", lw=1.2)
    ax.add_patch(rect_cust)
    ax.text(26, 16.9, "★ Eksepsi Kustom: AnomaliSensorError, MutuTBSRejectError", ha="center", va="center", fontsize=6.8, fontweight="bold", color="#14532d")

    # Right Container: 4-Block Flowchart (try - except - else - finally)
    rect_flow = patches.FancyBboxPatch((55, 14), 42, 74, boxstyle="round,pad=1.0", 
                                       facecolor="#f0fdf4", edgecolor="#16a34a", linewidth=2.0)
    ax.add_patch(rect_flow)
    ax.text(76, 84, "ALUR KENDALI 4-BLOK DETERMINISTIK", ha="center", fontsize=10, fontweight="bold", color="#14532d")

    # Block 1: try
    rect_try = patches.FancyBboxPatch((58, 68), 36, 10, boxstyle="round,pad=0.5", 
                                      facecolor="#eff6ff", edgecolor="#2563eb", linewidth=1.5)
    ax.add_patch(rect_try)
    ax.text(76, 74, "1. Blok 'try:'", ha="center", fontsize=8.5, fontweight="bold", color="#1e40af")
    ax.text(76, 70, "Menjalankan operasi berisiko tinggi (I/O, sensor)", ha="center", fontsize=7, color="#1d4ed8")

    # Branching Arrow
    ax.annotate("Terjadi Galat", xy=(65, 54), xytext=(68, 68), arrowprops=dict(facecolor="#dc2626", width=1.5, headwidth=5),
                fontsize=7, fontweight="bold", color="#b91c1c")
    ax.annotate("Sukses Mulus", xy=(87, 54), xytext=(84, 68), arrowprops=dict(facecolor="#16a34a", width=1.5, headwidth=5),
                fontsize=7, fontweight="bold", color="#15803d")

    # Block 2: except
    rect_exp = patches.FancyBboxPatch((57, 44), 17, 10, boxstyle="round,pad=0.5", 
                                      facecolor="#fee2e2", edgecolor="#dc2626", linewidth=1.5)
    ax.add_patch(rect_exp)
    ax.text(65.5, 50, "2a. 'except:'", ha="center", fontsize=8, fontweight="bold", color="#991b1b")
    ax.text(65.5, 46, "Tangani galat & log", ha="center", fontsize=6.5, color="#7f1d1d")

    # Block 3: else
    rect_els = patches.FancyBboxPatch((78, 44), 17, 10, boxstyle="round,pad=0.5", 
                                      facecolor="#fef3c7", edgecolor="#d97706", linewidth=1.5)
    ax.add_patch(rect_els)
    ax.text(86.5, 50, "2b. 'else:'", ha="center", fontsize=8, fontweight="bold", color="#92400e")
    ax.text(86.5, 46, "Jalan jika 0 galat", ha="center", fontsize=6.5, color="#78350f")

    # Arrow to finally
    ax.annotate("", xy=(76, 32), xytext=(65.5, 44), arrowprops=dict(facecolor="#475569", width=1.5, headwidth=5))
    ax.annotate("", xy=(76, 32), xytext=(86.5, 44), arrowprops=dict(facecolor="#475569", width=1.5, headwidth=5))

    # Block 4: finally
    rect_fin = patches.FancyBboxPatch((58, 22), 36, 10, boxstyle="round,pad=0.5", 
                                      facecolor="#e0e7ff", edgecolor="#4338ca", linewidth=1.5)
    ax.add_patch(rect_fin)
    ax.text(76, 28, "3. Blok 'finally:'", ha="center", fontsize=8.5, fontweight="bold", color="#312e81")
    ax.text(76, 24, "PASTI DIEKSEKUSI (Tutup koneksi/file, flush buffer)", ha="center", fontsize=7, color="#3730a3")

    # Bottom Banner
    rect_bot = patches.Rectangle((3, 4), 94, 7.5, facecolor="#f8fafc", edgecolor="#94a3b8", lw=1)
    ax.add_patch(rect_bot)
    ax.text(50, 7.8, "Aturan Rekayasa AI: Dilarang keras menggunakan 'except:' kosong (bare except); selalu tangkap tipe spesifik!", 
            ha="center", fontsize=7.8, fontweight="bold", color="#0f172a")

    plt.tight_layout()
    target_path = "docs/assets/hierarki_eksepsi_cpython_dan_alur_try_except.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")
    shutil.copy(target_path, os.path.join(artifact_dir, "hierarki_eksepsi_cpython_dan_alur_try_except.png"))


def generate_diagram_logging_debugging():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "ARSITEKTUR LOGGING TERSTRUKTUR DAN WORKFLOW DEBUGGING AI", 
            ha="center", va="center", fontsize=12, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Pipeline Pemantauan Operasional PKS: Logger -> Filter -> Formatter -> Handlers & Isolasi Bug via PDB", 
            ha="center", va="center", fontsize=8.5, style="italic", color="#4a5568")

    # Pipeline Container (Top / Middle)
    rect_pipe = patches.FancyBboxPatch((3, 38), 94, 50, boxstyle="round,pad=1.0", 
                                       facecolor="#f8fafc", edgecolor="#475569", linewidth=2.0)
    ax.add_patch(rect_pipe)
    ax.text(50, 84, "PIPELINE LOGGING STANDAR INDUSTRI (MODUL logging)", ha="center", fontsize=10.5, fontweight="bold", color="#1e293b")

    steps = [
        {"name": "1. LOGGER", "desc": "Titik masuk event:\nlogger.info(...)\nlogger.error(...)", "x": 6, "w": 18, "c": "#dbeafe", "bc": "#2563eb"},
        {"name": "2. SEVERITY FILTER", "desc": "Ambang batas level:\nDEBUG < INFO <\nWARNING < ERROR", "x": 28, "w": 18, "c": "#fef3c7", "bc": "#d97706"},
        {"name": "3. FORMATTER", "desc": "Struktur metadata:\n[Timestamp] [Level]\n[Modul:Line] Pesan", "x": 50, "w": 18, "c": "#e0e7ff", "bc": "#4338ca"},
        {"name": "4. HANDLERS", "desc": "Tujuan output ganda:\n• StreamHandler (Console)\n• RotatingFileHandler", "x": 72, "w": 22, "c": "#ecfdf5", "bc": "#059669"},
    ]

    for s in steps:
        rect_s = patches.FancyBboxPatch((s["x"], 43), s["w"], 36, boxstyle="round,pad=0.8", 
                                        facecolor=s["c"], edgecolor=s["bc"], linewidth=1.6)
        ax.add_patch(rect_s)
        ax.text(s["x"] + s["w"]/2, 73, s["name"], ha="center", fontsize=8.5, fontweight="bold", color="#0f172a")
        ax.text(s["x"] + s["w"]/2, 58, s["desc"], ha="center", fontsize=7.2, color="#334155")

    # Connecting arrows between pipeline stages
    for x_arr in [24.5, 46.5, 68.5]:
        ax.annotate("", xy=(x_arr + 3, 61), xytext=(x_arr - 0.5, 61), 
                    arrowprops=dict(facecolor="#475569", width=2, headwidth=6))

    # Bottom Container: Debugging via pdb / breakpoint()
    rect_debug = patches.FancyBboxPatch((3, 10), 94, 24, boxstyle="round,pad=0.8", 
                                        facecolor="#fef2f2", edgecolor="#dc2626", linewidth=1.8)
    ax.add_patch(rect_debug)
    ax.text(12, 28, "WORKFLOW DEBUGGING RUNTIME VIA breakpoint() (PEP 553 / PDB):", fontsize=9, fontweight="bold", color="#991b1b")
    ax.text(12, 21, "• breakpoint() menyela eksekusi dan mengaktifkan debugger interaktif CPython di terminal saat telemetri anomali terdeteksi.\n• Perintah esensial: 'n' (langkah berikutnya), 's' (masuk ke fungsi), 'c' (lanjutkan), 'p ekspresi' (cetak variabel), 'w' (jejak stack).", 
            fontsize=7.5, color="#7f1d1d")
    ax.text(12, 13, "Keunggulan: Menghilangkan kebutuhan menghapus 'print()' debug manual sebelum kode dinaikkan ke server produksi.", 
            fontsize=7.2, style="italic", color="#991b1b")

    plt.tight_layout()
    target_path = "docs/assets/arsitektur_logging_dan_debugging_ai.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")
    shutil.copy(target_path, os.path.join(artifact_dir, "arsitektur_logging_dan_debugging_ai.png"))


if __name__ == "__main__":
    generate_diagram_exception_hierarchy()
    generate_diagram_logging_debugging()
    print("All Modul 3.9 diagrams generated successfully!")
