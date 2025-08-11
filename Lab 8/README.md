# Lab 8 — Local Cloud Services with Docker Compose + Python CLI


---


## Introduction

This lab stands up **local cloud services** using Docker Compose and demonstrates **programmatic access** via a Python command-line driver:

- **MinIO** — S3-compatible object storage (shared file system semantics for this lab).
- **Postfix** — Local SMTP server (relays outbound mail to **MailHog** so we can view messages without real email delivery).
- **Redis** — In‑memory key‑value store (used here to show shared memory patterns).

The provided Python CLI performs end‑to‑end tasks against each service to prove functionality.

---

## Project Description

- **Infrastructure**: A single `docker-compose.yml` orchestrates four containers:
  - `minio` — exposes S3 API at `localhost:9000` and console at `localhost:9001`.
  - `redis` — exposes port `6379`.
  - `mailhog` — receives email and provides a web UI at `localhost:8025`.
  - `postfix` — listens on SMTP **25** inside the container and is published on the host as **2525** to avoid root; it relays outbound email to `mailhog:1025`.
- **App**: `cli.py` (Python + Click) contains commands to:
  - Create an S3 bucket, upload/download a file (**MinIO**).
  - Set/increment counters and manage a queue/list (**Redis**).
  - Send a test email through **Postfix** (visible in **MailHog**).

---

## Design

### Why these services?
- **MinIO** is drop‑in S3 with a friendly local console; perfect for testing object storage and “shared filesystem” workflows.
- **Postfix + MailHog** allows safe email testing without exposing the Internet; Postfix serves as the SMTP server, and MailHog captures messages.
- **Redis** models shared memory with simple primitives (strings, counters, lists).

### Isolation & Networking
- All services run on the default Docker network created by Compose, so containers can resolve each other by service name (`postfix` → `mailhog`, etc.).

### Configuration
- Credentials and settings live in **`.env`** (you may change values as needed).
- MinIO persistence via a named Docker volume `minio-data`; Redis with AOF for durability.

---

## Prerequisites

- Docker & Docker Compose (v2+)
- Python 3.10+
- (Optional) A virtual environment tool like `venv` or `conda`

---

## How to Run

2. **Create a Python virtual environment and install dependencies**:

   ```bash
   cd "Lab 8"
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start the services**:

   ```bash
   docker compose --env-file .env up -d
   ```

   - MinIO API: http://localhost:9000
   - MinIO Console: http://localhost:9001  (login with `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` from `.env`)
   - Redis: localhost:6379
   - Postfix (SMTP): localhost:2525
   - MailHog UI: http://localhost:8025

4. **Run the Python driver to test everything**:

   ```bash
   # Ensure your venv is active
   python cli.py test-all
   ```

   You should see output showing:
   - Bucket creation/upload/download on MinIO
   - Redis counter/list operations
   - Email sent notice (view it in MailHog UI)

5. **Verify via UIs / tools**:
   - Open **MailHog** (http://localhost:8025) and confirm the message “Lab 8 Test Email” is present.
   - Open **MinIO Console** (http://localhost:9001), log in, and check that bucket `${MINIO_BUCKET}` contains `hello.txt`.
   - (Optional) Use `redis-cli -h localhost -p 6379` to inspect keys:
     ```bash
     redis-cli
     > GET lab8:counter
     > LRANGE lab8:list 0 -1
     ```

---

## Detailed Commands (for grading convenience)

- Start: `docker compose --env-file .env up -d`
- Stop: `docker compose down`
- Logs: `docker compose logs -f postfix` (or minio/redis/mailhog)
- Recreate: `docker compose up -d --build --force-recreate`
- Python (single services):
  - `python cli.py test-minio`
  - `python cli.py test-redis`
  - `python cli.py test-email`

---

## Troubleshooting

- **Ports already in use**: Change the host ports in `docker-compose.yml` (e.g., `2526:25`, `9002:9000`).
- **Cannot reach SMTP**: Ensure Postfix is up and published on `2525`. The CLI waits up to ~20 seconds.
- **MinIO auth**: Verify `.env` values match your login; change both the container env and client env (or export `MINIO_ENDPOINT`, etc.).
- **Firewall/VPN**: Localhost port proxies may be blocked by security software—temporarily disable or adjust rules.

---