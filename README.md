
# E-Commerce Data Analytics Dashboard

This project presents a full-stack, real-time data analytics dashboard for an e-commerce dataset. It demonstrates a complete data pipeline, starting from a structured SQL database, processed through a Python backend, and visualized on a dynamic, live-updating web interface.


## 🚀Dashboard Preview

The web dashboard provides a clean, at-a-glance overview of key business metrics and trends, pulling data directly from the database every 5 seconds.

- Live Dashboard Screenshot:

(Your screenshot of `live_dashboard.html` in action will appear here)

- Exported Excel Report:

(Your screenshot of the `exported .csv` file opened in Excel will appear here)

## ✨ Core Features

- Real-Time Analytics: All KPIs and charts refresh automatically every 5 seconds to reflect the latest data from the database.

- Live Database Connection: A Python Flask backend serves as a robust API bridge to the Microsoft SQL Server (SSMS) database.

- Comprehensive KPIs: Displays over 10 key analytics, including:

    - Total Revenue & Total Orders

    - Average Order Value & Unique Customers

    - Items Per Order

- Interactive Visualizations:

     - Monthly Sales Trend: A smooth, gradient-filled line chart showing revenue over time.

   - Sales by Category: A doughnut chart breaking down revenue by product category.

   - Top Selling Products: A horizontal bar chart highlighting the best-performing products.

  -  Top Cities by Sales: A bar chart showing which geographical locations are most profitable.

  -  Payment Method Usage: A pie chart illustrating the popularity of different payment methods.

- Live Order Feed: A scrolling table that shows the 20 most recent order details as they happen.

- Export to Excel: A one-click button to download the current raw order data as a .csv file, ready for offline analysis in Excel.

## 🛠️ Technology Stack & Architecture

This project is built with a classic three-tier architecture, separating the database, server logic, and user interface.

- **Database:**
   - Microsoft SQL Server (managed via SSMS)

- **Backend API:**

  - **Language:** Python 3

  - **Core Libraries:** Flask (for the web server), pyodbc (for SQL Server connection), Pandas (for data handling).

- **Frontend:**

  - **Languages:** HTML5, CSS3, JavaScript

  - **Core Libraries:** Tailwind CSS (for styling), Chart.js (for visualizations).
  

**Data Flow**

The data flows in a simple, unidirectional path from the source to the presentation layer.

`[ MS SQL Server Database ] → [ Python (Flask) API ] → [ Frontend (HTML, CSS, Chart.js) ]`


## ⚙️ Local Setup and Installation

To run this project on your local machine, follow these steps.

**Prerequisites**

   - Microsoft SQL Server Management Studio (SSMS)

   - Python 3.8 or newer

   - Git (for cloning the repository)

 **1. Clone the Repository**
To get a copy of this project on your local machine, you'll need to clone it from GitHub.

     1. Go to the main page of the GitHub repository.

     2. Click the green <> Code button.

     3. Copy the URL under the "HTTPS" tab.

     4. Open a terminal or command prompt on your computer and 



```bash
# This command downloads the repository to your machine
git clone <paste-the-repository-url-here>

# This command navigates you inside the newly created project folder
cd ecommerce-dashboard
```

**2. Database Setup**

    1. Open SSMS and connect to your database engine.

    2. Create a new database named ECommerceDB.

    3. Open the provided SQL script files `(database_setup.sql, insert_data.sql, etc.)` and run them to create the tables and insert the sample data.
    

**3. Backend Configuration**

1.Create a virtual environment (recommended):
 ```bash
   python -m venv venv
```

2.Activate the environment:

```bash
On Windows: .\venv\Scripts\activate

On macOS/Linux: source venv/bin/activate
```

3.Install the required libraries:
 ```bash
 pip install -r requirements.txt
 ```
(Note: Ensure you have a `requirements.txt` file with Flask, pyodbc, flask-cors, etc.)


4.IMPORTANT: Configure the Database Connection:
- Open the `analysis.py` file.

- Find the conn_str variable and replace the placeholder `YOUR_SERVER_NAME` with your actual server name from SSMS.

```bash
# Find this line in analysis.py
r'SERVER=YOUR_SERVER_NAME;' # <-- CHANGE THIS
```

**4. Run the Application**

1.Start the Backend Server:

 - Open your terminal in the project directory.

  - Run the Flask application:

  ```bash
  python analysis.py
  ```
  
2.Launch the Frontend:

- Navigate to the project folder in your file explorer.

- Double-click the `live_dashboard.html` file to open it in your web browser.
## Screenshots

- Live Dashboard Screenshot:
![Dashboard Preview](./screenshorts/sc-1.png)
![Dashboard Preview](./screenshorts/sc-2.png)
![Dashboard Preview](./screenshorts/sc-3.png)
![Dashboard Preview](./screenshorts/sc-4.png)

-Exported Excel Report:



## 🚧 Future Improvements

- ✅ Add authentication for dashboard access

- ✅ Deploy on cloud (Heroku/Azure/AWS)

- ✅ Add predictive analytics (e.g., sales forecasting with ML)
## 📁 Project Structure

        ecommerce-dashboard/
        │
        ├── 📂 screenshort/
        │   ├── dashboard_screenshot.png
        │   ├──
        │   ├──
        │   └── excel_export_screenshot.png
        │
        ├── 📜 analysis.py         # The Python Flask backend     server and API logic.
        ├── 📜 live_dashboard.html # The main frontend file for the web dashboard.
        ├── 📜 README.md           # This documentation file.
        ├── 📜 ecommerce_sales_report.xlsx
        ├── 
        ├── live_ecommerce_export.csv
        └── 📜 e_commerce_dashboard_report.xlsx   