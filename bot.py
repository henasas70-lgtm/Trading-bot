from telegram import Bot
import os

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))

bot.send_message(chat_id=os.getenv("CHAT_ID"), text="ТЕСТ 🚀")
