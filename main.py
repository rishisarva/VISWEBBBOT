import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from bot.handlers import start, handle_text

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
