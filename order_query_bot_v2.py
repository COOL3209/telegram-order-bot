from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import pyodbc
import os

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
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        sql = "SELECT AssignDriver, Last_Location, STATE FROM Transport WHERE ODNO = ?"
        cursor.execute(sql, order_no)
        result = cursor.fetchone()
        if result:
            driver, location, status = result
            reply = (
                f"📦 訂單號碼：{order_no}\n"
                f"🚛 司機：{driver}\n"
                f"📍 目前位置：{location}\n"
                f"📈 狀態：{status}\n"
                f"🧡 南亞成品處 榮幸為您服務"
            )
        else:
            reply = f"❌ 查無訂單號碼：{order_no}"
        cursor.close()
        conn.close()
    except Exception as e:
        reply = f"❗ 發生錯誤：{e}"
    update.message.reply_text(reply)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_order_query))
    print("🤖 Bot 已啟動")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
