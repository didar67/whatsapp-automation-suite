import os
import json
import requests
import logging

logger = logging.getLogger("WhatsappLogger")

def send_via_business_api(number, message, dry_run=False):
    """Send message using Whatsapp Buisness API"""
    if dry_run:
        logger.info(f"[DRY_RUN][API] Would send to number: {number}")
        return
    
    url = os.getenv("WHATSAPP_API_URL")
    token = os.getenv("WHATSAPP_API_TOKEN")
    sender_id = os.getenv("SENDER_PHONE_ID")

    if not url or not token or not sender_id:
        raise ValueError("Missing required environment variables: WHATSAPP_API_URL, WHATSAPP_API_TOKEN, or SENDER_PHONE_ID")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {"body": message},
        "sender": sender_id
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        logger.info(f"API message sent to {number}")
    else:
        raise Exception(f"API failed: {response.status_code} - {response.text}")
    