"""
Global Superstore — Interactive Business Dashboard
Task 5: Interactive Business Dashboard in Streamlit

Run with: streamlit run superstore_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------------------------------
# Data loading (cached so it only downloads once per session)
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    url = ('https://raw.githubusercontent.com/anurag3290/'
           'Retail-Giant-Sales-Forecasting-Time-Series-Modelling/'
           'master/Global%20Superstore.csv')
    df = pd.read_csv(url, encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    if df['Order Date'].isnull().mean() > 0.5:
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    return df

df = load_data()

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
st.sidebar.header("🔍 Filters")

regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

categories = sorted(df['Category'].unique())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

subcat_options = sorted(df[df['Category'].isin(selected_categories)]['Sub-Category'].unique())
selected_subcats = st.sidebar.multiselect("Sub-Category", subcat_options, default=subcat_options)

filtered_df = df[
    df['Region'].isin(selected_regions) &
    df['Category'].isin(selected_categories) &
    df['Sub-Category'].isin(selected_subcats)
]

st.sidebar.markdown(f"**{len(filtered_df):,}** orders match your filters")

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.title("📊 Global Superstore — Business Dashboard")
st.markdown("Interactive analysis of sales, profit, and segment-wise performance.")

# ----------------------------------------------------------------------------
# KPI row
# ----------------------------------------------------------------------------
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📦 Total Orders", f"{total_orders:,}")
col4.metric("📊 Profit Margin", f"{profit_margin:.1f}%")

st.markdown("---")

# ----------------------------------------------------------------------------
# Charts row 1: Sales & Profit by Category / Region
# ----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    cat_summary = filtered_df.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
    fig = px.bar(cat_summary, x='Category', y=['Sales', 'Profit'], barmode='group',
                 title='Sales & Profit by Category', color_discrete_sequence=['#4C72B0', '#55A868'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    region_summary = filtered_df.groupby('Region')[['Sales']].sum().reset_index().sort_values('Sales', ascending=False)
    fig = px.bar(region_summary, x='Region', y='Sales', title='Sales by Region',
                 color='Sales', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# Charts row 2: Sub-Category profitability & Sales trend over time
# ----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    subcat_summary = filtered_df.groupby('Sub-Category')[['Profit']].sum().reset_index().sort_values('Profit')
    fig = px.bar(subcat_summary, x='Profit', y='Sub-Category', orientation='h',
                 title='Profit by Sub-Category',
                 color='Profit', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    if filtered_df['Order Date'].notnull().any():
        monthly = filtered_df.dropna(subset=['Order Date']).set_index('Order Date').resample('ME')[['Sales', 'Profit']].sum().reset_index()
        fig = px.line(monthly, x='Order Date', y=['Sales', 'Profit'], title='Sales & Profit Over Time')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Order Date not available for trend chart.")

# ----------------------------------------------------------------------------
# Top 5 Customers by Sales
# ----------------------------------------------------------------------------
st.markdown("---")
st.subheader("🏆 Top 5 Customers by Sales")

top_customers = (filtered_df.groupby('Customer Name')['Sales']
                  .sum()
                  .sort_values(ascending=False)
                  .head(5)
                  .reset_index())

col1, col2 = st.columns([1, 2])
with col1:
    st.dataframe(top_customers.style.format({'Sales': '${:,.0f}'}), use_container_width=True)
with col2:
    fig = px.bar(top_customers, x='Sales', y='Customer Name', orientation='h',
                 title='Top 5 Customers by Sales', color='Sales', color_continuous_scale='Purples')
    fig.update_yaxes(categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# Raw data explorer
# ----------------------------------------------------------------------------
st.markdown("---")
with st.expander("🔎 View Filtered Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)

st.caption("Data source: Global Superstore Dataset")