import glob
import os
import subprocess

docs = sorted(glob.glob('docs/part-10/*.md'))
guides = sorted(glob.glob('instructor_resources/part-10/*.md'))

print(f"Compiling {len(docs)} diktats and {len(guides)} guides to DOCX in docx/part-10...")

for d in docs:
    base = os.path.basename(d).replace('.md', '.docx')
    target = f'docx/part-10/{base}'
    print(f"Compiling: {d} -> {target}")
    res = subprocess.run(['python', 'src/convert_md_to_docx.py', d, target], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error compiling {d}: {res.stderr}")

for g in guides:
    base = os.path.basename(g).replace('.md', '.docx')
    target = f'docx/part-10/{base}'
    print(f"Compiling: {g} -> {target}")
    res = subprocess.run(['python', 'src/convert_md_to_docx.py', g, target], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error compiling {g}: {res.stderr}")

print("All Part 10 DOCX files compiled successfully!")
