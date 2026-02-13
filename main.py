import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from datetime import datetime

# --- بخش وب‌سرور ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_web():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# --- متغیرهای اصلی ---
TOKEN = os.getenv("TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

# دیکشنری برای ذخیره تعداد عکس‌های ارسالی هر کاربر
# ساختار: { user_id: {"count": 0, "last_date": "2023-10-27"} }
user_usage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام لطفا عکس خود به همراه متن خواسته شده را ارسال کنید تا برای پشتیبانی ارسال شود")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    today = datetime.now().strftime("%Y-%m-%d")

    # بررسی و ریست کردن شمارنده اگر روز عوض شده باشد
    if user_id not in user_usage or user_usage[user_id]["last_date"] != today:
        user_usage[user_id] = {"count": 0, "last_date": today}

    # چک کردن سقف ۳۰ عکس
    if user_usage[user_id]["count"] >= 30:
        await update.message.reply_text("🚫 شما به سقف مجاز ۳۰ عکس در روز رسیده‌اید. لطفاً فردا تلاش کنید.")
        return

    # اگر مجاز بود، فوروارد کن و یکی به شمارنده اضافه کن
    if update.message:
        await update.message.forward(chat_id=GROUP_CHAT_ID)
        user_usage[user_id]["count"] += 1

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    app.run_polling()
