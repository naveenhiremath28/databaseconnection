from sqlalchemy import  Column, Integer, String
from db_connection.database import Base
from db_connection.database import engine

class DataBaseConnection(Base):
    __tablename__ = "database_connections"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String,nullable=False,unique=True)
    db_name = Column(String)
    db_type = Column(String)
    db_host = Column(String)
    db_port = Column(Integer)
    db_username = Column(String)
    db_password = Column(String)
    db_description = Column(String)

Base.metadata.create_all(bind=engine)
