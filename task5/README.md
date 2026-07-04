# Task 5: Interactive Business Dashboard in Streamlit (Global Superstore)

## 📌 Objective
Develop an interactive dashboard for analyzing sales, profit, and
segment-wise performance across a global retail dataset.

## 📊 Dataset
- **Name:** Global Superstore Dataset
- **Rows:** 51,290 orders, 24 columns
- **Loaded directly from a public URL inside the app** — no manual download needed

Includes order details, customer info, product category/sub-category,
region/market, sales, profit, and shipping cost for a global retailer.

## 🛠️ Approach

### 1. Data Preparation
- Loaded the dataset directly from a public CSV mirror (cached with `@st.cache_data` so it only downloads once per session)
- Parsed `Order Date` into a proper datetime column for time-series charting

### 2. Interactive Filters (Sidebar)
- **Region** — multi-select
- **Category** — multi-select
- **Sub-Category** — multi-select, dynamically scoped to the selected Category(ies)
- A live counter shows how many orders match the current filter selection

### 3. KPI Cards
- 💰 Total Sales
- 📈 Total Profit
- 📦 Total Orders
- 📊 Profit Margin (%)

All KPIs recalculate live as filters change.

### 4. Visualizations
- **Sales & Profit by Category** — grouped bar chart
- **Sales by Region** — bar chart, color-scaled by sales volume
- **Profit by Sub-Category** — horizontal bar chart, color-scaled (red = low/negative profit, green = high profit)
- **Sales & Profit Over Time** — monthly trend line
- **Top 5 Customers by Sales** — combined table + horizontal bar chart
- **Raw data explorer** — expandable table of the currently filtered dataset

## 📈 Results (Full Dataset, No Filters)

| KPI | Value |
|---|---|
| Total Sales | $12,642,502 |
| Total Profit | $1,467,457 |
| Total Orders | 25,035 |
| Profit Margin | 11.6% |

**Top 5 Customers by Sales:**

| Rank | Customer | Sales |
|---|---|---|
| 1 | Tom Ashbrook | $40,488 |
| 2 | Tamara Chand | $37,457 |
| 3 | Greg Tran | $35,551 |
| 4 | Christopher Conant | $35,187 |
| 5 | Sean Miller | $35,171 |

**Key observations:**
- Technology generates the highest sales among the three categories, but Office Supplies achieves the strongest profit-to-sales ratio
- Sales are heavily concentrated in the Central region compared to others
- Tables is the only sub-category showing a **net loss** in profit, standing out clearly in the color-scaled chart — a strong candidate for a pricing or discounting review
- Sales show a clear seasonal spike pattern over time, with year-end peaks

## 💡 Business Value
Rather than a static report, this dashboard lets a business user slice
performance by Region, Category, and Sub-Category interactively — surfacing
insights like the Tables sub-category loss or regional concentration
without needing to write any code or wait on an analyst.

## 🧰 Tools & Libraries
`streamlit`, `pandas`, `plotly`

## ▶️ How to Run
```bash
pip install streamlit pandas plotly
streamlit run task5/superstore_dashboard.py
```
This launches a local server and opens the dashboard automatically at
`http://localhost:8501`. The dataset downloads automatically on first load.

## ✅ Task Checklist
- [x] Cleaned and prepared the dataset
- [x] Built a Streamlit dashboard with filters (Region, Category, Sub-Category)
- [x] Displayed KPIs: Total Sales, Profit, Top 5 Customers by Sales
- [x] Additional visualizations: category/region breakdown, sub-category profitability, sales trend over time
