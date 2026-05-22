"""
Simple Data Split Creator - Customer Churn Prediction
Generates train/val/test/holdout splits with stratification
"""
import pandas as pd
import os
from sklearn.model_selection import train_test_split

print("Loading data...")
# Read raw data
df = pd.read_csv(r'..\04_Data_Raw\customer_churn.csv')
print(f"Data shape: {df.shape}")

# Get target column and ensure it's numeric/dummy
target_col = 'Churn_Yes' if 'Churn_Yes' in df.columns else 'Churn'
if target_col not in df.columns:
    df = pd.get_dummies(df, columns=['Churn'], drop_first=True)
    target_col = 'Churn_Yes'

if df[target_col].dtype == 'object':
    df[target_col] = (df[target_col] == 'Yes').astype(int)

print(f"Target column: {target_col}")
print(f"Churn rate: {df[target_col].mean():.2%}")

# Prepare splits
cols_to_drop = [target_col]
if 'customerID' in df.columns:
    cols_to_drop.append('customerID')

X = df.drop(columns=cols_to_drop)
y = df[target_col]

# Split: 60% train, 30% temp (will split into 20% val, 10% test), 10% holdout
X_temp, X_holdout, y_temp, y_holdout = train_test_split(
    X, y, test_size=0.10, random_state=42, stratify=y
)

# Split temp into train (80%) and test+val (20%)
X_train, X_test_val, y_train, y_test_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
)

# Split test+val into test (50%) and validation (50%)
X_validation, X_test, y_validation, y_test = train_test_split(
    X_test_val, y_test_val, test_size=0.50, random_state=42, stratify=y_test_val
)

# Create splits directory
out_dir = '../05_Data_Splits'
os.makedirs(out_dir, exist_ok=True)

# Save all splits
splits = {
    'training': (X_train, y_train),
    'validation': (X_validation, y_validation),
    'test': (X_test, y_test),
    'holdout': (X_holdout, y_holdout)
}

for name, (X_part, y_part) in splits.items():
    # Full split (with target)
    data = X_part.copy()
    data[target_col] = y_part.values
    data.to_csv(f'{out_dir}/{name}_split.csv', index=False)
    
    # Features only
    X_part.to_csv(f'{out_dir}/{name}_X.csv', index=False)
    
    # Target only
    pd.DataFrame({target_col: y_part.values}).to_csv(f'{out_dir}/{name}_y.csv', index=False)
    
    print(f"Saved {name}: {len(data)} records, {len(X_part.columns)} features")

print("\nSplit Summary:")
for name, (X_part, y_part) in splits.items():
    records = len(X_part)
    churn_rate = y_part.mean()
    churn_count = int(y_part.sum())
    pct = records / len(df) * 100
    print(f"{name:12} | {records:5} records | {churn_rate:6.2%} churn | {pct:5.1f}% of total")

print(f"\n[SUCCESS] All splits created in {out_dir}/ folder")
