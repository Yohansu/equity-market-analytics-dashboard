# Equity Market Analytics Dashboard

## Project Overview

Equity Market Analytics Dashboard is an interactive financial dashboard built with Python and Streamlit. The project is designed to analyze historical stock market performance using financial data, return metrics, risk indicators, and benchmark comparison.

The main goal of this project is to transform raw stock price data into clear and interactive visual insights that can support financial analysis and portfolio-building practice.

This project is intended for educational and analytical purposes. It does not provide investment recommendations or financial advice.

---

## Problem Statement

Stock market data is widely available online, but raw price data by itself is not enough to understand the behavior of a stock. To perform a meaningful analysis, users need to calculate returns, volatility, drawdowns, and compare performance against a market benchmark.

Many professional financial platforms are expensive or designed for institutional users. This creates a barrier for students, early-career analysts, and people interested in financial data analysis.

This dashboard addresses that problem by providing a simple and interactive tool to analyze historical equity performance using Python.

---

## Project Objective

The objective of this project is to develop an interactive dashboard that allows users to analyze historical stock performance through financial metrics and visualizations.

The tool is designed to help users:

- Load historical stock market data
- Visualize price behavior over time
- Analyze stock returns
- Measure risk through volatility and drawdown
- Compare individual stocks against a benchmark
- Communicate financial insights through interactive charts

---

## Current Features

The current version includes:
 
- Basic Streamlit dashboard layout
- User input for stock ticker selection
- Historical stock price download using `yfinance`
- Adjusted closing price visualization
- Daily return calculation
- Cumulative return calculation
- Total return calculation
- Data validation for invalid closing prices
- Unit tests for financial metrics using `pytest`
- Annualized return
- Trading periods
---

## Planned Features

Future versions of the dashboard will include:

- Annualized volatility
- Maximum drawdown
- Benchmark comparison against SPY or other market ETFs
- Multiple ticker comparison
- Summary tables with key financial metrics
- Moving averages
- Export processed data to CSV
- Interactive visualizations using Plotly

---

## Technologies Used

This project uses the following technologies:

- Python
- Streamlit
- pandas
- NumPy
- yfinance
- Plotly
- pytest
- Git
- GitHub

---

## Project Structure

```text
equity-market-analytics-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── metrics.py
│
├── tests/
│   ├── __init__.py
│   └── test_metrics.py
│   └── test_cumulative_return.py
│   └── test_daily_return.py    
│
└── scripts/
    ├── __init__.py
    ├── check_daily_return_real_data.py
    └── check_cumulative_return_real_data.py

```

As the project grows, the structure may be expanded to include additional folders such as:

```text
equity-market-analytics-dashboard/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── src/
│   ├── data_loader.py
│   ├── metrics.py
│   └── plots.py
│
├── data/
│   ├── raw/
│   └── processed/
│
└── notebooks/
    └── exploratory_analysis.ipynb
```

---

## Installation

To run this project locally, first clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/equity-market-analytics-dashboard.git
```

Navigate into the project folder:

```bash
cd equity-market-analytics-dashboard
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Tests

This project includes unit tests for the financial metrics.

To run the tests, use:

```bash
python -m pytest tests/test_metrics.py -v
```
---

## How to Run the App

Run the Streamlit app with:

```bash
streamlit run app.py
```

If the previous command does not work, use:

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

---

## Example Use Case

A user can enter a stock ticker such as:

```text
AAPL
MSFT
NVDA
TSLA
SPY
```

The dashboard will be developed to display historical price data, return metrics, risk indicators, and benchmark comparison.

---

## Financial Disclaimer

This project is for educational and analytical purposes only. It does not provide investment advice, trading signals, or recommendations to buy or sell financial assets.

---

## Author

Developed by Yohansu Nishikawa.