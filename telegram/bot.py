"""
Signal Genius AI - Telegram Bot
Sends 1 high-confidence signal per day (confidence >= 95%)
"""

import os
import json
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict
import aiohttp
from telegram import Bot
from telegram.error import TelegramError

# Configuration
API_ENDPOINT = os.getenv('API_ENDPOINT', 'https://signalgeniusai-production.up.railway.app/api/v1/signal/latest')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8371104272:AAFlp0NA8wz-HEKOqtsbyGR1_m8C3pzZO2c')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '7985984228')
ASSET = 'EUR/USD'
MIN_CONFIDENCE = 95

# Track sent signals to avoid duplicates
sent_signals_today = set()
last_check_date = None


async def fetch_signal() -> Optional[Dict]:
    """Fetch signal from API endpoint"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{API_ENDPOINT}?asset={ASSET}"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"❌ API returned status {response.status}")
                    return None
    except Exception as e:
        print(f"❌ Error fetching signal: {e}")
        return None


def format_signal_message(signal: Dict) -> str:
    """Format signal data into Telegram message using rich tier format"""
    
    # Extract data
    asset = signal.get('asset', 'EUR/USD')
    direction = signal.get('direction', 'BUY').upper()
    direction_icon = signal.get('direction_icon', "🟢")
    tier_label = signal.get('tier_label', direction)
    timeframe = signal.get('timeframe', 'M15')
    session = signal.get('session', 'London → New York Overlap')
    risk_note = signal.get('risk_note', '')
    
    price_levels = signal.get('price_levels', {})
    entry_zone = price_levels.get('entry_zone', ['N/A', 'N/A'])
    take_profit = price_levels.get('take_profit', 'N/A')
    stop_loss = price_levels.get('stop_loss', 'N/A')
    
    trade_details = signal.get('trade_details', {})
    target_pips = trade_details.get('target_pips', 0)
    risk_reward = trade_details.get('risk_reward', 'N/A')
    suggested_risk = trade_details.get('suggested_risk', '0.5% – 1%')
    
    trade_type = signal.get('trade_type', 'Intraday')
    confidence = signal.get('confidence', 0)
    posted_at = signal.get('posted_at_utc', datetime.now(timezone.utc).isoformat())
    
    # Format posted time
    try:
        dt = datetime.fromisoformat(posted_at.replace('Z', '+00:00'))
        posted_str = dt.strftime('%b %d, %Y — %H:%M UTC')
    except:
        posted_str = datetime.now(timezone.utc).strftime('%b %d, %Y — %H:%M UTC')
    
    # Build message
    message = f"""Asset: {asset}

📌 Trade: {direction_icon} {tier_label} (expect price to go {"up" if direction == "BUY" else "down"})

⏳ Timeframe: 15-Minute ({timeframe})
🌍 Session: {session}

💰 Price Levels:
• Entry Zone: {entry_zone[0]} – {entry_zone[1]}
• Take Profit (TP): {take_profit}
• Stop Loss (SL): {stop_loss}

📏 Trade Details:
• Target: +{target_pips} pips
• Risk–Reward: {risk_reward}
• Suggested Risk: {suggested_risk}

🕒 Trade Type: {trade_type}
🧠 AI Confidence: {confidence}% ⭐

⏰ Posted: {posted_str}

ℹ️ Note: {risk_note}

⏳ Auto-Expiry Rules:
• Signal is valid for this session only
• Expires at New York close or if TP or SL is hit
• Do not enter if price has already moved significantly beyond the entry zone

—
⚠️ Not financial advice. Trade responsibly."""

    return message


async def send_telegram_message(message: str) -> bool:
    """Send message to Telegram"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode=None  # Plain text, no markdown
        )
        print(f"✅ Signal sent to Telegram successfully")
        return True
    except TelegramError as e:
        print(f"❌ Telegram error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False


def should_send_signal(signal: Dict) -> bool:
    """Check if signal should be sent based on rules"""
    global sent_signals_today, last_check_date
    
    # 1. Check Confidence Gate
    # Use telegram_eligible flag if backend provides it, otherwise fallback to threshold
    telegram_eligible = signal.get('telegram_eligible')
    if telegram_eligible is False:
        print(f"⚠️ Signal is not eligible for Telegram (Tier: {signal.get('confidence_tier')})")
        return False
        
    confidence = signal.get('confidence', 0)
    if telegram_eligible is None and confidence < MIN_CONFIDENCE:
        print(f"⚠️ Confidence {confidence}% < {MIN_CONFIDENCE}% - Not sending")
        return False
    
    # 2. Daily Limit Gate
    today = datetime.now(timezone.utc).date()
    if last_check_date != today:
        sent_signals_today.clear()
        last_check_date = today
    
    signal_id = f"{signal.get('asset')}_{signal.get('direction')}_{today}"
    if signal_id in sent_signals_today:
        print(f"⚠️ Already sent signal for {signal.get('asset')} today - Not sending")
        return False
    
    sent_signals_today.add(signal_id)
    return True


async def check_and_send_signal():
    """Main function to check for signal and send if conditions are met"""
    print(f"\n🔍 Checking for signal at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # Fetch signal
    signal = await fetch_signal()
    
    if not signal:
        print("⚠️ No signal data available")
        return
    
    # Check if should send
    if not should_send_signal(signal):
        return
    
    # Format and send message
    message = format_signal_message(signal)
    success = await send_telegram_message(message)
    
    if success:
        print(f"✅ Signal sent successfully: {signal.get('asset')} {signal.get('direction')}")
    else:
        # Remove from sent list if sending failed
        sent_signals_today.discard(f"{signal.get('asset')}_{signal.get('direction')}_{datetime.now(timezone.utc).date()}")


async def run_bot():
    """Run bot with periodic checks (every 15 minutes)"""
    print("🤖 Signal Genius AI Telegram Bot started")
    print(f"📊 Monitoring: {ASSET}")
    print(f"🎯 Min Confidence: {MIN_CONFIDENCE}%")
    print(f"📢 Max signals per day: 1 per asset")
    print(f"⏰ Check interval: 15 minutes\n")
    
    while True:
        try:
            await check_and_send_signal()
        except Exception as e:
            print(f"❌ Error in bot loop: {e}")
        
        # Wait 15 minutes before next check
        await asyncio.sleep(15 * 60)


if __name__ == "__main__":
    # Run the bot
    asyncio.run(run_bot())
