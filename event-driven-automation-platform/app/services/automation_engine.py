import logging
from app.models.alert import Alert
from app.connectors.servicenow import ServiceNowConnector

logger = logging.getLogger(__name__)


class AutomationEngine:
    def __init__(self) -> None:
        self.snow = ServiceNowConnector()

    def should_create_ticket(self, alert: Alert) -> bool:
        decision = alert.severity.lower() in {"high", "critical"}
        logger.info(
            "ticket decision computed | alert=%s | severity=%s | create=%s",
            alert.name,
            alert.severity,
            decision,
        )
        return decision

    def enrich_alert(self, alert: Alert) -> Alert:
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
        logger.info(
            "processing alert | name=%s | severity=%s | source=%s",
            alert.name,
            alert.severity,
            alert.source,
        )

        enriched_alert = self.enrich_alert(alert)

        if not self.should_create_ticket(enriched_alert):
            logger.info("alert ignored | name=%s", enriched_alert.name)
            return {
                "status": "ignored",
                "reason": "severity below threshold",
                "alert": enriched_alert.model_dump(),
            }

        result = self.snow.create_incident(enriched_alert)
        logger.info("ticket created | name=%s", enriched_alert.name)
        return {
            "status": "ticket_created",
            "alert": enriched_alert.model_dump(),
            "itsm_result": result,
        }
