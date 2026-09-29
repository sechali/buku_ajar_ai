"""Script to generate high-resolution (300 DPI) diagrams for AI Modul 3.8
Penanganan Berkas (File Handling):
1. arsitektur_io_dan_context_manager_python.png
2. taksonomi_format_serialisasi_data_ai.png
"""

import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directories exist
os.makedirs("docs/assets", exist_ok=True)
artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"

def generate_diagram_io_context():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "ARSITEKTUR SUBSISTEM I/O CPYTHON DAN SIKLUS CONTEXT MANAGER", 
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Aliran Data Ber-buffer dan Jaminan Pembebasan Berkas Deskriptor Sistem Operasi (PEP 343)", 
            ha="center", va="center", fontsize=8.5, style="italic", color="#4a5568")

    # Outer Container: User Space / Python Runtime
    rect_user = patches.FancyBboxPatch((3, 20), 54, 68, boxstyle="round,pad=1.2", 
                                       facecolor="#f8fafc", edgecolor="#475569", linewidth=2.0)
    ax.add_patch(rect_user)
    ax.text(30, 84, "RUANG PENGGUNA (PYTHON RUNTIME / CPYTHON)", ha="center", fontsize=10.5, fontweight="bold", color="#1e293b")

    # Layer 1: Python Code & Context Manager with statement
    rect_cm = patches.FancyBboxPatch((6, 56), 48, 22, boxstyle="round,pad=0.8", 
                                     facecolor="#eff6ff", edgecolor="#2563eb", linewidth=1.8)
    ax.add_patch(rect_cm)
    ax.text(30, 73, "Pernyataan 'with open(\"telemetri.csv\", \"r\") as f:'", ha="center", fontsize=8.5, fontfamily="monospace", fontweight="bold", color="#1e40af")
    ax.text(30, 66, "1. Memanggil f.__enter__() -> Membuka stream & mengembalikan objek f\n2. Menjalankan blok kode pemrosesan data telemetri\n3. Memanggil f.__exit__() -> Otomatis menutup stream & flush buffer", 
            ha="center", fontsize=7.5, color="#1d4ed8")

    # Layer 2: TextIOWrapper & BufferedReader
    rect_buf = patches.FancyBboxPatch((6, 26), 48, 24, boxstyle="round,pad=0.8", 
                                      facecolor="#ecfdf5", edgecolor="#059669", linewidth=1.8)
    ax.add_patch(rect_buf)
    ax.text(30, 44, "Lapisan Abstraksi Stream (Modul io CPython)", ha="center", fontsize=9.5, fontweight="bold", color="#065f46")
    ax.text(30, 38, "• io.TextIOWrapper (Penyandian Karakter UTF-8, decoding byte -> str)\n• io.BufferedReader / BufferedWriter (Buffer RAM internal 8 KB)\n• Mencegah pemanggilan system call berlebih ke Kernel OS", 
            ha="center", fontsize=7.5, color="#047857")

    # Middle Arrow from User Space to Kernel Space
    ax.annotate("", xy=(63, 54), xytext=(57, 54),
                arrowprops=dict(facecolor="#2563eb", edgecolor="#1d4ed8", width=2.5, headwidth=7))
    ax.text(60, 57, "System Call\nread()/write()", ha="center", fontsize=7.5, fontweight="bold", color="#1e40af")

    # Right Container: OS Kernel & Hardware
    rect_kernel = patches.FancyBboxPatch((63, 20), 34, 68, boxstyle="round,pad=1.2", 
                                         facecolor="#fff7ed", edgecolor="#ea580c", linewidth=2.0)
    ax.add_patch(rect_kernel)
    ax.text(80, 84, "KERNEL OS & PERANGKAT KERAS", ha="center", fontsize=10, fontweight="bold", color="#9a3412")

    # Kernel File Descriptor Table
    rect_fd = patches.FancyBboxPatch((66, 52), 28, 26, boxstyle="round,pad=0.8", 
                                     facecolor="#ffedd5", edgecolor="#c2410c", linewidth=1.6)
    ax.add_patch(rect_fd)
    ax.text(80, 72, "Tabel Berkas Deskriptor", ha="center", fontsize=9, fontweight="bold", color="#7c2d12")
    ax.text(80, 66, "FD #0 : stdin\nFD #1 : stdout\nFD #2 : stderr\nFD #3 : telemetri.csv", 
            ha="center", fontsize=7.5, fontfamily="monospace", color="#9a3412")
    ax.text(80, 56, "[Dibatasi oleh OS ulimit]", ha="center", fontsize=7, style="italic", color="#c2410c")

    # Storage Hardware
    rect_disk = patches.FancyBboxPatch((66, 26), 28, 20, boxstyle="round,pad=0.8", 
                                       facecolor="#f1f5f9", edgecolor="#64748b", linewidth=1.6)
    ax.add_patch(rect_disk)
    ax.text(80, 40, "Penyimpanan Fisik (SSD/HDD)", ha="center", fontsize=9, fontweight="bold", color="#334155")
    ax.text(80, 32, "Sektor Blok Disk & Page Cache\nFormat Berkas: .csv, .json, .pkl", ha="center", fontsize=7.5, color="#475569")

    # Bottom Banner
    rect_bot = patches.Rectangle((3, 4), 94, 12, facecolor="#f8fafc", edgecolor="#94a3b8", lw=1)
    ax.add_patch(rect_bot)
    ax.text(50, 11, "Jaminan Integritas Data Melalui Context Manager:", ha="center", fontsize=8.5, fontweight="bold", color="#0f172a")
    ax.text(50, 7, "Blok 'with' menjamin f.__exit__() SELALU dipanggil untuk menutup FD #3 dan melakukan flush buffer,\nbahkan jika terjadi eksepsi tak terduga (ZeroDivisionError, ValueError) di tengah pemrosesan data.", 
            ha="center", fontsize=7.5, color="#334155")

    plt.tight_layout()
    target_path = "docs/assets/arsitektur_io_dan_context_manager_python.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")
    shutil.copy(target_path, os.path.join(artifact_dir, "arsitektur_io_dan_context_manager_python.png"))


def generate_diagram_serialization():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title
    ax.text(50, 96, "TAKSONOMI FORMAT SERIALISASI DATA KECERDASAN BUATAN AGRIBISNIS", 
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1a202c")
    ax.text(50, 92, "Perbandingan Format Berkas: Plain Text, Tabular CSV, Hirarki JSON/GeoJSON, dan Serialisasi Biner Pickle", 
            ha="center", va="center", fontsize=8.5, style="italic", color="#4a5568")

    formats = [
        {
            "title": "PLAIN TEXT / LOG (.log, .txt)",
            "color_bg": "#f8fafc",
            "color_border": "#64748b",
            "color_txt": "#1e293b",
            "use_case": "Pencatatan log transaksi timbangan lori, jejak eksepsi sensor, dan output audit.",
            "char": "• Berbasis baris (line-oriented)\n• Dibaca secara lazy stream O(1)\n• Human-readable universal",
            "x": 3, "w": 22
        },
        {
            "title": "TABULAR CSV (.csv)",
            "color_bg": "#f0fdf4",
            "color_border": "#16a34a",
            "color_txt": "#14532d",
            "use_case": "Deret waktu telemetri stasiun cuaca, hasil sensus kanopi pokok sawit, metrik panen.",
            "char": "• Modul csv (DictReader/Writer)\n• Ringkas untuk data tabular 2D\n• Sangat portabel ke Excel/Pandas",
            "x": 27, "w": 22
        },
        {
            "title": "HIERARKI JSON (.json, .geojson)",
            "color_bg": "#eff6ff",
            "color_border": "#2563eb",
            "color_txt": "#1e3a8a",
            "use_case": "Poligon batas blok kebun (GeoJSON), parameter konfigurasi model AI, metadata drone.",
            "char": "• Modul json (load/dump)\n• Struktur hierarki bersarang\n• Standar pertukaran API web",
            "x": 51, "w": 22
        },
        {
            "title": "BINER PICKLE (.pkl, .bin)",
            "color_bg": "#fef2f2",
            "color_border": "#dc2626",
            "color_txt": "#7f1d1d",
            "use_case": "Serialisasi model regresi terkalibrasi, struktur kelas kustom, cache array NumPy.",
            "char": "• Modul pickle (dump/load)\n• Preservasi objek Python penuh\n• PERINGATAN: Rawan celah RCE!",
            "x": 75, "w": 22
        }
    ]

    for fmt in formats:
        rect = patches.FancyBboxPatch((fmt["x"], 16), fmt["w"], 72, boxstyle="round,pad=1.0", 
                                      facecolor=fmt["color_bg"], edgecolor=fmt["color_border"], linewidth=2.0)
        ax.add_patch(rect)
        ax.text(fmt["x"] + fmt["w"]/2, 83, fmt["title"], ha="center", fontsize=8.5, fontweight="bold", color=fmt["color_txt"])
        
        # Karakteristik Box
        rect_in1 = patches.Rectangle((fmt["x"] + 1, 46), fmt["w"] - 2, 33, facecolor="#ffffff", edgecolor=fmt["color_border"], lw=1)
        ax.add_patch(rect_in1)
        ax.text(fmt["x"] + 2, 75, "Karakteristik Teknis:", fontsize=7.5, fontweight="bold", color=fmt["color_txt"])
        ax.text(fmt["x"] + 2, 60, fmt["char"], fontsize=7, color="#334155")

        # Kasus Penggunaan Box
        rect_in2 = patches.Rectangle((fmt["x"] + 1, 18), fmt["w"] - 2, 26, facecolor="#ffffff", edgecolor=fmt["color_border"], lw=1)
        ax.add_patch(rect_in2)
        ax.text(fmt["x"] + 2, 40, "Aplikasi di Perkebunan:", fontsize=7.5, fontweight="bold", color=fmt["color_txt"])
        ax.text(fmt["x"] + 2, 28, fmt["use_case"], fontsize=6.8, color="#475569")

    # Bottom warning
    rect_bot = patches.Rectangle((3, 4), 94, 9, facecolor="#fef2f2", edgecolor="#ef4444", lw=1.2)
    ax.add_patch(rect_bot)
    ax.text(50, 8.5, "Peringatan Keamanan Serialisasi AI: Dilarang keras memuat berkas pickle dari sumber tak tepercaya!", 
            ha="center", fontsize=7.8, fontweight="bold", color="#b91c1c")

    plt.tight_layout()
    target_path = "docs/assets/taksonomi_format_serialisasi_data_ai.png"
    plt.savefig(target_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target_path}")
    shutil.copy(target_path, os.path.join(artifact_dir, "taksonomi_format_serialisasi_data_ai.png"))


if __name__ == "__main__":
    generate_diagram_io_context()
    generate_diagram_serialization()
    print("All Modul 3.8 diagrams generated successfully!")
