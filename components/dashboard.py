# import streamlit as st


# def render_metrics(df):

#     rows = len(df)

#     columns = len(df.columns)

#     missing = int(
#         df.isnull().sum().sum()
#     )

#     duplicates = int(
#         df.duplicated().sum()
#     )

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric(
#         "Rows",
#         f"{rows:,}"
#     )

#     col2.metric(
#         "Columns",
#         columns
#     )

#     col3.metric(
#         "Missing Values",
#         f"{missing:,}"
#     )

#     col4.metric(
#         "Duplicates",
#         f"{duplicates:,}"
#     )



import streamlit as st

def render_metrics(df):
    rows = len(df)
    columns = len(df.columns)
    missing = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{rows:,}")
    col2.metric("Columns", columns)
    col3.metric("Missing Values", f"{missing:,}")
    col4.metric("Duplicates", f"{duplicates:,}")