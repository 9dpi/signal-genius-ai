from datetime import datetime

def send_telegram_alert(signal):
    """
    Formats the signal exactly 1:1 with the Web Card layout for Telegram.
    """
    ts = datetime.fromisoformat(signal["timestamp"].replace("Z", "+00:00"))
    date_str = ts.strftime("%Y-%m-%d")
    direction_emoji = "🟢" if signal["direction"] == "BUY" else "🔴"
    
    message = (
        f"ℹ️ You are viewing today's signal\n"
        f"📅 Date: {date_str}\n"
        f"Status: Live Snapshot\n\n"
        f"📊 {signal['asset']} | M15\n"
        f"{direction_emoji} {signal['direction']} {signal['strength']}\n\n"
        f"🎯 Entry: {signal['entry']}\n"
        f"💰 TP: {signal['tp']}\n"
        f"🛑 SL: {signal['sl']}\n\n"
        f"⭐ Confidence: {signal['confidence']}%\n"
        f"🧠 Strategy: {signal['strategy']}\n"
        f"⏳ Validity: {signal.get('validity_passed', 85)} / {signal.get('validity', 90)} min\n"
        f"🌊 Volatility: {signal.get('volatility', '0.12% (Stabilized)')}\n\n"
        f"⚠️ Educational purpose only"
    )
    
    # In production, this would call the Telegram Bot API
    print("--- SENDING TELEGRAM ALERT ---")
    print(message)
    print("------------------------------")
    return message
