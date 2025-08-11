# CloudFinalProject

## Introduction
This project is a **containerized cloud application** built as part of a Cloud Computing final project.  
It demonstrates the design and deployment of a **multi-service cloud-native system** using **Docker Compose**.  
The application implements **modern cloud design patterns** including:

- **Microservices architecture**
- **Load balancing and scaling**
- **Persistent relational database**
- **Shared memory caching**
- **Email service**
- **Object storage**
- **Programmatic API access via a Python CLI**

This setup provides a realistic simulation of a production-ready environment suitable for deployment on cloud platforms like AWS ECS, Kubernetes, or Azure Container Instances.

---

## Project Description
The application is an **online guitar shop** with both a **web-based frontend** and a **REST API backend**.

Key features:
- User authentication with **cookie-based sessions**
- CRUD operations for **products** stored in **PostgreSQL**
- **Load balancing** between multiple backend replicas via **Nginx**
- **Email service** for sending test notifications (MailHog)
- **Object storage** for file uploads (MinIO, S3-compatible)
- **Shared memory** session store (Redis)
- **Web UI** for interacting with the app
- **Python CLI driver** for programmatic testing of all services

---

## Project Design

### **Architecture Overview**
```
            ┌───────────────────┐
            │   Frontend (Web)  │  ← Node.js BFF + HTML/JS
            └───────┬───────────┘
                    │
            ┌───────▼───────────┐
            │   Nginx Load Bal. │  ← Distributes traffic across backends
            └───────┬───────────┘
        ┌───────────┼───────────┐
        │           │           │
┌───────▼───────┐┌──▼────────┐┌─▼─────────┐
│ Backend API 1 ││Backend API││Backend API│ (FastAPI)
└───────┬───────┘└───┬───────┘└───┬───────┘
        │            │           │
        └───────┬────┴───────────┘
                │
        ┌───────▼───────────────────────┐
        │PostgreSQL  | Redis  | MinIO   │
        │(DB)        |(Cache) |(Storage)│
        └────────────┴────────┴─────────┘
```

### **Services**
- **`web`**: Node.js BFF serving the frontend
- **`backend`**: FastAPI application providing REST API
- **`db`**: PostgreSQL relational database
- **`pgadmin`**: Web-based DB admin interface
- **`redis`**: Shared memory/session store
- **`mailhog`**: Email capture/testing service
- **`minio`**: Object storage service
- **`nginx`**: Load balancer/proxy
- **`cli`**: Python driver for API + direct service access

---

## How to Run the Project


---

### **Start All Services**
```bash
docker compose up --build --scale backend=3
```
This will:
- Build the images
- Start **10+ containers** (3× backend replicas)
- Launch the database, storage, email service, and frontend

---

### **Access the Web Interfaces**
| Service       | URL                      | Credentials                  |
|---------------|--------------------------|------------------------------|
| Frontend      | http://localhost:8088    | demo / demo                   |
| MailHog       | http://localhost:8025    | *(no login)*                  |
| MinIO Console | http://localhost:9001    | minio / minio123              |
| pgAdmin       | http://localhost:5050    | admin@example.com / admin     |

---

### **Using the Frontend**
1. Open **http://localhost:8088**
2. Login with `demo / demo`
3. Use:
   - **Who Am I?** → confirms cookie-based auth
   - **Add Sample Product** → stores in PostgreSQL
   - **List** → view products from DB
   - **Send Test Email** → appears in MailHog UI
   - **File Upload** → stored in MinIO

---

### **pgAdmin Setup**
1. Go to http://localhost:5050
2. Login: `admin@example.com / admin`
3. **Register New Server**:
   - General → Name: `Cloud DB`
   - Connection:
     - Host: `db`
     - Port: `5432`
     - Maintenance DB: `guitarshop`
     - Username: `clouduser`
     - Password: `cloudpass`
4. Save and view the `products` table under `public → Tables`.

---

### **Running the Python CLI Driver**

#### Option A — Local Python
```bash
cd cli
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python driver.py
```

#### Option B — Run in a Python Docker Container
```bash
docker run -it --rm   --network cloudfinalproject_default   -v "$(pwd)/cli:/cli"   python:3.11 bash -lc "cd /cli && pip install -r requirements.txt && python driver.py"
```

The CLI will:
- Log in and call API endpoints
- Create/list products
- Upload file to MinIO
- Send email via API
- Connect directly to Postgres
- Connect directly to Redis
- Connect directly to MinIO

---

### **Proving Requirements**
| Requirement | Proof |
|-------------|-------|
| ≥10 services | `docker compose ps` (3 backends) |
| Relational DB | pgAdmin + products table |
| Load balancing | Nginx + stop one backend and site still works |
| Email service | MailHog inbox |
| Shared memory | Redis session store |
| Object storage | MinIO console shows uploaded files |
| Programmatic access | `driver.py` output |

---

## 🧹 Stopping the Project
```bash
docker compose down
```
To also remove volumes (DB data, uploads, etc.):
```bash
docker compose down -v
```

---