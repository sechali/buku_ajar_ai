import glob
import os
import json
import re

REPO_OWNER = "sechali"
REPO_NAME = "buku_ajar_ai"
BRANCH = "main"

files = sorted(glob.glob('notebooks/part-*/*.ipynb'))
print(f"Menginjeksi badge Google Colab 1-Klik ke {len(files)} berkas notebook...")
print(f"Target Repositori: https://github.com/{REPO_OWNER}/{REPO_NAME} (Branch: {BRANCH})\n")

success_count = 0

for f in files:
    fname = os.path.basename(f)
    pdir = os.path.basename(os.path.dirname(f))
    
    with open(f, 'r', encoding='utf-8') as fp:
        try:
            nb = json.load(fp)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue

    colab_url = f"https://colab.research.google.com/github/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH}/notebooks/{pdir}/{fname}"
    badge_html = f'<a href="{colab_url}" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>\n\n'

    cells = nb.get('cells', [])
    if not cells:
        continue

    cell0 = cells[0]
    
    if cell0.get('cell_type') == 'markdown':
        src_lines = cell0.get('source', [])
        src_text = "".join(src_lines)
        
        # Check if colab badge already exists in cell 0
        if 'colab.research.google.com' in src_text:
            # Replace existing badge pattern
            cleaned_text = re.sub(
                r'<a\s+href=[\"\']https://colab\.research\.google\.com[^\"]*[\"\'][^>]*>.*?</a>\s*\n*',
                '',
                src_text,
                flags=re.DOTALL | re.IGNORECASE
            )
            cleaned_text = re.sub(
                r'\[\!\[Open In Colab\]\(.*?\)\]\(https://colab\.research\.google\.com[^\)]*\)\s*\n*',
                '',
                cleaned_text,
                flags=re.DOTALL | re.IGNORECASE
            )
            new_text = badge_html + cleaned_text.lstrip()
            # Split back into lines preserving formatting
            cell0['source'] = [line + '\n' for line in new_text.splitlines()[:-1]] + ([new_text.splitlines()[-1]] if new_text.splitlines() else [])
        else:
            new_text = badge_html + src_text
            cell0['source'] = [line + '\n' for line in new_text.splitlines()[:-1]] + ([new_text.splitlines()[-1]] if new_text.splitlines() else [])
    else:
        # Cell 0 is a code cell, create new markdown cell at index 0
        new_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [badge_html.strip()]
        }
        cells.insert(0, new_cell)

    with open(f, 'w', encoding='utf-8') as fp:
        json.dump(nb, fp, indent=1, ensure_ascii=False)
        fp.write('\n')
        
    success_count += 1

print(f"BERHASIL: {success_count} / {len(files)} notebook telah dilengkapi dengan badge deep link Google Colab!")
