import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Medical Store Dashboard", layout="wide")

# -------------------------
# 🎨 CUSTOM UI (CSS)
# -------------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141e30, #243b55);
        color: white;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    }

    h1, h2, h3 {
        color: #FFD700;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------
st.title("💊 Medical Store Analytics Dashboard")

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("data/processed/cleaned_data.csv")

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.strftime("%B")

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.markdown("## 🔎 Advanced Filters")

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

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💰 Revenue</h3>
        <h2>₹{total_revenue:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🧾 Orders</h3>
        <h2>{total_orders}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📊 Avg Order</h3>
        <h2>₹{avg_order:,}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# 🏆 MOST SOLD MEDICINE
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

    bar_fig = px.bar(
        top_med.head(5),
        x="medicine",
        y="quantity",
        title="🏆 Top 5 Medicines"
    )

    bar_fig.update_layout(
        title=dict(x=0.5, font=dict(size=22, color="white")),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )

    st.plotly_chart(bar_fig, use_container_width=True)

else:
    st.warning("No data available.")

# -------------------------
# 📍 BEST MEDICINE PER CITY
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
# 🔵 SCATTER PLOT
# -------------------------
st.subheader("🔵 Price vs Quantity (Interactive Scatter)")

scatter_df = filtered_df_medicine.copy()
scatter_df["revenue"] = scatter_df["price"] * scatter_df["quantity"]

if not scatter_df.empty:
    fig = px.scatter(
        scatter_df,
        x="price",
        y="quantity",
        color="city",
        size="revenue",
        hover_data=["medicine"],
        title="🔵 Price vs Quantity Sold",
        opacity=0.7
    )

    fig.update_layout(
        title=dict(
            x=0.5,
            font=dict(size=24, color="white", family="Arial Black")
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(
            title="Price",
            title_font=dict(size=18, color="white"),
            tickfont=dict(size=14, color="white"),
            showgrid=True,
            gridcolor="rgba(255,255,255,0.2)"
        ),
        yaxis=dict(
            title="Quantity",
            title_font=dict(size=18, color="white"),
            tickfont=dict(size=14, color="white"),
            showgrid=True,
            gridcolor="rgba(255,255,255,0.2)"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data for scatter plot.")

# -------------------------
# 📈 SALES OVER TIME
# -------------------------
st.subheader("📈 Sales Over Time")

time_df = (
    filtered_df.groupby("date")["revenue"]
    .sum()
    .reset_index()
)

fig2 = px.line(time_df, x="date", y="revenue")

fig2.update_layout(
    title=dict(
        text="📈 Revenue Over Time",
        x=0.5,
        xanchor='center',
        font=dict(size=26, color="white", family="Arial Black")
    ),
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    xaxis=dict(
        title="Date",
        title_font=dict(size=18, color="white"),
        tickfont=dict(size=14, color="white"),
        showgrid=True,
        gridcolor="rgba(255,255,255,0.2)"
    ),
    yaxis=dict(
        title="Revenue",
        title_font=dict(size=18, color="white"),
        tickfont=dict(size=14, color="white"),
        showgrid=True,
        gridcolor="rgba(255,255,255,0.2)"
    )
)

st.plotly_chart(fig2, use_container_width=True)
