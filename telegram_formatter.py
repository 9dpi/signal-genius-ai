import os
import requests
from datetime import datetime

def send_telegram(chat_id, signal):
    """
    Formats the signal in a clean, concise format for Telegram.
    Shows only essential trading information.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token or not chat_id:
        print("⚠️ Telegram credentials missing. Skipping alert.")
        return None

    # Get status from signal
    status = signal.get("status", "EXECUTED")
    
    # 1. Handle Market Closed State
    if status == "MARKET_CLOSED":
        message = (
            "SIGNAL GENIUS AI\n\n"
            "Market Status: CLOSED\n\n"
            "The Forex market is currently closed.\n"
            "No signals are generated during this period.\n\n"
            "Signals will resume when the market reopens."
        )
    else:
        # 2. Standard Signal Format
        validity = signal.get("validity_status", "ACTIVE")
        direction = str(signal.get("direction", "WAIT")).upper()
        direction_emoji = "🟢" if direction == "BUY" else "🔴" if direction == "SELL" else "⚪"
        
        message = (
            f"SIGNAL GENIUS AI\n"
            f"Status: {status}\n"
            f"Validity: {validity}\n\n"
            f"{signal['asset']} | M15\n"
            f"{direction_emoji} {signal['direction']}\n\n"
            f"🎯 Entry: {signal['entry']}\n"
            f"💰 TP: {signal['tp']}\n"
            f"🛑 SL: {signal['sl']}\n"
            f"--\n"
            f"⚠️ Educational purpose only\n"
            f"--"
        )
    
    # Gửi tin nhắn dùng text thuần, KHÔNG parse_mode, kèm theo buttons
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "📈 View Latest Signal", "url": "https://www.signalgeniusai.com/"},
                        {"text": "🔄 Refresh", "callback_data": "refresh_signal"}
                    ],
                    [
                        {"text": "📊 Stats", "callback_data": "view_stats"}
                    ]
                ]
            }
        }
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print(f"✅ Telegram signal sent: {signal['asset']}")
        return r.json()
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")
        return None
