import logging
import os
import requests
from app.models.alert import Alert

logger = logging.getLogger(__name__)


class JiraConnector:
    def __init__(self) -> None:
        self.base_url = os.getenv("JIRA_URL", "")
        self.user = os.getenv("JIRA_USER", "")
        self.api_token = os.getenv("JIRA_API_TOKEN", "")
        self.project_key = os.getenv("JIRA_PROJECT_KEY", "DEMO")
        self.enabled = os.getenv("JIRA_ENABLED", "false").lower() == "true"

    def create_issue(self, alert: Alert) -> dict:
        if not self.enabled:
            logger.info("jira disabled | returning mocked response")
            return {
                "status": "mocked",
                "message": "Jira integration disabled",
                "payload": {
                    "project": self.project_key,
                    "summary": f"[{alert.severity.upper()}] {alert.name}",
                    "description": alert.details,
                    "issue_type": "Task",
                },
            }

        url = f"{self.base_url}/rest/api/3/issue"

        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": f"[{alert.severity.upper()}] {alert.name}",
                "description": alert.details,
                "issuetype": {"name": "Task"},
            }
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        logger.info("creating issue in jira | alert=%s", alert.name)

        response = requests.post(
            url,
            headers=headers,
            auth=(self.user, self.api_token),
            json=payload,
            timeout=15,
        )

        response.raise_for_status()
        return response.json()
