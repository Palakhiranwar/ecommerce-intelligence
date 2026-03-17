SELECT ROUND(SUM(payment_value),2) AS total_revenue
FROM fact_sales;

SELECT 
    YEAR(order_purchase_timestamp) AS year,
    MONTH(order_purchase_timestamp) AS month,
    ROUND(SUM(payment_value),2) AS revenue
FROM fact_sales
GROUP BY year, month
ORDER BY year, month;

SELECT 
    customer_unique_id,
    ROUND(SUM(payment_value),2) AS total_spent
FROM fact_sales
GROUP BY customer_unique_id
ORDER BY total_spent DESC
LIMIT 10;

SELECT 
    product_id,
    COUNT(*) AS total_orders,
    ROUND(SUM(payment_value),2) AS revenue
FROM fact_sales
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;

SELECT 
    product_id,
    COUNT(*) AS total_orders,
    ROUND(SUM(payment_value),2) AS revenue
FROM fact_sales
GROUP BY product_id
ORDER BY revenue ASC
LIMIT 10;

SELECT 
    customer_unique_id,
    SUM(payment_value) AS total_spent,
    CASE
        WHEN SUM(payment_value) > 10000 THEN 'VIP'
        WHEN SUM(payment_value) > 5000 THEN 'Regular'
        ELSE 'Low Value'
    END AS segment
FROM fact_sales
GROUP BY customer_unique_id
ORDER BY total_spent DESC;