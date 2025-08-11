import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

def get_connection():
    """Create and return a MySQL connection using env vars.
    
    ENV:
      DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
    """
    config = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "rootpass"),
        "database": os.getenv("DB_NAME", "my_guitar_shop"),
    }
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        raise RuntimeError(f"Failed to connect to DB ({config['host']}:{config['port']} as {config['user']}): {e}")
