import os
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN missing")

async def start(update, context):
    await update.message.reply_text(
        "Bot is live ✅\nType a club or player name (eg: Barcelona, Ronaldo)"
    )

async def echo(update, context):
    text = update.message.text
    await update.message.reply_text(f"You typed: {text}")

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
