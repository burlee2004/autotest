class AuthAPI:
    def __init__(self, api_client):
        self.api_client = api_client

    def login(self, username, password):
        payload = {
            "username": username,
            "password": password
        }
        return self.api_client.post("/auth/login", json=payload)

    def logout(self, token=None):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return self.api_client.post("/auth/logout", headers=headers)