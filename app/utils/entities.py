from sqlalchemy import  Column, Integer, String
from app.db_connection.database import Base
from app.db_connection.database import engine
from pydantic import BaseModel
import uuid

class DataBaseConnection(Base):
    __tablename__ = "database_connections"

    id = Column(String,primary_key=True,unique=True)
    db_name = Column(String)
    db_type = Column(String)
    db_host = Column(String)
    db_port = Column(Integer)
    db_username = Column(String)
    db_password = Column(String)
    db_description = Column(String, nullable=True)
    
Base.metadata.create_all(bind=engine)

class DataBaseSchema(BaseModel):
    id: str = str(uuid.uuid4())
    db_name: str
    db_type: str
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_description: str | None = None