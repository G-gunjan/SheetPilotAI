# import pandas as pd


# def load_dataframe(uploaded_file):

#     if uploaded_file is None:
#         return None

#     file_name = uploaded_file.name.lower()

#     if file_name.endswith(".csv"):
#         return pd.read_csv(uploaded_file)

#     elif file_name.endswith(".xlsx"):
#         return pd.read_excel(uploaded_file)

#     else:
#         raise ValueError(
#             "Only CSV and Excel files are supported."
#         )


# def get_dataframe_profile(df):

#     profile = {
#         "rows": len(df),
#         "columns": len(df.columns),
#         "missing_values": int(df.isnull().sum().sum()),
#         "duplicate_rows": int(df.duplicated().sum()),
#         "numeric_columns": len(
#             df.select_dtypes(include="number").columns
#         )
#     }

#     return profile



import pandas as pd

def load_dataframe(uploaded_file):
    if uploaded_file is None:
        return None
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Only CSV and Excel files are supported.")