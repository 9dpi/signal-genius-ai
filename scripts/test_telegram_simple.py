
import asyncio
from telegram import Bot
import os

TELEGRAM_BOT_TOKEN = '8371104272:AAFlp0NA8wz-HEKOqtsbyGR1_m8C3pzZO2c'
TELEGRAM_CHAT_ID = '7985984228'

async def test_telegram():
    print(f"🔌 Testing connection to Telegram Bot...")
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Bot connected: @{me.username} ({me.first_name})")
        
        print(f"📤 Sending test message to {TELEGRAM_CHAT_ID}...")
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text="🚀 *Quantix MVP Health Check*\nSystem is ONLINE and operational.",
            parse_mode='Markdown'
        )
        print(f"✅ Message sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_telegram())
