"""
Setup metadata and prepare everything for the reduced feature model
"""

import json
import os
import joblib

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the reduced model
model_path = os.path.join(project_root, "07_Models_Trained", "final_optimized_churn_model_reduced.pkl")
model_bundle = joblib.load(model_path)

print("Model bundle keys:", model_bundle.keys())
print("\nModel details:")
print(f"  - Features: {model_bundle['features']}")
print(f"  - Target: {model_bundle['target_col']}")

# Create metadata JSON
metadata = {
    "total_features": len(model_bundle['features']),
    "features": model_bundle['features'],
    "target_col": model_bundle['target_col'],
    "model_accuracy": 0.76,
    "model_roc_auc": 0.7768,
    "model_path": model_path
}

metadata_path = os.path.join(project_root, "07_Models_Trained", "model_metadata.json")
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"\n✓ Metadata created at: {metadata_path}")
print(json.dumps(metadata, indent=2))
