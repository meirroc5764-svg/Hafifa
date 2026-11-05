"""
Data validation module.

Provides functions for validating uploaded air quality data,
checking required columns, converting data types, and removing
rows containing missing or invalid values.
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def master_validator(df):
    """
    Validate and clean the uploaded air quality DataFrame.

    Removes completely empty rows, checks required columns,
    converts date values, and filters invalid records.

    Args:
        df (pd.DataFrame): Raw DataFrame loaded from a CSV file.

    Returns:
        pd.DataFrame: Cleaned DataFrame containing valid records.
                      Returns an empty DataFrame if required columns
                      are missing.
    """
    df = df.dropna(how="all")

    if not check_missing_columns(df):
        return pd.DataFrame()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    ).dt.date

    clean_data = check_if_invalid_or_empty_column(df)

    return pd.DataFrame(clean_data)


def check_if_invalid_or_empty_column(df):
    """
    Remove rows containing missing or invalid values.

    Converts PM2.5, NO2, and CO2 values to numeric types.
    Rows containing missing or non-numeric values are skipped.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Returns:
        list[dict]: Validated records represented as dictionaries.
    """
    numeric_columns = ["PM2.5", "NO2", "CO2"]

    clean_data = []

    for index, row in df.iterrows():

        if row.isna().any():
            logger.warning("Row %s skipped: empty values", index)
            continue

        numeric_values = pd.to_numeric(
            row[numeric_columns],
            errors="coerce"
        )

        if numeric_values.isna().any():
            logger.warning("Row %s skipped: invalid numeric values", index)
            continue

        row_data = row.to_dict()
        row_data.update(numeric_values.to_dict())

        clean_data.append(row_data)

    return clean_data


def check_missing_columns(df):
    """
    Check whether the DataFrame contains all required columns.

    Args:
        df (pd.DataFrame): DataFrame whose columns are checked.

    Returns:
        bool: True if all required columns exist, otherwise False.
    """
    required_columns = ["date", "city", "PM2.5", "NO2", "CO2"]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        logger.error("Missing columns: %s", missing_columns)
        return False

    return True