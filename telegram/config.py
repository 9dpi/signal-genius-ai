"""
Telegram Bot Configuration
Environment variables for bot credentials and channel settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token from @BotFather
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Target Channel/Group ID (e.g., @YourChannel or -100123456789)
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

# API URL for fetching signals
API_URL = os.getenv("SIGNAL_API_URL", "https://signalgeniusai-production.up.railway.app/api/v1/signal/latest")

# Polling interval (seconds)
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))

# Minimum confidence change to trigger update (%)
MIN_CONFIDENCE_CHANGE = int(os.getenv("MIN_CONFIDENCE_CHANGE", "5"))
