# Telegram Bot - Production Guide

## 🎯 Overview

Professional Telegram bot with anti-spam protection and quality control.

### Key Features
- ✅ **Anti-Spam**: Prevents duplicate signals
- ✅ **Quality Filter**: Only sends confidence >= 60%
- ✅ **State Persistence**: Restart-safe
- ✅ **Shared Formatter**: 100% consistent with Web UI

## 🚀 Quick Start

### 1. Setup Bot
```bash
# Telegram: @BotFather
/newbot
# Save token: 8371104272:AAFlp0NA8wz-HEKOqtsbyGR1_m8C3pzZO2c
```

### 2. Get Chat ID
```bash
# Create channel/group → Add bot → Send test message
# Visit: https://api.telegram.org/bot<TOKEN>/getUpdates
# Copy chat_id
```

### 3. Configure
```env
TELEGRAM_BOT_TOKEN=8371104272:AAFlp0NA8wz-HEKOqtsbyGR1_m8C3pzZO2c
TELEGRAM_CHAT_ID=@your_channel
```

### 4. Install
```bash
cd backend/bot
pip install -r requirements.txt
```

### 5. Test
```bash
python bot.py
```

## 📊 Dispatch Rules

| Rule | Description |
|------|-------------|
| **R1** | Only send if confidence >= 60% |
| **R2** | Block duplicate (same direction + entry) |
| **R3** | One signal per asset/timeframe per 24h |
| **R4** | Restart-safe (persistent state) |
| **R5** | All decisions logged |

## 🧪 Testing

### Run Test Suite
```bash
python test_dispatch.py
```

### Check Stats
```bash
python bot.py --stats
```

### Manual Test
```bash
# First run - should send
python bot.py

# Second run - should skip (duplicate)
python bot.py

# Wait or change signal - should send
python bot.py
```

## 📁 Structure

```
backend/bot/
├── bot.py              # Main runner
├── formatter.py        # Telegram message formatter
├── telegram_sender.py  # HTTP API sender
├── dispatch_guard.py   # Anti-spam logic ⭐
├── test_dispatch.py    # Test suite
├── requirements.txt    # Dependencies
└── dispatch_state.json # State (auto-generated)
```

## 🔧 Production Deployment

### Option A: Cron (Recommended)
```bash
# Every 5 minutes
*/5 * * * * cd /app/backend/bot && python bot.py >> bot.log 2>&1
```

### Option B: Railway Worker
```yaml
# railway.toml
[deploy]
startCommand = "cd backend/bot && python bot.py"
```

### Option C: Continuous Loop
```python
# bot_loop.py
import time
from bot import run_bot_once

while True:
    run_bot_once()
    time.sleep(300)  # 5 minutes
```

## 📝 Example Output

```
==================================================
🤖 Telegram Bot - Signal Dispatch
==================================================

📡 Fetching latest signal...

🛡️ Checking dispatch rules...
✅ DISPATCH APPROVED: EUR/USD BUY @ 85%

📝 Formatting Telegram message...

📤 Sending to Telegram...
✅ Message sent to @your_channel

✅ SIGNAL SENT SUCCESSFULLY
==================================================
```

## ⚠️ Important Notes

1. **Never commit** `.env` or `dispatch_state.json`
2. **Test on private channel** first
3. **Monitor logs** regularly
4. **Backup state file** in production
5. **Use cron** for reliable scheduling

## 🐛 Troubleshooting

### Bot not sending
```bash
# Check credentials
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# Test API manually
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

### Duplicate signals
```bash
# Check state
cat dispatch_state.json

# Reset if needed (caution!)
rm dispatch_state.json
```

### Markdown errors
- All special characters are auto-escaped
- Use Markdown v2 format
- Test with simple message first

## 📈 Monitoring

```bash
# View logs
tail -f bot.log

# Check stats
python bot.py --stats

# Test dispatch logic
python test_dispatch.py
```
