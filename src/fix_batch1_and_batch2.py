# Fix batch 2 inner docstrings
with open('src/build_part12_batch2.py', 'r', encoding='utf-8') as f:
    text2 = f.read()

s1 = '"""\n    Membangun model Transfer Learning berbasis ResNet-18 Pretrained.\n    """'
r1 = "'''\n    Membangun model Transfer Learning berbasis ResNet-18 Pretrained.\n    '''"
s2 = '"""\n    Membangun optimizer AdamW dengan 3 kelompok laju pembelajaran bertingkat.\n    """'
r2 = "'''\n    Membangun optimizer AdamW dengan 3 kelompok laju pembelajaran bertingkat.\n    '''"

text2 = text2.replace(s1, r1).replace(s2, r2)
with open('src/build_part12_batch2.py', 'w', encoding='utf-8') as f:
    f.write(text2)
print("Fixed batch 2!")

# Fix batch 1 variable shadowing
with open('src/build_part12_batch1.py', 'r', encoding='utf-8') as f:
    text1 = f.read()

text1 = text1.replace("N, C_in, H, W = X.shape", "N, C_in, H_in, W_in = X.shape")
text1 = text1.replace("H - Kh", "H_in - Kh")
text1 = text1.replace("W - Kw", "W_in - Kw")

with open('src/build_part12_batch1.py', 'w', encoding='utf-8') as f:
    f.write(text1)
print("Fixed batch 1 variable shadowing!")
