from typing import List, Dict, Any
from .db import get_connection

# Each query returns a list of dicts for easy CLI/table printing.

def fetch_all_dicts(cursor) -> List[Dict[str, Any]]:
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

def top_products_by_price(limit: int = 5) -> List[Dict[str, Any]]:
    sql = """
        SELECT p.product_id, p.product_name, p.list_price, c.category_name
        FROM products p
        JOIN categories c USING (category_id)
        ORDER BY p.list_price DESC, p.product_id ASC
        LIMIT %s
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (limit,))
        return fetch_all_dicts(cur)

def discounted_products(min_discount: float = 20.0) -> List[Dict[str, Any]]:
    sql = """
        SELECT product_id, product_name, list_price, discount_percent
        FROM products
        WHERE discount_percent >= %s
        ORDER BY discount_percent DESC, product_id ASC
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (min_discount,))
        return fetch_all_dicts(cur)

def unshipped_orders() -> List[Dict[str, Any]]:
    sql = """
        SELECT o.order_id, o.customer_id, o.order_date, o.ship_date, o.ship_amount, o.tax_amount
        FROM orders o
        WHERE o.ship_date IS NULL
        ORDER BY o.order_date ASC
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return fetch_all_dicts(cur)

def revenue_by_category() -> List[Dict[str, Any]]:
    # Revenue = sum((item_price - discount_amount) * quantity)
    sql = """
        SELECT c.category_name,
               ROUND(SUM((oi.item_price - oi.discount_amount) * oi.quantity), 2) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY revenue DESC, c.category_name ASC
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return fetch_all_dicts(cur)

def customer_order_summary(customer_id: int) -> List[Dict[str, Any]]:
    sql = """
        SELECT o.order_id,
               DATE(o.order_date) AS order_date,
               ROUND(SUM((oi.item_price - oi.discount_amount) * oi.quantity), 2) AS subtotal,
               o.ship_amount,
               o.tax_amount,
               ROUND(
                 SUM((oi.item_price - oi.discount_amount) * oi.quantity)
                 + o.ship_amount + o.tax_amount, 2
               ) AS total
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.customer_id = %s
        GROUP BY o.order_id, DATE(o.order_date), o.ship_amount, o.tax_amount
        ORDER BY o.order_date ASC
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (customer_id,))
        return fetch_all_dicts(cur)

def search_products(keyword: str) -> List[Dict[str, Any]]:
    sql = """
        SELECT product_id, product_name, list_price
        FROM products
        WHERE product_name LIKE %s OR description LIKE %s
        ORDER BY product_id ASC
    """
    kw = f"%{keyword}%"
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (kw, kw))
        return fetch_all_dicts(cur)

def recent_products(days: int = 120) -> List[Dict[str, Any]]:
    sql = """
        SELECT product_id, product_name, date_added
        FROM products
        WHERE date_added IS NOT NULL
          AND date_added >= (NOW() - INTERVAL %s DAY)
        ORDER BY date_added DESC
    """
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (days,))
        return fetch_all_dicts(cur)