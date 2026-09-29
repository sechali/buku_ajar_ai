import glob
import os
import re

files = sorted(glob.glob('docs/part-*/*.md'))

MORE_WORDS = [
    r'\botak-atik\b', r'\bmengotak-atik\b', r'\bdiotak-atik\b',
    r'\bcontekan\b', r'\bjurus\b', r'\bngeles\b', r'\bakal-akalan\b',
    r'\becek-ecek\b', r'\biseng\b', r'\bkacau\b', r'\bbikin pusing\b',
    r'\bdinosaurus\b', r'\bujung tanduk\b', r'\bkambing hitam\b',
    r'\bbiang kerok\b', r'\bsenjata rahasia\b', r'\brahasia dapur\b',
    r'\bcoba-coba\b', r'\bmati rasa\b', r'\bbabak baru\b',
    r'\bcuap-cuap\b', r'\bkoar-koar\b', r'\bgembar-gembor\b',
    r'\btergila-gila\b', r'\bmelejit\b', r'\bmoncer\b', r'\bjawara\b',
    r'\bkesasar\b', r'\bkeblinger\b', r'\bngeri\b', r'\bseram\b',
    r'\bheboh\b', r'\bvital\b'
]

results2 = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        
    for l_idx, line in enumerate(lines, 1):
        line_clean = line.strip()
        if line_clean.startswith('```') or line_clean.startswith('http') or line_clean.startswith('data:'):
            continue
            
        for pat in MORE_WORDS:
            m = re.search(pat, line, re.I)
            if m:
                matched_word = m.group(0)
                w_low = matched_word.lower()
                # filter out false positives if any
                if w_low == 'vital' and 'organ vital' in line.lower():
                    continue
                results2.append((f, l_idx, matched_word, line_clean))

print(f'Total findings (Set 2): {len(results2)}')
by_word2 = {}
for f, l_idx, w, ctx in results2:
    w_l = w.lower()
    by_word2.setdefault(w_l, []).append((os.path.basename(f), l_idx, ctx))

for w, occurrences in sorted(by_word2.items(), key=lambda x: len(x[1]), reverse=True):
    print(f'=== KATA: "{w}" ({len(occurrences)} kali) ===')
    for fn, l_no, ctx in occurrences[:3]:
        print(f'  • {fn}:{l_no} -> {ctx[:120]}...')
