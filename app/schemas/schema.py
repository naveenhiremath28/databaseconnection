from pydantic import BaseModel, ConfigDict
from datetime import datetime

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

    model_config = ConfigDict(from_attributes=True)

def format_output(data):
    if data:
        return {"timestamp": datetime.now(), "Status": "SUCCESS", "message": {"validation": "SUCCESS", "data": data}}
    else:
        return {"timestamp": datetime.now(), "Status": "FAILED", "message": "Invalid Id"}

def invalid_format(e):
        return {"timestamp": datetime.now(), "Status": "SUCCESS", "message": {"validation": "FAILED", "data": e}}
