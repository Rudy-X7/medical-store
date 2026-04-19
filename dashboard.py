import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Load data
df = pd.read_csv("data/processed/cleaned_data.csv")
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month_name()

# -----------------------
# 🎛 FILTERS
# -----------------------
st.sidebar.title("🔎 Advanced Filters")

city = st.sidebar.multiselect(
    "Select City",
    df["city"].unique(),
    default=df["city"].unique()
)

month = st.sidebar.multiselect(
    "Select Month",
    df["month"].unique(),
    default=df["month"].unique()
)

medicine = st.sidebar.multiselect(
    "Select Medicine",
    df["medicine"].unique(),
    default=df["medicine"].unique()
)

# Apply filters
filtered_df = df[
    (df["city"].isin(city)) &
    (df["month"].isin(month)) &
    (df["medicine"].isin(medicine))
]

# -----------------------
# 📊 KPIs
# -----------------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"₹{int(filtered_df['final_amount'].sum()):,}")
col2.metric("🧾 Orders", len(filtered_df))
col3.metric("📈 Avg Order", f"₹{int(filtered_df['final_amount'].mean()):,}")

st.markdown("---")

# -----------------------
# 🏆 TOP MEDICINE (ANSWER YOUR QUESTION)
# -----------------------
st.subheader("🏆 Most Sold Medicine (Filtered)")

top_med = filtered_df.groupby("medicine")["quantity"].sum().sort_values(ascending=False)

st.write("👉 Answer:", top_med.idxmax())

fig1, ax1 = plt.subplots()
top_med.plot(kind="bar", ax=ax1)
st.pyplot(fig1)

# -----------------------
# 📍 BEST MEDICINE PER CITY
# -----------------------
st.subheader("📍 Best Selling Medicine in Each City")

city_med = df.groupby(["city", "medicine"])["quantity"].sum().reset_index()

best_city = city_med.loc[city_med.groupby("city")["quantity"].idxmax()]

st.dataframe(best_city)

# -----------------------
# 🔵 SCATTER PLOT
# -----------------------
st.subheader("🔵 Price vs Quantity (Scatter)")

fig2, ax2 = plt.subplots()
ax2.scatter(filtered_df["price"], filtered_df["quantity"])

ax2.set_xlabel("Price")
ax2.set_ylabel("Quantity Sold")

st.pyplot(fig2)

# -----------------------
# 📈 SALES TREND
# -----------------------
st.subheader("📅 Sales Trend")

sales = filtered_df.groupby("date")["final_amount"].sum()

fig3, ax3 = plt.subplots()
sales.plot(ax=ax3)

st.pyplot(fig3)

st.success("✅ Advanced Dashboard Ready!")
