"""
Signal Ledger - Immutable Signal History
Append-only log for transparency and accountability
"""
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional


LEDGER_FILE = "signals_ledger.json"


def append_signal(signal_data: Dict) -> bool:
    """
    Append signal to immutable ledger.
    
    Rules:
    - Append only (no updates, no deletes)
    - Each signal gets one entry
    - Timestamp is immutable
    
    Args:
        signal_data: Full signal payload
        
    Returns:
        bool: True if appended successfully
    """
    try:
        # Load existing ledger
        ledger = load_ledger()
        
        # Extract essential fields for ledger
        ledger_entry = {
            "signal_id": signal_data.get("signal_id"),
            "created_at": signal_data.get("generated_at"),
            "symbol": signal_data.get("symbol") or signal_data.get("asset"),
            "direction": signal_data.get("direction"),
            "entry": signal_data.get("entry"),
            "tp": signal_data.get("tp"),
            "sl": signal_data.get("sl"),
            "confidence": signal_data.get("confidence"),
            "timeframe": signal_data.get("timeframe"),
            "strategy": signal_data.get("strategy"),
            "status": signal_data.get("status", "ACTIVE"),
            "source": signal_data.get("source"),
            "logged_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Append to ledger
        ledger.append(ledger_entry)
        
        # Save ledger
        save_ledger(ledger)
        
        print(f"✅ Signal {ledger_entry['signal_id']} logged to ledger")
        return True
        
    except Exception as e:
        print(f"❌ Failed to append to ledger: {e}")
        return False


def update_signal_status(signal_id: str, status: str, outcome_data: Dict = None) -> bool:
    """
    Update the status of an existing signal in the ledger.
    
    Args:
        signal_id: ID of the signal to update
        status: New status (HIT_TP, HIT_SL, EXPIRED)
        outcome_data: Optional dict with pips, closed_at, etc.
        
    Returns:
        bool: True if updated successfully
    """
    try:
        ledger = load_ledger()
        updated = False
        
        for signal in ledger:
            if signal.get("signal_id") == signal_id:
                signal["status"] = status
                signal["closed_at"] = datetime.now(timezone.utc).isoformat()
                if outcome_data:
                    signal.update(outcome_data)
                updated = True
                break
        
        if updated:
            save_ledger(ledger)
            print(f"✅ Signal {signal_id} updated to {status}")
            return True
        else:
            print(f"⚠️ Signal {signal_id} not found in ledger")
            return False
            
    except Exception as e:
        print(f"❌ Failed to update signal: {e}")
        return False


def get_active_signals() -> List[Dict]:
    """Get all signals with status 'ACTIVE'"""
    ledger = load_ledger()
    return [s for s in ledger if s.get("status") == "ACTIVE"]


def load_ledger() -> List[Dict]:
    """Load signal ledger from file"""
    if not os.path.exists(LEDGER_FILE):
        return []
    
    try:
        with open(LEDGER_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading ledger: {e}")
        return []


def save_ledger(ledger: List[Dict]) -> None:
    """Save ledger to file"""
    try:
        with open(LEDGER_FILE, "w") as f:
            json.dump(ledger, f, indent=2)
    except Exception as e:
        print(f"⚠️ Error saving ledger: {e}")


def get_signal_by_id(signal_id: str) -> Optional[Dict]:
    """Retrieve signal from ledger by ID"""
    ledger = load_ledger()
    for signal in ledger:
        if signal.get("signal_id") == signal_id:
            return signal
    return None


def get_all_signals(limit: int = 100) -> List[Dict]:
    """Get all signals (most recent first)"""
    ledger = load_ledger()
    return list(reversed(ledger[-limit:]))


def calculate_stats() -> Dict:
    """
    Calculate performance statistics from ledger.
    
    Returns:
        dict: Performance metrics
    """
    ledger = load_ledger()
    
    if not ledger:
        return {
            "total_signals": 0,
            "win_rate": 0,
            "avg_confidence": 0,
            "by_tier": {}
        }
    
    # Basic stats
    total = len(ledger)
    closed = [s for s in ledger if s.get("status") in ["HIT_TP", "HIT_SL", "EXPIRED"]]
    wins = [s for s in ledger if s.get("status") == "HIT_TP"]
    
    win_rate = (len(wins) / len(closed) * 100) if closed else 0
    
    # Confidence distribution
    confidences = [s.get("confidence", 0) for s in ledger]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    # Tier breakdown
    tiers = {"HIGH": [], "MEDIUM": [], "LOW": []}
    for signal in ledger:
        conf = signal.get("confidence", 0)
        if conf >= 85:
            tiers["HIGH"].append(signal)
        elif conf >= 60:
            tiers["MEDIUM"].append(signal)
        else:
            tiers["LOW"].append(signal)
    
    tier_stats = {}
    for tier, signals in tiers.items():
        tier_signals = signals
        tier_closed = [s for s in tier_signals if s.get("status") in ["HIT_TP", "HIT_SL", "EXPIRED"]]
        tier_wins = [s for s in tier_signals if s.get("status") == "HIT_TP"]
        
        tier_stats[tier] = {
            "count": len(tier_signals),
            "win_rate": round(len(tier_wins) / len(tier_closed) * 100, 1) if tier_closed else 0,
            "avg_confidence": round(sum(s.get("confidence", 0) for s in tier_signals) / len(tier_signals), 1) if tier_signals else 0
        }
    
    return {
        "total_signals": total,
        "total_closed": len(closed),
        "win_rate": round(win_rate, 1),
        "avg_confidence": round(avg_confidence, 1),
        "by_tier": tier_stats,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


def export_ledger_csv(output_file: str = "signals_export.csv") -> bool:
    """Export ledger to CSV for analysis"""
    try:
        import csv
        ledger = load_ledger()
        
        if not ledger:
            print("⚠️ No signals to export")
            return False
        
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=ledger[0].keys())
            writer.writeheader()
            writer.writerows(ledger)
        
        print(f"✅ Exported {len(ledger)} signals to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return False
