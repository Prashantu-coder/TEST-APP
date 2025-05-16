import streamlit as st
import pandas as pd
import json
import os

st.title("Nepali Stock Portfolio Calculator with Save/Delete")

# --- Portfolio storage file ---
PORTFOLIO_FILE = "portfolio_data.json"

# Load portfolio from local JSON file if exists
def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return pd.DataFrame(json.load(f))
    else:
        return pd.DataFrame(columns=["Symbol", "Shares", "BuyPrice"])

# Save portfolio to local JSON file
def save_portfolio(df):
    with open(PORTFOLIO_FILE, "w") as f:
        f.write(df.to_json(orient="records"))

# Initialize portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = load_portfolio()

# Display current portfolio with delete option
st.header("Your Portfolio")

if st.session_state.portfolio.empty:
    st.info("Your portfolio is empty. Add stocks below.")
else:
    # Show portfolio with delete buttons per row
    for idx, row in st.session_state.portfolio.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        col1.write(f"**{row['Symbol']}**")
        col2.write(f"Shares: {row['Shares']}")
        col3.write(f"Buy Price: NPR {row['BuyPrice']:.2f}")
        if col4.button("Delete", key=f"del_{idx}"):
            st.session_state.portfolio = st.session_state.portfolio.drop(idx).reset_index(drop=True)
            save_portfolio(st.session_state.portfolio)
            st.experimental_rerun()

# Add new stock form
st.header("Add a Stock to Your Portfolio")

with st.form("add_stock_form"):
    symbol = st.text_input("Symbol (e.g. NABIL)").upper()
    shares = st.number_input("Shares", min_value=1, step=1)
    buy_price = st.number_input("Buy Price (NPR)", min_value=0.01, step=0.01, format="%.2f")
    submitted = st.form_submit_button("Add Stock")
    if submitted:
        if symbol and shares > 0 and buy_price > 0:
            # Check if symbol already in portfolio
            if symbol in st.session_state.portfolio["Symbol"].values:
                st.warning(f"{symbol} already in portfolio. Delete first to re-add.")
            else:
                new_entry = pd.DataFrame([{"Symbol": symbol, "Shares": shares, "BuyPrice": buy_price}])
                st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_entry], ignore_index=True)
                save_portfolio(st.session_state.portfolio)
                st.success(f"Added {symbol} to portfolio!")
                st.experimental_rerun()
        else:
            st.error("Please enter valid values.")

# Upload daily LTP CSV
st.header("Upload Daily LTP CSV (Symbol, LTP)")

ltp_file = st.file_uploader("Upload LTP CSV", type=["csv"])

if ltp_file is not None and not st.session_state.portfolio.empty:
    ltp_df = pd.read_csv(ltp_file)
    # Validate LTP CSV columns
    if not {"Symbol", "LTP"}.issubset(ltp_df.columns):
        st.error("LTP CSV must contain 'Symbol' and 'LTP' columns.")
    else:
        # Merge with portfolio
        merged = pd.merge(st.session_state.portfolio, ltp_df, on="Symbol", how="left")

        # Calculate values
        merged["CurrentValue"] = merged["LTP"] * merged["Shares"]
        merged["Investment"] = merged["BuyPrice"] * merged["Shares"]
        merged["P/L"] = merged["CurrentValue"] - merged["Investment"]
        merged["P/L %"] = (merged["P/L"] / merged["Investment"]) * 100

        st.header("Portfolio Valuation")

        st.dataframe(merged[["Symbol", "Shares", "BuyPrice", "LTP", "CurrentValue", "Investment", "P/L", "P/L %"]])

        total_investment = merged["Investment"].sum()
        total_value = merged["CurrentValue"].sum()
        total_pl = total_value - total_investment
        total_pl_pct = (total_pl / total_investment) * 100 if total_investment > 0 else 0

        st.markdown(f"**Total Investment:** NPR {total_investment:,.2f}")
        st.markdown(f"**Current Portfolio Value:** NPR {total_value:,.2f}")
        st.markdown(f"**Total Profit/Loss:** NPR {total_pl:,.2f} ({total_pl_pct:.2f}%)")

        st.header("Portfolio Distribution by Current Value")
        chart_data = merged.set_index("Symbol")["CurrentValue"]
        st.bar_chart(chart_data)

elif ltp_file is not None and st.session_state.portfolio.empty:
    st.warning("Your portfolio is empty. Please add stocks first.")

else:
    st.info("Upload LTP CSV to see portfolio valuation.")

