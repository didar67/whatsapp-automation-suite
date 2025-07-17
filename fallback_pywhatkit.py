import pywhatkit
import logging

logger = logging.getLogger("WhatsappLogger")

def send_via_pywhatkit(number, message, config, dry_run: bool = False):
    """Send message using Pywhatkit as fallback."""

    if dry_run:
        logger.info(f"[DRY-RUN][PYWHATKIT] Would send to {number}")
        return
    
    hour = config["send_hour"]
    minute = config["send_minute"]
    wait_time = config.get("wait_time", 20)  # default 20 if not provided

    try:
        pywhatkit.sendwhatmsg(number, message, hour, minute, wait_time=wait_time)
        logger.info(f"Fallback message scheduled to {number} at {hour}:{minute}")
        logger.info("Keep WhatsApp Web open in browser.")
    except Exception as e:
        logger.error(f"Failed to send message using pywhatkit: {e}")
