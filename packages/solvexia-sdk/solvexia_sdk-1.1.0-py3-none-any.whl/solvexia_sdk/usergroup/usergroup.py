import requests
from solvexia_sdk import api

class userGroup:
    def __init__(self, usergroup_id):
        self.usergroup_id = usergroup_id
    
    def get_usergroup_list(self):
        response = api.api_get("userGroups")
        api.status_code_check(response, "Error getting user group list")
        return response.json()
    
    def get_usergroup(self):
        response = api.api_get(f"userGroups/{self.usergroup_id}")
        api.status_code_check(response, f"Error getting user group with usergroup_id {self.usergroup_id}")
        return response.json()
    
    def get_members(self):
        response = api.api_get(f"userGroups/{self.usergroup_id}/members")
        api.status_code_check(response, f"Error getting user group members with usergroup_id {self.usergroup_id}")
        return response.json()

    def get_permissions(self):
        response = api.api_get(f"userGroups/{self.usergroup_id}/permissions")
        api.status_code_check(response, f"Error getting user group permissions with usergroup_id {self.usergroup_id}")
        return response.json()

    def update_permission(self, resource_id, role):
        payload = {
            'role': role
        }
        response = api.api_post(f"userGroups/{self.usergroup_id}/permissions/{resource_id}", payload)
        api.status_code_check(response, f"Error updating user group permissions with usergroup_id {self.usergroup_id} for resource_id {resource_id}")
        return response.json()
    
    def delete_permission(self, resource_id):
        response = api.api_delete(f"userGroups/{self.usergroup_id}/permissions/{resource_id}")
        api.status_code_check(response, f"Error deleting user group permissions with usergroup_id {self.usergroup_id} for resource_id {resource_id}")
