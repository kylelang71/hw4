import json
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

from agent import run_agent
from auth import hash_password, verify_password
from db import get_connection
from models import ChatRequest, ChatResponse, Product, SizeStock

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

app = FastAPI(title="Campus Customs API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/products-images", StaticFiles(directory=DATA_DIR / "products"), name="products-images")


def _row_to_product(row: dict, sizes: list[SizeStock]) -> Product:
    return Product(
        product_id=row["product_id"],
        name=row["name"],
        garment_type=row["garment_type"],
        description=row["description"],
        colors=json.loads(row["colors"]),
        search_tags=json.loads(row["search_tags"]),
        image_file_path=row["image_file_path"],
        price=row["price"],
        sizes=sizes,
    )


def _get_sizes(conn, product_id: str) -> list[SizeStock]:
    cur = conn.execute(
        "SELECT size, quantity FROM inventory WHERE product_id = ? ORDER BY id",
        (product_id,),
    )
    return [SizeStock(size=r["size"], quantity=r["quantity"]) for r in cur.fetchall()]


@app.get("/api/products", response_model=list[Product])
def list_products():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM catalogue ORDER BY name").fetchall()
        return [_row_to_product(dict(r), _get_sizes(conn, r["product_id"])) for r in rows]
    finally:
        conn.close()


@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM catalogue WHERE product_id = ?", (product_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return _row_to_product(dict(row), _get_sizes(conn, product_id))
    finally:
        conn.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def _user_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
        "email": row["email"],
    }


@app.post("/api/auth/register")
def register(req: RegisterRequest):
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if len(req.password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters"
        )

    conn = get_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (req.email,)
        ).fetchone()
        if existing is not None:
            raise HTTPException(status_code=409, detail="Email is already registered")

        name = f"{req.first_name} {req.last_name}".strip()
        password_hash = hash_password(req.password)
        cur = conn.execute(
            """
            INSERT INTO users (name, first_name, last_name, email, password_hash)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, req.first_name, req.last_name, req.email, password_hash),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
        return _user_to_dict(row)
    finally:
        conn.close()


@app.post("/api/auth/login")
def login(req: LoginRequest):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (req.email,)
        ).fetchone()
        if row is None or not verify_password(req.password, row["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return _user_to_dict(row)
    finally:
        conn.close()


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = run_agent(req.message, req.user_id, req.page_html)
    return ChatResponse(
        reply=result.get("reply", ""),
        tools_used=list(result.get("tools_used") or []),
        products=list(result.get("products") or []),
    )
