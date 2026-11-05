import pandas as pd
import pytest

from data_validation import (
    master_validator,
    check_missing_columns,
    check_if_invalid_or_empty_column
)


def test_valid_data():
    df = pd.DataFrame({
        "date": ["2026-11-05"],
        "city": ["Tel Aviv"],
        "PM2.5": [10],
        "NO2": [20],
        "CO2": [3]
    })

    result = master_validator(df)

    assert len(result) == 1
    assert result.iloc[0]["city"] == "Tel Aviv"


def test_missing_column():
    df = pd.DataFrame({
        "date": ["2026-11-05"],
        "city": ["Tel Aviv"],
        "PM2.5": [10],
        "NO2": [20]
    })

    result = master_validator(df)

    assert result.empty


def test_empty_values_are_removed():
    df = pd.DataFrame({
        "date": ["2026-11-05", "2026-11-06"],
        "city": ["Tel Aviv", "Haifa"],
        "PM2.5": [10, None],
        "NO2": [20, 30],
        "CO2": [3, 4]
    })

    result = master_validator(df)

    assert len(result) == 1
    assert result.iloc[0]["city"] == "Tel Aviv"


def test_invalid_numeric_values_are_removed():
    df = pd.DataFrame({
        "date": ["2026-11-05", "2026-11-06"],
        "city": ["Tel Aviv", "Haifa"],
        "PM2.5": [10, "invalid"],
        "NO2": [20, 30],
        "CO2": [3, 4]
    })

    result = master_validator(df)

    assert len(result) == 1
    assert result.iloc[0]["city"] == "Tel Aviv"


def test_numeric_strings_are_converted():
    df = pd.DataFrame({
        "date": ["2026-11-05"],
        "city": ["Tel Aviv"],
        "PM2.5": ["10"],
        "NO2": ["20"],
        "CO2": ["3"]
    })

    result = master_validator(df)

    assert len(result) == 1
    assert pd.api.types.is_numeric_dtype(result["PM2.5"])


def test_empty_rows_are_removed():
    df = pd.DataFrame({
        "date": [None, "2026-11-05"],
        "city": [None, "Tel Aviv"],
        "PM2.5": [None, 10],
        "NO2": [None, 20],
        "CO2": [None, 3]
    })

    result = master_validator(df)

    assert len(result) == 1
    assert result.iloc[0]["city"] == "Tel Aviv"


def test_check_missing_columns_returns_true():
    df = pd.DataFrame({
        "date": ["2026-11-05"],
        "city": ["Tel Aviv"],
        "PM2.5": [10],
        "NO2": [20],
        "CO2": [3]
    })

    assert check_missing_columns(df) is True


def test_check_if_invalid_or_empty_column():
    df = pd.DataFrame({
        "date": ["2026-11-05"],
        "city": ["Tel Aviv"],
        "PM2.5": [10],
        "NO2": [20],
        "CO2": [3]
    })

    result = check_if_invalid_or_empty_column(df)

    assert len(result) == 1
    assert result[0]["city"] == "Tel Aviv"
