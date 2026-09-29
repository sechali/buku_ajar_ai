import glob
import os
import re

files = sorted(glob.glob('docs/part-*/*.md'))

MORE_METAPHORS = [
    r'\bdahsyat\b', r'\bhebat\b', r'\bsangar\b', r'\bgila\b',
    r'\bbukan main\b', r'\bbatu loncatan\b', r'\banak emas\b', r'\banak tiri\b',
    r'\bnaik daun\b', r'\bbanting setir\b', r'\bpontang-panting\b',
    r'\bmembabi buta\b', r'\bjungkir balik\b', r'\blumer\b', r'\bmeleleh\b',
    r'\bhancur\b', r'\bremuk\b', r'\bambrol\b', r'\bjebol\b', r'\bambles\b',
    r'\bamblas\b', r'\bludes\b', r'\blenyap tanpa jejak\b', r'\bsapu bersih\b'
]

results4 = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        
    for l_idx, line in enumerate(lines, 1):
        line_clean = line.strip()
        if line_clean.startswith('```') or line_clean.startswith('http') or line_clean.startswith('data:'):
            continue
            
        for pat in MORE_METAPHORS:
            m = re.search(pat, line, re.I)
            if m:
                results4.append((f, l_idx, m.group(0), line_clean))

print(f'Total findings (Set 4): {len(results4)}')
for f, l_idx, w, ctx in results4:
    print(f'  • {os.path.basename(f)}:{l_idx} [{w}] -> {ctx[:130]}')
