from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from rds_model import Base


# SQLite configuration
sqlite_url = "sqlite:///courses.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False},echo=True)
                                         
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False , autoflush=False)

# Initial migration to create database and tables
def create_db_and_tables():
    Base.metadata.create_all(engine)

# Session dependency
def get_session():
    with SessionLocal() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]