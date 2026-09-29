import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = sorted(glob.glob('docs/part-*/*.md'))

ENGLISH_IDIOMS = [
    r'\bsilver bullet\b', r'\bholy grail\b', r'\brule of thumb\b',
    r'\bquick and dirty\b', r'\bhacky\b', r'\bworkaround\b',
    r'\bno-brainer\b', r'\bballpark\b', r'\bgame changer\b',
    r'\bbottom line\b', r'\bcut corner\b', r'\btouch and go\b'
]

results5 = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        
    for l_idx, line in enumerate(lines, 1):
        line_clean = line.strip()
        if line_clean.startswith('```') or line_clean.startswith('http') or line_clean.startswith('data:'):
            continue
            
        for pat in ENGLISH_IDIOMS:
            m = re.search(pat, line, re.I)
            if m:
                results5.append((f, l_idx, m.group(0), line_clean))

print(f'Total findings (English Idioms): {len(results5)}')
for f, l_idx, w, ctx in results5:
    clean_ctx = ctx.encode('ascii', 'replace').decode('ascii')
    print(f'  • {os.path.basename(f)}:{l_idx} [{w}] -> {clean_ctx[:130]}')
