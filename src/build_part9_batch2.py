import os
import json
import re

BANNED_WORDS = ['taksonomi', 'tripartit', 'ontologis', 'epistemologis', 'dialektika', 'manifestasi dependensi', 'de facto']

def validate_text(text, filename):
    lower = text.lower()
    for w in BANNED_WORDS:
        if w in lower:
            raise ValueError(f"BANNED WORD FOUND in {filename}: '{w}'")
    print(f"[VALIDATED] 0 banned words in {filename}")

def build_batch2():
    batch_map = [
        {
            "old_idx": 2,
            "new_idx": 4,
            "topic": "Activation_Function",
            "title": "AI Modul 9.4: Activation Function",
            "code": "AI-09-04",
            "prereq": "AI Modul 9.3 (Struktur Neuron)",
            "bridging": "AI Modul 9.5: Loss Function",
            "image": "../assets/kurva_dan_gradien_fungsi_aktivasi_deep_learning.png",
            "image_caption": "Kurva dan Gradien Fungsi Aktivasi Deep Learning"
        },
        {
            "old_idx": 3,
            "new_idx": 5,
            "topic": "Loss_Function",
            "title": "AI Modul 9.5: Loss Function",
            "code": "AI-09-05",
            "prereq": "AI Modul 9.4 (Activation Function)",
            "bridging": "AI Modul 9.6: Backpropagation",
            "image": "../assets/anatomi_loss_functions_dan_learning_rate.png",
            "image_caption": "Anatomi Loss Functions dan Learning Rate"
        },
        {
            "old_idx": 4,
            "new_idx": 6,
            "topic": "Backpropagation",
            "title": "AI Modul 9.6: Backpropagation",
            "code": "AI-09-06",
            "prereq": "AI Modul 9.5 (Loss Function)",
            "bridging": "AI Modul 9.7: Training Neural Network",
            "image": "../assets/arsitektur_aliran_mundur_backpropagation_dan_vektor_delta.png",
            "image_caption": "Arsitektur Aliran Mundur Backpropagation dan Vektor Delta"
        }
    ]

    for item in batch_map:
        old_i = item["old_idx"]
        new_i = item["new_idx"]
        topic = item["topic"]
        
        # 1. Diktat Markdown
        src_md_pattern = f"staging_dl/AI_Modul_8.{old_i}_*.md"
        import glob
        src_md_files = [f for f in glob.glob(src_md_pattern) if not f.endswith("Panduan_Instruktur_dan_Kunci_Solusi.md")]
        with open(src_md_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update title & headers
        content = re.sub(r'^# AI Modul 8\.\d+:.*$', f'# {item["title"]}', content, flags=re.MULTILINE)
        content = re.sub(r'\* \*\*Kode Modul\*\*: AI-08-\d+', f'* **Kode Modul**: {item["code"]}', content)
        content = re.sub(r'\* \*\*Prasyarat\*\*:.*$', f'* **Prasyarat**: {item["prereq"]}', content, flags=re.MULTILINE)
        content = re.sub(rf'Sub-CPMK 8\.{old_i}\.', f'Sub-CPMK 9.{new_i}.', content)
        content = re.sub(r'AI-08-0\d', item["code"], content)
        content = re.sub(r'AI-08-\d\d', item["code"], content)
        content = re.sub(r'AI-09-0\d', item["code"], content)
        content = re.sub(r'AI-09-\d\d', item["code"], content)
        content = re.sub(r'## 9\. Jembatan Konsep \(Bridging\).*$', f'## 9. Jembatan Konsep (Bridging) ke {item["bridging"]}', content, flags=re.MULTILINE)
        
        # Ensure image is present
        img_tag = f"![{item['image_caption']}]({item['image']})"
        if item['image'] not in content:
            # Insert after Section 3 heading
            content = re.sub(r'(## 3\..*\n+)', r'\1' + img_tag + '\n\n', content, count=1)
            
        # Clean any accidental banned words
        # (check and fix if any)
        out_md_path = f"docs/part-09/AI_Modul_9.{new_i}_{topic}.md"
        validate_text(content, out_md_path)
        with open(out_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Generated {out_md_path}")
        
        # 2. Notebook
        src_nb_files = glob.glob(f"staging_dl/AI_Modul_8.{old_i}_*.ipynb")
        with open(src_nb_files[0], 'r', encoding='utf-8') as f:
            nb = json.load(f)
            
        nb_str = json.dumps(nb)
        nb_str = nb_str.replace(f"Modul 8.{old_i}", f"Modul 9.{new_i}")
        nb_str = nb_str.replace(f"AI-08-0{old_i}", item["code"])
        nb_str = nb_str.replace(f"AI-08-{old_i:02d}", item["code"])
        if old_i == 2:
            nb_str = nb_str.replace("Praktikum Fungsi Aktivasi & Arsitektur MLP", "Praktikum Activation Function")
        elif old_i == 3:
            nb_str = nb_str.replace("Praktikum Forward Propagation & Loss Functions", "Praktikum Loss Function")
        elif old_i == 4:
            nb_str = nb_str.replace("Praktikum Backpropagation & Aturan Rantai", "Praktikum Backpropagation")
            
        out_nb_path = f"notebooks/part-09/AI_Modul_9.{new_i}_Praktikum_{topic}.ipynb"
        with open(out_nb_path, 'w', encoding='utf-8') as f:
            f.write(nb_str)
        print(f"[OK] Generated {out_nb_path}")
        
        # 3. Instructor Guide
        src_g_files = glob.glob(f"staging_dl/AI_Modul_8.{old_i}_Panduan_Instruktur_dan_Kunci_Solusi.md")
        with open(src_g_files[0], 'r', encoding='utf-8') as f:
            guide = f.read()
            
        guide = re.sub(r'^# AI Modul 8\.\d+:', f'# AI Modul 9.{new_i}:', guide, flags=re.MULTILINE)
        guide = guide.replace(f"AI-08-0{old_i}", item["code"])
        guide = guide.replace(f"AI-08-{old_i:02d}", item["code"])
        guide = guide.replace(f"Modul 8.{old_i}", f"Modul 9.{new_i}")
        out_g_path = f"instructor_resources/part-09/AI_Modul_9.{new_i}_Panduan_Instruktur_dan_Kunci_Solusi.md"
        validate_text(guide, out_g_path)
        with open(out_g_path, 'w', encoding='utf-8') as f:
            f.write(guide)
        print(f"[OK] Generated {out_g_path}")

if __name__ == '__main__':
    build_batch2()
