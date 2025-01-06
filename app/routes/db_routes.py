from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import ValidationError
from db_connection.database import get_db
from schemas.schema import DataBaseSchema, ResponseSchema, format_response, generate_schema_object
from models.model import DataBaseConnection
from exceptions.app_exceptions import APIResponseException
import uuid

router = APIRouter()

@router.get("/", summary="Root Page", response_description="Successfully retrieved the root page")
def root() -> ResponseSchema:
    return format_response("SUCCESS","The API is LIVE..!!!")

@router.post("/add-connection", summary="Add New Connection", response_description="Successfully added new connection")
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

@router.get("/read-all",summary="Read All Records", response_description="Successfully retrieved all data")
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

@router.get("/read/{id}", summary="Read Record by ID", response_description="Successfully retrieved the record with the specified ID")
def read_by_id(id: int, db: Session = Depends(get_db)) -> ResponseSchema:
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
        raise APIResponseException(500,f"Error while reading record: {str(e)}")
    
@router.delete("/delete-all/", summary="Delete All Records", response_description="Successfully deleted all data")
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
                       
@router.delete("/delete/{id}", summary="Delete Record by ID", response_description="Successfully deleted the record with the specified ID")
def delete_by_id(id: int, db: Session = Depends(get_db)) -> ResponseSchema:
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

@router.put("/update/{id}", summary="Update Record by ID", response_description="Successfully updated the record with the specified ID")
def update_by_id(id: int, fields_to_update: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema:
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
            raise APIResponseException(status_code=404, detail="Database connection not found")
    except Exception as e:
        raise APIResponseException(status_code=500, detail=f"Error while updating record: {str(e)}")