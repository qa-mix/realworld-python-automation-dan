from api.clients.api_client import ApiClient


class UserApi:
    def __init__(self, client: ApiClient):
        self.client = client

    def get_current_user(self, token):
        return self.client.get(
            "/user",
            headers={
                "Authorization": f"Token {token}",
            }
        )

    def update_user(self, token, payload):
        return self.client.put(
            "/user",
            headers={
                "Authorization": f"Token {token}",
            },
            json={"user": payload}
        )