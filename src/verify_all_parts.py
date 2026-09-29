import glob
import os

banned = ['taksonomi', 'tripartit', 'ontologis', 'epistemologis', 'dialektika', 'manifestasi dependensi', 'de facto']

parts = ['part-08', 'part-09', 'part-10', 'part-11', 'part-12', 'part-13']
expected_counts = {'part-08': 5, 'part-09': 9, 'part-10': 7, 'part-11': 9, 'part-12': 10, 'part-13': 5}

print('=== AUDIT VERIFIKASI MENYELURUH PART 8 HINGGA PART 13 ===\n')

total_banned_found = 0
all_counts_match = True

for p in parts:
    print(f'Checking {p.upper()} (Target: {expected_counts[p]} modul)...')
    md_docs = sorted(glob.glob(f'docs/{p}/*.md'))
    nb_docs = sorted(glob.glob(f'notebooks/{p}/*.ipynb'))
    inst_docs = sorted(glob.glob(f'instructor_resources/{p}/*.md'))
    docx_docs = sorted(glob.glob(f'docx/{p}/*.docx'))
    docx_inst = sorted(glob.glob(f'docx/instructor_resources/{p}/*.docx'))
    
    print(f'  docs                : {len(md_docs)} / {expected_counts[p]}')
    print(f'  notebooks           : {len(nb_docs)} / {expected_counts[p]}')
    print(f'  instructor_resources: {len(inst_docs)} / {expected_counts[p]}')
    print(f'  docx                : {len(docx_docs)} / {expected_counts[p]}')
    print(f'  docx_instructor     : {len(docx_inst)} / {expected_counts[p]}')
    
    for count in [len(md_docs), len(nb_docs), len(inst_docs), len(docx_docs), len(docx_inst)]:
        if count != expected_counts[p]:
            all_counts_match = False
            
    for f in md_docs + inst_docs:
        with open(f, 'r', encoding='utf-8') as fh:
            text = fh.read().lower()
        for b in banned:
            if b in text:
                print(f'  [BANNED WORD] "{b}" found in {f}!')
                total_banned_found += 1

print(f'\nTotal banned words found: {total_banned_found}')
if total_banned_found == 0 and all_counts_match:
    print('STATUS: 100% SUKSES DAN SEMPURNA! SELURUH PART 8 HINGGA PART 13 LENGKAP & BERSIH!')
else:
    print('STATUS: ADA INKONSISTENSI ATAU KATA TERLARANG DITEMUKAN!')
