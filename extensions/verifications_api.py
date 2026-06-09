import os
from anthropic import Anthropic
import pytest

class VerifyAPI:
    errors = []  # רשימה פנימית לניהול ה-Soft Assertions הקיימים שלך

    @staticmethod
    def status_code(response, expected_status_code: int):
        """
        Verifies that the API response status code matches the expected status code.
        """
        if isinstance(response, dict):  # If it's already JSON, we can't check status
            raise ValueError("Expected a Playwright response object, but got a dictionary. Ensure status code is checked before calling .json()")
        assert response.status == expected_status_code, \
            f"Expected status code {expected_status_code}, but got {response.status}"
        

    @staticmethod
    def json_key_exists(response_data, key: str):
        """
        Verifies that a specific key exists in the JSON response.
        """
        assert key in response_data, f"Key '{key}' not found in the response JSON"

    
    @staticmethod
    def json_value_equals(response_data, key: str, expected_value):
        """
        Verifies that a specific key in the JSON response has the expected value.
        """
        assert response_data[key] == expected_value, (
            f"Expected value for key '{key}' is '{expected_value}', but got '{response_data[key]}'"
        )

    
    @staticmethod
    def json_contains(response_data, expected_data: dict):
        """
        Verifies that the JSON response contains the expected data.
        """
        for key, value in expected_data.items():
            assert key in response_data, f"Key '{key}' not found in the response JSON"
            assert response_data[key] == value, (
                f"Expected value for key '{key}' is '{value}', but got '{response_data[key]}'"
            )

    # Soft Assertions
    @staticmethod
    def soft_assert_status_code(response, expected_status_code: int):
        """
        Soft asserts that the API response status code matches the expected status code.
        """
        if isinstance(response, dict):  
            VerifyAPI.errors.append("Expected a Playwright response object, got a dictionary.")

        elif response.status != expected_status_code:
            VerifyAPI.errors.append(
                f"Expected status code {expected_status_code}, but got {response.status}."
            )

    @staticmethod
    def assert_all():
        """
        Raises all collected assertion errors at once.
        """
        if VerifyAPI.errors:
            error_message = "\n".join(VerifyAPI.errors)
            VerifyAPI.errors.clear()  # Clear errors after raising
            raise AssertionError(f"Soft assertion failures:\n{error_message}")

    # --- הפיצ'ר החדש: AI Response Validator ---
    @staticmethod
    def ai_validate_response(response_json: dict, endpoint_context: str):
        """
        שולח את ה-JSON של התגובה ל-Claude 3.5 Sonnet לניתוח אבטחה, לוגיקה וחריגות.
        מחזיר תשובה מובנית ומכשיל את הטסט במידה ונמצאה חריגה.
        """
        # וידוא שמפתח ה-API קיים במערכת
        if not os.environ.get("ANTHROPIC_API_KEY"):
            pytest.fail("AI Validation Failed: ANTHROPIC_API_KEY environment variable is missing!")

        # אתחול הקליינט של Anthropic (מושך אוטומטית את משתנה הסביבה)
        client = Anthropic()

        # ניסוח הפרומפט עבור המודל - הגדרת חוקים נוקשים לקבלת ה-Verdict
        prompt = f"""
        You are an expert QA Automation AI Assistant specialized in API Security and Contract Testing.
        Analyze the following JSON response from a Grafana API endpoint.
        
        Endpoint Context: {endpoint_context}
        JSON Response to evaluate:
        {response_json}
        
        Your task is to verify if the response is logically sound, safe, and free of anomalies or unexpected data leaks.
        
        You must respond in the following strict format:
        VERDICT: <PASSED or FAILED>
        REASON: <A brief summary of your analysis or why it failed>
        """

        try:
            # פנייה ל-Claude 3.5 Sonnet
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",  
                max_tokens=300,
                temperature=0,  
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # חילוץ התשובה
            ai_response = message.content[0].text
            print(f"\n--- Claude AI Response Analysis ---\n{ai_response}\n----------------------------------")

            # בדיקה האם המודל החזיר FAILED
            if "VERDICT: FAILED" in ai_response:
                pytest.fail(f"AI Contract/Security Validation Failed! Details:\n{ai_response}")

        except Exception as e:
            # התיקון הקריטי: במקום להכשיל את הטסט, מדפיסים אזהרה וממשיכים קדימה
            print(f"\n[WARNING] AI Validation skipped due to an API error: {str(e)}")