from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import ValidationError
from databaseconnection.database import get_db
from schemas.schema import format_output, DataBaseSchema, invalid_format
from models.model import DataBaseConnection
import uuid
from datetime import datetime

app = FastAPI()

@app.get("/")
def homePage():
    return {"message": "Good Morning...!"}

@app.post("/addConnection")
def add_data(req: DataBaseSchema, db: Session = Depends(get_db)): 
    data = DataBaseConnection(uid=str(uuid.uuid4()), db_name=req.db_name, db_type=req.db_type, 
                              db_host=req.db_host, db_port=req.db_port, db_username=req.db_username, 
                              db_password=req.db_password, db_description=req.db_description)
    db.add(data)
    db.commit()
    db.refresh(data)
    return format_output(data)

@app.get("/readAll")
def getall_data(db: Session = Depends(get_db)):
    try:
        data = db.query(DataBaseConnection).all()
        vData =  [DataBaseSchema.model_validate(info) for info in data]
        # print(type(vData[0])) // DataBaseSchema
        return format_output(vData)
    except ValidationError as e:
        return invalid_format(e)

@app.get("/read/{id}")
def get_data(id: int, db: Session = Depends(get_db)):
    try:
        data = db.query(DataBaseConnection).filter(DataBaseConnection.id == id).first()
        vData = DataBaseSchema.model_validate(data)
        return format_output(vData)
    except ValidationError as e:
        return invalid_format(e)

@app.delete("/delete/{id}")
def delete_data(id: int, db: Session = Depends(get_db)):
    data = db.query(DataBaseConnection).filter(DataBaseConnection.id == id).first()
    try:
        if data:
            vData = DataBaseSchema.model_validate(data)
            dataDeleted = vData
            db.delete(data)
            db.commit()
        return format_output(dataDeleted)
    except ValidationError as e:
        invalid_format(e)

@app.put("/update/{id}")
def update_data(id: int, dataToUpdate: DataBaseSchema, db: Session = Depends(get_db)):
    data = db.query(DataBaseConnection).filter(DataBaseConnection.id == id).first()
    if data:
        data.db_name = dataToUpdate.db_name
        data.db_host = dataToUpdate.db_host
        data.db_type = dataToUpdate.db_type
        data.db_port = dataToUpdate.db_port
        data.db_username = dataToUpdate.db_username
        data.db_password = dataToUpdate.db_password
        data.db_description = dataToUpdate.db_description
        db.commit()
        db.refresh(data)
    return format_output(data)
