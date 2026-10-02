class TestLoginPositive:

    def test_valid_data_returns_200(self, auth_api, registered_user):
        response = auth_api.login_user(
            registered_user["email"],
            registered_user["password"]
        )

        body = response.json()

        assert response.status_code == 200
        assert body["user"]["email"] == registered_user["email"]
        assert body["user"]["username"] == registered_user["username"]
        assert body["user"]["token"] is not None


class TestLoginNegative:

    def test_invalid_password_returns_401(self, auth_api, registered_user):
        response = auth_api.login_user(
            registered_user["email"],
            "123"
        )

        body = response.json()

        assert response.status_code == 401
        assert "credentials" in body["errors"]

    def test_invalid_email_returns_401(self, auth_api, registered_user):
        response = auth_api.login_user(
            "email",
            registered_user["password"]
        )

        body = response.json()

        assert response.status_code == 401
        assert "credentials" in body["errors"]