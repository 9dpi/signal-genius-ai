"""
Telegram Bot - Signal Broadcaster
Fetches signals from API and sends to Telegram channel.
"""
import asyncio
import httpx
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

from config import BOT_TOKEN, CHANNEL_ID, API_URL, POLL_INTERVAL
from sender import format_telegram_message, should_send_signal


class SignalBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.last_signal = None
        
    async def fetch_signal(self):
        """Fetch latest signal from API"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(API_URL)
                response.raise_for_status()
                data = response.json()
                
                if data.get('status') == 'ok' and data.get('payload'):
                    return data['payload']
                return None
        except Exception as e:
            print(f"❌ Error fetching signal: {e}")
            return None
    
    async def send_signal(self, signal):
        """Send signal to Telegram channel"""
        try:
            message = format_telegram_message(signal)
            
            await self.bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
            
            print(f"✅ Signal sent: {signal.get('direction')} @ {signal.get('confidence')}%")
            return True
            
        except TelegramError as e:
            print(f"❌ Telegram error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    async def run(self):
        """Main bot loop"""
        print(f"🤖 Signal Bot started")
        print(f"📡 Polling API every {POLL_INTERVAL}s")
        print(f"📢 Broadcasting to: {CHANNEL_ID}")
        print("-" * 50)
        
        while True:
            try:
                # Fetch latest signal
                signal = await self.fetch_signal()
                
                if signal:
                    # Check if we should send
                    if should_send_signal(signal, self.last_signal):
                        success = await self.send_signal(signal)
                        if success:
                            self.last_signal = signal
                    else:
                        print(f"⏭️  Skipped (no significant change)")
                else:
                    print(f"⚠️  No valid signal received")
                
            except Exception as e:
                print(f"❌ Loop error: {e}")
            
            # Wait before next poll
            await asyncio.sleep(POLL_INTERVAL)


async def main():
    """Entry point"""
    if not BOT_TOKEN or not CHANNEL_ID:
        print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID")
        print("Please set environment variables:")
        print("  TELEGRAM_BOT_TOKEN=your_bot_token")
        print("  TELEGRAM_CHANNEL_ID=@your_channel")
        return
    
    bot = SignalBot()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
