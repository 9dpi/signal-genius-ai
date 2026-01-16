"""
Dispatch Guard - Anti-Spam Logic
Prevents duplicate signals and manages sending rules
"""
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional


STATE_FILE = "dispatch_state.json"


def load_state() -> Dict:
    """Load dispatch state from file"""
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading state: {e}")
        return {}


def save_state(state: Dict) -> None:
    """Save dispatch state to file"""
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"⚠️ Error saving state: {e}")


def should_dispatch(data: dict) -> bool:
    """
    Determine if signal should be sent to Telegram.
    
    Rules:
    - R1: Only send if confidence >= 60%
    - R2: Don't resend same direction + entry zone
    - R3: One signal per asset/timeframe per 24h (unless changed)
    - R4: Restart-safe (uses persistent state)
    - R5: All decisions are logged
    
    Args:
        data: Full API response with payload
        
    Returns:
        bool: True if should send
    """
    if not data or data.get("status") != "ok":
        print("❌ R0: Invalid data")
        return False
    
    p = data.get("payload", {})
    
    # Extract key fields
    asset = p.get("symbol") or p.get("asset", "EUR/USD")
    timeframe = p.get("timeframe", "M15")
    confidence = p.get("confidence", 0)
    direction = p.get("direction", "BUY")
    entry = p.get("entry", 0)
    
    # Get confidence tier metadata
    confidence_meta = p.get("confidence_meta", {})
    
    # Create unique key for this asset/timeframe pair
    key = f"{asset}_{timeframe}"
    
    # R1: Telegram eligibility (tier-based)
    if not confidence_meta.get("telegram", False):
        tier = confidence_meta.get("tier", "UNKNOWN")
        print(f"❌ R1: Not eligible for Telegram (tier: {tier}, confidence: {confidence}%)")
        print(f"   💡 Tip: Only HIGH tier signals (≥85%) are sent to Telegram")
        return False
    
    # Load previous state
    state = load_state()
    last = state.get(key)
    
    now = datetime.now(timezone.utc)
    
    # If we have previous signal for this pair
    if last:
        try:
            last_time = datetime.fromisoformat(last["last_sent"])
            time_diff = now - last_time
            
            # R3: Check 24h window
            if time_diff < timedelta(hours=24):
                # R2: Check if signal is essentially the same
                if (last["direction"] == direction and 
                    last["entry"] == entry):
                    print(f"❌ R2: Duplicate signal (same direction + entry)")
                    print(f"   Last sent: {time_diff.seconds // 3600}h ago")
                    return False
                else:
                    print(f"✅ R2: Signal changed (direction or entry different)")
            else:
                print(f"✅ R3: 24h window passed ({time_diff.days} days ago)")
        except Exception as e:
            print(f"⚠️ Error parsing last state: {e}")
    
    # Update state
    state[key] = {
        "last_sent": now.isoformat(),
        "direction": direction,
        "entry": entry,
        "confidence": confidence
    }
    
    save_state(state)
    
    # R5: Log decision
    print(f"✅ DISPATCH APPROVED: {asset} {direction} @ {confidence}%")
    return True


def get_dispatch_stats() -> Dict:
    """Get statistics about sent signals"""
    state = load_state()
    return {
        "total_signals": len(state),
        "pairs": list(state.keys()),
        "state": state
    }


def reset_state() -> None:
    """Reset dispatch state (use with caution)"""
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        print("✅ Dispatch state reset")
