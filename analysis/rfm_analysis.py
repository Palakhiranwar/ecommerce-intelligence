import pandas as pd

df = pd.read_csv("data/cleaned/fact_sales.csv")

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

reference_date = df['order_purchase_timestamp'].max()
rfm = df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,
    'order_id': 'nunique',
    'payment_value': 'sum'
}).reset_index()

rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
print(rfm.head())
rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])
def segment(row):
    if row['m_score'] == 5 and row['f_score'] >= 4:
        return 'VIP'
    elif row['f_score'] >= 3:
        return 'Regular'
    else:
        return 'Low Value'

rfm['segment'] = rfm.apply(segment, axis=1)
rfm.to_csv("data/cleaned/rfm_analysis.csv", index=False)