import os
import re

replacements = [
    ('docs/part-07/AI_Modul_7.5_Random_Forest.md',
     'daya komputasi yang menguras sumber daya',
     'kapasitas komputasi yang intensif'),
    ('docs/part-11/AI_Modul_11.9_Real-time_camera_processing.md',
     'menguras penumpukan frame lama',
     'mengosongkan penumpukan frame lama (*buffer flushing*)'),
    ('docs/part-01/AI_Modul_1.7_Etika_dalam_Penggunaan_AI.md',
     'merancang racun biokimia mematikan',
     'merancang senyawa toksik biokimia berbahaya'),
    ('docs/part-02/AI_Modul_2.8_Fungsi_dalam_Pemrograman.md',
     'terjerumus ke dalam kode spageti',
     'berkembang menjadi struktur kode spageti (*spaghetti code*)'),
    ('docs/part-05/AI_Modul_5.3_Dataset_Training_dan_Testing.md',
     'performa fantastis dengan akurasi',
     'performa semu yang over-optimistik dengan akurasi'),
    ('docs/part-08/AI_Modul_8.4_Interpretasi_Hasil_Model.md',
     'kotak hitam yang misterius',
     'entitas kotak hitam yang tidak terjelaskan (*opaque black-box*)'),
    ('docs/part-09/AI_Modul_9.5_Loss_Function.md',
     'dengan trik stabilisasi',
     'dengan teknik stabilisasi numerik')
]

for filepath, target, repl in replacements:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            c = f.read()
        if target in c:
            c = c.replace(target, repl)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Polished: {filepath}")
        else:
            print(f"Target not found in {filepath}: {target}")

print("Done polishing final words!")
