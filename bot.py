from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

from flask import Flask
from threading import Thread
import os

# Render uchun web server
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot ishlayapti ✅"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()

import os
print("BOT_TOKEN :", os.getenv("BOT_TOKEN"))
print("ADMIN_ID :", os.getenv("ADMIN_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

reply_map = {}

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id == ADMIN_ID:
        return

    username = f"@{user.username}" if user.username else "Username yo'q"

    text = f"""
📩 Yangi xabar

👤 Ism: {user.first_name}
🔗 Username: {username}
🆔 ID: {user.id}

✉️ Xabar:
{update.message.text}
"""

    sent = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )

    reply_map[sent.message_id] = user.id

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        msg_id = update.message.reply_to_message.message_id

        if msg_id in reply_map:
            user_id = reply_map[msg_id]

            await context.bot.send_message(
                chat_id=user_id,
                text=f"📨 Javob:\n\n{update.message.text}"
            )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.User(ADMIN_ID), user_message)
)

app.add_handler(
    MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_reply)
)

print("Bot ishga tushdi ✅")

app.run_polling()
