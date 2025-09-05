'''
import pandas as pd
import pyodbc
import xlsxwriter # For more advanced Excel writing including charts

# --- 1. Connect to the SQL Server Database ---
# Update 'YOUR_SERVER_NAME'
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=BALJEET_SINGH\SQLEXPRESS;'
    r'DATABASE=ECommerceDB;'
    r'Trusted_Connection=yes;' # Uses Windows authentication
)

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connection to SQL Server successful!")
except Exception as e:
    print(f"❌ Error connecting to SQL Server: {e}")
    exit()

# --- 2. Extract Comprehensive Data ---
# We need more data for sales trends, so we'll get all necessary details.
sql_query = """
SELECT
    o.OrderID,
    o.OrderDate,
    c.CustomerID,
    c.FirstName,
    c.LastName,
    c.City,
    p.ProductID,
    p.ProductName,
    cat.CategoryName,
    od.Quantity,
    od.Subtotal
FROM OrderDetails od
JOIN Orders o ON od.OrderID = o.OrderID
JOIN Products p ON od.ProductID = p.ProductID
JOIN Categories cat ON p.CategoryID = cat.CategoryID
JOIN Customers c ON o.CustomerID = c.CustomerID;
"""

df_raw_sales = pd.read_sql_query(sql_query, conn)
conn.close()
print("✅ Raw sales data extracted from SQL Server.")

# Convert OrderDate to datetime objects for time-series analysis
df_raw_sales['OrderDate'] = pd.to_datetime(df_raw_sales['OrderDate'])


# --- 3. Perform Multiple Analyses ---

# A. Sales by Category
sales_by_category = df_raw_sales.groupby('CategoryName')['Subtotal'].sum().reset_index()
sales_by_category = sales_by_category.sort_values(by='Subtotal', ascending=False)
print("\n--- Sales by Category ---")
print(sales_by_category)

# B. Top 5 Products by Sales
sales_by_product = df_raw_sales.groupby('ProductName')['Subtotal'].sum().reset_index()
top_products = sales_by_product.sort_values(by='Subtotal', ascending=False).head(5)
print("\n--- Top 5 Products by Sales ---")
print(top_products)

# C. Monthly Sales Trend
df_raw_sales['OrderMonth'] = df_raw_sales['OrderDate'].dt.to_period('M')
monthly_sales_trend = df_raw_sales.groupby('OrderMonth')['Subtotal'].sum().reset_index()
# Convert Period to string for better Excel compatibility and sort
monthly_sales_trend['OrderMonth'] = monthly_sales_trend['OrderMonth'].astype(str)
monthly_sales_trend = monthly_sales_trend.sort_values(by='OrderMonth')
print("\n--- Monthly Sales Trend ---")
print(monthly_sales_trend)


# --- 4. Generate Excel Report with Charts ---
output_excel_file = 'e_commerce_dashboard_report.xlsx'
writer = pd.ExcelWriter(output_excel_file, engine='xlsxwriter')

# Write raw data to a sheet
df_raw_sales.to_excel(writer, sheet_name='Raw Sales Data', index=False)

# Write analysis results to separate sheets
sales_by_category.to_excel(writer, sheet_name='Sales by Category', index=False)
top_products.to_excel(writer, sheet_name='Top Products', index=False)
monthly_sales_trend.to_excel(writer, sheet_name='Monthly Sales Trend', index=False)


# Get the xlsxwriter workbook and worksheet objects
workbook = writer.book

# --- Add Charts to Excel ---

# Chart 1: Sales by Category (Bar Chart)
worksheet_cat = writer.sheets['Sales by Category']
chart_cat = workbook.add_chart({'type': 'column'})
chart_cat.add_series({
    'name':       ['Sales by Category', 0, 1], # Sheet name, row, col for header
    'categories': ['Sales by Category', 1, 0, len(sales_by_category), 0], # Sheet, start_row, start_col, end_row, end_col
    'values':     ['Sales by Category', 1, 1, len(sales_by_category), 1],
    'data_labels': {'value': True},
})
chart_cat.set_title({'name': 'Sales by Category'})
chart_cat.set_x_axis({'name': 'Category'})
chart_cat.set_y_axis({'name': 'Total Sales'})
worksheet_cat.insert_chart('D2', chart_cat) # Insert chart at cell D2

# Chart 2: Top 5 Products (Bar Chart)
worksheet_prod = writer.sheets['Top Products']
chart_prod = workbook.add_chart({'type': 'bar'})
chart_prod.add_series({
    'name':       ['Top Products', 0, 1],
    'categories': ['Top Products', 1, 0, len(top_products), 0],
    'values':     ['Top Products', 1, 1, len(top_products), 1],
    'data_labels': {'value': True},
})
chart_prod.set_title({'name': 'Top 5 Products by Sales'})
chart_prod.set_x_axis({'name': 'Product'})
chart_prod.set_y_axis({'name': 'Total Sales'})
worksheet_prod.insert_chart('D2', chart_prod)

# Chart 3: Monthly Sales Trend (Line Chart)
worksheet_month = writer.sheets['Monthly Sales Trend']
chart_month = workbook.add_chart({'type': 'line'})
chart_month.add_series({
    'name':       ['Monthly Sales Trend', 0, 1],
    'categories': ['Monthly Sales Trend', 1, 0, len(monthly_sales_trend), 0],
    'values':     ['Monthly Sales Trend', 1, 1, len(monthly_sales_trend), 1],
    'data_labels': {'value': True},
})
chart_month.set_title({'name': 'Monthly Sales Trend'})
chart_month.set_x_axis({'name': 'Month'})
chart_month.set_y_axis({'name': 'Total Sales'})
worksheet_month.insert_chart('D2', chart_month)


# Close the Pandas Excel writer and output the Excel file.
writer.close()
print(f"\n✅ All analyses complete and dashboard report saved to '{output_excel_file}' with embedded charts!")
'''


import pyodbc
from flask import Flask, jsonify
from flask_cors import CORS
import logging

# --- Basic Setup ---
app = Flask(__name__)
# Enable CORS to allow the HTML file to call the API
CORS(app) 
# Set debug=False for a cleaner terminal output, change to True for debugging
app.debug = False 

# Suppress informational logs for a cleaner terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

# --- Database Connection ---
# IMPORTANT: Replace 'YOUR_SERVER_NAME' with your actual server name from SSMS.
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=BALJEET_SINGH\SQLEXPRESS;'
    r'DATABASE=ECommerceDB;'
    r'Trusted_Connection=yes;'
)

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# --- API Endpoints ---

@app.route('/api/kpis', methods=['GET'])
def get_kpis():
    """Calculates and returns key performance indicators."""
    query = """
    SELECT 
        ISNULL(SUM(TotalAmount), 0) as TotalRevenue,
        ISNULL(COUNT(DISTINCT OrderID), 0) as TotalOrders,
        ISNULL(AVG(TotalAmount), 0) as AvgOrderValue,
        ISNULL(COUNT(DISTINCT CustomerID), 0) as UniqueCustomers,
        ISNULL(SUM(T.TotalQuantity), 0) as TotalItems
    FROM Orders
    CROSS APPLY (
        SELECT SUM(Quantity) as TotalQuantity 
        FROM OrderDetails 
        WHERE OrderDetails.OrderID = Orders.OrderID
    ) T;
    """
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        
        # Calculate ItemsPerOrder safely
        items_per_order = (row.TotalItems / row.TotalOrders) if row.TotalOrders > 0 else 0

        kpis = {
            "TotalRevenue": row.TotalRevenue,
            "TotalOrders": row.TotalOrders,
            "AvgOrderValue": row.AvgOrderValue,
            "UniqueCustomers": row.UniqueCustomers,
            "ItemsPerOrder": items_per_order
        }
        conn.close()
        return jsonify(kpis)
    except Exception as e:
        print(f"Database query failed: {e}")
        conn.close()
        return jsonify({"error": "Failed to fetch KPIs"}), 500

@app.route('/api/monthly-sales', methods=['GET'])
def get_monthly_sales():
    """Returns total sales for each month."""
    query = """
    SELECT 
        FORMAT(OrderDate, 'yyyy-MM') as OrderMonth,
        SUM(TotalAmount) as TotalSales
    FROM Orders
    GROUP BY FORMAT(OrderDate, 'yyyy-MM')
    ORDER BY OrderMonth;
    """
    # This endpoint is reused from the previous version
    conn = get_db_connection()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = [{"OrderMonth": row.OrderMonth, "TotalSales": row.TotalSales} for row in cursor.fetchall()]
        conn.close()
        return jsonify(data)
    except Exception as e:
        print(f"Database query failed: {e}")
        conn.close()
        return jsonify([])

@app.route('/api/category-sales', methods=['GET'])
def get_category_sales():
    """Returns total sales for each product category."""
    query = """
    SELECT 
        c.CategoryName,
        SUM(od.Subtotal) as TotalSales
    FROM OrderDetails od
    JOIN Products p ON od.ProductID = p.ProductID
    JOIN Categories c ON p.CategoryID = c.CategoryID
    GROUP BY c.CategoryName
    ORDER BY TotalSales DESC;
    """
    # This endpoint is reused from the previous version
    conn = get_db_connection()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = [{"CategoryName": row.CategoryName, "TotalSales": row.TotalSales} for row in cursor.fetchall()]
        conn.close()
        return jsonify(data)
    except Exception as e:
        print(f"Database query failed: {e}")
        conn.close()
        return jsonify([])

@app.route('/api/top-products', methods=['GET'])
def get_top_products():
    """Returns the top 5 selling products by sales."""
    query = """
    SELECT TOP 5
        p.ProductName,
        SUM(od.Subtotal) as TotalSales
    FROM OrderDetails od
    JOIN Products p ON od.ProductID = p.ProductID
    GROUP BY p.ProductName
    ORDER BY TotalSales DESC;
    """
    # This endpoint is reused from the previous version
    conn = get_db_connection()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = [{"ProductName": row.ProductName, "TotalSales": row.TotalSales} for row in cursor.fetchall()]
        conn.close()
        return jsonify(data)
    except Exception as e:
        print(f"Database query failed: {e}")
        conn.close()
        return jsonify([])

@app.route('/api/sales-by-city', methods=['GET'])
def get_sales_by_city():
    """NEW: Returns total sales for each customer city."""
    query = """
    SELECT TOP 5
        c.City,
        SUM(o.TotalAmount) as TotalSales
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
    GROUP BY c.City
    ORDER BY TotalSales DESC;
    """
    conn = get_db_connection()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = [{"City": row.City, "TotalSales": row.TotalSales} for row in cursor.fetchall()]
        conn.close()
        return jsonify(data)
    except Exception as e:
        print(f"Database query failed: {e}")
        conn.close()
        return jsonify([])
        
@app.route('/api/payment-methods', methods=['GET'])
def get_payment_methods():
    """NEW: Returns the usage count for each payment method."""
    query = """
    SELECT 
        PaymentMethod,
        COUNT(PaymentID) as UsageCount
    FROM Payment
    GROUP BY PaymentMethod
    ORDER BY UsageCount DESC;
    """
    conn = get_db_connection()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = [{"PaymentMethod": row.PaymentMethod, "UsageCount": row.UsageCount} for row in cursor.fetchall()]
        conn.close()
        return jsonify(data)
    except Exception as e:
        print(f"Database query failed: {e}")
        conn.close()
        return jsonify([])

@app.route('/api/sales-data', methods=['GET'])
def get_sales_data():
    """Returns the most recent 20 order details for the live feed."""
    query = """
    SELECT TOP 20
        o.OrderID, 
        c.FirstName + ' ' + c.LastName as CustomerName, 
        p.ProductName, 
        cat.CategoryName, 
        od.Subtotal
    FROM OrderDetails od
    JOIN Orders o ON od.OrderID = o.OrderID
    JOIN Products p ON od.ProductID = p.ProductID
    JOIN Categories cat ON p.CategoryID = cat.CategoryID
    JOIN Customers c ON o.CustomerID = c.CustomerID
    ORDER BY o.OrderDate DESC, o.OrderID DESC;
    """
    # This endpoint is reused from the previous version
    conn = get_db_connection()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = [{"OrderID": row.OrderID, "CustomerName": row.CustomerName, "ProductName": row.ProductName, "CategoryName": row.CategoryName, "Subtotal": row.Subtotal} for row in cursor.fetchall()]
        conn.close()
        return jsonify(data)
    except Exception as e:
        print(f"Database query failed: {e}")
        conn.close()
        return jsonify([])

# --- Main Execution ---
if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)
