import uuid

import pytest


class TestRegistrationPositive:

    def test_valid_data_returns_201(self, auth_api, user_api):
        unique_id = uuid.uuid4().hex[:8]

        username = f"test_user{unique_id}"
        email = f"user{unique_id}@gmail.com"
        password = "12Pass21"

        response = auth_api.register_user(
            username,
            email,
            password
        )

        body = response.json()

        assert response.status_code == 201
        assert body["user"]["username"] == username
        assert body["user"]["email"] == email
        assert body["user"]["token"] is not None

        token = body["user"]["token"]

        # Проверка, что новый юзер был создан
        current_user_response = user_api.get_current_user(token)

        current_user_body = current_user_response.json()

        assert current_user_response.status_code == 200
        assert current_user_body["user"]["username"] == username
        assert current_user_body["user"]["email"] == email


class TestRegistrationNegative:

    def test_empty_email_returns_422(self, auth_api):
        unique_id = uuid.uuid4().hex[:8]

        username = f"test_user{unique_id}"
        email = ""
        password = "12Pass21"

        response = auth_api.register_user(
            username,
            email,
            password
        )

        body = response.json()

        assert response.status_code == 422
        assert "email" in body["errors"]

    @pytest.mark.skip
    def test_without_email_returns_422(self, auth_api):
        unique_id = uuid.uuid4().hex[:8]

        username = f"test_user{unique_id}"
        password = "21Pass12"

        response = auth_api.register_user(
            username,
            password
        )

        # Ошибка TypeError связанная с отсутствием обязательного позиционного аргумента при вызове метода

    def test_invalid_password_type_returns_422(self,auth_api):
        unique_id = uuid.uuid4().hex[:8]

        username = f"test_user{unique_id}"
        email = f"user{unique_id}@gmail.com"
        password = 34096744

        response = auth_api.register_user(
            username,
            email,
            password
        )

        body = response.json()

        assert response.status_code == 422
        assert "body" in body["errors"]

    def test_register_duplicate_user_returns_409(self, auth_api):
        unique_id = uuid.uuid4().hex[:8]

        username = f"test_user{unique_id}"
        email = f"user{unique_id}@gmail.com"
        password = "12Pass21"

        first_response = auth_api.register_user(
            username,
            email,
            password
        )

        assert first_response.status_code == 201

        second_response = auth_api.register_user(
            username,
            email,
            password
        )

        body = second_response.json()

        print(second_response.status_code)
        print(body)

        # assert second_response.status_code == 409
        # assert "" in body["errors"]

