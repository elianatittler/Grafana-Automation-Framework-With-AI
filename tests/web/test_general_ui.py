from extensions.verifications import Verify
from tests.data.web_test_data import ADMIN_USER, ADMIN_PASS

def test_01_header_icons(web_flows):
    """ Verify header icons """
    web_flows.login(ADMIN_USER, ADMIN_PASS)
    web_flows.verify_header_icons()
    Verify.soft_all()  # This will verify all soft assertions