import glob
import os
import re

files = sorted(glob.glob('docs/part-*/*.md'))

# Extended list of non-academic / informal / colloquial / sensational words
WORDS_TO_CHECK = [
    # Slang & Colloquial
    r'\bnggak\b', r'\bgak\b', r'\bbanget\b', r'\bkayak\b', r'\bkayaknya\b',
    r'\bbikin\b', r'\bnyari\b', r'\bngitung\b', r'\bngeliat\b', r'\bnemu\b',
    r'\bdapet\b', r'\bpake\b', r'\bngatur\b', r'\bngubah\b', r'\bkalo\b',
    r'\bkarna\b', r'\btrus\b', r'\babis\b', r'\bcuma\b', r'\baja\b',
    r'\bgitu\b', r'\bbeneran\b', r'\bcepet\b', r'\bpelan\b', r'\bdong\b',
    r'\bdeh\b', r'\byuk\b', r'\bkok\b', r'\bloh\b', r'\bnih\b', r'\btuh\b',
    r'\babal-abal\b', r'\bkaleng-kaleng\b', r'\breceh\b', r'\brecehan\b',
    r'\bcuan\b', r'\bboncos\b', r'\bbuntung\b', r'\bjagoan\b', r'\bgacoan\b',
    r'\botak-atik\b', r'\bmengotak-atik\b', r'\bngotot\b', r'\becek-ecek\b',
    
    # Sensational / Hyperbolic / Metaphorical
    r'\bmalapetaka\b', r'\bsihir\b', r'\bmagis\b', r'\bsenjata pamungkas\b',
    r'\bpeluru perak\b', r'\bcawan suci\b', r'\bjampi-jampi\b', r'\bujug-ujug\b',
    r'\bkeblinger\b', r'\bhuru-hara\b', r'\bmoncer\b', r'\btokcer\b', r'\bnendang\b',
    r'\bkece\b', r'\bkeren\b', r'\bgahar\b', r'\bbuas\b', r'\bdewa\b',
    r'\bdapur pacu\b', r'\btipu-tipu\b', r'\bgembar-gembor\b', r'\bkelabakan\b',
    r'\bketar-ketir\b', r'\bkalang kabut\b', r'\bkacau balau\b', r'\bamburadul\b',
    r'\bmorat-marit\b', r'\bmati kutu\b', r'\bgigit jari\b', r'\bbiang kerok\b',
    r'\bbiang keladi\b', r'\bkambing hitam\b', r'\bangin segar\b', r'\bangin surga\b',
    r'\bjebakan betmen\b', r'\bbongkar pasang\b', r'\btelan mentah-mentah\b',
    r'\bbuta huruf visual\b', r'\bjurus\b', r'\bcontekan\b', r'\btrik\b',
    r'\bbombastis\b', r'\bfantastis\b', r'\bmisterius\b', r'\bajaib\b',
    r'\bmenyeramkan\b', r'\bangker\b', r'\bmonster\b', r'\bhantu\b',
    r'\bracun\b', r'\bmeroket\b', r'\bterjun bebas\b', r'\bmenukik tajam\b',
    r'\bmenggila\b', r'\bmencekik\b', r'\bmenguras\b', r'\bbabak belur\b',
    r'\bjungkir balik\b', r'\bhancur lebur\b', r'\bmati-matian\b',
    r'\bterjengkang\b', r'\btersungkur\b', r'\bterjerumus\b'
]

# Exceptions to ignore
EXCEPTIONS = [
    'gini',       # Gini impurity
    'dong, w.',   # Author name
    'weidong',    # Author name
    'dong',       # When followed by author or in references
    'racun tanaman', # Scientific context (phytotoxin / pest poison)
    'racun',      # Toxicological science in agro
]

results = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        
    fname = os.path.basename(f)
    pdir = os.path.basename(os.path.dirname(f))
    
    for l_idx, line in enumerate(lines, 1):
        line_clean = line.strip()
        if line_clean.startswith('```') or line_clean.startswith('http') or line_clean.startswith('data:'):
            continue
            
        for pat in WORDS_TO_CHECK:
            m = re.search(pat, line, re.I)
            if m:
                matched_word = m.group(0)
                # Check exceptions
                w_low = matched_word.lower()
                if w_low == 'gini':
                    continue
                if w_low == 'dong' and ('feifei' in line.lower() or 'deng' in line.lower() or 'imagenet' in line.lower()):
                    continue
                if w_low == 'trik' and 'kernel trick' in line.lower():
                    continue # Kernel trick is a legitimate mathematical concept in SVM!
                if w_low == 'racun' and any(bio in line.lower() for bio in ['hama', 'pestisida', 'toksin', 'tanaman', 'ulat']):
                    continue
                    
                results.append((f, l_idx, matched_word, line_clean))

print(f'Total findings: {len(results)}\n')

by_word = {}
for f, l_idx, w, ctx in results:
    w_l = w.lower()
    by_word.setdefault(w_l, []).append((os.path.basename(f), l_idx, ctx))

for w, occurrences in sorted(by_word.items(), key=lambda x: len(x[1]), reverse=True):
    print(f'=== KATA: "{w}" ({len(occurrences)} kali) ===')
    for fn, l_no, ctx in occurrences[:5]:
        print(f'  • {fn}:{l_no}')
        print(f'    Konteks: {ctx[:130]}...')
    if len(occurrences) > 5:
        print(f'    ... dan {len(occurrences)-5} lokasi lainnya.')
    print()
