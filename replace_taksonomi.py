import os

# Dictionary of file relative path -> list of (old_text, new_text)
replacements = {
    # Part 1
    r"docs\part-01\AI_Modul_1.4_Jenis_AI_ANI_AGI_ASI.md": [
        ("taksonomi tripartit kapabilitas", "klasifikasi tripartit kapabilitas"),
        ("## 3. Landasan Teori: Taksonomi Tripartit Kapabilitas AI", "## 3. Landasan Teori: Klasifikasi Tripartit Kapabilitas AI"),
        ("![Spektrum Taksonomi Kapabilitas AI]", "![Spektrum Klasifikasi Kapabilitas AI]")
    ],
    r"docs\part-01\AI_Modul_1.5_Contoh_Penerapan_AI_di_Berbagai_Bidang.md": [
        ("pemahaman teoretis taksonomi algoritma AI", "pemahaman teoretis klasifikasi algoritma AI"),
        ("1. **Peta Taksonomi Sektoral**:", "1. **Peta Klasifikasi Sektoral**:"),
        ("## 2. Peta Lanskap & Taksonomi Penerapan AI Lintas Sektor", "## 2. Peta Lanskap & Pemetaan Penerapan AI Lintas Sektor"),
        ("![Matriks Taksonomi Penerapan AI]", "![Matriks Pemetaan Penerapan AI]"),
        ("### 2.1. Taksonomi Modalitas Data dan Paradigma AI", "### 2.1. Klasifikasi Modalitas Data dan Paradigma AI")
    ],
    r"docs\part-01\AI_Modul_1.7_Etika_dalam_Penggunaan_AI.md": [
        ("taksonomi bias", "klasifikasi bias"),
        ("Berikut adalah taksonomi 7 dimensi etika AI", "Berikut adalah pemetaan 7 dimensi etika AI"),
        ("![Taksonomi 7 Dimensi Etika Penggunaan AI]", "![Pemetaan 7 Dimensi Etika Penggunaan AI]"),
        ("## 3. Taksonomi Sumber Bias Algoritmik", "## 3. Klasifikasi Sumber Bias Algoritmik"),
        ("Taksonomi spektrum ANI, AGI, dan peta jalan menuju ASI", "Klasifikasi spektrum ANI, AGI, dan peta jalan menuju ASI")
    ],
    r"instructor_resources\part-01\AI_Modul_1.3_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("Penguasaan Taksonomi AI-ML-DL", "Penguasaan Klasifikasi AI-ML-DL")
    ],
    r"instructor_resources\part-01\AI_Modul_1.4_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("Spektrum taksonomi ANI-AGI-ASI", "Spektrum klasifikasi ANI-AGI-ASI"),
        ("Penguasaan Konsep Taksonomi ANI-AGI-ASI", "Penguasaan Konsep Klasifikasi ANI-AGI-ASI")
    ],

    # Part 2
    r"docs\part-02\AI_Modul_2.1_Konsep_Algoritma.md": [
        ("taksonomi 3 struktur kontrol logika dasar", "klasifikasi 3 struktur kontrol logika dasar")
    ],
    r"docs\part-02\AI_Modul_2.2_Flowchart_dan_Pseudocode.md": [
        ("Berikut adalah taksonomi simbol utama", "Berikut adalah pengelompokan simbol utama")
    ],
    r"docs\part-02\AI_Modul_2.4_Variabel_dan_Tipe_Data.md": [
        ("### 3.2 Taksonomi Tipe Data Standar dalam AI", "### 3.2 Klasifikasi Tipe Data Standar dalam AI"),
        ("![Taksonomi Tipe Data AI]", "![Klasifikasi Tipe Data AI]")
    ],
    r"docs\part-02\AI_Modul_2.5_Operator_Matematika_dan_Logika.md": [
        ("### 3.1 Taksonomi Operator Aritmetika Standar dan Khusus", "### 3.1 Klasifikasi Operator Aritmetika Standar dan Khusus")
    ],
    r"docs\part-02\AI_Modul_2.6_Percabangan_If_Else.md": [
        ("## 2. Taksonomi Struktur Kontrol Alur Eksekusi", "## 2. Klasifikasi Struktur Kontrol Alur Eksekusi")
    ],
    r"docs\part-02\AI_Modul_2.7_Perulangan_For_While.md": [
        ("## 2. Taksonomi Perulangan Komputasional & Protokol Iterator Python", "## 2. Klasifikasi Perulangan Komputasional & Protokol Iterator Python"),
        ("Komputasi perulangan secara taksonomis dibagi", "Komputasi perulangan secara konseptual diklasifikasikan")
    ],
    r"docs\part-02\AI_Modul_2.9_Struktur_Data_Dasar.md": [
        ("### Taksonomi Koleksi Fundamental", "### Klasifikasi Koleksi Fundamental"),
        ("## 2. Taksonomi dan Karakteristik Formal Koleksi Data Python", "## 2. Klasifikasi dan Karakteristik Formal Koleksi Data Python"),
        ("![Taksonomi Struktur Data Dasar Python]", "![Klasifikasi Struktur Data Dasar Python]"),
        ("Gambar 2.9.1: Taksonomi Koleksi Data Fundamental", "Gambar 2.9.1: Klasifikasi Koleksi Data Fundamental")
    ],
    r"instructor_resources\part-02\AI_Modul_2.7_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("Taksonomi Loop (Definite vs Indefinite)", "Klasifikasi Loop (Definite vs Indefinite)")
    ],
    r"instructor_resources\part-02\AI_Modul_2.9_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("Taksonomi Koleksi Fundamental", "Klasifikasi Koleksi Fundamental"),
        ("Taksonomi 4 Pilar Koleksi Python", "Klasifikasi 4 Pilar Koleksi Python")
    ],
    r"notebooks\part-02\AI_Modul_2.9_Praktikum_Struktur_Data_Dasar.ipynb": [
        ("Taksonomi Koleksi Fundamental", "Klasifikasi Koleksi Fundamental")
    ],

    # Part 3
    r"docs\part-03\AI_Modul_3.3_Sintaks_Dasar_Python.md": [
        ("### 2.1 Taksonomi Token Python", "### 2.1 Klasifikasi Token Python"),
        ("![Taksonomi PEP 8 dan Docstring]", "![Standarisasi PEP 8 dan Docstring]"),
        ("Taksonomi Konvensi Penamaan PEP 8", "Sistematika Konvensi Penamaan PEP 8")
    ],
    r"docs\part-03\AI_Modul_3.4_Variabel_dan_Tipe_Data.md": [
        ("Taksonomi Tipe Data Skalar", "Klasifikasi Tipe Data Skalar"),
        ("## 4. Taksonomi dan Karakteristik Tipe Data Skalar Fundamental", "## 4. Klasifikasi dan Karakteristik Tipe Data Skalar Fundamental"),
        ("![Taksonomi Tipe Data Skalar AI]", "![Klasifikasi Tipe Data Skalar AI]"),
        ("Taksonomi Tipe Data Skalar Fundamental Python", "Klasifikasi Tipe Data Skalar Fundamental Python")
    ],
    r"docs\part-03\AI_Modul_3.8_Penanganan_Berkas.md": [
        ("![Taksonomi Format Serialisasi Data Kecerdasan Buatan Agribisnis]", "![Klasifikasi Format Serialisasi Data Kecerdasan Buatan Agribisnis]"),
        ("Taksonomi Format Serialisasi Data Kecerdasan Buatan", "Klasifikasi Format Serialisasi Data Kecerdasan Buatan")
    ],
    r"docs\part-03\AI_Modul_3.9_Penanganan_Pengecualian_dan_Debugging.md": [
        ("taksonomi kelas pengecualian kustom", "hierarki kelas pengecualian kustom"),
        ("### 3.1 Merancang Taksonomi Eksepsi Domain Kustom", "### 3.1 Merancang Hierarki Eksepsi Domain Kustom"),
        ("Pewarisan Taksonomi Eksepsi Khusus", "Pewarisan Hierarki Eksepsi Khusus"),
        ("Penjelajahan taksonomi pustaka kecerdasan buatan utama", "Penjelajahan ekosistem pustaka kecerdasan buatan utama")
    ],
    r"docs\part-03\AI_Modul_3.10_Penggunaan_Package_Manager_pip.md": [
        ("Taksonomi Pustaka AI Agribisnis", "Ekosistem Pustaka AI Agribisnis"),
        ("taksonomi hierarki tumpukan pustaka", "sistematika hierarki tumpukan pustaka"),
        ("## 4. Taksonomi Ekosistem Pustaka Sains Data dan Kecerdasan Buatan Agribisnis", "## 4. Pemetaan Ekosistem Pustaka Sains Data dan Kecerdasan Buatan Agribisnis"),
        ("![Taksonomi Arsitektur Ekosistem Pustaka Kecerdasan Buatan Agribisnis]", "![Pemetaan Arsitektur Ekosistem Pustaka Kecerdasan Buatan Agribisnis]"),
        ("Taksonomi Arsitektur Ekosistem Pustaka Kecerdasan Buatan Agribisnis", "Pemetaan Arsitektur Ekosistem Pustaka Kecerdasan Buatan Agribisnis")
    ],
    r"instructor_resources\part-03\AI_Modul_3.4_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("Taksonomi Tipe Data Skalar", "Klasifikasi Tipe Data Skalar"),
        ("Taksonomi Tipe Skalar", "Klasifikasi Tipe Skalar")
    ],
    r"instructor_resources\part-03\AI_Modul_3.9_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("Taksonomi Eksepsi Kustom", "Hierarki Eksepsi Kustom")
    ],
    r"instructor_resources\part-03\AI_Modul_3.10_Panduan_Instruktur_dan_Kunci_Solusi.md": [
        ("Taksonomi Pustaka AI Agribisnis", "Ekosistem Pustaka AI Agribisnis"),
        ("Taksonomi Pustaka AI & Benchmark", "Ekosistem Pustaka AI & Benchmark")
    ],
    r"notebooks\part-03\AI_Modul_3.4_Praktikum_Variabel_dan_Tipe_Data.ipynb": [
        ("Taksonomi Tipe Data Skalar", "Klasifikasi Tipe Data Skalar")
    ],
    r"notebooks\part-03\AI_Modul_3.9_Praktikum_Penanganan_Pengecualian_dan_Debugging.ipynb": [
        ("taksonomi eksepsi kustom domain", "hierarki eksepsi kustom domain"),
        ("Definisi Taksonomi Eksepsi Khusus PKS Sawit", "Definisi Hierarki Eksepsi Khusus PKS Sawit")
    ],
    r"notebooks\part-03\AI_Modul_3.10_Praktikum_Penggunaan_Package_Manager_pip.ipynb": [
        ("Taksonomi Pustaka AI Agribisnis", "Ekosistem Pustaka AI Agribisnis")
    ],

    # Part 4
    r"docs\part-04\AI_Modul_4.1_Pengantar_Data_Science.md": [
        ("![Taksonomi Data Science dan CRISP-DM]", "![Peta Konsep Data Science dan CRISP-DM]"),
        ("## 4. Taksonomi Peran dan Ekosistem Profesi Data Modern", "## 4. Pemetaan Peran dan Ekosistem Profesi Data Modern")
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
