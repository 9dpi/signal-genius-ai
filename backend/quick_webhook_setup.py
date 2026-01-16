#!/usr/bin/env python3
"""
Quick Webhook Setup Script
Run this to configure Telegram webhook
"""

# Your bot token
BOT_TOKEN = "8371104272:AAFlp0NA8wz-HEKOqtsbyGR1_m8C3pzZO2c"

# Your Railway webhook URL
WEBHOOK_URL = "https://signalgeniusai-production.up.railway.app/telegram/webhook"

import requests

print("=" * 60)
print("🤖 TELEGRAM WEBHOOK SETUP")
print("=" * 60)

# Set webhook
print(f"\n🔧 Setting webhook to: {WEBHOOK_URL}")
response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": WEBHOOK_URL}
)

result = response.json()
if result.get("ok"):
    print("✅ Webhook set successfully!")
else:
    print(f"❌ Failed: {result}")

# Verify webhook
print("\n📊 Verifying webhook...")
response = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
)

info = response.json().get("result", {})
print(f"\n✅ Webhook URL: {info.get('url')}")
print(f"✅ Pending updates: {info.get('pending_update_count', 0)}")
print(f"✅ Last error: {info.get('last_error_message', 'None')}")

print("\n" + "=" * 60)
print("🎯 SETUP COMPLETE!")
print("=" * 60)
print("\n📱 Test your bot now:")
print("   1. Open Telegram")
print("   2. Find: @signal_genius_ai_bot")
print("   3. Send: /start")
print("\n✅ Bot should respond immediately!")
print("=" * 60)
