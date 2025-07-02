
-- Q1: List all categories
SELECT * FROM categories;

-- Q2: Get product names and prices for products costing more than $500
SELECT product_name, list_price FROM products WHERE list_price > 500;

-- Q3: Get customer names with last names starting with 'S'
SELECT first_name, last_name FROM customers WHERE last_name LIKE 'S%';

-- Q4: Get products with a discount greater than 20%
SELECT product_name, list_price, discount_percent FROM products WHERE discount_percent > 20;

-- Q5: Inner join products and order_items to show product names and quantities sold
SELECT p.product_name, oi.quantity FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id;

-- Q6: Inner join orders and customers to show order id and customer names
SELECT o.order_id, c.first_name, c.last_name FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- Q7: Count number of products in each category
SELECT c.category_name, COUNT(p.product_id) AS num_products FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name;

-- Q8: Count total orders per customer
SELECT customer_id, COUNT(order_id) AS total_orders FROM orders
GROUP BY customer_id;

-- Q9: Sum quantity sold per product
SELECT product_id, SUM(quantity) AS total_sold FROM order_items
GROUP BY product_id;

-- Q10: Calculate average product price
SELECT AVG(list_price) AS avg_price FROM products;
