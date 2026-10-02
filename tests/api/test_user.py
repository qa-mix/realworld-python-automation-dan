import pytest


class TestCurrentUser:

    def test_get_current_user_returns_200(self, registered_user, user_api):

        response = user_api.get_current_user(
            registered_user["token"]
        )

        body = response.json()

        assert response.status_code == 200
        assert body["user"]["username"] == registered_user["username"]
        assert body["user"]["token"] == registered_user["token"]

    def test_get_current_user_missing_token_returns_401(self, registered_user, user_api):
        response = user_api.get_current_user(
            token=None
        )

        body = response.json()

        assert response.status_code == 401
        assert body["errors"]["token"] == ["is missing"]

    def test_get_current_user_invalid_token_returns_401(self, user_api):

        invalid_token = "invalid token"

        response = user_api.get_current_user(
            token=invalid_token
        )

        body = response.json()

        assert response.status_code == 401
        assert body["errors"]["token"] == ["is missing"]


class TestUpdateUser:

    @pytest.mark.parametrize(
        "field, value",
        [
            ("email", "new_email@gmail.com"),
            ("username", "new_username"),
            ("password", "12New_pass43"),
            ("bio", "my bio"),
            ("image", "my image")
        ]
    )

    def test_valid_data_returns_200(self, user_api, registered_user, auth_api, field, value):

        token = registered_user["token"]

        payload = {
                field: value
            }

        response = user_api.update_user(token, payload)

        body = response.json()

        assert response.status_code == 200

        if field == "password":

            login_response = auth_api.login_user(
                registered_user["email"],
                value
            )
            assert login_response.status_code == 200
        else:
            assert body["user"][field] == value

            current_user_response = user_api.get_current_user(token)
            current_user_body = current_user_response.json()

            assert current_user_response.status_code == 200
            assert current_user_body["user"][field] == value


    @pytest.mark.parametrize(
        "field, value, expected_error",
        [
            ("email", "", ["email is a string of less than 100 chars"]),
            ("username", 322356, ["Invalid request body"]), # must be a string
            ("password", "7.Chars", ["password must be a string between 8 and 128 chars"]),
            ("bio", 2, ["Invalid request body"]),   # must be a string
            ("image", 3, ["Invalid request body"])  # must be a string
        ]
    )

    def test_update_user_invalid_data_returns_422(
            self,
            user_api,
            registered_user,
            field,
            value,
            expected_error
    ):

        token = registered_user["token"]

        payload = {
            field: value
        }

        update_response = user_api.update_user(token, payload)

        body = update_response.json()

        assert update_response.status_code == 422
        assert body["errors"]["body"] == expected_error

        current_user_response = user_api.get_current_user(token)

        body = current_user_response.json()

        assert current_user_response.status_code == 200

        # if server messages have been recorder
        assert body["user"]["email"] == registered_user["email"]
        assert body["user"]["username"] == registered_user["username"]
        assert body["user"]["bio"] == registered_user["bio"]
        assert body["user"]["image"] == registered_user["image"]


    @pytest.mark.parametrize(
        "email_value, expected_status",
        [
            ("e", 200),
            ("e" * 99, 200),
            ("e" * 100, 200),
            ("e" * 101, 422)
        ]
    )

    def test_email_length_boundary(
            self,
            user_api,
            registered_user,
            email_value,
            expected_status
    ):

        token = registered_user["token"]

        payload = {
                "email": email_value
            }

        response = user_api.update_user(token, payload)

        assert response.status_code == expected_status

