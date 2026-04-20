import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Medical Store Dashboard", layout="wide")

st.title("💊 Medical Store Analytics Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("data/processed/cleaned_data.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.strftime("%B")

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("🔎 Advanced Filters")

selected_city = st.sidebar.multiselect(
    "Select City",
    options=df["city"].unique(),
    default=df["city"].unique()
)

selected_month = st.sidebar.multiselect(
    "Select Month",
    options=df["month"].unique(),
    default=df["month"].unique()
)

selected_medicine = st.sidebar.multiselect(
    "Select Medicine",
    options=df["medicine"].unique(),
    default=[]
)

# -------------------------
# APPLY FILTERS
# -------------------------
filtered_df = df.copy()

if selected_city:
    filtered_df = filtered_df[filtered_df["city"].isin(selected_city)]

if selected_month:
    filtered_df = filtered_df[filtered_df["month"].isin(selected_month)]

# Apply medicine filter ONLY for charts where needed
filtered_df_medicine = filtered_df.copy()
if selected_medicine:
    filtered_df_medicine = filtered_df_medicine[
        filtered_df_medicine["medicine"].isin(selected_medicine)
    ]

# -------------------------
# KPI METRICS
# -------------------------
filtered_df["revenue"] = filtered_df["price"] * filtered_df["quantity"]

total_revenue = int(filtered_df["revenue"].sum())
total_orders = filtered_df.shape[0]
avg_order = int(total_revenue / total_orders) if total_orders > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"₹{total_revenue:,}")
col2.metric("🧾 Orders", total_orders)
col3.metric("📊 Avg Order", f"₹{avg_order:,}")

st.markdown("---")

# -------------------------
# ✅ FIXED: MOST SOLD MEDICINE (NO MEDICINE FILTER)
# -------------------------
st.subheader("🏆 Most Sold Medicine (Based on Filters)")

top_med = (
    filtered_df.groupby("medicine")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

if not top_med.empty:
    st.write(f"👉 Answer: **{top_med.iloc[0]['medicine']}**")
    st.bar_chart(top_med.set_index("medicine").head(5))
else:
    st.warning("No data available for selected filters.")

# -------------------------
# BEST SELLING MEDICINE PER CITY
# -------------------------
st.subheader("📍 Best Selling Medicine in Each City")

city_best = (
    filtered_df.groupby(["city", "medicine"])["quantity"]
    .sum()
    .reset_index()
)

idx = city_best.groupby("city")["quantity"].idxmax()
best_per_city = city_best.loc[idx]

st.dataframe(best_per_city)

# -------------------------
# ✅ IMPROVED SCATTER PLOT
# -------------------------
st.subheader("🔵 Price vs Quantity (Interactive Scatter)")

scatter_df = filtered_df_medicine.copy()
scatter_df["revenue"] = scatter_df["price"] * scatter_df["quantity"]

if not scatter_df.empty:
    fig = px.scatter(
        scatter_df,
        x="price",
        y="quantity",
        color="city",             # 🎨 color by city
        size="revenue",           # 🔵 size by revenue
        hover_data=["medicine"],  # 🧠 hover info
        title="Price vs Quantity Sold",
        trendline="ols"           # 🔥 regression line
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data for scatter plot.")

# -------------------------
# OPTIONAL: SALES OVER TIME (BONUS 🔥)
# -------------------------
st.subheader("📈 Sales Over Time")

time_df = (
    filtered_df.groupby("date")["revenue"]
    .sum()
    .reset_index()
)

fig2 = px.line(time_df, x="date", y="revenue", title="Revenue Over Time")
st.plotly_chart(fig2, use_container_width=True)
