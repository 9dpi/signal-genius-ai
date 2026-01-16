"""
Telegram Message Formatter (HTML - Production Safe)
Formats signal data for Telegram using HTML parse mode
"""

def render_telegram_message(signal_data: dict) -> str:
    """
    Format signal data for Telegram using HTML.
    
    Args:
        signal_data: Signal payload with keys:
            - symbol: Trading pair (e.g., "EUR/USD")
            - timeframe: Timeframe (e.g., "M15")
            - direction: "BUY" or "SELL"
            - entry: Entry price
            - tp: Take profit
            - sl: Stop loss
            - confidence: Confidence percentage
            - strategy: Strategy name
            
    Returns:
        str: HTML-formatted message ready for Telegram
    """
    # Extract data with fallbacks
    symbol = signal_data.get('symbol') or signal_data.get('asset', 'EUR/USD')
    timeframe = signal_data.get('timeframe', 'M15')
    direction = signal_data.get('direction', 'BUY')
    entry = signal_data.get('entry', 0)
    tp = signal_data.get('tp', 0)
    sl = signal_data.get('sl', 0)
    confidence = signal_data.get('confidence', 0)
    strategy = signal_data.get('strategy', 'Rule Engine')
    
    # Direction emoji
    dir_emoji = "🟢" if direction == "BUY" else "🔴"
    
    # Format message (HTML - no escaping needed)
    message = f"""<b>📊 {symbol} | {timeframe}</b>
{dir_emoji} <b>{direction}</b>

🎯 <b>Entry:</b> {entry}
💰 <b>TP:</b> {tp}
🛑 <b>SL:</b> {sl}

⭐ <b>Confidence:</b> {confidence}%
🧠 <b>Strategy:</b> {strategy}

⚠️ <i>Not financial advice</i>"""
    
    return message.strip()


def render_telegram_message_with_id(signal_data: dict) -> str:
    """
    Format signal with Signal ID for traceability.
    
    Args:
        signal_data: Signal payload (same as render_telegram_message)
        
    Returns:
        str: HTML-formatted message with Signal ID
    """
    # Get signal ID if available
    signal_id = signal_data.get('signal_id', 'N/A')
    
    # Get base message
    base_message = render_telegram_message(signal_data)
    
    # Add signal ID at the top
    message = f"""🆔 <code>{signal_id}</code>

{base_message}"""
    
    return message.strip()


# Example usage:
if __name__ == "__main__":
    # Test data
    test_signal = {
        "signal_id": "SIG-EURUSD-20260116-1530",
        "symbol": "EUR/USD",
        "timeframe": "M15",
        "direction": "BUY",
        "entry": 1.16112,
        "tp": 1.16412,
        "sl": 1.15912,
        "confidence": 65,
        "strategy": "EMA Trend + RSI + ATR"
    }
    
    # Format message
    message = render_telegram_message(test_signal)
    print("=" * 50)
    print("TELEGRAM MESSAGE (HTML)")
    print("=" * 50)
    print(message)
    print("=" * 50)
    
    # Format with ID
    message_with_id = render_telegram_message_with_id(test_signal)
    print("\nTELEGRAM MESSAGE WITH ID (HTML)")
    print("=" * 50)
    print(message_with_id)
    print("=" * 50)
