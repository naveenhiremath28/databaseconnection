from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import Depends
from fastapi.testclient import TestClient
from app.db_connection.database import Base, get_db
import uuid
from app.logs.app_logger import FILE_NAME
import json
import os

DATABASE_URL = "sqlite:///./test_connections.db"

engine =  create_engine(DATABASE_URL) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "a+") as file:
        file.seek(0)
        logs = file.readlines()
        global CURRENT_CURSOR
        CURRENT_CURSOR = file.tell()-2


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def test_client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture()
def generate_uuid():
    return str(uuid.uuid4())
    
@pytest.fixture()
def db_payload(generate_uuid):
    return {
        "id": generate_uuid,
        "db_name": "test_database",
        "db_type": "connection",
        "db_host": "localhost",
        "db_port": 3306,
        "db_username": "root",
        "db_password": "root@123",
        "db_description": "This is test_database"
    }

@pytest.fixture(scope="function")
def get_credentials():
    return {
        "username": "naveen",
        "password": "naveen@123"
    }

@pytest.fixture(scope="function")
def get_invalid_username():
    return {
        "username": "user",
        "password": "naveen@123"
    }

@pytest.fixture(scope="function")
def get_invalid_password():
    return {
        "username": "naveen",
        "password": "user@123"
    }

@pytest.fixture(scope="function")
def get_file():
    return FILE_NAME

@pytest.fixture(scope="function")
def get_cursor():
    return CURRENT_CURSOR