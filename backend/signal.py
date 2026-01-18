from market import get_price
from datetime import datetime, timezone
import random

def get_latest_signal():
    price = get_price()
    confidence = random.randint(55, 95)
    
    # Logic for strength label
    strength = "(HIGH)" if confidence > 75 else "(MID)" if confidence > 60 else "(LOW)"

    return {
        "asset": "EUR/USD",
        "direction": "BUY",
        "strength": strength,
        "entry": round(price, 5),
        "tp": round(price + 0.0020, 5),
        "sl": round(price - 0.0015, 5),
        "confidence": confidence,
        "strategy": "Trend Follow (Stabilizer)",
        "validity": 90,
        "validity_passed": random.randint(30, 85),
        "volatility": "0.12% (Stabilized)",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
