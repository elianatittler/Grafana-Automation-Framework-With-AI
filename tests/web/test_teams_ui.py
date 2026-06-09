from extensions.verifications import Verify
from tests.data.web_test_data import ADMIN_USER, ADMIN_PASS, WELCOME_MESSAGE, TEAM_NAME, TEAM_EMAIL, FIRST_DAY_OF_THE_WEEK, NO_TEAMS

def test_01_grafa_login(web_flows):
    web_flows.login(ADMIN_USER, ADMIN_PASS)
    Verify.text(web_flows.login_page.welcome_text, WELCOME_MESSAGE)


def test_02_create_team(web_flows):
    web_flows.go_to_teams_page()
    web_flows.create_team(TEAM_NAME, TEAM_EMAIL)
    Verify.contain_text(web_flows.create_team_page.page_heading, TEAM_NAME)


def test_03_update_team(web_flows):
    web_flows.go_to_teams_page_updated()
    web_flows.update_team(TEAM_NAME)
    Verify.value(web_flows.update_team_page.starting_day_dropdown, FIRST_DAY_OF_THE_WEEK)


def test_04_delete_team(web_flows):
        web_flows.go_to_teams_page_updated()
        web_flows.delete_team(TEAM_NAME)
        Verify.contain_text(web_flows.delete_team_page.page_content, NO_TEAMS)