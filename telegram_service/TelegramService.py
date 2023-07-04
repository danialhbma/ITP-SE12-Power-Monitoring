import asyncio
import telegram
import os 
from dotenv import load_dotenv
import sys

class TelegramService:
    def __init__(self, TELEGRAM_API_TOKEN, CHAT_ID):
        self.api_token = TELEGRAM_API_TOKEN
        self.chat_id = CHAT_ID

    async def send_telegram_message(self, message):
        bot = telegram.Bot(token=self.api_token)
        await bot.send_message(chat_id=self.chat_id, text=message)

async def main():
    load_dotenv()
    try:
        TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")
        if not TELEGRAM_API_TOKEN:
            raise ValueError("TELEGRAM_API_TOKEN environment variable is missing")
        if not CHAT_ID:
            raise ValueError("CHAT_ID environment variable is missing")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    tele_client = TelegramService(TELEGRAM_API_TOKEN, CHAT_ID)
    await tele_client.send_telegram_message("Hello World")

if __name__ == "__main__":
    asyncio.run(main())