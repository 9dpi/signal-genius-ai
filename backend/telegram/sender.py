"""
Telegram Message Formatter
Converts signal payload to Telegram-ready Markdown text.
Mirrors the logic from signals.js for consistency.
"""
import re

def escape_markdown_v2(text):
    """Escape special characters for Telegram Markdown v2"""
    special_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(special_chars)}])', r'\\\1', str(text))


def format_telegram_message(payload):
    """
    Format signal data for Telegram using Markdown v2.
    
    Args:
        payload: Signal data from API
        
    Returns:
        str: Formatted message ready for Telegram
    """
    if not payload:
        return "⚠️ *Signal unavailable*"
    
    # Extract data with fallbacks
    asset = payload.get('symbol') or payload.get('asset', 'EUR/USD')
    timeframe = payload.get('timeframe', 'M15')
    direction = payload.get('direction', 'BUY')
    confidence = payload.get('confidence', 0)
    entry = payload.get('entry', 0)
    tp = payload.get('tp', 0)
    sl = payload.get('sl', 0)
    session = payload.get('session', 'Global')
    
    # Handle entry as array or single value
    if isinstance(entry, list):
        entry_text = f"{escape_markdown_v2(entry[0])} – {escape_markdown_v2(entry[1])}"
    else:
        entry_text = escape_markdown_v2(entry)
    
    # Direction emoji
    dir_emoji = "🟢 BUY" if direction == "BUY" else "🔴 SELL"
    
    # Risk assessment (matching signals.js logic)
    if confidence >= 80:
        risk = "Low"
    elif confidence >= 60:
        risk = "Medium"
    else:
        risk = "High"
    
    # Build message (Markdown v2 format)
    message = f"""📊 *{escape_markdown_v2(asset)}* \\| *{escape_markdown_v2(timeframe)}*
{dir_emoji} \\(Confidence: *{confidence}%*\\)

📍 *Entry:* {entry_text}
🎯 *TP:* {escape_markdown_v2(tp)}
🛑 *SL:* {escape_markdown_v2(sl)}

🕒 *Session:* {escape_markdown_v2(session)}
⚠️ *Risk:* {risk}
🤖 _Signal by Quantix AI_"""
    
    return message


def should_send_signal(current_signal, previous_signal):
    """
    Determine if a new signal should be sent to Telegram.
    
    Rules:
    - Always send if no previous signal
    - Send if direction changed
    - Send if confidence changed by ±5%
    - Don't spam on minor updates
    
    Args:
        current_signal: Latest signal payload
        previous_signal: Last sent signal payload
        
    Returns:
        bool: True if should send
    """
    if not previous_signal:
        return True
    
    # Check direction change
    if current_signal.get('direction') != previous_signal.get('direction'):
        return True
    
    # Check confidence change (±5%)
    curr_conf = current_signal.get('confidence', 0)
    prev_conf = previous_signal.get('confidence', 0)
    
    if abs(curr_conf - prev_conf) >= 5:
        return True
    
    # Check if it's a completely new signal (different generated_at timestamp)
    curr_time = current_signal.get('generated_at', '')
    prev_time = previous_signal.get('generated_at', '')
    
    if curr_time != prev_time and curr_time:
        return True
    
    return False
