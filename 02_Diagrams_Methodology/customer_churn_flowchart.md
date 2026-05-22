# Customer Churn Flow Chart

```mermaid
flowchart TB
    classDef inputLayer fill:#E8F1FF,stroke:#2563EB,stroke-width:2px,color:#0F172A;
    classDef prepLayer fill:#ECFDF5,stroke:#16A34A,stroke-width:2px,color:#052E16;
    classDef trainLayer fill:#FFF7ED,stroke:#EA580C,stroke-width:2px,color:#431407;
    classDef evalLayer fill:#F5F3FF,stroke:#7C3AED,stroke-width:2px,color:#2E1065;
    classDef inferLayer fill:#FFF1F2,stroke:#E11D48,stroke-width:2px,color:#4C0519;
    classDef dbLayer fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#0F172A;

    subgraph L1[Layer 1 - Input Data]
        A[Customer Churn Dataset<br/>04_Data_Raw/customer_churn.csv<br/>7,043 records]:::inputLayer
        B[(Connected Database<br/>Prediction Store)]:::dbLayer
    end

    subgraph L2[Layer 2 - Preprocessing and Feature Engineering]
        C[Data Inspection and EDA<br/>missing values, class balance, feature types]:::prepLayer
        D[Encoding and Cleaning<br/>get_dummies, binary mapping, label cleanup]:::prepLayer
        E[Feature Scaling<br/>StandardScaler]:::prepLayer
        F[Stratified Data Splits<br/>training, validation, test, holdout]:::prepLayer
    end

    subgraph L3[Layer 3 - Model Training]
        G[Candidate Model Training<br/>MLPClassifier configurations]:::trainLayer
        H[Hyperparameter Tuning<br/>best setup: (32, 16, 8)<br/>lr=0.001, max_iter=300, alpha=0.0001]:::trainLayer
        I[Saved Model Artifact<br/>final_optimized_churn_model.pkl]:::trainLayer
    end

    subgraph L4[Layer 4 - Evaluation and Model Selection]
        J[Evaluation Metrics<br/>Accuracy, Precision, Recall, F1, ROC-AUC]:::evalLayer
        K[Best Model Selection<br/>optimized MLP chosen for inference]:::evalLayer
    end

    subgraph L5[Layer 5 - Inference and Output]
        L[Streamlit App or FastAPI Service]:::inferLayer
        M[New Customer Input]:::inferLayer
        N[Apply Same Preprocessing<br/>scaling + encoding rules]:::inferLayer
        O[Predicted Output<br/>Churn or No Churn<br/>with probability score]:::inferLayer
    end

    A --> C --> D --> E --> F --> G --> H --> I --> J --> K --> L --> M --> N --> O
    F --> J
    K --> I
    L --> O
    O --> B
    B <--> A

```

This flow chart follows the project files and outputs:
- input source: customer_churn.csv
- preprocessing: cleaning, encoding, scaling, stratified splits
- training: tuned MLP model
- evaluation: test metrics and best-model selection
- inference: selected model produces churn predictions
- database: stores or receives prediction records
