import os
class Settings:
    app_name = "LegalEase AI"
    app_version = "1.0.0"
    cors_origins = ["http://localhost:3000"]
    gemini_model = "gemini-2.5-flash"
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    mock_mode = True

def get_settings():
    return Settings()