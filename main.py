from tgb import bot
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!"

def start_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000)
