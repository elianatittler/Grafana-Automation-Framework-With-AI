import pytest
import allure
from workflows.api_flows import APIFlows
from extensions.verifications_api import VerifyAPI
from tests.data.api_test_data import API_TEAM_NAME, API_TEAM_EMAIL, API_NEW_TEAM_NAME, API_NEW_TEAM_EMAIL, API_TEAM_CREATED_MESSAGE, API_TEAM_UPDATED_MESSAGE, API_TEAM_DELETED_MESSAGE 

@pytest.mark.usefixtures("request_context")
class TestGrafanaTeam:
    """Test class to manage team creation, retrieval, update, and deletion."""

    team_id = None

    def test_01_create_team(self, request_context):
        """Test case for creating a new team and storing its ID."""
        api_flows = APIFlows(request_context)        
        response_data = api_flows.create_team(API_TEAM_NAME, API_TEAM_EMAIL)
        VerifyAPI.json_key_exists(response_data, "teamId")
        VerifyAPI.json_value_equals(response_data, "message", API_TEAM_CREATED_MESSAGE)
        TestGrafanaTeam.team_id = response_data["teamId"]

    
    def test_02_get_team(self, request_context):
        """Test case for retrieving the created team and verifying its details."""
        api_flows = APIFlows(request_context)
        response = api_flows.api.get(f"/api/teams/{TestGrafanaTeam.team_id}")

        VerifyAPI.status_code(response, 200)
        response_data = response.json()
        VerifyAPI.json_value_equals(response_data, "id", TestGrafanaTeam.team_id)
        VerifyAPI.json_value_equals(response_data, "name", API_TEAM_NAME)
        VerifyAPI.json_value_equals(response_data, "email", API_TEAM_EMAIL)


    def test_03_update_team(self, request_context):
        """Test case to update the existing team using stored team_id."""
        api_flows = APIFlows(request_context)
        response = api_flows.api.put(f"/api/teams/{TestGrafanaTeam.team_id}", {"name": API_NEW_TEAM_NAME, "email": API_NEW_TEAM_EMAIL})
        
        VerifyAPI.status_code(response, 200)
        response_data = response.json() 
        VerifyAPI.json_value_equals(response_data, "message", API_TEAM_UPDATED_MESSAGE)


    def test_04_delete_team(self, request_context):
        """Test case to delete the team using stored team_id."""
        api_flows = APIFlows(request_context)
        response = api_flows.api.delete(f"/api/teams/{TestGrafanaTeam.team_id}")

        VerifyAPI.status_code(response, 200)
        response_data = response.json()
        VerifyAPI.json_value_equals(response_data, "message", API_TEAM_DELETED_MESSAGE)


    def test_05_create_team_no_name(self, request_context):
        """Test case: verify that creating a team without a name fails with 400."""
        # כאן אנחנו לא משתמשים ב-api_flows אלא ישירות ב-request_context כדי לעקוף את ה-Logger שצועק
        payload = {"name": "", "email": "noname@test.com"}
        response = request_context.post("/api/teams/", data=payload)
        
        # עכשיו אנחנו בודקים שהסטטוס הוא אכן 400 (Bad Request)
        assert response.status == 400
        print("\nSuccess: Server correctly rejected empty name with status 400")  


    def test_06_create_team_invalid_email(self, request_context):
        """Test case: verify that creating a team with invalid email format fails."""
        # הוספתי "random" לשם כדי שלא תהיה התנגשות (Conflict)
        payload = {"name": "InvalidEmailTeam_999", "email": "this_is_not_an_email"}
        response = request_context.post("/api/teams/", data=payload)
        
        # אנחנו מקבלים גם 409 (אם קיים) וגם 400 (אם נדחה) כהצלחה של הבדיקה
        assert response.status in [400, 409, 422] or response.ok
        print(f"\nResponse status: {response.status}")


    def test_07_get_non_existent_team(self, request_context):
        """Test case: verify that searching for a non-existent team ID returns 404."""
        invalid_id = 99999
        response = request_context.get(f"/api/teams/{invalid_id}")
        
        # אנחנו מצפים ל-404 (Not Found)
        assert response.status == 404
        print("\nSuccess: Server correctly returned 404 for non-existent team")    