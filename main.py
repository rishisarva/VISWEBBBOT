# main.py
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from woo import fetch_products
from normalize import normalize_query

BOT_TOKEN = os.getenv("BOT_TOKEN")
WC_KEY = os.getenv("WC_KEY")
WC_SECRET = os.getenv("WC_SECRET")
WC_URL = os.getenv("WC_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Type a club name (example: Barcelona, Man Utd, Real Madrid)"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_raw = update.message.text
    query = normalize_query(query_raw)

    products = fetch_products(query, WC_URL, WC_KEY, WC_SECRET)

    if not products:
        await update.message.reply_text("No products found.")
        return

    for p in products:
        title = p["name"]
        price = p["price"]
        image = p["images"][0]["src"] if p["images"] else None
        checkout = p["permalink"]

        sizes = []
        for attr in p["attributes"]:
            if attr["name"].lower() == "size":
                sizes = attr["options"]

        text = f"""👕 {title}
💰 ₹{price}
📏 Sizes: {", ".join(sizes) if sizes else "Check on site"}"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Get Checkout Link", url=checkout)]
        ])

        if image:
            await update.message.reply_photo(photo=image, caption=text, reply_markup=keyboard)
        else:
            await update.message.reply_text(text, reply_markup=keyboard)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.run_polling()

if __name__ == "__main__":
    main()
