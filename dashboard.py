import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# CONFIG
# --------------------------
st.set_page_config(page_title="Medical Store Dashboard", layout="wide")

# --------------------------
# LOAD DATA
# --------------------------
df = pd.read_csv("data/processed/cleaned_data.csv")
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month_name()

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.title("🔍 Advanced Filters")

cities = st.sidebar.multiselect("Select City", df["city"].unique(), default=df["city"].unique())
months = st.sidebar.multiselect("Select Month", df["month"].unique(), default=df["month"].unique())
medicines = st.sidebar.multiselect("Select Medicine", df["medicine"].unique(), default=df["medicine"].unique())

filtered_df = df[
    (df["city"].isin(cities)) &
    (df["month"].isin(months)) &
    (df["medicine"].isin(medicines))
]

# --------------------------
# KPI METRICS
# --------------------------
st.title("💊 Medical Store Analytics Dashboard")

col1, col2, col3 = st.columns(3)

revenue = int((filtered_df["price"] * filtered_df["quantity"]).sum())
orders = filtered_df.shape[0]
avg_order = int(revenue / orders) if orders else 0

col1.metric("💰 Revenue", f"₹{revenue:,}")
col2.metric("📦 Orders", orders)
col3.metric("📊 Avg Order", f"₹{avg_order:,}")

# --------------------------
# MOST SOLD MEDICINE (FILTERED)
# --------------------------
st.subheader("🏆 Most Sold Medicine (Filtered)")

top_med = (
    filtered_df.groupby("medicine")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

if not top_med.empty:
    st.success(f"👉 {top_med.index[0]}")
else:
    st.warning("No data available")

# --------------------------
# SALES OVER TIME
# --------------------------
st.subheader("📈 Sales Over Time")

time_df = filtered_df.groupby("date").apply(
    lambda x: (x["price"] * x["quantity"]).sum()
).reset_index(name="revenue")

fig = px.line(time_df, x="date", y="revenue")

fig.update_layout(
    title=dict(
        text="📈 Revenue Over Time",
        x=0.5,
        xanchor='center',
        font=dict(size=26, color="white")
    ),
    plot_bgcolor="#1e1e2f",
    paper_bgcolor="#1e1e2f",
    font=dict(color="white"),
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------
# BEST MEDICINE PER CITY
# --------------------------
st.subheader("📍 Best Selling Medicine in Each City")

city_med = (
    filtered_df.groupby(["city", "medicine"])["quantity"]
    .sum()
    .reset_index()
)

best_city = city_med.loc[city_med.groupby("city")["quantity"].idxmax()]

st.dataframe(best_city)

# --------------------------
# SCATTER PLOT (IMPROVED)
# --------------------------
st.subheader("🔵 Price vs Quantity (Interactive Scatter)")

scatter_df = filtered_df.copy()

fig2 = px.scatter(
    scatter_df,
    x="price",
    y="quantity",
    color="city",
    size="quantity",
    hover_data=["medicine"],
    opacity=0.7
)

fig2.update_layout(
    plot_bgcolor="#1e1e2f",
    paper_bgcolor="#1e1e2f",
    font=dict(color="white"),
)

st.plotly_chart(fig2, use_container_width=True)
