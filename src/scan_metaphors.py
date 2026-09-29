import glob
import os
import re

files = sorted(glob.glob('docs/part-*/*.md'))

METAPHORS = [
    r'\bbayi yang buta\b', r'\bbayi buta\b', r'\bkotak hitam\b', r'\bmenghirup\b',
    r'\bmenelan\b', r'\bmelahap\b', r'\bbernafas\b', r'\bbernyawa\b', r'\broh\b',
    r'\bjiwa\b', r'\bsetan\b', r'\biblis\b', r'\bhantu\b', r'\bmonster\b',
    r'\bkeajaiban\b', r'\bkesaktian\b', r'\bsakti\b', r'\bmustajab\b',
    r'\bmandraguna\b', r'\bjawara\b', r'\bpawang\b', r'\bdukun\b',
    r'\bmeraba-raba\b', r'\bbuta arah\b', r'\bbuta huruf\b',
    r'\btangan dingin\b', r'\bkaki tangan\b', r'\bberdarah dingin\b'
]

results3 = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        
    for l_idx, line in enumerate(lines, 1):
        line_clean = line.strip()
        if line_clean.startswith('```') or line_clean.startswith('http') or line_clean.startswith('data:'):
            continue
            
        for pat in METAPHORS:
            m = re.search(pat, line, re.I)
            if m:
                matched_word = m.group(0)
                # Ignore legitimate 'kotak hitam' (black box in AI is standard if paired with 'black-box' or XAI)
                if matched_word.lower() == 'kotak hitam':
                    continue
                results3.append((f, l_idx, matched_word, line_clean))

print(f'Total findings (Metaphors): {len(results3)}')
for f, l_idx, w, ctx in results3:
    print(f'  • {os.path.basename(f)}:{l_idx} [{w}] -> {ctx[:130]}')
