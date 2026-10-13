# src/data_validator.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.

    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    rows_before = len(df)
    df = df.copy()

    # Every required column must exist
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Required column missing: {col}")
            raise ValueError(f"Required column missing: {col}")

    # Numeric columns: drop rows whose non-missing values are not numbers
    for col in numeric_columns:
        if col not in df.columns:
            logger.warning(f"Numeric column not found: {col}")
            continue

        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except (ValueError, TypeError):
                    invalid_rows.append(i)

        if invalid_rows:
            logger.warning(
                f"Removed {len(invalid_rows)} rows with invalid numeric "
                f"values in {col}"
            )
            df = df.drop(index=invalid_rows)

        # Convert the column to a numeric data type
        df[col] = pd.to_numeric(df[col])

    rows_after = len(df)
    logger.debug(
        f"Validation: {rows_before} → {rows_after} rows "
        f"(valid {rows_after}, removed {rows_before - rows_after})"
    )
    return df