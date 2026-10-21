# FraudShield AI — IEEE-CIS Fraud Detection System

> **An end-to-end machine learning pipeline for detecting fraudulent payment transactions,
> built on the IEEE-CIS dataset with a live Streamlit web application.**

---

## Quick Start

```powershell
# 1. Navigate to project
cd C:\Users\surya\.gemini\antigravity\scratch\fraud-detection

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Launch the web app
.\venv\Scripts\streamlit run app\app.py
```

Open **http://localhost:8501** in your browser.

---

## Project Overview

| Item | Detail |
|---|---|
| **Dataset** | IEEE-CIS Fraud Detection (Kaggle) |
| **Training samples** | 590,540 transactions |
| **Features** | 434 (after merge) → engineered to ~200 |
| **Fraud rate** | 3.5% (highly imbalanced) |
| **Best model** | XGBoost — ROC-AUC: **0.9399** |
| **Fraud recall** | **82.5%** (catches 82.5% of all fraud) |
| **Python version** | 3.13 |

---

## Web Application — User Guide

### Page 1: Single Transaction Analysis

Enter details about a transaction and get an **instant risk assessment**:

1. Fill in the transaction form on the left:
   - Transaction Amount, Product Code, Card details
   - Email domain, Device type, Distance
2. Click **"Analyze Transaction Risk"**
3. You'll see:
   - A **risk gauge** showing fraud probability (0–100%)
   - A **risk tier badge**: 🟢 Low / 🟡 Medium / 🟠 High / 🔴 Critical
   - A **decision**: APPROVE or BLOCK (at 0.5 threshold)

| Risk Tier | Probability | Action |
|---|---|---|
| 🟢 Low | 0–30% | Approve automatically |
| 🟡 Medium | 30–60% | Request additional authentication |
| 🟠 High | 60–80% | Manual review recommended |
| 🔴 Critical | 80–100% | Block transaction immediately |

---

### Page 2: Batch Analysis

Screen multiple transactions at once using a CSV file:

1. Click **"Browse files"** and upload your CSV
2. The CSV should contain transaction features (at minimum: `TransactionAmt`, `TransactionDT`, `ProductCD`, `card1`)
3. Click **"Run Batch Prediction"**
4. Results shown:
   - Total transactions, flagged count, fraud rate, average risk score
   - Risk tier distribution pie chart
   - Probability distribution histogram
5. Click **"Download Results CSV"** to export predictions

---

### Page 3: Model Performance

Live dashboard showing your trained model results:

- **Best model card** at the top (XGBoost with ROC-AUC 0.9399)
- **Comparison table**: ROC-AUC, PR-AUC, F1, Precision, Recall for all 3 models
- **Bar chart**: Visual metric comparison across models
- **Training plots**: ROC curves, confusion matrices, feature importance

---

### Page 4: About

Full documentation of the project, dataset, and tech stack.

---

## Running Individual Phases

Each phase is a standalone Jupyter notebook:

```powershell
# Activate environment first
.\venv\Scripts\Activate.ps1

# Launch Jupyter
jupyter notebook
```

Open any notebook from the `notebooks/` folder and select kernel:
**"Fraud Detection (venv)"** → then **Kernel → Restart & Run All**

| Notebook | What it does | Runtime |
|---|---|---|
| `phase1_load_data.ipynb` | Load & explore raw data | ~3 min |
| `phase2_preprocessing.ipynb` | Merge, clean, encode | ~2 min |
| `phase3_eda.ipynb` | 12 EDA visualizations | ~2 min |
| `phase4_feature_engineering.ipynb` | Create & scale features | ~1 min |
| `phase5_model_training.ipynb` | Train LR + RF + XGBoost | ~10 min |
| `phase6_evaluation.ipynb` | Metrics, ROC, PR, importance | ~1 min |
| `phase7_anomaly_detection.ipynb` | Isolation Forest | ~1 min |

---

## Re-running the Full Pipeline

To re-train everything from scratch (after Phase 1):

```powershell
# Run all phases 2 through 7
python run_pipeline.py

# Resume from a specific phase (e.g., re-train models only)
python run_pipeline.py --start-from 5

# Run only EDA + feature engineering
python run_pipeline.py --start-from 3 --stop-at 4
```

Expected total time: **~13 minutes**

---

## Project Structure

```
fraud-detection/
├── data/
│   ├── raw/                    ← Original CSV files (do not modify)
│   └── processed/              ← Auto-generated pickle files
├── notebooks/                  ← Phase notebooks (run in order)
├── src/                        ← Reusable Python modules
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── feature_engineer.py
│   ├── models.py
│   ├── evaluator.py
│   └── predictor.py
├── models/                     ← Trained model files
│   ├── xgboost_model.pkl       ← Best model (1.2 MB)
│   ├── random_forest.pkl       ← (63 MB)
│   ├── logistic_regression.pkl ← Baseline
│   └── isolation_forest.pkl    ← Anomaly detection
├── app/
│   └── app.py                  ← Streamlit web application
├── reports/
│   ├── figures/                ← 21 generated plots
│   ├── model_comparison.csv    ← Performance table
│   └── cv_results.csv          ← Cross-validation scores
├── run_pipeline.py             ← Master pipeline runner
├── requirements.txt
└── README.md
```

---

## Model Results

```
┌─────────────────────┬──────────┬────────┬───────┬───────────┬────────┐
│ Model               │ ROC-AUC  │ PR-AUC │  F1   │ Precision │ Recall │
├─────────────────────┼──────────┼────────┼───────┼───────────┼────────┤
│ Logistic Regression │  0.8413  │ 0.3227 │ 0.190 │   0.109   │ 0.743  │
│ Random Forest       │  0.9284  │ 0.6286 │ 0.403 │   0.272   │ 0.772  │
│ XGBoost ★ BEST      │  0.9399  │ 0.6413 │ 0.380 │   0.246   │ 0.825  │
└─────────────────────┴──────────┴────────┴───────┴───────────┴────────┘
```

**XGBoost** catches **82.5% of all fraud** on the held-out test set.

---

## Setup from Scratch

If setting up on a new machine:

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install all dependencies
pip install -r requirements.txt

# 3. Register Jupyter kernel
python -m ipykernel install --user --name fraud-detection-venv --display-name "Fraud Detection (venv)"

# 4. Place dataset files in data/raw/:
#    train_transaction.csv, train_identity.csv
#    test_transaction.csv, test_identity.csv

# 5. Run Phase 1 manually in Jupyter, then run the pipeline
python run_pipeline.py

# 6. Launch the app
.\venv\Scripts\streamlit run app\app.py
```

---

## Tech Stack

| Category | Libraries |
|---|---|
| Data processing | `pandas 3.0.5`, `numpy 2.5.3` |
| Machine learning | `scikit-learn 1.9.1`, `xgboost 3.4.1` |
| Imbalanced data | `imbalanced-learn 0.14.2` |
| Explainability | `shap 0.52.0` |
| Visualization | `matplotlib 3.11.2`, `seaborn 0.13.2`, `plotly 5.x` |
| Web application | `streamlit 1.63.0` |
| Model persistence | `joblib 1.4+` |
| Notebooks | `jupyter`, `nbconvert 7.17.1` |

---

## Troubleshooting

| Issue | Solution |
|---|---|
| App shows "No models found" | Run `python run_pipeline.py` first |
| Kernel not found in Jupyter | Run `python -m ipykernel install --user --name fraud-detection-venv --display-name "Fraud Detection (venv)"` |
| Phase 2 takes too long | Normal — loading 650MB CSVs takes 2–3 minutes |
| Streamlit port in use | Change port: `streamlit run app\app.py --server.port 8502` |
| Unicode error in terminal | Safe to ignore — cosmetic only, does not affect results |

---

*Built with Python 3.13 · IEEE-CIS Fraud Detection Dataset · Kaggle*
