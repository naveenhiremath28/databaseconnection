from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from typing import Annotated
import logging
import sys
from app.db_connection.database import get_db 
from app.schemas.schema import DataBaseSchema, DataBaseConnection, ResponseSchema
from app.schemas.schema import generate_schema_object, format_response
from app.exceptions.app_exceptions import APIResponseException
from app.jwt_handler.auth import *
from app.jwt_handler import auth


def get_login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], expiring_time: float) -> Token:
    """
    Specify the time limit in minutes.
    """
    user = authenticate_user(credentials, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(
        data={"sub": user.username}, expiry=expiring_time
    )
    return Token(access_token=access_token, token_type="bearer")


def get_add_connection(req: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema:
    """
    Add a new database connection configuration with the following details:

    - **db_name**: The name of the database must be specified.
    - **db_type**: Specify the type of database (e.g., MySQL, PostgreSQL, MongoDB, etc.).
    - **db_port**: Provide the port number required for the specified database.
    - **db_host**: Specify the host address where the database is located.
    - **db_username**: The database username must be specified.
    - **db_password**: Specify the password associated with the database user.
    - **db_description**: Include a short note about the database.
    """
    try:
        new_entry = DataBaseConnection(
            id = req.id,
            db_name=req.db_name,
            db_type=req.db_type,
            db_host=req.db_host,
            db_port=req.db_port,
            db_username=req.db_username,
            db_password=req.db_password,
            db_description=req.db_description
        )
        # new_entry = DataBaseConnection(**req.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        data = generate_schema_object(new_entry)
        return format_response("SUCCESS", data)
    except ValidationError as e:
        raise APIResponseException(500,f"Error while adding connection: {str(e)}")
    

def get_read_all(db: Session = Depends(get_db)) -> ResponseSchema:
    try:
        database_record = db.query(DataBaseConnection).all()
        if database_record:
            data_list = [generate_schema_object(info) for info in database_record]
            return format_response("SUCCESS",data_list)
        else:
            raise APIResponseException(404,"No database connection found")
    except ValidationError as e:
        raise APIResponseException(500,f"Error while reading records: {str(e)}")


def get_read_by_id(id: str, db: Session = Depends(get_db)) -> ResponseSchema:
    """
    Specify a valid **ID** to retrieve the data.
    """
    try:
        database_record = db.query(DataBaseConnection).filter(DataBaseConnection.id == id).first()
        if database_record:
            data = generate_schema_object(database_record)
            return format_response("SUCCESS", data)
        else:
            raise APIResponseException(404,"No database connection found")
    except ValidationError as e:
        raise HTTPException(500,f"Error while reading record: {str(e)}")
    

def get_delete_all(db:Session = Depends(get_db)) -> ResponseSchema:
    try:
        database_records = db.query(DataBaseConnection).all()
        if database_records:
            db.query(DataBaseConnection).delete()
            db.commit()
            return format_response("SUCCESS","All records deleted successfully.")
        else:
            raise APIResponseException(404, "No database connection found")
    except ValidationError as e:
        raise APIResponseException(500,f"Error while reading record: {str(e)}")

def get_delete_by_id(id: str, db: Session = Depends(get_db)) -> ResponseSchema:
    """
    Specify valid **ID** to delete the data.
    """
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
    
def get_update_by_id(id: str, fields_to_update: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema:
    """
    Make the necessary updates for the specified **ID**.
    """
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
            raise APIResponseException(status_code=400, detail="Database connection not found")
    except Exception as e:
        raise APIResponseException(status_code=500, detail=f"Error while updating record: {str(e)}")