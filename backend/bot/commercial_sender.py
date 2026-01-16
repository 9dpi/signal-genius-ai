"""
Commercial Telegram Sender
Supports FREE and VIP channels with optional delay
"""
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
VIP_CHAT_ID = os.getenv("TELEGRAM_VIP_CHAT_ID", "")
FREE_CHAT_ID = os.getenv("TELEGRAM_FREE_CHAT_ID", "")
ENABLE_FREE_CHANNEL = os.getenv("ENABLE_FREE_CHANNEL", "false").lower() == "true"
FREE_DELAY_SECONDS = int(os.getenv("FREE_DELAY_SECONDS", "600"))  # 10 minutes default


def send_to_channel(text: str, chat_id: str, channel_name: str = "Channel") -> bool:
    """
    Send message to specific Telegram channel.
    
    Args:
        text: Message text (Markdown v2 formatted)
        chat_id: Target channel ID
        channel_name: Channel name for logging
        
    Returns:
        bool: True if sent successfully
    """
    if not BOT_TOKEN or not chat_id:
        print(f"❌ Missing credentials for {channel_name}")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "MarkdownV2"
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        print(f"✅ Message sent to {channel_name} ({chat_id})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send to {channel_name}: {e}")
        return False


def send_vip(text: str) -> bool:
    """Send message to VIP channel (real-time)"""
    return send_to_channel(text, VIP_CHAT_ID, "VIP Channel")


def send_free(text: str, delay: int = 0) -> bool:
    """
    Send message to FREE channel (with optional delay).
    
    Args:
        text: Message text
        delay: Delay in seconds before sending
        
    Returns:
        bool: True if sent successfully
    """
    if not ENABLE_FREE_CHANNEL:
        print("⏭️  FREE channel disabled")
        return False
    
    if delay > 0:
        print(f"⏳ Delaying FREE channel send by {delay}s...")
        time.sleep(delay)
    
    return send_to_channel(text, FREE_CHAT_ID, "FREE Channel")


def broadcast_commercial(vip_message: str, free_message: str = None, free_delay: int = None) -> dict:
    """
    Broadcast to both VIP and FREE channels.
    
    Args:
        vip_message: Message for VIP channel
        free_message: Message for FREE channel (optional, defaults to vip_message)
        free_delay: Delay for FREE channel (optional, uses env default)
        
    Returns:
        dict: Status of both sends
    """
    results = {
        "vip": False,
        "free": False
    }
    
    # Send to VIP (real-time)
    results["vip"] = send_vip(vip_message)
    
    # Send to FREE (delayed, if enabled)
    if ENABLE_FREE_CHANNEL:
        free_msg = free_message or vip_message
        delay = free_delay if free_delay is not None else FREE_DELAY_SECONDS
        results["free"] = send_free(free_msg, delay=delay)
    
    return results
