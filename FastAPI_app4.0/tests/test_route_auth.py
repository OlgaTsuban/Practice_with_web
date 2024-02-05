from unittest.mock import Mock
import pytest
import asyncio
from sqlalchemy import select
from src.services.auth import auth_service
from src.entity.models import User
from tests.conftest import TestingSessionLocal
from src.conf import messages

user_data = {"username": "agent007", "email": "agent007@gmail.com", "password": "12345678"}


def test_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data
    assert "avatar" in data

def test_repeat_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == messages.ACCOUNT_EXIST

def test_not_confirmed_login(client):
    response = client.post("api/auth/login",
                           data={"username": user_data.get("email"), "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.EMAIL_NOT_CONFIRMED

@pytest.mark.asyncio
async def test_login(client):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).where(User.email == user_data.get("email")))
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.confirmed = True
            await session.commit()

    response = client.post("api/auth/login",
                           data={"username": user_data.get("email"), "password": user_data.get("password")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data

def test_wrong_password_login(client):
    response = client.post("api/auth/login",
                           data={"username": user_data.get("email"), "password": "password"})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.INVALID_PASSWORD

def test_wrong_email_login(client):
    response = client.post("api/auth/login",
                           data={"username": "email", "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.INVALID_EMAIL

@pytest.mark.asyncio
async def test_refresh_token(client):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).filter(User.email == user_data.get("email")))
        current_user = current_user.scalar_one_or_none()
        headers = {"Authorization": f"Bearer {current_user.refresh_token}"}
    response = client.get("api/auth/refresh_token", headers=headers)

    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" is not None
    assert "refresh_token" is not None
    assert "token_type" in data

def test_refresh_token_mistake(client):
    invalid_refresh_token = asyncio.run(
            auth_service.create_refresh_token(data={"sub": user_data.get("email")}, expires_delta=100)
        )
    headers = {"Authorization": f"Bearer {invalid_refresh_token}"}
    response = client.get("/api/auth/refresh_token", headers=headers)
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.INVALID_REF_TOKEN


@pytest.mark.asyncio
async def test_confirmed_email_successfully(client):
        async with TestingSessionLocal() as session:
            current_user = await session.execute(select(User).filter(User.email == user_data.get("email")))
            current_user = current_user.scalar_one_or_none()
            current_user.confirmed = False
            await session.commit()
        email_token = (
            auth_service.create_email_token(data={"sub": user_data.get("email")})
        )
        response = client.get("api/auth/confirmed_email/{token}".format(token=email_token))
        assert response.status_code == 200
        #assert response.json()['message'] == detail

def test_confirmed_email_invalid_email(client):
        invalid_email_token = auth_service.create_email_token(data={"sub": "invalid@test.com"})
        response = client.get("api/auth/confirmed_email/{token}".format(token=invalid_email_token))
        assert response.status_code == 400
        assert response.json()['detail'] == messages.VERIFICATION_ERROR

@pytest.mark.asyncio
async def test_already_confirmed_email(client):
     async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).filter(User.email == user_data.get("email")))
        current_user = current_user.scalar_one_or_none()
        current_user.confirmed = True
        await session.commit()
        email_token = (
            auth_service.create_email_token(data={"sub": current_user.email})
        )
        response = client.get("api/auth/confirmed_email/{token}".format(token=email_token))
        assert response.status_code == 200, response.text
        assert response.json()['message'] == messages.ALREADY_CONFIRMED

@pytest.mark.asyncio
async def test_request_email(client, monkeypatch):
     async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).filter(User.email == user_data.get("email")))
        current_user = current_user.scalar_one_or_none()
        current_user.confirmed = False
        await session.commit()
     mock_send_email = Mock()
     monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    
     response = client.post("api/auth/request_email", json={"email": current_user.email})
     assert response.status_code == 200, response.text
     assert response.json()['message'] == messages.EMAIL_SENT

def test_forget_password(client):
    response = client.post("api/auth/forget-password", json={"email": user_data.get("email")})
    assert response.status_code == 200, response.text
    assert response.json()['message'] ==  "Email has been sent"

@pytest.mark.asyncio
async def test_reset_password_post(client):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).filter(User.email == user_data.get("email")))
        current_user = current_user.scalar_one_or_none()
        current_user.confirmed = True
        await session.commit()
    email_token = auth_service.create_email_token(data={"sub": user_data.get("email")})   
    new_password = auth_service.get_password_hash(password="new_password")
    response = client.post(
        "api/auth/reset_password/{token}?new_password={new_password}".format(
            token=email_token,
            new_password=new_password
        )
    )
    assert response.status_code == 200, response.text
    assert response.json()['message'] ==  "Password changed"

@pytest.mark.asyncio
async def test_reset_password_get(client):
    email_token = auth_service.create_email_token(data={"sub": user_data.get("email")})   
    response = client.get("api/auth/reset_password/{token}".format(token=email_token))
    assert response.status_code == 200, response.text
    assert "Token" in response.json()
    assert email_token in response.json()["Token"]

    