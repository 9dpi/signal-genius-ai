"""
Signal Ledger - Immutable Signal History
Append-only log for transparency and accountability.
Updated for Signal Lifecycle Schema v1.0
"""
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional


LEDGER_FILE = "signals_ledger.json"


def append_signal(signal_data: Dict) -> bool:
    """
    Append signal to immutable ledger.
    
    Status Lifecycle: CREATED -> OPEN -> (TP_HIT | SL_HIT | EXPIRED)
    """
    try:
        ledger = load_ledger()
        
        # Normalize Entry (Single float)
        entry_val = signal_data.get("entry")
        if isinstance(entry_val, list):
            entry_val = entry_val[0]

        # Extract essential fields according to new schema
        ledger_entry = {
            "signal_id": signal_data.get("signal_id"),
            "symbol": signal_data.get("symbol") or signal_data.get("asset"),
            "timeframe": signal_data.get("timeframe"),
            "direction": signal_data.get("direction"),
            "entry": entry_val,
            "tp": signal_data.get("tp"),
            "sl": signal_data.get("sl"),
            "status": signal_data.get("status_life") or signal_data.get("status", "CREATED"),
            "confidence": signal_data.get("confidence"),
            "strategy": signal_data.get("strategy"),
            "created_at": signal_data.get("generated_at") or datetime.now(timezone.utc).isoformat(),
            "opened_at": None,
            "closed_at": None,
            "result": None,
            "pips": None
        }
        
        # If signal is already 'OPEN' at creation (market execution)
        if ledger_entry["status"] == "OPEN":
            ledger_entry["opened_at"] = ledger_entry["created_at"]
            
        ledger.append(ledger_entry)
        save_ledger(ledger)
        print(f"✅ Signal {ledger_entry['signal_id']} logged to ledger as {ledger_entry['status']}")
        return True
    except Exception as e:
        print(f"❌ Failed to append to ledger: {e}")
        return False


def update_signal_status(signal_id: str, new_status: str, data: Dict = None) -> bool:
    """
    Update the status of an existing signal in the ledger.
    
    Args:
        signal_id: ID of the signal
        new_status: OPEN, TP_HIT, SL_HIT, EXPIRED
        data: Optional closed field updates (result, pips, etc.)
    """
    try:
        ledger = load_ledger()
        updated = False
        now = datetime.now(timezone.utc).isoformat()
        
        for signal in ledger:
            if signal.get("signal_id") == signal_id:
                old_status = signal.get("status")
                
                # Prevent invalid transitions (e.g. from TP_HIT to OPEN)
                if old_status in ["TP_HIT", "SL_HIT", "EXPIRED"]:
                    continue

                signal["status"] = new_status
                
                if new_status == "OPEN":
                    signal["opened_at"] = now
                elif new_status in ["TP_HIT", "SL_HIT", "EXPIRED"]:
                    signal["closed_at"] = now
                    if data:
                        signal.update(data)
                
                updated = True
                break
        
        if updated:
            save_ledger(ledger)
            print(f"✅ Signal {signal_id} transitioned to {new_status}")
            return True
        return False
    except Exception as e:
        print(f"❌ Status update failed: {e}")
        return False


def load_ledger() -> List[Dict]:
    """Load signal ledger from file"""
    if not os.path.exists(LEDGER_FILE):
        return []
    try:
        with open(LEDGER_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_ledger(ledger: List[Dict]) -> None:
    """Save ledger to file"""
    try:
        with open(LEDGER_FILE, "w") as f:
            json.dump(ledger, f, indent=2)
    except Exception as e:
        print(f"⚠️ Error saving ledger: {e}")


def get_all_signals(limit: int = 100) -> List[Dict]:
    """Get all signals (most recent first)"""
    ledger = load_ledger()
    return list(reversed(ledger[-limit:]))


def calculate_stats() -> Dict:
    """
    Performance Stats (Trader-friendly format)
    """
    ledger = load_ledger()
    if not ledger:
        return {"total": 0, "win": 0, "loss": 0, "expired": 0, "win_rate": 0, "avg_pips": 0}
    
    total = len(ledger)
    win = len([s for s in ledger if s.get("status") == "TP_HIT"])
    loss = len([s for s in ledger if s.get("status") == "SL_HIT"])
    expired = len([s for s in ledger if s.get("status") == "EXPIRED"])
    closed_count = win + loss
    
    win_rate = round((win / closed_count * 100), 1) if closed_count > 0 else 0
    
    pips_list = [s.get("pips", 0) for s in ledger if s.get("pips") is not None]
    avg_pips = round(sum(pips_list) / len(pips_list), 1) if pips_list else 0
    
    return {
        "total": total,
        "win": win,
        "loss": loss,
        "expired": expired,
        "win_rate": win_rate,
        "avg_pips": avg_pips
    }

