"""
Set Telegram Webhook
Run this once to configure webhook URL
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://signalgeniusai-production.up.railway.app/telegram/webhook")

def set_webhook():
    """Set webhook URL for Telegram bot"""
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set in environment")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    
    print(f"🔧 Setting webhook to: {WEBHOOK_URL}")
    
    try:
        response = requests.post(url, json={"url": WEBHOOK_URL}, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook set successfully!")
            print(f"   URL: {WEBHOOK_URL}")
            return True
        else:
            print(f"❌ Failed to set webhook: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def get_webhook_info():
    """Get current webhook configuration"""
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set")
        return
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            info = result.get("result", {})
            print("\n📊 Webhook Info:")
            print(f"   URL: {info.get('url', 'Not set')}")
            print(f"   Pending updates: {info.get('pending_update_count', 0)}")
            print(f"   Last error: {info.get('last_error_message', 'None')}")
            return info
        else:
            print(f"❌ Failed to get webhook info: {result}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def delete_webhook():
    """Delete webhook (for testing)"""
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    
    try:
        response = requests.post(url, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook deleted")
            return True
        else:
            print(f"❌ Failed to delete webhook: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "set":
            set_webhook()
        elif command == "info":
            get_webhook_info()
        elif command == "delete":
            delete_webhook()
        else:
            print("Usage: python set_webhook.py [set|info|delete]")
    else:
        # Default: set webhook
        set_webhook()
        print("\n")
        get_webhook_info()
