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

# ============================================================================
# PATHS
# ============================================================================

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
training_data_path = os.path.join(project_root, "05_Data_Splits", "training_split.csv")
validation_data_path = os.path.join(project_root, "05_Data_Splits", "validation_split.csv")
test_data_path = os.path.join(project_root, "05_Data_Splits", "test_split.csv")
holdout_data_path = os.path.join(project_root, "05_Data_Splits", "holdout_split.csv")
old_model_path = os.path.join(project_root, "07_Models_Trained", "final_optimized_churn_model.pkl")
new_model_path = os.path.join(project_root, "07_Models_Trained", "final_optimized_churn_model_reduced.pkl")

# ============================================================================
# LOAD DATA
# ============================================================================

print("=" * 80)
print("LOADING DATA FOR FEATURE IMPORTANCE ANALYSIS")
print("=" * 80)

training_data = pd.read_csv(training_data_path)

# Preprocessing for categorical variables and dropping customerID
def preprocess_data(df):
    df = df.copy()
    if 'customerID' in df.columns: df = df.drop(columns=['customerID'])
    # Convert TotalCharges to numeric, handling spaces
    if 'TotalCharges' in df.columns: df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    # Simple label encoding for remaining categorical columns
    for col in df.select_dtypes(include=['object']).columns:
        if col != 'Churn' and col != 'Churn_Yes':
            df[col] = df[col].astype('category').cat.codes
    # Map target if it exists
    target = 'Churn_Yes' if 'Churn_Yes' in df.columns else 'Churn'
    if target in df.columns and df[target].dtype == 'object':
        df[target] = df[target].map({'Yes': 1, 'No': 0, '1': 1, '0': 0})
    return df

training_data = preprocess_data(training_data)
validation_data = preprocess_data(validation_data)
test_data = preprocess_data(test_data)
holdout_data = preprocess_data(holdout_data)

print(f"\nâœ“ Training data: {training_data.shape}")
print(f"âœ“ Validation data: {validation_data.shape}")
print(f"âœ“ Test data: {test_data.shape}")
print(f"âœ“ Holdout data: {holdout_data.shape}")

# ============================================================================
# IDENTIFY TARGET AND FEATURES
# ============================================================================

target_col = 'Churn_Yes' if 'Churn_Yes' in training_data.columns else 'Churn'
all_features = [col for col in training_data.columns if col != target_col]

print(f"\nâœ“ Target column: {target_col}")
print(f"âœ“ Total features available: {len(all_features)}")
print(f"\nFeature list:")
for i, feat in enumerate(all_features, 1):
    print(f"  {i:2d}. {feat}")

# ============================================================================
# ANALYZE PERMUTATION IMPORTANCE
# ============================================================================

print("\n" + "=" * 80)
print("ANALYZING FEATURE IMPORTANCE USING TREE-BASED METHOD")
print("=" * 80)

# Train a simple model to get feature importance
from sklearn.ensemble import RandomForestClassifier

X_train = training_data[all_features]
y_train = training_data[target_col]

print("\nTraining Random Forest for feature importance analysis...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# Get feature importance
feature_importance = pd.DataFrame({
    'feature': all_features,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nâœ“ Feature Importance Ranking:")
print(feature_importance.to_string(index=False))

# ============================================================================
# SELECT TOP FEATURES
# ============================================================================

print("\n" + "=" * 80)
print("SELECTING TOP FEATURES FOR REDUCED MODEL")
print("=" * 80)

top_n = 12  # Select top 12 features (user wanted reduced from 30, so 12 is good)
top_features = feature_importance.head(top_n)['feature'].tolist()

print(f"\nâœ“ Selected top {top_n} most important features:")
for i, feat in enumerate(top_features, 1):
    importance = feature_importance[feature_importance['feature'] == feat]['importance'].values[0]
    print(f"  {i:2d}. {feat:30s} (importance: {importance:.4f})")

cumulative_importance = feature_importance.head(top_n)['importance'].sum()
total_importance = feature_importance['importance'].sum()
print(f"\nâœ“ Cumulative importance of top {top_n}: {cumulative_importance:.4f} ({(cumulative_importance/total_importance)*100:.2f}%)")

# ============================================================================
# RETRAIN MODEL WITH TOP FEATURES
# ============================================================================

print("\n" + "=" * 80)
print("RETRAINING MODEL WITH TOP FEATURES ONLY")
print("=" * 80)

# Prepare data with top features only
X_train = training_data[top_features]
y_train = training_data[target_col]
X_val = validation_data[top_features]
y_val = validation_data[target_col]
X_test = test_data[top_features]
y_test = test_data[target_col]
X_holdout = holdout_data[top_features]
y_holdout = holdout_data[target_col]

print(f"\nâœ“ Training set shape: {X_train.shape}")
print(f"âœ“ Validation set shape: {X_val.shape}")
print(f"âœ“ Test set shape: {X_test.shape}")
print(f"âœ“ Holdout set shape: {X_holdout.shape}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
X_holdout_scaled = scaler.transform(X_holdout)

# Train MLP with top features
print("\nâœ“ Training MLPClassifier with top features...")
new_model = MLPClassifier(
    hidden_layer_sizes=(32, 16, 8),
    activation='relu',
    solver='adam',
    learning_rate_init=0.001,
    max_iter=500,
    random_state=42,
    verbose=1
)

new_model.fit(X_train_scaled, y_train)

# ============================================================================
# EVALUATE MODEL
# ============================================================================

print("\n" + "=" * 80)
print("MODEL EVALUATION")
print("=" * 80)

# Predictions
y_pred_train = new_model.predict(X_train_scaled)
y_pred_val = new_model.predict(X_val_scaled)
y_pred_test = new_model.predict(X_test_scaled)
y_pred_holdout = new_model.predict(X_holdout_scaled)

# Probabilities for ROC-AUC
y_proba_train = new_model.predict_proba(X_train_scaled)[:, 1]
y_proba_val = new_model.predict_proba(X_val_scaled)[:, 1]
y_proba_test = new_model.predict_proba(X_test_scaled)[:, 1]
y_proba_holdout = new_model.predict_proba(X_holdout_scaled)[:, 1]

# Calculate metrics
train_acc = accuracy_score(y_train, y_pred_train)
val_acc = accuracy_score(y_val, y_pred_val)
test_acc = accuracy_score(y_test, y_pred_test)
holdout_acc = accuracy_score(y_holdout, y_pred_holdout)

train_auc = roc_auc_score(y_train, y_proba_train)
val_auc = roc_auc_score(y_val, y_proba_val)
test_auc = roc_auc_score(y_test, y_proba_test)
holdout_auc = roc_auc_score(y_holdout, y_proba_holdout)

print("\nAccuracy:")
print(f"  Training:   {train_acc:.4f} ({train_acc*100:.2f}%)")
print(f"  Validation: {val_acc:.4f} ({val_acc*100:.2f}%)")
print(f"  Test:       {test_acc:.4f} ({test_acc*100:.2f}%)")
print(f"  Holdout:    {holdout_acc:.4f} ({holdout_acc*100:.2f}%)")

print("\nROC-AUC Score:")
print(f"  Training:   {train_auc:.4f}")
print(f"  Validation: {val_auc:.4f}")
print(f"  Test:       {test_auc:.4f}")
print(f"  Holdout:    {holdout_auc:.4f}")

print("\nTest Set Classification Report:")
print(classification_report(y_test, y_pred_test, target_names=["No Churn", "Churn"]))

# ============================================================================
# SAVE MODEL AND FEATURE LIST
# ============================================================================

print("\n" + "=" * 80)
print("SAVING MODEL AND FEATURE LIST")
print("=" * 80)

# Save the model
joblib.dump(new_model, new_model_path)
print(f"\nâœ“ Model saved to: {new_model_path}")

# Save feature list to text file for reference
feature_list_path = os.path.join(project_root, "07_Models_Trained", "top_features_list.txt")
with open(feature_list_path, 'w') as f:
    f.write("TOP FEATURES FOR REDUCED MODEL\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Total Features Selected: {len(top_features)}\n\n")
    f.write("Features (in order of importance):\n")
    f.write("-" * 60 + "\n")
    for i, feat in enumerate(top_features, 1):
        importance = feature_importance[feature_importance['feature'] == feat]['importance'].values[0]
        f.write(f"{i:2d}. {feat:30s} (importance: {importance:.4f})\n")
    f.write("\n" + "=" * 60 + "\n")
    f.write(f"Model Performance on Test Set:\n")
    f.write(f"  Accuracy:  {test_acc:.4f} ({test_acc*100:.2f}%)\n")
    f.write(f"  ROC-AUC:   {test_auc:.4f}\n")

print(f"âœ“ Feature list saved to: {feature_list_path}")

# Save as JSON for easy loading in apps
import json
feature_metadata = {
    "total_features": len(top_features),
    "features": top_features,
    "model_accuracy": round(test_acc, 4),
    "model_roc_auc": round(test_auc, 4),
    "model_path": new_model_path
}

metadata_path = os.path.join(project_root, "07_Models_Trained", "model_metadata.json")
with open(metadata_path, 'w') as f:
    json.dump(feature_metadata, f, indent=2)

print(f"âœ“ Model metadata saved to: {metadata_path}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"""
âœ“ Feature reduction complete!

Original features:        {len(all_features)}
Reduced to:               {len(top_features)} features
Features removed:         {len(all_features) - len(top_features)}

Model Performance (Test Set):
  Accuracy:               {test_acc*100:.2f}%
  ROC-AUC:                {test_auc:.4f}

Features explanation:
  These {len(top_features)} features account for {(cumulative_importance/total_importance)*100:.2f}% of total importance

Next steps:
  1. Update streamlit_app.py to use new model
  2. Update fastapi_server.py to use new model
  3. Test predictions in both apps
  4. Verify different inputs produce different results
""")

print("=" * 80)
