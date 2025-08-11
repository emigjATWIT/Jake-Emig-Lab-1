# Lab 7 — Cloud Computing: Python Query CLI for My Guitar Shop Database

## Introduction
This project extends the work from **Lab 6**, where a MySQL database for the *My Guitar Shop* application was deployed in Docker and seeded with sample data.  
In **Lab 7**, we build a Python-based command-line interface (CLI) to query this database, display results in a user-friendly format, and provide automated tests to validate query functionality.

The project is designed to allow quick database exploration without manually logging into MySQL, making it easier to retrieve insights such as product lists, discounted items, customer order summaries, and category-level revenues.

---

## Project Description
The Lab 7 deliverable includes:
- **Python query functions** that connect to the MySQL database and execute SQL queries.
- **A CLI driver** built with `argparse` to run individual queries with various parameters.
- **Formatted output** using `tabulate` for easy-to-read tables.
- **Integration tests** written with `unittest` to verify queries return expected structures.
- **Environment-based configuration** so database credentials are not hard-coded.
- **Compatibility with Lab 6** — assumes the MySQL container from Lab 6 is running and seeded.

This CLI allows:
- Listing top N products by price
- Viewing products with a discount greater than or equal to a given percentage
- Listing unshipped orders
- Summarizing revenue by category
- Viewing all orders for a specific customer with totals
- Searching for products by keyword
- Listing products added within the last N days

---

## Project Design
The project is organized as follows:

```
Lab-7/
├── src/
│   ├── __init__.py        # Marks src as a package
│   ├── db.py              # Handles database connections
│   ├── queries.py         # Contains all query functions
│   └── cli.py             # CLI entry point
├── tests/
│   └── test_queries.py    # Integration tests
├── requirements.txt       # Python dependencies
├── .env.example           # Example database environment config
└── README.md              # Project documentation
```

### Key Components:
- **db.py**
  - Loads environment variables from `.env`
  - Establishes MySQL connection using `mysql-connector-python`
- **queries.py**
  - Each function executes a single SQL query and returns a list of dictionaries
- **cli.py**
  - Implements subcommands using `argparse`
  - Displays results in a table format
- **test_queries.py**
  - Runs integration tests against a running MySQL instance
  - Skips tests automatically if the database is unreachable

---

## Detailed Instructions to Run the Project

### 1. Prerequisites
- **Lab 6 MySQL container running and seeded** with `createguitar.sql`
- Python 3.10+ installed
- `pip` package manager installed
- Optional: `virtualenv` for environment isolation

---


### 3. Navigate to Lab 7 Folder
```bash
cd Lab-7
```

---

### 4. Set Up a Virtual Environment (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or:
.venv\Scripts\activate      # Windows
```

---

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 6. Configure Database Connection
Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` so it matches your Lab 6 MySQL setup:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=lab7          # or root
DB_PASSWORD=lab7pass  # or rootpass
DB_NAME=my_guitar_shop
```

---

### 7. Run the CLI
```bash
python -m src.cli --help
```

#### Examples:
- Top 5 products by price:
```bash
python -m src.cli top-products --limit 5
```
- Products with ≥25% discount:
```bash
python -m src.cli discounted --min 25
```
- Unshipped orders:
```bash
python -m src.cli unshipped
```
- Revenue by category:
```bash
python -m src.cli revenue-by-category
```
- Orders for customer with ID 1:
```bash
python -m src.cli customer-orders 1
```
- Search products containing "Gibson":
```bash
python -m src.cli search Gibson
```
- Products added in the last 365 days:
```bash
python -m src.cli recent-products --days 365
```

---

### 8. Run Tests
```bash
python -m unittest -v
```
> If the DB is unreachable, the tests will be skipped automatically.