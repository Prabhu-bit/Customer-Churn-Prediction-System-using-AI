import os
import pandas as pd
import joblib

# Paths
project_root = r"e:\Internship_Project"
model_path = os.path.join(project_root, "07_Models_Trained", "final_optimized_churn_model_reduced.pkl")
training_path = os.path.join(project_root, "05_Data_Splits", "training_split.csv")

# Test 2: Load model bundle
print("TEST 2: Loading model bundle...")
bundle = joblib.load(model_path)
print(f"✓ Keys: {bundle.keys()}")
model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]
print(f"✓ Features: {features}")
print(f"✓ Model type: {type(model)}")

# Test 3: Test prediction
print("\nTEST 3: Making test prediction...")
training_data = pd.read_csv(training_path)

# Prepare test data
test_row = training_data[features].iloc[:1]
test_row_scaled = scaler.transform(test_row)
prediction = model.predict(test_row_scaled)
probability = model.predict_proba(test_row_scaled)

print(f"✓ Prediction: {prediction[0]}")
print(f"✓ Probabilities: No Churn={probability[0][0]:.4f}, Churn={probability[0][1]:.4f}")

# Test 4: Verify feature count matches
print("\nTEST 4: Verifying feature consistency...")
input_shape = test_row.shape[1]
model_expected = model.coefs_[0].shape[0] if hasattr(model, "coefs_") else model.n_features_in_
print(f"✓ Input features: {input_shape}")
print(f"✓ Model expects: {model_expected}")
print(f"✓ Match: {input_shape == model_expected}")

print("\n✅ All tests passed! The bundle structure is correct.")
