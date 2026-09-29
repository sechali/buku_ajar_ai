import glob
import os
import re

files = sorted(glob.glob('docs/part-*/*.md'))
print(f'Auditing {len(files)} files against reference image format...\n')

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

mismatches = []

for f in files:
    c = open(f, encoding='utf-8').read()
    fname = os.path.basename(f)
    pdir = os.path.basename(os.path.dirname(f))
    
    # Extract module code from filename or title
    m_num = re.search(r'AI_Modul_([\d\.]+)', fname)
    expected_code = f"AI Modul {m_num.group(1)}" if m_num else "AI Modul"
    
    # Check Section 1 heading
    m_s1 = re.search(r'^##\s*1\.\s*(.+)$', c, re.M)
    s1_title = m_s1.group(1).strip() if m_s1 else 'MISSING'
    
    # Check Kode Modul
    m_km = re.search(r'\*\s*\*\*Kode Modul\*\*\s*:\s*(.+)$', c, re.M | re.I)
    km = m_km.group(1).strip() if m_km else 'MISSING'
    
    # Check Mata Kuliah
    m_mk = re.search(r'\*\s*\*\*Mata Kuliah\*\*\s*:\s*(.+)$', c, re.M | re.I)
    mk = m_mk.group(1).strip() if m_mk else 'MISSING'
    
    # Check Alokasi Waktu
    m_aw = re.search(r'\*\s*\*\*Alokasi Waktu\*\*\s*:\s*(.+)$', c, re.M | re.I)
    aw = m_aw.group(1).strip() if m_aw else 'MISSING'
    
    # Check Beban SKS
    m_sks = re.search(r'\*\s*\*\*Beban SKS\*\*\s*:\s*(.+)$', c, re.M | re.I)
    sks = m_sks.group(1).strip() if m_sks else 'MISSING'
    
    # Check Prasyarat
    m_pr = re.search(r'\*\s*\*\*Prasyarat\*\*\s*:\s*(.+)$', c, re.M | re.I)
    pr = m_pr.group(1).strip() if m_pr else 'MISSING'
    
    # Check Level Kognitif
    m_lk = re.search(r'\*\s*\*\*Level Kognitif\*\*\s*:\s*(.+)$', c, re.M | re.I)
    lk = m_lk.group(1).strip() if m_lk else 'MISSING'
    
    diff = {}
    if s1_title != 'Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)':
        diff['Section 1 Heading'] = s1_title
    if km != expected_code:
        diff['Kode Modul'] = km
    if mk != 'Kecerdasan Buatan dan Sains Data Pertanian Presisi':
        diff['Mata Kuliah'] = mk
    if aw != '2 x 50 Menit (Kajian Teori & Diskusi) + 2 x 50 Menit (Eksplorasi Praktikum Mandiri)':
        diff['Alokasi Waktu'] = aw
    if sks != '3 SKS':
        diff['Beban SKS'] = sks
    if pr == 'MISSING':
        diff['Prasyarat'] = pr
    if lk == 'MISSING':
        diff['Level Kognitif'] = lk
        
    if diff:
        mismatches.append((f, diff))

print(f'Total files with format differences: {len(mismatches)} / {len(files)}')
by_part = {}
for f, diff in mismatches:
    pdir = os.path.basename(os.path.dirname(f))
    by_part.setdefault(pdir, []).append((os.path.basename(f), diff))

for pdir, items in by_part.items():
    print(f'\n--- {pdir} ({len(items)} files) ---')
    for fname, diff in items[:3]:
        print(f'  {fname}:')
        for k, v in diff.items():
            print(f'    - {k}: {v}')
    if len(items) > 3:
        print(f'    ... and {len(items)-3} more files in {pdir}')
