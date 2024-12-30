from sqlalchemy.orm import sessionmaker
from models import model

session = sessionmaker(autocommit=False, autoflush=True, bind=model.engine)

def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()
