# 🚀 HOW TO RUN THE APPLICATION (AFTER REORGANIZATION)

## 📍 Important: Files Have Moved!

After reorganization, the application files are now in:
- **Streamlit App:** `08_Applications_UI_API/streamlit_app.py`
- **FastAPI Server:** `08_Applications_UI_API/fastapi_server.py`

**DO NOT** run from the root directory anymore!

---

## 🎯 EASIEST WAY: Use Launcher Scripts

### Windows (PowerShell) - Recommended

**For Streamlit Web App:**
```powershell
.\RUN_STREAMLIT_APP.ps1
```

**For FastAPI REST API:**
```powershell
.\RUN_FASTAPI_SERVER.ps1
```

### Windows (Command Prompt)

**For Streamlit Web App:**
```cmd
RUN_STREAMLIT_APP.bat
```

**For FastAPI REST API:**
```cmd
RUN_FASTAPI_SERVER.bat
```

---

## 🔧 MANUAL METHOD: Run from Command Line

### Method 1: PowerShell (Recommended)

**Step 1: Activate Environment**
```powershell
cd e:\Internship_Project
.venv\Scripts\Activate.ps1
```

**Step 2a: Run Streamlit (Web App)**
```powershell
cd 08_Applications_UI_API
python -m streamlit run streamlit_app.py
```
- Browser opens at: **http://localhost:8501**

**Step 2b: Run FastAPI (REST API)**
```powershell
cd 08_Applications_UI_API
python fastapi_server.py
```
- Swagger docs at: **http://localhost:8000/docs**
- ReDoc at: **http://localhost:8000/redoc**

### Method 2: Command Prompt (Windows)

**Step 1: Navigate and Activate**
```cmd
cd e:\Internship_Project
.venv\Scripts\activate.bat
```

**Step 2a: Run Streamlit**
```cmd
cd 08_Applications_UI_API
python -m streamlit run streamlit_app.py
```

**Step 2b: Run FastAPI**
```cmd
cd 08_Applications_UI_API
python fastapi_server.py
```

### Method 3: From Different Directory

If you want to run from a different location, specify the full path:

```powershell
# Streamlit from anywhere
python -m streamlit run "e:\Internship_Project\08_Applications_UI_API\streamlit_app.py"

# FastAPI from anywhere
python "e:\Internship_Project\08_Applications_UI_API\fastapi_server.py"
```

---

## ✅ VERIFICATION: How to Know It's Working

### Streamlit (Web App)
```
✓ Message: "You can now view your Streamlit app in your browser"
✓ Local URL: http://localhost:8501
✓ Open browser → Should see beautiful UI
```

### FastAPI (REST API)
```
✓ Message: "Uvicorn running on http://0.0.0.0:8000"
✓ Open browser → http://localhost:8000/docs
✓ Should see interactive Swagger documentation
```

---

## ⚠️ COMMON ISSUES & FIXES

| Issue | Solution |
|-------|----------|
| **"streamlit: command not found"** | Use `python -m streamlit run streamlit_app.py` |
| **"ModuleNotFoundError: fastapi"** | Run `pip install -r ../requirements.txt` from 08_Applications_UI_API folder |
| **"streamlit_app.py not found"** | Make sure you're in the correct directory or use full path |
| **Port 8501 already in use** | Use `python -m streamlit run streamlit_app.py --server.port 8502` |
| **Port 8000 already in use** | Kill existing process or use different port |

---

## 📂 NEW FILE LOCATIONS REFERENCE

```
e:\Internship_Project/
│
├── 🚀 RUN_STREAMLIT_APP.bat ............... Windows batch launcher
├── 🚀 RUN_STREAMLIT_APP.ps1 .............. PowerShell launcher
├── 🚀 RUN_FASTAPI_SERVER.bat ............. Windows batch launcher
├── 🚀 RUN_FASTAPI_SERVER.ps1 ............. PowerShell launcher
│
├── 08_Applications_UI_API/
│   ├── 📱 streamlit_app.py ............... Web UI (moved here)
│   ├── 🔌 fastapi_server.py .............. REST API (moved here)
│   ├── streamlit_app_OLD_BACKUP.py ....... Old version backup
│   └── fastapi_server_OLD_BACKUP.py ...... Old version backup
│
├── 07_Models_Trained/
│   └── final_optimized_churn_model.pkl ... Model (path updated in apps)
│
├── 05_Data_Splits/
│   ├── training_split.csv ............... Training data
│   ├── validation_split.csv ............. Validation data
│   ├── test_split.csv ................... Test data
│   └── holdout_split.csv ................ Holdout data
│
└── requirements.txt ..................... Dependencies
```

---

## 🎓 UNDERSTANDING THE NEW STRUCTURE

### Why Files Moved?

**Before (Root Directory Chaos):**
```
e:\Internship_Project/
├── streamlit_app.py
├── fastapi_server.py
├── *.png (charts)
├── *.md (docs)
├── *.py (scripts)
├── *.pkl (models)
└── ... (40+ files scattered)
```

**After (Organized Structure):**
```
e:\Internship_Project/
├── 01_Documentation/
├── 02_Diagrams_Methodology/
├── 03_Visualizations_Charts/
├── 04_Data_Raw/
├── 05_Data_Splits/
├── 06_ML_Scripts/
├── 07_Models_Trained/
├── 08_Applications_UI_API/     ← Apps moved here
└── RUN_*.bat / RUN_*.ps1 ← Launchers for convenience
```

### Applications Automatically Find Resources

The apps now use **dynamic path resolution** to find resources:

```python
# streamlit_app.py and fastapi_server.py do this:
current_dir = os.path.dirname(os.path.abspath(__file__))  # 08_Applications_UI_API/
parent_dir = os.path.dirname(current_dir)                  # e:\Internship_Project/

# Then find everything else:
model_path = os.path.join(parent_dir, "07_Models_Trained", "final_optimized_churn_model.pkl")
training_path = os.path.join(parent_dir, "05_Data_Splits", "training_split.csv")
```

**Benefit:** Apps automatically find resources regardless of where they're run from!

---

## 🎯 QUICK START CHEAT SHEET

```powershell
# ONE-LINER TO RUN STREAMLIT
cd e:\Internship_Project; .venv\Scripts\Activate.ps1; cd 08_Applications_UI_API; python -m streamlit run streamlit_app.py

# ONE-LINER TO RUN FASTAPI
cd e:\Internship_Project; .venv\Scripts\Activate.ps1; cd 08_Applications_UI_API; python fastapi_server.py

# OR JUST USE THE LAUNCHERS
.\RUN_STREAMLIT_APP.ps1
.\RUN_FASTAPI_SERVER.ps1
```

---

## ✨ TESTING THE FIXED APPLICATIONS

### Test 1: Different Inputs = Different Results

**Streamlit:**
1. Run: `.\RUN_STREAMLIT_APP.ps1`
2. Go to "🔮 Make Prediction" tab
3. Enter 5 different customer profiles
4. Verify each gets a DIFFERENT churn prediction ✅

**FastAPI:**
1. Run: `.\RUN_FASTAPI_SERVER.ps1`
2. Open: http://localhost:8000/docs
3. Click "POST /predict"
4. Send 5 different customer JSONs
5. Verify each gets a DIFFERENT result ✅

### Test 2: Verify Model Loads

**Both apps log on startup:**
```
✓ Model loaded successfully from 07_Models_Trained
✓ Training data loaded: 30+ features
```

If you see these messages, everything is working!

---

## 🔗 USEFUL LINKS

### When Apps Are Running:

- **Streamlit Web App:** http://localhost:8501
- **FastAPI Swagger:** http://localhost:8000/docs
- **FastAPI ReDoc:** http://localhost:8000/redoc

---

## 📞 TROUBLESHOOTING

### Still Getting File Not Found?

Make sure you're in the correct directory:

```powershell
# Check current directory
Get-Location

# Should show: E:\Internship_Project (when using launcher)
# Or: E:\Internship_Project\08_Applications_UI_API (when running manually)
```

### Apps Not Finding Model/Data?

Check that these files exist:
```powershell
Test-Path "07_Models_Trained/final_optimized_churn_model.pkl"     # Should be True
Test-Path "05_Data_Splits/training_split.csv"                    # Should be True
```

---

## ✅ SUMMARY

1. **Use Launcher Scripts** for easiest launch:
   - `.\RUN_STREAMLIT_APP.ps1` (or `.bat`)
   - `.\RUN_FASTAPI_SERVER.ps1` (or `.bat`)

2. **Apps automatically find** all resources:
   - Models in `07_Models_Trained/`
   - Data in `05_Data_Splits/`
   - Everything else in respective folders

3. **Test predictions** - different inputs should give different results!

4. **Access via browser:**
   - Streamlit: http://localhost:8501
   - FastAPI: http://localhost:8000/docs

---

**Everything is organized and ready!** 🎉
