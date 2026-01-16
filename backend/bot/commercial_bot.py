"""
Commercial Bot Runner
Fetches signals and broadcasts to FREE/VIP channels
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from bot.commercial_formatter import format_free_message, format_vip_message
from bot.commercial_sender import broadcast_commercial
from bot.dispatch_guard import should_dispatch


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


def run_commercial_bot():
    """
    Commercial bot execution:
    1. Fetch signal
    2. Check dispatch rules (HIGH tier only)
    3. Format for VIP and FREE
    4. Broadcast to both channels
    """
    print("=" * 50)
    print("💰 Commercial Telegram Bot")
    print("=" * 50)
    
    # Step 1: Fetch
    print("\n📡 Fetching latest signal...")
    data = fetch_latest_signal()
    
    if not data:
        print("❌ No data received from API")
        return
    
    # Step 2: Dispatch Guard (checks tier eligibility)
    print("\n🛡️ Checking dispatch rules...")
    if not should_dispatch(data):
        print("\n⏭️  SKIPPED: Not eligible for Telegram")
        print("   (Only HIGH tier signals are sent)")
        return
    
    payload = data.get("payload", {})
    
    # Step 3: Format messages
    print("\n📝 Formatting messages...")
    vip_msg = format_vip_message(payload)
    free_msg = format_free_message(payload)
    
    print("   ✅ VIP message ready (full details)")
    print("   ✅ FREE message ready (simplified)")
    
    # Step 4: Broadcast
    print("\n📤 Broadcasting to channels...")
    results = broadcast_commercial(
        vip_message=vip_msg,
        free_message=free_msg
    )
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 BROADCAST SUMMARY")
    print("=" * 50)
    print(f"VIP Channel:  {'✅ Sent' if results['vip'] else '❌ Failed'}")
    print(f"FREE Channel: {'✅ Sent' if results['free'] else '⏭️  Disabled/Failed'}")
    print("=" * 50)


if __name__ == "__main__":
    run_commercial_bot()
