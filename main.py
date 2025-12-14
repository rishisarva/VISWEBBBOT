import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Bot is live ✅\n\nType a club or player name (example: barcelona / ronaldo)"
    )

def echo(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    update.message.reply_text(f"You searched for: {text}")

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN missing")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
