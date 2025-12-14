import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update: Update, context):
    update.message.reply_text(
        "Bot is running ✅\nSend a club or player name (e.g. Barcelona, Ronaldo)"
    )

def echo(update: Update, context):
    text = update.message.text.lower()
    update.message.reply_text(f"You searched for: {text}")

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
