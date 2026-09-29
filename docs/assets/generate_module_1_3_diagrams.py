import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 1. Diagram Venn Hierarkis AI vs ML vs DL
fig, ax = plt.subplots(figsize=(8, 7), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 9)
ax.axis('off')

# Outer: Artificial Intelligence
circle_ai = patches.Circle((5, 4.5), 4.2, facecolor='#EBF5FB', edgecolor='#2980B9', linewidth=2.5)
# Middle: Machine Learning
circle_ml = patches.Circle((5, 3.8), 2.9, facecolor='#D5F5E3', edgecolor='#27AE60', linewidth=2.5)
# Inner: Deep Learning
circle_dl = patches.Circle((5, 3.0), 1.6, facecolor='#FADBD8', edgecolor='#C0392B', linewidth=2.5)

ax.add_patch(circle_ai)
ax.add_patch(circle_ml)
ax.add_patch(circle_dl)

# Labels and descriptions
ax.text(5, 8.1, 'ARTIFICIAL INTELLIGENCE (AI)', ha='center', va='center', fontsize=12, fontweight='bold', color='#1B4F72')
ax.text(5, 7.3, 'Teknik apa pun yang memungkinkan mesin meniru kecerdasan manusia\n(Sistem Pakar, Logika Fuzzy, Algoritma Genetika, A* Search)', 
        ha='center', va='center', fontsize=8, color='#2874A6')

ax.text(5, 5.8, 'MACHINE LEARNING (ML)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1E8449')
ax.text(5, 5.0, 'Metode statistik & optimasi yang belajar dari data tanpa diprogram eksplisit\n(Regresi Linier, SVM, Random Forest, K-Means, XGBoost)', 
        ha='center', va='center', fontsize=7.5, color='#229954')

ax.text(5, 3.3, 'DEEP LEARNING (DL)', ha='center', va='center', fontsize=10, fontweight='bold', color='#922B21')
ax.text(5, 2.4, 'Jaringan Syaraf Tiruan Multi-Lapis\nEkstraksi Fitur Otomatis End-to-End\n(CNN, RNN/LSTM, Transformer, GAN)', 
        ha='center', va='center', fontsize=7.5, color='#B03A2E')

plt.title('Hubungan Taksonomi Hierarkis: AI vs Machine Learning vs Deep Learning', fontsize=12, fontweight='bold', pad=15, color='#2C3E50')
plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/venn_ai_ml_dl.png', dpi=300)
plt.close()


# 2. Kurva Skalabilitas Performa vs Volume Data (Andrew Ng Hypothesis)
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)

data_volume = np.linspace(1, 100, 200)

# Kurva Tradisional ML: cepat bagus di awal, lalu jenuh (plateau)
traditional_ml = 1.0 - 0.7 * np.exp(-0.06 * data_volume)
# Kurva Deep Learning: butuh data awal lebih banyak, tapi terus meningkat seiring data masif
deep_learning = 1.05 / (1.0 + np.exp(-0.04 * (data_volume - 30)))

ax.plot(data_volume, traditional_ml, label='Machine Learning Klasik (SVM, Random Forest, Regresi)', color='#2980B9', linewidth=2.5)
ax.plot(data_volume, deep_learning, label='Deep Learning Berkapasitas Besar (CNN, Transformer)', color='#C0392B', linewidth=3)

# Garis ambang batas kejenuhan
ax.axhline(0.85, color='#2980B9', linestyle=':', alpha=0.6)
ax.text(70, 0.81, 'Titik Kejenuhan Model Klasik (Plateau)', fontsize=8, color='#2980B9', fontweight='bold')

ax.set_title('Dinamika Performa Algoritma terhadap Volume Data (Data Scaling Curve)', fontsize=11, fontweight='bold', pad=12, color='#2C3E50')
ax.set_xlabel('Volume Data Latih (Jumlah Sampel / Skala Data)', fontsize=10)
ax.set_ylabel('Performa / Akurasi Prediksi Model', fontsize=10)
ax.set_xlim(0, 100)
ax.set_ylim(0.2, 1.1)
ax.legend(fontsize=9, loc='lower right')
ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/kurva_skalabilitas_data.png', dpi=300)
plt.close()


# 3. Diagram Alur Pipeline Fitur: ML Tradisional vs Deep Learning
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6), dpi=300)

for ax in [ax1, ax2]:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    ax.axis('off')

# Panel A: Traditional ML Pipeline
ax1.set_title('(A) Alur Kerja Machine Learning Tradisional: Rekayasa Fitur Manual oleh Manusia', fontsize=10, fontweight='bold', pad=8, color='#1A5276')

b1_data = patches.FancyBboxPatch((0.5, 0.8), 1.8, 1.8, boxstyle='round,pad=0.1', facecolor='#D6EAF8', edgecolor='#2980B9', lw=1.5)
b1_feat = patches.FancyBboxPatch((2.8, 0.8), 2.2, 1.8, boxstyle='round,pad=0.1', facecolor='#FCF3CF', edgecolor='#F39C12', lw=1.5)
b1_model = patches.FancyBboxPatch((5.5, 0.8), 2.0, 1.8, boxstyle='round,pad=0.1', facecolor='#D5F5E3', edgecolor='#27AE60', lw=1.5)
b1_out = patches.FancyBboxPatch((8.0, 0.8), 1.5, 1.8, boxstyle='round,pad=0.1', facecolor='#EAECEE', edgecolor='#7F8C8D', lw=1.5)

for b in [b1_data, b1_feat, b1_model, b1_out]: ax1.add_patch(b)

ax1.text(1.4, 1.7, 'DATA MENTAH\n(Citra Daun,\nSinyal Suara)', ha='center', va='center', fontweight='bold', fontsize=8)
ax1.text(3.9, 1.7, 'REKAYASA FITUR MANUAL\n(Pakar Ekstraksi Warna,\nTekstur GLCM, Tepi)', ha='center', va='center', fontweight='bold', fontsize=7.5, color='#7D6608')
ax1.text(6.5, 1.7, 'MODEL KLASIK\n(SVM, Decision Tree,\nLogistic Regression)', ha='center', va='center', fontweight='bold', fontsize=8, color='#196F3D')
ax1.text(8.75, 1.7, 'OUTPUT\n(Klasifikasi\nKelas)', ha='center', va='center', fontweight='bold', fontsize=8)

ax1.annotate('', xy=(2.7, 1.7), xytext=(2.4, 1.7), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax1.annotate('', xy=(5.4, 1.7), xytext=(5.1, 1.7), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax1.annotate('', xy=(7.9, 1.7), xytext=(7.6, 1.7), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))


# Panel B: Deep Learning Pipeline
ax2.set_title('(B) Alur Kerja Deep Learning: Pembelajaran Fitur & Klasifikasi End-to-End Otomatis', fontsize=10, fontweight='bold', pad=8, color='#78281F')

b2_data = patches.FancyBboxPatch((0.5, 0.8), 1.8, 1.8, boxstyle='round,pad=0.1', facecolor='#D6EAF8', edgecolor='#2980B9', lw=1.5)
b2_dl = patches.FancyBboxPatch((2.8, 0.8), 4.7, 1.8, boxstyle='round,pad=0.15', facecolor='#FADBD8', edgecolor='#C0392B', lw=2)
b2_out = patches.FancyBboxPatch((8.0, 0.8), 1.5, 1.8, boxstyle='round,pad=0.1', facecolor='#EAECEE', edgecolor='#7F8C8D', lw=1.5)

for b in [b2_data, b2_dl, b2_out]: ax2.add_patch(b)

ax2.text(1.4, 1.7, 'DATA MENTAH\n(Piksel Citra Langsung\nTanpa Pre-processing)', ha='center', va='center', fontweight='bold', fontsize=8)
ax2.text(5.15, 2.1, 'JARINGAN SYARAF MENDALAM (DEEP NEURAL NETWORK)', ha='center', va='center', fontweight='bold', fontsize=8.5, color='#922B21')
ax2.text(5.15, 1.3, '[Ekstraksi Fitur Hierarkis Otomatis: Garis -> Tekstur -> Bagian Objek] + [Klasifikasi]', 
         ha='center', va='center', fontsize=7.5, color='#78281F')
ax2.text(8.75, 1.7, 'OUTPUT\n(Klasifikasi\nKelas)', ha='center', va='center', fontweight='bold', fontsize=8)

ax2.annotate('', xy=(2.7, 1.7), xytext=(2.4, 1.7), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))
ax2.annotate('', xy=(7.9, 1.7), xytext=(7.6, 1.7), arrowprops=dict(facecolor='#333', width=1.5, headwidth=6))

plt.tight_layout()
plt.savefig('e:/Project Buku/docs/assets/pipeline_fitur_ml_vs_dl.png', dpi=300)
plt.close()

print('All 3 diagrams for AI Modul 1.3 generated successfully!')
