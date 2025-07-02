
# Lab 5: Guitar Shop MySQL Docker

## Introduction

This project provides a containerized implementation of the "My Guitar Shop" MySQL database using Docker Compose. It allows developers and learners to deploy a complete, ready-to-query relational database system with minimal setup.

## Project Description

The My Guitar Shop database simulates a music instrument e-commerce platform. It includes structured data for products, customers, orders, and administrative users. This version of the project uses Docker Compose to spin up a MySQL container and initialize it with a predefined schema and data.

## Project Design

The database consists of the following key tables:

- **categories**: Instrument categories (e.g., Guitars, Basses)
- **products**: Items available for purchase
- **customers**: Customer profiles
- **addresses**: Shipping and billing addresses
- **orders**: Orders placed by customers
- **order_items**: Items included in each order
- **administrators**: Admin login credentials

Docker Compose is used to orchestrate the MySQL container, preload it with the schema and data using a mounted SQL file, and expose port 3306 to your local machine.

## How to Run the Project

### 1. Prerequisites

- Docker installed on your system
- Docker Compose (included with Docker Desktop)

### 2. Folder Structure

```
guitar-shop-docker/
├── docker-compose.yml
└── init/
    └── createguitar.sql
```

### 3. Setup Steps

#### Step 1: Create the project directory
```bash
mkdir -p ~/Desktop/guitar-shop-docker/init
cd ~/Desktop/guitar-shop-docker
```

#### Step 2: Place Files
- Place `docker-compose.yml` inside `guitar-shop-docker/`
- Place `createguitar.sql` inside `guitar-shop-docker/init/`

#### Step 3: Start the container
```bash
docker-compose up -d
```

#### Step 4: Connect to the Database
Use MySQL Workbench or any SQL client:

- Host: `127.0.0.1`
- Port: `3306`
- User: `root`
- Password: `rootpass`
- Database: `my_guitar_shop`

Once connected, you can run SQL queries or import the provided query file to explore and analyze the dataset.
