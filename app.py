import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from datetime import date


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

# Sidebar
st.sidebar.header("User Inputs")

ticker = st.sidebar.text_input(
    "Enter a stock ticker:",
    "AAPL"
).upper()

start_date = st.sidebar.date_input(
    "Start date",
    date(2020, 1, 1)
)

end_date = st.sidebar.date_input(
    "End date",
    date.today()
)

load_data = st.sidebar.button("Load data")


if load_data:
    if start_date >= end_date:
        st.error("Start date must be earlier than end date.")
    else:
        st.subheader(f"Historical Stock Data: {ticker}")

        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False
        )

        # Some yfinance versions return multi-level columns.
        # This keeps the app compatible with both formats.
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if data.empty:
            st.error("No data found. Please check the ticker symbol or date range.")
        else:
            st.success("Data loaded successfully.")

            st.write("### Data Preview")
            st.dataframe(data.tail())

            st.write("### Adjusted Closing Price")

            fig = px.line(
                data,
                x=data.index,
                y="Close",
                title=f"{ticker} Adjusted Closing Price"
            )

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Enter a ticker, select a date range, and click 'Load data'.")