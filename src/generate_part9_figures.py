import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import FancyBboxPatch

# Set font styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Figure 9.1: Konsep Hierarki Representasi Deep Learning vs Classical ML
def fig_9_1():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    # Left: Classical Machine Learning
    ax = axes[0]
    ax.set_title("Paradigma Classical Machine Learning\n(Feature Engineering Manual)", fontsize=13, fontweight='bold', pad=15)
    boxes_c = [
        ("Input Data Mentah\n(Spektrometri Tanah / Drone)", "#E3F2FD", "#1565C0"),
        ("Hand-crafted Feature Extraction\n(Manual: NDVI, GLCM, Tekstur)", "#FFF3E0", "#E65100"),
        ("Klasifikasi / Regresi Dangkal\n(SVM, Random Forest, Linier)", "#E8F5E9", "#2E7D32"),
        ("Prediksi / Output\n(Kadar NPK / Defisiensi)", "#F3E5F5", "#6A1B9A")
    ]
    for i, (text, bg, border) in enumerate(boxes_c):
        ax.add_patch(FancyBboxPatch((0.15, 0.78 - i*0.24), 0.7, 0.16, boxstyle="round,pad=0.03", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(0.5, 0.86 - i*0.24, text, ha='center', va='center', fontsize=10, fontweight='bold', color=border)
        if i < len(boxes_c) - 1:
            ax.annotate("", xy=(0.5, 0.77 - i*0.24), xytext=(0.5, 0.81 - (i+1)*0.24 + 0.16),
                        arrowprops=dict(arrowstyle="->", lw=2.5, color='#455A64'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Right: Deep Learning
    ax = axes[1]
    ax.set_title("Paradigma Deep Learning\n(Hierarchical Feature Learning End-to-End)", fontsize=13, fontweight='bold', pad=15)
    boxes_d = [
        ("Input Data Mentah\n(Sensor Spektral / Citra Drone)", "#E3F2FD", "#1565C0"),
        ("Lapisan Bawah (Low-Level)\n(Ekstraksi Tepi, Tekstur Piksel, Gradien)", "#E0F7FA", "#00838F"),
        ("Lapisan Tengah (Mid-Level)\n(Pola Urat Daun, Kontur Kanopi Pohon)", "#E8F5E9", "#2E7D32"),
        ("Lapisan Atas (High-Level)\n(Representasi Semantik: Kanopi Sawit Sakit/Sehat)", "#FFF8E1", "#F57F17"),
        ("Output Prediksi End-to-End\n(Diagnosa Kesehatan & Estimasi Produksi)", "#FCE4EC", "#C2185B")
    ]
    for i, (text, bg, border) in enumerate(boxes_d):
        y_pos = 0.82 - i*0.19
        ax.add_patch(FancyBboxPatch((0.15, y_pos), 0.7, 0.13, boxstyle="round,pad=0.03", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(0.5, y_pos + 0.065, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=border)
        if i < len(boxes_d) - 1:
            ax.annotate("", xy=(0.5, y_pos - 0.01), xytext=(0.5, y_pos - 0.05),
                        arrowprops=dict(arrowstyle="->", lw=2.5, color='#1565C0'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('docs/assets/konsep_hierarki_representasi_deep_learning_agrokompleks.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/konsep_hierarki_representasi_deep_learning_agrokompleks.png")

# 2. Figure 9.2: Arsitektur Multi-Layer Perceptron (ANN)
def fig_9_2():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_title("Arsitektur Komputasi Artificial Neural Network (Multi-Layer Perceptron)", fontsize=13, fontweight='bold', pad=20)
    
    layer_sizes = [4, 6, 5, 2]
    layer_names = ["Input Layer\n(Fitur Sensor Agrikultur)", "Hidden Layer 1\n($a^{[1]} = \\sigma(W^{[1]}x + b^{[1]})$)", "Hidden Layer 2\n($a^{[2]} = \\sigma(W^{[2]}a^{[1]} + b^{[2]})$)", "Output Layer\n($\\hat{y} = \\mathrm{softmax}(z^{[3]})$)"]
    x_pos = [0.1, 0.4, 0.7, 0.95]
    
    node_positions = []
    for l_idx, (size, x) in enumerate(zip(layer_sizes, x_pos)):
        y_vals = np.linspace(0.85, 0.15, size)
        positions = [(x, y) for y in y_vals]
        node_positions.append(positions)
        ax.text(x, 0.95, layer_names[l_idx], ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1A237E')
        
    colors = ['#1565C0', '#2E7D32', '#F57F17', '#C2185B']
    
    # Draw connections
    for l in range(len(layer_sizes) - 1):
        for p1 in node_positions[l]:
            for p2 in node_positions[l+1]:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#90A4AE', alpha=0.35, linewidth=1)
                
    # Draw nodes
    for l_idx, positions in enumerate(node_positions):
        for n_idx, (x, y) in enumerate(positions):
            circle = plt.Circle((x, y), 0.035, facecolor='white', edgecolor=colors[l_idx], linewidth=2.5, zorder=5)
            ax.add_patch(circle)
            if l_idx == 0:
                ax.text(x, y, f"$x_{{{n_idx+1}}}$", ha='center', va='center', fontsize=9, fontweight='bold', zorder=6)
            elif l_idx == len(layer_sizes) - 1:
                ax.text(x, y, f"$\\hat{{y}}_{{{n_idx+1}}}$", ha='center', va='center', fontsize=9, fontweight='bold', zorder=6)
            else:
                ax.text(x, y, f"$a_{{{n_idx+1}}}^{{[{l_idx}]}}$", ha='center', va='center', fontsize=8, zorder=6)
                
    ax.text(0.25, 0.05, "Matriks Bobot $W^{[1]} \\in \\mathbb{R}^{6 \\times 4}$", ha='center', fontsize=10, style='italic', color='#37474F')
    ax.text(0.55, 0.05, "Matriks Bobot $W^{[2]} \\in \\mathbb{R}^{5 \\times 6}$", ha='center', fontsize=10, style='italic', color='#37474F')
    ax.text(0.825, 0.05, "Matriks Bobot $W^{[3]} \\in \\mathbb{R}^{2 \\times 5}$", ha='center', fontsize=10, style='italic', color='#37474F')
    
    ax.set_xlim(-0.02, 1.05)
    ax.set_ylim(0, 1.05)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('docs/assets/arsitektur_artificial_neural_network_multi_layer_perceptron.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/arsitektur_artificial_neural_network_multi_layer_perceptron.png")

# 3. Figure 9.9: Komparasi Arsitektur Framework PyTorch vs TensorFlow
def fig_9_9():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5), dpi=300)
    
    # Left: PyTorch
    ax = axes[0]
    ax.set_title("PyTorch: Dynamic Computation Graph\n(Define-by-Run & Eager Execution)", fontsize=13, fontweight='bold', pad=15)
    steps_pt = [
        ("1. Input Data Tensor & Model Definition\n(Subclass torch.nn.Module, __init__ & forward)", "#E3F2FD", "#1565C0"),
        ("2. Forward Pass Dinamis\nGraf komputasi dibangun secara on-the-fly per iterasi", "#E0F2F1", "#00796B"),
        ("3. Loss Calculation & Loss Tensor\nloss = criterion(output, target)", "#FFF3E0", "#E65100"),
        ("4. Autograd Engine (Dynamic Backward)\nloss.backward() melacak jejak gradien instan", "#F3E5F5", "#6A1B9A"),
        ("5. Optimizer Step & Zero Grad\noptimizer.step(); optimizer.zero_grad()", "#E8F5E9", "#2E7D32")
    ]
    for i, (text, bg, border) in enumerate(steps_pt):
        y_pos = 0.82 - i*0.19
        ax.add_patch(FancyBboxPatch((0.08, y_pos), 0.84, 0.13, boxstyle="round,pad=0.03", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(0.5, y_pos + 0.065, text, ha='center', va='center', fontsize=9, fontweight='bold', color=border)
        if i < len(steps_pt) - 1:
            ax.annotate("", xy=(0.5, y_pos - 0.01), xytext=(0.5, y_pos - 0.05),
                        arrowprops=dict(arrowstyle="->", lw=2, color='#1565C0'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Right: TensorFlow / Keras
    ax = axes[1]
    ax.set_title("TensorFlow / Keras: Static & Symbolic Graph\n(Define-and-Run / tf.function Optimization)", fontsize=13, fontweight='bold', pad=15)
    steps_tf = [
        ("1. Model Definition & Compilation\n(tf.keras.Sequential / Functional / Subclassing)", "#FFF8E1", "#F57F17"),
        ("2. tf.function JIT Compilation\nGraf statis dioptimasi oleh XLA Compiler ke GPU/TPU", "#E8EAF6", "#283593"),
        ("3. High-Level Training Loop\nmodel.compile(...) & model.fit(dataset, epochs)", "#EDE7F6", "#4527A0"),
        ("4. Low-Level Control via tf.GradientTape\nwith tf.GradientTape() as tape: ... grad = tape.gradient()", "#FCE4EC", "#AD1457"),
        ("5. Deployment Ecosystem\nSavedModel, TensorFlow Lite, TF Serving, ONNX", "#E8F5E9", "#1B5E20")
    ]
    for i, (text, bg, border) in enumerate(steps_tf):
        y_pos = 0.82 - i*0.19
        ax.add_patch(FancyBboxPatch((0.08, y_pos), 0.84, 0.13, boxstyle="round,pad=0.03", facecolor=bg, edgecolor=border, linewidth=2))
        ax.text(0.5, y_pos + 0.065, text, ha='center', va='center', fontsize=9, fontweight='bold', color=border)
        if i < len(steps_tf) - 1:
            ax.annotate("", xy=(0.5, y_pos - 0.01), xytext=(0.5, y_pos - 0.05),
                        arrowprops=dict(arrowstyle="->", lw=2, color='#F57F17'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('docs/assets/komparasi_arsitektur_framework_pytorch_vs_tensorflow.png', dpi=300)
    plt.close()
    print("[OK] Saved: docs/assets/komparasi_arsitektur_framework_pytorch_vs_tensorflow.png")

if __name__ == '__main__':
    fig_9_1()
    fig_9_2()
    fig_9_9()
