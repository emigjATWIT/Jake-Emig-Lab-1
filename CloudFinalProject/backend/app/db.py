import os
from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://clouduser:cloudpass@db:5432/guitarshop")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)  # demo only (plain), not for prod!

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)
    # seed a demo user if missing
    with SessionLocal() as s:
        exists = s.execute(text("SELECT 1 FROM users WHERE username='demo'")).first()
        if not exists:
            s.add(User(username="demo", password="demo"))
            s.commit()