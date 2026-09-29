import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = sorted(glob.glob('docs/part-*/*.md'))

jebakan_findings = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    for l_no, line in enumerate(lines, 1):
        if 'jebakan' in line.lower():
            jebakan_findings.append((f, l_no, line.strip()))

print(f'Total occurrences of "jebakan": {len(jebakan_findings)}')

by_file = {}
for f, l_no, line in jebakan_findings:
    by_file.setdefault(os.path.basename(f), []).append((l_no, line))

print(f'Total files containing "jebakan": {len(by_file)}\n')

for fname, items in sorted(by_file.items()):
    print(f'=== {fname} ({len(items)} kali) ===')
    for l_no, line in items:
        # replace non-ascii chars to avoid terminal issues
        clean_line = line.encode('ascii', 'replace').decode('ascii')
        print(f'  [L{l_no}] {clean_line[:120]}')
    print()
