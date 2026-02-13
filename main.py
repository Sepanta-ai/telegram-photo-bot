import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- بخش وب‌سرور برای زنده نگه داشتن ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

    def do_HEAD(self): # اضافه شده برای رفع خطای 501 در لاگ
        self.send_response(200)
        self.end_headers()

def run_web():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# --- بخش اصلی ربات تلگرام ---
TOKEN = os.getenv("TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 📸 عکس خود را بفرستید تا برای پشتیبانی ارسال شود.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # این متد پیام را دقیقا با همان کپشن و حالت فوروارد ارسال می‌کند
    if update.message:
        await update.message.forward(chat_id=GROUP_CHAT_ID)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    app.run_polling()
