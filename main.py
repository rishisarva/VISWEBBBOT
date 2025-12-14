from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

from wc_client import fetch_products
from normalize import normalize_query
from search import rank_products, extract_sizes
from cache import get_cached, set_cache

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USERS = list(map(int, os.getenv("ALLOWED_USERS").split(",")))

PRODUCTS = fetch_products()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        return
    await update.message.reply_text("Type club or player name")

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        return

    query = update.message.text
    query_obj = normalize_query(query)

    cache_key = f"{query_obj['type']}:{query_obj['value']}"
    results = get_cached(cache_key)

    if not results:
        results = rank_products(PRODUCTS, query_obj)
        set_cache(cache_key, results)

    results = results[:5]

    for p in results:
        sizes = extract_sizes(p)
        btn = InlineKeyboardButton(
            "Get Checkout Link",
            callback_data=p["permalink"]
        )
        text = f"""🟢 {p['name']}
₹{p['price']}
Sizes: {', '.join(sizes) if sizes else 'N/A'}"""

        await update.message.reply_photo(
            photo=p["images"][0]["src"],
            caption=text,
            reply_markup=InlineKeyboardMarkup([[btn]])
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"Checkout link:\n{query.data}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))
app.add_handler(filters.CallbackQueryHandler(button_handler))

app.run_polling()
