import os
import shutil
import glob
import re
import subprocess

# 1. Staging current 8.1 - 8.6 for Part 9
os.makedirs('staging_dl', exist_ok=True)
for i in range(1, 7):
    for f in glob.glob(f'docs/part-08/AI_Modul_8.{i}_*'):
        shutil.copy(f, 'staging_dl/')
    for f in glob.glob(f'notebooks/part-08/AI_Modul_8.{i}_*'):
        shutil.copy(f, 'staging_dl/')
    for f in glob.glob(f'instructor_resources/part-08/AI_Modul_8.{i}_*'):
        shutil.copy(f, 'staging_dl/')
    for f in glob.glob(f'docx/part-08/AI_Modul_8.{i}_*'):
        shutil.copy(f, 'staging_dl/')
print("Staged 8.1-8.6 into staging_dl/")

# 2. Map 8.7-8.11 to 8.1-8.5
part8_map = [
    (7, 1, 'Preprocessing_Dataset', 'AI Modul 8.1: Preprocessing Dataset', 'AI Modul 7.10 (Gradient Boosting)', 'AI Modul 8.2: Training Model'),
    (8, 2, 'Training_Model', 'AI Modul 8.2: Training Model', 'AI Modul 8.1 (Preprocessing Dataset)', 'AI Modul 8.3: Evaluasi Model'),
    (9, 3, 'Evaluasi_Model', 'AI Modul 8.3: Evaluasi Model', 'AI Modul 8.2 (Training Model)', 'AI Modul 8.4: Interpretasi Hasil Model'),
    (10, 4, 'Interpretasi_Hasil_Model', 'AI Modul 8.4: Interpretasi Hasil Model', 'AI Modul 8.3 (Evaluasi Model)', 'AI Modul 8.5: Pembuatan Sistem Prediksi Sederhana'),
    (11, 5, 'Pembuatan_Sistem_Prediksi_Sederhana', 'AI Modul 8.5: Pembuatan Sistem Prediksi Sederhana', 'AI Modul 8.4 (Interpretasi Hasil Model)', 'AI Modul 9.1: Konsep Deep Learning')
]

# Read, update, and write the 5 target files
for old_idx, new_idx, topic, title, prereq, bridging in part8_map:
    # 1. Diktat md
    old_md = glob.glob(f'docs/part-08/AI_Modul_8.{old_idx}_*.md')[0]
    with open(old_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update title
    content = re.sub(r'^# AI Modul 8\.\d+:.*$', f'# {title}', content, flags=re.MULTILINE)
    # Update Kode Modul
    content = re.sub(r'\* \*\*Kode Modul\*\*: AI-08-\d+', f'* **Kode Modul**: AI-08-0{new_idx}', content)
    # Update Prasyarat
    content = re.sub(r'\* \*\*Prasyarat\*\*:.*$', f'* **Prasyarat**: {prereq}', content, flags=re.MULTILINE)
    # Update Sub-CPMK numbers
    content = re.sub(rf'Sub-CPMK 8\.{old_idx}\.', f'Sub-CPMK 8.{new_idx}.', content)
    content = re.sub(rf'AI-08-{old_idx:02d}', f'AI-08-0{new_idx}', content)
    # Update bridging
    content = re.sub(r'## 9\. Jembatan Konsep \(Bridging\) ke AI Modul 8\.\d+:.*', f'## 9. Jembatan Konsep (Bridging) ke {bridging}', content)
    if new_idx == 5:
        content = re.sub(r'## 9\. Jembatan Konsep \(Bridging\).*', f'## 9. Jembatan Konsep (Bridging) ke {bridging}', content)
    
    new_md = f'docs/part-08/AI_Modul_8.{new_idx}_{topic}.md'
    with open(new_md, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written diktat: {new_md}")

    # 2. Notebook
    old_nb = glob.glob(f'notebooks/part-08/AI_Modul_8.{old_idx}_*.ipynb')[0]
    with open(old_nb, 'r', encoding='utf-8') as f:
        nb_str = f.read()
    nb_str = nb_str.replace(f'Modul 8.{old_idx}', f'Modul 8.{new_idx}')
    nb_str = nb_str.replace(f'AI-08-{old_idx:02d}', f'AI-08-0{new_idx}')
    new_nb = f'notebooks/part-08/AI_Modul_8.{new_idx}_Praktikum_{topic}.ipynb'
    with open(new_nb, 'w', encoding='utf-8') as f:
        f.write(nb_str)
    print(f"Written notebook: {new_nb}")

    # 3. Instructor Guide
    old_guide = glob.glob(f'instructor_resources/part-08/AI_Modul_8.{old_idx}_*.md')[0]
    with open(old_guide, 'r', encoding='utf-8') as f:
        g_str = f.read()
    g_str = re.sub(r'^# AI Modul 8\.\d+:', f'# AI Modul 8.{new_idx}:', g_str, flags=re.MULTILINE)
    g_str = g_str.replace(f'AI-08-{old_idx:02d}', f'AI-08-0{new_idx}')
    g_str = g_str.replace(f'Modul 8.{old_idx}', f'Modul 8.{new_idx}')
    new_guide = f'instructor_resources/part-08/AI_Modul_8.{new_idx}_Panduan_Instruktur_dan_Kunci_Solusi.md'
    with open(new_guide, 'w', encoding='utf-8') as f:
        f.write(g_str)
    print(f"Written guide: {new_guide}")

# Remove old files (8.6, 8.7, 8.8, 8.9, 8.10, 8.11)
for idx in [6, 7, 8, 9, 10, 11]:
    for f in glob.glob(f'docs/part-08/AI_Modul_8.{idx}_*'):
        os.remove(f)
    for f in glob.glob(f'notebooks/part-08/AI_Modul_8.{idx}_*'):
        os.remove(f)
    for f in glob.glob(f'instructor_resources/part-08/AI_Modul_8.{idx}_*'):
        os.remove(f)
    for f in glob.glob(f'docx/part-08/AI_Modul_8.{idx}_*'):
        os.remove(f)

# Also remove old 8.1 to 8.5 files from docs/part-08 that don't match the new topics
valid_new_files = [f'AI_Modul_8.{new_idx}_{topic}.md' for _, new_idx, topic, _, _, _ in part8_map]
for f in glob.glob('docs/part-08/AI_Modul_8.*.md'):
    if os.path.basename(f) not in valid_new_files:
        os.remove(f)

for f in glob.glob('notebooks/part-08/AI_Modul_8.*.ipynb'):
    nb_valid = [f'AI_Modul_8.{new_idx}_Praktikum_{topic}.ipynb' for _, new_idx, topic, _, _, _ in part8_map]
    if os.path.basename(f) not in nb_valid:
        os.remove(f)

for f in glob.glob('instructor_resources/part-08/AI_Modul_8.*.md'):
    g_valid = [f'AI_Modul_8.{new_idx}_Panduan_Instruktur_dan_Kunci_Solusi.md' for _, new_idx, _, _, _, _ in part8_map]
    if os.path.basename(f) not in g_valid:
        os.remove(f)

for f in glob.glob('instructor_resources/part-08/AI_Modul_8.*.docx'):
    os.remove(f)

for f in glob.glob('docx/part-08/AI_Modul_8.*.docx'):
    os.remove(f)

print("\nPart 8 cleaned and restructured to strictly 5 modules!")
