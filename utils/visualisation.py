import plotly.express as px

def create_visualization(df, chart_type=None):
    if df is None or df.empty:
        return None

    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = df.select_dtypes(exclude="number").columns.tolist()

    if chart_type == "bar" and categorical and numeric:
        return px.bar(df, x=categorical[0], y=numeric[0])
    if chart_type == "line" and categorical and numeric:
        return px.line(df, x=categorical[0], y=numeric[0])
    if chart_type == "scatter" and len(numeric) >= 2:
        return px.scatter(df, x=numeric[0], y=numeric[1])
    return None