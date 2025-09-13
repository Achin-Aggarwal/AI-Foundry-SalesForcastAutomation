import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from config import DB_PATH

def get_orders_date_range():
    conn = sqlite3.connect(DB_PATH)
    min_date = conn.execute("SELECT MIN(OrderDate) FROM Orders").fetchone()[0]
    max_date = conn.execute("SELECT MAX(OrderDate) FROM Orders").fetchone()[0]
    conn.close()
    return min_date, max_date

def get_last_month_range():
    _, max_date_str = get_orders_date_range()
    max_date = datetime.fromisoformat(max_date_str)

    first_day_this_month = max_date.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)

    return first_day_last_month.strftime("%Y-%m-%d"), last_day_last_month.strftime("%Y-%m-%d")

def adjust_last_month_sql(sql: str) -> str:
    start_date, end_date = get_last_month_range()
    if "date('now'" in sql or "last month" in sql.lower():
        sql = f"""
        SELECT SUM(UnitPrice * Quantity) AS Sales
        FROM Orders
        JOIN [Order Details] ON Orders.OrderID = [Order Details].OrderID
        WHERE OrderDate >= '{start_date}' AND OrderDate <= '{end_date}';
        """
    return sql.strip()

def execute_sql(sql: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        return {"error": str(e)}
