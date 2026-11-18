from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .database import Base, engine
from .models import User
from .routes import router
from .security import hash_password

app = FastAPI(title="Collaborative Document API")

# Get CORS origins from environment or use defaults
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
cors_origins = [origin.strip() for origin in cors_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def startup():
    """Create tables and seed demo users."""
    Base.metadata.create_all(bind=engine)
    
    # Run migration to add file_extension column if needed
    import sqlite3
    import os
    db_path = os.path.join(os.path.dirname(__file__), "..", "app.db")
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(documents)")
        columns = [row[1] for row in cursor.fetchall()]
        if "file_extension" not in columns:
            cursor.execute("ALTER TABLE documents ADD COLUMN file_extension VARCHAR(10) DEFAULT NULL")
            conn.commit()
        conn.close()
    
    # Seed demo users
    from .database import SessionLocal
    db = SessionLocal()
    try:
        # Check if users already exist
        if db.query(User).count() == 0:
            demo_users = [
                User(email="alice@example.com", name="Alice", password_hash=hash_password("password123")),
                User(email="bob@example.com", name="Bob", password_hash=hash_password("password123")),
                User(email="carol@example.com", name="Carol", password_hash=hash_password("password123")),
            ]
            db.add_all(demo_users)
            db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Collaborative Document API"}
