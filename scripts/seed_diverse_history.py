
import json
import os
from datetime import datetime, timezone, timedelta

LEDGER_FILE = "signals_ledger.json"

def seed_diverse_data():
    now = datetime.now(timezone.utc)
    
    signals = [
        {
            "signal_id": "EURUSD-M15-004",
            "symbol": "EUR/USD",
            "timeframe": "M15",
            "direction": "BUY",
            "entry": 1.1604,
            "tp": 1.1619,
            "sl": 1.1589,
            "status": "OPEN",
            "confidence": 55,
            "strategy": "EMA + RSI + ATR",
            "created_at": (now - timedelta(minutes=8)).isoformat(),
            "pips": None
        },
        {
            "signal_id": "GBPUSD-M5-003",
            "symbol": "GBP/USD",
            "timeframe": "M5",
            "direction": "SELL",
            "entry": 1.2712,
            "tp": 1.2695,
            "sl": 1.2725,
            "status": "TP_HIT",
            "confidence": 92,
            "strategy": "Trend Follow",
            "created_at": (now - timedelta(minutes=42)).isoformat(),
            "pips": 17
        },
        {
            "signal_id": "USDJPY-M15-002",
            "symbol": "USD/JPY",
            "timeframe": "M15",
            "direction": "SELL",
            "entry": 147.80,
            "tp": 148.10,
            "sl": 147.30,
            "status": "SL_HIT",
            "confidence": 78,
            "strategy": "Mean Reversion",
            "created_at": (now - timedelta(minutes=19)).isoformat(),
            "pips": -12
        },
        {
            "signal_id": "AUDUSD-M15-001",
            "symbol": "AUD/USD",
            "timeframe": "M15",
            "direction": "BUY",
            "entry": 0.6540,
            "tp": 0.6560,
            "sl": 0.6520,
            "status": "EXPIRED",
            "confidence": 65,
            "strategy": "Breakout",
            "created_at": (now - timedelta(hours=2)).isoformat(),
            "pips": 0
        },
        {
            "signal_id": "BTCUSD-H1-001",
            "symbol": "BTC/USD",
            "timeframe": "H1",
            "direction": "BUY",
            "entry": 42500,
            "tp": 43500,
            "sl": 42000,
            "status": "TP_HIT",
            "confidence": 88,
            "strategy": "H1 Trend",
            "created_at": (now - timedelta(hours=5)).isoformat(),
            "pips": 1000
        }
    ]
    
    with open(LEDGER_FILE, "w") as f:
        json.dump(signals, f, indent=2)
    
    print(f"✅ Seeded {len(signals)} diverse signals to {LEDGER_FILE}")

if __name__ == "__main__":
    seed_diverse_data()
