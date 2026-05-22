"""
Customer Churn ML - High-Quality Individual Visualizations
Generates separate, clear, professional charts for easy viewing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

print("Generating individual high-quality visualizations...\n")

# ============================================================================
# VISUALIZATION 1: Model Performance Comparison (Large, Clear)
# ============================================================================
print("[1/7] Creating Model Performance Comparison...")

fig, ax = plt.subplots(figsize=(14, 8))

models = ['Initial Model\n(16,8)', 'Tuned Model\n(32,16)', 'Final Optimized\n(32,16,8)']
x_pos = np.arange(len(models))
width = 0.15

metrics_data = {
    'Accuracy': [0.7740, 0.7732, 0.7640],
    'ROC-AUC': [0.7654, 0.7709, 0.7768],
    'Precision': [0.5897, 0.5821, 0.5656],
    'Recall': [0.5134, 0.5188, 0.4840],
    'F1-Score': [0.5490, 0.5488, 0.5216]
}

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#95E1D3', '#FFE66D']

for i, (metric, values) in enumerate(metrics_data.items()):
    offset = (i - 2) * width
    bars = ax.bar(x_pos + offset, values, width, label=metric, color=colors[i], 
                   alpha=0.85, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_xlabel('Model Architecture', fontsize=14, fontweight='bold')
ax.set_ylabel('Score', fontsize=14, fontweight='bold')
ax.set_title('Comprehensive Model Performance Comparison\n(All Metrics Across Models)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(models, fontsize=12, fontweight='bold')
ax.legend(fontsize=11, loc='upper right', framealpha=0.95)
ax.set_ylim([0.4, 0.8])
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('01_model_performance_comparison.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 01_model_performance_comparison.png")
plt.close()

# ============================================================================
# VISUALIZATION 2: Accuracy Trend Across Models
# ============================================================================
print("[2/7] Creating Accuracy Trend Chart...")

fig, ax = plt.subplots(figsize=(12, 7))

model_names = ['Initial\n(16,8)', 'Tuned\n(32,16)', 'Optimized\n(32,16,8)']
accuracies = [0.7740, 0.7732, 0.7640]
colors_trend = ['#FF6B6B', '#FFB347', '#45B7D1']

bars = ax.bar(model_names, accuracies, color=colors_trend, alpha=0.85, 
              edgecolor='black', linewidth=2.5, width=0.6)

# Add value labels
for i, (bar, acc) in enumerate(zip(bars, accuracies)):
    ax.text(i, acc + 0.001, f'{acc:.2%}', ha='center', va='bottom', 
            fontsize=13, fontweight='bold', color='darkred')

ax.axhline(y=0.77, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Baseline (77%)')
ax.set_ylabel('Accuracy Score', fontsize=13, fontweight='bold')
ax.set_title('Model Accuracy Evolution\n(Higher is Better)', fontsize=15, fontweight='bold', pad=20)
ax.set_ylim([0.75, 0.785])
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('02_accuracy_trend.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 02_accuracy_trend.png")
plt.close()

# ============================================================================
# VISUALIZATION 3: Confusion Matrix - Large Clear Version
# ============================================================================
print("[3/7] Creating Confusion Matrix...")

fig, ax = plt.subplots(figsize=(10, 8))

cm_data = np.array([[897, 136], [182, 192]])
sns.heatmap(cm_data, annot=True, fmt='d', cmap='Blues', ax=ax, 
            cbar_kws={'label': 'Number of Predictions', 'shrink': 0.8},
            xticklabels=['Predicted:\nNo Churn', 'Predicted:\nChurn'],
            yticklabels=['Actual:\nNo Churn', 'Actual:\nChurn'],
            linewidths=3, linecolor='black', square=True,
            annot_kws={'size': 16, 'weight': 'bold', 'color': 'darkblue'})

ax.set_title('Confusion Matrix - Final Optimized Model\n(Churn Prediction Results)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_ylabel('Actual Label', fontsize=12, fontweight='bold')
ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')

# Add accuracy metrics as text
total = cm_data.sum()
tn, fp, fn, tp = cm_data[0,0], cm_data[0,1], cm_data[1,0], cm_data[1,1]
accuracy = (tp + tn) / total
sensitivity = tp / (tp + fn)
specificity = tn / (tn + fp)

textstr = f'Accuracy: {accuracy:.2%}\nSensitivity: {sensitivity:.2%}\nSpecificity: {specificity:.2%}'
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('03_confusion_matrix_detailed.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 03_confusion_matrix_detailed.png")
plt.close()

# ============================================================================
# VISUALIZATION 4: Feature Importance - Top 15
# ============================================================================
print("[4/7] Creating Feature Importance Chart...")

fig, ax = plt.subplots(figsize=(12, 10))

features = [
    'PaymentMethod_Electronic check', 'gender_Male', 'Contract_One year',
    'PaymentMethod_Credit card (auto)', 'MultipleLines_Yes', 'tenure',
    'SeniorCitizen', 'PaymentMethod_Mailed check', 'TotalCharges',
    'StreamingTV_Yes', 'InternetService_Fiber optic', 'MonthlyCharges',
    'OnlineSecurity_Yes', 'DeviceProtection_Yes', 'OnlineBackup_Yes'
]

importance = [0.2574, 0.2554, 0.2479, 0.2468, 0.2433, 0.2416,
              0.2406, 0.2275, 0.2255, 0.2247, 0.2234, 0.2201, 0.2189, 0.2176, 0.2165]

colors_gradient = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(features)))
bars = ax.barh(range(len(features)), importance, color=colors_gradient, 
               edgecolor='black', linewidth=1.5, height=0.7)

ax.set_yticks(range(len(features)))
ax.set_yticklabels(features, fontsize=10)
ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Feature Importance for Churn Prediction\n(Relative Impact on Model)', 
             fontsize=14, fontweight='bold', pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, imp) in enumerate(zip(bars, importance)):
    ax.text(imp + 0.002, i, f'{imp:.4f}', va='center', fontsize=9, fontweight='bold')

ax.set_xlim([0.21, 0.27])
ax.grid(axis='x', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('04_feature_importance_top15.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 04_feature_importance_top15.png")
plt.close()

# ============================================================================
# VISUALIZATION 5: Hyperparameter Tuning Results Heatmap
# ============================================================================
print("[5/7] Creating Hyperparameter Tuning Heatmap...")

fig, ax = plt.subplots(figsize=(10, 7))

# Create data for heatmap
epochs = [30, 50]
neurons = [16, 32]
accuracy_grid = np.array([[0.7875, 0.7832], [0.7889, 0.7868]])

sns.heatmap(accuracy_grid, annot=True, fmt='.4f', cmap='RdYlGn', ax=ax,
            xticklabels=neurons, yticklabels=epochs,
            cbar_kws={'label': 'Accuracy Score'},
            linewidths=2, linecolor='black',
            annot_kws={'size': 14, 'weight': 'bold'})

ax.set_xlabel('Hidden Layer Neurons', fontsize=12, fontweight='bold')
ax.set_ylabel('Training Epochs', fontsize=12, fontweight='bold')
ax.set_title('Hyperparameter Tuning Results\nAccuracy Across Batch Sizes (Fixed Batch=16)', 
             fontsize=14, fontweight='bold', pad=20)

# Highlight best configuration
best_i, best_j = 1, 0  # 50 epochs, 16 neurons
rect = plt.Rectangle((best_j, best_i), 1, 1, fill=False, edgecolor='red', linewidth=4)
ax.add_patch(rect)
ax.text(best_j + 0.5, best_i - 0.35, '★ BEST', ha='center', fontsize=11, 
        fontweight='bold', color='red')

plt.tight_layout()
plt.savefig('05_hyperparameter_tuning_heatmap.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 05_hyperparameter_tuning_heatmap.png")
plt.close()

# ============================================================================
# VISUALIZATION 6: Model Metrics Radar/Spider Chart
# ============================================================================
print("[6/7] Creating Model Metrics Radar Chart...")

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='polar')

categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
N = len(categories)

# Data for three models
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

initial_values = [0.7740, 0.5897, 0.5134, 0.5490, 0.7654]
tuned_values = [0.7732, 0.5821, 0.5188, 0.5488, 0.7709]
final_values = [0.7640, 0.5656, 0.4840, 0.5216, 0.7768]

initial_values += initial_values[:1]
tuned_values += tuned_values[:1]
final_values += final_values[:1]

ax.plot(angles, initial_values, 'o-', linewidth=2.5, label='Initial (16,8)', color='#FF6B6B', markersize=8)
ax.fill(angles, initial_values, alpha=0.15, color='#FF6B6B')

ax.plot(angles, tuned_values, 's-', linewidth=2.5, label='Tuned (32,16)', color='#4ECDC4', markersize=8)
ax.fill(angles, tuned_values, alpha=0.15, color='#4ECDC4')

ax.plot(angles, final_values, '^-', linewidth=2.5, label='Optimized (32,16,8)', color='#45B7D1', markersize=8)
ax.fill(angles, final_values, alpha=0.15, color='#45B7D1')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8])
ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8'], fontsize=9)
ax.set_title('Model Performance Radar Chart\n(Multi-Metric Comparison)', 
             fontsize=14, fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11, framealpha=0.95)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('06_model_metrics_radar.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 06_model_metrics_radar.png")
plt.close()

# ============================================================================
# VISUALIZATION 7: Class Distribution & ROC-AUC Score Comparison
# ============================================================================
print("[7/7] Creating Class Distribution & ROC-AUC Chart...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Class Distribution
ax = axes[0]
classes = ['No Churn\n(Majority)', 'Churn\n(Minority)']
counts = [5163, 1880]
colors_pie = ['#95E1D3', '#FF6B6B']
wedges, texts, autotexts = ax.pie(counts, labels=classes, autopct='%1.1f%%',
                                    colors=colors_pie, startangle=90,
                                    textprops={'fontsize': 12, 'fontweight': 'bold'},
                                    wedgeprops={'edgecolor': 'black', 'linewidth': 2.5})
ax.set_title('Dataset Class Distribution\n(Target Variable Imbalance)', 
             fontsize=12, fontweight='bold', pad=15)

# Right: ROC-AUC Comparison
ax = axes[1]
models_roc = ['Initial\n(16,8)', 'Tuned\n(32,16)', 'Optimized\n(32,16,8)']
roc_scores = [0.7654, 0.7709, 0.7768]
colors_roc = ['#FF6B6B', '#FFB347', '#45B7D1']

bars = ax.bar(models_roc, roc_scores, color=colors_roc, alpha=0.85,
              edgecolor='black', linewidth=2.5, width=0.6)

# Add values on bars
for i, (bar, score) in enumerate(zip(bars, roc_scores)):
    ax.text(i, score + 0.002, f'{score:.4f}', ha='center', va='bottom',
            fontsize=12, fontweight='bold', color='darkred')

ax.axhline(y=0.75, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Good (0.75)')
ax.axhline(y=0.80, color='blue', linestyle='--', linewidth=2, alpha=0.5, label='Excellent (0.80)')
ax.set_ylabel('ROC-AUC Score', fontsize=12, fontweight='bold')
ax.set_title('ROC-AUC Score Comparison\n(Model Discrimination Ability)', 
             fontsize=12, fontweight='bold', pad=15)
ax.set_ylim([0.75, 0.82])
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('07_class_distribution_and_roc_auc.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 07_class_distribution_and_roc_auc.png")
plt.close()

print("\n" + "="*80)
print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print("="*80)
print("\n📊 Generated Individual Charts:")
print("   01_model_performance_comparison.png")
print("   02_accuracy_trend.png")
print("   03_confusion_matrix_detailed.png")
print("   04_feature_importance_top15.png")
print("   05_hyperparameter_tuning_heatmap.png")
print("   06_model_metrics_radar.png")
print("   07_class_distribution_and_roc_auc.png")
print("\n" + "="*80)
