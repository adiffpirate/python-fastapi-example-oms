import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_success():
    """Test creating a new user"""
    response = client.post("/users/register", json={
        "username": "integrationtestuser",
        "password": "testpassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "integrationtestuser"
    assert "id" in data

def test_create_duplicate_user_fails():
    """Test creating a user that already exists"""
    # First create the user
    client.post("/users/register", json={
        "username": "duplicateuser",
        "password": "testpassword123"
    })

    # Try to create the same user again
    response = client.post("/users/register", json={
        "username": "duplicateuser",
        "password": "testpassword123"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"
