from pydantic import BaseModel
from datetime import datetime
from typing import Any
from models.model import DataBaseConnection

class DataBaseSchema(BaseModel):
    id: int
    uid: str
    db_name: str
    db_type: str
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_description: str

class ResponseSchema(BaseModel):
    timestamp:datetime = datetime.now()
    status: str
    message: Any

def format_response(status: str, message: Any) -> ResponseSchema:
    return ResponseSchema(status=status, message=message)

def generate_schema_object(data: DataBaseConnection):
    return DataBaseSchema(
        id=data.id,
        uid=data.uid,
        db_name=data.db_name,
        db_type=data.db_type,
        db_host=data.db_host,
        db_port=data.db_port,
        db_username=data.db_username,
        db_password=data.db_password,
        db_description=data.db_description
    )
