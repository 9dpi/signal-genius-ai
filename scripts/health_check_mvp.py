
import requests
import json
import os
from datetime import datetime

def check_system():
    results = {
        "api": {"status": "unknown", "url": "https://signalgeniusai-production.up.railway.app"},
        "latest_signal": {"status": "unknown"},
        "history": {"status": "unknown"},
        "stats": {"status": "unknown"}
    }

    base_url = results["api"]["url"]

    # 1. Health Check
    try:
        r = requests.get(f"{base_url}/health", timeout=5)
        results["api"]["status"] = "online" if r.status_code == 200 else f"error ({r.status_code})"
    except Exception as e:
        results["api"]["status"] = f"offline ({str(e)})"

    # 2. Latest Signal
    try:
        r = requests.get(f"{base_url}/api/v1/signal/latest", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "ok":
                results["latest_signal"]["status"] = "working"
                results["latest_signal"]["data"] = {
                    "symbol": data["payload"].get("symbol"),
                    "confidence": data["payload"].get("confidence"),
                    "direction": data["payload"].get("direction"),
                    "source": data["payload"].get("source")
                }
            else:
                results["latest_signal"]["status"] = "api_error"
        else:
            results["latest_signal"]["status"] = f"http_error ({r.status_code})"
    except Exception as e:
        results["latest_signal"]["status"] = f"failed ({str(e)})"

    # 3. History
    try:
        r = requests.get(f"{base_url}/api/v1/signals/history", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "ok":
                results["history"]["status"] = "working"
                results["history"]["count"] = len(data.get("signals", []))
            else:
                results["history"]["status"] = "api_error"
        else:
            results["history"]["status"] = f"http_error ({r.status_code})"
    except Exception as e:
        results["history"]["status"] = f"failed ({str(e)})"

    # 4. Stats
    try:
        r = requests.get(f"{base_url}/api/v1/stats", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "ok":
                results["stats"]["status"] = "working"
                results["stats"]["data"] = data.get("stats")
            else:
                results["stats"]["status"] = "api_error"
        else:
            results["stats"]["status"] = f"http_error ({r.status_code})"
    except Exception as e:
        results["stats"]["status"] = f"failed ({str(e)})"

    return results

if __name__ == "__main__":
    print("🚀 QUANTIX MVP SYSTEM HEALTH CHECK")
    print("="*40)
    report = check_system()
    
    print(f"📡 API Status: {report['api']['status']}")
    
    ls = report['latest_signal']
    print(f"📊 Latest Signal: {ls['status']}")
    if 'data' in ls:
        d = ls['data']
        print(f"   - {d['symbol']} {d['direction']} (Conf: {d['confidence']}%) [Src: {d['source']}]")
        
    hist = report['history']
    print(f"📂 Signal History: {hist['status']} ({hist.get('count', 0)} entries)")
    
    st = report['stats']
    print(f"📈 Performance Stats: {st['status']}")
    if 'data' in st:
        d = st['data']
        print(f"   - Win Rate: {d.get('win_rate')}%")
        print(f"   - Total Signals: {d.get('total_signals')}")
        print(f"   - Avg Confidence: {d.get('avg_confidence')}%")

    print("="*40)
    print("✅ Check Completed")
