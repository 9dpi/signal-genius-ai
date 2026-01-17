import httpx
import os
from dotenv import load_dotenv

load_dotenv()

TWELVE_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com"

# Validate API key on module load
if not TWELVE_API_KEY:
    print("⚠️ WARNING: TWELVE_DATA_API_KEY not set in environment!")
    print("   Bot will use fallback signals only.")
else:
    print(f"✅ TwelveData API Key loaded: {TWELVE_API_KEY[:10]}...")

async def fetch_candles(symbol="EUR/USD", interval="15min", limit=50):
    """
    Fetch candle data from Twelve Data API.
    
    Raises:
        ValueError: If API key is missing or API returns error
    """
    if not TWELVE_API_KEY:
        raise ValueError("TWELVE_DATA_API_KEY not configured in environment variables")
    
    url = f"{BASE_URL}/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": limit,
        "apikey": TWELVE_API_KEY
    }

    print(f"📡 Fetching {symbol} data from TwelveData...")
    
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()

    # Check for API errors
    if "code" in data or "status" in data:
        if data.get("code") == 400 or data.get("status") == "error":
            error_msg = data.get("message", "Unknown API error")
            print(f"❌ TwelveData API Error: {error_msg}")
            raise ValueError(f"TwelveData API: {error_msg}")
    
    if "values" not in data:
        error_msg = data.get("message", "Invalid candle data from Twelve Data")
        print(f"❌ Invalid response: {error_msg}")
        raise ValueError(error_msg)

    print(f"✅ Received {len(data['values'])} candles")
    
    # newest → oldest → reverse to get chronological order (oldest to newest)
    return list(reversed(data["values"]))
