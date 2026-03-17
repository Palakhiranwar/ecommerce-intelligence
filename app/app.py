import streamlit as st
import pandas as pd

# PAGE CONFIG
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# CUSTOM CSS 
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# LOAD DATA
df = pd.read_csv("data/cleaned/fact_sales.csv")
rfm = pd.read_csv("data/cleaned/rfm_analysis.csv")

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])


# TITLE
st.markdown("# 🛒 E-Commerce Customer Intelligence Dashboard")
st.markdown("### 📊 Business Overview")


# SIDEBAR FILTERS
st.sidebar.header("🔍 Filters")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

df = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(date_range[0])) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(date_range[1]))
]


# METRICS
total_revenue = df['payment_value'].sum()
total_orders = df['order_id'].nunique()
total_customers = df['customer_unique_id'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"{total_revenue:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("👥 Total Customers", total_customers)

st.markdown("---")


# REVENUE TREND
st.subheader("📈 Monthly Revenue Trend")

df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
revenue_trend = df.groupby('year_month')['payment_value'].sum()

st.line_chart(revenue_trend)

st.markdown("---")

# TOP PRODUCTS
col4, col5 = st.columns(2)

with col4:
    st.subheader("🏆 Top Products")
    top_products = df.groupby('product_id')['payment_value'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_products)

with col5:
    st.subheader("📉 Low Performing Products")
    low_products = df.groupby('product_id')['payment_value'].sum().sort_values().head(10)
    st.bar_chart(low_products)

st.markdown("---")


# CUSTOMER SEGMENTATION
st.subheader("👤 Customer Segmentation")

segment_counts = rfm['segment'].value_counts()
st.bar_chart(segment_counts)

st.markdown("---")

# INSIGHTS 
st.subheader("📌 Key Business Insights")

st.markdown("""
<div style='background-color:#1c1f26; padding:15px; border-radius:10px;'>

- 💰 **Top customers drive majority of revenue**
- 📈 **Revenue shows monthly trends indicating seasonality**
- 🏆 **Few products dominate overall sales**
- 📉 **Many products underperform → optimization opportunity**
- 🎯 **Customer segmentation enables targeted marketing**

</div>
""", unsafe_allow_html=True)


# RECOMMENDATION SYSTEM 

st.markdown("---")
st.subheader("🎯 Product Recommendations")


rfm.columns = rfm.columns.str.lower()
df.columns = df.columns.str.lower()

if 'customer_id' in rfm.columns:
    rfm.rename(columns={'customer_id': 'customer_unique_id'}, inplace=True)


selected_segment = st.selectbox(
    "Select Customer Segment",
    rfm['segment'].unique()
)

#MERGE DATA 
merged = pd.merge(df, rfm, on='customer_unique_id', how='inner')


segment_data = merged[merged['segment'] == selected_segment]

#RECOMMENDATION LOGIC 
if selected_segment == 'VIP':
    recommended = (
        segment_data.groupby('product_id')['payment_value']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index(name='score')
    )

elif selected_segment == 'Regular':
    recommended = (
        segment_data.groupby('product_id')['payment_value']
        .count()
        .sort_values(ascending=False)
        .head(5)
        .reset_index(name='score')
    )

else:
    recommended = (
        segment_data.groupby('product_id')['payment_value']
        .sum()
        .sort_values()
        .head(5)
        .reset_index(name='score')
    )


recommended['product_name'] = "Product " + recommended['product_id'].astype(str).str[:6]


recommended = recommended[['product_name', 'product_id', 'score']]

st.dataframe(recommended)


st.caption("Recommendations are generated based on customer purchase behavior and segment value.")