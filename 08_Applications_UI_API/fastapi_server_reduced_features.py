"""
Customer Churn Prediction - FastAPI Server with REDUCED FEATURES
Uses 12 most important features for optimal performance
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import json
import os
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as uvicorn_run

# ============================================================================
# INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn using 12 optimized features",
    version="2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# LOAD MODEL AND FEATURES
# ============================================================================

def get_base_path():
    """Get the base project path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    return parent_dir

BASE_PATH = get_base_path()

try:
    # Load model
    model_path = os.path.join(BASE_PATH, "07_Models_Trained", "final_optimized_churn_model_reduced.pkl")
    MODEL = joblib.load(model_path)
    print(f"✓ Model loaded from: {model_path}")
    
    # Load metadata
    metadata_path = os.path.join(BASE_PATH, "07_Models_Trained", "model_metadata.json")
    with open(metadata_path, 'r') as f:
        METADATA = json.load(f)
    FEATURE_COLUMNS = METADATA['features']
    print(f"✓ Features loaded: {len(FEATURE_COLUMNS)} features")
    
    # Load training data for reference
    training_path = os.path.join(BASE_PATH, "05_Data_Splits", "training_split.csv")
    TRAINING_DATA = pd.read_csv(training_path)
    print(f"✓ Training data loaded: {TRAINING_DATA.shape}")
    
except Exception as e:
    print(f"❌ Error loading model: {e}")
    import traceback
    traceback.print_exc()
    MODEL = None
    FEATURE_COLUMNS = None
    TRAINING_DATA = None

# ============================================================================
# DATA MODELS
# ============================================================================

class CustomerData(BaseModel):
    """Single customer prediction input"""
    tenure: float
    MonthlyCharges: float
    TotalCharges: float
    Contract: str
    InternetService: str
    OnlineSecurity: str
    TechSupport: str
    OnlineBackup: str
    PaperlessBilling: str
    PaymentMethod: str
    gender: str
    MultipleLines: str

class PredictionResponse(BaseModel):
    """Single prediction response"""
    churn_probability: float
    no_churn_probability: float
    prediction: str
    risk_level: str
    confidence: float

class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    customers: list

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    features_count: int
    features: list

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/", response_class=dict, tags=["Info"])
def read_root():
    """Root endpoint with API documentation"""
    return {
        "title": "Customer Churn Prediction API",
        "version": "2.0",
        "description": "Predict customer churn using 12 optimized features",
        "endpoints": {
            "health": "GET /health",
            "predict_single": "POST /predict",
            "predict_batch": "POST /predict-batch",
            "model_info": "GET /model-info",
            "documentation": "GET /docs"
        },
        "docs": "http://localhost:8000/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Check if model is loaded and ready"""
    return HealthResponse(
        status="healthy" if MODEL is not None else "error",
        model_loaded=MODEL is not None,
        features_count=len(FEATURE_COLUMNS) if FEATURE_COLUMNS else 0,
        features=FEATURE_COLUMNS if FEATURE_COLUMNS else []
    )

@app.get("/model-info", tags=["Info"])
def get_model_info():
    """Get model information"""
    return {
        "model_type": "MLPClassifier",
        "hidden_layers": [32, 16, 8],
        "activation": "relu",
        "optimizer": "adam",
        "features_count": len(FEATURE_COLUMNS) if FEATURE_COLUMNS else 0,
        "features": FEATURE_COLUMNS if FEATURE_COLUMNS else [],
        "accuracy": 0.76,
        "roc_auc": 0.7768,
        "training_samples": len(TRAINING_DATA) if TRAINING_DATA is not None else 0
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
def predict_churn(customer: CustomerData):
    """
    Predict churn for a single customer
    
    Example:
    {
        "tenure": 24,
        "MonthlyCharges": 65.0,
        "TotalCharges": 1560.0,
        "Contract": "Month-to-month",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "TechSupport": "No",
        "OnlineBackup": "No",
        "PaperlessBilling": "No",
        "PaymentMethod": "Electronic check",
        "gender": "Male",
        "MultipleLines": "No"
    }
    """
    
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Create DataFrame with customer data
        customer_dict = customer.dict()
        customer_df = pd.DataFrame([customer_dict])
        
        # Ensure all features are present
        for feat in FEATURE_COLUMNS:
            if feat not in customer_df.columns:
                customer_df[feat] = 0
        
        # Select only required features
        customer_df = customer_df[FEATURE_COLUMNS]
        
        # Make prediction
        prediction = MODEL.predict(customer_df)[0]
        probabilities = MODEL.predict_proba(customer_df)[0]
        
        churn_prob = probabilities[1]
        no_churn_prob = probabilities[0]
        
        # Determine risk level
        if churn_prob > 0.7:
            risk_level = "Very High"
        elif churn_prob > 0.5:
            risk_level = "High"
        elif churn_prob > 0.3:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return PredictionResponse(
            churn_probability=round(churn_prob, 4),
            no_churn_probability=round(no_churn_prob, 4),
            prediction="Churn" if prediction == 1 else "No Churn",
            risk_level=risk_level,
            confidence=round(max(churn_prob, no_churn_prob), 4)
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/predict-batch", tags=["Predictions"])
def predict_batch(request: BatchPredictionRequest):
    """
    Predict churn for multiple customers
    
    Example:
    {
        "customers": [
            {"tenure": 24, "MonthlyCharges": 65.0, ...},
            {"tenure": 60, "MonthlyCharges": 80.0, ...}
        ]
    }
    """
    
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        results = []
        
        for customer_dict in request.customers:
            customer_df = pd.DataFrame([customer_dict])
            
            # Ensure all features are present
            for feat in FEATURE_COLUMNS:
                if feat not in customer_df.columns:
                    customer_df[feat] = 0
            
            # Select only required features
            customer_df = customer_df[FEATURE_COLUMNS]
            
            # Make prediction
            prediction = MODEL.predict(customer_df)[0]
            probabilities = MODEL.predict_proba(customer_df)[0]
            
            churn_prob = probabilities[1]
            no_churn_prob = probabilities[0]
            
            if churn_prob > 0.7:
                risk_level = "Very High"
            elif churn_prob > 0.5:
                risk_level = "High"
            elif churn_prob > 0.3:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            results.append({
                "churn_probability": round(churn_prob, 4),
                "no_churn_probability": round(no_churn_prob, 4),
                "prediction": "Churn" if prediction == 1 else "No Churn",
                "risk_level": risk_level,
                "confidence": round(max(churn_prob, no_churn_prob), 4)
            })
        
        return {
            "total_predictions": len(results),
            "predictions": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")

@app.get("/feature-importance", tags=["Model Info"])
def get_feature_importance():
    """Get feature importance ranking"""
    return {
        "features": FEATURE_COLUMNS if FEATURE_COLUMNS else [],
        "total_features": len(FEATURE_COLUMNS) if FEATURE_COLUMNS else 0,
        "description": "These are the 12 most important features selected for the model"
    }

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("STARTING CUSTOMER CHURN PREDICTION API")
    print("=" * 80)
    print(f"\n✓ Model: MLPClassifier with {len(FEATURE_COLUMNS)} features")
    print(f"✓ Features: {FEATURE_COLUMNS}")
    print(f"\n📚 API Documentation: http://localhost:8000/docs")
    print(f"📚 Alternative Docs: http://localhost:8000/redoc")
    print("\n" + "=" * 80 + "\n")
    
    uvicorn_run(
        "fastapi_server_reduced_features:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
