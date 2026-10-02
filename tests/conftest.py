import uuid

import pytest

from api.clients.api_client import ApiClient
from api.clients.auth_api import AuthApi
from api.clients.user_api import UserApi


@pytest.fixture
def api_client():
    client = ApiClient()
    yield client
    client.close()

@pytest.fixture
def auth_api(api_client):
    return AuthApi(api_client)

@pytest.fixture
def registered_user(auth_api):
    unique_id = uuid.uuid4().hex[:8]

    username = f"test_user{unique_id}"
    email = f"user{unique_id}@gmail.com"
    password = "12Pass21"

    response = auth_api.register_user(
        username,
        email,
        password
    )

    assert response.status_code == 201, response.text

    body = response.json()

    return {
        "username": username,
        "email": email,
        "password": password,
        "token": body["user"]["token"],
        "bio": body["user"]["bio"],
        "image": body["user"]["image"]
    }

@pytest.fixture
def user_api(api_client):
    return UserApi(api_client)
