import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs('docs/assets', exist_ok=True)
dpi = 300

# -------------------------------------------------------------
# 1. arsitektur_dan_operasi_konvolusi_cnn.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

# Input Tensor
input_rect = patches.Rectangle((0.5, 1.5), 3, 4, linewidth=2, edgecolor='#1E88E5', facecolor='#BBDEFB', alpha=0.7)
ax.add_patch(input_rect)
ax.text(2.0, 3.5, "Input Citra\n$H \\times W \\times C$\n(e.g., $128 \\times 128 \\times 3$)", ha='center', va='center', fontsize=11, fontweight='bold', color='#0D47A1')

# Receptive field patch
rf_patch = patches.Rectangle((1.5, 3.2), 1.2, 1.2, linewidth=2, edgecolor='#D81B60', facecolor='#F8BBD0', linestyle='--')
ax.add_patch(rf_patch)
ax.text(2.1, 3.8, "$3 \\times 3$", ha='center', va='center', fontsize=9, fontweight='bold', color='#880E4F')

# Convolution operator arrow
ax.annotate("", xy=(5.0, 3.5), xytext=(3.7, 3.5), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))
ax.text(4.35, 4.0, "Operasi\nKonvolusi\n$\\ast$", ha='center', va='center', fontsize=10, fontweight='bold')

# Kernel Tensor
kernel_rect = patches.Rectangle((5.2, 2.3), 1.8, 2.4, linewidth=2, edgecolor='#43A047', facecolor='#C8E6C9', alpha=0.8)
ax.add_patch(kernel_rect)
ax.text(6.1, 3.5, "Kernel / Filter\n$K \\times K \\times C$\n($3 \\times 3 \\times 3$)\n+ Bias ($b$)", ha='center', va='center', fontsize=10, fontweight='bold', color='#1B5E20')

# Activation arrow
ax.annotate("", xy=(8.5, 3.5), xytext=(7.2, 3.5), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))
ax.text(7.85, 4.1, "Stride $S=1$\nPadding $P=1$\n+ ReLU", ha='center', va='center', fontsize=9, fontweight='bold')

# Feature Map Output
fmap_rect = patches.Rectangle((8.7, 1.8), 2.8, 3.4, linewidth=2, edgecolor='#FB8C00', facecolor='#FFE0B2', alpha=0.8)
ax.add_patch(fmap_rect)
ax.text(10.1, 3.5, "Feature Map\n$H_{out} \\times W_{out} \\times N_{filters}$\n($128 \\times 128 \\times 32$)", ha='center', va='center', fontsize=11, fontweight='bold', color='#E65100')

# Mathematical formula box
formula_box = patches.FancyBboxPatch((0.5, 0.3), 12.5, 0.9, boxstyle="round,pad=0.2", edgecolor='#78909C', facecolor='#ECEFF1')
ax.add_patch(formula_box)
ax.text(6.75, 0.75, r"$O(i, j) = \sigma \left( \sum_{c=1}^C \sum_{m=-k}^k \sum_{n=-k}^k I_c(i+m, j+n) \cdot K_c(m, n) + b \right) \quad \text{dimana } H_{out} = \left\lfloor \frac{H - K + 2P}{S} \right\rfloor + 1$", ha='center', va='center', fontsize=10, fontweight='bold', color='#263238')

plt.title("Arsitektur dan Operasi Konvolusi 2D pada Convolutional Neural Network (CNN)", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/arsitektur_dan_operasi_konvolusi_cnn.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 2. evolusi_arsitektur_cnn_lenet_vgg_resnet.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.5), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7.5)
ax.axis('off')

# LeNet-5 (1998)
lenet_box = patches.FancyBboxPatch((0.5, 4.5), 3.8, 2.4, boxstyle="round,pad=0.15", edgecolor='#1E88E5', facecolor='#E3F2FD', linewidth=1.8)
ax.add_patch(lenet_box)
ax.text(2.4, 6.5, "LeNet-5 (1998)", ha='center', va='center', fontsize=11, fontweight='bold', color='#0D47A1')
ax.text(2.4, 5.4, "• Input: 32x32 Grayscale\n• Conv 5x5 + AvgPool\n• FC Layers (Dense)\n• Aktivasi Sigmoid/Tanh\n• ~60K Parameter", ha='center', va='center', fontsize=9, color='#1565C0')

# AlexNet (2012)
alex_box = patches.FancyBboxPatch((4.9, 4.5), 4.1, 2.4, boxstyle="round,pad=0.15", edgecolor='#43A047', facecolor='#E8F5E9', linewidth=1.8)
ax.add_patch(alex_box)
ax.text(6.95, 6.5, "AlexNet (2012)", ha='center', va='center', fontsize=11, fontweight='bold', color='#1B5E20')
ax.text(6.95, 5.4, "• Input: 224x224x3 RGB\n• Conv 11x11, 5x5, 3x3 + ReLU\n• Dropout (0.5) & MaxPool\n• Komputasi GPU Acceleration\n• ~60M Parameter", ha='center', va='center', fontsize=9, color='#2E7D32')

# VGG-16 (2014)
vgg_box = patches.FancyBboxPatch((9.5, 4.5), 4.0, 2.4, boxstyle="round,pad=0.15", edgecolor='#8E24AA', facecolor='#F3E5F5', linewidth=1.8)
ax.add_patch(vgg_box)
ax.text(11.5, 6.5, "VGG-16 (2014)", ha='center', va='center', fontsize=11, fontweight='bold', color='#4A148C')
ax.text(11.5, 5.4, "• Stack 3x3 Conv homogen\n• 2 stacked 3x3 = 5x5 receptive\n• MaxPool downsampling 2x\n• Repetitif & modular\n• ~138M Parameter (Heavy FC)", ha='center', va='center', fontsize=9, color='#6A1B9A')

# ResNet (2015) - Deep Residual Learning
resnet_box = patches.FancyBboxPatch((0.5, 0.7), 13.0, 3.2, boxstyle="round,pad=0.2", edgecolor='#E53935', facecolor='#FFEBEE', linewidth=2.0)
ax.add_patch(resnet_box)
ax.text(7.0, 3.5, "ResNet (Residual Network - He et al., 2015) & Skip Connection", ha='center', va='center', fontsize=12, fontweight='bold', color='#B71C1C')

# Diagram Residual Block
res_in = patches.Rectangle((1.5, 1.3), 1.6, 1.4, edgecolor='#B71C1C', facecolor='#FFCDD2')
ax.add_patch(res_in)
ax.text(2.3, 2.0, "Input\n$x$", ha='center', va='center', fontsize=11, fontweight='bold')

ax.annotate("", xy=(4.0, 2.0), xytext=(3.1, 2.0), arrowprops=dict(arrowstyle="->", lw=2, color='#B71C1C'))

conv_blk = patches.Rectangle((4.0, 1.1), 2.6, 1.8, edgecolor='#B71C1C', facecolor='#EF9A9A')
ax.add_patch(conv_blk)
ax.text(5.3, 2.0, "Weight Layer\n(Conv 3x3 + BN + ReLU)\nWeight Layer\n(Conv 3x3 + BN)", ha='center', va='center', fontsize=8.5, fontweight='bold')

ax.annotate("", xy=(7.7, 2.0), xytext=(6.6, 2.0), arrowprops=dict(arrowstyle="->", lw=2, color='#B71C1C'))

add_circle = patches.Circle((8.1, 2.0), 0.4, edgecolor='#B71C1C', facecolor='#FFCDD2', linewidth=2)
ax.add_patch(add_circle)
ax.text(8.1, 2.0, "+", ha='center', va='center', fontsize=16, fontweight='bold', color='#B71C1C')

# Skip connection curve
ax.annotate("", xy=(8.1, 2.4), xytext=(2.3, 2.7),
            arrowprops=dict(arrowstyle="->", lw=2.5, color='#D32F2F', connectionstyle="arc3,rad=-0.4", linestyle='--'))
ax.text(5.2, 3.0, "Identity Shortcut Mapping $\\mathcal{I}(x) = x$", ha='center', va='center', fontsize=10, fontweight='bold', color='#B71C1C')

ax.annotate("", xy=(9.5, 2.0), xytext=(8.5, 2.0), arrowprops=dict(arrowstyle="->", lw=2, color='#B71C1C'))

relu_out = patches.Rectangle((9.5, 1.3), 2.8, 1.4, edgecolor='#B71C1C', facecolor='#FFCDD2')
ax.add_patch(relu_out)
ax.text(10.9, 2.0, "Output $\\mathcal{F}(x) + x$\nReLU Aktivasi", ha='center', va='center', fontsize=10, fontweight='bold', color='#B71C1C')

plt.title("Evolusi Arsitektur Klasik CNN: LeNet-5, AlexNet, VGG-16, dan ResNet", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/evolusi_arsitektur_cnn_lenet_vgg_resnet.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 3. mekanisme_pooling_dan_receptive_field_cnn.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

# Grid 4x4 input
grid_data = np.array([
    [12, 20, 30,  0],
    [ 8, 12,  2, 14],
    [34, 70, 37,  4],
    [12, 10, 25, 12]
])

for i in range(4):
    for j in range(4):
        # Color quadrants
        if i < 2 and j < 2:
            fc = '#BBDEFB' # Blue
        elif i < 2 and j >= 2:
            fc = '#C8E6C9' # Green
        elif i >= 2 and j < 2:
            fc = '#FFE0B2' # Orange
        else:
            fc = '#E1BEE7' # Purple
        rect = patches.Rectangle((0.8 + j*0.9, 4.8 - i*0.9), 0.9, 0.9, edgecolor='#424242', facecolor=fc, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(0.8 + j*0.9 + 0.45, 4.8 - i*0.9 + 0.45, str(grid_data[i, j]), ha='center', va='center', fontsize=12, fontweight='bold')

ax.text(2.6, 5.9, "Input Feature Map (4 x 4)", ha='center', va='center', fontsize=11, fontweight='bold', color='#1565C0')

# Max Pooling Branch
ax.annotate("", xy=(6.5, 4.5), xytext=(4.6, 4.2), arrowprops=dict(arrowstyle="->", lw=2.5, color='#D81B60'))
ax.text(5.5, 4.8, "Max Pooling\n(2x2, Stride 2)", ha='center', va='center', fontsize=10, fontweight='bold', color='#C2185B')

max_res = np.array([[20, 30], [70, 37]])
for i in range(2):
    for j in range(2):
        colors = [['#BBDEFB', '#C8E6C9'], ['#FFE0B2', '#E1BEE7']]
        rect = patches.Rectangle((7.0 + j*1.2, 4.8 - i*1.2), 1.2, 1.2, edgecolor='#424242', facecolor=colors[i][j], linewidth=1.8)
        ax.add_patch(rect)
        ax.text(7.0 + j*1.2 + 0.6, 4.8 - i*1.2 + 0.6, str(max_res[i, j]), ha='center', va='center', fontsize=14, fontweight='bold', color='#880E4F')

ax.text(8.2, 5.8, "Max Pool Output (2 x 2)\n$\\max(Q_{i,j})$", ha='center', va='center', fontsize=11, fontweight='bold', color='#880E4F')

# Average Pooling Branch
ax.annotate("", xy=(6.5, 2.0), xytext=(4.6, 2.5), arrowprops=dict(arrowstyle="->", lw=2.5, color='#00897B'))
ax.text(5.5, 1.8, "Average Pooling\n(2x2, Stride 2)", ha='center', va='center', fontsize=10, fontweight='bold', color='#00695C')

avg_res = np.array([[13.0, 11.5], [31.5, 19.5]])
for i in range(2):
    for j in range(2):
        colors = [['#BBDEFB', '#C8E6C9'], ['#FFE0B2', '#E1BEE7']]
        rect = patches.Rectangle((7.0 + j*1.2, 2.3 - i*1.2), 1.2, 1.2, edgecolor='#424242', facecolor=colors[i][j], linewidth=1.8)
        ax.add_patch(rect)
        ax.text(7.0 + j*1.2 + 0.6, 2.3 - i*1.2 + 0.6, f"{avg_res[i, j]:.1f}", ha='center', va='center', fontsize=13, fontweight='bold', color='#004D40')

ax.text(8.2, 3.2, "Avg Pool Output (2 x 2)\n$\\frac{1}{|Q|}\\sum Q_{i,j}$", ha='center', va='center', fontsize=11, fontweight='bold', color='#004D40')

# Global Average Pooling (GAP) Box
gap_box = patches.FancyBboxPatch((10.3, 1.0), 3.2, 5.0, boxstyle="round,pad=0.2", edgecolor='#F57C00', facecolor='#FFF3E0', linewidth=1.8)
ax.add_patch(gap_box)
ax.text(11.9, 5.5, "Global Average Pooling\n(GAP)", ha='center', va='center', fontsize=11, fontweight='bold', color='#E65100')
ax.text(11.9, 3.4, "Mengompresi seluruh\nmatriks spasial $H \\times W$\nmenjadi tepat 1 skalar\nper channel fitur:\n\n$GAP_c = \\frac{1}{H \\cdot W} \\sum_{i,j} X_{i,j,c}$\n\nEliminasi 90% parameter\nFully-Connected layer\n& cegah overfitting!", ha='center', va='center', fontsize=9.5, color='#BF360C')

plt.title("Mekanisme Spasial Max Pooling, Average Pooling, dan Global Average Pooling (GAP)", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/mekanisme_pooling_dan_receptive_field_cnn.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 4. strategi_transfer_learning_feature_extraction_fine_tuning.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.5), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7.5)
ax.axis('off')

# Strategy 1: Feature Extraction
strat1_box = patches.FancyBboxPatch((0.5, 4.0), 13.0, 3.0, boxstyle="round,pad=0.2", edgecolor='#1565C0', facecolor='#E3F2FD', linewidth=2)
ax.add_patch(strat1_box)
ax.text(7.0, 6.6, "Strategi 1: Feature Extraction (Backbone Frozen)", ha='center', va='center', fontsize=12, fontweight='bold', color='#0D47A1')

# Backbone Frozen
bb1 = patches.Rectangle((1.0, 4.4), 6.5, 1.6, edgecolor='#0D47A1', facecolor='#90CAF9', linewidth=1.8)
ax.add_patch(bb1)
ax.text(4.25, 5.2, "Pretrained Backbone (ResNet-50 / EfficientNet)\nBobot Dibekukan (param.requires_grad = False)\nEkstraksi Representasi Visual General (ImageNet)", ha='center', va='center', fontsize=10, fontweight='bold', color='#0D47A1')

ax.annotate("", xy=(8.5, 5.2), xytext=(7.7, 5.2), arrowprops=dict(arrowstyle="->", lw=2.5, color='#0D47A1'))

# Head Trained
head1 = patches.Rectangle((8.6, 4.4), 4.4, 1.6, edgecolor='#2E7D32', facecolor='#A5D6A7', linewidth=1.8)
ax.add_patch(head1)
ax.text(10.8, 5.2, "Custom Classifier Head\n(Linear + Dropout + Linear)\nBobot Dilatih (Active Training)\nSesuai Jumlah Kelas Target", ha='center', va='center', fontsize=10, fontweight='bold', color='#1B5E20')

# Strategy 2: Fine-Tuning
strat2_box = patches.FancyBboxPatch((0.5, 0.5), 13.0, 3.2, boxstyle="round,pad=0.2", edgecolor='#E65100', facecolor='#FFF3E0', linewidth=2)
ax.add_patch(strat2_box)
ax.text(7.0, 3.3, "Strategi 2: Fine-Tuning (Differential / Discriminative Learning Rates)", ha='center', va='center', fontsize=12, fontweight='bold', color='#BF360C')

# Early Layers
l1 = patches.Rectangle((1.0, 0.9), 3.6, 1.8, edgecolor='#E65100', facecolor='#FFE0B2', linewidth=1.5)
ax.add_patch(l1)
ax.text(2.8, 1.8, "Early Conv Layers\nFitur Tepi & Tekstur\nFrozen / LR Sangat Rendah\n($\\eta = 10^{-6}$)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#E65100')

# Mid-Late Layers
l2 = patches.Rectangle((4.9, 0.9), 3.8, 1.8, edgecolor='#F57C00', facecolor='#FFCC80', linewidth=1.5)
ax.add_patch(l2)
ax.text(6.8, 1.8, "Deep Conv Layers (Stage 4)\nFitur Semantik Domain\nUnfrozen dengan LR Rendah\n($\\eta = 10^{-5}$)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#E65100')

# Head
l3 = patches.Rectangle((9.0, 0.9), 4.0, 1.8, edgecolor='#2E7D32', facecolor='#A5D6A7', linewidth=1.8)
ax.add_patch(l3)
ax.text(11.0, 1.8, "New Classification Head\nAdaptasi Penuh ke Data Baru\nUnfrozen dengan Standar LR\n($\\eta = 10^{-3}$)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1B5E20')

plt.title("Strategi Transfer Learning pada Deep Learning: Feature Extraction vs Fine-Tuning", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/strategi_transfer_learning_feature_extraction_fine_tuning.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 5. pipeline_image_classification_end_to_end_cnn.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 6), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

steps = [
    ("1. Dataset Citra", "RGB Images\nKatalog Multi-Kelas\nTrain / Val Split", "#BBDEFB", "#0D47A1"),
    ("2. Augmentasi Citra", "RandomCrop, Flip\nColorJitter, Affine\nStandarisasi ImageNet", "#C8E6C9", "#1B5E20"),
    ("3. CNN Backbone", "Feature Extraction\nConv + BatchNorm\n+ ReLU + Residual", "#FFE0B2", "#E65100"),
    ("4. Pooling & Head", "Global Avg Pool\nDropout (0.3)\nDense Layer ($C$ unit)", "#E1BEE7", "#4A148C"),
    ("5. Inferensi & Loss", "Logits $\\to$ Softmax\nCross-Entropy Loss\nPrediksi Label & Conf.", "#FFCDD2", "#B71C1C")
]

x_pos = [0.5, 3.2, 5.9, 8.6, 11.3]
for idx, (title, desc, bg, fg) in enumerate(steps):
    box = patches.FancyBboxPatch((x_pos[idx], 1.8), 2.2, 3.4, boxstyle="round,pad=0.15", edgecolor=fg, facecolor=bg, linewidth=2)
    ax.add_patch(box)
    ax.text(x_pos[idx] + 1.1, 4.7, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=fg)
    ax.text(x_pos[idx] + 1.1, 3.2, desc, ha='center', va='center', fontsize=9, color='#212121')
    
    if idx < 4:
        ax.annotate("", xy=(x_pos[idx+1], 3.5), xytext=(x_pos[idx] + 2.2, 3.5),
                    arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# Feedback optimization loop
ax.annotate("", xy=(6.5, 1.2), xytext=(12.4, 1.6),
            arrowprops=dict(arrowstyle="->", lw=2, color='#B71C1C', connectionstyle="arc3,rad=0.2", linestyle='--'))
ax.text(9.5, 0.7, "Backpropagation & Optimizer Step (AdamW / SGD)", ha='center', va='center', fontsize=10, fontweight='bold', color='#B71C1C')

plt.title("Pipeline End-to-End Image Classification Menggunakan Convolutional Neural Network", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/pipeline_image_classification_end_to_end_cnn.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 6. konsep_dasar_object_detection_bounding_box_iou_nms.png
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), dpi=dpi)

# Left: Bounding Box & IoU
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title("(A) Intersection over Union (IoU) & Bounding Box", fontsize=11, fontweight='bold')

# Box Ground Truth (Green)
gt_box = patches.Rectangle((1.5, 2.5), 5.0, 5.0, edgecolor='#2E7D32', facecolor='#A5D6A7', alpha=0.5, linewidth=2.5)
ax1.add_patch(gt_box)
ax1.text(2.0, 7.2, "Ground Truth ($B_{gt}$)", fontsize=10, fontweight='bold', color='#1B5E20')

# Box Prediction (Blue)
pred_box = patches.Rectangle((3.5, 4.0), 5.0, 4.5, edgecolor='#1565C0', facecolor='#90CAF9', alpha=0.5, linewidth=2.5)
ax1.add_patch(pred_box)
ax1.text(5.5, 8.2, "Prediction ($B_{pred}$)", fontsize=10, fontweight='bold', color='#0D47A1')

# Intersection region
intersect = patches.Rectangle((3.5, 4.0), 3.0, 3.5, edgecolor='#D81B60', facecolor='#F48FB1', alpha=0.7, linewidth=1.5, linestyle=':')
ax1.add_patch(intersect)
ax1.text(5.0, 5.7, "Intersection\n$A \\cap B$", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#880E4F')

ax1.text(5.0, 1.2, r"$\text{IoU} = \frac{\text{Area}(B_{gt} \cap B_{pred})}{\text{Area}(B_{gt} \cup B_{pred})}$", ha='center', va='center', fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="#ECEFF1", ec="#90A4AE"))

# Right: NMS (Non-Maximum Suppression)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title("(B) Mekanisme Non-Maximum Suppression (NMS)", fontsize=11, fontweight='bold')

# Target Object Placeholder
tgt_circ = patches.Circle((5, 5), 2.2, edgecolor='#78909C', facecolor='#ECEFF1', linestyle='--')
ax2.add_patch(tgt_circ)
ax2.text(5, 5, "Target Objek", ha='center', va='center', fontsize=11, fontweight='bold', color='#546E7A')

# Candidate boxes
b1 = patches.Rectangle((2.8, 2.7), 4.4, 4.5, edgecolor='#2E7D32', facecolor='none', linewidth=3) # Best
ax2.add_patch(b1)
ax2.text(2.9, 7.0, "Box 1: Conf 0.94 (KEPT)", fontsize=9, fontweight='bold', color='#1B5E20')

b2 = patches.Rectangle((2.5, 2.4), 4.5, 4.8, edgecolor='#E53935', facecolor='none', linewidth=1.5, linestyle='--')
ax2.add_patch(b2)
ax2.text(2.6, 2.1, "Box 2: Conf 0.81 (SUPPRESSED, IoU > 0.5)", fontsize=8.5, fontweight='bold', color='#C62828')

b3 = patches.Rectangle((3.2, 3.0), 4.0, 4.2, edgecolor='#E53935', facecolor='none', linewidth=1.5, linestyle='--')
ax2.add_patch(b3)
ax2.text(3.3, 1.5, "Box 3: Conf 0.65 (SUPPRESSED, IoU > 0.5)", fontsize=8.5, fontweight='bold', color='#C62828')

plt.tight_layout()
plt.savefig('docs/assets/konsep_dasar_object_detection_bounding_box_iou_nms.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 7. arsitektur_dan_mekanisme_grid_yolo.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

# Input Image with S x S grid
grid_box = patches.Rectangle((0.8, 1.2), 4.2, 4.2, edgecolor='#1E88E5', facecolor='#E3F2FD', linewidth=2)
ax.add_patch(grid_box)

for g in range(1, 7):
    ax.plot([0.8 + g*0.6, 0.8 + g*0.6], [1.2, 5.4], color='#90CAF9', linestyle='-', lw=1)
    ax.plot([0.8, 5.0], [1.2 + g*0.6, 1.2 + g*0.6], color='#90CAF9', linestyle='-', lw=1)

# Center cell highlighted
cell_hl = patches.Rectangle((0.8 + 3*0.6, 1.2 + 3*0.6), 0.6, 0.6, edgecolor='#D81B60', facecolor='#F48FB1', alpha=0.8, linewidth=2)
ax.add_patch(cell_hl)
ax.text(2.9, 0.7, "Grid Cell $S \\times S$ (e.g., $7 \\times 7$ atau Multi-Scale)\nDeteksi Objek via Pusat Grid Cell", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0D47A1')

# Arrow
ax.annotate("", xy=(6.0, 3.3), xytext=(5.2, 3.3), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))
ax.text(5.6, 3.8, "Single\nForward\nPass", ha='center', va='center', fontsize=9.5, fontweight='bold')

# Darknet / CSPDarknet Backbone + Neck
net_box = patches.FancyBboxPatch((6.2, 1.5), 3.0, 3.6, boxstyle="round,pad=0.2", edgecolor='#2E7D32', facecolor='#E8F5E9', linewidth=2)
ax.add_patch(net_box)
ax.text(7.7, 4.5, "YOLO Backbone & Neck", ha='center', va='center', fontsize=11, fontweight='bold', color='#1B5E20')
ax.text(7.7, 3.0, "• CSP-Darknet Backbone\n• PANet / FPN Neck\n  Multi-Scale Feature Fusion\n  (P3: 8x, P4: 16x, P5: 32x)\n• High FPS Real-Time Engine", ha='center', va='center', fontsize=9, color='#2E7D32')

# Arrow
ax.annotate("", xy=(10.2, 3.3), xytext=(9.4, 3.3), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# Output Tensor
out_box = patches.FancyBboxPatch((10.4, 1.2), 3.0, 4.2, boxstyle="round,pad=0.2", edgecolor='#E65100', facecolor='#FFF3E0', linewidth=2)
ax.add_patch(out_box)
ax.text(11.9, 4.8, "Detection Tensor Output", ha='center', va='center', fontsize=11, fontweight='bold', color='#BF360C')
ax.text(11.9, 3.0, "Setiap Bounding Box:\n$[t_x, t_y, t_w, t_h, p_o, c_1, \\dots, c_C]$\n\n• $(t_x, t_y)$: Offset pusat\n• $(t_w, t_h)$: Skala dimensi\n• $p_o$: Objectness confidence\n• $c_k$: Probabilitas kelas", ha='center', va='center', fontsize=9, color='#BF360C')

plt.title("Arsitektur You Only Look Once (YOLO): Grid-Based Real-Time Object Detection", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/arsitektur_dan_mekanisme_grid_yolo.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 8. arsitektur_single_shot_detector_ssd_multiscale.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

# Backbone (VGG-16 / ResNet)
bb_rect = patches.Rectangle((0.8, 2.0), 3.2, 3.5, edgecolor='#1565C0', facecolor='#BBDEFB', linewidth=2)
ax.add_patch(bb_rect)
ax.text(2.4, 4.5, "Base Network\n(VGG-16 Truncated)", ha='center', va='center', fontsize=11, fontweight='bold', color='#0D47A1')
ax.text(2.4, 3.0, "Input: 300x300x3\nFeature Extractor\nConv4_3: 38x38x512", ha='center', va='center', fontsize=9, color='#0D47A1')

# Multi-scale feature pyramidal layers
pyramids = [
    ("Conv7", "19x19", 4.4, 2.2, 1.4, 3.0, "#C8E6C9", "#1B5E20"),
    ("Conv8_2", "10x10", 6.2, 2.4, 1.3, 2.6, "#FFE0B2", "#E65100"),
    ("Conv9_2", "5x5", 7.9, 2.6, 1.2, 2.2, "#E1BEE7", "#4A148C"),
    ("Conv10_2", "3x3", 9.5, 2.8, 1.1, 1.8, "#FFCDD2", "#B71C1C"),
    ("Conv11_2", "1x1", 11.0, 3.0, 1.0, 1.4, "#B2DFDB", "#004D40")
]

for name, res, x, y, w, h, bg, fg in pyramids:
    r = patches.Rectangle((x, y), w, h, edgecolor=fg, facecolor=bg, linewidth=1.5)
    ax.add_patch(r)
    ax.text(x + w/2, y + h/2, f"{name}\n{res}", ha='center', va='center', fontsize=8.5, fontweight='bold', color=fg)
    
    # Arrow down to detection head
    ax.annotate("", xy=(x + w/2, 1.4), xytext=(x + w/2, y), arrowprops=dict(arrowstyle="->", lw=1.5, color=fg))

# Classifier & BBox Head Box
head_box = patches.FancyBboxPatch((4.0, 0.4), 8.5, 0.9, boxstyle="round,pad=0.1", edgecolor='#212121', facecolor='#ECEFF1', linewidth=1.5)
ax.add_patch(head_box)
ax.text(8.25, 0.85, "Multi-scale Default Boxes / Anchors Classifier & Regressor (Total 8732 Prediksi BBox)", ha='center', va='center', fontsize=10, fontweight='bold', color='#212121')

ax.text(4.4, 6.0, "Resolusi Tinggi (38x38, 19x19) $\\to$ Deteksi Objek Kecil\nResolusi Rendah (5x5, 1x1) $\\to$ Deteksi Objek Besar", fontsize=10, fontweight='bold', color='#37474F')

plt.title("Arsitektur Single Shot MultiBox Detector (SSD): Multi-Scale Feature Maps", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/arsitektur_single_shot_detector_ssd_multiscale.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 9. arsitektur_two_stage_faster_rcnn_rpn_roi_pooling.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.5), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7.5)
ax.axis('off')

# Stage 0: Backbone
bb_box = patches.Rectangle((0.5, 2.0), 2.8, 3.5, edgecolor='#1E88E5', facecolor='#BBDEFB', linewidth=2)
ax.add_patch(bb_box)
ax.text(1.9, 4.3, "Backbone CNN\n(ResNet-50 / FPN)", ha='center', va='center', fontsize=11, fontweight='bold', color='#0D47A1')
ax.text(1.9, 2.8, "Input Citra $H \\times W \\times 3$\nEkstraksi Feature Map\n$C \\times H' \\times W'$", ha='center', va='center', fontsize=9.5, color='#0D47A1')

# Arrow to RPN and RoI
ax.annotate("", xy=(3.9, 5.2), xytext=(3.3, 4.2), arrowprops=dict(arrowstyle="->", lw=2, color='#424242'))
ax.annotate("", xy=(6.5, 3.2), xytext=(3.3, 3.5), arrowprops=dict(arrowstyle="->", lw=2, color='#424242'))

# Stage 1: Region Proposal Network (RPN)
rpn_box = patches.FancyBboxPatch((4.0, 4.4), 4.2, 2.5, boxstyle="round,pad=0.15", edgecolor='#E53935', facecolor='#FFCDD2', linewidth=2)
ax.add_patch(rpn_box)
ax.text(6.1, 6.4, "Stage 1: Region Proposal Network (RPN)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#B71C1C')
ax.text(6.1, 5.2, "• Anchor Boxes (3 scales x 3 aspect ratios = $k=9$)\n• $2k$ Objectness Scores (Foreground vs Background)\n• $4k$ Bounding Box Regression Delays\n• Filtering via NMS $\\to$ ~2000 Candidate RoIs", ha='center', va='center', fontsize=8.5, color='#7F0000')

# Arrow from RPN to RoI Pooling
ax.annotate("", xy=(7.8, 3.9), xytext=(6.5, 4.4), arrowprops=dict(arrowstyle="->", lw=2, color='#B71C1C'))

# RoI Pooling / RoIAlign
roi_box = patches.Rectangle((6.7, 2.2), 2.4, 1.8, edgecolor='#6A1B9A', facecolor='#E1BEE7', linewidth=2)
ax.add_patch(roi_box)
ax.text(7.9, 3.1, "RoI Pooling /\nRoIAlign\n(Fixed $7 \\times 7$ Map)", ha='center', va='center', fontsize=10, fontweight='bold', color='#4A148C')

# Arrow to Stage 2
ax.annotate("", xy=(9.7, 3.1), xytext=(9.1, 3.1), arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

# Stage 2: Fast R-CNN Head
head_box = patches.FancyBboxPatch((9.8, 1.5), 3.7, 3.2, boxstyle="round,pad=0.15", edgecolor='#2E7D32', facecolor='#C8E6C9', linewidth=2)
ax.add_patch(head_box)
ax.text(11.65, 4.2, "Stage 2: Fast R-CNN Head", ha='center', va='center', fontsize=11, fontweight='bold', color='#1B5E20')
ax.text(11.65, 2.7, "• Fully-Connected / Conv Layers\n• Classification Branch:\n  Softmax atas $C + 1$ Kelas\n• BBox Regression Branch:\n  $4 \\times C$ Refined Coordinates\n  Akurasi Sangat Tinggi!", ha='center', va='center', fontsize=9, color='#1B5E20')

plt.title("Arsitektur Two-Stage Faster R-CNN: Integrasi RPN dan RoIAlign", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/arsitektur_two_stage_faster_rcnn_rpn_roi_pooling.png', dpi=dpi)
plt.close()

# -------------------------------------------------------------
# 10. pipeline_end_to_end_training_dataset_citra.png
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6), dpi=dpi)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')

stages = [
    ("1. Dataset & Labeling", "Format Anotasi:\n• YOLO (txt class x y w h)\n• COCO (json polygon/box)\n• Pascal VOC (xml xmin ymin)\nTrain/Val/Test Split 70:20:10", "#BBDEFB", "#0D47A1"),
    ("2. Augmentation & Loader", "Albumentations / Torchvision:\n• Mosaic & MixUp\n• Affine, HSV Shift, Blur\n• PyTorch DataLoader Multiworker\n• Pin Memory & Batching", "#C8E6C9", "#1B5E20"),
    ("3. Model & Loss Function", "Backbone + Detection Head:\n• Focal Loss (Class Imbalance)\n• CIoU / GIoU Loss (BBox)\n• Anchor Matching Optimization", "#FFE0B2", "#E65100"),
    ("4. Mixed-Precision Training", "AMP (torch.cuda.amp):\n• GradScaler FP16/BF16\n• Cosine Annealing LR Scheduler\n• Gradient Accumulation\n• TensorBoard & Checkpoint", "#E1BEE7", "#4A148C")
]

x_coords = [0.6, 3.8, 7.0, 10.2]
for i, (title, content, bg, fg) in enumerate(stages):
    box = patches.FancyBboxPatch((x_coords[i], 1.5), 3.0, 3.8, boxstyle="round,pad=0.15", edgecolor=fg, facecolor=bg, linewidth=2)
    ax.add_patch(box)
    ax.text(x_coords[i] + 1.5, 4.8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=fg)
    ax.text(x_coords[i] + 1.5, 3.0, content, ha='center', va='center', fontsize=8.8, color='#212121')
    
    if i < 3:
        ax.annotate("", xy=(x_coords[i+1], 3.4), xytext=(x_coords[i] + 3.0, 3.4),
                    arrowprops=dict(arrowstyle="->", lw=2.5, color='#424242'))

eval_box = patches.FancyBboxPatch((2.0, 0.3), 10.0, 0.9, boxstyle="round,pad=0.1", edgecolor='#B71C1C', facecolor='#FFCDD2', linewidth=1.5)
ax.add_patch(eval_box)
ax.text(7.0, 0.75, "Evaluasi Metrik Standar: Mean Average Precision (mAP@0.5, mAP@0.5:0.95), F1-Score, dan Latensi FPS", ha='center', va='center', fontsize=10, fontweight='bold', color='#B71C1C')

plt.title("Pipeline End-to-End Pelatihan Dataset Citra untuk Deep Learning Computer Vision", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('docs/assets/pipeline_end_to_end_training_dataset_citra.png', dpi=dpi)
plt.close()

print("[OK] Selesai menghasilkan 10 gambar diagram arsitektur Part 12 beresolusi 300 DPI!")
