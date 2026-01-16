"""
Telegram Message Formatter (Shared)
Mirrors renderTelegramMessage from signals.js
"""
import re

def escape_md(text: str) -> str:
    """Escape special characters for Telegram Markdown v2"""
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))


def renderTelegramMessage(data: dict) -> str:
    """
    Format signal data for Telegram using Markdown v2.
    
    Args:
        data: Full API response with status and payload
        
    Returns:
        str: Formatted message ready for Telegram
    """
    if not data or data.get("status") != "ok":
        return "⚠️ *Signal unavailable*"

    p = data.get("payload", {})
    
    # Extract values with fallbacks
    asset = p.get("symbol") or p.get("asset", "EUR/USD")
    direction = p.get("direction", "BUY")
    confidence = p.get("confidence", 0)
    timeframe = p.get("timeframe", "M15")
    session = p.get("session", "Global")
    
    # Handle entry as array or single value
    entry = p.get("entry", 0)
    if isinstance(entry, list):
        entry_text = f"{entry[0]} – {entry[1]}"
    else:
        entry_text = str(entry)
    
    tp = p.get("tp", 0)
    sl = p.get("sl", 0)

    # Direction emoji
    direction_emoji = "🟢 BUY" if direction == "BUY" else "🔴 SELL"

    # Risk assessment
    risk = "Low" if confidence >= 80 else "Medium" if confidence >= 60 else "High"

    return f"""📊 *{escape_md(asset)}* \\| *{escape_md(timeframe)}*
{direction_emoji} \\(Confidence: *{confidence}%*\\)

📍 *Entry:* {entry_text}
🎯 *TP:* {tp}
🛑 *SL:* {sl}

🕒 *Session:* {escape_md(session)}
⚠️ *Risk:* {risk}
🤖 _Signal by Quantix AI_""".strip()
