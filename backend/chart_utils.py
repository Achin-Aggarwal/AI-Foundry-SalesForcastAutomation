import pandas as pd

def prepare_chart_data(df: pd.DataFrame, chart_type: str):
    """
    Convert DataFrame into JSON-ready structure for charting.
    Supports: bar, pie, line
    """
    if df is None or df.empty:
        return {"error": "No data available for chart."}

    if df.shape[1] < 2:
        return {"error": "Need at least two columns for chart."}

    labels = df.iloc[:, 0].astype(str).tolist()
    values = df.iloc[:, 1].tolist()

    if chart_type == "bar":
        return {"type": "bar", "labels": labels, "values": values}

    elif chart_type == "pie":
        return {"type": "pie", "labels": labels, "values": values}

    elif chart_type == "line":
        return {"type": "line", "labels": labels, "values": values}

    else:
        return {"error": f"Unsupported chart type: {chart_type}"}
