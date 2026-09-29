import glob
import re

files = sorted(glob.glob("docs/**/*.md", recursive=True))
files = [f for f in files if "part-" in f]

missing_guide = []
for f in files:
    with open(f, "r", encoding="utf-8") as fp:
        content = fp.read()
    
    blocks = re.findall(r"\$\$(.*?)\$\$", content, re.DOTALL)
    has = any(k in content.lower() for k in ["cara baca", "cara membaca", "panduan membaca", "panduan pelafalan"])
    
    if len(blocks) > 0 and not has:
        missing_guide.append((f, len(blocks)))

print(f"Total modul dengan rumus tanpa panduan membaca: {len(missing_guide)}")
for path, count in missing_guide:
    print(f" - {path} ({count} blok rumus)")
