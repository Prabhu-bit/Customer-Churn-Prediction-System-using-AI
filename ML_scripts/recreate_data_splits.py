"""
Recreate Data Splits with Consolidated Files (No X/y Separation)
Handles new folder structure: 04_Data_Raw and 05_Data_Splits
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

print("=" * 70)
print("CONSOLIDATED DATA SPLITS CREATION")
print("=" * 70)

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "04_Data_Raw", "customer_churn.csv")
SPLITS_OUTPUT_DIR = os.path.join(BASE_DIR, "05_Data_Splits")

print(f"\n📍 Base Directory: {BASE_DIR}")
print(f"📍 Input Data: {RAW_DATA_PATH}")
print(f"📍 Output Directory: {SPLITS_OUTPUT_DIR}")

# Create output directory if it doesn't exist
os.makedirs(SPLITS_OUTPUT_DIR, exist_ok=True)

try:
    # Load original data
    print("\n⏳ Loading original data...")
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"✓ Loaded {len(df)} records with {len(df.columns)} columns")
    
    # Display basic info
    print(f"\nDataset Info:")
    print(f"  - Shape: {df.shape}")
    print(f"  - Columns: {list(df.columns)[:5]}... (showing first 5)")
    
    # Detect target column
    if 'Churn_Yes' in df.columns:
        target_col = 'Churn_Yes'
    elif 'Churn' in df.columns:
        target_col = 'Churn'
    else:
        print("❌ Error: Could not find target column 'Churn' or 'Churn_Yes'")
        exit(1)
    
    print(f"  - Target Column: {target_col}")
    
    # Ensure target is numeric
    if df[target_col].dtype == 'object':
        print(f"  - Converting {target_col} from {df[target_col].dtype} to numeric...")
        df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
    
    # Calculate churn stats
    churn_rate = df[target_col].map({'Yes': 1, 'No': 0}).mean()
    print(f"  - Churn Rate: {churn_rate:.2%}")
    
    # ========================================================================
    # CREATE STRATIFIED SPLITS
    # ========================================================================
    print("\n⏳ Creating stratified splits...")
    
    # Split 1: 80% temp, 20% test (10% holdout from temp later)
    temp, test = train_test_split(
        df, 
        test_size=0.10,
        stratify=df[target_col],
        random_state=42
    )
    print(f"✓ Test split: {len(test)} records ({len(test)/len(df):.1%})")
    
    # Split 2: From temp -> 75% train+val, 25% holdout
    train_val, holdout = train_test_split(
        temp,
        test_size=0.10,
        stratify=temp[target_col],
        random_state=42
    )
    print(f"✓ Holdout split: {len(holdout)} records ({len(holdout)/len(df):.1%})")
    
    # Split 3: From train_val -> 75% train, 25% validation
    training, validation = train_test_split(
        train_val,
        test_size=0.25,
        stratify=train_val[target_col],
        random_state=42
    )
    print(f"✓ Training split: {len(training)} records ({len(training)/len(df):.1%})")
    print(f"✓ Validation split: {len(validation)} records ({len(validation)/len(df):.1%})")
    
    # ========================================================================
    # SAVE CONSOLIDATED SPLITS
    # ========================================================================
    print("\n⏳ Saving consolidated split files...")
    
    splits_to_save = {
        'training_split.csv': training,
        'validation_split.csv': validation,
        'test_split.csv': test,
        'holdout_split.csv': holdout
    }
    
    for filename, split_df in splits_to_save.items():
        filepath = os.path.join(SPLITS_OUTPUT_DIR, filename)
        split_df.to_csv(filepath, index=False)
        churn_pct = split_df[target_col].map({'Yes': 1, 'No': 0}).mean()
        print(f"✓ {filename:30s} - {len(split_df):5d} records | Churn: {churn_pct:.2%} | Size: {os.path.getsize(filepath)/1024:.1f} KB")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("✅ DATA SPLITS SUCCESSFULLY CREATED")
    print("=" * 70)
    
    print("\n📊 SUMMARY:")
    print(f"  - Original Data: {len(df)} records")
    print(f"  - Training Set: {len(training)} records (60%) - Churn: {training[target_col].map({'Yes': 1, 'No': 0}).mean():.2%}")
    print(f"  - Validation Set: {len(validation)} records (20%) - Churn: {validation[target_col].map({'Yes': 1, 'No': 0}).mean():.2%}")
    print(f"  - Test Set: {len(test)} records (10%) - Churn: {test[target_col].map({'Yes': 1, 'No': 0}).mean():.2%}")
    print(f"  - Holdout Set: {len(holdout)} records (10%) - Churn: {holdout[target_col].map({'Yes': 1, 'No': 0}).mean():.2%}")
    print(f"\n  Total Split Size: {len(training) + len(validation) + len(test) + len(holdout)} records ✓")
    
    print(f"\n📁 Files saved to: {SPLITS_OUTPUT_DIR}")
    print(f"📝 Each file contains ALL features + target column (consolidated)")
    
    # List files
    print("\n📄 Created Files:")
    for filename in sorted(os.listdir(SPLITS_OUTPUT_DIR)):
        if filename.endswith('.csv'):
            filepath = os.path.join(SPLITS_OUTPUT_DIR, filename)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  ✓ {filename:30s} ({size_mb:.2f} MB)")

except Exception as e:
    print(f"\n❌ Error during data split creation: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 70)
print("✅ PROCESS COMPLETE!")
print("=" * 70)
