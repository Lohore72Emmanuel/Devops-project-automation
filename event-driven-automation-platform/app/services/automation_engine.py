import logging
from app.models.alert import Alert
from app.connectors.servicenow import ServiceNowConnector
from app.connectors.jira import JiraConnector

logger = logging.getLogger(__name__)


class AutomationEngine:
    def __init__(self) -> None:
        self.snow = ServiceNowConnector()
        self.jira = JiraConnector()

    def should_create_ticket(self, alert: Alert) -> bool:
        """
        Decide whether to create a ticket based on severity.
        """
        decision = alert.severity.lower() in {"high", "critical"}

        logger.info(
            "ticket decision computed | alert=%s | severity=%s | create=%s",
            alert.name,
            alert.severity,
            decision,
        )

        return decision

    def enrich_alert(self, alert: Alert) -> Alert:
        """
        Enrich alert with metadata.
        """
        enriched_metadata = {
            **alert.metadata,
            "processed_by": "automation_engine",
            "normalized_severity": alert.severity.lower(),
        }

        logger.info(
            "alert enriched | alert=%s | source=%s",
            alert.name,
            alert.source,
        )

        return Alert(
            name=alert.name,
            severity=alert.severity,
            source=alert.source,
            details=alert.details,
            metadata=enriched_metadata,
        )

    def process_alert(self, alert: Alert) -> dict:
        """
        Main entry point for alert processing.
        """
        logger.info(
            "processing alert | name=%s | severity=%s | source=%s",
            alert.name,
            alert.severity,
            alert.source,
        )

        # Enrich alert
        enriched_alert = self.enrich_alert(alert)

        # Decision
        if not self.should_create_ticket(enriched_alert):
            logger.info("alert ignored | name=%s", enriched_alert.name)

            return {
                "status": "ignored",
                "reason": "severity below threshold",
                "alert": enriched_alert.model_dump(),
            }

        # Create tickets
        jira_result = self.jira.create_issue(enriched_alert)
        snow_result = self.snow.create_incident(enriched_alert)

        logger.info("tickets created | name=%s", enriched_alert.name)

        return {
            "status": "ticket_created",
            "alert": enriched_alert.model_dump(),
            "jira_result": jira_result,
            "itsm_result": snow_result,
        }
