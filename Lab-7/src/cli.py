import argparse
from tabulate import tabulate
from . import queries

def print_table(rows):
    if not rows:
        print("(no results)")
        return
    headers = list(rows[0].keys())
    data = [list(r.values()) for r in rows]
    print(tabulate(data, headers=headers, tablefmt="github"))

def main():
    p = argparse.ArgumentParser(description="Lab 7: MySQL query CLI for My Guitar Shop")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("top-products", help="Show top N products by list price")
    sp.add_argument("--limit", type=int, default=5)

    sp = sub.add_parser("discounted", help="Products with discount >= min percent")
    sp.add_argument("--min", dest="min_discount", type=float, default=20.0)

    sub.add_parser("unshipped", help="Unshipped orders")

    sub.add_parser("revenue-by-category", help="Aggregated revenue per category")    

    sp = sub.add_parser("customer-orders", help="Order totals for a specific customer")
    sp.add_argument("customer_id", type=int)

    sp = sub.add_parser("search", help="Search products by keyword in name or description")
    sp.add_argument("keyword", type=str)

    sp = sub.add_parser("recent-products", help="Products added in the last N days")
    sp.add_argument("--days", type=int, default=120)

    args = p.parse_args()

    if args.cmd == "top-products":
        print_table(queries.top_products_by_price(args.limit))
    elif args.cmd == "discounted":
        print_table(queries.discounted_products(args.min_discount))
    elif args.cmd == "unshipped":
        print_table(queries.unshipped_orders())
    elif args.cmd == "revenue-by-category":
        print_table(queries.revenue_by_category())
    elif args.cmd == "customer-orders":
        print_table(queries.customer_order_summary(args.customer_id))
    elif args.cmd == "search":
        print_table(queries.search_products(args.keyword))
    elif args.cmd == "recent-products":
        print_table(queries.recent_products(args.days))

if __name__ == "__main__":
    main()
