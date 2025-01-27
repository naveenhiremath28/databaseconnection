from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing import Annotated
from app.db_connection.database import get_db
from app.schemas.schema import ResponseSchema, format_response
from app.utils.entities import  DataBaseSchema, DataBaseConnection
from app.exceptions.app_exceptions import APIResponseException
from app.jwt_handler.auth import *
from app.jwt_handler import auth
from app.services.service import *
# from app.main

db_router = APIRouter()

@db_router.get("/", summary="Root Page", response_description="Successfully retrieved the root page")
def root() -> ResponseSchema:
    return format_response("SUCCESS","The API is LIVE..!!!")


@db_router.post("/token/{expiring_time}", summary="Get Token Here", response_description="Successfully got the token.")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], expiring_time: float
    ) -> Token:
    return get_login_access_token(form_data, expiring_time)


@db_router.post("/connection/add-connection", summary="Add New Connection", response_description="Successfully added new connection")
def add_connection(req: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema:
    return get_add_connection(req, db)


@db_router.get("/connection/read-all",summary="Read All Records", response_description="Successfully retrieved all data")
def read_all(db: Session = Depends(get_db)) -> ResponseSchema:
    return get_read_all(db)
    

@db_router.get("/connection/read/{id}", summary="Read Record by ID", response_description="Successfully retrieved the record with the specified ID")
def read_by_id(id: str, db: Session = Depends(get_db)) -> ResponseSchema:
    return get_read_by_id(id, db)
    
    
@db_router.delete("/connection/delete-all", summary="Delete All Records", response_description="Successfully deleted all data")
def delete_all(db:Session = Depends(get_db)):
    return get_delete_all(db)
    
                       
@db_router.delete("/connection/delete/{id}", summary="Delete Record by ID", response_description="Successfully deleted the record with the specified ID")
def delete_by_id(id: str, db: Session = Depends(get_db)) -> ResponseSchema:
     return get_delete_by_id(id, db)


@db_router.put("/connection/update/{id}", summary="Update Record by ID", response_description="Successfully updated the record with the specified ID")
def update_by_id(id: str, fields_to_update: DataBaseSchema, db: Session = Depends(get_db)) -> ResponseSchema:
    return get_update_by_id(id, fields_to_update, db)