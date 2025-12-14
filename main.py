from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

from woocommerce import fetch_products
from normalize import normalize_query

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Type a club or player name.\nExample: barcelona, real madrid, messi"
    )

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = normalize_query(update.message.text)
    products = fetch_products(query)

    if not products:
        await update.message.reply_text("No products found.")
        return

    for product in products:
        title = product["name"]
        price = product["price"]
        image = product["images"][0]["src"] if product["images"] else None
        checkout_url = product["permalink"]

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Get Checkout Link", callback_data=checkout_url)]
        ])

        if image:
            await update.message.reply_photo(
                photo=image,
                caption=f"{title}\n₹{price}",
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text(
                f"{title}\n₹{price}",
                reply_markup=keyboard
            )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"Checkout link:\n{query.data}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
    app.add_handler(CallbackQueryHandler(button_click))

    app.run_polling()

if __name__ == "__main__":
    main()
