# ⚡ QUICK EXECUTION GUIDE - Customer Churn Prediction System

**Status**: ✅ Ready to Execute  
**Last Updated**: May 10, 2024  
**All Files Generated**: ✅ YES

---

## 🎯 What Was Just Created

### 1. Data Split Files (13 files in `data_splits/` folder)
```
├── training_split.csv (4,226 records - 60%)
├── training_X.csv
├── training_y.csv
├── validation_split.csv (1,409 records - 20%)
├── validation_X.csv
├── validation_y.csv
├── test_split.csv (704 records - 10%)
├── test_X.csv
├── test_y.csv
├── holdout_split.csv (704 records - 10% unseen)
├── holdout_X.csv
├── holdout_y.csv
└── split_metadata.json
```

**Purpose**: Proper ML workflow with stratified splits maintaining 26.7% churn rate across all sets

### 2. Pipeline Diagrams (3 high-res PNGs)
```
├── ML_Methodology_Diagram.png - Algorithms & techniques used
├── End_to_End_Pipeline.png - Complete data flow
└── Inference_Pipeline.png - Real-time prediction flow
```

**Purpose**: Visual understanding of the complete ML workflow

### 3. Comprehensive Documentation
```
├── ML_PIPELINE_GUIDE.md - 500+ line complete guide
├── README.md - Application documentation
└── QUICK_COMMANDS_GUIDE.txt - This file
```

---

## ⚡ QUICK START (Copy-Paste Ready)

### Step 1: Verify Environment
```bash
.venv\Scripts\activate
python -c "import pandas, sklearn, streamlit, fastapi; print('✓ All installed')"
```

### Step 2: Create Data Splits (if not already done)
```bash
python create_data_splits.py
```

### Step 3: Create Pipeline Diagrams (if not already done)
```bash
python create_pipeline_diagrams.py
```

### Step 4: Launch Web Application
```bash
python -m streamlit run streamlit_app.py
```
🌐 Opens at: **http://localhost:8501**

### Step 5 (Optional): Launch API
```bash
python fastapi_server.py
```
📚 API Docs at: **http://localhost:8000/docs**

---

## 🐛 FIXES FOR COMMON ISSUES

### ❌ "streamlit: command not found"
**Fix**: Use `python -m` instead
```bash
python -m streamlit run streamlit_app.py
```

### ❌ "ModuleNotFoundError: No module named 'fastapi'"
**Fix**: Reinstall dependencies
```bash
pip install -r requirements.txt --upgrade
```

### ❌ "Port 8501 already in use"
**Fix**: Use different port
```bash
python -m streamlit run streamlit_app.py --server.port 8502
```

### ❌ "Module not found" when running FastAPI
**Fix**: Make sure packages are installed
```bash
pip install fastapi uvicorn pydantic -q
python fastapi_server.py
```

---

## 📊 View Generated Files

### 1. Data Splits Analysis
```bash
# View the split summary
cat data_splits\SPLIT_SUMMARY_REPORT.txt

# View metadata
cat data_splits\split_metadata.json

# View visualization
start data_splits_analysis.png
```

### 2. Pipeline Diagrams
```bash
start ML_Methodology_Diagram.png
start End_to_End_Pipeline.png
start Inference_Pipeline.png
```

### 3. Complete Guides
```bash
# View ML Pipeline Guide
notepad ML_PIPELINE_GUIDE.md

# View Application Guide
notepad README.md
```

---

## 🚀 COMPLETE WORKFLOW

### For First-Time Users
1. Run `python -m streamlit run streamlit_app.py`
2. Open browser to http://localhost:8501
3. Click "🔮 Make Prediction" tab
4. Enter customer details
5. Click "Predict Churn"
6. View results with risk level and probability

### For Developers/Integration
1. Run `python fastapi_server.py`
2. Open http://localhost:8000/docs
3. Click "Try it out" on `/predict` endpoint
4. Enter customer JSON data
5. Execute and view response

### For Data Scientists
1. Load training split: `pd.read_csv('data_splits/training_split.csv')`
2. Train new model
3. Validate on validation split
4. Test on test split
5. Final validation on holdout split

---

## 📈 Example API Call (Python)

```python
import requests

url = "http://localhost:8000/predict"
customer = {
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

response = requests.post(url, json=customer, params={"customer_id": "CUST_001"})
result = response.json()

print(f"Churn Risk: {result['risk_level']}")
print(f"Probability: {result['churn_probability']:.2%}")
```

---

## 📋 Project File Structure

```
e:\Internship_Project\
├── 📊 VISUALIZATIONS
│   ├── ML_Methodology_Diagram.png ⭐
│   ├── End_to_End_Pipeline.png ⭐
│   ├── Inference_Pipeline.png ⭐
│   ├── data_splits_analysis.png
│   ├── 01_model_performance_comparison.png
│   ├── 02_accuracy_trend.png
│   └── ... (7 total visualizations)
│
├── 🤖 DATA SPLITS (NEW!)
│   └── data_splits/
│       ├── training_split.csv
│       ├── validation_split.csv
│       ├── test_split.csv
│       ├── holdout_split.csv
│       ├── split_metadata.json
│       └── SPLIT_SUMMARY_REPORT.txt
│
├── 🐍 PYTHON CODE
│   ├── streamlit_app.py (WEB UI)
│   ├── fastapi_server.py (REST API)
│   ├── create_data_splits.py ⭐ (NEW!)
│   ├── create_pipeline_diagrams.py ⭐ (NEW!)
│   ├── generate_visualizations.py
│   └── model_metrics_and_visualizations.py
│
├── 📚 DOCUMENTATION
│   ├── README.md (Application guide)
│   ├── ML_PIPELINE_GUIDE.md ⭐ (NEW!)
│   ├── index.html (Visual dashboard)
│   └── QUICK_COMMANDS_GUIDE.txt (This file)
│
├── 🤖 TRAINED MODELS
│   ├── final_optimized_churn_model.pkl
│   └── churn_model.pkl
│
├── 📂 DATA
│   └── customer_churn.csv
│
├── ⚙️ CONFIGURATION
│   └── requirements.txt
│
└── 📓 NOTEBOOKS
    ├── Customer_churn_2.ipynb (Complete analysis)
    └── Customer_Churn.ipynb
```

---

## 🎓 Learning Path

### Level 1: User (See Results)
1. Run Streamlit app
2. Input customer data
3. View predictions

### Level 2: Developer (Use API)
1. Understand API endpoints
2. Make HTTP requests
3. Integrate into applications

### Level 3: Data Scientist (Use Data Splits)
1. Load training data
2. Train own models
3. Evaluate on proper splits

### Level 4: ML Engineer (Full Pipeline)
1. Understand all phases
2. Modify hyperparameters
3. Deploy improvements

---

## ✅ VERIFICATION CHECKLIST

After running commands, verify:

- [ ] Streamlit app launches at http://localhost:8501
- [ ] Can enter customer data
- [ ] Predictions display with risk level
- [ ] API launches at http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] All 7 visualizations visible
- [ ] Data splits created in `data_splits/` folder
- [ ] Pipeline diagrams display correctly
- [ ] README and guides are readable

---

## 🔗 IMPORTANT LINKS

| Resource | Purpose |
|----------|---------|
| http://localhost:8501 | Streamlit Web UI |
| http://localhost:8000/docs | API Swagger Docs |
| http://localhost:8000/redoc | API ReDoc Docs |
| ./ML_PIPELINE_GUIDE.md | Complete ML Guide |
| ./README.md | App Documentation |
| ./data_splits/ | Training Data |

---

## 💡 TIPS & TRICKS

### Run Both UI and API
```bash
# Terminal 1
python fastapi_server.py

# Terminal 2
python -m streamlit run streamlit_app.py
```

### Export Predictions
```bash
# Save predictions to CSV
# In Streamlit: Download button in "Make Prediction" tab
# In API: Use batch endpoint /predict-batch
```

### Monitor API
```bash
# Check API health
curl http://localhost:8000/health

# Get model metrics
curl http://localhost:8000/model-metrics
```

### Debug Issues
```bash
# Check Python version
python --version

# List installed packages
pip list

# Show full errors
python -m streamlit run streamlit_app.py --logger.level=debug
```

---

## 🚨 IMPORTANT: Data Usage Guidelines

1. **Never use holdout set during development** - Keep it completely separate!
2. **Validation split only for tuning** - Don't use for final metrics
3. **Test split for reporting** - Use for presenting model performance
4. **Holdout for production validation** - Use after model is deployed
5. **Same preprocessing for all splits** - Ensure consistency

---

## 📞 TROUBLESHOOTING REFERENCE

| Issue | Error | Solution |
|-------|-------|----------|
| Command not found | `streamlit: command not found` | Use `python -m streamlit` |
| Module missing | `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Port in use | `Address already in use` | Use `--server.port 8502` |
| Import error | `ImportError` | Check venv is activated |
| File not found | `FileNotFoundError` | Check file path and verify it exists |

---

## 🎯 NEXT IMMEDIATE ACTIONS

1. Run: `python create_data_splits.py` ✓ (Already done)
2. Run: `python create_pipeline_diagrams.py` ✓ (Already done)
3. Run: `python -m streamlit run streamlit_app.py` ← **Do this next**
4. Make predictions and test the system
5. Review ML_PIPELINE_GUIDE.md for deep understanding

---

## ✨ You're All Set!

Everything is ready. Your ML system has:
- ✅ Properly stratified data splits (train/val/test/holdout)
- ✅ Complete ML methodology documented
- ✅ End-to-end pipeline visualized
- ✅ Production-ready web UI
- ✅ REST API with Swagger docs
- ✅ High-quality visualizations
- ✅ Comprehensive guides

**Ready to go live! 🚀**

---

**Generated**: May 10, 2024  
**Status**: 🟢 Production Ready  
**Questions**: Check ML_PIPELINE_GUIDE.md or README.md
