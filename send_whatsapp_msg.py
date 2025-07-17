#!/usr/bin/env python3

"""
send_whatsapp_msg.py

Sends WhatsApp messages using Business API or fallback via pywhatkit.
Handles dry-run, error logging, alerting, and secrets.
"""

import os
import sys
import logging
from numpy import number
import yaml
import argparse
from logging.handlers import RotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv

from fallback_pywhatkit import send_via_pywhatkit
from business_api import send_via_business_api
from monitor.alert_manager import send_alert_email

# Load environment secrets
load_dotenv()

# Logging Setup
def setup_logger(log_path: str):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger = logging.getLogger("WhatsAppLogger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    fh = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=3)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

# Config loader
def load_config(config_file: str) -> dict:
    defaults = {
        "use_api": True,
        "default_message_file": "message.txt",
        "default_contacts_file": "contacts.txt",
        "log_file": "logs/send.log",
        "wait_time": 15,
        "send_hour": datetime.now(),
        "send_minute": (datetime.now().minute + 2) %60,
        "alert_email": "admin@example.com"
    }

    if not os.path.exists(config_file):
        print("[⚠️] Config not found, using defaults.")
        return defaults
    
    with open(config_file, 'r') as f:
        user = yaml.safe_load(f) or {}
        return {**defaults, **user}
    
# File load
def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()
    
def read_contacts(path: str) -> list:
    content = read_file(path)
    contacts = [line.strip() for line in content.splitlines() if line.strip()]

    if not contacts:
        logger.error("Contacts file is empty.")
        send_alert_email("Email contact file", "No recipients found.")
        sys.exit(1)
    return contacts

# Main function 
def main():
    args = parse_args()
    config = load_config(args.config)

    global logger 
    logger = setup_logger(config["log_file"])

    message_path = args.message or config["default_message_file"]
    contacts_path = args.contacts or config["default_contacts_file"]

    message = read_file(message_path)
    contacts = read_contacts(contacts_path)

    for num in contacts:
        try:
            if config["use_api"]:
                send_via_business_api(number, message, dry_run=args.dry_run)
            else:
                send_via_pywhatkit(number, message, config, dry_run=args.dry_run)

        except Exception as e:
            logger.error(f"Failed to send to {number}: {e}")
            send_alert_email("Send failure", str(e))

def parse_args():
    parser = argparse.ArgumentParser(description="Whatsapp Automation")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--message", help="Path to message")
    parser.add_argument("--contacts", help="Path to contacts file")
    parser.add_argument("--dry_run", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"[File Error] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[Unhandled Error] {e}")
        sys.exit(2)
    finally:
        print("Program finished.")   