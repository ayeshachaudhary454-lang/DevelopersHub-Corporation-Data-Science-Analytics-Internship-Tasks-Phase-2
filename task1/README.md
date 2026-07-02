# Task 1: Term Deposit Subscription Prediction (Bank Marketing)

## 📌 Objective
Predict whether a bank customer will subscribe to a term deposit as a result of a
marketing campaign, and explain individual model predictions using SHAP.

## 📊 Dataset
- **Name:** Bank Marketing Dataset
- **Source:** UCI Machine Learning Repository — https://archive.ics.uci.edu/dataset/222/bank+marketing
- **File used:** `bank-additional-full.csv` (41,188 rows, 20 input features + target `y`)
- **Target variable:** `y` — has the client subscribed to a term deposit? (`yes` / `no`)

### Feature groups
| Type | Examples |
|---|---|
| Client demographics | age, job, marital, education, default, housing, loan |
| Campaign contact info | contact, month, day_of_week, duration, campaign |
| Previous campaign | pdays, previous, poutcome |
| Economic context | emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed |

> ⚠️ Note: `duration` is highly predictive but is only known **after** a call ends,
> so it causes data leakage if the goal is a pre-call prediction model. This is
> kept in the model as instructed by the task, with the caveat flagged in the notebook.

## 🛠️ Approach

### 1. Data Loading & Exploration
- Loaded the dataset directly from a public UCI mirror using pandas
- Checked shape (41,188 rows × 21 columns), dtypes, and `"unknown"` placeholder values
- Examined class balance of the target: **88.7% "no" vs 11.3% "yes"** — a significantly imbalanced target

### 2. Data Cleaning & Preprocessing
- Kept `"unknown"` category values as-is (may carry predictive signal) rather than dropping rows
- One-Hot Encoded nominal categorical features (job, marital, contact, month, poutcome, etc.)
- Ordinal-encoded `education` (natural order: illiterate → basic → high school → university)
- Scaled numeric features for Logistic Regression (StandardScaler)
- Addressed class imbalance using `class_weight='balanced'` on both models

### 3. Model Building
Trained and compared:
- **Logistic Regression** — interpretable baseline
- **Random Forest Classifier** — stronger non-linear performance

Stratified 80/20 train-test split used to preserve class ratio (32,950 train / 8,238 test).

### 4. Model Evaluation
- Confusion Matrix for both models
- Precision, Recall, and **F1-score** (prioritized over accuracy due to class imbalance)
- ROC Curve and AUC score

### 5. Explainable AI (SHAP)
- Used `shap.TreeExplainer` on a Random Forest model to compute SHAP values
- Generated a **global SHAP summary plot** (bar + beeswarm) to identify top drivers of subscription
- Generated **individual SHAP waterfall plots for 5 sample predictions**
  (correctly predicted "yes", correctly predicted "no", and one misclassified case)

## 📈 Results & Findings

| Model | F1-Score | ROC-AUC |
|---|---|---|
| Logistic Regression | 0.605 | 0.944 |
| Random Forest | 0.550 | 0.951 |

**Key observations:**
- Both models achieve strong ROC-AUC (>0.94), meaning they rank customers by subscription likelihood very well
- Logistic Regression achieved a higher F1-score under the balanced-class setup, while Random Forest achieved a marginally higher AUC and provided richer, non-linear SHAP explanations
- **Top global drivers of subscription (from SHAP):** economic indicators (`nr.employed`, `euribor3m`, `emp.var.rate`), previous campaign outcome (`poutcome_success`), and call `duration`
- Customers contacted during periods of less favorable macro-economic conditions (lower employment, lower interest rate environment) were more likely to subscribe — term deposits become relatively more attractive investments in those periods
- A previously **successful** campaign outcome is one of the strongest positive individual-level signals, as shown consistently across the SHAP waterfall plots

## 💡 Recommendations
1. Prioritize recontacting customers with a previous successful campaign outcome — they convert at a much higher rate than average
2. Use the ROC curve to choose a decision threshold that matches the marketing team's actual calling capacity and recall needs
3. Since `duration` is only known after a call happens, build a secondary **pre-call model excluding `duration`** if the goal is deciding who to call before the conversation
4. Time campaigns around favorable macro-economic conditions and monitor conversion by month

## 🧰 Tools & Libraries
`pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `shap`

## 📁 Repository Structure
