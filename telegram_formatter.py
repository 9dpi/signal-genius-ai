import os
import requests
from datetime import datetime

def format_signal_message(signal: dict) -> str:
    status = signal.get("status", "ACTIVE")
    if isinstance(status, str):
        status = status.upper()
    
    # 1. SPECIAL STATUS: MARKET CLOSED
    if status == "MARKET_CLOSED":
        return (
            "⚡️ SIGNAL GENIUS AI\n\n"
            "Status: Market Closed 🌑\n\n"
            "The Forex market is currently closed.\n"
            "No signals generated on weekends.\n\n"
            "System will auto-resume on Monday."
        )

    # Standard Fields Extraction
    asset = signal.get("asset") or signal.get("symbol") or "EURUSD"
    asset = asset.replace("/", "")
    timeframe = signal.get("timeframe", "M15")
    direction = str(signal.get("direction", "N/A")).upper()
    dir_emoji = "🟢" if direction == "BUY" else "🔴" if direction == "SELL" else "⚪"
    
    confidence = signal.get("confidence") or signal.get("ai_confidence") or 0
    if isinstance(confidence, float) and confidence <= 1.0:
        confidence = int(confidence * 100)
    
    strength = signal.get("strength") or 0
    if isinstance(strength, (int, float)) and strength <= 1.0:
        strength_pct = f"{int(strength * 100)}%"
    else:
        strength_pct = str(strength)

    entry = signal.get("entry") or signal.get("entry_low") or "N/A"
    tp = signal.get("tp") or "N/A"
    sl = signal.get("sl") or "N/A"

    # TEMPLATE 3 – SIGNAL ULTRA (95%+ FAST ALERT)
    if confidence >= 95 and status != "EXPIRED":
        return (
            f"🚨 *ULTRA SIGNAL (95%+)*\n\n"
            f"{asset} | {timeframe}\n"
            f"{dir_emoji} {direction}\n\n"
            f"Status: 🟢 ACTIVE\n"
            f"Entry window: OPEN\n\n"
            f"Confidence: {confidence}%\n"
            f"Strength: {strength_pct}\n\n"
            f"🎯 Entry: {entry}\n"
            f"💰 TP: {tp}\n"
            f"🛑 SL: {sl}\n\n"
            f"🔗 [View Live Dashboard](https://www.signalgeniusai.com/)"
        )

    # TEMPLATE 2 – SIGNAL ĐÃ HẾT ENTRY (EXPIRED – RECORD)
    if status in ["EXPIRED", "CLOSED"]:
        result = signal.get("result", "N/A")
        if result == "N/A": result = "Closed"
        return (
            f"⚡️ *SIGNAL GENIUS AI*\n\n"
            f"Asset: {asset}\n"
            f"Timeframe: {timeframe}\n"
            f"Direction: {dir_emoji} {direction}\n\n"
            f"Status: ⛔ EXPIRED (for record only)\n\n"
            f"Entry: {entry}\n"
            f"TP: {tp}\n"
            f"SL: {sl}\n\n"
            f"Result: {result}\n\n"
            f"🔗 [View Live Dashboard](https://www.signalgeniusai.com/)"
        )

    # TEMPLATE 1 – SIGNAL CÒN HIỆU LỰC (ACTIVE)
    validity_min = signal.get("validity", 90)
    passed = signal.get("validity_passed", 0)
    remaining = max(1, validity_min - passed)
    
    return (
        f"⚡️ *SIGNAL GENIUS AI*\n\n"
        f"Asset: {asset}\n"
        f"Timeframe: {timeframe}\n"
        f"Direction: {dir_emoji} {direction}\n\n"
        f"Status: 🟢 ACTIVE\n"
        f"Valid for: ~{remaining} minutes\n\n"
        f"Confidence: {confidence}%\n"
        f"Force/Strength: {strength_pct}\n\n"
        f"🎯 Entry: {entry}\n"
        f"💰 TP: {tp}\n"
        f"🛑 SL: {sl}\n\n"
        f"🔗 [View Live Dashboard](https://www.signalgeniusai.com/)"
    )

def send_telegram(chat_id, signal):
    """
    Formats the signal in a clean, concise format for Telegram.
    Shows only essential trading information.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token or not chat_id:
        print("⚠️ Telegram credentials missing. Skipping alert.")
        return None

    message = format_signal_message(signal)
    
    # Gửi tin nhắn dùng Markdown, kèm theo buttons
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
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
