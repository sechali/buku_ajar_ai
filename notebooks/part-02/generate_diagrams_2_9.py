import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os, shutil

os.makedirs('docs/assets', exist_ok=True)
artifact_dir = r'C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11'

# ==========================================
# DIAGRAM 1: Taksonomi Struktur Data Dasar Python & Arsitektur Memori
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=300)
fig.patch.set_facecolor('#F8FAFC')

def draw_box(ax, x, y, w, h, text, bg, border, shape='round', text_col='#0F172A', fs=8.5):
    if shape == 'round':
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.3', facecolor=bg, edgecolor=border, lw=1.5)
        ax.add_patch(rect)
    else:
        rect = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, lw=1.5)
        ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=text_col)

# Panel 1: Taksonomi 4 Struktur Data Dasar
ax1.set_facecolor('#FFFFFF')
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 100)
ax1.axis('off')
ax1.set_title('Taksonomi Koleksi Data Fundamental Python', fontsize=11, fontweight='bold', color='#1E293B', pad=10)

draw_box(ax1, 5, 75, 42, 18, 'LIST (Larik Dinamis Mutabel)\n- Urutan terindeks (Sequence)\n- Mutabel (bisa diubah)\n- Izinkan elemen duplikat\n- Akses indeks: O(1) | Cari: O(N)', '#DBEAFE', '#2563EB', fs=8.0)
draw_box(ax1, 53, 75, 42, 18, 'TUPLE (Larik Statis Imutabel)\n- Urutan terindeks (Sequence)\n- Imutabel (bersifat konstan)\n- Konsumsi RAM lebih hemat\n- Akses indeks: O(1) | Hashable', '#EDE9FE', '#7C3AED', fs=8.0)
draw_box(ax1, 5, 48, 42, 18, 'DICTIONARY (Pemetaan Kunci-Nilai)\n- Struktur Asosiatif (Key-Value)\n- Kunci unik & harus hashable\n- Nilai bisa bertipe apa pun\n- Akses/Cari via Kunci: O(1)', '#FEF08A', '#CA8A04', fs=8.0)
draw_box(ax1, 53, 48, 42, 18, 'SET (Himpunan Unik Tanpa Urutan)\n- Elemen unik (deduplikasi)\n- Berbasis Hash Table\n- Operasi: Irisan, Gabungan, Selisih\n- Uji Keanggotaan (in): O(1)', '#DCFCE7', '#16A34A', fs=8.0)

# Ringkasan Matriks Kompleksitas
draw_box(ax1, 5, 8, 90, 32, 'Matriks Kompleksitas Asimptotik Big-O Operasi Utama:\n'
                           '--------------------------------------------------------------------------\n'
                           'Operasi            | List (Larik)   | Tuple (Imutabel) | Dict (Hash)    | Set (Hash)\n'
                           '--------------------------------------------------------------------------\n'
                           'Akses Indeks [i]   | O(1) konstan   | O(1) konstan     | N/A            | N/A\n'
                           'Pencarian Nilai    | O(N) linier    | O(N) linier      | O(1) rata-rata | O(1) rata-rata\n'
                           'Penyisipan Elemen  | O(1)* append   | N/A (Imutabel)   | O(1) rata-rata | O(1) rata-rata\n'
                           'Penghapusan        | O(N) pergeseran| N/A (Imutabel)   | O(1) rata-rata | O(1) rata-rata',
         '#F1F5F9', '#475569', fs=7.8)

# Panel 2: Model Memori Fisik CPython (Larik Kontigu vs Hash Table)
ax2.set_facecolor('#F8FAFC')
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
ax2.axis('off')
ax2.set_title('Arsitektur Memori: Larik Kontigu vs Hash Table (Open Addressing)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)

# Model 1: List (Contiguous Pointer Array)
draw_box(ax2, 5, 80, 90, 14, '1. Struktur Memori List & Tuple (Larik Pointer Kontigu):\n'
                           '[Slot 0: Pointer] -> [Objek Nilai A di Heap]\n'
                           '[Slot 1: Pointer] -> [Objek Nilai B di Heap]\n'
                           '[Slot 2: Pointer] -> [Objek Nilai C di Heap]\n'
                           'Karakteristik: Alamat memori pointer berurutan -> Indeks dihitung instan O(1)',
         '#EFF6FF', '#2563EB', fs=8.0)

# Model 2: Dict & Set (Hash Table dengan Bucket Array)
draw_box(ax2, 5, 30, 90, 42, '2. Struktur Memori Dict & Set (Tabel Hash Compact):\n'
                           'Kunci Masukan (cth: "BLOK_A") -> Fungsi Hash: hash("BLOK_A") % Ukuran_Tabel\n'
                           '                   |\n'
                           '                   v\n'
                           'Indeks Hash Bucket -> [hash_val, pointer_key, pointer_value]\n'
                           '--------------------------------------------------------------------------\n'
                           'Keunggulan: Tidak perlu iterasi linier untuk mencari data.\n'
                           'Pencarian kunci melompat langsung ke slot indeks hasil hash O(1).\n'
                           'Resolusi Tabrakan (Collision): Python menggunakan Perturbation Open Addressing.',
         '#FEF9C3', '#CA8A04', fs=8.0)

draw_box(ax2, 5, 5, 90, 18, 'Rekomendasi Pemilihan Struktur Data:\n'
                          '- Gunakan List jika urutan data berindeks penting (data deret waktu sensor).\n'
                          '- Gunakan Tuple untuk pasangan koordinat/data konstan yang aman dari perubahan.\n'
                          '- Gunakan Dict untuk relasi kunci-nilai dan pencarian data berbasis ID entitas.\n'
                          '- Gunakan Set untuk operasi deduplikasi data dan uji keanggotaan cepat.',
         '#F0FDF4', '#15803D', fs=7.8)

plt.tight_layout()
p1 = 'docs/assets/taksonomi_struktur_data_dasar_python.png'
plt.savefig(p1, dpi=300)
shutil.copy(p1, os.path.join(artifact_dir, 'taksonomi_struktur_data_dasar_python.png'))
plt.close()

# ==========================================
# DIAGRAM 2: Pipeline Agregasi Mahadata Panen Sawit
# ==========================================
fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#F8FAFC')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 96, 'Pipeline Agregasi Mahadata Panen Kelapa Sawit Menggunakan Struktur Data Heterogen',
        fontsize=12, fontweight='bold', ha='center', color='#0F172A')

# Stage 1: Raw Records (List of Tuples)
draw_box(ax, 5, 75, 42, 14, '1. Rekaman Log Panen Mentah (List of Tuples):\n'
                          '[("PMR-01", "BLOK-A", 18.5, "2026-09-28"),\n'
                          ' ("PMR-02", "BLOK-B", 14.2, "2026-09-28"),\n'
                          ' ("PMR-01", "BLOK-A", 22.0, "2026-09-28")]', '#E0F2FE', '#0284C7', fs=7.8)

# Stage 2: Deduplikasi & Verifikasi (Set)
draw_box(ax, 53, 75, 42, 14, '2. Deduplikasi Pemanen Aktif (Set):\n'
                          'pemanen_aktif = {"PMR-01", "PMR-02"}\n'
                          'Pemeriksaan registrasi legalitas tenaga kerja\n'
                          'Kompleksitas keanggotaan: O(1) konstan', '#DCFCE7', '#16A34A', fs=7.8)

ax.annotate('', xy=(53, 82), xytext=(47, 82), arrowprops=dict(arrowstyle='->', lw=1.5, color='#0284C7'))

# Stage 3: Agregasi Tabular (Dict of Lists)
draw_box(ax, 15, 45, 70, 18, '3. Agregasi Tabular Produksi per Blok (Nested Dictionary & List):\n'
                           'agregasi_blok = {\n'
                           '  "BLOK-A": {"total_berat_kg": 40.5, "jumlah_janjang": 2, "daftar_pemanen": {"PMR-01"}},\n'
                           '  "BLOK-B": {"total_berat_kg": 14.2, "jumlah_janjang": 1, "daftar_pemanen": {"PMR-02"}}\n'
                           '}', '#FEF3C7', '#D97706', fs=8.2)

ax.annotate('', xy=(35, 63), xytext=(26, 75), arrowprops=dict(arrowstyle='->', lw=1.5, color='#0284C7'))
ax.annotate('', xy=(65, 63), xytext=(74, 75), arrowprops=dict(arrowstyle='->', lw=1.5, color='#16A34A'))

# Stage 4: Transformasi Comprehension Menuju Vektor Fitur AI
draw_box(ax, 10, 12, 80, 22, '4. Transformasi Fitur Cerdas (Comprehension Expressions):\n'
                           'rata_rata_berat = {k: v["total_berat_kg"] / v["jumlah_janjang"] for k, v in agregasi_blok.items()}\n'
                           'blok_prioritas = [b for b, v in agregasi_blok.items() if v["total_berat_kg"] > 30.0]\n'
                           '--> Luaran: Vektor Tensor Fitur untuk Model Prediksi Hasil Panen & Estimasi Ritase Truk',
         '#EDE9FE', '#7C3AED', fs=8.2)

ax.annotate('', xy=(50, 34), xytext=(50, 45), arrowprops=dict(arrowstyle='->', lw=1.5, color='#7C3AED'))

plt.tight_layout()
p2 = 'docs/assets/pipeline_agregasi_data_panen_sawit.png'
plt.savefig(p2, dpi=300)
shutil.copy(p2, os.path.join(artifact_dir, 'pipeline_agregasi_data_panen_sawit.png'))
plt.close()

print('[SUKSES] Dua aset visual 300 DPI Modul 2.9 berhasil dibuat!')
