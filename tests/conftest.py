from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.db_connection.database import Base, get_db
import uuid

DATABASE_URL = "sqlite:///./test_connection.db"

engine =  create_engine(DATABASE_URL) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=engine)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
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
        "id": 1,
        "uid": generate_uuid,
        "db_name": "test_database",
        "db_type": "connection",
        "db_host": "localhost",
        "db_port": 3306,
        "db_username": "root",
        "db_password": "root@123",
        "db_description": "This is test_database"
    }