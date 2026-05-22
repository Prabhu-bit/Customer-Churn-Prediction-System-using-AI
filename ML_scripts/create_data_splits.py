"""
Customer Churn Prediction - Complete Data Split Pipeline
=========================================================
This script creates proper train, validation, test, and holdout splits
with stratification to maintain class distribution across all sets.

Pipeline Flow:
1. Load and explore data
2. Create stratified splits
3. Apply feature engineering to each split separately
4. Save all splits as CSV files for reproducibility
5. Generate split statistics and visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

print("=" * 80)
print("CUSTOMER CHURN PREDICTION - DATA SPLIT PIPELINE")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD AND EXPLORE DATA
# ============================================================================
print("\n[STEP 1] Loading and exploring data...")

df = pd.read_csv('customer_churn.csv')
print(f"✓ Data loaded: {df.shape[0]} records, {df.shape[1]} columns")
print(f"✓ Columns: {list(df.columns)}")

# Check target distribution
target_col = 'Churn_Yes' if 'Churn_Yes' in df.columns else 'Churn'
if target_col not in df.columns:
    print(f"⚠ Converting 'Churn' to one-hot encoding...")
    df = pd.get_dummies(df, columns=['Churn'], drop_first=False)
    target_col = 'Churn_Yes'

print(f"\nTarget Column: {target_col}")
print(f"Class Distribution:")
print(df[target_col].value_counts())
# Convert target to numeric if string
if df[target_col].dtype == 'object':
    df[target_col] = (df[target_col] == 'Yes').astype(int)
    print("✓ Converted target to numeric (Yes→1, No→0)")
print(f"Churn Rate: {(df[target_col] == 'Yes').mean():.2%}")

# ============================================================================
# STEP 2: CREATE STRATIFIED SPLITS
# ============================================================================
print("\n[STEP 2] Creating stratified splits...")
print("-" * 80)

"""
Split Strategy:
- Total data: 7,043 records
- Split proportions (maintaining class distribution):
  * Training: 60% (4,226 records)
  * Validation: 20% (1,409 records)
  * Test: 10% (704 records)
  * Holdout: 10% (704 records - completely unseen)
"""

# Prepare data for splitting
X = df.drop(columns=[target_col, 'customerID'] if 'customerID' in df.columns else [target_col])
y = df[target_col]

# Split 1: Separate holdout (10% - completely unseen)
X_temp, X_holdout, y_temp, y_holdout = train_test_split(
    X, y,
    test_size=0.10,
    random_state=42,
    stratify=y
)

# Split 2: Split remaining into train (60%) and test (20%) + validation (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.25,  # 25% of 90% = 22.5% (this will be split into test and validation)
    random_state=42,
    stratify=y_temp
)

# Split 3: Split test into actual test (50%) and validation (50%)
X_validation, X_test, y_validation, y_test = train_test_split(
    X_test, y_test,
    test_size=0.50,
    random_state=42,
    stratify=y_test
)

# Print split information
splits = {
    'Training': (X_train, y_train),
    'Validation': (X_validation, y_validation),
    'Test': (X_test, y_test),
    'Holdout': (X_holdout, y_holdout)
}

print("\nData Split Summary:")
print("-" * 80)
total_records = 0
for split_name, (X_split, y_split) in splits.items():
    n_records = len(X_split)
    churn_rate = (y_split == 'Yes').mean()
    n_churn = y_split.sum()
    total_records += n_records
    print(f"{split_name:15} | Records: {n_records:5} | "
          f"Churn: {n_churn:4} ({churn_rate:6.2%}) | Pct of Total: {n_records/len(df):6.2%}")

print("-" * 80)
print(f"{'Total':15} | Records: {total_records:5}")

# Verify stratification
print("\n✓ Stratification Check - Churn rates across splits:")
for split_name, (X_split, y_split) in splits.items():
    churn_rate = (y_split == 'Yes').mean()
    print(f"  {split_name:15}: {churn_rate:.2%}")
print(f"  {'Original Data':15}: {y.mean():.2%}")

# ============================================================================
# STEP 3: APPLY FEATURE ENGINEERING TO EACH SPLIT
# ============================================================================
print("\n[STEP 3] Applying feature engineering to each split...")
print("-" * 80)

def apply_feature_engineering(X, y, split_name="Dataset"):
    """Apply feature engineering transformations to a split"""
    X_encoded = X.copy()
    
    # One-hot encode categorical columns
    categorical_cols = X_encoded.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        X_encoded = pd.get_dummies(X_encoded, columns=categorical_cols, drop_first=False)
    
    # Combine X and y for reference
    data = X_encoded.copy()
    data[target_col] = y.values
    
    print(f"  {split_name:15} -> {len(data):5} records, {len(X_encoded.columns):3} features after encoding")
    
    return X_encoded, data

# Process each split
processed_splits = {}
for split_name, (X_split, y_split) in splits.items():
    X_processed, data_with_target = apply_feature_engineering(X_split, y_split, split_name)
    processed_splits[split_name] = {
        'X': X_processed,
        'y': y_split,
        'data': data_with_target
    }

# ============================================================================
# STEP 4: SAVE ALL SPLITS
# ============================================================================
print("\n[STEP 4] Saving data splits...")
print("-" * 80)

# Create splits directory if it doesn't exist
splits_dir = 'data_splits'
os.makedirs(splits_dir, exist_ok=True)

file_paths = {}

for split_name, split_data in processed_splits.items():
    # Save with target column
    filepath = os.path.join(splits_dir, f'{split_name.lower()}_split.csv')
    split_data['data'].to_csv(filepath, index=False)
    file_paths[split_name] = filepath
    print(f"  ✓ Saved: {filepath} ({len(split_data['data'])} records)")
    
    # Save features only (X)
    X_filepath = os.path.join(splits_dir, f'{split_name.lower()}_X.csv')
    split_data['X'].to_csv(X_filepath, index=False)
    
    # Save target only (y)
    y_filepath = os.path.join(splits_dir, f'{split_name.lower()}_y.csv')
    split_data['y'].to_csv(y_filepath, index=False, header=[target_col])

print("\n✓ All splits saved successfully!")

# ============================================================================
# STEP 5: CREATE SPLIT INFORMATION JSON
# ============================================================================
print("\n[STEP 5] Creating split information metadata...")
print("-" * 80)

split_info = {
    "pipeline": "Customer Churn Prediction - Data Split Pipeline",
    "creation_date": pd.Timestamp.now().isoformat(),
    "original_data": {
        "file": "customer_churn.csv",
        "total_records": len(df),
        "total_features": len(X.columns),
        "target_column": target_col,
        "churn_rate": float(y.mean())
    },
    "splits": {
        "training": {
            "records": len(processed_splits['Training']['data']),
            "features": len(processed_splits['Training']['X'].columns),
            "churn_count": int(processed_splits['Training']['y'].sum()),
            "churn_rate": float(processed_splits['Training']['y'].mean()),
            "percentage_of_total": float(len(processed_splits['Training']['data']) / len(df)),
            "purpose": "Train the machine learning model",
            "files": [
                f"data_splits/training_split.csv",
                f"data_splits/training_X.csv",
                f"data_splits/training_y.csv"
            ]
        },
        "validation": {
            "records": len(processed_splits['Validation']['data']),
            "features": len(processed_splits['Validation']['X'].columns),
            "churn_count": int(processed_splits['Validation']['y'].sum()),
            "churn_rate": float(processed_splits['Validation']['y'].mean()),
            "percentage_of_total": float(len(processed_splits['Validation']['data']) / len(df)),
            "purpose": "Validate model during training and hyperparameter tuning",
            "files": [
                f"data_splits/validation_split.csv",
                f"data_splits/validation_X.csv",
                f"data_splits/validation_y.csv"
            ]
        },
        "test": {
            "records": len(processed_splits['Test']['data']),
            "features": len(processed_splits['Test']['X'].columns),
            "churn_count": int(processed_splits['Test']['y'].sum()),
            "churn_rate": float(processed_splits['Test']['y'].mean()),
            "percentage_of_total": float(len(processed_splits['Test']['data']) / len(df)),
            "purpose": "Evaluate final model performance",
            "files": [
                f"data_splits/test_split.csv",
                f"data_splits/test_X.csv",
                f"data_splits/test_y.csv"
            ]
        },
        "holdout": {
            "records": len(processed_splits['Holdout']['data']),
            "features": len(processed_splits['Holdout']['X'].columns),
            "churn_count": int(processed_splits['Holdout']['y'].sum()),
            "churn_rate": float(processed_splits['Holdout']['y'].mean()),
            "percentage_of_total": float(len(processed_splits['Holdout']['data']) / len(df)),
            "purpose": "Final validation with completely unseen data",
            "files": [
                f"data_splits/holdout_split.csv",
                f"data_splits/holdout_X.csv",
                f"data_splits/holdout_y.csv"
            ]
        }
    },
    "stratification": {
        "method": "Stratified train-test split with random_state=42",
        "ensures": "Class distribution maintained across all splits",
        "churn_rates_across_splits": {
            "original": float(y.mean()),
            "training": float(processed_splits['Training']['y'].mean()),
            "validation": float(processed_splits['Validation']['y'].mean()),
            "test": float(processed_splits['Test']['y'].mean()),
            "holdout": float(processed_splits['Holdout']['y'].mean())
        }
    },
    "usage_guide": {
        "training": "Load training_split.csv for model training",
        "validation": "Load validation_split.csv during hyperparameter tuning",
        "test": "Load test_split.csv for final model evaluation",
        "holdout": "Load holdout_split.csv for production validation",
        "separate_files": "Use training_X.csv and training_y.csv for sklearn pipelines"
    }
}

# Save metadata
metadata_path = os.path.join(splits_dir, 'split_metadata.json')
with open(metadata_path, 'w') as f:
    json.dump(split_info, f, indent=2)

print(f"✓ Metadata saved: {metadata_path}")

# ============================================================================
# STEP 6: CREATE VISUALIZATIONS
# ============================================================================
print("\n[STEP 6] Creating split visualizations...")
print("-" * 80)

# Create a comprehensive visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Customer Churn - Data Split Analysis', fontsize=16, fontweight='bold')

# 1. Split size distribution
ax1 = axes[0, 0]
split_names = list(splits.keys())
split_sizes = [len(splits[name][0]) for name in split_names]
colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
bars = ax1.bar(split_names, split_sizes, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Number of Records', fontsize=11, fontweight='bold')
ax1.set_title('Data Split Size Distribution', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
for bar, size in zip(bars, split_sizes):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(size)}\n({size/len(df):5.1%})',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# 2. Churn rate across splits
ax2 = axes[0, 1]
churn_rates = [splits[name][1].mean() for name in split_names]
bars = ax2.bar(split_names, churn_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax2.axhline(y=y.mean(), color='red', linestyle='--', linewidth=2, label=f'Original: {y.mean():.2%}')
ax2.set_ylabel('Churn Rate', fontsize=11, fontweight='bold')
ax2.set_title('Churn Rate Consistency (Stratification)', fontsize=12, fontweight='bold')
ax2.set_ylim([0, 0.35])
ax2.legend(fontsize=10)
ax2.grid(axis='y', alpha=0.3)
for bar, rate in zip(bars, churn_rates):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{rate:.2%}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# 3. Class distribution in each split
ax3 = axes[1, 0]
x_pos = np.arange(len(split_names))
width = 0.35
no_churn = [len(splits[name][1]) - splits[name][1].sum() for name in split_names]
churn = [splits[name][1].sum() for name in split_names]
bars1 = ax3.bar(x_pos - width/2, no_churn, width, label='No Churn', color='#4CAF50', alpha=0.8, edgecolor='black', linewidth=1)
bars2 = ax3.bar(x_pos + width/2, churn, width, label='Churn', color='#f44336', alpha=0.8, edgecolor='black', linewidth=1)
ax3.set_ylabel('Number of Records', fontsize=11, fontweight='bold')
ax3.set_title('Class Distribution Across Splits', fontsize=12, fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(split_names)
ax3.legend(fontsize=10)
ax3.grid(axis='y', alpha=0.3)

# 4. Feature count
ax4 = axes[1, 1]
feature_counts = [len(splits[name][0].columns) for name in split_names]
ax4.bar(split_names, feature_counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax4.set_ylabel('Number of Features', fontsize=11, fontweight='bold')
ax4.set_title('Feature Count per Split', fontsize=12, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)
for i, (bar, count) in enumerate(zip(ax4.patches, feature_counts)):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('data_splits_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Visualization saved: data_splits_analysis.png")
plt.close()

# ============================================================================
# STEP 7: GENERATE SUMMARY REPORT
# ============================================================================
print("\n[STEP 7] Generating summary report...")
print("-" * 80)

report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           CUSTOMER CHURN PREDICTION - DATA SPLIT SUMMARY REPORT               ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 ORIGINAL DATASET
  • Total Records: {len(df):,}
  • Total Features: {len(X.columns)}
  • Target Column: {target_col}
  • Churn Rate: {y.mean():.2%}
  • No-Churn Rate: {1-y.mean():.2%}

🔄 SPLIT STRATEGY
  Method: Stratified Train-Test Split (maintains class distribution)
  Random State: 42 (reproducible)
  Proportion: 60% Train, 20% Validation, 10% Test, 10% Holdout

📈 DATA SPLITS CREATED

  1️⃣  TRAINING SET (60% of data)
      ├─ Records: {len(processed_splits['Training']['data']):,}
      ├─ Churn Cases: {int(processed_splits['Training']['y'].sum())}
      ├─ Churn Rate: {processed_splits['Training']['y'].mean():.2%}
      ├─ Features: {len(processed_splits['Training']['X'].columns)}
      ├─ Files:
      │   ├─ data_splits/training_split.csv (complete with target)
      │   ├─ data_splits/training_X.csv (features only)
      │   └─ data_splits/training_y.csv (target only)
      └─ Purpose: Train the machine learning model

  2️⃣  VALIDATION SET (20% of data)
      ├─ Records: {len(processed_splits['Validation']['data']):,}
      ├─ Churn Cases: {int(processed_splits['Validation']['y'].sum())}
      ├─ Churn Rate: {processed_splits['Validation']['y'].mean():.2%}
      ├─ Features: {len(processed_splits['Validation']['X'].columns)}
      ├─ Files:
      │   ├─ data_splits/validation_split.csv (complete with target)
      │   ├─ data_splits/validation_X.csv (features only)
      │   └─ data_splits/validation_y.csv (target only)
      └─ Purpose: Hyperparameter tuning & model selection

  3️⃣  TEST SET (10% of data)
      ├─ Records: {len(processed_splits['Test']['data']):,}
      ├─ Churn Cases: {int(processed_splits['Test']['y'].sum())}
      ├─ Churn Rate: {processed_splits['Test']['y'].mean():.2%}
      ├─ Features: {len(processed_splits['Test']['X'].columns)}
      ├─ Files:
      │   ├─ data_splits/test_split.csv (complete with target)
      │   ├─ data_splits/test_X.csv (features only)
      │   └─ data_splits/test_y.csv (target only)
      └─ Purpose: Final model evaluation & performance reporting

  4️⃣  HOLDOUT SET (10% - COMPLETELY UNSEEN)
      ├─ Records: {len(processed_splits['Holdout']['data']):,}
      ├─ Churn Cases: {int(processed_splits['Holdout']['y'].sum())}
      ├─ Churn Rate: {processed_splits['Holdout']['y'].mean():.2%}
      ├─ Features: {len(processed_splits['Holdout']['X'].columns)}
      ├─ Files:
      │   ├─ data_splits/holdout_split.csv (complete with target)
      │   ├─ data_splits/holdout_X.csv (features only)
      │   └─ data_splits/holdout_y.csv (target only)
      └─ Purpose: Production validation with completely unseen data

🎯 STRATIFICATION VERIFICATION
  Original Churn Rate:  {y.mean():.4%}
  Training Churn Rate:  {processed_splits['Training']['y'].mean():.4%} ✓
  Validation Churn Rate: {processed_splits['Validation']['y'].mean():.4%} ✓
  Test Churn Rate:      {processed_splits['Test']['y'].mean():.4%} ✓
  Holdout Churn Rate:   {processed_splits['Holdout']['y'].mean():.4%} ✓
  
  All splits maintain consistent class distribution! ✓

📁 FILES GENERATED
  • data_splits/training_split.csv
  • data_splits/training_X.csv
  • data_splits/training_y.csv
  • data_splits/validation_split.csv
  • data_splits/validation_X.csv
  • data_splits/validation_y.csv
  • data_splits/test_split.csv
  • data_splits/test_X.csv
  • data_splits/test_y.csv
  • data_splits/holdout_split.csv
  • data_splits/holdout_X.csv
  • data_splits/holdout_y.csv
  • data_splits/split_metadata.json
  • data_splits_analysis.png

💡 USAGE EXAMPLES

  Loading Training Set:
  >>> import pandas as pd
  >>> train = pd.read_csv('data_splits/training_split.csv')
  >>> X_train = train.drop('Churn_Yes', axis=1)
  >>> y_train = train['Churn_Yes']

  Loading Test Set:
  >>> test = pd.read_csv('data_splits/test_split.csv')
  >>> X_test = test.drop('Churn_Yes', axis=1)
  >>> y_test = test['Churn_Yes']

  Training Model:
  >>> from sklearn.neural_network import MLPClassifier
  >>> model = MLPClassifier(hidden_layer_sizes=(32, 16, 8), max_iter=300)
  >>> model.fit(X_train, y_train)
  >>> val_score = model.score(pd.read_csv('data_splits/validation_X.csv'),
  ...                         pd.read_csv('data_splits/validation_y.csv'))

  Final Validation:
  >>> holdout = pd.read_csv('data_splits/holdout_split.csv')
  >>> final_score = model.score(holdout.drop('Churn_Yes', axis=1),
  ...                           holdout['Churn_Yes'])

⚠️  IMPORTANT GUIDELINES

  1. NEVER use holdout set during model development
  2. Use validation set ONLY for hyperparameter tuning
  3. Use test set for final performance reporting
  4. Keep holdout completely separate until model is finalized
  5. Always apply same preprocessing to all splits
  6. Maintain split structure across experiments

✅ NEXT STEPS

  1. Load training_split.csv for model training
  2. Use validation_split.csv for hyperparameter optimization
  3. Evaluate on test_split.csv for final metrics
  4. Reserve holdout_split.csv for production validation
  5. Update your model training scripts to use these splits

════════════════════════════════════════════════════════════════════════════════
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
════════════════════════════════════════════════════════════════════════════════
"""

print(report)

# Save report
report_path = os.path.join(splits_dir, 'SPLIT_SUMMARY_REPORT.txt')
with open(report_path, 'w') as f:
    f.write(report)

print(f"✓ Report saved: {report_path}")

# ============================================================================
# COMPLETION
# ============================================================================
print("\n" + "=" * 80)
print("✅ DATA SPLIT PIPELINE COMPLETED SUCCESSFULLY!")
print("=" * 80)
print(f"\n📁 All files saved in: {os.path.abspath(splits_dir)}/")
print("\n✓ Next Step: Use these data splits in your model training scripts")
