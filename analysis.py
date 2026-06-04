import pandas as pd
import sqlite3

conn = sqlite3.connect('olist_database.db')

df_monthly = pd.read_sql_query("""
SELECT 
    strftime('%Y-%m', o.order_purchase_timestamp) as month,
    COUNT(*) as total_orders,
    SUM(oi.price) as total_revenue
FROM olist_orders_dataset o
JOIN olist_order_items_dataset oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY strftime('%Y-%m', o.order_purchase_timestamp)
ORDER BY month
""", conn)

df_categories = pd.read_sql_query("""
SELECT 
    p.product_category_name,
    COUNT(*) as total_sales,
    ROUND(SUM(oi.price), 2) as total_revenue
FROM olist_order_items_dataset oi
JOIN olist_products_dataset p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10
""", conn)

df_cities = pd.read_sql_query("""
SELECT 
    customer_city,
    COUNT(*) as customer_count
FROM olist_customers_dataset
GROUP BY customer_city
ORDER BY customer_count DESC
LIMIT 10
""", conn)

conn.close()

print(df_monthly)
print(df_categories)
print(df_cities)