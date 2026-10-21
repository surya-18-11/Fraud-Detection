import os
import sys
import subprocess
import base64
from pathlib import Path

BASE_DIR = Path(r"C:\Users\surya\.gemini\antigravity\scratch\fraud-detection")
FIGURES_DIR = BASE_DIR / "reports" / "figures"
HTML_OUT = BASE_DIR / "documentation.html"
PDF_OUT = BASE_DIR / "FraudShield_AI_Complete_Documentation.pdf"

def img_to_b64(img_path):
    if img_path.exists():
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

img_roc = img_to_b64(FIGURES_DIR / "phase6_roc_curves.png")
img_pr = img_to_b64(FIGURES_DIR / "phase6_pr_curves.png")
img_cm = img_to_b64(FIGURES_DIR / "phase6_confusion_matrices.png")
img_feat = img_to_b64(FIGURES_DIR / "phase6_xgboost_feature_importance.png")
img_cv = img_to_b64(FIGURES_DIR / "phase5_cv_comparison.png")
img_dist = img_to_b64(FIGURES_DIR / "phase1_fraud_distribution.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>FraudShield AI - Complete Technical Documentation</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {{
      content: counter(page);
    }}
  }}

  * {{ box-sizing: border-box; }}
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.55;
    font-size: 13px;
    margin: 0;
    padding: 0;
  }}

  .cover {{
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 90vh;
    padding: 60px 40px;
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #312e81 100%);
    color: #ffffff;
    border-radius: 12px;
  }}
  .cover h1 {{
    font-size: 38px;
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 16px 0;
    color: #f8fafc;
    letter-spacing: -0.5px;
  }}
  .cover .subtitle {{
    font-size: 18px;
    color: #a5b4fc;
    margin-bottom: 40px;
    font-weight: 400;
  }}
  .cover .meta-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid rgba(255,255,255,0.15);
  }}
  .meta-card {{
    background: rgba(255,255,255,0.06);
    padding: 14px 18px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
  }}
  .meta-card .label {{
    font-size: 11px;
    text-transform: uppercase;
    color: #94a3b8;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }}
  .meta-card .val {{
    font-size: 16px;
    font-weight: 700;
    color: #f1f5f9;
  }}

  h2 {{
    font-size: 20px;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #6366f1;
    padding-bottom: 6px;
    margin-top: 32px;
    margin-bottom: 14px;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 15px;
    font-weight: 600;
    color: #312e81;
    margin-top: 22px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}

  p, li {{
    font-size: 12.5px;
    color: #334155;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 12px;
    page-break-inside: avoid;
  }}
  th, td {{
    padding: 8px 12px;
    text-align: left;
    border: 1px solid #e2e8f0;
  }}
  th {{
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
  }}
  tr:nth-child(even) {{
    background: #f8fafc;
  }}

  pre, code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
  }}
  code {{
    background: #f1f5f9;
    padding: 2px 5px;
    border-radius: 4px;
    color: #4338ca;
  }}
  pre {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 12px 16px;
    border-radius: 8px;
    overflow-x: auto;
    line-height: 1.45;
    page-break-inside: avoid;
    margin: 12px 0;
  }}

  .alert {{
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 14px 0;
    font-size: 12px;
  }}
  .alert-title {{
    font-weight: 700;
    color: #1e40af;
    margin-bottom: 3px;
  }}

  .figure-box {{
    margin: 16px 0;
    text-align: center;
    page-break-inside: avoid;
  }}
  .figure-box img {{
    max-width: 95%;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  }}
  .figure-caption {{
    font-size: 11px;
    color: #64748b;
    margin-top: 6px;
    font-style: italic;
  }}

  .page-break {{
    page-break-after: always;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover">
  <div style="font-size:14px; font-weight:700; letter-spacing:1px; color:#818cf8; text-transform:uppercase; margin-bottom:12px;">Technical Specification & Architecture Dossier</div>
  <h1>FraudShield AI</h1>
  <div class="subtitle">End-to-End Enterprise Fraud Detection System Built on the IEEE-CIS Dataset</div>
  
  <p style="color:#cbd5e1; max-width:650px; font-size:14px; line-height:1.6;">
    An exhaustive, parameter-level architectural guide detailing every data pipeline stage, feature engineering method, hyperparameter configuration, evaluation strategy, and real-time inference decision framework.
  </p>

  <div class="meta-grid">
    <div class="meta-card">
      <div class="label">Primary Dataset</div>
      <div class="val">IEEE-CIS Fraud Detection (590,540 Txns)</div>
    </div>
    <div class="meta-card">
      <div class="label">Champion Model</div>
      <div class="val">XGBoost (ROC-AUC: 0.9399 | PR-AUC: 0.6413)</div>
    </div>
    <div class="meta-card">
      <div class="label">Fraud Recall</div>
      <div class="val">82.5% (Catches &gt;82% of all Fraud)</div>
    </div>
    <div class="meta-card">
      <div class="label">Production Serving</div>
      <div class="val">Streamlit Glassmorphism UI (4 Risk Tiers)</div>
    </div>
  </div>
</div>

<!-- SECTION 1 -->
<h2>1. Executive Summary & Problem Formulation</h2>
<p>
  Payment fraud accounts for tens of billions of dollars in annual global losses. In this project, we implement an enterprise-grade machine learning system trained on the benchmark <b>IEEE-CIS Fraud Detection dataset</b> provided by Vesta Corporation.
</p>
<div class="alert">
  <div class="alert-title">The Core Data Challenge: Severe Class Imbalance</div>
  Only <b>3.5%</b> of transactions in the dataset are fraudulent (20,663 positive cases out of 590,540). A naive classifier that predicts non-fraud 100% of the time achieves <b>96.5% accuracy</b> while catching <b>0% of fraud</b>. Thus, standard accuracy is useless; the system must optimize for <b>ROC-AUC</b>, <b>PR-AUC</b>, and especially <b>Fraud Recall</b> to minimize catastrophic false negatives.
</div>

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Logistic Regression</th>
      <th>Random Forest</th>
      <th>XGBoost (Champion)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>ROC-AUC</b></td>
      <td>0.8413</td>
      <td>0.9284</td>
      <td><b>0.9399</b></td>
    </tr>
    <tr>
      <td><b>PR-AUC</b></td>
      <td>0.3227</td>
      <td>0.6286</td>
      <td><b>0.6413</b></td>
    </tr>
    <tr>
      <td><b>Fraud Recall</b></td>
      <td>74.3%</td>
      <td>77.2%</td>
      <td><b>82.5%</b></td>
    </tr>
    <tr>
      <td><b>F1-Score</b></td>
      <td>0.190</td>
      <td>0.403</td>
      <td><b>0.380</b></td>
    </tr>
  </tbody>
</table>

<!-- SECTION 2 -->
<h2>2. Data Ingestion Pipeline (<code>src/data_loader.py</code>)</h2>
<p>
  The IEEE-CIS dataset consists of two relational tables linked by <code>TransactionID</code>:
</p>
<ul>
  <li><b>Transactions Table (<code>train_transaction.csv</code>)</b>: 590,540 rows × 394 features. Contains monetary amounts, product codes, card network data, address zones, email domains, and Vesta-engineered V-features.</li>
  <li><b>Identity Table (<code>train_identity.csv</code>)</b>: 144,233 rows × 41 features. Contains device information, browser signatures, OS versions, and network proxy indicators.</li>
</ul>

<h3>Engineering Decision: In-Memory Pickling</h3>
<pre>pd.to_pickle(path)  # and pd.read_pickle(path)</pre>
<p>
  <b>Why we used it:</b> Parsing 650 MB of raw CSVs in Pandas takes 2 to 3 minutes each run. Pickling serializes the exact C-level memory structures of dataframes into binary blocks, slashing loading time to under <b>2.5 seconds</b>.
</p>

<!-- SECTION 3 -->
<h2>3. Cleaning & Preprocessing (<code>src/preprocessor.py</code>)</h2>

<h3>3.1 Relational Join Strategy</h3>
<pre>merged = txn_df.merge(id_df, on='TransactionID', how='left')</pre>
<ul>
  <li><b>Parameter:</b> <code>how='left'</code> on <code>TransactionID</code></li>
  <li><b>Rationale:</b> Only ~24.4% of transactions have an identity record. Performing an <code>inner</code> join would drop 75.6% of valid transactions. A <code>left</code> join retains all payments while enriching rows that possess digital identity signatures.</li>
</ul>

<h3>3.2 Sparse Feature Pruning</h3>
<pre>drop_high_missing(df, threshold=0.5)</pre>
<ul>
  <li><b>Parameter:</b> <code>threshold = 0.5</code> (50% missing cutoff)</li>
  <li><b>Rationale:</b> Over 200 V-columns and ID variables have 70% to 90% missing values. Imputing attributes that are 80-90% missing manufactures artificial variance and causes decision trees to overfit on noise. Dropping &gt;50% missing columns eliminates noise while preserving core signal.</li>
  <li><b>Safeguard:</b> <code>[c for c in cols if c != 'isFraud']</code> ensures the ground-truth target is never dropped.</li>
</ul>

<h3>3.3 Numeric Imputation</h3>
<pre>SimpleImputer(strategy='median')</pre>
<ul>
  <li><b>Parameter:</b> <code>strategy = 'median'</code></li>
  <li><b>Rationale:</b> Financial transactions are heavily right-skewed with extreme outliers (e.g. $5,000 corporate transactions). The mathematical mean is severely distorted by outliers, whereas the <b>median</b> represents the true central tendency of payment behavior.</li>
</ul>

<h3>3.4 Categorical Encoding</h3>
<pre>LabelEncoder() with fillna('unknown')</pre>
<ul>
  <li><b>Rationale:</b> High-cardinality columns (e.g. <code>card1</code> with 13,000+ unique values) would cause a catastrophic explosion in memory and dimensional collapse if One-Hot Encoded. Label encoding compacts variables into 1D integer space, which tree-based algorithms bifurcate with ease.</li>
  <li><b>Unseen Label Guard:</b> Test set elements not present in training are safely mapped to <code>'unknown'</code> rather than raising runtime index errors.</li>
</ul>

<div class="page-break"></div>

<!-- SECTION 4 -->
<h2>4. Feature Engineering Architecture (<code>src/feature_engineer.py</code>)</h2>

<h3>4.1 Cyclical Time Transformation</h3>
<pre>df['tx_hour'] = ((dt / 3600) % 24).astype(int)
df['tx_hour_sin'] = np.sin(2 * np.pi * df['tx_hour'] / 24)
df['tx_hour_cos'] = np.cos(2 * np.pi * df['tx_hour'] / 24)</pre>
<p>
  <b>Why Cyclical Encoding?</b> In linear coordinates, 11:00 PM (hour 23) and 1:00 AM (hour 1) appear 22 units apart. By mapping hours onto the unit circle via sine and cosine, late night and early morning become geometrically adjacent, allowing models to detect nocturnal fraud rings.
</p>

<h3>4.2 Group-Based Aggregation Features (Z-Score Signals)</h3>
<pre>group_cols = ['card1', 'card4', 'addr1', 'P_emaildomain']
df['card1_amt_mean'] = df['card1'].map(grp.mean())
df['card1_amt_std']  = df['card1'].map(grp.std()).fillna(0)</pre>
<p>
  <b>Why Group Aggregations?</b> A $400 transaction is normal for a corporate platinum card, but highly anomalous for a card whose historical mean is $25. Group aggregations provide dynamic baselines against which anomalous deviations can be measured.
</p>

<h3>4.3 Frequency Encoding</h3>
<pre>df[f'{{col}}_freq'] = df[col].map(df[col].value_counts())</pre>
<p>
  <b>Why Frequency Encoding?</b> Replaces raw categorical IDs with their global popularity. Legitimate transactions concentrate in high-frequency card IDs and reputable email domains; fraud syndicates frequently cycle through burner cards and ephemeral domains (frequency = 1 or 2).
</p>

<h3>4.4 Log-1p Transformation</h3>
<pre>df['TransactionAmt_log'] = np.log1p(df['TransactionAmt'].fillna(0))</pre>
<p>
  <b>Why log1p?</b> Since transaction amounts and distances can be zero, standard $\ln(0)$ yields $-\infty$. $\ln(1 + x)$ is smooth, monotonic, defined at $x=0$, and compresses exponential distribution tails into Gaussian-like bell curves.
</p>

<!-- SECTION 5 -->
<h2>5. Machine Learning Models & Hyperparameter Specifications (<code>src/models.py</code>)</h2>

<h3>5.1 XGBoost Classifier (Champion Model)</h3>
<table>
  <thead>
    <tr>
      <th>Hyperparameter</th>
      <th>Configured Value</th>
      <th>Deep Architectural Rationale</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>n_estimators</code></td>
      <td><b>500</b></td>
      <td>Provides sufficient boosting iterations to learn nuanced fraud interactions.</td>
    </tr>
    <tr>
      <td><code>learning_rate</code></td>
      <td><b>0.05</b></td>
      <td>Conservative shrinkage factor prevents the model from taking over-aggressive gradient steps.</td>
    </tr>
    <tr>
      <td><code>max_depth</code></td>
      <td><b>6</b></td>
      <td>Constrains tree depth to prevent memorization of individual transaction combinations.</td>
    </tr>
    <tr>
      <td><code>min_child_weight</code></td>
      <td><b>10</b></td>
      <td>Requires a minimum Hessian sum of 10 in leaf nodes, pruning splits created by rare noisy anomalies.</td>
    </tr>
    <tr>
      <td><code>subsample</code></td>
      <td><b>0.8</b></td>
      <td>Stochastic bagging: 80% row subsampling per tree prevents overfitting to dominant clusters.</td>
    </tr>
    <tr>
      <td><code>colsample_bytree</code></td>
      <td><b>0.8</b></td>
      <td>80% feature subsampling forces trees to discover secondary fraud predictors.</td>
    </tr>
    <tr>
      <td><code>scale_pos_weight</code></td>
      <td><b>~27.5</b></td>
      <td>Ratio of non-fraud to fraud (<code>570,000 / 20,600</code>). Directly amplifies fraud loss gradient by 27.5x.</td>
    </tr>
    <tr>
      <td><code>eval_metric</code></td>
      <td><b>'auc'</b></td>
      <td>Guides early stopping and boosting splits on ROC-AUC rather than logloss.</td>
    </tr>
  </tbody>
</table>

<h3>5.2 Random Forest Classifier</h3>
<ul>
  <li><code>n_estimators = 300</code>: 300 bagged trees eliminate ensemble variance.</li>
  <li><code>max_depth = 15</code>: Prevents trees from growing to infinite depth on 590K rows.</li>
  <li><code>min_samples_leaf = 10</code>: Restricts leaves to statistically significant sample groupings.</li>
  <li><code>class_weight = 'balanced'</code>: Automatically adjusts inverse class penalties.</li>
</ul>

<h3>5.3 Isolation Forest (Unsupervised Zero-Day Detection)</h3>
<ul>
  <li><code>contamination = 0.035</code>: Set to exactly match the empirical fraud rate (3.5%). Identifies zero-day attack patterns without needing historical fraud labels.</li>
</ul>

<div class="page-break"></div>

<!-- SECTION 6 -->
<h2>6. Model Evaluation & Visualizations</h2>

<div class="figure-box">
  {"<img src='" + img_roc + "' alt='ROC Curves' />" if img_roc else "<p>ROC Curves Figure</p>"}
  <div class="figure-caption">Figure 1: Receiver Operating Characteristic (ROC) Comparison across Models. XGBoost dominates with 0.9399 AUC.</div>
</div>

<div class="figure-box">
  {"<img src='" + img_pr + "' alt='PR Curves' />" if img_pr else "<p>PR Curves Figure</p>"}
  <div class="figure-caption">Figure 2: Precision-Recall Curves on Imbalanced Data. XGBoost maintains superior average precision (0.6413).</div>
</div>

<div class="figure-box">
  {"<img src='" + img_feat + "' alt='Feature Importance' />" if img_feat else "<p>Feature Importance Figure</p>"}
  <div class="figure-caption">Figure 3: Top Feature Importances in XGBoost. Transaction amount aggregates, card frequency, and V-features dominate.</div>
</div>

<div class="page-break"></div>

<!-- SECTION 7 -->
<h2>7. Production Inference Engine & Web Dashboard (<code>app/app.py</code> & <code>src/predictor.py</code>)</h2>

<h3>7.1 Calibrated Four-Tier Risk Framework</h3>
<p>
  Binary approve/decline rules create friction for customers and cause massive false decline costs. FraudShield AI establishes a 4-tier decision engine:
</p>

<table>
  <thead>
    <tr>
      <th>Risk Tier</th>
      <th>Probability Window</th>
      <th>System Action</th>
      <th>User Experience Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Low</b></td>
      <td>0.00 – 0.29</td>
      <td><b>Instant Approval</b></td>
      <td>Zero friction; instant payment clearance.</td>
    </tr>
    <tr>
      <td><b>Medium</b></td>
      <td>0.30 – 0.59</td>
      <td><b>Step-Up Challenge</b></td>
      <td>Triggers 3D-Secure 2.0 or SMS OTP verification.</td>
    </tr>
    <tr>
      <td><b>High</b></td>
      <td>0.60 – 0.79</td>
      <td><b>Manual Review</b></td>
      <td>Transferred to internal fraud operations desk.</td>
    </tr>
    <tr>
      <td><b>Critical</b></td>
      <td>0.80 – 1.00</td>
      <td><b>Hard Block</b></td>
      <td>Transaction blocked immediately and payment instrument frozen.</td>
    </tr>
  </tbody>
</table>

<h3>7.2 Web Application Features</h3>
<ul>
  <li><b>Live Single Transaction Risk Screener:</b> Real-time parameter inputs with animated Plotly Gauge meter.</li>
  <li><b>Batch Processing Engine:</b> Upload CSV files with hundreds of transactions; outputs probability distributions, risk breakdowns, and downloadable audited CSV reports.</li>
  <li><b>Live Model Performance Benchmark:</b> Interactively review confusion matrices, ROC/PR curves, and feature importance bar plots directly within Streamlit.</li>
  <li><b>State Management:</b> Utilizes <code>@st.cache_resource</code> to retain pre-loaded model pickles in RAM, guaranteeing sub-50ms inference times.</li>
</ul>

<!-- SECTION 8 -->
<h2>8. Pipeline Automation (<code>run_pipeline.py</code>)</h2>
<p>
  The full training and evaluation workflow is automated via <code>nbconvert</code>:
</p>
<pre>python run_pipeline.py --start-from 2 --stop-at 7</pre>
<ul>
  <li><b>Execution Timeout:</b> <code>--ExecutePreprocessor.timeout=3600</code> (1 hour cap per notebook to accommodate heavy cross-validation).</li>
  <li><b>Granular Resumption:</b> <code>--start-from N</code> allows engineers to resume model training without repeating 3-minute CSV preprocessing passes.</li>
</ul>

<div style="margin-top:40px; padding:16px; background:#f8fafc; border-radius:8px; border:1px solid #e2e8f0; font-size:11.5px; color:#64748b; text-align:center;">
  FraudShield AI Technical Dossier • Compiled for Enterprise Payment Protection • Built with Python 3.13 &amp; IEEE-CIS Benchmark
</div>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML at {HTML_OUT}")

# Try Chrome or Edge
chrome_path = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
edge_path = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

browser_bin = chrome_path if chrome_path.exists() else edge_path

cmd = [
    str(browser_bin),
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_OUT}",
    "--no-pdf-header-footer",
    str(HTML_OUT)
]

print(f"Executing: {' '.join(cmd)}")
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"Return code: {res.returncode}")
if PDF_OUT.exists():
    print(f"SUCCESS: PDF created at {PDF_OUT} ({PDF_OUT.stat().st_size / 1024:.1f} KB)")
else:
    print(f"FAILED: stderr={res.stderr}")
