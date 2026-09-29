with open('src/build_part12_batch1.py', 'r', encoding='utf-8') as f:
    text = f.read()

s1 = '"""\n    Implementasi konvolusi 2D murni berbasis NumPy untuk verifikasi matematis.\n    X: Input array dimensi (N, C_in, H, W)\n    W: Kernel weights dimensi (C_out, C_in, Kh, Kw)\n    b: Bias array dimensi (C_out,)\n    """'
r1 = "'''\n    Implementasi konvolusi 2D murni berbasis NumPy untuk verifikasi matematis.\n    X: Input array dimensi (N, C_in, H, W)\n    W: Kernel weights dimensi (C_out, C_in, Kh, Kw)\n    b: Bias array dimensi (C_out,)\n    '''"

s2 = '"""\n    Arsitektur CNN Standar Industri untuk Deteksi Patologi Daun Bibit Kelapa Sawit.\n    """'
r2 = "'''\n    Arsitektur CNN Standar Industri untuk Deteksi Patologi Daun Bibit Kelapa Sawit.\n    '''"

for s, r in [(s1, r1), (s2, r2)]:
    if s in text:
        text = text.replace(s, r)
        print(f"Replaced {s[:30]}...")
    else:
        print(f"NOT FOUND: {s[:30]}...")

with open('src/build_part12_batch1.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done fixing batch 1!")
