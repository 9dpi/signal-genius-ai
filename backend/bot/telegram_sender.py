"""
Telegram Sender - Simple HTTP API
Sends formatted messages to Telegram channel/group
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def send_telegram_message(text: str) -> bool:
    """
    Send message to Telegram using Bot API.
    
    Args:
        text: Message text (Markdown v2 formatted)
        
    Returns:
        bool: True if sent successfully
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "MarkdownV2"
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        print(f"✅ Message sent to {CHAT_ID}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send message: {e}")
        return False
