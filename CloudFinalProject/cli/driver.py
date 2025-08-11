import os
import time
from urllib.parse import urljoin

import requests
import redis
import boto3


# --------- Config (overridable via environment) ----------
# If running on host: API_BASE defaults to http://localhost:8088/
# If running in a Docker python container: set API_BASE=http://web/
API_BASE = os.getenv("API_BASE") or f"http://localhost:{os.getenv('WEB_PORT', '8088')}/"
API = urljoin(API_BASE, "api/")

# Postgres host:
# - Host run: "localhost"
# - In Docker: set DB_HOST=db
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "guitarshop")
DB_USER = os.getenv("DB_USER", "clouduser")
DB_PASS = os.getenv("DB_PASS", "cloudpass")

# Redis host:
# - Host run: "localhost"
# - In Docker: set REDIS_HOST=redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# MinIO endpoint visible to the client running this script
# - Host run: http://localhost:9000
# - In Docker: set MINIO_PUBLIC_ENDPOINT=http://minio:9000
MINIO_PUBLIC_ENDPOINT = os.getenv("MINIO_PUBLIC_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")
MINIO_REGION = os.getenv("MINIO_REGION", "us-east-1")

SESSION = requests.Session()  # keep cookies across calls


# ----------------- Helpers -----------------
def wait_for_web(timeout=60):
    """Wait until the LB/backend is reachable."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(API_BASE, timeout=2)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def api(path, method="GET", **kwargs):
    url = urljoin(API, path)
    r = SESSION.request(method, url, **kwargs)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return r.text


# ----------------- API Calls -----------------
def login(username="demo", password="demo"):
    return api("auth/login", method="POST", json={"username": username, "password": password})


def whoami():
    return api("auth/me")


def list_products():
    return api("products")


def create_product(name, price):
    return api("products", method="POST", json={"name": name, "price": price})


def send_email(to="customer@example.com", subject="Hello", body="From CLI"):
    return api("util/send-email", method="POST", json={"to": to, "subject": subject, "body": body})


def upload_sample_file():
    # Create a small file in-memory
    files = {'file': ('hello.txt', b'Hello from CLI')}
    url = urljoin(API, "files/upload")
    r = SESSION.post(url, files=files)
    r.raise_for_status()
    return r.text


# ----------------- Direct Infra Access -----------------
def direct_postgres():
    """
    Uses psycopg 3. Tries DB_HOST first; if it's 'localhost' and that fails,
    automatically retries with 'db' (useful when running inside Docker).
    """
    import psycopg

    conn_str = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

    def _query(conn_info):
        with psycopg.connect(conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM products")
                (count,) = cur.fetchone()
        return {"product_count": count}

    try:
        return _query(conn_str)
    except Exception as e:
        # If running inside a container but forgot DB_HOST=db, try fallback
        if DB_HOST == "localhost":
            try:
                fallback = f"host=db port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"
                return _query(fallback)
            except Exception:
                pass
        raise e


def direct_redis():
    """
    Connects to Redis. If REDIS_HOST=localhost fails and we're in Docker,
    automatically retries 'redis'.
    """
    def _get(host):
        r = redis.Redis(host=host, port=REDIS_PORT, decode_responses=True)
        r.setex("cli:ping", 60, "pong")
        return r.get("cli:ping")

    try:
        val = _get(REDIS_HOST)
        return {"redis_get": val}
    except Exception as e:
        if REDIS_HOST == "localhost":
            try:
                val = _get("redis")
                return {"redis_get": val}
            except Exception:
                pass
        raise e


def direct_minio():
    """
    Lists buckets via S3 API. Works against public MinIO endpoint configured above.
    """
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_PUBLIC_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        region_name=MINIO_REGION,
    )
    buckets = s3.list_buckets().get("Buckets", [])
    return {"buckets": [b["Name"] for b in buckets]}


# ----------------- Main -----------------
if __name__ == "__main__":
    print(f"API_BASE: {API_BASE}")
    print("Waiting for stack to be ready...")
    if not wait_for_web():
        raise SystemExit(
            "Backend/LB not reachable. Make sure `docker compose up --build --scale backend=2` is running "
            "and adjust API_BASE if running inside Docker (e.g., API_BASE=http://web/)."
        )

    print("Logging in:", login())
    print("Who am I?:", whoami())
    print("Create product:", create_product("Les Paul", 2499.00))
    print("List products:", list_products())
    print("Upload file:", upload_sample_file())
    print("Send email:", send_email())
    print("Direct Postgres:", direct_postgres())
    print("Direct Redis:", direct_redis())
    print("Direct MinIO:", direct_minio())
    print("Done.")