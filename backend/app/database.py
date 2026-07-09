import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


load_dotenv()


raw_database_url = os.getenv("DATABASE_URL", "sqlite:///./hcp_crm.db")
placeholder_postgres_url = "postgresql://postgres:password@localhost:5432/hcp_crm"
DATABASE_URL = (
    "sqlite:///./hcp_crm.db"
    if raw_database_url == placeholder_postgres_url
    else raw_database_url
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    import app.models

    Base.metadata.create_all(bind=engine)
