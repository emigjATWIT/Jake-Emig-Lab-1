import os
import unittest
from src import queries

def _db_available() -> bool:
    # Quick ping by attempting a lightweight query through an existing function.
    try:
        queries.top_products_by_price(1)
        return True
    except Exception:
        return False

DB_READY = _db_available()

@unittest.skipUnless(DB_READY, "Database not reachable with current env vars; skipping integration tests.")
class TestQueriesIntegration(unittest.TestCase):

    def test_top_products_structure(self):
        rows = queries.top_products_by_price(3)
        self.assertIsInstance(rows, list)
        if rows:
            self.assertIn("product_id", rows[0])
            self.assertIn("product_name", rows[0])
            self.assertIn("list_price", rows[0])

    def test_discounted_minimum(self):
        rows = queries.discounted_products(20.0)
        for r in rows:
            self.assertGreaterEqual(float(r["discount_percent"]), 20.0)

    def test_unshipped_orders(self):
        rows = queries.unshipped_orders()
        # ship_date must be None/NULL in each row; mysql-connector gives None
        for r in rows:
            self.assertTrue(r["ship_date"] is None)

    def test_revenue_by_category_has_name_and_value(self):
        rows = queries.revenue_by_category()
        for r in rows:
            self.assertIn("category_name", r)
            self.assertIn("revenue", r)

    def test_customer_order_summary_types(self):
        rows = queries.customer_order_summary(1)
        for r in rows:
            self.assertIn("order_id", r)
            self.assertIn("total", r)

    def test_search_products_keyword(self):
        rows = queries.search_products("Gibson")
        for r in rows:
            self.assertIn("product_id", r)
            self.assertIn("product_name", r)

if __name__ == "__main__":
    unittest.main(verbosity=2)
