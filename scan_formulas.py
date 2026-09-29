import os
import glob
import re

md_files = glob.glob('docs/**/*.md', recursive=True)
md_files = [f for f in md_files if 'part-' in f]

print("=== DAFTAR MODUL DENGAN RUMUS MATEMATIKA ===")
for f in sorted(md_files):
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    blocks = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)
    # also search for specific inline patterns like f: \mathcal{P} or \in \mathbb{R}
    inlines = [m for m in re.findall(r'\$([^\$\n]+)\$', content) if any(k in m for k in ['\\mathcal', '\\sum', '\\frac', '\\in \\mathbb', '\\nabla', 'f:', '\\le', '\\ge'])]
    
    if blocks or inlines:
        print(f"{f}: {len(blocks)} block math, {len(inlines)} significant inline math")
