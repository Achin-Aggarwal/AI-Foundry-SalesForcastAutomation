import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def forecast_sales(df: pd.DataFrame, periods: int = 6):
    df.columns = [c.lower() for c in df.columns]
    if "orderdate" not in df.columns or "sales" not in df.columns:
        raise ValueError("Forecast SQL must return OrderDate and sales columns.")

    df['orderdate'] = pd.to_datetime(df['orderdate'], errors="coerce")
    df = df.dropna(subset=['orderdate']).set_index('orderdate')
    ts = df.groupby('orderdate')['sales'].sum()
    ts = ts.resample('M').sum().fillna(0)

    model = SARIMAX(ts, order=(1,1,1), seasonal_order=(1,1,1,12))
    model_fit = model.fit(disp=False)
    forecast = model_fit.forecast(steps=periods)
    future_dates = pd.date_range(ts.index[-1] + pd.offsets.MonthBegin(), periods=periods, freq='M')
    forecast = pd.Series(forecast, index=future_dates)

    cutoff = ts.index.max() - pd.DateOffset(years=2)
    history = {str(d.date()): float(v) for d, v in ts.items() if d >= cutoff}
    future = {str(d.date()): float(v) for d, v in forecast.items()}
    return {"history": history, "forecast": future}