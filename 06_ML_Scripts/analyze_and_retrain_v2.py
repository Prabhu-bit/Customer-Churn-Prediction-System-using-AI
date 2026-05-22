"""
Analyze feature importance and retrain model with top N features
Fixes the 20 vs 30 features mismatch by reducing to important features only
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

# ============================================================================
# PATHS
# ============================================================================

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
training_data_path = os.path.join(project_root, "05_Data_Splits", "training_split.csv")
validation_data_path = os.path.join(project_root, "05_Data_Splits", "validation_split.csv")
test_data_path = os.path.join(project_root, "05_Data_Splits", "test_split.csv")
holdout_data_path = os.path.join(project_root, "05_Data_Splits", "holdout_split.csv")
new_model_path = os.path.join(project_root, "07_Models_Trained", "final_optimized_churn_model_reduced.pkl")

# ============================================================================
# LOAD AND PREPROCESS DATA
# ============================================================================

def preprocess_data(df):
    df = df.copy()
    if 'customerID' in df.columns: df = df.drop(columns=['customerID'])
    if 'TotalCharges' in df.columns: 
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    
    # Simple label encoding for remaining categorical columns
    for col in df.select_dtypes(include=['object']).columns:
        if col not in ['Churn', 'Churn_Yes']:
            df[col] = df[col].astype('category').cat.codes
            
    # Map target
    target = 'Churn_Yes' if 'Churn_Yes' in df.columns else 'Churn'
    if target in df.columns and df[target].dtype == 'object':
        df[target] = df[target].map({'Yes': 1, 'No': 0, '1': 1, '0': 0})
    return df

print("=" * 80)
print("LOADING DATA FOR FEATURE IMPORTANCE ANALYSIS")
print("=" * 80)

training_data = preprocess_data(pd.read_csv(training_data_path))
validation_data = preprocess_data(pd.read_csv(validation_data_path))
test_data = preprocess_data(pd.read_csv(test_data_path))
holdout_data = preprocess_data(pd.read_csv(holdout_data_path))

print(f"\nTraining data: {training_data.shape}")
print(f"Validation data: {validation_data.shape}")

target_col = 'Churn_Yes' if 'Churn_Yes' in training_data.columns else 'Churn'
all_features = [col for col in training_data.columns if col != target_col]

# ============================================================================
# ANALYZE FEATURE IMPORTANCE
# ============================================================================

X_train = training_data[all_features]
y_train = training_data[target_col]

print("\nTraining Random Forest for feature importance ranking...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

feature_importance = pd.DataFrame({
    'feature': all_features,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance Ranking:")
print(feature_importance.to_string(index=False))

# ============================================================================
# RETRAIN MODEL WITH TOP FEATURES
# ============================================================================

top_n = 12
top_features = feature_importance.head(top_n)['feature'].tolist()
print(f"\nRetraining with top {top_n} features: {top_features}")

X_train_reduced = training_data[top_features]
X_val_reduced = validation_data[top_features]
X_test_reduced = test_data[top_features]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_reduced)
X_val_scaled = scaler.transform(X_val_reduced)
X_test_scaled = scaler.transform(X_test_reduced)

print("\nTraining MLPClassifier...")
mlp = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
mlp.fit(X_train_scaled, y_train)

y_pred = mlp.predict(X_test_scaled)
print("\nModel Performance on Test Set:")
print(classification_report(test_data[target_col], y_pred))

# Save model components
model_data = {
    'model': mlp,
    'scaler': scaler,
    'features': top_features,
    'target_col': target_col
}
os.makedirs(os.path.dirname(new_model_path), exist_ok=True)
joblib.dump(model_data, new_model_path)
print(f"\nModel saved to: {new_model_path}")
