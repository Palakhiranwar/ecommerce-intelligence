import pandas as pd

df = pd.read_csv("data/cleaned/fact_sales.csv")

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])


# 1. TOTAL REVENUE
total_revenue = df['payment_value'].sum()
print("Total Revenue:", round(total_revenue,2))


# 2. MONTHLY REVENUE
df['year'] = df['order_purchase_timestamp'].dt.year
df['month'] = df['order_purchase_timestamp'].dt.month

monthly_revenue = df.groupby(['year','month'])['payment_value'].sum().reset_index()

print("\nMonthly Revenue:")
print(monthly_revenue.head())



# 3. TOP CUSTOMERS
top_customers = df.groupby('customer_unique_id')['payment_value'].sum().sort_values(ascending=False).head(10)

print("\nTop Customers:")
print(top_customers)



# 4. TOP PRODUCTS
top_products = df.groupby('product_id')['payment_value'].sum().sort_values(ascending=False).head(10)

print("\nTop Products:")
print(top_products)


# 5. LOW PERFORMING PRODUCTS 
low_products = df.groupby('product_id')['payment_value'].sum().sort_values().head(10)

print("\nLow Performing Products:")
print(low_products)