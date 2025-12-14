from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from woocommerce import get_products
from search import search_products

products_cache = get_products()

async def club(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    results = search_products(products_cache, query)

    if not results:
        await update.message.reply_text("❌ No products found")
        return

    for p in results:
        sizes = []
        for attr in p["attributes"]:
            if attr["name"].lower() == "size":
                sizes = attr["options"]

        buttons = [
            [InlineKeyboardButton("🛒 Get Checkout Link", callback_data=f"buy_{p['id']}")],
            [InlineKeyboardButton("➕ Show More", callback_data=f"more_{query}")]
        ]

        await update.message.reply_photo(
            photo=p["images"][0]["src"],
            caption=(
                f"🏷 {p['name']}\n"
                f"💰 ₹{p['price']}\n"
                f"📏 Sizes: {', '.join(sizes) if sizes else 'Check site'}"
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data
    await update.callback_query.answer()

    if query.startswith("buy_"):
        pid = query.replace("buy_", "")
        link = f"https://visionsjersey.com/?add-to-cart={pid}"
        await update.callback_query.message.reply_text(f"🛒 Checkout link:\n{link}")

    if query.startswith("more_"):
        term = query.replace("more_", "")
        context.args = term.split()
        await club(update.callback_query.message, context)

app = ApplicationBuilder().token(
    __import__("os").getenv("TELEGRAM_BOT_TOKEN")
).build()

app.add_handler(CommandHandler("club", club))
app.add_handler(CommandHandler("player", club))
app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Use /club or /player")))

app.add_handler(
    __import__("telegram.ext").CallbackQueryHandler(button_handler)
)

app.run_polling()
