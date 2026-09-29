import glob
import os
import re

files = sorted(glob.glob('docs/part-*/*.md'))

compliant = []
non_compliant = {}

for f in files:
    c = open(f, encoding='utf-8').read()
    fname = os.path.basename(f)
    pdir = os.path.basename(os.path.dirname(f))
    
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

    issues = []
    if s1_title != 'Identitas & Kerangka Capaian Pembelajaran (Sub-CPMK)':
        issues.append(f'Judul Bagian 1: "{s1_title}"')
    if km == 'MISSING':
        issues.append('Blok Identitas Modul belum ada')
    elif not km.startswith('AI Modul'):
        issues.append(f'Format Kode Modul: "{km}" (seharusnya "AI Modul X.Y")')
    if mk != 'Kecerdasan Buatan dan Sains Data Pertanian Presisi':
        issues.append(f'Nama Mata Kuliah: "{mk}"')
    if aw != '2 x 50 Menit (Kajian Teori & Diskusi) + 2 x 50 Menit (Eksplorasi Praktikum Mandiri)':
        issues.append(f'Alokasi Waktu: "{aw}"')
    if sks != '3 SKS':
        issues.append(f'Beban SKS: "{sks}"')
        
    if not issues:
        compliant.append((pdir, fname))
    else:
        non_compliant.setdefault(pdir, []).append((fname, issues))

print(f'Total Compliant: {len(compliant)} / {len(files)}')
print(f'Total Non-Compliant: {sum(len(v) for v in non_compliant.values())} / {len(files)}')

print('\n=== RINCIAN KETIDAKSESUAIAN PER PART ===')
for pdir, items in non_compliant.items():
    print(f'\n{pdir.upper()} ({len(items)} modul):')
    for fname, issues in items:
        print(f'  • {fname}:')
        for iss in issues:
            print(f'     - {iss}')
