from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os

from wc import fetch_products
from normalize import group_by_club

BOT_TOKEN = os.getenv("BOT_TOKEN")

PRODUCT_CACHE = {}
CLUB_CACHE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Type a club name (example: barcelona, man utd, real madrid)"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if not CLUB_CACHE:
        products = fetch_products()
        grouped = group_by_club(products)
        CLUB_CACHE.update(grouped)

    matches = []
    for club, items in CLUB_CACHE.items():
        if text in club:
            matches = items[:5]
            break

    if not matches:
        await update.message.reply_text("No matching products found.")
        return

    for p in matches:
        sizes = []
        for attr in p["attributes"]:
            if attr["name"].lower() == "size":
                sizes = attr["options"]

        caption = (
            f"*{p['name']}*\n"
            f"Price: ₹{p['price']}\n"
            f"Sizes: {', '.join(sizes) if sizes else 'N/A'}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Get Checkout Link",
                    callback_data=f"buy|{p['permalink']}"
                )
            ]
        ])

        await update.message.reply_photo(
            photo=p["images"][0]["src"],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, link = query.data.split("|", 1)

    if action == "buy":
        await query.message.reply_text(f"Checkout link:\n{link}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
