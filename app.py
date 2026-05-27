import streamlit as st

st.set_page_config(
    page_title="Equity Market Analytics Dashboard",
    layout="wide"
)

st.title("Equity Market Analytics Dashboard")

st.write(
    """
    This dashboard analyzes historical stock performance using Python,
    financial data, risk metrics and benchmark comparison.
    """
)

ticker = st.text_input("Enter a stock ticker:", "AAPL")

st.write(f"Selected ticker: {ticker}")