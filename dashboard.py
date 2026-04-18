import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("data/processed/cleaned_data.csv")
df["date"] = pd.to_datetime(df["date"])

st.title("💊 Medical Store Analytics Dashboard")

# Sidebar filters
city = st.sidebar.selectbox("Select City", ["All"] + list(df["city"].unique()))
if city != "All":
    df = df[df["city"] == city]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"₹{df['final_amount'].sum():,.0f}")
col2.metric("Transactions", len(df))
col3.metric("Customers", df["customer_id"].nunique())

# Top medicines
st.subheader("Top Medicines")
top_med = df.groupby("medicine")["quantity"].sum().reset_index()
fig1 = px.bar(top_med, x="medicine", y="quantity")
st.plotly_chart(fig1, use_container_width=True)

# Sales trend
st.subheader("Sales Over Time")
trend = df.groupby(df["date"].dt.date)["final_amount"].sum().reset_index()
fig2 = px.line(trend, x="date", y="final_amount")
st.plotly_chart(fig2, use_container_width=True)

# City distribution
st.subheader("City-wise Revenue")
city_df = df.groupby("city")["final_amount"].sum().reset_index()
fig3 = px.pie(city_df, names="city", values="final_amount")
st.plotly_chart(fig3)
