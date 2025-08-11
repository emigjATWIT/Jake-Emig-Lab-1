import os, io, json
from fastapi import FastAPI, Depends, Request, Response, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy.orm import Session
from .db import SessionLocal, init_db, User, Product
from .session import COOKIE_NAME, create_session, get_session
from .storage import upload_bytes
from .mailer import send_email

app = FastAPI(title="Guitar Shop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/", response_class=PlainTextResponse)
def root():
    return "OK"

# ---------------- Auth (cookie-based) ----------------
@app.post("/auth/login", response_class=PlainTextResponse)
def login(payload: dict, response: Response, db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    sid = create_session(username)
    response.set_cookie(key=COOKIE_NAME, value=sid, httponly=True, samesite="Lax")
    return "Logged in"

def require_user(request: Request):
    sid = request.cookies.get(COOKIE_NAME)
    sess = get_session(sid)
    if not sess:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return sess

@app.get("/auth/me", response_class=PlainTextResponse)
def me(user=Depends(require_user)):
    return f"Hello, {user['username']}"

# ---------------- Products ----------------
@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    items = db.query(Product).all()
    return [{"id": i.id, "name": i.name, "price": i.price} for i in items]

@app.post("/products")
def create_product(payload: dict, db: Session = Depends(get_db), user=Depends(require_user)):
    name = payload.get("name")
    price = float(payload.get("price", 0))
    p = Product(name=name, price=price)
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "name": p.name, "price": p.price}

# ---------------- Files -> MinIO ----------------
@app.post("/files/upload", response_class=PlainTextResponse)
async def upload(file: UploadFile = File(...), user=Depends(require_user)):
    data = await file.read()
    key = f"{user['username']}/{file.filename}"
    uri = upload_bytes(key, data, file.content_type or "application/octet-stream")
    return uri

# ---------------- Utilities ----------------
@app.post("/util/send-email")
def util_email(payload: dict, user=Depends(require_user)):
    result = send_email(payload["to"], payload.get("subject", "(no subject)"), payload.get("body", ""))
    return result