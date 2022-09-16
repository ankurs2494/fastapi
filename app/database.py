from sqlalchemy import create_engine, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:ankurs@localhost/fastapi'

# engine is needed for sqlalchemy to connect with postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session is needed to connect to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (To create session to the database and close once done)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        