from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def clean_sql(sql: str) -> str:
    if "```" in sql:
        sql = sql.split("```")[1]
        if sql.startswith("sql"):
            sql = sql[3:]
    return sql.strip()

def fix_table_names(sql: str) -> str:
    """
    Fix common table name issues from LLM output.
    """
    replacements = {
        "OrderDetails": "[Order Details]",
        "`OrderDetails`": "[Order Details]",
        "\"OrderDetails\"": "[Order Details]"
    }
    for wrong, correct in replacements.items():
        sql = sql.replace(wrong, correct)
    return sql


def generate_sql_from_question(question: str) -> str:
    prompt = f"""
You are an expert SQL generator and analytics assistant for the Northwind SQLite database.

Tables available:
- Orders(OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry)
- [Order Details](OrderID, ProductID, UnitPrice, Quantity, Discount)
- Customers(CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax)
- Employees(EmployeeID, LastName, FirstName, Title, TitleOfCourtesy, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Extension, Photo, Notes, ReportsTo, PhotoPath)
- Products(ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
- Shippers(ShipperID, CompanyName, Phone)
- Suppliers(SupplierID, CompanyName, ContactName, Address, City, Region, PostalCode, Country, Phone, Fax, HomePage)
- Categories(CategoryID, CategoryName, Description, Picture)
- Regions(RegionID, RegionDescription)
- Territories(TerritoryID, TerritoryDescription, RegionID)
- EmployeeTerritories(EmployeeID, TerritoryID)
- CustomerCustomerDemo(CustomerID, CustomerTypeID)
- CustomerDemographics(CustomerTypeID, CustomerDesc)

Rules:
- If the user asks for a sales forecast (e.g. "forecast sales for next month/quarter/year"), reply with a JSON object containing a "forecast_sql" key. The value should be a SQL query that returns at least two columns: OrderDate (as OrderDate) and aggregated sales (as sales). Optionally, include a third column for a dimension (like Region or Category).
- For all other analytic questions, reply with a JSON object containing "sql" (the SQL query), "chart" (the best chart type: 'bar', 'line', 'pie', or 'table'), and "insights" (a short summary).
- Do not include explanations or any text outside the JSON.
- Always use JOINs when needed.
- If question asks "last month", use `date('now','-1 month')`.
- If the user asks for "top N customers by total orders" or similar, use the Orders table and group by CustomerID. Only join Customers if the user specifically asks for company name or customer details.
- For "top N" queries, use ORDER BY ... DESC LIMIT N.
- For "total orders by company name", join Orders and Customers on CustomerID and group by Customers.CompanyName.
- **For sales by region, always use Orders.ShipRegion, not Customers.Region.**
- **If the user asks for sales in a region (e.g., 'western region'), filter Orders.ShipRegion using LIKE, e.g., WHERE Orders.ShipRegion LIKE 'Western%'.**
- Only join Customers if customer details are needed.

Question: {question}
"""
    response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {"role": "system", "content": "You are an expert SQL assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()