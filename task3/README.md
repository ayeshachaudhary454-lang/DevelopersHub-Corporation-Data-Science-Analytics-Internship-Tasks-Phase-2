# Task 3: Energy Consumption Time Series Forecasting (Household Power Consumption)

## 📌 Objective
Forecast short-term household energy usage using historical time-based
patterns, comparing ARIMA, Prophet, and XGBoost forecasting models.

## 📊 Dataset
- **Name:** Individual Household Electric Power Consumption Dataset
- **Source:** UCI Machine Learning Repository
- **Rows:** 2,075,259 minute-level measurements from a single household in Sceaux, France, December 2006 - November 2010 (47 months)
- **Loaded directly from a public URL inside the notebook** — no local file needed

| Column | Description |
|---|---|
| Global_active_power | Household global active power (kilowatts) — **forecasting target** |
| Global_reactive_power | Household global reactive power (kilowatts) |
| Voltage | Minute-averaged voltage (volts) |
| Global_intensity | Minute-averaged current intensity (amperes) |
| Sub_metering_1/2/3 | Energy sub-metering for kitchen, laundry room, and water-heater/AC |

## 🛠️ Approach

### 1. Parsing & Cleaning
- Combined Date + Time into a single DateTime index
- Converted string columns to numeric (missing values were marked `?` in the raw file)
- Dropped ~1.25% of rows with missing `Global_active_power` values (consistent with the dataset's documented gaps)

### 2. Resampling
- Resampled from minute-level to **hourly averages** to reduce noise while preserving daily/weekly patterns
- Focused modeling on the **most recent 60 days** (1,440 hours) for faster training while still capturing seasonality

### 3. Feature Engineering
- Engineered time-based features: `hour`, `dayofweek`, `is_weekend`, `day`, `month`
- Used to give XGBoost implicit access to daily/weekly seasonality patterns

### 4. Train/Test Split
- Held out the **last 7 days (168 hours)** as a test set
- Trained on all preceding hourly data

### 5. Model Comparison
Trained and compared three fundamentally different forecasting approaches:
- **XGBoost** — regression over engineered time features
- **ARIMA(2,1,2)** — models the series' own autocorrelation structure
- **Prophet** — purpose-built for time series with daily/weekly/yearly seasonality

## 📈 Results

| Model | MAE | RMSE |
|---|---|---|
| Prophet | 0.5065 | 0.6814 |
| ARIMA | 0.6956 | 0.8566 |
| XGBoost | 0.6358 | 0.8649 |

**Key observations:**
- **Prophet performed best** on both MAE and RMSE, consistent with its purpose-built handling of daily and weekly seasonality — exactly the pattern present in household energy usage
- All three models correctly captured the recurring morning/evening usage peaks and overnight troughs visible in the raw data
- ARIMA required no external features and modeled the series' autocorrelation directly, but showed the highest MAE among the three
- XGBoost, despite having no native time-series structure, performed competitively using only simple engineered time features

## 💡 Business Takeaway
For short-term household energy forecasting with clear daily/weekly cycles,
**Prophet's built-in seasonality decomposition gives it a natural edge**.
XGBoost remains attractive if additional external features (weather,
holidays, appliance schedules) become available, since it can incorporate
them directly as extra columns — something ARIMA and vanilla Prophet
cannot do as easily.

## 🧰 Tools & Libraries
`pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `statsmodels`, `prophet`, `xgboost`

## ▶️ How to Run
```bash
pip install pandas numpy scikit-learn matplotlib seaborn statsmodels prophet xgboost
jupyter notebook task3/energy_forecasting.ipynb
```
Then Run All Cells — the dataset downloads automatically at the start of the notebook.

## ✅ Task Checklist
- [x] Parsed and resampled the time series data
- [x] Engineered time-based features (hour of day, weekday/weekend)
- [x] Compared ARIMA, Prophet, and XGBoost models
- [x] Plotted actual vs. forecasted energy usage
- [x] Evaluated with MAE and RMSE
