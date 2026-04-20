import os
import time
import schedule
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

WATCHLIST = ["AAPL", "TSLA", "NVDA", "AMZN", "META"]

def analyze_stock(ticker):
    data = yf.download(ticker, period="10d", interval="1h")

    if data.empty:
        return None

    close = data["Close"]

    rsi = RSIIndicator(close).rsi().iloc[-1]
    ema = EMAIndicator(close, window=20).ema_indicator().iloc[-1]
    price = close.iloc[-1]

    if rsi < 30 and price > ema:
        return f"""
🚨 {ticker} → BUY

Entry: {round(price,2)}
Stop: {round(price*0.97,2)}
Target: {round(price*1.05,2)}
RSI: {round(rsi,1)}
"""
    return None

def send_signals():
    sent = False

    for stock in WATCHLIST:
        signal = analyze_stock(stock)
        if signal:
            bot.send_message(chat_id=CHAT_ID, text=signal)
            sent = True

    if not sent:
        bot.send_message(chat_id=CHAT_ID, text="Нет сильных сигналов")

schedule.every(10).minutes.do(send_signals)

print("Bot started...")

while True:
    schedule.run_pending()
    time.sleep(10)
