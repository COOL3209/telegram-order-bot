import os
import pyodbc
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# SQL Server 連線字串
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=172.24.9.54;"
    "DATABASE=MLTransport;"
    "UID=ML;"
    "PWD=Ml022640"
)

def handle_order_query(update: Update, context: CallbackContext):
    order_no = update.message.text.strip()
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT AssignDriver, Last_Location, STATE FROM Transport WHERE ODNO = ?", order_no)
        row = cursor.fetchone()
        if row:
            driver, location, state = row
            reply = (
                f"📦 訂單號碼：{order_no}
"
                f"🚛 司機：{driver}
"
                f"📍 目前位置：{location}
"
                f"📈 狀態：{state}

"
                f"南亞成品處 榮幸為您服務"
            )
        else:
            reply = f"❌ 查無訂單號碼：{order_no}"
        cursor.close()
        conn.close()
    except Exception as e:
        reply = f"❗ 發生錯誤：{e}"
    update.message.reply_text(reply)

def main():
    bot = Bot(token=BOT_TOKEN)
    updater = Updater(bot=bot, use_context=True)
    dp = updater.dispatcher

    # 初始歡迎訊息
    def welcome(update: Update, context: CallbackContext):
        update.message.reply_text("Hi~歡迎你~有訂單想要查詢嗎?")

    dp.add_handler(MessageHandler(Filters.command, welcome))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_order_query))

    print("🤖 Bot 已啟動")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()