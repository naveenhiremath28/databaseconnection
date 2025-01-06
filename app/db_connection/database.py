from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./database_connection.db"
engine = create_engine(DATABASE_URL) 
Base = declarative_base()


session = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()
