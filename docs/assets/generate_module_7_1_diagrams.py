import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig_dir = r"e:\Project Buku\docs\assets"
art_dir = r"C:\Users\IT INSTIPER\.gemini\antigravity\brain\43a50d1c-c669-4c47-b939-d1e0efdbca11"

# ==============================================================================
# FIGURE 1: Anatomi Regresi Linier OLS vs Gradient Descent
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel 1: OLS & Residuals
np.random.seed(42)
x = np.linspace(10, 50, 25) # Pupuk NPK (kg/pokok/tahun)
y_true = 12 + 0.45 * x
noise = np.random.normal(0, 2.8, size=len(x))
y = y_true + noise # Produksi TBS (ton/ha)

# Fit OLS
beta1 = np.cov(x, y)[0, 1] / np.var(x)
beta0 = np.mean(y) - beta1 * np.mean(x)
y_pred = beta0 + beta1 * x

ax1.scatter(x, y, color='#1f77b4', s=60, edgecolors='k', zorder=4, label='Data Observasi Lapangan (TBS ton/ha)')
ax1.plot(x, y_pred, color='#d62728', linewidth=2.5, zorder=3, label=f'Garis Regresi OLS: $\\hat{{y}} = {beta0:.2f} + {beta1:.2f}x$')

# Draw residuals (errors)
for xi, yi, ypi in zip(x, y, y_pred):
    ax1.plot([xi, xi], [yi, ypi], color='#7f7f7f', linestyle='--', linewidth=1.2, zorder=2)

# Highlight one residual
sample_idx = 14
ax1.plot([x[sample_idx], x[sample_idx]], [y[sample_idx], y_pred[sample_idx]], color='#2ca02c', linewidth=2.5, zorder=5)
ax1.annotate(f'Residual $e_i = y_i - \\hat{{y}}_i$\n$= {y[sample_idx]:.2f} - {y_pred[sample_idx]:.2f} = {y[sample_idx]-y_pred[sample_idx]:+.2f}$',
             xy=(x[sample_idx], (y[sample_idx] + y_pred[sample_idx])/2),
             xytext=(x[sample_idx] - 12, (y[sample_idx] + y_pred[sample_idx])/2 + 4),
             arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=7),
             fontsize=10, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2ca02c'))

ax1.set_title('A. Prinsip Ordinary Least Squares (OLS)\nMinimasi Jumlah Kuadrat Residual (SSR)', fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel('Aplikasi Pupuk NPK Terstandar ($x$, kg/pokok)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Produktivitas TBS Kelapa Sawit ($y$, ton/ha)', fontsize=11, fontweight='bold')
ax1.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
ax1.grid(True, linestyle=':', alpha=0.6)

# Panel 2: Gradient Descent Contour on MSE Loss Surface
b0_vals = np.linspace(5, 19, 100)
b1_vals = np.linspace(0.2, 0.7, 100)
B0, B1 = np.meshgrid(b0_vals, b1_vals)
MSE = np.zeros_like(B0)

for i in range(len(b0_vals)):
    for j in range(len(b1_vals)):
        pred = b0_vals[i] + b1_vals[j] * x
        MSE[j, i] = np.mean((y - pred)**2)

contours = ax2.contour(B0, B1, MSE, levels=20, cmap='viridis_r', linewidths=1.2)
ax2.clabel(contours, inline=True, fontsize=8, fmt='%.1f')

# Simulate Gradient Descent steps
gd_b0 = [6.0]
gd_b1 = [0.25]
lr_b0 = 0.08
lr_b1 = 0.0001 # scaled for visualization
for _ in range(7):
    cur_b0 = gd_b0[-1]
    cur_b1 = gd_b1[-1]
    grad_b0 = -2 * np.mean(y - (cur_b0 + cur_b1 * x))
    grad_b1 = -2 * np.mean((y - (cur_b0 + cur_b1 * x)) * x)
    new_b0 = cur_b0 - 0.25 * grad_b0
    new_b1 = cur_b1 - 0.00015 * grad_b1
    gd_b0.append(new_b0)
    gd_b1.append(new_b1)

ax2.plot(gd_b0, gd_b1, marker='o', color='#d62728', markersize=6, linewidth=2, linestyle='-', zorder=5, label='Lintasan Gradient Descent')
ax2.scatter([beta0], [beta1], color='#2ca02c', s=160, marker='*', zorder=6, label=f'Titik Minimum Global $(\\beta_0={beta0:.2f}, \\beta_1={beta1:.2f})$')

# Annotate initial point
ax2.annotate('Titik Inisiasi\n$(\\beta_0^{(0)}, \\beta_1^{(0)})$', xy=(gd_b0[0], gd_b1[0]), xytext=(gd_b0[0]+1.5, gd_b1[0]-0.03),
             arrowprops=dict(facecolor='#d62728', shrink=0.08, width=1.5, headwidth=6),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', edgecolor='#d62728'))

ax2.set_title('B. Optimasi Kontur Permukaan Rugi MSE\nKonvergensi Gradien Menuju Solusi Optimal', fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel('Intercept ($\\beta_0$)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Slope / Kemiringan ($\\beta_1$)', fontsize=11, fontweight='bold')
ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig1_path = os.path.join(fig_dir, "anatomi_regresi_linier_ols_dan_gradient_descent.png")
fig.savefig(fig1_path, dpi=300)
plt.close(fig)
shutil.copy(fig1_path, os.path.join(art_dir, "anatomi_regresi_linier_ols_dan_gradient_descent.png"))
print(f"[OK] Generated {fig1_path}")


# ==============================================================================
# FIGURE 2: Diagnostik Asumsi Klasik Gauss-Markov
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(15, 12), dpi=300)

residuals = y - y_pred
std_residuals = (residuals - np.mean(residuals)) / np.std(residuals)

# Subplot 1: Residuals vs Fitted (Linearity & Homoscedasticity)
ax = axes[0, 0]
ax.scatter(y_pred, residuals, color='#1f77b4', edgecolors='k', s=50, alpha=0.8)
ax.axhline(0, color='#d62728', linestyle='--', linewidth=1.8)
# Add loess-like smoothing line
sort_idx = np.argsort(y_pred)
ax.plot(y_pred[sort_idx], np.convolve(residuals[sort_idx], np.ones(5)/5, mode='same'), color='#2ca02c', linewidth=2, label='Tren Rerata Residual')
ax.set_title('A. Residual vs Nilai Prediksi (Fitted Values)\nEvaluasi Linearitas & Homoskedastisitas', fontsize=11, fontweight='bold')
ax.set_xlabel('Nilai Prediksi $\\hat{y}$ (Produksi TBS ton/ha)', fontsize=10, fontweight='bold')
ax.set_ylabel('Residual $e_i = y_i - \\hat{y}_i$', fontsize=10, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='lower right', frameon=True)

# Subplot 2: Normal Q-Q Plot
ax = axes[0, 1]
from scipy import stats
sorted_std_res = np.sort(std_residuals)
theoretical_quantiles = stats.norm.ppf((np.arange(1, len(x) + 1) - 0.5) / len(x))
ax.scatter(theoretical_quantiles, sorted_std_res, color='#9467bd', edgecolors='k', s=50, alpha=0.8)
# 45-degree line
q_line = np.linspace(-2.5, 2.5, 50)
ax.plot(q_line, q_line, color='#d62728', linestyle='--', linewidth=1.8, label='Garis Distribusi Teoretis Normal')
ax.set_title('B. Normal Q-Q Plot\nEvaluasi Normalitas Distribusi Galat (Error Term)', fontsize=11, fontweight='bold')
ax.set_xlabel('Kuantil Teoretis Standar Normal $\\mathcal{N}(0, 1)$', fontsize=10, fontweight='bold')
ax.set_ylabel('Kuantil Sampel Residual Standar', fontsize=10, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', frameon=True)

# Subplot 3: Scale-Location Plot (Square root of standardized residuals vs Fitted)
ax = axes[1, 0]
sqrt_abs_res = np.sqrt(np.abs(std_residuals))
ax.scatter(y_pred, sqrt_abs_res, color='#ff7f0e', edgecolors='k', s=50, alpha=0.8)
ax.plot(y_pred[sort_idx], np.convolve(sqrt_abs_res[sort_idx], np.ones(5)/5, mode='same'), color='#d62728', linewidth=2, label='Tren Dispersi Varians')
ax.set_title('C. Scale-Location Plot\nUji Ketat Homoskedastisitas (Konstansi Varians Galat)', fontsize=11, fontweight='bold')
ax.set_xlabel('Nilai Prediksi $\\hat{y}$ (Produksi TBS ton/ha)', fontsize=10, fontweight='bold')
ax.set_ylabel('$\\sqrt{|\\text{Standardized Residuals}|}$', fontsize=10, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right', frameon=True)

# Subplot 4: Residuals vs Leverage / Cook's Distance
ax = axes[1, 1]
# Compute leverage: H = X(X^T X)^-1 X^T
X_mat = np.column_stack([np.ones_like(x), x])
H = X_mat @ np.linalg.inv(X_mat.T @ X_mat) @ X_mat.T
leverage = np.diag(H)
# Cook's distance: D_i = (e_i^2 / (p * MSE)) * (h_ii / (1 - h_ii)^2)
mse_val = np.mean(residuals**2)
p_param = 2
cooks_d = (residuals**2 / (p_param * mse_val)) * (leverage / (1 - leverage)**2)

ax.stem(range(1, len(x) + 1), cooks_d, linefmt='b-', markerfmt='bo', basefmt='r-')
cook_thresh = 4 / len(x)
ax.axhline(cook_thresh, color='#d62728', linestyle='--', linewidth=1.8, label=f'Ambang Batas Pengaruh Kritis ($4/n = {cook_thresh:.3f}$)')
ax.set_title("D. Jarak Pengaruh Cook (Cook's Distance)\nDeteksi Titik Pengungkit Berpengaruh Ekstrem (Outliers/Leverage)", fontsize=11, fontweight='bold')
ax.set_xlabel('Indeks Observasi Sampel Blok Kebun', fontsize=10, fontweight='bold')
ax.set_ylabel("Cook's Distance ($D_i$)", fontsize=10, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right', frameon=True)

plt.tight_layout()
fig2_path = os.path.join(fig_dir, "diagnostik_asumsi_klasik_gauss_markov.png")
fig.savefig(fig2_path, dpi=300)
plt.close(fig)
shutil.copy(fig2_path, os.path.join(art_dir, "diagnostik_asumsi_klasik_gauss_markov.png"))
print(f"[OK] Generated {fig2_path}")
