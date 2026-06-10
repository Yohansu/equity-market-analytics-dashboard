import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from src.metrics import (
    calculate_daily_return,
    calculate_cumulative_return,
    calculate_total_return,
    calculate_annualized_return,
    calculate_annualized_volatility
)


# ---------------------------------------------------------
# Normal cases
# ---------------------------------------------------------
# These tests check that the formulas work correctly
# when the input data is valid.


def test_calculate_daily_return():
    # Sample prices:
    # 100 -> 110 = 10%
    # 110 -> 121 = 10%
    # 121 -> 108.9 = -10%
    data = pd.DataFrame({
        "Close": [100, 110, 121, 108.9]
    })

    result = calculate_daily_return(data)

    expected_daily_return = pd.Series(
        [0.0, 0.10, 0.10, -0.10],
        name="Daily Return"
    )

    assert_series_equal(
        result["Daily Return"],
        expected_daily_return,
        check_dtype=False,
        check_exact=False,
        rtol=1e-10,
        atol=1e-10
    )


def test_calculate_cumulative_return():
    # Cumulative return compares each price against the first price.
    data = pd.DataFrame({
        "Close": [100, 110, 121, 108.9]
    })

    result = calculate_cumulative_return(data)

    expected_cumulative_return = pd.Series(
        [0.0, 0.10, 0.21, 0.089],
        name="Cumulative Return"
    )

    assert_series_equal(
        result["Cumulative Return"],
        expected_cumulative_return,
        check_dtype=False,
        check_exact=False,
        rtol=1e-10,
        atol=1e-10
    )


def test_calculate_total_return():
    # Total return only compares final price vs initial price.
    data = pd.DataFrame({
        "Close": [100, 110, 121, 108.9]
    })

    result = calculate_total_return(data)

    expected_total_return = 0.089

    assert result == pytest.approx(expected_total_return)


def test_calculate_annualized_return_with_one_trading_year():
    # This test uses 253 closing prices.
    # 253 closing prices = 252 trading periods.
    #
    # Initial price = 100
    # Final price = 110
    # Total return = 10%
    # Since the period is one full trading year, annualized return should be 10%.
    data = pd.DataFrame({
        "Close": [100] * 252 + [110]
    })

    result = calculate_annualized_return(data)

    expected_annualized_return = 0.10

    assert result == pytest.approx(expected_annualized_return)


@pytest.mark.parametrize(
    "trading_periods, initial_price, final_price",
    [
        (21, 100, 105),    # Approximately 1 trading month
        (63, 100, 110),    # Approximately 3 trading months
        (126, 100, 115),   # Approximately 6 trading months
        (252, 100, 120),   # Approximately 1 trading year
        (504, 100, 140),   # Approximately 2 trading years
    ]
)
def test_calculate_annualized_return_for_different_periods(
    trading_periods,
    initial_price,
    final_price
):
    # This creates a price series with:
    # trading_periods + 1 closing prices
    #
    # Example:
    # 63 trading periods require 64 closing prices.
    data = pd.DataFrame({
        "Close": [initial_price] * trading_periods + [final_price]
    })

    result = calculate_annualized_return(data)

    total_return = (final_price / initial_price) - 1

    expected_annualized_return = (
        (1 + total_return) ** (252 / trading_periods)
    ) - 1

    assert result == pytest.approx(expected_annualized_return)

def test_calculate_annualized_volatility():
    data = pd.DataFrame({
        "Close": [100, 110, 121, 108.9]
    })

    result = calculate_annualized_volatility(data)

    daily_return = calculate_daily_return(data)

    total_d_return_std = daily_return["Daily Return"].std()

    expected_annualized_volatility = total_d_return_std * (252 ** 0.5)

    assert result == pytest.approx(expected_annualized_volatility)
# ---------------------------------------------------------
# Edge cases: invalid data
# ---------------------------------------------------------
# These tests check that the functions raise clear errors
# when the input data is invalid.


def test_raises_error_when_dataframe_is_empty():
    data = pd.DataFrame()

    with pytest.raises(ValueError, match="DataFrame is empty"):
        calculate_daily_return(data)


def test_raises_error_when_close_column_is_missing():
    data = pd.DataFrame({
        "Price": [100, 110, 121]
    })

    with pytest.raises(KeyError, match="Close"):
        calculate_daily_return(data)


def test_raises_error_when_close_contains_missing_values():
    data = pd.DataFrame({
        "Close": [100, None, 121]
    })

    with pytest.raises(ValueError, match="Close prices contain missing values"):
        calculate_daily_return(data)


def test_raises_error_when_close_contains_zero():
    data = pd.DataFrame({
        "Close": [100, 0, 121]
    })

    with pytest.raises(ValueError, match="Close prices must be greater than zero"):
        calculate_daily_return(data)


def test_raises_error_when_initial_close_is_zero_for_cumulative_return():
    data = pd.DataFrame({
        "Close": [0, 100, 121]
    })

    with pytest.raises(ValueError, match="Close prices must be greater than zero"):
        calculate_cumulative_return(data)


def test_raises_error_when_initial_close_is_zero_for_total_return():
    data = pd.DataFrame({
        "Close": [0, 100, 121]
    })

    with pytest.raises(ValueError, match="Close prices must be greater than zero"):
        calculate_total_return(data)


def test_raises_error_when_close_contains_negative_values():
    data = pd.DataFrame({
        "Close": [100, -50, 121]
    })

    with pytest.raises(ValueError, match="Close prices must be greater than zero"):
        calculate_daily_return(data)


def test_calculate_annualized_return_raises_error_with_single_price():
    # Annualized return needs at least 2 closing prices.
    # With only 1 closing price, there are 0 trading periods.
    data = pd.DataFrame({
        "Close": [100]
    })

    with pytest.raises(
        ValueError,
        match="At least two closing prices are required to calculate annualized return."
    ):
        calculate_annualized_return(data)


# ---------------------------------------------------------
# Edge cases: valid but special data
# ---------------------------------------------------------
# These are unusual cases, but they should still work.


def test_daily_return_with_single_price():
    data = pd.DataFrame({
        "Close": [100]
    })

    result = calculate_daily_return(data)

    expected_daily_return = pd.Series(
        [0.0],
        name="Daily Return"
    )

    assert_series_equal(
        result["Daily Return"],
        expected_daily_return,
        check_dtype=False
    )


def test_cumulative_return_with_single_price():
    data = pd.DataFrame({
        "Close": [100]
    })

    result = calculate_cumulative_return(data)

    expected_cumulative_return = pd.Series(
        [0.0],
        name="Cumulative Return"
    )

    assert_series_equal(
        result["Cumulative Return"],
        expected_cumulative_return,
        check_dtype=False
    )


def test_total_return_with_single_price():
    data = pd.DataFrame({
        "Close": [100]
    })

    result = calculate_total_return(data)

    assert result == pytest.approx(0.0)


def test_returns_with_constant_prices():
    data = pd.DataFrame({
        "Close": [100, 100, 100, 100]
    })

    daily_result = calculate_daily_return(data)
    cumulative_result = calculate_cumulative_return(data)
    total_result = calculate_total_return(data)

    expected_daily_return = pd.Series(
        [0.0, 0.0, 0.0, 0.0],
        name="Daily Return"
    )

    expected_cumulative_return = pd.Series(
        [0.0, 0.0, 0.0, 0.0],
        name="Cumulative Return"
    )

    assert_series_equal(
        daily_result["Daily Return"],
        expected_daily_return,
        check_dtype=False
    )

    assert_series_equal(
        cumulative_result["Cumulative Return"],
        expected_cumulative_return,
        check_dtype=False
    )

    assert total_result == pytest.approx(0.0)