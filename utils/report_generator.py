import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def fetch_orders():
    conn = sqlite3.connect('db/restaurant.db')
    df_orders = pd.read_sql_query("SELECT * FROM orders", conn)
    df_items = pd.read_sql_query("SELECT * FROM order_items", conn)
    conn.close()
    return df_orders, df_items

def generate_sales_summary():
    df_orders, _ = fetch_orders()
    df_orders['date'] = pd.to_datetime(df_orders['date'])

    today = pd.Timestamp.now().normalize()
    week_ago = today - pd.Timedelta(days=7)
    month_ago = today - pd.Timedelta(days=30)

    summary = {
        "Daily Sales": df_orders[df_orders['date'].dt.date == today.date()]['total'].sum(),
        "Weekly Sales": df_orders[df_orders['date'] >= week_ago]['total'].sum(),
        "Monthly Sales": df_orders[df_orders['date'] >= month_ago]['total'].sum(),
        "Total Orders": len(df_orders),
    }

    return summary

def generate_most_sold_items():
    _, df_items = fetch_orders()
    top_items = df_items.groupby('item')['quantity'].sum().sort_values(ascending=False).reset_index()
    return top_items

def export_sales_report():
    sales_summary = generate_sales_summary()
    most_sold = generate_most_sold_items()

    with open("data/sales_report.csv", "w") as f:
        f.write("SALES SUMMARY\n")
        for key, value in sales_summary.items():
            f.write(f"{key},{value}\n")

        f.write("\nMOST SOLD ITEMS\n")
        most_sold.to_csv(f, index=False)

    print("✅ Report exported to 'data/sales_report.csv'")
