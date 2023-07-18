import asyncio
import telegram
import os 
import sys

class TelegramService:
    def __init__(self, TELEGRAM_API_TOKEN = "", CHAT_ID = ""):
        """
        Initializes a TelegramService object. This TelegramService object will send messages to a telegram chat/channel.

        Args:
            TELEGRAM_API_TOKEN (str): The Telegram API token.
            CHAT_ID (str): The chat ID to sendmessages to.
        """
        self.api_token = TELEGRAM_API_TOKEN
        self.chat_id = CHAT_ID

    def retrieve_token_from_environment(self):
        """
        Retrieves the Telegram API token and chat ID from environment variables.
        Only need to be used if tokens are stored in .env file and token and chat id not passed in constructor.
        """
        from dotenv import load_dotenv
        load_dotenv()
        try:
            TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
            CHAT_ID = os.getenv("CHAT_ID")
            if not TELEGRAM_API_TOKEN:
                raise ValueError("TELEGRAM_API_TOKEN environment variable is missing")
            if not CHAT_ID:
                raise ValueError("CHAT_ID environment variable is missing")
            self.api_token = TELEGRAM_API_TOKEN
            self.chat_id = CHAT_ID
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    async def send_telegram_message(self, message:str):
        """
        Sends a Telegram message.

        Args:
            message (str): The message content.
        """
        bot = telegram.Bot(token=self.api_token)
        await bot.send_message(chat_id=self.chat_id, text=message)

    async def send_pdf(self, pdf_path):
        try:
            bot = telegram.Bot(token=self.api_token)
            with open(pdf_path, 'rb') as file:
                await bot.send_document(chat_id=self.chat_id, document=file)
        except FileNotFoundError as e:
            print(f"Error: File not found - {pdf_path}")
        except Exception as e:
            print(f"Error: {e}")

async def main():
    # Initialize and load tele_client using API keys stored in .env file
    tele_client = TelegramService()
    tele_client.retrieve_token_from_environment()  
    await tele_client.send_telegram_message("Hello World")
    await tele_client.send_pdf("Yap Ping 2101074 Mid Way Reflection.pdf")
    
if __name__ == "__main__":
    asyncio.run(main())