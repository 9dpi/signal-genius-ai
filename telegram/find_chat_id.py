import asyncio
import aiohttp
import sys

async def get_chat_id(token):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if not data.get("ok"):
                print(f"❌ Error: {data.get('description')}")
                return None
            
            results = data.get("result", [])
            if not results:
                print("⚠️ No updates found. Please send a message to the bot first!")
                return None
            
            # Get the latest chat ID
            latest_chat = results[-1]
            chat_id = None
            if "message" in latest_chat:
                chat_id = latest_chat["message"]["chat"]["id"]
            elif "my_chat_member" in latest_chat:
                chat_id = latest_chat["my_chat_member"]["chat"]["id"]
            
            if chat_id:
                print(f"✅ Found Chat ID: {chat_id}")
                return chat_id
            else:
                print("❌ Could not determine Chat ID from updates.")
                return None

if __name__ == "__main__":
    TOKEN = "8371104272:AAFlp0NA8wz-HEKOqtsbyGR1_m8C3pzZO2c"
    asyncio.run(get_chat_id(TOKEN))
