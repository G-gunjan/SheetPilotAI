import pandas as pd


def calculate_dataset_metrics(df):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }


def get_numeric_summary(df):

    numeric_df = df.select_dtypes(
        include="number"
    )

    if numeric_df.empty:
        return None

    return numeric_df.describe()