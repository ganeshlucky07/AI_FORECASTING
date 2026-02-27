import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use DATABASE_URL in production (e.g. PostgreSQL); default SQLite for local/dev.
# For containerized environments, use /app directory for SQLite
if os.getenv("DATABASE_URL"):
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    # Use /tmp for SQLite in containerized environments (Render, Docker)
    # as it may not have write permissions in /app
    db_path = "/tmp/forecasting.db" if os.path.isdir("/tmp") else "./forecasting.db"
    DATABASE_URL = f"sqlite:///{db_path}"

# Render/Heroku use postgres:// but SQLAlchemy 1.4+ expects postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a SQLAlchemy database session.
    It yields a session per request and ensures proper cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

