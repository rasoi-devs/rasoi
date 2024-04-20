from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DEBUG = False

USE_PG = True
PG_USER = "postgres"
PG_PASS = "password"
PG_DB = "rasoi3"

engine = None

if USE_PG:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql+psycopg://{PG_USER}:{PG_PASS}@localhost:5432/{PG_DB}"
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=DEBUG)
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./rasoi.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=DEBUG
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    # use it as a dependency in requests,
    # so that no matter what db connection is always closed
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
