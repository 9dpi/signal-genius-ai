from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from signal import get_latest_signal
from telegram import send_telegram_alert
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/signal/latest")
def latest():
    return get_latest_signal()

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """
    Handles incoming messages from Telegram via Webhook.
    """
    data = await request.json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text.startswith("/start") or text.startswith("/help"):
            welcome_msg = (
                "🚀 *Signal Genius AI Bot v1.1*\n\n"
                "Welcome trader! I am synced with the Web Dashboard.\n\n"
                "Commands:\n"
                "/signal - Get the latest AI signal\n"
                "/dashboard - Web link"
            )
            send_simple_message(chat_id, welcome_msg)
            
        elif text.startswith("/signal"):
            signal_data = get_latest_signal()
            send_telegram_alert(signal_data, override_chat_id=chat_id)
            
    return {"status": "ok"}

def send_simple_message(chat_id, text):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token: return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id, 
        "text": text,
        "parse_mode": "Markdown"
    })
