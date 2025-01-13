from pydantic import BaseModel
from datetime import datetime
from typing import Any
from app.utils.entities import DataBaseConnection, DataBaseSchema

class ResponseSchema(BaseModel):
    timestamp:datetime = datetime.now()
    status: str
    message: Any

def format_response(status: str, message: Any) -> ResponseSchema:
    return ResponseSchema(status=status, message=message)

def generate_schema_object(data: DataBaseConnection) -> DataBaseSchema:
    return DataBaseSchema(
        id=data.id,
        db_name=data.db_name,
        db_type=data.db_type,
        db_host=data.db_host,
        db_port=data.db_port,
        db_username=data.db_username,
        db_password=data.db_password,
        db_description=data.db_description
    )

class Token(BaseModel):
    acess_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
