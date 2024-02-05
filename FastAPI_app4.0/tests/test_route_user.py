from unittest.mock import patch, AsyncMock
import pytest
from src.services.auth import auth_service
from src.services.auth import auth_service
from unittest.mock import patch

user_data = {"username": "agent007", "email": "agent7@gmail.com", "password": "12345678"}

@pytest.mark.asyncio
async def test_get_me_invalid(client, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = "get_token"
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/me", headers=headers)
        assert response.status_code == 404, response.text

def test_get_me(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/users/me", headers=headers)
        assert response.status_code == 200, response.text

