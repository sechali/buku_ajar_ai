import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=300)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

# Box positions and text
boxes = [
    {"x": 0.5, "y": 4.5, "w": 3.6, "h": 1.8, "title": "1. Perumusan Masalah & Scoping", 
     "sub": "- Identifikasi ROI & Sasaran Bisnis\n- Translasi Metrik Bisnis ke Metrik AI\n- Kelayakan Data & Kendala Komputasi", "color": "#1f77b4"},
    {"x": 5.0, "y": 4.5, "w": 3.6, "h": 1.8, "title": "2. Rekayasa & Kurasi Data", 
     "sub": "- Data Ingestion & Schema Check\n- Data Cleaning & Outlier Imputation\n- Pencegahan Data Leakage Kritis", "color": "#2ca02c"},
    {"x": 9.5, "y": 4.5, "w": 3.8, "h": 1.8, "title": "3. EDA & Feature Engineering", 
     "sub": "- Korelasi & Analisis Variansi (VIF)\n- Ekstraksi Sinyal Domain Kebun/Pabrik\n- Transformasi Skala & Pipeline Fitur", "color": "#ff7f0e"},
    {"x": 9.5, "y": 1.0, "w": 3.8, "h": 1.8, "title": "4. Pelatihan & Validasi Model", 
     "sub": "- Stratified K-Fold Cross-Validation\n- Hyperparameter Tuning (Optuna/Grid)\n- Regularisasi L1/L2 & Early Stopping", "color": "#d62728"},
    {"x": 5.0, "y": 1.0, "w": 3.6, "h": 1.8, "title": "5. Audit Evaluasi Holistik", 
     "sub": "- Metrik Teknis (RMSE, F-beta, ROC)\n- Analisis Residual & Kasus Gagal\n- Uji Ketahanan & Audit Bias Etika", "color": "#9467bd"},
    {"x": 0.5, "y": 1.0, "w": 3.6, "h": 1.8, "title": "6. MLOps Deployment & Monitoring", 
     "sub": "- Model Packaging (Joblib/ONNX/API)\n- Serving di Edge Drone atau Cloud Server\n- Monitoring Drift (PSI) & Retraining Loop", "color": "#8c564b"}
]

for b in boxes:
    # Draw fancy rounded rectangle
    rect = patches.FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"], boxstyle="round,pad=0.2",
                                  facecolor=b["color"], alpha=0.15, edgecolor=b["color"], linewidth=2)
    ax.add_patch(rect)
    
    # Title
    ax.text(b["x"] + b["w"]/2, b["y"] + b["h"] - 0.35, b["title"], 
            fontsize=10.5, fontweight='bold', ha='center', va='center', color=b["color"])
    
    # Subtext
    ax.text(b["x"] + 0.2, b["y"] + b["h"]/2 - 0.25, b["sub"], 
            fontsize=8.5, ha='left', va='center', color='#222222', linespacing=1.4)

# Arrows
arrow_style = dict(arrowstyle="->", color="#333333", lw=2, mutation_scale=15)
feedback_style = dict(arrowstyle="->", color="#d62728", lw=1.8, linestyle="--", mutation_scale=15)

# Forward flow
ax.annotate("", xy=(5.0, 5.4), xytext=(4.1, 5.4), arrowprops=arrow_style)
ax.annotate("", xy=(9.5, 5.4), xytext=(8.6, 5.4), arrowprops=arrow_style)
ax.annotate("", xy=(11.4, 2.8), xytext=(11.4, 4.5), arrowprops=arrow_style)
ax.annotate("", xy=(8.6, 1.9), xytext=(9.5, 1.9), arrowprops=arrow_style)
ax.annotate("", xy=(4.1, 1.9), xytext=(5.0, 1.9), arrowprops=arrow_style)

# Feedback Loops
# From Phase 5 back to Phase 4 (Retrain / Change Algorithm)
ax.annotate("Audit Gagal:\nTuning Ulang Model", xy=(9.5, 2.3), xytext=(8.6, 2.3),
            arrowprops=feedback_style, fontsize=8, color="#d62728", fontweight='bold', ha='center')

# From Phase 6 back to Phase 2 (Data Drift Detected -> Collect New Data & Retrain Pipeline)
ax.annotate("", xy=(0.8, 4.5), xytext=(0.8, 2.8), arrowprops=feedback_style)
ax.text(0.9, 3.65, "Monitoring Mendeteksi Drift (PSI > 0.25):\nUmpan Balik Pengumpulan Data Baru & Retraining Otomatis", 
        fontsize=8.5, color="#d62728", fontweight='bold', va='center')

ax.set_title("Siklus Hidup Terpadu Rekayasa Proyek AI (End-to-End MLOps Lifecycle)", 
             fontsize=13, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(r"e:\Project Buku\docs\assets\ai_project_lifecycle_workflow.png", dpi=300, bbox_inches='tight')
plt.close()
print("AI Project Lifecycle diagram generated successfully.")
