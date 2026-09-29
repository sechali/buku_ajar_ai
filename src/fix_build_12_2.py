with open('src/build_part12_12_2_and_12_3.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the 4 inner docstring pairs
s1 = '"""\n    Blok Residual Dasar (BasicBlock) untuk ResNet-18 dan ResNet-34.\n    """'
r1 = "'''\n    Blok Residual Dasar (BasicBlock) untuk ResNet-18 dan ResNet-34.\n    '''"
s2 = '"""\n    Arsitektur ResNet-18 yang Dioptimasi untuk Klasifikasi Kematangan Buah Sawit.\n    """'
r2 = "'''\n    Arsitektur ResNet-18 yang Dioptimasi untuk Klasifikasi Kematangan Buah Sawit.\n    '''"
s3 = '"""\n    Implementasi Max Pooling 2D manual dengan NumPy.\n    X: Input tensor dimensi (N, C, H, W)\n    """'
r3 = "'''\n    Implementasi Max Pooling 2D manual dengan NumPy.\n    X: Input tensor dimensi (N, C, H, W)\n    '''"
s4 = '"""\n    Ekstraktor Fitur Standar Industri Menggunakan Global Average Pooling.\n    """'
r4 = "'''\n    Ekstraktor Fitur Standar Industri Menggunakan Global Average Pooling.\n    '''"

for s, r in [(s1, r1), (s2, r2), (s3, r3), (s4, r4)]:
    if s in text:
        text = text.replace(s, r)
        print(f"Replaced {s[:30]}...")
    else:
        print(f"NOT FOUND: {s[:30]}...")

with open('src/build_part12_12_2_and_12_3.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done fixing builder!")
