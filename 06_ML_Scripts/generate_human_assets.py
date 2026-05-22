"""Generate human-style diagrams and refreshed charts, removing old visual assets first."""

import json
import os
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
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

ROOT = Path(__file__).resolve().parents[1]
DIAG_DIR = ROOT / "02_Diagrams_Methodology"
DOC_DIAG_DIR = ROOT / "docs" / "diagrams"
DOC_PNG_DIR = DOC_DIAG_DIR / "png"
DOC_SVG_DIR = DOC_DIAG_DIR / "svg"
CHART_DIR = ROOT / "03_Visualizations_Charts"
DOC_DIR = ROOT / "01_Documentation"

MODEL_PATH = ROOT / "07_Models_Trained" / "final_optimized_churn_model_reduced.pkl"
METADATA_PATH = ROOT / "07_Models_Trained" / "model_metadata.json"
TRAIN_PATH = ROOT / "05_Data_Splits" / "training_split.csv"
TEST_PATH = ROOT / "05_Data_Splits" / "test_split.csv"


def clean_old_assets() -> None:
    for folder in [DIAG_DIR, CHART_DIR, DOC_PNG_DIR, DOC_SVG_DIR]:
        if folder.exists():
            for file in folder.iterdir():
                if file.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".md"}:
                    file.unlink(missing_ok=True)


def export_diagram_files(fig, legacy_path: Path) -> None:
    legacy_path.parent.mkdir(parents=True, exist_ok=True)
    DOC_PNG_DIR.mkdir(parents=True, exist_ok=True)
    DOC_SVG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(legacy_path, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(DOC_PNG_DIR / legacy_path.name, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(DOC_SVG_DIR / f"{legacy_path.stem}.svg", format="svg", bbox_inches="tight", facecolor="white")


def draw_node(ax, xy, text, color="#e2e8f0", edge="#334155", w=0.16, h=0.1):
    x, y = xy
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.7,
        edgecolor=edge,
        facecolor=color,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=9, weight="bold", color="#0f172a")


def draw_arrow(ax, start, end, color="#475569"):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.6,
        color=color,
        connectionstyle="arc3,rad=0.0",
    )
    ax.add_patch(arrow)


def save_diagram(title, nodes, arrows, path, figsize=(14, 6), bg="#ffffff"):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(bg)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.5, 0.95, title, ha="center", va="center", fontsize=16, weight="bold", color="#0f172a")

    for node in nodes:
        draw_node(ax, **node)

    for a in arrows:
        draw_arrow(ax, a[0], a[1])

    fig.tight_layout()
    export_diagram_files(fig, path)
    plt.close(fig)


def generate_diagrams() -> None:
    # Methodology
    nodes = [
        {"xy": (0.10, 0.55), "text": "Raw Data", "color": "#dbeafe", "edge": "#1d4ed8"},
        {"xy": (0.25, 0.55), "text": "Cleaning\nValidation", "color": "#e0f2fe", "edge": "#0369a1"},
        {"xy": (0.40, 0.55), "text": "Split\nTrain/Val/Test", "color": "#dcfce7", "edge": "#15803d"},
        {"xy": (0.55, 0.55), "text": "Feature\nSelection (12)", "color": "#fef3c7", "edge": "#b45309"},
        {"xy": (0.70, 0.55), "text": "Scaler +\nMLP Training", "color": "#fee2e2", "edge": "#b91c1c"},
        {"xy": (0.85, 0.55), "text": "Evaluation +\nDeployment", "color": "#ede9fe", "edge": "#6d28d9"},
    ]
    arrows = [
        ((0.17, 0.55), (0.18, 0.55)),
        ((0.32, 0.55), (0.33, 0.55)),
        ((0.47, 0.55), (0.48, 0.55)),
        ((0.62, 0.55), (0.63, 0.55)),
        ((0.77, 0.55), (0.78, 0.55)),
    ]
    save_diagram(
        "Methodology Diagram - Corrected Flow",
        nodes,
        arrows,
        DIAG_DIR / "methodology_diagram_human.png",
    )

    # System Architecture
    nodes = [
        {"xy": (0.20, 0.75), "text": "Streamlit UI", "color": "#dbeafe", "edge": "#1d4ed8"},
        {"xy": (0.20, 0.35), "text": "FastAPI", "color": "#dcfce7", "edge": "#15803d"},
        {"xy": (0.50, 0.55), "text": "Preprocessing\nMapping + Scaling", "color": "#fef3c7", "edge": "#b45309"},
        {"xy": (0.75, 0.55), "text": "MLP Model\n(12 Features)", "color": "#fee2e2", "edge": "#b91c1c"},
        {"xy": (0.50, 0.15), "text": "Model/Metadata\nStorage", "color": "#e2e8f0", "edge": "#475569"},
    ]
    arrows = [
        ((0.28, 0.73), (0.42, 0.58)),
        ((0.28, 0.37), (0.42, 0.52)),
        ((0.58, 0.55), (0.67, 0.55)),
        ((0.67, 0.50), (0.58, 0.50)),
        ((0.50, 0.22), (0.50, 0.45)),
        ((0.58, 0.22), (0.72, 0.48)),
    ]
    save_diagram(
        "System Architecture Diagram - Corrected",
        nodes,
        arrows,
        DIAG_DIR / "system_architecture_diagram_human.png",
    )

    # Data Flow
    nodes = [
        {"xy": (0.10, 0.5), "text": "Input", "color": "#dbeafe", "edge": "#1d4ed8", "w": 0.12},
        {"xy": (0.25, 0.5), "text": "Validate", "color": "#e0f2fe", "edge": "#0369a1", "w": 0.12},
        {"xy": (0.40, 0.5), "text": "Map\nFeatures", "color": "#fef3c7", "edge": "#b45309", "w": 0.14},
        {"xy": (0.55, 0.5), "text": "Scale", "color": "#fee2e2", "edge": "#b91c1c", "w": 0.12},
        {"xy": (0.70, 0.5), "text": "Predict", "color": "#ede9fe", "edge": "#6d28d9", "w": 0.12},
        {"xy": (0.85, 0.5), "text": "Risk Output\nG/O/R", "color": "#dcfce7", "edge": "#15803d", "w": 0.14},
    ]
    arrows = [
        ((0.16, 0.5), (0.19, 0.5)),
        ((0.31, 0.5), (0.34, 0.5)),
        ((0.47, 0.5), (0.49, 0.5)),
        ((0.61, 0.5), (0.64, 0.5)),
        ((0.76, 0.5), (0.78, 0.5)),
    ]
    save_diagram(
        "Data Flow Diagram - Corrected",
        nodes,
        arrows,
        DIAG_DIR / "data_flow_diagram_human.png",
    )

    # Inference pipeline
    nodes = [
        {"xy": (0.12, 0.5), "text": "Receive\nInput", "color": "#dbeafe", "edge": "#1d4ed8", "w": 0.13},
        {"xy": (0.29, 0.5), "text": "Validate\nFields", "color": "#e0f2fe", "edge": "#0369a1", "w": 0.13},
        {"xy": (0.46, 0.5), "text": "Feature\nMapping", "color": "#fef3c7", "edge": "#b45309", "w": 0.13},
        {"xy": (0.63, 0.5), "text": "Scaler\nTransform", "color": "#fee2e2", "edge": "#b91c1c", "w": 0.13},
        {"xy": (0.80, 0.5), "text": "MLP\nProbability", "color": "#ede9fe", "edge": "#6d28d9", "w": 0.13},
    ]
    arrows = [
        ((0.18, 0.5), (0.22, 0.5)),
        ((0.35, 0.5), (0.39, 0.5)),
        ((0.52, 0.5), (0.56, 0.5)),
        ((0.69, 0.5), (0.73, 0.5)),
    ]
    save_diagram(
        "Inference Pipeline Diagram - Corrected",
        nodes,
        arrows,
        DIAG_DIR / "inference_pipeline_diagram_human.png",
    )

    # End-to-end
    nodes = [
        {"xy": (0.10, 0.7), "text": "Raw Data", "color": "#dbeafe", "edge": "#1d4ed8"},
        {"xy": (0.28, 0.7), "text": "Preprocess", "color": "#e0f2fe", "edge": "#0369a1"},
        {"xy": (0.46, 0.7), "text": "Train +\nSelect Features", "color": "#fef3c7", "edge": "#b45309"},
        {"xy": (0.64, 0.7), "text": "Evaluate", "color": "#fee2e2", "edge": "#b91c1c"},
        {"xy": (0.82, 0.7), "text": "Deploy", "color": "#ede9fe", "edge": "#6d28d9"},
        {"xy": (0.64, 0.35), "text": "Charts +\nDiagrams", "color": "#dcfce7", "edge": "#15803d"},
    ]
    arrows = [
        ((0.17, 0.7), (0.21, 0.7)),
        ((0.35, 0.7), (0.39, 0.7)),
        ((0.53, 0.7), (0.57, 0.7)),
        ((0.71, 0.7), (0.75, 0.7)),
        ((0.64, 0.62), (0.64, 0.43)),
    ]
    save_diagram(
        "End-to-End Pipeline Diagram - Corrected",
        nodes,
        arrows,
        DIAG_DIR / "end_to_end_pipeline_diagram_human.png",
    )


def generate_charts() -> dict:
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
    prob = model.predict_proba(X_scaled)
    yes_idx = list(model.classes_).index("Yes") if "Yes" in model.classes_ else 1
    y_prob = prob[:, yes_idx]

    y_true_bin = (y_true == "Yes").astype(int)
    y_pred_bin = (pd.Series(y_pred) == "Yes").astype(int)

    accuracy = accuracy_score(y_true_bin, y_pred_bin)
    precision = precision_score(y_true_bin, y_pred_bin, zero_division=0)
    recall = recall_score(y_true_bin, y_pred_bin, zero_division=0)
    f1 = f1_score(y_true_bin, y_pred_bin, zero_division=0)
    roc_auc = roc_auc_score(y_true_bin, y_prob)

    # Metrics chart
    metric_df = pd.DataFrame(
        {
            "Metric": ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
            "Value": [accuracy, precision, recall, f1, roc_auc],
        }
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=metric_df, x="Metric", y="Value", palette=["#0284c7", "#16a34a", "#ea580c", "#dc2626", "#7c3aed"], ax=ax)
    ax.set_ylim(0, 1)
    ax.set_title("Model Performance Metrics (Reduced 12-Feature Model)")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "human_01_model_metrics.png", dpi=300)
    plt.close(fig)

    # Confusion matrix
    cm = confusion_matrix(y_true_bin, y_pred_bin)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax)
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticklabels(["No", "Yes"])
    ax.set_yticklabels(["No", "Yes"])
    fig.tight_layout()
    fig.savefig(CHART_DIR / "human_02_confusion_matrix.png", dpi=300)
    plt.close(fig)

    # ROC curve
    fpr, tpr, _ = roc_curve(y_true_bin, y_prob)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, color="#0284c7", linewidth=2, label=f"AUC = {roc_auc:.3f}")
    ax.plot([0, 1], [0, 1], "--", color="#94a3b8")
    ax.set_title("ROC Curve")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "human_03_roc_curve.png", dpi=300)
    plt.close(fig)

    # Probability distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(pd.DataFrame({"prob": y_prob, "actual": y_true_bin}), x="prob", hue="actual", bins=20, kde=True, palette=["#0284c7", "#dc2626"], ax=ax)
    ax.set_title("Predicted Churn Probability Distribution")
    ax.set_xlabel("P(churn)")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "human_04_probability_distribution.png", dpi=300)
    plt.close(fig)

    # Feature selection impact
    original = len([c for c in train_df.columns if c not in ["customerID", "Churn", "Churn_Yes"]])
    selected = len(features)
    removed = max(original - selected, 0)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=pd.DataFrame({"Type": ["Selected", "Removed"], "Count": [selected, removed]}),
        x="Type",
        y="Count",
        palette=["#16a34a", "#dc2626"],
        ax=ax,
    )
    ax.set_title("Feature Selection Impact")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "human_05_feature_selection_impact.png", dpi=300)
    plt.close(fig)

    # Permutation importance
    perm = permutation_importance(model, X_scaled, y_true_bin, n_repeats=5, random_state=42, scoring="roc_auc")
    imp_df = pd.DataFrame({"Feature": features, "Importance": perm.importances_mean}).sort_values("Importance", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.barplot(data=imp_df, x="Importance", y="Feature", palette="viridis", ax=ax)
    ax.set_title("Permutation Importance (12 Features)")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "human_06_permutation_importance.png", dpi=300)
    plt.close(fig)

    # Class distribution
    counts = pd.Series(y_true).value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90, colors=["#0284c7", "#dc2626"])
    ax.set_title("Class Distribution (Test Split)")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "human_07_class_distribution.png", dpi=300)
    plt.close(fig)

    summary = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "original_features": original,
        "selected_features": selected,
        "removed_features": removed,
        "metadata_accuracy": metadata.get("model_accuracy", "N/A"),
    }
    return summary


def write_summary(summary: dict) -> None:
    out = DOC_DIR / "updated_visualization_summary.txt"
    with out.open("w", encoding="utf-8") as f:
        f.write("HUMAN-STYLE VISUALIZATION SUMMARY\n")
        f.write("=" * 44 + "\n")
        f.write(f"Accuracy: {summary['accuracy']:.4f} ({summary['accuracy']*100:.2f}%)\n")
        f.write(f"Precision: {summary['precision']:.4f}\n")
        f.write(f"Recall: {summary['recall']:.4f}\n")
        f.write(f"F1 Score: {summary['f1']:.4f}\n")
        f.write(f"ROC-AUC: {summary['roc_auc']:.4f}\n")
        f.write(f"Original features: {summary['original_features']}\n")
        f.write(f"Selected features: {summary['selected_features']}\n")
        f.write(f"Removed features: {summary['removed_features']}\n")


def main() -> None:
    clean_old_assets()
    generate_diagrams()
    summary = generate_charts()
    write_summary(summary)
    print("Human-style diagrams and charts generated successfully.")


if __name__ == "__main__":
    main()
