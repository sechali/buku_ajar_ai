import glob
import os

for folder in ['docs', 'instructor_resources', 'slides']:
    files = glob.glob(f'{folder}/**/*.md', recursive=True)
    count = 0
    matched_files = []
    for f in files:
        c = open(f, encoding='utf-8', errors='ignore').read().lower()
        if 'jebakan' in c:
            count += c.count('jebakan')
            matched_files.append(f)
    print(f'{folder}: {count} occurrences in {len(matched_files)} files')
