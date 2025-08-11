#!/usr/bin/env python3
import os
import time
import click
import smtplib
from email.message import EmailMessage
from minio import Minio
from minio.error import S3Error
import redis

# ---------- Helpers ----------
def get_minio_client():
    endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key = os.getenv("MINIO_ROOT_USER", "lab8admin")
    secret_key = os.getenv("MINIO_ROOT_PASSWORD", "lab8admin123")
    secure = os.getenv("MINIO_SECURE", "false").lower() == "true"
    return Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

def get_bucket_name():
    return os.getenv("MINIO_BUCKET", "lab8-bucket")

def get_redis_client():
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    return redis.Redis(host=host, port=port, decode_responses=True)

def smtp_target():
    host = os.getenv("SMTP_HOST", "localhost")
    port = int(os.getenv("SMTP_PORT", "2525"))  # Postfix exposed at 2525 in compose
    return host, port

def wait_for_port(host, port, timeout=30):
    import socket
    start = time.time()
    while time.time() - start < timeout:
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect((host, port))
            s.close()
            return True
        except Exception:
            time.sleep(1)
    return False

# ---------- CLI ----------
@click.group()
def cli():
    """Lab 8 Command-Line Driver\"""
    pass

@cli.command("test-minio")
def test_minio():
    """Create a bucket, upload a file, then download it.\"""
    client = get_minio_client()
    bucket = get_bucket_name()

    # Ensure bucket exists
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)
        click.echo(f"Created bucket: {bucket}")
    else:
        click.echo(f"Bucket exists: {bucket}")

    # Upload sample file
    content = b"Hello from Lab 8 via MinIO!"
    obj_name = "hello.txt"
    import io
    client.put_object(bucket, obj_name, io.BytesIO(content), length=len(content))
    click.echo(f"Uploaded {obj_name} to bucket {bucket}")

    # Download and print content
    data = client.get_object(bucket, obj_name).read()
    click.echo(f"Downloaded content: {data.decode('utf-8')}")

@cli.command("test-redis")
def test_redis():
    """Demonstrate shared memory operations with Redis.\"""
    r = get_redis_client()
    # Simple counter
    r.set("lab8:counter", 0)
    r.incr("lab8:counter")
    r.incrby("lab8:counter", 41)
    counter = r.get("lab8:counter")

    # Shared list (queue semantics)
    r.delete("lab8:list")
    r.rpush("lab8:list", "alpha", "beta", "gamma")
    first = r.lpop("lab8:list")
    remaining = r.lrange("lab8:list", 0, -1)

    click.echo(f"Counter = {counter}")
    click.echo(f"Popped first element = {first}")
    click.echo(f"Remaining list = {remaining}")

@cli.command("test-email")
def test_email():
    """Send a test email through Postfix (relayed to MailHog).\"""
    host, port = smtp_target()
    if not wait_for_port(host, port, timeout=20):
        raise SystemExit(f"Unable to reach SMTP server at {host}:{port}. Is Docker Compose up?")

    msg = EmailMessage()
    msg["From"] = os.getenv("SMTP_FROM", "lab8@lab8.local")
    msg["To"] = os.getenv("SMTP_TO", "tester@example.com")
    msg["Subject"] = "Lab 8 Test Email"
    msg.set_content("Hello from Lab 8! If you see this in MailHog, Postfix relay works.")

    with smtplib.SMTP(host, port) as s:
        s.send_message(msg)

    click.echo(f"Email sent via SMTP {host}:{port}. Open MailHog UI on http://localhost:8025 to view.")

@cli.command("test-all")
def test_all():
    """Run all tests: MinIO, Redis, and Email.\"""
    click.echo("=== Testing MinIO ===")
    test_minio.main(standalone_mode=False)
    click.echo("=== Testing Redis ===")
    test_redis.main(standalone_mode=False)
    click.echo("=== Testing Email ===")
    test_email.main(standalone_mode=False)

if __name__ == "__main__":
    cli()
