import glob
import os
import re

print("=== MEMULAI PENYELARASAN SELURUH MODUL TEORI ===")

PART_PREREQUISITES = {
    "part-01": "Pengantar Logika Matematika / Pemikiran Komputasional Dasar",
    "part-02": "AI Modul 1.7 (Etika AI) / Pengantar Logika Komputasi",
    "part-03": "AI Modul 2.9 (Struktur Data Dasar) / Dasar Logika Pemrograman",
    "part-04": "AI Modul 3.10 (Ekosistem Pustaka Python) / Struktur Data",
    "part-05": "AI Modul 4.8 (Persiapan Dataset) / Aljabar Linier & Kalkulus Dasar",
    "part-06": "AI Modul 5.7 (Optimasi Numerik) / Dasar Probabilitas & Statistik",
    "part-07": "AI Modul 6.4 (Validasi Model) / Dasar Machine Learning",
    "part-08": "AI Modul 7.10 (Gradient Boosting) / Pemodelan Terbimbing",
    "part-09": "AI Modul 8.5 (Reduksi Dimensi) / Aljabar Linier & Optimasi Multivariat",
    "part-10": "AI Modul 9.9 (Framework Deep Learning) / Arsitektur Jaringan Saraf",
    "part-11": "AI Modul 10.7 (Regularisasi Deep Learning) / Pemrosesan Matriks Citra",
    "part-12": "AI Modul 11.9 (Real-time Camera Processing) / Visi Komputer Dasar",
    "part-13": "AI Modul 12.10 (Training Dataset Citra) / Arsitektur CNN & Object Detection"
}

PART_COGNITIVE_LEVELS = {
    "part-01": "C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)",
    "part-02": "C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)",
    "part-03": "C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)",
    "part-04": "C3 (Menerapkan), C4 (Menganalisis), C5 (Mengevaluasi)",
    "part-05": "C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)",
    "part-06": "C3 (Menerapkan), C4 (Menganalisis), C5 (Mengevaluasi)",
    "part-07": "C3 (Menerapkan), C4 (Menganalisis), C5 (Mengevaluasi)",
    "part-08": "C3 (Menerapkan), C4 (Menganalisis), C5 (Mengevaluasi)",
    "part-09": "C3 (Menerapkan), C4 (Menganalisis), C5 (Mengevaluasi)",
    "part-10": "C3 (Menerapkan), C4 (Menganalisis), C5 (Mengevaluasi)",
    "part-11": "C2 (Memahami), C3 (Menerapkan), C4 (Menganalisis)",
    "part-12": "C3 (Menerapkan), C4 (Menganalisis), C5 (Mengevaluasi)",
    "part-13": "C4 (Menganalisis), C5 (Mengevaluasi), C6 (Mencipta)"
}

# 1. Non-academic word replacements across docs
WORD_REPLACEMENTS = [
    # "jebakan" replacements
    (re.compile(r'##\s*7\.\s*Jebakan\s+Umum,\s*Kegagalan\s+Implementasi,\s*&\s*Mitigasi\s+Teknis', re.I),
     '## 7. Kekeliruan Metodologis, Potensi Kegagalan, & Mitigasi Teknis'),
    (re.compile(r'\bjebakan feromon\b', re.I), 'perangkap feromon'),
    
    # "malapetaka" replacements
    (re.compile(r'berujung pada malapetaka \*overfitting\* dan pemborosan komputasi', re.I),
     'berujung pada kegagalan generalisasi (*overfitting* parah) dan pemborosan komputasi'),
    (re.compile(r'Hal ini menjadi malapetaka komputasi karena satu gejala langka', re.I),
     'Hal ini memicu anomali komputasi (*zero probability breakdown*) karena satu fitur langka'),
    (re.compile(r'memiliki malapetaka komputasi dimensi saat menangani data berdimensi tinggi', re.I),
     'memiliki limitasi komputasi (*curse of dimensionality*) saat menangani data berdimensi tinggi'),
    (re.compile(r'mengakibatkan dua malapetaka komputasi: kehancuran relasi spasial', re.I),
     'mengakibatkan dua limitasi komputasi mendasar: hilangnya relasi spasial'),
    (re.compile(r'\bmalapetaka\b', re.I), 'kendala kritis'),

    # "magis" / "ajaib" / "kotak hitam magis"
    (re.compile(r'bukanlah kotak hitam magis', re.I), 'bukanlah entitas komputasi mistis (*opaque black-box*)'),
    (re.compile(r'Tidak ada algoritma ajaib \(\*silver bullet\*\)', re.I),
     'Tidak ada algoritma tunggal serbaguna (*no universal model / no silver bullet*)'),
    (re.compile(r'nomor ajaib \(\*magic number\*\)', re.I),
     'penanda biner unik (*file signature / magic number*)'),

    # "bayi yang buta" & "kacau"
    (re.compile(r'merupakan "bayi yang buta": bobot-bobotnya masih berupa angka acak dan prediksinya kacau', re.I),
     'belum memiliki representasi fitur terbobot: parameternya masih bernilai acak dengan distribusi prediksi berderau (*noisy*)'),

    # "paling sakti" & "keajaiban"
    (re.compile(r'algoritma paling sakti dalam dunia pembelajaran mesin', re.I),
     'algoritma paling tangguh dan berdaya generalisasi tinggi (*robust*) dalam machine learning'),
    (re.compile(r'\* \*\*Keajaiban Matematika Trik Kernel', re.I),
     '* **Elegansi Formulasi Matematika Metode Kernel'),
    (re.compile(r'Perhatikan keajaiban aljabar berikut: penyebut', re.I),
     'Perhatikan penyederhanaan aljabar eksak berikut: suku penyebut'),
    (re.compile(r'Trik Log-Sum-Exp', re.I), 'Metode Log-Sum-Exp'),
    (re.compile(r'trik stabilisasi', re.I), 'metode stabilisasi'),

    # "menelan bias" & "membabi buta" & "hancur lebur"
    (re.compile(r'MENELAN BIAS HISTORIS', re.I), 'MEREFLEKSIKAN BIAS HISTORIS DATA'),
    (re.compile(r'terakhir secara membabi buta', re.I), 'terakhir tanpa verifikasi metrik validasi (*unconditional checkpointing*)'),
    (re.compile(r'data uji akan hancur lebur \(\*overfitting\* parah\)', re.I),
     'data uji akan mengalami degradasi performa ekstrem (*overfitting* parah)'),
    (re.compile(r'pada data uji akan hancur\.', re.I), 'pada data uji akan terdegradasi secara signifikan.'),
    (re.compile(r'terjerumus ke dalam kode spageti', re.I), 'berkembang menjadi struktur kode spageti (*spaghetti code*)'),
    (re.compile(r'performa fantastis dengan akurasi', re.I), 'performa semu yang over-optimistik dengan akurasi'),
    (re.compile(r'Utas kamera menguras driver buffer terus-menerus', re.I),
     'Utas kamera mengosongkan antrean penyangga (*buffer flushing*) secara kontinu')
]

def clean_non_academic(text):
    for pat, repl in WORD_REPLACEMENTS:
        text = pat.sub(lambda m, r=repl: r, text)
    return text

def align_part12_part13_module(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)
    pdir = os.path.basename(os.path.dirname(filepath))

    # Extract module code and name
    m_code = re.search(r'AI_Modul_([\d\.]+)', fname)
    mod_code = f"AI Modul {m_code.group(1)}" if m_code else "AI Modul"

    # Extract title from line 1
    m_title = re.search(r'^#\s+(.+)$', content, re.M)
    full_title = m_title.group(1).strip() if m_title else fname
    mod_name = full_title.split(":", 1)[1].strip() if ":" in full_title else full_title

    prereq = PART_PREREQUISITES.get(pdir, "Prasyarat Terkait")
    cog_level = PART_COGNITIVE_LEVELS.get(pdir, "C3 (Menerapkan), C4 (Menganalisis), C5 (Mengevaluasi)")

    # Extract goal bullets from section 1 if present
    goals = re.findall(r'^\d+\.\s+(.+)$', content, re.M)
    cpmk_bullets = []
    for g in goals[:5]:
        g_clean = re.sub(r'[\*\#]', '', g).strip()
        cpmk_bullets.append(g_clean)

    if len(cpmk_bullets) < 3:
        cpmk_bullets = [
            f"Menganalisis (C4) arsitektur, landasan matematis, dan mekanisme komputasi pada {mod_name}.",
            f"Mengimplementasikan (C3) algoritma dan alur pemrosesan berbasis Python dan PyTorch sesuai standar industri.",
            f"Mengevaluasi (C5) kompleksitas komputasi, konsumsi memori, dan efisiensi inferensi untuk data visual lapangan.",
            f"Merancang (C6) integrasi modul cerdas untuk otomatisasi inspeksi dan monitoring pada ekosistem agrokompleks sawit."
        ]

    # Build standard Section 1 block
    meta_block = f"""## 1. Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)

* **Kode Modul**        : {mod_code}
* **Mata Kuliah**       : Kecerdasan Buatan dan Sains Data Pertanian Presisi
* **Alokasi Waktu**     : 2 x 50 Menit (Kajian Teori & Diskusi) + 2 x 50 Menit (Eksplorasi Praktikum Mandiri)
* **Beban SKS**         : 3 SKS
* **Prasyarat**         : {prereq}
* **Level Kognitif**    : {cog_level}

```mermaid
flowchart LR
    A["OUTPUTS<br/>- Dokumen Arsitektur & Notasi Formal<br/>- Skrip Implementasi Standar Industri<br/>- Laporan Validasi Kinerja Visual"] --> B["OUTCOMES<br/>- Penguasaan Formulasi Matematis Kunci<br/>- Keterampilan Penyetelan Parameter & Optimasi<br/>- Diagnosis Kerentanan & Mitigasi Teknis"]
    B --> C["IMPACTS<br/>- Keandalan Sistem Visi Komputer Edge<br/>- Efisiensi Sortasi & Monitoring Presisi<br/>- Peningkatan Produktivitas Kelapa Sawit"]
```

### 1.1 Capaian Pembelajaran Khusus (Sub-CPMK)
Setelah menyelesaikan modul ini, mahasiswa dan pembelajar diharapkan mampu:
"""
    for idx, b in enumerate(cpmk_bullets[:4], 1):
        meta_block += f"{idx}. {b}\n"

    meta_block += f"""
### 1.2 Kerangka Hasil Pembelajaran (Outputs, Outcomes, & Impacts)
* **Outputs (Keluaran Berwujud Langsung)**:
  * Dokumen rancangan arsitektur pemrosesan visual dan spesifikasi parameter model {mod_name}.
  * Berkas kode program Python modular tervalidasi menggunakan PyTorch/OpenCV yang siap diuji di lapangan.
  * Grafik metrik evaluasi kinerja (akurasi, mAP, latensi inferensi, dan konsumsi memori aktivasi).
* **Outcomes (Hasil Capaian & Perubahan Kompetensi)**:
  * Penguasaan mendalam terhadap formulasi matematika dan mekanisme konvolusi/deteksi objek visual.
  * Kemampuan analitis dalam memilih konfigurasi hyperparameter dan arsitektur model sesuai batasan sumber daya perangkat keras edge.
  * Keterampilan mengidentifikasi dan memitigasi potensi kegagalan sistem visual pada kondisi lapangan heterogen.
* **Impacts (Dampak Jangka Panjang & Nilai Guna Luas)**:
  * Terwujudnya sistem otomasi inspeksi dan monitoring perkebunan yang adaptif, berkinerja tinggi, dan efisien biaya operasional.
  * Menjadi pijakan kokoh untuk riset dan implementasi kecerdasan buatan terapan berskala komersial di sektor kelapa sawit dan pertanian presisi.

---
"""

    # Check if section 1 is Peta Konsep
    peta_pos = content.find("## 1. Peta Konsep & Orientasi Pembelajaran")
    sec2_pos = content.find("## 2.")
    
    if peta_pos != -1 and sec2_pos != -1:
        old_sec1_body = content[peta_pos + len("## 1. Peta Konsep & Orientasi Pembelajaran"):sec2_pos].strip()
        intro_paragraphs = []
        for p in old_sec1_body.split("\n\n"):
            p_strip = p.strip()
            if not p_strip.startswith("```") and not p_strip.startswith("Tujuan instruksional") and not re.match(r'^\d+\.', p_strip):
                intro_paragraphs.append(p_strip)
        intro_text = "\n\n".join(intro_paragraphs)
        if intro_text:
            intro_section = f"\n\n### 1.0 Orientasi Konsep & Urgensi Pembelajaran\n{intro_text}\n\n"
        else:
            intro_section = "\n\n"
            
        replacement = meta_block.strip() + intro_section
        new_content = content[:peta_pos] + replacement + content[sec2_pos:]
    else:
        new_content = content

    # Apply non-academic word cleaning
    new_content = clean_non_academic(new_content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated Part 12/13 module: {fname}")

def align_part07_part11_module(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)
    pdir = os.path.basename(os.path.dirname(filepath))

    m_code = re.search(r'AI_Modul_([\d\.]+)', fname)
    mod_code = f"AI Modul {m_code.group(1)}" if m_code else "AI Modul"

    # Standardize metadata lines
    content = re.sub(r'(\*\s*\*\*Kode Modul\*\*\s*:\s*).*$', lambda m: f"{m.group(1)}{mod_code}", content, flags=re.M | re.I)
    content = re.sub(r'(\*\s*\*\*Mata Kuliah\*\*\s*:\s*).*$', lambda m: f"{m.group(1)}Kecerdasan Buatan dan Sains Data Pertanian Presisi", content, flags=re.M | re.I)
    content = re.sub(r'(\*\s*\*\*Alokasi Waktu\*\*\s*:\s*).*$', lambda m: f"{m.group(1)}2 x 50 Menit (Kajian Teori & Diskusi) + 2 x 50 Menit (Eksplorasi Praktikum Mandiri)", content, flags=re.M | re.I)
    content = re.sub(r'(\*\s*\*\*Beban SKS\*\*\s*:\s*).*$', lambda m: f"{m.group(1)}3 SKS", content, flags=re.M | re.I)

    # Clean non-academic words
    content = clean_non_academic(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated Part 07-11 module: {fname}")

def align_part01_module(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)
    content = re.sub(r'(\*\s*\*\*Alokasi Waktu\*\*\s*:\s*).*$', lambda m: f"{m.group(1)}2 x 50 Menit (Kajian Teori & Diskusi) + 2 x 50 Menit (Eksplorasi Praktikum Mandiri)", content, flags=re.M | re.I)
    content = clean_non_academic(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated Part 01 module: {fname}")

def execute_all_alignments():
    all_files = sorted(glob.glob('docs/part-*/*.md'))
    print(f"Total files to process: {len(all_files)}")

    for f in all_files:
        pdir = os.path.basename(os.path.dirname(f))
        if pdir in ['part-12', 'part-13']:
            align_part12_part13_module(f)
        elif pdir in ['part-07', 'part-08', 'part-09', 'part-10', 'part-11']:
            align_part07_part11_module(f)
        elif pdir == 'part-01' and os.path.basename(f) in ['AI_Modul_1.2_Sejarah_dan_Perkembangan.md', 'AI_Modul_1.3_Perbedaan_AI_ML_dan_Deep_Learning.md', 'AI_Modul_1.4_Jenis_AI_ANI_AGI_ASI.md']:
            align_part01_module(f)
        else:
            with open(f, 'r', encoding='utf-8') as fp:
                c = fp.read()
            cleaned = clean_non_academic(c)
            if cleaned != c:
                with open(f, 'w', encoding='utf-8') as fp:
                    fp.write(cleaned)
                print(f"Cleaned non-academic words in: {os.path.basename(f)}")

    print("\n=== SEMUA MODUL BERHASIL DISELARASKAN! ===")

if __name__ == '__main__':
    execute_all_alignments()
