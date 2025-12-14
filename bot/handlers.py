from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send a club or player name (e.g. Barcelona, Ronaldo)"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()
    await update.message.reply_text(f"Searching for: {query}")
