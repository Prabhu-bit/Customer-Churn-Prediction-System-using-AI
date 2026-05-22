# Customer Churn System Architecture

```mermaid
flowchart TB
    %% =========================
    %% STYLES
    %% =========================
    classDef dataLayer fill:#E8F1FF,stroke:#2F6BFF,stroke-width:2px,color:#0F2557;
    classDef processLayer fill:#EAF8F1,stroke:#22A06B,stroke-width:2px,color:#0D3B26;
    classDef modelLayer fill:#FFF4E5,stroke:#F28C28,stroke-width:2px,color:#5C3700;
    classDef evalLayer fill:#F4ECFF,stroke:#8E5CE6,stroke-width:2px,color:#341A66;
    classDef deployLayer fill:#FFEAF0,stroke:#D93A6A,stroke-width:2px,color:#5A1230;
    classDef dbLayer fill:#EEF2F7,stroke:#5B6B7A,stroke-width:2px,color:#1F2D3A;

    %% =========================
    %% LAYER 1: DATA SOURCE
    %% =========================
    subgraph L1[Layer 1 - Data Source]
        A[Customer Churn CSV<br/>04_Data_Raw/customer_churn.csv]:::dataLayer
        B[(Connected Database /<br/>Prediction Store)]:::dbLayer
    end

    %% =========================
    %% LAYER 2: PREPROCESSING
    %% =========================
    subgraph L2[Layer 2 - Preprocessing & Feature Engineering]
        C[Data Cleaning<br/>- missing values check<br/>- schema review]:::processLayer
        D[Encoding & Feature Engineering<br/>- get_dummies / one-hot encoding<br/>- binary mapping<br/>- feature reduction]:::processLayer
        E[Feature Scaling<br/>StandardScaler]:::processLayer
        F[Stratified Splits<br/>train / validation / test / holdout]:::processLayer
    end

    %% =========================
    %% LAYER 3: TRAINING
    %% =========================
    subgraph L3[Layer 3 - Model Training & Selection]
        G[Candidate Models<br/>MLP configurations]:::modelLayer
        H[Hyperparameter Tuning<br/>best params: (32, 16, 8)<br/>lr=0.001, max_iter=300, alpha=0.0001]:::modelLayer
        I[Trained Model Artifact<br/>final_optimized_churn_model.pkl]:::modelLayer
    end

    %% =========================
    %% LAYER 4: EVALUATION
    %% =========================
    subgraph L4[Layer 4 - Evaluation]
        J[Test / Holdout Evaluation<br/>Accuracy, Precision, Recall, F1, ROC-AUC]:::evalLayer
        K[Best Model Decision<br/>select optimized MLP]:::evalLayer
    end

    %% =========================
    %% LAYER 5: INFERENCE & OUTPUT
    %% =========================
    subgraph L5[Layer 5 - Inference & Output]
        L[Streamlit UI / FastAPI Service]:::deployLayer
        M[Input Customer Features]:::deployLayer
        N[Preprocessed Inference Vector]:::deployLayer
        O[Predicted Output<br/>Churn / No Churn<br/>with probability score]:::deployLayer
    end

    %% =========================
    %% FLOWS
    %% =========================
    A --> C --> D --> E --> F --> G
    G --> H --> I --> J --> K --> L
    B <--> A
    B <--> O
    L --> M --> N --> I --> O
    O --> B

    %% =========================
    %% EXTERNAL SUPPORT FLOW
    %% =========================
    F --> J
    D --> I
    K --> I

```

The diagram above matches the project's current flow:
- raw input from the churn dataset
- preprocessing and feature engineering
- stratified train / validation / test / holdout splits
- tuned MLP model selection
- evaluation on unseen data
- inference through Streamlit or FastAPI
- connected persistence for prediction storage and retrieval