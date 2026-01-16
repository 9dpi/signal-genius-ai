"""
Cron Scheduler for Telegram Bot
Run this with cron: */15 * * * * python cron.py
"""
from bot import run_bot_once

if __name__ == "__main__":
    run_bot_once()
