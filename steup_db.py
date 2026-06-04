import pandas as pd
import sqlite3
import os

folder_path = os.path.dirname(os.path.abspath(file))
db_name = 'olist_database.db'

tables = [
    'olist_orders_dataset',
    'olist_order_items_dataset',
    'olist_products_dataset',
    'olist_customers_dataset',
    'olist_sellers_dataset',
    'olist_order_payments_dataset',
    'olist_order_reviews_dataset'
]

conn = sqlite3.connect(db_name)

for table in tables:
    file_path = os.path.join(folder_path, f"{table}.csv")
    df = pd.read_csv(file_path)
    df.to_sql(table, conn, if_exists='replace', index=False)
    print(f"{table}: {len(df)} rows")

conn.close()
print("Done!")