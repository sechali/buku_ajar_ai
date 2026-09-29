import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
import os

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def buat_diagram_pattern_matching():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Judul
    ax.text(5.5, 5.8, "Arsitektur Structural Pattern Matching (match-case) Python 3.10+", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.45, "Aplikasi Otomasi Sortasi Fraksi Kematangan Tandan Buah Segar (TBS) Kelapa Sawit di PKS", 
            ha='center', va='center', fontsize=9, style='italic', color='#4a5568')

    # Kotak Input Objek
    box_in = patches.FancyBboxPatch((0.5, 2.2), 2.2, 2.0, boxstyle="round,pad=0.1", 
                                    facecolor="#ebf8ff", edgecolor="#3182ce", linewidth=2)
    ax.add_patch(box_in)
    ax.text(1.6, 3.8, "OBJEK DATA TBS\n(Janjang Masuk)", ha='center', va='center', fontsize=9, fontweight='bold', color='#2b6cb0')
    ax.text(1.6, 2.9, "TiketTBS(\n fraksi=2,\n brondol=15.5,\n berat_kg=24.0\n)", ha='center', va='center', fontsize=7.5, family='monospace', color='#2d3748')

    # Kotak Evaluator match-case
    box_match = patches.FancyBboxPatch((3.4, 0.8), 7.0, 4.4, boxstyle="round,pad=0.15", 
                                      facecolor="#f7fafc", edgecolor="#4a5568", linewidth=2)
    ax.add_patch(box_match)
    ax.text(6.9, 4.85, "EVALUASI POLA STRUKTURAL (match tiket)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1a202c')

    cases = [
        {"y": 3.9, "title": "case TiketTBS(fraksi=0) | TiketTBS(brondol=0.0):", 
         "act": "-> [MUTU: MENTAH] Penalti Diskon Harga 50%", "bg": "#fed7d7", "bdr": "#e53e3e", "c": "#742a2a"},
        
        {"y": 2.9, "title": "case TiketTBS(fraksi=f, brondol=b) if f in [1, 2, 3] and b >= 12.5:", 
         "act": "-> [MUTU: MATANG PRIMA] Ekstraksi CPO Maksimal (Klausa Penjaga `if`)", "bg": "#c6f6d5", "bdr": "#276749", "c": "#1c4532"},
        
        {"y": 1.9, "title": "case TiketTBS(fraksi=4 | 5):", 
         "act": "-> [MUTU: LEWAT MATANG / BUSUK] Kadar Asam Lemak Bebas (ALB) Tinggi", "bg": "#fefcbf", "bdr": "#d69e2e", "c": "#744210"},

        {"y": 0.9, "title": "case _:", 
         "act": "-> [WILDCARD DEFAULT] Anomali Sensorik / Data Tidak Valid", "bg": "#edf2f7", "bdr": "#718096", "c": "#2d3748"}
    ]

    for cs in cases:
        c_box = patches.FancyBboxPatch((3.7, cs["y"]-0.05), 6.4, 0.85, boxstyle="round,pad=0.08", 
                                       facecolor=cs["bg"], edgecolor=cs["bdr"], linewidth=1.2)
        ax.add_patch(c_box)
        ax.text(3.9, cs["y"] + 0.55, cs["title"], ha='left', va='center', fontsize=7.5, family='monospace', fontweight='bold', color=cs["c"])
        ax.text(4.1, cs["y"] + 0.22, cs["act"], ha='left', va='center', fontsize=7.5, color='#1a202c')

    # Panah Transisi
    arrow_props = dict(facecolor='#3182ce', edgecolor='#3182ce', width=2, headwidth=7, shrink=0.05)
    ax.annotate('', xy=(3.4, 3.2), xytext=(2.7, 3.2), arrowprops=arrow_props)

    plt.tight_layout()
    output_path = "docs/assets/arsitektur_structural_pattern_matching_sawit.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 1 disimpan ke {output_path}")

def buat_diagram_siklus_loop():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Judul
    ax.text(5.5, 5.8, "Siklus Alur Eksekusi Perulangan (for / while) dengan break, continue, & else", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.45, "Semantik Unik: Klausa `else` Hanya Dieksekusi Jika Perulangan Selesai Alami Tanpa Interupsi `break`", 
            ha='center', va='center', fontsize=9, style='italic', color='#4a5568')

    # Elemen Flowchart
    # 1. Start Loop
    b_start = patches.FancyBboxPatch((0.6, 2.5), 1.8, 1.4, boxstyle="round,pad=0.1", 
                                     facecolor="#ebf8ff", edgecolor="#3182ce", linewidth=2)
    ax.add_patch(b_start)
    ax.text(1.5, 3.2, "MULAI LOOP\n(Ambil Elemen\nBerikutnya)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#2b6cb0')

    # 2. Decision Masih Ada Data?
    b_cond = patches.Polygon([[4.0, 3.9], [5.0, 3.2], [4.0, 2.5], [3.0, 3.2]], 
                             facecolor="#feebc8", edgecolor="#dd6b20", linewidth=2)
    ax.add_patch(b_cond)
    ax.text(4.0, 3.2, "Masih Ada\nData?", ha='center', va='center', fontsize=8, fontweight='bold', color='#7b341e')

    # 3. Tubuh Loop
    b_body = patches.FancyBboxPatch((3.0, 0.9), 2.0, 1.0, boxstyle="round,pad=0.08", 
                                    facecolor="#ffffff", edgecolor="#4a5568", linewidth=1.5)
    ax.add_patch(b_body)
    ax.text(4.0, 1.4, "Eksekusi Tubuh\nPernyataan Loop", ha='center', va='center', fontsize=8, color='#1a202c')

    # 4. Break Box (Kanan Bawah)
    b_break = patches.FancyBboxPatch((6.0, 0.9), 1.8, 1.0, boxstyle="round,pad=0.08", 
                                     facecolor="#fed7d7", edgecolor="#e53e3e", linewidth=1.5)
    ax.add_patch(b_break)
    ax.text(6.9, 1.4, "Kondisi break?\n-> Keluar Segera!", ha='center', va='center', fontsize=8, fontweight='bold', color='#742a2a')

    # 5. Blok ELSE Perulangan (Kanan Atas)
    b_else = patches.FancyBboxPatch((6.2, 2.7), 2.2, 1.4, boxstyle="round,pad=0.1", 
                                    facecolor="#c6f6d5", edgecolor="#276749", linewidth=2)
    ax.add_patch(b_else)
    ax.text(7.3, 3.4, "BLOK `else`:\nEksekusi Alami\n(Pencarian Gagal)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1c4532')

    # 6. Selesai
    b_end = patches.FancyBboxPatch((9.2, 1.8), 1.3, 1.4, boxstyle="round,pad=0.1", 
                                   facecolor="#edf2f7", edgecolor="#4a5568", linewidth=2)
    ax.add_patch(b_end)
    ax.text(9.85, 2.5, "SELESAI\n(Lanjut ke\nBaris Luar)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#2d3748')

    # Panah-panah
    arr = dict(facecolor='#4a5568', edgecolor='#4a5568', width=1.5, headwidth=6, shrink=0.05)
    ax.annotate('', xy=(3.0, 3.2), xytext=(2.4, 3.2), arrowprops=arr) # start -> cond
    ax.annotate('Ya', xy=(4.0, 1.9), xytext=(4.0, 2.5), arrowprops=arr, fontsize=8, fontweight='bold') # cond -> body
    ax.annotate('Tidak (Habis)', xy=(6.2, 3.2), xytext=(5.0, 3.2), arrowprops=arr, fontsize=8, fontweight='bold') # cond -> else
    ax.annotate('', xy=(6.0, 1.4), xytext=(5.0, 1.4), arrowprops=arr) # body -> break cond
    
    # Dari Else ke End
    ax.annotate('', xy=(9.2, 2.7), xytext=(8.4, 3.2), arrowprops=arr)
    # Dari Break ke End
    arr_red = dict(facecolor='#e53e3e', edgecolor='#e53e3e', width=1.5, headwidth=6, shrink=0.05)
    ax.annotate('break!', xy=(9.2, 2.3), xytext=(7.8, 1.4), arrowprops=arr_red, fontsize=8, color='#c53030', fontweight='bold')

    # Continue loop back
    ax.annotate('continue', xy=(1.5, 2.5), xytext=(3.0, 1.2), 
                arrowprops=dict(facecolor='#3182ce', edgecolor='#3182ce', width=1.2, headwidth=5, connectionstyle="arc3,rad=0.3"), 
                fontsize=8, color='#2b6cb0', fontweight='bold')

    plt.tight_layout()
    output_path = "docs/assets/siklus_iterasi_dan_kontrol_loop.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 2 disimpan ke {output_path}")

if __name__ == '__main__':
    os.makedirs('docs/assets', exist_ok=True)
    buat_diagram_pattern_matching()
    buat_diagram_siklus_loop()
    
    artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"
    shutil.copy("docs/assets/arsitektur_structural_pattern_matching_sawit.png", os.path.join(artifact_dir, "arsitektur_structural_pattern_matching_sawit.png"))
    shutil.copy("docs/assets/siklus_iterasi_dan_kontrol_loop.png", os.path.join(artifact_dir, "siklus_iterasi_dan_kontrol_loop.png"))
    print("[OK] Seluruh diagram berhasil disalin ke artifacts directory.")
