"""
Customer Churn Prediction - ML Methodology & Pipeline Diagrams
==============================================================
This script generates comprehensive visualizations of:
1. ML Methodology (algorithms and techniques used)
2. End-to-End Pipeline (data flow from input to prediction)
3. Inference Pipeline (how predictions are made in production)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from pathlib import Path

# Set style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parents[1]
DOC_DIAG_DIR = ROOT / 'docs' / 'diagrams'
DOC_PNG_DIR = DOC_DIAG_DIR / 'png'
DOC_SVG_DIR = DOC_DIAG_DIR / 'svg'


def save_diagram_outputs(fig, legacy_name):
        DOC_PNG_DIR.mkdir(parents=True, exist_ok=True)
        DOC_SVG_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(legacy_name, dpi=300, bbox_inches='tight', facecolor='white')
        stem = Path(legacy_name).stem
        fig.savefig(DOC_PNG_DIR / f'{stem}.png', dpi=300, bbox_inches='tight', facecolor='white')
        fig.savefig(DOC_SVG_DIR / f'{stem}.svg', format='svg', bbox_inches='tight', facecolor='white')

# ============================================================================
# DIAGRAM 1: ML METHODOLOGY & ALGORITHMS
# ============================================================================
print("Creating ML Methodology Diagram...")

fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Title
ax.text(5, 11.5, 'Customer Churn Prediction - ML Methodology', 
        fontsize=18, fontweight='bold', ha='center')
ax.text(5, 11, 'Advanced Algorithms & Techniques for Real-Time Classification',
        fontsize=12, ha='center', style='italic', color='#666')

# ========== SECTION 1: PROBLEM DEFINITION ==========
y_pos = 10.2
ax.add_patch(FancyBboxPatch((0.2, y_pos-0.6), 2.5, 0.7, boxstyle="round,pad=0.1", 
                            edgecolor='#FF6B6B', facecolor='#FFE5E5', linewidth=2))
ax.text(1.45, y_pos-0.2, 'PROBLEM TYPE', fontsize=11, fontweight='bold', ha='center')
ax.text(1.45, y_pos-0.45, 'Binary Classification', fontsize=9, ha='center')

# Arrow
arrow = FancyArrowPatch((2.7, y_pos-0.2), (3.3, y_pos-0.2), 
                       arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
ax.add_patch(arrow)

ax.add_patch(FancyBboxPatch((3.3, y_pos-0.6), 2.5, 0.7, boxstyle="round,pad=0.1",
                            edgecolor='#4ECDC4', facecolor='#E0F7F6', linewidth=2))
ax.text(4.55, y_pos-0.2, 'TARGET VARIABLE', fontsize=11, fontweight='bold', ha='center')
ax.text(4.55, y_pos-0.45, 'Churn (Yes/No)', fontsize=9, ha='center')

# Arrow
arrow = FancyArrowPatch((5.8, y_pos-0.2), (6.4, y_pos-0.2),
                       arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
ax.add_patch(arrow)

ax.add_patch(FancyBboxPatch((6.4, y_pos-0.6), 2.5, 0.7, boxstyle="round,pad=0.1",
                            edgecolor='#95E1D3', facecolor='#E8F8F5', linewidth=2))
ax.text(7.65, y_pos-0.2, 'DATASET SIZE', fontsize=11, fontweight='bold', ha='center')
ax.text(7.65, y_pos-0.45, '7,043 records', fontsize=9, ha='center')

# ========== SECTION 2: DATA PREPROCESSING ==========
y_pos = 8.8
ax.text(0.5, y_pos+0.3, '1. DATA PREPROCESSING', fontsize=12, fontweight='bold', color='#2C3E50')

steps = [
    ('Data Loading', '7,043\nrecords'),
    ('Exploratory\nAnalysis', 'Check\nmissing'),
    ('Feature\nScaling', 'Standard\nScaler'),
    ('Encoding', 'One-Hot\nEncoding'),
    ('Feature\nEngineering', '30 final\nfeatures')
]

for i, (step, detail) in enumerate(steps):
    x_pos = 0.5 + i * 1.8
    ax.add_patch(FancyBboxPatch((x_pos, y_pos-0.8), 1.6, 0.7, boxstyle="round,pad=0.05",
                                edgecolor='#667eea', facecolor='#F0F4FF', linewidth=1.5))
    ax.text(x_pos+0.8, y_pos-0.35, step, fontsize=8, fontweight='bold', ha='center', va='center')
    ax.text(x_pos+0.8, y_pos-0.65, detail, fontsize=7, ha='center', va='center', color='#555')
    
    if i < len(steps) - 1:
        arrow = FancyArrowPatch((x_pos+1.6, y_pos-0.45), (x_pos+1.8, y_pos-0.45),
                               arrowstyle='->', mutation_scale=15, linewidth=1.5, color='#667eea')
        ax.add_patch(arrow)

# ========== SECTION 3: DATA SPLITS ==========
y_pos = 7.5
ax.text(0.5, y_pos+0.3, '2. DATA STRATIFICATION (Maintain Class Distribution)', 
        fontsize=12, fontweight='bold', color='#2C3E50')

splits_data = [
    ('TRAINING\n60%', '4,226 records', '#8E44AD'),
    ('VALIDATION\n20%', '1,409 records', '#3498DB'),
    ('TEST\n10%', '704 records', '#E74C3C'),
    ('HOLDOUT\n10%', '704 records\n(Unseen)', '#27AE60')
]

for i, (title, count, color) in enumerate(splits_data):
    x_pos = 0.5 + i * 2.2
    ax.add_patch(FancyBboxPatch((x_pos, y_pos-0.85), 2, 0.8, boxstyle="round,pad=0.05",
                                edgecolor=color, facecolor=color, linewidth=2, alpha=0.3))
    ax.text(x_pos+1, y_pos-0.25, title, fontsize=8, fontweight='bold', ha='center', color=color)
    ax.text(x_pos+1, y_pos-0.65, count, fontsize=7, ha='center', color='#555')

# ========== SECTION 4: ML ALGORITHMS ==========
y_pos = 5.8
ax.text(0.5, y_pos+0.3, '3. MACHINE LEARNING ALGORITHMS COMPARISON', 
        fontsize=12, fontweight='bold', color='#2C3E50')

algorithms = [
    ('Multi-Layer\nPerceptron (MLP)\n✓ Selected', '76.40%', '#27AE60', 'Main Model'),
    ('Neural Network\n(MLPClassifier)', '78.89%\n(tuned)', '#2980B9', 'Best Accuracy'),
    ('Comparison Models\n(Baselines)', '75-77%', '#E67E22', 'Reference'),
    ('Ensemble Methods\n(Future)', 'TBD', '#95A5A6', 'To Explore')
]

for i, (algo, score, color, note) in enumerate(algorithms):
    x_pos = 0.5 + i * 2.2
    ax.add_patch(FancyBboxPatch((x_pos, y_pos-1.0), 2, 0.95, boxstyle="round,pad=0.05",
                                edgecolor=color, facecolor=color, linewidth=2, alpha=0.2))
    ax.text(x_pos+1, y_pos-0.2, algo, fontsize=8, fontweight='bold', ha='center', va='center')
    ax.text(x_pos+1, y_pos-0.65, f'Accuracy: {score}', fontsize=7, ha='center', 
            fontweight='bold', color=color)
    ax.text(x_pos+1, y_pos-0.85, note, fontsize=7, ha='center', style='italic', color='#555')

# ========== SECTION 5: HYPERPARAMETER TUNING ==========
y_pos = 4.2
ax.text(0.5, y_pos+0.3, '4. HYPERPARAMETER OPTIMIZATION', 
        fontsize=12, fontweight='bold', color='#2C3E50')

hyper_params = [
    ('Hidden Layers\n(32, 16, 8)', 'Architecture'),
    ('Learning Rate\n0.001', 'Optimization'),
    ('Max Iterations\n300', 'Convergence'),
    ('Batch Size\n64', 'Training'),
    ('Alpha (L2)\n0.0001', 'Regularization')
]

for i, (param, category) in enumerate(hyper_params):
    x_pos = 0.5 + i * 1.8
    ax.add_patch(FancyBboxPatch((x_pos, y_pos-0.8), 1.6, 0.7, boxstyle="round,pad=0.05",
                                edgecolor='#F39C12', facecolor='#FEF5E7', linewidth=1.5))
    ax.text(x_pos+0.8, y_pos-0.35, param, fontsize=7, fontweight='bold', ha='center', va='center')
    ax.text(x_pos+0.8, y_pos-0.65, category, fontsize=6, ha='center', va='center', 
            style='italic', color='#666')

# ========== SECTION 6: EVALUATION METRICS ==========
y_pos = 2.5
ax.text(0.5, y_pos+0.3, '5. MODEL EVALUATION METRICS', 
        fontsize=12, fontweight='bold', color='#2C3E50')

metrics = [
    ('Accuracy\n76.40%', '#27AE60'),
    ('Precision\n56.56%', '#3498DB'),
    ('Recall\n48.40%', '#E74C3C'),
    ('F1-Score\n0.5216', '#F39C12'),
    ('ROC-AUC\n0.7768 ⭐', '#9B59B6')
]

for i, (metric, color) in enumerate(metrics):
    x_pos = 0.5 + i * 1.85
    ax.add_patch(FancyBboxPatch((x_pos, y_pos-0.75), 1.75, 0.65, boxstyle="round,pad=0.05",
                                edgecolor=color, facecolor=color, linewidth=2, alpha=0.25))
    ax.text(x_pos+0.875, y_pos-0.35, metric, fontsize=8, fontweight='bold', 
            ha='center', va='center', color=color)

# ========== SECTION 7: DEPLOYMENT ==========
y_pos = 0.8
ax.text(0.5, y_pos+0.3, '6. PRODUCTION DEPLOYMENT', 
        fontsize=12, fontweight='bold', color='#2C3E50')

deployment = [
    ('Model\nSerialization', 'final_optimized\n_churn_model.pkl', '#667eea'),
    ('Streamlit\nWeb UI', 'Interactive\nInterface', '#FF6B6B'),
    ('FastAPI\nREST API', 'Production\nEndpoint', '#4ECDC4'),
    ('Real-Time\nPredictions', 'Inference\nPipeline', '#95E1D3')
]

for i, (title, detail, color) in enumerate(deployment):
    x_pos = 0.5 + i * 2.2
    ax.add_patch(FancyBboxPatch((x_pos, y_pos-0.65), 2, 0.6, boxstyle="round,pad=0.05",
                                edgecolor=color, facecolor=color, linewidth=2, alpha=0.25))
    ax.text(x_pos+1, y_pos-0.2, title, fontsize=8, fontweight='bold', ha='center')
    ax.text(x_pos+1, y_pos-0.5, detail, fontsize=7, ha='center', color='#555')
    
    if i < len(deployment) - 1:
        arrow = FancyArrowPatch((x_pos+2, y_pos-0.35), (x_pos+2.2, y_pos-0.35),
                               arrowstyle='->', mutation_scale=15, linewidth=1.5, color='#333')
        ax.add_patch(arrow)

plt.tight_layout()
save_diagram_outputs(fig, 'ML_Methodology_Diagram.png')
print("✓ Saved: ML_Methodology_Diagram.png")
plt.close()

# ============================================================================
# DIAGRAM 2: END-TO-END PIPELINE
# ============================================================================
print("Creating End-to-End Pipeline Diagram...")

fig, ax = plt.subplots(figsize=(14, 16))
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis('off')

# Title
ax.text(5, 15.5, 'End-to-End Customer Churn Prediction Pipeline',
        fontsize=16, fontweight='bold', ha='center')
ax.text(5, 15, 'Complete Data Flow: Input → Processing → Model → Output',
        fontsize=11, ha='center', style='italic', color='#666')

def add_pipeline_box(ax, x, y, width, height, text, color, fontsize=9):
    """Helper function to add a box to pipeline"""
    ax.add_patch(FancyBboxPatch((x-width/2, y-height/2), width, height, 
                                boxstyle="round,pad=0.1", edgecolor=color, 
                                facecolor=color, linewidth=2, alpha=0.25))
    ax.text(x, y, text, fontsize=fontsize, fontweight='bold', ha='center', va='center')

def add_arrow(ax, x1, y1, x2, y2, label='', color='#333'):
    """Helper function to add arrow"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->', 
                           mutation_scale=25, linewidth=2.5, color=color)
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
        ax.text(mid_x+0.3, mid_y, label, fontsize=8, style='italic', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# PHASE 1: INPUT DATA
y_pos = 14
ax.text(1, y_pos+0.5, 'PHASE 1: INPUT DATA', fontsize=11, fontweight='bold', color='#E74C3C')

add_pipeline_box(ax, 1, y_pos, 2, 0.6, 'Customer Information\n(Raw Data)', '#FF6B6B', 8)
add_arrow(ax, 1, y_pos-0.35, 1, y_pos-0.9, color='#333')

add_pipeline_box(ax, 1, y_pos-1.3, 2, 0.6, 'CSV/API Input\n7,043 records', '#FF8C42', 8)
add_arrow(ax, 1, y_pos-1.65, 1, y_pos-2.2, color='#333')

# PHASE 2: FEATURE ENGINEERING
y_pos = 12
ax.text(1, y_pos+0.5, 'PHASE 2: FEATURE ENGINEERING', fontsize=11, fontweight='bold', color='#3498DB')

features = [
    'Tenure',
    'Monthly\nCharges',
    'Internet\nService',
    'Contract',
    'Payment\nMethod'
]

for i, feature in enumerate(features):
    x = 0.2 + i * 0.45
    add_pipeline_box(ax, x, y_pos-1.2, 0.35, 0.5, feature, '#3498DB', 6)

ax.text(2.8, y_pos-1.2, '...and 25 more\nengineered features', fontsize=7, 
        style='italic', color='#666', bbox=dict(boxstyle='round', facecolor='#ECF0F1', alpha=0.5))

add_arrow(ax, 1.5, y_pos-1.5, 3, y_pos-2.4, label='30 Final Features', color='#3498DB')

# PHASE 3: DATA PREPROCESSING
y_pos = 10
ax.text(5.5, y_pos+0.5, 'PHASE 3: DATA PREPROCESSING', fontsize=11, fontweight='bold', color='#27AE60')

preprocessing_steps = [
    ('Scaling\nStandardScaler', 5, y_pos-1.2, '#27AE60'),
    ('Encoding\nOne-Hot', 6.5, y_pos-1.2, '#27AE60'),
    ('Splitting\n60-20-10-10', 8, y_pos-1.2, '#27AE60')
]

for step, x, y, color in preprocessing_steps:
    add_pipeline_box(ax, x, y, 1.2, 0.6, step, color, 8)

add_arrow(ax, 3, y_pos-2.4, 5, y_pos-1.5, color='#333')
add_arrow(ax, 5, y_pos-1.5, 5, y_pos-2.2, label='Prepared Data', color='#27AE60')
add_arrow(ax, 6.5, y_pos-1.5, 6.5, y_pos-2.2, color='#27AE60')
add_arrow(ax, 8, y_pos-1.5, 8, y_pos-2.2, color='#27AE60')

# PHASE 4: DATA SPLITS
y_pos = 8.3
ax.text(2.5, y_pos+0.5, 'PHASE 4: DATA STRATIFICATION', fontsize=11, fontweight='bold', color='#F39C12')

splits_boxes = [
    ('TRAINING\n60%\n4,226 rec', 1.5, y_pos-1.2, '#8E44AD'),
    ('VALIDATION\n20%\n1,409 rec', 3.5, y_pos-1.2, '#3498DB'),
    ('TEST\n10%\n704 rec', 5.5, y_pos-1.2, '#E74C3C'),
    ('HOLDOUT\n10%\n704 rec', 7.5, y_pos-1.2, '#27AE60')
]

for box_text, x, y, color in splits_boxes:
    add_pipeline_box(ax, x, y, 1.4, 0.8, box_text, color, 8)

ax.text(8.8, y_pos-1.2, 'Stratified\nClass Dist:\n26.7% Churn', fontsize=7, 
        bbox=dict(boxstyle='round', facecolor='#ECF0F1', alpha=0.7))

add_arrow(ax, 5, y_pos-2.2, 5, y_pos-2.8, label='Train Split', color='#8E44AD')
add_arrow(ax, 5, y_pos-2.8, 4.5, y_pos-3.8, color='#333')

# PHASE 5: MODEL TRAINING
y_pos = 6
ax.text(4.5, y_pos+0.5, 'PHASE 5: MODEL TRAINING', fontsize=11, fontweight='bold', color='#E67E22')

ax.add_patch(FancyBboxPatch((3, y_pos-1.2), 3, 0.8, boxstyle="round,pad=0.1",
                            edgecolor='#E67E22', facecolor='#FEF5E7', linewidth=2))
ax.text(4.5, y_pos-0.8, 'MLPClassifier(32,16,8)\nLearning Rate: 0.001\nMax Iterations: 300', 
        fontsize=8, fontweight='bold', ha='center', va='center')

add_arrow(ax, 4.5, y_pos-1.6, 4.5, y_pos-2.3, label='Train Model', color='#E67E22')

# PHASE 6: VALIDATION & HYPERPARAMETER TUNING
y_pos = 5
ax.text(7.5, y_pos+0.5, 'PHASE 6: HYPERPARAMETER TUNING', fontsize=11, fontweight='bold', color='#16A085')

ax.add_patch(FancyBboxPatch((6, y_pos-1.2), 3, 0.8, boxstyle="round,pad=0.1",
                            edgecolor='#16A085', facecolor='#D5F4E6', linewidth=2))
ax.text(7.5, y_pos-0.8, 'Grid Search\nValidation Set: 1,409 records\nBest: 78.89% Accuracy',
        fontsize=8, fontweight='bold', ha='center', va='center')

add_arrow(ax, 3.5, y_pos-2.3, 6.5, y_pos-0.8, label='Validate', color='#16A085')
add_arrow(ax, 7.5, y_pos-1.6, 7.5, y_pos-2.3, label='Tuned Model', color='#16A085')

# PHASE 7: TESTING & EVALUATION
y_pos = 3.2
ax.text(5, y_pos+0.5, 'PHASE 7: TESTING & EVALUATION', fontsize=11, fontweight='bold', color='#C0392B')

ax.add_patch(FancyBboxPatch((2, y_pos-1.4), 6, 1, boxstyle="round,pad=0.1",
                            edgecolor='#C0392B', facecolor='#FADBD8', linewidth=2))
ax.text(5, y_pos-0.5, 'Test Set Performance Metrics', fontsize=9, fontweight='bold', ha='center')
metrics_text = 'Accuracy: 76.40% | Precision: 56.56% | Recall: 48.40%\nF1-Score: 0.5216 | ROC-AUC: 0.7768'
ax.text(5, y_pos-0.95, metrics_text, fontsize=7, ha='center', family='monospace')

add_arrow(ax, 4.5, y_pos-2.3, 4.5, y_pos-1.4, label='Test', color='#C0392B')

# PHASE 8: MODEL SERIALIZATION
y_pos = 1.5
ax.text(2, y_pos+0.3, 'PHASE 8: SERIALIZATION', fontsize=11, fontweight='bold', color='#8E44AD')

add_pipeline_box(ax, 2, y_pos-0.8, 2.5, 0.6, 'Save Model\n.pkl file', '#8E44AD', 8)

add_arrow(ax, 5, y_pos+0.8, 2.5, y_pos-0.4, color='#8E44AD')

# PHASE 9: PRODUCTION DEPLOYMENT
ax.text(7.5, y_pos+0.3, 'PHASE 9: DEPLOYMENT & INFERENCE', fontsize=11, fontweight='bold', color='#16A085')

deployment_boxes = [
    ('Streamlit\nWeb UI', 6, y_pos-1.2, '#FF6B6B'),
    ('FastAPI\nREST API', 7.5, y_pos-1.2, '#4ECDC4'),
    ('Real-Time\nPredictions', 9, y_pos-1.2, '#95E1D3')
]

for box_text, x, y, color in deployment_boxes:
    add_pipeline_box(ax, x, y, 1.2, 0.6, box_text, color, 8)
    if x > 6:
        add_arrow(ax, x-0.7, y, x-0.3, y, color='#333')

add_arrow(ax, 2, y_pos-1.4, 5.3, y_pos-1, label='Load Model', color='#8E44AD')

# Add legend
ax.text(0.5, 0.1, '✓ Full pipeline ensures data quality, model validation, and proper deployment', 
        fontsize=9, style='italic', bbox=dict(boxstyle='round', facecolor='#D5F4E6', alpha=0.7))

plt.tight_layout()
save_diagram_outputs(fig, 'End_to_End_Pipeline.png')
print("✓ Saved: End_to_End_Pipeline.png")
plt.close()

# ============================================================================
# DIAGRAM 3: INFERENCE PIPELINE
# ============================================================================
print("Creating Inference Pipeline Diagram...")

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'Real-Time Inference Pipeline',
        fontsize=16, fontweight='bold', ha='center')
ax.text(5, 9, 'How the Model Makes Predictions in Production',
        fontsize=11, ha='center', style='italic', color='#666')

# INPUT - Customer Data
y = 8
ax.add_patch(FancyBboxPatch((0.5, y-0.7), 2.5, 0.8, boxstyle="round,pad=0.1",
                            edgecolor='#FF6B6B', facecolor='#FFE5E5', linewidth=2.5))
ax.text(1.75, y-0.3, '1. CUSTOMER INPUT', fontsize=10, fontweight='bold', ha='center')
ax.text(1.75, y-0.6, 'Tenure, Charges,\nServices, Contract',
        fontsize=8, ha='center')

add_arrow(ax, 3, y-0.3, 3.8, y-0.3, label='18 fields', color='#FF6B6B')

# FEATURE EXTRACTION
ax.add_patch(FancyBboxPatch((3.8, y-0.7), 2, 0.8, boxstyle="round,pad=0.1",
                            edgecolor='#F39C12', facecolor='#FEF5E7', linewidth=2.5))
ax.text(4.8, y-0.3, '2. FEATURE\nEXTRACTION', fontsize=10, fontweight='bold', ha='center')

add_arrow(ax, 5.8, y-0.3, 6.8, y-0.3, label='30 features', color='#F39C12')

# PREPROCESSING
ax.add_patch(FancyBboxPatch((6.8, y-0.7), 2.5, 0.8, boxstyle="round,pad=0.1",
                            edgecolor='#27AE60', facecolor='#E8F8F5', linewidth=2.5))
ax.text(8.05, y-0.3, '3. PREPROCESSING', fontsize=10, fontweight='bold', ha='center')
ax.text(8.05, y-0.6, 'Scaling, Encoding',
        fontsize=8, ha='center')

add_arrow(ax, 8.05, y-0.7, 8.05, y-1.4, color='#333')

# MODEL INFERENCE
y = 6.3
ax.add_patch(FancyBboxPatch((3.5, y-1), 3, 1.2, boxstyle="round,pad=0.1",
                            edgecolor='#667eea', facecolor='#F0F4FF', linewidth=3))
ax.text(5, y-0.2, '4. MODEL INFERENCE', fontsize=11, fontweight='bold', ha='center')
ax.text(5, y-0.55, 'MLPClassifier Forward Pass', fontsize=9, ha='center', style='italic')
ax.text(5, y-0.85, 'Input (30) → Hidden (32,16,8) → Output (2)',
        fontsize=8, ha='center', family='monospace')

# PREDICTIONS OUTPUT
y = 4.8
# Left branch - prediction
ax.add_patch(FancyBboxPatch((1, y-0.8), 2.5, 0.9, boxstyle="round,pad=0.1",
                            edgecolor='#E74C3C', facecolor='#FADBD8', linewidth=2))
ax.text(2.25, y-0.25, 'Churn Prediction', fontsize=10, fontweight='bold', ha='center')
ax.text(2.25, y-0.55, 'Binary: Yes (1) / No (0)', fontsize=8, ha='center')
ax.text(2.25, y-0.75, 'Confidence: 78%', fontsize=8, ha='center', fontweight='bold', color='#E74C3C')

add_arrow(ax, 5, y_pos-1.4, 2.25, y+0.05, color='#333')

# Middle branch - probability
ax.add_patch(FancyBboxPatch((4, y-0.8), 2.5, 0.9, boxstyle="round,pad=0.1",
                            edgecolor='#3498DB', facecolor='#D6EAF8', linewidth=2))
ax.text(5.25, y-0.25, 'Probabilities', fontsize=10, fontweight='bold', ha='center')
ax.text(5.25, y-0.55, 'P(Churn): 0.32', fontsize=8, ha='center')
ax.text(5.25, y-0.75, 'P(NoChurn): 0.68', fontsize=8, ha='center')

add_arrow(ax, 5, 6.3-1, 5.25, y+0.05, color='#333')

# Right branch - risk
ax.add_patch(FancyBboxPatch((7, y-0.8), 2.5, 0.9, boxstyle="round,pad=0.1",
                            edgecolor='#F39C12', facecolor='#FCF3CF', linewidth=2))
ax.text(8.25, y-0.25, 'Risk Level', fontsize=10, fontweight='bold', ha='center')
ax.text(8.25, y-0.55, 'Classification', fontsize=8, ha='center')
ax.text(8.25, y-0.75, 'LOW / MEDIUM / HIGH', fontsize=8, ha='center', fontweight='bold', color='#F39C12')

add_arrow(ax, 5, 6.3-1, 8.25, y+0.05, color='#333')

# DELIVERY CHANNELS
y = 3
channel_text = '5. DELIVER PREDICTIONS VIA'
ax.text(5, y+0.3, channel_text, fontsize=11, fontweight='bold', ha='center', color='#2C3E50')

channels = [
    ('Streamlit\nWeb Interface', 2, y-1, '#FF6B6B'),
    ('REST API\n(FastAPI)', 5, y-1, '#4ECDC4'),
    ('Database\nStorage', 8, y-1, '#95E1D3')
]

for channel_text, x, y_val, color in channels:
    ax.add_patch(FancyBboxPatch((x-0.9, y_val-0.5), 1.8, 0.7, boxstyle="round,pad=0.05",
                                edgecolor=color, facecolor=color, linewidth=1.5, alpha=0.25))
    ax.text(x, y_val-0.15, channel_text, fontsize=8, fontweight='bold', ha='center', va='center')

# RESPONSE FORMAT
y = 1.2
ax.add_patch(FancyBboxPatch((0.5, y-0.8), 9, 0.9, boxstyle="round,pad=0.1",
                            edgecolor='#16A085', facecolor='#D5F4E6', linewidth=2))
ax.text(5, y-0.1, '6. RESPONSE FORMAT (JSON)', fontsize=10, fontweight='bold', ha='center')
response_text = '{"prediction": 1, "churn_probability": 0.32, "risk_level": "MEDIUM", "confidence": 0.78, "timestamp": "2024-05-10T..."}'
ax.text(5, y-0.55, response_text, fontsize=7, ha='center', family='monospace',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

plt.tight_layout()
save_diagram_outputs(fig, 'Inference_Pipeline.png')
print("✓ Saved: Inference_Pipeline.png")
plt.close()

print("\n✅ All pipeline diagrams created successfully!")
print("   - ML_Methodology_Diagram.png")
print("   - End_to_End_Pipeline.png")
print("   - Inference_Pipeline.png")
