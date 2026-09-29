import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
import os

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def buat_diagram_anatomi_sintaks():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Judul Diagram
    ax.text(5.5, 5.8, "Anatomi Sintaksis Python: Mekanisme Indentasi Signifikan & Tokenisasi Blok", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.45, "Aturan Off-Side: Pengelompokan Pernyataan Berbasis Whitespace Menggantikan Kurung Kurawal {}", 
            ha='center', va='center', fontsize=9, style='italic', color='#4a5568')

    # Kotak Kode Visual (Kiri)
    rect_code = patches.FancyBboxPatch((0.6, 0.8), 5.2, 4.3, boxstyle="round,pad=0.15", 
                                       facecolor="#1a202c", edgecolor="#4a5568", linewidth=2)
    ax.add_patch(rect_code)
    ax.text(3.2, 4.8, "[KODE SUMBER PYTHON]", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#63b3ed')

    code_lines = [
        ("def evaluasi_lahan(kelembaban: float):", "#68d391", 0.9, 4.3, "Tingkat Indentasi 0 (Kolom 1)"),
        ("    if kelembaban < 30.0:", "#cbd5e0", 0.9, 3.8, "Token INDENT (+4 Spasi)"),
        ("        status = 'IRIGASI_DARURAT'", "#fbd38d", 0.9, 3.3, "Token INDENT (+4 Spasi / Kolom 8)"),
        ("        nyalakan_pompa()", "#cbd5e0", 0.9, 2.8, "Tingkat Indentasi 2 (Kolom 8)"),
        ("    else:", "#cbd5e0", 0.9, 2.3, "Token DEDENT (-4 Spasi / Kembali ke Kolom 4)"),
        ("        status = 'OPTIMAL'", "#fbd38d", 0.9, 1.8, "Token INDENT (+4 Spasi)"),
        ("    return status", "#68d391", 0.9, 1.3, "Token DEDENT (-4 Spasi / Kolom 4)"),
    ]

    for line, col, x_pos, y_pos, note in code_lines:
        ax.text(x_pos, y_pos, line, ha='left', va='center', fontsize=8.5, family='monospace', color=col)

    # Penjelasan Arsitektur Lexer (Kanan)
    rect_info = patches.FancyBboxPatch((6.1, 0.8), 4.3, 4.3, boxstyle="round,pad=0.15", 
                                       facecolor="#f7fafc", edgecolor="#cbd5e0", linewidth=2)
    ax.add_patch(rect_info)
    ax.text(8.25, 4.8, "[MEKANISME TOKENISASI LEXER]", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#2b6cb0')

    lexer_steps = [
        {"y": 3.9, "t": "1. Indentation Stack", "d": "Lexer mengelola stack integer alokasi spasi [0]. Saat indentasi bertambah, nilai baru di-push ke stack."},
        {"y": 2.9, "t": "2. Emisi Token INDENT", "d": "Ketika indentasi kolom bertambah (misal 0 -> 4), Lexer mengemisikan token internal INDENT ke parser."},
        {"y": 1.9, "t": "3. Emisi Token DEDENT", "d": "Saat indentasi berkurang, Lexer men-pop stack dan mengemisikan satu atau beberapa token DEDENT."},
        {"y": 1.0, "t": "4. Bebas 'Dangling Else'", "d": "Klausa 'else' terikat secara deterministik pada blok indentasi pasangannya tanpa ambiguitas logika."},
    ]

    for st in lexer_steps:
        ax.text(6.3, st["y"] + 0.25, st["t"], ha='left', va='center', fontsize=8.5, fontweight='bold', color='#2d3748')
        ax.text(6.3, st["y"] - 0.1, st["d"], ha='left', va='center', fontsize=7.5, color='#4a5568', wrap=True)

    plt.tight_layout()
    output_path = "docs/assets/anatomi_sintaks_dan_indentasi_python.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 1 disimpan ke {output_path}")

def buat_diagram_pep8_dan_docstring():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Judul
    ax.text(5.5, 5.8, "Taksonomi Konvensi Kode Bersih PEP 8 & Struktur Dokumentasi PEP 257", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1a365d')
    ax.text(5.5, 5.45, "Standarisasi Rekayasa Perangkat Lunak untuk Kecerdasan Buatan dan Sains Data Agribisnis", 
            ha='center', va='center', fontsize=9, style='italic', color='#4a5568')

    # Kotak Kiri: Konvensi Penamaan PEP 8
    rect_kiri = patches.FancyBboxPatch((0.6, 0.8), 4.6, 4.3, boxstyle="round,pad=0.15", 
                                       facecolor="#edf2f7", edgecolor="#4a5568", linewidth=2)
    ax.add_patch(rect_kiri)
    ax.text(2.9, 4.8, "KONVENSI IDENTIFIER (PEP 8)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1a202c')

    rules = [
        ("Nama Modul / Paket", "lowercase_dengan_garis", "misal: `irigasi_sawit.py`"),
        ("Nama Kelas", "PascalCase (CapWords)", "misal: `KalkulatorNeracaAir`"),
        ("Nama Fungsi & Metode", "snake_case (huruf kecil)", "misal: `hitung_evapotranspirasi()`"),
        ("Nama Variabel", "snake_case", "misal: `suhu_kanopi_c`"),
        ("Konstanta Global", "UPPER_SNAKE_CASE", "misal: `KONSTANTA_SOLAR_RAD`"),
        ("Atribut Terproteksi", "_single_leading_underscore", "misal: `_kalibrasi_internal`"),
    ]

    y_pos = 4.2
    for entitas, gaya, contoh in rules:
        ax.text(0.9, y_pos, f"* {entitas}:", fontsize=8, fontweight='bold', color='#2b6cb0')
        ax.text(1.1, y_pos - 0.22, f"  Gaya: {gaya} -> {contoh}", fontsize=7.5, color='#2d3748', family='monospace')
        y_pos -= 0.58

    # Kotak Kanan: Struktur Docstrings PEP 257 (Google Style)
    rect_kanan = patches.FancyBboxPatch((5.8, 0.8), 4.6, 4.3, boxstyle="round,pad=0.15", 
                                        facecolor="#f0fff4", edgecolor="#38a169", linewidth=2)
    ax.add_patch(rect_kanan)
    ax.text(8.1, 4.8, "STRUKTUR DOCSTRING (PEP 257)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#22543d')

    doc_elements = [
        ("1. Ringkasan Singkat (Satu Baris)", "Menjelaskan fungsi aksioma dalam satu kalimat deklaratif singkat."),
        ("2. Deskripsi Lanjutan (Opsional)", "Penjelasan konteks matematika atau fenomena agronomis yang dimodelkan."),
        ("3. Bagian 'Args:' / Parameter", "Mendokumentasikan nama argumen, tipe data, serta rentang validitas fisik."),
        ("4. Bagian 'Returns:'", "Mendokumentasikan tipe data nilai kembalian dan satuan fisik (kg/ha, °C)."),
        ("5. Bagian 'Raises:'", "Menyatakan potensi eksepsi yang dilemparkan (misal `ValueError`)."),
    ]

    y_pos = 4.2
    for judul, desc in doc_elements:
        ax.text(6.1, y_pos, judul, fontsize=8, fontweight='bold', color='#276749')
        ax.text(6.3, y_pos - 0.22, desc, fontsize=7.5, color='#2d3748')
        y_pos -= 0.65

    plt.tight_layout()
    output_path = "docs/assets/taksonomi_pep8_dan_docstring.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[OK] Diagram 2 disimpan ke {output_path}")

if __name__ == '__main__':
    os.makedirs('docs/assets', exist_ok=True)
    buat_diagram_anatomi_sintaks()
    buat_diagram_pep8_dan_docstring()
    
    artifact_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"
    shutil.copy("docs/assets/anatomi_sintaks_dan_indentasi_python.png", os.path.join(artifact_dir, "anatomi_sintaks_dan_indentasi_python.png"))
    shutil.copy("docs/assets/taksonomi_pep8_dan_docstring.png", os.path.join(artifact_dir, "taksonomi_pep8_dan_docstring.png"))
    print("[OK] Seluruh diagram berhasil disalin ke artifacts directory.")
