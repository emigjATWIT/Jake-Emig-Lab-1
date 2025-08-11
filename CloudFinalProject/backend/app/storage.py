import os, boto3
from botocore.client import Config

endpoint = os.getenv("MINIO_ENDPOINT", "minio:9000")
access_key = os.getenv("MINIO_ACCESS_KEY", "minio")
secret_key = os.getenv("MINIO_SECRET_KEY", "minio123")
bucket = os.getenv("MINIO_BUCKET", "guitar-uploads")
secure = os.getenv("MINIO_SECURE", "0") == "1"

s3 = boto3.client(
    "s3",
    endpoint_url=f"http{'s' if secure else ''}://{endpoint}",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

def ensure_bucket():
    existing = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    if bucket not in existing:
        s3.create_bucket(Bucket=bucket)

def upload_bytes(key: str, data: bytes, content_type="application/octet-stream"):
    ensure_bucket()
    s3.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    return f"s3://{bucket}/{key}"