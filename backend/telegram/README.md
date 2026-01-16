# Telegram Bot Setup Guide

## 📋 Prerequisites

1. **Create Telegram Bot**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow instructions
   - Save your bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Create Channel/Group**
   - Create a public channel or group
   - Add your bot as administrator
   - Get channel ID (for public: `@YourChannel`, for private: use @userinfobot)

## 🔧 Installation

```bash
cd backend/telegram
pip install -r requirements.txt
```

## ⚙️ Configuration

Create `.env` file in project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_or_group_id
SIGNAL_API_URL=https://signalgeniusai-production.up.railway.app/api/v1/signal/latest
POLL_INTERVAL=60
MIN_CONFIDENCE_CHANGE=5
```

## 🚀 Running the Bot

### Local Testing
```bash
cd backend/telegram
python bot.py
```

### Production (Railway/Heroku)
Add environment variables in your hosting platform dashboard.

## 📊 How It Works

1. **Polling**: Bot checks API every 60 seconds (configurable)
2. **Smart Sending**: Only sends when:
   - Direction changes (BUY ↔ SELL)
   - Confidence changes by ±5%
   - New signal generated
3. **Format**: Clean Markdown messages with emojis
4. **Reliability**: Handles API errors gracefully

## 🔍 Testing

Send a test message:
```python
from telegram import Bot
bot = Bot(token="YOUR_TOKEN")
bot.send_message(chat_id="@YourChannel", text="Test message")
```

## 📝 Message Format

```
📊 EUR/USD | M15
🟢 BUY (Confidence: 85%)

📍 Entry: 1.0874
🎯 TP: 1.0912
🛑 SL: 1.0849

🕒 Session: London-NewYork
⚠️ Risk: Medium
🔍 Strategy: EMA Trend + RSI + ATR

🤖 Signal by Quantix AI Core
```

## 🛡️ Security Notes

- Never commit `.env` file
- Keep bot token secret
- Use private channels for testing
- Monitor bot logs regularly
