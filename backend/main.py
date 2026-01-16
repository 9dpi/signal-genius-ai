import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from external_client import fetch_candles
    from signal_engine import generate_signal, generate_stabilizer_signal
    from signal_ledger import append_signal, calculate_stats, get_all_signals
except ImportError:
    from backend.external_client import fetch_candles
    from backend.signal_engine import generate_signal, generate_stabilizer_signal
    from backend.signal_ledger import append_signal, calculate_stats, get_all_signals

app = FastAPI(title="Signal Genius AI MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/signal/latest")
async def latest_signal():
    try:
        # 1. Try Real Fetch
        candles = await fetch_candles()
        signal = generate_signal(candles)
        
        # 2. Log to immutable ledger
        append_signal(signal)
        
        return {
            "status": "ok",
            "payload": signal
        }
        
    except Exception as e:
        print(f"⚠️ Error fetching/generating signal: {e}")
        
        # 3. EMERGENCY FALLBACK
        fallback_price = 1.0850 
        fallback_signal = generate_stabilizer_signal(
            fallback_price, 
            direction="BUY", 
            reason="Emergency Fallback"
        )
        
        # Log fallback too
        append_signal(fallback_signal)
        
        return {
            "status": "ok",
            "payload": fallback_signal
        }


@app.get("/api/v1/stats")
def get_stats():
    """
    Get performance statistics.
    
    Returns:
        - Total signals
        - Average confidence
        - Breakdown by tier
    """
    stats = calculate_stats()
    return {
        "status": "ok",
        "stats": stats
    }


@app.get("/api/v1/signals/history")
def get_history(limit: int = 50):
    """
    Get signal history (most recent first).
    
    Args:
        limit: Number of signals to return (max 100)
    """
    limit = min(limit, 100)
    signals = get_all_signals(limit=limit)
    
    return {
        "status": "ok",
        "count": len(signals),
        "signals": signals
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
