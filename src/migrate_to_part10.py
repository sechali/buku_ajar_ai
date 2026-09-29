import os
import shutil
import re

# Target directories
os.makedirs('docs/part-10', exist_ok=True)
os.makedirs('notebooks/part-10', exist_ok=True)
os.makedirs('instructor_resources/part-10', exist_ok=True)
os.makedirs('docx/part-10', exist_ok=True)

name_map = {
    'AI_Modul_9.1_Konsep_dan_Fundamental_Computer_Vision': 'AI_Modul_10.1_Konsep_Computer_Vision',
    'AI_Modul_9.2_Representasi_Citra_Digital_dan_Matriks_Piksel': 'AI_Modul_10.2_Representasi_Citra_Digital',
    'AI_Modul_9.3_Piksel_dan_Ruang_Warna': 'AI_Modul_10.3_Pixel_dan_Warna',
    'AI_Modul_9.4_Preprocessing_Citra': 'AI_Modul_10.4_Image_Preprocessing',
    'AI_Modul_9.5_Operasi_Filter_Spasial_dan_Konvolusi_2D': 'AI_Modul_10.5_Image_Filtering',
    'AI_Modul_9.6_Deteksi_Tepi_dan_Gradien_Citra': 'AI_Modul_10.6_Edge_Detection',
    'AI_Modul_9.7_Ekstraksi_Fitur_dan_Morfologi_Citra': 'AI_Modul_10.7_Feature_Extraction'
}

def update_content(text):
    # Replace part numbers and module codes
    text = text.replace('AI-09-0', 'AI-10-0')
    text = text.replace('part-09', 'part-10')
    text = text.replace('Part 9', 'Part 10')
    text = text.replace('Part 09', 'Part 10')
    
    # Replace Module numbers
    for i in range(1, 8):
        text = re.sub(rf'\bModul 9\.{i}\b', f'Modul 10.{i}', text)
        text = re.sub(rf'\bAI Modul 9\.{i}\b', f'AI Modul 10.{i}', text)
        
    # Replace bridging in 10.7 to Part 11
    text = text.replace('Part 10: Deep Learning untuk Computer Vision', 'Part 11: OpenCV untuk Pengolahan Citra & Video')
    text = text.replace('Part 10', 'Part 11') # in bridging context if any
    return text

print("Migrating docs/part-09 to docs/part-10...")
for old_base, new_base in name_map.items():
    old_file = f'docs/part-09/{old_base}.md'
    new_file = f'docs/part-10/{new_base}.md'
    if os.path.exists(old_file):
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        content = update_content(content)
        # Update title header
        new_title = new_base.replace('_', ' ').replace('AI Modul ', 'AI Modul ')
        content = re.sub(r'^# AI Modul 9\.\d:.*$', f'# {new_title}', content, flags=re.MULTILINE)
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] docs: {new_file}")

print("\nMigrating notebooks/part-09 to notebooks/part-10...")
for old_base, new_base in name_map.items():
    old_nb_name = old_base.replace('AI_Modul_9.', 'AI_Modul_9.').replace('AI_Modul_', 'AI_Modul_')
    # notebook names had Praktikum
    # e.g. AI_Modul_9.1_Praktikum_Konsep_dan_Fundamental_Computer_Vision.ipynb
    old_nb = f"notebooks/part-09/{old_base.replace('AI_Modul_9.', 'AI_Modul_9.').replace('AI_Modul_9.', 'AI_Modul_9.')}"
    # find actual notebook file
    import glob
    old_matches = glob.glob(f"notebooks/part-09/AI_Modul_9.{old_base.split('.')[1][0]}*.ipynb")
    if old_matches:
        old_file = old_matches[0]
        new_nb_name = new_base.replace('AI_Modul_10.', 'AI_Modul_10.').replace('AI_Modul_10.', 'AI_Modul_10._Praktikum_').replace('10._Praktikum_', '10.')
        new_file = f"notebooks/part-10/{new_base.replace('AI_Modul_10.', 'AI_Modul_10._Praktikum_').replace('10._Praktikum_', '10.')}.ipynb"
        # actually let's name it AI_Modul_10.X_Praktikum_<Topic>.ipynb
        topic_suffix = new_base.split('AI_Modul_10.')[1]
        mod_num = topic_suffix.split('_')[0]
        rest = '_'.join(topic_suffix.split('_')[1:])
        new_file = f"notebooks/part-10/AI_Modul_10.{mod_num}_Praktikum_{rest}.ipynb"
        
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        content = update_content(content)
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] notebook: {new_file}")

print("\nMigrating instructor_resources/part-09 to instructor_resources/part-10...")
for i in range(1, 8):
    old_file = f"instructor_resources/part-09/AI_Modul_9.{i}_Panduan_Instruktur_dan_Kunci_Solusi.md"
    new_file = f"instructor_resources/part-10/AI_Modul_10.{i}_Panduan_Instruktur_dan_Kunci_Solusi.md"
    if os.path.exists(old_file):
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        content = update_content(content)
        content = re.sub(r'# AI Modul 9\.\d:', f'# AI Modul 10.{i}:', content)
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] guide: {new_file}")

print("\nMigration to Part 10 complete!")
