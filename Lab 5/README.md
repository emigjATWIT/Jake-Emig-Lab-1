
# Lab 5: My Guitar Shop Database

## Introduction

This project centers around creating and querying a sample MySQL database for a fictional business called "My Guitar Shop." The purpose of the database is to model real-world ecommerce operations for a music store, including product listings, customers, orders, and administrative management.

## Project Description

The project utilizes a provided SQL file (`createguitar.sql`) to:
- Create the database schema
- Populate the database with sample data
- Establish relational links between tables

Additionally, it includes a set of 10 SQL queries designed to demonstrate various data retrieval techniques, including filtering, joining, grouping, and aggregation.

## Project Design

The database consists of the following tables:

- `categories` – Types of instruments (Guitars, Basses, Drums, etc.)
- `products` – Instruments available for purchase
- `customers` – Customer information
- `addresses` – Shipping and billing addresses
- `orders` – Order details per customer
- `order_items` – Line items for each order
- `administrators` – Admin login credentials

The schema models a typical ecommerce backend with foreign keys connecting products to categories, orders to customers, and orders to their corresponding items.

## How to Run This Project

### 1. Install MySQL
If not already installed, install MySQL via:
- macOS: `brew install mysql`
- Ubuntu: `sudo apt install mysql-server`
- Windows: Use the MySQL Installer

### 2. Start MySQL Server
- macOS: `brew services start mysql`
- Ubuntu: `sudo systemctl start mysql`
- Windows: Start MySQL from Services or Workbench

### 3. Load the Database
1. Open MySQL Workbench
2. Open the file `createguitar.sql` using **File > Open SQL Script**
3. Click the **lightning bolt** to run the full script
4. Refresh the schema panel to confirm that `my_guitar_shop` was created

### 4. Run the Queries
1. Open the `guitar_database_queries.sql` file
2. Click **Run** to execute all queries
3. Verify each query’s output in the results grid
