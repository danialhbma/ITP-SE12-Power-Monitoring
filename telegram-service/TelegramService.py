#!/usr/bin/env python3
import asyncio
import telegram

API_TOKEN = "6349105162:AAHztf3T2iIHIb6-NpSgQQZ_8NYcV0TaaWQ"
CHAT_ID = "-935942719"
CHANNEL_ID = "YOUR_CHANNEL_ID"

async def send_telegram_message():
	bot = telegram.Bot(token = API_TOKEN)
	message = "Sent via python test"
	await bot.send_message(chat_id = CHAT_ID, text = message)

if __name__ == "__main__":
	asyncio.run(send_telegram_message())
