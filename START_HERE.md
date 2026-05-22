# 🎯 START HERE - Quick Launch Guide

## ⚡ Quick Start (2 Options)

### Option 1: Run Web App (Recommended for Most Users)
```powershell
.\RUN_STREAMLIT_APP.ps1
```
👉 Opens interactive web app at http://localhost:8501

### Option 2: Run REST API (For Developers)
```powershell
.\RUN_FASTAPI_SERVER.ps1
```
👉 Opens API docs at http://localhost:8000/docs

---

## 📍 Current Status

✅ All 3 Major Issues Fixed:
1. ✅ Files organized into 8 folders
2. ✅ Data consolidated (12 → 4 files)  
3. ✅ Predictions working (different per input!)

---

## 📚 Documentation

- **Quick Launch:** This file (you are here!)
- **Detailed Running Guide:** `01_Documentation/HOW_TO_RUN_APPLICATIONS.md`
- **Complete Summary:** `FINAL_COMPLETE_SUMMARY.md`
- **Technical Details:** `01_Documentation/PROJECT_REORGANIZATION_FIXES.md`

---

## 🗂️ Project Structure

```
08_Applications_UI_API/     ← Applications are here
├── streamlit_app.py        ← Web UI
└── fastapi_server.py       ← REST API

07_Models_Trained/          ← ML Model
├── final_optimized_churn_model.pkl

05_Data_Splits/             ← Training data
├── training_split.csv
├── validation_split.csv
├── test_split.csv
└── holdout_split.csv
```

---

## 🧪 Test It!

1. Run: `.\RUN_STREAMLIT_APP.ps1`
2. Go to "🔮 Make Prediction" tab
3. Enter customer details
4. Verify different inputs give different predictions ✅

---

## ⚠️ Before You Start

### For PowerShell Users (Recommended)
If you get execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### For Command Prompt Users
Use batch files instead:
```cmd
RUN_STREAMLIT_APP.bat
```

---

## 📞 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Script won't run | Use batch file instead: `RUN_STREAMLIT_APP.bat` |
| "Port already in use" | Close other instances or wait 30 seconds |
| "Module not found" | Make sure `.venv` exists and environment is activated |
| "Same predictions for all inputs" | You have the OLD version - files are now in `08_Applications_UI_API/` |

---

## ✨ What Changed?

**Files Reorganized:**
- Before: 40+ files scattered in root
- After: 8 organized folders + 4 launchers

**Data Consolidated:**
- Before: 12 redundant files (training_X.csv, training_y.csv, etc.)
- After: 4 clean consolidated files

**Predictions Fixed:**
- Before: Same 78% for all inputs ❌
- After: Different predictions per input ✅

---

## 🚀 Ready to Go!

```powershell
.\RUN_STREAMLIT_APP.ps1
```

**Done!** 🎉

For more details, see `FINAL_COMPLETE_SUMMARY.md` or `01_Documentation/HOW_TO_RUN_APPLICATIONS.md`
