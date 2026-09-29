import glob
import os
import json
import re

files = sorted(glob.glob('notebooks/part-*/*.ipynb'))
print(f'Checking {len(files)} notebooks for Colab integration...\n')

has_badge = 0
generic_colab = 0
specific_colab = 0
missing_badge = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        try:
            nb = json.load(fp)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue

    fname = os.path.basename(f)
    found_in_nb = False
    colab_url = ""

    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            src = "".join(cell.get('source', []))
            if 'colab.research.google.com' in src:
                found_in_nb = True
                m = re.search(r'href=[\"\'](https://colab\.research\.google\.com[^\"]*)[\"\']', src)
                if not m:
                    m = re.search(r'\[\!\[Open In Colab\]\(.*?\)\]\((https://colab\.research\.google\.com[^\)]*)\)', src)
                if m:
                    colab_url = m.group(1)
                break

    if found_in_nb:
        has_badge += 1
        if colab_url == "https://colab.research.google.com/" or colab_url == "https://colab.research.google.com":
            generic_colab += 1
        else:
            specific_colab += 1
    else:
        missing_badge.append(f)

print(f"Total Notebooks: {len(files)}")
print(f"Notebooks with Colab badge: {has_badge} / {len(files)}")
print(f"  - Generic URL (https://colab.research.google.com/): {generic_colab}")
print(f"  - Specific Deep Link URL: {specific_colab}")
print(f"Notebooks missing Colab badge: {len(missing_badge)}")
if missing_badge:
    print("\nMissing badge notebooks:")
    for mb in missing_badge[:5]:
        print(f"  • {mb}")
    if len(missing_badge) > 5:
        print(f"  ... and {len(missing_badge)-5} more.")
