# 🎯 Customer Churn Prediction System

**Advanced Machine Learning Solution for Real-Time Customer Churn Prediction**

![Accuracy](https://img.shields.io/badge/Accuracy-76.40%25-brightgreen?style=flat-square)
![ROC-AUC](https://img.shields.io/badge/ROC--AUC-0.7768-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [How to Use](#-how-to-use)
- [API Documentation](#-api-documentation)
- [Model Metrics](#-model-metrics)
- [Visualizations](#-visualizations)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

✅ **Real-Time Predictions** - Get churn probability instantly  
✅ **Beautiful Streamlit UI** - Interactive, user-friendly interface  
✅ **REST API** - FastAPI backend with Swagger documentation  
✅ **Batch Processing** - Process multiple customers at once  
✅ **High-Quality Visualizations** - 7 individual, clear charts  
✅ **Model Metrics** - Complete performance analysis  
✅ **Feature Importance** - Understand what drives predictions  
✅ **CORS Enabled** - Easy frontend integration  

---

## 🚀 Quick Start

### Prerequisites

- Python 3.14+
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to project directory:**
   ```bash
   cd e:\Internship_Project
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Streamlit Frontend (Recommended for Users)

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

**Features available:**
- 🏠 Home - Overview and metrics
- 🔮 Make Prediction - Single & batch predictions
- 📊 Analytics - Performance insights
- ℹ️ About Model - Technical details

#### Option 2: FastAPI Backend (For Developers/Integration)

```bash
python fastapi_server.py
```

API runs at `http://localhost:8000`

**Access documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Option 3: Run Both Simultaneously

In **Terminal 1:**
```bash
python fastapi_server.py
```

In **Terminal 2:**
```bash
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
e:\Internship_Project\
│
├── 📊 VISUALIZATIONS (7 High-Quality PNGs)
│   ├── 01_model_performance_comparison.png      ⭐ All metrics comparison
│   ├── 02_accuracy_trend.png                    📈 Accuracy evolution
│   ├── 03_confusion_matrix_detailed.png         📋 Predictions breakdown
│   ├── 04_feature_importance_top15.png          🎯 Top features
│   ├── 05_hyperparameter_tuning_heatmap.png     🔥 Tuning results
│   ├── 06_model_metrics_radar.png               🎡 Multi-metric radar
│   └── 07_class_distribution_and_roc_auc.png    📊 Distribution & ROC
│
├── 🤖 MODELS & DATA
│   ├── final_optimized_churn_model.pkl          ✅ Trained model
│   ├── churn_model.pkl                          💾 Initial model
│   └── customer_churn.csv                       📂 Dataset
│
├── 🎨 FRONTEND & API
│   ├── streamlit_app.py                         🌐 Web UI
│   ├── fastapi_server.py                        🔌 REST API
│   ├── model_metrics_and_visualizations.py      📊 Metrics generator
│   └── generate_visualizations.py               🎨 Chart generator
│
├── 📝 NOTEBOOKS
│   ├── Customer_churn_2.ipynb                   📓 Main analysis
│   └── Customer_Churn.ipynb                     📓 Initial work
│
├── 📈 REPORTS & DATA
│   ├── model_evaluation_summary.txt             📄 Text report
│   ├── model_metrics_comparison.csv             📊 Metrics CSV
│   ├── hyperparameter_tuning_results.csv        📊 Tuning CSV
│   ├── feature_importance_ranking.csv           📊 Features CSV
│   └── .venv                                    🐍 Virtual env
│
├── ⚙️ CONFIGURATION
│   ├── requirements.txt                         📦 Dependencies
│   └── README.md                                📖 This file
```

---

## 🎯 How to Use

### Method 1: Web Interface (Streamlit)

1. **Start the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Navigate to Make Prediction tab**

3. **Enter customer details:**
   - Tenure, charges, services
   - Demographics, contracts
   - Payment methods

4. **Click "Predict Churn"**

5. **View results:**
   - Risk level (HIGH/LOW)
   - Churn probability
   - Confidence score
   - Recommendations

### Method 2: REST API (FastAPI)

#### Single Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "tenure": 24,
    "monthly_charges": 65.5,
    "total_charges": 1500.0,
    "gender": "Male",
    "senior_citizen": 0,
    "partner": "Yes",
    "dependents": "No",
    "phone_service": "Yes",
    "multiple_lines": "Yes",
    "internet_service": "Fiber optic",
    "online_security": "No",
    "online_backup": "Yes",
    "device_protection": "No",
    "tech_support": "No",
    "streaming_tv": "Yes",
    "streaming_movies": "No",
    "contract": "One year",
    "paperless_billing": "Yes",
    "payment_method": "Electronic check"
  }'
```

#### Python Client

```python
import requests

url = "http://localhost:8000/predict"
customer_data = {
    "tenure": 24,
    "monthly_charges": 65.5,
    "total_charges": 1500.0,
    "gender": "Male",
    "senior_citizen": 0,
    "partner": "Yes",
    "dependents": "No",
    "phone_service": "Yes",
    "multiple_lines": "Yes",
    "internet_service": "Fiber optic",
    "online_security": "No",
    "online_backup": "Yes",
    "device_protection": "No",
    "tech_support": "No",
    "streaming_tv": "Yes",
    "streaming_movies": "No",
    "contract": "One year",
    "paperless_billing": "Yes",
    "payment_method": "Electronic check"
}

response = requests.post(url, json=customer_data, params={"customer_id": "CUST_001"})
result = response.json()

print(f"Risk Level: {result['risk_level']}")
print(f"Churn Probability: {result['churn_probability']:.2%}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "accuracy": 0.7640,
  "roc_auc": 0.7768
}
```

#### 2. Single Prediction
```
POST /predict
```

**Request Body:**
```json
{
  "tenure": 24,
  "monthly_charges": 65.5,
  "total_charges": 1500.0,
  "gender": "Male",
  "senior_citizen": 0,
  "partner": "Yes",
  "dependents": "No",
  ...
}
```

**Response:**
```json
{
  "customer_id": "CUST_001",
  "prediction": 0,
  "churn_probability": 0.215,
  "no_churn_probability": 0.785,
  "risk_level": "LOW",
  "confidence": 0.785,
  "timestamp": "2024-05-10T14:30:00"
}
```

#### 3. Batch Predictions
```
POST /predict-batch
```

**Request:**
```json
{
  "records": [
    { "tenure": 24, "monthly_charges": 65.5, ... },
    { "tenure": 36, "monthly_charges": 75.0, ... }
  ]
}
```

**Response:**
```json
{
  "total_records": 2,
  "predictions": [...],
  "high_risk_count": 0,
  "low_risk_count": 2
}
```

#### 4. Model Metrics
```
GET /model-metrics
```

#### 5. Feature Importance
```
GET /feature-importance
```

### Full Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI

---

## 📊 Model Metrics

### Performance Scores

| Metric | Score |
|--------|-------|
| **Accuracy** | 76.40% |
| **Precision** | 56.56% |
| **Recall** | 48.40% |
| **F1-Score** | 0.5216 |
| **ROC-AUC** | 0.7768 ⭐ |

### Model Architecture

- **Type:** Multi-layer Perceptron (MLP)
- **Hidden Layers:** [32, 16, 8]
- **Activation:** ReLU
- **Solver:** Adam
- **Learning Rate:** 0.001
- **Max Iterations:** 300

### Dataset

- **Total Records:** 7,043
- **Features:** 30
- **Churn Rate:** 26.7%
- **Train-Test Split:** 80-20

---

## 📈 Visualizations

### Available Charts

All visualizations are **individual, high-quality PNG files**:

1. **01_model_performance_comparison.png** (14x8 inches)
   - All 5 metrics across 3 models
   - Easy to compare performance

2. **02_accuracy_trend.png** (12x7 inches)
   - Accuracy evolution across models
   - Baseline reference line

3. **03_confusion_matrix_detailed.png** (10x8 inches)
   - Prediction breakdown
   - Sensitivity and specificity metrics

4. **04_feature_importance_top15.png** (12x10 inches)
   - Top 15 most important features
   - Color-coded importance scale

5. **05_hyperparameter_tuning_heatmap.png** (10x7 inches)
   - Tuning results heatmap
   - Best configuration highlighted

6. **06_model_metrics_radar.png** (12x10 inches)
   - Multi-metric radar chart
   - All models comparison

7. **07_class_distribution_and_roc_auc.png** (14x6 inches)
   - Class distribution pie chart
   - ROC-AUC score comparison

### Opening Visualizations

All PNGs are high-resolution (300 DPI) and can be:
- ✅ Viewed in any image viewer
- ✅ Inserted in presentations
- ✅ Embedded in reports
- ✅ Zoomed without quality loss

---

## 🔑 Key Features Influencing Churn

**Top 5 Churn Predictors:**

1. 💳 **Payment Method** (Electronic check)
   - Impact Score: 0.2574

2. 👤 **Gender** (Male)
   - Impact Score: 0.2554

3. 📋 **Contract Type** (One year)
   - Impact Score: 0.2479

4. 💳 **Payment Method** (Credit card auto)
   - Impact Score: 0.2468

5. ☎️ **Multiple Lines** (Yes)
   - Impact Score: 0.2433

---

## ⚠️ Troubleshooting

### Issue: Model not loading
**Solution:**
```bash
# Check if model files exist
dir final_optimized_churn_model.pkl
dir churn_model.pkl

# Regenerate if needed
python model_metrics_and_visualizations.py
```

### Issue: Port already in use
**For Streamlit (8501):**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**For FastAPI (8000):**
```bash
python fastapi_server.py --host 0.0.0.0 --port 8001
```

### Issue: Dependencies missing
**Reinstall all:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Streamlit not displaying charts
```bash
# Clear cache and restart
streamlit run streamlit_app.py --logger.level=debug
```

---

## 📞 Support

For issues or questions:

1. Check this README
2. Review model documentation in Streamlit "About Model" tab
3. Check API docs at `/docs`
4. Review generated reports (.txt, .csv files)

---

## 📜 License

This project is for educational and commercial use.

---

## 👨‍💻 Author

**Customer Churn Prediction System**  
Built with ❤️ using Scikit-Learn, Streamlit, and FastAPI

---

## 🎉 Quick Command Reference

```bash
# Activate environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit frontend
streamlit run streamlit_app.py

# Run FastAPI backend
python fastapi_server.py

# Generate visualizations
python generate_visualizations.py

# Generate metrics
python model_metrics_and_visualizations.py

# View API docs
# Open: http://localhost:8000/docs

# View Streamlit app
# Open: http://localhost:8501
```

---

## 📊 Generated Files Summary

| File | Type | Purpose |
|------|------|---------|
| `streamlit_app.py` | Python | Web UI frontend |
| `fastapi_server.py` | Python | REST API backend |
| `generate_visualizations.py` | Python | Chart generator |
| `01-07_*.png` | Image | High-quality visualizations |
| `*.csv` | Data | Metrics and results |
| `requirements.txt` | Config | Dependencies |
| `README.md` | Doc | This file |

---

**Happy predicting! 🚀**
