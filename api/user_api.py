class UserAPI:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_users(self):
        return self.api_client.get("/users")

    def get_user_by_id(self, user_id):
        return self.api_client.get(f"/users/{user_id}")

    def create_user(self, user_data):
        return self.api_client.post("/users", json=user_data)

    def update_user(self, user_id, user_data):
        return self.api_client.put(f"/users/{user_id}", json=user_data)

    def delete_user(self, user_id):
        return self.api_client.delete(f"/users/{user_id}")