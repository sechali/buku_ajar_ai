import os

extra_replacements = {
    r"docs\part-01\AI_Modul_1.2_Sejarah_dan_Perkembangan.md": [
        ("taksonomi struktur", "sistematika struktur")
    ],
    r"docs\part-01\AI_Modul_1.3_Perbedaan_AI_ML_dan_Deep_Learning.md": [
        ("## 3. Landasan Teori & Hubungan Taksonomi Hierarkis", "## 3. Landasan Teori & Hubungan Hierarkis Keilmuan"),
        ("Hubungan taksonomi formal adalah", "Hubungan hierarkis formal adalah"),
        ("Klasifikasi taksonomi kapabilitas kecerdasan ini", "Klasifikasi kapabilitas kecerdasan ini")
    ],
    r"docs\part-01\AI_Modul_1.4_Jenis_AI_ANI_AGI_ASI.md": [
        ("Kajian Taksonomi Kapabilitas & Etika", "Kajian Klasifikasi Kapabilitas & Etika")
    ],
    r"instructor_resources\part-03\AI_Modul_3.10_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("memahami taksonomi pustaka AI", "memahami ekosistem pustaka AI")
    ],
    r"instructor_resources\part-03\AI_Modul_3.9_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("membuat taksonomi eksepsi agribisnis", "membuat hierarki eksepsi agribisnis")
    ]
}

base_dir = r"e:\Project Buku"
for rel_path, pairs in extra_replacements.items():
    full_path = os.path.join(base_dir, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        for old_txt, new_txt in pairs:
            if old_txt in content:
                content = content.replace(old_txt, new_txt)
                print(f"Replaced in {rel_path}: '{old_txt}' -> '{new_txt}'")
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
print("Extra replacements completed.")
