"""Utilities for preparing inputs for the reduced churn model."""

from __future__ import annotations

from typing import Any, Dict, Iterable

import pandas as pd


CONTRACT_MAP = {
    "Month-to-month": 0.0,
    "Two year": 0.5,
    "One year": 1.0,
}

PAYMENT_METHOD_MAP = {
    "Electronic check": 1.0,
    "Mailed check": 0.5,
    "Bank transfer": 0.75,
    "Bank transfer (automatic)": 0.75,
    "Credit card": 0.25,
    "Credit card (automatic)": 0.25,
}

YES_NO_MAP = {
    "No": 0.0,
    "Yes": 1.0,
}

GENDER_MAP = {
    "Female": 0.0,
    "Male": 1.0,
}

INTERNET_SERVICE_MAP = {
    "No": 0.0,
    "DSL": 0.5,
    "Fiber optic": 1.0,
}

FEATURE_MAPS = {
    "Contract": CONTRACT_MAP,
    "PaymentMethod": PAYMENT_METHOD_MAP,
    "TechSupport": YES_NO_MAP,
    "OnlineSecurity": YES_NO_MAP,
    "PaperlessBilling": YES_NO_MAP,
    "InternetService": INTERNET_SERVICE_MAP,
    "gender": GENDER_MAP,
    "OnlineBackup": YES_NO_MAP,
    "MultipleLines": YES_NO_MAP,
}

NUMERIC_COLUMNS = {"TotalCharges", "MonthlyCharges", "tenure"}


def _normalize_value(feature_name: str, value: Any) -> float:
    if feature_name in NUMERIC_COLUMNS:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    mapping = FEATURE_MAPS.get(feature_name)
    if mapping is None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    if value in mapping:
        return float(mapping[value])

    # Allow a few common synonyms without forcing the caller to use exact labels.
    if feature_name == "PaymentMethod" and isinstance(value, str):
        lowered = value.lower()
        if "electronic" in lowered:
            return 1.0
        if "mailed" in lowered:
            return 0.5
        if "bank" in lowered:
            return 0.75
        if "credit" in lowered:
            return 0.25

    return 0.0


def prepare_reduced_model_input(input_data: Dict[str, Any], feature_order: Iterable[str]) -> pd.DataFrame:
    """Create a numeric DataFrame matching the reduced model's expected feature order."""
    row = {}
    for feature_name in feature_order:
        row[feature_name] = _normalize_value(feature_name, input_data.get(feature_name, 0.0))
    return pd.DataFrame([row], columns=list(feature_order))
