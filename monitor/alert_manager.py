import logging
logger = logging.getLogger("WhatsappLogger")

def send_alert_email(subject, message):
    """Mock alert sender - replace with real email or Slack notification."""
    logger.warning(f"[ALERT] {subject} - {message}")  
    # Future: Add SMTP/Slack/Webhook here