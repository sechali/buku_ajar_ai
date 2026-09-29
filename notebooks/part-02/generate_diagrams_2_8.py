import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os, shutil

os.makedirs('docs/assets', exist_ok=True)
artifact_dir = r'C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11'

# ==========================================
# DIAGRAM 1: Anatomi Fungsi & Resolusi Lingkup LEGB
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=300)
fig.patch.set_facecolor('#F8FAFC')

# Helper function
def draw_node(ax, x, y, w, h, text, bg, border, shape='round', text_col='#0F172A', fs=8.5):
    if shape == 'round':
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.3', facecolor=bg, edgecolor=border, lw=1.5)
        ax.add_patch(rect)
    else:
        rect = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, lw=1.5)
        ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=text_col)

# Panel 1: Anatomi Tanda Tangan Fungsi (Function Signature & Parameters)
ax1.set_facecolor('#F1F5F9')
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 100)
ax1.axis('off')
ax1.set_title('Anatomi Fungsi Python: Parameter, Argumen Fleksibel & Type Hinting', fontsize=11, fontweight='bold', color='#1E293B', pad=10)

code_snippet = (
    "def kalkulasi_dobi(\n"
    "    absorbansi_446nm: float,          # Positional-or-Keyword\n"
    "    absorbansi_269nm: float,          # Type Hinted float\n"
    "    faktor_koreksi: float = 1.0,      # Default Parameter\n"
    "    *argumen_tambahan: float,         # Variable Positional (*args)\n"
    "    **metadata_sensor: str            # Variable Keyword (**kwargs)\n"
    ") -> Tuple[float, str]:              # Return Type Annotation\n"
    "    '''Menghitung rasio DOBI (Deterioration of Bleachability Index).'''\n"
    "    # Tubuh Fungsi (Function Body)\n"
    "    rasio = (absorbansi_446nm / absorbansi_269nm) * faktor_koreksi\n"
    "    status = 'PRIMA' if rasio >= 3.0 else 'TERDEGRADASI'\n"
    "    return rasio, status              # Return Statement\n"
)
ax1.text(0.05, 0.95, code_snippet, fontfamily='monospace', fontsize=8.8, va='top', ha='left',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFFFFF', edgecolor='#3B82F6', lw=1.5))

draw_node(ax1, 5, 20, 28, 12, 'Parameter Standar:\n- Wajib diisi\n- Tipe data teranotasi', '#DBEAFE', '#2563EB', fs=8.0)
draw_node(ax1, 36, 20, 28, 12, 'Default Parameter:\n- Opsional (ada default)\n- Diletakkan di belakang', '#FEF08A', '#CA8A04', fs=8.0)
draw_node(ax1, 67, 20, 28, 12, 'Variabel (*args, **kwargs):\n- *args -> tuple parameter\n- **kwargs -> dict parameter', '#DCFCE7', '#16A34A', fs=8.0)
draw_node(ax1, 10, 4, 80, 11, 'Kaidah Utama: Parameter posisional harus selalu mendahului default parameter dan variadic args', '#EDE9FE', '#7C3AED', fs=8.5)

# Panel 2: Hierarki Ruang Lingkup LEGB (Local, Enclosing, Global, Built-in)
ax2.set_facecolor('#FFFFFF')
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
ax2.axis('off')
ax2.set_title('Resolusi Ruang Lingkup Variabel: Aturan LEGB Python', fontsize=11, fontweight='bold', color='#1E293B', pad=10)

# Built-in (Outer)
b_rect = patches.FancyBboxPatch((5, 5), 90, 88, boxstyle='round,pad=0.5', facecolor='#EFF6FF', edgecolor='#1D4ED8', lw=2)
ax2.add_patch(b_rect)
ax2.text(10, 88, 'B - Built-in Scope (Pustaka Inti Python: len, sum, range, abs, ValueError)', fontsize=8.5, fontweight='bold', color='#1E40AF')

# Global
g_rect = patches.FancyBboxPatch((12, 12), 76, 70, boxstyle='round,pad=0.5', facecolor='#F0FDF4', edgecolor='#15803D', lw=2)
ax2.add_patch(g_rect)
ax2.text(17, 76, 'G - Global Scope (Variabel Tingkat Modul / File: KONSTANTA_PKS = 0.85)', fontsize=8.5, fontweight='bold', color='#166534')

# Enclosing
e_rect = patches.FancyBboxPatch((20, 20), 60, 50, boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#B45309', lw=2)
ax2.add_patch(e_rect)
ax2.text(25, 64, 'E - Enclosing Scope (Fungsi Pembungkus / Outer Closure)', fontsize=8.5, fontweight='bold', color='#92400E')

# Local
l_rect = patches.FancyBboxPatch((28, 28), 44, 30, boxstyle='round,pad=0.5', facecolor='#FEE2E2', edgecolor='#B91C1C', lw=2)
ax2.add_patch(l_rect)
ax2.text(32, 51, 'L - Local Scope', fontsize=9, fontweight='bold', color='#991B1B')
ax2.text(50, 38, 'Variabel lokal di dalam fungsi:\nx, rasio, status\n(Dihapus saat fungsi selesai)', ha='center', fontsize=8, color='#7F1D1D')

# Panah resolusi
ax2.annotate('Arah Pencarian Variabel (L -> E -> G -> B)', xy=(50, 83), xytext=(50, 60),
             arrowprops=dict(arrowstyle='->', lw=2, color='#475569'), fontsize=8.5, fontweight='bold', color='#475569', ha='center')

plt.tight_layout()
p1 = 'docs/assets/anatomi_fungsi_dan_lingkup_legb.png'
plt.savefig(p1, dpi=300)
shutil.copy(p1, os.path.join(artifact_dir, 'anatomi_fungsi_dan_lingkup_legb.png'))
plt.close()

# ==========================================
# DIAGRAM 2: Dekomposisi Modular Pipeline Uji Mutu CPO
# ==========================================
fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#F8FAFC')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 96, 'Dekomposisi Fungsional Modular Pipeline Analisis Mutu Crude Palm Oil (CPO)',
        fontsize=12, fontweight='bold', ha='center', color='#0F172A')

# Input Raw
draw_node(ax, 35, 84, 30, 8, 'DATA TELEMETRI LABORATORIUM CPO\n(Absorbansi Spektro, Titrasi FFA, Kadar Air)', '#E2E8F0', '#475569', fs=8.5)

# Level 1: 3 Pure Functions
draw_node(ax, 5, 60, 26, 12, 'Fungsi Murni 1:\nhitung_kadar_ffa(\n  vol_titran, normalitas, berat)\n-> % Asam Lemak Bebas', '#DBEAFE', '#2563EB', fs=8.0)
draw_node(ax, 37, 60, 26, 12, 'Fungsi Murni 2:\nhitung_kadar_air(\n  berat_basah, berat_kering)\n-> % Moisture Content', '#DCFCE7', '#16A34A', fs=8.0)
draw_node(ax, 69, 60, 26, 12, 'Fungsi Murni 3:\nhitung_indeks_dobi(\n  abs_446nm, abs_269nm)\n-> Nilai Rasio DOBI', '#FEF08A', '#CA8A04', fs=8.0)

ax.annotate('', xy=(18, 72), xytext=(45, 84), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2563EB'))
ax.annotate('', xy=(50, 72), xytext=(50, 84), arrowprops=dict(arrowstyle='->', lw=1.5, color='#16A34A'))
ax.annotate('', xy=(82, 72), xytext=(55, 84), arrowprops=dict(arrowstyle='->', lw=1.5, color='#CA8A04'))

# Level 2: Evaluator Agregator
draw_node(ax, 25, 34, 50, 14, 'Fungsi Agregator Komposisi:\nevaluasi_kelayakan_ekspor_cpo(\n  ffa: float, air: float, dobi: float\n) -> LaporanKelayakanCPO\n(Aturan SNI 01-2901-2021 & Standar PORAM)', '#EDE9FE', '#7C3AED', fs=8.5)

ax.annotate('', xy=(40, 48), xytext=(18, 60), arrowprops=dict(arrowstyle='->', lw=1.5, color='#7C3AED'))
ax.annotate('', xy=(50, 48), xytext=(50, 60), arrowprops=dict(arrowstyle='->', lw=1.5, color='#7C3AED'))
ax.annotate('', xy=(60, 48), xytext=(82, 60), arrowprops=dict(arrowstyle='->', lw=1.5, color='#7C3AED'))

# Output Keputusan
draw_node(ax, 10, 10, 36, 12, 'Status Mutu: SUPER CPO EKSPOR\n(FFA < 3.0%, Air < 0.15%, DOBI >= 2.5)\nSertifikasi Pelabuhan Lolos Otomatis', '#DCFCE7', '#15803D', text_col='#14532D', fs=8.0)
draw_node(ax, 54, 10, 36, 12, 'Status Mutu: SUB-STANDAR / RE-REFINE\n(FFA >= 5.0% atau DOBI < 2.0)\nDisposisi ke Unit Pemurnian Fraksinasi', '#FEE2E2', '#DC2626', text_col='#991B1B', fs=8.0)

ax.annotate('Lolos Seluruh Batas', xy=(28, 22), xytext=(40, 34), arrowprops=dict(arrowstyle='->', lw=1.5, color='#15803D'), fontsize=8, fontweight='bold', color='#15803D')
ax.annotate('Melanggar Batas SNI', xy=(72, 22), xytext=(60, 34), arrowprops=dict(arrowstyle='->', lw=1.5, color='#DC2626'), fontsize=8, fontweight='bold', color='#DC2626')

plt.tight_layout()
p2 = 'docs/assets/dekomposisi_modular_pipeline_cpo.png'
plt.savefig(p2, dpi=300)
shutil.copy(p2, os.path.join(artifact_dir, 'dekomposisi_modular_pipeline_cpo.png'))
plt.close()

print('[SUKSES] Dua aset visual 300 DPI Modul 2.8 berhasil dibuat!')
