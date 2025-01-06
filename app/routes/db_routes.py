from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import ValidationError
from db_connection.database import get_db
from schemas.schema import DataBaseSchema, ResponseSchema, format_response, generate_schema_object
from models.model import DataBaseConnection
from exceptions.app_exceptions import APIResponseException
import uuid
from datetime import datetime

router = APIRouter()

@router.get("/")
def homePage() -> ResponseSchema:
    return format_response("SUCCESS","The API is LIVE..!!!")

@router.post("/add-connection")
def add_connection(req: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema: 
    try:
        new_entry = DataBaseConnection(
            uid=str(uuid.uuid4()),
            db_name=req.db_name,
            db_type=req.db_type,
            db_host=req.db_host,
            db_port=req.db_port,
            db_username=req.db_username,
            db_password=req.db_password,
            db_description=req.db_description
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        data = generate_schema_object(new_entry)
        return format_response("SUCCESS", data)
    except Exception as e:
        raise APIResponseException(500,f"Error while adding connection: {str(e)}")

@router.get("/read-all")
def read_all(db: Session = Depends(get_db)) -> ResponseSchema:
    try:
        database_record = db.query(DataBaseConnection).all()
        if database_record:
            data_list = [generate_schema_object(info) for info in database_record]
            return format_response("SUCCESS",data_list)
        else:
            raise APIResponseException(404,"No database connection found")
    except ValidationError as e:
        raise APIResponseException(500,f"Error while reading records: {str(e)}")

@router.get("/read/{id}")
def read_by_id(id: int, db: Session = Depends(get_db)) -> ResponseSchema:
    try:
        database_record = db.query(DataBaseConnection).filter(DataBaseConnection.id == id).first()
        if database_record:
            data = generate_schema_object(database_record)
            return format_response("SUCCESS", data)
        else:
            raise APIResponseException(404,"No database connection found")
    except ValidationError as e:
        raise APIResponseException(500,f"Error while reading record: {str(e)}")
    
@router.delete("/delete-all/")
def delete_all(db:Session = Depends(get_db)):
    try:
        database_records = db.query(DataBaseConnection).all()
        if database_records:
            for data in database_records:
                db.delete(data)
                db.commit()
            return format_response("SUCCESS","All records deleted successfully")
        else:
            raise APIResponseException(404, "Not database connection found")
    except ValidationError as e:
        raise APIResponseException(500,f"Error while reading record: {str(e)}")
                       
@router.delete("/delete/{id}")
def delete_by_id(id: int, db: Session = Depends(get_db)) -> ResponseSchema:
    try:
        database_record = db.query(DataBaseConnection).filter(DataBaseConnection.id == id).first()
        if database_record:
            db.delete(database_record)
            db.commit()
            return format_response("SUCCESS",f"Database connection deleted successfully with Id: {id}")
        else:
            raise APIResponseException(404,"No database connection found")
    except ValidationError as e:
        raise APIResponseException(500,f"Error while deleting record: {str(e)}")

@router.put("/update/{id}")
def update_by_id(id: int, fields_to_update: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema:
    try:
        database_record = db.query(DataBaseConnection).filter(DataBaseConnection.id == id).first()
        if database_record:
            database_record.db_name = fields_to_update.db_name
            database_record.db_host = fields_to_update.db_host
            database_record.db_type = fields_to_update.db_type
            database_record.db_port = fields_to_update.db_port
            database_record.db_username = fields_to_update.db_username
            database_record.db_password = fields_to_update.db_password
            database_record.db_description = fields_to_update.db_description
            db.commit()
            db.refresh(database_record)
            data = generate_schema_object(database_record)
            return format_response("SUCCESS", data)
        else:
            raise APIResponseException(status_code=404, detail="Database connection not found")
    except Exception as e:
        raise APIResponseException(status_code=500, detail=f"Error while updating record: {str(e)}")
