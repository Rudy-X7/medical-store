import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Medical Dashboard", layout="wide")

df = pd.read_csv("data/processed/cleaned_data.csv")
df["date"] = pd.to_datetime(df["date"])

st.title("💊 Medical Store Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"₹{df['final_amount'].sum():,.0f}")
col2.metric("Transactions", len(df))

fig = px.line(
    df.groupby(df["date"].dt.date)["final_amount"].sum().reset_index(),
    x="date",
    y="final_amount"
)

st.plotly_chart(fig)

st.dataframe(df.head())
