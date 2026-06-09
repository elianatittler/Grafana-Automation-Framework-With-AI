import os
import sys

# מוצאים את הנתיב האבסולוטי של תיקיית API_Automation ומכניסים אותה לראש רשימת החיפוש
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# רק עכשיו מגיעים ה-Imports הרגילים של הפרויקט:
import pytest
from utils.common_ops import load_config
from utils.fixture_helpers import create_request_context
from tests.web.ai_handler import AIErrorHandler  # נתיב ישיר ומלא

# מכניסים את נתיב הפרויקט כדי שנוכל לייבא מה-utils
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# טעינת הגדרות (כאן נמצא ה-API KEY וה-BASE URL)
CONFIG = load_config()

@pytest.fixture(scope="session")
def request_context():
    """Fixture to create and dispose of an API request context for Grafana."""
    # משתמשים בפונקציית העזר שיצרת כדי ליצור חיבור API
    request_context, playwright = create_request_context(
        CONFIG["GRAFANA_API_KEY"],
        CONFIG["BASE_URL_API"]
    )
    yield request_context
    # סגירת החיבור בסיום הטסטים
    request_context.dispose()
    playwright.stop()

# --- רכיב ה-AI לתפיסת שגיאות וניתוח אוטומטי ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # מפעיל את ה-Hook הסטנדרטי של pytest כדי לקבל את תוצאת הטסט
    outcome = yield
    report = outcome.get_result()
    
    # בודק אם הטסט נכשל בשלב ה-setup או ה-call (ההרצה עצמה)
    if report.when in ["setup", "call"] and report.failed:
        error_msg = str(report.longrepr)
        
        # הפעלת מנגנון ה-AI
        ai = AIErrorHandler()
        ai_analysis = ai.analyze_error(item.name, error_msg)
        
        # הדפסת הניתוח ישירות לתוך הטרמינל בצורה בולטת למראיינים
        print(f"\n{'-'*60}\n🤖 AI ERROR ANALYSIS FOR {item.name}:\n{ai_analysis}\n{'-'*60}")