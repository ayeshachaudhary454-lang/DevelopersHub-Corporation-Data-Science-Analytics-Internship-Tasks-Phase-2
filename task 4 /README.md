# Task 4: Loan Default Risk with Business Cost Optimization (Home Credit)

## 📌 Objective
Predict the likelihood of a loan default and optimize the decision
threshold based on cost-benefit analysis rather than a generic 0.5 cutoff.

## 📊 Dataset
- **Name:** Home Credit Default Risk Dataset
- **Rows:** ~215,000 loan applications, 102 columns
- **Target:** `TARGET` — 1 = client had difficulty repaying (defaulted), 0 = repaid on time
- **Loaded directly from a public mirror inside the notebook** — no manual download needed

The dataset includes socio-demographic info, income, loan details, and
external credit bureau scores for each applicant.

## 🛠️ Approach

### 1. Data Cleaning & Preprocessing
- Dropped 32 columns with more than 40% missing values
- Dropped the ID column (not predictive)
- Imputed remaining missing numeric values with the median, categorical with `"missing"`
- One-Hot Encoded 12 categorical columns → final encoded shape (215,257 × 171)

### 2. Exploratory Data Analysis
- Target is highly imbalanced: only ~8% of loans defaulted
- Applicants with lower education levels showed a noticeably higher default rate
- Income and credit amount both varied meaningfully between repaid and defaulted loans

### 3. Model Building
Trained and compared two binary classifiers:
- **Logistic Regression** — interpretable baseline
- **CatBoost** — handles categorical structure and non-linear relationships natively

80/20 stratified train-test split (172,205 train / 43,052 test).

### 4. Business Cost Optimization
- Defined asymmetric costs: **$1,000** for a false positive (rejecting a good customer) vs. **$15,000** for a false negative (approving a loan that defaults) — a realistic 15:1 ratio reflecting that missed defaults are typically far costlier than missed approvals
- Swept classification thresholds from 0.05 to 0.95, computing total business cost at each
- Selected the threshold that minimizes total simulated cost, rather than defaulting to 0.5

### 5. Feature Importance
- Extracted CatBoost's built-in feature importance to identify key default risk drivers

## 📈 Results

| Model | ROC-AUC |
|---|---|
| Logistic Regression | 0.7178 |
| CatBoost | 0.7303 |

CatBoost outperformed the logistic regression baseline, as expected for
tabular data with non-linear feature interactions.

### Cost-Optimal Threshold vs. Default Threshold

| Threshold | Precision | Recall | F1-Score | Total Cost |
|---|---|---|---|---|
| 0.50 (default) | 0.159 | 0.632 | 0.254 | $30,915,000 |
| 0.43 (cost-optimal) | 0.136 | 0.740 | 0.230 | $30,014,000 |

**Optimal threshold: 0.43 | Savings from optimization: $901,000**

Shifting the threshold below 0.5 **traded precision for recall** —
catching significantly more true defaults (74.0% vs. 63.2%) at the cost of
flagging more good customers as risky. Given the 15:1 cost asymmetry
between missed defaults and missed approvals, this trade-off reduced total
simulated business cost by roughly $901K on the test set.

### Top Risk Drivers (CatBoost Feature Importance)
1. `EXT_SOURCE_2` / `EXT_SOURCE_3` / `EXT_SOURCE_4` — normalized external credit bureau scores (dominant predictors)
2. `AMT_GOODS_PRICE`, `AMT_CREDIT`, `AMT_ANNUITY`, `AMT_INCOME_TOTAL` — loan and income amounts
3. `DAYS_AGE`, `DAYS_EMPLOYMENT` — applicant age and employment tenure

## 💡 Recommendations
1. Calibrate the classification threshold to the lender's actual cost structure rather than defaulting to 0.5 — the "best" threshold from a pure accuracy/F1 standpoint is not the threshold that minimizes real financial loss
2. Prioritize collecting/maintaining external bureau scores (`EXT_SOURCE_*`), since they are the strongest available predictors of default
3. Periodically re-estimate the false-positive/false-negative cost ratio, since it directly determines the optimal threshold and should reflect actual portfolio economics, not a fixed assumption

## 🧰 Tools & Libraries
`pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `catboost`

## ▶️ How to Run
```bash
pip install pandas numpy scikit-learn matplotlib seaborn catboost requests
jupyter notebook task4/loan_default_risk.ipynb
```
Then Run All Cells — the dataset downloads automatically at the start of the notebook.

## ✅ Task Checklist
- [x] Cleaned and preprocessed the dataset
- [x] Trained binary classification models (Logistic Regression, CatBoost)
- [x] Defined business cost values for false positives and false negatives
- [x] Adjusted the model threshold to minimize total business cost
- [x] Feature importance analysis
