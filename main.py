import os
import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# ==========================
# Configuración básica
# ==========================

DB_PATH = "users.db"

load_dotenv()
PEPPER = os.getenv("APP_PEPPER", "")
if not PEPPER:
    raise RuntimeError("APP_PEPPER no está configurado")

# Argon2id
ph = PasswordHasher(
    time_cost=3,  # factor de trabajo
    memory_cost=64_000,  # KB (~64 MB)
    parallelism=4,
    hash_len=32,
    salt_len=16,
)

app = FastAPI(title="Auth con Argon2id y SQLite")


# ==========================
# Modelos Pydantic
# ==========================


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class MessageResponse(BaseModel):
    message: str


# ==========================
# Base de datos
# ==========================


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


# ==========================
# Funciones de contraseña
# ==========================


def hash_password(plain_password: str) -> str:
    value = plain_password + PEPPER
    return ph.hash(value)


def verify_password(plain_password: str, stored_hash: str) -> bool:
    value = plain_password + PEPPER
    try:
        ph.verify(stored_hash, value)
        return True
    except VerifyMismatchError:
        return False


def get_user_hash(username: str) -> Optional[str]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,),
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def create_user(username: str, password_hash: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise
    finally:
        conn.close()


# ==========================
# Eventos de aplicación
# ==========================


@app.on_event("startup")
def on_startup():
    init_db()


# ==========================
# Endpoints
# ==========================


@app.post(
    "/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate):
    if len(user.password) <= 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener más de 7 caracteres.",
        )

    password_hash = hash_password(user.password)

    try:
        create_user(user.username, password_hash)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe.",
        )

    return MessageResponse(message="Usuario registrado correctamente.")


@app.post("/login", response_model=MessageResponse)
def login(user: UserLogin):
    stored_hash = get_user_hash(user.username)
    if not stored_hash:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    if not verify_password(user.password, stored_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )

    return MessageResponse(message="Inicio de sesión exitoso.")
