import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "dev")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    SERVICENOW_URL: str = os.getenv("SERVICENOW_URL", "")
    SERVICENOW_USER: str = os.getenv("SERVICENOW_USER", "")
    SERVICENOW_PASSWORD: str = os.getenv("SERVICENOW_PASSWORD", "")
    SERVICENOW_ENABLED: bool = os.getenv("SERVICENOW_ENABLED", "false").lower() == "true"


settings = Settings()
