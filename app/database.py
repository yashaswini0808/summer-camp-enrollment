import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default to SQLite local file, but allow MySQL or Firestore/Postgres via env var DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./summer_camp.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for obtaining DB session per request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
