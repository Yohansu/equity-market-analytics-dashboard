import streamlit as st
import plotly.express as px
from datetime import date

from src.data_loader import download_stock_data
from src.metrics import calculate_daily_return


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

        data = download_stock_data(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date
        )

        if data.empty:
            st.error("No data found. Please check the ticker symbol or date range.")

        else:
            data = calculate_daily_return(data)

            st.success("Data loaded successfully.")

            # Key metrics
            latest_close = data["Close"].iloc[-1]
            latest_daily_return = data["Daily Return"].iloc[-1]

            col1, col2 = st.columns(2)

            col1.metric(
                label="Latest Close Price",
                value=f"${latest_close:,.2f}"
            )

            col2.metric(
                label="Latest Daily Return",
                value=f"{latest_daily_return:.2%}"
            )

            st.write("### Data Preview")
            st.dataframe(data.tail())

            st.write("### Adjusted Closing Price")

            price_fig = px.line(
                data,
                x=data.index,
                y="Close",
                title=f"{ticker} Adjusted Closing Price"
            )

            price_fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price",
                height=500
            )

            st.plotly_chart(price_fig, use_container_width=True)

            st.write("### Daily Returns")

            returns_fig = px.line(
                data,
                x=data.index,
                y="Daily Return",
                title=f"{ticker} Daily Returns"
            )

            returns_fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Daily Return",
                yaxis_tickformat=".2%",
                height=500
            )

            st.plotly_chart(returns_fig, use_container_width=True)

else:
    st.info("Enter a ticker, select a date range, and click 'Load data'.")