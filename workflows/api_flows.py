import allure
from extensions.api_actions import APIActions

class APIFlows:
    def __init__(self, request_context):
        """
        Initialize APIFlows with APIActions.
        """
        self.api = APIActions(request_context)


    @allure.step("Creating a team with name: {team_name} and email: {team_email}")
    def create_team(self, team_name: str, team_email: str):
        """
        Create a new team with the given name and email.
        """
        payload = {
            "name": team_name,
            "email": team_email
        }
        response = self.api.post("/api/teams/", payload)
        return response.json()
    

    @allure.step("Retrieving team with ID: {team_id}")
    def get_team(self, team_id: int):
        """
        Retrieve a team by its ID.
        """
        response = self.api.get(f"/api/teams/{team_id}/")
        return response.json()
    

    @allure.step("Updating team with ID: {team_id} with name: {new_name} and email: {new_email}")
    def update_team(self, team_id: int, new_name: str, new_email: str):
        """
        Update a team's name and email by its ID.
        """
        payload = {
            "name": new_name,
            "email": new_email
        }
        response = self.api.put(f"/api/teams/{team_id}/", payload)
        return response.json()
    

    @allure.step("Deleting team with ID: {team_id}")
    def delete_team(self, team_id: int):
        """
        Delete a team by its ID.
        """
        response = self.api.delete(f"/api/teams/{team_id}/")
        return response.json()