"""
Professional Scheduler for Signal Genius AI
Runs signal generation and outcome monitoring.
"""
import sys
import os
import time
from datetime import datetime

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from bot import run_bot_once
    from outcome_checker import check_outcomes
except ImportError:
    # Fallback for different execution contexts
    from backend.bot.bot import run_bot_once
    from backend.outcome_checker import check_outcomes

def run_scheduler():
    """
    Run the complete cycle:
    1. Monitor existing signals (Outcome checker)
    2. Generate new signals (Bot runner)
    """
    print("=" * 60)
    print(f"🚀 SIGNAL GENIUS AI SCHEDULER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Check outcomes of active signals
    try:
        check_outcomes()
    except Exception as e:
        print(f"❌ Error in outcome checker: {e}")

    print("-" * 30)

    # 2. Run signal generation bot
    try:
        run_bot_once()
    except Exception as e:
        print(f"❌ Error in bot runner: {e}")

    print("=" * 60)
    print("✅ CYCLE COMPLETE. Waiting for next run...")

if __name__ == "__main__":
    # If run directly, execute once
    # For server-less environments like GitHub Actions or simple CRON
    run_scheduler()
