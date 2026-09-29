import os

replacements = {
    # 1. Tripartit -> Tiga Tingkat / Tiga Pilar / Tiga Representasi
    r"docs\part-01\AI_Modul_1.2_Sejarah_dan_Perkembangan.md": [
        ("perpaduan tripartit:", "sinergi tiga pilar:")
    ],
    r"docs\part-01\AI_Modul_1.4_Jenis_AI_ANI_AGI_ASI.md": [
        ("klasifikasi tripartit kapabilitas kecerdasan buatan:", "klasifikasi tiga tingkat kapabilitas kecerdasan buatan:"),
        ("## 3. Landasan Teori: Klasifikasi Tripartit Kapabilitas AI", "## 3. Landasan Teori: Klasifikasi Tiga Tingkat Kapabilitas AI")
    ],
    r"docs\part-02\AI_Modul_2.2_Flowchart_dan_Pseudocode.md": [
        ("Keterampilan Translasi Lintas-Representasi (*Tripartite Translation*)", "Keterampilan Translasi Lintas-Representasi (*Three-Way Representation Translation*)")
    ],

    # 2. Ontologis -> Struktural / Hakikat / Kedudukan Fungsional / Logis
    r"docs\part-03\AI_Modul_3.10_Penggunaan_Package_Manager_pip.md": [
        ("posisi ontologis dan interaksi fungsional", "posisi struktural dan interaksi fungsional")
    ],
    r"docs\part-03\AI_Modul_3.6_Fungsi_dan_Modularisasi.md": [
        ("arti ontologis bahwa fungsi", "arti mendasar bahwa fungsi"),
        ("Status ontologis entitas program", "Kedudukan fungsional entitas program")
    ],
    r"docs\part-03\AI_Modul_3.7_Struktur_Data_Lanjut.md": [
        ("hubungan ontologis antara metode dunder", "hubungan logis antara metode dunder")
    ],
    r"instructor_resources\part-01\AI_Modul_1.1_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("namun secara ontologis filosofis, model tersebut", "namun secara hakikat, model tersebut")
    ],
    r"instructor_resources\part-03\AI_Modul_3.7_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("hubungan ontologis antara metode dunder", "hubungan logis antara metode dunder")
    ],

    # 3. Epistemologis -> Keilmuan / Aliran Pemikiran Fundamental
    r"docs\part-01\AI_Modul_1.1_Konsep_Dasar_Artificial_Intelligence.md": [
        ("dua **paradigma epistemologis pemikiran**:", "dua **aliran pemikiran fundamental**:")
    ],
    r"docs\part-04\AI_Modul_4.1_Pengantar_Data_Science.md": [
        ("Secara epistemologis, sains data bertumpu pada", "Secara keilmuan, sains data bertumpu pada")
    ],

    # 4. Manifestasi Dependensi -> Manifes Dependensi
    r"docs\part-03\AI_Modul_3.2_Instalasi_dan_Environment.md": [
        ("### 5.5 Tahap 5: Ekspor Manifestasi Dependensi (`requirements.txt`)", "### 5.5 Tahap 5: Ekspor Manifes Dependensi (`requirements.txt`)")
    ],
    r"instructor_resources\part-03\AI_Modul_3.2_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("manifestasi dependensi", "manifes dependensi"),
        ("Manifestasi Dependensi", "Manifes Dependensi")
    ],

    # 5. Dialektika -> Dinamika
    r"docs\part-01\AI_Modul_1.1_Konsep_Dasar_Artificial_Intelligence.md": [
        ("Seluruh dialektika pasang-surut", "Seluruh dinamika pasang-surut")
    ],

    # 6. De facto -> Standar Industri
    r"docs\part-04\AI_Modul_4.1_Pengantar_Data_Science.md": [
        ("merupakan metodologi de facto yang memandu", "merupakan metodologi standar industri yang memandu")
    ]
}

base_dir = r"e:\Project Buku"
total_changed = 0

for rel_path, pairs in replacements.items():
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"File not found: {rel_path}")
        continue
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    for old_txt, new_txt in pairs:
        if old_txt in content:
            content = content.replace(old_txt, new_txt)
            modified = True
            total_changed += 1
            print(f"Replaced in {rel_path}: '{old_txt}' -> '{new_txt}'")
        else:
            print(f"Warning: '{old_txt}' not found in {rel_path}")
            
    if modified:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

print(f"\nTotal replacements applied: {total_changed}")
