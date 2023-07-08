# Telegram Bot Set Up
1. Search for @BotFather in Telegram.
2. Type /newbot in the chat.
3. Follow prompts provided by @BotFather and specify name and username of bot.
4. Copy the API token that @BotFather returns.
5. Add the newly created bot to a group chat or channel.
6. Retrieve the chat / channel ID by:
	a) Send a message to the group chat / channel e.g., Hello
	b) https://api.telegram.org/bot<API_TOKEN>/getUpdates
	c) e.g., https://api.telegram.org/bot634XXXXXXXXXXXXXXXXXXXXXXXXXXWQ/getUpdates
	d) chat id will look something like this: -944799166
	
# Configuring Telegram and Grafana
The Telegram Bot and groups/channels created above can be used as a contact point for Grafana. i.e., Grafana can use them to send alerts. 
Follow the documentation below to add Telegram as a Contact Point and how alerts can be configured.
1. Telegram & Grafana:  https://grafana.com/docs/grafana-cloud/oncall/notify/telegram/
2. Grafana Alerts: https://grafana.com/docs/grafana/latest/alerting/

# Telegram Python Set Up
1. pip install python-telegram-bot.
2. Create and add TELEGRAM_API_TOKEN, CHAT_ID and CHANNEL_ID into .env file.
3. pip install python-dotenv
4. run TelegramService.py, if valid telegran API token, chat and channel ID exists in .env file, a 'hello' will be sent to the group chat.

# System Monitoring Agent
The System Monitoring Agent, is a routine systems check for cpu load, memory (RAM) usage, network traffic and more importantly disk usage. It is scheduled to run at 2359 daily using the CRON expression below.
* 59 23 * * * cd /home/yappi/ITP-SE12-Power-Monitoring/telegram_service && python3 SystemMonitoringAgent.py >> monitoring_reports.txt 2>&1
 
