import os

replacements = [
    ('docs/part-07/AI_Modul_7.5_Random_Forest.md',
     'menjalankan ratusan struktur pohon dapat menguras baterai dan memori.',
     'menjalankan ratusan struktur pohon dapat menghabiskan daya baterai dan membebani alokasi memori secara signifikan.'),
    ('docs/part-11/AI_Modul_11.9_Real-time_camera_processing.md',
     'Multi-threading menguras antrean ini secara terus-menerus',
     'Multi-threading mengosongkan antrean penyangga (*buffer flushing*) ini secara terus-menerus'),
    ('docs/part-01/AI_Modul_1.7_Etika_dalam_Penggunaan_AI.md',
     'molekul racun kimia baru, termasuk varian-varian yang secara teoritis jauh lebih mematikan daripada racun saraf gas VX dan sarin.',
     'molekul senyawa toksik kimia baru, termasuk varian-varian yang secara teoritis berpotensi jauh lebih mematikan daripada senyawa neurotoksik gas VX dan sarin.'),
    ('docs/part-02/AI_Modul_2.8_Fungsi_dalam_Pemrograman.md',
     'akan terjerumus ke dalam bentuk **prosedur monolitik**',
     'akan berkembang menjadi bentuk **prosedur monolitik**'),
    ('docs/part-05/AI_Modul_5.3_Dataset_Training_dan_Testing.md',
     'mencapai skor determinasi fantastis $R^2 = 0.994$',
     'mencapai skor determinasi semu yang over-optimistik sebesar $R^2 = 0.994$'),
    ('docs/part-09/AI_Modul_9.5_Loss_Function.md',
     'trik *Log-Sum-Exp*',
     'metode numerik *Log-Sum-Exp*')
]

for p, old, new in replacements:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if old in c:
        c = c.replace(old, new)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Successfully replaced in {p}")
    else:
        print(f"ERROR: String not found in {p}")
