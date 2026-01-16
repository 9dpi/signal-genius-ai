"""
Signal Outcome Checker
Monitors ACTIVE signals in ledger and detects TP/SL hits or expiry.
"""
import os
import time
from datetime import datetime, timezone
from typing import Dict, List

try:
    from external_client import fetch_candles
    from signal_ledger import get_active_signals, update_signal_status
    from main import send_telegram_message
except ImportError:
    from backend.external_client import fetch_candles
    from backend.signal_ledger import get_active_signals, update_signal_status
    from backend.main import send_telegram_message

def check_outcomes():
    """
    Check all active signals against current market price.
    """
    print(f"\n🔍 [{datetime.now().strftime('%H:%M:%S')}] Checking outcomes for active signals...")
    
    active_signals = get_active_signals()
    if not active_signals:
        print("ℹ️ No active signals to check.")
        return

    try:
        # Fetch current price (using EUR/USD as it's our main pair)
        candles = None
        try:
            candles = fetch_candles(symbol="EUR/USD", limit=5)
        except Exception as e:
            print(f"❌ Error fetching current price: {e}")
            return

        if not candles:
            return

        current_price = float(candles[-1]['close'])
        print(f"📊 Current EUR/USD Price: {current_price}")

        for s in active_signals:
            signal_id = s['signal_id']
            symbol = s['symbol']
            direction = s['direction']
            entry = float(s['entry'])
            tp = float(s['tp'])
            sl = float(s['sl'])
            
            # 1. Check Expiry
            expiry_str = s.get('expiry', {}).get('expires_at')
            if expiry_str:
                expiry_dt = datetime.fromisoformat(expiry_str.replace("Z", "+00:00"))
                if datetime.now(timezone.utc) > expiry_dt:
                    print(f"⏰ Signal {signal_id} EXPIRED")
                    update_signal_status(signal_id, "EXPIRED", {"result": "NO_TRADE"})
                    notify_outcome(s, "EXPIRED")
                    continue

            # 2. Check TP/SL
            hit_tp = False
            hit_sl = False

            if direction == "BUY":
                if current_price >= tp: hit_tp = True
                elif current_price <= sl: hit_sl = True
            else: # SELL
                if current_price <= tp: hit_tp = True
                elif current_price >= sl: hit_sl = True

            if hit_tp:
                pips = round(abs(tp - entry) * 10000, 1)
                print(f"✅ Signal {signal_id} HIT TP (+{pips} pips)")
                update_signal_status(signal_id, "HIT_TP", {"result": "WIN", "pips": pips})
                notify_outcome(s, "WIN", pips)
            elif hit_sl:
                pips = round(abs(sl - entry) * 10000, 1)
                print(f"❌ Signal {signal_id} HIT SL (-{pips} pips)")
                update_signal_status(signal_id, "HIT_SL", {"result": "LOSS", "pips": -pips})
                notify_outcome(s, "LOSS", pips)

    except Exception as e:
        print(f"❌ Error in check_outcomes: {e}")


def notify_outcome(signal: Dict, result: str, pips: float = 0):
    """Notify Telegram about signal outcome"""
    chat_id = os.getenv("TELEGRAM_VIP_CHAT_ID")
    if not chat_id:
        return

    signal_id = signal['signal_id']
    symbol = signal['symbol']
    
    if result == "WIN":
        emoji = "✅"
        msg = f"<b>{emoji} CLOSED SIGNAL: WIN</b>\n\n🆔 <code>{signal_id}</code>\n📊 {symbol}\n🎯 RESULT: <b>WIN (+{pips} pips)</b>\n💰 Trust in AI established!"
    elif result == "LOSS":
        emoji = "❌"
        msg = f"<b>{emoji} CLOSED SIGNAL: LOSS</b>\n\n🆔 <code>{signal_id}</code>\n📊 {symbol}\n📉 RESULT: <b>LOSS (-{pips} pips)</b>\n⚠️ Risk management is key!"
    elif result == "EXPIRED":
        emoji = "⏰"
        msg = f"<b>{emoji} CLOSED SIGNAL: EXPIRED</b>\n\n🆔 <code>{signal_id}</code>\n📊 {symbol}\n🕒 RESULT: <b>NO TRADE (Expired)</b>\n💡 Market didn't reach target in time."
    else:
        return

    send_telegram_message(chat_id, msg)


if __name__ == "__main__":
    # Test run
    import asyncio
    
    async def main():
        # Setup env for testing if needed
        from dotenv import load_dotenv
        load_dotenv()
        
        # Run check
        check_outcomes()

    asyncio.run(main())
