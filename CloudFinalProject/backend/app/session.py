import os, secrets, json
from http import cookies
import redis

COOKIE_NAME = os.getenv("COOKIE_NAME", "session_id")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def create_session(username: str) -> str:
    sid = secrets.token_hex(16)
    r.setex(f"session:{sid}", 60*60*12, json.dumps({"username": username}))  # 12h
    return sid

def get_session(sid: str):
    if not sid: return None
    data = r.get(f"session:{sid}")
    return json.loads(data) if data else None