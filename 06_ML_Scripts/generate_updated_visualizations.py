"""Generate updated charts for the reduced-feature churn model."""

import json
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from reduced_model_utils import prepare_reduced_model_input

sns.set_theme(style="whitegrid")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT, "03_Visualizations_Charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_PATH = os.path.join(ROOT, "07_Models_Trained", "final_optimized_churn_model_reduced.pkl")
METADATA_PATH = os.path.join(ROOT, "07_Models_Trained", "model_metadata.json")
TRAIN_PATH = os.path.join(ROOT, "05_Data_Splits", "training_split.csv")
TEST_PATH = os.path.join(ROOT, "05_Data_Splits", "test_split.csv")

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]

with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

target_col = "Churn_Yes" if "Churn_Yes" in test_df.columns else "Churn"
y_raw = test_df[target_col]
if y_raw.dtype == object:
    y_true = y_raw.astype(str)
else:
    y_true = y_raw.copy()

rows = [
    prepare_reduced_model_input(rec, features).iloc[0].to_dict()
    for rec in test_df[features].to_dict(orient="records")
]
X = pd.DataFrame(rows, columns=features)
X_scaled = scaler.transform(X)

y_pred = model.predict(X_scaled)
proba = model.predict_proba(X_scaled)
yes_idx = list(model.classes_).index("Yes") if "Yes" in model.classes_ else 1
y_prob_yes = proba[:, yes_idx]

y_true_bin = (y_true == "Yes").astype(int)
y_pred_bin = (pd.Series(y_pred) == "Yes").astype(int)

accuracy = accuracy_score(y_true_bin, y_pred_bin)
precision = precision_score(y_true_bin, y_pred_bin, zero_division=0)
recall = recall_score(y_true_bin, y_pred_bin, zero_division=0)
f1 = f1_score(y_true_bin, y_pred_bin, zero_division=0)
roc_auc = roc_auc_score(y_true_bin, y_prob_yes)

# 1) Updated model metrics bar
metrics_df = pd.DataFrame(
    {
        "Metric": ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        "Value": [accuracy, precision, recall, f1, roc_auc],
    }
)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=metrics_df, x="Metric", y="Value", palette=["#0284c7", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed"], ax=ax)
ax.set_ylim(0, 1)
ax.set_title("Updated Evaluation Metrics (Reduced 12-Feature Model)")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "updated_01_metrics_bar.png"), dpi=300)
plt.close(fig)

# 2) Confusion matrix
cm = confusion_matrix(y_true_bin, y_pred_bin)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax)
ax.set_title("Updated Confusion Matrix (Test Split)")
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
ax.set_xticklabels(["No", "Yes"])
ax.set_yticklabels(["No", "Yes"])
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "updated_02_confusion_matrix.png"), dpi=300)
plt.close(fig)

# 3) ROC curve
fpr, tpr, _ = roc_curve(y_true_bin, y_prob_yes)
fig, ax = plt.subplots(figsize=(6, 5))
ax.plot(fpr, tpr, color="#0284c7", linewidth=2, label=f"AUC = {roc_auc:.3f}")
ax.plot([0, 1], [0, 1], "--", color="#94a3b8")
ax.set_title("Updated ROC Curve")
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "updated_03_roc_curve.png"), dpi=300)
plt.close(fig)

# 4) Probability distribution
prob_df = pd.DataFrame({"prob_yes": y_prob_yes, "actual": y_true_bin})
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(data=prob_df, x="prob_yes", hue="actual", bins=20, kde=True, palette=["#0284c7", "#dc2626"], ax=ax)
ax.set_title("Updated Churn Probability Distribution")
ax.set_xlabel("Predicted probability of churn")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "updated_04_probability_distribution.png"), dpi=300)
plt.close(fig)

# 5) Feature selection impact
orig_count = len([c for c in train_df.columns if c not in ["Churn", "Churn_Yes", "customerID"]])
selected_count = len(features)
removed_count = max(orig_count - selected_count, 0)

impact_df = pd.DataFrame(
    {
        "Category": ["Selected Features", "Removed Features"],
        "Count": [selected_count, removed_count],
    }
)
fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=impact_df, x="Category", y="Count", palette=["#16a34a", "#dc2626"], ax=ax)
ax.set_title("Feature Selection Impact")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "updated_05_feature_selection_impact.png"), dpi=300)
plt.close(fig)

# 6) Permutation importance
perm = permutation_importance(
    model,
    X_scaled,
    y_true_bin,
    n_repeats=5,
    random_state=42,
    scoring="roc_auc",
)
importance_df = pd.DataFrame({"Feature": features, "Importance": perm.importances_mean}).sort_values("Importance", ascending=False)

fig, ax = plt.subplots(figsize=(9, 6))
sns.barplot(data=importance_df, x="Importance", y="Feature", palette="viridis", ax=ax)
ax.set_title("Updated Permutation Feature Importance (Top 12)")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "updated_06_permutation_importance.png"), dpi=300)
plt.close(fig)

# 7) Class balance (test split)
class_counts = pd.Series(y_true).value_counts()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(
    class_counts.values,
    labels=class_counts.index,
    autopct="%1.1f%%",
    colors=["#0284c7", "#dc2626"],
    startangle=90,
)
ax.set_title("Updated Class Distribution (Test Split)")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "updated_07_class_distribution.png"), dpi=300)
plt.close(fig)

summary_path = os.path.join(ROOT, "01_Documentation", "updated_visualization_summary.txt")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("UPDATED VISUALIZATION SUMMARY\n")
    f.write("=" * 40 + "\n")
    f.write(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1 Score: {f1:.4f}\n")
    f.write(f"ROC-AUC: {roc_auc:.4f}\n")
    f.write(f"Original features: {orig_count}\n")
    f.write(f"Selected features: {selected_count}\n")
    f.write(f"Removed features: {removed_count}\n")
    f.write("\nGenerated chart files:\n")
    for name in sorted([n for n in os.listdir(OUTPUT_DIR) if n.startswith("updated_") and n.endswith(".png")]):
        f.write(f"- {name}\n")

print("Updated visualizations generated successfully.")
