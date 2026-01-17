
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from signal_ledger import calculate_stats, get_all_signals

def test():
    print("🧪 Testing Local Signal Ledger Logic...")
    stats = calculate_stats()
    print(f"Stats: {stats}")
    
    signals = get_all_signals(limit=5)
    print(f"Total signals in ledger: {len(signals)}")
    for s in signals:
        print(f"  [{s['status']}] {s['symbol']} {s['direction']} | Pips: {s.get('pips')}")

if __name__ == "__main__":
    test()
