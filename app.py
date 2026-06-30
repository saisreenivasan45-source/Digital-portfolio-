import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Digital Banking Analytics Dashboard",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Digital Banking Analytics Dashboard")

# Load dataset
df = pd.read_csv("Credit card transactions - India - Simple.csv")

# Convert date
df["Date"] = pd.to_datetime(df["Date"])

# Sidebar
st.sidebar.header("Filters")

city = st.sidebar.multiselect(
    "City",
    sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

card = st.sidebar.multiselect(
    "Card Type",
    df["Card Type"].unique(),
    default=df["Card Type"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered = df[
    (df["City"].isin(city)) &
    (df["Card Type"].isin(card)) &
    (df["Gender"].isin(gender))
]

# KPI
total_transactions = len(filtered)
total_amount = filtered["Amount"].sum()
average_amount = filtered["Amount"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("Transactions", f"{total_transactions:,}")
c2.metric("Total Amount", f"₹{total_amount:,.0f}")
c3.metric("Average Amount", f"₹{average_amount:,.0f}")

st.divider()

# Top Cities
city_df = (
    filtered.groupby("City")["Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    city_df,
    x="City",
    y="Amount",
    color="Amount",
    title="Top 10 Cities by Transaction Amount"
)

st.plotly_chart(fig, use_container_width=True)

# Card Type
fig = px.pie(
    filtered,
    names="Card Type",
    title="Card Type Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# Expense Type
exp = (
    filtered.groupby("Exp Type")["Amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    exp,
    x="Exp Type",
    y="Amount",
    color="Amount",
    title="Expense Category"
)

st.plotly_chart(fig, use_container_width=True)

# Monthly
filtered["Month"] = filtered["Date"].dt.strftime("%b")

month = (
    filtered.groupby("Month")["Amount"]
    .sum()
    .reindex(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    .reset_index()
)

fig = px.line(
    month,
    x="Month",
    y="Amount",
    markers=True,
    title="Monthly Transaction Amount"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Transaction Details")

st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    "transactions.csv",
    "text/csv"
)