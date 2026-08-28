from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
DB_URL = "postgresql://postgres:password@localhost/OllamaBridge"
engine = create_engine(url=DB_URL)
SessionLocal = sessionmaker(engine, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()