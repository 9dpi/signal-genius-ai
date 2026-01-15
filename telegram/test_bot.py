"""
Signal Genius AI - Telegram Bot Quick Test
Sends one sample signal immediately to verify connection
"""

import os
import asyncio
from datetime import datetime, timezone
import aiohttp
from telegram import Bot
from dotenv import load_dotenv

# Load local .env if exists
load_dotenv()

# Configuration (Priority: Environment variables > Manual entry)
# Note: In production on Railway, these are set in the dashboard
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
API_URL = "https://signalgeniusai-production.up.railway.app/api/v1/lab/market-reference"

async def test_send():
    print("🚀 Starting Telegram Bot Test...")
    
    if not TOKEN or not CHAT_ID:
        print("❌ Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found in environment.")
        print("Please set them in your .env file or environment variables.")
        return

    print(f"📡 Fetching sample signal from API: {API_URL}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, timeout=10) as response:
                if response.status != 200:
                    print(f"❌ API Error: Status {response.status}")
                    return
                signal = await response.json()
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    print("📝 Formatting message...")
    # Clean formatting for Telegram
    message = f"""Asset: {signal.get('asset', 'EUR/USD')}

📌 Trade: {signal.get('direction_icon', '🟢')} {signal.get('direction', 'BUY')}

⏳ Timeframe: 15-Minute ({signal.get('timeframe', 'M15')})
🌍 Session: {signal.get('session', 'London → New York Overlap')}

💰 Price Levels:
• Entry Zone: {signal.get('price_levels', {}).get('entry_zone', ['N/A', 'N/A'])[0]} – {signal.get('price_levels', {}).get('entry_zone', ['N/A', 'N/A'])[1]}
• Take Profit (TP): {signal.get('price_levels', {}).get('take_profit', 'N/A')}
• Stop Loss (SL): {signal.get('price_levels', {}).get('stop_loss', 'N/A')}

📏 Trade Details:
• Target: +{signal.get('trade_details', {}).get('target_pips', 0)} pips
• Risk–Reward: {signal.get('trade_details', {}).get('risk_reward', 'N/A')}
• Suggested Risk: {signal.get('trade_details', {}).get('suggested_risk', '0.5% – 1%')}

🕒 Trade Type: {signal.get('trade_type', 'Intraday')}
🧠 AI Confidence: {signal.get('confidence', 0)}% ⭐

⏰ Posted: {datetime.now(timezone.utc).strftime('%b %d, %Y — %H:%M UTC')}

⏳ Auto-Expiry Rules:
• Signal is valid for this session only
• Expires at New York close
• Do not enter if price missed the zone

—
🤖 TEST MESSAGE (Manual Trigger)
"""

    print(f"📤 Sending to Chat ID: {CHAT_ID}...")
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("✅ SUCCESS! Check your Telegram.")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_send())
