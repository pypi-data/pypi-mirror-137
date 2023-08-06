import requests
from solvexia_sdk import api

class user:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_user_list(self):
        response = api.api_get("users")
        api.status_code_check(response, "Error getting user list")
        return response.json()
    
    def get_user(self):
        response = api.api_get(f"users/{self.user_id}")
        api.status_code_check(response, f"Error getting user with user_id {self.user_id}")
        return response.json()

    def disable_user(self):
        payload = {
            'accountActive': False
        }
        response = api.api_post(f"users/{self.user_id}", payload)
        api.status_code_check(response, f"Error disabling user with user_id {self.user_id}")
        return response.json()

    def get_permissions(self):
        response = api.api_get(f"users/{self.user_id}/permissions")
        api.status_code_check(response, f"Error getting user's permissions with user_id {self.user_id}")
        return response.json()

    def update_permission(self, resource_id, role):
        payload = {
            'role': role
        }
        response = api.api_post(f"users/{self.user_id}/permissions/{resource_id}", payload)
        api.status_code_check(response, f"Error updating user's permissions with user_id {self.user_id} for resource_id {resource_id}")
        return response.json()
    
    def delete_permission(self, resource_id):
        response = api.api_delete(f"users/{self.user_id}/permissions/{resource_id}")
        api.status_code_check(response, f"Error deleting user's permissions with user_id {self.user_id} for resource_id {resource_id}")
