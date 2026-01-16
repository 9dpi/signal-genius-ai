"""
Telegram Bot Runner (Production-Ready)
Fetches signal from API, applies dispatch rules, and sends to Telegram
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from bot.formatter import renderTelegramMessage
from bot.telegram_sender import send_telegram_message
from bot.dispatch_guard import should_dispatch, get_dispatch_stats


API_URL = os.getenv(
    "SIGNAL_API_URL", 
    "https://signalgeniusai-production.up.railway.app/api/v1/signal/latest"
)


def fetch_latest_signal():
    """Fetch latest signal from API"""
    try:
        response = httpx.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching signal: {e}")
        return None


def run_bot_once():
    """
    Single execution with anti-spam protection:
    1. Fetch signal from API
    2. Check dispatch rules
    3. Format message
    4. Send to Telegram
    """
    print("=" * 50)
    print("🤖 Telegram Bot - Signal Dispatch")
    print("=" * 50)
    
    # Step 1: Fetch
    print("\n📡 Fetching latest signal...")
    data = fetch_latest_signal()
    
    if not data:
        print("❌ No data received from API")
        return
    
    # Step 2: Dispatch Guard
    print("\n🛡️ Checking dispatch rules...")
    if not should_dispatch(data):
        print("\n⏭️  SKIPPED: Dispatch rules blocked this signal")
        print("   (Prevents spam, maintains quality)")
        return
    
    # Step 3: Format
    print("\n📝 Formatting Telegram message...")
    message = renderTelegramMessage(data)
    
    # Step 4: Send
    print("\n📤 Sending to Telegram...")
    success = send_telegram_message(message)
    
    if success:
        print("\n✅ SIGNAL SENT SUCCESSFULLY")
        print("=" * 50)
    else:
        print("\n❌ FAILED TO SEND")
        print("=" * 50)


def show_stats():
    """Show dispatch statistics"""
    stats = get_dispatch_stats()
    print("\n📊 Dispatch Statistics:")
    print(f"   Total signals sent: {stats['total_signals']}")
    print(f"   Tracked pairs: {', '.join(stats['pairs'])}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Telegram Signal Bot")
    parser.add_argument("--stats", action="store_true", help="Show dispatch stats")
    args = parser.parse_args()
    
    if args.stats:
        show_stats()
    else:
        run_bot_once()
