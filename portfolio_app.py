import streamlit as st
import pandas as pd

st.title("Nepali Stock Portfolio Calculator")

# Upload LTP file
st.header("1. Upload Daily LTP CSV")
ltp_file = st.file_uploader("Upload LTP CSV (Symbol, LTP)", type=["csv"])

ltp_df = None
if ltp_file:
    ltp_df = pd.read_csv(ltp_file)
    st.write("Uploaded LTP Data:")
    st.dataframe(ltp_df)

# Portfolio input
st.header("2. Enter Your Portfolio")

# Option to upload portfolio CSV or manual input
upload_portfolio = st.checkbox("Upload portfolio CSV instead of manual input?")

if upload_portfolio:
    portfolio_file = st.file_uploader("Upload Portfolio CSV (Symbol, Shares, BuyPrice)", type=["csv"])
    if portfolio_file:
        portfolio_df = pd.read_csv(portfolio_file)
else:
    # Manual input - build a small DataFrame on the fly
    portfolio_data = []
    num_rows = st.number_input("How many different stocks in your portfolio?", min_value=1, max_value=50, value=3)
    for i in range(num_rows):
        col1, col2, col3 = st.columns(3)
        with col1:
            symbol = st.text_input(f"Stock Symbol #{i+1}", key=f"sym{i}").upper()
        with col2:
            shares = st.number_input(f"Shares #{i+1}", min_value=0, step=1, key=f"shares{i}")
        with col3:
            buy_price = st.number_input(f"Buy Price #{i+1}", min_value=0.0, step=0.01, key=f"buy{i}")
        portfolio_data.append({"Symbol": symbol, "Shares": shares, "BuyPrice": buy_price})
    portfolio_df = pd.DataFrame(portfolio_data)

if 'portfolio_df' in locals() and ltp_df is not None:
    # Merge LTP with portfolio on Symbol
    merged = pd.merge(portfolio_df, ltp_df, on='Symbol', how='left')

    # Calculate values
    merged["CurrentValue"] = merged["LTP"] * merged["Shares"]
    merged["Investment"] = merged["BuyPrice"] * merged["Shares"]
    merged["P/L"] = merged["CurrentValue"] - merged["Investment"]
    merged["P/L %"] = (merged["P/L"] / merged["Investment"]) * 100

    st.header("Portfolio Summary")
    st.dataframe(merged)

    total_investment = merged["Investment"].sum()
    total_value = merged["CurrentValue"].sum()
    total_pl = total_value - total_investment
    total_pl_pct = (total_pl / total_investment) * 100 if total_investment > 0 else 0

    st.markdown(f"**Total Investment:** NPR {total_investment:,.2f}")
    st.markdown(f"**Current Portfolio Value:** NPR {total_value:,.2f}")
    st.markdown(f"**Total Profit/Loss:** NPR {total_pl:,.2f} ({total_pl_pct:.2f}%)")

    # Pie chart of portfolio by current value
    st.header("Portfolio Distribution by Current Value")
    chart_data = merged.set_index("Symbol")["CurrentValue"]
    st.bar_chart(chart_data)

else:
    st.info("Please upload both your portfolio and LTP data to see calculations.")
