from pydantic import BaseModel
from datetime import datetime
from typing import Any

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

    class Config:
        orm_mode = True
        from_attributes = True

class ResponseSchema(BaseModel):
    timestamp:datetime = datetime.now()
    status: str
    message: Any

def format_response(status: str, message: Any) -> ResponseSchema:
    return ResponseSchema(status=status, message=message)
