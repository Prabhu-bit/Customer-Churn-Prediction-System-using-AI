"""Generate the customer churn methodology flow chart as a PNG."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "02_Diagrams_Methodology"
OUT_FILE = OUT_DIR / "customer_churn_flowchart.png"


def box(ax, x, y, w, h, title, body, face, edge, title_color="#0f172a"):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.03,rounding_size=0.03",
        linewidth=2,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=10, weight="bold", color=title_color)
    if body:
        ax.text(x + w / 2, y + h * 0.32, body, ha="center", va="center", fontsize=8, color="#334155")


def arrow(ax, start, end, color="#475569"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=1.8,
            color=color,
        )
    )


def add_layer_label(ax, x, y, text, color="#0f172a"):
    ax.text(x, y, text, ha="left", va="center", fontsize=12, weight="bold", color=color)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(20, 12))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis("off")

    ax.text(10, 11.55, "Customer Churn System Architecture Flow Chart", ha="center", va="center", fontsize=22, weight="bold", color="#0f172a")
    ax.text(10, 11.15, "Input data -> preprocessing -> training -> evaluation -> inference -> connected database", ha="center", va="center", fontsize=11, color="#475569")

    add_layer_label(ax, 0.7, 10.2, "Layer 1 - Input Data", "#1d4ed8")
    box(ax, 0.7, 9.2, 4.0, 0.9, "Customer Churn CSV", "04_Data_Raw/customer_churn.csv\n7,043 records", "#dbeafe", "#2563eb")
    box(ax, 5.4, 9.2, 3.2, 0.9, "Connected Database", "Prediction store", "#f1f5f9", "#64748b")
    arrow(ax, (4.7, 9.65), (5.25, 9.65))
    arrow(ax, (5.4, 9.35), (4.7, 9.35), color="#64748b")

    add_layer_label(ax, 0.7, 8.5, "Layer 2 - Preprocessing and Feature Engineering", "#15803d")
    prep_boxes = [
        (0.7, "Data Inspection and EDA", "missing values\nclass balance\nfeature types", "#ecfdf5", "#16a34a"),
        (4.2, "Encoding and Cleaning", "get_dummies\nbinary mapping\nlabel cleanup", "#ecfdf5", "#16a34a"),
        (7.7, "Feature Scaling", "StandardScaler", "#ecfdf5", "#16a34a"),
        (10.7, "Stratified Splits", "train / validation / test / holdout", "#ecfdf5", "#16a34a"),
    ]
    prep_widths = [3.0, 3.0, 2.6, 4.0]
    for idx, (x, title, body, face, edge) in enumerate(prep_boxes):
        box(ax, x, 7.35, prep_widths[idx], 0.95, title, body, face, edge)
        if idx < len(prep_boxes) - 1:
            arrow(ax, (x + prep_widths[idx], 7.82), (prep_boxes[idx + 1][0] - 0.05, 7.82), color="#16a34a")

    add_layer_label(ax, 0.7, 6.45, "Layer 3 - Model Training", "#c2410c")
    train_boxes = [
        (0.7, 5.3, 4.3, 1.0, "Candidate Model Training", "MLPClassifier configurations", "#fff7ed", "#ea580c"),
        (5.6, 5.3, 4.4, 1.0, "Hyperparameter Tuning", "best setup: (32, 16, 8)\nlr=0.001, max_iter=300, alpha=0.0001", "#fff7ed", "#ea580c"),
        (10.6, 5.3, 3.8, 1.0, "Saved Model Artifact", "final_optimized_churn_model.pkl", "#fff7ed", "#ea580c"),
    ]
    for idx, (x, y, w, h, title, body, face, edge) in enumerate(train_boxes):
        box(ax, x, y, w, h, title, body, face, edge)
        if idx < len(train_boxes) - 1:
            arrow(ax, (x + w, y + h / 2), (train_boxes[idx + 1][0] - 0.08, y + h / 2), color="#ea580c")

    add_layer_label(ax, 0.7, 4.8, "Layer 4 - Evaluation and Model Selection", "#7c3aed")
    eval_boxes = [
        (0.7, 3.65, 4.2, 0.95, "Evaluation Metrics", "Accuracy, Precision, Recall, F1, ROC-AUC", "#f5f3ff", "#7c3aed"),
        (5.4, 3.65, 4.2, 0.95, "Best Model Selection", "optimized MLP chosen for inference", "#f5f3ff", "#7c3aed"),
    ]
    for idx, (x, y, w, h, title, body, face, edge) in enumerate(eval_boxes):
        box(ax, x, y, w, h, title, body, face, edge)
        if idx < len(eval_boxes) - 1:
            arrow(ax, (x + w, y + h / 2), (eval_boxes[idx + 1][0] - 0.08, y + h / 2), color="#7c3aed")

    add_layer_label(ax, 0.7, 2.9, "Layer 5 - Inference and Output", "#be123c")
    infer_boxes = [
        (0.7, 1.75, 3.7, 1.0, "Streamlit App or FastAPI Service", "production interface", "#fff1f2", "#e11d48"),
        (4.9, 1.75, 3.6, 1.0, "New Customer Input", "manual or API request", "#fff1f2", "#e11d48"),
        (9.0, 1.75, 3.9, 1.0, "Preprocessed Inference Vector", "same encoding and scaling rules", "#fff1f2", "#e11d48"),
        (13.4, 1.75, 5.0, 1.0, "Predicted Output", "Churn / No Churn with probability score", "#fff1f2", "#e11d48"),
    ]
    for idx, (x, y, w, h, title, body, face, edge) in enumerate(infer_boxes):
        box(ax, x, y, w, h, title, body, face, edge)
        if idx < len(infer_boxes) - 1:
            arrow(ax, (x + w, y + h / 2), (infer_boxes[idx + 1][0] - 0.08, y + h / 2), color="#e11d48")

    arrow(ax, (8.15, 9.2), (1.55, 8.3), color="#475569")
    arrow(ax, (14.4, 4.15), (15.4, 2.75), color="#7c3aed")
    arrow(ax, (18.3, 2.25), (18.3, 10.0), color="#475569")
    ax.text(18.0, 10.15, "write results", fontsize=8, color="#64748b", ha="right")

    fig.tight_layout()
    fig.savefig(OUT_FILE, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {OUT_FILE}")


if __name__ == "__main__":
    main()