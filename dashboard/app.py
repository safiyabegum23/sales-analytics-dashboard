
import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. LOAD DATA
# ==========================================
st.title("📊 Sales Analytics Dashboard")
st.write("Analyze revenue, profit, products, and city performance.")

data_path = Path(__file__).resolve().parent.parent / "data" / "sales.csv"

try:
    df = pd.read_csv(data_path)

    required_columns = [
        "Order_ID", "Product", "City",
        "Quantity", "Price", "Profit"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        st.stop()

    if df.empty:
        st.warning("Your sales CSV file contains no records.")
        st.stop()

    # Convert numeric columns safely
    for col in ["Quantity", "Price", "Profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=required_columns)

    if df.empty:
        st.warning("No valid sales records are available.")
        st.stop()

except FileNotFoundError:
    st.error("Sales data file not found. Check that data/sales.csv exists.")
    st.stop()

except Exception as e:
    st.error(f"Unable to load the sales data: {e}")
    st.stop()

# ==========================================
# 3. CALCULATE REVENUE
# ==========================================
df["Revenue"] = df["Quantity"] * df["Price"]

# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================
st.sidebar.header("🔎 Dashboard Filters")

city_options = ["All"] + sorted(df["City"].astype(str).unique().tolist())
product_options = ["All"] + sorted(df["Product"].astype(str).unique().tolist())

selected_city = st.sidebar.selectbox("Select City", city_options)
selected_product = st.sidebar.selectbox("Select Product", product_options)

filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_product != "All":
    filtered_df = filtered_df[filtered_df["Product"] == selected_product]

st.sidebar.caption(f"Matching orders: {len(filtered_df)}")

# ==========================================
# 5. KEY PERFORMANCE INDICATORS
# ==========================================
st.subheader("Business Performance")

total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
total_quantity = filtered_df["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders if total_orders > 0 else 0
)

profit_margin = (
    total_profit / total_revenue * 100 if total_revenue > 0 else 0
)

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")

col4, col5, col6 = st.columns(3)
col4.metric("Average Order Value", f"₹{average_order_value:,.0f}")
col5.metric("Quantity Sold", f"{total_quantity:,.0f}")
col6.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# ==========================================
# 6. REVENUE ANALYSIS
# ==========================================
st.subheader("📈 Revenue Analysis")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("**Revenue by City**")
    city_revenue = (
        filtered_df.groupby("City")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    if not city_revenue.empty:
        st.bar_chart(city_revenue)
    else:
        st.info("No city revenue data available.")

with chart_col2:
    st.write("**Revenue by Product**")
    product_revenue = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    if not product_revenue.empty:
        st.bar_chart(product_revenue)
    else:
        st.info("No product revenue data available.")

# ==========================================
# 7. PROFIT ANALYSIS
# ==========================================
st.subheader("💰 Profit Analysis")

profit_col1, profit_col2 = st.columns(2)

with profit_col1:
    st.write("**Profit by Product**")
    product_profit = (
        filtered_df.groupby("Product")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )
    if not product_profit.empty:
        st.bar_chart(product_profit)
    else:
        st.info("No product profit data available.")

with profit_col2:
    st.write("**Quantity Sold by Product**")
    product_quantity = (
        filtered_df.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
    )
    if not product_quantity.empty:
        st.bar_chart(product_quantity)
    else:
        st.info("No quantity data available.")


# ==========================================
# 8. TOP-PERFORMING CITY AND PRODUCT
# ==========================================
st.subheader("🏆 Top Performers")

top_col1, top_col2 = st.columns(2)

with top_col1:
    if not filtered_df.empty:
        city_totals = filtered_df.groupby("City")["Revenue"].sum()
        best_city = city_totals.idxmax()
        st.metric("Top City by Revenue", best_city)
        st.caption(f"Revenue: ₹{city_totals.max():,.0f}")
    else:
        st.info("No city results to display.")

with top_col2:
    if not filtered_df.empty:
        product_totals = filtered_df.groupby("Product")["Revenue"].sum()
        best_product = product_totals.idxmax()
        st.metric("Top Product by Revenue", best_product)
        st.caption(f"Revenue: ₹{product_totals.max():,.0f}")
    else:
        st.info("No product results to display.")
        # 9. DOWNLOAD SALES REPORT

st.subheader("📥 Download Sales Report")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
label="⬇️ Download Filtered Sales Report",
data=csv_data,
file_name="sales_report.csv",
mime="text/csv"
)


