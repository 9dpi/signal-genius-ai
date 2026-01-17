from datetime import datetime, timezone

def render_telegram_message(signal_data: dict) -> str:
    """
    Format signal data for Telegram using the new Lifecycle format.
    """
    symbol = signal_data.get('symbol') or signal_data.get('asset', 'EUR/USD')
    timeframe = signal_data.get('timeframe', 'M15')
    direction = signal_data.get('direction', 'BUY')
    entry = signal_data.get('entry', 0)
    tp = signal_data.get('tp', 0)
    sl = signal_data.get('sl', 0)
    status = signal_data.get('status_life') or signal_data.get('status', 'OPEN')
    confidence = signal_data.get('confidence', 0)
    pips = signal_data.get('pips')
    # Duration could be calculated if closed_at/opened_at available
    
    # 1. TP HIT / SL HIT Case
    if status == "TP_HIT":
        return f"✅ <b>TP HIT – {symbol} ({timeframe})</b>\n\n💰 <b>+{pips if pips else '—'} pips</b>\n⏱ <i>Trade Closed</i>".strip()
    
    if status == "SL_HIT":
        return f"❌ <b>SL HIT – {symbol} ({timeframe})</b>\n\n📉 <b>{pips if pips else '—'} pips</b>\n⏱ <i>Trade Closed</i>".strip()

    if status == "EXPIRED":
        return f"⚪ <b>EXPIRED – {symbol} ({timeframe})</b>\n\nTrade closed by time rule.".strip()

    # 2. OPEN Case (Standard Signal)
    dir_emoji = "🟢" if direction == "BUY" else "🔴"
    
    message = f"""<b>📊 {symbol} | {timeframe}</b>
{dir_emoji} <b>{direction}</b>

🎯 <b>Entry:</b> {entry}
💰 <b>TP:</b> {tp}
🛑 <b>SL:</b> {sl}

📈 <b>Status:</b> {status}
⭐ <b>Confidence:</b> {confidence}%

⚠️ <i>Educational purpose only</i>"""

    return message.strip()

def render_telegram_payload(signal_data: dict) -> dict:
    """Generate Telegram payload with interactive buttons."""
    symbol = signal_data.get('symbol') or signal_data.get('asset', 'EUR/USD')
    clean_symbol = symbol.replace("/", "").replace("-", "")
    chart_url = f"https://www.tradingview.com/chart/?symbol=FX:{clean_symbol}"
    
    return {
        "text": render_telegram_message(signal_data),
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "📈 View Chart", "url": chart_url},
                    {"text": "📊 Stats", "callback_data": "stats"}
                ]
            ]
        }
    }

