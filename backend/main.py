from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import execute_sql, adjust_last_month_sql
from llm import generate_sql_from_question, clean_sql, fix_table_names
from chart_utils import prepare_chart_data
from forecast_utils import forecast_sales
import json
import re
import pandas as pd


app = FastAPI(title="SQL Query API", version="1.2")

# 🚀 Allow all origins during dev (safer)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Allow all for now, can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    chart_type: str | None = None   # "bar", "pie", "line" or None

def extract_json_from_llm_output(text: str) -> str:
    """
    Extracts the first JSON object from a string, even if wrapped in code blocks or has extra text.
    Removes all code block markers and trims whitespace.
    """
    text = text.strip()
    
    # Remove code block markers more thoroughly
    # Handle ```json\n{...}\n``` format
    if text.startswith("```"):
        # Find the first { after ```
        start_idx = text.find("{")
        # Find the last } before ```
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            text = text[start_idx:end_idx + 1]
    
    # Additional cleanup for any remaining backticks
    text = text.replace("```", "").strip()
    
    # Extract JSON object using regex (handles newlines and whitespace)
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)
    return text


def extract_forecast_period(question: str) -> int:
    """
    Extracts the forecast period (in months) from the user's question.
    Supports 'next X months', 'next X years', or defaults to 3 months.
    """
    import re
    question = question.lower()
    match = re.search(r'next\s+(\d+)\s+month', question)
    if match:
        return int(match.group(1))
    match = re.search(r'next\s+(\d+)\s+year', question)
    if match:
        return int(match.group(1)) * 12
    return 3

@app.get("/")
def root():
    return {"message": "Welcome to the SQL Query API. Use /ask endpoint."}

@app.post("/ask")
def ask_question(req: QuestionRequest):
    sql = generate_sql_from_question(req.question)

    # --- Clean LLM output for JSON ---
    json_str = extract_json_from_llm_output(sql)

    cleaned_sql = None
    chart_type = req.chart_type
    insights = ""
    
    try:
        parsed = json.loads(json_str)
        # If forecast_sql, run forecasting logic
        if "forecast_sql" in parsed:
            import sqlite3
            from config import DB_PATH
            
            forecast_sql = parsed["forecast_sql"]
            # Fix the forecast SQL - it needs to JOIN with Order Details table for proper sales calculation
            forecast_sql = """
            SELECT 
                OrderDate,
                SUM(od.Quantity * od.UnitPrice * (1 - od.Discount)) AS sales
            FROM Orders o
            JOIN [Order Details] od ON o.OrderID = od.OrderID
            GROUP BY OrderDate
            ORDER BY OrderDate
            """
            
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query(forecast_sql, conn)
            conn.close()
            periods = extract_forecast_period(req.question)
            forecast_result = forecast_sales(df, periods=periods)
            # forecast_result = forecast_sales(df, periods=3)  # 3 months as requested
            return {
                "question": req.question,
                "forecast": forecast_result,
                "llm_response": "Forecast generated for next 3 months",
                "forecast_sql": forecast_sql
            }
        # Otherwise, normal SQL
        cleaned_sql = parsed.get("sql")
        chart_type = parsed.get("chart", req.chart_type)
        insights = parsed.get("insights", "")
    except json.JSONDecodeError as e:
        # JSON parsing failed, treat as raw SQL
        print(f"JSON parse error: {e}")
        print(f"Attempted to parse: {json_str}")
        
        if json_str.strip().startswith("{") and json_str.strip().endswith("}"):
            # Looks like JSON but failed to parse, return error with details
            return {
                "error": f"Failed to parse LLM output as JSON: {str(e)}", 
                "llm_response": sql,
                "extracted_json": json_str
            }
        cleaned_sql = clean_sql(sql)
        chart_type = req.chart_type
        insights = ""
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "llm_response": sql}

    # Handle regular SQL queries
    if cleaned_sql:
        fixed_sql = fix_table_names(cleaned_sql)
        adjusted_sql = adjust_last_month_sql(fixed_sql)

        df = execute_sql(adjusted_sql)
        response = {
            "question": req.question,
            "generated_sql": sql,
            "cleaned_sql": cleaned_sql,
            "adjusted_sql": adjusted_sql,
            "result": df if isinstance(df, dict) else df.to_dict(orient="records"),
            "insights": insights
        }
        if chart_type and not isinstance(df, dict):
            response["chart"] = prepare_chart_data(df, chart_type)
        return response
    
    return {"error": "No SQL query could be extracted or generated"}