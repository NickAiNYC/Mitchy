"""
Community Telegram Bot (stub for manager networking)
- Enables group networking among property managers
- Can be extended for VR/AR event invites
"""

import telebot
import os

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
GROUP_LINK = "https://t.me/joinchat/xxxx"

bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=['start','help'])
def welcome(message):
    bot.reply_to(message, f"Welcome! Join the ML Manager networking group: {GROUP_LINK}")

def start():
    bot.polling()

if __name__ == "__main__":
    start()
