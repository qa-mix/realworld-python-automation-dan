from api.clients.api_client import ApiClient


class AuthApi:
    def __init__(self, client: ApiClient):
        self.client = client

    def register_user(self, username, email, password):
        payload = {
            "user": {
                "username": username,
                "email": email,
                "password": password,
                }
        }

        return self.client.post(
            "/users",
            json=payload
        )

    def login_user(self, email, password):
        payload = {
            "user": {
                "email": email,
                "password": password,
            }
        }

        return self.client.post(
            "/users/login",
            json=payload
        )