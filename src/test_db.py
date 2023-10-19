from fastapi.testclient import TestClient
  # Import your FastAPI app instance
#from myapp.database import get_db  # Import your database session setup
from main import app
from models import UserCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base



# Create a test database engine and session
Base = declarative_base()
test_db_engine = create_engine("sqlite:///test.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
try:
    Base.metadata.create_all(test_db_engine)

except Exception as e:
    print(f"Error creating tables: {e}")

# Create a TestClient for the FastAPI app
client = TestClient(app)

@pytest.fixture(scope="function")
def test_db_session():
    """
    Provide a test database session for each test function.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_create_user_endpoint(test_db_session):
    # Define test user data
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com",
    }

    # Make a POST request to the create_user endpoint
    response = client.post("/register/", json=user_data)

    # Assert that the request was successful (status code 200)
    assert response.status_code == 200

    # Assert that the response contains the expected user data
    response_data = response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]

    # Assert that the user was added to the test database
    db_user = test_db_session.query(UserCreate).filter_by(username=user_data["username"]).first()
    assert db_user is not None
    assert db_user.email == user_data["email"]
