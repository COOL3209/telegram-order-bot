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
        result = cursor.fetchone()
        if result:
            driver, location, status = result
            reply = (
                f"📦 訂單號碼：{order_no}\n"
                f"🚛 司機：{driver}\n"
                f"📍 目前位置：{location}\n"
                f"📈 狀態：{status}\n"
                f"💡 南亞成品處 榮幸為您服務"
            )
        else:
            reply = f"❌ 查無訂單號碼：{order_no}"
        cursor.close()
        conn.close()
    except Exception as e:
        reply = f"❗ 發生錯誤：{e}"
    update.message.reply_text(reply)

def welcome_message(update: Update, context: CallbackContext):
    update.message.reply_text("🙋‍♂️ 南亞成品處訂單小幫手！\n很高興為您服務！\n請輸入訂單號碼來查詢物流資訊～")

def main():
    bot = Bot(token=BOT_TOKEN)
    updater = Updater(bot=bot, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.command, welcome_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_order_query))

    print("🤖 Bot 已啟動")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()