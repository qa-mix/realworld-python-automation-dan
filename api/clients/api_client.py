import httpx

from config.settings import BASE_API_URL


class ApiClient:
    def __init__(self):
        self.client = httpx.Client(
            base_url=BASE_API_URL,
            timeout=10.0
        )

    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.client.get(endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.client.post(endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> httpx.Response:
        return self.client.put(endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.client.delete(endpoint, **kwargs)

    def close(self):
        self.client.close()
