import logging
import requests
from app.core.config import settings
from app.models.alert import Alert

logger = logging.getLogger(__name__)


class ServiceNowConnector:
    def __init__(self) -> None:
        self.url = settings.SERVICENOW_URL
        self.auth = (settings.SERVICENOW_USER, settings.SERVICENOW_PASSWORD)

    def create_incident(self, alert: Alert) -> dict:
        if not settings.SERVICENOW_ENABLED:
            logger.info("servicenow disabled | returning mocked response")
            return {
                "status": "mocked",
                "message": "ServiceNow integration disabled",
                "payload": {
                    "short_description": f"[{alert.severity.upper()}] {alert.name}",
                    "description": alert.details,
                    "category": alert.source,
                },
            }

        payload = {
            "short_description": f"[{alert.severity.upper()}] {alert.name}",
            "description": alert.details,
            "category": alert.source,
            "impact": "1" if alert.severity.lower() == "critical" else "2",
            "urgency": "1" if alert.severity.lower() == "critical" else "2",
        }

        logger.info("creating incident in servicenow | alert=%s", alert.name)

        response = requests.post(
            self.url,
            auth=self.auth,
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
