from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import ValidationError
from app.db_connection.database import get_db
from app.schemas.schema import ResponseSchema, format_response, generate_schema_object
from app.utils.entities import  DataBaseSchema, DataBaseConnection
from app.exceptions.app_exceptions import APIResponseException
from app.jwt_handler.auth import *
from app.jwt_handler import auth
from typing import Annotated

db_router = APIRouter()

@db_router.get("/", summary="Root Page", response_description="Successfully retrieved the root page")
def root() -> ResponseSchema:
    return format_response("SUCCESS","The API is LIVE..!!!")


@db_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> Token:
    user = authenticate_user(credentials, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(
        data={"sub": user.username}, expiry=TOKEN_EXP
    )
    auth.TOKEN = access_token
    return Token(access_token=access_token, token_type="bearer")


@db_router.post("/connection/add-connection", summary="Add New Connection", response_description="Successfully added new connection")
def add_connection(req: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema:
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
    

@db_router.get("/connection/read-all",summary="Read All Records", response_description="Successfully retrieved all data")
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
    

@db_router.get("/connection/read/{id}", summary="Read Record by ID", response_description="Successfully retrieved the record with the specified ID")
def read_by_id(id: str, db: Session = Depends(get_db)) -> ResponseSchema:
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
    
    
@db_router.delete("/connection/delete-all", summary="Delete All Records", response_description="Successfully deleted all data")
def delete_all(db:Session = Depends(get_db)):
    try:
        database_records = db.query(DataBaseConnection).all()
        if database_records:
            db.query(DataBaseConnection).delete()
            db.commit()
            return format_response("SUCCESS","All records deleted successfully")
        else:
            raise APIResponseException(404, "No database connection found")
    except ValidationError as e:
        raise APIResponseException(500,f"Error while reading record: {str(e)}")
    
                       
@db_router.delete("/connection/delete/{id}", summary="Delete Record by ID", response_description="Successfully deleted the record with the specified ID")
def delete_by_id(id: str, db: Session = Depends(get_db)) -> ResponseSchema:
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
    

@db_router.put("/connection/update/{id}", summary="Update Record by ID", response_description="Successfully updated the record with the specified ID")
def update_by_id(id: str, fields_to_update: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema:
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