import glob, os, re

parts = ['part-01', 'part-02', 'part-03', 'part-04', 'part-05', 'part-06']
total_modified = 0

for p in parts:
    files = sorted(glob.glob(f'docs/{p}/*.md'))
    for f in files:
        text = open(f, encoding='utf-8').read()
        
        # Regex to find reference header: e.g. ## 11. Daftar Pustaka, ## 9. Referensi Akademik, ## 9. Referensi Ilmiah Terstandar, etc.
        pattern_header = r'(##\s*\d+\.\s*)(?:Daftar Pustaka dan Referensi Akademik|Daftar Pustaka|Referensi Akademik|Referensi Ilmiah Terstandar)'
        match = re.search(pattern_header, text)
        
        if not match:
            print(f"[WARN] No reference header found in {f}")
            continue
            
        header_start = match.start()
        prefix_number = match.group(1) # e.g. "## 12. "
        new_header = f"{prefix_number}Daftar Pustaka dan Referensi Akademik"
        
        # Split text before reference section and reference section itself
        pre_ref = text[:header_start]
        ref_section = text[header_start:]
        
        # Replace the header line
        ref_section = re.sub(pattern_header, new_header, ref_section, count=1)
        
        # Unbold author names in reference entries:
        # Matches: 1. **Author Name.** (Year) or 1. **Author Name** (Year)
        # We replace **Author Name** with Author Name
        def unbold_authors(m):
            num = m.group(1) # e.g. "1. "
            authors = m.group(2) # e.g. "Van Rossum, G., & Drake, F. L."
            rest = m.group(3) # e.g. " (2009)..."
            return f"{num}{authors}{rest}"

        ref_section = re.sub(r'(^\s*\d+\.\s*)\*\*([^*]+)\*\*\s*(\([12]\d{3}[^)]*\))', unbold_authors, ref_section, flags=re.MULTILINE)
        
        # Also clean any weird double periods like "ANSI/ISO.. (1985)" if any
        ref_section = re.sub(r'\.\.\s*\(', '. (', ref_section)

        new_text = pre_ref + ref_section
        if new_text != text:
            open(f, 'w', encoding='utf-8').write(new_text)
            total_modified += 1
            print(f"[OK] Standardized references in {f}")
        else:
            print(f"[SKIP] Already standard: {f}")

print(f"\nCompleted! Total files updated: {total_modified} of {sum(len(glob.glob(f'docs/{p}/*.md')) for p in parts)}.")
