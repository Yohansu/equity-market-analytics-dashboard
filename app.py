import streamlit as st
import plotly.express as px
from datetime import date

from src.data_loader import download_stock_data
from src.metrics import (
    calculate_daily_return,
    calculate_cumulative_return,
    calculate_total_return,
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_maximum_drawdown
)


st.set_page_config(
    page_title="Equity Market Analytics Dashboard",
    layout="wide"
)


st.markdown(
    """
    <style>
    .short-period-metric-card {
        background-color: rgba(255, 193, 7, 0.18);
        border: 1px solid rgba(255, 193, 7, 0.45);
        border-left: 0.35rem solid rgba(255, 193, 7, 0.85);
        border-radius: 0.5rem;
        padding: 1rem;
        min-height: 7rem;
    }

    .short-period-metric-label {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .short-period-metric-value {
        font-size: 2.25rem;
        line-height: 1.1;
        font-weight: 400;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def display_short_period_metric(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="short-period-metric-card">
            <div class="short-period-metric-label">{label}</div>
            <div class="short-period-metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
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
            try:
                # Calculate metrics
                data = calculate_daily_return(data)
                data = calculate_cumulative_return(data)

                total_return = calculate_total_return(data)
                maximum_drawdown = calculate_maximum_drawdown(data)

                # Annualized return is a scalar value.
                # It requires at least 2 closing prices.
                try:
                    annualized_return = calculate_annualized_return(data)
                except ValueError as error:
                    annualized_return = None
                    st.warning(str(error))

                # Annualized volatility is a scalar value.
                # It measures the annualized dispersion of daily returns.
                try:
                    annualized_volatility = calculate_annualized_volatility(data)
                except ValueError as error:
                    annualized_volatility = None
                    st.warning(str(error))

                st.success("Data loaded successfully.")

                # Trading periods
                number_of_trading_periods = len(data) - 1
                short_period_warning = 0 < number_of_trading_periods < 63

                if short_period_warning:
                    st.warning(
                        "The selected period contains fewer than 63 trading periods. "
                        "Annualized return and annualized volatility may be highly "
                        "sensitive to short-term price movements."
                    )

                # Latest values
                latest_close = data["Close"].iloc[-1]
                latest_daily_return = data["Daily Return"].iloc[-1]

                annualized_return_value = (
                    "N/A"
                    if annualized_return is None
                    else f"{annualized_return:.2%}"
                )

                annualized_volatility_value = (
                    "N/A"
                    if annualized_volatility is None
                    else f"{annualized_volatility:.2%}"
                )

                # Metric cards
                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    label="Latest Close Price",
                    value=f"${latest_close:,.2f}"
                )

                col2.metric(
                    label="Latest Daily Return",
                    value=f"{latest_daily_return:.2%}"
                )

                col3.metric(
                    label="Total Return",
                    value=f"{total_return:.2%}"
                )

                col4.metric(
                    label="Trading Periods",
                    value=f"{number_of_trading_periods}"
                )

                col5, col6, col7 = st.columns(3)

                with col5:
                    if short_period_warning:
                        display_short_period_metric(
                            label="Annualized Return",
                            value=annualized_return_value
                        )
                    else:
                        st.metric(
                            label="Annualized Return",
                            value=annualized_return_value
                        )

                with col6:
                    if short_period_warning:
                        display_short_period_metric(
                            label="Annualized Volatility",
                            value=annualized_volatility_value
                        )
                    else:
                        st.metric(
                            label="Annualized Volatility",
                            value=annualized_volatility_value
                        )

                col7.metric(
                    label="Maximum Drawdown",
                    value=f"{maximum_drawdown:.2%}"
                )

                st.caption(
                    "Annualized Return converts the selected period's total return "
                    "into a yearly equivalent using 252 trading periods per year. "
                    "Annualized Volatility converts the standard deviation of daily "
                    "returns into a yearly risk estimate using sqrt(252). "
                    "Maximum Drawdown measures the worst percentage decline from a "
                    "previous peak during the selected period."
                )

                # Data preview
                st.write("### Data Preview")
                st.dataframe(data.tail())

                # Price chart
                st.write("### Adjusted Closing Prices")

                price_fig = px.line(
                    data,
                    x=data.index,
                    y="Close",
                    title=f"{ticker} Adjusted Closing Prices"
                )

                price_fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Price",
                    height=500
                )

                st.plotly_chart(price_fig, use_container_width=True)

                # Daily returns chart
                st.write("### Daily Returns")

                daily_return_fig = px.line(
                    data,
                    x=data.index,
                    y="Daily Return",
                    title=f"{ticker} Daily Returns"
                )

                daily_return_fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Daily Return",
                    yaxis_tickformat=".2%",
                    height=500
                )

                st.plotly_chart(daily_return_fig, use_container_width=True)

                # Cumulative return chart
                st.write("### Cumulative Return")

                cumulative_return_fig = px.line(
                    data,
                    x=data.index,
                    y="Cumulative Return",
                    title=f"{ticker} Cumulative Return"
                )

                cumulative_return_fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Cumulative Return",
                    yaxis_tickformat=".2%",
                    height=500
                )

                st.plotly_chart(cumulative_return_fig, use_container_width=True)

            except (ValueError, KeyError) as error:
                st.error(f"Unable to calculate metrics: {error}")

else:
    st.info("Enter a ticker, select a date range, and click 'Load data'.")