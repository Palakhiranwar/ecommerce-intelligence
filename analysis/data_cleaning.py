import pandas as pd

customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

df = orders.merge(customers, on="customer_id", how="left")
df = df.merge(items, on="order_id", how="left")
df = df.merge(payments, on="order_id", how="left")

fact_sales = df[[
    "order_id",
    "customer_unique_id",
    "order_purchase_timestamp",
    "product_id",
    "price",
    "payment_value"
]]

fact_sales = fact_sales.drop_duplicates()

fact_sales.to_csv("data/cleaned/fact_sales.csv", index=False)

print("✅ fact_sales created successfully")