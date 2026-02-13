import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

def run_web():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()

threading.Thread(target=run_web).start()

TOKEN = os.getenv("TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # این دستور کل پیام شامل عکس و کپشن را عیناً فوروارد می‌کند
    await update.message.forward(chat_id=GROUP_CHAT_ID)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
