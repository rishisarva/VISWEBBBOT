import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN missing")

# -----------------------
# Flask app (Render needs this)
# -----------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# -----------------------
# Telegram bot logic
# -----------------------
async def start(update, context):
    await update.message.reply_text("Bot is live ✅")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
