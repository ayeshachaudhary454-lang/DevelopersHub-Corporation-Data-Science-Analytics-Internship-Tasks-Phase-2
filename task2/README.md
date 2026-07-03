# Task 2: Customer Segmentation Using Unsupervised Learning (Mall Customers)

## 📌 Objective
Cluster customers based on spending habits and propose marketing strategies
tailored to each identified segment.

## 📊 Dataset
- **Name:** Mall Customers Dataset
- **Rows:** 200 customers, 5 columns
- **Loaded directly from a public URL inside the notebook** — no local CSV needed

| Column | Description |
|---|---|
| CustomerID | Unique identifier |
| Gender | Male / Female |
| Age | Customer age |
| Annual Income (k$) | Annual income in thousands of dollars |
| Spending Score (1-100) | Score assigned by the mall based on customer behavior and spending |

No missing values across any column.

## 🛠️ Approach

### 1. Exploratory Data Analysis (EDA)
- Examined distributions of Age, Annual Income, and Spending Score
- Checked gender balance (~56% female / 44% male)
- Visualized Income vs. Spending Score (colored by Age) — visible cluster structure was already apparent before any modeling

### 2. Preprocessing
- Selected **Age**, **Annual Income**, and **Spending Score** as clustering features (CustomerID dropped; Gender excluded from clustering but kept for profiling)
- Standardized features with `StandardScaler`, since K-Means is distance-based and income (tens of thousands) would otherwise dominate over spending score (1-100) and age (18-70) purely due to scale

### 3. Finding the Optimal Number of Clusters
- **Elbow Method**: inertia plotted for k = 2 to 10 — clear bend around k = 5
- **Silhouette Score**: peaked at k = 5-6 (0.417-0.428)
- Selected **k = 5**, the standard, business-interpretable segmentation for this dataset

### 4. K-Means Clustering
- Applied `KMeans(n_clusters=5, random_state=42, n_init=10)` on the standardized features
- Visualized clusters directly (Income vs. Spending Score) with centroids marked
- Validated the clustering held up in full feature space using **PCA** and **t-SNE** 2D projections
- Compared Age / Income / Spending Score distributions across clusters via boxplots

## 📈 Results — Cluster Profiles

| Cluster | Count | Avg Age | Avg Income (k$) | Avg Spending Score | Segment |
|---|---|---|---|---|---|
| 0 | 20 | 46.2 | 26.8 | 18.4 | Budget-Conscious (Low Income, Low Spending) |
| 1 | 54 | 25.2 | 41.1 | 62.2 | Impulse / Trend-Driven (Low-Mid Income, High Spending) |
| 2 | 40 | 32.9 | 86.1 | 81.5 | VIP / Premium (High Income, High Spending) |
| 3 | 39 | 39.9 | 86.1 | 19.4 | Untapped Potential (High Income, Low Spending) |
| 4 | 47 | 55.6 | 54.4 | 48.9 | Standard / Average (Moderate Income, Moderate Spending) |

**Key finding:** spending behavior is not simply proportional to income.
Cluster 2 and Cluster 3 have nearly identical average income (~86k) but
wildly different spending scores (81.5 vs 19.4) — a pattern that plain
income-based segmentation would completely miss.

## 💡 Recommended Marketing Strategies

**Cluster 2 — VIP / Premium (High Income, High Spending)**
- Highest priority: loyalty programs, early access to sales, premium/exclusive product lines
- Personalized outreach; protect this segment's satisfaction above all others

**Cluster 3 — Untapped Potential (High Income, Low Spending)**
- Biggest revenue opportunity: same spending power as Cluster 2 but not converting
- Investigate product-fit or trust barriers; use targeted promotions and personalized recommendations

**Cluster 1 — Impulse / Trend-Driven (Low-Mid Income, High Spending)**
- Largest segment (54 customers) — respond well to flash sales and social-media-driven promotions
- Loyalty/rewards programs to retain them sustainably given spend relative to income

**Cluster 0 — Budget-Conscious (Low Income, Low Spending)**
- Value-oriented messaging: discounts, bundle deals, budget-friendly product lines
- Broad, low-cost campaigns rather than personalized spend

**Cluster 4 — Standard / Average (Moderate Income, Moderate Spending)**
- Second-largest segment (47 customers) — general seasonal campaigns and broad promotions
- Test upsell/cross-sell offers to shift them toward higher-value segments over time

## 🧰 Tools & Libraries
`pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`

## ▶️ How to Run
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
jupyter notebook task2/customer_segmentation.ipynb
```
Then Run All Cells — the dataset downloads automatically at the start of the notebook.

## ✅ Task Checklist
- [x] Exploratory Data Analysis (EDA)
- [x] K-Means clustering applied to segment customers
- [x] PCA and t-SNE used to visualize clusters
- [x] Marketing strategies proposed for each segment
