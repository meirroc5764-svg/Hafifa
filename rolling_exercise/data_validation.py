
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def master_validator(df):
    df = df.dropna(how="all")

    clean_data = check_if_invalid_or_empty_column(df)

    return pd.DataFrame(clean_data)


def check_if_invalid_or_empty_column(df):
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

        clean_data.append(row)

    return clean_data


