
import json
import os
from datetime import datetime, timezone, timedelta

LEDGER_FILE = "signals_ledger.json"

def seed_data():
    now = datetime.now(timezone.utc)
    
    signals = [
        {
            "signal_id": "EURUSD-M15-20260117-003",
            "symbol": "EUR/USD",
            "timeframe": "M15",
            "direction": "SELL",
            "entry": 1.08650,
            "tp": 1.08450,
            "sl": 1.08750,
            "status": "OPEN",
            "confidence": 75,
            "strategy": "EMA + RSI + ATR",
            "created_at": (now - timedelta(minutes=10)).isoformat(),
            "opened_at": (now - timedelta(minutes=5)).isoformat(),
            "closed_at": None,
            "result": None,
            "pips": None
        },
        {
            "signal_id": "EURUSD-M15-20260117-002",
            "symbol": "EUR/USD",
            "timeframe": "M15",
            "direction": "BUY",
            "entry": 1.08550,
            "tp": 1.08700,
            "sl": 1.08450,
            "status": "TP_HIT",
            "confidence": 85,
            "strategy": "Trend Convergence",
            "created_at": (now - timedelta(hours=2)).isoformat(),
            "opened_at": (now - timedelta(hours=1, minutes=50)).isoformat(),
            "closed_at": (now - timedelta(hours=1, minutes=20)).isoformat(),
            "result": "WIN",
            "pips": 15
        },
        {
            "signal_id": "EURUSD-M15-20260117-001",
            "symbol": "EUR/USD",
            "timeframe": "M15",
            "direction": "SELL",
            "entry": 1.08400,
            "tp": 1.08250,
            "sl": 1.08500,
            "status": "SL_HIT",
            "confidence": 60,
            "strategy": "Mean Reversion",
            "created_at": (now - timedelta(hours=4)).isoformat(),
            "opened_at": (now - timedelta(hours=3, minutes=55)).isoformat(),
            "closed_at": (now - timedelta(hours=3, minutes=10)).isoformat(),
            "result": "LOSS",
            "pips": -10
        },
        {
            "signal_id": "EURUSD-M15-20260116-010",
            "symbol": "EUR/USD",
            "timeframe": "M15",
            "direction": "BUY",
            "entry": 1.08300,
            "tp": 1.08500,
            "sl": 1.08200,
            "status": "EXPIRED",
            "confidence": 55,
            "strategy": "Scalp Logic",
            "created_at": (now - timedelta(days=1)).isoformat(),
            "opened_at": (now - timedelta(days=1, minutes=20)).isoformat(),
            "closed_at": (now - timedelta(days=1, minutes=60)).isoformat(),
            "result": "NEUTRAL",
            "pips": 0
        }
    ]
    
    with open(LEDGER_FILE, "w") as f:
        json.dump(signals, f, indent=2)
    
    print(f"✅ Seeded {len(signals)} signals with new Trader-Grade Schema to {LEDGER_FILE}")

if __name__ == "__main__":
    seed_data()
