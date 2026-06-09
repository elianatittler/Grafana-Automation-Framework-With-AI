import pytest
import allure
from workflows.api_flows import APIFlows
from extensions.verifications_api import VerifyAPI

@pytest.mark.usefixtures("request_context")
class TestGrafanaTeam:
    """Test class to manage team creation, update, and deletion."""

    team_id = None # Class variable to store team ID
    name = "FinalProjectTeam"
    email = "FinalProject_team@test.com"
    new_name = "FinalProjectTeamUpdated"
    new_email = "FinalProject_teamUpdated@test.com"

    @allure.title("Test 01: Create Team")
    def test_01_create_team(self, request_context):
        """Test case for creating a new team and storing its ID."""
        api_flows = APIFlows(request_context)        
        response_data = api_flows.create_team(self.name, self.email)
        VerifyAPI.json_key_exists(response_data, "teamId")
        TestGrafanaTeam.team_id = response_data["teamId"]

    @allure.title("Test 02: Get Team Details")
    def test_02_get_team_details(self, request_context):
        """Test case for retrieving team details and verifying they are correct."""
        api_flows = APIFlows(request_context)
        response = api_flows.api.get(f"/api/teams/{TestGrafanaTeam.team_id}")

        VerifyAPI.status_code(response, 200)
        response_data = response.json()
        VerifyAPI.json_value_equals(response_data, "id", TestGrafanaTeam.team_id)
        VerifyAPI.json_value_equals(response_data, "name", self.name)
        VerifyAPI.json_value_equals(response_data, "email", self.email)
        
        # השילוב של ה-AI Response Validator החדש שלנו:
        VerifyAPI.ai_validate_response(response_data, "Grafana Get Team Details Endpoint")

    @allure.title("Test 03: Update Team")
    def test_03_update_team(self, request_context):
        """Test case to update the existing team."""
        api_flows = APIFlows(request_context)
        response = api_flows.api.put(f"/api/teams/{TestGrafanaTeam.team_id}", 
                                   {"name": self.new_name, "email": self.new_email})
        
        VerifyAPI.status_code(response, 200)
        response_data = response.json() 
        VerifyAPI.json_value_equals(response_data, "message", "Team updated")

    @allure.title("Test 04: Delete Team")
    def test_04_delete_team(self, request_context):
        """Test case to delete the team."""
        api_flows = APIFlows(request_context)
        response = api_flows.api.delete(f"/api/teams/{TestGrafanaTeam.team_id}")

        VerifyAPI.status_code(response, 200)
        response_data = response.json()
        VerifyAPI.json_value_equals(response_data, "message", "Team deleted")
       
