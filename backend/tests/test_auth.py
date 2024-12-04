import pytest
from app.utils.security import hash_password

def test_signup(client, db):
    user_data = {
        "username": "admin",
        "email": "admin@example.com",
        # "phone": "+1234567890",
        "password": "admin.password@1234",
        # "role": "student",
    }
    response = client.post("/auth/users", json=user_data)
    assert response.status_code == 200
    assert "User ID" in response.text

def test_login(client, db):
    login_data = {"email": "admin@example.com", "password": "admin.password@1234"}
    response = client.post("/auth/users/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
