"""Shared evaluation helpers for the Streamlit app and regression tests."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve

from reduced_model_utils import prepare_reduced_model_input


def evaluate_bundle(_bundle, test_df):
    model = _bundle["model"]
    scaler = _bundle["scaler"]
    features = _bundle["features"]

    target_col = "Churn_Yes" if "Churn_Yes" in test_df.columns else "Churn"
    y_raw = test_df[target_col]
    if y_raw.dtype == object:
        y_true = y_raw.astype(str)
    else:
        y_true = y_raw.map({0: "No", 1: "Yes"}).fillna("No")

    x_rows = [prepare_reduced_model_input(row, features).iloc[0].to_dict() for row in test_df[features].to_dict(orient="records")]
    x_df = pd.DataFrame(x_rows, columns=features)
    x_scaled = scaler.transform(x_df)

    y_pred = model.predict(x_scaled)
    proba = model.predict_proba(x_scaled)
    yes_idx = list(model.classes_).index("Yes") if "Yes" in model.classes_ else 1
    y_prob = proba[:, yes_idx]

    y_true_bin = (y_true == "Yes").astype(int)
    y_pred_bin = (pd.Series(y_pred) == "Yes").astype(int)

    accuracy = accuracy_score(y_true_bin, y_pred_bin)
    precision = precision_score(y_true_bin, y_pred_bin, zero_division=0)
    recall = recall_score(y_true_bin, y_pred_bin, zero_division=0)
    f1 = f1_score(y_true_bin, y_pred_bin, zero_division=0)

    if y_true_bin.nunique() < 2 or y_true_bin.sum() == 0:
        roc_auc = float("nan")
        fpr, tpr = [], []
    else:
        roc_auc = roc_auc_score(y_true_bin, y_prob)
        fpr, tpr, _ = roc_curve(y_true_bin, y_prob)

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
    }

    cm = confusion_matrix(y_true_bin, y_pred_bin, labels=[0, 1])
    return metrics, cm, fpr, tpr, y_prob